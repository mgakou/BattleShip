# -*- coding: utf-8 -*-
#### ---- Importation des modules du projet

# Prise en charge de séléction aléatoire
import os
import json
from random import randint
import ihm

#### ---- Initalisation des variables global

global gameMode
global mapSize
global mapNumber
global gameDataBoat
global atqDone
global ennemieMapSelect

#### ---- Affectation des variables global

# Paramètre de party
mapData = []
atqHistory = []
boatData = []
boatGuiData = []
playerDeathData = []
tmpAtqDone = []
inGame = False
ennemieMapSelect = 2

playerMapSelect = 1
gameMode = 0
testAddBoat = 0
lastBuildBoat = ""
atqDone = False
allAtqDone = False

# Preset de partie
mapSize = 10
mapNumber = 3
adversAtqAdvers = True
gameDataBoat = ["a","c","f","s","p"]
cooldown = 1
strikerMap = 1

def loadGamePreset():
    global mapSize
    global adversAtqAdvers
    global gameDataBoat
    global cooldown 
    global mapNumber
    global strikerMap
    if gameMode == 0:
        mapSize = 10
        mapNumber = 2
        adversAtqAdvers = True
        gameDataBoat = ["a","c","f","s","p"]
        cooldown = 1.5
        strikerMap = 1
    if gameMode == 1:
        mapSize = 12
        mapNumber = 3
        adversAtqAdvers = True
        gameDataBoat.clear()
        gameDataBoat = ["a","a","c","c","c","f","f","f","f","s","s"]
        cooldown = 1.5
        strikerMap = 1
    if gameMode == 2:
        mapSize = 4
        mapNumber = 4
        adversAtqAdvers = True
        gameDataBoat.clear()
        gameDataBoat = ["s"]
        cooldown = 1
        strikerMap = 1
    if gameMode == 3:
        mapSize = 15
        mapNumber = 10
        adversAtqAdvers = False
        gameDataBoat.clear()
        gameDataBoat = ["a","f","f","f"]
        cooldown = 0.5
        strikerMap = 2

#### ---- Interaction utilisateur

def laucheGame():
    global inGame
    global ennemieMapSelect
    global atqDone
    global allAtqDone
    for i in range(mapNumber):
        if i != playerMapSelect:
            creatRandomMap(i)
    inGame = True
    atqDone = False
    allAtqDone = False
    tmpAtqDone.clear()
    if playerMapSelect != 1:
        ennemieMapSelect = 1
        ihm.textMaster.config(text=ihm.lg("Le joueur {} exécute ses tirs.").format(strikerMap),fg="grey")
        ihm.app.after(2000,ihm.refreshToure)

    else:
        ennemieMapSelect = 2
        ihm.textMaster.config(text=ihm.lg("Veuillez exécuter vos tirs sur chaque flotte adverse."),fg="black")
        ihm.refreshToure()


    ihm.switch(ihm.partyPage)

def stopGame():
    global inGame 
    inGame = False
    ihm.buttonSound(3)
    ihm.switch(ihm.mainMenuPage)

# Attaquer une position ennemie
def addBoat(map,type,x,y,direction):
    global lastBuildBoat
    initialX = x
    initialY = y
    if type == "a":
        size = 4
    if type == "c":
        size = 3
    if type == "f":
        size = 2
    if type == "s":
        size = 2
    if type == "p":
        size = 1
    if direction == "N":
        x2 = x
        y2 = y + size//2
        y -= size//2 + int(size%2)
    elif direction == "S":
        x2 = x
        y2 = y + size//2 + int(size%2)
        y -= size//2
    elif direction == "W":
        x2 = x + size//2
        x -= size//2 + int(size%2)
        y2 = y 
    else:
        x2 = x + size//2 + int(size%2)
        y2 = y
        x -= size//2
    noBoat = 1
    if x>0 and x2<mapSize+1 and y>0 and y2<mapSize+1:
        for i in range(x,x2+1):
            for j in range(y,y2+1):
                if mapRead(map,i,j)[0] != "--":
                    noBoat = 0
        if not type in boatData[map-1] and noBoat:
            occurence = 0
            while type+str(occurence) in boatData[map-1]:
                occurence += 1
            if type+str(occurence) not in boatData[map-1]:
                mapZoneModifType(map,type+str(occurence),x,y,x2,y2)
                boatData[map-1] += [type+str(occurence)]
                lastBuildBoat = type+str(occurence)
                boatGuiData[map-1].append([type+str(occurence),initialX,initialY,direction])

