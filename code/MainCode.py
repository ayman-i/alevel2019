#Written by Ayman Islam (https://www.linkedin.com/in/aymansislam/) between 2017-2019

import os
import pygame
import levels
import random
import datetime
import math

import time
from TableCreate import *

#Please comment out this line after the first time running
create_tables()

#Wall class for creating wall objects.
class Wall():
    def __init__(self,x,y,disappearing):
        self.rect = pygame.Rect(x,y,30,30)
        self.colour = (BLACK)
        self.disappeared = False
        self.hit = False
        self.disappearing = disappearing
        walls.append(self)

    #Used to make the disappearing maze walls disappear.
    def disappear(self):
        if self.disappearing == True:
            self.colour = (WHITE)
        if self.hit == True:
            self.colour = (255,0,0)

#ShopItem class for creating ShopItem objects.
class ShopItem():
    def __init__(self,price,x,y,name):
        ShopItems.append(self)
        self.rect = pygame.Rect(x,y,30,30)
        self.colour = (0,0,255)
        self.price=price
        self.name = name
        
    #Used to purchase whatever is behind the object (door).
    def Open(self,amount):
        if self.name != "Med":
            if amount > self.price or amount == self.price:
                ShopItems.remove(self)
                for i in range(0,self.price):
                    player.itemsOwned.remove("Gold")
        if self.name == "Med":
            if amount > self.price or amount == self.price:
                for i in range(0,self.price):
                    player.itemsOwned.remove("Gold")
                create_ground_item(397,221,(255,0,0),"Med")

#Door class for creating Door objects.
class Door():
    def __init__(self,x,y,levelLink,Lx,Ly,LLN):
        doors.append(self)
        self.rect = pygame.Rect(x,y,30,30)
        self.levelLink = levelLink
        self.Lx = Lx
        self.Ly = Ly
        self.LLN = LLN
        if self.LLN == "LS":
            self.colour = (RED)
        else:
            self.colour = (BROWN)      

#Character superclass for creating Characters.
class Character(pygame.sprite.Sprite):
    def __init__(self,image,health,attackDMG,charType,runningLeft,runningRight,runningUpwards,runningDownwards, itemsOwned, lives, maxhealth):
        super().__init__()
        self.image = pygame.image.load(image)
        self.frameCount=0
        self.lives=lives
        self.idleImage = pygame.image.load(image)
        self.runningLeft = runningLeft
        self.runningRight = runningRight
        self.runningUpwards = runningUpwards
        self.runningDownwards = runningDownwards
        self.rect = self.image.get_rect()
        self.itemsOwned=itemsOwned
        self.maxhealth=maxhealth
        self.Status = True
        Characters.append(self)

    #Used to move the Characters.
    def move(self,dx,dy,direction):
        if self.Status == True:
            self.frameCount+=1
            self.rect.x+=dx
            self.rect.y+=dy
            self.updateImages(direction)

            for wall in walls:
                if self.rect.colliderect(wall.rect):
                    if wall.disappearing == True:
                        if damageTimer%10 == 0:
                            self.takeDamage(8)
                            wall.hit = True
                            
                    if dx > 0:
                        self.rect.right = wall.rect.left
                    if dx < 0:
                        self.rect.left = wall.rect.right
                    if dy > 0:
                        self.rect.bottom = wall.rect.top
                    if dy < 0:
                        self.rect.top = wall.rect.bottom

            for door in doors:
                if self.rect.colliderect(door.rect):
                    if dx > 0:
                        self.rect.right = door.rect.left
                    if dx < 0:
                        self.rect.left = door.rect.right
                    if dy > 0:
                        self.rect.bottom = door.rect.top
                    if dy < 0:
                        self.rect.top = door.rect.bottom

            for char in Characters:
                if char != self:
                    if char.Status == True:
                        if self.rect.colliderect(char.rect):
                            if dx > 0:
                                self.rect.right = char.rect.left
                            if dx < 0:
                                self.rect.left = char.rect.right
                            if dy > 0:
                                self.rect.bottom = char.rect.top
                            if dy < 0:
                                self.rect.top = char.rect.bottom

            for SI in ShopItems:
                if self.rect.colliderect(SI.rect):
                    if dx > 0:
                        self.rect.right = SI.rect.left
                    if dx < 0:
                        self.rect.left = SI.rect.right
                    if dy > 0:
                        self.rect.bottom = SI.rect.top
                    if dy < 0:
                        self.rect.top = SI.rect.bottom

            for item in Items:
                rect1 = item[2]
                if self.rect.colliderect(rect1):
                    self.pickupItem(item[3])
                    Items.remove(item)

    #Used to pick up an item and add it to the inventory.
    def pickupItem(self,item):
        self.itemsOwned.append(item)
        if item == "Map":
            global mapBought
            mapBought=True
        if item == "Key1":
            global key1Found
            key1Found = True
        if item == "Key2":
            global key2Found
            key2Found = True
        if item == "Key3":
            global key3Found
            key3Found = True

    #Used to attack other Characters.
    def attack(self,target):
        if self.Status == True:
            if self.charType == "P":
                reach=90
            if self.charType == "E":
                reach=45
            if self.charType == "B":
                reach = 120
            if self.rect.x < target.rect.x+reach and self.rect.x > target.rect.x-reach:
                if self.rect.y > target.rect.y-reach and self.rect.y < target.rect.y+reach:
                    target.takeDamage(self.attackDMG)
                    if self.rect.x < target.rect.x-15:
                        if self.rect.y < target.rect.y-30:
                            target.move(10,10,"idle")
                        if self.rect.y > target.rect.y+30:
                            target.move(10,-10,"idle")
                        else:
                            target.move(10,0,"idle")
                    if self.rect.x > target.rect.x+15:
                        if self.rect.y < target.rect.y-30:
                            target.move(-10,10,"idle")
                        if self.rect.y > target.rect.y+30:
                            target.move(-10,-10,"idle")
                        else:
                            target.move(-10,0,"idle")
                    else:
                        if self.rect.y < target.rect.y:
                            target.move(0,10,"idle")
                        if self.rect.y > target.rect.y:
                            target.move(0,-10,"idle")

    #Used to remove health from the Character.
    def takeDamage(self,attackDMG):
        if self.Status == True:
            self.health -= attackDMG
            if self.health <= 0:
                self.Die()

    #Used to handle deaths of Characters, including the player.
    def Die(self):
        self.Status=False
        self.lives-=1
        if self.lives==0:
            self.dropItems()
            self.kill()
            if self in Characters:
                Characters.remove(self)
            if self in Enemies:
                Enemies.remove(self)
            if self.charType == "P":
                screen.fill(WHITE)
                message_display("Game Over",width/2-10,height/2,50,RED)
                time.sleep(3)
            if self.charType == "B":
                win()
        else:
            if self.charType == "P":
                screen.fill(WHITE)
                okay=False
                okButton = pygame.draw.rect(screen, (0,255,0), ((width/2-75),(height/2+50),100,30))
                quitButton = pygame.draw.rect(screen, (255,0,0), ((width/2-75),(height/2+100),100,30))
                while okay != True:
                    message_display("You died. Remaining lives: {}".format(self.lives),width/2-10,height/2,50,BLACK)
                    message_display(("Respawn"),width/2-30,height/2+65,20,BLACK)
                    message_display(("Quit"),width/2-30,height/2+115,20,BLACK)
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 1:
                                (x,y) = pygame.mouse.get_pos()
                                if x > okButton.left and x < okButton.right:
                                    if y > okButton.top and y < okButton.bottom:
                                        okay=True
                                if x > quitButton.left and x < quitButton.right:
                                    if y > quitButton.top and y < quitButton.bottom:
                                        okay=True
                                        exitMenu()
                draw_objects(level1,630,400,"L1")
                self.Status=True
                self.health=self.maxhealth

            self.rect.x = 300
            self.rect.y = 300
            self.health = self.maxhealth
            self.Status = True

    #Used to drop all of the Character's items, usually after dying.
    def dropItems(self):
        for item in self.itemsOwned:
            if item == "Gold":
                create_ground_item(self.rect.x,self.rect.y,(255,215,0),"Gold")

    #Used to give the Characters animated movements.
    def updateImages(self,direction):
        if direction == "left":
            if self.frameCount == 1:
                self.image = pygame.image.load(self.runningLeft[0])
            elif self.frameCount == 10:
                self.image = pygame.image.load(self.runningLeft[1])
            elif self.frameCount == 19:
                self.frameCount = 0
        if direction == "right":
            if self.frameCount == 1:
                self.image = pygame.image.load(self.runningRight[0])
            elif self.frameCount == 10:
                self.image = pygame.image.load(self.runningRight[1])
            elif self.frameCount == 19:
                self.frameCount = 0
        if direction == "up":
            if self.frameCount == 1:
                self.image = pygame.image.load(self.runningUpwards[0])
            elif self.frameCount == 10:
                self.image = pygame.image.load(self.runningUpwards[1])
            elif self.frameCount == 19:
                self.frameCount = 0
        if direction == "down":
            if self.frameCount == 1:
                self.image = pygame.image.load(self.runningDownwards[0])
            elif self.frameCount == 10:
                self.image = pygame.image.load(self.runningDownwards[1])
            elif self.frameCount == 19:
                self.frameCount = 0        
        if direction == "idle":
            self.image=self.idleImage
            self.frameCount=0

    #Used to create an EnergyAttack object that the Character will fire.
    def ray(self,mx,my):
        rx = self.rect.x
        ry = self.rect.y

        if self.charType == "B":
            rx+=45
            ry+=45

        playerVec = vec1(rx,ry)
        mouseVec = vec1(mx,my)

        resultVec1 = mouseVec-playerVec

        resultVec = resultVec1.normalize() * 5

        attackVec = EnergyAttack(playerVec, resultVec, self.charType)

        if self.charType == "B":
            attackVec.charged = True

