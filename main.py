# Hi!!!!!!!!!! This is a gamE!!!
import time
import pygame
import sys
from pygame.locals import *
import random

from timeit import default_timer as timer


class MessageDisplay:
    """Helper class for handling messages that should be shown to the user.
    Class instance attributes:
    font: pygame.freetype.SysFont -- the font of the displayed messages
    font_size: int -- the font size (in pixels) of the displayed messages
    font_color: (int, int, int) -- the RGB color of the displayed messages
    msg_height: float -- factor between 0 and 1 that determines the height
    at which messages are displayed (where 0 is the top and 1 is the bottom)
    message
    message: str -- the message that should be displayed
    dispatch_start: default_timer -- a timer that keeps track of when a message
    started displaying
    show: bool -- whether the message should be displayed
    """

    def __init__(
        self,
        font=None,
        font_size=24,
        font_color=(255, 255, 255),
        msg_height=0.5,
    ):
        self.font_size = font_size
        self.font_color = font_color
        if font is None:
            self.font = pygame.freetype.SysFont("Arial", font_size)
        else:
            self.font = font
        self.msg_height = msg_height
        self.message = ""
        self.dispatch_start = timer()
        self.show = True

    def word_wrap(self, screen, text, font, color):
        """Render message to screen with word wrap.
        Slightly modified from the pygame documentation here
        pygame.org/docs/ref/freetype.html#pygame.freetype.Font.render_to
        """
        font.origin = True
        words = text.split(" ")
        width, height = screen.get_size()
        width *= 0.9
        line_spacing = font.get_sized_height() + 2
        x, y = 0.2 * screen.get_width(), self.msg_height * screen.get_height()
        line_words = ""
        for word in words:
            line_words += word + " "
            bounds = font.get_rect(line_words)
            if x + bounds.x + bounds.width >= width:
                rx = 0.5 * screen.get_width() - 0.5 * bounds.width
                font.render_to(screen, (rx, y), None, color)
                x, y = 0.2 * screen.get_width(), y + line_spacing
                line_words = ""
        rx = 0.5 * screen.get_width() - 0.5 * bounds.width
        font.render_to(screen, (rx, y), None, color)

    def show_message(self, msg, time_sec=3):
        """Set a message to be shown to the screen."""
        self.message = msg
        self.dispatch_start = timer() + time_sec
        self.show = True

    def render_message(self, screen):
        """Render a message to the screen (called every frame)"""
        if self.show:
            if self.dispatch_start - timer() < 0:
                self.show = False
            # only wrap if text doesn't fit neatly on the screen
            full_rectangle = self.font.get_rect(self.message)
            if full_rectangle.width > 0.9 * screen.get_width():
                self.word_wrap(screen, self.message,
                               self.font, self.font_color)
            else:
                x, y = (
                    0.5 * screen.get_width() - 0.5 * full_rectangle.width,
                    self.msg_height * screen.get_height(),
                )
                self.font.render_to(screen, (x, y),
                                    self.message, self.font_color)


# initialization
pygame.init()
pygame.freetype.init()
clock = pygame.time.Clock()


WIDTH = 640
HEIGHT = 640
FPS = 60
GAMETITLE = "Where's Mom?"
SUBTITLE = "An Innocent Game with No Plot Twists"
STARTTEXT = "Press Enter to Start"
# colours

LIGHTCREAM = (241, 241, 241)
BLUEBLACK = (44, 51, 51)

# fonts

GAMETITLEFONT = pygame.freetype.Font('./fonts/CubicPixel.otf', 135)
GTITLEDISP = MessageDisplay(GAMETITLEFONT, 135, BLUEBLACK, 0.4)

SUBTITLEFONT = pygame.freetype.Font(
    './fonts/EmotionEngine.ttf', 30)
SUBTITLEDISP = MessageDisplay(SUBTITLEFONT, 30, BLUEBLACK, 0.7)


STARTFONT = pygame.freetype.Font('./fonts/PixelEmulator.ttf', 15)
STARTDISP = MessageDisplay(STARTFONT, 15, BLUEBLACK, 0.9)

buttonFont = pygame.font.Font('./fonts/PixelEmulator.ttf', 15)

tickCount = 0

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(GAMETITLE)
icon = pygame.image.load('./img/search.png')
pygame.display.set_icon(icon)

creatorIcon = pygame.image.load('./img/buildersiconography.png')
creatorIcon = pygame.transform.smoothscale(creatorIcon, (WIDTH, HEIGHT))

magLgIcon = pygame.image.load('./img/search-lg.png')
magLgIcon = pygame.transform.smoothscale(magLgIcon, (100, 100))
magRect = magLgIcon.get_rect()

# user typing
base_font = pygame.font.Font('./fonts/PixelEmulator.ttf', 32)
user_text = ''

# story text
speakerFont = pygame.freetype.Font('./fonts/PixelEmulator.ttf', 30)
storyFont = pygame.freetype.Font('./fonts/PixelEmulator.ttf', 18)
tipsFont = pygame.freetype.Font('./fonts/PixelEmulator.ttf', 13)
textbox = pygame.image.load('./img/UIAssets/Textbox.png')

tipsbox = pygame.image.load('./img/UIAssets/TipsBox.png')

itemBox = pygame.image.load('./img/UIAssets/ItemBoard.png')

# game assets
attentionBubble = pygame.image.load(
    './img/UIAssets/attentionBubble.png')


input_rect = pygame.Rect(0, 0, 400, 42)
input_rect.centerx = WIDTH/2
input_rect.centery = HEIGHT/2

# color_active stores color(lightskyblue3) which
# gets active when input box is clicked by user
color_active = pygame.Color('chartreuse4')

# color_passive store color(chartreuse4) which is
# color of input box.
color_passive = pygame.Color(255, 31, 1)
color = color_passive
hover_colour = "#E64848"

hover_active = False
box_active = False

userInventory = []

# bound rect


class BoundarySprite(pygame.sprite.Sprite):
    def __init__(self, img, originx=0, originy=0):
        super().__init__()
        self.image = img
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.originx = originx
        self.originy = originy

    def position(self, x, y):
        self.rect.center = (x, y)


# settings

# bedroom
bedroomBG = pygame.image.load('./img/bkg/Bedroom.png')
bedroomMask = pygame.image.load(
    './img/bkgBounds/BedroomMask.png')
bedroomSprite = BoundarySprite(bedroomMask)
bedroomNextImg = pygame.image.load(
    './img/next/BedroomNext.png')
bedroomNext = BoundarySprite(bedroomNextImg, 510, 360)

# hallway
hallwayBG = pygame.image.load('./img/bkg/Hallway.png')
hallwayMask = pygame.image.load('./img/bkgBounds/HallwayBound.png')
hallwaySprite = BoundarySprite(hallwayMask, WIDTH-120, HEIGHT/2+40)
HallwayBedroomNextImg = pygame.image.load(
    './img/next/HallwayToBedroom.png')
hallwayBedroomNext = BoundarySprite(HallwayBedroomNextImg, 320, 540)
HallwayKitchenNextImg = pygame.image.load(
    './img/next/HallwaytoKitchen.png')
HallwayKitchenNext = BoundarySprite(HallwayKitchenNextImg, 215, 510)
HallwayParentNextImg = pygame.image.load(
    './img/next/HallwayToParent.png')
HallwayParentNext = BoundarySprite(HallwayParentNextImg, 320, 540)

# Kitchen
kitchenBG = pygame.image.load('./img/bkg/Kitchen.png')
kitchenMask = pygame.image.load('./img/bkgBounds/KitchenBound.png')
kitchenSprite = BoundarySprite(kitchenMask, 2*WIDTH/3, HEIGHT/3+40)
KitchenHallwayNextImg = pygame.image.load(
    './img/next/KitchenToHallway.png')
KitchenDiningNextImg = pygame.image.load(
    './img/next/KitchenToDining.png')
KitchenHallwayNext = BoundarySprite(KitchenHallwayNextImg, 325, 360)
KitchemDiningNext = BoundarySprite(KitchenDiningNextImg, 60, 460)

# Parent Room
parentBG = pygame.image.load('./img/bkg/ParentRoom.png')
parentMask = pygame.image.load(
    './img/bkgBounds/ParentRoomBound.png')
parentRmSprite = BoundarySprite(parentMask, WIDTH/2, HEIGHT-80)
ParentRoomNextImg = pygame.image.load(
    './img/next/ParentRoomNext.png')
ParentRoomNext = BoundarySprite(ParentRoomNextImg, 150, 360)

# Dining Room
diningBG = pygame.image.load('./img/bkg/DiningRoom.png')
diningMask = pygame.image.load(
    './img/bkgBounds/DiningBound.png')
diningSprite = BoundarySprite(diningMask, WIDTH-50, 2*HEIGHT/3)
diningKitchenNextImg = pygame.image.load(
    './img/next/DiningToKitchen.png')
diningKitchenNext = BoundarySprite(diningKitchenNextImg, 550, 460)
diningGardenNextImg = pygame.image.load(
    './img/next/DiningToGarden.png')
diningGardenNext = BoundarySprite(diningGardenNextImg, 320, 540)

# Garden
gardenBG = pygame.image.load('./img/bkg/Garden.png')
gardenMask = pygame.image.load('./img/bkgBounds/GardenBound.png')
gardenSprite = BoundarySprite(gardenMask)
gardenNextImg = pygame.image.load('./img/next/GardenNext.png')
gardenNext = BoundarySprite(gardenNextImg, 500, 230)


roomslist = [bedroomSprite, hallwaySprite, kitchenSprite, diningSprite]

roomSprites = pygame.sprite.Group()
for i in roomslist:
    roomSprites.add(i)

# object assets
dirtMound = pygame.image.load(
    './img/objectAssets/DirtMound.png')
dirtMoundSprite = BoundarySprite(dirtMound)

diningTable = pygame.image.load(
    './img/objectAssets/DiningTable.png')
diningTableSprite = BoundarySprite(diningTable)


class Object(pygame.sprite.Sprite):
    def __init__(self, img):
        self.image = img
        self.mask = pygame.mask.from_surface(img)
        self.rect = img.get_rect()
        self.interacted = False
        self.rect.midbottom = (320, 320)

    def position(self, x, y):
        self.rect.midbottom = (x, y)


ring = pygame.image.load(
    './img/objectAssets/Ring.png')
ringSprite = BoundarySprite(ring)

gardenObjects = pygame.sprite.Group()
gardenObjects.add(dirtMoundSprite)
gardenObjects.add(ringSprite)


jojo = pygame.image.load(
    './img/objectAssets/PhotoSmall.png')
jojoSprite = BoundarySprite(jojo)

marPic1 = pygame.image.load(
    './img/objectAssets/marPic1.png')
marPic1Sprite = BoundarySprite(marPic1)

marPic2 = pygame.image.load(
    './img/objectAssets/marPic2.png')
marPic2Sprite = BoundarySprite(marPic2)

boxSmall = pygame.image.load(
    './img/objectAssets/boxSmall.png')
boxSmallSprite = BoundarySprite(boxSmall)

parentRoomObjects = pygame.sprite.Group()
parentRoomObjects.add(jojoSprite, marPic1Sprite, marPic2Sprite, boxSmallSprite)


