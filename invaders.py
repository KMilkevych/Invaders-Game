
import pygame
from pygame.locals import *
import math
import random
import sys
import os

class PowerButton():
    '''A Power Button. Is defined with a custom render function, and a list of parameters,
    allowing for high customization of each entity of this class.'''

    def __init__(self, size=(64, 64), pos=(64, 64), renderfunction=None, onclick=None, param=None):
        self.size = size
        self.pos = pos

        self.param = param

        self.surface = pygame.Surface(self.size)
        self.rect = self.surface.get_rect()
        self.rect.topleft = self.pos

        self.renderfunction = renderfunction
        self.render()

        self.onclick_event = onclick

    
    def render(self):
        self.renderfunction(self)

    def update(self, renderfunction=None):
        if renderfunction is not None:
            self.renderfunction = renderfunction
        self.render()
    
    def onclick(self):
        self.onclick_event(self)
    
    def draw(self, window):
        window.blit(self.surface, self.rect)

class Button():
    '''A SHOP button consisting of an image and some text. Used exclusively in shops.'''

    def __init__(self, image=None, image_pos=None, size=None, pos=None, onclick=None, price=None, purchased=False, flavourtext=""):
        
        global content

        if type(content[image]) != tuple:
            self.image = content[image]
        else:
            self.image = content[image][0]
        
        self.image_rect = self.image.get_rect()
        self.image_rect.topleft = image_pos

        self.surface = pygame.Surface(size)
        self.rect = self.surface.get_rect()
        self.rect.topleft = pos

        #Creating a surface for the falvourtext.
        self.fsurface = pygame.Surface((248, 340))

        self.price = price

        #Aestethic variables

        self.bordercolor = (255, 255, 255)
        self.borderthickness = 11
        self.highlightcolor = (100, 100, 100)

        self.purchased = purchased

        if self.price:            

            #Price or "PURCHASED" text
            self.font = pygame.font.SysFont("Arial", 22)

            #render text
            pricetext = "PRICE " + str(self.price)
            purchasedtext = "PURCHASED"

            self.pricetext = self.font.render(pricetext, False, (255, 255, 255))
            self.purchasedtext = self.font.render(purchasedtext, False, (255, 255, 255))

            self.pricetext_rect = self.pricetext.get_rect()
            self.pricetext_rect.x = (self.rect.width - (self.pricetext_rect.width + 36))/2
            self.pricetext_rect.y = self.rect.height - self.pricetext_rect.height - 12

            self.purchasedtext_rect = self.purchasedtext.get_rect()
            self.purchasedtext_rect.centerx = self.rect.width/2
            self.purchasedtext_rect.y = self.rect.height - self.purchasedtext_rect.height - 12

        #Action variables

        self.active = False
        self.lift = True

        self.onclick_event = onclick

        self.flavourtext = flavourtext
        #Render itself

        self.render()
        if self.flavourtext:
            self.render_flavour()

    def onclick(self):
        self.onclick_event(self)

    def render(self):

        imgRect = pygame.Rect(self.image_rect)
        if self.active or self.purchased:
            self.surface.fill(self.highlightcolor)
        else:
            self.surface.fill((0, 0, 0))

        if self.lift and self.active and not self.purchased:
            imgRect.y -= 16
        

        #draw borders
        topleft = (0, 0)
        topright = (self.rect.width , 0 )
        bottomleft = (0, self.rect.height)
        bottomright = (self.rect.width, self.rect.height)
        
        #top border
        pygame.draw.line(self.surface, self.bordercolor, topleft, topright, self.borderthickness)
        #left border
        pygame.draw.line(self.surface, self.bordercolor, topleft, bottomleft, self.borderthickness)
        #bottom border
        pygame.draw.line(self.surface, self.bordercolor, (bottomleft[0], bottomleft[1] - 1), (bottomright[0], bottomright[1] - 1), self.borderthickness)
        #right border
        pygame.draw.line(self.surface, self.bordercolor, (bottomright[0] - 1, bottomright[1]), (topright[0] - 1, topright[1]), self.borderthickness)

        #draw image to button surface
        self.surface.blit(self.image, imgRect)

        #Draw text at the bottom
        if self.purchased and self.price:
            self.surface.blit(self.purchasedtext, self.purchasedtext_rect)
        elif self.price:
            global content
            self.surface.blit(self.pricetext, self.pricetext_rect)
            self.surface.blit(content["coin"], (self.pricetext_rect.width + self.pricetext_rect.x + 4, self.pricetext_rect.centery - 16))

    def render_flavour(self):

        ffont = pygame.font.SysFont("Arial", 23)
        
        for i in range(0, len(self.flavourtext)):
            rendered_text = ffont.render(self.flavourtext[i], False, (255, 255, 255))
            self.fsurface.blit(rendered_text, (0, i*26))


    def draw(self, window):
        window.blit(self.surface, self.rect)
    
class InformationTable():

    """Information table object. Contains information about current travelpoint, and some global data such as current area and number of bigbullets and lives left etc."""

    def __init__(self, frame_width = 2, current_travelpoint = None):
        self.frame_width = frame_width

        if current_travelpoint:
            self.travelpoint = current_travelpoint
        
        #Creates a small and a slightly larger font
        self.font = pygame.font.SysFont("Arial", 48)
        self.font_small = pygame.font.SysFont("Arial", 36)
        self.update_text(current_travelpoint)

        #Renders the header text, this one contains the area number eg. "AREA 3"
        ht = "AREA " + str(global_data["area"])
        self.headline_text = self.font_small.render(ht, False, (255, 255, 255))
        self.headline_rect = self.headline_text.get_rect()
        self.headline_rect.center = (window.get_width()/2, 20) #Sets target location of text to be centered at the top of the screen

        #renders text parts for the amount of lives and big bullets left. Those are stored as ic1_text and ic2_text.
        #ItemTracker object is not used here, due to the life image being animated
        self.do_misc()


    def draw(self, window):
        """Draws the virtual surface and frame around it to the screen together with other text"""

        global travelpoint_boundaries
        global content
        end_y = travelpoint_boundaries[1][1] + math.floor(self.frame_width/2)

        #drawing the virtual surface containing image and travelpoint information to the screen
        window.blit(self.drawing, self.drawingRect)

        #drawing headline text
        window.blit(self.headline_text, self.headline_rect)
        window.blit(self.ic1_text, self.ic1_rect)
        window.blit(self.ic2_text, self.ic2_rect)
        window.blit(self.ic3_text, self.ic3_rect)

        #drawing frame
        pygame.draw.line(window, (255,255,255), (0, end_y), (810, end_y), self.frame_width) #top line
        pygame.draw.line(window, (255,255,255), (0, 598), (810, 598), self.frame_width) #bottom line
        pygame.draw.line(window, (255,255,255), (0, end_y), (0, 600), self.frame_width) #left line
        pygame.draw.line(window, (255,255,255), (808, end_y), (808, 600), self.frame_width) #right line

        pygame.draw.line(window, (255,255,255), (218, end_y), (218, 600), self.frame_width) #middle left line
        pygame.draw.line(window, (255,255,255), (580, end_y), (580, 600), self.frame_width*2) #middle right line


    
    def update_text(self, travelpoint):
        """A function for updating all the text holding the information about the current travelpoint object. """
        global global_data
        
        text_to_display = {"planetname": travelpoint.name, "difficulty":"Difficulty: " +  str(travelpoint.diff)} #the string that should be rendered

        display_text = {"planetname":self.font.render(text_to_display["planetname"], False, (255, 255, 255)),
                            "difficulty":self.font.render(text_to_display["difficulty"], False, (255, 255, 255))} #the actual rendered text to be displayed

        textRect = {"planetname":display_text["planetname"].get_rect(), "difficulty":display_text["difficulty"].get_rect()} #the rect objects for the rendered text

        #creates a virtual surface that all objects will be drawn to
        self.drawing = pygame.Surface((806, 215))
        self.drawingRect = self.drawing.get_rect()
        self.drawingRect.center = (window.get_width()/2, 490)

        #Draws the planetname and difficulty texts to the virtual surface
        self.drawing.blit(display_text["planetname"], (230, 10))
        if travelpoint.type == 0:
            self.drawing.blit(display_text["difficulty"], (230, 70))

        #Draws the travelpoint image to the virtual surface
        travelpoint_image_rect = travelpoint.image.get_rect()
        travelpoint_image_rect.center = (108, 108)
        self.drawing.blit(travelpoint.image, travelpoint_image_rect)

    
    def do_misc(self):
        """Renders texts containining how many lives, bigbullets and money/coins the player has left."""
        ic1t = "× " + str(global_data["lives"])
        ic2t = "× " + str(global_data["bigbullets"])
        ic3t = "× " + str(global_data["money"])

        self.ic1_text = self.font_small.render(ic1t, False, (255, 255, 255))
        self.ic1_rect = self.ic1_text.get_rect()
        self.ic1_rect.topleft = (638, 396)

        self.ic2_text = self.font_small.render(ic2t, False, (255, 255, 255))
        self.ic2_rect = self.ic2_text.get_rect()
        self.ic2_rect.topleft = (638, 432)

        self.ic3_text = self.font_small.render(ic3t, False, (255, 255, 255))
        self.ic3_rect = self.ic3_text.get_rect()
        self.ic3_rect.topleft = (638, 468)

