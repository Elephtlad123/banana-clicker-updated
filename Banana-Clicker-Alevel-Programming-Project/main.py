import pygame
import random
import time
import UnpackData

from AridropSettings import GetRandomBonus, AirdropData
from sys import exit

pygame.init()

WIDTH = 480
HEIGHT = 800

WIN = pygame.display.set_mode((WIDTH, HEIGHT), vsync=True)
pygame.display.set_caption("Top Banana!")

AirDropEventSpawnRate = 0 #roughly how long it takes for the airdrop to spawn there is a Â±20% bias to this
CurrentAirDropDelay = random.randint(AirDropEventSpawnRate * 8, AirDropEventSpawnRate * 12) / 10
LastAirDropEvent = time.time()

BackgroundColour = (138, 210, 255, 255)

CLOCK = pygame.time.Clock()
FPSCAP = 30

BANANAIMG = pygame.image.load("Assets/banana.png")
BANANA = pygame.transform.scale(BANANAIMG, (250,250))

######### USER #########

UserData = UnpackData.UnpackData()

BoostBananasPerClick = UserData["BananasPerClick"]
BoostBananasPerSecond = UserData["BananasPerSecond"]

gradien = pygame.image.load("/Users/tobyholder/Documents/Programs/Banana-Clicker-Alevel-Programming-Project/Assets/gradient.png").convert_alpha()
gradien = pygame.transform.scale(gradien, (480,120))
gradien.set_alpha(30)

######### CLASSES #########

class SettingsButton:
    def __init__(self):
        self.Size = [75, 75]

        self.Image = pygame.image.load("Assets/SettingsIcon.png").convert_alpha()
        self.Image = pygame.transform.scale(self.Image, self.Size)
        self.Rect = self.Image.get_rect(center=(50, HEIGHT-50))
        self.Mask = pygame.mask.from_surface(self.Image)



class ShopButton:
    def __init__(self):
        self.Size = [75,  75]

        self.Image = pygame.image.load("Assets/ShopIcon.png").convert_alpha()
        self.Image = pygame.transform.scale(self.Image, self.Size)
        self.Rect = self.Image.get_rect(center=(WIDTH-50, HEIGHT-50))
        self.Mask = pygame.mask.from_surface(self.Image)



class BananaMain:
    def __init__(self):
        self.Size = [300,300]

        self.Image = pygame.image.load("Assets/banana.png").convert_alpha()
        self.Image = pygame.transform.scale(self.Image, self.Size)
        self.Rect = self.Image.get_rect(center=(WIDTH/2, HEIGHT/2))
        self.Mask = pygame.mask.from_surface(self.Image)



class BananaParticle:
    def __init__(self):
        self.Position = [random.randint(0,WIDTH),-50]
        self.Speed = [0,random.randint(5,10)]
        self.Opacity = 255 #stored as an 8bit denary number - 255 = 100% 0 = 0% opacity

        self.Image = pygame.image.load("Assets/BananaParticleNoBG.png").convert_alpha()
        self.Image = pygame.transform.scale(self.Image, (50, 50))
        self.Rect = self.Image.get_rect(center=self.Position)
        self.Mask = pygame.mask.from_surface(self.Image)



class BananaParticles:
    def __init__(self):
        self.Particles = []
        self.LastParticle = time.time()

    def UpdateParticles(self):

        for particle in self.Particles:
            particle.Position[1] += particle.Speed[1]
            particle.Rect.move_ip(particle.Speed)
            #particle.Opacity = 255 - ((particle.Position[1] /(HEIGHT * 0.9)) * 255)
            particle.Opacity = 255-((((particle.Position[1]/(HEIGHT*0.9))*255)**3)/255**2)  #decreases the opacity of the particles based on this graph: https://www.desmos.com/calculator/dgvyxo5tff
            particle.Image.set_alpha(particle.Opacity)

            if particle.Position[1] > HEIGHT + 50 or particle.Opacity == 0:  #checks to see if the current particle has left the screen or if its opacity = 0
                self.Particles.remove(particle)  #if it has then it is removed

    def RenderParticles(self):

        for particle in self.Particles:
            WIN.blit(particle.Image, particle.Rect)

    def AddParticles(self, amount):
        for i in range(amount):
            self.Particles.append(BananaParticle())