#Player class for creating the player.
class Player(Character):
    def __init__(self):
        self.image = "Player1.png"
        self.attackDMG = 10
        self.health = 50
        maxhealth=50
        lives=3
        self.rL = ["runningL1.png","runningL2.png"]
        self.rR = ["runningR1.png","runningR2.png"]
        self.rU = ["runningU1.png","runningU2.png"]
        self.rD = ["runningD1.png","runningD2.png"]
        self.charType = "P"
        itemsOwned=[]
        super().__init__(self.image,self.health,self.attackDMG,self.charType,self.rL,self.rR,self.rU,self.rD,itemsOwned,lives,maxhealth)
        sprites_List.add(self)

    #Used to handle interactions between the player and Doors, ShopItem objects.
    def interact(self):
        for door in doors:
            if self.rect.right==door.rect.left:
                if self.rect.y > door.rect.y-30 and self.rect.y < door.rect.y+30:
                    if door.LLN == "L10":
                        if gotAllKeys() == True:
                            draw_objects(door.levelLink,door.Lx,door.Ly,door.LLN)
                    else:
                        draw_objects(door.levelLink,door.Lx,door.Ly,door.LLN)
                        

            if self.rect.left==door.rect.right:
                if self.rect.y > door.rect.y-30 and self.rect.y < door.rect.y+30:
                    if door.LLN == "L10":
                        if gotAllKeys() == True:
                            draw_objects(door.levelLink,door.Lx,door.Ly,door.LLN)
                    else:
                        draw_objects(door.levelLink,door.Lx,door.Ly,door.LLN)

            if self.rect.top==door.rect.bottom:
                if self.rect.x > door.rect.x-30 and self.rect.x < door.rect.x+30:
                    if door.LLN == "L10":
                        if gotAllKeys() == True:
                            draw_objects(door.levelLink,door.Lx,door.Ly,door.LLN)
                    else:
                        draw_objects(door.levelLink,door.Lx,door.Ly,door.LLN)

            if self.rect.bottom==door.rect.top:
                if self.rect.x > door.rect.x-30 and self.rect.x < door.rect.x+30:
                    if door.LLN == "L10":
                        if gotAllKeys() == True:
                            draw_objects(door.levelLink,door.Lx,door.Ly,door.LLN)
                    else:
                        draw_objects(door.levelLink,door.Lx,door.Ly,door.LLN)

        if CurrentLevelName == "LS":
            playerGold=0
            for item in player.itemsOwned:
                if item == "Gold":
                    playerGold+=1
            for SI in ShopItems:
                if self.rect.right==SI.rect.left:
                    if self.rect.y > SI.rect.y-30 and self.rect.y < SI.rect.y+30:
                         SI.Open(playerGold)                         

                if self.rect.left==SI.rect.right:
                    if self.rect.y > SI.rect.y-30 and self.rect.y < SI.rect.y+30:
                         SI.Open(playerGold)

                if self.rect.top==SI.rect.bottom:
                    if self.rect.x > SI.rect.x-30 and self.rect.x < SI.rect.x+30:
                         SI.Open(playerGold)
                         
                if self.rect.bottom==SI.rect.top:
                    if self.rect.x > SI.rect.x-30 and self.rect.x < SI.rect.x+30:
                         SI.Open(playerGold)

#EnergyAttack class used to create EnergyAttack objects.
class EnergyAttack(pygame.sprite.Sprite):
    def __init__(self,posVec,resVec,shooter):
        self.image = pygame.image.load("EnergyAttack.png")
        self.posVec = posVec
        self.resVec = resVec
        self.shooter = shooter
        self.rect = pygame.Rect(posVec.x,posVec.y,30,30)
        self.damage = 5
        self.used = False
        self.charged = False
        super().__init__()
        sprites_List.add(self)
        EnergyAttacks.append(self)

    #Used to update the position of the EnergyAttack object.
    def update(self):
        if self.charged != False:
            self.move(self.resVec)

    #Used to decide how to move the EnergyAttack object based on its resultant vector.
    def move(self,resVec):
        if resVec.x != 0:
            self.move_axis(resVec.x,0)
        if resVec.y != 0:
            self.move_axis(0,resVec.y)

    #Used to calculate the damage of an EnergyAttack object.
    def calcDamage(self,chargeCount):
        seconds = math.floor((chargeCount/60))
        for i in range(0,seconds):
            self.damage = self.damage*2

    #Used to move an EnergyAttack object and handle its collisions.
    def move_axis(self,dx,dy):
        self.rect.x += dx
        self.rect.y += dy

        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if self in EnergyAttacks:
                    EnergyAttacks.remove(self)
                self.kill()

        for char in Characters:
            if char.charType != self.shooter:
                if self.used != True:
                    if self.rect.colliderect(char.rect):
                        if char.Status == True:
                            char.takeDamage(self.damage)
                            self.used = True
                            if self in EnergyAttacks:
                                EnergyAttacks.remove(self)
                            self.kill()

