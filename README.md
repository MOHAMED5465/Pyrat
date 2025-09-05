# Pyrat
Projet académique IMT Atlantique : développement de joueurs Python pour PyRat, un jeu de collecte de fromages dans un labyrinthe modélisé en graphe pondéré. Notre groupe a conçu plusieurs stratégies : Greedy, GreedyEachCheese, GreedyEachTurn, GreedyEachTurn_density et Two_opt_reactive.

# Students
- **Responsable du code** :  RHARRASSI Mohamed  
- **Responsable de la documentation** : EL KARMI Sohaib  
- **Responsable des tests unitaires** : OUNZAR Aymane

Bien que les rôles aient été attribués comme demandé, toute l’équipe a collaboré étroitement sur l’ensemble du projet.  
Chaque membre a activement contribué au code, à la documentation et aux tests, garantissant un effort collectif et une compréhension partagée du travail.  


# Players

Nous avons implémenté trois joueurs utilisant des stratégies gloutonnes pour collecter les morceaux de fromage dans un labyrinthe. Voici une description générale de chaque joueur, des choix effectués, des fonctions créées, et des détails sur leur complexité.

## Greedy

Le joueur **Greedy** calcule dès le début de la partie un chemin complet passant par tous les morceaux de fromage, en choisissant à chaque étape le fromage le plus proche. Ce chemin est fixe et ne s'adapte pas aux changements, comme le ramassage des fromages par l'adversaire.

### Méthodes et Complexité
- **`meta_graph`** : Construit un graphe méta reliant les morceaux de fromage et le joueur avec les distances les plus courtes.  
  - Utilise la méthode `traversal` pour calculer les distances.  
  - **`traversal` (Dijkstra)** : $O(V \log V)$ dans notre cas, car $E < 4V$ (le labyrinthe est peu dense).  
  - Complexité totale : $O(V^2 \log V)$, car chaque sommet effectue un Dijkstra.
- **`partial_path`** : Génère une séquence optimale de fromages à visiter en fonction du graphe méta.  
  - Complexité : $O(V^2)$, pour comparer les distances entre sommets.
- **`complete_path`** : Traduit le chemin partiel en une liste complète de déplacements dans le labyrinthe.  
  - Complexité : $O(V^2)$, pour construire le chemin complet à partir du graphe méta.

---

## GreedyEachCheese

Le joueur **GreedyEachCheese** améliore le joueur précédent en recalculant le prochain fromage cible uniquement lorsque le joueur atteint son objectif actuel. Cela permet une meilleure réactivité lorsque des modifications surviennent dans le labyrinthe.

### Méthodes et Complexité
- **`meta_graph`** : Identique à celle du joueur Greedy.  
  - Complexité : $O(V^2 \log V)$.
- **`neighbors_sorted`** : Trie les voisins en fonction de la distance pour faciliter les décisions locales.  
  - Complexité : $O(V^2)$.
- **`next_destination`** : Détermine si le joueur doit recalculer sa destination.  
  - Utilise `traversal` pour recalculer les distances.  
  - Complexité : $O(V \log V)$ pour un recalcul.

---

## GreedyEachTurn

Le joueur **GreedyEachTurn** adopte une approche encore plus dynamique en recalculant la cible optimale à chaque tour. Cela lui permet de s'adapter rapidement aux changements, par exemple si un fromage est pris par l'adversaire.

### Méthodes et Complexité
- **`meta_graph`** : Identique à celle des deux joueurs précédents.  
  - Complexité : $O(V^2 \log V)$.
- **`neighbors_sorted`** : Identique à celle du joueur GreedyEachCheese.  
  - Complexité : $O(V^2)$.
- **`next_destination`** : Vérifie et réévalue la destination à chaque tour si nécessaire.  
  - Utilise `traversal` pour recalculer les distances.  
  - Complexité : $O(V \log V)$ par tour.

## Two_opt_reactive  

Le joueur **Two_opt_reactive** combine une stratégie gloutonne avec l’heuristique **2-opt** pour améliorer le chemin prévu, ce qui le rapproche d’une solution approchée du problème du voyageur de commerce (TSP).  

### Principe  
1. **Construction d’un chemin initial** :  
   - Génère un chemin partiel en choisissant les fromages de manière gloutonne (le plus proche à chaque étape).  
2. **Optimisation par 2-opt** :  
   - Applique l’heuristique 2-opt pour échanger deux sommets dans le chemin et réduire sa longueur.  
   - Ce processus est réactif et limité dans le temps pour rester compatible avec les contraintes de jeu.  
3. **Adaptation dynamique** :  
   - Le joueur suit le chemin optimisé, mais si un fromage disparaît (ramassé par un adversaire), il réajuste sa destination en conséquence.
### Méthodes et Complexité  
- **`meta_graph`** : construit un graphe méta reliant le joueur et les fromages avec leurs distances.  
  - Complexité : $O(V^2 \log V)$ (comme dans les autres joueurs gloutons).  
