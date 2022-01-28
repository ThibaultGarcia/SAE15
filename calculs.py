from math import sqrt
from pylab import *

def mesure_moyenne(liste):
    somme = 0
    for valeur in liste:
        somme += valeur
    moyenne = somme / len(liste)
    return moyenne

def mesure_ecartype(liste):
    moyenne = mesure_moyenne(liste)
    somme = 0
    for valeur in liste:
        somme += (valeur - moyenne)**2
    ecartype = sqrt (somme/len (liste))
    return ecartype

def courbe(listel, liste2):
    y = np.array(listel)
    x = np.array(liste2)
    plt.plot(x, y)
    plt.show()