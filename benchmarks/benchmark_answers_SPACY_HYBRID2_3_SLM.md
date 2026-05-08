# Benchmark RAG — storia

**Modello:** Qwen/Qwen3.5-4B  |  **top-k:** 5  |  **top-N SLM:** 3

| Metrica | StdRAG | SLM-RAG |
|---|---|---|
| Speedup retrieval | — | **2.3x** |
| Pool medio | 118 chunk | 4 chunk (-96%) |
| Keyword hit | 44% | **45%** |
| Overlap medio top-5 | 36% | — |

---

## 1. Who imported spices into Europe during the Middle Ages?

*da chi venivano importate le spezie in europa nel medioevo?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 10.5 ms | 4.9 ms (2.1x) |
| **Generazione** | 4121 ms | 582 ms |
| **Totale** | 4131 ms | 587 ms |
| **Pool chunk** | 118 | 4 |
| **Keyword hit** | 100% | 100% |

### Risposta StdRAG

Dall'Oriente.

### Risposta SLM-RAG

Le spezie venivano importate in Europa nel Medioevo dall'Oriente.

### Ground Truth

Il commercio delle spezie era controllato dai mercanti arabi insieme alla repubblica veneziana, che detenevano il monopolio attraversando i territori musulmani. I molteplici rischi del viaggio e i vari passaggi di mano aumentavano considerevolmente il prezzo della merce.

---

## 2. What territories did Charles V control?

*quali territori controllava Carlo V?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 10.9 ms | 4.2 ms (2.6x) |
| **Generazione** | 5315 ms | 4328 ms |
| **Totale** | 5326 ms | 4332 ms |
| **Pool chunk** | 118 | 4 |
| **Keyword hit** | 50% | 50% |

### Risposta StdRAG

In base al contesto fornito, i territori controllati da Carlo V (e successivamente dal suo figlio Filippo II) includono:

*   I **territori del nuovo mondo**.
*   Il **Portogallo** (la cui sede era vacante).
*   Il **Sacro romano impero germanico** (menzionato nel contesto come parte dei vasti territori degli Asburgo, sebbene il testo associ esplicitamente l'elezione imperiale e la struttura territoriale a Massimiliano I, il testo collega Carlo V come imperatore tedesco e successore di Massimiliano).
*   I **Paesi Bassi** e la **Franca Contea** (menzionati come parte dei possedimenti degli Asburgo nel contesto di Massimiliano I, ma il testo indica che Carlo V iniziò un conflitto contro la Francia e il predominio spagnolo su gran parte dell'Italia, implicando il controllo di queste aree come parte dell'impero asburgico).

Il testo specifica esplicitamente che, dopo Carlo V, Filippo II stabilì la reggia a Madrid e che oltre ai territori del nuovo mondo ne facevano parte anche il Portogallo. Inoltre, si menziona il predominio spagnolo su

### Risposta SLM-RAG

In base al contesto fornito, Carlo V controllava un impero enorme e complesso che includeva:

*   I territori del **nuovo mondo**.
*   Il **Portogallo** (la cui sede era vacante).
*   Il **Sacro romano impero germanico** (menzionato nel contesto come parte del vasto territorio degli Asburgo, sebbene il testo lo associ esplicitamente a Massimiliano I, il contesto storico e la continuità indicano che Carlo V ereditò questa struttura).
*   Gli **antichi possedimenti degli Asburgo**: Austria, Tirolo, Stiria, Corinzia e Carniola.
*   I **Paesi Bassi** e la **Franca Contea** (territori acquisiti grazie all'unione matrimoniale con Maria di Borgogna).
*   Gran parte dell'**Italia**, luogo strategico per il dominio spagnolo, dove si distinsero i regni di Savoia, Toscana, Venezia e Genova.

### Ground Truth

Carlo V controllava un vasto impero che comprendeva la Spagna, i territori asburgici, le Fiandre, il Regno di Napoli e le colonie americane. Il suo regno fu segnato da conflitti con la Francia, i principi tedeschi luterani e l'impero ottomano.

---

## 3. What were the main causes of the French Revolution?

*quali furono le cause della rivoluzione francese?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 10.0 ms | 4.1 ms (2.5x) |
| **Generazione** | 3523 ms | 5252 ms |
| **Totale** | 3533 ms | 5256 ms |
| **Pool chunk** | 118 | 4 |
| **Keyword hit** | 33% | 83% |

### Risposta StdRAG

Le cause della Rivoluzione francese indicate nel contesto sono:

*   **Crisi agraria e carestie:** Nel 1788, a causa di capricci del clima e raccolti esigui, aumentò drasticamente il prezzo del pane, aggravando le condizioni di una popolazione dove la terra era la principale fonte di reddito.
*   **Il modello dell'Ancien Régime:** Un sistema di stato, economia e politica basato su impostazioni medioevali, caratterizzato da una monarchia assoluta, una società divisa in rigidi ordini sociali e la persistenza di diritti feudali.
*   **Conseguenze sociali delle carestie:** Le difficoltà economiche derivanti dalla crisi agraria mettevano sempre in agguato le conseguenze sociali per le masse.

### Risposta SLM-RAG

In base al contesto fornito, le cause della Rivoluzione francese furono:

*   **Crisi agraria e climatica:** Capricci del clima che causarono raccolti esigui e carestie (come nel 1788), portando all'aumento del prezzo del pane.
*   **Struttura economica e sociale dell'Ancien Regime:**
    *   Monarchia assoluta.
    *   Società divisa in rigidi ordini sociali con persistenza di diritti feudali.
    *   La terra come principale fonte di reddito, rendendo la popolazione vulnerabile alle carestie.
*   **Pressione della borghesia:** La borghesia, avendo acquistato peso economico, esercitava una notevole pressione politica per ottenere riforme, contro cui si opponevano le forze conservatrici (aristocrazia e proprietari terrieri).
*   **Gestione finanziaria del Re:** Luigi XVI, salito al trono nel 1774, tentò inizialmente riforme (con Jacques Turgot) ma queste fallirono a causa dell'opposizione dei proprietari terrieri (es. tassa sulle terre) e della necessità di reperire risorse.
*   **

### Ground Truth

Le principali cause della Rivoluzione Francese furono la crisi economica dell'Ancien Régime, le ingiustizie fiscali che gravavano sul terzo stato, la convocazione degli Stati Generali e la crescente influenza dell'opinione pubblica. La nobiltà e il clero godevano di privilegi fiscali che alimentavano il malcontento popolare.

---

## 4. How did James Watt's steam engine work?

*come funzionava la macchina a vapore di james watt?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 10.8 ms | 4.7 ms (2.3x) |
| **Generazione** | 527 ms | 546 ms |
| **Totale** | 538 ms | 550 ms |
| **Pool chunk** | 118 | 5 |
| **Keyword hit** | 83% | 83% |

### Risposta StdRAG

The answer is not available in the provided context.

### Risposta SLM-RAG

The answer is not available in the provided context.

### Ground Truth

James Watt impiegò la macchina a vapore nella tessitura, nell'estrazione dei minerali e nella loro lavorazione (siderurgia). Il vapore veniva prodotto grazie all'utilizzo del carbone, per cui le attività industriali dovevano svilupparsi vicino alle miniere.

---

## 5. What were the key principles of the Enlightenment?

*quali erano i principi fondamentali dell'illuminismo?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 10.9 ms | 4.4 ms (2.5x) |
| **Generazione** | 5262 ms | 4315 ms |
| **Totale** | 5273 ms | 4320 ms |
| **Pool chunk** | 118 | 3 |
| **Keyword hit** | 67% | 67% |

### Risposta StdRAG

In base al contesto fornito, i principi fondamentali dell'Illuminismo sono:

*   **La ragione:** È il "lume" naturale dell'uomo che lo sollecita a svincolarsi dalle tradizioni e dai pregiudizi per affermare un nuovo modo di guardare la realtà, la società, la politica, la cultura e la religione.
*   **La libertà:** È un valore centrale, applicato concretamente con la nascita degli Stati Uniti come stato non legato alle tradizioni storiche dell'Europa.
*   **I diritti del singolo e del popolo:** L'Illuminismo difende questi diritti contro il despotismo delle autorità.
*   **L'uscita dallo stato di minorità:** Definito da Kant come la capacità dell'uomo di imputare a se stesso la propria condizione di minorità, basata sulla capacità di servirsi della propria intelligenza.
*   **Il coraggio di servirsi della propria intelligenza:** Espresso dal motto "Sapere aude" ("Abbi il coraggio di servirti della tua intelligenza").
*   **L'uguaglianza:** Un valore che ha dato nuove speranze ai contadini e contribuito a dissolvere il principio di autorità.

### Risposta SLM-RAG

In base al contesto fornito, i principi fondamentali dell'Illuminismo sono:

*   **La ragione:** È il "lume" naturale dell'uomo che sollecita a svincolarsi dalle tradizioni e dai pregiudizi per affermare un nuovo modo di guardare la realtà, la società, la politica, la cultura e la religione.
*   **La libertà:** È un principio concreto applicato con la nascita degli USA, uno stato non legato alle tradizioni storiche dell'Europa.
*   **I diritti del singolo e del popolo:** L'Illuminismo difende questi diritti contro il despotismo delle autorità.
*   **Il coraggio di usare la propria intelligenza:** Espresso dal motto di Kant "Sapere aude" (Abbi il coraggio di servirti della tua intelligenza).
*   **L'uscita dallo stato di minorità:** Definizione data da Kant, che indica l'uomo che deve imputare a se stesso la sua condizione di minorità.

### Ground Truth

L'Illuminismo si fondava sul primato del 'lume naturale' della ragione come strumento di conoscenza e critica della realtà. I philosophes propugnavano una nuova visione dell'economia e della politica basata sulla libertà, sul progresso e sui diritti naturali dell'individuo.

---

## 6. What was the American Revolution?

*che cosa fu la rivoluzione americana?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 11.0 ms | 4.9 ms (2.2x) |
| **Generazione** | 520 ms | 476 ms |
| **Totale** | 531 ms | 481 ms |
| **Pool chunk** | 118 | 6 |
| **Keyword hit** | 33% | 50% |

### Risposta StdRAG

The answer is not available in the provided context.

### Risposta SLM-RAG

The answer is not available in the provided context.

### Ground Truth

La Rivoluzione Americana fu il processo con cui le tredici colonie americane si ribellarono al dominio inglese, principalmente a causa delle difficili condizioni economiche e fiscali imposte dalla madrepatria. Nel 1776 fu stilata la Dichiarazione d'Indipendenza; la sconfitta inglese fu sancita dalla pace di Parigi del 1783, che diede vita al nuovo stato federale americano.

---

## 7. Who were the Mongols and how did they expand?

*chi erano i mongoli e come si espansero?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 9.7 ms | 4.0 ms (2.4x) |
| **Generazione** | 541 ms | 4484 ms |
| **Totale** | 551 ms | 4488 ms |
| **Pool chunk** | 118 | 3 |
| **Keyword hit** | 17% | 83% |

### Risposta StdRAG

The answer is not available in the provided context.

### Risposta SLM-RAG

Secondo il contesto fornito, i mongoli erano un esercito composto da cavalieri addestrati e pronti a tutto, la cui ferocia nei combattimenti permise loro di espandersi rapidamente. Venivano temuti dagli europei e chiamati con il nome di **Tartari** (derivante dal "Tartaro", che significa inferno).

La loro espansione avvenne in diverse fasi:
1.  **Gengis Khan** scatenò l'offensiva verso la Cina, oltrepassando la **Grande Muraglia**, occupò le steppe della Russia meridionale conquistando **Samarcanda** e **Bukara**, e infine si rivolse verso la Persia, la Georgia e la Bulgaria.
2.  Dopo la sua morte, i suoi successori continuarono l'espansione arrivando a **Baghdad** nel 1258 e in **Polonia**, dove sconfissero la cavalleria polacco-tedesca e conquistarono l'**Ungheria**.

### Ground Truth

I Mongoli erano un popolo di cavalieri guidati da Gengis Khan, che scatenò la sua offensiva verso la Cina oltrepassando la Grande Muraglia, poi occupò le steppe della Russia meridionale, conquistò Samarcanda e Bukara e attaccò Persia, Georgia e Bulgaria. Erano chiamati Tartari dagli europei. Dopo la sua morte il regno fu diviso tra i quattro figli, dando origine a quattro Khanati.

---

## 8. What was Luther's Protestant Reformation?

*che cosa fu la riforma protestante di lutero?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 10.8 ms | 4.4 ms (2.5x) |
| **Generazione** | 2796 ms | 3085 ms |
| **Totale** | 2807 ms | 3090 ms |
| **Pool chunk** | 118 | 4 |
| **Keyword hit** | 100% | 100% |

### Risposta StdRAG

La Riforma protestante di Lutero fu un movimento iniziato nel 1520 dopo che Martin Lutero, monaco tedesco, pubblicò le 95 tesi contro le indulgenze e la dottrina tradizionale della Chiesa cattolica. Lutero affermò che per la salvezza dell'anima basta la sola fede e che ogni individuo dispone del libero arbitrio per leggere e interpretare personalmente la Bibbia. Questo cambiamento radicale fu facilitato dalla diffusione della stampa. La Chiesa cattolica emise una scomunica contro Lutero nel 1520, segnando l'inizio della Riforma.

### Risposta SLM-RAG

La Riforma protestante di Lutero fu un movimento iniziato dopo che Martin Lutero, monaco tedesco, pubblicò le 95 tesi nel 1517, sollevando forti dubbi sulla dottrina tradizionale della Chiesa cattolica, in particolare sulle indulgenze. Nel 1520, dopo essere stato scomunicato, Lutero iniziò la Riforma affermando che **la sola fede** è sufficiente per la salvezza dell'anima e che ogni individuo possiede il **libero arbitrio** per leggere e interpretare personalmente la Bibbia. Questo cambiamento radicale fu facilitato dalla recente invenzione della stampa, che ne permise la rapida diffusione in Europa.

### Ground Truth

La Riforma protestante di Lutero segnò una rottura definitiva con la dottrina cattolica, ribadita nella Confessione Augustana presentata da Filippo Melantone alla Dieta di Augusta del 1530. La pace di Augusta del 1555 riconobbe ufficialmente la religione protestante stabilendo il principio 'cuius regio eius religio'.

---

## 9. How was the Italian state formed during the Risorgimento?

*come si formò lo stato italiano nel risorgimento?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 9.4 ms | 4.7 ms (2.0x) |
| **Generazione** | 5322 ms | 5267 ms |
| **Totale** | 5331 ms | 5271 ms |
| **Pool chunk** | 118 | 7 |
| **Keyword hit** | 50% | 83% |

### Risposta StdRAG

In base al contesto fornito, la formazione dello Stato italiano nel Risorgimento si può riassumere come segue:

Lo Stato italiano nacque nel **1861** come risultato di un processo di unificazione che condusse all'indipendenza del territorio dall'occupazione straniera e all'unificazione di vari regni interni. Questo processo fu guidato da un'intesa politica tra il politico italiano **Cavour** e l'imperatore francese **Napoleone III**, conclusasi il 21 luglio 1858 a **Plombières**.

Secondo gli accordi di Plombières, la Francia si impegnò a intervenire a fianco del Regno di Sardegna solo in caso di guerra dichiarata dall'Austria. In cambio, la Francia avrebbe ottenuto Nizza e la Savoia in caso di vittoria. Per la questione italiana, si concordò la costituzione di tre entità:
1.  Un **Regno dell'Alta Italia** sotto la guida della famiglia Savoia.
2.  Un **Regno del Centro Italia** guidato da Girolamo Bonaparte.
3.  Il **Regno delle due Sicilie**, con a capo il figlio di Gioacchino Murat.

Il

### Risposta SLM-RAG

Lo Stato italiano si formò nel 1861 con la proclamazione di Vittorio Emanuele II come Re d'Italia, evento che segna la fine del processo di unificazione iniziato con i "Mille" di Garibaldi nel 1860.

Il processo di unificazione si basò su un complesso di eventi, dottrine politiche e iniziative che portarono all'indipendenza del territorio dall'occupazione straniera e all'unificazione dei vari regni interni. La fase decisiva fu guidata da Garibaldi, che con circa mille volontari sbarcò a Genova nel maggio 1860, conquistò rapidamente la Sicilia e la Calabria, e si diresse verso Napoli, che conquistò a settembre. Garibaldi creò un governo provvisorio presieduto da Crispi.

Per evitare che Garibaldi adottasse l'idea repubblicana di Mazzini o conquistasse Roma (causando problemi internazionali con la Francia), il Regno di Sardegna inviò un esercito che conquistò le Marche e l'Umbria, subito annessi al Piemonte con plebisciti. Il Re Vittorio Emanuele II spinse il suo esercito a sud e incontrò Garibaldi a Teano, dove

### Ground Truth

L'unità d'Italia fu il risultato del Risorgimento, guidato da figure come Mazzini (fondatore della Giovine Italia), Cavour (che condusse la politica diplomatica e la Seconda guerra d'Indipendenza) e Garibaldi (che guidò la Spedizione dei Mille). Il Piemonte fu il fulcro del processo unitario.

---

## 10. What were the social consequences of the Industrial Revolution?

*quali furono le conseguenze sociali della rivoluzione industriale?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 9.3 ms | 4.0 ms (2.3x) |
| **Generazione** | 5332 ms | 5224 ms |
| **Totale** | 5342 ms | 5228 ms |
| **Pool chunk** | 118 | 3 |
| **Keyword hit** | 100% | 83% |

### Risposta StdRAG

In base al contesto fornito, le conseguenze sociali della Rivoluzione Industriale includono:

*   **Cambiamento demografico e urbano:** Inizia un profondo aumento demografico; cambiano gli spazi con la crescita delle città e la formazione di nuovi quartieri, in particolare di operai impiegati nelle fabbriche.
*   **Nascita di nuove classi sociali:** Si passa da una società chiusa a una con nuove classi sociali, tra cui la borghesia, i ceti emergenti, la nuova figura dell'imprenditore e il proletariato (chi possiede solo i figli come ricchezza).
*   **Mobilità sociale e lavoro:** Molti braccianti fuggono dalla campagna (a causa delle enclosures) per trovare lavoro nelle prime fabbriche, dove il lavoro è parcellizzato e c'è lo sfruttamento della mano d'opera (inclusi donne e bambini).
*   **Fenomeno del Luddismo:** Nasce come reazione al cambiamento e allo sfruttamento.
*   **Organizzazioni di difesa:** Nascono prime società di mutuo soccorso per difendere gli operai dallo sfruttamento e, successivamente, iniziano le prime organizzazioni sindacali per la difesa dei diritti.

### Risposta SLM-RAG

In base al contesto fornito, le conseguenze sociali della rivoluzione industriale includono:

*   **Nascita di nuove classi sociali:** Si passa da una società chiusa a una basata sul lavoro operaio, con l'emergere di una nuova classe sociale e la figura dell'imprenditore.
*   **Nascita del proletariato:** Nasce la classe operaia, definita come chi possiede solo la propria prole come ricchezza, spesso sfruttato e ridotto in condizioni misere.
*   **Mobilità demografica e urbana:** Molti braccianti fuggono dalla campagna (a causa delle recinzioni) per trovare lavoro nelle fabbriche, causando la crescita delle città e la formazione di quartieri operai.
*   **Sfruttamento del lavoro:** Si registra un lavoro parcellizzato e lo sfruttamento della mano d'opera, che include donne e bambini.
*   **Fenomeno del luddismo:** Nasce come reazione alle nuove tecnologie e alle condizioni di lavoro.
*   **Organizzazione della difesa:** Nascono prime società di mutuo soccorso per difendere gli operai dallo sfruttamento e, successivamente, le prime organizzazioni sindacali per la difesa dei diritti.

### Ground Truth

La Rivoluzione Industriale determinò la nascita del proletariato operaio, che lavorava in fabbriche in condizioni di sfruttamento. Si accentuò la divisione tra borghesia proprietaria e classe operaia. Gli effetti negativi dell'industrializzazione includevano orari di lavoro estenuanti e condizioni igieniche precarie.

---

## 11. How did the population of Europe change from the year 1000 to the 14th century?

*come cambiò la popolazione europea dall'anno Mille al Trecento?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 9.6 ms | 4.4 ms (2.2x) |
| **Generazione** | 974 ms | 691 ms |
| **Totale** | 984 ms | 695 ms |
| **Pool chunk** | 118 | 4 |
| **Keyword hit** | 100% | 100% |

### Risposta StdRAG

La popolazione europea raddoppiò, passando da circa 40 milioni di abitanti all'inizio del Mille a circa 80 milioni all'inizio del Trecento.

### Risposta SLM-RAG

La popolazione europea raddoppiò, passando da circa 40 milioni di abitanti a circa 80 milioni.

### Ground Truth

La popolazione europea aumentò dall'anno Mille fino all'inizio del Trecento, raddoppiando da circa 40 milioni a circa 80 milioni di abitanti. Questo comportò la necessità di disboscare nuovi terreni per aumentare la produzione, anche se si verificarono ciclicamente carestie decennali che causarono migliaia di vittime.

---

## 12. How did the plague spread from Crimea to Europe?

*come si diffuse la peste dalla Crimea all'Europa?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 10.8 ms | 4.0 ms (2.7x) |
| **Generazione** | 455 ms | 345 ms |
| **Totale** | 465 ms | 349 ms |
| **Pool chunk** | 118 | 3 |
| **Keyword hit** | 14% | 0% |

### Risposta StdRAG

The answer is not available in the provided context.

### Risposta SLM-RAG

The answer is not available in the provided context.

### Ground Truth

La prima epidemia di peste scoppiò in una colonia genovese in Crimea assediata dai Tartari, che lanciarono con le catapulte cadaveri infettati oltre le mura. I cittadini genovesi in fuga portarono il contagio via mare. Intorno al 1347 la peste raggiunse Genova, Venezia e la Sicilia, dilagando l'anno successivo in Toscana, Francia, Inghilterra, Spagna e Germania. Nel 1353 aveva ucciso circa un terzo della popolazione europea.

---

## 13. What is the difference between bubonic plague and pneumonic plague?

*qual è la differenza tra peste bubbonica e peste polmonare?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 10.8 ms | 4.3 ms (2.5x) |
| **Generazione** | 471 ms | 379 ms |
| **Totale** | 482 ms | 384 ms |
| **Pool chunk** | 118 | 3 |
| **Keyword hit** | 0% | 0% |

### Risposta StdRAG

The answer is not available in the provided context.

### Risposta SLM-RAG

The answer is not available in the provided context.

### Ground Truth

La peste bubbonica si presentava sotto forma di tumefazioni chiamate bubboni. La peste polmonare, detta anche peste nera, provocava invece emorragie cutanee che, rapprendosi, formavano chiazze nere sulla pelle.

---

## 14. How was the plague transmitted from animals to humans?

*come veniva trasmessa la peste dagli animali all'uomo?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 10.2 ms | 4.3 ms (2.4x) |
| **Generazione** | 443 ms | 381 ms |
| **Totale** | 453 ms | 386 ms |
| **Pool chunk** | 118 | 3 |
| **Keyword hit** | 0% | 14% |

### Risposta StdRAG

The answer is not available in the provided context.

### Risposta SLM-RAG

The answer is not available in the provided context.

### Ground Truth

Il bacillo della peste era presente nei ratti. Era la pulce che, succhiando il sangue dei topi infetti, trasmetteva la malattia agli esseri umani. Le cattive condizioni igieniche e la promiscuità in cui vivevano gli esseri umani aumentavano ulteriormente la contaminazione.

---

## 15. Who were blamed for spreading the plague and what happened to them?

*chi fu accusato di diffondere la peste e cosa accadde?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 9.7 ms | 4.3 ms (2.2x) |
| **Generazione** | 459 ms | 417 ms |
| **Totale** | 469 ms | 421 ms |
| **Pool chunk** | 118 | 3 |
| **Keyword hit** | 0% | 17% |

### Risposta StdRAG

The answer is not available in the provided context.

### Risposta SLM-RAG

The answer is not available in the provided context.

### Ground Truth

Come capri espiatori furono indicati emarginati, lebbrosi e soprattutto gli Ebrei, accusati di avvelenare l'acqua dei pozzi o di contaminare l'aria con veleni. Di conseguenza migliaia di ebrei subirono persecuzioni — i pogrom — in Francia, Germania e Svizzera.

---

## 16. Who was Joan of Arc and what role did she play in the Hundred Years' War?

*chi era Giovanna d'Arco e quale ruolo ebbe nella Guerra dei Cent'anni?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 9.7 ms | 4.8 ms (2.0x) |
| **Generazione** | 484 ms | 517 ms |
| **Totale** | 494 ms | 522 ms |
| **Pool chunk** | 118 | 7 |
| **Keyword hit** | 0% | 0% |

### Risposta StdRAG

The answer is not available in the provided context.

### Risposta SLM-RAG

The answer is not available in the provided context.

### Ground Truth

Giovanna d'Arco era una giovane contadina analfabeta della Champagne che affermava di sentire voci attribuite all'Arcangelo Michele. Presentatasi a Carlo VII, guidò l'esercito alla conquista di Orléans e il re fu incoronato a Reims. Fu catturata dagli inglesi e condannata al rogo per eresia a soli diciannove anni nella piazza di Rouen.

---

## 17. When did the Hundred Years' War start and end, and what caused it?

*quando iniziò e finì la Guerra dei Cent'anni e quale ne fu la causa?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 10.0 ms | 4.3 ms (2.3x) |
| **Generazione** | 452 ms | 379 ms |
| **Totale** | 462 ms | 383 ms |
| **Pool chunk** | 118 | 3 |
| **Keyword hit** | 0% | 0% |

### Risposta StdRAG

The answer is not available in the provided context.

### Risposta SLM-RAG

The answer is not available in the provided context.

### Ground Truth

La Guerra dei Cent'anni durò dal 1337 al 1453 non continuativamente. Fu scatenata dal tentativo di Filippo VI (Valois) di appropriarsi dei feudi inglesi sul suolo francese, provocando la reazione di Edoardo III d'Inghilterra.

---

## 18. How did Columbus persuade the Spanish monarchs to fund his voyage?

*come convinse Colombo i sovrani spagnoli a finanziare il suo viaggio?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 10.1 ms | 4.2 ms (2.4x) |
| **Generazione** | 478 ms | 379 ms |
| **Totale** | 488 ms | 383 ms |
| **Pool chunk** | 118 | 3 |
| **Keyword hit** | 0% | 0% |

### Risposta StdRAG

The answer is not available in the provided context.

### Risposta SLM-RAG

The answer is not available in the provided context.

### Ground Truth

Dopo il rifiuto del Portogallo, Colombo si rivolse a Isabella di Castiglia e Ferdinando d'Aragona. I sovrani, appena conclusa la Reconquista, accettarono attratti dalla possibilità di trovare oro nelle Indie per finanziare una nuova crociata. Il progetto era basato sulla teoria di Toscanelli secondo cui la Terra era sferica e si poteva raggiungere l'oriente navigando verso occidente.

---

## 19. From which port did Columbus depart and when?

*da quale porto partì Colombo e quando?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 9.6 ms | 4.5 ms (2.1x) |
| **Generazione** | 455 ms | 364 ms |
| **Totale** | 465 ms | 368 ms |
| **Pool chunk** | 118 | 3 |
| **Keyword hit** | 0% | 0% |

### Risposta StdRAG

The answer is not available in the provided context.

### Risposta SLM-RAG

The answer is not available in the provided context.

### Ground Truth

Il 3 agosto 1492 dal porto di Palos partirono tre caravelle: due di piccola stazza battezzate la Pinta e la Niña, e la nave ammiraglia Santa María.

---

## 20. Who was Henry the Navigator and what was his contribution to exploration?

*chi era Enrico il Navigatore e qual è il suo contributo all'esplorazione?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 10.2 ms | 4.7 ms (2.2x) |
| **Generazione** | 478 ms | 452 ms |
| **Totale** | 489 ms | 457 ms |
| **Pool chunk** | 118 | 5 |
| **Keyword hit** | 0% | 0% |

### Risposta StdRAG

The answer is not available in the provided context.

### Risposta SLM-RAG

The answer is not available in the provided context.

### Ground Truth

Enrico il Navigatore era il re del Portogallo che fondò una scuola nautica nella sua residenza di Capo di Sagres nell'Algarve. Lì si raccoglievano informazioni su maree, venti e sull'Oceano Atlantico. Favorì la sostituzione della galera con la più maneggevole caravella e avviò le esplorazioni portoghesi verso le Azzorre e la circumnavigazione dell'Africa.

---

## 21. Who was Bartolomeo Díaz and why did he not complete his voyage?

*chi era Bartolomeo Diaz e perché non completò il suo viaggio?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 10.0 ms | 4.3 ms (2.3x) |
| **Generazione** | 447 ms | 380 ms |
| **Totale** | 457 ms | 384 ms |
| **Pool chunk** | 118 | 3 |
| **Keyword hit** | 33% | 33% |

### Risposta StdRAG

The answer is not available in the provided context.

### Risposta SLM-RAG

The answer is not available in the provided context.

### Ground Truth

Bartolomeo Diaz era un ammiraglio portoghese che nel 1487 raggiunse il Capo di Buona Speranza ma non lo doppiò a causa dell'ammutinamento dei suoi marinai.

---

## 22. What was the triangular trade and why was it ethically problematic?

*cos'era il commercio triangolare e perché era eticamente problematico?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 9.6 ms | 4.5 ms (2.1x) |
| **Generazione** | 484 ms | 422 ms |
| **Totale** | 494 ms | 426 ms |
| **Pool chunk** | 118 | 5 |
| **Keyword hit** | 50% | 17% |

### Risposta StdRAG

The answer is not available in the provided context.

### Risposta SLM-RAG

The answer is not available in the provided context.

### Ground Truth

Il commercio triangolare prevedeva tre tappe: partenza dall'Europa con armi, alcol e suppellettili; sosta in Africa dove si acquistavano schiavi sfruttando le rivalità tribali; arrivo in America dove gli schiavi erano venduti in cambio di tabacco, cotone e canna da zucchero che tornavano in Europa. Generava enormi ricchezze ma pose le basi per la tratta degli schiavi, una grave ingiustizia storica.

---

## 23. What new food products did Europe import from the Americas after 1492?

*quali nuovi prodotti alimentari arrivarono in Europa dalle Americhe dopo il 1492?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 10.7 ms | 4.3 ms (2.5x) |
| **Generazione** | 1071 ms | 2046 ms |
| **Totale** | 1082 ms | 2050 ms |
| **Pool chunk** | 118 | 3 |
| **Keyword hit** | 100% | 100% |

### Risposta StdRAG

I nuovi prodotti alimentari arrivati in Europa dalle Americhe sono: il mais, il girasole, il peperone, la patata, il fagiolo, il pomodoro e il tabacco.

### Risposta SLM-RAG

I nuovi prodotti alimentari arrivati in Europa dalle Americhe dopo il 1492, secondo il contesto fornito, sono:

*   Mais
*   Girasole
*   Peperone
*   Patata
*   Fagiolo
*   Pomodoro
*   Tabacco

Inoltre, tra le specie animali trasferite dall'America all'Europa si ricordano il tacchino, il cincillà e il visone americano.

### Ground Truth

Tra i prodotti agricoli importati dall'America ricordiamo: mais, girasole, peperone, patata, fagiolo, pomodoro e tabacco. Tra le specie animali giunsero il tacchino, il cincillà, il visone americano e la trota arcobaleno.

---

## 24. What happened at the Diet of Augsburg in 1530?

*cosa accadde alla Dieta di Augusta del 1530?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 10.0 ms | 4.0 ms (2.5x) |
| **Generazione** | 460 ms | 379 ms |
| **Totale** | 470 ms | 383 ms |
| **Pool chunk** | 118 | 3 |
| **Keyword hit** | 17% | 17% |

### Risposta StdRAG

The answer is not available in the provided context.

### Risposta SLM-RAG

The answer is not available in the provided context.

### Ground Truth

Alla Dieta di Augusta del 1530 partecipò Filippo Melantone, portavoce di Lutero, che presentò la Confessione Augustana in cui furono ribadite le tesi luterane, sancendo la definitiva rottura con la dottrina cattolica. I principi tedeschi luterani avevano intanto costituito la Lega di Smalcalda in funzione anti-imperiale.

---

## 25. What did the Peace of Augsburg of 1555 establish?

*cosa stabilì la pace di Augusta del 1555?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 10.1 ms | 4.8 ms (2.1x) |
| **Generazione** | 525 ms | 448 ms |
| **Totale** | 535 ms | 452 ms |
| **Pool chunk** | 118 | 5 |
| **Keyword hit** | 0% | 0% |

### Risposta StdRAG

The answer is not available in the provided context.

### Risposta SLM-RAG

The answer is not available in the provided context.

### Ground Truth

La pace di Augusta del 1555 riconobbe ufficialmente la religione protestante e stabilì il principio 'cuius regio eius religio': ogni principe tedesco poteva scegliere la propria religione e i sudditi erano tenuti ad uniformarsi. A chi non volesse aderire era concesso il diritto di emigrare.

---

## 26. What was Calvin's doctrine of predestination?

*qual era la dottrina calvinista della predestinazione?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 10.3 ms | 3.9 ms (2.6x) |
| **Generazione** | 1712 ms | 1482 ms |
| **Totale** | 1722 ms | 1486 ms |
| **Pool chunk** | 118 | 3 |
| **Keyword hit** | 17% | 17% |

### Risposta StdRAG

Secondo il contesto fornito, la dottrina calvinista sulla predestinazione afferma che l'uomo, con la sua natura imperfetta, **non può salvarsi per fede**. Al contrario, è **Dio**, nella sua bontà imperscrutabile, a **predestinare l'uomo alla salvezza eterna**.

### Risposta SLM-RAG

Secondo il contesto fornito, la dottrina calvinista della predestinazione afferma che l'uomo, con la sua natura imperfetta, non può salvarsi per fede; è invece Dio, nella sua bontà imperscrutabile, a predestinare l'uomo alla salvezza eterna.

### Ground Truth

Calvino affermava la sovranità assoluta di Dio sull'uomo e la dottrina della predestinazione: l'umanità è divisa in eletti, destinati al Paradiso, e dannati. L'uomo con la sua natura imperfetta non può salvarsi per propria fede; è Dio a predestinarlo alla salvezza. Calvino riconobbe come sacramenti validi solo il battesimo e l'eucaristia.

---

## 27. What was England's Glorious Revolution?

*cos'era la Gloriosa Rivoluzione inglese?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 10.8 ms | 4.3 ms (2.5x) |
| **Generazione** | 517 ms | 416 ms |
| **Totale** | 527 ms | 421 ms |
| **Pool chunk** | 118 | 4 |
| **Keyword hit** | 40% | 20% |

### Risposta StdRAG

The answer is not available in the provided context.

### Risposta SLM-RAG

The answer is not available in the provided context.

### Ground Truth

La Gloriosa Rivoluzione inglese è descritta nel contesto del passaggio dall'assolutismo verso forme più costituzionali di governo in Inghilterra nel Seicento, in cui il parlamento limitò il potere assoluto del sovrano.

---

## 28. What were the main features of the First Industrial Revolution?

*quali furono le caratteristiche principali della Prima Rivoluzione Industriale?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 10.3 ms | 4.7 ms (2.2x) |
| **Generazione** | 5328 ms | 5226 ms |
| **Totale** | 5338 ms | 5231 ms |
| **Pool chunk** | 118 | 4 |
| **Keyword hit** | 100% | 50% |

### Risposta StdRAG

Le caratteristiche principali della Prima Rivoluzione Industriale, secondo il contesto fornito, sono:

*   **Nuove fonti di energia:** L'utilizzo della forza motrice dell'**acqua** e del **carbone**.
*   **Nuove tecnologie:**
    *   Nel settore tessile: perfezionamento del telaio (con spoletta mobile).
    *   Macchina a vapore costruita da **Watt**, usata in diversi ambiti.
    *   Locomotiva realizzata da **Stephenson** e nascita delle **ferrovie**.
*   **Cambiamento economico e sociale:**
    *   Passaggio da un'economia basata sull'agricoltura a un'economia basata sulle macchine e sul lavoro operaio.
    *   Nascita di nuove classi sociali e del **capitalismo**.
    *   Aumento degli scambi commerciali e delle materie prime (commercio triangolare).
    *   Miglioramenti nelle tecniche agricole (rotazioni, primi macchinari, recinzioni).
*   **Struttura del lavoro:**
    *   Lavoro parcellizzato e divisione dei compiti nelle fabbriche.
    *   S

### Risposta SLM-RAG

In base al contesto fornito, le caratteristiche principali della **Prima Rivoluzione Industriale** (definita nel testo come il periodo tra il 1770 e il 1850) sono:

*   **Origine e diffusione:** Si diffuse a partire dalla realtà economica e sociale in rapida crescita dell'Inghilterra, modificando mentalità e modi di vivere.
*   **Profondità del cambiamento:** Il termine "rivoluzione" indica un cambiamento profondo, paragonabile alla rivoluzione neolitica (passaggio dall'agricoltura alla civiltà urbana).
*   **Fattori sociali ed economici:**
    *   **Aumento demografico:** Favorito dalla tecnologia agricola e dai nuovi prodotti (in Inghilterra la popolazione raddoppiò in un secolo).
    *   **Crescita urbana:** Si formarono nuove città e quartieri, specialmente di operai impiegati nelle fabbriche.
    *   **Diffusione dell'informazione:** Nascita dei primi giornali (gazzette) e diffusione del sapere tra borghesia e ceti emergenti, sebbene con l'avvento della censura.
*   **Modifica del lavoro

### Ground Truth

La Prima Rivoluzione Industriale fu caratterizzata dall'introduzione di nuove tecnologie come la macchina a vapore di James Watt, dalla nascita della fabbrica come luogo di produzione accentrata, dall'uso massiccio del carbone e dalla trasformazione dei rapporti sociali con la nascita del proletariato operaio.

---

## 29. Who were the philosophes and what was their central idea?

*chi erano i philosophes e qual era la loro idea centrale?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 10.3 ms | 4.3 ms (2.4x) |
| **Generazione** | 417 ms | 361 ms |
| **Totale** | 427 ms | 365 ms |
| **Pool chunk** | 118 | 3 |
| **Keyword hit** | 0% | 50% |

### Risposta StdRAG

The answer is not available in the provided context.

### Risposta SLM-RAG

The answer is not available in the provided context.

### Ground Truth

I philosophes erano i pensatori dell'Illuminismo che sostenevano il primato del 'lume naturale' della ragione come strumento di conoscenza e critica della realtà sociale e politica. Proponevano una nuova visione dell'economia e della politica fondata sui diritti naturali e sul progresso.

---

## 30. Who was Catherine II of Russia and why is she considered an enlightened despot?

*chi era Caterina II di Russia e perché è considerata un despota illuminato?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 10.3 ms | 4.5 ms (2.3x) |
| **Generazione** | 2164 ms | 3314 ms |
| **Totale** | 2174 ms | 3319 ms |
| **Pool chunk** | 118 | 4 |
| **Keyword hit** | 40% | 40% |

### Risposta StdRAG

Caterina II di Russia è stata una sovrana che, insieme ad altri monarchi come Maria Teresa d'Austria e Federico II di Prussia, ha fatto parte del movimento del "despotismo illuminato" maturato nella seconda metà del Settecento. È considerata un despota illuminato per la sua mentalità aperta al riformismo illuminista e per l'accoglienza che ha rivolto ai filosofi, ospitandoli spesso nelle sue corti.

### Risposta SLM-RAG

Secondo il contesto fornito, **Caterina II di Russia** è una sovrana che, nella seconda metà del Settecento, ha cercato di "svecchiare la società" russa. È considerata un esempio di **despota illuminato** insieme a Maria Teresa d'Austria e Federico II di Prussia (soprannominati "re-filosofi") per la sua mentalità aperta al riformismo illuminista e per l'accoglienza rivolta ai filosofi, che spesso ospitava nelle loro corti.

Il contesto specifica inoltre che i sovrani illuminati, tra cui Caterina II, ebbero in comune l'intenzione di rendere più forte il potere dello stato nei confronti della nobiltà e della Chiesa.

### Ground Truth

Caterina II di Russia è descritta tra i cosiddetti 're filosofi', sovrani che cercarono di applicare i principi illuministi al governo mantenendo però il potere assoluto. È inserita, insieme a Giuseppe II d'Austria e Federico II di Prussia, tra i rappresentanti del dispotismo illuminato.

---

## 31. What were the economic causes of the French Revolution?

*quali furono le cause economiche della Rivoluzione Francese?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 9.8 ms | 4.0 ms (2.4x) |
| **Generazione** | 4487 ms | 5260 ms |
| **Totale** | 4497 ms | 5264 ms |
| **Pool chunk** | 118 | 4 |
| **Keyword hit** | 20% | 100% |

### Risposta StdRAG

In base al contesto fornito, le cause economiche della Rivoluzione Francese sono:

*   **Crisi agraria e carestie:** Nel 1788 si verificarono carestie e raccolti esigui dovuti ai "capricci del clima", che causarono un aumento immediato del prezzo del pane.
*   **Situazione della terra:** La terra costituiva la principale fonte di reddito in Francia, rendendo le popolazioni vulnerabili alle fluttuazioni dei raccolti.
*   **Modello dell'Ancien Régime:** Il contesto economico era caratterizzato da impostazioni medioevali, tra cui la monarchia assoluta, una società divisa in rigidi ordini sociali e la persistenza di diritti feudali.

Il testo non elenca altre cause economiche specifiche per la Francia, concentrandosi invece su fattori morali, politici e demografici, o su eventi economici di altri paesi (come la Rivoluzione Industriale in Inghilterra o la Riforma in Germania).

### Risposta SLM-RAG

Le cause economiche della Rivoluzione Francese, secondo il contesto fornito, sono:

*   **Crisi agraria e carestie:** La terra era la principale fonte di reddito, ma i "capricci del clima" provocavano raccolti esigui (come nel 1788), portando a carestie e all'aumento del prezzo del pane.
*   **Debito pubblico:** La Francia affrontava una pesante crisi economica e un debito significativo.
*   **Politica fiscale iniqua:** Il sistema dell'Ancien Regime era basato su una società divisa in rigidi ordini sociali con persistenza di diritti feudali. I proprietari terrieri e l'aristocrazia godevano di privilegi, mentre il Terzo Stato (la borghesia e i contadini) sopportava il peso delle imposte.
*   **Misure fiscali repressive:** Tentativi di reperire risorse, come la tassa sulle terre introdotta da Jacques Turgot, hanno alienato le simpatie dei proprietari terrieri e aggravato le tensioni sociali.
*   **Spesa pubblica eccessiva:** Il lusso della corte e le uscite statali ingenti, spesso coperte da

### Ground Truth

La crisi economica è individuata come una delle principali premesse della Rivoluzione Francese. L'Ancien Régime era caratterizzato da privilegi fiscali per nobiltà e clero, mentre il peso delle tasse gravava sul terzo stato. La convocazione degli Stati Generali fu una risposta diretta a questa crisi finanziaria.

---

## 32. When was the Bastille stormed and what did it symbolize?

*quando fu presa la Bastiglia e cosa simboleggiò?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 9.5 ms | 3.9 ms (2.4x) |
| **Generazione** | 1915 ms | 460 ms |
| **Totale** | 1925 ms | 464 ms |
| **Pool chunk** | 118 | 7 |
| **Keyword hit** | 67% | 0% |

### Risposta StdRAG

La Bastiglia fu presa il **14 luglio 1789**. Simboleggia l'inizio di un periodo di **riforme** e l'esplosione di **fermenti popolari** che sfociarono nell'assalto alla prigione, segnando l'inizio della fase di riforme in cui la Monarchia divenne **costituzionale**.

### Risposta SLM-RAG

The answer is not available in the provided context.

### Ground Truth

La Bastiglia fu presa il 14 luglio 1789. L'evento rappresentò una svolta simbolica della Rivoluzione Francese, segnando il passaggio dall'azione delle assemblee all'azione popolare diretta contro il potere monarchico.

---

## 33. What was the War of the Vendée during the French Revolution?

*cos'era la guerra della Vandea durante la Rivoluzione Francese?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 9.8 ms | 4.6 ms (2.1x) |
| **Generazione** | 2681 ms | 2605 ms |
| **Totale** | 2691 ms | 2610 ms |
| **Pool chunk** | 118 | 4 |
| **Keyword hit** | 80% | 80% |

### Risposta StdRAG

La guerra della Vandea fu una rivolta scoppiata nelle campagne francesi durante la Rivoluzione Francese. Essa fu causata dall'arruolamento di massa di 300.000 uomini deciso dalla Convenzione, che creò un forte malcontento perché mancava già la manodopera necessaria per il raccolto. La rivolta si diffuse nella Vandea, una regione dove il consenso e l'attaccamento alla Chiesa erano molto forti. La Convenzione reagì con durezza reprimendo ogni manifestazione fino a sottomettere chi si opponeva.

### Risposta SLM-RAG

La guerra della Vandea fu una rivolta scoppiata nelle campagne francesi durante la Rivoluzione Francese, causata dall'arruolamento di massa di 300.000 uomini (leva di massa) che creò un grave malcontento per la mancanza di manodopera necessaria al raccolto. La rivolta si insediò nella regione della **Vandea**, dove il consenso e l'attaccamento alla Chiesa erano molto forti. La Convenzione reagì con durezza reprimendo ogni manifestazione fino a sottomettere i ribelli.

### Ground Truth

La guerra della Vandea fu una delle difficoltà interne della Rivoluzione Francese: un conflitto civile che oppose i rivoluzionari a una parte della popolazione francese — in particolare contadini e fedeli alla monarchia e alla Chiesa — nella regione della Vandea.

---

## 34. What were Napoleon's main military campaigns and how did his empire end?

*quali furono le principali campagne di Napoleone e come finì il suo impero?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 10.1 ms | 4.3 ms (2.3x) |
| **Generazione** | 4606 ms | 5273 ms |
| **Totale** | 4616 ms | 5278 ms |
| **Pool chunk** | 118 | 4 |
| **Keyword hit** | 33% | 33% |

### Risposta StdRAG

In base al contesto fornito, le informazioni disponibili sono le seguenti:

**Sulle principali campagne:**
Il testo menziona specificamente la **campagna d'Italia del 1796**, che mise in luce le capacità militari di Napoleone e lo portò a diventare rapidamente il generale più valido nel difendere la Francia e i suoi ideali rivoluzionari. Non vengono elencate altre campagne specifiche nel testo.

**Su come finì il suo impero:**
L'impero di Napoleone finì con la sua **ultima pesante sconfitta a Waterloo**, avvenuta il **18 giugno 1815**. Dopo questa sconfitta, Napoleone fu costretto all'esilio sulla lontana isola di **Sant'Elena** nell'Atlantico, dove morì il **5 maggio 1821**. Parallelamente, le nazioni europee si riunirono a Vienna per un congresso che avviò la **Restaurazione**, con lo scopo di ristabilire le condizioni politiche precedenti alle imprese napoleoniche.

### Risposta SLM-RAG

In base al contesto fornito, le principali campagne e la fine dell'impero di Napoleone sono descritte come segue:

**Principali campagne:**
*   **Campagna di Russia (1812):** Napoleone iniziò questa campagna dopo che la Russia si dissocia dal blocco continentale contro gli Inglesi. La campagna si concluse con una rapida conquista del territorio russo, ma i francesi furono obbligati a una "ritirata invernale disastrosa".
*   **Guerre contro le coalizioni antifrancesi:** Il testo menziona una serie di guerre e interventi militari vinti dal genio strategico di Napoleone che portarono quasi tutta l'Europa in una situazione di subalternità alla Francia (intorno al 1810).
*   **Seconda guerra d'Indipendenza (1859):** Sebbene il testo descriva questa guerra come un evento successivo al suo impero (dove Napoleone III, suo nipote, comandò le truppe franco-piemontesi vincendo a Palestro, Magenta, Solferino e San Martino), è l'unico conflitto specifico dettagliato nel testo.

**Come finì il suo

### Ground Truth

Napoleone condusse la campagna d'Italia con la nascita delle Repubbliche, la campagna d'Egitto che ne accelerò l'ascesa politica, poi instaurò il Consolato e l'Impero estendendo l'egemonia sull'Europa. La conquista di Mosca segnò l'inizio del declino; l'impero si concluse con la sconfitta definitiva e l'esilio sull'isola di Sant'Elena.

---

## 35. What did the Congress of Vienna decide and who were its main actors?

*cosa stabilì il Congresso di Vienna e chi ne furono i protagonisti?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 10.8 ms | 4.7 ms (2.3x) |
| **Generazione** | 5363 ms | 5328 ms |
| **Totale** | 5374 ms | 5333 ms |
| **Pool chunk** | 118 | 5 |
| **Keyword hit** | 80% | 40% |

### Risposta StdRAG

In base al contesto fornito, ecco la risposta:

**Cosa stabilì il Congresso di Vienna:**
Il Congresso decise di riportare l'ordine in Europa ripristinando quasi la situazione precedente alla Rivoluzione (*Ancien Regime*). I principi fondamentali stabiliti furono:
*   **Equilibrio:** limitare i 4 stati più potenti e creare stati cuscinetto.
*   **Legittimità:** al governo devono tornare i re precedenti alla Rivoluzione.
*   **Interventismo:** reprimere insurrezioni o colpi di stato con l'esercito.

Le conseguenze di queste decisioni includevano:
*   La nascita della Confederazione Germanica.
*   L'annessione parziale della Polonia dalla Russia.
*   Il consolidamento della presenza austriaca al Nord Italia e l'unificazione del Regno delle due Sicilie (Borboni).
*   Il ritorno dello Stato Pontificio ai confini precedenti.
*   La dichiarazione illegale della tratta degli schiavi.
*   La nascita di sistemi di alleanze per evitare nuove rivoluzioni: la Santa Alleanza e la Quadruplice Alleanza.

**Chi ne furono i protagonisti:**
I principali

### Risposta SLM-RAG

In base al contesto fornito, ecco la risposta:

**Cosa stabilì il Congresso di Vienna:**
Il Congresso decise di convocare un incontro per riportare l'ordine in Europa e ripristinare quasi la situazione precedente alla Rivoluzione (l'Ancien Regime), definendo il periodo successivo come "Restaurazione" (dal 1815 al 1848).

**Chi ne furono i protagonisti:**
I principali artefici delle decisioni furono i ministri degli esteri:
*   **Lord Castlereagh** (per la Gran Bretagna);
*   **Von Metternich** (per l'Austria);
*   **Talleyrand** (per la Francia, abile diplomatico che difese gli interessi della sua nazione).

Altri partecipanti che intervennero di persona o con grande rilievo furono:
*   Lo zar **Alessandro I** (Russia);
*   I quattro grandi poteri che avevano sconfitto Napoleone: **Austria, Russia, Prussia e Gran Bretagna**.

Il Congresso si tenne dal novembre 1814 al giugno 1815 e vide la partecipazione di 216 delegati in rappresentanza di vari paesi

### Ground Truth

Il Congresso di Vienna stabilì un nuovo assetto europeo volto a restaurare l'ordine precedente alla Rivoluzione Francese e alle conquiste napoleoniche. Portò alla creazione della Santa Alleanza tra le potenze conservatrici. I protagonisti furono i rappresentanti delle grandi potenze europee vincitrici su Napoleone.

---

## 36. Who was Mazzini and what was the Giovine Italia?

*chi era Mazzini e cos'era la Giovine Italia?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 10.5 ms | 4.8 ms (2.2x) |
| **Generazione** | 4380 ms | 4309 ms |
| **Totale** | 4391 ms | 4314 ms |
| **Pool chunk** | 118 | 9 |
| **Keyword hit** | 80% | 100% |

### Risposta StdRAG

Secondo il contesto fornito, **Mazzini** era un genovese di famiglia agiata, inizialmente aderente alla Carboneria, che si rese conto che la segretezza dei suoi fini era un elemento limitante. Egli fondò la **Giovine Italia** per divulgare le sue finalità di unificazione dell'Italia sotto forma repubblicana, unendo la politica a una personale visione religiosa. I suoi motti erano "Dio e Popolo" e "Pensiero e Azione".

La **Giovine Italia** era l'associazione fondata da Mazzini che si diffuse soprattutto nel nord del paese. Il suo obiettivo era l'unificazione dell'Italia sotto una repubblica, senza intervento della monarchia. Tra i suoi aderenti vi fu anche il giovane Giuseppe Garibaldi. L'associazione utilizzava come bandiera quella tricolore rossa, bianca e verde a strisce orizzontali con la scritta centrale "unione, forza, libertà" su sfondo bianco.

### Risposta SLM-RAG

Secondo il contesto fornito, **Mazzini** era un genovese di famiglia agiata, inizialmente aderente alla Carboneria, che si rese conto che la segretezza dei suoi fini era un elemento limitante. Egli fondò la **Giovine Italia** per divulgare le sue finalità di unificazione dell'Italia sotto forma repubblicana, unendo la politica a una personale visione religiosa. I suoi motti erano "Dio e Popolo" e "Pensiero e Azione".

La **Giovine Italia** era l'associazione fondata da Mazzini che si diffuse soprattutto nel nord del paese. Il suo obiettivo era l'unificazione dell'Italia sotto una repubblica, senza intervento della monarchia. La sua bandiera era rossa, bianca e verde a strisce orizzontali con la scritta centrale "unione, forza, libertà" su sfondo bianco. Tra i suoi aderenti vi fu anche il giovane Giuseppe Garibaldi.

### Ground Truth

Giuseppe Mazzini fu uno dei principali protagonisti del Risorgimento e fondatore della Giovine Italia, un'associazione che propugnava l'indipendenza e l'unificazione dell'Italia come nazione libera e repubblicana, ispirata al motto 'Dio e Popolo'.

---

## 37. What was Cavour's role in the unification of Italy?

*quale fu il ruolo di Cavour nell'unificazione d'Italia?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 9.7 ms | 4.7 ms (2.0x) |
| **Generazione** | 5407 ms | 5345 ms |
| **Totale** | 5417 ms | 5350 ms |
| **Pool chunk** | 118 | 7 |
| **Keyword hit** | 60% | 60% |

### Risposta StdRAG

In base al contesto fornito, il ruolo di Cavour nell'unificazione d'Italia può essere sintetizzato nei seguenti punti:

*   **Architetto politico e riformatore:** Cavour è descritto come un "nobile imprenditore" e politico **liberale** che ha guidato il Piemonte verso la modernizzazione. Ha attuato riforme significative in ambito agricolo, industriale e infrastrutturale (creazione della prima rete ferroviaria italiana), garantendo i diritti individuali e promuovendo il **liberismo** economico.
*   **Separazione dalla Chiesa:** Ha cercato una netta separazione tra Stato e Chiesa, proponendo il principio della "libera chiesa in libero stato" e riducendo l'ingerenza ecclesiastica attraverso leggi come quelle Siccardi.
*   **Controllo del movimento patriottico:** Per ridurre l'influenza di Mazzini e le sue idee repubblicane, ha fondato la **Società Nazionale Italiana**, un'organizzazione che proiettava l'unità d'Italia ma sotto il controllo della casa Savoia.
*   **Diplomazia e alleanze:** Ha compreso che l'Italia non poteva unificarsi senza supporto internazionale.

### Risposta SLM-RAG

In base al contesto fornito, il ruolo di Cavour nell'unificazione d'Italia fu quello di un abile politico e primo ministro italiano che adottò una strategia **liberale** ed economica basata sul **liberismo**, puntando sull'intervento armato della casa Savoia per l'unificazione piuttosto che su iniziative rivoluzionarie come quelle di Mazzini.

I punti chiave del suo ruolo sono:
*   **Diplomazia e alleanze:** Comprendendo che l'Italia non poteva modificare la situazione senza aiuti internazionali, ottenne il credito di Francia e Inghilterra inviando l'esercito piemontese in Crimea (1853).
*   **Patto di Plombières:** Nel 1858, dopo un attentato a Napoleone III, concluse un accordo segreto con l'imperatore francese per un intervento francese a fianco del Regno di Sardegna in caso di guerra austriaca, ottenendo in cambio Nizza e la Savoia.
*   **Seconda guerra d'Indipendenza (1859):** Guidò la politica estera che portò alla guerra contro l'Austria, ottenendo l'annessione della Lombardia e cedendo

### Ground Truth

Camillo Benso conte di Cavour fu la figura politica centrale del processo di unificazione. Attuò riforme nel Regno di Sardegna, condusse una politica estera che portò all'alleanza con la Francia, guidò la Seconda guerra d'Indipendenza e creò le condizioni diplomatiche per la Spedizione dei Mille di Garibaldi.

---

## 38. What was Taylorism and in what historical context did it emerge?

*cos'era il Taylorismo e in quale contesto storico nacque?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 10.0 ms | 4.4 ms (2.3x) |
| **Generazione** | 461 ms | 482 ms |
| **Totale** | 471 ms | 486 ms |
| **Pool chunk** | 118 | 5 |
| **Keyword hit** | 17% | 33% |

### Risposta StdRAG

The answer is not available in the provided context.

### Risposta SLM-RAG

The answer is not available in the provided context.

### Ground Truth

Il Taylorismo fu un sistema di organizzazione scientifica del lavoro sviluppato durante la Seconda Rivoluzione Industriale. Rappresentò una nuova forma di razionalizzazione della produzione in fabbrica, finalizzata ad aumentare la produttività attraverso la standardizzazione dei compiti operai.

---

## 39. What was the Monroe Doctrine and in what context was it issued?

*cos'era la dottrina Monroe e in quale contesto fu proclamata?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 9.5 ms | 5.3 ms (1.8x) |
| **Generazione** | 2070 ms | 2808 ms |
| **Totale** | 2079 ms | 2814 ms |
| **Pool chunk** | 118 | 6 |
| **Keyword hit** | 67% | 67% |

### Risposta StdRAG

La dottrina Monroe fu proclamata dal Presidente Monroe nel 1800 (secondo il contesto fornito) e consisteva nel dichiarare che gli interessi dell'America spettavano esclusivamente agli americani, opponendosi alle ingerenze dell'Europa. Questa dottrina segnò il taglio del "cordone ombelicale" con la vecchia Europa e legittimò agli Stati Uniti una politica di egemonia su tutto il continente.

### Risposta SLM-RAG

La dottrina Monroe fu proclamata dal Presidente Monroe nel contesto dell'espansione degli Stati Uniti verso ovest (il "mitico west") che iniziò nel 1800, portando alla distruzione dei pellirossa e all'aumento della popolazione a causa dei coloni provenienti dall'Europa. In quel periodo, l'economia americana era ben distinta: industriale nel Nord e agricola nel Sud, e gli stati erano ormai 27.

La dottrina dichiarava che gli interessi dell'America spettavano esclusivamente agli americani, ponendosi in opposizione alle ingerenze dell'Europa.

### Ground Truth

La dottrina Monroe fu proclamata nell'ambito delle lotte per l'indipendenza dell'America latina e dei moti liberali. Affermava il principio che l'America non doveva essere considerata campo di ulteriore colonizzazione europea, opponendosi all'interventismo delle potenze del Vecchio Continente nelle Americhe.

---

## 40. How were the price revolution of the 16th century and the geographical discoveries connected?

*come erano collegati la rivoluzione dei prezzi del Cinquecento e le scoperte geografiche?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 9.7 ms | 4.3 ms (2.2x) |
| **Generazione** | 2381 ms | 426 ms |
| **Totale** | 2391 ms | 430 ms |
| **Pool chunk** | 118 | 4 |
| **Keyword hit** | 100% | 17% |

### Risposta StdRAG

Le scoperte geografiche, in particolare l'importazione di enormi quantità di oro e di argento dalle Americhe da parte della Spagna e del Portogallo, furono la causa principale della **rivoluzione dei prezzi** del Cinquecento.

Secondo l'interpretazione di Jean Bodin citata nel contesto, l'afflusso di queste grandi quantità di metalli preziosi causò la perdita di valore della moneta, portando all'inflazione che divorò il potere d'acquisto dei salariati.

### Risposta SLM-RAG

The answer is not available in the provided context.

### Ground Truth

Nel Cinquecento i prezzi subirono un incremento di circa il 400%. Il pensatore Jean Bodin spiegò il fenomeno sostenendo che l'importazione massiccia di oro e argento dalle Americhe da parte di Spagna e Portogallo aveva causato la svalutazione della moneta. I salariati furono i più penalizzati, poiché l'inflazione erose il loro già esiguo potere d'acquisto.

---

