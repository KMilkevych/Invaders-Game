import pygame
from pygame.locals import *
import math
import random
import sys
import os

class InformationTable():

    def __init__(self, frame_width = 2, current_travelpoint = None):
        self.frame_width = frame_width

        if current_travelpoint:
            self.travelpoint = current_travelpoint
        
        self.font = pygame.font.SysFont("Arial", 48)
        self.font_small = pygame.font.SysFont("Arial", 36)
        self.update_text(current_travelpoint)

        ht = "AREA " + str(global_data["area"])
        self.headline_text = self.font_small.render(ht, False, (255, 255, 255))
        self.headline_rect = self.headline_text.get_rect()
        self.headline_rect.center = (window.get_width()/2, 20)

        self.do_misc()


    def draw(self, window):
        global travelpoint_boundaries
        global content
        end_y = travelpoint_boundaries[1][1] + math.floor(self.frame_width/2)

        #drawing text and image
        window.blit(self.drawing, self.drawingRect)

        #drawing headline text
        window.blit(self.headline_text, self.headline_rect)
        window.blit(self.ic1_text, self.ic1_rect)
        window.blit(self.ic2_text, self.ic2_rect)

        #drawing frame
        pygame.draw.line(window, (255,255,255), (0, end_y), (810, end_y), self.frame_width) #top line
        pygame.draw.line(window, (255,255,255), (0, 598), (810, 598), self.frame_width) #bottom line
        pygame.draw.line(window, (255,255,255), (0, end_y), (0, 600), self.frame_width) #left line
        pygame.draw.line(window, (255,255,255), (808, end_y), (808, 600), self.frame_width) #right line

        pygame.draw.line(window, (255,255,255), (218, end_y), (218, 600), self.frame_width) #middle left line
        pygame.draw.line(window, (255,255,255), (580, end_y), (580, 600), self.frame_width*2) #middle right line


    
    def update_text(self, travelpoint):
        global global_data
        text_to_display = {"planetname": travelpoint.name, "difficulty":"Difficulty: " +  str(travelpoint.diff)}        
        display_text = {"planetname":self.font.render(text_to_display["planetname"], False, (255, 255, 255)),
                            "difficulty":self.font.render(text_to_display["difficulty"], False, (255, 255, 255))}
        textRect = {"planetname":display_text["planetname"].get_rect(), "difficulty":display_text["difficulty"].get_rect()}

        self.drawing = pygame.Surface((806, 215))
        self.drawingRect = self.drawing.get_rect()
        self.drawingRect.center = (window.get_width()/2, 490)


        '''
        textRect["planetname"].x = 0
        textRect["planetname"].y = 30
        '''

        #self.drawing.fill((0, 255, 0))
        self.drawing.blit(display_text["planetname"], (230, 10))
        self.drawing.blit(display_text["difficulty"], (230, 70))

        travelpoint_image_rect = travelpoint.image.get_rect()
        travelpoint_image_rect.center = (108, 108)
        self.drawing.blit(travelpoint.image, travelpoint_image_rect)

    
    def do_misc(self):
        ic1t = "× " + str(global_data["lives"])
        ic2t = "× " + str(global_data["bigbullets"])
        self.ic1_text = self.font_small.render(ic1t, False, (255, 255, 255))
        self.ic1_rect = self.ic1_text.get_rect()
        self.ic1_rect.topleft = (638, 396)

        self.ic2_text = self.font_small.render(ic2t, False, (255, 255, 255))
        self.ic2_rect = self.ic2_text.get_rect()
        self.ic2_rect.topleft = (638, 432)

class ItemTracker():
    def __init__(self, xPos, yPos, xSize, ySize, value, sprite):
        self.xPos = xPos
        self.yPos = yPos

        self.xSize = xSize
        self.ySize = ySize

        self.value = value

        global content
        self.image = content[sprite]
        self.imagerect = self.image.get_rect()

        self.font = pygame.font.SysFont("Arial", 36)

        self.surface = pygame.Surface((self.xSize, self.ySize))
        self.surfaceRect = self.surface.get_rect()
        self.surfaceRect.x = self.xPos
        self.surfaceRect.y = self.yPos

        self.render()
    
    def render(self):
        self.imagerect.centery = self.surfaceRect.height/2

        #render text
        ctext = " × " + str(self.value)
        self.ctext = self.font.render(ctext, False, (255, 255, 255))
        self.ctext_rect = self.ctext.get_rect()
        self.ctext_rect.x = self.image.get_width()
        self.ctext_rect.centery = self.surfaceRect.height/2

        self.surface.fill((0, 0, 0))
        self.surface.blit(self.image, self.imagerect)
        self.surface.blit(self.ctext, self.ctext_rect)

    def update(self, value):
        self.value = value
        #do the updating/re-render of surface
        self.render()
    
    def draw(self, window):
        window.blit(self.surface, self.surfaceRect)

