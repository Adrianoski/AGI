"""
benchmark.py — Confronto RAG standard vs SLM-routed retrieval.

Metriche:
  - Latenza media (ms) per query
  - Dimensione del pool di ricerca (n. chunk esaminati)
  - Overlap@5 tra i due sistemi (per stimare la qualità relativa)

Uso:
    python3 benchmark.py
"""

import time
import json
import re
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi
import chromadb

from router import load_registry, find_top_n_slms

# ── Config ─────────────────────────────────────────────────────────────
TOP_N_SLMS        = 3
TOP_K             = 5
RRF_K             = 60
COLLECTION        = None                  # None = usa la prima collection disponibile
GENERATION_MODEL  = "Qwen/Qwen3.5-4B"    # modello HuggingFace per la generazione
MAX_NEW_TOKENS    = 256
OUTPUT_FILE       = "benchmark_answers_keybert.md"

# (query_en, query_it_for_bm25, expected_keywords_in_answer, ground_truth)
QUERIES = [
    # ── ORIGINAL 10 ──────────────────────────────────────────────────────────
    (
        "Who imported spices into Europe during the Middle Ages?",
        "da chi venivano importate le spezie in europa nel medioevo?",
        ["arabi", "veneziana", "mercanti", "spezie", "oriente", "monopolio"],
        (
            "Il commercio delle spezie era controllato dai mercanti arabi insieme alla "
            "repubblica veneziana, che detenevano il monopolio attraversando i territori "
            "musulmani. I molteplici rischi del viaggio e i vari passaggi di mano "
            "aumentavano considerevolmente il prezzo della merce."
        ),
    ),
    (
        "What territories did Charles V control?",
        "quali territori controllava Carlo V?",
        ["carlo", "spagna", "impero", "asburgo", "fiandre", "napoli"],
        (
            "Carlo V controllava un vasto impero che comprendeva la Spagna, i territori "
            "asburgici, le Fiandre, il Regno di Napoli e le colonie americane. Il suo "
            "regno fu segnato da conflitti con la Francia, i principi tedeschi luterani "
            "e l'impero ottomano."
        ),
    ),
    (
        "What were the main causes of the French Revolution?",
        "quali furono le cause della rivoluzione francese?",
        ["crisi", "stato", "terzo", "nobiltà", "tasse", "assemblea"],
        (
            "Le principali cause della Rivoluzione Francese furono la crisi economica "
            "dell'Ancien Régime, le ingiustizie fiscali che gravavano sul terzo stato, "
            "la convocazione degli Stati Generali e la crescente influenza dell'opinione "
            "pubblica. La nobiltà e il clero godevano di privilegi fiscali che "
            "alimentavano il malcontento popolare."
        ),
    ),
    (
        "How did James Watt's steam engine work?",
        "come funzionava la macchina a vapore di james watt?",
        ["vapore", "watt", "carbone", "industria", "energia", "tessitura"],
        (
            "James Watt impiegò la macchina a vapore nella tessitura, nell'estrazione "
            "dei minerali e nella loro lavorazione (siderurgia). Il vapore veniva "
            "prodotto grazie all'utilizzo del carbone, per cui le attività industriali "
            "dovevano svilupparsi vicino alle miniere."
        ),
    ),
    (
        "What were the key principles of the Enlightenment?",
        "quali erano i principi fondamentali dell'illuminismo?",
        ["ragione", "philosophes", "libertà", "progresso", "lume", "diritti"],
        (
            "L'Illuminismo si fondava sul primato del 'lume naturale' della ragione come "
            "strumento di conoscenza e critica della realtà. I philosophes propugnavano "
            "una nuova visione dell'economia e della politica basata sulla libertà, sul "
            "progresso e sui diritti naturali dell'individuo."
        ),
    ),
    (
        "What was the American Revolution?",
        "che cosa fu la rivoluzione americana?",
        ["colonie", "indipendenza", "inglesi", "america", "tasse", "dichiarazione"],
        (
            "La Rivoluzione Americana fu il processo con cui le tredici colonie "
            "americane si ribellarono al dominio inglese, principalmente a causa delle "
            "difficili condizioni economiche e fiscali imposte dalla madrepatria. Nel "
            "1776 fu stilata la Dichiarazione d'Indipendenza; la sconfitta inglese fu "
            "sancita dalla pace di Parigi del 1783, che diede vita al nuovo stato "
            "federale americano."
        ),
    ),
    (
        "Who were the Mongols and how did they expand?",
        "chi erano i mongoli e come si espansero?",
        ["mongoli", "gengis", "khan", "asia", "impero", "tartari"],
        (
            "I Mongoli erano un popolo di cavalieri guidati da Gengis Khan, che scatenò "
            "la sua offensiva verso la Cina oltrepassando la Grande Muraglia, poi occupò "
            "le steppe della Russia meridionale, conquistò Samarcanda e Bukara e attaccò "
            "Persia, Georgia e Bulgaria. Erano chiamati Tartari dagli europei. Dopo la "
            "sua morte il regno fu diviso tra i quattro figli, dando origine a quattro Khanati."
        ),
    ),
    (
        "What was Luther's Protestant Reformation?",
        "che cosa fu la riforma protestante di lutero?",
        ["lutero", "chiesa", "bibbia", "riforma", "fede", "protestante"],
        (
            "La Riforma protestante di Lutero segnò una rottura definitiva con la "
            "dottrina cattolica, ribadita nella Confessione Augustana presentata da "
            "Filippo Melantone alla Dieta di Augusta del 1530. La pace di Augusta del "
            "1555 riconobbe ufficialmente la religione protestante stabilendo il "
            "principio 'cuius regio eius religio'."
        ),
    ),
    (
        "How was the Italian state formed during the Risorgimento?",
        "come si formò lo stato italiano nel risorgimento?",
        ["cavour", "garibaldi", "mazzini", "unità", "piemonte", "italia"],
        (
            "L'unità d'Italia fu il risultato del Risorgimento, guidato da figure come "
            "Mazzini (fondatore della Giovine Italia), Cavour (che condusse la politica "
            "diplomatica e la Seconda guerra d'Indipendenza) e Garibaldi (che guidò la "
            "Spedizione dei Mille). Il Piemonte fu il fulcro del processo unitario."
        ),
    ),
    (
        "What were the social consequences of the Industrial Revolution?",
        "quali furono le conseguenze sociali della rivoluzione industriale?",
        ["operai", "fabbriche", "lavoro", "proletariato", "borghesia", "sfruttamento"],
        (
            "La Rivoluzione Industriale determinò la nascita del proletariato operaio, "
            "che lavorava in fabbriche in condizioni di sfruttamento. Si accentuò la "
            "divisione tra borghesia proprietaria e classe operaia. Gli effetti negativi "
            "dell'industrializzazione includevano orari di lavoro estenuanti e condizioni "
            "igieniche precarie."
        ),
    ),

    # ── NUOVE 30 ─────────────────────────────────────────────────────────────
    (
        "How did the population of Europe change from the year 1000 to the 14th century?",
        "come cambiò la popolazione europea dall'anno Mille al Trecento?",
        ["popolazione", "raddoppiando", "40 milioni", "80 milioni", "carestie", "disboscare"],
        (
            "La popolazione europea aumentò dall'anno Mille fino all'inizio del Trecento, "
            "raddoppiando da circa 40 milioni a circa 80 milioni di abitanti. Questo "
            "comportò la necessità di disboscare nuovi terreni per aumentare la "
            "produzione, anche se si verificarono ciclicamente carestie decennali che "
            "causarono migliaia di vittime."
        ),
    ),
    (
        "How did the plague spread from Crimea to Europe?",
        "come si diffuse la peste dalla Crimea all'Europa?",
        ["crimea", "genovesi", "catapulte", "cadaveri", "genova", "venezia", "sicilia"],
        (
            "La prima epidemia di peste scoppiò in una colonia genovese in Crimea "
            "assediata dai Tartari, che lanciarono con le catapulte cadaveri infettati "
            "oltre le mura. I cittadini genovesi in fuga portarono il contagio via mare. "
            "Intorno al 1347 la peste raggiunse Genova, Venezia e la Sicilia, dilagando "
            "l'anno successivo in Toscana, Francia, Inghilterra, Spagna e Germania. "
            "Nel 1353 aveva ucciso circa un terzo della popolazione europea."
        ),
    ),
    (
        "What is the difference between bubonic plague and pneumonic plague?",
        "qual è la differenza tra peste bubbonica e peste polmonare?",
        ["bubbonica", "bubboni", "tumefazioni", "polmonare", "emorragie", "chiazze"],
        (
            "La peste bubbonica si presentava sotto forma di tumefazioni chiamate "
            "bubboni. La peste polmonare, detta anche peste nera, provocava invece "
            "emorragie cutanee che, rapprendosi, formavano chiazze nere sulla pelle."
        ),
    ),
    (
        "How was the plague transmitted from animals to humans?",
        "come veniva trasmessa la peste dagli animali all'uomo?",
        ["pulce", "ratti", "bacillo", "sangue", "topi", "igieniche", "promiscuità"],
        (
            "Il bacillo della peste era presente nei ratti. Era la pulce che, succhiando "
            "il sangue dei topi infetti, trasmetteva la malattia agli esseri umani. "
            "Le cattive condizioni igieniche e la promiscuità in cui vivevano gli esseri "
            "umani aumentavano ulteriormente la contaminazione."
        ),
    ),
    (
        "Who were blamed for spreading the plague and what happened to them?",
        "chi fu accusato di diffondere la peste e cosa accadde?",
        ["ebrei", "pogrom", "pozzi", "capro espiatorio", "emarginati", "lebbrosi"],
        (
            "Come capri espiatori furono indicati emarginati, lebbrosi e soprattutto "
            "gli Ebrei, accusati di avvelenare l'acqua dei pozzi o di contaminare "
            "l'aria con veleni. Di conseguenza migliaia di ebrei subirono persecuzioni "
            "— i pogrom — in Francia, Germania e Svizzera."
        ),
    ),
    (
        "Who was Joan of Arc and what role did she play in the Hundred Years' War?",
        "chi era Giovanna d'Arco e quale ruolo ebbe nella Guerra dei Cent'anni?",
        ["giovanna", "orléans", "voci", "carlo vii", "rouen", "rogo", "diciannove"],
        (
            "Giovanna d'Arco era una giovane contadina analfabeta della Champagne che "
            "affermava di sentire voci attribuite all'Arcangelo Michele. Presentatasi "
            "a Carlo VII, guidò l'esercito alla conquista di Orléans e il re fu "
            "incoronato a Reims. Fu catturata dagli inglesi e condannata al rogo per "
            "eresia a soli diciannove anni nella piazza di Rouen."
        ),
    ),
    (
        "When did the Hundred Years' War start and end, and what caused it?",
        "quando iniziò e finì la Guerra dei Cent'anni e quale ne fu la causa?",
        ["1337", "1453", "filippo vi", "edoardo", "feudi", "valois"],
        (
            "La Guerra dei Cent'anni durò dal 1337 al 1453 non continuativamente. "
            "Fu scatenata dal tentativo di Filippo VI (Valois) di appropriarsi dei "
            "feudi inglesi sul suolo francese, provocando la reazione di Edoardo III "
            "d'Inghilterra."
        ),
    ),
    (
        "How did Columbus persuade the Spanish monarchs to fund his voyage?",
        "come convinse Colombo i sovrani spagnoli a finanziare il suo viaggio?",
        ["isabella", "ferdinando", "toscanelli", "sferica", "occidente", "crociata"],
        (
            "Dopo il rifiuto del Portogallo, Colombo si rivolse a Isabella di Castiglia "
            "e Ferdinando d'Aragona. I sovrani, appena conclusa la Reconquista, "
            "accettarono attratti dalla possibilità di trovare oro nelle Indie per "
            "finanziare una nuova crociata. Il progetto era basato sulla teoria di "
            "Toscanelli secondo cui la Terra era sferica e si poteva raggiungere "
            "l'oriente navigando verso occidente."
        ),
    ),
    (
        "From which port did Columbus depart and when?",
        "da quale porto partì Colombo e quando?",
        ["palos", "agosto", "1492", "caravelle", "pinta", "nina"],
        (
            "Il 3 agosto 1492 dal porto di Palos partirono tre caravelle: due di piccola "
            "stazza battezzate la Pinta e la Niña, e la nave ammiraglia Santa María."
        ),
    ),
    (
        "Who was Henry the Navigator and what was his contribution to exploration?",
        "chi era Enrico il Navigatore e qual è il suo contributo all'esplorazione?",
        ["enrico il navigatore", "sagres", "caravella", "algarve", "venti", "atlantico"],
        (
            "Enrico il Navigatore era il re del Portogallo che fondò una scuola nautica "
            "nella sua residenza di Capo di Sagres nell'Algarve. Lì si raccoglievano "
            "informazioni su maree, venti e sull'Oceano Atlantico. Favorì la "
            "sostituzione della galera con la più maneggevole caravella e avviò "
            "le esplorazioni portoghesi verso le Azzorre e la circumnavigazione dell'Africa."
        ),
    ),
    (
        "Who was Bartolomeo Díaz and why did he not complete his voyage?",
        "chi era Bartolomeo Diaz e perché non completò il suo viaggio?",
        ["diaz", "buona speranza", "1487", "ammutinamento", "capo", "circumnavigazione"],
        (
            "Bartolomeo Diaz era un ammiraglio portoghese che nel 1487 raggiunse il "
            "Capo di Buona Speranza ma non lo doppiò a causa dell'ammutinamento "
            "dei suoi marinai."
        ),
    ),
    (
        "What was the triangular trade and why was it ethically problematic?",
        "cos'era il commercio triangolare e perché era eticamente problematico?",
        ["triangolare", "schiavi", "africa", "tabacco", "cotone", "tratta"],
        (
            "Il commercio triangolare prevedeva tre tappe: partenza dall'Europa con "
            "armi, alcol e suppellettili; sosta in Africa dove si acquistavano schiavi "
            "sfruttando le rivalità tribali; arrivo in America dove gli schiavi erano "
            "venduti in cambio di tabacco, cotone e canna da zucchero che tornavano "
            "in Europa. Generava enormi ricchezze ma pose le basi per la tratta "
            "degli schiavi, una grave ingiustizia storica."
        ),
    ),
    (
        "What new food products did Europe import from the Americas after 1492?",
        "quali nuovi prodotti alimentari arrivarono in Europa dalle Americhe dopo il 1492?",
        ["mais", "patata", "pomodoro", "fagiolo", "tacchino", "tabacco"],
        (
            "Tra i prodotti agricoli importati dall'America ricordiamo: mais, girasole, "
            "peperone, patata, fagiolo, pomodoro e tabacco. Tra le specie animali "
            "giunsero il tacchino, il cincillà, il visone americano e la trota arcobaleno."
        ),
    ),
    (
        "What happened at the Diet of Augsburg in 1530?",
        "cosa accadde alla Dieta di Augusta del 1530?",
        ["augusta", "melantone", "luterane", "rottura", "cattolica", "lega"],
        (
            "Alla Dieta di Augusta del 1530 partecipò Filippo Melantone, portavoce di "
            "Lutero, che presentò la Confessione Augustana in cui furono ribadite le "
            "tesi luterane, sancendo la definitiva rottura con la dottrina cattolica. "
            "I principi tedeschi luterani avevano intanto costituito la Lega di "
            "Smalcalda in funzione anti-imperiale."
        ),
    ),
    (
        "What did the Peace of Augsburg of 1555 establish?",
        "cosa stabilì la pace di Augusta del 1555?",
        ["cuius regio", "1555", "principe", "religione", "emigrare", "protestante"],
        (
            "La pace di Augusta del 1555 riconobbe ufficialmente la religione "
            "protestante e stabilì il principio 'cuius regio eius religio': ogni "
            "principe tedesco poteva scegliere la propria religione e i sudditi erano "
            "tenuti ad uniformarsi. A chi non volesse aderire era concesso il diritto "
            "di emigrare."
        ),
    ),
    (
        "What was Calvin's doctrine of predestination?",
        "qual era la dottrina calvinista della predestinazione?",
        ["predestinazione", "eletti", "dannati", "calvino", "grazia", "paradiso"],
        (
            "Calvino affermava la sovranità assoluta di Dio sull'uomo e la dottrina "
            "della predestinazione: l'umanità è divisa in eletti, destinati al "
            "Paradiso, e dannati. L'uomo con la sua natura imperfetta non può "
            "salvarsi per propria fede; è Dio a predestinarlo alla salvezza. "
            "Calvino riconobbe come sacramenti validi solo il battesimo e l'eucaristia."
        ),
    ),
    (
        "What was England's Glorious Revolution?",
        "cos'era la Gloriosa Rivoluzione inglese?",
        ["gloriosa rivoluzione", "inghilterra", "parlamento", "sovrano", "costituzionale"],
        (
            "La Gloriosa Rivoluzione inglese è descritta nel contesto del passaggio "
            "dall'assolutismo verso forme più costituzionali di governo in Inghilterra "
            "nel Seicento, in cui il parlamento limitò il potere assoluto del sovrano."
        ),
    ),
    (
        "What were the main features of the First Industrial Revolution?",
        "quali furono le caratteristiche principali della Prima Rivoluzione Industriale?",
        ["rivoluzione industriale", "fabbrica", "operai", "carbone", "watt", "inghilterra"],
        (
            "La Prima Rivoluzione Industriale fu caratterizzata dall'introduzione di "
            "nuove tecnologie come la macchina a vapore di James Watt, dalla nascita "
            "della fabbrica come luogo di produzione accentrata, dall'uso massiccio "
            "del carbone e dalla trasformazione dei rapporti sociali con la nascita "
            "del proletariato operaio."
        ),
    ),
    (
        "Who were the philosophes and what was their central idea?",
        "chi erano i philosophes e qual era la loro idea centrale?",
        ["philosophes", "ragione", "lume", "conoscenza", "critica", "illuminismo"],
        (
            "I philosophes erano i pensatori dell'Illuminismo che sostenevano il "
            "primato del 'lume naturale' della ragione come strumento di conoscenza "
            "e critica della realtà sociale e politica. Proponevano una nuova visione "
            "dell'economia e della politica fondata sui diritti naturali e sul progresso."
        ),
    ),
    (
        "Who was Catherine II of Russia and why is she considered an enlightened despot?",
        "chi era Caterina II di Russia e perché è considerata un despota illuminato?",
        ["caterina", "russia", "re filosofi", "illuminati", "assolutismo"],
        (
            "Caterina II di Russia è descritta tra i cosiddetti 're filosofi', sovrani "
            "che cercarono di applicare i principi illuministi al governo mantenendo "
            "però il potere assoluto. È inserita, insieme a Giuseppe II d'Austria e "
            "Federico II di Prussia, tra i rappresentanti del dispotismo illuminato."
        ),
    ),
    (
        "What were the economic causes of the French Revolution?",
        "quali furono le cause economiche della Rivoluzione Francese?",
        ["crisi economica", "ancien regime", "stati generali", "terzo stato", "debito"],
        (
            "La crisi economica è individuata come una delle principali premesse della "
            "Rivoluzione Francese. L'Ancien Régime era caratterizzato da privilegi "
            "fiscali per nobiltà e clero, mentre il peso delle tasse gravava sul terzo "
            "stato. La convocazione degli Stati Generali fu una risposta diretta a "
            "questa crisi finanziaria."
        ),
    ),
    (
        "When was the Bastille stormed and what did it symbolize?",
        "quando fu presa la Bastiglia e cosa simboleggiò?",
        ["bastiglia", "14 luglio", "1789", "rivoluzione", "popolo", "simbolo"],
        (
            "La Bastiglia fu presa il 14 luglio 1789. L'evento rappresentò una svolta "
            "simbolica della Rivoluzione Francese, segnando il passaggio dall'azione "
            "delle assemblee all'azione popolare diretta contro il potere monarchico."
        ),
    ),
    (
        "What was the War of the Vendée during the French Revolution?",
        "cos'era la guerra della Vandea durante la Rivoluzione Francese?",
        ["vandea", "rivoluzionari", "guerra", "interna", "controrivoluzione"],
        (
            "La guerra della Vandea fu una delle difficoltà interne della Rivoluzione "
            "Francese: un conflitto civile che oppose i rivoluzionari a una parte della "
            "popolazione francese — in particolare contadini e fedeli alla monarchia "
            "e alla Chiesa — nella regione della Vandea."
        ),
    ),
    (
        "What were Napoleon's main military campaigns and how did his empire end?",
        "quali furono le principali campagne di Napoleone e come finì il suo impero?",
        ["campagna d'italia", "mosca", "sant'elena", "consolato", "impero", "sconfitta"],
        (
            "Napoleone condusse la campagna d'Italia con la nascita delle Repubbliche, "
            "la campagna d'Egitto che ne accelerò l'ascesa politica, poi instaurò il "
            "Consolato e l'Impero estendendo l'egemonia sull'Europa. La conquista di "
            "Mosca segnò l'inizio del declino; l'impero si concluse con la sconfitta "
            "definitiva e l'esilio sull'isola di Sant'Elena."
        ),
    ),
    (
        "What did the Congress of Vienna decide and who were its main actors?",
        "cosa stabilì il Congresso di Vienna e chi ne furono i protagonisti?",
        ["congresso di vienna", "restaurazione", "santa alleanza", "europa", "equilibrio"],
        (
            "Il Congresso di Vienna stabilì un nuovo assetto europeo volto a restaurare "
            "l'ordine precedente alla Rivoluzione Francese e alle conquiste napoleoniche. "
            "Portò alla creazione della Santa Alleanza tra le potenze conservatrici. "
            "I protagonisti furono i rappresentanti delle grandi potenze europee "
            "vincitrici su Napoleone."
        ),
    ),
    (
        "Who was Mazzini and what was the Giovine Italia?",
        "chi era Mazzini e cos'era la Giovine Italia?",
        ["mazzini", "giovine italia", "dio e popolo", "repubblica", "indipendenza"],
        (
            "Giuseppe Mazzini fu uno dei principali protagonisti del Risorgimento e "
            "fondatore della Giovine Italia, un'associazione che propugnava "
            "l'indipendenza e l'unificazione dell'Italia come nazione libera e "
            "repubblicana, ispirata al motto 'Dio e Popolo'."
        ),
    ),
    (
        "What was Cavour's role in the unification of Italy?",
        "quale fu il ruolo di Cavour nell'unificazione d'Italia?",
        ["cavour", "seconda guerra", "spedizione dei mille", "piemonte", "diplomatica"],
        (
            "Camillo Benso conte di Cavour fu la figura politica centrale del processo "
            "di unificazione. Attuò riforme nel Regno di Sardegna, condusse una "
            "politica estera che portò all'alleanza con la Francia, guidò la Seconda "
            "guerra d'Indipendenza e creò le condizioni diplomatiche per la Spedizione "
            "dei Mille di Garibaldi."
        ),
    ),
    (
        "What was Taylorism and in what historical context did it emerge?",
        "cos'era il Taylorismo e in quale contesto storico nacque?",
        ["taylorismo", "organizzazione", "lavoro", "seconda rivoluzione", "fabbrica", "scientifica"],
        (
            "Il Taylorismo fu un sistema di organizzazione scientifica del lavoro "
            "sviluppato durante la Seconda Rivoluzione Industriale. Rappresentò una "
            "nuova forma di razionalizzazione della produzione in fabbrica, finalizzata "
            "ad aumentare la produttività attraverso la standardizzazione dei compiti operai."
        ),
    ),
    (
        "What was the Monroe Doctrine and in what context was it issued?",
        "cos'era la dottrina Monroe e in quale contesto fu proclamata?",
        ["monroe", "america latina", "indipendenza", "colonizzazione", "europa", "intervento"],
        (
            "La dottrina Monroe fu proclamata nell'ambito delle lotte per l'indipendenza "
            "dell'America latina e dei moti liberali. Affermava il principio che "
            "l'America non doveva essere considerata campo di ulteriore colonizzazione "
            "europea, opponendosi all'interventismo delle potenze del Vecchio Continente "
            "nelle Americhe."
        ),
    ),
    (
        "How were the price revolution of the 16th century and the geographical discoveries connected?",
        "come erano collegati la rivoluzione dei prezzi del Cinquecento e le scoperte geografiche?",
        ["rivoluzione dei prezzi", "bodin", "oro", "argento", "americhe", "inflazione"],
        (
            "Nel Cinquecento i prezzi subirono un incremento di circa il 400%. "
            "Il pensatore Jean Bodin spiegò il fenomeno sostenendo che l'importazione "
            "massiccia di oro e argento dalle Americhe da parte di Spagna e Portogallo "
            "aveva causato la svalutazione della moneta. I salariati furono i più "
            "penalizzati, poiché l'inflazione erose il loro già esiguo potere d'acquisto."
        ),
    ),
]