#Boss class for creating the boss.
class Boss(Character):
    def __init__(self,x,y):
        self.image = "Boss.png"
        self.attackDMG = 30
        self.rL = ["Boss.png","Boss.png"]
        self.rR = ["Boss.png","Boss.png"]
        self.rU = ["Boss.png","Boss.png"]
        self.rD = ["Boss.png","Boss.png"]
        self.health = 1000000000
        maxhealth = 1000000000
        lives=3
        itemsOwned = []
        self.charType = "B"
        super().__init__(self.image,self.health,self.attackDMG,self.charType,self.rL,self.rR,self.rU,self.rD,itemsOwned,lives,maxhealth)
        self.rect.x = x
        self.rect.y = y
        BossList.append(self)

#Enemy class for creating Enemies.
class Enemy(Character):
    def __init__(self,x,y,lvlOn):
        self.image = "Enemy.png"
        self.attackDMG = 10
        self.rL = ["enemyL1.png","enemyL2.png"]
        self.rR = ["enemyR1.png","enemyR2.png"]
        self.rU = ["enemyU1.png","enemyU2.png"]
        self.rD = ["enemyD1.png","enemyD2.png"]
        self.health = 50
        self.spawnX=x
        self.spawnY=y
        maxhealth=50
        lives=1
        self.lvlOn = lvlOn
        itemsOwned=[]
        ranNum=random.randint(1,3)
        for i in range(0,ranNum):
            itemsOwned.append("Gold")
        self.charType = "E"
        super().__init__(self.image,self.health,self.attackDMG,self.charType,self.rL,self.rR,self.rU,self.rD,itemsOwned,lives,maxhealth)
        self.rect.x = x
        self.rect.y = y
        Enemies.append(self)

    #Used to move the enemy to the player if it is in the enemy's range.
    def goToPlayer(self):
        if self.Status == True:
            if player.Status == True:
                if player.rect.x>self.rect.x-300 and player.rect.x<self.rect.x+300:
                    if player.rect.y>self.rect.y-300 and player.rect.y<self.rect.y+300:
                        if self.rect.x > player.rect.x+30:
                            self.move(-3,0,"left")
                        elif self.rect.x < player.rect.x-30:
                            self.move(+3,0,"right")
                        if self.rect.y < player.rect.y-30:
                            self.move(0,+3,"down")
                        elif self.rect.y > player.rect.y+30:
                            self.move(0,-3,"up")
                else:
                    if self.rect.x>self.spawnX:
                        self.move(-3,0,"left")
                    elif self.rect.x<self.spawnX:
                        self.move(3,0,"right")
                    elif self.rect.y<self.spawnY:
                        self.move(0,3,"down")
                    elif self.rect.y>self.spawnY:
                        self.move(0,-3,"up")

    #Used to find the closest node to the enemy for use in the A* pathfinding algorithm.
    def findClosestNode(self):
        rect1 = pygame.Rect(self.rect.x,self.rect.y,30,30)
        rect1.x = self.rect.x
        rect1.y = self.rect.y
        while rect1.x%30 != 0:
            rect1.x-=1
        while rect1.y%30 != 0:
            rect1.y-=1

        closeNodes = []

        for i in range(0,4):
            visited = False
            while visited == False:
                if i == 0:
                    rect1.x-=30
                if i == 1:
                    rect1.x+=30
                if i == 2:
                    rect1.y-=30
                if i == 3:
                    rect1.y+=30
                    
                for wall in walls:
                    if rect1.colliderect(wall.rect):
                        visited = True

                for node in Nodes:
                    if rect1.x == node.x:
                        if rect1.y == node.y:
                            closeNodes.append(node)
                            visited = True
            rect1.x = self.rect.x
            rect1.y = self.rect.y
            while rect1.x%30 != 0:
                rect1.x-=1
            while rect1.y%30 != 0:
                rect1.y-=1

        lowestDist = 100000000

        for node in closeNodes:
            dist = node.distToPlayer()
            if dist<lowestDist:
                lowestDist = dist
                closestNodeName = node.name
                closestNode = node

        return closestNode

    #Used to start off the pathfinding algorithm.
    def findNodes(self):
        global queue
        queue = PriorityQueue()

        closestNodeToEnemy = self.findClosestNode()
        closestNodeToPlayer = closest_node_to_player()

        for node in Nodes:
            currDist = 999999
            heuristic = node.distToOtherNode(closestNodeToPlayer)
            if node == closestNodeToEnemy:
                combined = heuristic
                currDist = 0
            else:
                combined = 999999
                currDist = 999999
            comingFrom = ""
                
            tuple1 = (node,currDist,heuristic,combined,comingFrom)
            queue.insert(tuple1)

        self.findPath(closestNodeToEnemy,closestNodeToPlayer)

    #Used to find the whole path.
    def findPath(self,closestNodeToEnemy,closestNodeToPlayer):
        nodeToExpand = queue.delete()
        if nodeToExpand[0].playerInSights() == True:
            self.findEndPath()

        else:
            for node in nodeToExpand[0].neighbours:
                newCurrDist = node.distToOtherNode(nodeToExpand[0])
                newHeuristic = node.distToOtherNode(closestNodeToPlayer)
                newCombined = newCurrDist+newHeuristic
                newComingFrom = nodeToExpand[0].name
                newTuple = (node,newCurrDist,newHeuristic,newCombined,newComingFrom)
                if newCombined < queue.currentCombined(node):
                    queue.change(node,newTuple)

            self.findPath(closestNodeToEnemy,closestNodeToPlayer)

    #Used to change the path into names of nodes.
    def findEndPath(self):
        nodeList=[]
        endList = queue.finishedList
        finishedList=endList
        for i in finishedList:
            if i[0].playerInSights() == True:
                nodeBeforeEnd = i[0].name
                nodeList.append(nodeBeforeEnd)

        self.reversePath(nodeList,finishedList)

    #Used to get the path in the correct order for the Enemy to follow.
    def reversePath(self,nodeList,finishedList):
        lastNode = (len(nodeList)-1)
        node = nodeList[lastNode]
        if node == "":
            self.finalPath(nodeList)
        else:
            for i in finishedList:
                if i[0].name == node:
                    nodeList.append(i[4])
                    self.reversePath(nodeList,finishedList)

    #Used to generate the final list of node rectangles for the Enemy to follow.
    def finalPath(self,nodeList):
        for i in nodeList:
            if i == "":
                nodeList.remove(i)

        nodeList = nodeList[::-1]
        global pathRects
        pathRects = []
    
        for i in nodeList:
            for node in Nodes:
                if node.name==i:
                    rect1 = node.rect
                    pathRects.append(rect1)

        global pathFound
        pathFound = True

        self.currentNode = 0

    #Used to move between nodes and follow, attack player if in range.
    def followPath(self):
        if self.Status == True:
            if self.currentNode < len(pathRects):
                node = pathRects[self.currentNode]
                
                if self.rect.x < node.x:
                    self.move(+5,0,"right")
                if self.rect.x > node.x:
                    self.move(-5,0,"left")
                if self.rect.y < node.y:
                    self.move(0,+5,"down")
                if self.rect.y > node.y:
                    self.move(0,-5,"up")
                if self.rect.colliderect(node):
                    self.currentNode+=1

            if self.currentNode == (len(pathRects)):
                lastNode = pathRects[self.currentNode-1] 
                for n in Nodes:
                    if lastNode == n.rect:
                        if n.playerInSights() == True:
                            if self.rect.x < player.rect.x:
                                self.move(+5,0,"right")
                            if self.rect.x > player.rect.x:
                                self.move(-5,0,"left")
                            if self.rect.y < player.rect.y:
                                self.move(0,+5,"down")
                            if self.rect.y > player.rect.y:
                                self.move(0,-5,"up")

            if tickCounter%60 == 0:
                if player.rect.x < self.rect.x+60 and player.rect.x > self.rect.x-60:
                    if player.rect.y < self.rect.y+60 and player.rect.y > self.rect.y-60:
                        self.attack(player)
                                    