class TravelPoint():

    def __init__(self, xPos, yPos, diff, tp_list, visited = False, current = False, parent = None):
        self.xPos = xPos
        self.yPos = yPos

        self.diff = diff
        nameparts = ["ao", "ak", "bu", "re", "tan", "san", "on", "i", "ka", "nu", "mo", "ke", "tsu", "su", "fu", "ki", "ra", "shi", "cho", "de", "ba", "ra", "n"]
        name = ""
        for x in range(2, 5):
            name += nameparts[random.randint(0, 22)]
        self.name = name.capitalize()

        global content
        self.image = content["planets"][random.randint(0, len(content["planets"])-1)]
        #self.image = content["planets"][0]

        self.visited = visited
        self.current = False
        self.accessible = True

        self.children = []

        self.hover = False

        self.parent = parent


        tp_list.append(self)
    
    def draw(self, window):
        radius = 10
        width = 0
        color = (150, 150, 150)
        if self.visited or self.current:
            width = 0
            color = (255, 255, 255)
        
        pygame.draw.circle(window, color, (self.xPos, self.yPos), radius, width)

        if (not self.visited and not self.current) and (not self.hover) and self.accessible:
            pygame.draw.circle(window, (0,0,0), (self.xPos, self.yPos), 5, 0)

        if self.hover:
            pygame.draw.circle(window, (255,255,255), (self.xPos, self.yPos), radius*2, 2)
    
    def draw_line_to_children(self, window):
        
        for child in self.children:
            '''
            #removing lines if no longer accessible
            if not child.accessible and not child.visited:
                continue
            '''

            width = 3
            color = (150, 150, 150)
            if child.visited:
                color = (255, 255, 255)
            
            pygame.draw.line(window, color, (self.xPos, self.yPos), (child.xPos, child.yPos), width)
    
    def generate_children(self, tp_list, number_mm = (1,3), distancex_mm = (1, 3), distancey_mm = (-2, 2)):
        used_coordinates = []

        for x in range(random.randint(number_mm[0], number_mm[1])):

            nx = self.xPos + random.randint(distancex_mm[0], distancex_mm[1])*50
            ny = self.yPos + random.randint(distancey_mm[0], distancey_mm[1])*50

            #check if reached the end!
            if self.xPos >= 740:
                #print("You have reached the end. Congratulations!")
                return "end"

            #screen dimensions: 810x600
            #drawing travelpoints on area: [10, 800]x[10, 340]
            #rest of space in the bottom used for info screen
            
            global travelpoint_boundaries

            while (nx, ny) in used_coordinates or (nx > travelpoint_boundaries[1][0]) or (ny < travelpoint_boundaries[0][0]) or (ny > travelpoint_boundaries[1][1]):
                nx = self.xPos + random.randint(distancex_mm[0], distancex_mm[1])*50
                ny = self.yPos + random.randint(distancey_mm[0], distancey_mm[1])*50

            global global_data
            child = TravelPoint(nx, ny, diff=math.floor(global_data["diff_multi"]*get_distance((nx, ny), (self.xPos, self.yPos))/10), tp_list=tp_list)
            child.parent = self
            self.children.append(child)
            used_coordinates.append((nx, ny))

            '''
            used_coordinates.append((nx + 1, ny))            
            used_coordinates.append((nx + 1, ny + 1))
            used_coordinates.append((nx + 1, ny - 1))
            '''


class Level():
    #Notation:
    # P = pawn (32x32)
    # I = invader (32x32)
    # R = rook (32x48)
    # G = Gunship (64x64)

    def __init__(self, layout, rows, columns, xMargin = 0, yMargin = 0, xSpace = 0, ySpace = 0, pawn_anim = (0.5, 0.5), invader_anim = (0.5, 0.5), rook_anim = (0.5, 0.5), gunship_anim = (0.5, 0.5)):
        self.layout = layout

        if xMargin == "center":
            self.xMargin = (810 - (32 * columns + xSpace * (columns - 1)))/2
        else:
            self.xMargin = xMargin
        
        if yMargin == "center":
            self.yMargin = (600 - (32 * rows + ySpace * (rows - 1)))/2
        else:
            self.yMargin = yMargin

        self.rows = rows
        self.columns = columns

        self.xSpace = xSpace
        self.ySpace = ySpace

        self.pawn_anim = pawn_anim
        self.invader_anim = invader_anim
        self.rook_anim = rook_anim
        self.gunship_anim = gunship_anim
        
    
    def generate_enemies(self):
        enemies = []

        for y in range(self.rows):
            for x in range(self.columns):
                cell = self.layout[y][x]

                if cell == ' ' or cell == 'g':
                    continue

                if cell == 'P':
                    enemies.append(Pawn(self.xMargin +  x * 32 + x * self.xSpace, self.yMargin + y * 32 + y * self.ySpace, animX = self.pawn_anim[0], animY = self.pawn_anim[1]))
                
                if cell == 'I':
                    enemies.append(Invader(self.xMargin +  x * 32 + x * self.xSpace, self.yMargin + y * 32 + y * self.ySpace, animX = self.invader_anim[0], animY = self.invader_anim[1]))

                if cell == 'R':
                    enemies.append(Rook(self.xMargin +  x * 32 + x * self.xSpace, self.yMargin + y * 32 + y * self.ySpace, animX = self.rook_anim[0], animY = self.rook_anim[1]))
                
                if cell == "G":
                    enemies.append(Gunship(self.xMargin + x*32 + x * self.xSpace, self.yMargin + y*32 + y * self.ySpace, animX = self.gunship_anim[0], animY = self.gunship_anim[1]))
        
        return enemies

class Animation():
    def __init__(self, xPos, yPos, frames, fps):
        self.xPos = xPos
        self.yPos = yPos

        global content
        self.frames = content[frames]

        self.cframe = 0

        self.frameduration = 60 / fps
    
    def draw(self, window):
        image = self.frames[self.cframe]
        window.blit(image, (self.xPos, self.yPos))
    
    def update(self, step, removefrom = None):        
        if step % self.frameduration == 0:
            self.cframe += 1
            if self.cframe >= len(self.frames):
                self.cframe = 0
                if removefrom != None:
                    removefrom.remove(self)

'''
class Explosion():
    def __init__(self, xPos, yPos, xplosionType = "small"):
        self.xPos = xPos
        self.yPos = yPos

        if xplosionType == "small": #if 32x32 explosion | else would be 64x64 explosion
            
            global content
            self.frames = content["explosion_small"]
        
        self.cframe = 0
    
    def draw(self, window):
        image = self.frames[self.cframe]
        window.blit(image, (self.xPos, self.yPos))
    
    def update(self, step, explosionlist):
        if step % 10 == 0: #change to depend on number of frames etc.
            self.cframe += 1
            if self.cframe >= len(self.frames):
                explosionlist.remove(self)

'''

