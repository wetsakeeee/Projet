import pygame, sys, subprocess, time
from pygame.display import flip
pygame.init()
width , height = 1280 , 720
screen = pygame.display.set_mode((width,height))

#Icon
icon = pygame.image.load("images/logo.png").convert_alpha()
pygame.display.set_icon(icon)
#BG
BG = pygame.image.load("images/fondmenu.jpeg").convert_alpha()
BG = pygame.transform.scale(BG, (1280, 720))
pygame.display.set_caption("L'Enfer")
#Couleurs
Blanc = (255,255,255)
bleu_transparent = (0,80,200,180)
bleu_selection = (0,140,255,220)
shadow = (0,0,0)
#Polices d'écritures
try :   
    Police_titre = pygame.font.Font("Coolvetica Rg.otf", 72)
    Police_bouton =  pygame.font.Font("Coolvetica Rg.otf", 36)

except :
    Police_titre = pygame.font.SysFont(None, 72)
    Police_bouton =  pygame.font.SysFont(None, 36)

class Button :
    def __init__(self,text,center_y,action):
        self.text = text
        self.action = action
        self.center_y = center_y
        self.widht, self.height = 320,70
        self.rect = pygame.Rect((0,0,self.widht,self.height))
        self.rect.center = (width//2 , center_y)
   
    def draw(self, win, mouse_pos):
        is_hover = self.rect.collidepoint(mouse_pos)
        color = bleu_selection if is_hover else bleu_transparent 
        button_surface = pygame.Surface((self.widht,self.height), pygame.SRCALPHA)
        pygame.draw.rect(button_surface,color,(0,0,self.widht,self.height),border_radius = 16)
        win.blit(button_surface, self.rect)
        
        text_surf = Police_bouton.render(self.text, True, Blanc)
        text_rect = text_surf.get_rect(center=self.rect.center)
        win.blit(text_surf, text_rect)
    def is_clicked(self,mouse_pos, mouse_pressed):
        return self.rect.collidepoint(mouse_pos) and mouse_pressed[0]

#Logo
LOGO = pygame.image.load("images/logo.png").convert_alpha()
LOGO = pygame.transform.scale(LOGO, (300, 300))
logo_rect = LOGO.get_rect(center=(width // 2, 150))



#Listes des boutons
buttons = [
    Button("Jouer", 360, "play"),
    Button("Parametres", 440, "settings"),
    Button("Sauvegarde", 520, "code"),
    Button("Quitter", 600, "quit"),
]

#Musique et son
musique_menu = pygame.mixer.Sound("menu.ogg")
musique_menu.play(-1,0,3000) #boucle infini
musique_menu.set_volume(1.0)
son_bouton = pygame.mixer.Sound("bouton.mp3")




















  
running = True
clock = pygame.time.Clock()
while running:
    clock.tick(60)
    screen.fill((0,0,0))
    screen.blit(BG,(0,0))
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    screen.blit(BG, (0,0))
    screen.blit(LOGO, logo_rect)


    for btn in buttons:
        btn.draw(screen,mouse_pos)
        if btn.is_clicked(mouse_pos,mouse_pressed):
            pygame.time.delay(200)
        
            if btn.action == "play":
                print("nouvelle partie")
                son_bouton.play(0,0,0)
                son_bouton.set_volume(1.0)
                time.sleep(0.3)
                pygame.quit()
                subprocess.run(['python', "general.py"])
                sys.exit()
            elif btn.action == "code":
                son_bouton.play(0,0,0)
                son_bouton.set_volume(0.5)
                print("interface code")
            elif btn.action == "settings":
                son_bouton.play(0,0,0)
                son_bouton.set_volume(0.5)
                print("interface paramètres")
            elif btn.action == "quit":
                son_bouton.play(0,0,0)
                son_bouton.set_volume(0.5)
                time.sleep(0.3)
                running = False














    
    
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()



pygame.quit()
sys.exit()   
    

