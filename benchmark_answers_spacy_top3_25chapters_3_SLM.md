# Benchmark RAG — storia

**Modello:** Qwen/Qwen3.5-4B  |  **top-k:** 3  |  **top-N SLM:** 3

| Metrica | StdRAG | SLM-RAG |
|---|---|---|
| Speedup retrieval | — | **2.3x** |
| Pool medio | 83 chunk | 11 chunk (-86%) |
| Keyword hit | 55% | **55%** |
| Overlap medio top-3 | 59% | — |

---

## 1. Who imported spices into Europe during the Middle Ages?

*da chi venivano importate le spezie in europa nel medioevo?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 11.1 ms | 4.0 ms (2.8x) |
| **Generazione** | 4028 ms | 460 ms |
| **Totale** | 4039 ms | 464 ms |
| **Pool chunk** | 83 | 6 |
| **Keyword hit** | 100% | 17% |

### Risposta StdRAG

Dall'Oriente.

### Risposta SLM-RAG

The answer is not available in the provided context.

### Ground Truth

Il commercio delle spezie era controllato dai mercanti arabi insieme alla repubblica veneziana, che detenevano il monopolio attraversando i territori musulmani. I molteplici rischi del viaggio e i vari passaggi di mano aumentavano considerevolmente il prezzo della merce.

---

## 2. What territories did Charles V control?

*quali territori controllava Carlo V?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 10.3 ms | 4.1 ms (2.5x) |
| **Generazione** | 5254 ms | 3703 ms |
| **Totale** | 5264 ms | 3708 ms |
| **Pool chunk** | 83 | 6 |
| **Keyword hit** | 33% | 33% |

### Risposta StdRAG

Based on the provided context, the territories controlled by Charles V (Carlo V) include:

*   **The Duchy of Milan:** He occupied it to remove it from French dominance.
*   **Spain and its possessions:** The text mentions the "possessions of the Spanish" (*possedimenti spagnoli*) and refers to the "Spanish Empire" (*Impero Spagnolo*).
*   **The Holy Roman Empire (specifically German territories):** The text notes his desire to impose his sovereignty over "German princes" (*principi tedeschi*) and mentions his realms in 1598 (though this is a later date, it confirms the scope of his empire).
*   **Italy (as a strategic field of battle):** While not explicitly listed as a permanent possession in the same way as Spain, the text describes Italy as the "natural communication route" between Spanish and Habsburg possessions in central Europe and a "battlefield" where his forces fought.

The text does not provide a complete, exhaustive list of every specific territory he controlled at any given moment, but it highlights the strategic importance of **Italy**, the **Duchy of Milan**, **Spain**, and the **German princes** under his influence or sovereignty.

### Risposta SLM-RAG

Based on the provided context, the territories controlled by **Carlo V** are:

*   **Ducato di Milano** (Duchy of Milan)
*   **Regno di Napoli** (Kingdom of Naples)
*   **Sicilia** (Sicily)
*   **Sardegna** (Sardinia)
*   **Coste toscane** (Tuscan coasts)

This information is found in **Chunk 2**, which states: "Gli Spagnoli invece dominavano direttamente sul ducato di Milano, sul Regno di Napoli, sulla Sicilia, sulla Sardegna e lungo le coste toscane." Since Carlo V was the Spanish sovereign at the time of the peace of Cateau-Cambrésis (mentioned in the same section), these were the territories under his direct dominion.

### Ground Truth

Carlo V controllava un vasto impero che comprendeva la Spagna, i territori asburgici, le Fiandre, il Regno di Napoli e le colonie americane. Il suo regno fu segnato da conflitti con la Francia, i principi tedeschi luterani e l'impero ottomano.

---

## 3. What were the main causes of the French Revolution?

*quali furono le cause della rivoluzione francese?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 10.3 ms | 4.8 ms (2.1x) |
| **Generazione** | 5213 ms | 5223 ms |
| **Totale** | 5223 ms | 5228 ms |
| **Pool chunk** | 83 | 12 |
| **Keyword hit** | 33% | 33% |

### Risposta StdRAG

Based on the provided context, the causes of the French Revolution include:

*   **Social and Economic Crisis:** The consequences of famines and poor harvests, specifically in 1788, which were caused by erratic weather patterns ("capricci del clima"). This led to a significant increase in the price of bread.
*   **Agricultural Dependence:** The fact that land was the main source of income in a country with approximately 25 million inhabitants, making the population highly vulnerable to agricultural failures.
*   **The "Ancien Régime" Structure:** The prevailing model of state, economy, and politics at the end of the 1700s, characterized by:
    *   Absolute monarchy.
    *   A society divided into rigid social orders.
    *   The persistence of feudal rights.
*   **Moral Decay and Inequality:** While the text explicitly links moral decay and luxury in the papal court to the causes of the *Reformation* (in Chunk 1), it notes in Chunk 3 that the French society was divided into rigid orders and subject to feudal rights, implying a similar structural inequality and social tension that contributed to the revolutionary climate.

*Note: The text

### Risposta SLM-RAG

In base al contesto fornito, le cause della Rivoluzione Francese includono:

*   **Crisi agraria e carestie:** Nel 1788, capricci del clima provocarono raccolti esigui, portando a carestie e all'aumento del prezzo del pane.
*   **Struttura economica e sociale dell'Ancien Régime:** Il modello di stato e di economia vigeva alla fine del 1700 con una monarchia assoluta, una società divisa in rigidi ordini sociali e la persistenza di diritti feudali.
*   **Conflitto con la Chiesa:** La confisca di beni, lo scioglimento degli ordini religiosi (eccettuati quelli di assistenza e istruzione) e l'approvazione della Costituzione Civile del Clero, che sottoponeva i religiosi al controllo statale, crearono una rottura con il clero e una frattura nell'opinione pubblica.
*   **Politica economica radicale:** La creazione del "maximum" (prezzo massimo del grano e della farina) e la leva di massa per l'arruolamento di 300.000 uomini, che creò malcontento nelle

### Ground Truth

Le principali cause della Rivoluzione Francese furono la crisi economica dell'Ancien Régime, le ingiustizie fiscali che gravavano sul terzo stato, la convocazione degli Stati Generali e la crescente influenza dell'opinione pubblica. La nobiltà e il clero godevano di privilegi fiscali che alimentavano il malcontento popolare.

---

## 4. What were the key principles of the Enlightenment?