def removeBoat(map,type):
    mapZoneModifType(map,"--",BoatReadPos(map,type)[1],BoatReadPos(map,type)[2],BoatReadPos(map,type)[3],BoatReadPos(map,type)[4])
    boatData[map-1].remove(type)
    for boat in range(len(boatGuiData[map-1])):
        if boatGuiData[map-1][boat][0] == type:
            del boatGuiData[map-1][boat]
            break

# --- Attaque d'un joueur
def atq(user,map,posX,posY):
    global atqDone
    global allAtqDone
    type = mapRead(map,posX,posY)[0]

    # Effet réaliser sur le GUI selon le typoe de la case
    if mapRead(map,posX,posY)[0] != "--" and (map == ennemieMapSelect or map == playerMapSelect):
        ihm.shake(0.2)
        ihm.magicsound.magicsound("gui/sound/Explosion/explosion{}.mp3".format(randint(1,3)),block = False)
    if mapRead(map,posX,posY)[0] == "--":
        ihm.magicsound.magicsound("gui/sound/Water/Splash{}.mp3".format(randint(1,6)),block = False)

    if mapData[map-1][posY-1][posX-1][1] != "DD" and mapData[map-1][posY-1][posX-1][1] == "--":
        mapData[map-1][posY-1][posX-1][1] = "X"+str(user)
        tmpAtqDone.append(map)
        atqDone = True
        ihm.refreshGUImap()
        if len(tmpAtqDone) == playerDeathData.count(False) -1:
            allAtqDone = True

    if not [posX,posY,type,mapRead(map,posX,posY)[1]] in atqHistory[user-1][map-1]:
        atqHistory[user-1][map-1] += [[posX,posY,type,mapRead(map,posX,posY)[1]]]
    # Rafraichissement des touchés-coulés
    for map in range(len(mapData)):
        totalBoatDeath = 0
        for boat in range(len(boatData[map])):
            counter = 0
            for x in range(len(mapData[map])):
                for y in range(len(mapData[map][x])):
                    if boatData[map][boat] == mapRead(map+1,x,y)[0] and (mapRead(map+1,x,y)[1][0] == "X" or mapRead(map+1,x,y)[1] == "DD"):
                        counter += 1
            if counter >= BoatReadPos(map+1,boatData[map][boat])[0]:
                mapZoneModifStatus(map+1,"DD",BoatReadPos(map+1,boatData[map][boat])[1],BoatReadPos(map+1,boatData[map][boat])[2],BoatReadPos(map+1,boatData[map][boat])[3],BoatReadPos(map+1,boatData[map][boat])[4])
                totalBoatDeath += 1
        if totalBoatDeath >= len(gameDataBoat):
            playerDeathData[map] = True
    
#### ---- Manipulation des maps

# Création des maps
def creatmap():
    global testAddBoat
    loadGamePreset()
    testAddBoat = 0
    mapData.clear()
    atqHistory.clear()
    boatData.clear()
    boatGuiData.clear()
    playerDeathData.clear()
    for i in range(mapNumber):
        mapData.append([])
        atqHistory .append([])
        boatData.append([])
        boatGuiData.append([])
        playerDeathData.append(False)
        for i2 in range(mapNumber):
            atqHistory[i] += [[]]
        for j in range(mapSize):
            mapData[i] += [[]*mapSize]
            for k in range(mapSize):
                mapData[i][j] += [["--","--"]]

# Lire une position
def mapRead(map,posX,posY):
    return mapData[map-1][posY-1][posX-1]

