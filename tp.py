import requests
import time
import xml.etree.ElementTree as ET
from lxml import etree
import datetime

def getDate():
    return str(datetime.date.today()) + "@" + datetime.datetime.now().strftime("%H-%M-%S")

parkings=['FR_MTP_ANTI','FR_MTP_COME','FR_MTP_CORU','FR_MTP_EURO','FR_MTP_FOCH','FR_MTP_GAMB','FR_MTP_GARE','FR_MTP_TRIA','FR_MTP_ARCT','FR_MTP_PITO','FR_MTP_CIRC','FR_MTP_SABI','FR_MTP_GARC','FR_MTP_SABL','FR_MTP_MOSS','FR_STJ_SJLC','FR_MTP_MEDC','FR_MTP_OCCI','FR_CAS_VICA','FR_MTP_GA109','FR_MTP_GA250','FR_CAS_CDGA','FR_MTP_ARCE','FR_MTP_POLY'] 
noms = ["Antigone","Comédie","Corum","Europa","Foch","Gambetta","Gare St Roch","Triangle","Arc du Triomphe","Pitot","Circe","Sabines","Garcia Lorca","Sablassou","Mosson","Saint Jean Le Sec","Euromedecine","Occitanie","Vicarello","Gaumont EST","Gaumont OUEST","Charles de Gaulle","Les Arceaux","Polygone"]
ids = ["016","002","005","--","007","020","001","--","--","--","--","043","033","--","--","--","041","036","--","--","--","--","023","--"]
#liste des parkings, leurs noms, et leur lien avec les ID des parkings à vélos

while True:
    
    classement = open("./data/data" + getDate() + ".dat","w",encoding="utf-8")

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




    for i in range(len(parkings)):
        response = requests.get("https://data.montpellier3m.fr/sites/default/files/ressources/"+parkings[i]+".xml")

        tree = ET.ElementTree(ET.fromstring(response.text)) #extraction des données de la page

        Free = int(tree.find("./Free").text) #trouver les places libres sur la plage
        Total = int(tree.find("./Total").text) #trouver les places libres sur la page

        velo = {}

        for searchvelo in vraiListeVelo: 
            if searchvelo["id"] == ids[i]:
                velo = searchvelo
        #associate velo id and parking id
        if "fr" in velo and "to" in velo:
            velo["fr"] = int(velo["fr"])
            velo["to"] = int(velo["to"])
            stringfinal = noms[i] + ";" + str(Free) + ";" + str(Total) + ";" + str(velo["fr"]) + ";" + str(velo["to"]) #association des éléments pour l'écriture dans un fichier pouvant être exploité
        else:
            stringfinal = noms[i] + ";" + str(Free) + ";" + str(Total) + ";" + "None" + ";" + "None" #association des éléments pour l'écriture dans un fichier pouvant être exploité
        classement.write(stringfinal + "\n") #write in file

        parkingDataFile = open("./parkings/" + noms[i] + ".dat", "a+", encoding='utf-8')

        parkingDataFile.seek(0)
        if parkingDataFile.read() == "": 
            parkingDataFile.write("#Temps                 ;        % P. Voitures     ;        % P. Vélos\n")

        if "fr" in velo and "to" in velo:
            parkingDataFile.write(getDate() + "    ;    " + str((Free/Total) * 100) + "    ;    " + str((velo["fr"]/velo["to"]) * 100) + "\n")
        else: 
            parkingDataFile.write(getDate() + "    ;    " + str((Free/Total) * 100) + "    ;    " + "0" "\n")
        
        parkingDataFile.close()

    classement.close()

    time.sleep(60 * 5)