import sys
import pygame
from pygame.locals import *
from random import randint
from threading import Thread,RLock,Lock
from time import clock,sleep
import time
from random import uniform
import PIL
from PIL import Image
from pygame import mixer
pygame.init()
pygame.mixer.init




#____________Fonction de déplacement du fond_____________

def deplacement_fond(coord):                                                            # fonction qui permet le déplacement du joueur/ des virus/ des cellules
    global pos_fond,pos_vert1,pos_vert2,pos_vert3,pos_vert4,coord_cellule                  # la variable pos_fond est globale
    a=(450-(coord[0]))/100                                          #coord x calculé avec le centre - les coord de la souris/100
    b=(450-(coord[1]))/100                                          #coord x calculé avec le centre - les coord de la souris/100


    if -3780<=pos_fond[0]<=0 and -3794<=pos_fond[1]<=0 :            # limite de la carte
        pos_fond=(pos_fond[0]+a,pos_fond[1]+b)                      # coord de base du fond + celle calculée en fonction de la position de la souris

        pos_vert1=(pos_vert1[0]+a,pos_vert1[1]+b)                       #déplacement les 4 virus
        pos_vert2=(pos_vert2[0]+a,pos_vert2[1]+b)
        pos_vert3=(pos_vert3[0]+a,pos_vert3[1]+b)
        pos_vert4=(pos_vert4[0]+a,pos_vert4[1]+b)


    if -3780>pos_fond[0]:                                           #pour chaque cotés on redéplace un peu le joueur pour qu'il ne reste pas bloqué dans la limite
        pos_fond=(pos_fond[0]+1,pos_fond[1])
    if -3794>pos_fond[1]:
        pos_fond=(pos_fond[0],pos_fond[1]+1)
    if 0<pos_fond[0]:
        pos_fond=(pos_fond[0]-1,pos_fond[1])
    if 0<pos_fond[1]:
        pos_fond=(pos_fond[0],pos_fond[1]-1)

    for i in range(len(coord_cellule)):                           # déplacement des cellules (même procédé que pour le joueur)

        if -3780<=pos_fond[0]<=0 and -3794<=pos_fond[1]<=0 :
            coord_cellule[i]=(coord_cellule[i][0]+a,coord_cellule[i][1]+b)

        if -3780>pos_fond[0]:                                       #limite de la carte pour les cellules quand le joueur est sur les bords
            coord_cellule[i]=(coord_cellule[i][0]+1.41,coord_cellule[i][1])
        if -3794>pos_fond[1]:
            coord_cellule[i]=(coord_cellule[i][0],coord_cellule[i][1]+1.41)
        if 0<pos_fond[0]:
            coord_cellule[i]=(coord_cellule[i][0]-1.41,coord_cellule[i][1])
        if 0<pos_fond[1]:
            coord_cellule[i]=(coord_cellule[i][0],coord_cellule[i][1]-1.41)




#__________________________fonction pour manger des cellules______________________________
def manger():                                           # fonction qui permet de manger les cellules avec le joueur
    global n,k,pos_cell_joueur,x,y,l1,compteur_cel,w

    for i in range(len(coord_cellule)):                     #boucle qui vérifie pour chaque cellules si elles sont dans les coordonnées du joueur
        if x<coord_cellule[i][0]<y and x<coord_cellule[i][1]<y:
            coord_cellule[i]=(1000000,1000000)                  # si elles le sont alors on les envoit en 1000000,1000000 (en dehors de la carte)
            compteur_cel=compteur_cel-1                         #compteur pour enlever le nombre de boule mangée (qui ne sont donc plus dans la carte)

            '''
            son=pygame.mixer.Sound("pop.mp3")
            son.play()                  #bruit quand on mange une cellule
            '''


    for j in range(len(coord_cellule)) :
        if coord_cellule[j]==(1000000,1000000) and w<35:       #condition qui vérifie si la cellule est en 1000000;1000000 et si le joueur n'est pas trop gros
            n=n+1                                               #compteur de cellules mangées
            if n==k:                                            # compteur pour que toutes les 5 cellules le joueur grossisse
                redimention()                                       #applique la fonction redimention
                pos_cell_joueur=(x,x)                               #on applique les nouvelles coord au joueur
                fenetre.blit(cell_joueur,pos_cell_joueur)        #on recolle le joueur à ses nouvelles coord pour qu'il reste au centre de l'écran
                k=k+5                                           # on ajoute 5 au compteur pour qu'il regrossisse toutes les 5 cellules
                l1=l1*1.05                                      #on multiplie la longueur de la longueur du joueur par le coefficient de grossissement
                x=x-(l1*0.025)                                   # on soustrait au coord du joueur un % de celui de l'image pour le déplacer en haut à gauche pour qu'il reste au centre de l'image et que l'hitbox soit bonne
                y=y+(l1*0.0125)                                     #on additione au coord du joueur un % de celui de l'image pour le déplacer en bas à droite pour que l'hitbox reste bonne
                w=w+1                                               #compteur pour savoir combien de fois le joueur a grossi
                print("boule grossie",w,"fois")                      #on affiche le nombre de fois qu'il a grossi

