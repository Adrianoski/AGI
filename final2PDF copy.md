# Benchmark RAG — AAIX, storia

**Modello:** Qwen/Qwen3.5-4B  |  **top-k:** 5  |  **top-N SLM:** 3

| Metrica | StdRAG | SLM-RAG |
|---|---|---|
| Speedup retrieval | — | **4.9x** |
| Pool medio | 219 chunk | 11 chunk (-95%) |
| Keyword hit | 62% | **60%** |
| Overlap medio top-5 | 49% | — |

---

## 1. Who imported spices into Europe during the Middle Ages?

*Chi importava le spezie in Europa nel Medioevo?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 21.7 ms | 4.0 ms (5.4x) |
| **Generazione** | 5358 ms | 554 ms |
| **Totale** | 5379 ms | 558 ms |
| **Pool chunk** | 219 | 6 |
| **Keyword hit** | 100% | 17% |

### Risposta StdRAG

Based on the provided context, spices were imported into Europe during the Middle Ages by **Arab merchants** and the **Venetian Republic**.

The text states: "I mercanti arabi insieme alla repubblica veneziana detenevano il monopolio di questo commercio" (Arab merchants together with the Venetian Republic held the monopoly of this trade).

### Risposta SLM-RAG

The answer is not available in the provided context.

### Ground Truth

The spice trade was controlled by Arab merchants together with the Venetian republic, who held the monopoly by crossing Muslim territories. The many risks of the journey and the various changes of hands considerably raised the price of the goods.

---

## 2. What territories did Charles V control?

*Quali territori controllava Carlo V?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 20.5 ms | 4.1 ms (5.0x) |
| **Generazione** | 5085 ms | 5407 ms |
| **Totale** | 5105 ms | 5411 ms |
| **Pool chunk** | 219 | 6 |
| **Keyword hit** | 33% | 33% |

### Risposta StdRAG

Based on the provided context, Charles V controlled the following territories:

*   **The Duchy of Milan:** He occupied it to remove it from French dominance.
*   **The Holy Roman Empire (implied):** The text mentions his "Imperial" status (e.g., "Impero di Carlo V", "sovrano francese", "imperatore Carlo V") and his role in opposing French hegemony over German princes, indicating control over the German territories and the Empire.
*   **Spain and its realms:** The text refers to "possessments Spanish" (possedimenti spagnoli) and mentions "Philip II" and "The Spanish Empire" in the context of the same era, noting that Charles V was crowned by Clement VII and that his realms included Spain.
*   **Parts of Italy:** He fought for the "dominance of Italy" and occupied the Duchy of Milan, which was a strategic part of the Italian peninsula.

The text does not provide an exhaustive list of every specific territory, but it confirms his control over the Spanish possessions, the Duchy of Milan, and the German territories of the Holy Roman Empire.

### Risposta SLM-RAG

Based on the provided context, Charles V controlled the following territories:

