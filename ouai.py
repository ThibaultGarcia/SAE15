import requests
from lxml import etree
import urllib.request
import time

response = requests.get("https://data.montpellier3m.fr/sites/default/files/ressources/TAM_MMM_VELOMAG.xml")

page_velo = open("tempo.xml", "w", encoding='utf-8')
page_velo.write(response.text)
page_velo.close()
tree = etree.parse("tempo.xml")

listeVelo = tree.xpath("/vcs/sl/si")
vraiListeVelo = [] #création de la liste qui sera reportée au fichier final

for velo in listeVelo:
    currentVelo = {} #création d'un dictionnaire pour les vélos
    keys = velo.keys() #clé du cictionnaire
    values = velo.values() #valeur du dictionnaire

    for i in range(len(keys)):
        currentVelo[keys[i]] = values[i]

    vraiListeVelo.append(currentVelo)
    # print(currentVelo["na"])

# print(vraiListeVelo)