# Modifier le type d"une position
def mapPosModifType(map,modiftype,posX,posY):
    mapData[map-1][posY-1][posX-1][0] = modiftype

# Modifier le status d"une position
def mapPosModifStatus(map,modifstatus,posX,posY):
    mapData[map-1][posY-1][posX-1][1] = modifstatus

# Obtenire les positions de zone d"un élément
def BoatReadPos(map,type):
    pos = [0]
    for i in range(len(mapData[map-1])):
        for j in range(len(mapData[map-1][i])):
            if mapData[map-1][i][j][0] == type:
                pos += j+1,i+1
                pos[0] += 1
    if len(pos) >= 5:
        pos = [pos[0],pos[1],pos[2],pos[-2],pos[-1]]
    return pos

# Modifier le type d"une zone
def mapZoneModifType(map,modiftype,posX1,posY1,posX2,posY2):
    if posX2>posX1:
        for i in range(posX2-posX1+1):
            if posY2>posY1:
                for j in range(posY2-posY1+1):
                    mapPosModifType(map,modiftype,posX1+i,posY1+j)
            else:
                for j in range(posY1-posY2+1):
                    mapPosModifType(map,modiftype,posX1+i,posY2+j)   
    else:
        for i in range(posX1-posX2+1):
            if posY2>posY1:
                for j in range(posY2-posY1+1):
                    mapPosModifType(map,modiftype,posX2+i,posY1+j)
            else:
                for j in range(posY1-posY2+1):
                    mapPosModifType(map,modiftype,posX2+i,posY2+j)  

# Modifier le status d"une zone
def mapZoneModifStatus(map,modifstatus,posX1,posY1,posX2,posY2):
    if posX2>posX1:
        for i in range(posX2-posX1+1):
            if posY2>posY1:
                for j in range(posY2-posY1+1):
                    mapPosModifStatus(map,modifstatus,posX1+i,posY1+j)
            else:
                for j in range(posY1-posY2+1):
                    mapPosModifStatus(map,modifstatus,posX1+i,posY2+j)   
    else:
        for i in range(posX1-posX2+1):
            if posY2>posY1:
                for j in range(posY2-posY1+1):
                    mapPosModifStatus(map,modifstatus,posX2+i,posY1+j)
            else:
                for j in range(posY1-posY2+1):
                    mapPosModifStatus(map,modifstatus,posX2+i,posY2+j)  
                    
# Compte le nombre de fois qu'un type de bateau est présent dans une map
def boatDataTypeCount(type,map):
    count = 0
    for i in range(len(boatData[map-1])):
        if boatData[playerMapSelect-1][i][0] == type:
            count += 1
    return count

# Générer une map aléatoirement
def creatRandomMap(map):
    direction = "NSEW"
    testAddBoat = 0
    while testAddBoat < len(gameDataBoat):
        addBoat(map,gameDataBoat[testAddBoat],randint(1,mapSize),randint(1,mapSize),direction[randint(0,3)])
        if testAddBoat < len(boatData[map-1]):
            testAddBoat += 1