class Enemy():

    def __init__(self, xPos, yPos, xSize, ySize, animX = 0.5, animY = 0.5, shootnum = True, sprite = False, color = (255, 0, 0), life = 1, collissionradius = 32):
        self.collissionradius = collissionradius
        
        self.baseX = xPos
        self.baseY = yPos

        self.xPos = xPos
        self.yPos = yPos
        self.color = list(color)

        self.xSize = xSize
        self.ySize = ySize

        self.life = life

        self.animX = animX
        self.animY = animY

        self.tag = "enemy"

        #if the given shootnum is greater than 1000 (e.g 1017), it subtracts 1000 and creates that number of random numbers that's left
        self.shootnum = []
        if shootnum == True:
            self.shootnum.append(random.randint(0, 240))
        elif type(shootnum) == type(3):
            if shootnum < 1000:
                for x in range(1, shootnum + 1): #The modifications were added so that the shooting didn't start at frame 0 and ended at frame 240 - (240/shootnum), but instead one "step" further
                    self.shootnum.append(int((240 / shootnum) * x))
            else:
                for x in range(shootnum - 1000):
                    self.shootnum.append(random.randint(0, 240))
        else:
            self.shootnum = False
        

        #adding the sprite
        global content
        if sprite != False:
            self.image = content[sprite]
        else:
            self.image = False
    
    def draw(self, window):
        if self.image != False:
            window.blit(self.image, (self.xPos, self.yPos))
        else:
            window.fill(self.color, ((self.xPos, self.yPos), (self.xSize, self.ySize)))
    
    def move(self, stepx, stepy, x = True, y = False):
        if x:
            self.xPos = self.baseX + self.animX*stepx
        if y:
            self.yPos = self.baseY + self.animY*stepy
    
    def shoot(self, bulletlist, shootstep, player):
        if self.shootnum == False:
            return

        if shootstep in self.shootnum:
            bullet = Bullet(self.xPos  + self.xSize/2 - 2, self.yPos + self.ySize , direction = 1, collisionlist=[player], speed = 10)
            bulletlist.append(bullet)

class Pawn(Enemy):
    def __init__(self, xPos, yPos, animX = 0.5, animY = 0.5):
        super().__init__(xPos, yPos, xSize = 32, ySize = 32, animX = animX, animY = animY, shootnum = False, sprite = "pawn", collissionradius=16)

class Invader(Enemy):
    def __init__(self, xPos, yPos, animX = 0.5, animY = 0.5):
        super().__init__(xPos, yPos, xSize = 32, ySize = 32, animX = animX, animY = animY, shootnum = True, sprite = "invader", collissionradius=16)

class Rook(Enemy):
    def __init__(self, xPos, yPos, animX = 0.5, animY = 0.5):
        super().__init__(xPos, yPos, 32, 48, animX = animX, animY = animY, shootnum = 4, sprite = "rook", collissionradius=16) #shootnum = 4

class Gunship(Enemy):
    def __init__(self, xPos, yPos, animX = 0.5, animY = 0.5):
        super().__init__(xPos, yPos, 64, 64, animX = animX, animY = animY, shootnum = 1002, sprite = "gunship", collissionradius=24)
    
    def shoot(self, bulletlist, shootstep, player):
        if self.shootnum == False:
            return

        if shootstep in self.shootnum:
            bullet = Bullet(self.xPos  + self.xSize/2 - 2, self.yPos + self.ySize , direction = 1, collisionlist=[player], speed = 20)

            bullet1 = Bullet(self.xPos + 9, self.yPos + self.ySize - 10, direction = 1, collisionlist=[player], speed = 10)
            bullet2 = Bullet(self.xPos + self.xSize - 13, self.yPos + self.ySize - 10, direction = 1, collisionlist=[player], speed = 10)

            bulletlist.append(bullet)
            bulletlist.append(bullet1)
            bulletlist.append(bullet2)

class StepObject():

    def __init__(self, minStep = 0, maxStep = 60, startStep = 0, bidirectional = True, growthDirection = 1):
        self.minStep = minStep
        self.maxStep = maxStep
        self.bidirectional = bidirectional
        self.step = startStep

        self.growth = growthDirection
    
    def update(self):
        nstep = self.step + self.growth
        if nstep > self.maxStep:
            if self.bidirectional == True:
                self.step = self.maxStep - 1
                self.growth = -1
            else:
                self.step = self.minStep
            return
        if nstep < self.minStep:
            if self.bidirectional == True:
                self.step = self.minStep + 1
                self.growth = 1
            else:
                self.step = self.maxStep
            return
        
        self.step = nstep
        

class Bullet():

    def __init__(self, xPos, yPos, collisionlist = [], speed = 20, color = (255, 255, 255), direction = -1):
        self.xPos = xPos
        self.yPos = yPos
        self.speed = speed
        self.color = color
        self.direction = direction

        self.xSize = 4
        self.ySize = 20

        self.collisionlist = collisionlist

        self.type = "bullet"
    
    def draw(self, window):
        window.fill(self.color, ((self.xPos, self.yPos), (self.xSize, self.ySize)))

    def colcheck(self):
        top = self.yPos
        bottom = self.yPos + self.ySize
        xmid = self.xPos + self.xSize / 2

        for obj in self.collisionlist:
            
            if xmid >= obj.xPos and xmid <= (obj.xPos + obj.xSize):

                if (top >= obj.yPos and top <= (obj.yPos + obj.ySize)) or (bottom <= (obj.yPos + obj.ySize) and bottom >= obj.yPos):
                    return obj
            continue

        return False

    def move(self, bulletlist, enemylist, explosionlist, remove_animations_list, player):
        self.yPos += self.speed * self.direction

        col = self.colcheck()
        if col != False:

            if col.tag == "enemy":
                col.life -= 1
                if col.life <= 0:
                    print(col.baseY)
                    explosionlist.append(Animation(col.xPos, col.yPos, frames="explosion_small", fps=6))
                    enemylist.remove(col)

            elif col.tag == "player":

                #del player #Works!  but ends game
                player.removeLife(remove_animations_list)
                explosionlist.append(Animation(col.xPos, col.yPos, frames="explosion_small", fps=6))

                print("Aw man! You hit me!")

            bulletlist.remove(self)