#Class to implement a priority queue for use in the A* pathfinding algorithm.                                
class PriorityQueue(object):
    def __init__(self): 
        self.queue = []
        self.finishedList = []
        
    #Used to return the current combined distance of a node.
    def currentCombined(self,item):
        for i in self.queue:
            if i[0].name == item.name:
                returned = i[3]
                return returned
        for i in self.finishedList:
            if i[0].name == item.name:
                returned = i[3]
                return returned

    #Used to add data to the queue.
    def insert(self, data): 
        self.queue.append(data) 

    #Used to return the item with the highest priority and remove it from the queue.
    def delete(self): 
        min = 0
        for i in range(len(self.queue)): 
            if self.queue[i][3] < self.queue[min][3]: 
                min = i 
        item = self.queue[min]
        self.finishedList.append(item)
        del self.queue[min]
        return item

    #Used to swap a tuple in the queue for one that's passed in.
    def change(self,changedItem,newItem):
        for i in range(len(self.queue)):
            if self.queue[i][0] == changedItem:
                self.queue[i] = newItem

#Node class for creating Node objects, for use in pathfinding.
class Node():
    def __init__(self,x,y,name):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x,self.y,30,30)
        self.neighbours = []
        self.name = name
        Nodes.append(self)

    #Returns the distance from the Node object to the player (manhattan method)
    def distToPlayer(self):
        xDist = abs(player.rect.x-self.x)
        yDist = abs(player.rect.y-self.y)
        totalDist = xDist+yDist
        return totalDist

    #Used to find the node object's immediate neighbours.
    def findNeighbours(self):
        rect1 = pygame.Rect(self.x,self.y,30,30)
        rect1.x = self.x
        rect1.y = self.y

        for i in range(0,4):
            visited = False
            while visited == False:
                if i == 0:
                    rect1.x-=30
                if i == 1:
                    rect1.x+=30
                if i == 2:
                    rect1.y-=30
                if i == 3:
                    rect1.y+=30
                    
                for wall in walls:
                    if rect1.colliderect(wall.rect):
                        visited = True
                for node in Nodes:
                    if node != self:
                        if rect1.x == node.x:
                            if rect1.y == node.y:
                                self.neighbours.append(node)
                                visited = True
            rect1.x = self.x
            rect1.y = self.y

    #Used to check if the player is nearby to the Node object.
    def playerInSights(self):
        rect1 = pygame.Rect(self.x,self.y,30,30)
        rect1.x = self.x
        rect1.y = self.y
        inSights = False

        for i in range(0,4):
            visited = False
            while visited == False:
                if i == 0:
                    rect1.x-=30
                if i == 1:
                    rect1.x+=30
                if i == 2:
                    rect1.y-=30
                if i == 3:
                    rect1.y+=30
                    
                for wall in walls:
                    if rect1.colliderect(wall.rect):
                        visited = True

                for node in Nodes:
                    if rect1.colliderect(node.rect):
                        visited = True

                if rect1.colliderect(player.rect):
                    inSights = True
                    visited = True

            rect1.x = self.x
            rect1.y = self.y

        return inSights

    #Used to find the distance between the Node and another Node.
    def distToOtherNode(self,otherNode):
        xDist = abs(self.rect.x-otherNode.rect.x)
        yDist = abs(self.rect.y-otherNode.rect.y)
        totalDist = xDist+yDist

        return totalDist
                                
os.environ["SDL_VIDEO_CENTERED"] = "1"
mapBought = False
pygame.init()
WHITE = (255,255,255)
BLACK = (0,0,0)
BROWN = (166,101,13)
RED = (255,0,0)

vec1 = pygame.math.Vector2
startTime = ()
attackCount=0
chargeCount=0
Charging = False

width=1260 
height=930

Nodes=[]

Items=[]
doors=[]
Characters=[]
Enemies = []
ShopItems=[]
EnergyAttacks=[]
BossList=[]

screen = pygame.display.set_mode((width,height))
screen.fill(WHITE)

sprites_List = pygame.sprite.Group()
player = Player()

level1 = levels.level1
level2 = levels.level2
level3 = levels.level3
level4 = levels.level4
level5 = levels.level5
level6 = levels.level6
level7 = levels.level7
level8 = levels.level8
level9 = levels.level9
level10 = levels.level10
levelSHOP = levels.levelSHOP
levelMAP = levels.levelMAP

damageTimer = 0

clock = pygame.time.Clock() 

#Used to create all of the door objects for each level.
def draw_doors(Level,Ln):
    global doors
    doors=[]
    if Ln == "L1":
        door1 = Door(0,225,level2,1207,450,"L2")
        door2 = Door(900,0,level3,607,865,"L3")
        door3 = Door(1230,675,level4,37,450,"L4")
        door4 = Door(300,900,level5,607,38,"L5")
        doorSHOP = Door(30,30,levelSHOP,600,435,"LS")
        
    if Ln == "L2":
        door5 = Door(1230,450,level1,38,225,"L1")
        door9 = Door(0,200,level6,635,450,"L6")

    if Ln == "L3":
        door6 = Door(600,900,level1,907,38,"L1")
        door10 = Door(300,0,level7,607,865,"L7")
        door11 = Door(1230,675,level8,37,450,"L8")

    if Ln == "L4":
        door7 = Door(0,450,level1,1205,675,"L1")
        door12 = Door(1230,675,level9,37,450,"L9")

    if Ln == "L5":
        door8 = Door(600,0,level1,307,862,"L1")
        door13 = Door(600,900,level10,607,38,"L10")

    if Ln == "LS":
        doorSHOP = Door(30,30,level1,60,60,"L1")

    if Ln == "L6":
        door14 = Door(450,60,level2,43,200,"L2")

    if Ln == "L7":
        door15 = Door(1230,204,level3,300,50,"L3")

    if Ln == "L9":
        door16 = Door(0,255,level4,1200,675,"L4")

#Used to create dropped items that can be picked up.
def create_ground_item(x,y,colour,name):
    rect=(screen, (colour), (x,y,15,15),name)
    Items.append(rect)

#Used to create all of the Enemy objects.
def create_enemies():
    enemy1 = Enemy(600,450,"L2")
    enemy2 = Enemy(607,165,"L3")
    enemy3 = Enemy(400,450,"L4")
    enemy4 = Enemy(607,800,"L5")
    enemy5 = Enemy(360,570,"L6")
    enemy6 = Enemy(300,300,"L2")
    enemy7 = Enemy(400,600,"L2")
    enemy8 = Enemy(600,100,"L2")
    enemy9 = Enemy(600,200,"L3")
    enemy10 = Enemy(900,200,"L3")
    enemy11 = Enemy(100,300,"L3")
    enemy12 = Enemy(900,500,"L4")
    enemy13 = Enemy(750,100,"L4")
    enemy14 = Enemy(100,100,"L4")
    enemy15 = Enemy(800,800,"L5")
    enemy16 = Enemy(300,800,"L5")
    enemy17 = Enemy(400,400,"L5")
    Boss1 = Boss(300,300)

#Used to "activate" Enemy objects.
def place_enemies(Ln):
    for enemy in Enemies:
        if enemy.lvlOn == Ln:
            enemy.Status=True
        elif enemy.lvlOn != Ln:
            enemy.Status=False
            enemy.kill()
            
