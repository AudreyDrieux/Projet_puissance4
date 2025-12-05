Partie 1 : Conception de stratégie de test

Tâche 4.1 : Concevoir votre plan de test

1.1 Que tester ?

1) Tests fonctionnels :  

    .Lorsque c'est son tour de jouer, l'agent sélectionne t-il une 
     colonne valide (indice compris entre 0 et 6) ?

    .L'agent fait t-il des coups légaux c'est-à-dire sélectionne t-il
     sa colonne parmi les colonnes jouables ?

    .Lorsque la partie est terminée, l'agent arrête t-il de faire des 
     coups ?

2) Tests de performance :  

   .Combien de temps met l'agent pour faire un coup ?

   .Combien de mémoire est utilisée ?

3) Tests stratégiques :  

   .Combien de parties gagne l'agent intelligent contre l'agent aléatoire ?

   .L'agent intelligent bloque t-il son adversaire lorsque celui-ci peut 
    gagner ?

   .L'agent intelligent joue t-il le coup gagnant lorsque celui-ci existe ?

   .L'agent intelligent bloque t-il une double menace lorsque celle-ci existe ?

   .L'agent évite t-il une colonne qui donnerait une opportunité à son adversaire 
    de gagner à son prochain tour ?


1.2 Comment tester ?

1) Tests fonctionnels :  

   .Sélection d'un coup valide : vérifier que l'indice de la colonne choisie est bien
    un entier compris entre 0 et 6

   .Coups légaux : créer des états de plateau spécifiques et vérifier que l'agent
    choisit des coups légaux

   .Jouer une partie et vérifier que celle-ci se termine au bout d'un nombre fini
    de coups

2) Tests de performance :  

   .Utilisation de time.time() et de tracemalloc pour mesurer les ressources

3) Tests stratégiques :  

   .Taux de victoire : Jouer N parties et mesurer le pourcentage de victoires

   .Créer un état de plateau dans lequel l'adversaire a la possibilité de gagner
    à son prochain tour. Vérifier que l'agent intelligent le bloque.

   .Créer un état de plateau dans lequel l'agent intelligent a la possibilité de 
    gagner immédiatement. Vérifier que l'agent intelligent joue le coup gagnant.

   .Créer un état de plateau dans lequel l'adversaire a la possibilité de créer
    une double menace. Vérifier que l'agent intelligent le bloque.

   .Créer un état de plateau dans lequel l'adversaire aurait la possibilité de 
    gagner à son prochain tour si une colonne spécifique est choisie. Vérifier 
    que l'agent intelligent ne choisit pas cette colonne.


1.3 Critères de succès    

   .L'agent intelligent doit gagner 90 pourcents des parties contre l'agent
    aléatoire

   .L'agent intelligent ne doit pas prendre plus de 3 secondes pour choisir un
    coup

   .La mémoire utilisée ne doit pas dépasser 10 MB
  
  
Tâche 4.2 : Conception de cas de test

Scénario 1 : Détecter une victoire immédiate

Etat du plateau :  

L'agent dont c'est le tour de jouer a 3 jetons dans la ligne 5 et qui sont 
dans les colonnes 0, 1 et 2.

Attendu : L'agent joue la colonne 3 pour gagner
  
  
Scénario 2 : Bloquer la victoire de l'adversaire 

Etat du plateau :  

Ladversaire a 3 jetons dans la ligne 5 et qui sont dans les colonnes 0, 1 et 2.

Attendu : L'agent joue la colonne 3 pour bloquer 
  
  
Scénario 3 : Bloquer une double menace de l'adversaire 

Etat du plateau :  

L'agent dont c'est le tour de jouer a un jeton dans la ligne 4 et qui est dans la 
colonne 3.

L'adversaire a 2 jetons dans la ligne 5 et qui sont dans les colonnes 2 et 3.

Attendu : L'agent joue la colonne 1 ou 4 pour bloquer la double menace
  
  
Scénario 4 : Créer une double menace

Etat du plateau :  

L'agent dont c'est le tour de jouer a 2 jetons dans la ligne 5 et qui sont dans 
les colonnes 3 et 4.

L'adversaire a un jeton dans la ligne 5 et qui est dans la colonne 0. Il a également un 
jeton dans la ligne 4 et qui est dans la colonne 3.

Attendu : L'agent choisit soit la colonne 2 soit la colonne 5 pour créer une double menace 
  
  
Scénario 5 : Eviter une colonne qui donnerait l'opportunité à l'adversaire de
gagner à son prochain tour

Etat du plateau :  

L'agent dont c'est le tour de jouer a 2 jetons dans la ligne 5 et qui sont dans
les colonnes 1 et 3. Il a également un jeton dans la ligne 4 et qui est dans la 
colonne 2. Enfin, il a 3 jetons dans la colonne 2 et qui sont dans les lignes
0, 1 et 2.

L'adversaire a 3 jetons dans la ligne 5 et qui sont dans les colonnes 0, 2 et 4. 
Il a également 2 jetons dans la ligne 4 et qui sont dans les colonnes 1 et 3. 
Enfin, il a un jeton dans la ligne 3 et qui est dans la colonne 2.

Attendu : L'agent ne choisit ni la colonne 1 ni la colonne 3
  
  
Scénario 6 : Détecter les colonnes jouables

Etat du plateau :  

La colonne 3 est pleine.

Attendu : l'agent ne choisit pas la colonne 3 

