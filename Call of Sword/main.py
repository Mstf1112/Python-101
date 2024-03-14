import pygame
from pygame import mixer
from dovuscu import Dovuscu


mixer.init()
pygame.init()


# pencere oluşturma
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600



screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
# pencere isim adlandırma
pygame.display.set_caption("Call of Sword")



# fps ayarları
clock = pygame.time.Clock()
FPS = 60



# can barları
GREEN = (0,255,0)
WHITE = (255,255,255)
RED = (255,0,0)



#ss
intro_count = 3
last_count = pygame.time.get_ticks()
score = [0, 0]
round_over = False
ROUND_OVER_COOLDOWN = 2000



#s
DOVUSCU_SIZE = 162
DOVUSCU_SCALE = 4
DOVUSCU_OFFSET = [72, 60]
DOVUSCU_DATA = [DOVUSCU_SIZE, DOVUSCU_SCALE, DOVUSCU_OFFSET]
NPC_SIZE = 250
NPC_SCALE = 3
NPC_OFFSET = [112, 111]
NPC_DATA = [NPC_SIZE, NPC_SCALE, NPC_OFFSET]



#müzik
pygame.mixer.music.load("assets/audio/music.mp3")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1, 0.0, 5000)


# s
sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
sword_fx.set_volume(0.1)


# ss
magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")
magic_fx.set_volume(0.1)



# arkaplan görselimi yükleme
bg_image = pygame.image.load("levels/desert.png").convert_alpha()



# animasyon görselleri
dovuscu_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
npc_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()



# kazanma görseli
victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()



# animasyon index belirleme
DOVUSCU_ANIMATION_STEPS = [10,8,1,7,7,3,7]
NPC_ANIMATION_STEPS = [8,8,1,8,8,3,7]



#font
font = pygame.font.Font("assets/fonts/turok.ttf", 80)
score_f = pygame.font.Font("assets/fonts/turok.ttf", 30)



def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))



# arkaplan görselimi yazdırma fonksiyonum
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image , (SCREEN_WIDTH,SCREEN_HEIGHT))  # arkaplan görselimi ölçeklendirme
    screen.blit(scaled_bg, (0,0))



# can çubuklarını yazdırma fonksiyonum
def draw_health_bar (health, x, y):
    
    i = health / 1000

    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, GREEN, (x, y, 400 * i, 30))
    


# dovusculeri oluşturma fonksiyonum
dovuscu_1 = Dovuscu(1, 200, 390, False, DOVUSCU_DATA, dovuscu_sheet, DOVUSCU_ANIMATION_STEPS, sword_fx)
dovuscu_2 = Dovuscu(2, 700, 390, True, NPC_DATA, npc_sheet, NPC_ANIMATION_STEPS, magic_fx)



# oyun döngüsü
run = True
while run:

    # FPS
    clock.tick(FPS)

    # arkaplan görsel fonksiyonunu aktif etme
    draw_bg()

    # can barları görsel fonksiyonunu aktif etme
    draw_health_bar(dovuscu_1.health, 20,20)
    draw_health_bar(dovuscu_2.health, 580,20)

    # puan yazdırma
    draw_text("Sovalye : " + str(score[0]), score_f, RED, 20, 60)
    draw_text("Buyucu : " + str(score[1]), score_f, RED, 580, 60)



# başlangıç
    if intro_count <= 0:

        #dovusculerimi haraketlerimi ekrana cizdirme
        dovuscu_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, dovuscu_2, round_over)
        dovuscu_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, dovuscu_1, round_over)
    
    else:
        draw_text(str(intro_count), font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)

        if (pygame.time.get_ticks() - last_count) >= 1000:
            intro_count -= 1
            last_count = pygame.time.get_ticks()



    if round_over == False:
        if dovuscu_1.alive == False:
            score[1] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()

        elif dovuscu_2.alive == False:
            score[0] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()

    else:

        screen.blit(victory_img, (360, 150))

        if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
            round_over = False
            intro_count = 3
            dovuscu_1 = Dovuscu(1, 200, 390, False, DOVUSCU_DATA, dovuscu_sheet, DOVUSCU_ANIMATION_STEPS, sword_fx)
            dovuscu_2 = Dovuscu(2, 700, 390, True, NPC_DATA, npc_sheet, NPC_ANIMATION_STEPS, magic_fx)
                



    #animasyon uptade
    dovuscu_1.uptade()
    dovuscu_2.uptade()


    #dovusculerimi ekrana cizdirme
    dovuscu_1.draw(screen)
    dovuscu_2.draw(screen)


    # haraket döngüsü
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    # pencere güncelleme
    pygame.display.update()



# pygame çıkış
pygame.quit()
