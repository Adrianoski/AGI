# Benchmark RAG — storia

**Modello:** Qwen/Qwen3.5-4B  |  **top-k:** 5  |  **top-N SLM:** 3

| Metrica | StdRAG | SLM-RAG |
|---|---|---|
| Speedup retrieval | — | **2.8x** |
| Pool medio | 181 chunk | 8 chunk (-95%) |
| Keyword hit | 52% | **44%** |
| Overlap medio top-5 | 36% | — |

---

## 1. Who imported spices into Europe during the Middle Ages?

*da chi venivano importate le spezie in europa nel medioevo?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 18.5 ms | 5.5 ms (3.4x) |
| **Generazione** | 4142 ms | 327 ms |
| **Totale** | 4161 ms | 333 ms |
| **Pool chunk** | 181 | 3 |
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
| **Retrieval** | 16.7 ms | 6.7 ms (2.5x) |
| **Generazione** | 4179 ms | 3007 ms |
| **Totale** | 4196 ms | 3014 ms |
| **Pool chunk** | 181 | 4 |
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

In base al contesto fornito, Carlo V controllava:

*   **L'impero enorme e complesso** che includeva i **territori del nuovo mondo**.
*   Il **Ducato di Milano** (riprese il controllo alla morte di Francesco Sforza).
*   Il **Portogallo** (la cui sede era vacante).
*   Gran parte dell'**Italia** (dove si distinguono i regni di Savoia, Toscana, Venezia e Genova, oltre ai territori sotto il dominio spagnolo).
*   **Vienna** e altri territori (minacciati dai turchi, ma implicati nel conflitto e nel controllo imperiale).

### Ground Truth

Carlo V controllava un vasto impero che comprendeva la Spagna, i territori asburgici, le Fiandre, il Regno di Napoli e le colonie americane. Il suo regno fu segnato da conflitti con la Francia, i principi tedeschi luterani e l'impero ottomano.

---

## 3. What were the main causes of the French Revolution?

*quali furono le cause della rivoluzione francese?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 16.5 ms | 6.2 ms (2.7x) |
| **Generazione** | 3123 ms | 4589 ms |
| **Totale** | 3139 ms | 4595 ms |
| **Pool chunk** | 181 | 22 |
| **Keyword hit** | 50% | 33% |

### Risposta StdRAG

The answer is not available in the provided context.

