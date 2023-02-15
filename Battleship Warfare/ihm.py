# -*- coding: utf-8 -*-

# --- Importation des bibliothèque

# Imporations des données
from data import *
import data as d

# Gestion des interfaces graphiques
from tkinter import *
from tkinter import messagebox 
import tkinter as tk

# Customisation des widgets
from tkinter import ttk

# Gestion des polices
from tkinter.font import *
import tkinter.font as tkFont

# Gestion des images
try: # Teste l'importation du module PIL
    from PIL import ImageTk, Image
except: # install le module s'il n'est pas présent
    os.system("python -m pip uninstall pil")
    os.system("python -m pip install pillow")
    from PIL import ImageTk, Image

# Gestion des son
try: # Teste l'importation du module magicsound
    import magicsound
except: # install le module s'il n'est pas présent
    os.system("python -m pip install magicsound")
    import magicsound

from time import sleep

# --- Affectation des variables
def appinit():
    global app
    app = tk.Tk()

appinit()

globalSize = 1
buildBoatDirection = 1
buildBoatSelected = ""
mouseX = 0 
mousY = 0
inBuildMap = False
inEnnemieMap = False
shakeTime = 2
shakeWindow = False
page = ""
restart = False
fps = 0
oneS = False
menuTitleText = False
windowResize = False

# --- Réglage
with open("usersettings.json", 'r') as file:
    settings = json.load(file)

lang = 0
fullScreen = False
W  = 800
H = 450
Hz = 30
shakeIntensity = 4
showLetter = True
inversLetter = False
mainVolume = 100
musicVolume = 100
effectVolume = 100

# Application de langue du jeu
country = ["EN","FR","DE","ES","PT","JP","KR","CN"]
with open("gui/lang/{}.txt".format(country[lang]), "r", encoding='utf-8') as lgFile:
    langFile = lgFile.readlines()

# --- y
window = Frame(app)
startPage = Canvas(window,bg="black",cursor="none")
mainMenuPage = Canvas(window)
selectPartyPage = Frame(window)
gameSettingsPage = Frame(window)
prePartyPage = Frame(window)
partyPage = Frame(window)
settingsPage = Frame(window)
creditsPage = Frame(window)

# --- Style du text
titleStyle = tkFont.Font(family="Impact")
default_font = nametofont("TkDefaultFont")

# --- Musique

# Fonction d'action de fenêtre
def switch(frame):
    global page
    global backPage
    for widget in window.winfo_children():
        widget.place_forget()
    window.place(relx=0.5,x=0,rely=0.5,y=0,relheight=1,relwidth=1,anchor=CENTER)
    frame.place(relx=0.5,rely=0.5,relheight=1,relwidth=1,anchor=CENTER)
    backPage = page
    page = frame
    refreshAllGUI()
    app.update()
    refreshGUImap()

# --- Gestion des images

# Écran de démarage
img_Start_Screen_Source = Image.open("gui/image/Screen/Start_Screen.png")
img_Start_Screen = ImageTk.PhotoImage(img_Start_Screen_Source.resize((int((800*globalSize)),int((450*globalSize))), Image.ANTIALIAS))

# Titre du menu
img_Title_Source = Image.open("gui/image/Title.png")

# Porte avion
img_Aboat_N_Source = Image.open("gui/image/Aboat/Aboat_N.png"); img_Aboat_E_Source = Image.open("gui/image/Aboat/Aboat_E.png"); img_Aboat_S_Source = Image.open("gui/image/Aboat/Aboat_S.png"); img_Aboat_W_Source = Image.open("gui/image/Aboat/Aboat_W.png")
# Cuirrasé
img_Cboat_N_Source = Image.open("gui/image/Cboat/Cboat_N.png"); img_Cboat_E_Source = Image.open("gui/image/Cboat/Cboat_E.png"); img_Cboat_S_Source = Image.open("gui/image/Cboat/Cboat_S.png"); img_Cboat_W_Source = Image.open("gui/image/Cboat/Cboat_W.png")
# Frégate
img_Fboat_N_Source = Image.open("gui/image/Fboat/Fboat_N.png"); img_Fboat_E_Source = Image.open("gui/image/Fboat/Fboat_E.png"); img_Fboat_S_Source = Image.open("gui/image/Fboat/Fboat_S.png"); img_Fboat_W_Source = Image.open("gui/image/Fboat/Fboat_W.png")
# Sous-marin
img_Sboat_N_Source = Image.open("gui/image/Sboat/Sboat_N.png"); img_Sboat_E_Source = Image.open("gui/image/Sboat/Sboat_E.png"); img_Sboat_S_Source = Image.open("gui/image/Sboat/Sboat_S.png"); img_Sboat_W_Source = Image.open("gui/image/Sboat/Sboat_W.png")
# Patrouilleur
img_Pboat_N_Source = Image.open("gui/image/Pboat/Pboat_N.png"); img_Pboat_E_Source = Image.open("gui/image/Pboat/Pboat_E.png"); img_Pboat_S_Source = Image.open("gui/image/Pboat/Pboat_S.png"); img_Pboat_W_Source = Image.open("gui/image/Pboat/Pboat_W.png")

# Case touché
img_X_Source = Image.open("gui/image/Status/X.png")
# Case coulé
img_D_Source = Image.open("gui/image/Status/D.png")

