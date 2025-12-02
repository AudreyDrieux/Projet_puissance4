Partie 3 : Décomposition du problème

Tâche 3.1 : Décomposer l'implémentation de l'agent

1) L'agent reçoit les informations suivantes : 
   
   -l'espace d'action qui est un tableau dont les éléments sont
    les entiers de 0 à 6. Chaque entier correspond à l'indice de 
    la colonne dans laquelle un jeton doit être déposé.

   -l'espace d'observation qui est un tableau dont les éléments sont
    deux tableaux de taille 6x7. Les deux tableaux indiquent à l'agent
    dont c'est le tour de jouer où sont ses pièces et les pièces de 
    l'adversaire dans le plateau.

   -le tableau action_mask qui indique à l'agent dont c'est le tour de 
    jouer quelles sont les colonnes jouables.

   -les booléens termination et truncation.


2) On utilise le tableau action_mask pour déterminer quelles sont les colonnes 
   jouables. Si la i-ème colonne est jouable (i.e. colonne i n'est pas pleine)
   alors la i-ème case du tableau action_mask est égale à 1 sinon elle est égale
   à 0.

3) L'agent choisit une colonne selon une stratégie :
   
   -soit il choisit une colonne de manière aléatoire sans préférence et sans tenir
    compte des colonnes jouables.

   -soit il choisit une colonne de manière aléatoire et sans préférence parmi les
    colonnes jouables.

   -soit il choisit une colonne selon une règle simple:
               -s'il peut gagner, joue le coup gagnant
               -si l'adversaire peut gagner, le bloque
               -si la colonne du milieu n'est pas pleine, la choisir
               -sinon, choisir une colonne de manière aléatoire et sans
                préférence parmi les colonnes jouables

   -soit il choisit une colonne qui crée une configuration dans laquelle il a deux
    possibilités de gagner à son prochain tour.

   -soit il choisit une colonne selon une stratégie plus avancée:
               -algorithme minimax
               -Monte Carlo 
               -apprentissage par renforcement

4) L'agent doit retourner l'indice de la colonne choisie où insérer son jeton.


Tâche 3.2 : Conception d'algorithme-Progression

1) Niveau 0 : l'agent choisit une colonne de manière aléatoire sans préférence et
              sans tenir compte des colonnes jouables

2) Niveau 1 : l'agent choisit une colonne de manière aléatoire sans préférence 
              parmi les colonnes jouables

3) Niveau 2 : si l'agent peut gagner, joue le coup gagnant

4) Niveau 3 : -si l'adversaire peut gagner, l'agent le bloque
              -l'agent choisit une colonne qui empêche l'adversaire d'avoir deux 
               possibilités de gagner à son prochain tour

5) Niveau 4 : -si la colonne du milieu n'est pas pleine, l'agent la choisit
              -parmi les colonnes jouables, l'agent choisit les colonnes 
               intermédiaires plutôt que les colonnes extérieures
              -l'agent choisit une colonne qui crée une configuration dans 
               laquelle il a deux possibilités de gagner à son prochain tour

6) Niveau 5+ : l'agent choisit une colonne selon une stratégie plus avancée 
               (algorithme minimax, Monte Carlo, apprentissage par renforcement)

Tâche 3.3 : Définir l'interface de l'agent

Squelette de la classe Agent par stratégie :

Niveau 0 : 

class Agent
      |- env - environnement Pettingzoo
      |- action_space - l'espace d'action: tableau de taille 7 
      |- player_name - prénom pour l'agent

      choose_action() - choisit une colonne de manière aléatoire sans
                        préférence et sans tenir compte des colonnes
                        jouables


Niveau 1 : 

class Agent
      |- env - environnement Pettingzoo
      |- action_space - l'espace d'action: tableau de taille 7 
      |- player_name - prénom pour l'agent

      choose_action()
          |- get_valid_actions() - Retourne la liste des indices des
                                   colonnes jouables

Niveau 2 :  

class Agent
      |- env - environnement Pettingzoo
      |- action_space - l'espace d'action: tableau de taille 7 
      |- player_name - prénom pour l'agent
                 
      choose_action()
          |- get_valid_actions() - Retourne la liste des indices des 
                                   colonnes jouables

          |- find_winning_move() - Retourne l'indice de la colonne
                                   qui permet à l'agent de gagner
                                   (si celle-ci existe)

Niveau 3 :  

class Agent
      |- env - environnement Pettingzoo
      |- action_space - l'espace d'action: tableau de taille 7 
      |- player_name - prénom pour l'agent
                 
      choose_action()
          |- get_valid_actions() - Retourne la liste des indices des
                                   colonnes jouables

          |- find_blocking_move() - Retourne l'indice de la colonne
                                    qui empêche l'adversaire de gagner
                                    (si celle-ci existe)

          |- find_blocking_double_threat() - Retourne l'indice de la colonne
                                             qui empêche l'adversaire d'avoir
                                             deux possibilités de gagner à son
                                             prochain tour
                                             (si celle-ci existe)
                                                           
Niveau 4 :  

class Agent
      |- env - environnement Pettingzoo
      |- action_space - l'espace d'action: tableau de taille 7 
      |- player_name - prénom pour l'agent

      choose_action()
          |- get_valid_actions() - Retourne la liste des indices des
                                   colonnes jouables

          |- prefer_center_columns() - Si la colonne du milieu est
                                       jouable, la jouer 
                                       Sinon préférer les colonnes intermédiaires 
                                       aux colonnes extérieures
                    
          |- find_double_threat() - Retourne l'indice de la colonne qui
                                    permet à l'agent d'avoir deux possibilités 
                                    de gagner à son prochain tour
                                    (si celle-ci existe)




