# TD3-lieux-insolites.py

# Application exemple : affichage de mes lieux préférés à la Croix-Rousse 2018-10-24

import http.server
import socketserver
from urllib.parse import urlparse, parse_qs, unquote
import json
import sqlite3
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as pltd

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
        self.send_ponctualite(data)

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
  def send_ponctualite(self,data):

    conn = sqlite3.connect('Velov.sqlite')
    c = conn.cursor()
    # On teste que la région demandée existe bien
    c.execute("SELECT DISTINCT velov_number FROM 'velov-histo2018'")
    station = c.fetchall()
    idn = int(self.path_info[1])
    if ('velov-'+ str(data[idn-1]['idnum']),) in station:   # Rq: reg est une liste de tuples
        stations = [('velov-'+ str(data[idn-1]['idnum']),"blue")]
    else:
        print ('Erreur nom')
        self.send_error(404)    # Région non trouvée -> erreur 404
        return None
    
    # configuration du tracé
    plt.figure(figsize=(18,6))
    plt.ylim(0,15)
    plt.grid(which='major', color='#888888', linestyle='-')
    plt.grid(which='minor',axis='x', color='#888888', linestyle=':')
    
    ax = plt.subplot(111)
    loc_major = pltd.YearLocator()
    loc_minor = pltd.MonthLocator()
    ax.xaxis.set_major_locator(loc_major)
    ax.xaxis.set_minor_locator(loc_minor)
    format_major = pltd.DateFormatter('%B %Y')
    ax.xaxis.set_major_formatter(format_major)
    ax.xaxis.set_tick_params(labelsize=10)
    
    # boucle sur les régions
    for l in (stations) :
        c.execute("SELECT * FROM 'velov-histo2018' WHERE velov_number=? ORDER BY Time_ISO",l[:1])  # ou (l[0],)
        r = c.fetchall()
        # recupération de la date (colonne 2) et transformation dans le format de pyplot
        x = [int(a[0][11:13]+a[0][14:16]) for a in r if not a[2] == '']
        # récupération de la régularité (colonne 8)
        y = [float(a[2]) for a in r if not a[2] == '']
        # tracé de la courbe
        plt.plot_date(x,y,linewidth=1, linestyle='-', marker='o', color=l[1], label=l[0])
        
    # légendes
    plt.legend(loc='lower left')
    plt.title('Disponibilité des velos',fontsize=16)
    plt.ylabel('Nombre de velos disponibles')
    plt.xlabel('temps')

    # génération des courbes dans un fichier PNG
    fichier = 'dispoVelo{}.png'.format(idn)
    plt.savefig('client/{}'.format(fichier))

    html = '<img src="/{}?{}" alt="disponibilite {}" width="100%">'.format(fichier,self.date_time_string(),self.path)

    headers = [('Content-Type','text/html;charset=utf-8')]
    self.send(html,headers)

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
httpd = socketserver.TCPServer(("", 8080), RequestHandler)
httpd.serve_forever()