class ItemTracker():

    """Itemtracker object. Consists of a static image (sprite) and a corresponding value.
        When drawn, shows [SPRITE] x [VALUE]. Used to inform the user about number of big bullets, coins etc."""

    def __init__(self, xPos, yPos, xSize, ySize, value, sprite):
        self.type = "itemtracker"

        self.xPos = xPos
        self.yPos = yPos

        self.xSize = xSize
        self.ySize = ySize

        self.value = value

        global content
        self.image = content[sprite]
        self.imagerect = self.image.get_rect()

        #creating the font used to draw the "x"
        self.font = pygame.font.SysFont("Arial", 36)

        #generates a virtual surface that all parts of the object will be rendered to. When drawn, this virtual surface will be drawn.
        self.surface = pygame.Surface((self.xSize, self.ySize))
        self.surfaceRect = self.surface.get_rect()
        self.surfaceRect.x = self.xPos
        self.surfaceRect.y = self.yPos

        self.render() #render all parts to the surface
    
    def render(self):
        """Renders all parts to a virtual surface"""

        #Sets the target y-position of the sprite, so that it's centered inside the virtual surface.
        self.imagerect.centery = self.surfaceRect.height/2

        #render text
        ctext = " × " + str(self.value)
        self.ctext = self.font.render(ctext, False, (255, 255, 255))
        self.ctext_rect = self.ctext.get_rect()
        self.ctext_rect.x = self.image.get_width()
        self.ctext_rect.centery = self.surfaceRect.height/2

        #draw text and sprite to the virtual surface
        self.surface.fill((0, 0, 0))
        self.surface.blit(self.image, self.imagerect)
        self.surface.blit(self.ctext, self.ctext_rect)

    def update(self, value):
        """Updates value, and re-renders with this value."""
        self.value = value
        self.render()
    
    def draw(self, window):
        """Draws virtual surface with all components to the screen"""
        window.blit(self.surface, self.surfaceRect)

class TravelPoint():

    """A travelpoint object. These are displayed in the level selection screen. Each travelpoint holds information about its parent tp, its children,
        its difficulty, name, image (planet visualization), if it has been visited before, and if it's the tp the player is currently at (the player just completed this level).
        A TravelPoint's type (0 or 1) refers to whether or not the travelpoint is a shop - 1 or a regular node - 0."""

    def __init__(self, xPos, yPos, diff, tp_list, visited = False, current = False, parent = None, type=0):
        self.xPos = xPos
        self.yPos = yPos

        self.diff = diff

        self.type = type
        if self.type == 0:
            #generates the name for this travelpoint out of a random combination of the following strings
            nameparts = ["ao", "ak", "bu", "re", "tan", "san", "on", "i", "ka", "nu", "mo", "ke", "tsu", "su", "fu", "ki", "ra", "shi", "cho", "de", "ba", "ra", "n"]
            name = ""
            for x in range(2, 5):
                name += nameparts[random.randint(0, len(nameparts) - 1)]
            self.name = name.capitalize()
        else:
            self.name = "Gerd's Shop"

        #sets image (planet visualization)
        global content
        self.image = content["planets"][random.randint(0, len(content["planets"])-1)] if self.type == 0 else content["planet_shop"]


        self.visited = visited
        self.current = False
        self.accessible = True

        self.children = []

        self.hover = False

        self.parent = parent

        self.text = pygame.font.SysFont("Arial", 24).render("SHOP", False, (255, 255, 255))
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (self.xPos, self.yPos + 28)

        tp_list.append(self)
    
    def draw(self, window):
        """Draws the travelpoint object. If the tp is current or has been visited, then the circle representing it will be white, else grey.
            If the tp is currently hovered over, then draws a thin circle around it also.
            If the tp is no longer available, and hasn't been visited, then draws a small black circle inside it."""
        
        radius = 10
        width = 0
        color = (150, 150, 150)
        if self.visited or self.current:
            width = 0
            color = (255, 255, 255)
        
        #draw the travelpoint itself
        pygame.draw.circle(window, color, (self.xPos, self.yPos), radius, width)

        #If tp not available anymore, and hasn't been visited, draw a small black circle inside.
        if (not self.visited and not self.current) and (not self.hover) and self.accessible:
            pygame.draw.circle(window, (0,0,0), (self.xPos, self.yPos), 5, 0)

        #if tp hovered over then draw thin circle around tp
        if self.hover:
            pygame.draw.circle(window, (255,255,255), (self.xPos, self.yPos), radius*2, 2)

        #Lastly, draw the "SHOP" text underneath
        if self.type == 1:
            window.blit(self.text, self.text_rect)
    
    def draw_line_to_children(self, window):
        """Draws lines to each of the travelpoints children, if it has any."""

        for child in self.children:

            width = 3
            color = (150, 150, 150)
            if child.visited: # if the child has been visited, then the line connecting it with the current tp should be white, ekse grey.
                color = (255, 255, 255)
            
            pygame.draw.line(window, color, (self.xPos, self.yPos), (child.xPos, child.yPos), width) #draws the line connecting the two travelpoints
    
    def generate_children(self, tp_list, number_mm = (1,3), distancex_mm = (1, 3), distancey_mm = (-2, 2)):

        """Generates a random number of children. This number can be between number_mm[0] and number_mm[1].
            Each child is generated at a given x and y offset from current travelpoint coordinates. 
            These offsets are a multiple of 50 pixels and are calculated randomly using distancex_mm and distancey_mm tuples."""

        #if the x position of the current travelpoint is so far to the right, that its impossible to generate children inside the boundaries, returns "end"
        if self.xPos >= 740:
            return "end"

        used_coordinates = [] #a list of used coordinates, to make sure function doesn't generate multiple children at same coordinate

        for x in range(random.randint(number_mm[0], number_mm[1])): #generating a random number of children

            nx = self.xPos + random.randint(distancex_mm[0], distancex_mm[1])*50 #determining the new x coordinate of child
            ny = self.yPos + random.randint(distancey_mm[0], distancey_mm[1])*50 #determining the new y coordinate of child

            #screen dimensions: 810x600
            #drawing travelpoints on area: [10, 800]x[10, 340]
            #rest of space in the bottom used for info screen
            
            global travelpoint_boundaries

            #if travelpoint is generated outside of boundaries or already has a child at those coordinates, generates new coordinates for the travelpoint
            while (nx, ny) in used_coordinates or (nx > travelpoint_boundaries[1][0]) or (ny < travelpoint_boundaries[0][0]) or (ny > travelpoint_boundaries[1][1]):
                nx = self.xPos + random.randint(distancex_mm[0], distancex_mm[1])*50
                ny = self.yPos + random.randint(distancey_mm[0], distancey_mm[1])*50

            global global_data
            #Determines if point should be a shop
            tp_type = 1 if (random.randint(0, 100) <= global_data["shopchance"]*100) else 0

            #Creates the travelpoint object with the difference being the global difference multiplier times the distance between this child and it's parent
            child = TravelPoint(nx, ny, diff=math.floor(global_data["diff_multi"]*get_distance((nx, ny), (self.xPos, self.yPos))/10), tp_list=tp_list, type=tp_type)
            child.parent = self
            self.children.append(child)
            used_coordinates.append((nx, ny))
           

