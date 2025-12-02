## Tâche 3.8 : Comparaison des performances
### 1. Taux de victoire : Intelligent vs Aléatoire sur 100 parties
En exécutant la fonction de test dix fois,  il y a eu dix fois un taux de victoire de 100 %.

### 2. Efficacité de la stratégie : Quelles règles se déclenchent le plus souvent ?
La règle de préférence pour le centre est celle qui est déclenchée le plus souvent.

### 3. Cas d'échec : Quand votre agent intelligent perd-il ?
Avant les améliorations apportées au `smart_agent_improved`, l’agent intelligent présentait un cas d’échec très typique : l’agent joue dans une colonne qui permettait à l’adversaire de gagner immédiatement au coup suivant.  
Voici un exemple représentatif de cette situation : l’agent place son pion dans une position qui crée directement une opportunité de victoire pour l’agent aléatoire, faute d’avoir vérifié les « coups suicides ». Grâce à l’ajout de la règle d’évitement des coups dangereux `_find_not_suicidal_move`, ce problème a été corrigé et l’agent ne tombe plus dans ce piège.
```
SmartAgent LOST this game!  
Move history for this losing game:  
  Step 1: player_0 played column 3  
  Step 2: player_1 played column 5  
  Step 3: player_0 played column 3  
  Step 4: player_1 played column 3  
  Step 5: player_0 played column 3  
  Step 6: player_1 played column 5  
  Step 7: player_0 played column 3  
  Step 8: player_1 played column 2  
  Step 9: player_0 played column 3  
  Step 10: player_1 played column 2  
  Step 11: player_0 played column 2  
  Step 12: player_1 played column 2  
  Step 13: player_0 played column 2  
  Step 14: player_1 played column 5  
  Step 15: player_0 played column 5  
  Step 16: player_1 played column 5  
  Step 17: player_0 played column 2  
  Step 18: player_1 played column 5  
  Step 19: player_0 played column 4  
  Step 20: player_1 played column 4  
```
Après que RandomAgent a joué dans la colonne 3 au quatrième coup, il ne restait plus que trois cases libres dans cette colonne. Même si SmartAgent continuait à privilégier cette colonne centrale, cela ne pouvait plus mener à une position gagnante. Cependant, SmartAgent a tout de même continué à jouer prioritairement dans cette colonne.   
De plus, le dernier coup de SmartAgent a créé une occasion de victoire immédiate pour l’adversaire, alors que ses règles ne prévoient aucune vérification visant à éviter de donner une position gagnante à l’adversaire.  

### 3. Améliorations : Qu'est-ce qui pourrait le rendre plus fort ?
`_find_not_suicidal_move`:   Ajouter une règle pour éviter les « coups suicidaires » :  
 Avant de jouer un coup, SmartAgent simule le résultat de ce coup ; si, après ce coup, l’adversaire peut réaliser immédiatement un alignement de quatre dans une colonne, alors ce coup est considéré comme un « coup suicidaire » et doit absolument être évité.  

`_extend_chain_move`: Extension des chaînes de pions  
Avant de jouer réellement, SmartAgent simule chaque coup possible et lui attribue un score :  
+100 points pour la création d’un alignement de trois,    
+10 points pour un alignement de deux,  
+20 points pour un coup joué dans la colonne centrale, etc.  
Plus le score est élevé, plus le coup est considéré comme favorable et plus il rapproche le joueur d’un alignement de quatre, donc d’une victoire potentielle.