# ── Helpers ────────────────────────────────────────────────────────────

def tokenize(text: str):
    return re.sub(r'[^\w\s]', ' ', text.lower()).split()


def rrf(rankings, k=RRF_K):
    scores = {}
    for ranking in rankings:
        for rank, idx in enumerate(ranking):
            scores[idx] = scores.get(idx, 0.0) + 1.0 / (k + rank + 1)
    return sorted(scores.keys(), key=lambda x: scores[x], reverse=True)


def cosine_scores(q_emb, embeddings):
    q_norm = float(np.linalg.norm(q_emb))
    scores = []
    for emb in embeddings:
        e = np.array(emb, dtype=np.float32)
        e_norm = float(np.linalg.norm(e))
        scores.append(float(np.dot(q_emb, e) / (q_norm * e_norm)) if e_norm > 0 else 0.0)
    return scores


# ── RAG standard: cerca su TUTTI i chunk della collection ──────────────

def retrieve_standard(query, q_emb, col, top_k=TOP_K):
    t0 = time.perf_counter()

    data = col.get(include=["embeddings", "documents", "metadatas"])
    embeddings = data["embeddings"]
    documents  = data["documents"]

    dense_scores = cosine_scores(q_emb, embeddings)
    dense_rank   = sorted(range(len(embeddings)), key=lambda i: dense_scores[i], reverse=True)

    bm25       = BM25Okapi([tokenize(d) for d in documents])
    bm25_sc    = bm25.get_scores(tokenize(query))
    bm25_rank  = sorted(range(len(embeddings)), key=lambda i: float(bm25_sc[i]), reverse=True)

    fused = rrf([dense_rank, bm25_rank])[:top_k]
    elapsed = (time.perf_counter() - t0) * 1000

    return [documents[i] for i in fused], len(embeddings), elapsed