# Prise de décision par l'IA de niveau 1
def IaAtq(map,atqMap):
    focus = False
    atqX = randint(1,mapSize)
    atqY = randint(1,mapSize)
    # Focus une position touché il y en à une dans la carte à attaquer sinon choisi un position aléatoire
    for x in range(1,mapSize+1):
        for y in range(1,mapSize+1):
            if mapRead(atqMap,x,y)[1][0] == "X" and mapRead(atqMap,x,y)[0] != "--":
                focus = True
                initialX = x
                initialY = y
                break
        if mapRead(atqMap,x,y)[1][0] == "X" and mapRead(atqMap,x,y)[0] != "--":
            break

    if focus:                     
        # Si il n'y à rien à côté, fait une croix jusqu'a trouver la position voisine
        N=["OO","OO"];E=["OO","OO"];S=["OO","OO"];W=["OO","OO"]
        atqX = initialX
        atqY = initialY
        HdirectionTest = False
        VdirectionTest = False

        if initialY - 1 > 0:
            N = mapRead(atqMap,initialX,initialY-1)
                
        if initialX + 1 <= mapSize:
            E = mapRead(atqMap,initialX+1,initialY)

        if initialY + 1 <= mapSize:
            S = mapRead(atqMap,initialX,initialY+1)

        if initialX - 1 > 0:
            W = mapRead(atqMap,initialX-1,initialY)
        
        if (N[0] != "--" and N[1][0] == "X") or (S[0] != "--" and S[1][0] == "X"):
            HdirectionTest = False
            VdirectionTest = True
            # print("Il y à un truc à la verticale")
        elif (E[0] != "--" and E[1][0] == "X") or (W[0] != "--" and W[1][0] == "X"):
            HdirectionTest = True
            VdirectionTest = False
            # print("Il y à un truc à l'horizontale")

        if not HdirectionTest and not VdirectionTest:
            while mapRead(atqMap,atqX,atqY)[1] != "--":
                atqX = initialX
                atqY = initialY
                direction = randint(0,3)
                if direction == 0 and N[1] == "--":
                    atqY -= 1
                elif direction == 1 and E[1] == "--":
                    atqX += 1
                elif direction == 2 and S[1] == "--":
                    atqY += 1
                elif direction == 3 and W[1] == "--":
                    atqX -= 1
        else:
            Succes = False
            direction = randint(0,1)
            while not Succes:
                # Sur les bateaux détecté à l'horizontale
                if HdirectionTest:
                    # print("C'est partie pour tester l'horizontale")
                    horizontaleOk = True
                    while HdirectionTest: # Tant qu'une position non touché n'a pas été trouvé il recommence
                        if not atqX > 0 or not atqX < mapSize + 1: # Si la position testé est hors zone, alors il test une autre direction
                            # print("bon je vais checher de l'autre côté c'est la limite en",lettre[atqY-1],atqX)
                            if direction == 0:
                                direction = 1
                            else:
                                direction = 0
                            atqX = initialX
                            atqY = initialY
                            if horizontaleOk == False:
                                HdirectionTest = False
                                VdirectionTest = True
                                # print("Je suis piégé à l'horizontale, je teste la verticale")
                            else:
                                horizontaleOk = False

                        elif mapRead(atqMap,atqX,atqY)[1] == "--":
                            # print("j'ai trouvé, c'est",lettre[atqY-1],atqX)
                            Succes = True
                            break

                        elif mapRead(atqMap,atqX,atqY)[1][0] == "X" and mapRead(atqMap,atqX,atqY)[0] != "--": # Si la position testé est un bateau touché, alors il avance avance dans la direction choisie la position testé
                            # print("bon j'avance en",lettre[atqY-1],atqX)
                            if direction == 0:
                                atqX -= 1
                            else:
                                atqX += 1

                        elif (mapRead(atqMap,atqX,atqY)[1][0] == "X" or mapRead(atqMap,atqX,atqY)[1] == "DD"): # Si la position testé est de l'eau ou un bateau coulé, alors il test une autre direction
                            # print("bon je vais changer de côté, c'est le bord içi")
                            if direction == 0:
                                direction = 1
                            else:
                                direction = 0
                            atqX = initialX
                            atqY = initialY
                            if horizontaleOk == False:
                                HdirectionTest = False
                                VdirectionTest = True
                                # print("Je suis piégé à l'horizontale, je teste la verticale")
                            else:
                                horizontaleOk = False

                # Sur les bateaux détecté à la verticale      
                if VdirectionTest:         
                    verticaleOk = True
                    # print("C'est partie pour tester la verticale")
                    while VdirectionTest: # Tant qu'une position non touché n'a pas été trouvé il recommence
                        if not atqY > 0 or not atqY < mapSize + 1: # Si la position testé est hors zone, alors il test une autre direction
                            # print("bon je vais checher de l'autre côté c'est la limite en",lettre[atqY-1],atqX)
                            if direction == 0:
                                direction = 1
                            else:
                                direction = 0
                            atqX = initialX
                            atqY = initialY
                            if verticaleOk == False:
                                HdirectionTest = True
                                VdirectionTest = False
                                # print("Je suis piégé à la verticale, je teste l'horizontale")
                            else:
                                verticaleOk = False

                        elif mapRead(atqMap,atqX,atqY)[1] == "--":
                            # print("j'ai trouvé, c'est",lettre[atqY-1],atqX)
                            Succes = True
                            break

                        elif mapRead(atqMap,atqX,atqY)[1][0] == "X" and mapRead(atqMap,atqX,atqY)[0] != "--": # Si la position testé est un bateau touché, alors il avance avance dans la direction choisie la position testé
                            # print("bon j'avance en",lettre[atqY-1],atqX)
                            if direction == 0:
                                atqY -= 1
                            else:
                                atqY += 1

                        elif (mapRead(atqMap,atqX,atqY)[1][0] == "X" or mapRead(atqMap,atqX,atqY)[1] == "DD"): # Si la position testé est de l'eau ou un bateau coulé, alors il test une autre direction
                            # print("bon je vais changer de côté, c'est le bord içi")
                            if direction == 0:
                                direction = 1
                            else:
                                direction = 0
                            atqX = initialX
                            atqY = initialY
                            if verticaleOk == False:
                                HdirectionTest = True
                                VdirectionTest = False
                                # print("Je suis piégé à la verticale, je teste l'horizontale")
                            else:
                                verticaleOk = False
                if Succes:
                    break


    if mapRead(atqMap,atqX,atqY)[1] != "--": # Tire aléatoire si par une "rare erreur non trouvé"
        while mapRead(atqMap,atqX,atqY)[1] != "--":
            atqX = randint(1,mapSize)
            atqY = randint(1,mapSize)

    # print("atq",lettre[atqY-1],atqX)
    atq(map,atqMap,atqX,atqY)