#____________________________fermer_______________________________________

def fermer():                                                #fonction qui permet de fermer le programme
    sys.exit
    pygame.quit()
    Accueil=0

#________________________redimenssion_image_____________________________

def redimention():                                      #fonction qui permet la redimenssion du joueur
    image = Image.open('boule_grossie.png')             #on ouvre l'image "boule grossie" qui est celle qu'on va redimentionner
    global cell_joueur
    l,h=image.size                                      #on défini l et h comme longueur et hauteur de l'image
    image= image.resize((int(l*1.05),int(h*1.05)),Image.ANTIALIAS)  #on multiplie l et h avec le coefficient de grossissement
    image.save('boule_grossie.png')                        #on écrase l'ancienne boule grossie par la nouvelle plus grosse
    cell_joueur=pygame.image.load('boule_grossie.png')      #on charge la nouvelle image pour le joueur

#_____________________Division________________________________________
'''
def division_cellule(im,i):   # im est le "nom du fichier image.png"
    image = Image.open(im)
    l,h=image.size
    image= image.resize((int(l*0.5),int(h*0.5)),Image.ANTIALIAS)
    image.save('%s.png'%i)
'''
#_____________________calsse de creation d'un Thread___________________
class generateur_coord_cell(Thread):

    """Thread chargé simplement de générer un nombre(nombre) donné de couples de coordonnées avec un intervalle de temps(delta_t) entre deux créations fixé.,
    le thread ne se charge pas de l'affichage, du collage des images sinon il y aurait un problème de synchronisation avec le collage du fond ,
    de l'image de la cellule du joueur et le rafraichissement qui sont, eux , gérés par le programme principal"""

    def __init__(self,nombre, delta_t):
        Thread.__init__(self)
        self.nombre=nombre
        self.delta_t=delta_t
        self.running=True

    def run(self):
        """Code à exécuter pendant l'exécution du thread."""
        global coord_cellule,continuer,compteur_cel     # liste de tuple partagé avec le programme principal, (il va falloir la verrouiller pour éviter un accès simultané du thread et du prog ppal: non inutile)

        while self.running==True :
            while compteur_cel<self.nombre and compteur_cel<400:  # tant que le nombre de couples de coordonnées de cellules crés est < self.nombre

                coord_cellule.append((uniform(pos_fond[0]+300,pos_fond[0]+3580),uniform(pos_fond[1]+300,pos_fond[1]+3594))) # générer aleatoirement les coordonnées d'une nouvelle cellule
                compteur_cel=compteur_cel+1                            #on compte le nombre de cellule crée

                time.sleep(self.delta_t)   # pause
    def stop(self):
        self.running=False



### _________________main prog_______________________________

#initialisation des variables
pos_cell_joueur=(400,400)   # position initiale de la cellule rouge
continuer=1                 #variable qui lance le jeu
compteur_cel=0   # nombre de cellules dans le décor
coord_cellule=[] # liste des coordonnées des cellules du décor
n=0             #compteur du nombre de boule manger
k=5             #compteur pour que les 5 boules grossissent
w=0             #compteur pour ne pas trop grossir
pos_vert1=(randint(0,3700),(randint(0,3700)))       #création des coord aléatoires des 4 virus
pos_vert2=(randint(0,3700),(randint(0,3700)))
pos_vert3=(randint(0,3700),(randint(0,3700)))
pos_vert4=(randint(0,3700),(randint(0,3700)))
Accueil=1       #variable qui lance l'acceuil
x=400           #coordonnée de la cel joueur / de la hitbox haut gauche
y=500           #coordonnée de la hitbox bas droite
l1=100          #taille pour calculer le grossissement de la boule/hitbox
continuer=0     #variable qui ferme le jeu
coord=(450,450)     #centre de l'écran/boule



