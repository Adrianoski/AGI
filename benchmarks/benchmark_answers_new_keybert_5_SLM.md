# Benchmark RAG — STORIAZ

**Modello:** Qwen/Qwen3.5-4B  |  **top-k:** 5  |  **top-N SLM:** 5

| Metrica | StdRAG | SLM-RAG |
|---|---|---|
| Speedup retrieval | — | **2.3x** |
| Pool medio | 181 chunk | 9 chunk (-95%) |
| Keyword hit | 52% | **48%** |
| Overlap medio top-5 | 38% | — |

---

## 1. Who imported spices into Europe during the Middle Ages?

*da chi venivano importate le spezie in europa nel medioevo?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 17.8 ms | 6.2 ms (2.9x) |
| **Generazione** | 4120 ms | 442 ms |
| **Totale** | 4137 ms | 448 ms |
| **Pool chunk** | 181 | 6 |
| **Keyword hit** | 100% | 100% |

### Risposta StdRAG

Dall'Oriente.

### Risposta SLM-RAG

Dall'Oriente.

### Ground Truth

Il commercio delle spezie era controllato dai mercanti arabi insieme alla repubblica veneziana, che detenevano il monopolio attraversando i territori musulmani. I molteplici rischi del viaggio e i vari passaggi di mano aumentavano considerevolmente il prezzo della merce.

---

## 2. What territories did Charles V control?

*quali territori controllava Carlo V?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 16.0 ms | 6.0 ms (2.7x) |
| **Generazione** | 4105 ms | 2925 ms |
| **Totale** | 4121 ms | 2931 ms |
| **Pool chunk** | 181 | 6 |
| **Keyword hit** | 33% | 50% |

### Risposta StdRAG

In base al contesto fornito, i territori controllati da Carlo V includono:

*   Il **Ducato di Milano** (riprese il controllo alla morte di Francesco Sforza).
*   L'**Impero** (descritto come "enorme e complesso", che includeva i territori del **nuovo mondo**).
*   Il **Portogallo** (la cui sede era vacante).
*   Gran parte dell'**Italia** (segna il predominio spagnolo su gran parte dell'Italia dopo la pace di Cateau-Cambresis).
*   I territori che facevano parte dell'**Impero Spagnolo nel 1598** (menzionati in un'immagine di riferimento).

Il testo non elenca in modo esaustivo ogni singolo stato o regione specifica oltre a questi gruppi generali (Nuovo Mondo, Portogallo, Ducato di Milano, Italia, Impero).

### Risposta SLM-RAG

In base al contesto fornito, Carlo V controllava un impero enorme e complesso che includeva:

*   I **territori del nuovo mondo**.
*   Il **Portogallo** (la cui sede era vacante).
*   **Gran parte dell'Italia**, che era considerata un luogo strategico per il dominio spagnolo.

Il testo specifica che dopo la pace di Cateau-Cambresis (1559), il predominio spagnolo su gran parte dell'Italia era consolidato, e che sotto il suo figlio Filippo II questi territori (insieme al nuovo mondo e al Portogallo) facevano parte dell'impero.

### Ground Truth

Carlo V controllava un vasto impero che comprendeva la Spagna, i territori asburgici, le Fiandre, il Regno di Napoli e le colonie americane. Il suo regno fu segnato da conflitti con la Francia, i principi tedeschi luterani e l'impero ottomano.

---

## 3. What were the main causes of the French Revolution?

*quali furono le cause della rivoluzione francese?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 16.8 ms | 6.8 ms (2.5x) |
| **Generazione** | 3100 ms | 5284 ms |
| **Totale** | 3117 ms | 5291 ms |
| **Pool chunk** | 181 | 6 |
| **Keyword hit** | 50% | 50% |

### Risposta StdRAG

The answer is not available in the provided context.