# sprite images
walkRight = [pygame.image.load('./img/playersprite/1x/Right1.png'), pygame.image.load('./img/playersprite/1x/Right2.png'), pygame.image.load('./img/playersprite/1x/Right3.png'), pygame.image.load('./img/playersprite/1x/Right4.png'), pygame.image.load(
    './img/playersprite/1x/Right5.png'), pygame.image.load('./img/playersprite/1x/Right6.png'), pygame.image.load('./img/playersprite/1x/Right7.png'), pygame.image.load('./img/playersprite/1x/Right8.png'), pygame.image.load('./img/playersprite/1x/Right9.png')]
walkLeft = [pygame.image.load('./img/playersprite/1x/Left1.png'), pygame.image.load('./img/playersprite/1x/Left2.png'), pygame.image.load('./img/playersprite/1x/Left3.png'), pygame.image.load('./img/playersprite/1x/Left4.png'), pygame.image.load(
    './img/playersprite/1x/Left5.png'), pygame.image.load('./img/playersprite/1x/Left6.png'), pygame.image.load('./img/playersprite/1x/Left7.png'), pygame.image.load('./img/playersprite/1x/Left8.png'), pygame.image.load('./img/playersprite/1x/Left9.png'), ]
walkUp = [pygame.image.load('./img/playersprite/1x/Up1.png'), pygame.image.load('./img/playersprite/1x/Up2.png'), pygame.image.load('./img/playersprite/1x/Up3.png'), pygame.image.load('./img/playersprite/1x/Up4.png'), pygame.image.load(
    './img/playersprite/1x/Up5.png'), pygame.image.load('./img/playersprite/1x/Up6.png'), pygame.image.load('./img/playersprite/1x/Up7.png'), pygame.image.load('./img/playersprite/1x/Up8.png'), pygame.image.load('./img/playersprite/1x/Up9.png'), ]
walkDown = [pygame.image.load('./img/playersprite/1x/Down1.png'), pygame.image.load('./img/playersprite/1x/Down2.png'), pygame.image.load('./img/playersprite/1x/Down3.png'), pygame.image.load('./img/playersprite/1x/Down4.png'), pygame.image.load(
    './img/playersprite/1x/Down5.png'), pygame.image.load('./img/playersprite/1x/Down6.png'), pygame.image.load('./img/playersprite/1x/Down7.png'), pygame.image.load('./img/playersprite/1x/Down8.png'), pygame.image.load('./img/playersprite/1x/Down9.png'), ]


dwalkRight = [pygame.image.load('./img/playersprite/1x/Right1.png'), pygame.image.load('./img/playersprite/1x/Right2.png'), pygame.image.load('./img/playersprite/1x/Right3.png'), pygame.image.load('./img/playersprite/1x/Right4.png'), pygame.image.load(
    './img/playersprite/1x/Right5.png'), pygame.image.load('./img/playersprite/1x/Right6.png'), pygame.image.load('./img/playersprite/1x/Right7.png'), pygame.image.load('./img/playersprite/1x/Right8.png'), pygame.image.load('./img/playersprite/1x/Right9.png')]
dwalkLeft = [pygame.image.load('./img/playersprite/1x/Left1.png'), pygame.image.load('./img/playersprite/1x/Left2.png'), pygame.image.load('./img/playersprite/1x/Left3.png'), pygame.image.load('./img/playersprite/1x/Left4.png'), pygame.image.load(
    './img/playersprite/1x/Left5.png'), pygame.image.load('./img/playersprite/1x/Left6.png'), pygame.image.load('./img/playersprite/1x/Left7.png'), pygame.image.load('./img/playersprite/1x/Left8.png'), pygame.image.load('./img/playersprite/1x/Left9.png'), ]
dwalkUp = [pygame.image.load('./img/playersprite/1x/Up1.png'), pygame.image.load('./img/playersprite/1x/Up2.png'), pygame.image.load('./img/playersprite/1x/Up3.png'), pygame.image.load('./img/playersprite/1x/Up4.png'), pygame.image.load(
    './img/playersprite/1x/Up5.png'), pygame.image.load('./img/playersprite/1x/Up6.png'), pygame.image.load('./img/playersprite/1x/Up7.png'), pygame.image.load('./img/playersprite/1x/Up8.png'), pygame.image.load('./img/playersprite/1x/Up9.png'), ]
dwalkDown = [pygame.image.load('./img/playersprite/1x/Down1.png'), pygame.image.load('./img/playersprite/1x/Down2.png'), pygame.image.load('./img/playersprite/1x/Down3.png'), pygame.image.load('./img/playersprite/1x/Down4.png'), pygame.image.load(
    './img/playersprite/1x/Down5.png'), pygame.image.load('./img/playersprite/1x/Down6.png'), pygame.image.load('./img/playersprite/1x/Down7.png'), pygame.image.load('./img/playersprite/1x/Down8.png'), pygame.image.load('./img/playersprite/1x/Down9.png'), ]


def scale_player(w, h):
    global walkDown
    global walkLeft
    global walkRight
    global walkUp
    global dwalkDown
    global dwalkLeft
    global dwalkRight
    global dwalkUp
    dwalkRight = [pygame.transform.smoothscale(i, (w, h)) for i in walkRight]
    dwalkLeft = [pygame.transform.smoothscale(i, (w, h)) for i in walkLeft]
    dwalkUp = [pygame.transform.smoothscale(i, (w, h)) for i in walkUp]
    dwalkDown = [pygame.transform.smoothscale(i, (w, h)) for i in walkDown]


# sister walk images
siswalkRight = [pygame.image.load('./img/sisterSprite/Right1.png'), pygame.image.load('./img/sisterSprite/Right2.png'), pygame.image.load('./img/sisterSprite/Right3.png'), pygame.image.load('./img/sisterSprite/Right4.png'), pygame.image.load(
    './img/sisterSprite/Right5.png'), pygame.image.load('./img/sisterSprite/Right6.png'), pygame.image.load('./img/sisterSprite/Right7.png'), pygame.image.load('./img/sisterSprite/Right8.png'), pygame.image.load('./img/sisterSprite/Right9.png')]
siswalkLeft = [pygame.image.load('./img/sisterSprite/Left1.png'), pygame.image.load('./img/sisterSprite/Left2.png'), pygame.image.load('./img/sisterSprite/Left3.png'), pygame.image.load('./img/sisterSprite/Left4.png'), pygame.image.load(
    './img/sisterSprite/Left5.png'), pygame.image.load('./img/sisterSprite/Left6.png'), pygame.image.load('./img/sisterSprite/Left7.png'), pygame.image.load('./img/sisterSprite/Left8.png'), pygame.image.load('./img/sisterSprite/Left9.png'), ]
siswalkUp = [pygame.image.load('./img/sisterSprite/Up1.png'), pygame.image.load('./img/sisterSprite/Up2.png'), pygame.image.load('./img/sisterSprite/Up3.png'), pygame.image.load('./img/sisterSprite/Up4.png'), pygame.image.load(
    './img/sisterSprite/Up5.png'), pygame.image.load('./img/sisterSprite/Up6.png'), pygame.image.load('./img/sisterSprite/Up7.png'), pygame.image.load('./img/sisterSprite/Up8.png'), pygame.image.load('./img/sisterSprite/Up9.png'), ]
siswalkDown = [pygame.image.load('./img/sisterSprite/Down1.png'), pygame.image.load('./img/sisterSprite/Down2.png'), pygame.image.load('./img/sisterSprite/Down3.png'), pygame.image.load('./img/sisterSprite/Down4.png'), pygame.image.load(
    './img/sisterSprite/Down5.png'), pygame.image.load('./img/sisterSprite/Down6.png'), pygame.image.load('./img/sisterSprite/Down7.png'), pygame.image.load('./img/sisterSprite/Down8.png'), pygame.image.load('./img/sisterSprite/Down9.png'), ]


dsiswalkRight = [pygame.image.load('./img/sisterSprite/Right1.png'), pygame.image.load('./img/sisterSprite/Right2.png'), pygame.image.load('./img/sisterSprite/Right3.png'), pygame.image.load('./img/sisterSprite/Right4.png'), pygame.image.load(
    './img/sisterSprite/Right5.png'), pygame.image.load('./img/sisterSprite/Right6.png'), pygame.image.load('./img/sisterSprite/Right7.png'), pygame.image.load('./img/sisterSprite/Right8.png'), pygame.image.load('./img/sisterSprite/Right9.png')]
dsiswalkLeft = [pygame.image.load('./img/sisterSprite/Left1.png'), pygame.image.load('./img/sisterSprite/Left2.png'), pygame.image.load('./img/sisterSprite/Left3.png'), pygame.image.load('./img/sisterSprite/Left4.png'), pygame.image.load(
    './img/sisterSprite/Left5.png'), pygame.image.load('./img/sisterSprite/Left6.png'), pygame.image.load('./img/sisterSprite/Left7.png'), pygame.image.load('./img/sisterSprite/Left8.png'), pygame.image.load('./img/sisterSprite/Left9.png'), ]
dsiswalkUp = [pygame.image.load('./img/sisterSprite/Up1.png'), pygame.image.load('./img/sisterSprite/Up2.png'), pygame.image.load('./img/sisterSprite/Up3.png'), pygame.image.load('./img/sisterSprite/Up4.png'), pygame.image.load(
    './img/sisterSprite/Up5.png'), pygame.image.load('./img/sisterSprite/Up6.png'), pygame.image.load('./img/sisterSprite/Up7.png'), pygame.image.load('./img/sisterSprite/Up8.png'), pygame.image.load('./img/sisterSprite/Up9.png'), ]
dsiswalkDown = [pygame.image.load('./img/sisterSprite/Down1.png'), pygame.image.load('./img/sisterSprite/Down2.png'), pygame.image.load('./img/sisterSprite/Down3.png'), pygame.image.load('./img/sisterSprite/Down4.png'), pygame.image.load(
    './img/sisterSprite/Down5.png'), pygame.image.load('./img/sisterSprite/Down6.png'), pygame.image.load('./img/sisterSprite/Down7.png'), pygame.image.load('./img/sisterSprite/Down8.png'), pygame.image.load('./img/sisterSprite/Down9.png'), ]


dadwalkRight = [pygame.image.load('./img/dadsprite/Right1.png'), pygame.image.load('./img/dadsprite/Right2.png'), pygame.image.load('./img/dadsprite/Right3.png'), pygame.image.load('./img/dadsprite/Right4.png'), pygame.image.load(
    './img/dadsprite/Right5.png'), pygame.image.load('./img/dadsprite/Right6.png'), pygame.image.load('./img/dadsprite/Right7.png'), pygame.image.load('./img/dadsprite/Right8.png'), pygame.image.load('./img/dadsprite/Right9.png')]
dadwalkLeft = [pygame.image.load('./img/dadsprite/Left1.png'), pygame.image.load('./img/dadsprite/Left2.png'), pygame.image.load('./img/dadsprite/Left3.png'), pygame.image.load('./img/dadsprite/Left4.png'), pygame.image.load(
    './img/dadsprite/Left5.png'), pygame.image.load('./img/dadsprite/Left6.png'), pygame.image.load('./img/dadsprite/Left7.png'), pygame.image.load('./img/dadsprite/Left8.png'), pygame.image.load('./img/dadsprite/Left9.png'), ]