# ── SLM-routed retrieval ───────────────────────────────────────────────

def retrieve_slm(query, q_emb, registry, chroma_client, top_k=TOP_K):
    t0 = time.perf_counter()

    top_slms = find_top_n_slms(q_emb, registry, n=TOP_N_SLMS)

    all_chunks = []
    for slm_name, _ in top_slms:
        entry = registry[slm_name]
        chunks_path = Path(entry["chunks_json"])
        if not chunks_path.exists():
            continue
        with open(chunks_path) as f:
            chunk_ids = [c["id"] for c in json.load(f)]
        col = chroma_client.get_collection(entry["collection"])
        data = col.get(ids=chunk_ids, include=["embeddings", "documents", "metadatas"])
        for i, emb in enumerate(data["embeddings"]):
            e = np.array(emb, dtype=np.float32)
            e_norm = float(np.linalg.norm(e))
            q_norm = float(np.linalg.norm(q_emb))
            ds = float(np.dot(q_emb, e) / (q_norm * e_norm)) if e_norm > 0 else 0.0
            all_chunks.append({"text": data["documents"][i], "score": ds})

    if not all_chunks:
        return [], 0, (time.perf_counter() - t0) * 1000

    dense_rank = sorted(range(len(all_chunks)), key=lambda i: all_chunks[i]["score"], reverse=True)
    bm25       = BM25Okapi([tokenize(c["text"]) for c in all_chunks])
    bm25_sc    = bm25.get_scores(tokenize(query))
    bm25_rank  = sorted(range(len(all_chunks)), key=lambda i: float(bm25_sc[i]), reverse=True)

    fused   = rrf([dense_rank, bm25_rank])[:top_k]
    elapsed = (time.perf_counter() - t0) * 1000

    return [all_chunks[i]["text"] for i in fused], len(all_chunks), elapsed


