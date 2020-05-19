# -*- coding: utf-8 -*-

# Nicolas, 2020-03-20

from __future__ import absolute_import, print_function, unicode_literals
from gameclass import Game, check_init_game_done
from spritebuilder import SpriteBuilder
from players import Player
from sprite import MovingSprite
from ontology import Ontology
from itertools import chain
import pygame
import glo
from aStar import aStar
import random 
import numpy as np
import sys



    
# ---- ---- ---- ---- ---- ----
# ---- Main                ----
# ---- ---- ---- ---- ---- ----

game = Game()

def init(_boardname=None):
    global player,game
    # pathfindingWorld_MultiPlayer4
    name = _boardname if _boardname is not None else 'kolkata_6_10'
    game = Game('Cartes/' + name + '.json', SpriteBuilder)
    game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
    game.populate_sprite_names(game.O)
    game.fps = 5  # frames per second
    game.mainiteration()
    game.mask.allow_overlaping_players = True
    #player = game.player

    
def main():

    #for arg in sys.argv:
    iterations = 2 # default
    if len(sys.argv) == 2:
        iterations = int(sys.argv[1])
    print ("Iterations: ")
    print (iterations)

    init()

    #-------------------------------
    # Initialisation
    #-------------------------------
    nbLignes = game.spriteBuilder.rowsize
    nbColonnes = game.spriteBuilder.colsize
    print("lignes", nbLignes)
    print("colonnes", nbColonnes)
    
    
    players = [o for o in game.layers['joueur']]
    nbPlayers = len(players)
    
    
    # on localise tous les états initiaux (loc du joueur)
    initStates = [o.get_rowcol() for o in game.layers['joueur']]
    print ("Init states:", initStates)
    
    
    # on localise tous les objets  ramassables (les restaurants)
    goalStates = [o.get_rowcol() for o in game.layers['ramassable']]
    print ("Goal states:", goalStates)
    nbRestaus = len(goalStates)
        
    # on localise tous les murs
    wallStates = [w.get_rowcol() for w in game.layers['obstacle']]
    #print ("Wall states:", wallStates)
    
    # on liste toutes les positions permises
    allowedStates = [(x,y) for x in range(nbLignes) for y in range(nbColonnes)\
                     if (x,y) not in wallStates or goalStates]

    #-------------------------------
    # Boucle principale de déplacements 
    #-------------------------------


    restau = [-1] * nbPlayers
    matrix = [[0]*nbRestaus for x in range(iterations)]
    points = [0] * nbPlayers
    for i in range(iterations):
        print("iteration ", i)
        for j in range(nbPlayers/2):
            c = strategy(matrix, restau[j], nbRestaus)
            print("player", j, "restau ", c)
            restau[j] = c
            matrix[i][c] = matrix[i][c] + 1
        for j in range(nbPlayers/2 + 1, nbPlayers ):
            c = aleaStrategy(nbRestaus)
            print("player", j, "restau ", c)
            restau[j] = c
            matrix[i][c] = matrix[i][c] + 1
        print(matrix)
        for j in range(nbRestaus):
            if matrix[i][j] > 0:
                if matrix[i][j] == 1:
                    client = restau.index(j)
                    points[client] = points[client] + 1
                else:
                    clients = [k for k in range(len(restau)) if restau[k] == j]
                    winner = random.randint(0, len(clients)-1)
                    points[clients[winner]] = points[clients[winner]] + 1
        move(restau, players, initStates, goalStates, wallStates)
        for p in range(nbPlayers):
            row_col = initStates[p]
            players[p].set_rowcol(row_col[0], row_col[1])
            game.mainiteration()

    print(points)


    pygame.quit()
    
        
    
def strategy(matrix, previousChoice, nbRestaus):
    if previousChoice == -1:
        return random.randint(0, nbRestaus-1)

    if matrix[len(matrix)-1][previousChoice] > 1:
        while True:
            pos = random.randint(0, nbRestaus - 1)
            if pos != previousChoice:
                return pos
    else:
        return previousChoice


def strategy2(matrix, previousChoice, nbRestaus,iteration):
    if previousChoice == -1:
        return random.randint(0, nbRestaus - 1)
    else:
        return min(matrix[iteration-1])


def strategy3(matrix, previousChoice, nbRestaus,iteration):
    if previousChoice == -1:
        return random.randint(0, nbRestaus - 1)
    else:
        average=[]
        for i in range(nbRestaus):
            mean=0
            for j in range(iteration):
                mean+=matrix[j][i]
            average.append(mean/nbRestaus)
        return  average.index(min(average))


def strategy4(matrix, previousChoice, nbRestaus,iteration):
    if previousChoice == -1:
        return random.randint(0, nbRestaus - 1)
    else:
        average = []
        for i in range(nbRestaus):
            mean=0
            for j in range(iteration):
                mean+=matrix[j][i]
            average.append(mean/nbRestaus)
        return average.index(max(average))

def aleaStrategy(nbRestaus):
    return random.randint(0,nbRestaus-1)

def sameStrategy(previousChoice, nbRestaus):
    if previousChoice == -1:
        return random.randint(0, nbRestaus - 1)
    else:
        return previousChoice

def move(restau, players, initStates, goalStates, wallStates):
    for j in range(len(players)):
        states = (initStates[j], goalStates[restau[j]], wallStates)
        path = aStar(states)
        for position in path:
            next_row = position[0]
            next_col = position[1]
            players[j].set_rowcol(next_row, next_col)
            game.mainiteration()

if __name__ == '__main__':
    main()
    