- **`partial_path`** : génère un ordre initial des fromages à visiter.  
  - Complexité : $O(V^2)$, car on choisit le plus proche à chaque itération.  
- **`two_opt`** : applique des échanges pour améliorer le chemin.  
  - Complexité théorique : $O(V^2)$ par itération, limitée en pratique par un **time limit** pour garantir la réactivité.  
- **`complete_path`** : construit le chemin complet dans le labyrinthe.  
  - Complexité : $O(V^2)$.  

### Points forts  
- Produit des chemins plus courts que la stratégie gloutonne simple.  
- Réagit aux changements de l’environnement (ex. : fromages ramassés par un adversaire).

## GreedyEachTurn_density

Le joueur **GreedyEachTurn_density** est une variante de **GreedyEachTurn**.  
Il choisit sa prochaine cible non seulement en fonction de la distance, mais aussi en tenant compte de la **densité locale** de fromages autour de chaque case.

### Principe
- À chaque tour, le joueur recalcule le fromage cible.  
- Pour chaque fromage candidat, il évalue :  
  - **La distance au fromage** (via Dijkstra).  
  - **La densité de fromages voisins** (dans une zone 5×5 autour de la case).  
- Le choix final minimise le rapport `distance / densité`.  

### Méthodes principales et Complexité
- **`traversal` (Dijkstra)** : $O(V \log V)$.  
- **`find_route_and_distance`** : reconstruit le chemin le plus court entre deux sommets.  
  - Complexité : $O(V)$ dans le pire cas.  
- **`meta_graph`** : calcule un graphe méta reliant source et fromages.  
  - Complexité : $O(V^2 \log V)$.  
- **`density`** : calcule la densité de fromages autour d’une case (5×5).  
  - Complexité : $O(25) = O(1)$ par fromage.  
- **`nearest`** : sélectionne le fromage optimal en combinant distance et densité.  
  - Complexité : $O(F)$, où $F$ est le nombre de fromages.  
- **`next_destination`** : met à jour la destination si atteinte ou invalidée.  
  - Complexité : $O(V \log V + F)$.  

### Points forts
- Plus performant dans les zones à forte concentration de fromages.  
- Plus robuste face à l’adversaire, car il privilégie les régions "riches" en fromages.  

## Two_opt_reactive

Le joueur **Two_opt_reactive** combine une approche gloutonne et une optimisation par l’heuristique **2-opt**.  
Il commence par construire un chemin partiel en reliant les fromages de manière gloutonne (plus proche en premier), puis améliore ce chemin à l’aide de l’algorithme **2-opt** afin de réduire la distance totale.  
Ensuite, il s’adapte en cours de jeu de manière **réactive** : si un fromage disparaît ou qu’une destination est atteinte, il met à jour sa trajectoire.

### Principe
1. Construction d’un **graphe méta** reliant la position initiale et tous les fromages (plus courts chemins via Dijkstra).  
2. Génération d’un **chemin partiel glouton** qui visite les fromages dans l’ordre croissant des distances.  
3. Amélioration du chemin via l’heuristique **2-opt**, qui échange des sommets pour réduire la longueur totale.  
4. Durant la partie, le joueur **réagit** aux changements (fromages mangés par l’adversaire, nouvelle position atteinte) pour mettre à jour la destination.  

### Méthodes principales et Complexité
- **`traversal` (Dijkstra)** : calcule les plus courts chemins.  
  - Complexité : $O(V \log V)$.  
- **`find_route_and_distance`** : reconstruit un chemin le plus court entre deux sommets.  
  - Complexité : $O(V)$.  
- **`meta_graph`** : construit le graphe méta reliant source et fromages.  
  - Complexité : $O(V^2 \log V)$.  
- **`partial_path`** : construit un chemin partiel glouton (choix du fromage le plus proche).  
  - Complexité : $O(F^2)$ dans le pire cas.  
- **`complete_path`** : reconstruit le chemin complet à partir du chemin partiel et du graphe méta.  
  - Complexité : $O(F)$.  
- **`two_opt`** : améliore le chemin par la méthode 2-opt.  
  - Complexité : $O(F^2)$ par itération (limité par un temps d’exécution).  
- **`next_destination`** : met à jour la destination si elle est atteinte ou invalidée.  
  - Complexité : $O(V \log V + F)$.  

### Points forts
- Génère des chemins optimisés grâce à **2-opt** (souvent bien meilleurs qu’une simple stratégie gloutonne).  
- Stratégie **réactive**, capable de s’adapter aux changements en cours de partie.  
- Convient particulièrement aux labyrinthes avec beaucoup de fromages dispersés.  

# Games

## Game Scripts Overview

Les scripts de jeu créés permettent de simuler et de visualiser le comportement de différents algorithmes  dans un environnement de labyrinthe.  
Ils permettent de tester et comparer les performances de diverses stratégies lors de la navigation et de la collecte de morceaux de fromage, dans le but de résoudre une variante du problème du voyageur de commerce (TSP).  

### 1. `visualize_Greedy.ipynb`