dadwalkUp = [pygame.image.load('./img/dadsprite/Up1.png'), pygame.image.load('./img/dadsprite/Up2.png'), pygame.image.load('./img/dadsprite/Up3.png'), pygame.image.load('./img/dadsprite/Up4.png'), pygame.image.load(
    './img/dadsprite/Up5.png'), pygame.image.load('./img/dadsprite/Up6.png'), pygame.image.load('./img/dadsprite/Up7.png'), pygame.image.load('./img/dadsprite/Up8.png'), pygame.image.load('./img/dadsprite/Up9.png'), ]
dadwalkDown = [pygame.image.load('./img/dadsprite/Down1.png'), pygame.image.load('./img/dadsprite/Down2.png'), pygame.image.load('./img/dadsprite/Down3.png'), pygame.image.load('./img/dadsprite/Down4.png'), pygame.image.load(
    './img/dadsprite/Down5.png'), pygame.image.load('./img/dadsprite/Down6.png'), pygame.image.load('./img/dadsprite/Down7.png'), pygame.image.load('./img/dadsprite/Down8.png'), pygame.image.load('./img/dadsprite/Down9.png'), ]


def scale_sister(w, h):
    global siswalkDown
    global siswalkLeft
    global siswalkRight
    global siswalkUp
    global dsiswalkDown
    global dsiswalkLeft
    global dsiswalkRight
    global dsiswalkUp
    dsiswalkRight = [pygame.transform.smoothscale(
        i, (w, h)) for i in siswalkRight]
    dsiswalkLeft = [pygame.transform.smoothscale(
        i, (w, h)) for i in siswalkLeft]
    siswalkUp = [pygame.transform.smoothscale(i, (w, h)) for i in siswalkUp]
    dsiswalkDown = [pygame.transform.smoothscale(
        i, (w, h)) for i in siswalkDown]


scale_player(60, 100)

# game functions


def changeRoom(newRoom):
    global currentRoom
    currentRoom = newRoom


def redrawWindow(bg, mask, *next):
    if next:
        for i in next:
            screen.blit(i, (0, 0))
    screen.blit(mask, (0, 0))
    screen.blit(bg, (0, 0))

    tempmask = pygame.mask.from_surface(mask)


def checkRoomCollide(sprite, currentRoom):
    return pygame.sprite.collide_mask(sprite, currentRoom)


# sprites

class NPC(pygame.sprite.Sprite):
    def __init__(self, walkDown, walkUp, walkLeft, walkRight):
        pygame.sprite.Sprite.__init__(self)
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.facing = 'Down'
        self.walkCount = 0
        self.walkLeft = walkLeft
        self.walkRight = walkRight
        self.walkUp = walkUp
        self.walkDown = walkDown
        self.dwalkLeft = walkLeft
        self.dwalkRight = walkRight
        self.dwalkUp = walkUp
        self.dwalkDown = walkDown
        self.image = dwalkDown[0]
        self.moving = False
        self.rect = self.image.get_rect()
        self.rect.midbottom = (160, 240)
        self.mask = pygame.mask.from_surface(self.image)
        self.inMessage = False
        global attentionBubble
        self.attentionBubble = attentionBubble
        self.attention = True

    def scale(self, w, h):
        self.rect = self.image.get_rect()
        # self.walkDown
        # self.walkLeft
        # self.walkRight
        # self.walkUp
        # self.dwalkDown
        # self.dwalkLeft
        # self.dwalkRight
        # self.dwalkUp
        self.dwalkRight = [pygame.transform.smoothscale(
            i, (w, h)) for i in self.walkRight]
        self.dwalkLeft = [pygame.transform.smoothscale(
            i, (w, h)) for i in self.walkLeft]
        self.dwalkUp = [pygame.transform.smoothscale(
            i, (w, h)) for i in self.walkUp]
        self.dwalkDown = [pygame.transform.smoothscale(
            i, (w, h)) for i in self.walkDown]

    def position(self, x, y):
        self.rect.midbottom = (x, y)

    def facingd(self, direction):
        self.facing = direction

    def atAttention(self, boola=True):
        self.attention = boola

    def update(self, currentRoom):

        self.mask = pygame.mask.from_surface(self.image)
        self.speedx = 0
        self.speedy = 0
        # if not self.inMessage:
        #     key_state = pygame.key.get_pressed()
        #     opposemovex = -(self.rect.x-WIDTH/2)*0.1
        #     opposemovey = -(self.rect.y-HEIGHT/2)*0.1
        #     if key_state[pygame.K_RIGHT]:
        #         if not self.rect.right >= WIDTH:
        #             self.speedx = 8
        #             self.left = False
        #             self.right = True
        #             self.up = False
        #             self.down = False
        #         if checkRoomCollide(self, currentRoom):
        #             self.speedx = 0
        #             self.rect.x += opposemovex
        #             self.rect.y += opposemovey
        #     elif key_state[pygame.K_LEFT]:
        #         if not self.rect.left <= 0:
        #             self.speedx = -8
        #             self.left = True
        #             self.right = False
        #             self.up = False
        #             self.down = False
        #         if checkRoomCollide(self, currentRoom):
        #             self.speedx = 0
        #             self.rect.x += opposemovex
        #             self.rect.y += opposemovey
        #     elif key_state[pygame.K_UP]:
        #         if not self.rect.top <= 0:
        #             self.speedy = -8
        #             self.left = False
        #             self.right = False
        #             self.up = True
        #             self.down = False
        #         if checkRoomCollide(self, currentRoom):
        #             self.speedy = 0
        #             self.rect.x += opposemovex
        #             self.rect.y += opposemovey
        #     elif key_state[pygame.K_DOWN]:
        #         if not self.rect.bottom >= HEIGHT:
        #             self.speedy = 8
        #             self.left = False
        #             self.right = False
        #             self.up = False
        #             self.down = True
        #         if checkRoomCollide(self, currentRoom):
        #             self.speedy = 0
        #             self.rect.x += opposemovex
        #             self.rect.y += opposemovey
        #     else:
        #         self.left = False
        #         self.right = False
        #         self.up = False
        #         self.down = False

        #     self.rect.centerx += self.speedx
        #     self.rect.centery += self.speedy
        #     if self.walkCount+1 >= 27:
        #         self.walkCount = 0

        #     if self.left:
        #         self.image = dwalkLeft[self.walkCount//3]
        #         self.walkCount += 1
        #     elif self.right:
        #         self.image = dwalkRight[self.walkCount//3]
        #         self.walkCount += 1
        #     elif self.down:
        #         self.image = dwalkDown[self.walkCount//3]
        #         self.walkCount += 1
        #     elif self.up:
        #         self.image = dwalkUp[self.walkCount//3]
        #         self.walkCount += 1
        #     else:
        #         self.image = dwalkDown[0]
        self.image = self.dwalkDown[0]
        if not self.moving:
            if self.facing == "Down":
                self.image = self.dwalkDown[0]
            elif self.facing == "Up":
                self.image = self.dwalkUp[0]
            elif self.facing == "Left":
                self.image = self.dwalkLeft[0]
            elif self.facing == "Right":
                self.image = self.dwalkRight[0]
        if self.attention:
            screen.blit(self.attentionBubble,
                        (self.rect.topright[0]-15, self.rect.topright[1]-15))


Sister = NPC(siswalkDown, siswalkUp, siswalkLeft, siswalkRight)
Sister.scale(60, 100)

Dad = NPC(dadwalkDown, dadwalkUp, dadwalkLeft, dadwalkRight)
Dad.scale(60, 100)

sisterGroup = pygame.sprite.Group()
sisterGroup.add(Sister)

dadGroup = pygame.sprite.Group()
dadGroup.add(Dad)