class BigBullet:

    def __init__(self, xPos, yPos, collisionlist = [], speed = 6, color = (255, 255, 255), direction = -1, sprite = "bigbullet"):
        self.xPos = xPos
        self.yPos = yPos

        self.xSize = 16
        self.ySize = 32

        self.collisionlist = collisionlist

        self.speed = speed
        self.color = color

        self.direction = direction

        global content
        self.image = content["bigbullet"]

        self.type = "bigbullet"

        self.exploderadius = 64
    
    def draw(self, window):
        #window.fill(self.color, ((self.xPos, self.yPos), (self.xSize, self.ySize)))
        window.blit(self.image, (self.xPos, self.yPos))

    def move(self, bulletlist, enemylist, explosionlist, remove_animations_list, player):
        self.yPos += self.speed * self.direction

    def explode(self):
        return Blast(int(self.xPos + self.xSize/2), int(self.yPos + self.ySize/2))

class Decay:
    def __init__(self, xPos, yPos, radius = 64, duration = 30, basecolor = 255):
        self.xPos = xPos
        self.yPos = yPos

        self.radius = radius
        self.duration = duration

        self.opacitydecrement = int(basecolor/duration)
        self.ccolor = basecolor

        self.type = "decay"
    
    def draw(self, window):
        pygame.draw.circle(window, (self.ccolor, self.ccolor, self.ccolor), (self.xPos, self.yPos), self.radius, 10)
    
    def update(self, removefrom):
        if self.ccolor == 0:
            removefrom.remove(self)

        self.ccolor -= self.opacitydecrement
        if self.ccolor < 0:
            self.ccolor = 0

class Blast:
    def __init__(self, xPos, yPos, blastradius = 96, blastspeed = 30):
        self.xPos = xPos
        self.yPos = yPos

        self.blastradius = blastradius
        self.blastspeed = blastspeed

        self.currentradius = 0

        self.type = "blast"
    def draw(self, window):
        width = 10 if self.currentradius >= 10 else self.currentradius
        pygame.draw.circle(window, (255, 255, 255), (self.xPos, self.yPos), self.currentradius, width)
        
    
    def update(self, step, enemylist, removefrom, explosionlist):

        if step % 4 == 0:

            if self.currentradius >= self.blastradius:
                #this baby has finished exploding!!
                #create decaying circle
                removefrom.append(Decay(self.xPos, self.yPos, self.blastradius, duration=30, basecolor = 255))

                removefrom.remove(self)

            rdif = self.blastradius - self.currentradius
            self.currentradius += math.ceil(rdif/2)

            #check collissions with enemies
            for enemy in enemylist:
                distance = get_distance([self.xPos, self.yPos], [enemy.xPos, enemy.yPos])
                radiussum = self.currentradius + enemy.collissionradius

                if distance <= radiussum:
                    #collission!!
                    enemy.life -= 5
                    if enemy.life <= 0:
                        explosionlist.append(Animation(enemy.xPos, enemy.yPos, frames="explosion_small", fps=6))
                        enemylist.remove(enemy)

class Drawable:

    def __init__(self, xPos, yPos, sprite):
        self.xPos = xPos
        self.yPos = yPos

        global content
        self.image = content[sprite]
        self.image_rect = self.image.get_rect()
        self.image_rect.topleft = (xPos, yPos)
    
    def draw(self, window):
        window.blit(self.image, self.image_rect)

class Player:

    def __init__(self, xPos, yPos, color = (255, 255, 255)):
        self.xPos = xPos
        self.yPos = yPos
        self.color = list(color)

        self.xSize = 48
        self.ySize = 64

        self.moveSpeed = 6

        self.tag = "player"

        global global_data
        self.life = global_data["lives"]
        self.liveslist = []

        global content
        self.image = content["player"]

        self.superpowers = {
            "tripleshot" : False,
            "cheatshot" : False,
            "lifecontrol" : False
        }
    
    def generateLives(self, window):
        global content
        for x in range(1, self.life + 1):        
            self.liveslist.append(Animation(window.get_width() - x*48, window.get_height() - 34, frames = "heart", fps = 10))

    def removeLife(self, remove_animations_list):
        self.life -= 1
        global global_data
        global_data["lives"] = self.life
        #generate life removal animation
        try:
            life_remove_animation = Animation(self.liveslist[-1].xPos, self.liveslist[-1].yPos, frames="heart_destruction", fps=12)
        except:
            try:
                life_remove_animation = Animation(self.liveslist[0].xPos, self.liveslist[0].yPos, frames="heart_destruction", fps=12)
            except:
                pass
            pass
            
        remove_animations_list.append(life_remove_animation)

        del self.liveslist[-1]
    
    def addLife(self, window):
        self.life += 1
        self.liveslist.append(Animation(window.get_width() - (len(self.liveslist) + 1)*48, window.get_height() - 34, frames="heart", fps=10))

    def draw(self, window):
        if self.image != False:
            window.blit(self.image, (self.xPos, self.yPos))
        else:
            window.fill(self.color, ((self.xPos, self.yPos), (self.xSize, self.ySize)))
    
    def move(self, direction = -1): #-1 is left, 1 is right
        newpos = self.xPos + direction*self.moveSpeed
        if newpos < 0:
            self.xPos = 0
            return
        elif (newpos + self.xSize) > dim[0]:
            self.xPos = dim[0] - self.xSize
            return
        self.xPos = newpos
    
    def shoot(self, bulletlist, enemylist, bullettype = "normal"):
        if bullettype == "normal":
            bullet = Bullet(self.xPos + (self.xSize / 2) - 2, self.yPos, enemylist)

        elif bullettype == "bigbullet":
            bullet = BigBullet(self.xPos + (self.xSize / 2) - 8, self.yPos - 26, enemylist)

        bulletlist.append(bullet)

        if self.superpowers["tripleshot"] == True and bullettype == "normal":
            bullet1 = Bullet(self.xPos, self.yPos, enemylist)
            bullet2 = Bullet(self.xPos + self.xSize - 4, self.yPos, enemylist)

            bulletlist.append(bullet1)
            bulletlist.append(bullet2)
        
        if bullettype == "bigbullet":
            return bullet

