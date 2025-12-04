Partie 5 : Analyse 

Tâche 3.8 : Comparaison des performances

1) Sur 100 parties, l'agent intelligent en a gagné 99 tandis que 
   l'agent aléatoire en a gagné 1.

2) Sur 100 parties, l'agent intelligent a choisi 405 fois la colonne
   du milieu. Il a bloqué 33 fois l'adversaire lorsque celui-ci pouvait
   gagner et il a joué 24 fois le coup gagnant.

3) L'agent intelligent perd dans le cas où l'agent aléatoire choisit une
   colonne qui lui donne deux possibilités de gagner à son prochain tour.
   L'agent intelligent perd aussi dans le cas où il a choisi une colonne 
   qui crée une opportunité pour l'agent aléatoire de gagner à son prochain 
   tour.

4) Pour rendre l'agent intelligent plus performant, on peut:    

   -ajouter une méthode creates_double_threat qui retourne True si le choix 
    d'une colonne donne à l'agent deux possibilités de gagner à son prochain 
    tour    

   -ajouter une méthode check_threat_from_position qui retourne True si le choix
    d'une colonne donne une opportunité à l'adversaire de gagner à son prochain
    tour.  


