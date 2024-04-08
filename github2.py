
import numpy as np

# Durée de la simulation en mois
DUREE_SIMULATION = 62

# Santé économique de base
BASE_SANTE_ECONOMIQUE = 1000

# Définition des différents types d'emplois avec leurs caractéristiques
OUVRIER = {"nom": "Ouvrier", "cout_mensuel_formation": 100, "duree_formation": 4, "gain_mensuel_emploi": 150, "estimation_par_mois": 100}
INTERMEDIAIRE = {"nom": "Intermédiaire", "cout_mensuel_formation": 150, "duree_formation": 30, "gain_mensuel_emploi": 200, "estimation_par_mois": 40}
CADRE = {"nom": "Cadre", "cout_mensuel_formation": 210, "duree_formation": 60, "gain_mensuel_emploi": 120, "estimation_par_mois": 15}

# Liste des différents types d'emploi
EMPLOIS = [OUVRIER, INTERMEDIAIRE, CADRE]

# Fonction pour obtenir de nouveaux migrants de chaque type d'emploi
def obtenir_nouveaux_migrants(liste_migrants, sante_economique):
    for emploi in EMPLOIS:
        if sante_economique > 0:
            nouveaux_migrants_emploi = np.random.poisson(emploi["estimation_par_mois"])
        else:
            nouveaux_migrants_emploi = 0
        liste_migrants[emploi["nom"]] += [emploi["duree_formation"]] * nouveaux_migrants_emploi
    return liste_migrants

# Fonction principale
def main():
    sante_economique = BASE_SANTE_ECONOMIQUE
    liste_migrants = {emploi["nom"]: [] for emploi in EMPLOIS}
    evolution_sante = []
    evolution_migrants_ouvrier = []
    evolution_migrants_intermediaire = []
    evolution_migrants_cadre = []

    # Pour les nouveaux graphiques
    cout_formation_mensuel = []
    gains_mensuels_migrants = []

    # Définir des mois aléatoires pour les événements (crises ou booms)
    evenements_mois = np.random.choice(range(1, DUREE_SIMULATION), size=2, replace=False)
    
    for mois in range(DUREE_SIMULATION):
        evolution_sante.append(sante_economique)
        liste_migrants = obtenir_nouveaux_migrants(liste_migrants, sante_economique)

        nb_migrants_ouvrier = len(liste_migrants["Ouvrier"])
        nb_migrants_intermediaire = len(liste_migrants["Intermédiaire"])
        nb_migrants_cadre = len(liste_migrants["Cadre"])

        evolution_migrants_ouvrier.append(nb_migrants_ouvrier)
        evolution_migrants_intermediaire.append(nb_migrants_intermediaire)
        evolution_migrants_cadre.append(nb_migrants_cadre)

        cout_formation = 0
        gains_mensuels = 0
        for emploi in EMPLOIS:
            liste = liste_migrants[emploi["nom"]]
            for i in range(len(liste)):
                if liste[i] > 0:
                    liste[i] -= 1
                    sante_economique -= emploi["cout_mensuel_formation"]
                    cout_formation += emploi["cout_mensuel_formation"]
                else:
                    sante_economique += emploi["gain_mensuel_emploi"]
                    gains_mensuels += emploi["gain_mensuel_emploi"]
                    
        cout_formation_mensuel.append(cout_formation)
        gains_mensuels_migrants.append(gains_mensuels)

        # Appliquer un événement aléatoire si le mois actuel est un mois d'événement
        if mois in evenements_mois:
            # Choisir aléatoirement entre un boom économique et une crise
            evenement_type = np.random.choice(["boom", "crise"])
            if evenement_type == "boom":
                sante_economique *= 1 + np.random.uniform(0.1, 0.2)  # Augmenter de 10% à 20%
            else:
                sante_economique *= 1 - np.random.uniform(0.1, 0.2)  # Diminuer de 10% à 20%

    