Ce script est une extension de `visualize_Dijkstra.ipynb`.  
Il sert à visualiser le comportement d’un joueur basé sur une stratégie gloutonne dans le jeu, en particulier la façon dont il se déplace vers plusieurs morceaux de fromage.  
Une modification importante a été introduite : le paramètre **nb_cheese**.  
Alors que la version précédente ne gérait qu’un seul fromage, ce script permet désormais d’en gérer plusieurs.  
Ce changement rend la simulation plus réaliste, puisque le joueur doit atteindre plusieurs cibles, ce qui se rapproche davantage d’une résolution du **TSP**.  

### 2. `match_Greedy_GreedyEachTurn.ipynb`

Ce script configure une partie entre deux équipes : un joueur **Greedy** contre un joueur **GreedyEachTurn**.  
L’objectif est d’évaluer leurs performances lorsqu’ils s’affrontent dans le même environnement pour ramasser du fromage.  
Ce dispositif permet une comparaison directe entre les deux algorithmes.  
Le script s’inspire de `sample_game.ipynb` et `tutorial.ipynb` situés dans le répertoire `pyrat_workspace/games`.  
Un total de **100 parties** est exécuté afin de collecter suffisamment de données pour une analyse robuste.  

### 3. `match_GreedyEachCheese_GreedyEachTurn.ipynb`

Ce script oppose un joueur **GreedyEachCheese** à un joueur **GreedyEachTurn**.  
Il compare deux approches :  
- **GreedyEachCheese** : ne réévalue sa cible qu’une fois le fromage atteint.  
- **GreedyEachTurn** : met à jour sa cible à chaque tour.  

Ce scénario permet de tester l’adaptabilité et la réactivité des deux stratégies dans des contextes dynamiques, par exemple lorsqu’un adversaire prend un fromage avant l’arrivée du joueur.  
Là encore, le script exécute **100 parties** pour obtenir une évaluation fiable.  

# Unit tests

## Unit Test Overview

Nous avons créé plusieurs fichiers de test comme : `tests_Greedy.ipynb`, `tests_GreedyEachCheese.ipynb`, `tests_GreedyEachTurn.ipynb` et `two_opt_test`.  
Ils permettent de tester les méthodes utilisées dans les algorithmes **Greedy**, **GreedyEachCheese**, **GreedyEachTurn** et **two_opt_reactive**.  
L’objectif est de vérifier que le processus de décision fonctionne correctement et que toutes les méthodes principales se comportent comme prévu.  

### test_traversal Function

Ce test vérifie la méthode de parcours utilisée par les trois algorithmes gloutons. Il assure que :  
- Tous les sommets accessibles sont visités.  
- La table de routage forme un arbre valide (chaque nœud pointe vers son prédécesseur).  
- Les distances augmentent correctement le long des chemins, garantissant un plus court chemin.  
- Les sorties ont le bon type et la bonne structure (table de routage + dictionnaire de distances valides).  

### `test_find_route_and_distance` Function

Ce test vérifie que la méthode `find_route_and_distance` fonctionne correctement pour reconstruire un chemin :  
- Le bon chemin est trouvé entre deux nœuds.  
- La distance calculée correspond bien au plus court chemin.  
- Le cas particulier où la source et la cible sont identiques est correctement géré.  

### `test_meta_graph` Function

Ce test s’assure que la méthode `meta_graph` construit correctement le graphe des plus courts chemins :  
- Le graphe inclut bien la source et tous les morceaux de fromage.  
- Les chemins et distances entre les nœuds sont corrects.  
- Les arêtes reflètent fidèlement les plus courts chemins.  

### `test_neighbors_sorted` Function

Ce test vérifie que `neighbors_sorted` trie correctement les voisins d’un sommet par ordre croissant de distance.  
Cela garantit que les choix du joueur reposent toujours sur les fromages les plus proches.  

### `test_next_destination` Function

Ce test contrôle que la méthode `next_destination` :  
- Met à jour la cible si le joueur a atteint son fromage.  
- S’adapte lorsque le fromage est pris par un adversaire.  
- Gère les cas où la destination devient invalide.  

### Test Results

Les tests ont été concluants : les algorithmes ont validé toutes les vérifications de base.  
Nous confirmons que les méthodes `traversal`, `find_route_and_distance`, `meta_graph` et autres fonctionnent correctement dans différents scénarios.  
Ces résultats valident la justesse des implémentations de **Greedy**, **GreedyEachCheese**, **GreedyEachTurn** et **GreedyEachTurn_density**.  

# Utils

Nous n’avons pas eu besoin d’utiliser ce dossier, car toutes les fonctionnalités nécessaires ont été intégrées directement.  

# Documentation

La documentation est claire, bien structurée et guide efficacement l’utilisateur à travers le projet.  
Elle fournit des explications détaillées sur les composants clés et le rôle de chaque script.  
De plus, des commentaires ont été ajoutés dans le code pour décrire le comportement et l’objectif de chaque procédure, ce qui rend le projet plus facile à comprendre et à maintenir.  