class Level():

    """A Level class. Takes a layout as an parameter, and can then generate a list of enemies at their corresponding positions based on different settings."""

    #Notation:
    # P = pawn (32x32)
    # I = invader (32x32)
    # R = rook (32x48)
    # G = Gunship (64x64)

    def __init__(self, layout, rows, columns, xMargin = 0, yMargin = 0, xSpace = 0, ySpace = 0, pawn_anim = (0.5, 0.5), invader_anim = (0.5, 0.5), rook_anim = (0.5, 0.5), gunship_anim = (0.5, 0.5)):
        self.layout = layout

        #determines what the left xMargin should be, centers the "block" of enemies on the x-axis if "center"
        if xMargin == "center":
            self.xMargin = (810 - (32 * columns + xSpace * (columns - 1)))/2
        else:
            self.xMargin = xMargin
        
        #same as xMargin, but for y-axis
        if yMargin == "center":
            self.yMargin = (600 - (32 * rows + ySpace * (rows - 1)))/2
        else:
            self.yMargin = yMargin

        self.rows = rows
        self.columns = columns

        #space between each row and column
        self.xSpace = xSpace
        self.ySpace = ySpace

        #values for movement of the different enemies
        self.pawn_anim = pawn_anim
        self.invader_anim = invader_anim
        self.rook_anim = rook_anim
        self.gunship_anim = gunship_anim
        
    
    def generate_enemies(self):
        """Generates the enemies based on the layout and settings."""
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

    """Animation class. Holds a list of sprites as frames, and an fps value."""

    def __init__(self, xPos, yPos, frames, fps):
        self.xPos = xPos
        self.yPos = yPos

        #sets the frames
        global content
        self.frames = content[frames]

        #sets the current frame index to be 0 (first frame in list)
        self.cframe = 0

        #determines the duration of each frame
        self.frameduration = 60 / fps
    
    def draw(self, window):
        image = self.frames[self.cframe]
        window.blit(image, (self.xPos, self.yPos))
    
    def update(self, step, removefrom = None):
        #Updates itself.
        # If the animation needs to be destroyed when if finishes, then it needs a removefrom list, which is a list containing this animation (eg. explosionlist)        
        if step % self.frameduration == 0: #if the frameduration has passed, then move to next frame
            self.cframe += 1
            if self.cframe >= len(self.frames): #if last frame is reached, then set current frame to 0 (start over)
                self.cframe = 0
                if removefrom != None: #if there's a removefrom list, then remove itself from that list and delete itself.
                    removefrom.remove(self)
                    del self


class Enemy():

    """Enemy class. Enemies can shoot move around their base coordinates (movement coefficients are described as animX and animY), and shoot with precise or random intervals.
        They also have a sprite, and can have a variable number of lives."""

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
        
        #shooting
        #steps referred to, are numbers. When a corresponding "shootstep" stepobject has it's current step as that number, the enemy will fire
        self.shootnum = []
        if shootnum == True:
            self.shootnum.append(random.randint(0, 240)) #if True, chooses one random step out of 240 steps, at which this enemy is gonna shoot
        elif type(shootnum) == type(3):
            if shootnum < 1000: #if the shootnum is less than 1000, it chooses the a shootnum number of steps at which this enemy will fire a bullet; the time between shots is constant
                for x in range(1, shootnum + 1): #The modifications were added so that the shooting didn't start at frame 0 and ended at frame 240 - (240/shootnum), but instead one "step" further
                    self.shootnum.append(int((240 / shootnum) * x))
            else:
                for x in range(shootnum - 1000): #If shootnum is greater than 1000, it subtracts 1000 and then chooses that amount of steps to shoot a bullet on; these steps are random, and have random time between them.
                    self.shootnum.append(random.randint(0, 240))
        else:
            self.shootnum = False
        

        #setting the sprite
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
        """Sets the current coordinates to be an offset from the base coordinates. The offset is determined by a movement stepobject, and the animX and animY variables."""
        if x:
            self.xPos = self.baseX + self.animX*stepx
        if y:
            self.yPos = self.baseY + self.animY*stepy
    
    def shoot(self, bulletlist, shootstep, player):
        if self.shootnum == False:
            return

        #if current value of shootstep object is inside the shootnum list, then it's time for the enemy to fire a bullet
        if shootstep in self.shootnum:
            bullet = Bullet(self.xPos  + self.xSize/2 - 2, self.yPos + self.ySize , direction = 1, collisionlist=[player], speed = 10)
            bulletlist.append(bullet)

class Pawn(Enemy):
    def __init__(self, xPos, yPos, animX = 0.5, animY = 0.5):
        super().__init__(xPos, yPos, xSize = 32, ySize = 32, animX = animX, animY = animY, shootnum = False, sprite = "pawn", collissionradius=16)
        self.type = "pawn"

class Invader(Enemy):
    def __init__(self, xPos, yPos, animX = 0.5, animY = 0.5):
        super().__init__(xPos, yPos, xSize = 32, ySize = 32, animX = animX, animY = animY, shootnum = True, sprite = "invader", collissionradius=16)
        self.type = "invader"

class Rook(Enemy):
    def __init__(self, xPos, yPos, animX = 0.5, animY = 0.5):
        super().__init__(xPos, yPos, 32, 48, animX = animX, animY = animY, shootnum = 4, sprite = "rook", collissionradius=16) #shootnum = 4
        self.type = "rook"

