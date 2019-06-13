# VelovProjet
***Bienvenue à l'application Web Vélov à Lyon.***  
*Exploité par la société JCDecaux, [Le vélov](https://velov.grandlyon.com/) est l'un des plus grands réseaux de vélos en libre-service ouvert en France  depuis mai 2005. Commandité par le UE INF tc3, l'application web Vélov à Lyon a été conçue en vue de visualiser les données temporelles et statiqtiques de la disponibilité des vélos distribués à 349 stations à Lyon. Après 3 semaines de développement, l'application voit le jour.*  
<img src=https://upload.wikimedia.org/wikipedia/fr/0/08/Logo_Velov.gif alt="LogoVelov"/>

## Pré-requis
Ces instructions vous donneront l'accès à l'ensemble des fichiers exécutables à local pour les usages de test.

### Pré-installation
Avant de télécharger les fichiers, vous devriez vous diposer d'un environement composé de :  

- Anaconda complètement installé
- SQlite BD Browser
- Un compilateur Python disposant des Packages Anaconda
- Internet connecté

### Installation
Afin d'utiliser cette application Web, il suffit de suivre les étapes suivantes :

- télécharger ce répertoire Github en cliquant sur **Clone or download**-->**Download ZIP**. 
- Après avoir décompressé, exécutez le serveur **ServeurVelov.py**. 
- Accéder à [Cette URL](http://localhost:8082/velov.html)

Dès maintenant vous avez fini l'installation. 

## Test des fonctionnement
Après que l'application Web est ouvert, une carte glissante sur laquelle se trouvent les POIs représentant les stations de vélos est sur la gauche. A votre droite se trouvent les widgets proposant les choix de la plage temporrelle et les modes d'analyse. L'application vous offre 3 fonctionnements principaux. 

### Affichage ponctuel
Le premier fonctionnement consiste à faire afficher les informations ainsi que la courbe de disponibilité de la station dont le POI est cliqué sur la carte glissante. 
- Choix de **plage temporrelle**
- Mettre les autres option en **NON**
- **Cliquer** sur la station à consulter

### Mode comparaison
Le deuxième fonctionnement vous permettra de comparer les données de différentes stations. Il suffit de
- Choix de **plage temporelle**
- Mettre le widget **Mode Comparaison** en OUI
- **Cliquer consécutivement** les stations que vous voulez comparer

### Analyse régionale
Le troisème fonctionnement est consacré à l'analyse de la disponibilité moyenne des vélos dans un arrondissement. 
- Choix de **plage temporelle**
- Choix de **arrondissement**
- Cliquer n'importe quelle station sur la carte  
***Lors que la mode d'analyse régionale est activée (un arrondissement est choisi), seul le choix de la plage tempotelle est significative.***

## Outil de développement
- [Anaconda](https://www.anaconda.com/)
- [Microsoft VScode](https://code.visualstudio.com/)
- [Github Desktop](https://desktop.github.com/)

## Auteurs et développeurs
- ANSELMO HADDAD Victoria - HTML et CSS
- MEDDAI Myriam - HTML et CSS
- LI Chen - HTML
- TAN Yu - Serveur
 
