# Galileo 2d
## Projet de : Eugenie , Sebastian et Emmanuel.

<img width="1350" height="759" alt="image" src="https://github.com/user-attachments/assets/18e5de7e-43ff-4bb0-8fb7-8b354c498ed8" />  

  

Nous souhaitons faire un jeu en 2d. Avec des graphismes du type "Celeste".  
Le personnage principal est coincé en enfer et doit essayer de remonter sur terre, en passant par 3 dimensions contenant 2-3 niveaux:  
- L'Enfer
- Le Purigatoire
- Le Paradis  
  
Il peut y avoir des sauts décisifs (si on rate = on recommence)

C'est un jeu de parkour de plus en plus difficile avec des fonctionnalités évoluant au cours du jeu.  
Sur le menu il y aura : paramètre, choix du personnages, lancer une partie
Un cheatcode sera donné à la fin de chaque niveaux permettant au joueur de retourner au dernier niveau terminé. 
On utilisera la bibliothèque pygame.

## ASPECT SONORE ET GRAPHIQUE
  
Ca sera un jeu solo et en 2d.  
Pour ce qui concerne les graphismes, ça sera des graphismes simples et pixelisés, et pour cela on va utiliser Pygame.  
Le jeu contiendra des dialogues avec des NPC, qui nous servira à obtenir des vies, à comprendre l'histoire et à avancer dans les niveaux. 
Il y aura une musique de fond dans l'écran du menu qui durera moins d'une minute et sera joué en boucle, jusqu'à que le joueur appui sur le bouton Jouer. Dans les niveaux, il y aura avec des musiques de fond, qui aura un lien avec la dimension où le joueur se trouve et des SFX en fonction des actions du personnages : un son différent selon le matériaux où le personnage se trouve, quand on appui sur un bouton du menu, quand un NPC parle.  

## ENNEMIS :

Pendant les niveaux, il y aura peu d'ennemis pour faciliter la jouabilité du joueur. Ces ennemis seront mobile, allant de droite à gauche aléatoirement, et dès que le joueur et l'ennemi ont une distance de environ 3 blocs, l'ennemi va courser le joueur pour lui faire des dégats. A la fin de chaque dimension, il y aura principalement des boss, qui seront immobiles et présent en arrière plan, et qui nous lancera des projectiles. Il ne faudra pas le tuer, mais s'échapper de la dimension en atteignant une porte, qui nous menera vers la prochaine dimension. Pour esquiver ses projectiles, on pourra se cacher en dessous de plateformes par exemple, autrement on se déplace.

## COMMANDES :  
  
Saut = Espace   
Aller à droite = d  
Aller à gauche = q  
S'accrocher à des liannes/tyroliennes, lire des panneaux = z  
Se Baisser = s  
Pause = Echap   
se déplacer vers le haut (liannes, echelles) = flèche du haut  
se deplacer vers le bas (liannes, echelles) = flèche du bas  
  
Système de score : Temps par niveaux et temps total
Il aura 3 vies, où il recommencera tout le niveau si il les perds. Chaque vie se perd :  
- Dès qu'il tombe dans du vide
- Dès que sa barre de vie descend à 0, initialement à 100  
Les checkpoints seront fréquents. 


## LIENS
SFX et Musiques de fond : https://www.youtube.com/watch?v=pcdB2s2y4Qc  
Menu gui : https://www.youtube.com/watch?v=GMBqjxcKogA  

 
















































