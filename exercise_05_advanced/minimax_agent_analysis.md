## `choose_action`
`choose_action` applique d’abord une série de règles tactiques pour gérer rapidement les situations critiques — **gagner immédiatement / bloquer une menace directe / éviter un coup suicidaire / créer une double menace** — puis utilise **Minimax** sur les coups restants pour une évaluation plus approfondie.  
1. **Rule 1 – Immediate Win**   
Appelle `_find_winning_move(board, channel=0)`et joue directement le coup si une connexion de quatre est possible.  
2. **Rule 2 – Block Immediate Loss**    
Appelle `_find_winning_move(board, channel=1)`, si l’adversaire peut gagner au prochain coup, on bloque en priorité.  
3. **Rule 3 – Block Double Two-Spot**  
Appelle`_find_block_double_two_spot(board, channel=0)`pour repérer les colonnes où l’adversaire pourrait créer une menace double à deux pièces, puis joue pour empêcher cette configuration.   
4. **Rule 4 – Avoid Suicidal Moves**  
Appelle`_find_suicidal_move(board, col)`: si un coup donné permettrait à l’adversaire de gagner immédiatement, il est éliminé des options possibles.  
5. **Rule 5 –Forced win in two moves**   
Appelle `_is_forced_win_in_two(board, a, channel=0)` et vérifie si ce coup garantit une victoire forcée en deux demi-coups.   
6. **Rule 6 – Create Double Threat**  
Appelle`_creates_double_threat(board, col, channel=0)`: si un coup peut générer deux menaces gagnantes simultanées, il est privilégié.    
7. **Rule 7 – Minimax Search**  
Effectue une recherche `_minimax` sur les candidate_actions filtrés et choisit le coup avec la meilleure évaluation.  

## Algorithme de recherche : Minimax avec élagage Alpha-Beta 
1. **`_minimax(self, board, depth, alpha, beta, maximizing)`**:    
**Conditions d’arrêt** : un joueur a déjà gagné / depth=0 → on appelle `_evaluate`.  
**maximizing = True**: signifie que c’est notre tour (channel 0), sinon c’est celui de l’adversaire.   
**Alpha-Beta**: est utilisé pour réduire le nombre de branches explorées.   
2. **Profondeur adaptative `_adaptive_depth(self, board)`**：  
Le nombre de cases vides détermine la profondeur de recherche :  
· en fin de partie (peu de cases libres) → profondeur augmentée (self.depth),  
· en début de partie → profondeur légèrement réduite (self.depth - 1).   

## Conception de la fonction d’évaluation`_evaluate()`
1. `_check_win`    
Victoire : renvoie +100000 (situation idéale)  
Défaite : renvoie -100000 (situation à éviter absolument)  
2. `_opponent_can_win_next`  
Si l’adversaire peut gagner au prochain coup, une pénalité de -5000 est appliquée.  
Cela garantit que l’agent privilégie toujours la défense contre une menace directe.  
3. `_count_three_in_row`  
Trois pièces alignées avec au moins une extrémité libre :  
· channel=0 : +200 (augmenter cette valeur permet de rendre l’agent plus offensif que défensif, ce qui augmente ses chances de victoire)  
· channel=1 : -50  
4. `_count_two_in_row`    
Deux pièces alignées :  
· channel=0 : +20  
· channel=1 : -10    
5. `self.POSITION_WEIGHTS`  
Pour refléter la préférence stratégique pour les colonnes centrales, la stratégie initiale consistait à attribuer un bonus de +30 pour un pion placé en colonne 3, +20 pour les colonnes 2 et 4, et +10 pour les autres colonnes. Cette pondération par colonne permettait de capturer une première idée stratégique.  
Cependant, dans les parties réelles, la plupart des combinaisons gagnantes apparaissent entre les lignes 2 et 5. Autrement dit, même si un pion est placé dans une colonne centrale, sa contribution à la victoire reste limitée s’il se trouve sur les lignes 0 ou 1.  
À partir de cette observation, j’ai abandonné une pondération uniquement basée sur les colonnes pour adopter une pondération case par case, ce qui permet à la fonction d’évaluation de refléter plus précisément la valeur stratégique de chaque position sur le plateau.  
```
[10, 10 , 10 , 10 , 10 , 10 , 10],
[10, 50 , 50 , 50 , 50 , 50 , 10],
[10, 50 , 100, 200, 100, 50 , 10],
[25, 50 , 100, 300, 100, 50 , 25],
[50, 100, 200, 300, 200, 100, 50],
[75, 100, 200, 300, 200, 100, 75],
```    

## Détection de motifs tactiques et mécanismes défensifs  
1. **Coup suicidaire `_find_suicidal_move`**  
Simule un de nos coups puis toutes les réponses adverses possibles ;
si une réponse mène immédiatement à une victoire adverse, le coup est considéré comme suicidaire et écarté.  
2. **Détection de double menace**    
`_is_double_two_spot`: vérifie si une case permettrait, pour un joueur donné, de former des chaînes d’au moins deux pièces dans au moins deux directions différentes.  
`_find_block_double_two_spot`: parcourt toutes les colonnes pour identifier les endroits où l’adversaire pourrait créer ce type de double menace, afin de jouer préventivement.  
`_creates_double_threat`: vérifie si un de nos coups crée deux menaces gagnantes au tour suivant.  

## Gestion du temps et table de transposition
1. Une limite de temps `time_limit` est imposée à chaque appel de `choose_action` via un deadline `_deadline`.  
2. Les fonctions `_minimax` et `_is_forced_win_in_two` vérifient régulièrement cette limite et retournent une valeur neutre si le temps est écoulé, ce qui évite les dépassements de temps.  
3. Une table de transposition `self.transposition` mémorise les évaluations déjà calculées pour un état de plateau donné (représenté par `board.tobytes()` et le flag `maximizing`), ce qui permet de réduire le nombre de nœuds explorés.  