# Chargement des images
fond=pygame.image.load("quadri2.png")
cell_joueur=pygame.image.load('Rond_rouge.png')
cellv=pygame.image.load("cellule_verte.png")
cellb=pygame.image.load("cellule_bleu.png")
cellj=pygame.image.load("cellule_jaune.png")
rondv=pygame.image.load("Rond-vert.png")
accueil=pygame.image.load("Accueil.png")
exi=pygame.image.load("exit.png")
image = Image.open("Rond_rouge.png")
image.save('boule_grossie.png')  # creation de l'image boule grossie initialement égal au Rond_rouge
musicon=pygame.image.load("MusicOn.png")
musicoff=pygame.image.load("MusicOff.png")

#musique
pygame.mixer.music.load("Space-Battle.mp3")  #Musique pendant le jeu
pygame.mixer.music.load("Jungle Mayhem.mp3")
pygame.mixer.music.queue("Jungle Mayhem.mp3")
pygame.mixer.music.set_volume(0.5)

# Création de la fenetre

fenetre=pygame.display.set_mode((900,900))

# Position de base du fond
pos_fond=(-1000,-1000)      #position initiale du fond


# Creation du thread
thread_cellule = generateur_coord_cell(10000000,0.1)       # génère jusqu'à100000000 couples de coordonnées de cellules , un couple toutes les 0.1 secondes


# Boucle de jeu
pygame.key.set_repeat(10,50)
pygame.mixer.music.play()


while Accueil==1:   #On crée une boucle Menu dans lequel sera intégré la boucle du jeu même.

    fenetre.blit(fond,(pos_fond))  #Collage des images
    fenetre.blit(exi,(738,0))
    fenetre.blit(accueil,(338,326))
    fenetre.blit(musicon,(0,794))
    fenetre.blit(musicoff,(0,847))
    pygame.display.flip() #Rafraîchissement des images

    for event in pygame.event.get(): #Pour les événements
        if event.type==MOUSEBUTTONDOWN: #Evenement clic de souris
           if event.button==1: #Clic gauche de la souris

                if 0<event.pos[0]<204 and 794<event.pos[1]<847:  #Si on clique sur le bouton qui se trouve dans ces coordonnées, la musique redemarre là où on la mise en pause
                    pygame.mixer.music.unpause()
                if 0<event.pos[0]<204 and 847<event.pos[1]<900: #Si on clique sur le bouton qui se trouve dans ces coordonnées, la musique se met en pause
                    pygame.mixer.music.pause()


                if 371<event.pos[0]<548 and 470<event.pos[1]<555:  #Si clic de souris sur le bouton jouer, la boucle du jeu démarre
                    continuer=1

                    thread_cellule.start()      # Démarrage du thread

                if 738<event.pos[0]<900 and 0<event.pos[1]<64: # clic sur le bouton fermer, la fenêtre du jeu se ferme
                    fermer()

                if event.type==QUIT:
                    thread_cellule.stop()
                    fermer() #On quitte la boucle accueil, la fenêtre du jeu se ferme


    while continuer==1: #boucle fonctionnelle du jeu

        fenetre.blit(fond,(pos_fond))

        for i in range(len(coord_cellule)):   # choix de la couleur de la cellule en fonction du rang des coordonnées dans la liste
            if i%3==0:
                fenetre.blit(cellb,coord_cellule[i])
            elif i%3==1:
                fenetre.blit(cellj,coord_cellule[i])
            else:
                fenetre.blit(cellv,coord_cellule[i])

        fenetre.blit(cell_joueur,pos_cell_joueur)
        fenetre.blit(rondv,pos_vert1)
        fenetre.blit(rondv,pos_vert2)
        fenetre.blit(rondv,pos_vert3)
        fenetre.blit(rondv,pos_vert4)
        fenetre.blit(exi,(738,0))
        fenetre.blit(musicon,(0,794))
        fenetre.blit(musicoff,(0,847))




        for event in pygame.event.get():
            if event.type == MOUSEMOTION: #Si mouvement de souris
                coord=(event.pos[0],event.pos[1])       #On change les coordonnées

            if event.type==QUIT:
                thread_cellule.stop()
                fermer()



            if event.type==MOUSEBUTTONDOWN:
                if event.button==1:
                    if 738<event.pos[0]<900 and 0<event.pos[1]<64:  #bouton fermer, la boucle du jeu se ferme, on revient à l'accueil.
                        thread_cellule.stop()
                        continuer=0

                    if 0<event.pos[0]<204 and 794<event.pos[1]<847:
                        pygame.mixer.music.unpause()
                    if 0<event.pos[0]<204 and 847<event.pos[1]<900:
                        pygame.mixer.music.pause()

        deplacement_fond(coord) #On execute les fonctions déplacement et manger
        manger()


        pygame.display.flip()