def ennemiPlay(striker):
    global allAtqDone
    if adversAtqAdvers:
        if adversAtqAdvers:
            for map in range(playerDeathData.count(False)):
                if striker != map+1:
                        IaAtq(striker,map+1)
    elif not adversAtqAdvers:
        IaAtq(striker,playerMapSelect)
        allAtqDone = True


def loadSettings():
    with open("usersettings.json", 'r') as file:
        settings = json.load(file)

    ihm.lang = settings.get("settings").get("lang")
    ihm.fullScreen = settings.get("settings").get("fullScreen")
    ihm.W = settings.get("settings").get("W")
    ihm.H = settings.get("settings").get("H")
    ihm.Hz = settings.get("settings").get("Hz")
    ihm.shakeIntensity = settings.get("settings").get("shakeIntensity")
    ihm.showLetter = settings.get("settings").get("showLetter")
    ihm.inversLetter = settings.get("settings").get("inversLetter")
    ihm.mainVolume = settings.get("settings").get("mainVolume")
    ihm.musicVolume = settings.get("settings").get("musicVolume")
    ihm.effectVolume = settings.get("settings").get("effectVolume")

    ihm.app.attributes("-fullscreen", ihm.fullScreen)

def applySettings():
    ihm.app.attributes("-fullscreen", ihm.fullScreen)
    if ihm.restart:
        ihm.app.destroy()
        os.system("python controller.py")

def saveSettings():
    settings ={
    "settings" : {
        "lang": ihm.lang,
        "fullScreen": ihm.fullScreen,
        "W": ihm.W,
        "H": ihm.H,
        "Hz": ihm.Hz,
        "shakeIntensity": ihm.shakeIntensity,
        "showLetter": ihm.showLetter,
        "inversLetter": ihm.inversLetter,
        "mainVolume": ihm.mainVolume,
        "musicVolume": ihm.musicVolume,
        "effectVolume": ihm.effectVolume
        }
    }

    with open("usersettings.json", 'w') as file:
        json.dump(settings, file)