#Used to create text images and rectangles.
def text_objects(text,font,colour):
    textSurface = font.render(text, True, colour)
    return textSurface, textSurface.get_rect()

#Used to find the closest Node object to the player object.
def closest_node_to_player():
    min = 10000
    for node in Nodes:
        if node.playerInSights() == True:
            dist = node.distToPlayer()
            if dist < min:
                min = dist
                closestNode = node
    return closestNode

#Used to display messages on the screen.
def message_display(text,x,y,size,colour):
    largeText = pygame.font.Font("freesansbold.ttf",size)
    TextSurf, TextRect = text_objects(text, largeText,colour)
    TextRect.center= (x,y)
    screen.blit(TextSurf, TextRect)
    pygame.display.update()

PreviousLevelName=()
CurrentLevelName=()
PreviousLevel=()
CurrentLevel=()

loadingSave = False

#Used to switch between levels.
def draw_objects(Level,Px,Py,Ln):
    global Items
    Items=[]

    global CurrentLevelName
    CurrentLevelName = Ln

    global CurrentLevel
    CurrentLevel = Level

    global walls
    walls = []

    global ShopItems
    ShopItems=[]

    Boss1 = BossList[0]
    if Ln == "L10":
        Boss1.Status = True
    else:
        Boss1.Status = False
        Boss1.kill()

    for attack in EnergyAttacks:
        if attack in EnergyAttacks:
            attack.kill()
    EnergyAttacks.clear()
    
    x=y=0
    player.rect.x=Px
    player.rect.y=Py

    count=1
    
    for row in Level:
        for col in row:
            if col == "W":
                Wall(x, y,False)
            if col == "D":
                Wall(x,y,True)
            if col == "N":
                NodeName = ("Node"+"{}".format(count))
                Node(x,y,NodeName)
                count+=1
                
            x+=30
        y+=30
        x=0
    draw_doors(Level,Ln)
    place_enemies(Ln)
    place_keys(Ln)

    if Ln == "LS":
        create_shop()
    if Ln == "L6":
        mazeInstructions()
        global startTime
        startTime = datetime.datetime.now()
        for node in Nodes:
            node.findNeighbours()
        global pathFound
        pathFound = False
        global tickCounter
        tickCounter = 0

    if Ln == "L7":
        disMazeInstructions()
        startTime = datetime.datetime.now()
    if Ln == "L8":
        waveInstructions()
        global currentWave
        currentWave = 0
        global checkCount
        checkCount = 0
        global amountOfEnemies
        amountOfEnemies = 1
        global EnemiesAlive
        EnemiesAlive = 1
        global key3Placed
        key3Placed = False
    if Ln == "LM":
        player.Status = False    
    else:
        player.Status = True

def main_menu_screen():
    start=False
    while start != True:
        message_display("Game1",width/2,height/2,100,BLACK)
        rect2 = pygame.draw.rect(screen, (208,208,208), ((width/2-140),(height/2+70),280,40))
        message_display("New Game",(630),(555),30,BLACK)
        rect3 = pygame.draw.rect(screen, (208,208,208), ((width/2-140),(height/2+120),280,40))
        message_display("Load Game",(630),(610),30,BLACK)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    (x,y) = pygame.mouse.get_pos()
                    if x > rect2.left and x < rect2.right:
                        if y > rect2.top and y < rect2.bottom:
                            start = True
                    if x > rect3.left and x < rect3.right:
                        if y > rect3.top and y < rect3.bottom:
                            start = True
                            global loadingSave
                            loadingSave = True

#Used to check if the player has got all of the keys.
def gotAllKeys():
    GotK1 = False
    GotK2 = False
    GotK3 = False
    for i in player.itemsOwned:
        if i == "Key1":
            GotK1 = True
        if i == "Key2":
            GotK2 = True
        if i == "Key3":
            GotK3 = True

    if GotK1 == True and GotK2 == True and GotK3 == True:
        return True
    else:
        getAllKeys()
        return False

def getAllKeys():
    start=False
    screen.fill(WHITE)
    while start != True:
        okButton = pygame.draw.rect(screen, (0,255,0), ((width/2-75),(height/4+510),100,30))
        message_display("Ok",width/2-30,height/4+525,25,BLACK)
        message_display("You need all 3 keys to enter this level.",width/2-10,height/4-80,50,BLACK)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    (x,y) = pygame.mouse.get_pos()
                    if x > okButton.left and x < okButton.right:
                        if y > okButton.top and y < okButton.bottom:
                            start = True
    
def instructions():
    start=False
    screen.fill(WHITE)
    while start != True:
        okButton = pygame.draw.rect(screen, (0,255,0), ((width/2-75),(height/4+510),100,30))
        message_display("Ok",width/2-30,height/4+525,25,BLACK)
        message_display("Instructions",width/2-10,height/4-80,50,BLACK)
        message_display("W,A,S and D move the player up, left, down and right respectively.",width/2-30,height/4,25,BLACK)
        message_display("To interact with doors and the shop's item doors, press E.",width/2-30,height/4+60,25,BLACK)
        message_display("Doors are shown as brown squares:",width/2-30,height/4+120,25,BLACK)
        doorExample = pygame.draw.rect(screen, (BROWN), ((width/2+200),(height/4+105),30,30))
        message_display("The entrance to the shop is shown as a red square, and an item door is shown as a blue square:",width/2-30,height/4+180,25,BLACK)
        shopExample = pygame.draw.rect(screen, (255,0,0), ((width/2+560),(height/4+165),30,30))
        shopExample2 = pygame.draw.rect(screen, (0,0,255), ((width/2+595),(height/4+165),30,30))
        message_display("To attack an enemy, use left click for close range and right click for an energy attack.",width/2-30,height/4+240,25,BLACK)
        message_display("You can only attack an enemy that is close to you. Press R to use a Med. (Restores 10HP)",width/2-30,height/4+300,25,BLACK)
        message_display("You get 3 lives. When you die, your remaining lives will be displayed on screen.",width/2-30,height/4+360,25,BLACK)
        message_display("To access the Map (if you own it), press M. The Map cannot be used while you are in the Shop.",width/2-30,height/4+420,25,BLACK)
        message_display("To view your inventory, press Q. You can get Gold by killing Enemies and finding it in mazes.",width/2-30,height/4+480,25,BLACK)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    (x,y) = pygame.mouse.get_pos()
                    if x > okButton.left and x < okButton.right:
                        if y > okButton.top and y < okButton.bottom:
                            start = True

def mazeInstructions():
    start = False
    screen.fill(WHITE)
    while start != True:
        okButton = pygame.draw.rect(screen, (0,255,0), ((width/2-75),(height/2+120),100,30))
        message_display("Ok",width/2-25,height/2+135,25,BLACK)
        message_display("The maze",width/2-30,height/2-20,30,BLACK)
        message_display("You have 25 seconds to complete the maze.",width/2-10,height/2+10,30,BLACK)
        message_display("Try to get the key shown by the grey rectangle.",width/2-10,height/2+50,30,BLACK)
        message_display("The exit is indicated by the brown door.", width/2-10,height/2+90,30,BLACK)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    (x,y) = pygame.mouse.get_pos()
                    if x > okButton.left and x < okButton.right:
                        if y > okButton.top and y < okButton.bottom:
                            start = True

