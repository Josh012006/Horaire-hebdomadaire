# Membres du groupe
# Josué Mongan (20290870)
# Kuza Twagiramungu (20317467)
# Date: 13-12-2024


import codeboot


# Variables globales pour la maintenabilité du code.

debut_horaire = "0800"
fin_horaire = "1700"
duree_case = 30           # durée de la case en minutes

jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]

signe_clic = "⇅"

palette = ["#0FF", "#CFA", "#CDF", "#EB8", "#FF0", "#69E", "#F0F"]
couleur_actuel = 0

restant = []              # tableau contenant les couleurs de la palette non
                          # utilisées après une importation

cliquer = None            # variable gardant l'état de clic de l'utilisateur
  
evenements = []






# La fonction operations_horaire prend deux paramètres: deux chaînes de
# caractère operande et operateur. Le paramètre operande précise une heure sous
# format militaire et le paramètre operateur précise l'opération à effectuer
# (+ ou -). Cette fonction ajoute ou retire la durée d'une case à l'heure
# passée en paramètre et renvoie la réponse en format militaire.

def operations_horaire(operande, operateur):
 
    heure = int(operande[:2])
    minutes = int(operande[2:])
 
    nb_minutes = heure * 60 + minutes     # nombre total de minutes
 
    if(operateur == '+'):
     
        nv_minutes = nb_minutes + duree_case
     
    else:
     
        nv_minutes = nb_minutes - duree_case
     
        # Cas d'une soustraction ramenant à avant 00h.
     
        if(nv_minutes < 0):
            nv_minutes = 24 * 60 + nv_minutes
 
    nv_heure = str((nv_minutes // 60) % 24)
    nv_minutes = str(nv_minutes % 60)
 
    # Reconstitution de la nouvelle heure.
  
    res = "0" * (len(nv_heure) == 1) + nv_heure
    res += "0" * (len(nv_minutes) == 1) + nv_minutes
 
    return res



# La fonction table_heures ne prend aucun paramètre. Elle génère un tableau qui
# contient l'ensemble des heures de l'horaire en format militaire tout en
# tenant compte de l'heure de début, l'heure de fin et la durée de la case.

def table_heures():
 
    actuel = debut_horaire
 
    resultat = [debut_horaire]
 
    while (actuel < operations_horaire(fin_horaire, '-')):
      
        # Générer l'heure suivante en ajoutant la durée de la case.
      
        actuel = operations_horaire(actuel, '+')
        resultat.append(actuel)
  
    return resultat



# La fonction matrice prend deux paramètres qui sont des entiers. Le premier
# est le nombre de rangées de la matrice et le deuxième le nombre de colonnes.
# La fonction retourne une matrice correspondante avec la valeur None à toutes
# les positions.

def matrice(nb_ligne, nb_col):
 
    resultat = []
 
    for _ in range(nb_ligne):
        resultat.append([None] * nb_col)
 
    return resultat



# La procédure dessiner_horaire ne prend aucun paramètre. Elle reproduit, sur
# le HTML de la page, les informations que la matrice horaire contient.

def dessiner_horaire():
  
    tbody = ""            # HTML du body de la table
  
    for i in range(len(horaire)):
      
        # Formation du HTML de la ligne de la matrice.
      
        heure = heures[i]
        tr = "<td>" + heure[:2] + "h" + heure[2:] + "</td>"
      
        for j in range(len(horaire[i])):
          
            info = horaire[i][j]
          
            # Formation de l'id et du gestionnaire d'événement de la case.
          
            ID = "case_" + str(i) + "_" + str(j)
            ev = "clic(" + str(i) + "," + str(j) + ")"
          
            attributs = 'class="cell" id="' + ID + '" onclick="' + ev + '"'
          
          
            # Gestion de chaque état possible d'une case.
          
            if(not info):
              
                contenu = ""
          
            elif(info == signe_clic):
              
                contenu = "<b>" + signe_clic + "</b>"
              
            else:
              
                contenu = info.nom
                attributs += 'style="background-color:' + info.couleur + '"'
              
          
            td = "<td " + attributs + ">" + contenu + "</td>"
            tr += td
          
          
        tbody += "<tr>" + tr + "</tr>"
  
    # Ajout du HTML sur la page.
  
    table_body = document.querySelector(".table-body")
    table_body.innerHTML = tbody



# La fonction colonne prend en paramètre un entier. Elle renvoie la colonne de
# la matrice horaire qui a pour index l'entier en question.

def colonne(j):
  
    resultat = []
  
    for i in range(len(horaire)):
        resultat.append(horaire[i][j])
      
    return resultat



# La procédure inserer_colonne prend deux paramètres. Le premier est un tableau
# et le deuxième est un entier qui est l'index d'une colonne de la matrice
# horaire. Dans la matrice horaire, cette procédure remplace les valeurs de la
# colonne indexée par celles contenues dans le tableau.

def inserer_colonne(col, j):
  
    global horaire
  
    for i in range(len(col)):
        horaire[i][j] = col[i]



# La fonction index prend deux paramètres: le premier est un tableau et le
# deuxième est une valeur. Elle renvoie l'index de la première occurence de la
# valeur à l'intérieur du tableau et -1 si elle n'y ai pas trouvée.

def index(tab, valeur):
  
    for i in range(len(tab)):
        if(tab[i] == valeur):
            return i
    return -1



# La fonction index_ev prend un seul paramètre. Il s'agit d'un enregistrement
# qui possède les champs jour, debut, fin, nom, couleur et représentant un
# événement. Elle retourne un enregistrement ayant un champ debut qui est
# l'index de la rangée de début de l'événement et un champ fin qui est l'index
# de la rangée de fin de l'événement.

def index_ev(ev):
  
    idx_debut = index(heures, ev.debut)
    idx_fin = index(heures, operations_horaire(ev.fin, '-'))
  
    return struct(debut=idx_debut, fin=idx_fin)


 
# La fonction conflit prend trois paramètres. Le premier est un tableau
# représentant une colonne de la matrice horaire. Le deuxième est un entier qui
# est un index de début et le troisième est un entier qui est un index de fin.
# Cette fonction retourne un booléen qui est True si l'une des cases entre ces
# deux index contient déjà un événement.

def conflit(col, debut, fin):
  
    for i in range(debut, fin + 1):
        if(col[i] and col[i] != signe_clic):
            return True
    return False



# La procédure err prend un seul paramètre qui est un message texte. Elle
# affiche le message sur la grille et réinitialise la grille comme si aucun
# clic n'avait eut lieu.

def err(msg):
  
    global horaire, cliquer
  
    if(msg != ""):
        alert(msg)
  
    # Réinitialiser l'horaire et la variable cliquer.
  
    horaire[cliquer.i][cliquer.j] = None
    cliquer = None


  
# La fonction nv_couleur ne prend aucun paramètre. Elle retourne un texte
# correspondant au code couleur à appliquer pour le nouvel événement, tout en
# respectant la spécification de l'énoncé c'est-à-dire en tenant aussi compte
# de l'importation de nouveaux fichiers.

def nv_couleur():
  
    global restant, couleur_actuel
  
    if(len(restant) == 0):
      
        # Cycler sur les couleurs.
      
        couleur = palette[couleur_actuel]
        couleur_actuel = (couleur_actuel + 1) % 7
      
    else:
      
        # Utiliser la prochaine couleur non utilisée dans celles restantes.
      
        couleur = restant.pop(0)
      
    return couleur
 


# La procédure init ne prend aucun paramètre. Elle lance l'application et
# ajoute les styles CSS et le HTML de l'horaire à la page.

def init():
 
    global heures, horaire
 
    # Ajout du code css dans le head de la page.
 
    style = readFile("styles.css") 
    document.head.innerHTML += "<style>" + style + "</style>"
 
    # Ajout de la table au body de la page.
 
    structure = """
    <div class="container">
        <div class="entete">
            <h2>Planificateur hebdomadaire</h2>
            <button class="droite" onclick="exporter_csv()">Exporter</button>
        </div>
        <div class="horaire">
            <table>
                <thead class="table-head"></thead>
                <tbody class="table-body"></tbody>
            </table>
        </div>
    </div>
    """
    document.body.innerHTML = structure
 
    # Ajout de l'écouteur d'événement drag-and-drop à l'horaire.
 
    codeboot.add_file_drop_handler(document.querySelector('.horaire'),
                                   importer_csv)
 
    # Générer les heures de la table.
 
    heures = table_heures()
 
    # Générer une grille d'état initial de l'horaire.
 
    horaire = matrice(len(heures), len(jours))

    # Formation du header du tableau et insertion dans le HTML
 
    table_head = document.querySelector(".table-head")
 
    thead = "".join(map(lambda j: "<th>" + j + "</th>", jours))
 
    table_head.innerHTML = "<tr><th>Heure</th>" + thead + "</tr>"
 
    # Affichage de l'horaire initial.
 
    dessiner_horaire()



# La procédure clic prend en paramètre les entiers i et j qui sont les
# coordonnées de la case cliquée et traite l'événement selon la spécification
# de l'énoncé.

def clic(i, j):
  
    global cliquer, horaire, couleur_actuel, evenements
  
    if(not cliquer):
      
        # Cas du premier clic.
      
        if(not horaire[i][j]):
          
            horaire[i][j] = signe_clic
            cliquer = struct(i=i, j=j)
      
        # Cas de la suppression d'un événement de l'horaire.
      
        else:
          
            supprimer = confirm("Supprimer l'événement?")
          
            if(supprimer):
              
                supprime = horaire[i][j]   # événement à supprimer
              
                # Récupération de la colonne contenant l'événement à supprimer.
              
                col = colonne(j)
              
                # Suppression de l'événement dans la matrice horaire.
              
                for x in range(len(col)):
                  
                    elem = col[x]
                  
                    if(elem and elem.nom == supprime.nom):
                        col[x] = None
              
                inserer_colonne(col, j)
              
                # Suppression de l'événement de la tables des événements.
              
                for ev in evenements:
                  
                    idx = index_ev(ev)
                  
                    if(idx.debut <= i and i <= idx.fin):
                        evenements.remove(ev)
                        break
  
    else:
      
        if(j != cliquer.j):
          
            # Cas d'un deuxième clic dans une autre colonne.
          
            msg = "Vous devez cliquer une case dans la même journée."
            err(msg)
          
        else:
          
            # Cas d'un deuxième clic dans la même colonne.
          
            col = colonne(j)
            heure_debut = min(i, cliquer.i)
            heure_fin = max(i, cliquer.i)
          
            if(conflit(col, heure_debut, heure_fin)):
              
                # Cas d'un conflit horaire.
              
                msg = "Il y a un conflit avec une plage horaire déjà occupée."
                err(msg)
             
            else:
             
                nom = prompt("Nom de l'événement?")
                msg = "Le nom ne doit pas débuter ou terminer avec un espace."
              
                if(nom != "" and not nom):
                  
                    # Cas d'une annulation de l'opération.
                  
                    err("")
              
                elif(nom == "" or nom[0].isspace() or nom[-1].isspace()):
                  
                    err(msg)
              
                else:
                  
                    # Vérifier si un événement pareil n'existe pas déjà et
                    # prendre sa couleur si c'est le cas.
                  
                    for ev in evenements:
                        if (ev.nom == nom):
                            couleur = ev.couleur
                            break
                    else:
                        couleur = nv_couleur()
                  
                    # Modifier l'horaire.
                  
                    for x in range(heure_debut, heure_fin + 1):
                        col[x] = struct(nom=nom, couleur=couleur)
       
                    inserer_colonne(col, j)
                  
                    # Ajouter le nouvel événement à la table des événements.
                  
                    jour = jours[j]
                    debut = heures[heure_debut]
                    fin = operations_horaire(heures[heure_fin], '+')
                  
                    nv_ev = struct(jour=jour, debut=debut, fin=fin, nom=nom,
                                   couleur=couleur)
                  
                    evenements.append(nv_ev)
                  
                    # Réinitialiser le clic.
                  
                    cliquer = None
                    
  
    # Mettre l'horaire à jour.
  
    dessiner_horaire()
            


# La procédure exporter_csv n'a aucun paramètre. Elle télécharge le fichier CSV
# correspondant à l'horaire créé par l'utilisateur.

def exporter_csv():
  
    # Récupération du nom du fichier à récupérer.
  
    nom = prompt("Nom de fichier?")
  
    # Vérification de l'entrée effective d'un nom.
  
    if(nom == "" or nom):
      
        # Formation du contenu du fichier.
  
        contenu = ""

        for ev in evenements:
            ligne = [ev.jour, ev.debut, ev.fin, ev.nom, ev.couleur]

            contenu += ",".join(ligne) + "\n"

        # Téléchargement du fichier.

        codeboot.download(nom, contenu) 



# La procédure importer_csv prend en paramètre un tableau de fichiers ayant un
# seul élément. Il s'agit d'un fichier csv qui contient des informations sur un
# nouvel horaire que la procédure réflète dans le navigateur.

def importer_csv(fichiers):
  
    global horaire, evenements, restant, couleur_actuel
  
    # Récupération du contenu du fichier.
  
    contenu = fichiers[0].content

    # Récupération des lignes du fichier.
  
    lignes = contenu.split("\n")
  
    # Générer les événements contenus dans le fichier.
  
    evenements = []         # réinitialisation de la table des événements
  
    for ligne in lignes:
      
        elem = ligne.split(',')
      
        if(ligne != ''):    # vérification de la présence d'un contenu
           
            ev = struct(jour=elem[0], debut=elem[1], fin=elem[2], nom=elem[3],
                    couleur=elem[4])
      
            evenements.append(ev)
      
    # Gestion des couleurs.
  
    restant = []               # réinitialisation du tableau restant
  
    couleurs_ev = list(map(lambda ev: ev.couleur, evenements))
  
    for couleur in palette:
        if(couleur not in couleurs_ev):
            restant.append(couleur)
          
    couleur_actuel = 0         # réinitialisation de la couleur actuelle
      
    # Modification de la matrice horaire.
  
    horaire = matrice(len(heures), len(jours))  # réinitialiser l'horaire
  
    for ev in evenements:
      
        # Extraction de la colonne contenant l'événement.
      
        idx_col = index(jours, ev.jour)
        col = colonne(idx_col)
      
        # Récupération de l'index de début et de l'index de fin de la partie
        # concernée par l'événement.
      
        idx = index_ev(ev)
      
        # Modification de la colonne concernée dans la matrice horaire.
      
        for x in range(idx.debut, idx.fin + 1):
            col[x] = struct(nom=ev.nom, couleur=ev.couleur)
          
        inserer_colonne(col, idx_col)
  
  
    # Mettre l'horaire à jour visuellement.
  
    dessiner_horaire()


init()