*quali erano i principi fondamentali dell'illuminismo?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 10.6 ms | 5.3 ms (2.0x) |
| **Generazione** | 5222 ms | 3999 ms |
| **Totale** | 5232 ms | 4004 ms |
| **Pool chunk** | 83 | 20 |
| **Keyword hit** | 67% | 67% |

### Risposta StdRAG

In base al contesto fornito, i principi fondamentali dell'Illuminismo sono:

*   **La ragione:** È il "lume naturale" dell'uomo che sollecita a svincolarsi dalle tradizioni e dai pregiudizi per affermare un nuovo modo di guardare la realtà, la società, la politica, la cultura e la religione.
*   **Il coraggio di usare la propria intelligenza:** Espresso dal motto *Sapere aude* ("Abbi il coraggio di servirti della tua intelligenza").
*   **L'accesso universale al sapere:** Rappresentato dall'*Enciclopedia*, che intendeva spiegare tutte le conoscenze disponibili in ordine alfabetico per renderle disponibili a tutti.
*   **La libertà individuale e le libertà fondamentali:** Include la proprietà privata, la libertà di espressione, di parola, di stampa e di iniziativa economica.
*   **Il liberalismo economico:** Un principio che porta lo Stato a non intervenire nell'economia, lasciando che si autoregoli secondo il disegno di una "mano invisibile" (teoria di Adam Smith).
*   **La critica alle pratiche religiose oppressive:** Come le indulgenze e i pellegrinaggi, visti come strumenti per

### Risposta SLM-RAG

In base al contesto fornito, i principi fondamentali dell'Illuminismo sono:

*   **La ragione:** È il "lume" naturale dell'uomo che sollecita a svincolarsi dalle tradizioni e dai pregiudizi.
*   **L'audacia intellettuale:** Espressa dal motto *Sapere aude* ("Abbi il coraggio di servirti della tua intelligenza").
*   **L'accesso universale al sapere:** Rappresentato dall'*Enciclopedia*, che intendeva spiegare tutte le conoscenze disponibili in ordine alfabetico per renderle disponibili a tutti.
*   **Un nuovo modo di guardare la realtà:** Che include la società, la politica, la cultura e la religione.
*   **L'uscita dallo stato di minorità:** Definizione data da Kant, dove l'uomo deve imputare a se stesso la necessità di uscire da questa condizione.

### Ground Truth

L'Illuminismo si fondava sul primato del 'lume naturale' della ragione come strumento di conoscenza e critica della realtà. I philosophes propugnavano una nuova visione dell'economia e della politica basata sulla libertà, sul progresso e sui diritti naturali dell'individuo.

---

## 5. What was the American Revolution?

*che cosa fu la rivoluzione americana?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 10.3 ms | 4.1 ms (2.5x) |
| **Generazione** | 456 ms | 453 ms |
| **Totale** | 466 ms | 457 ms |
| **Pool chunk** | 83 | 10 |
| **Keyword hit** | 33% | 33% |

### Risposta StdRAG

The answer is not available in the provided context.

### Risposta SLM-RAG

The answer is not available in the provided context.

### Ground Truth

La Rivoluzione Americana fu il processo con cui le tredici colonie americane si ribellarono al dominio inglese, principalmente a causa delle difficili condizioni economiche e fiscali imposte dalla madrepatria. Nel 1776 fu stilata la Dichiarazione d'Indipendenza; la sconfitta inglese fu sancita dalla pace di Parigi del 1783, che diede vita al nuovo stato federale americano.

---

## 6. Who were the Mongols and how did they expand?

*chi erano i mongoli e come si espansero?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 10.2 ms | 3.9 ms (2.6x) |
| **Generazione** | 453 ms | 5036 ms |
| **Totale** | 463 ms | 5040 ms |
| **Pool chunk** | 83 | 9 |
| **Keyword hit** | 0% | 67% |

### Risposta StdRAG

The answer is not available in the provided context.

### Risposta SLM-RAG

