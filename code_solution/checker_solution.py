def convertisseur(chemin_fichier, chemin_fichier_solution : str):
    with open(chemin_fichier, 'r') as  f1 :
        liste_para=list(map(int,f1.readline().split()))
        print(liste_para)
        liste_pt=list(map(int,f1.readline().split()))
        liste_nt=list(map(int,f1.readline().split()))
    

        I=liste_para[0]
        J=liste_para[1]
        T=liste_para[2]

        
        liste_fi=[]#matrice 2d des couts de construction des sites
        liste_cij=[]#matrice 3d des couts d'affection des usager selon leur I et l année

        for i in range(I):
            liste_fi.append(list(map(int, f1.readline().split())))
            liste_j=[]
            for j in range (J):
                liste_j.append(list(map(int, f1.readline().split())))
            liste_cij.append(liste_j)
        


    liste_solution_I=[]#matrice 2d des sites et de la periode ou ils sont construits
    liste_solution_J=[]#matrice 2d des usagers et de quand ils sont affectés


    with open(chemin_fichier_solution, 'r') as fs:
        cout_tot0=int(fs.readline())
        for r in range(I):
            
            liste_solution_I.append(list(map(int,fs.readline().split())))
            if r+1!=liste_solution_I[r][0]:
                print("les sites ne sont pas dans le bon ordre")
                return -1
        for q in range (J):

            liste_solution_J.append(list(map(int,fs.readline().split())))
            if liste_solution_J[q][0]!=q+1:
                print("les usagers ne sont pas dans le bon ordre")
                return -1
        
        #verification que le nombre de sites est respecté par an

        verif_pt=[0]*(T+1)
        for i in range(I):
            
            verif_pt[liste_solution_I[i][1]]+=1
        
        for i in range (T):
                if verif_pt[i+1]!=liste_pt[i]:
                    print("le nombre de sites a la periode :", i+1,"n'est pas respecté")
                    return -1
                
        #verification que le nombre d'usager est respecté par an

        verif_nt=[0]*(T+1)
        for i in range(J):
            if liste_solution_J[i][1]==0:
                print("les usagées :", i+1, "ne sont jamais affectées")
                return -1
            verif_nt[liste_solution_J[i][1]]+=1
        compteur_j=0
        for i in range (T):
            
            compteur_j+=verif_nt[i+1]
            if compteur_j < liste_nt[i]:
                print("le nombre d'affectation a la periode :", i+1, "n'est pas respectée")
                return -1
            
       #verification que le cout renvoyée correspond bien a la solution          
        cout_tot=0
        site_utilisés=set()
        for i in range(I):

            if not liste_solution_I[i][0] in site_utilisés:
                site_utilisés.add(liste_solution_I[i][0])
            else:
                print(f"le site {i+1} à deja été construit")
                return -1 
            

            année=liste_solution_I[i][1]
            if année!=0:
                cout_tot+=liste_fi[i][année-1]

    for i in range(J):
        dbt_af=liste_solution_J[i][1]
        for j in range(dbt_af-1,T):
            
            cout_tot+=minimum_cout_site_ouverts(liste_cij,i,j,liste_solution_I,I)
    
    if cout_tot!=cout_tot0:
        return -1
    
    return cout_tot

    



def minimum_cout_site_ouverts(l,u,n,L,I):
    min=float('inf')
    for i in range(I):
        if l[i][u][n]<min and L[i][1]<=n+1 and L[i][1]!=0:
            min=l[i][u][n]
    return min