*   **The Duchy of Milan:** He occupied it to remove it from French dominance.
*   **The Kingdom of Naples:** Mentioned as a territory dominated by the Spanish.
*   **Sicily:** Mentioned as a territory dominated by the Spanish.
*   **Sardinia:** Mentioned as a territory dominated by the Spanish.
*   **The Coast of Tuscany:** Mentioned as a territory dominated by the Spanish.
*   **The Papal States (Stato Pontificio):** The text notes that after the Sack of Rome, Charles V ordered mercenaries to arrive in Rome, implying control or direct military presence, though the context later lists the Papal States as one of the territories *not* under Spanish dominion (sottratti) in the final peace agreement, suggesting the context describes the situation *during* the conflict or the immediate aftermath of specific actions. However, the text explicitly states in the section "L'Italia sotto il dominio spagnolo" that the Papal States were *not* included in the list of territories from which Spain withdrew its dominance (i.e., they remained under Spanish influence or were the exception to the

### Ground Truth

Charles V controlled a vast empire that included Spain, the Habsburg territories, Flanders, the Kingdom of Naples, and the American colonies. His reign was marked by conflicts with France, the Lutheran German princes, and the Ottoman Empire.

---

## 3. What were the main causes of the French Revolution?

*Quali furono le principali cause della Rivoluzione Francese?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 20.9 ms | 4.9 ms (4.3x) |
| **Generazione** | 5228 ms | 5370 ms |
| **Totale** | 5249 ms | 5375 ms |
| **Pool chunk** | 219 | 12 |
| **Keyword hit** | 33% | 33% |

### Risposta StdRAG

Based on the provided context, the main causes of the French Revolution include:

*   **Social and Economic Crisis:** The country suffered from poor harvests and bad weather (specifically in 1788), leading to food shortages and a sharp increase in the price of bread.
*   **Agricultural Dependence:** The economy was heavily reliant on land as the primary source of income, making the population vulnerable to agricultural failures.
*   **The "Ancien Régime" Structure:** The existing political, economic, and social model was characterized by an absolute monarchy, a society divided into rigid social orders, and the persistence of feudal rights.
*   **Pre-revolutionary Events:** Various events occurred during the agricultural crisis that served as a prelude to the revolution.

*Note: The provided text also discusses the causes of the Protestant Reformation (such as moral decay, indulgences, and the desire for peasant emancipation) and the French Revolution of 1789 (such as the confiscation of church property and the Civil Constitution of the Clergy), but it does not explicitly list the specific causes of the 1789 Revolution other than the points above.*

### Risposta SLM-RAG

Based on the provided context, the main causes of the French Revolution include:

*   **Agrarian Crisis:** The revolution was preceded by an agricultural crisis caused by erratic weather patterns (specifically in 1788), which led to poor harvests and famines.
*   **Food Prices:** The poor harvests resulted in a significant increase in the price of bread, a primary source of income for the land.
*   **Economic Structure:** The country was characterized by an "ancien regime" model featuring an absolute monarchy, a society divided into rigid social orders, and the persistence of feudal rights.
*   **Financial Mismanagement and Corruption:** The text highlights the excessive spending of the royal court and the "wasteful" nature of the state's machinery, which contributed to a critical economic situation.
*   **Social Inequality and Taxation:** The government's attempt to raise resources involved alienating the sympathies of landowners through taxes on land, while also proposing reforms (like abolishing corvées) that faced fierce opposition from the aristocracy.
*   **Church-State Conflict:** The state's confiscation of church property, the dissolution of religious orders, and the approval of the Civil Constitution of the Clery created

### Ground Truth

The main causes of the French Revolution were the economic crisis of the Ancien Régime, the fiscal injustices that burdened the third estate, the convening of the Estates General, and the growing influence of public opinion. The nobility and clergy enjoyed fiscal privileges that fuelled popular discontent.

---

## 4. What were the key principles of the Enlightenment?

*Quali erano i principi fondamentali dell'Illuminismo?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 19.4 ms | 4.8 ms (4.1x) |
| **Generazione** | 5322 ms | 4542 ms |
| **Totale** | 5341 ms | 4547 ms |
| **Pool chunk** | 219 | 20 |
| **Keyword hit** | 67% | 67% |

### Risposta StdRAG

Based on the provided context, the key principles of the Enlightenment include:

*   **Reason and Self-Reliance:** The movement is defined as the human exit from a state of minority caused by one's own lack of reason. It advocates for using one's own intelligence and courage ("Sapere aude" – Have the courage to use your own understanding).
*   **Liberation from Tradition:** It encourages individuals to free themselves from traditions and prejudices to adopt a new way of viewing reality, society, politics, culture, and religion.
*   **Liberty and Individual Rights:** Fundamental freedoms must be guaranteed, including private property, freedom of expression, speech, the press, and economic initiative.
*   **Limitation of State Power:** The state should limit the sovereign's powers through a constitution and the separation of powers (legislative, executive, and judicial), a theory attributed to Montesquieu.
*   **Economic Autonomy (Liberalism):** The state should not intervene in the economy, which should self-regulate according to an "invisible hand" (a concept associated with Adam Smith) to naturally regulate inequalities.
*   **Secular Knowledge:** Represented by the *Encyclopedia*, the movement aimed to

### Risposta SLM-RAG

Based on the provided context, the key principles of the Enlightenment include:

*   **Reason:** The movement emphasized reason as the "natural light" of man, which calls him to free himself from traditions and prejudices.
*   **Courage to use one's intelligence:** Expressed by Kant's motto "**Sapere aude**" (Have the courage to use your own intelligence).
*   **A new way of viewing reality:** This involved looking at reality, society, politics, culture, and religion in an absolutely new manner.
*   **Access to knowledge:** Represented by the *Encyclopedia*, which aimed to explain all available knowledge in alphabetical order to make it accessible to everyone.
*   **Critique of authority and tradition:** The movement encouraged svincolarsi (freeing oneself) from traditions and biases.

*(Note: The context also mentions that the movement started in England during the Industrial Revolution and spread to France through the philosophes like Montesquieu, Rousseau, and Voltaire.)*

### Ground Truth

The Enlightenment was founded on the primacy of the 'natural light' of reason as a tool for knowledge and criticism of reality. The philosophes advocated a new vision of economics and politics based on freedom, progress, and the natural rights of the individual.

---

## 5. Who were the Mongols and how did they expand?

*Chi erano i Mongoli e come si espansero?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 21.2 ms | 3.9 ms (5.5x) |
| **Generazione** | 580 ms | 5131 ms |
| **Totale** | 602 ms | 5135 ms |
| **Pool chunk** | 219 | 9 |
| **Keyword hit** | 0% | 67% |

### Risposta StdRAG

The answer is not available in the provided context.

### Risposta SLM-RAG

Based on the provided context, the Mongols were a group of warriors led by Gengis Khan who were known for their ferocity in combat, which allowed for rapid expansion. They were composed of trained cavalrymen and were feared by Europeans, earning them the name "Tartars" (derived from "Tartaro," meaning hell).

Their expansion occurred through a series of military offensives:
1.  **Gengis Khan's Campaigns:** He launched an offensive against China, crossing the Great Wall. He then moved to occupy the southern steppes of Russia, conquering the cities of Samarcanda and Bukara. His attacks continued toward Persia, Georgia, and Bulgaria.
2.  **Successors' Campaigns:** After Gengis Khan's death, his successors continued the expansion, reaching Baghdad in 1258 and invading Poland. In Poland, they defeated the Polish-German cavalry and conquered Hungary.
3.  **Division of the Empire:** Following Gengis Khan's death in August 1227, his kingdom was divided among his four sons, resulting in four Khanates, including the Great Khanate in China.

### Ground Truth

The Mongols were a people of horsemen led by Genghis Khan, who launched his offensive toward China by crossing the Great Wall, then occupied the steppes of southern Russia, conquered Samarkand and Bukhara, and attacked Persia, Georgia, and Bulgaria. They were called Tartars by Europeans. After his death the kingdom was divided among his four sons, giving rise to four Khanates.

---

## 6. What was Luther's Protestant Reformation?

*Che cos'era la Riforma protestante di Lutero?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 21.2 ms | 4.4 ms (4.9x) |
| **Generazione** | 5367 ms | 4749 ms |
| **Totale** | 5389 ms | 4753 ms |
| **Pool chunk** | 219 | 11 |
| **Keyword hit** | 67% | 67% |

### Risposta StdRAG

Based on the provided context, Martin Luther's Protestant Reformation was a religious movement initiated by Martin Luther, born on November 10, 1483, in Eisenach (referred to as Eislaben in the text) in Saxony. It arose from his deep religious anxiety and the belief that no man could achieve salvation through their own efforts or good intentions because they are sinners destined for eternal damnation in the eyes of God.

Luther taught Sacred Scripture at the University of Wittenberg, where he delivered a course on the Epistle to the Romans. In these writings, he found an anthropological concept similar to his own and answers to his anguished questions. The text notes that the Reformation was caused by factors such as the moral decline and luxury of the papal court compared to the misery of the peasantry, the desire of Emperor Charles V to impose sovereignty on German princes (which led some to join the Reformation to counter this), and the spread of practices like indulgences which were criticized as stratagems to condone sins for money. Luther's work is described as finding a conception of humanity and answers to his questions regarding salvation within the pages of the Epistle to the Romans.

### Risposta SLM-RAG

Based on the provided context, Martin Luther's Protestant Reformation was a movement initiated by Martin Luther, born in 1483 in Saxony, who entered the Augustinian monastery at age 22. Driven by a traumatic religious experience that led him to view God as a terrible judge and feel perpetual guilt, Luther taught Sacred Scripture at the University of Wittenberg, specifically focusing on the Letter to the Romans. There, he found an anthropological concept similar to his own and answers to his anguished questions regarding salvation. The text notes that Luther, alongside the German monk Calvin, emphasized that the only valid sacraments were baptism and the Eucharist. However, the context also states that Luther highlighted that, unlike Calvin's view on predestination, the imperfect human cannot save themselves by faith alone (though the text attributes the specific predestination doctrine to Calvin in the same sentence, it distinguishes their emphases). The Reformation was a response to the historical context where indulgences were seen by many Christians as a strategy to condone sins for money, a practice Luther opposed.

### Ground Truth

Luther's Protestant Reformation marked a definitive break with Catholic doctrine, reaffirmed in the Augsburg Confession presented by Philip Melanchthon at the Diet of Augsburg in 1530. The Peace of Augsburg of 1555 officially recognised the Protestant religion by establishing the principle 'cuius regio eius religio'.

---

## 7. How was the Italian state formed during the Risorgimento?

*Come si formò lo Stato italiano durante il Risorgimento?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 20.2 ms | 4.2 ms (4.9x) |
| **Generazione** | 5413 ms | 5344 ms |
| **Totale** | 5434 ms | 5348 ms |
| **Pool chunk** | 219 | 12 |
| **Keyword hit** | 83% | 83% |

### Risposta StdRAG

Based on the provided context, the Italian state was formed through the **Risorgimento**, a complex process of events, political doctrines, and initiatives that began in **1861** and led to the unification of Italy. This process aimed to achieve independence from foreign occupation and the unification of various internal kingdoms, which Italy had experienced for centuries.

The formation involved a political debate between two main factions:
*   **The Moderates (Historical Right):** They believed in reaching national unification by gradually involving the existing monarchic governments, particularly the Kingdom of Sardinia (House of Savoy).
*   **The Democrats (Historical Left):** They were skeptical of monarchs due to the disastrous outcomes of the revolutions of the 1820s and 1830s and advocated for a different approach.

The unification was executed by extending the laws of Piedmont to the entire country (a process known as **piemontesizzazione**), adopting the **Albertine Statute** as the constitution, and establishing the **lira** as the currency. The government, influenced by the **Historical Right**, adopted a conservative and moderate policy favoring entrepreneurs while being less attentive to the needs of the common people.

### Risposta SLM-RAG

Based on the provided context, the Italian state was formed through a complex process of political debate, diplomatic agreements, and military events leading to unification:

1.  **Political Debate and Factions:** The process began with a debate among different political groups. The **Moderates** (right wing) believed in achieving unification gradually by involving the existing monarchic governments, particularly the Kingdom of Sardinia (House of Savoy). The **Democrats** (left wing) rejected the reliability of monarchs, citing the disastrous outcomes of the uprisings in the 1820s and 1830s, and advocated for a republic supported by the people without monarchical intervention. Key figures included Mazzini (who founded the *Young Italy* and sought a republic), Carlo Cattaneo (who promoted federalism), and Gioberti (who proposed a confederation under the Pope).

2.  **Diplomatic Intervention:** A crucial turning point was the secret meeting between Italian Prime Minister **Cavour** and French Emperor **Napoleon III** at **Plombières** on July 21, 1858. This agreement, solidified after an attempt on Napoleon's life by Felice Orsini, stipulated

### Ground Truth

Italian unification was the result of the Risorgimento, led by figures such as Mazzini (founder of Young Italy), Cavour (who conducted diplomatic policy and the Second War of Independence), and Garibaldi (who led the Expedition of the Thousand). Piedmont was the fulcrum of the unification process.

---

## 8. What were the social consequences of the Industrial Revolution?

*Quali furono le conseguenze sociali della Rivoluzione Industriale?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 21.3 ms | 4.3 ms (4.9x) |
| **Generazione** | 5380 ms | 5381 ms |
| **Totale** | 5401 ms | 5385 ms |
| **Pool chunk** | 219 | 14 |
| **Keyword hit** | 100% | 100% |

### Risposta StdRAG

Based on the provided context, the social consequences of the Industrial Revolution include:

*   **Demographic and Urban Changes:** There was a profound increase in population, particularly in England and France. Cities grew rapidly, and new neighborhoods, especially for factory workers, were formed.
*   **Formation of New Social Classes:** The revolution created the **proletariat** (the working class, whose only wealth was their children) and the **bourgeoisie** (the capitalist class, formed by owners of production means and entrepreneurs).
*   **Labor Conditions:** Work became specialized and parceled out. Women and children were often employed (sometimes as young as seven), were generally underpaid, and faced long working hours (up to 16 hours a day) with few holidays.
*   **Living Conditions:** The rapid growth of cities led to the expansion of peripheries and worker quarters characterized by misery, filth, and the spread of alcoholism. Hygiene in these environments was often poor, leading to severe health issues, particularly for children.
*   **Social Movements:** The phenomenon of **Luddism** emerged as a reaction to these changes.
*   **Shift in Economic Power:** There was a shift from an agricultural,

### Risposta SLM-RAG

Based on the provided context, the social consequences of the Industrial Revolution include:

*   **Demographic Changes:** A profound increase in population, particularly in England and France, leading to the growth of cities and the formation of new worker quarters.
*   **Social Class Transformation:** The emergence of new social classes, specifically the **proletariat** (workers who owned only their labor/children as wealth) and the **bourgeoisie capitalist** (owners of production means and entrepreneurs).
*   **Urbanization and Living Conditions:** Massive migration from the countryside to cities, causing rapid urban growth. This led to the expansion of worker peripheries characterized by misery, filth, and the spread of alcoholism.
*   **Labor Conditions:** The introduction of the factory system, which involved the division of labor, long working hours (up to 16 hours a day), and the exploitation of women and children (often starting work at age seven).
*   **Social Movements:** The rise of **Luddism** (a movement against machinery) and the formation of mutual aid societies to protect workers from exploitation.
*   **Political and Ideological Shifts:** The crisis of monarchic and liberal government models due to poor worker conditions,

### Ground Truth

The Industrial Revolution brought about the birth of the working-class proletariat, who worked in factories under exploitative conditions. The divide between the property-owning bourgeoisie and the working class deepened. The negative effects of industrialisation included exhausting working hours and poor sanitary conditions.

---

## 9. How did the population of Europe change from the year 1000 to the 14th century?

*Come cambiò la popolazione europea dall'anno 1000 al XIV secolo?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 22.5 ms | 3.4 ms (6.7x) |
| **Generazione** | 1814 ms | 1122 ms |
| **Totale** | 1837 ms | 1126 ms |
| **Pool chunk** | 219 | 5 |
| **Keyword hit** | 100% | 100% |

### Risposta StdRAG

From the year 1000 to the beginning of the 14th century, the European population doubled, increasing from approximately 40 million to around 80 million inhabitants. However, this growth was accompanied by cyclical decennial famines that caused thousands of deaths, and the demographic crisis was further exacerbated by a plague epidemic and numerous wars.

### Risposta SLM-RAG

From the year 1000 to the beginning of the 14th century, the European population doubled, increasing from approximately 40 million to around 80 million inhabitants.

### Ground Truth

The European population grew from the year 1000 until the beginning of the fourteenth century, doubling from around 40 million to around 80 million inhabitants. This made it necessary to clear new land to increase agricultural production, although cyclical famines occurring every decade caused thousands of deaths.

---

## 10. How did the plague spread from Crimea to Europe?

*Come si diffuse la peste dalla Crimea all'Europa?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 21.0 ms | 5.0 ms (4.2x) |
| **Generazione** | 3590 ms | 3507 ms |
| **Totale** | 3611 ms | 3512 ms |
| **Pool chunk** | 219 | 17 |
| **Keyword hit** | 100% | 100% |

### Risposta StdRAG

According to the provided context, the plague spread from Crimea to Europe through the following process:

1.  **Origin in Crimea:** The first epidemic occurred in a Genoese colony in Crimea that was besieged by the Tartars.
2.  **Transmission to Italy:** To capture the city, the besiegers threw corpses infected with the disease into the city using catapults. This caused the Genoese to surrender quickly. Some citizens managed to escape and sail to Italy, carrying the contagio with them.
3.  **Spread to Major Cities:** Around 1347, the plague reached Genoa, Venice, and Sicily.
4.  **Expansion Across Europe:** The following year, it spread to Tuscany and then to France, England, Spain, and Germany.

### Risposta SLM-RAG

According to the provided context, the plague spread from Crimea to Europe in the following way:

1.  **Origin in Crimea:** The first epidemic broke out in a Genoese colony in Crimea, which was besieged by the Tartars.
2.  **Transmission to Italy:** To capture the city, the besiegers threw corpses infected with the disease into the city using catapults. This caused the Genoese to surrender quickly. Some citizens managed to escape and sail to Italy, bringing the contagio with them.
3.  **Spread to the rest of Europe:** Around 1347, the plague reached Genoa, Venice, and Sicily. The following year, it spread to Tuscany and then to France, England, Spain, and Germany.

### Ground Truth

The first epidemic of plague broke out in a Genoese colony in Crimea besieged by the Tartars, who hurled infected corpses over the walls using catapults. Genoese citizens fleeing the siege spread the contagion by sea. Around 1347 the plague reached Genoa, Venice, and Sicily, spreading the following year to Tuscany, France, England, Spain, and Germany. By 1353 it had killed approximately one third of the European population.

---

## 11. Who were blamed for spreading the plague and what happened to them?

*Chi fu accusato di diffondere la peste e cosa accadde loro?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 20.2 ms | 3.5 ms (5.8x) |
| **Generazione** | 1706 ms | 1639 ms |
| **Totale** | 1726 ms | 1642 ms |
| **Pool chunk** | 219 | 8 |
| **Keyword hit** | 0% | 0% |

### Risposta StdRAG

Based on the provided context, the blame for spreading the plague was placed on **some citizens** who managed to escape the siege of the Genoese colony in Crimea and sailed to Italy.

What happened to them is not explicitly stated in the text; the context only notes that they brought the contagio (contagion) to Italy.

### Risposta SLM-RAG

Based on the provided context, the text does not mention who was specifically blamed for spreading the plague or what happened to them. It states that Genoese citizens who fled Crimea brought the contagio to Italy, but it does not describe any blame or punishment assigned to them.


### Ground Truth

Scapegoats included the marginalised, lepers, and above all Jews, who were accused of poisoning well water or of contaminating the air with poisons. As a result, thousands of Jews were persecuted — in pogroms — across France, Germany, and Switzerland.

---

## 12. Who was Henry the Navigator and what was his contribution to exploration?

*Chi era Enrico il Navigatore e qual fu il suo contributo all'esplorazione?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 19.7 ms | 4.2 ms (4.7x) |
| **Generazione** | 2438 ms | 2092 ms |
| **Totale** | 2458 ms | 2096 ms |
| **Pool chunk** | 219 | 18 |
| **Keyword hit** | 83% | 83% |

### Risposta StdRAG

Based on the provided context, **Henry the Navigator** (Enrico il Navigatore) was the King of Portugal who initiated the **Age of Exploration** (*l'età delle esplorazioni*). His contribution was founding a **nautical school** (*scuola nautica*) in his residence at **Cabo de Sagres** in the Algarve. In this school, information regarding high and low tides and the behavior of winds in the "Dark Sea" (the Atlantic Ocean) were carefully collected.

### Risposta SLM-RAG

Based on the provided context, **Henry the Navigator** (Enrico il Navigatore) was the King of Portugal who initiated the "age of exploration." His contribution was founding a **nautical school** in his residence at **Cape of Sagres** in the Algarve. In this school, information regarding tides and the behavior of winds in the "Dark Sea" (the Atlantic Ocean) were carefully collected.

### Ground Truth

Henry the Navigator was the king of Portugal who founded a naval school at his residence at Cape Sagres in the Algarve. There, information was gathered on tides, winds, and the Atlantic Ocean. He promoted the replacement of the galley with the more manoeuvrable caravel and launched Portuguese explorations toward the Azores and the circumnavigation of Africa.

---

## 13. What was Calvin's doctrine of predestination?

*Qual era la dottrina della predestinazione di Calvino?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 19.3 ms | 4.2 ms (4.6x) |
| **Generazione** | 1391 ms | 1396 ms |
| **Totale** | 1410 ms | 1400 ms |
| **Pool chunk** | 219 | 11 |
| **Keyword hit** | 17% | 17% |

### Risposta StdRAG

According to the provided context, Calvin's doctrine of predestination holds that, due to the imperfection of human nature, man cannot save himself through faith. Instead, it is God, in His inscrutable goodness, who predestines man to eternal salvation.

### Risposta SLM-RAG

According to the provided context, Calvin's doctrine of predestination holds that, due to the imperfection of human nature, man cannot save himself through faith. Instead, it is God, in His inscrutable goodness, who predestines individuals to eternal salvation.

### Ground Truth

Calvin affirmed the absolute sovereignty of God over humanity and the doctrine of predestination: mankind is divided into the elect, destined for Heaven, and the damned. With his imperfect nature, man cannot save himself through his own faith; it is God who predestines him to salvation. Calvin recognised only baptism and the Eucharist as valid sacraments.

---

## 14. What was England's Glorious Revolution?

*Che cos'era la Gloriosa Rivoluzione inglese?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 19.6 ms | 3.6 ms (5.5x) |
| **Generazione** | 2165 ms | 2098 ms |
| **Totale** | 2184 ms | 2102 ms |
| **Pool chunk** | 219 | 6 |
| **Keyword hit** | 60% | 60% |

### Risposta StdRAG

Based on the provided context, the **Glorious Revolution** was a peaceful transition in England where King Charles II, who was Catholic and had lost the favor of the citizens, was deposed by the Parliament. The Parliament offered the crown to William of Orange, a Calvinist from the Netherlands. As a result of this event, King Charles II was forced to sign and accept the **Declaration of Rights**, and England became a **constitutional monarchy**.

### Risposta SLM-RAG

Based on the provided context, the **Glorious Revolution** was a peaceful transition in England where King Charles II, who was Catholic and had lost the favor of the citizens, was deposed by the Parliament. The Parliament offered the crown to William of Orange, a Calvinist from the Netherlands. As a result of this event, Charles II was forced to sign and accept the **Declaration of Rights**, and England became a **constitutional monarchy**.

### Ground Truth

The Glorious Revolution in England is described in the context of the transition from absolutism toward more constitutional forms of government in seventeenth-century England, in which Parliament limited the absolute power of the sovereign.

---

## 15. What were the main features of the First Industrial Revolution?

*Quali furono le principali caratteristiche della Prima Rivoluzione Industriale?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 21.4 ms | 4.3 ms (5.0x) |
| **Generazione** | 5414 ms | 5385 ms |
| **Totale** | 5436 ms | 5389 ms |
| **Pool chunk** | 219 | 14 |
| **Keyword hit** | 100% | 100% |

### Risposta StdRAG

Based on the provided context, the main features of the First Industrial Revolution include:

*   **Technological Innovations:** Key advancements included the improvement of the spinning jenny (mobile bobbin) in the textile sector, the construction of the steam engine by Watt, and the creation of the locomotive and railways by Stephenson.
*   **Energy Sources:** The primary sources of power were water and coal.
*   **Economic and Social Shifts:** The economy transitioned from agriculture to machinery and industrial labor, leading to the emergence of new social classes (the bourgeoisie and the proletariat). There was a significant increase in commercial exchanges and raw materials, including the triangular trade.
*   **Agricultural Changes:** Improvements in farming techniques (such as crop rotations and early machinery), the cultivation of new plants, and the use of fences (enclosures) to develop and exploit land.
*   **Labor Conditions:** Many rural workers moved to cities to work in factories. Work became specialized (parceled out), often involving long hours (up to 16 daily) and low pay for women and children.
*   **Urban Growth:** Rapid population growth led to the expansion of cities and the formation of worker quarters, often characterized by poverty

### Risposta SLM-RAG

Based on the provided context, the main features of the First Industrial Revolution include:

*   **Technological Innovations:** Key advancements included the perfection of the spinning jenny (mobile shuttle) in the textile sector, the invention of the steam engine by Watt, and the creation of the locomotive and railways by Stephenson.
*   **Energy Sources:** The primary sources of power were water and coal.
*   **Economic and Social Shifts:** The economy transitioned from an agricultural, closed society to one based on machines, industrial labor, and the emergence of new social classes. This period saw an increase in commercial exchanges and raw materials (including the triangular trade), as well as improvements in agricultural techniques such as crop rotations and the use of new machinery.
*   **The Factory System:** Many rural workers (braccianti) fled the countryside due to enclosures to find work in early factories. Work became specialized (parcellized), and there was significant exploitation of labor, including women and children. This led to rapid urban growth, the formation of worker quarters, and the rise of Luddism.
*   **New Social Classes:** The revolution gave rise to the bourgeoisie (capitalist owners of production means and entrepreneurs) and the proletariat

### Ground Truth

The First Industrial Revolution was characterised by the introduction of new technologies such as James Watt's steam engine, the emergence of the factory as a centre of concentrated production, the massive use of coal, and the transformation of social relations with the birth of the working-class proletariat.

---

## 16. Who were the philosophes and what was their central idea?

*Chi erano i philosophes e qual era la loro idea centrale?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 20.5 ms | 3.9 ms (5.3x) |
| **Generazione** | 3021 ms | 3385 ms |
| **Totale** | 3042 ms | 3389 ms |
| **Pool chunk** | 219 | 9 |
| **Keyword hit** | 83% | 83% |

### Risposta StdRAG

Based on the provided context, the **philosophes** were scholars and intellectuals who spread the Enlightenment movement in France during the 18th century. Key figures mentioned include **Montesquieu, Rousseau, and Voltaire**.

Their central idea was the use of **reason** (described as the "natural light" or *lume naturale* of man) to free humanity from traditions and prejudices. They advocated for a new way of viewing reality, society, politics, culture, and religion, emphasizing the courage to use one's own intelligence, encapsulated in Kant's motto **"Sapere aude"** (Dare to know).

### Risposta SLM-RAG

Based on the provided context, the **philosophes** were scholars and intellectuals who spread the Enlightenment movement in France during the 18th century. The text specifically names **Montesquieu, Rousseau, and Voltaire** as examples.

Their central idea was the use of **reason** (described as the "natural light" of man) to free humanity from traditions and prejudices. They advocated for a new way of viewing reality, society, politics, culture, and religion, emphasizing the courage to use one's own intelligence (summarized by Kant's motto *Sapere aude*). A key work of this movement was the *Encyclopedia*, which aimed to make all available knowledge accessible to everyone in alphabetical order.

### Ground Truth

The philosophes were the thinkers of the Enlightenment who championed the primacy of the 'natural light' of reason as a tool for knowledge and criticism of social and political reality. They proposed a new vision of economics and politics grounded in natural rights and progress.

---

## 17. What were the economic causes of the French Revolution?

*Quali furono le cause economiche della Rivoluzione Francese?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 19.4 ms | 4.3 ms (4.5x) |
| **Generazione** | 3687 ms | 4488 ms |
| **Totale** | 3707 ms | 4493 ms |
| **Pool chunk** | 219 | 9 |
| **Keyword hit** | 20% | 40% |

### Risposta StdRAG

Based on the provided context, the economic causes of the French Revolution include:

*   **Agricultural Crisis:** The economy was based on agriculture, making it highly vulnerable to poor harvests and famines. A specific crisis occurred in 1788 due to erratic weather patterns ("capricci del clima") which led to low yields.
*   **Rising Food Prices:** The agricultural crisis directly caused an immediate increase in the price of bread, which was a primary source of income for the population.
*   **Feudal Rights:** The "ancien regime" persisted with feudal rights that contributed to the rigid social structure and economic burdens.
*   **Economic Structure:** The country was characterized by a monarchy absolute and a society divided into rigid social orders, where land was the main source of revenue.

### Risposta SLM-RAG

Based on the provided context, the economic causes of the French Revolution include:

*   **Critical economic situation:** The country faced severe financial difficulties due to bad harvests and famines (specifically mentioned for 1788).
*   **Speculative activities:** Merchants engaged in speculation, which was exacerbated by the poor harvests.
*   **Fiscal policies and taxation:**
    *   **Jacques Turgot** imposed a tax on land to raise resources, which alienated the landowners.
    *   **Necker** attempted to contain state expenditures rather than increase taxes, but the court's luxury led to massive public spending.
*   **Agricultural crisis:** The "ancien regime" relied heavily on agriculture as the main source of income. Poor harvests and bad weather led to immediate increases in the price of bread, creating social instability.
*   **Social structure:** The society was divided into rigid social orders with the persistence of feudal rights, contributing to economic inequality.

### Ground Truth

The economic crisis is identified as one of the main preconditions of the French Revolution. The Ancien Régime was characterised by fiscal privileges for the nobility and clergy, while the burden of taxation fell on the third estate. The convening of the Estates General was a direct response to this financial crisis.

---

## 18. What was the War of the Vendée during the French Revolution?

*Che cos'era la guerra della Vandea durante la Rivoluzione Francese?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 19.8 ms | 3.9 ms (5.1x) |
| **Generazione** | 2172 ms | 2153 ms |
| **Totale** | 2192 ms | 2157 ms |
| **Pool chunk** | 219 | 10 |
| **Keyword hit** | 80% | 80% |

### Risposta StdRAG

Based on the provided context, the War of the Vendée was an uprising that occurred in the Vendée region of France. It was sparked by the conscription of an additional 300,000 men for the revolutionary army, which caused dissatisfaction in the rural areas where labor was already scarce for the harvest. The conflict was fueled by strong local consensus and attachment to the Church. The Convention responded with harsh repression against those opposing the revolution.

### Risposta SLM-RAG

Based on the provided context, the War of the Vendée was an uprising that occurred in the Vendée region of France. It was sparked by the conscription of an additional 300,000 men for the revolutionary army, which caused dissatisfaction in the countryside where labor was already scarce for the harvest. The rebellion was fueled by strong consensus and attachment to the Church in that area. The Convention responded with harsh repression against those opposing the revolution.

### Ground Truth

The War of the Vendée was one of the internal difficulties of the French Revolution: a civil conflict that pitted the revolutionaries against part of the French population — particularly peasants and those loyal to the monarchy and the Church — in the Vendée region.

---

## 19. What were Napoleon's main military campaigns and how did his empire end?

*Quali furono le principali campagne militari di Napoleone e come finì il suo impero?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 20.1 ms | 4.1 ms (4.8x) |
| **Generazione** | 5394 ms | 5424 ms |
| **Totale** | 5415 ms | 5428 ms |
| **Pool chunk** | 219 | 10 |
| **Keyword hit** | 67% | 33% |

### Risposta StdRAG

Based on the provided context, here are the details regarding Napoleon's military campaigns and the end of his empire:

**Main Military Campaigns:**
*   **Campaign of Russia:** In response to Russia's refusal to adhere to the Continental System (the economic blockade against Britain), Napoleon organized the campaign of Russia. It began in the summer of 1812, and the French army entered Moscow on September 14, 1812. The text notes that the victory was only partial ("Ma la vittoria fu solo...").
*   **Invasions of Portugal and Spain:** Due to the negative economic impact of the Continental System on France, which relied on importing British raw materials, Napoleon was forced to invade Portugal and Spain to support his country.
*   **Battle of Waterloo:** The context mentions the "Battle of Waterloo" in the list of images, implying it was a significant military event, though the text does not provide further details on the battle itself.

**How His Empire Ended:**
*   **Exile to St. Helena:** After his defeat, Napoleon was exiled to the island of St. Helena.
*   **Death:** The context mentions an image titled "Napoleon at St. Helena," indicating his

### Risposta SLM-RAG

Based on the provided context, here are the details regarding Napoleon's military campaigns and the end of his empire:

**Main Military Campaigns:**
*   **Campaign of Russia (1812):** Triggered by Russia's decision to stop adhering to the Continental Block, Napoleon organized this campaign in the summer of 1812. The French army entered Moscow on September 14, 1812. The text notes that the victory was "only" (the sentence is cut off, but the context implies it was not a decisive or lasting one).
*   **Invasions of Portugal and Spain:** Due to the economic damage caused by the Continental Block (which hurt France's reliance on English raw materials), Napoleon was forced to invade Portugal and Spain to support his country.
*   **Conquest of Southern Italy (1860):** The text mentions a campaign led by Garibaldi (not Napoleon) to liberate Southern Italy, but it also references the context of the "Empire" ending with the "epilogue of St. Helena" in the section header, implying the fall of Napoleon's rule occurred before this 1860 event.

**How His Empire Ended:**
*   **The Continental

### Ground Truth

Napoleon led the Italian campaign, during which the Republics were established, and the Egyptian campaign, which accelerated his political rise; he then installed the Consulate and the Empire, extending his hegemony over Europe. The conquest of Moscow marked the beginning of his decline; the empire ended with his final defeat and exile to the island of Saint Helena.

---

## 20. What did the Congress of Vienna decide and who were its main actors?

*Cosa stabilì il Congresso di Vienna e chi furono i suoi protagonisti?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 19.6 ms | 4.7 ms (4.2x) |
| **Generazione** | 5422 ms | 5417 ms |
| **Totale** | 5442 ms | 5422 ms |
| **Pool chunk** | 219 | 21 |
| **Keyword hit** | 80% | 80% |

### Risposta StdRAG

Based on the provided context, here are the decisions and main actors of the Congress of Vienna:

**Main Actors:**
The four great powers that had defeated Napoleon were the primary decision-makers:
*   **Austria:** Represented by the famous diplomat **Metternich**.
*   **Russia:** Represented by **Tsar Alexander I**, who intervened personally in the debates.
*   **Prussia:** Mentioned as one of the four powers.
*   **Great Britain:** Represented by **Lord Castlereagh**.
*   **France:** Although not one of the four victors, **Talleyrand** (the French minister) was invited and successfully defended his nation's interests without causing heavy repercussions.

**Decisions and Principles:**
The Congress was guided by the following principles and decisions:
*   **Restoration:** The goal was to restore order in Europe and return to the situation of the *Ancien Regime* (pre-revolutionary era).
*   **Legitimacy:** The previous monarchs (those before the Revolution) were to return to power.
*   **Balance of Power:** The four most powerful states were to be limited, and "buffer states" were to be created.

### Risposta SLM-RAG

Based on the provided context, here are the answers to your questions:

**Main Actors:**
The main actors were the four great powers that had defeated Napoleon:
*   **Austria** (represented by the famous diplomat **Metternich**)
*   **Russia** (represented by **Tsar Alexander I**, who intervened personally)
*   **Prussia** (represented by **King William IV** and later **William I**)
*   **Great Britain** (represented by **Lord Castlereagh**)

Additionally, the French diplomat **Talleyrand** played a crucial role in defending his nation's interests without causing heavy repercussions for France.

**Decisions and Principles:**
The Congress was guided by the following principles:
*   **Equilibrium:** Limiting the four most powerful states and creating "buffer states."
*   **Legitimacy:** Restoring the kings who ruled before the Revolution (the *Ancien Regime*).
*   **Intervention:** Using the army to suppress insurrections or coups d'état.

**Specific Outcomes:**
*   It led to a general geographical reorganization of Europe.
*   It resulted in the birth of the **German Confederation**.
*

### Ground Truth

The Congress of Vienna established a new European order aimed at restoring the situation prior to the French Revolution and Napoleon's conquests. It led to the creation of the Holy Alliance among the conservative powers. The main actors were representatives of the great European powers that had defeated Napoleon.

---

## 21. Who was Mazzini and what was the Giovine Italia?

*Chi era Mazzini e cos'era la Giovine Italia?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 21.8 ms | 5.1 ms (4.2x) |
| **Generazione** | 3563 ms | 3537 ms |
| **Totale** | 3585 ms | 3542 ms |
| **Pool chunk** | 219 | 23 |
| **Keyword hit** | 80% | 80% |

### Risposta StdRAG

Based on the provided context, **Giuseppe Mazzini** was a Genoese man from an affluent family who initially joined the Carboneria but left because he felt its secrecy limited its goals. He founded the **Giovine Italia** (Young Italy), an association to which **Garibaldi** also joined.

The **Giovine Italia** was an organization that spread primarily in the north of the country. Its main purpose was to unify Italy under a **republican form of government**. Mazzini combined politics with a personal religious vision, using the mottos "God and People" and "Thought and Action." The association aimed to achieve the unification of Italy and also envisioned a project for European unification. However, the failure of numerous insurrections eventually reduced its importance.

### Risposta SLM-RAG

Based on the provided context, **Giuseppe Mazzini** was a Genoese man from an affluent family who initially joined the Carboneria but left because he felt its secrecy limited its goals. He founded the **Giovine Italia** (Young Italy), an association to which Garibaldi also joined.

The **Giovine Italia** was an organization that spread primarily in the north of the country. Its main purpose was to unify Italy under a **republican form of government**. Mazzini combined politics with a personal religious vision, using the mottos "God and People" and "Thought and Action." The association aimed to achieve the unification of Italy and also envisioned a project for European unification. However, the failure of numerous insurrections eventually reduced its importance.

### Ground Truth

Giuseppe Mazzini was one of the leading figures of the Risorgimento and founder of Young Italy (Giovine Italia), an association that advocated the independence and unification of Italy as a free republican nation, inspired by the motto 'God and the People'.

---

## 22. What was Cavour's role in the unification of Italy?

*Qual fu il ruolo di Cavour nell'unificazione d'Italia?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 19.5 ms | 3.8 ms (5.2x) |
| **Generazione** | 5432 ms | 5416 ms |
| **Totale** | 5451 ms | 5420 ms |
| **Pool chunk** | 219 | 11 |
| **Keyword hit** | 60% | 40% |

### Risposta StdRAG

Based on the provided context, Camillo Benso, Count of Cavour, played a central role in the unification of Italy as the Prime Minister of the Kingdom of Sardinia (Piedmont) and a key architect of the political strategy for unification. His specific roles and actions include:

*   **Political Leadership and Reform:** He was a liberal statesman who implemented reforms guaranteeing individual rights and promoting economic liberalism. He oversaw significant internal changes, including the creation of the Ansaldo company, the first Italian railway network, and the separation of the Church from the State (based on the principle of "a free church in a free state").
*   **Diplomatic Strategy:** Cavour recognized that Italy needed international support to change its situation. To gain the trust and aid of France and Britain, he sent 15,000 bersaglieri to fight in the Crimean War against Russia in 1853.
*   **The Plombières Agreement:** In 1858, he met secretly with Napoleon III at Plombières to form an alliance. They agreed that France would intervene on the side of the Kingdom of Sardinia if attacked by Austria, with the promise that France would gain

### Risposta SLM-RAG

Based on the provided context, Camillo Benso, Count of Cavour, played the following roles in the unification of Italy:

*   **Prime Minister and Liberal Reformer:** He served as Prime Minister of the Kingdom of Sardinia (appointed in 1852) and implemented a liberal political and economic policy. His reforms included agricultural and industrial changes, the creation of the Ansaldo company, and the establishment of the first Italian railway network.
*   **Architect of the "Società Nazionale Italiana":** To reduce the political influence of Mazzini and ensure the unification project remained under Savoyard control, Cavour helped found this society, which designed the unification plan.
*   **Diplomat and Modernizer:** He pursued a moderate reformist policy, separating the state from the Church (advocating for a "free church in a free state") and reducing the Church's political interference through laws like those of Siccardi. He also worked to modernize the Piedmontese state, turning it into a constitutional monarchy and eventually a parliamentary monarchy.
*   **Key Figure in the Plombières Agreement:** He was the Italian Prime Minister who met with Napoleon III in Plombières on July 2

### Ground Truth

Count Camillo Benso di Cavour was the central political figure in the unification process. He introduced reforms in the Kingdom of Sardinia, pursued a foreign policy that led to an alliance with France, directed the Second War of Independence, and created the diplomatic conditions for Garibaldi's Expedition of the Thousand.

---

## 23. What was the Monroe Doctrine and in what context was it issued?

*Che cos'era la dottrina Monroe e in quale contesto fu proclamata?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 20.9 ms | 4.0 ms (5.2x) |
| **Generazione** | 3518 ms | 4052 ms |
| **Totale** | 3539 ms | 4056 ms |
| **Pool chunk** | 219 | 11 |
| **Keyword hit** | 67% | 67% |

### Risposta StdRAG

Based on the provided context, the **Monroe Doctrine** was a declaration by the President of the United States (James Monroe) stating that the interests of the American continent belonged to the Americans and were opposed to European interference.

It was issued in the context of the **19th century**, specifically following a period of US expansion toward the west where the nation reached and passed the Mississippi River by **1830**. This expansion was accompanied by the "myth of the frontier," the elimination of Native American tribes, and a growing population. The doctrine emerged as the United States sought to assert its dominance and prevent European powers from interfering in the newly formed or existing American states, which were noted to have reached a total of **27 states by 1837**.

### Risposta SLM-RAG

Based on the provided context, the **Monroe Doctrine** was a declaration by President Monroe stating that the interests of the American continent belonged to the Americans and were to be protected against interference from Europe.

It was issued in the context of the **19th century (specifically around 1800-1830)**, a period characterized by:
*   The beginning of US expansion westward (the "mitico west").
*   The destruction of Native Americans ("pellirossa") due to this expansion and the influx of European colonists.
*   Rapid population growth, reaching 27 states by 1837.
*   A distinct economic division between an industrial North and an agricultural South.
*   The broader geopolitical tension of the era, including revolutions in France (1830) and independence movements in Belgium, Germany, Switzerland, and Poland.

### Ground Truth

The Monroe Doctrine was proclaimed in the context of the Latin American independence struggles and liberal uprisings. It asserted the principle that America should not be considered a field for further European colonisation, opposing the interventionism of Old World powers in the Americas.

---

## 24. How were the price revolution of the 16th century and the geographical discoveries connected?

*Come erano collegate la rivoluzione dei prezzi del XVI secolo e le scoperte geografiche?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 20.9 ms | 4.0 ms (5.2x) |
| **Generazione** | 2300 ms | 1838 ms |
| **Totale** | 2321 ms | 1842 ms |
| **Pool chunk** | 219 | 8 |
| **Keyword hit** | 17% | 17% |

### Risposta StdRAG

The answer is not available in the provided context.

### Risposta SLM-RAG

The provided context does not contain information connecting the price revolution of the 16th century with geographical discoveries. While the text mentions the 16th century in the context of population growth, colonial empires, and the search for new trade routes to the East, it does not discuss a "price revolution" or establish a causal link between that economic phenomenon and the discoveries.

### Ground Truth

In the sixteenth century, prices rose by approximately 400%. The thinker Jean Bodin explained this phenomenon by arguing that the massive importation of gold and silver from the Americas by Spain and Portugal had caused the devaluation of money. Wage earners were the most penalised, as inflation eroded their already meagre purchasing power.

---