# --- Rafraichissement de la taille des images (toute les secondes)
def refreshIMG():
    if page == startPage: # Affichage uniquement quand nécaissaire par soucis de performance
        global img_Start_Screen # Écran de démarage
        img_Start_Screen = ImageTk.PhotoImage(img_Start_Screen_Source.resize((int((800*globalSize)),int((450*globalSize))), Image.ANTIALIAS))

    if page == partyPage or page == prePartyPage: # Affichage uniquement quand nécaissaire par soucis de performance

        global img_X
        img_X = ImageTk.PhotoImage(img_X_Source.resize((int((200//7*globalSize)/(d.mapSize/10)),int((200//7*globalSize)/(d.mapSize/10))), Image.ANTIALIAS))
        global img_D
        img_D = ImageTk.PhotoImage(img_D_Source.resize((int((200//7*globalSize)/(d.mapSize/10)),int((200//7*globalSize)/(d.mapSize/10))), Image.ANTIALIAS))

        # Porte avion
        global img_Aboat_N; global img_Aboat_E; global img_Aboat_S; global img_Aboat_W
        img_Aboat_N = ImageTk.PhotoImage(img_Aboat_N_Source.resize((int((200//7*globalSize)/(d.mapSize/10)),int((1000//7*globalSize)/(d.mapSize/10))), Image.ANTIALIAS)); img_Aboat_E = ImageTk.PhotoImage(img_Aboat_E_Source.resize((int((1000/7*globalSize)/(d.mapSize/10)),int((200/7*globalSize)/(d.mapSize/10))), Image.ANTIALIAS)); img_Aboat_S = ImageTk.PhotoImage(img_Aboat_S_Source.resize((int((200//7*globalSize)/(d.mapSize/10)),int((1000//7*globalSize)/(d.mapSize/10))), Image.ANTIALIAS)); img_Aboat_W = ImageTk.PhotoImage(img_Aboat_W_Source.resize((int((1000//7*globalSize)/(d.mapSize/10)),int((200//7*globalSize)/(d.mapSize/10))), Image.ANTIALIAS))    
        # Cuirrasé 
        global img_Cboat_N; global img_Cboat_E ;global img_Cboat_S; global img_Cboat_W
        img_Cboat_N = ImageTk.PhotoImage(img_Cboat_N_Source.resize((int((200//7*globalSize)/(d.mapSize/10)),int((800//7*globalSize)/(d.mapSize/10))), Image.ANTIALIAS)); img_Cboat_E = ImageTk.PhotoImage(img_Cboat_E_Source.resize((int((800//7*globalSize)/(d.mapSize/10)),int((200//7*globalSize)/(d.mapSize/10))), Image.ANTIALIAS)); img_Cboat_S = ImageTk.PhotoImage(img_Cboat_S_Source.resize((int((200//7*globalSize)/(d.mapSize/10)),int((800//7*globalSize)/(d.mapSize/10))), Image.ANTIALIAS)); img_Cboat_W = ImageTk.PhotoImage(img_Cboat_W_Source.resize((int((800//7*globalSize)/(d.mapSize/10)),int((200//7*globalSize)/(d.mapSize/10))), Image.ANTIALIAS))    
        # Frégate
        global img_Fboat_N; global img_Fboat_E; global img_Fboat_S; global img_Fboat_W
        img_Fboat_N = ImageTk.PhotoImage(img_Fboat_N_Source.resize((int((200//7*globalSize)/(d.mapSize/10)),int((600//7*globalSize)/(d.mapSize/10))), Image.ANTIALIAS)); img_Fboat_E = ImageTk.PhotoImage(img_Fboat_E_Source.resize((int((600//7*globalSize)/(d.mapSize/10)),int((200//7*globalSize)/(d.mapSize/10))), Image.ANTIALIAS)); img_Fboat_S = ImageTk.PhotoImage(img_Fboat_S_Source.resize((int((200//7*globalSize)/(d.mapSize/10)),int((600//7*globalSize)/(d.mapSize/10))), Image.ANTIALIAS)); img_Fboat_W = ImageTk.PhotoImage(img_Fboat_W_Source.resize((int((600//7*globalSize)/(d.mapSize/10)),int((200//7*globalSize)/(d.mapSize/10))), Image.ANTIALIAS))    
        # Sous-marin
        global img_Sboat_N; global img_Sboat_E; global img_Sboat_S; global img_Sboat_W
        img_Sboat_N = ImageTk.PhotoImage(img_Sboat_N_Source.resize((int((200//7*globalSize)/(d.mapSize/10)),int((600//7*globalSize)/(d.mapSize/10))), Image.ANTIALIAS)); img_Sboat_E = ImageTk.PhotoImage(img_Sboat_E_Source.resize((int((600//7*globalSize)/(d.mapSize/10)),int((200//7*globalSize)/(d.mapSize/10))), Image.ANTIALIAS)); img_Sboat_S = ImageTk.PhotoImage(img_Sboat_S_Source.resize((int((200//7*globalSize)/(d.mapSize/10)),int((600//7*globalSize)/(d.mapSize/10))), Image.ANTIALIAS)); img_Sboat_W = ImageTk.PhotoImage(img_Sboat_W_Source.resize((int((600//7*globalSize)/(d.mapSize/10)),int((200//7*globalSize)/(d.mapSize/10))), Image.ANTIALIAS))
        # Patrouilleur
        global img_Pboat_N; global img_Pboat_E; global img_Pboat_S; global img_Pboat_W
        img_Pboat_N = ImageTk.PhotoImage(img_Pboat_N_Source.resize((int((200//7*globalSize)/(d.mapSize/10)),int((400//7*globalSize)/(d.mapSize/10))), Image.ANTIALIAS)); img_Pboat_E = ImageTk.PhotoImage(img_Pboat_E_Source.resize((int((400//7*globalSize)/(d.mapSize/10)),int((200//7*globalSize)/(d.mapSize/10))), Image.ANTIALIAS)); img_Pboat_S = ImageTk.PhotoImage(img_Pboat_S_Source.resize((int((200//7*globalSize)/(d.mapSize/10)),int((400//7*globalSize)/(d.mapSize/10))), Image.ANTIALIAS)); img_Pboat_W = ImageTk.PhotoImage(img_Pboat_W_Source.resize((int((400//7*globalSize)/(d.mapSize/10)),int((200//7*globalSize)/(d.mapSize/10))), Image.ANTIALIAS))

#  --- Trouveur de l'image correspondante à un type de bateau et sa direction
def finfBoatImg(type,direction):
    orientation = "NESW"
    typeList = "acfsp"
    imgName = ["img_Aboat","img_Cboat","img_Fboat","img_Sboat","img_Pboat"]
    if not isinstance(direction, int):
        direction = orientation.index(direction) 
    return globals()[imgName[typeList.index(type)]+"_"+orientation[direction]]
### --- Action de boutton --- ###

def closeApp(): 
    if d.inGame:
        if messagebox.askokcancel(lg("Battleship Warfare Alert"), lg("Êtes-vous sûr de vouloir quitter le jeu ?")): 
            app.destroy()
    else:
        app.destroy()

def leaveGame():
    if d.inGame:
        if messagebox.askokcancel(lg("Battleship Warfare Alert"), lg("Êtes-vous sûr de vouloir abandonner ?")): 
            d.stopGame()
    else:
        d.stopGame()

def FPSloop():
    global fps
    global Hz
    fps = 0
    app.after(1000,FPSloop)

# Redimentionnement

def setFullScreen():
    global fullScreen
    global globalSize
    if fullScreen :
        fullScreen = False
    else:
        fullScreen = True
    app.attributes("-fullscreen", fullScreen) 
    globalSize = 1 + (app.winfo_height() - 450)*(app.winfo_width() - 800)*0.0000025
    refreshGUI()
    refreshGUImap()

def buttonSound(sound):
    try:
        magicsound.magicsound("gui/sound/Button/Click{}.mp3".format(sound),block = False)
    except:
        magicsound.magicsound("gui/sound/Button/Click{}.wav".format(sound),block = False)

def changeGameMode():
    d.gameMode += 1
    if d.gameMode > 3:
        d.gameMode = 0

def changeLang():
    global lang
    lang += 1
    if lang > 7:
        lang = 0

# Selection de la map adverse visible
def nextEnnemieMap(select):
    if select and d.ennemieMapSelect + 1 == d.playerMapSelect:
        d.ennemieMapSelect += 2
    elif select:
        d.ennemieMapSelect += 1
    elif not select and d.ennemieMapSelect - 1 == d.playerMapSelect:
        d.ennemieMapSelect -= 2
    else:
        d.ennemieMapSelect -= 1

    if d.ennemieMapSelect > d.mapNumber:
        d.ennemieMapSelect = d.mapNumber
        if d.ennemieMapSelect == d.playerMapSelect:
            d.ennemieMapSelect -= 1
    elif d.ennemieMapSelect < 1:
        d.ennemieMapSelect = 1
        if d.ennemieMapSelect == d.playerMapSelect:
            d.ennemieMapSelect += 1
    refreshGUI()
    refreshGUImap()

def refreshToure():
    if d.inGame:
        # A un autre joueur de jouer
        if d.allAtqDone:        
            d.allAtqDone = False
            d.atqDone = False
            d.tmpAtqDone.clear()
            if d.strikerMap != d.playerMapSelect:
                try:
                    magicsound.magicsound("gui/sound/Beep/beep{}.wav".format(randint(1,6)),block = False)
                except:
                    magicsound.magicsound("gui/sound/Beep/beep{}.mp3".format(randint(1,3)),block = False)

            if d.strikerMap < d.mapNumber:
                d.strikerMap += 1
            else:
                d.strikerMap = 1

            if d.strikerMap != d.playerMapSelect and not d.playerDeathData[d.strikerMap-1]:
                textMaster.config(text=lg("Le joueur {} exécute ses tirs.").format(d.strikerMap),fg="grey")
                app.after(int(d.cooldown*500),refreshToure)

            elif d.strikerMap == d.playerMapSelect and not d.playerDeathData[d.strikerMap-1]:
                if d.mapNumber > 2:
                    textMaster.config(text=lg("Veuillez exécuter vos tirs sur chaque flotte adverse."),fg="black")
                else:
                    textMaster.config(text=lg("Veuillez exécuter vos tirs sur la flotte adverse."),fg="black")
                refreshToure()

        # Au toure d'un adversaire
        elif d.strikerMap != d.playerMapSelect and not d.playerDeathData[d.strikerMap-1]:
            ennemiPlay(d.strikerMap)
            app.after(int(d.cooldown*500),refreshToure)

        elif d.strikerMap != d.playerMapSelect and d.playerDeathData[d.strikerMap-1]:
            d.allAtqDone = True
            refreshToure()

        # Au toure de l'utilisateur    
        elif d.strikerMap == d.playerMapSelect and not d.playerDeathData[d.strikerMap-1]:
            d.allAtqDone = False
            d.atqDone = False

        refreshGUI()

    if d.playerDeathData[d.playerMapSelect-1]:
        d.inGame = False
        textMaster.config(text=lg("Échec de la mission, votre flotte a été anéanti !"),fg="red")
    elif not d.playerDeathData[d.playerMapSelect-1] and d.playerDeathData.count(True) == d.mapNumber - 1:
        d.inGame = False
        textMaster.config(text=lg("Félicitation, vous avez anéanti la flotte ennemie !"),fg="green")

def changeBoatDirection(event):
    global buildBoatDirection
    if not buildBoatSelected == "":
        if buildBoatDirection < 3:
            buildBoatDirection += 1
        else:
            buildBoatDirection = 0
        magicsound.magicsound("gui/sound/Build/Rotate.wav",block = False)

def setInBuildMap(value):
    global inBuildMap
    inBuildMap = value

def setInEnnemieMap(value):
    global inEnnemieMap
    inEnnemieMap = value

def windowResizeOn():
    global windowResize
    windowResize = True

def boatSelect(type,direction,forceSelect):
    global buildBoatSelected
    global buildBoatDirection
    orientation = "NESW"
    buildBoatSelected = ""
    buildBoatDirection = 1
    if boatDataTypeCount(type,d.playerMapSelect) != d.gameDataBoat.count(type) or forceSelect:
        buildBoatSelected = type
        if isinstance(direction, int):
            buildBoatDirection = direction
        else:
            buildBoatDirection = orientation.index(direction)
        magicsound.magicsound("gui/sound/Build/boatSelected.wav",block = False)
        
    if type == "":
        magicsound.magicsound("gui/sound/Build/boatUnselected.wav",block = False)
    refreshGUImap()

# Gestion de la langue
def lg(text):
    try:
        with open("usersettings.json", 'r') as file:
            settings = json.load(file)
        with open("gui/lang/FR.txt", "r", encoding='utf-8') as lgFile:
            frenchLangFile = lgFile.readlines()
        with open("gui/lang/{}.txt".format(country[settings.get("settings").get("lang")]), "r", encoding='utf-8') as lgFile:
            langFile = lgFile.readlines()
        return langFile[frenchLangFile.index(text+"\n")][0:-1]
    except:
        return "[missing text]"

def selectGameMode(mode):
    d.gameMode = mode
    refreshGUI()

def clickEnnemieMap(event):
    if d.mapNumber > 2 and d.ennemieMapSelect in d.tmpAtqDone and not d.playerDeathData[d.playerMapSelect-1]:
        textMaster.config(text=lg("Vous avez déjà tiré sur le joueur {}. Vous n'avez pas tiré sur {} flotte encore.").format(d.ennemieMapSelect,d.mapNumber-len(d.tmpAtqDone)-1),fg="red")
        refreshGUImap()
        refreshToure()
        
    if d.strikerMap == d.playerMapSelect and mapRead(d.ennemieMapSelect,event.x//(ennemieMap.winfo_width()//d.mapSize)+1,event.y//(ennemieMap.winfo_height()//d.mapSize)+1)[1][0] != "X" and not d.playerDeathData[d.ennemieMapSelect-1] and not d.playerDeathData[d.playerMapSelect-1] and not d.ennemieMapSelect in d.tmpAtqDone and not d.atqDone:
        atq(d.playerMapSelect,d.ennemieMapSelect,event.x//(ennemieMap.winfo_width()//d.mapSize)+1,event.y//(ennemieMap.winfo_height()//d.mapSize)+1)
        refreshGUI()
        refreshGUImap()
        refreshToure()

def clickBuild(event):
    global testAddBoat
    global lastBuildBoat
    map = d.playerMapSelect
    direction = "NESW"
    if buildBoatSelected != "":
        if len(boatData[map-1]) < len(d.gameDataBoat) and boatDataTypeCount(buildBoatSelected,map) != d.gameDataBoat.count(buildBoatSelected):
            if buildBoatSelected == "c" or buildBoatSelected == "p":
                    if buildBoatDirection == 0:
                        addBoat(map,buildBoatSelected,event.x//(playerMapBuild.winfo_width()//d.mapSize)+1,event.y//(playerMapBuild.winfo_height()//d.mapSize)+2,direction[buildBoatDirection])
                    elif buildBoatDirection == 3:
                        addBoat(map,buildBoatSelected,event.x//(playerMapBuild.winfo_width()//d.mapSize)+2,event.y//(playerMapBuild.winfo_height()//d.mapSize)+1,direction[buildBoatDirection])
                    else:
                        addBoat(map,buildBoatSelected,event.x//(playerMapBuild.winfo_width()//d.mapSize)+1,event.y//(playerMapBuild.winfo_height()//d.mapSize)+1,direction[buildBoatDirection])
            else:
                addBoat(map,buildBoatSelected,event.x//(playerMapBuild.winfo_width()//d.mapSize)+1,event.y//(playerMapBuild.winfo_height()//d.mapSize)+1,direction[buildBoatDirection])
            if testAddBoat < len(boatData[map-1]):
                testAddBoat += 1
            refreshGUI()
        magicsound.magicsound("gui/sound/Water/Splash{}.mp3".format(randint(1,6)),block = False)
        boatSelect("",1,0)
    else:
        type = mapRead(map,event.x//(playerMapBuild.winfo_width()//d.mapSize)+1,event.y//(playerMapBuild.winfo_height()//d.mapSize)+1)[0]
        if type != "--":
            for i in range(len(boatGuiData[map-1])):
                if boatGuiData[map-1][i][0] == type:
                    boatSelect(type[0],boatGuiData[map-1][i][3],True)
            removeBoat(map,type)
    refreshGUImap()
    

def refreshGUIloop():
    # Effet de tremblement de la fenêtre
    if shakeWindow:
        window.place(relx=0.5,x=randint(-shakeIntensity,shakeIntensity),rely=0.5,y=randint(-shakeIntensity,shakeIntensity),relheight=1,relwidth=1,anchor=CENTER)
    global windowResize
    if not windowResize:
        refreshGUI()
    app.after(int((1/(Hz))*1000),refreshGUIloop)

def refreshAllGUIloop():
    refreshAllGUI()
    app.after(1000,refreshAllGUIloop)

def refreshAllGUI():
    refreshIMG()
    refreshGUImap()

# Lanement des tremblements de la fenêtre
def shake(time):
    global shakeWindow
    shakeWindow = True
    app.after(int(time*1000),shakerOff)

# Arret des tremblements de la fenêtre
def shakerOff():
    global shakeWindow
    shakeWindow = False
    window.place(relx=0.5,x=0,rely=0.5,y=0,relheight=1,relwidth=1,anchor=CENTER)

def refreshGUI():
    global titleStyle
    global buildBoatDirection
    global shakeIntensity
    global shakeWindow
    global globalSize
    global restart
    global fps

    fps += 1

    globalSize = 1 + (app.winfo_height() - 450)*(app.winfo_width() - 800)*0.0000025

    # AllPage
    titleStyle.configure(size=int(50*globalSize))
    default_font.configure(family="Arial",size=int(11*(globalSize*0.30+0.70)),weight=BOLD)

    if d.inGame:
        app.title("Battleship Warfare - In game")
    else:
        app.title("Battleship Warfare")

    if page == prePartyPage or page == gameSettingsPage:
        if d.gameMode:
            text_selectGame.config(text="[BETA] "+lg("Personnalisé"))
            text_selectGame2.config(text="[BETA] "+lg("Personnalisé"))
        else:
            text_selectGame.config(text=lg("Standard"))
            text_selectGame2.config(text=lg("Standard"))

    # Start
    if page == startPage:
        startPage.delete("all")
        startPage.create_image(app.winfo_width()//2,app.winfo_height()//2,image=img_Start_Screen)

    # MainMenu
    if page == mainMenuPage:

        if not menuTitleText:
            mainMenuPage.delete("all")
            text_gameTitle.destroy()
            global img_Title # Titre
            img_Title = ImageTk.PhotoImage(img_Title_Source.resize((int((1080//2*globalSize)),int((300//2*globalSize))), Image.ANTIALIAS))
            mainMenuPage.create_image(app.winfo_width()//2,app.winfo_height()//3,image=img_Title)
        else:
            text_gameTitle.place(relx = 0.5, rely = 0.45, anchor = S)

    # Settings
    if page == settingsPage:
        with open("gui/lang/{}.txt".format(country[lang]), "r", encoding='utf-8') as lgFile:
            langFile = lgFile.readlines()
        mainSettingsPage_lang_button.config(text=langFile[0][0:-1])
        if fullScreen:
            mainSettingsPage_fullscreen_label.config(text=lg("Basculer en mode fenêtré"))
        else:
            mainSettingsPage_fullscreen_label.config(text=lg("Basculer en plein écran"))

        mainSettingsPage_button_apply.config(text=lg("Appliquer"))
        mainSettingsPage_button_apply.place(height=30,width=75,relheight=0.025,relwidth=0.05,relx=0.05,rely=1,x=60,y=-10,anchor = SW)

        with open("usersettings.json", 'r') as fp:
            settings = json.load(fp)
        if lang != settings.get("settings").get("lang") or fullScreen != settings.get("settings").get("fullScreen"):
            mainSettingsPage_button_apply.config(stat=NORMAL)
            if lang != settings.get("settings").get("lang"):
                restart = True
                mainSettingsPage_button_apply.config(text=lg("Redémarrer et appliquer"))
                mainSettingsPage_button_apply.place(height=30,width=150,relheight=0.025,relwidth=0.1,relx=0.05,rely=1,x=60,y=-10,anchor = SW)
            else:
                restart = False
        else:
            mainSettingsPage_button_apply.config(stat=DISABLED)
            
        mainSettingsPage_button_apply.config(command=lambda:[switch(backPage),d.saveSettings(),d.loadSettings(),d.applySettings(),buttonSound(1)])
        mainSettingsPage_button_back.config(command=lambda:[switch(backPage),d.loadSettings(),buttonSound(2)])

    # GameSettings
    if page == gameSettingsPage:
        if d.gameMode == 0:
            button_gameMode.config(text=lg("Standard"))
        if d.gameMode == 1:
            button_gameMode.config(text=lg("Haute Mer"))
        if d.gameMode == 2:
            button_gameMode.config(text=lg("Casual"))
        if d.gameMode == 3:
            button_gameMode.config(text=lg("Hardcore !"))

    # PreParty
    if page == prePartyPage:
        if buildBoatSelected != "":
            boatBuildZone.config(cursor="fleur")
        else:
            boatBuildZone.config(cursor="arrow")

        boatBuildZone.delete("all")
        playerMapBuild.delete(buildBoatSelected+"BoatSelect")

        selectForBuildBoat()

        if showLetter:
            for x in range(d.mapSize):
                if inversLetter:
                    boatBuildZone.create_text(boatBuildZone.winfo_width()//2-playerMapBuild.winfo_width()//2+playerMapBuild.winfo_width()/d.mapSize*(x+0.5),boatBuildZone.winfo_height()//2-playerMapBuild.winfo_height()//2-5*globalSize,text="ABCDEFGHIJKLMNOPQRST"[x],fill="steelBlue4",anchor=S)
                else:
                    boatBuildZone.create_text(boatBuildZone.winfo_width()//2-playerMapBuild.winfo_width()//2+playerMapBuild.winfo_width()/d.mapSize*(x+0.5),boatBuildZone.winfo_height()//2-playerMapBuild.winfo_height()//2-5*globalSize,text=str(x+1),fill="steelBlue4",anchor=S)
            for y in range(d.mapSize):
                if inversLetter:
                    boatBuildZone.create_text(boatBuildZone.winfo_width()//2-playerMapBuild.winfo_width()//2-10*globalSize,boatBuildZone.winfo_height()//2-playerMapBuild.winfo_height()//2+playerMapBuild.winfo_width()/d.mapSize*(y+0.5),text=str(y+1),fill="steelBlue4",anchor=E)
                else:
                    boatBuildZone.create_text(boatBuildZone.winfo_width()//2-playerMapBuild.winfo_width()//2-10*globalSize,boatBuildZone.winfo_height()//2-playerMapBuild.winfo_height()//2+playerMapBuild.winfo_width()/d.mapSize*(y+0.5),text="ABCDEFGHIJKLMNOPQRST"[y],fill="steelBlue4",anchor=E)

            if len(boatData[d.playerMapSelect-1]) == len(d.gameDataBoat) :
                button_launchGame.config(state=ACTIVE)
            else:
                button_launchGame.config(state=DISABLED)

    # Party
    if page == partyPage:

        if d.inGame:
            button_backToMainMenu.config(text=lg("Abandonner"))
        else:
            button_backToMainMenu.config(text=lg("Menu principal"))

        if d.strikerMap == d.playerMapSelect and not d.ennemieMapSelect in d.tmpAtqDone:
            ennemieMap.config(cursor="crosshair")
        else:
            ennemieMap.config(cursor="arrow")

        if d.playerDeathData[d.ennemieMapSelect-1] == True:
            ennemieName.config(text="Player "+str(d.ennemieMapSelect),fg="red")
        else:
            ennemieName.config(text="Player "+str(d.ennemieMapSelect),fg="black")
        ennemieName.place(height=30,width=50,relheight=0.025,relwidth=0.05,relx=0.5,rely=1,y=-10,anchor = S)

        if d.mapNumber > 2 :
            if d.ennemieMapSelect + 1 == d.playerMapSelect:
                button_nextMap.config(text="Player "+str(d.ennemieMapSelect+2))
            else:
                button_nextMap.config(text="Player "+str(d.ennemieMapSelect+1))
            if d.ennemieMapSelect - 1 == d.playerMapSelect:
                button_backMap.config(text="Player "+str(d.ennemieMapSelect-2))
            else:
                button_backMap.config(text="Player "+str(d.ennemieMapSelect-1))

            if d.ennemieMapSelect < d.mapNumber and not (d.playerMapSelect == d.mapNumber and d.ennemieMapSelect+1 == d.mapNumber):
                button_nextMap.place(height=30,width=50,relheight=0.025,relwidth=0.1,relx=0.9,rely=1,y=-10,anchor = SE)
            else:
                button_nextMap.place_forget()
            if d.ennemieMapSelect > 1 and not (d.playerMapSelect == 1 and d.ennemieMapSelect-1 == 1):
                button_backMap.place(height=30,width=50,relheight=0.025,relwidth=0.1,relx=0.1,rely=1,y=-10,anchor = SW)
            else:
                button_backMap.place_forget()
        else:
            button_nextMap.place_forget()
            button_backMap.place_forget()

def selectForBuildBoat():
    allBoatType = ["a","c","f","s","p"]
    for type in range(len(allBoatType)):
            if buildBoatSelected == allBoatType[type]:
                imgSelect = finfBoatImg(allBoatType[type],buildBoatDirection)
            else:
                imgSelect = finfBoatImg(allBoatType[type],1)

            if buildBoatSelected == allBoatType[type] and boatDataTypeCount(allBoatType[type],d.playerMapSelect) != d.gameDataBoat.count(allBoatType[type]):
                if inBuildMap:
                    if buildBoatSelected == "c" or buildBoatSelected == "p":
                        if buildBoatDirection == 0 or buildBoatDirection == 2:
                            playerMapBuild.create_image((((playerMapBuild.winfo_pointerx() - playerMapBuild.winfo_rootx())//(playerMapBuild.winfo_width()//d.mapSize))*(playerMapBuild.winfo_width()//d.mapSize))+((playerMapBuild.winfo_width()//d.mapSize)//2), (((playerMapBuild.winfo_pointery() - playerMapBuild.winfo_rooty())//(playerMapBuild.winfo_height()//d.mapSize))*(playerMapBuild.winfo_height()//d.mapSize))+((playerMapBuild.winfo_height()//d.mapSize)),image=imgSelect,tags=str(allBoatType[type])+"BoatSelect")
                        else:
                            playerMapBuild.create_image((((playerMapBuild.winfo_pointerx() - playerMapBuild.winfo_rootx())//(playerMapBuild.winfo_width()//d.mapSize))*(playerMapBuild.winfo_width()//d.mapSize))+((playerMapBuild.winfo_width()//d.mapSize)), (((playerMapBuild.winfo_pointery() - playerMapBuild.winfo_rooty())//(playerMapBuild.winfo_height()//d.mapSize))*(playerMapBuild.winfo_height()//d.mapSize))+((playerMapBuild.winfo_height()//d.mapSize)//2),image=imgSelect,tags=str(allBoatType[type])+"BoatSelect")
                    else:
                        playerMapBuild.create_image((((playerMapBuild.winfo_pointerx() - playerMapBuild.winfo_rootx())//(playerMapBuild.winfo_width()//d.mapSize))*(playerMapBuild.winfo_width()//d.mapSize))+((playerMapBuild.winfo_width()//d.mapSize)//2), (((playerMapBuild.winfo_pointery() - playerMapBuild.winfo_rooty())//(playerMapBuild.winfo_height()//d.mapSize))*(playerMapBuild.winfo_height()//d.mapSize))+((playerMapBuild.winfo_height()//d.mapSize)//2),image=imgSelect,tags=str(allBoatType[type])+"BoatSelect")
                else:
                    boatBuildZone.create_image(app.winfo_pointerx() - app.winfo_rootx(),app.winfo_pointery() - app.winfo_rooty(),image=imgSelect,tags=str(allBoatType[type])+"BoatSelect")

            elif buildBoatSelected != allBoatType[type] and boatDataTypeCount(allBoatType[type],d.playerMapSelect) != d.gameDataBoat.count(allBoatType[type]):
                boatBuildZone.create_image(app.winfo_width()//7,app.winfo_height()//8+app.winfo_height()//8*(type+1),image=imgSelect,tags=str(allBoatType[type])+"Boat")
        
    boatBuildZone.tag_raise(buildBoatSelected+"BoatSelect")

def refreshGUImap():
    global windowResize
    if windowResize:
        windowResize = False
    if page == prePartyPage:
        refreshOnlyGUImap(boatBuildZone,playerMapBuild,d.playerMapSelect,False)
    if page == partyPage:
        refreshOnlyGUImap(mapZoneUser,playerMap,d.playerMapSelect,False)
        refreshOnlyGUImap(mapZoneEnnemie,ennemieMap,d.ennemieMapSelect,True)

def refreshOnlyGUImap(globalContenter,mapContener,map,ennemie):
    mapContener.place(width = 300*globalSize, height = 300*globalSize,relx = 0.5, rely = 0.5, anchor = CENTER) # Redimensionement de la grille
    globalContenter.delete("all")
    mapContener.delete("all")
    # Construction de la grille
    cases = []
    for i in range(d.mapSize):
        cases_i=[]
        for j in range(d.mapSize):
            if d.mapRead(map,j+1,i+1)[1] == "DD":
                caseColor="steelBlue3"
            elif d.mapRead(map,j+1,i+1)[0] != "--" and d.mapRead(map,j+1,i+1)[1][0] == "X":
                caseColor="steelBlue3"
            elif d.mapRead(map,j+1,i+1)[0] == "--" and d.mapRead(map,j+1,i+1)[1][0] == "X":
                caseColor="steelblue"
            else:
                caseColor="steelBlue3"
            if ennemie and (d.strikerMap == d.playerMapSelect and d.ennemieMapSelect and playerDeathData[d.ennemieMapSelect-1] == False and not playerDeathData[d.playerMapSelect-1] and d.mapRead(d.ennemieMapSelect,j+1,i+1)[1] == "--" and not d.ennemieMapSelect in d.tmpAtqDone and not d.atqDone):
                cases_i.append(mapContener.create_rectangle((j*(mapContener.winfo_width()/d.mapSize)), (i*(mapContener.winfo_height()/d.mapSize)), ((j+1)*(mapContener.winfo_width()/d.mapSize)-int(2*(globalSize*0.5+0.5))), ((i+1)*(ennemieMap.winfo_height()/d.mapSize)-int(2*(globalSize*0.5+0.5))),outline=caseColor,activeoutline="white",fill=caseColor,activewidth=1*globalSize))
            else:
                cases_i.append(mapContener.create_rectangle((j*(mapContener.winfo_width()/d.mapSize)), (i*(mapContener.winfo_height()/d.mapSize)), ((j+1)*(mapContener.winfo_width()/d.mapSize)-int(2*(globalSize*0.5+0.5))), ((i+1)*(mapContener.winfo_height()/d.mapSize)-int(2*(globalSize*0.5+0.5))),outline=caseColor,fill=caseColor))
        cases.append(cases_i)
    # Affichage des images de bateaux
    for i in range(len(boatGuiData[map-1])):
        imgSelect = finfBoatImg(boatGuiData[map-1][i][0][0],boatGuiData[map-1][i][3])
        if not ennemie or ennemie and d.mapRead(map,boatGuiData[map-1][i][1],boatGuiData[map-1][i][2])[1] == "DD":
            if boatGuiData[map-1][i][0][0] == "c" or boatGuiData[map-1][i][0][0] == "p":
                if boatGuiData[map-1][i][3] == "N":
                    mapContener.create_image((boatGuiData[map-1][i][1]*(mapContener.winfo_width()/d.mapSize))-(mapContener.winfo_width()/d.mapSize/2), (boatGuiData[map-1][i][2]*(mapContener.winfo_height()/d.mapSize))-(mapContener.winfo_height()/d.mapSize),image=imgSelect)
                elif boatGuiData[map-1][i][3] == "E":
                    mapContener.create_image((boatGuiData[map-1][i][1]*(mapContener.winfo_width()/d.mapSize)), (boatGuiData[map-1][i][2]*(mapContener.winfo_height()/d.mapSize))-(mapContener.winfo_height()/d.mapSize/2),image=imgSelect)
                elif boatGuiData[map-1][i][3] == "S":
                    mapContener.create_image((boatGuiData[map-1][i][1]*(mapContener.winfo_width()/d.mapSize))-(mapContener.winfo_width()/d.mapSize/2), (boatGuiData[map-1][i][2]*(mapContener.winfo_height()/d.mapSize)),image=imgSelect)
                else:
                    mapContener.create_image((boatGuiData[map-1][i][1]*(mapContener.winfo_width()/d.mapSize))-(mapContener.winfo_width()/d.mapSize), (boatGuiData[map-1][i][2]*(mapContener.winfo_height()/d.mapSize))-(mapContener.winfo_height()/d.mapSize/2),image=imgSelect)
            else:
                mapContener.create_image((boatGuiData[map-1][i][1]*(mapContener.winfo_width()/d.mapSize))-(mapContener.winfo_width()/d.mapSize/2), (boatGuiData[map-1][i][2]*(mapContener.winfo_height()/d.mapSize))-(mapContener.winfo_height()/d.mapSize/2),image=imgSelect)
    # Affichage des icones de status
    for x in range(d.mapSize):
        for y in range(d.mapSize):
            if d.mapRead(map,x+1,y+1)[1][0] == "X" and d.mapRead(map,x+1,y+1)[0] != "--":
                mapContener.create_image(((x+1)*(mapContener.winfo_width()/d.mapSize))-(mapContener.winfo_width()/d.mapSize/2), ((y+1)*(mapContener.winfo_height()/d.mapSize))-(mapContener.winfo_height()/d.mapSize/2),image=img_X)
            if d.mapRead(map,x+1,y+1)[1] == "DD" :
                mapContener.create_image(((x+1)*(mapContener.winfo_width()/d.mapSize))-(mapContener.winfo_width()/d.mapSize/2), ((y+1)*(mapContener.winfo_height()/d.mapSize))-(mapContener.winfo_height()/d.mapSize/2),image=img_D)
    # Affichage des lettres
    if showLetter:
        for x in range(d.mapSize):
            if inversLetter:
                globalContenter.create_text(globalContenter.winfo_width()//2-playerMap.winfo_width()//2+playerMap.winfo_width()/d.mapSize*(x+0.5),globalContenter.winfo_height()//2-playerMap.winfo_height()//2-5*globalSize,text="ABCDEFGHIJKLMNOPQRST"[x],fill="steelBlue4",anchor=S)
            else:
                globalContenter.create_text(globalContenter.winfo_width()//2-playerMap.winfo_width()//2+playerMap.winfo_width()/d.mapSize*(x+0.5),globalContenter.winfo_height()//2-playerMap.winfo_height()//2-5*globalSize,text=str(x+1),fill="steelBlue4",anchor=S)
        for y in range(d.mapSize):
            if inversLetter:
                globalContenter.create_text(globalContenter.winfo_width()//2-playerMap.winfo_width()//2-10*globalSize,globalContenter.winfo_height()//2-playerMap.winfo_height()//2+playerMap.winfo_width()/d.mapSize*(y+0.5),text=str(y+1),fill="steelBlue4",anchor=E)
            else:
                globalContenter.create_text(globalContenter.winfo_width()//2-playerMap.winfo_width()//2-10*globalSize,globalContenter.winfo_height()//2-playerMap.winfo_height()//2+playerMap.winfo_width()/d.mapSize*(y+0.5),text="ABCDEFGHIJKLMNOPQRST"[y],fill="steelBlue4",anchor=E)

text_gameTitle = Label(mainMenuPage,text="BATTLESHIP WARFARE",fg="black",font=titleStyle)

button_play = ttk.Button(mainMenuPage, text=lg("Jouer"),command=lambda:[switch(prePartyPage),selectGameMode(0),creatmap(),buttonSound(1)],takefocus = 0)
button_play.place(height=20,relheight=0.05,relwidth=0.25,relx = 0.5, rely = 0.6,y=-20, anchor = CENTER)

button_settings = ttk.Button(mainMenuPage, text=lg("Réglage"),command=lambda:[switch(settingsPage),buttonSound(1)],takefocus = 0)
button_settings.place(height=20,relheight=0.05, relwidth=0.25,relx = 0.5, rely = 0.65, anchor = CENTER)

button_credit = ttk.Button(mainMenuPage, text=lg("Crédit"),command=lambda:[switch(creditsPage),buttonSound(1)],takefocus = 0)
button_credit.place(height=20,relheight=0.05, relwidth=0.25,relx = 0.5, rely = 0.7,y=20, anchor = CENTER)

button_exit = ttk.Button(mainMenuPage, text=lg("Quitter"),command=lambda:app.destroy(),takefocus = 0)
button_exit.place(height=15,relheight=0.05, relwidth=0.1,relx=1,rely=1,x=-10,y=-10,anchor = SE)

mainMenuPage_label = Label(mainMenuPage, text="v0.2.4",fg="grey70")
mainMenuPage_label.place(height=15,relheight=0.05, relwidth=0.1,rely=1,x=2,y=-2,anchor = SW)

# Settings

mainSettingsPage_title_label = Label(settingsPage,text=lg("Réglage"),fg="black")
mainSettingsPage_title_label.place(width=100,relheight=0.075,relwidth=0.1,relx = 0.5, rely = 0, anchor = N)

mainSettingsPage_lang_label = Label(settingsPage,text=lg("Langage"),fg="black",anchor="w")
mainSettingsPage_lang_label.place(height=11,width=-150,relheight=0.025,relwidth=0.7,relx = 0.1, rely = 0.15,anchor=SW)
mainSettingsPage_lang_label2 = Label(settingsPage,text=lg("Nécessite un redémarrage pour prendre effet"),fg="grey",anchor="w")
mainSettingsPage_lang_label2.place(height=11,width=-150,relheight=0.025,relwidth=0.7,relx = 0.1, rely = 0.15,anchor=NW)
mainSettingsPage_lang_button = ttk.Button(settingsPage,command=lambda:[changeLang(),buttonSound(3)],takefocus = 0)
mainSettingsPage_lang_button.place(height=30,width=100,relheight=0.025,relwidth=0.1,relx = 0.9, rely = 0.15,anchor="e")

mainSettingsPage_fullscreen_label = Label(settingsPage,fg="black",anchor="w")
mainSettingsPage_fullscreen_label.place(height=11,width=-150,relheight=0.025,relwidth=0.7,relx = 0.1, rely = 0.225,y=30,anchor=SW)
mainSettingsPage_fullscreen_label2 = Label(settingsPage,text=lg("Changez rapidement avec en pressant <F11>"),fg="grey",anchor="w")
mainSettingsPage_fullscreen_label2.place(height=11,width=-150,relheight=0.025,relwidth=0.7,relx = 0.1, rely = 0.225,y=30,anchor=NW)
mainSettingsPage_fullscreen_button = ttk.Button(settingsPage,text=lg("Changer"),command=lambda:[setFullScreen(),buttonSound(3)],takefocus = 0)
mainSettingsPage_fullscreen_button.place(height=30,width=100,relheight=0.025,relwidth=0.1,relx = 0.9, rely = 0.225,y=30,anchor="e")

mainSettingsPage_commingSoon_label = Label(settingsPage,text=lg("Prochainement")+"...",fg="black",anchor="w")
mainSettingsPage_commingSoon_label.place(height=11,width=-150,relheight=0.025,relwidth=0.7,relx = 0.1, rely = 0.3,y=60,anchor=SW)

mainSettingsPage_button_apply = ttk.Button(settingsPage,takefocus = 0)

mainSettingsPage_button_back = ttk.Button(settingsPage, text=lg("Annuler"),takefocus = 0)
mainSettingsPage_button_back.place(height=30,width=50,relheight=0.025,relwidth=0.05,relx=0,rely=1,x=10,y=-10,anchor = SW)

# Credits

text_credit = Label(creditsPage,text="Code and graphics\nOkiushi\n\nWebsite and communication\nGakou",bg="black",fg="white")
text_credit.place(relheight=1,relwidth=1,relx = 0.5, rely = 0.5, anchor = CENTER)

button_back = ttk.Button(creditsPage, text=lg("Retour"),command=lambda:[switch(mainMenuPage),buttonSound(2)],takefocus = 0)
button_back.place(height=30,width=50,relheight=0.025,relwidth=0.05,relx=0,rely=1,x=10,y=-10,anchor = SW)

# Select Party

text_selectGame = Label(selectPartyPage,text=lg("Sélectionnez un mode de jeu"),fg="black")
text_selectGame.place(relheight=0.1,relwidth=1,relx = 0.5, rely = 0.05, anchor = CENTER)

button_selectIAGame = ttk.Button(selectPartyPage, text=lg("Standard").upper(),command=lambda:[switch(prePartyPage),selectGameMode(0),creatmap(),buttonSound(1)],takefocus = 0)
button_selectIAGame.place(relwidth=0.4, relheight=0.75,relx = 0.3, rely = 0.475, anchor = CENTER)

button_selectCustomGame = ttk.Button(selectPartyPage, text=lg("Personnalisé").upper(),command=lambda:[d.loadGamePreset(),switch(gameSettingsPage),creatmap(),buttonSound(1)],takefocus = 0)
button_selectCustomGame.place(relwidth=0.4, relheight=0.75,relx = 0.7, rely = 0.475, anchor = CENTER)

button_back = ttk.Button(selectPartyPage, text=lg("Retour"),command=lambda:[switch(mainMenuPage),buttonSound(2)],takefocus = 0)
button_back.place(height=30,width=50,relheight=0.025,relwidth=0.05,relx=0,rely=1,x=10,y=-10,anchor = SW)

# gameSettingsPage

text_selectGame2 = Label(gameSettingsPage,fg="black")
text_selectGame2.place(width=100,relheight=0.075,relwidth=0.1,relx = 0.5, rely = 0, anchor = N)

button_gameMode = ttk.Button(gameSettingsPage,command=lambda:[changeGameMode(),buttonSound(3)],takefocus = 0)
button_gameMode.place(height=30,width=100,relheight=0.025,relwidth=0.05,relx=0.5,rely=0.7,anchor = CENTER)

button_back = ttk.Button(gameSettingsPage, text=lg("Retour"),command=lambda:[d.loadGamePreset(),switch(selectPartyPage),buttonSound(2)],takefocus = 0)
button_back.place(height=30,width=50,relheight=0.025,relwidth=0.05,relx=0,rely=1,x=10,y=-10,anchor = SW)

text_commingSoon = Label(gameSettingsPage,text=lg("Prochainement"),bg="black",fg="white")
text_commingSoon.place(relheight=0.1,relwidth=1,relx = 0.5, rely = 0.5, anchor = CENTER)

button_creatParty = ttk.Button(gameSettingsPage, text=lg("Crée la partie"),command=lambda:[creatmap(),switch(prePartyPage),buttonSound(1)],takefocus = 0)
button_creatParty.place(height=50,width=100,relheight=0.05,relwidth=0.15,relx=1,rely=1,x=-10,y=-10,anchor = SE)

# Pre-Party

boatBuildZone = Canvas(prePartyPage)
boatBuildZone.place(relheight=1,relwidth=1,relx=0.5,rely=0.5,anchor=CENTER)

playerMapBuild = Canvas(boatBuildZone,bg="steelBlue1")

text_selectGame = Label(prePartyPage,fg="black")
text_selectGame.place(width=100,relheight=0.075,relwidth=0.1,relx = 0.5, rely = 0, anchor = N)

button_back = ttk.Button(prePartyPage, text=lg("Retour"),command=lambda:[switch(backPage),buttonSound(2)],takefocus = 0)
button_back.place(height=30,width=50,relheight=0.025,relwidth=0.05,relx=0,rely=1,x=10,y=-10,anchor = SW)

button_launchGame = ttk.Button(prePartyPage, text=lg("/// LANCER ///"),command=lambda:[d.laucheGame(),buttonSound(1)],takefocus = 0)
button_launchGame.place(height=50,width=100,relheight=0.05,relwidth=0.15,relx=1,rely=1,x=-10,y=-10,anchor = SE)

button_creatyRandomMap = ttk.Button(prePartyPage, text=lg("Aléatoire"),command=lambda:[creatmap(),creatRandomMap(d.playerMapSelect),buttonSound(3),refreshGUImap()],takefocus = 0)
button_creatyRandomMap.place(height=30,width=100,relheight=0.025,relwidth=0.15,relx=1,rely=0.95,x=-10,y=-65,anchor = SE)

# Party

mapZone = Frame(partyPage)
mapZone.place(relx = 0.5, rely = 0.5, relwidth = 1, relheight = 1,anchor = CENTER)
mapZoneUser = Canvas(mapZone)
mapZoneUser.place(relheight=1,relwidth=0.5)
mapZoneEnnemie = Canvas(mapZone,)
mapZoneEnnemie.place(relheight=1,relwidth=0.5, relx=0.5)
playerMap = Canvas(mapZoneUser,bg="steelBlue1")
ennemieMap = Canvas(mapZoneEnnemie,bg="steelBlue1")

textMaster = Label(partyPage)
textMaster.place(height=10,relheight=0.05,relwidth=1,relx = 0.5, rely = 0, anchor = N)

button_backToMainMenu = ttk.Button(partyPage, text=lg("Réglage"),command=lambda:[switch(settingsPage),buttonSound(1)],takefocus = 0)
button_backToMainMenu.place(height=30,width=50,relheight=0.025,relwidth=0.1,relx=0.1,rely=1,x=85,y=-10,anchor = SW)

button_backToMainMenu = ttk.Button(partyPage, text="",command=leaveGame,takefocus = 0)
button_backToMainMenu.place(height=30,width=75,relheight=0.025,relwidth=0.1,relx=0,rely=1,x=10,y=-10,anchor = SW)

ennemieName = Label(mapZoneEnnemie)

button_nextMap = ttk.Button(mapZoneEnnemie, text="Player "+str(d.ennemieMapSelect+1),command=lambda:[nextEnnemieMap(1),buttonSound(3)],takefocus = 0)
button_backMap = ttk.Button(mapZoneEnnemie, text="Player "+str(d.ennemieMapSelect-1),command=lambda:[nextEnnemieMap(0),buttonSound(3)],takefocus = 0)

### --- Main execution --- ###

def ihmStart():
    app.minsize(800, 450)
    app.maxsize(app.winfo_screenwidth(),app.winfo_screenheight())
    app.geometry('%dx%d+%d+%d' % (W, H, (app.winfo_screenwidth()/2) - (W/2), (app.winfo_screenheight()/2) - (H/2)))
    app.iconbitmap("gui/image/icon.ico")
    d.loadSettings()
    d.applySettings()
    creatmap()
    # Ouverture du menu
    switch(startPage)
    app.after(3,lambda:switch(mainMenuPage))
    # magicsound.magicsound('gui/sound/StartScreen/StartScreen.mp3',block = False)