class AirDropEvent:
    def __init__(self):
        self.Size = [100,150]
        self.Position = [random.randint(100,WIDTH-100),-150]
        self.Speed = [0,1.5]
        self.Opacity = 255 #stored as an 8bit denary number - 255 = 100% 0 = 0% opacity

        self.Image = pygame.image.load("Assets/AirDrop.png").convert_alpha()
        self.Image = pygame.transform.scale(self.Image, self.Size)
        self.Rect = self.Image.get_rect(center=(self.Position[0], self.Position[1]))
        self.Mask = pygame.mask.from_surface(self.Image)

        self.LastDrop = time.time()
        self.Visible = False

        self.Bonus = GetRandomBonus()
        self.BonusStart = 0
        self.BonusTime = 0

    def RenderAirDrop(self):
        WIN.blit(self.Image, self.Rect)
        #print(self.Position)

    def UpdateAirDrop(self):
        global LastAirDropEvent, CurrentAirDropDelay, AirDropEventsEnabled

        self.Position[1] += self.Speed[1]
        self.Rect.move_ip(self.Speed)
        #self.Opacity = 255 - ((self.Position[1] /(HEIGHT * 0.9)) * 255)
        self.Opacity = 255-((((self.Position[1]/(HEIGHT*0.9))*255)**3)/255**2)  #decreases the opacity of the particles based on this graph: https://www.desmos.com/calculator/dgvyxo5tff
        self.Image.set_alpha(self.Opacity)

        if self.Position[1] > HEIGHT + 150 or self.Opacity == 0:
            self.LastDrop = time.time()
            CurrentAirDropDelay = random.randint(AirDropEventSpawnRate * 6, AirDropEventSpawnRate * 14) / 10
            self.Visible = False


######### FUNCTIONS #########

def WriteText(Message, Position, Size):
    Font = pygame.font.Font('Assets/Fonts/TitanOne.ttf', Size)
    TextSurface = Font.render(Message, True, (255,255,255))
    TextRect = TextSurface.get_rect()
    TextRect.center  = Position
    WIN.blit(TextSurface, TextRect)



BananaParticlesManager = BananaParticles()
Banana = BananaMain()


AirDrop = AirDropEvent( )
SettingsButton = SettingsButton()
ShopButton = ShopButton()

ToAdd = 0
AddEachFrame = ToAdd/30
TotalAdded = 0

def AwardBananas(Amount):
    global ToAdd, AddEachFrame, TotalAdded

    ToAdd = Amount
    AddEachFrame = ToAdd/30
    TotalAdded = 0

if __name__ == "__main__":

    while True:

        CLOCK.tick(FPSCAP)

        pygame.display.set_caption(str("Top Banana! ({})").format(int(pygame.Clock.get_fps(CLOCK))))

        if time.time() - AirDrop.BonusStart < AirDrop.BonusTime:
            BananasPerSecond = BoostBananasPerSecond
            BananasPerClick = BoostBananasPerClick
        else:
            BoostBananasPerClick = UserData["BananasPerClick"]
            BoostBananasPerSecond = UserData["BananasPerSecond"]

            BananasPerSecond = UserData["BananasPerSecond"]
            BananasPerClick = UserData["BananasPerClick"]

        if TotalAdded <= ToAdd:
            TotalAdded += AddEachFrame
            UserData["Bananas"] += AddEachFrame

        UserData["Bananas"] += BananasPerSecond / FPSCAP

        WIN.fill(BackgroundColour)

        #BananaParticlesManager.AddParticles(1)
        BananaParticlesManager.UpdateParticles()
        BananaParticlesManager.RenderParticles()

        if BananasPerSecond != 0:
            if BananasPerSecond != 30:
                if time.time() - BananaParticlesManager.LastParticle > 1 / BananasPerSecond:
                    BananaParticlesManager.AddParticles(1)
                    BananaParticlesManager.LastParticle = time.time()
            else:
                BananaParticlesManager.AddParticles(1)

        WIN.blit(Banana.Image, Banana.Rect)
        WIN.blit(SettingsButton.Image, SettingsButton.Rect)
        WIN.blit(ShopButton.Image, ShopButton.Rect)

        if time.time() - AirDrop.LastDrop > CurrentAirDropDelay and AirDrop.Visible == False:
            AirDrop = AirDropEvent()
            AirDrop.Visible = True

        if AirDrop.Visible == True:
            AirDrop.UpdateAirDrop()
            AirDrop.RenderAirDrop()

        WIN.blit(gradien,(0,0))

        WriteText(str(int(UserData["Bananas"]))+"  Bananas", (WIDTH/2, 50), 48-len(str(int(UserData["Bananas"]))))
        WriteText(str(BananasPerSecond)+"  Bps", (WIDTH/2, 85), 24)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                UnpackData.WriteDataToFile(UserData)
                pygame.quit()
                exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                Pos = event.pos
                PosInBanana = Pos[0] - Banana.Rect.x, Pos[1] - Banana.Rect.y
                TouchingBanana = Banana.Rect.collidepoint(Pos) and Banana.Mask.get_at(PosInBanana)

                if AirDrop.Rect.collidepoint(Pos) == True:
                    exec(AirDrop.Bonus[0])
                    AirDrop = AirDropEvent()
                    if AirDrop.Bonus[1] != -1:
                        AirDrop.BonusStart = time.time()
                        AirDrop.BonusTime = AirDrop.Bonus[1]
                
                elif ShopButton.Rect.collidepoint(Pos) == True:
                    print("shop")

                elif SettingsButton.Rect.collidepoint(Pos) == True:
                    print("settings")

                if TouchingBanana == True:
                    UserData["Bananas"] += BananasPerClick
                    BananaParticlesManager.AddParticles(1)

        pygame.display.update()