class Player(pygame.sprite.Sprite):
    def __init__(self, username):
        pygame.sprite.Sprite.__init__(self)
        self.username = username
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.walkCount = 0
        self.image = walkDown[0]
        self.rect = self.image.get_rect()
        self.rect.midbottom = (160, 240)
        self.mask = pygame.mask.from_surface(self.image)
        self.inMessage = False
        global attentionBubble
        self.attentionBubble = attentionBubble
        self.attention = False

    def position(self, x, y):
        self.rect.midbottom = (x, y)

    def startMessage(self):
        self.inMessage = True

    def endMessage(self):
        self.inMessage = False

    def atAttention(self, boola=True):
        self.attention = boola

    def update(self, currentRoom):
        self.mask = pygame.mask.from_surface(self.image)

        self.speedx = 0
        self.speedy = 0
        if not self.inMessage:
            key_state = pygame.key.get_pressed()
            opposemovex = -(self.rect.x-WIDTH/2)*0.1
            opposemovey = -(self.rect.y-HEIGHT/2)*0.1
            if key_state[pygame.K_RIGHT]:
                if not self.rect.right >= WIDTH:
                    self.speedx = 8
                    self.left = False
                    self.right = True
                    self.up = False
                    self.down = False
                if checkRoomCollide(self, currentRoom):
                    self.speedx = 0
                    self.rect.x += opposemovex
                    self.rect.y += opposemovey
            elif key_state[pygame.K_LEFT]:
                if not self.rect.left <= 0:
                    self.speedx = -8
                    self.left = True
                    self.right = False
                    self.up = False
                    self.down = False
                if checkRoomCollide(self, currentRoom):
                    self.speedx = 0
                    self.rect.x += opposemovex
                    self.rect.y += opposemovey
            elif key_state[pygame.K_UP]:
                if not self.rect.top <= 0:
                    self.speedy = -6
                    self.left = False
                    self.right = False
                    self.up = True
                    self.down = False
                if checkRoomCollide(self, currentRoom):
                    self.speedy = 0
                    self.rect.x += opposemovex
                    self.rect.y += opposemovey
            elif key_state[pygame.K_DOWN]:
                if not self.rect.bottom >= HEIGHT:
                    self.speedy = 8
                    self.left = False
                    self.right = False
                    self.up = False
                    self.down = True
                if checkRoomCollide(self, currentRoom):
                    self.speedy = 0
                    self.rect.x += opposemovex
                    self.rect.y += opposemovey
            else:
                self.left = False
                self.right = False
                self.up = False
                self.down = False

            self.rect.centerx += self.speedx
            self.rect.centery += self.speedy
            if self.walkCount+1 >= 27:
                self.walkCount = 0

            if self.left:
                self.image = dwalkLeft[self.walkCount//3]
                self.walkCount += 1
            elif self.right:
                self.image = dwalkRight[self.walkCount//3]
                self.walkCount += 1
            elif self.down:
                self.image = dwalkDown[self.walkCount//3]
                self.walkCount += 1
            elif self.up:
                self.image = dwalkUp[self.walkCount//3]
                self.walkCount += 1
            else:
                self.image = dwalkDown[0]
            if self.attention:
                screen.blit(self.attentionBubble,
                            (self.rect.topright[0]+10, self.rect.topright[1]-10))


playerSpriteGrp = pygame.sprite.Group()


class Button:

    def __init__(self, text, width, height, pos, elevation) -> None:
        # toprect
        self.toprect = pygame.Rect(pos, (width, height))
        self.toprect.centerx = pos[0]
        self.toprect.centery = pos[1]
        self.top_color = "#FF1E00"
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.originalYpos = pos[1]
        self.text = text
        # bottom
        self.botton_rect = pygame.Rect(pos, (width, height))
        self.bottom_color = "#C21010"
        # text
        self.textsurf = buttonFont.render(text, True, '#FFFFFF')
        self.textrect = self.textsurf.get_rect(center=self.toprect.center)

    def draw(self):
        self.toprect.y = self.originalYpos-self.dynamic_elevation
        self.textrect.center = self.toprect.center

        self.botton_rect.midtop = self.toprect.midtop
        self.botton_rect.height = self.toprect.height+self.dynamic_elevation
        pygame.draw.rect(screen, self.bottom_color, self.botton_rect)

        pygame.draw.rect(screen, self.top_color, self.toprect)
        screen.blit(self.textsurf, self.textrect)

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.toprect.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            self.top_color = "#E64848"
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elevation = 0
                self.pressed = True

            else:
                self.dynamic_elevation = self.elevation
                if self.pressed == True:
                    self.pressed = False
                    self.top_color = "#59CE8F"
                    return True

        else:
            self.dynamic_elevation = self.elevation
            self.top_color = "#FF1E00"
            self.dynamic_elevation = self.elevation
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        return False


button1 = Button('Start Now', 200, 40, (WIDTH/2, HEIGHT/2+70), 6)


class ButtonKeep:

    def __init__(self, width, height, pos, elevation) -> None:
        # toprect
        self.toprect = pygame.Rect(pos, (width, height))
        self.toprect.centerx = pos[0]
        self.toprect.centery = pos[1]
        self.top_color = "#30F400"
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.originalYpos = pos[1]

        # bottom
        self.botton_rect = pygame.Rect(pos, (width, height))
        self.bottom_color = "#25A800"
        # text
        self.textsurf = buttonFont.render('Keep', True, '#FFFFFF')
        self.textrect = self.textsurf.get_rect(center=self.toprect.center)

    def draw(self):
        self.toprect.y = self.originalYpos-self.dynamic_elevation
        self.textrect.center = self.toprect.center

        self.botton_rect.midtop = self.toprect.midtop
        self.botton_rect.height = self.toprect.height+self.dynamic_elevation
        pygame.draw.rect(screen, self.bottom_color, self.botton_rect)

        pygame.draw.rect(screen, self.top_color, self.toprect)
        screen.blit(self.textsurf, self.textrect)

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.toprect.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            self.top_color = "#70EF4D"
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elevation = 0
                self.pressed = True

            else:
                self.dynamic_elevation = self.elevation
                if self.pressed == True:
                    self.pressed = False
                    self.top_color = "#70EF4D"
                    return True

        else:
            self.dynamic_elevation = self.elevation
            self.top_color = "#30F400"
            self.dynamic_elevation = self.elevation
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        return False


class ButtonDiscard:

    def __init__(self, width, height, pos, elevation) -> None:
        # toprect
        self.toprect = pygame.Rect(pos, (width, height))
        self.toprect.centerx = pos[0]
        self.toprect.centery = pos[1]
        self.top_color = "#F70000"
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.originalYpos = pos[1]

        # bottom
        self.botton_rect = pygame.Rect(pos, (width, height))
        self.bottom_color = "#CE0000"
        # text
        self.textsurf = buttonFont.render('Discard', True, '#FFFFFF')
        self.textrect = self.textsurf.get_rect(center=self.toprect.center)

    def draw(self):
        self.toprect.y = self.originalYpos-self.dynamic_elevation
        self.textrect.center = self.toprect.center

        self.botton_rect.midtop = self.toprect.midtop
        self.botton_rect.height = self.toprect.height+self.dynamic_elevation
        pygame.draw.rect(screen, self.bottom_color, self.botton_rect)

        pygame.draw.rect(screen, self.top_color, self.toprect)
        screen.blit(self.textsurf, self.textrect)

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.toprect.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            self.top_color = "#FC4F4F"
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elevation = 0
                self.pressed = True

            else:
                self.dynamic_elevation = self.elevation
                if self.pressed == True:
                    self.pressed = False
                    self.top_color = "#FC4F4F"
                    return True

        else:
            self.dynamic_elevation = self.elevation
            self.top_color = "#F70000"
            self.dynamic_elevation = self.elevation

        return False


class ItemBoard:
    '''Create a new Item Board Popup'''

    def __init__(self, itemName: str, img: pygame.Surface, text: str, choice: bool, showDesc=True) -> None:
        self.itemName = itemName
        self.image = img
        self.imgrect = self.image.get_rect()
        self.text = text
        self.done = False
        self.dynamictxt = self.text
        self.choice = choice
        if self.choice:
            self.buttonKeep = ButtonKeep(
                150, 40, (2*screen.get_width()/3, 320), 8)
            self.buttonDiscard = ButtonDiscard(
                150, 40, (screen.get_width()/3, 320), 8)
        self.speaker = 'Description'
        self.show = True
        global userPlayer
        self.player = userPlayer
        self.choiceMade = False
        self.resolved = False
        self.showDesc = showDesc

    def wordwrap(self, text):
        color = (255, 255, 255)
        words = text.split(" ")
        width = 510
        height = 100
        y = 485
        ybound = 590
        line_spacing = storyFont.get_sized_height() + 2
        remainderText = ''
        line_words = ""
        done = False
        for word in words:
            line_words += word + " "
            bounds = storyFont.get_rect(line_words)
            if 60 + bounds.x + bounds.width >= width:
                if words[-1] == word:
                    storyFont.render_to(screen, (60, y), None, color)
                    words = [
                        i for i in words if i not in line_words.split(' ')]
                    done = True
                    remainderText = ''
                else:
                    if y <= ybound:
                        storyFont.render_to(screen, (60, y), None, color)
                        words = [
                            i for i in words if i not in line_words.split(' ')]
                    if y >= ybound:
                        remainderText += line_words
                    y = y + line_spacing

                    line_words = ""

        if not y >= ybound and not done:
            storyFont.render_to(screen, (60, y), ' '.join(words), color)
            remainderText = ''
        else:
            remainderText = ' '.join(words)
        self.dynamictxt = remainderText

    def switchText(self):
        self.text = self.dynamictxt
        if not self.choice:
            self.show = False
            self.player.endMessage()
            self.done = True
        elif self.choice:
            if self.choiceMade:
                self.show = False
                self.player.endMessage()
                self.done = True

    def showItembox(self):
        global userInventory
        global userPlayer
        self.player = userPlayer
        self.dynamictxt = self.text
        if self.show:
            screen.blit(itemBox, (0, 0))

            itemTextRect = speakerFont.get_rect(
                self.itemName)
            itemTextRect.center = (320, 90)
            speakerFont.render_to(screen, itemTextRect,
                                  self.itemName, (0, 0, 0))

            screen.blit(self.image, (320-(self.imgrect.width/2),
                        200-self.imgrect.height/2))

            if self.showDesc:
                screen.blit(textbox, (0, 0))
                speakerNameRect = pygame.Rect(60, 450, 520, 120)
                speakerFont.render_to(screen, speakerNameRect,
                                      self.speaker, (255, 255, 255))
                full_rectangle = storyFont.get_rect(self.text)
                if full_rectangle.width > 510:
                    self.wordwrap(self.text)
                else:
                    storyFont.render_to(screen, (60, 485),
                                        self.text, (255, 255, 255))
                    self.dynamictxt = ''
            if self.player:
                self.player.startMessage()
            if self.choice and not self.choiceMade:
                self.buttonKeep.draw()
                self.buttonDiscard.draw()
                if self.buttonKeep.check_click():
                    self.choiceMade = "Keep"
                    userInventory.append({self.itemName: self.image})
                    self.switchText()
                if self.buttonDiscard.check_click():
                    self.choiceMade = "Discard"
                    self.switchText()


banner = pygame.image.load('./img/UIAssets/Banner.png')


class Choice:
    '''Create a new Choice Popup'''

    def __init__(self, choicetitle: str,  *choices: str) -> None:
        self.title = choicetitle
        self.choices = choices
        self.done = False
        self.buttons = []
        self.choices = choices
        self.numChoices = len(choices)
        for i in range(self.numChoices):
            y = 180+i*30+(i*500/(self.numChoices+1))
            x = 320
            buttonNew = Button(self.choices[i], 400, 100, (x, y), 15)
            self.buttons.append(buttonNew)
        self.show = True
        global userPlayer
        self.player = userPlayer
        self.choiceMade = False
        self.musicchanged = False

    def switchText(self):
        if self.choiceMade:
            self.show = False
            if self.player:
                self.player.endMessage()
            self.done = True

    def showChoice(self):
        if not self.musicchanged:
            pygame.mixer.music.load('./music/intense.mp3')
            pygame.mixer.music.set_volume(0.06)
            pygame.mixer.music.play(-1)
            self.musicchanged = True
        global userPlayer
        self.player = userPlayer

        if self.show:
            itemTextRect = speakerFont.get_rect(
                self.title)
            titleRect = pygame.Rect(
                60, 450, itemTextRect.width, itemTextRect.height)
            screen.blit(banner, (0, 0))

            titleRect.center = (320, 104)
            speakerFont.render_to(screen, titleRect,
                                  self.title, (0, 0, 0))
            for i in self.buttons:
                i.draw()
            if self.player:
                self.player.startMessage()
            if not self.choiceMade:
                for i in self.buttons:
                    if i.check_click():
                        self.choiceMade = i.text
                        self.switchText()


def img(fileName):
    return pygame.image.load('./img'+fileName)


retryBtn = img('/UIAssets/retryBtn.png')
menuBtn = img('/UIAssets/menuBtn.png')
failDeath = img('/UIAssets/FailDeath.png')
cowardEnding = img('/UIAssets/CowardEnding.png')
braveEnding = img('/UIAssets/BraveEnding.png')
goodEnding = img('/UIAssets/GoodEnding.png')

LdanceSet = [img('/editedLs/'+str(i)+'.png') for i in range(14)]
waltSet = [img('/walt/'+str(i)+'.jpg') for i in range(56)]

currentEnding = None


class Ending:
    def __init__(self, endingType) -> None:
        self.endingType = endingType
        if endingType == 'Fail':
            self.image = failDeath
            self.Lcount = 0
        if endingType == 'Coward':
            self.image = cowardEnding
            self.waltCount = 0
        if endingType == 'Brave':
            self.image = braveEnding
        if endingType == 'Good':
            self.image = goodEnding
        self.pressed = False
        self.retry = False
        self.menu = False
        self.musicchanged = False

    def showEnding(self):
        if not self.musicchanged:
            pygame.mixer.music.load('./music/katamari.ogg')
            pygame.mixer.music.set_volume(0.12)
            pygame.mixer.music.play(-1)
            self.musicchanged = True
        global userPlayer
        self.player = userPlayer
        userPlayer.startMessage()
        if self.endingType == 'Fail':
            if self.Lcount > 39:
                self.Lcount = 0
            screen.blit(LdanceSet[self.Lcount//3], (125, 70))
            self.Lcount += 1
        if self.endingType == 'Coward':
            if self.waltCount > 165:
                self.waltCount = 0
            screen.blit(waltSet[self.waltCount//3], (71, 137.5))
            self.waltCount += 1
        screen.blit(self.image, (0, 0))
        retryBtnRect = retryBtn.get_rect()
        retryBtnRect.x = 50
        retryBtnRect.y = 527
        screen.blit(retryBtn, retryBtnRect)
        screen.blit(menuBtn, (490, 527))
        mouse_pos = pygame.mouse.get_pos()
        global currentEnding
        if retryBtn.get_rect().collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
                self.retry = True

        # if menuBtn.get_rect().collidepoint(mouse_pos):
        #     pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        #     if pygame.mouse.get_pressed()[0]:
        #         self.pressed = True
        #         self.menu = True

        return False


class TextboxMessage:
    '''Create a new Text Box Message'''

    def __init__(self, speaker, text):
        self.text = text
        self.dynamictxt = text
        self.speaker = speaker
        self.show = True
        self.keyPressed = False
        self.done = False
        self.interaction = False

    def wordwrap(self, text):
        color = (255, 255, 255)
        words = text.split(" ")
        width = 510
        height = 100
        y = 485
        ybound = 590
        line_spacing = storyFont.get_sized_height() + 2
        remainderText = ''
        line_words = ""
        done = False
        for word in words:
            line_words += word + " "
            bounds = storyFont.get_rect(line_words)
            if 60 + bounds.x + bounds.width >= width:
                if words[-1] == word:
                    storyFont.render_to(screen, (60, y), None, color)
                    words = [
                        i for i in words if i not in line_words.split(' ')]
                    done = True
                    remainderText = ''
                else:
                    if y <= ybound:
                        storyFont.render_to(screen, (60, y), None, color)
                        words = [
                            i for i in words if i not in line_words.split(' ')]
                    if y >= ybound:
                        remainderText += line_words
                    y = y + line_spacing

                    line_words = ""

        if not y >= ybound and not done:
            storyFont.render_to(screen, (60, y), ' '.join(words), color)
            remainderText = ''
        else:
            remainderText = ' '.join(words)
        self.dynamictxt = remainderText

    def switchText(self):
        self.text = self.dynamictxt
        if self.text == '':
            self.show = False
            self.player.endMessage()

            self.done = True

    def showTextbox(self):
        global userPlayer
        self.player = userPlayer
        self.dynamictxt = self.text
        if self.show:
            speakerNameRect = pygame.Rect(60, 450, 520, 120)

            screen.blit(textbox, (0, 0))
            speakerFont.render_to(screen, speakerNameRect,
                                  self.speaker, (255, 255, 255))
            full_rectangle = storyFont.get_rect(self.text)
            if full_rectangle.width > 510:
                self.wordwrap(self.text)
            else:
                storyFont.render_to(screen, (60, 485),
                                    self.text, (255, 255, 255))
                self.dynamictxt = ''

            self.player.startMessage()


class TipsboxMessage:
    '''Create a new Tips Box Message'''

    def __init__(self, text):
        self.text = text
        self.dynamictxt = text
        self.show = True
        self.done = False
        self.interaction = False

    def wordwrap(self, text):
        color = BLUEBLACK
        words = text.split(" ")
        width = 240
        height = 50
        y = 51
        ybound = 110
        line_spacing = tipsFont.get_sized_height() + 2
        remainderText = ''
        line_words = ""
        done = False
        for word in words:
            line_words += word + " "
            bounds = tipsFont.get_rect(line_words)
            if 55 + bounds.x + bounds.width >= width:
                if words[-1] == word:
                    tipsFont.render_to(screen, (350, y), None, color)
                    words = [
                        i for i in words if i not in line_words.split(' ')]
                    done = True
                    remainderText = ''
                else:
                    if y <= ybound:
                        tipsFont.render_to(screen, (350, y), None, color)
                        words = [
                            i for i in words if i not in line_words.split(' ')]
                    if y >= ybound:
                        remainderText += line_words
                    y = y + line_spacing

                    line_words = ""

        if not y >= ybound and not done:
            tipsFont.render_to(screen, (350, y), ' '.join(words), color)
            remainderText = ''
        else:
            remainderText = ' '.join(words)
        self.dynamictxt = remainderText

    def switchText(self):
        self.text = self.dynamictxt
        if self.text == '':
            self.show = False
            self.player.endMessage()
            self.done = True

    def showTextbox(self):
        global userPlayer
        self.player = userPlayer
        self.dynamictxt = self.text
        if self.show:
            screen.blit(tipsbox, (0, 0))
            speakerNameRect = pygame.Rect(350, 37, 520, 120)

            tipsFont.render_to(screen, speakerNameRect,
                               "Tip!", (0, 0, 0))
            full_rectangle = tipsFont.get_rect(self.text)
            if full_rectangle.width > 220:
                self.wordwrap(self.text)
            else:
                tipsFont.render_to(screen, (350, 51),
                                   self.text, BLUEBLACK)
                self.dynamictxt = ''
            self.player.startMessage()


# events
CHANGEROOM = pygame.USEREVENT + 1
TEXTDISPLAY = pygame.USEREVENT + 2
CHOICE = pygame.USEREVENT + 3

change_room = pygame.event.Event(CHANGEROOM)
nextText = pygame.event.Event(TEXTDISPLAY)

choicepoint = pygame.event.Event(CHOICE)

username = ''


faded = False
prevFade = 0
prevShow = 0

searchImgPosX = (WIDTH/2)-(magRect.width/2)
searchImgPosY = -120

enterGame = False
nameEntered = False


running = True


# mouse stuff


currentRoom = ''
currentBoundary = ''
currentMask = ''
currentNext = ''

#textboxes and tips
tips0 = TipsboxMessage(
    "Press ENTER to proceed with the story. You can use the arrow keys to move when a message is not being shown. Have fun!")
textbox1 = TextboxMessage("Dad", "Rise and Shine, ")
textbox2 = TextboxMessage(
    "You", "*thinking* (Doesn't mom usually wake me up?)")
tipsbox1 = TipsboxMessage("Hi wassup")
tipsbox2 = TipsboxMessage(
    "I'm your tips guy. I’ll be laughing at you throughout this game. What’re you waiting for, get moving to the Kitchen.")


tipsBoxTalk = TipsboxMessage(
    "See that question mark next to your sister? It means she has something to say. Walk over to her and talk.")

textbox3 = TextboxMessage(
    "You", "What a surprise to see you cooking, sis. Usually mom cooks this early.")
textbox4 = TextboxMessage(
    "Sister", "I always cook breakfast.")
textbox5 = TextboxMessage(
    "You", "(She could've left out the sarcasm)")
tipsbox3 = TipsboxMessage("Go to the garden. Maybe that's where mom is.")

thinkInGarden1 = TextboxMessage(
    'You', '(Usually mom is in the garden. It feels empty without her.)')

textbox6 = TextboxMessage(
    'You', 'Dad, where is mom? Usually she\'s here in the mornings.')

textbox7 = TextboxMessage('Dad', 'Mom? What mom?')

textbox8 = TextboxMessage(
    'You', 'You know the one that gave birth to me? Woke me up yesterday? Cooked dinner last night? Married YOU?')

textbox9 = TextboxMessage(
    'Dad', 'I don’t know what you’re talking about. Maybe you’re hungry, let’s go have breakfast.')

tipsboxExpected = TipsboxMessage(
    'Totally expected! How can you expect a man to remember his wife?')

thinkInGarden = TextboxMessage('You', '(He’s acting suspicious.)')
# Dad leaves

# tipsboxFollowHim = TipsboxMessage('Follow him to the Dining Room')

tipsbox4 = TipsboxMessage(
    'There is absolutely nothing strange going on. Time to eat breakfast. Go to the dining room.')

# go to dining room

# 17

# 18
textbox10 = TextboxMessage(
    'You (to Sister)', 'You cooked, why aren’t you eating?')

textboxsisnothyngry = TextboxMessage('Sister', 'I\'m not hungry.')

textbox11 = TextboxMessage('You', '(Is that blonde hair on my bacon?)')

tipsbox5 = TipsboxMessage(
    'Are you actually gonna eat that??? You know, only your mother has blonde hair. Let’s just let that sink in.')

# Take the hair? Yes or no

textbox12 = TextboxMessage(
    'You (to Dad)', 'Where did this blonde hair come from? Isn\'t this mom’s hair?')
# Dad takes the plate nonchalantly

textbox13 = TextboxMessage('Dad', 'Some pigs are blonde.')

textbox14 = TextboxMessage('You', 'Where\'s mom?')

# sister gets up and leaves without a word

thinkinDiningroom = TextboxMessage(
    'You', '(That\'s strange. She\'s hiding something)')

atipsbox5 = TipsboxMessage('Follow her! Go to the garden.')
# 25


# When the MC follows the sister, she is sitting and staring at the garden, crying. There is a mound in the center of the garden with a flowerpot on top of it.
# Click the flowerpot
# MC goes to interact with flowerpot and notices a glimmer. Finds a wedding ring. Prompted to take or leave ring
thinkInGarden2 = TextboxMessage('You',
                                '(Why is this ring here? This day is becoming weirder!)')
# textbox15 = TextboxMessage('You','(What’s going on? why are you crying?)')
# textbox16 = TextboxMessage('Sister','(I’ll never forgive him for what he did”)')

# thinkInGarden= TextboxMessage('(Who is he? And What did he do?)')

# tipsbox6= TipsboxMessage('(Go to your parents’ room. Maybe it’s about time you do some investigating.)')
# #MC enters the house and goes to parents’ room
# #Finds picture of blonde guy on the pillow, with Johnathan (Jojo) <3 and a number on the back (Take the image yes or no)

# thinkinBedroom= TextboxMessage('(Who's he?))

# tipsbox7= TipsboxMessage('(Whose is this? Your mom's? Or your dad's? I don't Judge)'
# #Sees torn image

# tipsbox= TipsboxMessage('(The torn pieces of the photo left a trail. Follow it.)'

seeDirt = TextboxMessage('You', '(A dirt mound. This wasn\'t here yesterday.)')
seeTip = TipsboxMessage(
    'Strangely human body shaped. Could also fit two reasonably sized pigs.')

textboxwhycry = TextboxMessage(
    "You", "What's going on? Why are you crying?"
)
textboxsister = TextboxMessage(
    "Sister", "I'll never forgive him for what he did!"
)
textboxsister1 = TextboxMessage(
    'You', '(Who is he? What is she talking about?)')


tipsboxsister2 = TipsboxMessage(
    'Go to your parent\'s room. Maybe it\'s about time you do some investigating.')

# MC enters the house and goes to parent/'s room
# Finds picture of blonde guy on the pillow,
# with Johnathan (Jojo) <3 and a number on the back (Take the image yes or no)
textboxsister3 = TextboxMessage(
    'You', '(Who\'s he?)')

textboxsister4 = TipsboxMessage(
    'Whose is this? Your Mom\'s? Or your Dad\'s? I don\'t judge.'

)
# Sees torn image
textboxsister5 = TipsboxMessage(
    'The torn pieces of the photo left a trail. Follow it.'
)
# Torn pieces lead to a box with a human heart (Take the box? Yes or no)
textboxsister6 = TipsboxMessage(
    "WHAT? WHAT IS THAT? WHAT? IS THERE A SERIAL KILLER IN THIS HOUSE? Listen to me. Run."
)
tipsRUN = TipsboxMessage(" Right now.")
# Music switch until the end. More intense.
# Choice: Call the police? Confront your dad? Keep it a secret?
# Keep it a secret: Coward ending (you live with a killer maybe, you don\'t deserve to know the truth, you lost tbh)
# Call the police:

textboxsister7 = TipsboxMessage(
    'Bad move dude. Serial killers only get caught after 30 victims. You\'re next.')
# The dad catches MC
textboxsister8 = TextboxMessage(
    "Dad", "You\'ve seen too much."
)
textboxsister9 = TextboxMessage(
    "You", "I know what you did."
)
textboxsister10 = TipsboxMessage(
    "Why did you say that. Do you want to die?"

)
# Choice- What do you think happened to mom: Dad killed her?
#  Dad killed mom\'s lover?
# If you choose dad killed her,the dad kills you, you\'re tomorrow\'s breakfast
# If you choose dad killed mom\'s lover, you chose correctly, you win!!
# The good ending. Your dad appreciates your detective skills and you live together with a serial killer, happily ever after.
# Confront your dad

atextboxsister11 = TipsboxMessage(
    "Go find your dad in the dining room. Time to teach him a lesson! Or not. You could\'ve always just ran. Are you stupid?"
)
# Present the items you picked up in your inventory one by one


checkpointfood = TextboxMessage(
    "You", " There was blonde hair in our food this morning. You know mom has blonde hair, so tell me where she is. Unless we were eating her."
)
dadsilence = TextboxMessage("Dad", "*Conspicuous Silence*")
# Dad: conspicuous slience
weddingringtext = TextboxMessage(
    'You', 'Here\'s mom\'s wedding ring. I know you recognize this. It was in the garden next to a strange mound of dirt.'

)

# Torn picture
weddingpicturetext = TextboxMessage(
    "You", "This was your wedding picture... torn... shredded to pieces."
)
# Dad visible irritation
dadirritation = TextboxMessage("Dad", "*Visible Irritation*")
# Picture of Johnathan (Jojo)
jojopictext = TextboxMessage(
    "You", "I\'m not sure who this guy is, but maybe it\'s important. "
)
putthat = TextboxMessage(
    "Dad", "Put that away! You don\'t know what you\'re talking about!"
)

# Human heart in a box
thisisaheart = TextboxMessage(
    "You", "And this...a human heart? Whose even...Who are you? This is gruesome..."
)
# Choice- What do you think happened to Mom: Dad killed her? Dad killed Mom's lover?
# If you choose dad killed her, the dad kills you, you\'re tomorrow\'s breakfast
youkilledmom = TextboxMessage(
    "You", "You killed Mom, didn't you?"
)
# Dad walks to MC in silence

# If you choose dad killed mom\'s lover, you chose correctly, you win!
yuoukilledjojo = TextboxMessage(
    "You", "You killed Mom's lover, this Johnathan (Jojo) guy. Didn't you?"
)

textboxsister19 = TextboxMessage(
    "Dad", "Wait, you actually got that?"
)

textboxsister20 = TextboxMessage(
    "You", "Am I right?"
)

textboxsister21 = TextboxMessage(
    "Dad", "Yes, I\'m just surprised. You shouldn\'t have eaten the \'bacon\' this morning though..."
)

textboxsister22 = TextboxMessage(
    "You", "Why not?"
)

textboxsister23 = TextboxMessage(
    "Dad", "Mmm...Well, that was actually Johnathan (Jojo)'s leg..."
)
textboxsister24 = TextboxMessage(
    "You", "AAAAAAAAAAAAA!!!!!!"
)
textboxsister25 = TipsboxMessage(
    "AHHHHHHHHHHHH!"
)
# GAME ENDS
# Achievement: Confident (You brave soul)

allText = [tips0, textbox1, textbox2, tipsbox1,
           tipsbox2, tipsBoxTalk, textbox3, textbox4, textbox5,
           tipsbox3, thinkInGarden1, textbox6, textbox7, textbox8,
           textbox9, tipsboxExpected, thinkInGarden, tipsbox4,
           textbox10, textboxsisnothyngry, textbox11, tipsbox5, textbox12,
           textbox13, textbox14, thinkinDiningroom, atipsbox5, textboxwhycry,
           textboxsister, textboxsister1, tipsboxsister2,
           textboxsister7, textboxsister8, textboxsister9, textboxsister10,
           atextboxsister11, checkpointfood,
           dadsilence, weddingringtext, weddingpicturetext, dadirritation,
           jojopictext, putthat, thisisaheart,
           youkilledmom, yuoukilledjojo, textboxsister19,
           textboxsister20, textboxsister21, textboxsister22, textboxsister23, textboxsister24,
           textboxsister25]
currentTextIndex = 0
currentText = allText[currentTextIndex]
userPlayer = None


def reinitializeAllText():
    global allText
    allText = [tips0, textbox1, textbox2, tipsbox1,
               tipsbox2, tipsBoxTalk, textbox3, textbox4, textbox5,
               tipsbox3, thinkInGarden1, textbox6, textbox7, textbox8,
               textbox9, tipsboxExpected, thinkInGarden, tipsbox4,
               textbox10, textboxsisnothyngry, textbox11, tipsbox5, textbox12,
               textbox13, textbox14, thinkinDiningroom, atipsbox5, textboxwhycry,
               textboxsister, textboxsister1, tipsboxsister2,
               textboxsister7, textboxsister8, textboxsister9, textboxsister10,
               atextboxsister11, checkpointfood,
               dadsilence, weddingringtext, weddingpicturetext, dadirritation,
               jojopictext, putthat, thisisaheart,
               youkilledmom, yuoukilledjojo, textboxsister19,
               textboxsister20, textboxsister21, textboxsister22, textboxsister23, textboxsister24,
               textboxsister25]


returnTo = None

currentBlock = 1
storyBlocks = {
    0: True, 1: False, 2: False, 3: False, 4: False, 5: False, 6: False, 7: False, 8: False, 9: False, 10: False, 11: False
}

calledText = False

renderSister = False
renderFather = False

floattimer = 0
setTimer = False

# item boxes
RingLarge = pygame.image.load('./img/objectAssets/RingLarge.png')
ringItembox = ItemBoard("Wedding Ring", RingLarge,
                        'This is a ring. You recognize it as your mother\'s wedding ring. Now what would it be doing next to a human sized pile of dirt?', True)
ringItembox2 = ItemBoard("Wedding Ring", RingLarge,
                         'This is a ring. You recognize it as your mother\'s wedding ring. Now what would it be doing next to a human sized pile of dirt?', False)

HeartInBox = pygame.image.load('./img/objectAssets/heartInBox.png')
heartItemBox = ItemBoard("Human Heart In a Box (???)",
                         HeartInBox, 'Ok what? What... even... Whose... Are you gonna keep that???', True)
heartItemBox2 = ItemBoard("Human Heart In a Box (???)",
                          HeartInBox, 'Ok what? What... even... Whose... Are you gonna keep that???', False)

DirtMoundLg = pygame.image.load(
    './img/objectAssets/DirtMoundLarge.png')
dirtItemBox = ItemBoard("Dirt Mound", DirtMoundLg,
                        "Strangely human shaped. A surprise clue that will help us later.", False)
dirtItemBox2 = ItemBoard("Dirt Mound", DirtMoundLg,
                         "Strangely human shaped. A surprise clue that will help us later.", False)

PhotoLarge = pygame.image.load('./img/objectAssets/PhotoLarge.png')
PhotoLarge = pygame.transform.smoothscale(
    PhotoLarge, (148, 180))
PhotoBox = ItemBoard("Photo of Johnathan", PhotoLarge,
                     "One of your parents had this for some reason. ZA WARUDO!!!", True)
PhotoBox2 = ItemBoard("Photo of Johnathan", PhotoLarge,
                      "One of your parents had this for some reason. ZA WARUDO!!!", False)

MarPicLarge = pygame.image.load(
    './img/objectAssets/marPicLarge.png')
MarBox = ItemBoard("Torn Marriage Photo", MarPicLarge,
                   "A torn wedding picture of your dad and... mom. So she does exist, and you're not crazy.", True)
MarBox2 = ItemBoard("Torn Marriage Photo", MarPicLarge,
                    "A torn wedding picture of your dad and... mom. So she does exist, and you're not crazy.", False)

food = pygame.image.load(
    './img/objectAssets/food.png')
foodBox = ItemBoard("Food (Hair Included)", food,
                    "A tasty breakfast. Your bacon has blonde hair on it. Still bussin tho.", True)
foodBox2 = ItemBoard("Food (Hair Included)", food,
                     "A tasty breakfast. Your bacon has blonde hair on it. Still bussin tho.", False)

currentItemBox = None

yourepsycho = TipsboxMessage("You are a psycopath")
whattheheck = TipsboxMessage(
    "Um what? Why would you keep that? Are you in your right mind?")


# Choices
WhatDo = Choice("What do you do?", "Confront Your Dad",
                "Call the Police", "Remain Silent")

SayWhat = Choice("Where's mom?", "Dad Killed Her",
                 "Mom is alive but Dad killed Jojo", "Pigs can be Blonde")
SayWhatFinal = Choice("Where's mom?", "Dad Killed Her",
                      "Mom is alive but Dad killed Jojo")


# Ending
death = Ending('Fail')
coward = Ending('Coward')
brave = Ending('Brave')
good = Ending('Good')

choicebased = False

currentEnding = None

currentChoice = None

# music
pygame.mixer.music.load('./music/reprise.ogg')
pygame.mixer.music.set_volume(0.06)
pygame.mixer.music.play(-1)


def storyCompleted(num) -> bool:
    global storyBlocks
    dones = []
    for i in range(0, num+1):
        dones.append(storyBlocks[i])
    return all(dones)


while running:
    tickCount += 1
    clock.tick(FPS)

    if enterGame == False:
        if 30 < tickCount < 300:
            screen.blit(creatorIcon, (0, 0))
        elif 300 < tickCount < 420:
            screen.fill(LIGHTCREAM)
        elif 420 < tickCount < 640:
            screen.fill(LIGHTCREAM)
            GTITLEDISP.show_message(GAMETITLE, 0.0167)
            GTITLEDISP.render_message(screen)

        if 460 < tickCount:
            SUBTITLEDISP.show_message(SUBTITLE, 0.0167)
            SUBTITLEDISP.render_message(screen)

        if 500 < tickCount:
            screen.blit(magLgIcon, (searchImgPosX, searchImgPosY))
            if searchImgPosY < 30:
                searchImgPosY += 5
        if 500 < tickCount:

            if time.time() % 1 > 0.5:
                STARTDISP.font_color = BLUEBLACK
            else:
                STARTDISP.font_color = LIGHTCREAM
                faded = True
            STARTDISP.show_message(STARTTEXT, 0.0167)
            STARTDISP.render_message(screen)

    else:
        if nameEntered == False:
            screen.fill(LIGHTCREAM)
            STARTDISP.msg_height = 0.4

            STARTDISP.show_message(
                "Click below to enter your character name.", 3)
            STARTDISP.render_message(screen)
            if box_active:
                color = color_active
                if hover_active:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)
            elif hover_active:
                color = hover_colour
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)
            else:

                color = color_passive

            if user_text != '':
                button1.draw()
                nameEntered = button1.check_click()
                if nameEntered:
                    username = user_text
                    userPlayer = Player(username)
                    playerSpriteGrp.add(userPlayer)
                    currentRoom = "Bedroom"

            pygame.draw.rect(screen, color, input_rect)

            text_surface = base_font.render(
                user_text, True, (255, 255, 255))

            # render at position stated in arguments
            screen.blit(text_surface, (input_rect.x+5, input_rect.y+5))
            input_rect.w = max(400, text_surface.get_width()+10)
            # set width of textfield so that text cannot get
            # outside of user's text input

            mousepos = pygame.mouse.get_pos()
            if input_rect.collidepoint(mousepos):

                hover_active = True
            else:

                hover_active = False
        else:
            screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if enterGame == False:
                    enterGame = True
                    tickCount = 500
                if currentText != None:
                    currentText.switchText()

                if currentItemBox != None:
                    currentItemBox.switchText()
            elif event.key == pygame.K_BACKSPACE:

                user_text = user_text[:-1]

            else:
                user_text += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)
            if input_rect.collidepoint(event.pos):
                box_active = True
            else:
                box_active = False
        if event.type == CHANGEROOM:

            userPlayer.position(currentNext.originx,
                                currentNext.originy)
        if event.type == TEXTDISPLAY:
            if not storyCompleted(currentBlock):
                currentTextIndex += 1
            if currentTextIndex+1 > len(allText):
                currentText = None
            else:
                if currentText:
                    if not currentText.interaction:
                        if not choicebased:
                            currentText = allText[currentTextIndex]
                        else:
                            while not allText[currentTextIndex]:
                                currentTextIndex += 1
                                currentText = allText[currentTextIndex]
                else:
                    currentText = allText[currentTextIndex]
            if currentText == tipsbox1 and tipsbox1 != None:
                tipsbox1.text += ' '+username+'!'
            if currentText == textbox1 and textbox1 != None:
                textbox1.text += ' '+username+'!'
    if nameEntered:
        if currentRoom == "Bedroom":
            redrawWindow(bedroomBG, bedroomMask, bedroomNextImg)
            currentBoundary = bedroomSprite
            currentMask = bedroomMask
            currentNext = bedroomNext
            scale_player(60, 100)
            if pygame.sprite.collide_mask(userPlayer, bedroomNext):
                currentRoom = "Hallway"
                pygame.event.post(change_room)
                currentBoundary = hallwaySprite
                currentNext = bedroomNext
        elif currentRoom == "Hallway":
            redrawWindow(hallwayBG, hallwayMask,
                         HallwayBedroomNextImg, HallwayKitchenNextImg, HallwayParentNextImg)
            currentBoundary = hallwaySprite
            currentMask = hallwayMask
            scale_player(30, 50)
            if pygame.sprite.collide_mask(userPlayer, hallwayBedroomNext):
                currentRoom = "Bedroom"
                currentBoundary = bedroomSprite
                pygame.event.post(change_room)
                currentNext = hallwayBedroomNext
            if pygame.sprite.collide_mask(userPlayer, HallwayKitchenNext):
                currentRoom = "Kitchen"
                pygame.event.post(change_room)
                currentBoundary = kitchenSprite
                currentNext = HallwayKitchenNext
            if pygame.sprite.collide_mask(userPlayer, HallwayParentNext):
                currentRoom = "Parent Room"
                pygame.event.post(change_room)
                currentBoundary = parentRmSprite
                currentNext = HallwayParentNext
        elif currentRoom == "Kitchen":
            redrawWindow(kitchenBG, kitchenMask,
                         KitchenDiningNextImg, KitchenHallwayNextImg)
            currentBoundary = kitchenSprite
            currentMask = kitchenMask
            scale_player(60, 100)
            if pygame.sprite.collide_mask(userPlayer, KitchenHallwayNext):
                currentRoom = "Hallway"
                pygame.event.post(change_room)
                currentBoundary = hallwaySprite
                currentNext = KitchenHallwayNext
            if pygame.sprite.collide_mask(userPlayer, KitchemDiningNext):
                currentRoom = "Dining Room"
                pygame.event.post(change_room)
                currentNext = KitchemDiningNext
                # currentBoundary = hallwaySprite
        elif currentRoom == "Parent Room":
            redrawWindow(parentBG, parentMask, ParentRoomNextImg)
            currentBoundary = parentRmSprite
            currentMask = parentMask
            scale_player(60, 100)
            jojoSprite.position(320, 280)
            boxSmallSprite.position(110, 230)
            marPic1Sprite.position(125, 275)
            marPic2Sprite.position(170, 315)
            parentRoomObjects.update()
            parentRoomObjects.draw(screen)

            if pygame.sprite.collide_mask(userPlayer, ParentRoomNext):
                currentRoom = "Hallway"
                pygame.event.post(change_room)
                currentBoundary = hallwaySprite
                currentNext = ParentRoomNext
            if pygame.sprite.collide_mask(userPlayer, jojoSprite) and textboxsister3:
                currentText = textboxsister3
                currentText.interaction = True
                calledText = False
            if textboxsister3:
                if textboxsister3.done:
                    currentText = textboxsister4
                    currentText.interaction = True
                    textboxsister3 = None
            if textboxsister4:
                if textboxsister4.done:
                    currentItemBox = PhotoBox
                    textboxsister4 = None
                    currentText = None
            if PhotoBox:
                if PhotoBox.done:
                    currentItemBox = None
                    if PhotoBox.choiceMade == 'Keep':
                        parentRoomObjects.remove(jojoSprite)
                    PhotoBox = None

            if pygame.sprite.collide_mask(userPlayer, marPic2Sprite) and textboxsister5:
                currentText = textboxsister5
                currentText.interaction = True
                calledText = False
            if pygame.sprite.collide_mask(userPlayer, marPic2Sprite):
                parentRoomObjects.remove(marPic2Sprite)
            if pygame.sprite.collide_mask(userPlayer, marPic1Sprite):
                parentRoomObjects.remove(marPic1Sprite)
                currentItemBox = MarBox

            if textboxsister5:
                if textboxsister5.done:
                    currentText.interaction = True
                    textboxsister5 = None
                    currentText = None
            if pygame.sprite.collide_mask(userPlayer, boxSmallSprite) and textboxsister6:

                currentItemBox = heartItemBox

            if heartItemBox:
                if heartItemBox.done and not heartItemBox.resolved:
                    if heartItemBox.choiceMade == "Keep":
                        parentRoomObjects.remove(boxSmallSprite)
                    heartItemBox.done = False
                    currentText = yourepsycho
                    currentText.interaction = True
            if yourepsycho:
                if yourepsycho.done:
                    currentText = None
                    yourepsycho = None

        elif currentRoom == "Dining Room":
            screen.blit(diningTable, (0, 0))
            redrawWindow(diningBG, diningMask,
                         diningGardenNextImg, diningKitchenNextImg)
            currentBoundary = diningSprite
            currentMask = diningMask
            scale_player(60, 100)
            if pygame.sprite.collide_mask(userPlayer, diningKitchenNext):
                currentRoom = "Kitchen"
                pygame.event.post(change_room)
                currentBoundary = kitchenSprite
                currentNext = diningKitchenNext
            if pygame.sprite.collide_mask(userPlayer, diningGardenNext):
                currentRoom = "Garden"
                pygame.event.post(change_room)
                currentBoundary = kitchenSprite
                currentNext = diningGardenNext
        elif currentRoom == "Garden":
            redrawWindow(gardenBG, gardenMask,
                         gardenNextImg)

            dirtMoundSprite.position(320, 320)
            ringSprite.position(380, 350)
            currentBoundary = gardenSprite
            currentMask = gardenMask
            gardenObjects.update()
            gardenObjects.draw(screen)
            scale_player(30, 50)
            if pygame.sprite.collide_mask(userPlayer, gardenNext):
                currentRoom = "Dining Room"
                pygame.event.post(change_room)
                currentBoundary = diningSprite
                currentNext = gardenNext
            if pygame.sprite.collide_mask(userPlayer, ringSprite) and thinkInGarden2:
                currentText = thinkInGarden2
                currentText.interaction = True
                calledText = False
            if thinkInGarden2:
                if thinkInGarden2.done:
                    currentItemBox = ringItembox
                    currentText = None
                    thinkInGarden2 = None
            if pygame.sprite.collide_mask(userPlayer, dirtMoundSprite) and seeDirt:

                currentText = seeDirt
                currentText.interaction = True
                calledText = False
            if seeDirt:
                if seeDirt.done:
                    currentText = seeTip
                    currentText.interaction = True
                    seeDirt = None
            if seeTip:
                if seeTip.done:
                    seeTip = None
                    currentText.interaction = False
                    currentText = None
                    currentItemBox = dirtItemBox
            if ringItembox:
                if ringItembox.done:
                    if ringItembox.choiceMade == "Keep":
                        gardenObjects.remove(ringSprite)

        if renderSister:
            Sister.update(currentBoundary)
            sisterGroup.draw(screen)
        if renderFather:
            Dad.update(currentBoundary)
            dadGroup.draw(screen)

        playerSpriteGrp.update(currentBoundary)
        playerSpriteGrp.draw(screen)

        if currentText:
            currentText.showTextbox()
        if currentItemBox:
            currentItemBox.showItembox()
        if currentChoice:
            currentChoice.showChoice()
        if currentEnding:
            currentEnding.showEnding()
        if tips0:
            if tips0.done:
                pygame.event.post(nextText)
                tips0 = None
                renderFather = True
                Dad.position(160, 380)
                Dad.facingd("Up")
                Dad.atAttention(False)
        if textbox1:
            if textbox1.done:
                pygame.event.post(nextText)
                textbox1 = None

        if tipsbox1:
            if tipsbox1.done:
                pygame.event.post(nextText)
                tipsbox1 = None

        if textbox2:
            if textbox2.done:
                pygame.event.post(nextText)
                textbox2 = None
        if tipsbox2:
            if tipsbox2.done:
                storyBlocks[1] = True
                currentBlock += 1
                tipsbox2 = None
        else:
            if currentBlock == 2:
                if pygame.sprite.collide_mask(userPlayer, bedroomNext):
                    renderFather = False

        if not storyCompleted(currentBlock):
            if currentBlock == 2:
                if currentRoom == "Kitchen" and pygame.sprite.collide_mask(userPlayer, HallwayKitchenNext) and not calledText:
                    renderSister = True
                    Sister.position(525, 340)
                    Sister.facingd("Up")
                    floattimer = timer()+1
                    setTimer = True
                if floattimer-timer() < 0 and setTimer:
                    pygame.event.post(nextText)
                    calledText = True
                    setTimer = False
                if calledText:
                    if allText[5]:
                        if allText[5].done:
                            storyBlocks[2] = True
                            currentBlock += 1
                            allText[5] = None
                            calledText = False
            if currentBlock == 3:
                if currentRoom == "Kitchen" and not calledText and pygame.sprite.collide_mask(userPlayer, Sister):
                    pygame.event.post(nextText)
                    Sister.facingd("Down")
                    Sister.atAttention(False)
                    calledText = True
                if calledText:
                    if allText[6]:
                        if allText[6].done:
                            pygame.event.post(nextText)

                            allText[6] = None
                    if allText[7]:
                        if allText[7].done:
                            pygame.event.post(nextText)

                            allText[7] = None
                    if allText[8]:
                        if allText[8].done:
                            pygame.event.post(nextText)
                            allText[8] = None
                    if allText[9]:
                        if allText[9].done:
                            storyBlocks[3] = True
                            allText[9] = None

                            Sister.facingd("Up")

                            calledText = False
                            currentBlock += 1
            if currentBlock == 4:
                if currentRoom == "Dining Room" and not calledText:
                    renderSister = False
                if currentRoom == "Garden" and not calledText and not setTimer:
                    floattimer = timer()+0.5
                    Dad.atAttention(True)
                    Dad.scale(30, 50)
                    Dad.position(300, 280)

                    renderFather = True
                    setTimer = True
                if floattimer-timer() < 0 and setTimer:
                    pygame.event.post(nextText)
                    calledText = True
                    setTimer = False
                if calledText:
                    if allText[10]:
                        if allText[10].done:
                            storyBlocks[4] = True
                            currentBlock += 1
                            allText[10] = None
                            calledText = False
            if currentBlock == 5:
                if currentRoom == "Garden" and not calledText and pygame.sprite.collide_mask(userPlayer, Dad):
                    pygame.event.post(nextText)
                    Dad.facingd("Down")
                    Dad.atAttention(True)
                    calledText = True

                if calledText:
                    if allText[11]:
                        if allText[11].done:
                            pygame.event.post(nextText)
                            allText[11] = None
                    if allText[12]:
                        if allText[12].done:
                            pygame.event.post(nextText)
                            allText[12] = None
                    if allText[13]:
                        if allText[13].done:
                            pygame.event.post(nextText)
                            allText[13] = None
                    if allText[14]:
                        if allText[14].done:
                            pygame.event.post(nextText)
                            allText[14] = None
                    if allText[15]:
                        if allText[15].done:
                            pygame.event.post(nextText)
                            allText[15] = None
                    if allText[16]:
                        if allText[16].done:
                            pygame.event.post(nextText)
                            allText[16] = None
                    if allText[17]:
                        if allText[17].done:
                            storyBlocks[5] = True
                            currentBlock += 1
                            allText[17] = None
                            renderFather = False
                            calledText = False
            if currentBlock == 6:
                if currentRoom == "Dining Room" and not calledText:
                    renderSister = True
                    renderFather = True
                    Dad.scale(60, 100)
                    Dad.position(175, 350)
                    Dad.facingd('Right')
                    Dad.atAttention(False)
                    Sister.scale(60, 100)
                    Sister.position(445, 420)

                    Sister.facingd('Left')
                if currentRoom == "Dining Room" and not calledText and pygame.sprite.collide_mask(userPlayer, diningTableSprite):
                    pygame.event.post(nextText)

                    calledText = True
                if calledText:
                    if allText[18]:
                        if allText[18].done:
                            pygame.event.post(nextText)
                            allText[18] = None
                    if allText[19]:
                        if allText[19].done:
                            pygame.event.post(nextText)
                            allText[19] = None
                    if allText[20]:
                        if allText[20].done:
                            currentItemBox = foodBox
                            allText[20] = None
                    if foodBox:
                        if foodBox.done:
                            if foodBox.choiceMade == "Keep":
                                currentText = whattheheck
                                currentText.interaction = True
                            else:
                                pygame.event.post(nextText)
                                currentItemBox = None
                            foodBox = None
                    if whattheheck:
                        if whattheheck.done:
                            pygame.event.post(nextText)
                            whattheheck = None
                            currentText = None
                    if allText[21]:
                        if allText[21].done:
                            pygame.event.post(nextText)
                            allText[21] = None
                    if allText[22]:
                        if allText[22].done:
                            pygame.event.post(nextText)
                            allText[22] = None
                    if allText[23]:
                        if allText[23].done:
                            pygame.event.post(nextText)

                            allText[23] = None
                    if allText[24]:
                        if allText[24].done:
                            pygame.event.post(nextText)
                            renderSister = False
                            allText[24] = None
                    if allText[25]:
                        if allText[25].done:
                            pygame.event.post(nextText)
                            allText[25] = None
                    if allText[26]:
                        if allText[26].done:
                            storyBlocks[6] = True
                            currentBlock += 1
                            allText[26] = None
                            calledText = False
                            renderFather = False
            if currentBlock == 7:
                if currentRoom == "Garden":
                    if not calledText:
                        Sister.scale(30, 50)
                        Sister.position(320, 420)
                        Sister.facingd('Up')
                        renderSister = True
                        Sister.atAttention(True)
                        if pygame.sprite.collide_mask(userPlayer, Sister):
                            pygame.event.post(nextText)
                            calledText = True
                if calledText:
                    if allText[27]:
                        if allText[27].done:
                            pygame.event.post(nextText)
                            allText[27] = None
                    if allText[28]:
                        if allText[28].done:
                            pygame.event.post(nextText)
                            allText[28] = None
                    if allText[29]:
                        if allText[29].done:
                            pygame.event.post(nextText)
                            allText[29] = None
                    if allText[30]:
                        if allText[30].done:
                            storyBlocks[7] = True
                            currentBlock += 1
                            allText[30] = None
                            calledText = False
                            renderFather = False
            if currentBlock == 8:
                if currentRoom == 'Dining Room' and not calledText and not setTimer:
                    renderSister = False
                    returnTo = [8, 30]
                if heartItemBox:
                    if currentRoom == 'Parent Room' and not calledText and not setTimer and heartItemBox.choiceMade:
                        floattimer = timer()+1
                        setTimer = True
                        heartItemBox = None
                if floattimer-timer() < 0 and setTimer:
                    currentChoice = WhatDo
                    setTimer = False

                if WhatDo:
                    if WhatDo.done:
                        if WhatDo.choiceMade == "Remain Silent":
                            Dad.position(320, 550)
                            Dad.atAttention(False)
                            renderFather = True
                            currentEnding = coward
                        if WhatDo.choiceMade == "Call the Police":
                            currentBlock += 1
                        if WhatDo.choiceMade == "Confront Your Dad":
                            currentBlock += 2
                            currentTextIndex = 34
                            pygame.event.post(nextText)
                        WhatDo = None
                        storyBlocks[8] = True
                        calledText = False
            if currentBlock == 9:
                if currentRoom == 'Parent Room' and not calledText:
                    retrunTo = [9, 30]
                    calledText = True
                    pygame.event.post(nextText)
                    Dad.position(320, 550)
                    Dad.atAttention(False)
                    Dad.facingd("Up")
                    renderFather = True
                    print("here")
                if calledText:
                    if allText[31]:
                        if allText[31].done:
                            pygame.event.post(nextText)
                            allText[31] = None
                    if allText[32]:
                        if allText[32].done:
                            pygame.event.post(nextText)
                            allText[32] = None
                    if allText[33]:
                        if allText[33].done:
                            pygame.event.post(nextText)
                            allText[33] = None
                    if allText[34]:
                        if allText[34].done:
                            allText[34] = None
                            pygame.event.post(nextText)
                            currentChoice = SayWhat
                    if SayWhat:
                        if SayWhat.done:
                            if SayWhat.choiceMade == "Dad Killed Her" or SayWhat.choiceMade == "Pigs can be Blonde":
                                currentEnding = death

                                calledText = False
                            if SayWhat.choiceMade == "Mom is alive but Dad killed Jojo":
                                currentEnding = good

                                calledText = False
                            storyBlocks[9] = True
            if currentBlock == 10:
                if currentRoom != "Dining Room" and not calledText:
                    if allText[35]:
                        if allText[35].done:
                            allText[35] = None

                if currentRoom == 'Dining Room' and not calledText:
                    returnTo = [10, 34]
                    Dad.position(320, 580)
                    Dad.atAttention(False)
                    Dad.facingd("Up")
                    renderFather = True
                    invItems = []
                    for i in userInventory:
                        invItems.extend(i.keys())
                    print(invItems)
                    if "Food (Hair Included)" not in invItems:
                        allText[36] = None
                        allText[37] = None
                    if "Wedding Ring" not in invItems:
                        allText[38] = None
                    if "Torn Marriage Photo" not in invItems:
                        allText[39] = None
                        allText[40] = None
                    if "Photo of Johnathan" not in invItems:
                        allText[41] = None
                        allText[42] = None
                    if "Human Heart In a Box (???)" not in invItems:
                        allText[43] = None
                    # choicebased = True
                    calledText = True
                    foodBox2.showDesc = False
                    currentItemBox = foodBox2
                    pygame.event.post(nextText)

                if calledText:
                    if allText[36]:
                        if allText[36].done:
                            pygame.event.post(nextText)
                            allText[36] = None
                    if allText[37]:
                        if allText[37].done:
                            pygame.event.post(nextText)
                            allText[37] = None
                            ringItembox2.showDesc = False
                            currentItemBox = ringItembox2
                    if allText[38]:
                        if allText[38].done:
                            pygame.event.post(nextText)
                            allText[38] = None
                            MarBox2.showDesc = False
                            currentItemBox = MarBox2
                    if allText[39]:
                        if allText[39].done:
                            allText[39] = None
                            pygame.event.post(nextText)
                    if allText[40]:
                        if allText[40].done:
                            allText[40] = None
                            pygame.event.post(nextText)
                            PhotoBox2.showDesc = False
                            currentItemBox = PhotoBox2
                    if allText[41]:
                        if allText[41].done:
                            allText[41] = None
                            pygame.event.post(nextText)
                    if allText[42]:
                        if allText[42].done:
                            allText[42] = None
                            pygame.event.post(nextText)
                            heartItemBox2.showDesc = False
                            currentItemBox = heartItemBox2
                    if allText[43]:
                        if allText[43].done:
                            allText[43] = None
                            currentChoice = SayWhatFinal
                    if SayWhatFinal:
                        if SayWhatFinal.done:
                            if SayWhatFinal.choiceMade == "Dad Killed Her" or SayWhatFinal.choiceMade == "Pigs can be Blonde":
                                currentEnding = death
                                SayWhatFinal.done = False
                                calledText = False
                                Dad.position(userPlayer.rect.x+30,
                                             userPlayer.rect.y+120)
                            if SayWhatFinal.choiceMade == "Mom is alive but Dad killed Jojo":

                                currentTextIndex += 1
                                SayWhatFinal = None
                                calledText = False
                                pygame.event.post(nextText)
                                storyBlocks[10] = True
                    if allText[44]:
                        if allText[44].done:

                            allText[43] = None

                    if allText[45]:
                        if allText[45].done:
                            Dad.position(userPlayer.rect.x,
                                         userPlayer.rect.y+80)
                            allText[45] = None
                            pygame.event.post(nextText)
                    if allText[46]:
                        if allText[46].done:
                            allText[46] = None
                            pygame.event.post(nextText)
                    if allText[47]:
                        if allText[47].done:
                            allText[47] = None
                            pygame.event.post(nextText)
                    if allText[48]:
                        if allText[48].done:
                            allText[48] = None
                            pygame.event.post(nextText)
                    if allText[49]:
                        if allText[49].done:
                            allText[49] = None
                            pygame.event.post(nextText)
                    if allText[50]:
                        if allText[50].done:
                            allText[50] = None
                            pygame.event.post(nextText)
                    if allText[51]:
                        if allText[51].done:
                            allText[51] = None
                            pygame.event.post(nextText)
                    if allText[52]:
                        if allText[52].done:
                            allText[52] = None

                            currentEnding = brave

        if death:
            if death.pressed:
                if death.menu:
                    tickCount = 0
                    currentBlock = None
                    nameEntered = False
                    enterGame = False
                    currentEnding = None
                    death.pressed = False
        if currentEnding:
            if currentEnding:
                if currentEnding.retry:
                    reinitializeAllText()
                    currentBlock = returnTo[0]
                    currentTextIndex = returnTo[1]
                    for i in range(12):
                        storyBlocks[i]: False
                    currentEnding=None
    pygame.display.update()