# ── Generation ────────────────────────────────────────────────────────

_gen_tok = None
_gen_mdl = None

def _load_gen_model(model_name: str):
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM
    global _gen_tok, _gen_mdl
    if _gen_tok is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        dtype  = torch.float16 if device == "cuda" else torch.float32
        print(f"  Carico {model_name} su {device}...")
        _gen_tok = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        _gen_mdl = AutoModelForCausalLM.from_pretrained(
            model_name, torch_dtype=dtype, trust_remote_code=True
        ).to(device).eval()


def generate(query: str, docs: list, model_name: str) -> str:
    import torch
    from SLMAgent import build_messages, _apply_chat_template_no_think
    _load_gen_model(model_name)
    device = next(_gen_mdl.parameters()).device
    # apply_chat_template with enable_thinking=False prevents <think> tokens at the source.
    text = _apply_chat_template_no_think(_gen_tok, build_messages(query, docs))
    inputs = _gen_tok(text, return_tensors="pt", truncation=True, max_length=2048).to(device)
    with torch.no_grad():
        out = _gen_mdl.generate(
            **inputs,
            max_new_tokens=MAX_NEW_TOKENS,
            do_sample=False,
            pad_token_id=_gen_tok.eos_token_id,
        )
    return _gen_tok.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True).strip()