The provided text discusses the causes of the **Reformation** (e.g., moral decay of the papal court, Emperor Charles V's ambitions, peasant equality, indulgences) and the causes of the **French Revolution** only in a very general sense, mentioning the "crisis agraria" (agricultural crisis), "carestie" (famines), "capiucci del clima" (capriccio of the climate), and the "ancien regime" (absolute monarchy, rigid social orders, feudal rights). However, it does not provide a comprehensive list or detailed explanation of the specific causes of the French Revolution as requested.

### Risposta SLM-RAG

In base al contesto fornito, le cause della Rivoluzione Francese sono:

*   **Crisi economica e sociale:** La popolazione contadina era colpita dalla crisi e dalle piogge, mentre gli operai venivano espulsi dalle industrie a causa della sovrapproduzione, chiedendo misure contro la disoccupazione che significava fame e miseria.
*   **Rottura con la Chiesa:** La confisca dei beni del clero e lo scioglimento degli ordini religiosi (eccettuati quelli di assistenza e istruzione) portarono a una rottura di rapporti con il clero e la Chiesa, creando disagio in molti cittadini.
*   **Intervento militare straniero:** Gli stati europei sembravano pronti a un intervento militare in favore della monarchia francese per ristabilire l'ordine, il che portò alla guerra contro l'Austria e la Prussia, mettendo in difficoltà l'esercito francese.
*   **Insurrezione popolare:** Il popolo di Parigi insorse contro il proprio sovrano, assaltando le Tuileries e deponendo il re.

Il testo non elenca cause specifiche come la disuguaglianza fiscale o l'assolutismo del re,

### Ground Truth

Le principali cause della Rivoluzione Francese furono la crisi economica dell'Ancien Régime, le ingiustizie fiscali che gravavano sul terzo stato, la convocazione degli Stati Generali e la crescente influenza dell'opinione pubblica. La nobiltà e il clero godevano di privilegi fiscali che alimentavano il malcontento popolare.

---

## 4. How did James Watt's steam engine work?

*come funzionava la macchina a vapore di james watt?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 15.5 ms | 7.0 ms (2.2x) |
| **Generazione** | 501 ms | 478 ms |
| **Totale** | 517 ms | 485 ms |
| **Pool chunk** | 181 | 5 |
| **Keyword hit** | 67% | 83% |

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
| **Retrieval** | 15.3 ms | 6.5 ms (2.3x) |
| **Generazione** | 4476 ms | 4645 ms |
| **Totale** | 4491 ms | 4651 ms |
| **Pool chunk** | 181 | 6 |
| **Keyword hit** | 67% | 50% |

### Risposta StdRAG

In base al contesto fornito, i principi fondamentali dell'Illuminismo sono:

*   **La ragione:** È il "lume" naturale dell'uomo che lo sollecita a svincolarsi dalle tradizioni e dai pregiudizi per affermare un nuovo modo di guardare la realtà, la società, la politica, la cultura e la religione.
*   **Il coraggio di usare la propria intelligenza:** Espresso dal motto di Kant *Sapere aude* ("Abbi il coraggio di servirti della tua intelligenza").
*   **La libertà:** Come dimostrato dalla nascita degli Stati Uniti, un stato non legato alle tradizioni storiche dell'Europa ma basato sulla libertà.
*   **I diritti del singolo e del popolo:** L'Illuminismo difende questi diritti contro il despotismo delle autorità.
*   **L'uscita dallo stato di minorità:** Definizione data da Kant, che indica l'uomo che deve imputare a se stesso la sua condizione di minorità.

### Risposta SLM-RAG

In base al contesto fornito, i principi fondamentali dell'Illuminismo sono:

*   **La ragione:** È il "lume" naturale dell'uomo che sollecita a svincolarsi dalle tradizioni e dai pregiudizi.
*   **L'affermazione di un nuovo modo di guardare la realtà:** Questo include la società, la politica, la cultura e la religione.
*   **Il coraggio di usare la propria intelligenza:** Espresso dal motto di Kant "Sapere aude" (Abbi il coraggio di servirti della tua intelligenza).
*   **La libertà:** Un principio chiave per lo stato americano, non legato alle tradizioni storiche dell'Europa.
*   **Il diritto:** Come forza utilizzata dal popolo americano per sconfiggere la Gran Bretagna.
*   **Il riformismo illuminista:** Una mentalità aperta al cambiamento, adottata da sovrani come Caterina II, Maria Teresa e Federico II, che cercavano di rendere più forte il potere dello stato nei confronti della nobiltà e della Chiesa.

### Ground Truth

L'Illuminismo si fondava sul primato del 'lume naturale' della ragione come strumento di conoscenza e critica della realtà. I philosophes propugnavano una nuova visione dell'economia e della politica basata sulla libertà, sul progresso e sui diritti naturali dell'individuo.

---

## 6. What was the American Revolution?

*che cosa fu la rivoluzione americana?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 15.6 ms | 5.8 ms (2.7x) |
| **Generazione** | 1915 ms | 4725 ms |
| **Totale** | 1931 ms | 4731 ms |
| **Pool chunk** | 181 | 6 |
| **Keyword hit** | 50% | 100% |

### Risposta StdRAG

The answer is not available in the provided context.

While the context mentions "LA RIVOLUZIONE AMERICANA" in the table of contents in Chunk 2 and lists sub-sections regarding the situation of American colonists, economic relations with the mother country, and the path from war to the Declaration of Independence, it does not provide a description or definition of what the American Revolution was.

### Risposta SLM-RAG

La rivoluzione americana fu un conflitto che portò alla nascita del nuovo stato federale degli Stati Uniti d'America, sancito dalla pace di Parigi del 1783. Il conflitto iniziò con il boicottaggio delle merci inglesi (incluso il gesto del Boston Tea Party) e le ostilità tra inglesi e americani, dove inizialmente le forze inglesi, meglio organizzate, prevalsero, ma poi prevalsero le vittorie dei coloni guidati da G. Washington, grazie anche agli interventi di Francia e Spagna.

La rivoluzione si basò sui principi dell'Illuminismo, che difendono i diritti del singolo e del popolo contro il despotismo delle autorità. Gli americani cercavano una maggiore libertà e indipendenza, una concreta libertà religiosa e la salvaguardia dei diritti individuali. Dopo la Dichiarazione di Indipendenza del 1776 e la sconfitta inglese, le 13 colonie divennero cittadini legati alla madrepatria ma in ricerca di maggior libertà, portando alla fine del controllo inglese e alla formazione di uno stato federale.

### Ground Truth

La Rivoluzione Americana fu il processo con cui le tredici colonie americane si ribellarono al dominio inglese, principalmente a causa delle difficili condizioni economiche e fiscali imposte dalla madrepatria. Nel 1776 fu stilata la Dichiarazione d'Indipendenza; la sconfitta inglese fu sancita dalla pace di Parigi del 1783, che diede vita al nuovo stato federale americano.

---

## 7. Who were the Mongols and how did they expand?

*chi erano i mongoli e come si espansero?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 15.2 ms | 6.2 ms (2.4x) |
| **Generazione** | 2183 ms | 4852 ms |
| **Totale** | 2198 ms | 4858 ms |
| **Pool chunk** | 181 | 7 |
| **Keyword hit** | 50% | 83% |

### Risposta StdRAG

The answer is not available in the provided context.

While the context mentions "La via della seta: i Mongoli" (The Silk Road: The Mongols) as a section title in Chunk 1, it does not provide any description of who the Mongols were or how they expanded. The text in Chunk 2 discusses the history of spice trade, Arab merchants, and the Venetian Republic, but does not mention the Mongols.

### Risposta SLM-RAG

Secondo il contesto fornito, i mongoli erano un esercito composto da cavalieri addestrati e pronti a tutto, noti per la loro ferocia nei combattimenti, che li rendeva assai temuti dagli europei (venivano chiamati "Tartari").

Si espansero in modo rapido e continuo attraverso le seguenti tappe:
*   **Gengis Khan** scatenò l'offensiva verso la Cina, superando la Grande Muraglia, occupò le steppe della Russia meridionale (conquistando Samarcanda e Bukara) e si rivolse verso la Persia, la Georgia e la Bulgaria.
*   Dopo la sua morte, i suoi successori continuarono l'espansione arrivando a Baghdad (nel 1258) e in Polonia, dove sconfissero la cavalleria polacco-tedesca e conquistarono l'Ungheria.
*   Il regno di Gengis Khan fu poi diviso tra i suoi quattro figli, dando origine a quattro Khanati, tra cui quello del Gran Khan in Cina.

### Ground Truth

I Mongoli erano un popolo di cavalieri guidati da Gengis Khan, che scatenò la sua offensiva verso la Cina oltrepassando la Grande Muraglia, poi occupò le steppe della Russia meridionale, conquistò Samarcanda e Bukara e attaccò Persia, Georgia e Bulgaria. Erano chiamati Tartari dagli europei. Dopo la sua morte il regno fu diviso tra i quattro figli, dando origine a quattro Khanati.

---

## 8. What was Luther's Protestant Reformation?

*che cosa fu la riforma protestante di lutero?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 15.2 ms | 5.6 ms (2.7x) |
| **Generazione** | 2769 ms | 2774 ms |
| **Totale** | 2785 ms | 2779 ms |
| **Pool chunk** | 181 | 6 |
| **Keyword hit** | 100% | 100% |

### Risposta StdRAG

La Riforma protestante di Lutero fu un movimento iniziato da Martin Lutero, monaco e studioso, che si sviluppò a partire dalla sua pubblicazione delle 95 tesi contro le indulgenze e la dottrina tradizionale della Chiesa cattolica. Lutero affermò che per la salvezza dell'anima basta la sola fede e che ogni individuo dispone del libero arbitrio per leggere e interpretare personalmente la Bibbia. Questo cambiamento radicale fu facilitato dalla diffusione della stampa. La Chiesa cattolica reagì scomunicando Lutero nel 1520, dando inizio alla Riforma.

### Risposta SLM-RAG

La riforma protestante di Lutero fu un movimento iniziato da Martin Lutero, monaco e studioso, che sentì fortemente il problema della salvezza dell'anima. Lutero pubblicò le 95 tesi contro le indulgenze e la dottrina tradizionale, affermando che **la sola fede** basta per la salvezza e che ognuno dispone del **libero arbitrio** per leggere e interpretare personalmente la Bibbia. Questo cambiamento radicale fu facilitato dalla diffusione della stampa. La Chiesa cattolica rispose con la scomunica nel 1520, dando inizio alla Riforma.

### Ground Truth

La Riforma protestante di Lutero segnò una rottura definitiva con la dottrina cattolica, ribadita nella Confessione Augustana presentata da Filippo Melantone alla Dieta di Augusta del 1530. La pace di Augusta del 1555 riconobbe ufficialmente la religione protestante stabilendo il principio 'cuius regio eius religio'.

---

## 9. How was the Italian state formed during the Risorgimento?

*come si formò lo stato italiano nel risorgimento?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 15.6 ms | 7.2 ms (2.2x) |
| **Generazione** | 5325 ms | 5290 ms |
| **Totale** | 5341 ms | 5297 ms |
| **Pool chunk** | 181 | 13 |
| **Keyword hit** | 50% | 100% |

### Risposta StdRAG

In base al contesto fornito, la formazione dello Stato italiano nel Risorgimento si può riassumere come segue:

Il termine **Risorgimento** indica il complesso di eventi, dottrine politiche e iniziative che condussero, a partire dal **1861**, al processo di **unificazione dell'Italia**. Questo processo ebbe come obiettivo la rinascita spirituale del concetto di **nazione**, con la fine dell'occupazione straniera e l'unificazione dei vari regni interni, condizione che l'Italia aveva vissuto per secoli.

Il nuovo Stato italiano nacque nel **1861**. La sua costituzione fu caratterizzata da una serie di scelte politiche e amministrative che, sebbene abbiano unito il territorio, generarono forti tensioni sociali, specialmente nel Sud Italia. Tra le novità introdotte dal nuovo Stato vi furono:
*   L'aumento della pressione fiscale e delle tasse.
*   L'estensione del servizio di leva obbligatorio su tutta l'Italia.
*   L'eliminazione delle barriere doganali, che portò al fallimento di molte aziende meridionali non in grado di competere con quelle settentrionali.
*   La mancata assegnazione di lavori alle

### Risposta SLM-RAG

Lo stato italiano si formò nel 1861 con la proclamazione di Vittorio Emanuele II come Re d'Italia a Torino, dopo che il primo parlamento nazionale si riunì nello stesso anno. Questo processo, noto come Risorgimento, fu il risultato di un complesso di eventi, dottrine politiche e iniziative che portarono all'unificazione dell'Italia, separandola dall'occupazione straniera (in particolare l'Austria) e riunendo vari regni interni.

Il processo di unificazione fu guidato da diverse forze politiche e figure chiave:
*   **La posizione moderata:** Appoggiò il governo monarchico dei Savoia per raggiungere l'unificazione.
*   **La posizione democratica:** Punta alla realizzazione di una repubblica con l'aiuto del popolo, senza intervento monarchico. I suoi principali protagonisti furono **Mazzini** (fondatore della *Giovane Italia*, che sognava un'unificazione repubblicana e europea) e **Garibaldi**.

L'unificazione fu concretizzata attraverso l'estensione delle leggi del Piemonte a tutto il paese (piemontesizzazione), l'adozione della lira, dello Statuto Albertino e di altre leggi. La capitale fu stabilita a Roma

### Ground Truth

L'unità d'Italia fu il risultato del Risorgimento, guidato da figure come Mazzini (fondatore della Giovine Italia), Cavour (che condusse la politica diplomatica e la Seconda guerra d'Indipendenza) e Garibaldi (che guidò la Spedizione dei Mille). Il Piemonte fu il fulcro del processo unitario.

---

## 10. What were the social consequences of the Industrial Revolution?

*quali furono le conseguenze sociali della rivoluzione industriale?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 15.2 ms | 5.8 ms (2.6x) |
| **Generazione** | 5315 ms | 5286 ms |
| **Totale** | 5331 ms | 5292 ms |
| **Pool chunk** | 181 | 6 |
| **Keyword hit** | 83% | 83% |

### Risposta StdRAG

In base al contesto fornito, le conseguenze sociali della Rivoluzione Industriale includono:

*   **Aumento demografico:** Inizia un profondo aumento della popolazione in Europa, favorito dalla tecnologia agricola e dai nuovi prodotti. In Inghilterra la popolazione raddoppia in un secolo, e anche la Francia cresce notevolmente.
*   **Cambiamento degli spazi urbani:** Crescono le città e si formano nuovi quartieri, in particolare quelli dedicati agli operai impiegati nelle fabbriche.
*   **Diffusione dell'informazione:** Nascono i primi giornali (gazzette), sia statali che indipendenti, permettendo la diffusione di conoscenze e novità tra la borghesia e i ceti emergenti (il principio "sapere è potere"), sebbene nasca anche la censura.
*   **Nascita di nuove classi sociali:**
    *   Il **proletariato**, la cui unica ricchezza era costituita dalla prole (i figli).
    *   La **borghesia capitalista**, formata dai proprietari dei mezzi di produzione (macchinari) che agiscono come imprenditori.
*   **Condizioni di lavoro precarie:** A causa dell'abbandono

### Risposta SLM-RAG

In base al contesto fornito, le conseguenze sociali della Rivoluzione Industriale includono:

*   **Cambiamenti demografici e urbanistici:** Si è verificato un profondo aumento demografico in Europa, con la popolazione che raddoppia in Inghilterra in un secolo. Si sono modificati gli spazi, crescono le città e si formano nuovi quartieri, specialmente di operai impiegati nelle fabbriche.
*   **Nascita di nuove classi sociali:** Sono emerse due classi principali: il **proletariato**, la cui unica ricchezza era la prole, e la **borghesia capitalista**, formata dai proprietari dei mezzi di produzione (macchinari) che agiscono come imprenditori.
*   **Diffusione dell'informazione:** Si è diffusa l'informazione con la nascita dei primi giornali (gazzette), sia statali che indipendenti, permettendo alle conoscenze e alle novità di diffondersi tra la borghesia e i ceti emergenti (il principio "sapere è potere"), sebbene nascesse anche la censura.
*   **Condizioni di lavoro e conflitti:** I salari sono diventati bassi e le condizioni di lavoro molto pesanti, specialmente per

### Ground Truth

La Rivoluzione Industriale determinò la nascita del proletariato operaio, che lavorava in fabbriche in condizioni di sfruttamento. Si accentuò la divisione tra borghesia proprietaria e classe operaia. Gli effetti negativi dell'industrializzazione includevano orari di lavoro estenuanti e condizioni igieniche precarie.

---

## 11. How did the population of Europe change from the year 1000 to the 14th century?

*come cambiò la popolazione europea dall'anno Mille al Trecento?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 15.5 ms | 8.0 ms (1.9x) |
| **Generazione** | 978 ms | 1025 ms |
| **Totale** | 993 ms | 1033 ms |
| **Pool chunk** | 181 | 26 |
| **Keyword hit** | 100% | 100% |

### Risposta StdRAG

La popolazione europea raddoppiò, passando da circa 40 milioni di abitanti all'inizio del Mille a circa 80 milioni all'inizio del Trecento.

### Risposta SLM-RAG

La popolazione europea raddoppiò, passando da circa 40 milioni di abitanti all'inizio del Mille a circa 80 milioni all'inizio del Trecento.

### Ground Truth

La popolazione europea aumentò dall'anno Mille fino all'inizio del Trecento, raddoppiando da circa 40 milioni a circa 80 milioni di abitanti. Questo comportò la necessità di disboscare nuovi terreni per aumentare la produzione, anche se si verificarono ciclicamente carestie decennali che causarono migliaia di vittime.

---

## 12. How did the plague spread from Crimea to Europe?

*come si diffuse la peste dalla Crimea all'Europa?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 14.7 ms | 5.8 ms (2.5x) |
| **Generazione** | 455 ms | 441 ms |
| **Totale** | 470 ms | 447 ms |
| **Pool chunk** | 181 | 5 |
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
| **Retrieval** | 14.6 ms | 6.3 ms (2.3x) |
| **Generazione** | 452 ms | 502 ms |
| **Totale** | 467 ms | 508 ms |
| **Pool chunk** | 181 | 8 |
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
| **Retrieval** | 14.9 ms | 5.1 ms (2.9x) |
| **Generazione** | 425 ms | 476 ms |
| **Totale** | 440 ms | 482 ms |
| **Pool chunk** | 181 | 6 |
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
| **Retrieval** | 14.2 ms | 5.8 ms (2.5x) |
| **Generazione** | 459 ms | 478 ms |
| **Totale** | 474 ms | 484 ms |
| **Pool chunk** | 181 | 6 |
| **Keyword hit** | 0% | 0% |

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
| **Retrieval** | 14.9 ms | 5.8 ms (2.6x) |
| **Generazione** | 480 ms | 458 ms |
| **Totale** | 495 ms | 464 ms |
| **Pool chunk** | 181 | 8 |
| **Keyword hit** | 0% | 14% |

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
| **Retrieval** | 15.2 ms | 7.2 ms (2.1x) |
| **Generazione** | 482 ms | 463 ms |
| **Totale** | 497 ms | 470 ms |
| **Pool chunk** | 181 | 8 |
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
| **Retrieval** | 15.3 ms | 6.5 ms (2.4x) |
| **Generazione** | 550 ms | 484 ms |
| **Totale** | 565 ms | 490 ms |
| **Pool chunk** | 181 | 7 |
| **Keyword hit** | 17% | 33% |

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
| **Retrieval** | 15.9 ms | 6.8 ms (2.3x) |
| **Generazione** | 509 ms | 475 ms |
| **Totale** | 525 ms | 482 ms |
| **Pool chunk** | 181 | 18 |
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
| **Retrieval** | 15.3 ms | 6.1 ms (2.5x) |
| **Generazione** | 1458 ms | 423 ms |
| **Totale** | 1474 ms | 429 ms |
| **Pool chunk** | 181 | 6 |
| **Keyword hit** | 17% | 0% |

### Risposta StdRAG

The answer is not available in the provided context.

Although "Enrico il Navigatore" (Henry the Navigator) is mentioned in Chunk 2 as part of a list of images and links, the text does not provide any information about who he was or his contribution to exploration.

### Risposta SLM-RAG

The answer is not available in the provided context.

### Ground Truth

Enrico il Navigatore era il re del Portogallo che fondò una scuola nautica nella sua residenza di Capo di Sagres nell'Algarve. Lì si raccoglievano informazioni su maree, venti e sull'Oceano Atlantico. Favorì la sostituzione della galera con la più maneggevole caravella e avviò le esplorazioni portoghesi verso le Azzorre e la circumnavigazione dell'Africa.

---

## 21. Who was Bartolomeo Díaz and why did he not complete his voyage?

*chi era Bartolomeo Diaz e perché non completò il suo viaggio?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 14.7 ms | 6.4 ms (2.3x) |
| **Generazione** | 462 ms | 484 ms |
| **Totale** | 476 ms | 490 ms |
| **Pool chunk** | 181 | 6 |
| **Keyword hit** | 33% | 17% |

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
| **Retrieval** | 15.2 ms | 7.0 ms (2.2x) |
| **Generazione** | 1585 ms | 442 ms |
| **Totale** | 1600 ms | 449 ms |
| **Pool chunk** | 181 | 9 |
| **Keyword hit** | 67% | 17% |

### Risposta StdRAG

The answer is not available in the provided context.

While Chunk 2 lists "Nuove rotte – commercio triangolare" (New routes – triangular trade) as a section heading, the actual text describing what the triangular trade was and why it was ethically problematic is not present in any of the provided chunks.

### Risposta SLM-RAG

The answer is not available in the provided context.

### Ground Truth

Il commercio triangolare prevedeva tre tappe: partenza dall'Europa con armi, alcol e suppellettili; sosta in Africa dove si acquistavano schiavi sfruttando le rivalità tribali; arrivo in America dove gli schiavi erano venduti in cambio di tabacco, cotone e canna da zucchero che tornavano in Europa. Generava enormi ricchezze ma pose le basi per la tratta degli schiavi, una grave ingiustizia storica.

---

## 23. What new food products did Europe import from the Americas after 1492?

*quali nuovi prodotti alimentari arrivarono in Europa dalle Americhe dopo il 1492?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 15.0 ms | 6.1 ms (2.5x) |
| **Generazione** | 1434 ms | 1416 ms |
| **Totale** | 1449 ms | 1422 ms |
| **Pool chunk** | 181 | 6 |
| **Keyword hit** | 100% | 100% |

### Risposta StdRAG

Secondo il contesto fornito, i nuovi prodotti alimentari arrivate rapidamente in Europa dalle Americhe sono:

*   Mais
*   Girasole
*   Peperone
*   Patata
*   Fagiolo
*   Pomodoro
*   Tabacco

### Risposta SLM-RAG

Secondo il contesto fornito, i nuovi prodotti alimentari arrivate rapidamente in Europa dalle Americhe sono:

*   Mais
*   Girasole
*   Peperone
*   Patata
*   Fagiolo
*   Pomodoro
*   Tabacco

### Ground Truth

Tra i prodotti agricoli importati dall'America ricordiamo: mais, girasole, peperone, patata, fagiolo, pomodoro e tabacco. Tra le specie animali giunsero il tacchino, il cincillà, il visone americano e la trota arcobaleno.

---

## 24. What happened at the Diet of Augsburg in 1530?

*cosa accadde alla Dieta di Augusta del 1530?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 15.2 ms | 6.9 ms (2.2x) |
| **Generazione** | 504 ms | 477 ms |
| **Totale** | 519 ms | 484 ms |
| **Pool chunk** | 181 | 5 |
| **Keyword hit** | 33% | 17% |

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
| **Retrieval** | 15.5 ms | 6.9 ms (2.3x) |
| **Generazione** | 521 ms | 495 ms |
| **Totale** | 537 ms | 502 ms |
| **Pool chunk** | 181 | 6 |
| **Keyword hit** | 17% | 33% |

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
| **Retrieval** | 15.5 ms | 7.8 ms (2.0x) |
| **Generazione** | 1732 ms | 1678 ms |
| **Totale** | 1747 ms | 1686 ms |
| **Pool chunk** | 181 | 19 |
| **Keyword hit** | 17% | 17% |

### Risposta StdRAG

Secondo il contesto fornito, la dottrina calvinista sulla predestinazione afferma che l'uomo, con la sua natura imperfetta, **non può salvarsi per fede**. Al contrario, è **Dio**, nella sua bontà imperscrutabile, a **predestinare l'uomo alla salvezza eterna**.

### Risposta SLM-RAG

Secondo il contesto fornito, la dottrina calvinista della predestinazione afferma che l'uomo, con la sua natura imperfetta, **non può salvarsi per fede**. Al contrario, è **Dio**, nella sua bontà imperscrutabile, a **predestinare l'uomo alla salvezza eterna**.

### Ground Truth

Calvino affermava la sovranità assoluta di Dio sull'uomo e la dottrina della predestinazione: l'umanità è divisa in eletti, destinati al Paradiso, e dannati. L'uomo con la sua natura imperfetta non può salvarsi per propria fede; è Dio a predestinarlo alla salvezza. Calvino riconobbe come sacramenti validi solo il battesimo e l'eucaristia.

---

## 27. What was England's Glorious Revolution?

*cos'era la Gloriosa Rivoluzione inglese?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 15.7 ms | 5.6 ms (2.8x) |
| **Generazione** | 1477 ms | 449 ms |
| **Totale** | 1492 ms | 455 ms |
| **Pool chunk** | 181 | 6 |
| **Keyword hit** | 60% | 20% |

### Risposta StdRAG

The answer is not available in the provided context.

While the context mentions "L'Inghilterra e la 'Gloriosa Rivoluzione'" in the table of contents of Chunk 2, it does not provide a description or definition of what the Glorious Revolution was.

### Risposta SLM-RAG

The answer is not available in the provided context.

### Ground Truth

La Gloriosa Rivoluzione inglese è descritta nel contesto del passaggio dall'assolutismo verso forme più costituzionali di governo in Inghilterra nel Seicento, in cui il parlamento limitò il potere assoluto del sovrano.

---

## 28. What were the main features of the First Industrial Revolution?

*quali furono le caratteristiche principali della Prima Rivoluzione Industriale?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 15.0 ms | 6.5 ms (2.3x) |
| **Generazione** | 5324 ms | 5353 ms |
| **Totale** | 5339 ms | 5359 ms |
| **Pool chunk** | 181 | 6 |
| **Keyword hit** | 100% | 100% |

### Risposta StdRAG

In base al contesto fornito, le caratteristiche principali della Prima Rivoluzione Industriale sono:

*   **Innovazioni tecnologiche e fonti di energia:** Dopo il 1750 in Gran Bretagna, si passò dall'agricoltura alle macchine. Le principali fonti di energia furono l'**acqua** e il **carbone**.
*   **Nuove tecnologie specifiche:** Nel settore tessile si perfezionò il telaio (con la spoletta mobile); James Watt costruì la **macchina a vapore**; George Stephenson realizzò la **locomotiva** e nacque il sistema delle **ferrovie**.
*   **Trasformazione economica e sociale:** Si passò da un'economia chiusa e basata sull'agricoltura a un'economia basata sulle macchine e sul lavoro operaio. Questo portò a un aumento degli scambi commerciali e delle materie prime (commercio triangolare) e a miglioramenti nelle tecniche agricole.
*   **Nascita della fabbrica e del proletariato:** Molti braccianti fuggirono dalla campagna (a causa delle enclosures) per lavorare nelle prime **fabbriche**, dove il lavoro era parcellizzato. N

### Risposta SLM-RAG

Le caratteristiche principali della Prima Rivoluzione Industriale, secondo il contesto fornito, sono:

*   **Cambiamento economico e sociale:** Passaggio da un'economia basata sull'agricoltura e una società chiusa a un'economia basata sulle macchine, sul lavoro operaio e alla nascita di nuove classi sociali.
*   **Nuove fonti di energia:** Utilizzo della forza motrice dell'**acqua** e del **carbone**.
*   **Innovazioni tecnologiche:**
    *   Perfezionamento del telaio tessile (con la spoletta mobile).
    *   Costruzione della **macchina a vapore** (da parte di Watt).
    *   Realizzazione della **locomotiva** e nascita delle **ferrovie** (da parte di Stephenson).
*   **Modifiche sociali e demografiche:**
    *   Aumento demografico in Europa (in Inghilterra la popolazione raddoppia in un secolo).
    *   Fuga dei braccianti dalla campagna verso le città e le prime fabbriche.
    *   Crescita delle città e formazione di nuovi quartieri operai.
    *

### Ground Truth

La Prima Rivoluzione Industriale fu caratterizzata dall'introduzione di nuove tecnologie come la macchina a vapore di James Watt, dalla nascita della fabbrica come luogo di produzione accentrata, dall'uso massiccio del carbone e dalla trasformazione dei rapporti sociali con la nascita del proletariato operaio.

---

## 29. Who were the philosophes and what was their central idea?

*chi erano i philosophes e qual era la loro idea centrale?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 14.9 ms | 6.0 ms (2.5x) |
| **Generazione** | 430 ms | 462 ms |
| **Totale** | 445 ms | 468 ms |
| **Pool chunk** | 181 | 6 |
| **Keyword hit** | 50% | 50% |

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
| **Retrieval** | 15.2 ms | 6.6 ms (2.3x) |
| **Generazione** | 3352 ms | 3182 ms |
| **Totale** | 3367 ms | 3188 ms |
| **Pool chunk** | 181 | 7 |
| **Keyword hit** | 80% | 60% |

### Risposta StdRAG

Caterina II di Russia è stata una delle sovrani più famosi del cosiddetto "dispotismo illuminato", un movimento che coinvolse anche Austria, Italia, Spagna e Portogallo nella seconda metà del Settecento. È considerata un despota illuminato per la sua mentalità aperta al riformismo illuminista e per l'accoglienza che ha rivolto ai filosofi, i quali furono spesso ospitati nelle sue corti.

Come altri sovrani illuminati (come Maria Teresa d'Austria e Federico II di Prussia), Caterina II aveva l'intenzione di rendere più forte il potere dello stato nei confronti della nobiltà e della Chiesa. In Russia, ha cercato specificamente di "svecchiare la società".

### Risposta SLM-RAG

Caterina II di Russia era una sovrana che, insieme a Maria Teresa d'Austria e Federico II di Prussia, è soprannominata "re-filosofo" per la sua mentalità aperta al riformismo illuminista e per l'accoglienza che ha rivolto ai filosofi, ospitandoli spesso nelle sue corti. È considerata un despota illuminato perché, come gli altri sovrani di questo movimento, aveva l'intenzione di rendere più forte il potere dello stato nei confronti della nobiltà e della Chiesa. In particolare, in Russia cercò di "svecchiare la società" e attuò una politica di riforme ispirate all'Illuminismo.

### Ground Truth

Caterina II di Russia è descritta tra i cosiddetti 're filosofi', sovrani che cercarono di applicare i principi illuministi al governo mantenendo però il potere assoluto. È inserita, insieme a Giuseppe II d'Austria e Federico II di Prussia, tra i rappresentanti del dispotismo illuminato.

---

## 31. What were the economic causes of the French Revolution?

*quali furono le cause economiche della Rivoluzione Francese?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 15.6 ms | 5.9 ms (2.7x) |
| **Generazione** | 3937 ms | 5278 ms |
| **Totale** | 3952 ms | 5284 ms |
| **Pool chunk** | 181 | 6 |
| **Keyword hit** | 0% | 20% |

### Risposta StdRAG

In base al contesto fornito, le cause economiche della Rivoluzione Francese sono:

*   **Mancanza di fondi per lo Stato:** Il re fu costretto a ritornare a Parigi perché lo Stato non aveva più risorse finanziarie.
*   **Legge di confisca dei beni del clero:** Per trovare risorse, l'assemblea approvò questa legge, che portò a una rottura con la Chiesa ma soddisfece la richiesta dei borghesi e dei contadini di impadronirsi delle vastissime terre possedute dalla Chiesa.
*   **Rigidità del controllo statale sul clero:** L'approvazione della Costituzione Civile del Clero e lo scioglimento degli ordini religiosi (tranne quelli di assistenza e istruzione) crearono disagio e divisero l'opinione pubblica, aggravando le tensioni sociali ed economiche.

### Risposta SLM-RAG

In base al contesto fornito, le cause economiche della Rivoluzione Francese includono:

*   **Mancanza di fondi per lo Stato:** L'assemblea fu costretta ad approvare una legge di confisca dei beni del clero per trovare risorse, poiché lo Stato non aveva più fondi.
*   **Inflazione e crisi dei prezzi:** Si verificò una "rivoluzione dei prezzi" con un incremento del 400% circa. I salariati furono penalizzati perché l'inflazione divorò il loro esiguo potere d'acquisto.
*   **Importazione di metalli preziosi:** Secondo Jean Bodin, l'importazione di enormi quantità di oro e argento dalle Americhe (da parte di Spagna e Portogallo) causò la perdita di valore della moneta.
*   **Crisi agraria e carestie:** La situazione economica era critica a causa delle carestie e dei cattivi raccolti (come nel 1788), che determinavano l'aumento del prezzo del pane e attività speculative da parte dei mercanti.
*   **Politica fiscale di Luigi XVI e Turgot:** Il re decise di mettere in atto riforme, ma Jacques T

### Ground Truth

La crisi economica è individuata come una delle principali premesse della Rivoluzione Francese. L'Ancien Régime era caratterizzato da privilegi fiscali per nobiltà e clero, mentre il peso delle tasse gravava sul terzo stato. La convocazione degli Stati Generali fu una risposta diretta a questa crisi finanziaria.

---

## 32. When was the Bastille stormed and what did it symbolize?

*quando fu presa la Bastiglia e cosa simboleggiò?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 16.4 ms | 9.0 ms (1.8x) |
| **Generazione** | 1725 ms | 500 ms |
| **Totale** | 1741 ms | 509 ms |
| **Pool chunk** | 181 | 23 |
| **Keyword hit** | 83% | 33% |

### Risposta StdRAG

La Bastiglia fu presa il **14 luglio 1789**. Simboleggiò l'inizio della fase di riforme e la trasformazione della monarchia in **monarchia costituzionale**, segnando anche l'esplodere dei fermenti popolari e la perdita dei privilegi feudali e nobiliari.

### Risposta SLM-RAG

The answer is not available in the provided context.

### Ground Truth

La Bastiglia fu presa il 14 luglio 1789. L'evento rappresentò una svolta simbolica della Rivoluzione Francese, segnando il passaggio dall'azione delle assemblee all'azione popolare diretta contro il potere monarchico.

---

## 33. What was the War of the Vendée during the French Revolution?

*cos'era la guerra della Vandea durante la Rivoluzione Francese?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 15.9 ms | 7.4 ms (2.1x) |
| **Generazione** | 2809 ms | 459 ms |
| **Totale** | 2825 ms | 466 ms |
| **Pool chunk** | 181 | 20 |
| **Keyword hit** | 80% | 60% |

### Risposta StdRAG

La guerra della Vandea fu una rivolta scoppiata nelle campagne francesi durante la Rivoluzione Francese. Essa fu causata dal malcontento generato dall'arruolamento di massa di 300.000 uomini (leva di massa) deciso dalla Convenzione, che creò carenza di manodopera per il raccolto. La rivolta si intensificò in una zona dove il consenso e l'attaccamento alla Chiesa erano molto forti. La Convenzione reagì con durezza reprimendo ogni manifestazione fino a sconfiggere chi si opponeva.

### Risposta SLM-RAG

The answer is not available in the provided context.

### Ground Truth

La guerra della Vandea fu una delle difficoltà interne della Rivoluzione Francese: un conflitto civile che oppose i rivoluzionari a una parte della popolazione francese — in particolare contadini e fedeli alla monarchia e alla Chiesa — nella regione della Vandea.

---

## 34. What were Napoleon's main military campaigns and how did his empire end?

*quali furono le principali campagne di Napoleone e come finì il suo impero?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 15.0 ms | 7.2 ms (2.1x) |
| **Generazione** | 5328 ms | 5326 ms |
| **Totale** | 5343 ms | 5333 ms |
| **Pool chunk** | 181 | 13 |
| **Keyword hit** | 33% | 33% |

### Risposta StdRAG

In base al contesto fornito, le informazioni disponibili sono le seguenti:

**Principali campagne menzionate:**
*   **Campagna d'Egitto:** Seguita da gravi perdite in Italia e Renania.
*   **Campagna d'Italia del 1796:** Posse in luce le capacità militari di Napoleone, permettendogli di diventare il generale più valido per difendere la Francia e i suoi ideali rivoluzionari.
*   **Battaglia di Marengo (1800):** La sconfitta più importante inflitta agli austriaci, che spianò la strada per la costituzione della Repubblica Italiana e la nomina di Napoleone a Re d'Italia.
*   **Ultima campagna (1815):** Napoleone sfuggì all'esilio, rientrò in Francia il 1° marzo 1815 e subì la sua "ultima pesante sconfitta" a **Waterloo** il 18 giugno 1815.

**Come finì il suo impero:**
Il suo impero finì dopo la sconfitta a Waterloo. Napoleone fu costretto all'esilio, questa volta alle condizioni inglesi, sulla lontana isola

### Risposta SLM-RAG

In base al contesto fornito, le principali campagne e la fine dell'impero di Napoleone sono descritte come segue:

**Principali campagne e conquiste:**
Dopo la campagna d'Egitto, Napoleone inflisse agli austriaci numerose sconfitte, la più importante delle quali fu la **battaglia di Marengo (1800)**. Questa vittoria permise la costituzione in Italia di una Repubblica (di cui Napoleone fu nominato presidente e poi Re d'Italia nel 1805) e l'estensione della sfera d'influenza francese su gran parte dell'Europa.

**Come finì il suo impero:**
L'impero crollò dopo una coalizione antifrancese che sfruttò un momento critico.
1.  **Sconfitta di Lipsia (1813):** Napoleone fu costretto a un primo esilio sull'isola d'Elba.
2.  **I 100 giorni:** Dopo quasi un anno, Napoleone fuggì dall'Elba, iniziò un periodo di tentativi di recupero militare e tentò di rendere le leggi più liberali.
3.  **Sconfitta definitiva di

### Ground Truth

Napoleone condusse la campagna d'Italia con la nascita delle Repubbliche, la campagna d'Egitto che ne accelerò l'ascesa politica, poi instaurò il Consolato e l'Impero estendendo l'egemonia sull'Europa. La conquista di Mosca segnò l'inizio del declino; l'impero si concluse con la sconfitta definitiva e l'esilio sull'isola di Sant'Elena.

---

## 35. What did the Congress of Vienna decide and who were its main actors?

*cosa stabilì il Congresso di Vienna e chi ne furono i protagonisti?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 15.3 ms | 7.7 ms (2.0x) |
| **Generazione** | 5361 ms | 5394 ms |
| **Totale** | 5377 ms | 5402 ms |
| **Pool chunk** | 181 | 24 |
| **Keyword hit** | 100% | 100% |

### Risposta StdRAG

In base al contesto fornito, ecco la risposta:

**Chi ne furono i protagonisti:**
I principali attori furono i ministri degli esteri:
*   **Lord Castlereagh** per la Gran Bretagna.
*   **Von Metternich** per l'Austria.
*   Lo zar **Alessandro I** (che intervenne di persona).
*   Il francese **Talleyrand**, abile diplomatico che difese gli interessi della Francia.
*   I quattro grandi poteri che avevano sconfitto Napoleone: **Austria, Russia, Prussia e Gran Bretagna**.

**Cosa stabilì il Congresso di Vienna:**
Il Congresso, convocato per riportare l'ordine in Europa e ripristinare la situazione precedente alla Rivoluzione (l'Ancien Regime), stabilì i seguenti principi e conseguenze:
*   **Equilibrio:** Limitare i quattro stati più potenti e creare stati cuscinetto.
*   **Legittimità:** Far tornare al governo i re precedenti alla Rivoluzione.
*   **Intervento:** Diritto di reprimere insurrezioni o colpi di stato con l'esercito.
*   **Riassetto geografico

### Risposta SLM-RAG

In base al contesto fornito, ecco la risposta:

**I protagonisti:**
I principali attori del Congresso di Vienna furono:
*   L'Austria (rappresentata da Metternich)
*   La Russia (rappresentata da Alessandro I)
*   La Prussia
*   La Gran Bretagna (rappresentata da Lord Castlereagh)
*   La Francia (che riuscì a limitare i danni grazie al suo ministro Talleyrand)

**Cosa stabilì:**
Il Congresso stabilì i seguenti principi e conseguenze:
*   **Principi guida:**
    *   **Equilibrio:** Limitare i 4 stati più potenti e creare stati cuscinetto.
    *   **Legittimità:** Far tornare al governo il re precedente alla Rivoluzione.
    *   **Interventismo:** Reprimere insurrezioni o colpi di stato con l'esercito.
*   **Riassetto geografico:**
    *   Nascita della Confederazione Germanica.
    *   Annessione parziale della Polonia dalla Russia.
    *   Consolidamento della presenza Austriaca al Nord Italia.
    *   Unificazione

### Ground Truth

Il Congresso di Vienna stabilì un nuovo assetto europeo volto a restaurare l'ordine precedente alla Rivoluzione Francese e alle conquiste napoleoniche. Portò alla creazione della Santa Alleanza tra le potenze conservatrici. I protagonisti furono i rappresentanti delle grandi potenze europee vincitrici su Napoleone.

---

## 36. Who was Mazzini and what was the Giovine Italia?

*chi era Mazzini e cos'era la Giovine Italia?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 15.0 ms | 6.7 ms (2.2x) |
| **Generazione** | 5316 ms | 4116 ms |
| **Totale** | 5331 ms | 4123 ms |
| **Pool chunk** | 181 | 12 |
| **Keyword hit** | 100% | 80% |

### Risposta StdRAG

Basandosi sul contesto fornito, ecco le risposte alle domande:

**Chi era Mazzini?**
Giuseppe Mazzini era un genovese di famiglia agiata. Inizialmente aderì alla Carboneria, ma si rese conto che la segretezza dei suoi fini era un elemento limitante. Mostrò fin da giovane interesse per le idee democratiche e patriottiche; a 22 anni entrò nella Carboneria e, dopo essere stato arrestato, fu costretto all'esilio a Marsiglia dove entrò in contatto con patrioti esuli. Attraverso studi e dibattiti, arrivò alla conclusione che le associazioni segrete dovessero rinunciare alla segretezza per coinvolgere il popolo. Univa la politica a una personale visione religiosa e i suoi motti erano "Dio e Popolo" e "Pensiero e Azione".

**Cos'era la Giovine Italia?**
La Giovine Italia fu fondata da Mazzini nel 1831. Era un'associazione che si diffondeva soprattutto nel nord Italia (in Lombardia, Liguria, Toscana e Stato pontificio) con lo scopo di unificare il Paese e liberarlo dal potere assoluto dei governanti. Il suo programma prevedeva che

### Risposta SLM-RAG

Secondo il contesto fornito, **Mazzini** era un genovese di famiglia agiata, inizialmente aderente alla Carboneria, che si rese conto che la segretezza dei suoi fini era un elemento limitante. Fondò la **Giovine Italia** nel 1831.

La **Giovine Italia** era un'associazione con le finalità di unificare l'Italia sotto forma repubblicana, liberandola dal potere assoluto dei governanti. Il suo metodo preferito era l'**insurrezione popolare**. Il messaggio dell'associazione era rivolto soprattutto alle classi medie e popolari. I suoi motti erano "Dio e Popolo" e "Pensiero e Azione". L'associazione si diffuse principalmente nel nord Italia (Lombardia, Liguria, Toscana, Stato pontificio), attecchendo meno nel Piemonte e venendo quasi ignorata nel Mezzogiorno e in Sicilia.

### Ground Truth

Giuseppe Mazzini fu uno dei principali protagonisti del Risorgimento e fondatore della Giovine Italia, un'associazione che propugnava l'indipendenza e l'unificazione dell'Italia come nazione libera e repubblicana, ispirata al motto 'Dio e Popolo'.

---

## 37. What was Cavour's role in the unification of Italy?

*quale fu il ruolo di Cavour nell'unificazione d'Italia?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 15.0 ms | 6.0 ms (2.5x) |
| **Generazione** | 5413 ms | 5344 ms |
| **Totale** | 5428 ms | 5350 ms |
| **Pool chunk** | 181 | 12 |
| **Keyword hit** | 80% | 60% |

### Risposta StdRAG

In base al contesto fornito, il ruolo di Cavour nell'unificazione d'Italia può essere sintetizzato nei seguenti punti:

*   **Ruolo politico e ideologico:** Cavour è definito un "abile politico" e un "nobile imprenditore" con idee **liberali**. La sua politica interna garantiva i diritti individuali e proponeva il **liberismo** economico. Ha attuato riforme agricole, industriali e ha creato la prima rete ferroviaria italiana. Ha inoltre cercato una netta separazione dalla Chiesa ("libera chiesa in libero stato") e ha usato il Piemonte come rifugio per i patrioti che vedevano nella casa Savoia l'unica via per l'unificazione.
*   **Organizzazione dell'unità:** Per ridurre l'influenza di Mazzini e garantire il controllo dei Savoia sull'unificazione, ha fondato la **Società Nazionale Italiana**.
*   **Politica estera e alleanze:** Cavour ha capito che l'Italia non poteva unificarsi senza aiuti internazionali. Per ottenere il credito di Francia e Inghilterra, ha inviato l'esercito piemontese alla guerra in Crimea (1853). Ha stretto un'intesa segreta

### Risposta SLM-RAG

In base al contesto fornito, il ruolo di Cavour nell'unificazione d'Italia è stato quello di un abile politico e primo ministro piemontese che ha guidato il processo attraverso la diplomazia, il liberismo e la modernizzazione, evitando la via rivoluzionaria. I suoi ruoli specifici includono:

*   **Diplomazia e alleanze:** Ha ottenuto l'intervento della Francia contro l'Austria grazie a un incontro segreto con Napoleone III a Plombières (1858), concordando un piano per l'unificazione sotto la guida dei Savoia e ottenendo in cambio Nizza e Savoia.
*   **Modernizzazione e riforme:** Ha avviato un processo di modernizzazione del Piemonte, attuando una politica liberale che garantiva i diritti individuali e proponeva il liberismo economico. Ha creato l'Ansaldo, la prima rete ferroviaria italiana e promosso riforme agricole e industriali.
*   **Controllo politico:** Ha fondato la Società Nazionale Italiana per proiettare l'unità sotto il controllo dei Savoia, contrastando l'influenza di Mazzini e le spedizioni armate come quella di Pisacane.
*   **Gestione della

### Ground Truth

Camillo Benso conte di Cavour fu la figura politica centrale del processo di unificazione. Attuò riforme nel Regno di Sardegna, condusse una politica estera che portò all'alleanza con la Francia, guidò la Seconda guerra d'Indipendenza e creò le condizioni diplomatiche per la Spedizione dei Mille di Garibaldi.

---

## 38. What was Taylorism and in what historical context did it emerge?

*cos'era il Taylorismo e in quale contesto storico nacque?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 15.2 ms | 6.0 ms (2.5x) |
| **Generazione** | 1616 ms | 560 ms |
| **Totale** | 1631 ms | 566 ms |
| **Pool chunk** | 181 | 10 |
| **Keyword hit** | 67% | 17% |

### Risposta StdRAG

The answer is not available in the provided context.

Although Chunk 4 lists "L'organizzazione del lavoro ed il Taylorismo" (The organization of work and Taylorism) as a sub-section of the Second Industrial Revolution, it does not provide a definition of what Taylorism is or the historical context in which it originated.

### Risposta SLM-RAG

The answer is not available in the provided context.

### Ground Truth

Il Taylorismo fu un sistema di organizzazione scientifica del lavoro sviluppato durante la Seconda Rivoluzione Industriale. Rappresentò una nuova forma di razionalizzazione della produzione in fabbrica, finalizzata ad aumentare la produttività attraverso la standardizzazione dei compiti operai.

---

## 39. What was the Monroe Doctrine and in what context was it issued?

*cos'era la dottrina Monroe e in quale contesto fu proclamata?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 14.9 ms | 6.2 ms (2.4x) |
| **Generazione** | 2775 ms | 1669 ms |
| **Totale** | 2790 ms | 1675 ms |
| **Pool chunk** | 181 | 7 |
| **Keyword hit** | 67% | 33% |

### Risposta StdRAG

La dottrina Monroe fu proclamata dal Presidente Monroe nel 1800 (o all'inizio del 1800) e stabiliva che gli interessi dell'America spettavano agli americani, opponendosi alle ingerenze dell'Europa. Fu emessa in un contesto di espansione verso ovest (il "mitico west"), che portò alla distruzione dei pellirossa a causa dei tanti coloni provenienti dall'Europa. Inoltre, in quel periodo, gli Stati Uniti erano ormai 27 e l'economia era ben distinta: industriale nel Nord e agricola nel Sud.

### Risposta SLM-RAG

La dottrina Monroe fu una politica di egemonia degli Stati Uniti su tutto il continente americano, che significava il taglio del "cordone ombelicale" con la vecchia Europa. Fu proclamata nel 1845, in seguito alla quale gli Stati Uniti annessero gli stati della California e del Texas a danno del Messico.

### Ground Truth

La dottrina Monroe fu proclamata nell'ambito delle lotte per l'indipendenza dell'America latina e dei moti liberali. Affermava il principio che l'America non doveva essere considerata campo di ulteriore colonizzazione europea, opponendosi all'interventismo delle potenze del Vecchio Continente nelle Americhe.

---

## 40. How were the price revolution of the 16th century and the geographical discoveries connected?

*come erano collegati la rivoluzione dei prezzi del Cinquecento e le scoperte geografiche?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 15.7 ms | 8.1 ms (1.9x) |
| **Generazione** | 2688 ms | 2388 ms |
| **Totale** | 2704 ms | 2396 ms |
| **Pool chunk** | 181 | 24 |
| **Keyword hit** | 100% | 100% |

### Risposta StdRAG

Secondo il contesto fornito, la **rivoluzione dei prezzi** del Cinquecento fu causata dall'**importazione di enormi quantità di oro e di argento dalle Americhe**, che avvenne grazie alle **scoperte geografiche** (in particolare quelle della Spagna e del Portogallo).

Questo afflusso di metalli preziosi causò la perdita di valore della moneta, portando a un incremento dei prezzi del 400% circa. Di conseguenza, i salariati furono i più penalizzati perché l'inflazione erose il loro potere d'acquisto.

### Risposta SLM-RAG

Secondo il contesto fornito, la **rivoluzione dei prezzi** del Cinquecento fu causata dall'**importazione di enormi quantità di oro e di argento dalle Americhe** (dalle scoperte geografiche) da parte della Spagna e del Portogallo. Questo afflusso di metalli preziosi causò la **perdita di valore della moneta** e un incremento del 400% circa dei prezzi, fenomeno che fu definito "rivoluzione dei prezzi" da Jean Bodin.

### Ground Truth

Nel Cinquecento i prezzi subirono un incremento di circa il 400%. Il pensatore Jean Bodin spiegò il fenomeno sostenendo che l'importazione massiccia di oro e argento dalle Americhe da parte di Spagna e Portogallo aveva causato la svalutazione della moneta. I salariati furono i più penalizzati, poiché l'inflazione erose il loro già esiguo potere d'acquisto.

---

