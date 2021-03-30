import pygame
import time
from pygame.locals import *
import random
import piece

pygame.init()
ecran = pygame.display.set_mode((1,1))          
pygame.time.set_timer(USEREVENT+1, 200)

class Piece:
    def __init__(self):
        self.nom = None
        self.forme = None
        self.deplacement = 0
        self.rotation = 0
        self.choisir_piece()

    def choisir_piece(self):
        LISTE_PIECES = ['L','T','carre','droit']
        self.nom = random.choice(LISTE_PIECES)
        self.forme =int("".join(str(x) for x in (piece.ensemble_piece[self.nom]['0'])),2)

    def tourner_piece(self):
        if self.nom != 'carre':
            if self.rotation == 3:
                self.rotation = -1

            if self.rotation !=3:
               # if terrain.detection_colision('piece_tourné') == False:
                self.forme =int("".join(str(x) for x in (piece.ensemble_piece[self.nom][str(self.rotation+1)])),2)
                if self.deplacement == 0:
                    pass

                else:
                    self.forme =int(self.forme/2**abs(self.deplacement))
            self.rotation +=1

                


class Terrain:
    def __init__(self):
        self.apparence = piece.ensemble_piece['Terrain']['0']
        self.piece_en_cours = Piece()
        self.terrain_et_piece = None
        self.limite = piece.ensemble_piece['Terrain']['1']

    def to_binaire(self):
        return int("".join(str(x) for x in self.apparence),2)

    def deplacer_une_case_droite(self):
        return int(self.piece_en_cours.forme/2)

    def deplacer_une_case_gauche(self):
        return int(self.piece_en_cours.forme*2)

    def descendre_une_case(self):
        return int(self.piece_en_cours.forme/1024)

    def coller_piece_sur_terrain(self):  
        self.terrain_et_piece =[int(nombre) for nombre in str("{0:b}".format(self.to_binaire() ^ self.piece_en_cours.forme))]
        return self.terrain_et_piece

    def detection_colision(self, endroit_a_tester):
        if endroit_a_tester == 'droite':
            return bool(self.to_binaire() & self.deplacer_une_case_droite())

        if endroit_a_tester == 'gauche':
            return bool(self.to_binaire() & self.deplacer_une_case_gauche())

        if endroit_a_tester == 'bas':
            return bool(self.to_binaire() & self.descendre_une_case())

        if endroit_a_tester == 'limite':
            self.limite = int("".join(str(x) for x in (piece.ensemble_piece['Terrain']['1'])),2)
            return bool(self.to_binaire() & self.limite)

        #if endroit_a_tester == 'piece_tourné':
         #   return bool(self.to_binaire() & int(int("".join(str(x) for x in (piece.ensemble_piece[self.piece_en_cours.nom][str(self.piece_en_cours.rotation+1)])),2)/2**self.piece_en_cours.deplacement))
            


    def gravite_bloc(self):
        if self.detection_colision('limite') == True:
            print("PERDU") 
        else:
            if self.detection_colision('bas') == False:
                self.piece_en_cours.forme = self.descendre_une_case()
                self.coller_piece_sur_terrain()
                self.piece_en_cours.deplacement +=10
                affichage()

            else:
                self.apparence = self.coller_piece_sur_terrain()
                self.piece_en_cours.choisir_piece()
                self.piece_en_cours.deplacement = 0
                affichage()
        
    def bouger_droite(self):
        if self.detection_colision('droite') == False:
            self.piece_en_cours.forme= self.deplacer_une_case_droite()
            self.piece_en_cours.deplacement +=1 
            affichage()

    def bouger_gauche(self):
        if self.detection_colision('gauche') == False:
            self.piece_en_cours.forme= self.deplacer_une_case_gauche()
            self.piece_en_cours.deplacement -=1    
            affichage()
def affichage():
    for index, nombre in enumerate(terrain.terrain_et_piece):
        if index % 10 == 0 and index > 0:   
            print("")
        if nombre == 0:
            print(" ",end="")
            time.sleep(0)
        else:
            print(nombre,end="")
    print("")

terrain = Terrain()

while True:
    for event in pygame.event.get():
        if event.type == USEREVENT+1:
          terrain.gravite_bloc()

        if event.type == QUIT:
            pygame.quit()
            break            

        if event.type== pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                break

            if event.key == pygame.K_RIGHT:
                terrain.bouger_droite()
                
            if event.key == pygame.K_LEFT:
                terrain.bouger_gauche()

            if event.key == pygame.K_UP:
                terrain.piece_en_cours.tourner_piece()
                
   # time.sleep(0.1) je dois utiliser b