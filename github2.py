import random

def embaucher_migrant(categorie, sante_econ):
    bonus = {"cadre": 120, "ouvrier": 15, "intermediaire": 60}
    return sante_econ + bonus.get(categorie, 0)

def simulation_formation(personnes, sante_initiale, cout_mensuel, mois_formation):
    resultats_globaux = []
    for _ in range(personnes):
        sante_econ = sante_initiale
        resultats_mois = [sante_econ]
        for mois in range(1, mois_formation + 1):
            sante_econ -= cout_mensuel
            resultats_mois.append(sante_econ)
        resultats_globaux.append(resultats_mois)
    return resultats_globaux

def simulation_migration(resultats_formation, categorie, sante_depart, mois_migration):
    resultats_globaux = []
    for formation in resultats_formation:
        sante_econ = sante_depart
        resultats_mois = formation[:]
        for mois in range(1, mois_migration + 1):
            sante_econ = embaucher_migrant(categorie, sante_econ)
            resultats_mois.append(sante_econ)
        resultat_annuel = resultats_mois[-1] - resultats_mois[len(formation)]
        resultats_globaux.append((resultats_mois, resultat_annuel))
    return resultats_globaux

def afficher_resultats_mois(resultats_mois, categorie):
    print(f"Résultats mois par mois pour la personne en {categorie} :")
    for mois, resultat in enumerate(resultats_mois):
        print(f"Mois {mois}: Santé économique = {resultat}")

def simuler_formation_migration(categorie, nombre_personnes, sante_initiale, cout_mensuel_formation, mois_formation, mois_migration):
    resultats_globaux = []
    resultats_formation = simulation_formation(nombre_personnes, sante_initiale, cout_mensuel_formation, mois_formation)
    
    if resultats_formation:  # Vérifier si la liste n'est pas vide
        sante_depart = resultats_formation[0][-1]
        resultats_migration = simulation_migration(resultats_formation, categorie, sante_depart, mois_migration)
        resultats_globaux.extend(resultats_migration)
    
    return resultats_globaux

def determiner_nombre_embauches(sante_economique):
    moyenne = 0.5
    ecart_type = 0.2
    return round(random.normalvariate(moyenne, ecart_type) * sante_economique)

# Initialisation des paramètres
nombre_personnes = 5
sante_initiale = 100
cout_mensuel_formation_cadre = 55
mois_formation_cadre = 8
mois_migration_cadre = 12
cout_mensuel_formation_ouvrier = 10
mois_migration_ouvrier = 12
duree_simulation = 12  # 1 an

def afficher_resultats_total(resultats_migration, categorie):
    total = sum(resultat[1] for resultat in resultats_migration)
    print(f"Résultat total pour {categorie} : {total}")

# Simulation de la formation et migration pour un cadre
resultats_migration_cadre = simuler_formation_migration("cadre", 1, sante_initiale, cout_mensuel_formation_cadre, mois_formation_cadre, mois_migration_cadre)

# Affichage des résultats mois par mois pour un cadre
for resultat in resultats_migration_cadre:
    afficher_resultats_mois(resultat[0], "cadre")

# Affichage du résultat total pour un cadre
afficher_resultats_total(resultats_migration_cadre, "cadre")

# Simulation de la formation et migration pour un ouvrier
nombre_embauches_ouvriers = determiner_nombre_embauches(sante_initiale)
resultats_migration_ouvrier = simuler_formation_migration("ouvrier", 1, sante_initiale, cout_mensuel_formation_ouvrier, 4, mois_migration_ouvrier)

# Affichage des résultats mois par mois pour un ouvrier
for resultat in resultats_migration_ouvrier:
    afficher_resultats_mois(resultat[0], "ouvrier")

# Affichage du résultat total pour un ouvrier
afficher_resultats_total(resultats_migration_ouvrier, "ouvrier")

# Calcul du résultat total pour un cadre
total_cadre = sum(resultat[1] for resultat in resultats_migration_cadre)

# Calcul du résultat total pour un ouvrier
total_ouvrier = sum(resultat[1] for resultat in resultats_migration_ouvrier)

# Calcul de la somme des deux résultats totaux
somme_totale = total_cadre + total_ouvrier

print(f"La somme des résultats totaux pour les cadres et les ouvriers est : {somme_totale}")