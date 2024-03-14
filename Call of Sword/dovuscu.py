import pygame


class Dovuscu():
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, sound):
        self.player = player
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0 # 0 : idle , 1 : run , 2 : jump , 3 : attack1 , 4 = attack2 , 5 : hit , 6 : death
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 80, 180)) # 80 ve 180 değerleri dikdörtgenimin çizilceği koordinatlar
        self.vel_y = 0 # jump kontrolü için ekstra bir y yönünde değişken
        self.run = False
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.a_cooldown = 0
        self.attack_sound = sound
        self.hit = False
        self.health = 1000
        self.alive = True





    def load_images(self, sprite_sheet, animation_steps):
        
        animation_list = []
        
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
           
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
    
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        
        return animation_list





    def move(self, screen_width, screen_height, surface, target, round_rover):
        
        speed = 10
        gravity = 2
        dx = 0  # bu benım delta değişkenim haraketleri belirlerken x koordinatında kullanmak için ayarlandı
        dy = 0  # bu benım delta değişkenim haraketleri belirlerken y koordinatında kullanmak için ayarlandı
        self.run = False
        self.attack_type = 0

        # basılan tuşları algılama
        key = pygame.key.get_pressed()

        
        if self.attacking == False and self.alive == True and round_rover == False:

            #PLAYER 
            if self.player == 1:
                # move tuşları
                if key[pygame.K_a]:
                    dx = -speed
                    self.run = True

                if key[pygame.K_d]:
                    dx = speed
                    self.run = True

                # zıplama
                if key[pygame.K_w] and self.jump == False:
                    self.vel_y = -30
                    self.jump = True

                # saldırı kontrolleri
                if key[pygame.K_r] or key[pygame.K_t]:

                    self.attack(target)

                    # attack tiplerini ayarlama
                    if key[pygame.K_r]:
                        self.attack_type = 1
                    
                    if key[pygame.K_t]:
                        self.attack_type = 2




                #NPC
            if self.player == 2:
                # move tuşları
                if key[pygame.K_LEFT]:
                    dx = -speed
                    self.run = True

                if key[pygame.K_RIGHT]:
                    dx = speed
                    self.run = True

                # zıplama
                if key[pygame.K_UP] and self.jump == False:
                    self.vel_y = -30
                    self.jump = True

                # saldırı kontrolleri
                if key[pygame.K_KP1] or key[pygame.K_KP2]:

                    self.attack(target)

                    # attack tiplerini ayarlama
                    if key[pygame.K_KP1]:
                        self.attack_type = 1
                    
                    if key[pygame.K_KP2]:
                        self.attack_type = 2








        # yercekimi ayarlama
        self.vel_y += gravity
        dy += self.vel_y



        # pencere sınırlandırma işlemi
        # pencerenin sol tarafı
        if self.rect.left + dx < 0:
            dx = -self.rect.left

        #pencerenin sağ tarafı
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right

        #pencerenin aşağı tarafı
        if self.rect.bottom + dy > screen_height - 30:
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 30 - self.rect.bottom   

        # oyuncu karşılaşma
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True 

        
        # attack cooldown
        if self.a_cooldown > 0:
            self.a_cooldown -= 1




        # haraket sonrasında karakter pozisyonumu güncelleme
        self.rect.x += dx
        self.rect.y += dy






    def uptade(self):
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.uptade_action(6)

        elif self.hit == True:
            self.uptade_action(5)
        
        elif self.attacking == True:

            if self.attack_type == 1:
                self.uptade_action(3)
            
            elif self.attack_type == 2:
                self.uptade_action(4)


        elif self.jump == True:
            self.uptade_action(2)
    

        elif self.run == True:
            self.uptade_action(1)

        else:
            self.uptade_action(0)


        cooldown = 50
        self.image = self.animation_list[self.action][self.frame_index]

        if pygame.time.get_ticks() - self.time > cooldown:
            self.frame_index += 1
            self.time = pygame.time.get_ticks()

        if self.frame_index >= len(self.animation_list[self.action]):

            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1

            else:
                
                self.frame_index = 0

                if self.action == 3 or self.action == 4:
                    self.attacking = False
                    self.a_cooldown = 20

                if self.action == 5:
                    self.hit = False

                    self.attacking = False
                    self.a_cooldown = 20





    def attack(self, target):
        
        if self.a_cooldown == 0:
            self.attacking = True
            self.attack_sound.play()
            
            attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height) #attack skilleri için oluşturduğumuz hitbox
            
            if attacking_rect.colliderect(target.rect):
                target.health -= 50
                target.hit = True
                print("Çarpışma Başarılı Oldu.")
            

            # pygame.draw.rect(surface, (255,0,0), attacking_rect) # attack hitbox draw





    def uptade_action(self, n_action):
       
        if n_action != self.action:
            self.action = n_action

            self.frame_index = 0
            self.time = pygame.time.get_ticks()





    # yarattığım hitboxları çizdirmek için kullanacağım fonksiyonum
    def draw(self, surface):
       
        gorsel = pygame.transform.flip(self.image, self.flip, False)
        
        # pygame.draw.rect(surface, (0,255,255), self.rect) # self.rect komutum yukarıda dövüscüler için belirtmiş olduğum dikdörtgen
        
        surface.blit(gorsel, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))