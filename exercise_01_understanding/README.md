Activité 1 : Comprendre le Puissance 4 et le framework Python PettingZoo

Partie 1 : Règles du Puissance 4

Tâche 1.1 : Analyse des règles du jeu 

1) Le plateau du Puissance 4 est composé de 6 lignes et de 7 colonnes.

2) Un joueur gagne la partie s'il aligne quatre jetons consécutifs de sa 
   couleur avant l'adversaire, que ce soit à l'horizontale, à la verticale 
   ou en diagonale.

3) Si le plateau est complètement rempli sans gagnant alors le match est nul.

4) Un joueur ne peut pas placer un pion dans une colonne qui est déjà pleine.

5) Les résultats possibles d'une partie sont :

   -soit un des deux joueurs a aligné quatre jetons consécutifs de sa couleur
    avant l'adversaire et dans ce cas, il gagne la partie.

   -soit le plateau est complètement rempli sans gagnant et dans ce cas, le
    match est nul.

Tâche 1.2 : Analyse des conditions de victoire

1) Les quatres motifs de victoire sont : 

   xxxx (horizontale), | (verticale), / (diagonale à pente positive), \ (diagonale à pente négative)

2) Pour une position donnée, il y a quatre directions à vérifier pour une 
   victoire : horizontale, verticale, diagonale à pente positive et diagonale
   à pente négative.

3) Fonction check_fourtokens_align_horizontally(token, grid)

        nb_column = 7
        nb_row = 6

        Pour c allant de 0 à 3
            Pour r allant de 0 à 5
                Si grid[r,c], grid[r,c+1], grid[r,c+2] et grid[r,c+3] sont égaux
                à token
                Alors retourner True

            Fin pour
        Fin pour

        retourner False

    Fin Fonction


    Fonction check_fourtokens_align_vertically(token, grid)

        nb_column = 7
        nb_row = 6

        Pour c allant de 0 à 6
            Pour r allant de 0 à 2
                Si grid[r,c], grid[r+1,c], grid[r+2,c] et grid[r+3,c] sont égaux
                à token
                Alors retourner True

            Fin pour
        Fin pour

        retourner False

    Fin Fonction


    Fonction check_fourtokens_align_diagonally_slippositive(token, grid)

        nb_column = 7
        nb_row = 6

        Pour c allant de 0 à 3
            Pour r allant de 3 à 5
                Si grid[r,c], grid[r-1,c+1], grid[r-2,c+2] et grid[r-3,c+3] sont égaux
                à token
                Alors retourner True

            Fin pour
        Fin pour

        retourner False

    Fin Fonction


    Fonction check_fourtokens_align_diagonally_slipnegative(token, grid)

        nb_column = 7
        nb_row = 6

        Pour c allant de 0 à 3
            Pour r allant de 0 à 2
                Si grid[r,c], grid[r+1,c+1], grid[r+2,c+2] et grid[r+3,c+3] sont égaux
                à token
                Alors retourner True

            Fin pour
        Fin pour

        retourner False

    Fin Fonction


Partie 2 : Comprendre PettingZoo
Tâche 2.1 : Lire la documentation

1) Les noms des deux agents dans l'environnement sont player_0 et player_1.

2) La variable action représente le coup d'un agent dont c'est le tour de jouer.
   Dans le cas du jeu Puissance 4, la variable action est un entier compris entre 
   0 et 6 et correpond à l'indice de la colonne où l'agent souhaite insérer son 
   jeton. C'est une variable de type int.
   La variable action peut aussi valoir None dans le cas où l'agent ne peut plus
   faire de coup (cela arrive lorsque la partie est terminée).

3) env.agent_iter() est un itérateur qui permet de parcourir une séquence qui 
   contient tous les agents d'une partie.
   La fonction env.step(action) vérifie si l'action de l'agent est légale, l'éxécute
   si oui et donne la main à l'autre agent.

4) Les informations retournées par env.last() sont :
   
   -deux booléens termination et truncation. Le booléen termination est égal à True
    si la partie est terminée.

   -un dictionnaire info 

   -un entier reward qui correspond au nombre de points gagnés par l'agent depuis sa 
    dernière action

   -un dictionnaire observation qui contient deux clés : observation et action_mask.
    La valeur associée à la clé observation est une liste de deux grilles de taille
    6x7. Chaque grille représente l'état du jeu d'un des deux agents. Le tableau 
    observation['observation'][:,:,0] indique à l'agent dont c'est le tour de jouer
    où sont ses pièces dans le plateau tandis que le tableau observation['observation'][:,:,1]
    lui indique où sont les pièces de l'adversaire.

5) La variable observation est un dictionnaire qui contient deux clés : observation
   et action_mask.

6) Un action_mask est un tableau où chaque élément est un booléen qui indique à 
   l'agent dont c'est le tour de jouer si le coup est légal ou non.
   Dans le cas du jeu Puissance 4, l'action_mask est un tableau de taille 7. Si 
   on peut insérer un jeton à la colonne i (i compris entre 0 et 6) alors la i-ème
   case du tableau action_mask contient 1 sinon elle contient 0.
   L'intérêt de déclarer un action_mask est de proscrire les coups illégaux. En
   effet, si un des agents joue un coup illégal alors le jeu s'arrête et l'agent 
   perd un point.

Tâche 2.2 : Analyse de l'espace d'observation

1) La forme du tableau d'observation est (6,7,2).

2) Le tableau d'observation contient deux tableaux de taille 6x7 (6 lignes et 7
   colonnes).

3) Les valeurs possibles dans le tableau d'observation sont 1 et 0 : 1 si une case
   contient un jeton de l'agent et 0 sinon.

Tâche 2.3 : Comprendre la représentation du plateau

Création d'un script appelé print_board.py qui permet de visualiser l'état du
plateau du puissance 4.