def get_tp_at_mouse(mouse_pos, tp_list, info_table):
    for tp in tp_list:
        if get_distance((tp.xPos, tp.yPos), mouse_pos) <= 15:
            info_table.update_text(tp)
            if tp.accessible == True and not tp.visited:
                return tp

def get_distance(p1, p2):
    sq = (p1[0]-p2[0])**2 + (p1[1] - p2[1])**2
    return math.sqrt(sq)

def load_content():
    content = dict()
    
    #First loading the explosion sprites
    #print(os.path.isfile(os.path.join("sprites", "explosion_small0.png")))
    try:
        explosion = (pygame.image.load(os.path.join("sprites", "explosion_small0.png")).convert_alpha(), pygame.image.load(os.path.join("sprites", "explosion_small1.png")).convert_alpha(), pygame.image.load(os.path.join("sprites", "explosion_small2.png")).convert_alpha())
    except:
        f1 = pygame.Surface((32, 32))
        f1.fill((255, 255, 255))
        f2 = pygame.Surface((32, 32))
        f2.fill((200, 200, 200))
        f3 = pygame.Surface((32, 32))
        f3.fill((150, 150, 150))
        explosion = (f1, f2, f3)
    
    content["explosion_small"] = explosion

    #Then loading the heart animation sprites
    try:
        heart = (pygame.image.load(os.path.join("sprites", "heart0.png")).convert_alpha(), pygame.image.load(os.path.join("sprites", "heart1.png")).convert_alpha(),
        pygame.image.load(os.path.join("sprites", "heart2.png")).convert_alpha(), pygame.image.load(os.path.join("sprites", "heart3.png")).convert_alpha(),
        pygame.image.load(os.path.join("sprites", "heart4.png")).convert_alpha(), pygame.image.load(os.path.join("sprites", "heart5.png")).convert_alpha())
    except:
        f1 = pygame.Surface((32, 32))
        f1.fill((255, 255, 255))

        f2 = pygame.Surface((32, 32))
        f2.fill((200, 200, 200))

        f3 = pygame.Surface((32, 32))
        f3.fill((150, 150, 150))

        f4 = pygame.Surface((32, 32))
        f4.fill((150, 150, 150))

        f5 = pygame.Surface((32, 32))
        f5.fill((200, 200, 200))

        f6 = pygame.Surface((32, 32))
        f6.fill((255, 255, 255))
        heart = (f1, f2, f3, f4, f5, f6)
    
    content["heart"] = heart

    #then loading the heart destruction animation sprites
    try:
        heart_destruction = (pygame.image.load(os.path.join("sprites", "heart_destruction0.png")).convert_alpha(),
        pygame.image.load(os.path.join("sprites", "heart_destruction1.png")).convert_alpha(),
        pygame.image.load(os.path.join("sprites", "heart_destruction2.png")).convert_alpha())
    except:
        f1 = pygame.Surface((32, 32))
        f1.fill((255, 255, 255))

        f2 = pygame.Surface((32, 32))
        f2.fill((155, 155, 155))

        f3 = pygame.Surface((32, 32))
        f3.fill((55, 55, 55))

        heart_destruction = (f1, f2, f3)
    content["heart_destruction"] = heart_destruction


    #Then loading enemy sprites
    try:
        pawn = pygame.image.load(os.path.join("sprites", "pawn.png")).convert_alpha()
    except:
        pawn = False
    content["pawn"] = pawn

    try:
        rook = pygame.image.load(os.path.join("sprites", "rook.png")).convert_alpha()
    except:
        rook = False
    content["rook"] = rook

    try:
        invader = pygame.image.load(os.path.join("sprites", "invader.png")).convert_alpha()
    except:
        invader = False
    content["invader"] = invader

    try:
        gunship = pygame.image.load(os.path.join("sprites", "gunship.png")).convert_alpha()
    except:
        gunship = False
    content["gunship"] = gunship

    #Loading big bullet sprite
    try:
        bigbullet = pygame.image.load(os.path.join("sprites", "bigbullet.png")).convert_alpha()
    except:
        bigbullet = pygame.Surface((16, 32))
        bigbullet.fill((255, 255, 255))
    content["bigbullet"] = bigbullet


    #load the different planet sprites
    planets = []
    try:
        planet1 = pygame.image.load(os.path.join("sprites", "planet1.png")).convert_alpha()
    except:
        planet1 = pygame.Surface((216, 216))
        planet1.fill((0, 0, 0))
        pygame.draw.circle(planet1, (255, 255, 255), (108, 108), 108)
    planets.append(planet1)

    #load more planets
    try:
        planet1large = pygame.image.load(os.path.join("sprites", "planet1_large.png")).convert_alpha()
    except:
        planet1large = pygame.Surface((216, 216))
        planet1large.fill((0, 0, 0))
        pygame.draw.circle(planet1large, (255, 255, 255), (108, 108), 108)
    planets.append(planet1large)

    try:
        planet2 = pygame.image.load(os.path.join("sprites", "planet2.png")).convert_alpha()
    except:
        planet2 = pygame.Surface((216, 216))
        planet2.fill((0, 0, 0))
        pygame.draw.circle(planet2, (255, 255, 255), (108, 108), 108)
    planets.append(planet2)

    try:
        planet2medium = pygame.image.load(os.path.join("sprites", "planet2_medium.png")).convert_alpha()
    except:
        planet2medium  = pygame.Surface((216, 216))
        planet2medium .fill((0, 0, 0))
        pygame.draw.circle(planet2medium , (255, 255, 255), (108, 108), 108)
    planets.append(planet2medium )

    try:
        planet2large = pygame.image.load(os.path.join("sprites", "planet2_large.png")).convert_alpha()
    except:
        planet2large = pygame.Surface((216, 216))
        planet2large.fill((0, 0, 0))
        pygame.draw.circle(planet2large, (255, 255, 255), (108, 108), 108)
    planets.append(planet2large)

    content["planets"] = planets


    #Lastly load the player sprite
    try:
        player = pygame.image.load(os.path.join("sprites", "playership2.png")).convert_alpha()
    except:
        player = False
    content["player"] = player

    return content