class Gunship(Enemy):
    """Derives from Enemy class, major difference being it fires two additional bullets."""
    def __init__(self, xPos, yPos, animX = 0.5, animY = 0.5):
        super().__init__(xPos, yPos, 64, 64, animX = animX, animY = animY, shootnum = 1002, sprite = "gunship", collissionradius=24)
        self.type = "gunship"
    
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

    """Stepobject class. An object that has a step value that moves inside of an interval in a direction, each time the object is updated.
        Can move either from left to right, then back to initial starting point, the other way around, or ping-pong between min and max values."""

    def __init__(self, minStep = 0, maxStep = 60, startStep = 0, bidirectional = True, growthDirection = 1):
        self.minStep = minStep
        self.maxStep = maxStep
        self.bidirectional = bidirectional
        self.step = startStep

        self.growth = growthDirection
    
    def update(self):
        """Updates the step value"""
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
    """Bullet class for normal bullets which don't have sprites and move fast. These are shot both by player and enemies,
        and therefore need a list of objects they can collide with on creation."""

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
        """Checks for collissions with the objects in its collissionlist"""

        top = self.yPos
        bottom = self.yPos + self.ySize
        xmid = self.xPos + self.xSize / 2

        for obj in self.collisionlist:            
            if xmid >= obj.xPos and xmid <= (obj.xPos + obj.xSize):
                if (top >= obj.yPos and top <= (obj.yPos + obj.ySize)) or (bottom <= (obj.yPos + obj.ySize) and bottom >= obj.yPos):
                    return obj #returns the object the bullet has collided with
            continue

        return False

    def move(self, bulletlist, enemylist, explosionlist, remove_animations_list, player):
        """Moves the bullet in the direction specified on creation, checks for collissions, and acts accordingly"""

        self.yPos += self.speed * self.direction #move bullet

        col = self.colcheck() #get the object the bullet collided with
        if col != False:

            if col.tag == "enemy": #if collided with enemy, remove 1 life from enemy
                col.life -= 1
                if col.life <= 0: #if enemy is dead, delete it, and create an explosion in its place
                    explosionlist.append(Animation(col.xPos, col.yPos, frames="explosion_small", fps=6))
                    if isinstance(col, Gunship):
                        explosionlist.append(Animation(col.xPos + 32, col.yPos, frames="explosion_small", fps=6))
                        explosionlist.append(Animation(col.xPos, col.yPos + 32, frames="explosion_small", fps=6))
                        explosionlist.append(Animation(col.xPos + 32, col.yPos + 32, frames="explosion_small", fps=6))            
                    enemylist.remove(col)

                    #Adds money for killing enemy
                    global global_data
                    reward = global_data["kill_reward"]
                    if col.type == "invader":
                        reward = reward * 1.5
                    elif col.type == "rook":
                        reward = reward * 2.0
                    elif col.type == "gunship":
                        reward = reward * 4.0
                    global_data["money"] += int(reward)


            elif col.tag == "player": #if collided with player, remove 1 life, and create an explosion animation

                #del player works,  but ends game
                player.removeLife(remove_animations_list)
                explosionlist.append(Animation(col.xPos, col.yPos, frames="explosion_small", fps=6))

            bulletlist.remove(self) #deletes itself on collision

class BigBullet:
    """Class for the big bullets. This isn't a child of the bullet class because this doesn't collide with anything. On detonation creates a deadly Blast"""
    def __init__(self, xPos, yPos, speed = 6, color = (255, 255, 255), direction = -1, sprite = "bigbullet"):
        self.xPos = xPos
        self.yPos = yPos

        self.xSize = 16
        self.ySize = 32

        self.speed = speed
        self.color = color

        self.direction = direction

        global content
        self.image = content["bigbullet"]

        self.type = "bigbullet"

        #the maximum radius of the blast it creates on detonation
        self.exploderadius = 64
    
    def draw(self, window):
        """Draws itself to the screen"""
        window.blit(self.image, (self.xPos, self.yPos))

    def move(self, bulletlist, enemylist, explosionlist, remove_animations_list, player):
        """Moves itself"""
        self.yPos += self.speed * self.direction

    def explode(self):
        """Returns a deadly Blast object, which expands as a shockwave and damages enemies."""
        return Blast(int(self.xPos + self.xSize/2), int(self.yPos + self.ySize/2))

class Decay:
    """A harmless decay object which is represented as a circle with same width and radius as the Blast it was created by"""

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
        """Fades out, if already invisible, destroy itself"""
        if self.ccolor == 0:
            removefrom.remove(self)

        self.ccolor -= self.opacitydecrement
        if self.ccolor < 0:
            self.ccolor = 0

class Blast:
    """Deadly expanding shockwave that expands each frame up to it's maximum radius, and when an enemy colliding area is within that radius, the enemy is damaged.
        Creates a Decay object on death, which is a fading out silhoutte of the shockwave, Decay object is harmless."""
    def __init__(self, xPos, yPos, blastradius = 96, blastspeed = 30):
        self.xPos = xPos
        self.yPos = yPos

        self.blastradius = blastradius
        self.blastspeed = blastspeed

        self.currentradius = 0

        self.type = "blast"
    
    def draw(self, window):
        """Draws itself to the screen"""
        width = 10 if self.currentradius >= 10 else self.currentradius #circle can't have a thicker width than it's radius, therefore set width to radius until radius is 10
        pygame.draw.circle(window, (255, 255, 255), (self.xPos, self.yPos), self.currentradius, width)
        
    
    def update(self, step, enemylist, removefrom, explosionlist):
        #Updates every 4 frames, should generally finish expanding after 7 cycles, which means 28 frames and is basically half a second
        if step % 4 == 0:

            if self.currentradius >= self.blastradius: #If the blast has reached it's maximum radius, it get's destroyed, and creates a Decay object in it's place.
                removefrom.append(Decay(self.xPos, self.yPos, self.blastradius, duration=30, basecolor = 255))
                removefrom.remove(self)

            #Calculates the difference between the maximum radius (target radius) and it's current radius
            rdif = self.blastradius - self.currentradius

            #Halves the this difference in radiuses by expanding the current radius by half the current difference (rdif/2)
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
                        if isinstance(enemy, Gunship):
                            explosionlist.append(Animation(enemy.xPos + 32, enemy.yPos, frames="explosion_small", fps=6))
                            explosionlist.append(Animation(enemy.xPos, enemy.yPos + 32, frames="explosion_small", fps=6))
                            explosionlist.append(Animation(enemy.xPos + 32, enemy.yPos + 32, frames="explosion_small", fps=6))
                        enemylist.remove(enemy)

                        #Rewards money for killing enemy
                        global global_data
                        reward = global_data["kill_reward"]
                        if enemy.type == "invader":
                            reward = reward * 1.5
                        elif enemy.type == "rook":
                            reward = reward * 2.0
                        elif enemy.type == "gunship":
                            reward = reward * 4.0
                        global_data["money"] += int(reward)

