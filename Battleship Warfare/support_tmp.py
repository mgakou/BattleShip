

# Affichage d'une grille
def printTab(M):
    w=[max([len(str(M[i][j])) for i in range(len(M))]) for j in range(len(M[0]))]
    for i in range(len(M)):
        for j in range(len(M[0])):
            print("%*s" %(w[j],str(M[i][j])), end= ' ')
        print()

# Affichage horizontal des données maps
def printMapData(mapData):
    printer = "\n"
    for i in range(len(mapData)):
        printer += "          Données de la Carte "+str(i+1)+"             "
    printer += "\n\n"
    for j in range(len(mapData[0])):
        for i in range(len(mapData)):
            printer += " "
            for l in range(len(mapData[i][j])): 
                printer += str(mapData[i][j][l][0])+str(mapData[i][j][l][1])+" "
            printer += "   "
        printer += "\n"
    print(printer)

# Affichage vertical des données maps
def printMapDataV(mapData):
    printer = ""
    for i in range(len(mapData)):
        printer += "\n  Données de la Carte "+str(i+1)+"\n\n"
        for j in range(len(mapData[i])):
            printer += "  "
            for k in range(len(mapData[i][j])):
                printer += str(mapData[i][j][k][0].upper())+str(mapData[i][j][k][1])+" "
            printer += "\n"
    print(printer)

# Affichage vertical de la grilles des adversaires vu utilisateur 
def printAdversMapV(adversMapData):
    printer = "\n"
    abc = "ABCDEFGHIJ"
    for i in range(len(adversMapData)):
        printer += "Position connu du joueur "+str(i+1)+":\n"
        for j in range(len(adversMapData[i])):
            if j != i:
                printer += " - Chez le joueur "+str(j+1)+":  "
                for k in range(len(adversMapData[i][j])):
                    printer += str(abc[adversMapData[i][j][k][0]])+str(adversMapData[i][j][k][1])+" "
                    if adversMapData[i][j][k][2] != "--":
                        printer += "touché, "
                    else:
                        printer +=  "à l'eau, "
                printer += "\n"
    print(printer)