def generateLayout(columns = 7, rows = 6, d = 100, symmetric = True):
    
    
    #Vælg om man vil lave en symmetrisk bane ved kun at generere halvdelen af banen

    #Bestem antallet af rækker og kolonner tilfældigt på baggrund af sværhadsgraden (d)
    columns = columns
    rows = rows

    rnd = True
    if rnd == True:
        if d <= 10:
            columns = random.randint(3, 4)
            rows = random.randint(2, 3)
        elif d <= 30:
            columns = random.randint(4, 5)
            rows = random.randint(3, 4)
        elif d <= 50:
            columns = random.randint(5, 6)
            rows = random.randint(3, 4)
        elif d <= 80:
            columns = random.randint(6, 8)
            rows = random.randint(4, 5)
        elif d <= 100:
            columns = random.randint(8, 10)
            rows = random.randint(5, 6)
        elif d <= 150:
            columns = random.randint(8, 12)
            rows = random.randint(5, 7)
        else:
            columns = random.randint(10, 14)
            rows = random.randint(6, 7)

    layout = [[' ' for x in range(columns)] for x in range(rows)]

    enemy_count = 0

    #Chances need adjustment
    gnum = 0.5*d/20 
    rnum = 0.5*d/5 + gnum 
    inum = 10 + d/10 + rnum 
    pnum =  30 + 2*d/10 + inum 

    mLine = True
    if columns % 2 == 0:
        mLine = False


    if not symmetric:
        for y in range(rows):
            for x in range(columns):

                if layout[y][x] == 'g':
                    continue
                
                num = random.randint(0, 100)

                if num <= gnum and d >= 50: #can only come after difficulty 50
                    layout[y][x] = 'G'
                    enemy_count += 1
                    try:
                        layout[y][x + 1] = 'g'
                    except:
                        pass
                
                    try:
                        layout[y + 1][x] = 'g'
                    except:
                        pass
                
                    try:
                        layout[y + 1][x + 1] = 'g'
                    except:
                        pass
                
                    continue

                elif num <= rnum and d >= 30: #can only come after difficulty 30
                    layout[y][x] = 'R'
                    enemy_count += 1
                    continue
                elif num <= inum and d >= 10: #can only come after difficulty 10
                    layout[y][x] = 'I'
                    enemy_count += 1
                    continue
                elif num <= pnum:
                    layout[y][x] = 'P'
                    enemy_count += 1
                    continue
                else:
                    layout[y][x] = ' '
        
        #do cloning of left side into right side


        if enemy_count <= 0:
            layout = generateLayout(columns = columns, rows = rows, d = d, symmetric=False)

    else:
        generated_columns = columns//2 if not mLine else columns//2 + 1

        for y in range(rows): #do for every row AND the line in middle, although Gunships cannot be generated on the middle line or the lines around it
            for x in range(generated_columns):

                if layout[y][x] == 'g':
                    continue
                

                num = random.randint(0, 100)

                if num <= gnum and d >= 50: #can only come after difficulty 50

                    if not mLine or x < (generated_columns - 1): #makes sure that Gunships aren't generated at middle or right before last column
                        layout[y][x] = 'G'
                        enemy_count += 1
                        try:
                            layout[y][x + 1] = 'g'
                        except:
                            pass
                    
                        try:
                            layout[y + 1][x] = 'g'
                        except:
                            pass
                    
                        try:
                            layout[y + 1][x + 1] = 'g'
                        except:
                            pass
                            
                        #cloning this ship to the other side is more work than the other ships because of it's size
                        nx = columns - (x + 2)
                        layout[y][nx] = 'G'
                        enemy_count += 1
                        try:
                            layout[y][nx + 1] = 'g'
                        except:
                            pass

                        try:
                            layout[y + 1][nx] = 'g'
                        except:
                            pass
                        
                        try:
                            layout[y + 1][nx + 1] = 'g'
                        except:
                            pass
                        
                        continue
                elif num <= rnum and d >= 30: #can only come after difficulty 30
                    layout[y][x] = 'R'
                    enemy_count += 1

                    if not mLine or x < generated_columns:
                        nx = columns - (x + 1)
                        layout[y][nx] = 'R'
                        enemy_count += 1

                    continue
                elif num <= inum and d >= 10: #can only come after difficulty 10
                    layout[y][x] = 'I'
                    enemy_count += 1

                    if not mLine or x < generated_columns:
                        nx = columns - (x + 1)
                        layout[y][nx] = 'I'
                        enemy_count += 1

                    continue
                elif num <= pnum:
                    layout[y][x] = 'P'
                    enemy_count += 1

                    if not mLine or x < generated_columns:
                        nx = columns - (x + 1)
                        layout[y][nx] = 'P'
                        enemy_count += 1

                    continue
                else:
                    layout[y][x] = ' '
        
        if enemy_count <= 0:
            layout = generateLayout(columns = columns, rows = rows, d = d, symmetric = True)

    '''
    for line in layout:
        print(line)
    '''

    return layout