class Drawable:
    """A drawable class; a basic that has no collission and can be drawn"""

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
    """Main Player Class"""

    def __init__(self, xPos, yPos, color = (255, 255, 255)):
        self.xPos = xPos
        self.yPos = yPos
        self.color = list(color)

        self.xSize = 48
        self.ySize = 64

        self.moveSpeed = 6

        self.tag = "player"

        #reads the amount of lives it has from the global data
        global global_data
        self.life = global_data["lives"]
        self.liveslist = []

        #dictionary for cheat management
        global superpowers
        self.superpowers = superpowers

        #sets player sprite
        global content
        if self.superpowers["tripleshot"]:
            self.image = content["player_tripleshot"]
        else:
            self.image = content["player"]

        
    
    def generateLives(self, window):
        """Generates a list of rotating hearts (animations) that are displayed at the bottom of the screen"""
        global content
        for x in range(1, self.life + 1):        
            self.liveslist.append(Animation(window.get_width() - x*48, window.get_height() - 34, frames = "heart", fps = 10))

    def removeLife(self, remove_animations_list):
        """Removes one of the players lives, creating a heart destruction animation"""
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
        """Adds a new life to the player"""
        self.life += 1
        self.liveslist.append(Animation(window.get_width() - (len(self.liveslist) + 1)*48, window.get_height() - 34, frames="heart", fps=10))

    def draw(self, window):
        """Draws the player to the screen at it's current coordinates"""
        if self.image != False:
            window.blit(self.image, (self.xPos, self.yPos))
        else:
            window.fill(self.color, ((self.xPos, self.yPos), (self.xSize, self.ySize)))
    
    def move(self, direction = -1): #-1 is left, 1 is right
        """Moves the player"""
        newpos = self.xPos + direction*self.moveSpeed
        if newpos < 0:
            self.xPos = 0
            return
        elif (newpos + self.xSize) > dim[0]:
            self.xPos = dim[0] - self.xSize
            return
        self.xPos = newpos
    
    def shoot(self, bulletlist, enemylist, bullettype = "normal"):
        """When this method is called, creates a bullet and adds it to the bulletlist"""
        if bullettype == "normal":
            bullet = Bullet(self.xPos + (self.xSize / 2) - 2, self.yPos, enemylist)

        elif bullettype == "bigbullet":
            bullet = BigBullet(self.xPos + (self.xSize / 2) - 8, self.yPos - 26)

        bulletlist.append(bullet)

        #if tripleshot is active, and is shooting normal bullet, fire 2 more bullets
        if self.superpowers["tripleshot"] == True and bullettype == "normal":
            bullet1 = Bullet(self.xPos, self.yPos, enemylist)
            bullet2 = Bullet(self.xPos + self.xSize - 4, self.yPos, enemylist)

            bulletlist.append(bullet1)
            bulletlist.append(bullet2)
        
        #returns the bullet if the bullet being shot is a big bullet (necesarry for detonating it later)
        if bullettype == "bigbullet":
            return bullet

def get_tp_at_mouse(mouse_pos, tp_list, info_table):
    """Determines which travelpoint is currently hovered over"""
    for tp in tp_list:
        if get_distance((tp.xPos, tp.yPos), mouse_pos) <= 15:
            info_table.update_text(tp)
            if tp.accessible == True and not tp.visited:
                return tp

def get_distance(p1, p2): 
    """Computes distance between two points represented as lists or tuples"""
    sq = (p1[0]-p2[0])**2 + (p1[1] - p2[1])**2
    return math.sqrt(sq)

def load_content():

    """Loads sprites and other content from main memory and saves in a global dictionary (content)"""

    content = dict()
    
    #First loading the explosion sprites
    try:
        explosion = (pygame.image.load(os.path.join("sprites", "explosion_small0.png")).convert_alpha(), pygame.image.load(os.path.join("sprites", "explosion_small1.png")).convert_alpha(), pygame.image.load(os.path.join("sprites", "explosion_small2.png")).convert_alpha())
    except: #if fails to load, replace sprites with squares
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

    #Now, loading only the first image of that heart animation:
    try:
        heart_sprite = pygame.image.load(os.path.join("sprites", "heart0.png")).convert_alpha()
    except:
        heart_sprite = pygame.Surface((32, 32))
        heart_sprite.fill((255, 255, 255))

    content["heart_sprite"] = heart_sprite

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

    try:
        planet_shop = pygame.image.load(os.path.join("sprites", "planet_shop.png")).convert_alpha()
    except:
        planet_shop = pygame.Surface((192, 192))
        planet_shop.fill((0, 0, 0))
        pygame.draw.circle(planet_shop, (255, 255, 255), (108, 108), 169)

    content["planet_shop"] = planet_shop

    try:
        backarrow = pygame.image.load(os.path.join("sprites", "backarrow.png")).convert_alpha()
    except:
        backarrow = pygame.Surface((48, 32))
        backarrow.fill((255, 255, 255))
    
    content["backarrow"] = backarrow

    try:
        coin = pygame.image.load(os.path.join("sprites", "coin.png")).convert_alpha()
    except:
        coin = pygame.Surface((32,32))
        coin.fill((0, 0, 0))
        pygame.draw.circle(coin, (255,255,255), (15,15), 16)
    
    content["coin"] = coin

    try:
        player_tripleshot = pygame.image.load(os.path.join("sprites", "playership_tripleshot.png")).convert_alpha()
    except:
        player_tripleshot = pygame.Surface((32, 48))
        player_tripleshot.fill((255, 255, 255))

    content["player_tripleshot"] = player_tripleshot

    #Lastly load the player sprite
    try:
        player = pygame.image.load(os.path.join("sprites", "playership2.png")).convert_alpha()
    except:
        player = False
    content["player"] = player

    return content

def generateLayout(columns = 7, rows = 6, d = 100, symmetric = True):
    
    """Generates a random symmetrical (or assymetrical) layout with a random amount of rows and columns and enemies based on the difficulty (d)"""

    #Determine the number of columns and rows randomly
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

    #generates an empty 2-dimensional list that will hold the layout
    layout = [[' ' for x in range(columns)] for x in range(rows)]

    #number of generated enemies
    enemy_count = 0

    #probabilities for spawning a Gunship, Rook, Invader or Pawn
    gnum = 0.5*d/20 
    rnum = 0.5*d/5 + gnum 
    inum = 10 + d/10 + rnum 
    pnum =  30 + 2*d/10 + inum 

    mLine = True #determine if there's a middle column (false if even number of columns)
    if columns % 2 == 0:
        mLine = False


    if not symmetric: #if layout doesn't need to be symmetric
        for y in range(rows):
            for x in range(columns):

                if layout[y][x] == 'g': #small letter, means this square is reserved for a larger enemy that takes up more space
                    continue
                
                num = random.randint(0, 100)

                if num <= gnum and d >= 50: #can only spawn after difficulty 50
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

                elif num <= rnum and d >= 30: #can only spawn after difficulty 30
                    layout[y][x] = 'R'
                    enemy_count += 1
                    continue
                elif num <= inum and d >= 10: #can only spawn after difficulty 10
                    layout[y][x] = 'I'
                    enemy_count += 1
                    continue
                elif num <= pnum:
                    layout[y][x] = 'P'
                    enemy_count += 1
                    continue
                else:
                    layout[y][x] = ' '

        if enemy_count <= 0: #if it didn't generate any enemies, run the function again
            layout = generateLayout(columns = columns, rows = rows, d = d, symmetric=False)

    else: #if the layout needs to be symmetric
        generated_columns = columns//2 if not mLine else columns//2 + 1 #determine for how many columns we will generate (left half is generated, and then cloned to the right)

        for y in range(rows): #do for every row AND the line in middle, although Gunships cannot be generated on the middle line or the lines around it because they take up 2x2 spaces
            for x in range(generated_columns):

                if layout[y][x] == 'g':
                    continue
                

                num = random.randint(0, 100)

                if num <= gnum and d >= 50: #can only spawn after difficulty 50

                    if not mLine or x < (generated_columns - 1): #makes sure that Gunships aren't generated in the middle or right before the last column
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

                elif num <= rnum and d >= 30: #can only spawn after difficulty 30
                    layout[y][x] = 'R'
                    enemy_count += 1

                    #clone to the right
                    if not mLine or x < generated_columns:
                        nx = columns - (x + 1)
                        layout[y][nx] = 'R'
                        enemy_count += 1

                    continue
                elif num <= inum and d >= 10: #can only spawn after difficulty 10
                    layout[y][x] = 'I'
                    enemy_count += 1

                    #clone
                    if not mLine or x < generated_columns:
                        nx = columns - (x + 1)
                        layout[y][nx] = 'I'
                        enemy_count += 1

                    continue
                elif num <= pnum:
                    layout[y][x] = 'P'
                    enemy_count += 1

                    #clone
                    if not mLine or x < generated_columns:
                        nx = columns - (x + 1)
                        layout[y][nx] = 'P'
                        enemy_count += 1

                    continue
                else:
                    layout[y][x] = ' '
        
        if enemy_count <= 0: #if no enemies were generated, run function again
            layout = generateLayout(columns = columns, rows = rows, d = d, symmetric = True)

    return layout

