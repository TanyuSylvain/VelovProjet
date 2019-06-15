# Projet Vélo'v
***Bienvenue sur l'application Web Vélo'v à Lyon.***  
*Exploité par la société JCDecaux, [Le vélo'v](https://velov.grandlyon.com/) est l'un des plus grands réseaux de vélos en libre-service ouvert en France depuis mai 2005. Commandité par le UE INF tc3, l'application web Vélo'v à Lyon a été conçue en vue de visualiser les données temporelles et statiqtiques de disponibilité des vélos distribués dans 349 stations à Lyon. Après 3 semaines de développement, l'application a vu le jour.*  
<img src=https://upload.wikimedia.org/wikipedia/fr/0/08/Logo_Velov.gif alt="LogoVelov"/>

## Pré-requis
Ces instructions vous permettont d'accéder à l'ensemble des fichiers exécutables en local pour effectuer les tests.

### Pré-installation
Avant de télécharger les fichiers, vous devez diposer d'un environement composé de :  

- Anaconda complètement installé
- SQlite BD Browser
- Un compilateur Python disposant des Packages Anaconda
- Internet connecté

### Installation
Afin d'utiliser cette application Web, il suffit de suivre les étapes suivantes :

- Télécharger ce répertoire Github en cliquant sur **Clone or download**-->**Download ZIP**. 
- Après avoir décompressé le dit fichier, exécutez le serveur **ServeurVelov.py**. 
- Accéder à [Cette URL](http://localhost:8082/velov.html)

Dès lors vous avez fini l'installation et pouvez utiliser l'application. 

## Tests de fonctionnement
Après avoir ouvert l'Application Web, une carte glissante sur laquelle se trouvent les POIs, qui représentent les stations de vélos, apparaît sur la gauche. À droite de l'écran se trouvent les widgets avec les choix de la plage temporelle et les modes d'analyse. L'application vous offre 3 fonctionnalités principales. 

### Affichage ponctuel
La première fonctionnalité consiste à  afficher les informations ainsi que la courbe de disponibilité pour le POI sur lequel on a cliqué sur la carte glissante. Pour ce faire, il faut :
- Choisir la **plage temporrelle**
- Mettre les autres options sur **NON**
- **Cliquer** sur la station à consulter  

***Le temps d'attente peut varier en fonction de l'ordinateur.***

### Mode comparaison
La deuxième fonctionnalité vous permettra de comparer les données des différentes stations. Il suffit de :
- Choisir la **plage temporelle**
- Mettre le widget **Mode Comparaison** sur OUI
- **Cliquer consécutivement** sur les stations que vous voulez comparer

### Analyse régionale
La troisème fonctionnalité est consacrée à l'analyse de la disponibilité moyenne des vélos dans un arrondissement. Pour y avoir accès, il faut :
- Choisir la **plage temporelle**
- Choisir l'**arrondissement**
- Cliquer sur n'importe quelle station sur la carte  

***Lorsque le mode Analyse régionale est activé, c'est-à-dire lorsqu'un arrondissement est choisi, seul le choix de la plage temporelle est significatif.***

## Outil de développement
- [Anaconda](https://www.anaconda.com/)
- [Microsoft VScode](https://code.visualstudio.com/)
- [Github Desktop](https://desktop.github.com/)

## Auteurs et développeurs
- ANSELMO HADDAD Victoria - *HTML et CSS*
- MEDDAHI Myriam - *HTML et CSS*
- LI Chen - *HTML*
- TAN Yu - *Serveur*
 