I mongoli erano un popolo che, sotto la guida di Gengis Khan, si espanso rapidamente grazie a un esercito composto da cavalieri addestrati e pronti a tutto, la cui ferocia nei combattimenti permise questa rapida espansione. Venivano chiamati dagli europei "Tartari", termine derivante dal "Tartaro" (l'inferno).

L'espansione iniziò con Gengis Khan, che scatenò un'offensiva verso la Cina, arrivando oltrepassare la Grande Muraglia, poi occupò le steppe della Russia meridionale conquistando le città di Samarcanda e Bukara, e infine volse il suo attacco verso la Persia, la Georgia e la Bulgaria. Dopo la sua morte, i suoi successori continuarono l'espansione arrivando a Baghdad nel 1258 e in Polonia, dove travolsero la cavalleria polacco-tedesca conquistando l'Ungheria.

Il regno di Gengis Khan fu diviso tra i suoi quattro figli, dando origine a quattro Khanati, tra cui quello del Gran Khan in Cina.

### Ground Truth

I Mongoli erano un popolo di cavalieri guidati da Gengis Khan, che scatenò la sua offensiva verso la Cina oltrepassando la Grande Muraglia, poi occupò le steppe della Russia meridionale, conquistò Samarcanda e Bukara e attaccò Persia, Georgia e Bulgaria. Erano chiamati Tartari dagli europei. Dopo la sua morte il regno fu diviso tra i quattro figli, dando origine a quattro Khanati.

---

## 7. What was Luther's Protestant Reformation?

*che cosa fu la riforma protestante di lutero?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 10.1 ms | 3.9 ms (2.6x) |
| **Generazione** | 2869 ms | 2868 ms |
| **Totale** | 2879 ms | 2872 ms |
| **Pool chunk** | 83 | 11 |
| **Keyword hit** | 67% | 67% |

### Risposta StdRAG

The answer is not available in the provided context.

While the context mentions Martin Luther's birth, his entry into the Augustinian convent, his traumatic religious experience, his teaching at the University of Wittenberg, and his course on the Letter to the Romans where he found answers to his questions, it does not explicitly define or describe "what the Protestant Reformation of Luther was" in terms of its core theological tenets, historical impact, or specific actions taken by him as a reformer. The text focuses more on the causes of the Reformation, the role of indulgences, and the subsequent spread of Calvinism and the English Reformation.

### Risposta SLM-RAG

The answer is not available in the provided context.

While the context mentions Martin Luther's birth, his entry into the Augustinian convent, his traumatic religious experience, his teaching at the University of Wittenberg, and his course on the Letter to the Romans where he found answers to his questions, it does not explicitly define or describe "what the Protestant Reformation of Luther was" in terms of its core theological tenets, historical impact, or specific actions taken by him as a reformer. The text focuses more on the causes of the Reformation, the role of indulgences, and the subsequent spread of Calvinism and the English Reformation.

### Ground Truth

La Riforma protestante di Lutero segnò una rottura definitiva con la dottrina cattolica, ribadita nella Confessione Augustana presentata da Filippo Melantone alla Dieta di Augusta del 1530. La pace di Augusta del 1555 riconobbe ufficialmente la religione protestante stabilendo il principio 'cuius regio eius religio'.

---

## 8. How was the Italian state formed during the Risorgimento?

*come si formò lo stato italiano nel risorgimento?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 9.8 ms | 4.1 ms (2.4x) |
| **Generazione** | 4941 ms | 5210 ms |
| **Totale** | 4951 ms | 5214 ms |
| **Pool chunk** | 83 | 12 |
| **Keyword hit** | 33% | 33% |

### Risposta StdRAG

Based on the provided context, the formation of the Italian state during the Risorgimento is described as follows:

The process began around **1861** with the unification of Italy, which was the result of a complex set of events, political doctrines, and initiatives. This process aimed to achieve the independence of the territory from foreign occupation and the unification of various internal kingdoms, a condition Italy had lived in for centuries.

The unification was driven by a political debate between two opposing factions:
*   **The Moderates (Historical Right):** They believed the national unification could be achieved by gradually involving the existing monarchic governments, particularly the Kingdom of Sardinia (Savoia).
*   **The Democrats (Historical Left):** They opposed the reliability of the monarchs, citing the disastrous outcomes of the uprisings of the 1820s and 1830s.

The text notes that while the unification process was underway, the new state faced significant economic and social backwardness compared to other European powers, with a population mostly composed of peasants, low industrialization, and high illiteracy.

### Risposta SLM-RAG

Lo stato italiano si formò attraverso un processo di unificazione che condusse alla proclamazione del Regno d'Italia il 17 marzo 1861 a Torino, quando Vittorio Emanuele II fu proclamato Re d'Italia. Questo evento segna la fine del processo iniziato nel 1861, che ha visto la graduale unificazione dei vari regni interni e l'indipendenza del territorio dall'occupazione straniera.

Il processo fu sostenuto da un'intesa tra il Primo Ministro italiano, Camillo Benso di Cavour, e l'Imperatore francese Napoleone III, conclusasi a Plombières il 21 luglio 1858. Secondo questi accordi, la Francia avrebbe intervenuto a fianco del Regno di Sardegna solo in caso di guerra dichiarata dall'Austria. In cambio, in caso di vittoria, la Francia avrebbe ottenuto Nizza e la Savoia, e l'Italia sarebbe stata divisa in un Regno dell'Alta Italia (sotto i Savoia), un Regno del Centro Italia (guidato da Girolamo Bonaparte) e il Regno delle due Sicilie (con il figlio di Gioacchino Murat come re), mentre il Papa avrebbe mantenuto il Lazio

### Ground Truth

L'unità d'Italia fu il risultato del Risorgimento, guidato da figure come Mazzini (fondatore della Giovine Italia), Cavour (che condusse la politica diplomatica e la Seconda guerra d'Indipendenza) e Garibaldi (che guidò la Spedizione dei Mille). Il Piemonte fu il fulcro del processo unitario.

---

## 9. What were the social consequences of the Industrial Revolution?

*quali furono le conseguenze sociali della rivoluzione industriale?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 9.1 ms | 4.1 ms (2.2x) |
| **Generazione** | 5261 ms | 5295 ms |
| **Totale** | 5270 ms | 5299 ms |
| **Pool chunk** | 83 | 14 |
| **Keyword hit** | 100% | 100% |

### Risposta StdRAG

Le conseguenze sociali della Rivoluzione Industriale, secondo il contesto fornito, includono:

*   **Cambiamento demografico e urbano:** Inizia un profondo aumento demografico; cambiano gli spazi con la crescita delle città e la formazione di nuovi quartieri, in particolare di operai impiegati nelle fabbriche.
*   **Nascita di nuove classi sociali:** Si passa da una società chiusa a una con nuove classi, tra cui la borghesia, i ceti emergenti, la nuova figura dell'imprenditore e il proletariato (chi ha solo i figli come ricchezza).
*   **Migrazione e lavoro:** Molti braccianti fuggono dalla campagna (a causa delle *enclosures*) per trovare lavoro nelle prime fabbriche. Il lavoro diventa parcellizzato e comporta lo sfruttamento della mano d'opera, che include donne e bambini.
*   **Fenomeno del Luddismo:** Nasce come reazione al cambiamento e allo sfruttamento.
*   **Diffusione dell'informazione:** Si diffonde l'informazione con la nascita dei primi giornali (gazzette), sia statali che indipendenti, che favoriscono la circolazione di conoscenze tra borghesia e ceti emerg

### Risposta SLM-RAG

In base al contesto fornito, le conseguenze sociali della Rivoluzione Industriale includono:

*   **Cambiamento demografico e urbano:** Inizia un profondo aumento demografico; crescono le città e si formano nuovi quartieri, in particolare di operai impiegati nelle fabbriche.
*   **Nascita di nuove classi sociali:** Si passa da una società chiusa a una con nuove classi, tra cui il **proletariato** (chi ha solo i figli come ricchezza) e la **borghesia capitalista** (formata dai proprietari dei mezzi di produzione/imprenditori).
*   **Sfruttamento del lavoro:** Si diffonde il lavoro parcellizzato e lo sfruttamento della mano d'opera, che include donne e bambini (spesso introdotti al lavoro verso i sette anni, sottopagati e soggetti a lunghi turni, fino a 16 ore giornaliere).
*   **Condizioni di vita nelle città:** Le città crescono rapidamente con quartieri operai caratterizzati da miseria, sporcizia, carenze igieniche e diffusione dell'alcolismo.
*   **Fenomeno del Luddismo:** Nasce come reazione al cambiamento e allo sfrutt

### Ground Truth

La Rivoluzione Industriale determinò la nascita del proletariato operaio, che lavorava in fabbriche in condizioni di sfruttamento. Si accentuò la divisione tra borghesia proprietaria e classe operaia. Gli effetti negativi dell'industrializzazione includevano orari di lavoro estenuanti e condizioni igieniche precarie.

---

## 10. How did the population of Europe change from the year 1000 to the 14th century?

*come cambiò la popolazione europea dall'anno Mille al Trecento?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 9.1 ms | 3.3 ms (2.7x) |
| **Generazione** | 981 ms | 1019 ms |
| **Totale** | 990 ms | 1022 ms |
| **Pool chunk** | 83 | 5 |
| **Keyword hit** | 100% | 100% |

### Risposta StdRAG

La popolazione europea raddoppiò, passando da circa 40 milioni di abitanti all'inizio del Mille a circa 80 milioni all'inizio del Trecento.

### Risposta SLM-RAG

La popolazione europea aumentò raddoppiando, passando da circa 40 milioni di abitanti all'inizio del Mille a circa 80 milioni all'inizio del Trecento.

### Ground Truth

La popolazione europea aumentò dall'anno Mille fino all'inizio del Trecento, raddoppiando da circa 40 milioni a circa 80 milioni di abitanti. Questo comportò la necessità di disboscare nuovi terreni per aumentare la produzione, anche se si verificarono ciclicamente carestie decennali che causarono migliaia di vittime.

---

## 11. How did the plague spread from Crimea to Europe?

*come si diffuse la peste dalla Crimea all'Europa?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 10.4 ms | 4.4 ms (2.4x) |
| **Generazione** | 4442 ms | 3902 ms |
| **Totale** | 4452 ms | 3907 ms |
| **Pool chunk** | 83 | 17 |
| **Keyword hit** | 100% | 100% |

### Risposta StdRAG

La peste si diffuse dalla Crimea all'Europa attraverso i seguenti passaggi:

1.  **Origine in Crimea:** La prima epidemia scoppiò in una colonia genovese situata in Crimea, assediata dai Tartari. Gli assedianti gettarono cadaveri infettati dal morbo, con le catapulte, al di là delle mura urbane.
2.  **Diffusione interna a Genova:** A causa del rapido diffondersi del contagio, i genovesi si arresero. Alcuni cittadini riuscirono a fuggire e salparono verso l'Italia, portando il contagio con sé.
3.  **Arrivo in Italia:** Intorno al 1347 la peste raggiunse Genova, Venezia e la Sicilia.
4.  **Espansione in Europa:** L'anno successivo (1348), la malattia dilagò in Toscana, per poi diffondersi in Francia, Inghilterra, Spagna e Germania.

### Risposta SLM-RAG

La peste si diffuse dalla Crimea all'Europa attraverso i seguenti passaggi:

1.  **Origine in Crimea:** La prima epidemia scoppiò in una colonia genovese situata in Crimea, assediata dai Tartari.
2.  **Trasporto iniziale:** Gli assedianti gettarono cadaveri infettati dal morbo, tramite catapulte, al di fuori delle mura della città.
3.  **Fuga dei sopravvissuti:** Alcuni cittadini genovesi riuscirono a fuggire e salparono verso l'Italia.
4.  **Arrivo in Europa:** Questi fuggitivi portarono il contagio in Italia. Intorno al 1347 la malattia raggiunse Genova, Venezia e la Sicilia; l'anno successivo si diffuse in Toscana, Francia, Inghilterra, Spagna e Germania.

### Ground Truth

La prima epidemia di peste scoppiò in una colonia genovese in Crimea assediata dai Tartari, che lanciarono con le catapulte cadaveri infettati oltre le mura. I cittadini genovesi in fuga portarono il contagio via mare. Intorno al 1347 la peste raggiunse Genova, Venezia e la Sicilia, dilagando l'anno successivo in Toscana, Francia, Inghilterra, Spagna e Germania. Nel 1353 aveva ucciso circa un terzo della popolazione europea.

---

## 12. Who were blamed for spreading the plague and what happened to them?

*chi fu accusato di diffondere la peste e cosa accadde?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 10.4 ms | 3.9 ms (2.7x) |
| **Generazione** | 448 ms | 3060 ms |
| **Totale** | 458 ms | 3064 ms |
| **Pool chunk** | 83 | 8 |
| **Keyword hit** | 0% | 0% |

### Risposta StdRAG

The answer is not available in the provided context.

### Risposta SLM-RAG

In base al contesto fornito, non è indicato chi fu specificamente **accusato** di diffondere la peste. Il testo descrive solo come la malattia si diffuse:

1.  La prima epidemia scoppiò in una colonia genovese in Crimea assediata dai Tartari.
2.  Gli assedianti gettarono cadaveri infettati con le catapulte al di fuori delle mura.
3.  Alcuni cittadini genovesi riuscirono a fuggire e salparono verso l'Italia, **portando il contagio**.

Il contesto non menziona alcuna accusa formale o un processo contro qualcuno per aver diffuso la peste.

### Ground Truth

Come capri espiatori furono indicati emarginati, lebbrosi e soprattutto gli Ebrei, accusati di avvelenare l'acqua dei pozzi o di contaminare l'aria con veleni. Di conseguenza migliaia di ebrei subirono persecuzioni — i pogrom — in Francia, Germania e Svizzera.

---

## 13. Who was Henry the Navigator and what was his contribution to exploration?

*chi era Enrico il Navigatore e qual è il suo contributo all'esplorazione?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 9.3 ms | 4.5 ms (2.1x) |
| **Generazione** | 2246 ms | 2250 ms |
| **Totale** | 2255 ms | 2255 ms |
| **Pool chunk** | 83 | 18 |
| **Keyword hit** | 83% | 83% |

### Risposta StdRAG

Enrico il Navigatore era il re del Portogallo. Il suo contributo all'esplorazione fu quello di aver avviato l'età delle esplorazioni grazie alla sua attenzione. Fondò una scuola nautica nella sua residenza di Capo di Sagres nell'Algarve, dove venivano raccolte con cura tutte le informazioni sui fenomeni di alta e bassa marea e sull'andamento dei venti del "Mare Tenebroso" (l'Oceano Atlantico).

### Risposta SLM-RAG

Enrico il Navigatore era il re del Portogallo. Il suo contributo all'esplorazione fu quello di aver avviato l'età delle esplorazioni grazie alla sua attenzione. Fondò una scuola nautica nella sua residenza di Capo di Sagres nell'Algarve, dove venivano raccolte con cura tutte le informazioni sui fenomeni di alta e bassa marea e sull'andamento dei venti del "Mare Tenebroso" (l'Oceano Atlantico).

### Ground Truth

Enrico il Navigatore era il re del Portogallo che fondò una scuola nautica nella sua residenza di Capo di Sagres nell'Algarve. Lì si raccoglievano informazioni su maree, venti e sull'Oceano Atlantico. Favorì la sostituzione della galera con la più maneggevole caravella e avviò le esplorazioni portoghesi verso le Azzorre e la circumnavigazione dell'Africa.

---

## 14. What happened at the Diet of Augsburg in 1530?

*cosa accadde alla Dieta di Augusta del 1530?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 10.6 ms | 4.0 ms (2.6x) |
| **Generazione** | 500 ms | 448 ms |
| **Totale** | 511 ms | 452 ms |
| **Pool chunk** | 83 | 9 |
| **Keyword hit** | 17% | 0% |

### Risposta StdRAG

The answer is not available in the provided context.

### Risposta SLM-RAG

The answer is not available in the provided context.

### Ground Truth

Alla Dieta di Augusta del 1530 partecipò Filippo Melantone, portavoce di Lutero, che presentò la Confessione Augustana in cui furono ribadite le tesi luterane, sancendo la definitiva rottura con la dottrina cattolica. I principi tedeschi luterani avevano intanto costituito la Lega di Smalcalda in funzione anti-imperiale.

---

## 15. What was Calvin's doctrine of predestination?

*qual era la dottrina calvinista della predestinazione?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 9.5 ms | 4.1 ms (2.3x) |
| **Generazione** | 1572 ms | 1576 ms |
| **Totale** | 1582 ms | 1580 ms |
| **Pool chunk** | 83 | 12 |
| **Keyword hit** | 17% | 17% |

### Risposta StdRAG

Secondo il contesto fornito, la dottrina calvinista della predestinazione afferma che l'uomo, con la sua natura imperfetta, non può salvarsi per fede; è invece Dio, nella sua bontà imperscrutabile, a predestinare l'uomo alla salvezza eterna.

### Risposta SLM-RAG

Secondo il contesto fornito, la dottrina calvinista della predestinazione afferma che l'uomo, con la sua natura imperfetta, non può salvarsi per fede; è invece Dio, nella sua bontà imperscrutabile, a predestinare l'uomo alla salvezza eterna.

### Ground Truth

Calvino affermava la sovranità assoluta di Dio sull'uomo e la dottrina della predestinazione: l'umanità è divisa in eletti, destinati al Paradiso, e dannati. L'uomo con la sua natura imperfetta non può salvarsi per propria fede; è Dio a predestinarlo alla salvezza. Calvino riconobbe come sacramenti validi solo il battesimo e l'eucaristia.

---

## 16. What was England's Glorious Revolution?

*cos'era la Gloriosa Rivoluzione inglese?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 10.0 ms | 3.6 ms (2.8x) |
| **Generazione** | 2175 ms | 2178 ms |
| **Totale** | 2185 ms | 2182 ms |
| **Pool chunk** | 83 | 6 |
| **Keyword hit** | 60% | 60% |

### Risposta StdRAG

La "rivoluzione gloriosa" fu un passaggio storico in cui il Parlamento inglese depose il re cattolico Carlo II e gli offerse la corona a Guglielmo d'Orange, un calvinista olandese. Questo evento si caratterizzò per essere stato ottenuto in modo pacifico. In seguito, il nuovo re dovette firmare e accettare la dichiarazione dei diritti, con cui la Gran Bretagna divenne una monarchia costituzionale.

### Risposta SLM-RAG

La "Gloriosa Rivoluzione" fu un passaggio storico in cui il Parlamento inglese depose il re cattolico Carlo II e gli offrì la corona a Guglielmo d'Orange, un calvinista olandese. Questo evento si caratterizzò per essere stato ottenuto in modo pacifico. In seguito, il nuovo re dovette firmare e accettare la dichiarazione dei diritti, trasformando la Gran Bretagna in una monarchia costituzionale.

### Ground Truth

La Gloriosa Rivoluzione inglese è descritta nel contesto del passaggio dall'assolutismo verso forme più costituzionali di governo in Inghilterra nel Seicento, in cui il parlamento limitò il potere assoluto del sovrano.

---

## 17. What were the main features of the First Industrial Revolution?

*quali furono le caratteristiche principali della Prima Rivoluzione Industriale?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 9.0 ms | 5.4 ms (1.7x) |
| **Generazione** | 5266 ms | 5266 ms |
| **Totale** | 5275 ms | 5271 ms |
| **Pool chunk** | 83 | 14 |
| **Keyword hit** | 100% | 100% |

### Risposta StdRAG

Le caratteristiche principali della Prima Rivoluzione Industriale, secondo il contesto fornito, sono:

*   **Trasformazione economica e sociale:** passaggio da un'economia basata sull'agricoltura e una società chiusa a un'economia basata sulle macchine, sul lavoro operaio e alla nascita di nuove classi sociali.
*   **Fonti di energia:** utilizzo della forza motrice dell'acqua e del carbone.
*   **Aumento degli scambi:** crescita degli scambi commerciali e delle materie prime (commercio triangolare).
*   **Miglioramenti agricoli:** introduzione di nuove tecniche (rotazioni, primi macchinari), coltivazione di nuove piante e sviluppo dei terreni grazie alle recinzioni.
*   **Nuove tecnologie:** perfezionamento del telaio tessile (spoletta mobile), costruzione della macchina a vapore da parte di Watt, realizzazione della locomotiva e nascita delle ferrovie da parte di Stephenson.
*   **Nascita della fabbrica:** fuga dei braccianti dalla campagna (a causa delle enclosures), lavoro parcellizzato e sfruttamento della mano d'opera (inclusi donne e bambini), crescita delle città con quartieri operai

### Risposta SLM-RAG

Le caratteristiche principali della Prima Rivoluzione Industriale, secondo il contesto fornito, sono:

*   **Cambiamento economico e sociale:** passaggio da un'economia basata sull'agricoltura e una società chiusa a un'economia basata sulle macchine, sul lavoro operaio e alla nascita di nuove classi sociali.
*   **Fonti di energia:** utilizzo della forza motrice dell'acqua e del carbone.
*   **Aumento degli scambi:** crescita degli scambi commerciali e delle materie prime (incluso il commercio triangolare).
*   **Miglioramenti agricoli:** introduzione di nuove tecniche (rotazioni, primi macchinari), coltivazione di nuove piante e sviluppo dei terreni grazie alle recinzioni.
*   **Nuove tecnologie:** perfezionamento del telaio tessile (spoletta mobile), costruzione della macchina a vapore da parte di Watt, realizzazione della locomotiva e delle ferrovie da parte di Stephenson.
*   **Nascita della fabbrica:** molti braccianti fuggono dalla campagna (a causa delle enclosures) per lavorare nelle fabbriche, dove il lavoro è parcellizzato e sfruttato (con l'impiego di donne e bambini

### Ground Truth

La Prima Rivoluzione Industriale fu caratterizzata dall'introduzione di nuove tecnologie come la macchina a vapore di James Watt, dalla nascita della fabbrica come luogo di produzione accentrata, dall'uso massiccio del carbone e dalla trasformazione dei rapporti sociali con la nascita del proletariato operaio.

---

## 18. Who were the philosophes and what was their central idea?

*chi erano i philosophes e qual era la loro idea centrale?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 9.9 ms | 4.5 ms (2.2x) |
| **Generazione** | 3416 ms | 3899 ms |
| **Totale** | 3426 ms | 3903 ms |
| **Pool chunk** | 83 | 9 |
| **Keyword hit** | 83% | 83% |

### Risposta StdRAG

I **philosophes** erano studiosi e intellettuali che, insieme a figure come Montesquieu, Rousseau e Voltaire, diffusero il movimento illuminista in Francia durante il Settecento.

La loro idea centrale era quella della **ragione**, definita come il "lume naturale" dell'uomo. Questa ragione sollecitava gli individui a svincolarsi dalle tradizioni e dai pregiudizi per affermare un nuovo modo di guardare la realtà, la società, la politica, la cultura e la religione. L'obiettivo era rendere il sapere accessibile a tutti, come dimostrò l'*Enciclopedia*, e guidare l'uomo verso la maturità attraverso il coraggio di usare la propria intelligenza (*Sapere aude*).

### Risposta SLM-RAG

In base al contesto fornito, i **philosophes** erano studiosi e intellettuali che, insieme all'Inghilterra, diffusero il movimento illuminista in Francia nel Settecento. Tra di essi si ricordano Montesquieu, Rousseau e Voltaire.

La loro **idea centrale** era quella della **ragione**, definita come il "lume" naturale dell'uomo. Questa ragione sollecitava l'uomo a svincolarsi dalle tradizioni e dai pregiudizi per affermare un nuovo modo di guardare la realtà, la società, la politica, la cultura e la religione. L'obiettivo era rendere il sapere accessibile a tutti, come dimostrò l'*Enciclopedia*, e il motto che esprimeva lo spirito illuminista era "**Sapere aude**" (Abbi il coraggio di servirti della tua intelligenza).

### Ground Truth

I philosophes erano i pensatori dell'Illuminismo che sostenevano il primato del 'lume naturale' della ragione come strumento di conoscenza e critica della realtà sociale e politica. Proponevano una nuova visione dell'economia e della politica fondata sui diritti naturali e sul progresso.

---

## 19. What were the economic causes of the French Revolution?

*quali furono le cause economiche della Rivoluzione Francese?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 9.7 ms | 3.7 ms (2.7x) |
| **Generazione** | 442 ms | 5017 ms |
| **Totale** | 451 ms | 5020 ms |
| **Pool chunk** | 83 | 9 |
| **Keyword hit** | 0% | 40% |

### Risposta StdRAG

The answer is not available in the provided context.

### Risposta SLM-RAG

In base al contesto fornito, le cause economiche della Rivoluzione Francese includono:

*   **Situazione economica critica:** Causata da carestie e cattivi raccolti.
*   **Attività speculative:** I mercanti intrapresero attività speculative a causa delle carestie e dei cattivi raccolti.
*   **Crisi agraria:** Derivante dai "capricci del clima" che portarono a raccolti esigui.
*   **Aumento del prezzo del pane:** Conseguenza diretta dell'aumento dei prezzi dovuto alla crisi agraria.
*   **Tassa sulle terre:** Introdotta dal ministro Jacques Turgot per reperire risorse, che alienò le simpatie dei proprietari terrieri.
*   **Spese statali eccessive:** Il lusso della corte e le uscite statali ingenti, che portarono al licenziamento del ministro Necker nel 1781 dopo che aveva reso pubblico il bilancio.
*   **Modello economico dell'Ancien Régime:** Caratterizzato da una società divisa in rigidi ordini sociali e persistenza di diritti feudali.

### Ground Truth

La crisi economica è individuata come una delle principali premesse della Rivoluzione Francese. L'Ancien Régime era caratterizzato da privilegi fiscali per nobiltà e clero, mentre il peso delle tasse gravava sul terzo stato. La convocazione degli Stati Generali fu una risposta diretta a questa crisi finanziaria.

---

## 20. What was the War of the Vendée during the French Revolution?

*cos'era la guerra della Vandea durante la Rivoluzione Francese?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 8.9 ms | 4.3 ms (2.1x) |
| **Generazione** | 2523 ms | 2613 ms |
| **Totale** | 2532 ms | 2617 ms |
| **Pool chunk** | 83 | 10 |
| **Keyword hit** | 80% | 80% |

### Risposta StdRAG

La guerra della Vandea fu una rivolta scoppiata nelle campagne francesi durante la Rivoluzione Francese. Essa fu causata dall'arruolamento di massa di 300.000 uomini deciso dalla Convenzione, che creò un forte malcontento perché mancava già la manodopera necessaria per il raccolto. La rivolta si diffuse in aree dove il consenso e l'attaccamento alla Chiesa erano molto forti. La Convenzione reagì con durezza reprimendo ogni manifestazione fino a sconfiggere chi si opponeva.

### Risposta SLM-RAG

La guerra della Vandea fu una rivolta scoppiata nelle campagne francesi durante la Rivoluzione Francese. Essa fu causata dall'arruolamento di massa di 300.000 uomini deciso dalla Convenzione, che creò un forte malcontento perché mancava già la manodopera necessaria per il raccolto. La rivolta si insediò in una zona dove il consenso e l'attaccamento alla Chiesa erano molto forti. La Convenzione reagì con durezza reprimendo ogni manifestazione fino a sconfiggere chi si opponeva.

### Ground Truth

La guerra della Vandea fu una delle difficoltà interne della Rivoluzione Francese: un conflitto civile che oppose i rivoluzionari a una parte della popolazione francese — in particolare contadini e fedeli alla monarchia e alla Chiesa — nella regione della Vandea.

---

## 21. What were Napoleon's main military campaigns and how did his empire end?

*quali furono le principali campagne di Napoleone e come finì il suo impero?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 10.2 ms | 5.2 ms (1.9x) |
| **Generazione** | 5139 ms | 4666 ms |
| **Totale** | 5149 ms | 4671 ms |
| **Pool chunk** | 83 | 13 |
| **Keyword hit** | 50% | 50% |

### Risposta StdRAG

In base al contesto fornito, le informazioni disponibili sono parziali e non completano la domanda:

1.  **Sulle campagne di Napoleone:** Il testo menziona solo la **campagna di Russia** (iniziata nell'estate del 1812, con l'ingresso a Mosca il 14 settembre 1812). Non vengono elencate altre campagne principali né dettagliate le loro esiti specifici oltre al fatto che la vittoria fu "solo" (la frase si interrompe).
2.  **Su come finì il suo impero:** Il testo afferma che la sconfitta di Napoleone "dà origine alla 3a Repubblica" e menziona l'insurrezione del popolo a Parigi che portò alla proclamazione della Comune. Tuttavia, non descrive il momento esatto della fine dell'impero (come la battaglia di Waterloo o l'esilio a Sant'Elena, che sono citati solo come titolo di sezione ma non sviluppati nel testo).

Poiché il contesto non contiene una lista completa delle campagne né una descrizione completa della fine dell'impero, la risposta esatta non è disponibile.

The answer is not available in the provided context.

### Risposta SLM-RAG

In base al contesto fornito, le informazioni disponibili sono parziali e non completano la domanda:

1.  **Sulle campagne di Napoleone:** Il testo menziona specificamente la **campagna di Russia** (iniziata nell'estate del 1812, con l'ingresso a Mosca il 14 settembre), ma la frase relativa al risultato ("Ma la vittoria fu solo") viene interrotta e non fornisce ulteriori dettagli su altre campagne.
2.  **Su come finì il suo impero:** Il contesto non descrive l'epilogo o la fine dell'impero napoleonico. Si limita a citare il titolo della sezione "Dalla conquista di Mosca all'epilogo di Sant'Elena" e menziona che la sconfitta di Napoleone ha dato origine alla Terza Repubblica francese, senza dettagliare i fatti storici che portarono a tale fine.

Poiché il contesto non contiene le informazioni complete richieste per rispondere a entrambe le parti della domanda, la risposta è:

The answer is not available in the provided context.

### Ground Truth

Napoleone condusse la campagna d'Italia con la nascita delle Repubbliche, la campagna d'Egitto che ne accelerò l'ascesa politica, poi instaurò il Consolato e l'Impero estendendo l'egemonia sull'Europa. La conquista di Mosca segnò l'inizio del declino; l'impero si concluse con la sconfitta definitiva e l'esilio sull'isola di Sant'Elena.

---

## 22. What did the Congress of Vienna decide and who were its main actors?

*cosa stabilì il Congresso di Vienna e chi ne furono i protagonisti?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 9.5 ms | 5.6 ms (1.7x) |
| **Generazione** | 5285 ms | 5284 ms |
| **Totale** | 5294 ms | 5290 ms |
| **Pool chunk** | 83 | 21 |
| **Keyword hit** | 80% | 60% |

### Risposta StdRAG

In base al contesto fornito, ecco la risposta:

**I Protagonisti:**
I principali protagonisti furono i ministri degli esteri delle quattro potenze vincitrici di Napoleone:
*   **Lord Castlereagh** (per la Gran Bretagna);
*   **Von Metternich** (per l'Austria);
*   **Alessandro I** (Zar della Russia, che intervenne di persona);
*   **Talleyrand** (per la Francia, abile diplomatico che difese gli interessi della sua nazione).
Inoltre, furono invitati 216 diplomatici in rappresentanza di vari paesi ed interessi.

**Le Decisioni Stabilite:**
Il Congresso stabilì i seguenti principi e decisioni:
*   **Principi guida:**
    *   **Equilibrio:** Limitare i quattro stati più potenti e creare stati cuscinetto.
    *   **Legittimità:** Restituire al governo i sovrani precedenti alla Rivoluzione (Ancien Regime).
    *   **Interventismo:** Utilizzare l'esercito per reprimere insurrezioni o colpi di stato.
*   **Riassetto territoriale

### Risposta SLM-RAG

In base al contesto fornito, ecco le risposte alle tue domande:

**Chi ne furono i protagonisti?**
I principali artefici delle decisioni furono i ministri degli esteri:
*   **Lord Castlereagh** (per la Gran Bretagna);
*   **Von Metternich** (per l'Austria);
*   Lo zar **Alessandro I** (che intervenne di persona);
*   Il francese **Talleyrand** (abile diplomatico che difese gli interessi della Francia).

Le potenze che decisero di convocare il congresso furono le quattro grandi che avevano sconfitto Napoleone: **Austria, Russia, Prussia e Gran Bretagna**.

**Cosa stabilì il Congresso di Vienna?**
Il contesto specifica che il Congresso si tenne dal novembre 1814 al giugno 1815 e che le sue decisioni furono orientate da alcuni principi (sebbene nel testo fornito non siano elencati esplicitamente i nomi di tali principi, si cita che il Congresso intese riportare l'ordine in Europa ripristinando quasi la situazione precedente alla Rivoluzione, ovvero l'Ancien Régime). Inoltre, il contesto menziona che il Congresso disegnò la mappa dell

### Ground Truth

Il Congresso di Vienna stabilì un nuovo assetto europeo volto a restaurare l'ordine precedente alla Rivoluzione Francese e alle conquiste napoleoniche. Portò alla creazione della Santa Alleanza tra le potenze conservatrici. I protagonisti furono i rappresentanti delle grandi potenze europee vincitrici su Napoleone.

---

## 23. Who was Mazzini and what was the Giovine Italia?

*chi era Mazzini e cos'era la Giovine Italia?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 9.6 ms | 5.6 ms (1.7x) |
| **Generazione** | 3205 ms | 3323 ms |
| **Totale** | 3214 ms | 3329 ms |
| **Pool chunk** | 83 | 23 |
| **Keyword hit** | 80% | 80% |

### Risposta StdRAG

Giuseppe Mazzini era un genovese di famiglia agiata, inizialmente aderente alla Carboneria, che si rese conto che la segretezza dei suoi fini era un elemento limitante. Fondò la **Giovine Italia** (a cui aderì anche Garibaldi) per divulgare le finalità di unificazione dell'Italia sotto forma repubblicana, con anche un progetto di unificazione europea. Mazzini univa la politica a una personale visione religiosa; i suoi motti erano "Dio e Popolo" e "Pensiero e Azione". La Giovine Italia si diffuse soprattutto nel nord del paese, ma il fallimento di numerose insurrezioni ne ridusse l'importanza.

### Risposta SLM-RAG

Secondo il contesto fornito, **Giuseppe Mazzini** era un genovese di famiglia agiata, inizialmente aderente alla Carboneria, che si rese conto che la segretezza dei suoi fini era un elemento limitante. Fondò la **Giovine Italia** (a cui aderì anche Garibaldi) per divulgare le finalità di unificazione dell'Italia sotto forma repubblicana, con anche un progetto di unificazione europea. Mazzini univa la politica a una personale visione religiosa; i suoi motti erano "Dio e Popolo" e "Pensiero e Azione". L'associazione si diffuse soprattutto nel nord del paese, ma la sua importanza si ridusse dopo il fallimento di numerose insurrezioni.

### Ground Truth

Giuseppe Mazzini fu uno dei principali protagonisti del Risorgimento e fondatore della Giovine Italia, un'associazione che propugnava l'indipendenza e l'unificazione dell'Italia come nazione libera e repubblicana, ispirata al motto 'Dio e Popolo'.

---

## 24. What was Cavour's role in the unification of Italy?

*quale fu il ruolo di Cavour nell'unificazione d'Italia?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 10.0 ms | 4.2 ms (2.4x) |
| **Generazione** | 5278 ms | 5266 ms |
| **Totale** | 5288 ms | 5270 ms |
| **Pool chunk** | 83 | 11 |
| **Keyword hit** | 40% | 40% |

### Risposta StdRAG

In base al contesto fornito, il ruolo di Cavour nell'unificazione d'Italia è il seguente:

*   **Politica Liberale ed Economica:** Ha guidato una politica di tipo liberale che garantiva i diritti individuali e proponeva il liberismo economico.
*   **Riforme e Modernizzazione:** Ha messo in pratica riforme agricole e industriali, creato l'Ansaldo e la prima rete ferroviaria italiana, e ha promosso la separazione dalla Chiesa ("libera chiesa in libero stato").
*   **Costruzione del Governo:** È stato nominato Primo Ministro nel 1852, trasformando progressivamente la monarchia costituzionale dei Savoia in una vera monarchia parlamentare.
*   **Controllo dell'Unità:** Ha fondato la Società Nazionale Italiana per progettare l'unità d'Italia ma sotto il controllo della casa Savoia, riducendo l'influenza politica di Mazzini.
*   **Diplomazia e Alleanza:** Ha stretto un'intesa con Napoleone III (gli accordi di Plombières, luglio 1858) che prevedeva l'intervento francese a fianco del Regno di Sardegna contro l'Austria,

### Risposta SLM-RAG

In base al contesto fornito, il ruolo di Cavour nell'unificazione d'Italia include:

*   **Politica interna e riforme:** È stato nominato primo ministro (dopo Massimo d'Azeglio) e ha guidato un processo di modernizzazione del Piemonte. La sua politica è stata di tipo **liberale**, garantendo i diritti individuali e proponendo il **liberismo** in economia. Ha attuato riforme agricole e industriali, creato l'Ansaldo e la prima rete ferroviaria italiana, e ha cercato una netta separazione dalla Chiesa ("libera chiesa in libero stato").
*   **Diplomazia e alleanze:** Ha stretto un'intesa con Napoleone III, che è stata messa in crisi da un attentato di Felice Orsini. Proprio dopo l'attentato, il 21 luglio 1858, a Plombières, Cavour ha incontrato Napoleone III per concordare un intervento francese a fianco del Regno di Sardegna contro l'Austria, con l'obiettivo di ottenere Nizza e la Savoia e di creare un Regno dell'Alta Italia sotto la guida dei Savoia.
*   **Strategia per l'

### Ground Truth

Camillo Benso conte di Cavour fu la figura politica centrale del processo di unificazione. Attuò riforme nel Regno di Sardegna, condusse una politica estera che portò all'alleanza con la Francia, guidò la Seconda guerra d'Indipendenza e creò le condizioni diplomatiche per la Spedizione dei Mille di Garibaldi.

---

## 25. What was the Monroe Doctrine and in what context was it issued?

*cos'era la dottrina Monroe e in quale contesto fu proclamata?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 9.2 ms | 4.2 ms (2.2x) |
| **Generazione** | 1816 ms | 2667 ms |
| **Totale** | 1825 ms | 2671 ms |
| **Pool chunk** | 83 | 11 |
| **Keyword hit** | 67% | 67% |

### Risposta StdRAG

La dottrina di Monroe fu una dichiarazione del Presidente Monroe secondo cui gli interessi dell'America spettavano agli americani, in opposizione alle ingerenze dell'Europa. Fu proclamata nel contesto dell'espansione degli Stati Uniti verso ovest che, nel 1830, raggiunse e oltrepassò il Mississippi, portando alla nascita del "mito della frontiera".

### Risposta SLM-RAG

La dottrina Monroe era un principio dichiarato dal Presidente Monroe secondo cui gli interessi dell'America spettavano esclusivamente agli americani, ponendosi in opposizione alle ingerenze dell'Europa. Fu proclamata nel contesto dell'espansione verso ovest degli Stati Uniti iniziata nel 1800, un periodo caratterizzato anche dalla distruzione dei nativi americani (pellirossa) dovuta all'arrivo di molti coloni europei e dalla crescita della popolazione. In quel momento, gli Stati Uniti erano ormai 27 e l'economia era ben distinta tra industriale al Nord e agricola al Sud.

### Ground Truth

La dottrina Monroe fu proclamata nell'ambito delle lotte per l'indipendenza dell'America latina e dei moti liberali. Affermava il principio che l'America non doveva essere considerata campo di ulteriore colonizzazione europea, opponendosi all'interventismo delle potenze del Vecchio Continente nelle Americhe.

---

## 26. How were the price revolution of the 16th century and the geographical discoveries connected?

*come erano collegati la rivoluzione dei prezzi del Cinquecento e le scoperte geografiche?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 9.5 ms | 4.0 ms (2.4x) |
| **Generazione** | 442 ms | 424 ms |
| **Totale** | 452 ms | 428 ms |
| **Pool chunk** | 83 | 9 |
| **Keyword hit** | 17% | 17% |

### Risposta StdRAG

The answer is not available in the provided context.

### Risposta SLM-RAG

The answer is not available in the provided context.

### Ground Truth

Nel Cinquecento i prezzi subirono un incremento di circa il 400%. Il pensatore Jean Bodin spiegò il fenomeno sostenendo che l'importazione massiccia di oro e argento dalle Americhe da parte di Spagna e Portogallo aveva causato la svalutazione della moneta. I salariati furono i più penalizzati, poiché l'inflazione erose il loro già esiguo potere d'acquisto.

---