def doscrolltext(window, displaytext, font):
    #prepare text
    alpha = 100
    text = font.render(displaytext, False, (255, 255, 255))
    textRect = text.get_rect()

    surface = pygame.Surface(textRect.size)
    surfaceRect = surface.get_rect()
    surfaceRect.center = (window.get_width()/2, -64)

    surface.blit(text, textRect)

    clock = pygame.time.Clock()

    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    return()

        if surfaceRect.center[1] <= 360:
            surfaceRect.center = (surfaceRect.center[0], surfaceRect.center[1] + 4)
        else:
            if alpha > 0:
                alpha -= 0.6
                surface.set_alpha(alpha)
            else:
                return

        '''
        surface.fill(0, 0, 0)
        surface.blit(text, textRect)
        '''

        window.fill((0, 0, 0))
        window.blit(surface, surfaceRect)
        pygame.display.update()

        clock.tick(60)


def doLevel(window, level, loading = True, lspeed = 1, pstart = "center", planetname = "PLANET"):

    global global_data

    #disable when porting
    cheats = True

    #prepare text for drawing
    font = pygame.font.SysFont("Arial", 64)

    stext = font.render(planetname, False, (255, 255, 255))
    stextRect = stext.get_rect()
    stextRect.center = (window.get_width()/2, 460)

    finishtext = str(planetname).upper() + " CLEARED"
    gameovertext = "GAME OVER"

    if pstart == "center":
        player = Player(dim[0]/2 - 24, 500)
    else:
        player = Player(pstart[0], pstart[1])
    player.generateLives(window)

    bulletlist = []
    bigbullet = None

    #level = Level(levelLayout, rows = len(levelLayout), columns = len(levelLayout[0]), xMargin = 64, yMargin = 64, xSpace = 10, ySpace = 10, rook_anim=(0.0, 0.5), invader_anim=(0.6, 0.5))
    enemylist = level.generate_enemies()

    explosionlist = []

    remove_animations_list = []

    miscobjectslist = []
    
    itemtrackers = []
    bigbullet_tracker = ItemTracker(10, 10, 128, 64, value=global_data["bigbullets"], sprite="bigbullet")
    itemtrackers.append(bigbullet_tracker)

    #GameSteps
    enemStepX = StepObject(-120, 120, 0, True, 1)
    enemStepY = StepObject(-120, 120, -120, True, 1) 
    shootStep = StepObject(0, 240, 0, False, 1)

    animationStep = StepObject(1, 60, 1, False, 1) #for explosionanimations and so on

    stepObjects = [enemStepX, enemStepY, shootStep, animationStep]
    
    if loading:
        originY = enemylist[0].yPos
        offset = -(level.rows * 32 + (level.rows - 1) * level.ySpace + 170) #calculates how much the enemies are going to be moved up for animation

        for enemy in enemylist:
            enemy.yPos += offset
            enemy.baseY += 120*enemy.animY

    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue
            if event.type == pygame.KEYDOWN:
                #shooting
                if event.key == pygame.K_UP and not loading:
                    player.shoot(bulletlist, enemylist, bullettype = "normal")

                #big bullet
                if event.key == pygame.K_z and not loading :
                    if not bigbullet:
                        if global_data["bigbullets"] > 0:
                            
                            bigbullet = player.shoot(bulletlist, enemylist, bullettype = "bigbullet")

                            global_data["bigbullets"] -= 1
                            bigbullet_tracker.update(global_data["bigbullets"])
                    else:
                        blast = bigbullet.explode()
                        miscobjectslist.append(blast)

                        bulletlist.remove(bigbullet)
                        bigbullet = None
                    
                
                #These are cheats you can both disable and enable!! <3
                if event.key == pygame.K_1 and cheats == True:
                    player.superpowers["tripleshot"] = not player.superpowers["tripleshot"]
                
                if event.key == pygame.K_2 and cheats == True:
                    player.superpowers["cheatshot"] = not player.superpowers["cheatshot"]
                
                if event.key == pygame.K_3 and cheats == True:
                    player.superpowers["lifecontrol"] = not player.superpowers["lifecontrol"]
                
                #other controls
                if event.key == pygame.K_q and player.superpowers["lifecontrol"]:
                    player.removeLife(remove_animations_list)
                
                if event.key == pygame.K_w and player.superpowers["lifecontrol"]:
                    player.addLife(window)
                
                if event.key == pygame.K_RETURN and loading:
                    loading = False

                    

        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            player.move(-1)
        if keys[K_RIGHT]:
            player.move(1)
        if keys[K_UP] and player.superpowers["cheatshot"] == True:
            player.shoot(bulletlist, enemylist)
        
        if not loading:

            #updating bullets
            for bullet in bulletlist:
                bullet.move(bulletlist, enemylist, explosionlist, remove_animations_list, player)
                if bullet.yPos < (0 - bullet.ySize) or bullet.yPos > 600:
                    if bullet.type == "bigbullet":
                        bigbullet = None
                    bulletlist.remove(bullet)
                    
            
            for enemy in enemylist:
                enemy.move(enemStepX.step, enemStepY.step, x = True, y = True) #move enemy
                enemy.shoot(bulletlist, shootStep.step, player) #Call the shoot method, if it is shoot time, then it shoots
        else:
            for enemy in enemylist:
                enemy.yPos += lspeed
            if enemylist[0].yPos >= originY:
                loading = False

        window.fill((0, 0, 0)) #clear screen

        player.draw(window) #draw player

        for bullet in bulletlist: #draw all bullets
            bullet.draw(window)

        for obj in miscobjectslist:
            obj.draw(window)

            if obj.type == "decay":
                obj.update(miscobjectslist)
            
            elif obj.type == "blast":
                obj.update(animationStep.step, enemylist, miscobjectslist, explosionlist)

        for enemy in enemylist: #draw and then move every single enemy downwards
            enemy.draw(window)
            if not loading:
                enemy.baseY += 0.05 #moves every enemy down by a bit

                if enemy.yPos > 600:
                        enemylist.remove(enemy)
                        player.removeLife(remove_animations_list)

                if enemy.baseY >= 430:

                    if (enemy.yPos + enemy.ySize) >= player.yPos and (enemy.xPos <= player.xPos + player.xSize and enemy.xPos >= player.xPos - 32):
                        explosionlist.append(Animation(enemy.xPos, enemy.yPos, frames="explosion_small", fps=6))
                        enemylist.remove(enemy)
                        player.removeLife(remove_animations_list)
                

        for explosion in explosionlist:
            explosion.draw(window)
            explosion.update(animationStep.step, explosionlist)

        for life in player.liveslist:
            life.draw(window)
            life.update(animationStep.step)
        
        for animation in remove_animations_list:
            animation.draw(window)
            animation.update(animationStep.step, remove_animations_list)
        
        for itemtracker in itemtrackers:
            itemtracker.draw(window)

        #DRAWING TEXT WHEN LOADING UP LEVEL
        if loading:
            window.blit(stext, stextRect) #show text

        pygame.display.update()

        if not loading:
            for step in stepObjects:
                step.update()

        #check if player has killed all enemies, return True if he has after finish
        if len(enemylist) == 0:
            outcome = doscrolltext(window, finishtext, font)
            if outcome == False:
                return outcome
            
            return [player.xPos, player.yPos]
        
        #check if players life is zero, return False if it is 
        if player.life == 0:
            doscrolltext(window, gameovertext, font)
            return False

        clock.tick(60)
    
    return False