def doscrolltext(window, displaytext, font):
    #prepare text
    alpha = 100
    text = font.render(displaytext, False, (255, 255, 255))
    textRect = text.get_rect()

    #create a surface the text will be rendered to
    surface = pygame.Surface(textRect.size)
    surfaceRect = surface.get_rect()
    surfaceRect.center = (window.get_width()/2, -64)

    surface.blit(text, textRect)

    clock = pygame.time.Clock()

    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            #if space or enter is pressed, skip the scrolltext
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    return()

        #if text hasn't reached y=360 yet, then move it down by a bit
        if surfaceRect.center[1] <= 360:
            surfaceRect.center = (surfaceRect.center[0], surfaceRect.center[1] + 6)
        
        else: #else, start the fade out "animation"
            if alpha > 0:
                alpha -= 0.6
                surface.set_alpha(alpha)
            else:
                return

        #draw the text 
        window.fill((0, 0, 0))
        window.blit(surface, surfaceRect)
        pygame.display.update()

        #limit framerate to 60fps
        clock.tick(60)


def doLevel(window, level, loading = True, lspeed = 1, pstart = "center", planetname = "PLANET"):

    """Runs the level passed as parameter. This is where the actual shooting happens"""

    global global_data #Get the global data

    cheats = True #disable on release

    #Prepare font for the scrolltext on load
    font = pygame.font.SysFont("Arial", 64)

    #Render the scrolltext
    stext = font.render(planetname, False, (255, 255, 255))
    stextRect = stext.get_rect()
    stextRect.center = (window.get_width()/2, 460)

    #Generate sthe strings for when the player either dies, or completes the level
    finishtext = str(planetname).upper() + " CLEARED"
    gameovertext = "GAME OVER"

    #Generates the player object with the given starting position
    if pstart == "center":
        player = Player(dim[0]/2 - 24, 500)
    else:
        player = Player(pstart[0], pstart[1])
    
    #generates the lives of the player
    player.generateLives(window)

    #Creates list for bullets
    bulletlist = []
    #Sets the current active bigbullet to None
    bigbullet = None

    #Creates a list for enemies, and generates the enemies using the data stored in the level object
    enemylist = level.generate_enemies()

    #Creates a list for explosions
    explosionlist = []

    #Creates a list for animations that should be removed
    remove_animations_list = []

    #Creates a list for other objects to be drawn (such as item trackers)
    miscobjectslist = []
    
    #Creates and adds a tracker for those big bullets and coinzz (coins) :-P
    bigbullet_tracker = ItemTracker(26, 10, 128, 48, value=global_data["bigbullets"], sprite="bigbullet")
    money_tracker = ItemTracker(10, (48 + 8), 192, (32), value=global_data["money"], sprite="coin")
    miscobjectslist.append(bigbullet_tracker)
    miscobjectslist.append(money_tracker)

    #Generates the step objects needed for animations, enemy movement and enemy shooting
    enemStepX = StepObject(-120, 120, 0, True, 1)
    enemStepY = StepObject(-120, 120, -120, True, 1) 
    shootStep = StepObject(0, 240, 0, False, 1)

    animationStep = StepObject(1, 60, 1, False, 1)

    stepObjects = [enemStepX, enemStepY, shootStep, animationStep]
    
    #Enemies have an originY, and they have a yPos; when loading, their yPos will be off screen, and they will move down into view, and when they have moved to their originY positions, the action starts
    if loading:
        originY = enemylist[0].yPos
        offset = -(level.rows * 32 + (level.rows - 1) * level.ySpace + 170) #calculates how much the enemies are going to be moved up for animation

        for enemy in enemylist:
            enemy.yPos += offset
            enemy.baseY += 120*enemy.animY

    #Game loop
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue
            
            if event.type == pygame.KEYDOWN:
                #shooting
                if event.key == pygame.K_UP and not loading: #can't shoot if the enemies are loading
                    player.shoot(bulletlist, enemylist, bullettype = "normal")

                #big bullet
                if event.key == pygame.K_z and not loading:
                    if not bigbullet: #if there isn't a bigbullet active
                        if global_data["bigbullets"] > 0: #and you still have bigbullets left to shoot
                            
                            bigbullet = player.shoot(bulletlist, enemylist, bullettype = "bigbullet") #creates a bigbullet

                            #updates the global data and item trackers
                            global_data["bigbullets"] -= 1
                            bigbullet_tracker.update(global_data["bigbullets"])
                        
                    else: #If there is a bigbullet active, detonate it creating a blast (explosion wave that damages enemies)
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
                
                #If player presses ENTER, it skips the loading animation
                if event.key == pygame.K_RETURN and loading:
                    loading = False

                    
        #Player movement
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            player.move(-1)
        if keys[K_RIGHT]:
            player.move(1)
        if keys[K_UP] and player.superpowers["cheatshot"] == True: #If the "cheatshot" cheat is activated, the player will shoot every frame, if shootbutton is down
            player.shoot(bulletlist, enemylist)
        
        #if the game is not loading anymore, do actual calculations
        if not loading:

            #updating bullets
            for bullet in bulletlist:
                bullet.move(bulletlist, enemylist, explosionlist, remove_animations_list, player)
                if bullet.yPos < (0 - bullet.ySize) or bullet.yPos > 600:
                    if bullet.type == "bigbullet":
                        bigbullet = None
                    bulletlist.remove(bullet)
                    
            #updating enemies
            for enemy in enemylist:
                enemy.move(enemStepX.step, enemStepY.step, x = True, y = True) #move enemy
                enemy.shoot(bulletlist, shootStep.step, player) #If it's time for enemy to shoot, it'll shoot
            
            #updating money counter
            money_tracker.update(value=global_data["money"])

        else: #if the enemies are still loading (sliding in from top), more them a bit down, and check if they have reached the target position
            for enemy in enemylist:
                enemy.yPos += lspeed
            if enemylist[0].yPos >= originY:
                loading = False

        #clear screen
        window.fill((0, 0, 0))

        #draw player
        player.draw(window) 

        #draw all bullets
        for bullet in bulletlist: 
            bullet.draw(window)

        #draw miscellanous objects
        for obj in miscobjectslist:
            obj.draw(window)

            #animated objects should also be updated
            if obj.type == "decay":
                obj.update(miscobjectslist)
            
            elif obj.type == "blast":
                obj.update(animationStep.step, enemylist, miscobjectslist, explosionlist)
        


        #draw enemies, and if not loading, move each enemy down by a bit, (this is their natural motion, as enemies want to move past you, where they die and remove a life from player)
        for enemy in enemylist: 
            enemy.draw(window)
            if not loading:
                enemy.baseY += 0.05 #moves every enemy down by a bit

                if enemy.yPos > 600: #if enemy has moved past player, destroy the enemy and remove 1 life from player
                        enemylist.remove(enemy)
                        player.removeLife(remove_animations_list)

                if enemy.baseY >= 430: #If enemy is far enough down, and collides with player, create explosion, destroy enemy and remove 1 life from player

                    if (enemy.yPos + enemy.ySize) >= player.yPos and (enemy.xPos <= player.xPos + player.xSize and enemy.xPos >= player.xPos - 32):
                        explosionlist.append(Animation(enemy.xPos, enemy.yPos, frames="explosion_small", fps=6))
                        enemylist.remove(enemy)
                        player.removeLife(remove_animations_list)
                

        #draw and update explosions
        for explosion in explosionlist:
            explosion.draw(window)
            explosion.update(animationStep.step, explosionlist)

        #draw and update life animations at the bottom of screen
        for life in player.liveslist:
            life.draw(window)
            life.update(animationStep.step)
        
        #draw and update other animations
        for animation in remove_animations_list:
            animation.draw(window)
            animation.update(animationStep.step, remove_animations_list)

        #DRAWING TEXT WHEN LOADING UP LEVEL
        if loading:
            window.blit(stext, stextRect) #show text

        #updates the screen
        pygame.display.update()

        #makes sure to update the stepobjects when game is not loading
        if not loading:
            for step in stepObjects:
                step.update()

        #check if player has killed all enemies, return players position if he survived
        if len(enemylist) == 0:
            outcome = doscrolltext(window, finishtext, font)
            if outcome == False:
                return outcome
            
            return [player.xPos, player.yPos]
        
        #check if players life is zero, return False if it is 
        if player.life == 0:
            doscrolltext(window, gameovertext, font)
            return False

        #limit framerate to 60 fps
        clock.tick(60)
    
    return False


