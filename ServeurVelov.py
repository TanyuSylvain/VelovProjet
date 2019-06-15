# TD3-lieux-insolites.py

# Application exemple : affichage de mes lieux préférés à la Croix-Rousse 2018-10-24
import matplotlib
#matplotlib.use('TkAgg')
import http.server
import socketserver
from urllib.parse import urlparse, parse_qs, unquote
import json
import sqlite3
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as pltd
import numpy as np
import os

# définition du handler
class RequestHandler(http.server.SimpleHTTPRequestHandler):

  # sous-répertoire racine des documents statiques
  static_dir = '/client'

  # version du serveur
  server_version = 'TD4/serveur.py/0.1'

  # on surcharge la méthode qui traite les requêtes GET
  def do_GET(self):
    self.init_params()

    # requete location - retourne la liste de lieux et leurs coordonnées géogrpahiques
    conn = sqlite3.connect('Velov.sqlite')
    c = conn.cursor()
    c.execute("SELECT * FROM 'station-velov2018'")
    r = c.fetchall()
    data = []
    nb=0
    for station in r:
      data.append({'id': nb, 'idnum': station[3],'name':station[4],'lat':station[1],'lon':station[0],\
                    'adresse1':station[5],'adresse2':station[6],'commune':station[7],\
                    'numdansarr':station[8],'nbbornette':station[9],'pole':station[11],\
                    'ouverte':station[12],'insee':station[15]})
      nb+=1
    if self.path_info[0] == "location":
      self.send_json(data)

    # requete description - retourne la description du lieu dont on passe l'id en paramètre dans l'URL
    elif self.path_info[0] == "disponibilite":
      self.send_disponibilite(data)

    # requête générique
    elif self.path_info[0] == "service":
      self.send_html('<p>Path info : <code>{}</p><p>Chaîne de requête : <code>{}</code></p>' \
          .format('/'.join(self.path_info),self.query_string))

    else:
      self.send_static()


  # méthode pour traiter les requêtes HEAD
  def do_HEAD(self):
      self.send_static()


  # méthode pour traiter les requêtes POST - non utilisée dans l'exemple
  def do_POST(self):
    self.init_params()

    # requête générique
    if self.path_info[0] == "service":
      self.send_html(('<p>Path info : <code>{}</code></p><p>Chaîne de requête : <code>{}</code></p>' \
          + '<p>Corps :</p><pre>{}</pre>').format('/'.join(self.path_info),self.query_string,self.body))

    else:
      self.send_error(405)


  # on envoie le document statique demandé
  def send_moyenne(self,data,donnee,commune):
    conn = sqlite3.connect('Velov.sqlite')
    c = conn.cursor()
    c.execute("SELECT idstation FROM 'station-velov2018' WHERE commune=?",(commune,))
    r = c.fetchall()
    stations = []
    for stationid in r:
      stations.append('velov-'+str(stationid[0]))

    # Configuration de la figure
    plt.figure(figsize=(12,6))
    plt.ylim(0,30)
    plt.grid(which='major', color='#888888', linestyle='-')
    plt.grid(which='minor',axis='x', color='#888888', linestyle=':')
    
    ax = plt.subplot(111)
    loc_major = pltd.HourLocator()
    loc_minor = pltd.MinuteLocator()
    ax.xaxis.set_major_locator(loc_major)
    ax.xaxis.set_minor_locator(loc_minor)
    format_major = pltd.DateFormatter('%H:%M')
    ax.xaxis.set_major_formatter(format_major)
    ax.xaxis.set_tick_params(labelsize=10)

    timeDebut = dt.time(int(donnee['heureDebut']),int(donnee['minuteDebut']))
    timeFin = dt.time(int(donnee['heureFin']),int(donnee['minuteFin']))
    time = timeDebut
    x = []
    y = []
    while time <= timeFin:
      timeiso = dt.datetime(2018,11,int(donnee['jour']),time.hour,time.minute).isoformat()+'+00:00'
      c.execute("SELECT * FROM 'velov-histo2018' WHERE time_ISO=?",(timeiso,))
      r = c.fetchall()
      nbvelo = 0
      nbtot = 0
      for a in r:
        if a[1] in stations:
          nbvelo += int(a[2])
          nbtot+= 1
      if nbtot:
        y.append(float(nbvelo/nbtot))
        x.append(dt.datetime(2018,11,int(donnee['jour']),time.hour,time.minute))
      time = (dt.datetime(2018,11,int(donnee['jour']),time.hour,time.minute)+dt.timedelta(minutes=5)).time()
      
    couleur = [np.random.rand() for i in range(3)]
    plt.plot_date(x,y,linewidth=1, linestyle='-', marker='o', color=couleur
    , label=commune)
        
    # légendes
    plt.legend(loc='lower left')
    plt.title("Agrégation de la disponibilité dans la commune {}".format(commune),fontsize=16)
    plt.ylabel('Nombre moyen des vélos disponibles')
    plt.xlabel('Temps')
    idn = int(self.path_info[1])
    lx = len(y)
    if lx < 2:
      print('Veuillez bien choisir la plage temporelle OU station fermée')
      html = "Veuillez vous assurez que la plage temporelle est valide. \
              Si c'est le cas, la station que vous consultez est actuellement fermée"
    else:
      fichier = 'ARRVelo{}.png'.format(idn)
      plt.savefig('client/{}'.format(fichier))
      html = '<img src="/{}?{}" alt="disponibilite {}" width="100%">'.format(fichier,self.date_time_string(),self.path)  
    
    
    if data[idn]['adresse2']:
      adresse2 = data[idn]['adresse2']
    else:
      adresse2 = 'Vide'
    if data[idn]['pole']:
      pole = data[idn]['pole']
    else:
      pole = 'Vide'
    body = json.dumps({'stationId':'StationId de la station choisie : '+'Velov-'+donnee['stationId'],\
                      'name':'Nom de la station : '+data[idn]['name'],\
                      'adresse1':'Adresse : '+data[idn]['adresse1'],\
                      'adresse2':'Complément : '+adresse2,\
                      'commune':'Commune : '+data[idn]['commune'],\
                      'numdansarr':'Numéro de la station selon le code arrondissement : '+str(data[idn]['numdansarr']),\
                      'nbbornette':'Nombre de bornettes dans cette station : '+str(data[idn]['nbbornette']),\
                      'pole':'Pôle : '+pole,\
                      'ouverte':'État :'+data[idn]['ouverte'],\
                      'insee': 'Code INSEE : '+str(data[idn]['insee']),\
                      'image':html})
    headers = [('Content-Type','application/json')]
    self.send(body,headers)
    return 
  def send_disponibilite(self,data):
    # Mise à jour de la base de donnée Cache
    idn = int(self.path_info[1])
    conn = sqlite3.connect('cache.sqlite')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS historique 
                (StationId, Jour, HeureDebut, MinuteDebut, HeureFin, MinuteFin, Comparaison)''')
    c.execute("SELECT * FROM 'historique'")
    hist = c.fetchall()
    donnee = {'stationId':str(data[idn]['idnum']), 'jour':self.params['jr'][0], 'heureDebut':self.params['hd'][0], 'minuteDebut':self.params['md'][0], \
              'heureFin':self.params['hf'][0], 'minuteFin':self.params['mf'][0], 'comparaison':self.params['cp'][0]}
    stations = ['velov-'+ donnee['stationId']]
    if self.params['arr'][0] != 'NON':
      commune = self.params['arr'][0]
      self.send_moyenne(data,donnee,commune)
      return 
    #Mode comparaison
    if donnee['comparaison'] == 'OUI':
      stations = ['velov-'+ donnee['stationId']]
      cursor = -1
      while hist[cursor][-1] == 'OUI':
        stations.append('velov-'+hist[cursor][0])
        cursor -= 1
    interList = list(set(stations))
    interList.sort(key=stations.index)
    stations = interList[:]
    if tuple(donnee.values()) not in hist:
      c.execute("INSERT INTO historique VALUES (?, ?, ?, ?, ?, ?, ?)", \
      (donnee['stationId'],donnee['jour'],donnee['heureDebut'],donnee['minuteDebut'],donnee['heureFin'],donnee['minuteFin'],donnee['comparaison']))
    else:
      fichier = 'dispoVelo{}.png'.format(idn)
      if os.path.isfile('client/'+fichier):
        html = '<img src="/{}?{}" alt="disponibilite {}" width="100%">'.format(fichier,self.date_time_string(),self.path)
        if data[idn]['adresse2']:
          adresse2 = data[idn]['adresse2']
        else:
          adresse2 = 'Vide'
        if data[idn]['pole']:
          pole = data[idn]['pole']
        else:
          pole = 'Vide'
        body = json.dumps({'stationId':'StationId de la station choisie : '+'Velov-'+donnee['stationId'],\
                          'name':'Nom de la station : '+data[idn]['name'],\
                          'adresse1':'Adresse : '+data[idn]['adresse1'],\
                          'adresse2':'Complément : '+adresse2,\
                          'commune':'Commune : '+data[idn]['commune'],\
                          'numdansarr':'Numéro de la station selon le code arrondissement : '+str(data[idn]['numdansarr']),\
                          'nbbornette':'Nombre de bornettes dans cette station : '+str(data[idn]['nbbornette']),\
                          'pole':'Pôle : '+pole,\
                          'ouverte':'État :'+data[idn]['ouverte'],\
                          'insee': 'Code INSEE : '+str(data[idn]['insee']),\
                          'image':html})
        headers = [('Content-Type','application/json')]
        self.send(body,headers)
        return
      
    

    conn.commit()
    conn.close()

    conn = sqlite3.connect('Velov.sqlite')
    c = conn.cursor()
    # On teste que la région demandée existe bien
    '''
    c.execute("SELECT DISTINCT velov_number FROM 'velov-histo2018'")
    station = c.fetchall()
    
    if ('velov-'+ str(data[idn-1]['idnum']),) in station:   # Rq: reg est une liste de tuples
        stations = [('velov-'+ str(data[idn-1]['idnum']),"blue")]
    else:
        print ('Erreur nom')
        self.send_error(404)    # Région non trouvée -> erreur 404
        return None
    '''
    # configuration du tracé
    plt.figure(figsize=(12,6))
    plt.ylim(0,30)
    plt.grid(which='major', color='#888888', linestyle='-')
    plt.grid(which='minor',axis='x', color='#888888', linestyle=':')
    
    ax = plt.subplot(111)
    loc_major = pltd.HourLocator()
    loc_minor = pltd.MinuteLocator()
    ax.xaxis.set_major_locator(loc_major)
    ax.xaxis.set_minor_locator(loc_minor)
    format_major = pltd.DateFormatter('%H:%M')
    ax.xaxis.set_major_formatter(format_major)
    ax.xaxis.set_tick_params(labelsize=10)
    
    # boucle sur les régions
    for l in stations :
        c.execute("SELECT * FROM 'velov-histo2018' WHERE velov_number=? ORDER BY Time_ISO",(l,))  # ou (l[0],)
        r = c.fetchall()
        # recupération de la date (colonne 2) et transformation dans le format de pyplot
        timeDebut = dt.time(int(donnee['heureDebut']),int(donnee['minuteDebut']))
        timeFin = dt.time(int(donnee['heureFin']),int(donnee['minuteFin']))
        x = []
        y = []
        for a in r:
          time = dt.time(int(a[0][11:13]),int(a[0][14:16]))
          jour = a[0][8:10]
          if jour == donnee['jour'] and time > timeDebut and time < timeFin : 
            x.append(dt.datetime(2018,11,int(donnee['jour']),time.hour,time.minute))
            y.append(float(a[2]))
        #x = [int(a[0][8:10]+a[0][11:13]+a[0][14:16]) for a in r if not a[2] == '']
        # récupération de la régularité (colonne 8)
        #y = [float(a[2]) for a in r if not a[2] == '']
        # tracé de la courbe
        couleur = [np.random.rand() for i in range(3)]
        plt.plot_date(x,y,linewidth=1, linestyle='-', marker='o', color=couleur
        , label=l)
        
    # légendes
    plt.legend(loc='lower left')
    plt.title('Disponibilité des vélos',fontsize=16)
    plt.ylabel('Nombre de vélos disponibles')
    plt.xlabel('Temps')
    
    
    #x_ticks = [x[int(lx/10*i)] for i in range(0,11)]
    #plt.xticks(x_ticks)
    #plt.gcf().autofmt_xdate()
    # génération des courbes dans un fichier PNG
    
    lx = len(x)
    if lx == 0:
      print('Veuillez bien choisir la plage temporelle OU station fermée')
      html = "Veuillez bien choisir la plage temporelle. Si vous l'avez bien choisie, \
              la station que vous consultez est actuellement fermée"
              
    else :
      fichier = 'dispoVelo{}.png'.format(idn)
      plt.savefig('client/{}'.format(fichier))
      html = '<img src="/{}?{}" alt="disponibilite {}" width="100%">'.format(fichier,self.date_time_string(),self.path)
    if data[idn]['adresse2']:
      adresse2 = data[idn]['adresse2']
    else:
      adresse2 = 'Vide'
    if data[idn]['pole']:
      pole = data[idn]['pole']
    else:
      pole = 'Vide'
    body = json.dumps({'stationId':'StationId de la station choisie : '+'Velov-'+donnee['stationId'],\
                        'name':'Nom de la station : '+data[idn]['name'],\
                        'adresse1':'Adresse : '+data[idn]['adresse1'],\
                        'adresse2':'Complément : '+adresse2,\
                        'commune':'Commune : '+data[idn]['commune'],\
                        'numdansarr':'Numéro de la station selon la code arrondissement : '+str(data[idn]['numdansarr']),\
                        'nbbornette':'Nombre de bornettes dans cette station : '+str(data[idn]['nbbornette']),\
                        'pole':'Pôle : '+pole,\
                        'ouverte':'État :'+data[idn]['ouverte'],\
                        'insee': 'Code INSEE : '+str(data[idn]['insee']),\
                        'image':html})
    headers = [('Content-Type','application/json')]
    self.send(body,headers)
    '''
    html = '<img src="/{}?{}" alt="disponibilite {}" width="100%">'.format(fichier,self.date_time_string(),self.path)

    headers = [('Content-Type','text/html;charset=utf-8')]
    self.send(html,headers)
    '''
  def send_static(self):

    # on modifie le chemin d'accès en insérant le répertoire préfixe
    self.path = self.static_dir + self.path

    # on appelle la méthode parent (do_GET ou do_HEAD)
    # à partir du verbe HTTP (GET ou HEAD)
    if (self.command=='HEAD'):
        http.server.SimpleHTTPRequestHandler.do_HEAD(self)
    else:
        http.server.SimpleHTTPRequestHandler.do_GET(self)


  # on envoie un document html dynamique
  def send_html(self,content):
     headers = [('Content-Type','text/html;charset=utf-8')]
     html = '<!DOCTYPE html><title>{}</title><meta charset="utf-8">{}' \
         .format(self.path_info[0],content)
     self.send(html,headers)

  # on envoie un contenu encodé en json
  def send_json(self,data,headers=[]):
    body = bytes(json.dumps(data),'utf-8') # encodage en json et UTF-8
    self.send_response(200)
    self.send_header('Content-Type','application/json')
    self.send_header('Content-Length',int(len(body)))
    [self.send_header(*t) for t in headers]
    self.end_headers()
    self.wfile.write(body) 

  # on envoie la réponse
  def send(self,body,headers=[]):
     encoded = bytes(body, 'UTF-8')

     self.send_response(200)

     [self.send_header(*t) for t in headers]
     self.send_header('Content-Length',int(len(encoded)))
     self.end_headers()

     self.wfile.write(encoded)


  # on analyse la requête pour initialiser nos paramètres
  def init_params(self):
    # analyse de l'adresse
    info = urlparse(self.path)
    self.path_info = [unquote(v) for v in info.path.split('/')[1:]]
    self.query_string = info.query
    self.params = parse_qs(info.query)

    # récupération du corps
    length = self.headers.get('Content-Length')
    ctype = self.headers.get('Content-Type')
    if length:
      self.body = str(self.rfile.read(int(length)),'utf-8')
      if ctype == 'application/x-www-form-urlencoded' : 
        self.params = parse_qs(self.body)
    else:
      self.body = ''
   
    # traces
    print('info_path =',self.path_info)
    print('body =',length,ctype,self.body)
    print('params =', self.params)


# instanciation et lancement du serveur
httpd = socketserver.TCPServer(("", 8081), RequestHandler)
httpd.serve_forever()