# ── Main ───────────────────────────────────────────────────────────────

def main():
    print("Carico modelli...")
    emb_model    = SentenceTransformer("BAAI/bge-m3")
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    registry     = load_registry()

    col_name = COLLECTION or chroma_client.list_collections()[0].name
    col      = chroma_client.get_collection(col_name)
    total_chunks = col.count()

    print(f"Collection: {col_name}  |  chunk totali: {total_chunks}  |  SLM: {len(registry)}")
    print(f"Query: {len(QUERIES)}  |  top-k={TOP_K}  |  top-N SLM={TOP_N_SLMS}  |  model={GENERATION_MODEL}\n")

    def hit_rate(docs, keywords):
        joined = " ".join(docs).lower()
        hits = sum(1 for kw in keywords if kw in joined)
        return hits / len(keywords) * 100 if keywords else 0.0

    std_times, slm_times = [], []
    std_pools, slm_pools = [], []
    overlaps, std_hits, slm_hits = [], [], []
    md_rows = []

    SEP = "=" * 110
    for idx, (query_en, query_it, expected_kws, ground_truth) in enumerate(QUERIES, 1):
        print(f"\n[{idx}/{len(QUERIES)}] {query_en}")

        # BGE-M3 è multilingue: si usa la query italiana per embedding e BM25
        # così dense retrieval e lexical retrieval operano nella stessa lingua dei documenti
        q_emb = emb_model.encode(
            [query_it], normalize_embeddings=True, convert_to_numpy=True
        )[0].astype(np.float32)

        docs_std, pool_std, t_std = retrieve_standard(query_it, q_emb, col)
        docs_slm, pool_slm, t_slm = retrieve_slm(query_it, q_emb, registry, chroma_client)

        overlap = len(set(docs_std[:TOP_K]) & set(docs_slm[:TOP_K])) / TOP_K * 100
        hr_std  = hit_rate(docs_std, expected_kws)
        hr_slm  = hit_rate(docs_slm, expected_kws)

        std_times.append(t_std); slm_times.append(t_slm)
        std_pools.append(pool_std); slm_pools.append(pool_slm)
        overlaps.append(overlap)
        std_hits.append(hr_std); slm_hits.append(hr_slm)

        speedup = t_std / t_slm if t_slm > 0 else float("inf")

        print(f"  Retrieval  —  StdRAG: {t_std:.1f}ms (pool={pool_std})  |  SLM-RAG: {t_slm:.1f}ms (pool={pool_slm})  speedup={speedup:.1f}x")
        print(f"  Generazione StdRAG...")
        t_gen0 = time.perf_counter()
        ans_std = generate(query_it, docs_std, GENERATION_MODEL)
        t_gen_std = (time.perf_counter() - t_gen0) * 1000

        print(f"  Generazione SLM-RAG...")
        t_gen0 = time.perf_counter()
        ans_slm = generate(query_it, docs_slm, GENERATION_MODEL)
        t_gen_slm = (time.perf_counter() - t_gen0) * 1000

        print(f"  Gen times  —  StdRAG: {t_gen_std:.0f}ms  |  SLM-RAG: {t_gen_slm:.0f}ms")
        print(f"  StdRAG : {ans_std[:100]}…")
        print(f"  SLM-RAG: {ans_slm[:100]}…")

        md_rows.append({
            "query_en":     query_en,
            "query_it":     query_it,
            "ground_truth": ground_truth,
            "ans_std":      ans_std,
            "ans_slm":      ans_slm,
            "docs_std":     docs_std,
            "docs_slm":     docs_slm,
            "t_ret_std":    t_std,
            "t_ret_slm":    t_slm,
            "t_gen_std":    t_gen_std,
            "t_gen_slm":    t_gen_slm,
            "speedup":      speedup,
            "pool_std":     pool_std,
            "pool_slm":     pool_slm,
            "hr_std":       hr_std,
            "hr_slm":       hr_slm,
            "overlap":      overlap,
        })

    # ── Salva Markdown ─────────────────────────────────────────────────
    avg_speedup    = np.mean(std_times) / np.mean(slm_times)
    pool_reduction = (1 - np.mean(slm_pools) / np.mean(std_pools)) * 100

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(f"# Benchmark RAG — {col_name}\n\n")
        f.write(f"**Modello:** {GENERATION_MODEL}  |  **top-k:** {TOP_K}  |  **top-N SLM:** {TOP_N_SLMS}\n\n")
        f.write(f"| Metrica | StdRAG | SLM-RAG |\n|---|---|---|\n")
        f.write(f"| Speedup retrieval | — | **{avg_speedup:.1f}x** |\n")
        f.write(f"| Pool medio | {int(np.mean(std_pools))} chunk | {int(np.mean(slm_pools))} chunk (-{pool_reduction:.0f}%) |\n")
        f.write(f"| Keyword hit | {np.mean(std_hits):.0f}% | **{np.mean(slm_hits):.0f}%** |\n")
        f.write(f"| Overlap medio top-{TOP_K} | {np.mean(overlaps):.0f}% | — |\n\n")
        f.write("---\n\n")

        for i, r in enumerate(md_rows, 1):
            f.write(f"## {i}. {r['query_en']}\n\n")
            f.write(f"*{r['query_it']}*\n\n")
            f.write(f"| | StdRAG | SLM-RAG |\n|---|---|---|\n")
            f.write(f"| **Retrieval** | {r['t_ret_std']:.1f} ms | {r['t_ret_slm']:.1f} ms ({r['speedup']:.1f}x) |\n")
            f.write(f"| **Generazione** | {r['t_gen_std']:.0f} ms | {r['t_gen_slm']:.0f} ms |\n")
            f.write(f"| **Totale** | {r['t_ret_std']+r['t_gen_std']:.0f} ms | {r['t_ret_slm']+r['t_gen_slm']:.0f} ms |\n")
            f.write(f"| **Pool chunk** | {r['pool_std']} | {r['pool_slm']} |\n")
            f.write(f"| **Keyword hit** | {r['hr_std']:.0f}% | {r['hr_slm']:.0f}% |\n\n")
            f.write(f"### Risposta StdRAG\n\n{r['ans_std']}\n\n")
            f.write(f"### Risposta SLM-RAG\n\n{r['ans_slm']}\n\n")
            f.write(f"### Ground Truth\n\n{r['ground_truth']}\n\n")
            f.write("---\n\n")

    print(f"\nFile salvato: {OUTPUT_FILE}")

    # ── Salva JSON per evaluate_quality.py ────────────────────────────
    json_path = OUTPUT_FILE.replace(".md", "_keybert_results.json")
    json_data = {
        "metadata": {
            "collection": col_name,
            "model":      GENERATION_MODEL,
            "top_k":      TOP_K,
            "top_n_slm":  TOP_N_SLMS,
        },
        "results": [
            {
                "query_en":     r["query_en"],
                "query_it":     r["query_it"],
                "ground_truth": r["ground_truth"],
                "std": {
                    "chunks":          r["docs_std"],
                    "answer":          r["ans_std"],
                    "t_ret_ms":        r["t_ret_std"],
                    "t_gen_ms":        r["t_gen_std"],
                    "pool":            r["pool_std"],
                    "keyword_hit_pct": r["hr_std"],
                },
                "slm": {
                    "chunks":          r["docs_slm"],
                    "answer":          r["ans_slm"],
                    "t_ret_ms":        r["t_ret_slm"],
                    "t_gen_ms":        r["t_gen_slm"],
                    "pool":            r["pool_slm"],
                    "keyword_hit_pct": r["hr_slm"],
                },
                "overlap_pct": r["overlap"],
                "speedup":     r["speedup"],
            }
            for r in md_rows
        ],
    }
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    print(f"JSON salvato:  {json_path}")
    print(f"\nRIEPILOGO")
    print(f"  Speedup retrieval     : {avg_speedup:.1f}x")
    print(f"  Riduzione pool        : {pool_reduction:.1f}%  ({int(np.mean(std_pools))} → {int(np.mean(slm_pools))} chunk)")
    print(f"  Overlap medio top-{TOP_K}  : {np.mean(overlaps):.0f}%")
    print(f"  Keyword hit StdRAG    : {np.mean(std_hits):.0f}%")
    print(f"  Keyword hit SLM-RAG   : {np.mean(slm_hits):.0f}%")


if __name__ == "__main__":
    main()