def doLevelSelectionScreen(window):

    """ Runs the level selection screen with a window as the drawing surface.
        Makes sure to generate new levels, and run those levels when they are selected,
        as well as keeping track of other things. """

    #Gets the global variables
    global travelpoint_boundaries
    global global_data

    #Initializes stepobjects for animations
    stepobjects = []
    animationStep = StepObject(1, 60, 1, False, 1)
    stepobjects.append(animationStep)


    heart_animation = Animation(600, 400, "heart", 12)#Creates an animation for a rotating heart (counter for lives)
    bigbullet_sprite = Drawable(608, 436, "bigbullet")#Creates a static sprite for a bigbullet icon (counter for big bullets)
    coin_sprite = Drawable(600, 472, "coin")#Creates a static sprite for a coin (used in the counter for coins)
    misc_drawable_objects = [heart_animation, bigbullet_sprite, coin_sprite]

    #Initializes a list of all travelpoints in area, and initializes the initial travelpoint
    travelpoints = []
    tp1 = TravelPoint(50, math.floor(travelpoint_boundaries[1][1]/2), math.floor(random.randint(10, 15)*global_data["diff_multi"]), tp_list = travelpoints)

    #Initializes the information table that displays data about the travelpoint the mouse would hover over
    info_table = InformationTable(current_travelpoint=tp1)

    #Gets the current mouse position, and gets the travelpoint the mouse currently is over, whilst updating the informationtable
    mouse_pos = pygame.mouse.get_pos()
    tp_hover = get_tp_at_mouse(mouse_pos, travelpoints, info_table)

    #Starts the loop
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue
            
            #If mouse moves, get the new mouse position and update the info table<
            if event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                tp_hover = get_tp_at_mouse(mouse_pos, travelpoints, info_table)
                
            
            #If mouse clicks and is currently hovering over a travelpoint, it sets tp_clicked to the travelpoint currently hovered over
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    #tp_clicked = get_tp_at_mouse(mouse_pos, travelpoints)
                    tp_clicked = tp_hover
                    if tp_clicked == None: #If no travelpoint is hovered over, then break out of the event checking loop, since the next part is about running the selected level
                        break
                    
                    if tp_clicked.parent != None: #If this isn't the starting travelpoint, then set all the other choices for a new level to unavailable, because user is only allowed to choose one
                        for child in tp_clicked.parent.children:
                            child.accessible = False
                            child.current = False



                    tp_clicked.current = True

                    #The difficulty multiplier increases with each selected level
                    global_data["diff_multi"] += global_data["diff_multi_increase"]

                    #Generates new children for the selected travelpoint, that will be available to choose when current travelpoint/level is cleared by player
                    result = tp_clicked.generate_children(travelpoints) #Function returns "end" if the player has completed the last travelpoint in this area
                    tp_clicked.visited = True               

                    if tp_clicked.type == 0:

                        #doing the actual level selectewd by user
                        randomlevelLayout = generateLayout(d=tp_clicked.diff) #generates a random level layout with the travelpoints difficulty

                        #creates the actual level based on the level layout
                        randomlevel = Level(randomlevelLayout, rows = len(randomlevelLayout), columns = len(randomlevelLayout[0]), xMargin = "center", yMargin = 64, xSpace = 20, ySpace = 20, pawn_anim=(0.5, 0.5), rook_anim=(0.0, 0.5), invader_anim=(0.6, 0.5))

                        #runs the level, if outcome is False, the player has died, else the outcome is True
                        outcome = doLevel(window, randomlevel, loading=True, lspeed=2, pstart="center", planetname = tp_clicked.name)
                    elif tp_clicked.type == 1:
                        outcome = doShop(window)

                    #Updates the counters for lives and big bullets on the information table
                    info_table.do_misc()

                    if outcome == False: #Returns False if player died during level
                        return False


                    if result == "end": #If the player has completed the last travelpoint in this area, returns True
                        return True

        #update the stepobjects
        for step in stepobjects:
            step.update()

        heart_animation.update(animationStep.step) #updates the heart animation with the new step

        #clear the screen
        window.fill((0,0,0))

        #draw the travelpoints and such
        for tp in travelpoints:
            tp.hover = True if tp == tp_hover else False          
            tp.draw_line_to_children(window)
            tp.draw(window)
      
        #draw the information table
        info_table.draw(window)

        #drawing misc items, such as life animations and static sprites    
        for drawable in misc_drawable_objects:
            drawable.draw(window)

        #updates display
        pygame.display.update()

        #limits framerate to 60fps
        clock.tick(60)
    
    return False

