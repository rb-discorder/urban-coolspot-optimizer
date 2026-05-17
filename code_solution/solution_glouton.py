def main(link : str):
    #appelle de fonction...

    return #fichier de la solution dans le bon format

# importe l'instance afin de pouvoir la traiter et trouver une solution
def import_instance(instance : str):
     with open(instance, 'r') as  f :
        I, J, T=map(int,f.readline().split()) #I : nombre d'usagers, J : nombre de sites, T : nombre d'années

        print(I,J,T) 

        liste_pt=list(map(int,f.readline().split()))
        liste_nt=list(map(int,f.readline().split()))

    

        liste_fi=[]#matrice 2d des couts de construction des sites ordre : site->année
        liste_cij=[]#matrice 3d des couts d'affection des usager selon leurs sites et  l'année ordre : année->site->usager

        for i in range(I):
            liste_fi.append(list(map(int, f.readline().split())))
            liste_j=[]
            for j in range (J):
                liste_j.append(list(map(int, f.readline().split())))
            liste_cij.append(liste_j)

        return I, J, T, liste_pt, liste_nt, liste_fi, liste_cij

#creer un fichier vierge pour y ajouter la solution
def creer_fichier(nom : str):
    with open(nom, 'w', encoding='utf-8') as f:
        pass


#ajoute une ligne de texte dans un fichier
def ajouter_ligne_fichier(fichier : str, contenu : str):
    with open(fichier, 'a', encoding='utf-8') as f:
        f.write(contenu)

#additione le coût du site avec la mediane des coûts d'affectations
def score_site(i,t,lc_site,lc_usager,coef):
    return lc_site[i][t] + coef*cout_affectation_median(i,t,lc_usager)



     


def cout_affectation_median(i,t,lc_usager):
    copie=sorted(lc_usager[t][i])
    return copie[len(copie)//2]


#classe les sites selon leur score a l'année t,le site avec le score le plus bas est premier dans le classement
def classement_sites(I,t,lc_site,lc_usager,coef):
    classement=[]
    for i in range(I):
        classement.append((i,score_site(i,t,lc_site,lc_usager,coef)))
    classement.sort(key=lambda x: x[1])
    return classement



def affecte_usager_couvert(t,l_site_c,lc_usager,l_usager_c):
    return None





def solution_glouton(instance : str, nom_fichier_solution : str):
    I, J, T, liste_pt, liste_nt, liste_fi, liste_cij = import_instance(instance)

    #coût total de la solution
    cout_total=0


    creer_fichier(nom_fichier_solution)

    #liste des sites construit durant le temps [(site1, année5),...]
    site_construit=[]
    # liste des uagers et de leurs premiere année d'affectation

    usager_affectée=[]
    usager_non_affectée=[x for x in range(J)]

    
    # listes des usagée et de leur affectation actuelle ex : [(usager1, site8), (usager5, site4)]
    meilleur_cout_usager=[]


    PT=0 #nombre de site total a la fin de la periode t


    for t in range(T):
        PT+=liste_pt[t] #nombre de site a la fin de l'année

        ratio=liste_nt[t]/PT #nombre de d'usager moyen par site a la fin de la periode t : nt/PT

        classement=classement_sites(I, t, liste_fi, liste_cij,ratio)

        set={x[0] for x in site_construit}



        pt=0
        while pt< liste_pt[t]:

            if classement[pt][0] not in set:
                site_construit.append((classement[pt][0],t))
                cout_total+=liste_fi[classement[pt][0]][t]
                pt+=1

        # liste des couples (site, usagée) les moins chere parmi les usager deja couvert anterieurement
        liste_best_uaf=couts_min_tout_usager(t,site_construit,usager_affectée,liste_cij)


        # liste des couples (site, usagée) les moins chere parmi les usager non couvert anterieurement
        liste_best_u=couts_min_tout_usager(t,site_construit,usager_non_affectée,liste_cij)
        for x in liste_best_u[x]:
            usager_affectée.append(liste_best_u[x][1])
            usager_non_affectée.remove(liste_best_u[x][1])

            

            
# a finir




 













#l_site_c est une matrice 2d ou chaque element est composée du numero du site et de son année ex : [(site1,anné4),(site7,année8)]
def cout_min_usager(t,j,l_site_c , lc_usager):
    min=lc_usager[t][0][j]
    af_min=(0,j)  # numero du sites affectée et l'usagée
    for i in l_site_c:
        index=i[0]
        if lc_usager[t][index][j]<min:
            min=lc_usager[t][index][j]
            af_min=(index,min)

    return af_min



# la variable liste_usager permet de choisir quelle variable regarder ou non, exemple on peut regarder seulement les usager affectée les année anterieures
#c'est une liste composer des numero des usager : [0,1,2,3,4,5,6,7,8,9,...]

def couts_min_tout_usager(t,l_site_c,liste_usager,lc_usager):
    liste_min=[]
    for j in liste_usager:
        liste_min.append(cout_min_usager(t,j,l_site_c,lc_usager))

    return liste_min