def disMazeInstructions():
    start = False
    screen.fill(WHITE)
    while start != True:
        okButton = pygame.draw.rect(screen, (0,255,0), ((width/2-75),(height/2+120),100,30))
        message_display("Ok",width/2-25,height/2+135,25,BLACK)
        message_display("The disappearing maze",width/2-30,height/2-20,30,BLACK)
        message_display("You have 10 seconds to look at the maze before it disappears.",width/2-10,height/2+10,30,BLACK)
        message_display("Try to get the key shown by the grey rectangle.",width/2-10,height/2+50,30,BLACK)
        message_display("The exit is indicated by the brown door.", width/2-10,height/2+90,30,BLACK)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    (x,y) = pygame.mouse.get_pos()
                    if x > okButton.left and x < okButton.right:
                        if y > okButton.top and y < okButton.bottom:
                            start = True

def waveInstructions():
    start = False
    screen.fill(WHITE)
    while start != True:
        okButton = pygame.draw.rect(screen, (0,255,0), ((width/2-75),(height/2+120),100,30))
        message_display("Ok",width/2-25,height/2+135,25,BLACK)
        message_display("The wave survival game",width/2-30,height/2-20,30,BLACK)
        message_display("You have to try to defeat 4 waves of enemies.",width/2-10,height/2+10,30,BLACK)
        message_display("If you beat all 4 waves, a key will be spawned for you to take.",width/2-10,height/2+50,30,BLACK)
        message_display("The exit is indicated by the brown door (when you win).", width/2-10,height/2+90,30,BLACK)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    (x,y) = pygame.mouse.get_pos()
                    if x > okButton.left and x < okButton.right:
                        if y > okButton.top and y < okButton.bottom:
                            start = True

def escMenu():
    decisionMade = False
    decision = ""
    screen.fill(WHITE)
    while decisionMade != True:
        resumeButton = pygame.draw.rect(screen, (0,255,0), ((width/2-360),(height/3+82),225,35))
        message_display("Resume game",width/2-250,height/3+100,30,BLACK)
        exitButton = pygame.draw.rect(screen, (255,0,0), ((width/2+130), (height/3+82),180,35))
        message_display("Exit game",width/2+220,height/3+100,30,BLACK)
        message_display("Game paused.",width/2-10,height/3,50,BLACK)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    (x,y) = pygame.mouse.get_pos()
                    if x > resumeButton.left and x < resumeButton.right:
                        if y > resumeButton.top and y < resumeButton.bottom:
                            decisionMade = True
                            decision = "RESUME"
                    if x > exitButton.left and x < exitButton.right:
                        if y > exitButton.top and y < exitButton.bottom:
                            decisionMade = True
                            decision = "EXIT"

        if decision == "RESUME":
            pass

        if decision == "EXIT":
            exitMenu()

def exitMenu():
    decisionMade = False
    decision = ""
    screen.fill(WHITE)
    while decisionMade != True:
        saveButton = pygame.draw.rect(screen, (208,208,208), ((width/2-360),(height/3+82),225,35))
        message_display("Save game",width/2-250,height/3+100,30,BLACK)
        noSaveButton = pygame.draw.rect(screen, (208,208,208), ((width/2+30), (height/3+82),390,35))
        message_display("Exit game without saving",width/2+230,height/3+100,30,BLACK)
        message_display("Would you like to save your progress?",width/2-10,height/3,50,BLACK)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    (x,y) = pygame.mouse.get_pos()
                    if x > saveButton.left and x < saveButton.right:
                        if y > saveButton.top and y < saveButton.bottom:
                            decisionMade = True
                            decision = "SAVE"
                    if x > noSaveButton.left and x < noSaveButton.right:
                        if y > noSaveButton.top and y < noSaveButton.bottom:
                            decisionMade = True
                            decision = "QUIT"
        
        if decision == "QUIT":
            global running
            running = False

        if decision == "SAVE":
            saveScreen()

def saveScreen():
    screen.fill(WHITE)
    done=False
    while done != True:
        okButton = pygame.draw.rect(screen, (0,255,0), ((width/2-98),(height/2+140),100,35))
        message_display("Ok",width/2-50,height/2+160,30,BLACK)
        message_display("Enter save name using keyboard.",width/2-30,height/2-20,30,BLACK)
        message_display("Press the enter key when you have finished typing.",width/2-30,height/2+20,30,BLACK)
        message_display("Press the backspace key to delete characters.",width/2-30,height/2+60,30,BLACK)
        message_display("Either hold shift or activate caps lock to use capital letters.",width/2-30,height/2+100,30,BLACK)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    (x,y) = pygame.mouse.get_pos()
                    if x > okButton.left and x < okButton.right:
                        if y > okButton.top and y < okButton.bottom:
                            done = True

    enteringName()

def enteringName():
    screen.fill(WHITE)
    string1=""
    keys = [pygame.K_a,
    pygame.K_b,pygame.K_c,pygame.K_d,pygame.K_e,pygame.K_f,pygame.K_g,pygame.K_h,pygame.K_i,pygame.K_j,pygame.K_k,
    pygame.K_l,pygame.K_m,pygame.K_n,pygame.K_o,pygame.K_p,pygame.K_q,pygame.K_r,pygame.K_s,pygame.K_t,pygame.K_u,
    pygame.K_v,pygame.K_w,pygame.K_x,pygame.K_y,pygame.K_z,
    pygame.K_0,pygame.K_1,pygame.K_2,pygame.K_3,pygame.K_4,pygame.K_5,pygame.K_6,pygame.K_7,pygame.K_8,pygame.K_9]
    done = False
    holdingShift = False
    capsLock = False
    while done != True:
        screen.fill(WHITE)
        message_display("{}".format(string1),width/2-30,height/2,30,BLACK)
        for event in pygame.event.get():
            
            if event.type == pygame.KEYDOWN:
                key1 = pygame.key.get_pressed()

                if key1[pygame.K_LSHIFT] == True:
                    holdingShift = True
                elif key1[pygame.K_LSHIFT] == False:
                    holdingShift = False
    
                if key1[pygame.K_CAPSLOCK] == True:
                    capsLock = True
                elif key1[pygame.K_CAPSLOCK] == False:
                    capsLock = False

                if key1[pygame.K_SPACE] == True:
                    string1 = string1+" "

                for key in keys:
                    if key1[key] == True:
                        keyName = pygame.key.name(key)
                        
                        if capsLock == True or holdingShift == True:
                            keyName = keyName.capitalize()

                        string1 = string1+keyName
                            
                if key1[pygame.K_RETURN] == True:
                    done = True
                    
                if key1[pygame.K_BACKSPACE] == True:
                    try:
                        string1 = string1[:-1]
                    except:
                        pass

    addToDbase(string1)

#Used to add saves to the database.
def addToDbase(save_name):
    mapOwned=False
    goldCount=0
    medCount=0
    overwriteCount = 0
    if player.lives!=0:  
        for i in range(0,len(player.itemsOwned)):
            if player.itemsOwned[i] == "Map":
                mapOwned=True
            if player.itemsOwned[i] == "Gold":
                goldCount+=1
            if player.itemsOwned[i] == "Med":
                medCount+=1
        lives = player.lives
        health = player.health
        added=False
        for i in (view_table_values("Saves")):
            if save_name == i[0]:

                if overwriteCount < 1:
                    overwriteResponse = overwrite()
                    overwriteCount+=1

                if overwriteResponse == "Y":
                    delete_save(save_name)
                    add_save(save_name,mapOwned,goldCount,lives,health,key1Found,key2Found,key3Found,medCount)
                    added=True
                    
                if overwriteResponse == "N":
                    add_save(save_name,mapOwned,goldCount,lives,health,key1Found,key2Found,key3Found,medCount)
                    added=True

        if added != True:
            add_save(save_name,mapOwned,goldCount,lives,health,key1Found,key2Found,key3Found,medCount)
        
    elif player.lives == 0:
        if loadedFromDbase == True:
            delete_save(saveChosen)

    saved(save_name)
    global running
    running = False

