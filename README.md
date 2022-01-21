# PPC-project
## Cambiecolo
### Informations générales

Nous avons créé le jeu Cambiecolo en utilisant python.

Sur une table, il existe 4 joueurs possédant chacun 5 cartes distribuées au hasard (avec des types de transports plus ou moins différents selon la distribution).

Nous avons fait une interface de la table pour que ce soit plus visuel.

![Capture d’écran du 2022-01-21 20-53-45](https://user-images.githubusercontent.com/92338357/150604408-b775c281-a496-4dfe-8041-1701798af424.png)

Chacun voit seulement son paquet de cartes et peut faire une offre.

Dans notre code, les joueurs ont tous accès à une liste des offres, où ils ne voient pas quelles cartes sont offertes, mais n'ont accès qu'au nombre de cartes offertes et à l'adresse IP du joueur qui fait l'offre (pour ne pas prendre sa propre offre).

Ils font le choix de prendre ou de laisser une offre, basé sur ce nombre de cartes offertes.

Le but d'un joueur est d'avoir 5 cartes de transports identiques pour terminer le jeu.

Lorsqu'un des joueurs a réussi à avoir 5 cartes identiques, il sonne la cloche et gagne.

Quand on sonne la cloche, les processus player sont tués par des signaux.

Le gagnant est affiché, ainsi que ses cartes et son nombre de points.

![271979946_896968850976905_609944567705730011_n](https://user-images.githubusercontent.com/92338357/150606506-f9cedc31-a779-4bd7-9a6c-383b2333c526.png)

### Constitution du dossier

Fichiers python:

main.py contenant le code principal

player.py contenant le processus des joueurs


Fichiers images:

nécessaires à l'interface


### Démarrage:

Exécuter le fichier main.py



### Auteurs
Jessica SPERA
Chanbin LEE