The provided text discusses the causes of the **Reformation** (e.g., moral decay of the papal court, Emperor Charles V's ambitions, peasant equality, indulgences) and the causes of the **French Revolution** only in a very general sense, mentioning the "crisis agraria" (agricultural crisis), "carestie" (famines), "capiucci del clima" (capriccio of the climate), and the "ancien regime" (absolute monarchy, rigid social orders, feudal rights). However, it does not provide a comprehensive list or detailed explanation of the specific causes of the French Revolution as requested.

### Risposta SLM-RAG

In base al contesto fornito, le cause della Rivoluzione Francese sono:

*   **La situazione economica critica:** Causata da carestie e cattivi raccolti.
*   **L'attività speculativa dei mercanti:** Stimolata dalla crisi economica.
*   **Le politiche fiscali di Luigi XVI:** In particolare la imposizione di una tassa sulle terre da parte del ministro Jacques Turgot per reperire risorse, che alienò le simpatie dei proprietari terrieri.
*   **L'opposizione delle forze conservatrici:** L'aristocrazia si oppose furente alle proposte di riforma (come l'abolizione delle corporazioni e delle corvées) e opponeva una resistenza strenua alla borghesia, che pur avendo acquistato peso economico, non era ancora in grado di esercitare il suo peso politico contro queste forze.
*   **La richiesta di trasformazione:** La Francia era il paese in cui era più forte la richiesta di trasformazione politica e sociale.

### Ground Truth

Le principali cause della Rivoluzione Francese furono la crisi economica dell'Ancien Régime, le ingiustizie fiscali che gravavano sul terzo stato, la convocazione degli Stati Generali e la crescente influenza dell'opinione pubblica. La nobiltà e il clero godevano di privilegi fiscali che alimentavano il malcontento popolare.

---

## 4. How did James Watt's steam engine work?

*come funzionava la macchina a vapore di james watt?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 15.7 ms | 4.9 ms (3.2x) |
| **Generazione** | 503 ms | 418 ms |
| **Totale** | 519 ms | 423 ms |
| **Pool chunk** | 181 | 3 |
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
| **Retrieval** | 15.6 ms | 5.1 ms (3.0x) |
| **Generazione** | 4511 ms | 4332 ms |
| **Totale** | 4527 ms | 4337 ms |
| **Pool chunk** | 181 | 4 |
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

*   **La ragione:** È indicata come il "lume" naturale dell'uomo che sollecita a svincolarsi dalle tradizioni e dai pregiudizi.
*   **Il coraggio di usare la propria intelligenza:** Espresso dal motto *Sapere aude* ("Abbi il coraggio di servirti della tua intelligenza").
*   **La libertà:** Un principio fondamentale dello stato americano, non legato alle tradizioni storiche dell'Europa.
*   **L'uguaglianza:** Un valore diffuso che ha dato nuove speranze ai contadini.
*   **La dissoluzione del principio di autorità:** Portato dalla nuova dottrina, che permetteva l'emancipazione dai vincoli feudali.
*   **Un nuovo modo di guardare la realtà, la società, la politica, la cultura e la religione:** Caratterizzato dal rifiuto delle tradizioni e dei pregiudizi.

### Ground Truth

L'Illuminismo si fondava sul primato del 'lume naturale' della ragione come strumento di conoscenza e critica della realtà. I philosophes propugnavano una nuova visione dell'economia e della politica basata sulla libertà, sul progresso e sui diritti naturali dell'individuo.

---

## 6. What was the American Revolution?

*che cosa fu la rivoluzione americana?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 16.5 ms | 7.3 ms (2.3x) |
| **Generazione** | 1934 ms | 5427 ms |
| **Totale** | 1950 ms | 5435 ms |
| **Pool chunk** | 181 | 22 |
| **Keyword hit** | 50% | 100% |

### Risposta StdRAG

The answer is not available in the provided context.

While the context mentions "LA RIVOLUZIONE AMERICANA" in the table of contents in Chunk 2 and lists sub-sections regarding the situation of American colonists, economic relations with the mother country, and the path from war to the Declaration of Independence, it does not provide a description or definition of what the American Revolution was.

### Risposta SLM-RAG

La Rivoluzione Americana fu un conflitto che portò alla nascita del nuovo stato federale degli Stati Uniti d'America, sancito dalla pace di Parigi del 1783.

Il processo iniziò con la nascita e il rapido sviluppo delle 13 colonie, caratterizzate da una ricerca di maggior libertà e indipendenza, motivata dalla necessità di concreta libertà religiosa e dalla salvaguardia dei diritti individuali. I rapporti con la madrepatria inglese divennero difficili a causa dell'impiego del controllo inglese e dell'inasprimento delle tasse (per finanziare la guerra dei 7 anni), che provocarono proteste americane per una maggior rappresentatività.

Il conflitto si aggravò con il boicottaggio delle merci inglesi, il gesto del Boston Tea Party e l'inizio delle ostilità. Inizialmente le forze inglesi, meglio organizzate, prevalsero, ma poi prevalsero le vittorie dei coloni, guidati da George Washington, grazie anche agli interventi della Francia e della Spagna che volevano contenere il predominio inglese.

Nel 1776 gli americani stilarono la Dichiarazione di Indipendenza. La sconfitta inglese e la nascita dello stato federale rappresentano la concreta

### Ground Truth

La Rivoluzione Americana fu il processo con cui le tredici colonie americane si ribellarono al dominio inglese, principalmente a causa delle difficili condizioni economiche e fiscali imposte dalla madrepatria. Nel 1776 fu stilata la Dichiarazione d'Indipendenza; la sconfitta inglese fu sancita dalla pace di Parigi del 1783, che diede vita al nuovo stato federale americano.

---

## 7. Who were the Mongols and how did they expand?

*chi erano i mongoli e come si espansero?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 15.7 ms | 5.5 ms (2.9x) |
| **Generazione** | 2198 ms | 4529 ms |
| **Totale** | 2213 ms | 4534 ms |
| **Pool chunk** | 181 | 3 |
| **Keyword hit** | 50% | 83% |

### Risposta StdRAG

The answer is not available in the provided context.

While the context mentions "La via della seta: i Mongoli" (The Silk Road: The Mongols) as a section title in Chunk 1, it does not provide any description of who the Mongols were or how they expanded. The text in Chunk 2 discusses the history of spice trade, Arab merchants, and the Venetian Republic, but does not mention the Mongols.

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
| **Retrieval** | 16.1 ms | 5.0 ms (3.2x) |
| **Generazione** | 2780 ms | 2728 ms |
| **Totale** | 2796 ms | 2733 ms |
| **Pool chunk** | 181 | 3 |
| **Keyword hit** | 100% | 100% |

### Risposta StdRAG

La Riforma protestante di Lutero fu un movimento iniziato da Martin Lutero, monaco e studioso, che si sviluppò a partire dalla sua pubblicazione delle 95 tesi contro le indulgenze e la dottrina tradizionale della Chiesa cattolica. Lutero affermò che per la salvezza dell'anima basta la sola fede e che ogni individuo dispone del libero arbitrio per leggere e interpretare personalmente la Bibbia. Questo cambiamento radicale fu facilitato dalla diffusione della stampa. La Chiesa cattolica reagì scomunicando Lutero nel 1520, dando inizio alla Riforma.

### Risposta SLM-RAG

La Riforma protestante di Lutero fu un movimento iniziato da Martin Lutero, monaco e studioso, che sentì fortemente il problema della salvezza dell'anima. Lutero pubblicò le 95 tesi contro le indulgenze e la dottrina tradizionale, affermando che **la sola fede** basta per la salvezza e che ognuno dispone del **libero arbitrio** per leggere e interpretare personalmente la Bibbia. Questo cambiamento radicale fu facilitato dalla diffusione della stampa. La Chiesa cattolica rispose con la scomunica nel 1520, dando inizio alla Riforma.

### Ground Truth

La Riforma protestante di Lutero segnò una rottura definitiva con la dottrina cattolica, ribadita nella Confessione Augustana presentata da Filippo Melantone alla Dieta di Augusta del 1530. La pace di Augusta del 1555 riconobbe ufficialmente la religione protestante stabilendo il principio 'cuius regio eius religio'.

---

## 9. How was the Italian state formed during the Risorgimento?

*come si formò lo stato italiano nel risorgimento?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 15.7 ms | 7.6 ms (2.1x) |
| **Generazione** | 5357 ms | 5395 ms |
| **Totale** | 5373 ms | 5403 ms |
| **Pool chunk** | 181 | 21 |
| **Keyword hit** | 50% | 67% |

### Risposta StdRAG

In base al contesto fornito, la formazione dello Stato italiano nel Risorgimento si può riassumere come segue:

Il termine **Risorgimento** indica il complesso di eventi, dottrine politiche e iniziative che condussero, a partire dal **1861**, al processo di **unificazione dell'Italia**. Questo processo ebbe come obiettivo la rinascita spirituale del concetto di **nazione**, con la fine dell'occupazione straniera e l'unificazione dei vari regni interni, condizione che l'Italia aveva vissuto per secoli.

Il nuovo Stato italiano nacque nel **1861**. La sua costituzione fu caratterizzata da una serie di scelte politiche e amministrative che, sebbene abbiano unito il territorio, generarono forti tensioni sociali, specialmente nel Sud Italia. Tra le novità introdotte dal nuovo Stato vi furono:
*   L'aumento della pressione fiscale e delle tasse.
*   L'estensione del servizio di leva obbligatorio su tutta l'Italia.
*   L'eliminazione delle barriere doganali, che portò al fallimento di molte aziende meridionali non in grado di competere con quelle settentrionali.
*   La mancata assegnazione di lavori alle

### Risposta SLM-RAG

In base al contesto fornito, la formazione dello Stato italiano nel Risorgimento è descritta come segue:

Il processo di unificazione dell'Italia, definito **Risorgimento**, si è svolto a partire dal **1861**. Questo complesso di eventi, dottrine politiche e iniziative ebbe come fine l'indipendenza del territorio dall'occupazione straniera e l'unificazione di vari regni interni, condizione che l'Italia aveva vissuto per secoli.

Il nuovo Stato italiano fu creato attraverso un processo che portò a una serie di novità poco gradite nel sud Italia, tra cui:
*   Un aumento della pressione fiscale e delle tasse.
*   L'estensione del servizio di leva obbligatorio su tutta l'Italia.
*   L'eliminazione delle barriere doganali, che causò il fallimento di molte aziende meridionali non in grado di competere con quelle settentrionali.
*   Una scarsa assegnazione di lavori alle imprese del mezzogiorno, impedendo lo sviluppo economico.

Queste misure generarono un diffuso malcontento e un rifiuto concreto del nuovo stato, portando al fenomeno del **brigantaggio** (aggregazioni di ex soldati borbonici, cont

### Ground Truth

L'unità d'Italia fu il risultato del Risorgimento, guidato da figure come Mazzini (fondatore della Giovine Italia), Cavour (che condusse la politica diplomatica e la Seconda guerra d'Indipendenza) e Garibaldi (che guidò la Spedizione dei Mille). Il Piemonte fu il fulcro del processo unitario.

---

## 10. What were the social consequences of the Industrial Revolution?

*quali furono le conseguenze sociali della rivoluzione industriale?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 16.0 ms | 5.2 ms (3.1x) |
| **Generazione** | 5339 ms | 5316 ms |
| **Totale** | 5355 ms | 5321 ms |
| **Pool chunk** | 181 | 4 |
| **Keyword hit** | 83% | 100% |

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

*   **Cambiamento demografico e urbano:** Inizia un profondo aumento demografico; cambiano gli spazi con la crescita delle città e la formazione di nuovi quartieri, in particolare di operai impiegati nelle fabbriche.
*   **Nascita di nuove classi sociali:** Si passa da una società chiusa a una con nuove classi sociali, tra cui la nascita del **proletariato** (chi ha solo i figli come ricchezza) e la figura dell'imprenditore.
*   **Trasformazione del lavoro:** Il lavoro diventa parcellizzato e basato sulle macchine; si registra lo sfruttamento della mano d'opera, che include donne e bambini. Molti braccianti fuggono dalla campagna (a causa delle *enclosures*) per trovare lavoro nelle fabbriche.
*   **Fenomeno del Luddismo:** Nasce come reazione al cambiamento e allo sfruttamento.
*   **Diffusione dell'informazione:** Nascono i primi giornali (gazzette) e le conoscenze si diffondono tra la borghesia e i ceti emergenti, sebbene nasca anche la censura.

### Ground Truth

La Rivoluzione Industriale determinò la nascita del proletariato operaio, che lavorava in fabbriche in condizioni di sfruttamento. Si accentuò la divisione tra borghesia proprietaria e classe operaia. Gli effetti negativi dell'industrializzazione includevano orari di lavoro estenuanti e condizioni igieniche precarie.

---

## 11. How did the population of Europe change from the year 1000 to the 14th century?

*come cambiò la popolazione europea dall'anno Mille al Trecento?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 15.9 ms | 5.2 ms (3.1x) |
| **Generazione** | 986 ms | 887 ms |
| **Totale** | 1002 ms | 893 ms |
| **Pool chunk** | 181 | 3 |
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
| **Retrieval** | 15.1 ms | 5.5 ms (2.7x) |
| **Generazione** | 457 ms | 423 ms |
| **Totale** | 472 ms | 428 ms |
| **Pool chunk** | 181 | 3 |
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
| **Retrieval** | 16.4 ms | 4.9 ms (3.4x) |
| **Generazione** | 451 ms | 383 ms |
| **Totale** | 468 ms | 388 ms |
| **Pool chunk** | 181 | 3 |
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
| **Retrieval** | 15.2 ms | 4.9 ms (3.1x) |
| **Generazione** | 427 ms | 383 ms |
| **Totale** | 442 ms | 388 ms |
| **Pool chunk** | 181 | 3 |
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
| **Retrieval** | 15.8 ms | 5.1 ms (3.1x) |
| **Generazione** | 463 ms | 384 ms |
| **Totale** | 479 ms | 389 ms |
| **Pool chunk** | 181 | 3 |
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
| **Retrieval** | 16.7 ms | 6.5 ms (2.6x) |
| **Generazione** | 482 ms | 582 ms |
| **Totale** | 499 ms | 588 ms |
| **Pool chunk** | 181 | 17 |
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
| **Retrieval** | 16.0 ms | 5.4 ms (3.0x) |
| **Generazione** | 483 ms | 382 ms |
| **Totale** | 499 ms | 387 ms |
| **Pool chunk** | 181 | 3 |
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
| **Retrieval** | 16.9 ms | 5.1 ms (3.3x) |
| **Generazione** | 545 ms | 364 ms |
| **Totale** | 561 ms | 369 ms |
| **Pool chunk** | 181 | 3 |
| **Keyword hit** | 17% | 0% |

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
| **Retrieval** | 15.7 ms | 7.0 ms (2.2x) |
| **Generazione** | 482 ms | 520 ms |
| **Totale** | 497 ms | 527 ms |
| **Pool chunk** | 181 | 16 |
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
| **Retrieval** | 16.7 ms | 6.4 ms (2.6x) |
| **Generazione** | 1465 ms | 549 ms |
| **Totale** | 1482 ms | 556 ms |
| **Pool chunk** | 181 | 16 |
| **Keyword hit** | 17% | 17% |

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
| **Retrieval** | 15.9 ms | 5.2 ms (3.0x) |
| **Generazione** | 462 ms | 347 ms |
| **Totale** | 478 ms | 352 ms |
| **Pool chunk** | 181 | 3 |
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
| **Retrieval** | 15.0 ms | 5.4 ms (2.8x) |
| **Generazione** | 1591 ms | 526 ms |
| **Totale** | 1606 ms | 532 ms |
| **Pool chunk** | 181 | 5 |
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
| **Retrieval** | 15.8 ms | 4.6 ms (3.4x) |
| **Generazione** | 1441 ms | 1257 ms |
| **Totale** | 1457 ms | 1262 ms |
| **Pool chunk** | 181 | 3 |
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

I nuovi prodotti alimentari arrivate in Europa dalle Americhe dopo il 1492, secondo il contesto fornito, sono: il mais, il girasole, il peperone, la patata, il fagiolo, il pomodoro e il tabacco.

### Ground Truth

Tra i prodotti agricoli importati dall'America ricordiamo: mais, girasole, peperone, patata, fagiolo, pomodoro e tabacco. Tra le specie animali giunsero il tacchino, il cincillà, il visone americano e la trota arcobaleno.

---

## 24. What happened at the Diet of Augsburg in 1530?

*cosa accadde alla Dieta di Augusta del 1530?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 15.7 ms | 4.9 ms (3.2x) |
| **Generazione** | 511 ms | 454 ms |
| **Totale** | 527 ms | 459 ms |
| **Pool chunk** | 181 | 4 |
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
| **Retrieval** | 14.9 ms | 5.1 ms (2.9x) |
| **Generazione** | 520 ms | 449 ms |
| **Totale** | 535 ms | 454 ms |
| **Pool chunk** | 181 | 5 |
| **Keyword hit** | 17% | 0% |

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
| **Retrieval** | 15.5 ms | 5.0 ms (3.1x) |
| **Generazione** | 1740 ms | 1597 ms |
| **Totale** | 1755 ms | 1602 ms |
| **Pool chunk** | 181 | 3 |
| **Keyword hit** | 17% | 33% |

### Risposta StdRAG

Secondo il contesto fornito, la dottrina calvinista sulla predestinazione afferma che l'uomo, con la sua natura imperfetta, **non può salvarsi per fede**. Al contrario, è **Dio**, nella sua bontà imperscrutabile, a **predestinare l'uomo alla salvezza eterna**.

### Risposta SLM-RAG

Secondo il contesto fornito, la dottrina calvinista della predestinazione sostiene che l'uomo, con la sua natura imperfetta, **non può salvarsi per fede**. Al contrario, è **Dio, nella sua bontà imperscrutabile, a predestinarlo alla salvezza eterna**.

### Ground Truth

Calvino affermava la sovranità assoluta di Dio sull'uomo e la dottrina della predestinazione: l'umanità è divisa in eletti, destinati al Paradiso, e dannati. L'uomo con la sua natura imperfetta non può salvarsi per propria fede; è Dio a predestinarlo alla salvezza. Calvino riconobbe come sacramenti validi solo il battesimo e l'eucaristia.

---

## 27. What was England's Glorious Revolution?

*cos'era la Gloriosa Rivoluzione inglese?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 15.9 ms | 6.8 ms (2.3x) |
| **Generazione** | 1534 ms | 3111 ms |
| **Totale** | 1550 ms | 3118 ms |
| **Pool chunk** | 181 | 22 |
| **Keyword hit** | 60% | 40% |

### Risposta StdRAG

The answer is not available in the provided context.

While the context mentions "L'Inghilterra e la 'Gloriosa Rivoluzione'" in the table of contents of Chunk 2, it does not provide a description or definition of what the Glorious Revolution was.

### Risposta SLM-RAG

Based on the provided context, the "Glorious Revolution" (Gloriosa Rivoluzione) is mentioned in **Chunk 1** as a section title under **7.3** within the chapter on "Absolute States: France and England" (STATI ASSOLUTI: FRANCIA E INGHILTERRA), located on page 98.

However, the provided text **does not contain a description or explanation** of what the Glorious Revolution was, its date, or its specific events. It only lists it as a topic to be covered.

Therefore, using ONLY the information provided:

The answer is not available in the provided context.

### Ground Truth

La Gloriosa Rivoluzione inglese è descritta nel contesto del passaggio dall'assolutismo verso forme più costituzionali di governo in Inghilterra nel Seicento, in cui il parlamento limitò il potere assoluto del sovrano.

---

## 28. What were the main features of the First Industrial Revolution?

*quali furono le caratteristiche principali della Prima Rivoluzione Industriale?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 15.8 ms | 6.8 ms (2.3x) |
| **Generazione** | 5369 ms | 5385 ms |
| **Totale** | 5385 ms | 5391 ms |
| **Pool chunk** | 181 | 22 |
| **Keyword hit** | 100% | 67% |

### Risposta StdRAG

In base al contesto fornito, le caratteristiche principali della Prima Rivoluzione Industriale sono:

*   **Innovazioni tecnologiche e fonti di energia:** Dopo il 1750 in Gran Bretagna, si passò dall'agricoltura alle macchine. Le principali fonti di energia furono l'**acqua** e il **carbone**.
*   **Nuove tecnologie specifiche:** Nel settore tessile si perfezionò il telaio (con la spoletta mobile); James Watt costruì la **macchina a vapore**; George Stephenson realizzò la **locomotiva** e nacque il sistema delle **ferrovie**.
*   **Trasformazione economica e sociale:** Si passò da un'economia chiusa e basata sull'agricoltura a un'economia basata sulle macchine e sul lavoro operaio. Questo portò a un aumento degli scambi commerciali e delle materie prime (commercio triangolare) e a miglioramenti nelle tecniche agricole.
*   **Nascita della fabbrica e del proletariato:** Molti braccianti fuggirono dalla campagna (a causa delle enclosures) per lavorare nelle prime **fabbriche**, dove il lavoro era parcellizzato. N

### Risposta SLM-RAG

In base al contesto fornito, le caratteristiche principali della Prima Rivoluzione Industriale sono:

*   **Periodo:** Si è svolta tra il **1770 e il 1850**.
*   **Origine e diffusione:** È partita dalla realtà economica e sociale dell'**Inghilterra** (in rapida crescita) e si è diffusa modificando mentalità e modi di vivere in Europa.
*   **Natura del cambiamento:** Il termine "rivoluzione" indica che il cambiamento fu **profondo**, paragonabile alla rivoluzione neolitica del 9000 a.C. (passaggio dall'agricoltura alla civiltà urbana).
*   **Fattori sociali e demografici:**
    *   **Aumento demografico:** In Europa la popolazione è cresciuta grazie alla tecnologia agricola e ai nuovi prodotti (in Inghilterra la popolazione raddoppiò in un secolo; anche la Francia ha subito una crescita notevole).
    *   **Cambiamento degli spazi urbani:** Le città sono cresciute e si sono formati nuovi quartieri, specialmente per gli operai impiegati nelle fabbriche.
*   **Diffusione dell'informazione:**

### Ground Truth

La Prima Rivoluzione Industriale fu caratterizzata dall'introduzione di nuove tecnologie come la macchina a vapore di James Watt, dalla nascita della fabbrica come luogo di produzione accentrata, dall'uso massiccio del carbone e dalla trasformazione dei rapporti sociali con la nascita del proletariato operaio.

---

## 29. Who were the philosophes and what was their central idea?

*chi erano i philosophes e qual era la loro idea centrale?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 16.1 ms | 4.9 ms (3.3x) |
| **Generazione** | 480 ms | 418 ms |
| **Totale** | 496 ms | 423 ms |
| **Pool chunk** | 181 | 4 |
| **Keyword hit** | 50% | 0% |

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
| **Retrieval** | 15.8 ms | 6.5 ms (2.4x) |
| **Generazione** | 3393 ms | 2857 ms |
| **Totale** | 3409 ms | 2863 ms |
| **Pool chunk** | 181 | 16 |
| **Keyword hit** | 80% | 40% |

### Risposta StdRAG

Caterina II di Russia è stata una delle sovrani più famosi del cosiddetto "dispotismo illuminato", un movimento che coinvolse anche Austria, Italia, Spagna e Portogallo nella seconda metà del Settecento. È considerata un despota illuminato per la sua mentalità aperta al riformismo illuminista e per l'accoglienza che ha rivolto ai filosofi, i quali furono spesso ospitati nelle sue corti.

Come altri sovrani illuminati (come Maria Teresa d'Austria e Federico II di Prussia), Caterina II aveva l'intenzione di rendere più forte il potere dello stato nei confronti della nobiltà e della Chiesa. In Russia, ha cercato specificamente di "svecchiare la società".

### Risposta SLM-RAG

Caterina II di Russia è stata una sovrana che, insieme ad altri monarchi come Maria Teresa d'Austria e Federico II di Prussia, è stata soprannominata "re-filosofo". È considerata un despota illuminato perché, come gli altri sovrani di questo tipo, aveva una mentalità aperta al riformismo illuminista e accoglieva i filosofi nelle sue corti. Inoltre, come descritto nel contesto, i sovrani illuminati ebbero in comune l'intenzione di rendere più forte il potere dello stato nei confronti della nobiltà e della Chiesa.

### Ground Truth

Caterina II di Russia è descritta tra i cosiddetti 're filosofi', sovrani che cercarono di applicare i principi illuministi al governo mantenendo però il potere assoluto. È inserita, insieme a Giuseppe II d'Austria e Federico II di Prussia, tra i rappresentanti del dispotismo illuminato.

---

## 31. What were the economic causes of the French Revolution?

*quali furono le cause economiche della Rivoluzione Francese?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 16.1 ms | 6.8 ms (2.4x) |
| **Generazione** | 3982 ms | 5433 ms |
| **Totale** | 3998 ms | 5440 ms |
| **Pool chunk** | 181 | 22 |
| **Keyword hit** | 0% | 20% |

### Risposta StdRAG

In base al contesto fornito, le cause economiche della Rivoluzione Francese sono:

*   **Mancanza di fondi per lo Stato:** Il re fu costretto a ritornare a Parigi perché lo Stato non aveva più risorse finanziarie.
*   **Legge di confisca dei beni del clero:** Per trovare risorse, l'assemblea approvò questa legge, che portò a una rottura con la Chiesa ma soddisfece la richiesta dei borghesi e dei contadini di impadronirsi delle vastissime terre possedute dalla Chiesa.
*   **Rigidità del controllo statale sul clero:** L'approvazione della Costituzione Civile del Clero e lo scioglimento degli ordini religiosi (tranne quelli di assistenza e istruzione) crearono disagio e divisero l'opinione pubblica, aggravando le tensioni sociali ed economiche.

### Risposta SLM-RAG

Based on the provided context, the economic causes of the French Revolution include:

*   **Critical economic situation:** The text states the situation was "molto critica" (very critical).
*   **Food shortages and poor harvests:** These factors ("carestie e dei cattivi raccolti") led to speculative activities by merchants.
*   **Fiscal policies of Jacques Turgot:** To find resources, Turgot imposed a tax on land ("mise una tassa sulle terre"), which alienated the sympathies of the landowners ("alienandosi le simpatie dei proprietari terrieri").
*   **Social and economic pressure:** The bourgeoisie had already gained "peso a livello economico" (weight at the economic level) and intended to exercise this influence politically, while facing strong resistance from conservative forces.
*   **Abolition of privileges:** Turgot proposed the abolition of corporations and corvées (free labor services from peasants), which caused fierce opposition from the aristocracy.

*(Note: The provided text describes the economic context and the reforms attempted by Turgot that led to the crisis, but it does not explicitly list a final, summarized bullet-point list titled "economic causes of the French Revolution".)*

### Ground Truth

La crisi economica è individuata come una delle principali premesse della Rivoluzione Francese. L'Ancien Régime era caratterizzato da privilegi fiscali per nobiltà e clero, mentre il peso delle tasse gravava sul terzo stato. La convocazione degli Stati Generali fu una risposta diretta a questa crisi finanziaria.

---

## 32. When was the Bastille stormed and what did it symbolize?

*quando fu presa la Bastiglia e cosa simboleggiò?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 15.7 ms | 5.1 ms (3.1x) |
| **Generazione** | 1733 ms | 1298 ms |
| **Totale** | 1749 ms | 1303 ms |
| **Pool chunk** | 181 | 3 |
| **Keyword hit** | 83% | 67% |

### Risposta StdRAG

La Bastiglia fu presa il **14 luglio 1789**. Simboleggiò l'inizio della fase di riforme e la trasformazione della monarchia in **monarchia costituzionale**, segnando anche l'esplodere dei fermenti popolari e la perdita dei privilegi feudali e nobiliari.

### Risposta SLM-RAG

La Bastiglia fu presa il 14 luglio 1789. Simboleggiò l'inizio dei fermenti popolari e l'assalto popolare che sfociò in quel giorno, segnando un momento cruciale della Rivoluzione Francese.

### Ground Truth

La Bastiglia fu presa il 14 luglio 1789. L'evento rappresentò una svolta simbolica della Rivoluzione Francese, segnando il passaggio dall'azione delle assemblee all'azione popolare diretta contro il potere monarchico.

---

## 33. What was the War of the Vendée during the French Revolution?

*cos'era la guerra della Vandea durante la Rivoluzione Francese?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 16.1 ms | 7.2 ms (2.2x) |
| **Generazione** | 2835 ms | 562 ms |
| **Totale** | 2851 ms | 569 ms |
| **Pool chunk** | 181 | 25 |
| **Keyword hit** | 80% | 80% |

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
| **Retrieval** | 15.8 ms | 5.5 ms (2.9x) |
| **Generazione** | 5367 ms | 5348 ms |
| **Totale** | 5383 ms | 5353 ms |
| **Pool chunk** | 181 | 9 |
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

**Principali campagne:**
*   **Campagna di Russia (1812):** Napoleone iniziò questa campagna dopo che la Russia si dissociò dal blocco contro gli Inglesi. Sebbene ci fosse stata una rapida conquista del territorio, i francesi furono obbligati a una "ritirata invernale disastrosa".
*   **Sconfitta di Lipsia (1813):** Dopo questa sconfitta militare, Napoleone fu costretto ad un primo esilio.

**Come finì il suo impero:**
Dopo quasi un anno di pausa, Napoleone fuggì dall'esilio sull'isola d'Elba nel 1815 e iniziò il periodo dei "100 giorni", cercando un recupero militare rendendo le leggi più liberali. Tuttavia, dopo la sconfitta definitiva nella **battaglia di Waterloo (1815)**, l'imperatore fu condannato dagli inglesi all'esilio sulla lontana isola di **S.Elena**, dove morì nel 1821. Contemporaneamente, in Europa iniziò il periodo della

### Ground Truth

Napoleone condusse la campagna d'Italia con la nascita delle Repubbliche, la campagna d'Egitto che ne accelerò l'ascesa politica, poi instaurò il Consolato e l'Impero estendendo l'egemonia sull'Europa. La conquista di Mosca segnò l'inizio del declino; l'impero si concluse con la sconfitta definitiva e l'esilio sull'isola di Sant'Elena.

---

## 35. What did the Congress of Vienna decide and who were its main actors?

*cosa stabilì il Congresso di Vienna e chi ne furono i protagonisti?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 15.6 ms | 6.3 ms (2.5x) |
| **Generazione** | 5394 ms | 2333 ms |
| **Totale** | 5410 ms | 2339 ms |
| **Pool chunk** | 181 | 18 |
| **Keyword hit** | 100% | 40% |

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

The answer is not available in the provided context.

While the context mentions the "Congresso di Vienna" in Chunk 3 and Chunk 4 as a reference for maps of Europe and Italy drawn after 1815, it does not describe what the Congress established or list its protagonists. The text focuses instead on the revolutions of 1848, the rise of Prussia and Bismarck, and the revolutions of 1830 in France and Belgium.

### Ground Truth

Il Congresso di Vienna stabilì un nuovo assetto europeo volto a restaurare l'ordine precedente alla Rivoluzione Francese e alle conquiste napoleoniche. Portò alla creazione della Santa Alleanza tra le potenze conservatrici. I protagonisti furono i rappresentanti delle grandi potenze europee vincitrici su Napoleone.

---

## 36. Who was Mazzini and what was the Giovine Italia?

*chi era Mazzini e cos'era la Giovine Italia?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 15.5 ms | 5.5 ms (2.8x) |
| **Generazione** | 5343 ms | 4942 ms |
| **Totale** | 5358 ms | 4947 ms |
| **Pool chunk** | 181 | 10 |
| **Keyword hit** | 100% | 80% |

### Risposta StdRAG

Basandosi sul contesto fornito, ecco le risposte alle domande:

**Chi era Mazzini?**
Giuseppe Mazzini era un genovese di famiglia agiata. Inizialmente aderì alla Carboneria, ma si rese conto che la segretezza dei suoi fini era un elemento limitante. Mostrò fin da giovane interesse per le idee democratiche e patriottiche; a 22 anni entrò nella Carboneria e, dopo essere stato arrestato, fu costretto all'esilio a Marsiglia dove entrò in contatto con patrioti esuli. Attraverso studi e dibattiti, arrivò alla conclusione che le associazioni segrete dovessero rinunciare alla segretezza per coinvolgere il popolo. Univa la politica a una personale visione religiosa e i suoi motti erano "Dio e Popolo" e "Pensiero e Azione".

**Cos'era la Giovine Italia?**
La Giovine Italia fu fondata da Mazzini nel 1831. Era un'associazione che si diffondeva soprattutto nel nord Italia (in Lombardia, Liguria, Toscana e Stato pontificio) con lo scopo di unificare il Paese e liberarlo dal potere assoluto dei governanti. Il suo programma prevedeva che

### Risposta SLM-RAG

Secondo il contesto fornito, Giuseppe Mazzini era un genovese di famiglia agiata, nato nel 1805, che mostrò fin da giovane interesse per le idee democratiche e patriottiche. Inizialmente aderì alla Carboneria, ma si rese conto che la segretezza dei suoi fini era un elemento limitante, portando alla sua uscita e all'esilio a Marsiglia dove entrò in contatto con patrioti esuli.

La **Giovine Italia** fu fondata da Mazzini nel 1831. Era un'associazione che si diffondeva soprattutto nel nord Italia (in Lombardia, Liguria, Toscana e Stato pontificio) con lo scopo di unificare il Paese e liberarlo dal potere assoluto dei governanti. Il programma dell'associazione prevedeva che l'Italia dovesse essere **una, libera, indipendente e repubblicana**. Il metodo scelto per raggiungere questi obiettivi era quello dell'**insurrezione popolare**. L'associazione univa la politica a una personale visione religiosa e aveva come motti "Dio e Popolo" e "Pensiero e Azione".

### Ground Truth

Giuseppe Mazzini fu uno dei principali protagonisti del Risorgimento e fondatore della Giovine Italia, un'associazione che propugnava l'indipendenza e l'unificazione dell'Italia come nazione libera e repubblicana, ispirata al motto 'Dio e Popolo'.

---

## 37. What was Cavour's role in the unification of Italy?

*quale fu il ruolo di Cavour nell'unificazione d'Italia?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 16.0 ms | 5.2 ms (3.1x) |
| **Generazione** | 5438 ms | 5369 ms |
| **Totale** | 5454 ms | 5374 ms |
| **Pool chunk** | 181 | 7 |
| **Keyword hit** | 80% | 60% |

### Risposta StdRAG

In base al contesto fornito, il ruolo di Cavour nell'unificazione d'Italia può essere sintetizzato nei seguenti punti:

*   **Ruolo politico e ideologico:** Cavour è definito un "abile politico" e un "nobile imprenditore" con idee **liberali**. La sua politica interna garantiva i diritti individuali e proponeva il **liberismo** economico. Ha attuato riforme agricole, industriali e ha creato la prima rete ferroviaria italiana. Ha inoltre cercato una netta separazione dalla Chiesa ("libera chiesa in libero stato") e ha usato il Piemonte come rifugio per i patrioti che vedevano nella casa Savoia l'unica via per l'unificazione.
*   **Organizzazione dell'unità:** Per ridurre l'influenza di Mazzini e garantire il controllo dei Savoia sull'unificazione, ha fondato la **Società Nazionale Italiana**.
*   **Politica estera e alleanze:** Cavour ha capito che l'Italia non poteva unificarsi senza aiuti internazionali. Per ottenere il credito di Francia e Inghilterra, ha inviato l'esercito piemontese alla guerra in Crimea (1853). Ha stretto un'intesa segreta

### Risposta SLM-RAG

In base al contesto fornito, il ruolo di Cavour nell'unificazione d'Italia può essere sintetizzato nei seguenti punti:

*   **Stratega politico e diplomatico:** Cavour è definito un "abile politico" che, invece di chiedere nuovi territori, mise in evidenza il pericolo che il conservatorismo asburgico rappresentava per l'equilibrio della penisola. Ha compreso che senza aiuti internazionali era impossibile modificare la situazione in Italia.
*   **Promotore del liberalismo e del liberismo:** La sua politica interna era di tipo liberale, garantiva i diritti individuali e proponeva il liberismo economico. Ha attuato riforme agricole, industriali (creazione dell'Ansaldo e della prima rete ferroviaria) e ha cercato una netta separazione dalla Chiesa ("libera chiesa in libero stato").
*   **Architetto dell'alleanza franco-piemontese:** Grazie all'attentato di Felice Orsini, convinse Napoleone III che era necessario agire per la questione italiana. Il 21 luglio 1858, a Plombières, concordò con l'imperatore francese un intervento a fianco del Regno di Sardegna contro l'Austria, in cambio

### Ground Truth

Camillo Benso conte di Cavour fu la figura politica centrale del processo di unificazione. Attuò riforme nel Regno di Sardegna, condusse una politica estera che portò all'alleanza con la Francia, guidò la Seconda guerra d'Indipendenza e creò le condizioni diplomatiche per la Spedizione dei Mille di Garibaldi.

---

## 38. What was Taylorism and in what historical context did it emerge?

*cos'era il Taylorismo e in quale contesto storico nacque?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 16.2 ms | 5.5 ms (2.9x) |
| **Generazione** | 1622 ms | 526 ms |
| **Totale** | 1638 ms | 531 ms |
| **Pool chunk** | 181 | 7 |
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
| **Retrieval** | 15.6 ms | 4.7 ms (3.3x) |
| **Generazione** | 2792 ms | 413 ms |
| **Totale** | 2808 ms | 418 ms |
| **Pool chunk** | 181 | 3 |
| **Keyword hit** | 67% | 33% |

### Risposta StdRAG

La dottrina Monroe fu proclamata dal Presidente Monroe nel 1800 (o all'inizio del 1800) e stabiliva che gli interessi dell'America spettavano agli americani, opponendosi alle ingerenze dell'Europa. Fu emessa in un contesto di espansione verso ovest (il "mitico west"), che portò alla distruzione dei pellirossa a causa dei tanti coloni provenienti dall'Europa. Inoltre, in quel periodo, gli Stati Uniti erano ormai 27 e l'economia era ben distinta: industriale nel Nord e agricola nel Sud.

### Risposta SLM-RAG

The answer is not available in the provided context.

### Ground Truth

La dottrina Monroe fu proclamata nell'ambito delle lotte per l'indipendenza dell'America latina e dei moti liberali. Affermava il principio che l'America non doveva essere considerata campo di ulteriore colonizzazione europea, opponendosi all'interventismo delle potenze del Vecchio Continente nelle Americhe.

---

## 40. How were the price revolution of the 16th century and the geographical discoveries connected?

*come erano collegati la rivoluzione dei prezzi del Cinquecento e le scoperte geografiche?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 16.7 ms | 5.1 ms (3.3x) |
| **Generazione** | 2704 ms | 1280 ms |
| **Totale** | 2721 ms | 1285 ms |
| **Pool chunk** | 181 | 4 |
| **Keyword hit** | 100% | 100% |

### Risposta StdRAG

Secondo il contesto fornito, la **rivoluzione dei prezzi** del Cinquecento fu causata dall'**importazione di enormi quantità di oro e di argento dalle Americhe**, che avvenne grazie alle **scoperte geografiche** (in particolare quelle della Spagna e del Portogallo).

Questo afflusso di metalli preziosi causò la perdita di valore della moneta, portando a un incremento dei prezzi del 400% circa. Di conseguenza, i salariati furono i più penalizzati perché l'inflazione erose il loro potere d'acquisto.

### Risposta SLM-RAG

Le scoperte geografiche, in particolare l'importazione di enormi quantità di oro e di argento dalle Americhe da parte della Spagna e del Portogallo, causarono la perdita di valore della moneta, il che spiega il fenomeno della rivoluzione dei prezzi.

### Ground Truth

Nel Cinquecento i prezzi subirono un incremento di circa il 400%. Il pensatore Jean Bodin spiegò il fenomeno sostenendo che l'importazione massiccia di oro e argento dalle Americhe da parte di Spagna e Portogallo aveva causato la svalutazione della moneta. I salariati furono i più penalizzati, poiché l'inflazione erose il loro già esiguo potere d'acquisto.

---