def doShop(window):
    '''Function for running the environment, when player enters Shop.'''
    global global_data
    global superpowers

    #
    # Two sections, first section where you can buy x = [0, 554]
    #
    # Second section where you see image and text x = [555, 810]
    #
    # Also need some lines somwhere
    #

    #Rendering the area title text
    title_text = pygame.font.SysFont("Arial", 64).render("SHOP", False, (255, 255, 255))
    title_text_rect = title_text.get_rect()
    title_text_rect.center = (277, 38)

    #Preparing all the lines to be drawn
    borders = [((0, 70), (554, 70)), 
            ((554, 0), (554, 600)),            
            ((554, 256), (810, 256)),
            ((0, 598), (810, 598)),
            ((0, 0), (810, 0)),
            ((808, 0), (808, 600)),
            ((0, 0), (0, 600))]

    #Creating onclick events for buttons
    global shop_prices

    def btn_life_onclick(object=None):
        life_price = shop_prices["life"]
        if global_data["money"] >= life_price:
            global_data["lives"] += 1
            global_data["money"] -= life_price

            lifetracker.update(global_data["lives"])
            cointracker.update(global_data["money"])
    
    def btn_bigbullet_onclick(object=None):
        bigbullet_price = shop_prices["bigbullet"]
        if global_data["money"] >= bigbullet_price:
            global_data["bigbullets"] += 1
            global_data["money"] -= bigbullet_price

            bigbullettracker.update(global_data["bigbullets"])
            cointracker.update(global_data["money"])
    
    def btn_tripleshot_onclick(object=None):
        tripleshot_price = shop_prices["tripleshot"]
        if global_data["money"] >= tripleshot_price and not object.purchased:
            superpowers["tripleshot"] = True
            global_data["money"] -= tripleshot_price
            object.purchased = superpowers["tripleshot"]

            cointracker.update(global_data["money"])

        

    #Creating all clickable buttons
    buttonlist = []
    #Creating flavourtexts for all relevant buttons:
    bigbullet_fvtext = ["A detonatable bullet that","causes a big explosion,","destroying several targets.","Press Z to fire projectile,","and Z again to detonate it."]
    life_fvtext = ["An extra life to save you","from trouble."]
    tripleshot_fvtext = ["A powerful upgrade for your","ship. Allows you to permantly", "fire 3 projectiles at once in a","volley."]
    #each button is 158px wide, 235px tall, and the space is 20 px between buttons on x axis and y axis
    #also each button has a flavourtext as described earlier
    btn_bigbullet = Button(image="bigbullet", image_pos=(71, 101), size=(158, 235), pos=(20, (20+70)), onclick=btn_bigbullet_onclick, price=shop_prices["bigbullet"], flavourtext=bigbullet_fvtext)
    btn_life = Button(image="heart", image_pos=(63, 101), size=(158, 235), pos=(20+(158+20), (20+70)), onclick=btn_life_onclick, price=shop_prices["life"], flavourtext=life_fvtext)
    btn_tripleshot = Button(image="player_tripleshot", image_pos=(55, 86), size=(158, 235), pos=(20+(158+20)*2, (20+70)), onclick=btn_tripleshot_onclick, purchased=superpowers["tripleshot"], price=shop_prices["tripleshot"], flavourtext=tripleshot_fvtext)


    btn_back = Button(image="backarrow", image_pos=(24, 8), size=(96, 48), pos=(20, 11), price=None)
    btn_back.lift = False

    btn_life.render()
    btn_bigbullet.render()
    btn_tripleshot.render()

    btn_back.render()

    buttonlist.append(btn_life)
    buttonlist.append(btn_tripleshot)
    buttonlist.append(btn_bigbullet)
    buttonlist.append(btn_back)
    
    # Initializes Itemtrackers to display information about items you have bought

    itemtrackers = []
    cointracker = ItemTracker(558, 2, 250, 36, global_data["money"], "coin")
    lifetracker = ItemTracker(558, 38, 250, 36, global_data["lives"], "heart_sprite")
    bigbullettracker = ItemTracker(566, 74, 242, 36, global_data["bigbullets"], "bigbullet")

    itemtrackers.append(cointracker)
    itemtrackers.append(lifetracker)
    itemtrackers.append(bigbullettracker)

    # Initializes stepobjects for animations
    stepobjects = []
    animationStep = StepObject(1, 60, 1, False, 1)
    stepobjects.append(animationStep)

    
    mouse_pos = pygame.mouse.get_pos()
    button_hover = None
    current_flavourtext = None

    running = True
    clock = pygame.time.Clock()
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue
                
            if event.type == MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()

                #determine which button is currently hover over
                button_hover = None
                current_flavourtext = None
                for button in buttonlist:
                    if (mouse_pos[0] > button.rect.left) and (mouse_pos[0] < (button.rect.right)) and (mouse_pos[1] > button.rect.top) and (mouse_pos[1] < (button.rect.bottom)):
                        button.active = True
                        button_hover = button
                        current_flavourtext = button_hover.fsurface
                    else:
                        button.active = False
                    button.render()
            
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and button_hover:
                    if button_hover == btn_back:
                        return True
                    elif button_hover.onclick_event:
                        button_hover.onclick()

        for stepobject in stepobjects:
            stepobject.update()

        window.fill((0, 0, 0))

        #Draw Here
        window.blit(title_text, title_text_rect)

        for border in borders:
            pygame.draw.line(window, (255, 255, 255), border[0], border[1], 2)

        for button in buttonlist:
            button.draw(window)
        
        #Drawing the money counter and stuff to the right (including flavourtext)
        for tracker in itemtrackers:
            tracker.draw(window)
        if current_flavourtext != None:
            window.blit(current_flavourtext, (560, 258))

        pygame.display.update()
        clock.tick(60)

    return False

def doMainMenu(window):
    '''Runs the main menu.'''

    def btn_menu_render(self):
        '''Custom render function for a menu button'''

        bgcolor = (0, 0, 0)
        if self.param['active'] == True:
            bgcolor = (100, 100, 100)


        font = pygame.font.SysFont("Arial", 32)
        text = font.render(self.param["text"], True, (255, 255, 255), bgcolor)
        text_rect = text.get_rect()
        text_rect.center = (self.size[0]/2, self.size[1]/2)

        self.surface.fill(bgcolor)
        self.surface.blit(text, text_rect)
        pygame.draw.rect(self.surface, (255, 255, 255), ((0, 0), (self.size[0], self.size[1])), 3)
    
    
    def btn_play_onclick(self):
        '''Onclick event action for menu PLAY button.'''
        out = doLevelSelectionScreen(window)
        running = out
        while out: # a do-while loop would have been ideal
            global_data["area"] += 1

            if global_data["shopchance"] < 0.15:
                global_data["shopchance"] = global_data["shopchance"]*1.1

            out = doLevelSelectionScreen(window)
        

    # Define a list of buttons beforehand
    buttonlist = []

    # Create a PowerButton object, serving as the PLAY button.
    btn_play = PowerButton((192, 64), (405, 300), renderfunction=btn_menu_render, onclick=btn_play_onclick, param={'active': False, 'text': "PLAY"})
    btn_play.rect.center = btn_play.pos

    #btn_options = PowerButton((192, 64), (405, 372), renderfunction=btn_menu_render, onclick=None, param={'active': False, 'text': "OPTIONS"})
    #btn_options.rect.center = btn_options.pos

    buttonlist.append(btn_play)
    #buttonlist.append(btn_options)

    # Prepare mouse position and hover object before action loop
    mouse_pos = pygame.mouse.get_pos()
    button_hover = None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue
                
            if event.type == MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()

                # Determine which button is currently hovered over
                button_hover = None
                for button in buttonlist:

                    if isinstance(button, PowerButton):
                        if (mouse_pos[0] > button.rect.left) and (mouse_pos[0] < (button.rect.right)) and (mouse_pos[1] > button.rect.top) and (mouse_pos[1] < (button.rect.bottom)):
                            button_hover = button
                            button.param['active'] = True
                        else:
                            button.param['active'] = False                        
                        button.update()

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and button_hover:
                    if button_hover.onclick_event:
                        button_hover.onclick()
        
        # Clear screen
        window.fill((0, 0, 0))

        # Draw stuff
        for button in buttonlist:
            button.draw(window)
        

        # Update display
        pygame.display.update()

#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#
#GAME IS RUN HERE
#
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------

if getattr(sys, 'frozen', False): #Does something very important for file management
    os.chdir(sys._MEIPASS)

#Initializes pygame window
pygame.init()
dim = (810, 600)
window = pygame.display.set_mode(dim)
pygame.display.set_caption("INVADERS")

#Calls load_content function that loads sprites and other content into RAM
content = load_content()

#Setting global parameters, such as the range in which travelpoints can be drawn, and values for difficulty scaling etc.
travelpoint_boundaries = ((10, 10), (800, 380))
global_data = {"lives": 8, "diff_multi": 1.0, "area": 1, "bigbullets": 0, "shopchance": 0.08, "money": 0, "kill_reward": 10, "diff_multi_increase": 0.15}
shop_prices = {"life": 190, "bigbullet": 110, "tripleshot": 1478}
superpowers = {
            "tripleshot" : False,
            "cheatshot" : False,
            "lifecontrol" : False,
            "conshot" : False
        }

#starting the level selection screen
#out = doLevelSelectionScreen(window) #launches the level selection screen with the created window as the drawing surface
out = doMainMenu(window)
sys.exit()