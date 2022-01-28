import matplotlib.pyplot as plt
import datetime
import numpy as np
import pandas as pd
from os import walk
listeFichiers = []
for (repertoire, sousRepertoires, fichiers) in walk("./parkings"):
    listeFichiers.extend(fichiers)

data = []

for name in listeFichiers:
    fichier = open("./parkings/" + name, "r")

    dates = []
    voitures = []
    vélos = []

    for line in fichier.read().split("\n"):
        if not line.startswith("#") and line != "":
            [date, voiture, vélo] = line.split(";")
            dates.append(date)
            voitures.append(100 - round(float(voiture.replace(" ", "")), 2)) # Enregisté en % de places libres donc on récupère le % de places occupées
            vélos.append(100 - round(float(vélo.replace(" ", "")), 2))
    data.append({ "name" : name.replace(".dat", ""), "dates": dates, "voitures": voitures, "vélos": vélos })



for current in data:

    #define data
    df = pd.DataFrame({'date': current["dates"], 'voitures': current["voitures"]})

    df2 = pd.DataFrame({'date': current["dates"], 'velos': current["vélos"]})

    plt.xticks(rotation=45, fontweight='light', fontsize=7)#adjust date text to be readable on graph

    #plot both time series
    plt.plot(df.date, df.voitures, label='Voitures', linewidth=3)
    plt.plot(df2.date, df2.velos, color='red', label='Vélos', linewidth=3)

    #add title an axis labels
    plt.title(current["name"])
    plt.xlabel("Date et heure")
    plt.ylabel("% d'occupation")

    #add legend
    plt.legend()

    #display plot
    plt.show() 