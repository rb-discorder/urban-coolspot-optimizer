def main(link : str):
    #appelle de fonction...

    return #fichier de la solution dans le bon format

#//////////////////////////////////////////////////////////////////////////
# importe l'instance afin de pouvoir la traiter et trouver une solution
def import_instance(instance : str):
     with open(instance, 'r') as  f :
        I, J, T=map(int,f.readline().split()) #J : nombre d'usagers, I : nombre de sites, T : nombre d'années
        print(I,J,T) 
        liste_pt=list(map(int,f.readline().split()))
        liste_nt=list(map(int,f.readline().split()))
        liste_fi=[]#matrice 2d des couts de construction des sites ordre : site->année
        liste_cij=[]#matrice 3d des couts d'affection des usager selon leurs sites et  l'année ordre : site->usager->année

        for i in range(I):
            liste_fi.append(list(map(int, f.readline().split())))
            liste_j=[]
            for j in range (J):
                liste_j.append(list(map(int, f.readline().split())))
            liste_cij.append(liste_j)

        return I, J, T, liste_pt, liste_nt, liste_fi, liste_cij
     
#////////////////////////////////////////////////////////////////////////////
#creer un fichier vierge pour y ajouter la solution
def creer_fichier(nom : str):
    with open(nom, 'w', encoding='utf-8') as f:
        pass


#ajoute une ligne de texte dans un fichier
def ajouter_ligne_fichier(fichier : str, contenu : str):
    with open(fichier, 'a', encoding='utf-8') as f:
        f.write(contenu)

#/////////////////////////////////////////////////////////////////////////////////
#initialisation des fonctions de calcul des choix
#calcul le cout median d'un usager pour un site i
def cout_affectation_median(i,J,t,lc_usager):
    copie=[]

    for j0 in range(J):
        copie.append(lc_usager[i][j0][t])
    copie=sorted(copie)
    return copie[len(copie)//2]


#additione le coût du site avec la mediane des coûts d'affectations
def score_site(i,J,t,lc_site,lc_usager,coef):
    return lc_site[i][t] + coef*cout_affectation_median(i,J,t,lc_usager)


#classe les sites selon leur score a l'année t,le site avec le score le plus bas est premier dans le classement
def classement_sites(I,J,t,lc_site,lc_usager,coef):
    classement=[]

    for i in range(I):
        classement.append((i,score_site(i,J,t,lc_site,lc_usager,coef)))
    classement.sort(key=lambda x: x[1])
    return classement


#calcul le cout minimum d'un usager parmi tout les affectation possible a l'année t
#l_site_c est une matrice 2d ou chaque element est composée du numero du site et de son année ex : [(site1,anné4),(site7,année8)]
def cout_min_usager(t,j,l_site_c , lc_usager):
    if len(l_site_c)==0:
        return -1
    
    min0=lc_usager[l_site_c[0][0]][j][t]
    af_min=(j,min0)  # le numero de l'usager et son cout minimum

    for i in l_site_c:
        index=i[0]
        if lc_usager[index][j][t]<min0:
            min0=lc_usager[index][j][t]
            af_min=(j,min0)

    return af_min


#calcul le cout minimum de tout les usagers concernée 
# la variable liste_usager permet de choisir quelle variable regarder ou non, exemple on peut regarder seulement les usager affectée les année anterieures
#c'est une liste composer des numero des usager : [0,1,2,3,4,5,6,7,8,9,...]
def couts_min_tout_usager(t,l_site_c,liste_usager,lc_usager):
    liste_min=[]

    for j in liste_usager:
        liste_min.append(cout_min_usager(t,j,l_site_c,lc_usager))

    return liste_min

#//////////////////////////////////////////////////////////////////////////////////////
#fonction de calcul d'une solution
def solution_glouton(instance : str, nom_fichier_solution : str):
    creer_fichier(nom_fichier_solution)

    #//////////////////
    #variable et listes pour l'ensemble des année 
    #variable dentrée et jeu de donnée
    I, J, T, liste_pt, liste_nt, liste_fi, liste_cij = import_instance(instance)
    #coût total de la solution
    cout_total=0
    #liste des sites construit durant le temps [(site1, année5),...]
    site_construit=[]
    # liste composée des usager et de leur premiere année d'affectation : pour les ligne du document
    usager_ouverture=[]
    # liste des uagers affectée et non affectée 
    usager_affectée=[]
    usager_non_affectée=[x for x in range(J)]
    #nombre de site total a la fin de la periode t
    PT=0

    #//////////////////////////
    # boucle de construction et d'affectation sur chaque année t
    for t in range(T):
        #////////////////////
        #initialisation des variable de l'année
        PT+=liste_pt[t] #nombre de site a la fin de l'année
        ratio=liste_nt[t]/PT #nombre de d'usager moyen par site a la fin de la periode t : nt/PT
        classement=classement_sites(I,J, t, liste_fi, liste_cij,ratio)
        set0={x[0] for x in site_construit}

        #/////////////////////
        #selection des sites a construire cette année
        pt=0
        i=0
        while pt< liste_pt[t] and i< I:
            if classement[i][0] not in set0:
                
                site_construit.append((classement[i][0],t))
                cout_total+=liste_fi[classement[i][0]][t]
                pt+=1
            
            i+=1  
        #////////////////////////
        #selection des usager à affectée cette année
        # liste des couples (usager, cout minimum) les moins chere parmi les usager deja couvert anterieurement
        liste_best_uaf=couts_min_tout_usager(t,site_construit,usager_affectée,liste_cij)
        
        for af in liste_best_uaf:
            cout_total+=af[1]

        # liste des couples (usager, cout minimum) les moins chere parmi les usager non couvert anterieurement
        liste_best_u=couts_min_tout_usager(t,site_construit,usager_non_affectée,liste_cij)
        liste_best_u.sort(key=lambda x: x[1])
        
        for x in liste_best_u:
            if len(usager_affectée)>=liste_nt[t]:
                break
            usager_affectée.append(x[0])
            usager_ouverture.append((x[0],t))
            cout_total+=x[1]
            usager_non_affectée.remove(x[0])

        
        