def doLevelSelectionScreen(window):

    global travelpoint_boundaries
    global global_data

    stepobjects = []
    animationStep = StepObject(1, 60, 1, False, 1)
    stepobjects.append(animationStep)

    heart_animation = Animation(600, 400, "heart", 12)
    bigbullet_sprite = Drawable(608, 436, "bigbullet")

    travelpoints = []
    tp1 = TravelPoint(50, math.floor(travelpoint_boundaries[1][1]/2), math.floor(random.randint(10, 15)*global_data["diff_multi"]), tp_list = travelpoints)

    info_table = InformationTable(current_travelpoint=tp1)

    mouse_pos = pygame.mouse.get_pos()
    tp_hover = get_tp_at_mouse(mouse_pos, travelpoints, info_table)

    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue

            if event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                tp_hover = get_tp_at_mouse(mouse_pos, travelpoints, info_table)
                if tp_hover:
                    info_table.update_text(tp_hover)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    #tp_clicked = get_tp_at_mouse(mouse_pos, travelpoints)
                    tp_clicked = tp_hover
                    if tp_clicked == None:
                        break
                    
                    if tp_clicked.parent != None:
                        for child in tp_clicked.parent.children:
                            child.accessible = False
                            child.current = False



                    tp_clicked.current = True
                    global_data["diff_multi"] += 0.2
                    result = tp_clicked.generate_children(travelpoints)
                    tp_clicked.visited = True

                    #doing the actual level
                    randomlevelLayout = generateLayout(d=tp_clicked.diff)
                    randomlevel = Level(randomlevelLayout, rows = len(randomlevelLayout), columns = len(randomlevelLayout[0]), xMargin = "center", yMargin = 64, xSpace = 20, ySpace = 20, pawn_anim=(0.5, 0.5), rook_anim=(0.0, 0.5), invader_anim=(0.6, 0.5))

                    outcome = doLevel(window, randomlevel, loading=True, lspeed=2, pstart="center", planetname = tp_clicked.name)
                    info_table.do_misc()

                    if outcome == False:
                        '''
                        sys.exit()
                        break
                        '''
                        return False


                    if result == "end":
                        return True
                        print("You have reached the end")

        #do calculations
        for step in stepobjects:
            step.update()

        #do drawing
        window.fill((0,0,0))

        #draw the travelpoints and such
        for tp in travelpoints:
            tp.hover = True if tp == tp_hover else False          
            tp.draw_line_to_children(window)
            tp.draw(window)
      
        

        #draw the frame for info box and text and such
        #pygame.draw.line(window, (255, 255, 255), (0, 390), (810, 390), 2)
        info_table.draw(window)

        #drawing the icons
        heart_animation.update(animationStep.step)
        heart_animation.draw(window)

        bigbullet_sprite.draw(window)

        pygame.display.update()

        clock.tick(60)


if getattr(sys, 'frozen', False): #Does something very important for file management
    os.chdir(sys._MEIPASS)

pygame.init()
dim = (810, 600)
window = pygame.display.set_mode(dim)
pygame.display.set_caption("INVADERS")

content = load_content() #very important to do

travelpoint_boundaries = ((10, 10), (800, 380)) #setting the global boundaries for where travelpoints can be shown
global_data = {"lives": 10, "diff_multi": 1.0, "area": 1, "bigbullets": 999}

#starting the level selection screen
out = doLevelSelectionScreen(window)
while out:
    global_data["area"] += 1
    out = doLevelSelectionScreen(window)
sys.exit()