def overwrite():
    screen.fill(WHITE)
    done=False
    response=""
    while done != True:
        yesButton = pygame.draw.rect(screen, (0,255,0), ((width/2-200),(height/2+40),100,35))
        message_display("Yes",width/2-160,height/2+60,30,BLACK)
        noButton = pygame.draw.rect(screen, (255,0,0), ((width/2+150),(height/2+40),100,35))
        message_display("No",width/2+200,height/2+60,30,BLACK)
        message_display("Another save has the same name. Overwrite?",width/2,height/2,40,BLACK)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    (x,y) = pygame.mouse.get_pos()
                    if x > yesButton.left and x < yesButton.right:
                        if y > yesButton.top and y < yesButton.bottom:
                            response = "Y"
                            done = True
                    if x > noButton.left and x < noButton.right:
                        if y > noButton.top and y < noButton.bottom:
                            response = "N"
                            done = True

    return response

def saved(save_name):
    screen.fill(WHITE)
    message_display("Game saved under name: {}".format(save_name),width/2,height/2,50,BLACK)
    time.sleep(3)

#Used to load saves from the database.
def load_from_dbase():
    count=0
    for i in (view_table_values("Saves")):
        if i[0] != ():
            count+=1
    if count != 0:
        screen.fill(WHITE)
        keyEntered=()
        num =0
        chosen = False
        global loadedFromDbase
        loadedFromDbase = True
        while chosen != True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                     keyEntered = pygame.key.name(event.key)
                     
            for i in range(0,len(view_table_values("Saves"))):
                messageToShow = view_table_values("Saves")[i][0]
                numberOfSave = str(i+1)
                numberOfSaveShow = (numberOfSave+". ")
                message_display((numberOfSaveShow+messageToShow),width/2,(height/2+(30*i)),20,BLACK)
                if numberOfSave == keyEntered:
                    global saveChosen
                    saveChosen = messageToShow
                    chosen = True
                    num = (i)
        
        if view_table_values("Saves")[num][1] == "True":
            player.itemsOwned.append("Map")
            global mapBought
            mapBought = True

        if view_table_values("Saves")[num][2] != 0:
            for i in range(0,view_table_values("Saves")[num][2]):
                player.itemsOwned.append("Gold")

        if view_table_values("Saves")[num][8] != 0:
            for i in range(0,view_table_values("Saves")[num][8]):
                player.itemsOwned.append("Med")

        if view_table_values("Saves")[num][5] == "True":
            player.itemsOwned.append("Key1")
            global key1Found
            key1Found = True

        if view_table_values("Saves")[num][6] == "True":
            player.itemsOwned.append("Key2")
            global key2Found
            key2Found = True

        if view_table_values("Saves")[num][7] == "True":
            player.itemsOwned.append("Key3")
            global key3Found
            key3Found = True

        player.lives = view_table_values("Saves")[num][3]
        player.health = view_table_values("Saves")[num][4]

        screen.fill(WHITE)
        message_display("Loading: {}".format(saveChosen),width/2,(height/2),50,BLACK)
        time.sleep(2)
    if count == 0:
        screen.fill(WHITE)
        message_display("No saves.",width/2,(height/2),50,BLACK)
        time.sleep(2)
        screen.fill(WHITE)
        main_menu_screen()

#Used to create all of the ShopItem objects for the shop.
def create_shop():
    if mapBought == False:
        mapBuy = ShopItem(3,810,210,"Map")
        mapItem = create_ground_item(817,190,(255,0,0),"Map")

    medBuy = ShopItem(5,390,180,"Med")

#Used to create the keys as ground items.
def place_keys(Ln):
    if Ln == "L6":
        if key1Found == False:
            key1Item = create_ground_item(158,824,(192,192,192),"Key1")
    if Ln == "L7":
        if key2Found == False:
            key2Item = create_ground_item(430,430,(192,192,192),"Key2")

#Used to display the prices of items in the shop.
def display_shop_prices():
    message_display("Buy a Map for 3 Gold.",830,130,20,BLACK)
    message_display("Buy meds for 5 Gold each.",390,130,20,BLACK)

#Used to retrieve the player's inventory and format it to be shown on screen.
def getInv():
    playerInv = player.itemsOwned
    if playerInv == []:
        toShow=["Empty"]
    else:
        GoldCount=0
        MedCount=0
        toShow=[]
        for item in playerInv:
            if item == "Gold":
                GoldCount+=1
            elif item == "Med":
                MedCount+=1
            else:
                toShow.append(item)
        if GoldCount > 0:
            toShow.append("{}x Gold".format(GoldCount))
        if MedCount > 0:
            toShow.append("{}x Meds".format(MedCount))
    return toShow

#Used to decide where to put the red rectangle on the map (that indicates where
#the player is).
def MapCoords():
    xM = 0
    xY = 0
    if PreviousLevelName == "L1":
        xM=485
        xY=359
    if PreviousLevelName == "L2":
        xM = 346
        xY = 379
    if PreviousLevelName == "L3":
        xM = 494
        xY = 258
    if PreviousLevelName == "L4":
        xM = 646
        xY = 373
    if PreviousLevelName == "L5":
        xM = 498
        xY = 497
    if PreviousLevelName == "L6":
        xM = 225
        xY = 379
    if PreviousLevelName == "L7":
        xM = 498
        xY = 140
    if PreviousLevelName == "L8":
        xM = 619
        xY = 253
    if PreviousLevelName == "L9":
        xM = 765
        xY = 377
    if PreviousLevelName == "L10":
        xM = 535
        xY = 593
    return (xM,xY)

def win():
    screen.fill(WHITE)
    message_display("You win.",width/2,height/2,40,(0,255,0))
    time.sleep(3)

main_menu_screen()

key1Found = False
key2Found = False
key3Found = False
key3Placed = False

if loadingSave!= True:
    instructions()
if loadingSave == True:
    load_from_dbase()
    
items1=[]

create_enemies()

bossBlastTimer = 0
bossAttackCount = 0

paused = False
ShowingItems = False
draw_objects(level1,630,400,"L1")
running = True
ShowingMap=False

#Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                player.interact()
            if event.key == pygame.K_ESCAPE:
                escMenu()

            if event.key == pygame.K_q:
                if ShowingItems == True:
                    ShowingItems = False
                elif ShowingItems == False:
                    ShowingItems = True
                items1 = getInv()

            if event.key == pygame.K_m:
                if CurrentLevelName == "LM":
                    screen.fill(WHITE)
                    draw_objects(PreviousLevel,PrevPX,PrevPY,PreviousLevelName)
                    ShowingMap=False
                else:
                    if CurrentLevelName != "L6" and CurrentLevelName != "LM" and CurrentLevelName != "LS" and CurrentLevelName != "L7":
                        if mapBought == True:
                                PreviousLevel=CurrentLevel
                                PreviousLevelName=CurrentLevelName
                                PrevPX=player.rect.x
                                PrevPY=player.rect.y
                                draw_objects(levelMAP,10000,100,"LM")
                                ShowingMap=True

            if event.key == pygame.K_r:
                if player.Status == True:
                    medCount = 0
                    for i in player.itemsOwned:
                        if i == "Med":
                            medCount+=1
                    if medCount>0:
                        player.health+=10
                        player.itemsOwned.remove("Med")
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player.updateImages("idle")
            if event.key == pygame.K_w:
                player.updateImages("idle")
            if event.key == pygame.K_s:
                player.updateImages("idle")
            if event.key == pygame.K_d:
                player.updateImages("idle")
                
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for enemy in Enemies:
                    (x,y) = pygame.mouse.get_pos()
                    if x > enemy.rect.left and x < enemy.rect.right:
                        if y > enemy.rect.top and y < enemy.rect.bottom:
                            player.attack(enemy)

            if event.button == 3:
                Charging=True
                chargeCount = 0

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:
                Charging = False
                (mx,my) = pygame.mouse.get_pos()
                player.ray(mx,my)
                for attack in EnergyAttacks:
                    if attack.charged == False:
                        attack.calcDamage(chargeCount)
                        attack.charged = True

    if Charging:
        chargeCount += 1
            
    user_input = pygame.key.get_pressed()
    
    if user_input[pygame.K_a]:
        player.move(-5,0,"left")
    if user_input[pygame.K_d]:
        player.move(5,0,"right")
    if user_input[pygame.K_w]:
        player.move(0,-5,"up")
    if user_input[pygame.K_s]:
        player.move(0,5,"down")

    if CurrentLevelName != "L6" and CurrentLevelName != "L8":
        attackCount+=1
        for enemy in Enemies:
            if enemy.Status == True:
                enemy.goToPlayer()
                if attackCount%60 == 0:
                    enemy.attack(player)

    for char in Characters:
        if char.Status == True:
            sprites_List.add(char)

    screen.fill(WHITE)

    if CurrentLevelName == "L8":
        checkCount+=1
        if currentWave < 5:
            if checkCount%120 == 0:
                    EnemiesAlive = 0
                    for enemy in Enemies:
                        if enemy.Status == True:
                            EnemiesAlive += 1
                    if EnemiesAlive == 0:
                        currentWave+=1
                        if currentWave != 5:
                            for i in range(1,currentWave):
                                amountOfEnemies = amountOfEnemies+2
                            for i in range(0,amountOfEnemies):
                                ranx = random.randint(40,800)
                                rany = random.randint(40,800)
                                enemy1 = Enemy(ranx,rany,"L8")
            for enemy in Enemies:
                if enemy.Status == True:
                    if enemy.rect.x > player.rect.x+30:
                        enemy.move(-3,0,"left")
                    elif enemy.rect.x < player.rect.x-30:
                        enemy.move(+3,0,"right")
                    if enemy.rect.y < player.rect.y-30:
                        enemy.move(0,+3,"down")
                    elif enemy.rect.y > player.rect.y+30:
                        enemy.move(0,-3,"up")
                    attackCount+=1
                    if attackCount%60 == 0:
                        enemy.attack(player)
        if currentWave >= 5:
            door200 = Door(500,500,level3,1210,675,"L3")
            if key3Found == False:
                if key3Placed == False:
                    key3Item = create_ground_item(430,430,(192,192,192),"Key3")
                    key3Placed = True

    sprites_List.update()
    sprites_List.draw(screen)
    
    for wall in walls:
        pygame.draw.rect(screen, (wall.colour), wall.rect)

    for SI in ShopItems:
        pygame.draw.rect(screen, (SI.colour), SI.rect)
    
    for door in doors:
        pygame.draw.rect(screen, (door.colour), door.rect)

    for item in Items:
        pygame.draw.rect(item[0],item[1],item[2])

    for attack in EnergyAttacks:
        attack.update()

    if Charging == True:
        pygame.draw.rect(screen, (0,50,255), (player.rect.x+3,player.rect.y+5,10,10))
        chargedFor = math.floor(chargeCount/60)
        message_display(("{}".format(chargedFor)),(player.rect.x-5),(player.rect.y-10),20,(0,50,255))

    if ShowingItems:
        mult=0
        for item in items1:
            mult+=15
            if player.rect.x>=width-200:
                InvX=player.rect.x-60
            elif player.rect.x<200:
                InvX=player.rect.x+60
            else:
                InvX=player.rect.x+60
            if player.rect.y<=200:
                InvY=player.rect.y+30
            elif player.rect.y>=height-200:
                InvY=player.rect.y-30
            else:
                InvY=player.rect.y-30
            message_display(item,InvX,InvY+(15+mult),15,BLACK)

    if CurrentLevelName == "LS":
        display_shop_prices()        

    if ShowingMap:
        pX,pY = MapCoords()
        pygame.draw.rect(screen, (255,0,0),( pX, pY, 30,30))

    if CurrentLevelName == "L6":
        tickCounter += 1
        currentTime = (datetime.datetime.now())
        timeDelay = str(currentTime-startTime)
        timeDelay = timeDelay.replace(":","")
        timeDelay = int(timeDelay.replace(".",""))
        timeDelay = timeDelay/1000000
        tDelay = str(timeDelay)
        message = ""
        message+=(tDelay[0])
        try:
            message+=(tDelay[1])
        except:
            pass
        try:
            message+=(tDelay[2])
        except:
            pass
        try:
            message+=(tDelay[3])
        except:
            pass
        message_display("{}".format(message),177,450,30,(0,0,0))
        if timeDelay >= 25:
            player.Die()
        if pathFound == True:
            for enemy in Enemies:
                if enemy.Status == True:
                    enemy.followPath()
        if tickCounter%120 == 0:
            for enemy in Enemies:
                if enemy.Status == True:
                    enemy.findNodes()

    if CurrentLevelName == "L7":
        damageTimer+=1
        currentTime = (datetime.datetime.now())
        timeDelay = str(currentTime-startTime)
        timeDelay = timeDelay.replace(":","")
        timeDelay = int(timeDelay.replace(".",""))
        timeDelay = timeDelay/1000000
        timeDelay = 10-timeDelay
        tDelay = str(timeDelay)
        message = ""
        message+=(tDelay[0])
        message+=(tDelay[1])
        message+=(tDelay[2])
        if timeDelay <= 0:
            for wall in walls:
                wall.disappear()
            player.Status = True
        if timeDelay > 0:
            message_display("{}".format(message),177,450,30,(0,0,0))
            player.Status = False

    if CurrentLevelName == "L8":
        if currentWave < 5:
            message_display("Wave {}".format(currentWave),800,915,30,(0,0,255))

    if CurrentLevelName == "L10":
        message_display("Hint: A 31 second charged energy attack will one shot the boss.",1050,890,10,(0,0,0))
        bossAttackCount+=1
        Boss1 = BossList[0]
        if Boss1.Status == True:
            bossBlastTimer+=1
            if bossBlastTimer>30 and bossBlastTimer<40:
                Boss1.ray(player.rect.x,player.rect.y)
                bossBlastTimer=0
            if Boss1.rect.x < player.rect.x:
                Boss1.move(+2,0,"right")
            if Boss1.rect.x > player.rect.x:
                Boss1.move(-2,0,"left")
            if Boss1.rect.y < player.rect.y:
                Boss1.move(0,+2,"down")
            if Boss1.rect.y > player.rect.y:
                Boss1.move(0,-2,"up")

            if bossAttackCount%120 == 0:
                Boss1.attack(player)
            
    message_display("Health: {}".format(player.health),1100,915,30,(0,255,0))
    
    pygame.display.update()
    clock.tick(60)

pygame.quit() 
