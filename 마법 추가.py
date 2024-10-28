
import pygame
import sys

# Pygame 초기화
pygame.init()

# 화면 설정
screen_width, screen_height = 1920, 1000
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Weapon Selection Menu")

# 폰트 설정
font = pygame.font.Font('C:/Users/User/Desktop/startcoding/CookieRun bold.ttf', 55)

# 무기 리스트
weapons = ["Sword", "HandGun", "Magic"]
selected_weapon_index = 0

# 메뉴 표시 함수
def draw_menu():
    screen.fill((0, 0, 100))  # 검은색 배경

    title_text = font.render("Select Your Weapon", True, (255, 255, 255))
    screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 100))

    for i, weapon in enumerate(weapons):
        color = (255, 0, 0) if i == selected_weapon_index else (255, 255, 255)
        weapon_text = font.render(weapon, True, color)
        screen.blit(weapon_text, (screen_width // 2 - weapon_text.get_width() // 2, 200 + i * 100))

    pygame.display.flip()

# 메뉴 루프
running = True
while running:
    draw_menu()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                selected_weapon_index = (selected_weapon_index - 1) % len(weapons)
            elif event.key == pygame.K_DOWN:
                selected_weapon_index = (selected_weapon_index + 1) % len(weapons)
            elif event.key == pygame.K_RETURN:
                selected_weapon = weapons[selected_weapon_index]
                running = False

# 선택한 무기 출력 (게임 시작 전 무기 선택 결과를 사용)
print(f"Selected Weapon: {selected_weapon}")

# 기존 게임 코드에 선택된 무기 반영
weapon_type = selected_weapon.lower()  # 무기 타입을 소문자로 변환하여 사용

import pygame
import sys
import math
import random
'''import shutil

# 파일을 현재 작업 디렉토리로 복사

shutil.copy("C:/Users/User/Desktop/startcoding/gun_reloading.mp3", ".")'''

# 초기화
pygame.init()
pygame.mixer.init()

# 화면 크기 설정
screen_width = 1920
screen_height = 1000
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pygame Player with Enemies')

#총 소리
gunshot_sound = pygame.mixer.Sound("gunshot_sound.mp3")
gun_reloading_sound = pygame.mixer.Sound("gun_reloading.mp3")

#폰트
font = pygame.font.Font('CookieRun Regular.ttf', 22)
ammo_font = pygame.font.Font('CookieRun Regular.ttf', 37)  # 폰트 크기 48로 변경
damage_texts = []       # Damage 텍스트 리스트와 폰트
damage_font = pygame.font.Font('CookieRun Regular.ttf', 30)

# 색상
GROUND_COLOR = (139, 69, 19)  # 땅 색상
PLAYER_COLOR = (0, 255, 0)  # 플레이어 색상
ENEMY_COLOR = (0, 0, 255)  # 적 색상
PROJECTILE_COLOR = (255, 0, 0)  # 투사체 색상
WARNING_COLOR = (255, 0, 0)  # 빨간색 느낌표 색상
WHITE = (255, 255, 255)

# 화면 진동 설정
shake_duration = 140  # 진동 지속 시간 (밀리초)
shake_magnitude = 3 # 진동의 강도 (화면이 흔들리는 범위)
shake_start_time = None  # 진동 시작 시간

#불 이미지
fire_image = pygame.image.load('C:/Users/User/Desktop/startcoding/fire.png')
fire_image = pygame.transform.scale(fire_image, (37, 51))

#총알 이미지
bullet_image = pygame.image.load('C:/Users/User/Desktop/startcoding/bullet.png')
bullet_image = pygame.transform.scale(bullet_image, (15, 32))

# 검 이미지 추가
sword_image = pygame.image.load('C:/Users/User/Desktop/startcoding/sword.png')
sword_image = pygame.transform.scale(sword_image, (400, 60))

#총 이미지
handgun_image = pygame.image.load('C:/Users/User/Desktop/startcoding/handgun.png')
handgun_image = pygame.transform.scale(handgun_image, (25, 110))

#조준점 이미지
pointer_image = pygame.image.load('C:/Users/User/Desktop/startcoding/pointer.png')
pointer_image = pygame.transform.scale(pointer_image, (120, 120))
big_pointer_image = pygame.image.load('C:/Users/User/Desktop/startcoding/big pointer.png')
big_pointer_image = pygame.transform.scale(big_pointer_image, (180, 180))

#적 생성 경고 이미지
warning_image = pygame.image.load('C:/Users/User/Desktop/startcoding/warning.png')
warning_image = pygame.transform.scale(warning_image, (80, 80))

# 플레이어 설정
player_image = pygame.image.load('C:/Users/User/Desktop/startcoding/player.png')  # 업로드한 이미지 파일
player_image = pygame.transform.scale(player_image, (75, 75))  # 이미지 크기 조정
player_x = screen_width // 2
player_y = screen_height // 2
player_speed_x = 0  # X축 속도
player_speed_y = 0  # Y축 속도
acceleration = 0.5  # 가속도
friction = 0.97  # 마찰(감속 비율)
projectile_speed = 50  # 투사체 속도
player_Maxhp = 150
player_hp = 150  # 플레이어 HP

enemy_image = pygame.image.load('C:/Users/User/Desktop/startcoding/zombie.png')  # 적 이미지 파일
enemy_image = pygame.transform.scale(enemy_image, (75, 75))  # 적 이미지 크기 조정

fast_enemy_image = pygame.image.load('C:/Users/User/Desktop/startcoding/fast zombie.png')  # 적 이미지 파일
fast_enemy_image = pygame.transform.scale(fast_enemy_image, (75, 75))  # 적 이미지 크기 조정

giant_enemy_image = pygame.image.load('C:/Users/User/Desktop/startcoding/giant zombie.png')  # 적 이미지 파일
giant_enemy_image = pygame.transform.scale(giant_enemy_image, (100, 100))  # 적 이미지 크기 조정

#적 이미지 지정
enemy_imagenumber = [enemy_image, fast_enemy_image, giant_enemy_image]

# 함수: 화면 진동 시작
def start_screen_shake():
    global shake_start_time
    shake_start_time = pygame.time.get_ticks()  # 진동 시작 시간 기록

# 함수: 화면 진동 적용
def apply_screen_shake():
    if shake_start_time is not None:
        elapsed_time = pygame.time.get_ticks() - shake_start_time
        if elapsed_time < shake_duration:
            # 진동 중인 경우
            shake_offset_x = random.randint(-shake_magnitude, shake_magnitude)
            shake_offset_y = random.randint(-shake_magnitude, shake_magnitude)
            return shake_offset_x, shake_offset_y
        else:
            # 진동 종료
            return 0, 0
    return 0, 0

# Damage Text 클래스
class DamageText:
    def __init__(self, x, y, damage):
        self.x = x + random.randint(-70, 70)  
        self.y = y + random.randint(-70, 70)  
        self.damage = damage
        self.lifetime = 400  
        self.hold_time = 350
        self.start_time = pygame.time.get_ticks()
        self.initial_font_size = 60  # 초기 폰트 크기

    def draw(self, screen, base_font):
        # 현재 시간이 텍스트 시작 시간보다 작다면 화면에 표시
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.start_time
        if elapsed_time < self.lifetime:
            # 텍스트가 유지되는 시간 동안 크기를 유지
            if elapsed_time < self.hold_time:
                font_size = self.initial_font_size
            # 그 이후에는 텍스트 크기가 갑자기 줄어듦
            else:
                shrink_factor = (elapsed_time - self.hold_time) / (self.lifetime - self.hold_time)
                font_size = max(10, int(self.initial_font_size * (1 - shrink_factor)))

            # 폰트를 생성하고 화면에 그리기
            font = pygame.font.Font(None, font_size)
            damage_text = font.render(str(int(self.damage)), True, (0, 0, 0))
            screen.blit(damage_text, (self.x, self.y))
            return True
        return False

damage_texts = []

def apply_damage(target, damage, color):
    damage_texts.append(DamageText(target.x, target.y, damage, color))  # 대미지 텍스트 생성

player_experience = 0
experience_to_level_up = 200
player_level = 1
damage_up = 1

# 경험치 추가 함수
def add_experience(amount):
    global player_experience, player_level, experience_to_level_up, player_hp, player_Maxhp, weapon_damage, damage_up
    player_experience += amount
    if player_experience >= experience_to_level_up:
        player_experience -= experience_to_level_up
        player_level += 1
        experience_to_level_up = int(experience_to_level_up * 1.5)  # 레벨업 시 필요한 경험치 증가
        
        player_Maxhp *= 1.2
        player_hp *= 1.2  
        damage_up *= 1.2 
        
# 적 클래스
class Enemy:
    def __init__(self, x, y, hp, speed, size, number, enemy_weight, damage):
        self.x = x
        self.y = y
        self.hp = hp
        self.Maxhp = hp
        self.radius = size  # 적의 크기
        self.speed = speed  # 적의 기본 속도
        self.base_speed = speed# base_speed 추가
        self.weight = enemy_weight #무게(밀려나는 정도)
        self.damage = damage #공격력
        self.color = (0, 0, 0)  # 적의 색상
        self.vx = 0
        self.vy = 0
        self.friction = 0.97
        self.noise_intensity = 2  # 이 부분은 필요 시 조절
        self.num = number
        
    def draw(self, screen):
        angle = math.degrees(math.atan2(player_y - self.y, player_x - self.x))
        rotated_enemy = pygame.transform.rotate(enemy_imagenumber[self.num], -angle)  # 적 이미지를 회전
        enemy_rect = rotated_enemy.get_rect(center=(self.x + shake_offset_x, self.y + shake_offset_y))
        screen.blit(rotated_enemy, enemy_rect.topleft)  # 회전된 적을 그립니다.
        
    def hit(self, damage):
        self.hp -= damage
        damage_texts.append(DamageText(self.x, self.y, damage))
        if self.hp <= 0:
            self.die()

    def die(self):
        add_experience(self.exp_reward)  # 적 처치 시 경험치 추가

    def follow_player(self, player_x, player_y):
        # 플레이어와의 거리 계산
        distance = math.hypot(player_x - self.x, player_y - self.y)

        # 거리 기반으로 속도 조절
        if distance < 150:
            speed = self.base_speed * 5  # 가까이 있을 때 속도 증가
        else:
            speed = self.base_speed

        # 플레이어를 향하는 각도 계산
        angle = math.atan2(player_y - self.y, player_x - self.x)

        # 기존 속도에 새로운 속도를 더하여 부드럽게 움직임
        self.vx += (speed * math.cos(angle)) * 0.1  # x방향 속도 업데이트
        self.vy += (speed * math.sin(angle)) * 0.1  # y방향 속도 업데이트

        # 감속(friction) 적용
        self.vx *= self.friction
        self.vy *= self.friction

        # 움직임에 노이즈 추가
        #noise_x = random.uniform(-self.noise_intensity, self.noise_intensity)
      #  noise_y = random.uniform(-self.noise_intensity, self.noise_intensity)

        # 최종적으로 적의 위치 업데이트
        self.x += self.vx # noise_x
        self.y += self.vy  #noise_y

        
# 강력한 적 클래스
#숫자 : 체력, 속도, 크기(반지름), 번호,무게, 공격력
class StrongEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, 250, 3, 50, 2, 1.5, 15)  # 큰 적
        self.exp_reward = 50

# 빠른 적 클래스
class FastEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, 100, 6, 37, 1, 0.75, 20)  # 빠른 적
        self.exp_reward = 30

# 일반 적 클래스
class NormalEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, 100, 3.5, 37, 0, 1, 10)  # 일반 적
        self.exp_reward = 20

# 랜덤으로 적을 생성하는 함수
def spawn_random_enemy():
    x = random.randint(50, screen_width - 50)
    y = random.randint(50, screen_height - 50)
    enemy_type = random.choice([FastEnemy, StrongEnemy, NormalEnemy])
    return enemy_type(x, y)

# 적 리스트
enemies = []
enemy_spawn_delay = 3000
last_enemy_spawn_time = pygame.time.get_ticks()

# 게임 루프 내에서 적 생성 로직
current_time = pygame.time.get_ticks()
if current_time - last_enemy_spawn_time > enemy_spawn_delay:
    enemies.append(spawn_random_enemy())
    last_enemy_spawn_time = current_time

# 투사체 발사 딜레이 설정
shoot_delay = 150  # 밀리초
last_shot_time = pygame.time.get_ticks()  # 마지막으로 발사된 시간

# 플레이어가 검을 휘두를 때를 위한 변수 설정
is_swinging_sword = False
sword_swing_duration = 300  # 휘두르는 시간 (밀리초)
sword_last_swing_time = 0  # 마지막 휘두른 시간

# 투사체 클래스
class Projectile:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = projectile_speed
        self.radius = 8
        self.to_remove = False 

    def update(self):
        # 투사체의 방향에 따라 위치 업데이트
        self.x += self.speed * math.cos(math.radians(self.angle))
        self.y += self.speed * math.sin(math.radians(self.angle))

    def draw(self, screen):
        # 무기 회전 및 그리기
        rotated_projectile = pygame.transform.rotate((bullet_image), -self.angle - 90)  # 투사체 회전  # 원형 투사체 그리기
        projectile_rect = rotated_projectile.get_rect(center=(self.x+ shake_offset_x, self.y+ shake_offset_y))
        screen.blit(rotated_projectile, projectile_rect.topleft)  # 화면에 그리기

class FireProjectile:
    def __init__(self, x, y, target_x, target_y):
        self.angle = math.degrees(math.atan2(target_y - y, target_x - x))
        self.x = x 
        self.y = y 
        self.speed = 12.5  # 원하는 속도 설정
        self.radius = 45
        self.image = pygame.transform.scale(fire_image, (122, 77))  # 불 크기 조정
        self.exploded = False
        self.explosion_radius = 125  # 폭발 반경
        self.explosion_damage = 25  # 폭발에 의한 피해량
        self.to_remove = False  # 삭제 플래그

    def update(self):
        # 각도에 따라 위치 업데이트
        self.x += self.speed * math.cos(math.radians(self.angle))
        self.y += self.speed * math.sin(math.radians(self.angle))

                # 각도에 따라 위치 업데이트
        self.x += self.speed * math.cos(math.radians(self.angle))
        self.y += self.speed * math.sin(math.radians(self.angle))

    def draw(self, screen):
        # 위치에 따라 불 이미지 회전 및 화면에 그리기
        rotated_fire = pygame.transform.rotate(self.image, -self.angle)
        fire_rect = rotated_fire.get_rect(center=(self.x+ shake_offset_x, self.y+ shake_offset_y))
        screen.blit(rotated_fire, fire_rect.topleft)
        
    def explode(self, enemies):
        # 폭발 발생 시 반경 내의 적들에게 피해를 주고 폭발 이펙트를 추가
        explosion_effect_color = (255, 0, 0)  # 폭발 이펙트 색상 (주황색)
        pygame.draw.circle(screen, explosion_effect_color, (int(self.x), int(self.y)), self.explosion_radius)  # 폭발 반경을 표시
        
        # 폭발 반경 내의 적들에게 피해 적용
        for enemy in enemies:
            distance = math.hypot(enemy.x - self.x, enemy.y - self.y)
            if distance <= self.explosion_radius:
                total_damage = self.explosion_damage * damage_up
                enemy.hit(total_damage)  # 적의 HP 감소
        self.exploded = True
        self.to_remove = True  # 투사체 삭제 플래그 설정

              
# 투사체 리스트
projectiles = []

# 적 리스트
enemies = []
enemy_spawn_time = pygame.time.get_ticks()  # 적 생성 시간
# 적 생성 경고 시간과 딜레이 설정
enemy_warning_time = 2000  # 경고를 미리 표시할 시간 (밀리초)
enemy_spawn_delay = 1000  # 적 생성 간격 (밀리초)
enemy_spawn_warning_time = None  # 생성 경고를 표시할 시간 변수
last_enemy_spawn_time = pygame.time.get_ticks()
new_enemy_x = None  # 적이 생성될 x 좌표
new_enemy_y = None  # 적이 생성될 y 좌표


# 총알 관련 변수
max_ammo_per_magazine = 20  # 한 탄창당 최대 총알 수
current_ammo = max_ammo_per_magazine  # 현재 탄창의 총알 수
total_magazines = 5  # 가지고 있는 탄창 수
reload_time = 1100  # 재장전 시간 (밀리초)
is_reloading = False  # 재장전 상태인지 확인
last_reload_time = 0  # 마지막 재장전 시간

#마법 관련 변수
hand_select = 0

# 게임 루프
running = True
while running:
    if weapon_type == 'handgun' : 
        weapon_damage = 30 * damage_up
        shoot_delay = 150           
    elif weapon_type == 'sword':
        weapon_damage == 50
    elif weapon_type == 'magic':
        weapon_damage = 25 * damage_up
        shoot_delay = 500  
                
    # 화면 그리기
    screen.fill(GROUND_COLOR)  # 배경을 땅 색상으로 채우기
    # 화면 진동 적용
    shake_offset_x, shake_offset_y = apply_screen_shake()
    # 키 입력 처리
    keys = pygame.key.get_pressed()
    
    # WASD로 가속도 추가
    if keys[pygame.K_a]:  # A키
        player_speed_x -= acceleration
    if keys[pygame.K_d]:  # D키
        player_speed_x += acceleration
    if keys[pygame.K_w]:  # W키
        player_speed_y -= acceleration
    if keys[pygame.K_s]:  # S키
        player_speed_y += acceleration
        # R키로 재장전
    if keys[pygame.K_r] and not is_reloading or current_ammo == 0 and not is_reloading:  # 재장전 중이 아닐 때만 재장전 가능
        if total_magazines > 0 and current_ammo < max_ammo_per_magazine:
            is_reloading = True
            gun_reloading_sound.play()  # 총쏘는 소리 재생
            last_reload_time = pygame.time.get_ticks()  # 재장전 시작 시간 갱신
            
    if is_reloading:
            current_time = pygame.time.get_ticks()
            if current_time - last_reload_time >= reload_time:
                if total_magazines > 0:
                    current_ammo = max_ammo_per_magazine  # 탄창을 새로 채움
                    is_reloading = False  # 재장전 상태 해제
                    
    # 플레이어 감속 (마찰)
    player_speed_x *= friction
    player_speed_y *= friction

    # 플레이어 위치 업데이트
    player_x += player_speed_x
    player_y += player_speed_y


    # 게임 루프에서 마우스 각도 계산
    mouse_x, mouse_y = pygame.mouse.get_pos()
    delta_x = mouse_x - player_x
    delta_y = mouse_y - player_y
    
    angle = math.degrees(math.atan2(delta_y, delta_x))
    sword_range = 200  # 검의 범위를 늘림
    
    if angle < 0:
        angle += 360
        
    # 무기 위치 계산
    if weapon_type == 'handgun':
        weapon_offset_x = 35 * math.cos(math.radians(angle + 90))
        weapon_offset_y = 35 * math.sin(math.radians(angle + 90))
    elif weapon_type == 'magic':
        weapon_offset_x = 0 * math.cos(math.radians(angle + 90))
        weapon_offset_y = 0 * math.sin(math.radians(angle + 90))

    # 무기 위치 업데이트
    weapon_x = player_x + weapon_offset_x
    weapon_y = player_y + weapon_offset_y


    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # 마우스 클릭 시 투사체 발사
        # 투사체 발사 시 위치를 무기 끝으로 조정
        if event.type == pygame.MOUSEBUTTONDOWN:
            current_time = pygame.time.get_ticks()
            
            if is_reloading and current_time - last_reload_time < reload_time:
                continue  # 재장전 중이면 발사할 수 없음
            if weapon_type == 'handgun' : 
                if current_ammo > 0:  # 남은 총알이 있을 때만 발사
                    if current_time - last_shot_time > shoot_delay:
                        # 플레이어의 현재 각도에 따라 투사체 생성
                        projectiles.append(Projectile(weapon_x, weapon_y, angle))  # 무기 끝에서 발사
                        current_ammo -= 1
                        gunshot_sound.play()  # 총쏘는 소리 재생
                        last_shot_time = current_time  # 마지막 발사 시간을 현재 시간으로 갱신
            elif weapon_type == 'sword':
                if current_time - sword_last_swing_time > sword_swing_duration:
                    is_swinging_sword = True
                    sword_last_swing_time = current_time
            elif weapon_type == 'magic':
                if current_time - last_shot_time > shoot_delay:
                    # 발사할 손 결정 (왼손과 오른손 번갈아 가며 발사)
                    target_x, target_y = pygame.mouse.get_pos()
                    angle_to_pointer = math.degrees(math.atan2(target_y - weapon_y, target_x - weapon_x))
                    if hand_select == 0:
                        # 왼손 발사
                        offset_distance = 60 # 손 사이의 거리
                        hand_x = weapon_x - offset_distance * math.cos(math.radians(angle_to_pointer + 90))
                        hand_y = weapon_y - offset_distance * math.sin(math.radians(angle_to_pointer + 90))
                        hand_select = 1
                    else:
                        # 오른손 발사
                        offset_distance = 60  # 손 사이의 거리
                        hand_x = weapon_x + offset_distance * math.cos(math.radians(angle_to_pointer + 90))
                        hand_y = weapon_y + offset_distance * math.sin(math.radians(angle_to_pointer + 90))
                        hand_select= 0
                        
                    # 손에서 발사체 생성
                    projectiles.append(FireProjectile(hand_x, hand_y, pointer_x, pointer_y))
                
                    last_shot_time = current_time
                
    # 화면 경계 처리 및 벽에서 튕김
    if player_x < 37:
        player_x = 37
        player_speed_x = -player_speed_x  # 속도 반전
    if player_x > screen_width - 37:
        player_x = screen_width - 37
        player_speed_x = -player_speed_x  # 속도 반전
    if player_y < 37:
        player_y = 37
        player_speed_y = -player_speed_y  # 속도 반전
    if player_y > screen_height - 37:
        player_y = screen_height - 37
        player_speed_y = -player_speed_y  # 속도 반전

   # 투사체 업데이트
    for projectile in projectiles[:]:
        projectile.update()
        # 투사체가 화면 밖으로 나가면 삭제
        if (projectile.x < 0 or projectile.x > screen_width or
                projectile.y < 0 or projectile.y > screen_height):
            projectiles.remove(projectile)
            continue  # 다음 투사체로 넘어감

        # 투사체와 적 충돌 확인
        for enemy in enemies[:]:
            dist = math.hypot(enemy.x - projectile.x, enemy.y - projectile.y)
            if dist < enemy.radius + projectile.radius :
                enemy.hit(weapon_damage)  # 적의 HP 감소
                
                start_screen_shake()
                
                # 적을 플레이어의 방향으로 밀리게 함
                push_back_strength = 0.8  # 밀리는 힘 조절
                current_angle = math.atan2(enemy.y - player_y, enemy.x - player_x)  # 적과 플레이어 사이의 각도 계산
                enemy.x += math.cos(current_angle) * push_back_strength * 9 / enemy.weight  # 밀려나는 방향으로 이동
                enemy.y += math.sin(current_angle) * push_back_strength * 9 / enemy.weight
                enemy.vx += math.cos(current_angle) * push_back_strength * 7 / enemy.weight # 밀려나는 방향으로 이동
                enemy.vy += math.sin(current_angle) * push_back_strength * 7 / enemy.weight# 밀려나는 방향으로 이동
                
                if isinstance(projectile, FireProjectile):
                    projectile.explode(enemies)  # 불 투사체 폭발
                
                projectile.to_remove = True  # 투사체 삭제 플래그 설정
                break  # 충돌 시 더 이상의 적과의 충돌 확인을 건너뜀

    # 삭제 플래그가 설정된 투사체와 적 제거
    projectiles = [p for p in projectiles if not p.to_remove]
    enemies = [e for e in enemies if e.hp > 0]
    
    # 적과 검의 충돌 확인 (검이 휘두를 때만 적용)
    if is_swinging_sword:
        for enemy in enemies[:]:
            dist = math.hypot(enemy.x - player_x, enemy.y - player_y)
            if dist < 100:  # 검의 범위 내에 적이 있을 때
                enemy.hit()  # 적에게 데미지
                # 적을 밀어내는 로직 추가 가능
            # 적을 플레이어의 방향으로 밀리게 함
                push_back_strength = 0.8  # 밀리는 힘 조절
                current_angle = math.atan2(enemy.y - player_y, enemy.x - player_x)  # 적과 플레이어 사이의 각도 계산
                enemy.x += math.cos(current_angle) * push_back_strength * 9 / enemy.weight  # 밀려나는 방향으로 이동
                enemy.y += math.sin(current_angle) * push_back_strength * 9 / enemy.weight
                enemy.vx += math.cos(current_angle) * push_back_strength * 7 / enemy.weight # 밀려나는 방향으로 이동
                enemy.vy += math.sin(current_angle) * push_back_strength * 7 / enemy.weight# 밀려나는 방향으로 이동

                projectiles.remove(projectile)  # 투사체 삭제
                if enemy.hp <= 0:
                    enemies.remove(enemy)  # 적을 제거
                break  # 충돌 시 더 이상의 적과의 충돌 확인을 건너뜀

        # 적과 충돌 체크
        for enemy in enemies[:]:
            dist = math.hypot(enemy.x - sword_x, enemy.y - sword_y)
            if dist < sword_range:  # 검의 범위 내에 적이 있을 때
                enemy.hit()  # 적에게 데미지
                start_screen_shake()
                # 밀리는 로직 추가
                push_back_strength = 0.8  # 밀리는 힘 조절
                current_angle = math.atan2(enemy.y - player_y, enemy.x - player_x)
                enemy.x += math.cos(current_angle) * push_back_strength * 9 / enemy.weight
                enemy.y += math.sin(current_angle) * push_back_strength * 9 / enemy.weight
                if enemy.hp <= 0:
                    enemies.remove(enemy)
                break  # 충돌 시 더 이상의 적과의 충돌 확인을 건너뜀

    # 일정 시간이 지나면 휘두르기 중지
    if pygame.time.get_ticks() - sword_last_swing_time > sword_swing_duration:
        is_swinging_sword = False
    
    # 적 업데이트 및 생성
    current_time = pygame.time.get_ticks()
    # 적 생성 경고 및 생성 딜레이
    if enemy_spawn_warning_time is None and current_time - last_enemy_spawn_time > enemy_spawn_delay:
        # 적이 생성될 좌표를 미리 정함 (이 좌표는 경고 이미지와 적 생성에 동일하게 사용)
        new_enemy_x = random.randint(50, screen_width - 50)
        new_enemy_y = random.randint(50, screen_height - 50)
        enemy_spawn_warning_time = current_time  # 경고 표시 시작 시간을 현재 시간으로 설정

    # 경고 시간이 지나면 적을 생성
    if enemy_spawn_warning_time and current_time - enemy_spawn_warning_time >= enemy_warning_time:
        # 경고가 표시된 위치에 적을 생성하고 적 리스트에 추가
        new_enemy = spawn_random_enemy()
        new_enemy.x = new_enemy_x  # 경고 이미지와 동일한 x 좌표
        new_enemy.y = new_enemy_y  # 경고 이미지와 동일한 y 좌표
        enemies.append(new_enemy)  # 적을 리스트에 추가
        enemy_spawn_warning_time = None
        last_enemy_spawn_time = current_time

    # 적 생성 경고 표시
    if enemy_spawn_warning_time and current_time - enemy_spawn_warning_time < enemy_warning_time:
        # 경고 이미지 표시 (미리 정한 좌표에 표시)
        screen.blit(warning_image, (new_enemy_x - 37, new_enemy_y - 37))

        
    for enemy in enemies:
        enemy.follow_player(player_x, player_y)  # 적이 플레이어를 따라가게 함

    #플레이어와 적과의 충돌 확인
    for enemy in enemies[:]:
        dist = math.hypot(enemy.x - player_x, enemy.y - player_y)
        if dist < enemy.radius + 50:  # 플레이어의 반지름
            player_hp -= enemy.damage  # 플레이어 HP 감소
            damage_texts.append(DamageText(player_x, player_y, enemy.damage))

            # 플레이어와 적 모두 밀리게 함
            push_back_strength = 0.8  # 밀리는 힘 조절 (기존 0.3에서 증가)

            # 플레이어 밀리기
            player_angle = math.atan2(player_y - enemy.y, player_x - enemy.x)  # 플레이어와 적의 각도
            player_speed_x += math.cos(player_angle) * push_back_strength * 5  # 플레이어를 밀어냄
            player_speed_y += math.sin(player_angle) * push_back_strength * 5  # 플레이어를 밀어냄

            # 적 밀리기
            enemy_angle = math.atan2(enemy.y - player_y, enemy.x - player_x)  # 적과 플레이어의 각도
            enemy.speed = 2  # 적의 밀려나는 속도 (기존 2에서 감소)
            enemy.x += math.cos(enemy_angle) * push_back_strength * enemy.speed * 50 / enemy.weight # 적을 밀어냄
            enemy.y += math.sin(enemy_angle) * push_back_strength * enemy.speed * 50  / enemy.weight# 적을 밀어냄
            enemy.vx += math.cos(enemy_angle) * push_back_strength * enemy.speed * 17 / enemy.weight # 적을 밀어냄
            enemy.vy += math.sin(enemy_angle) * push_back_strength * enemy.speed * 17  / enemy.weight# 적을 밀어냄
            
        # 예시: 플레이어가 적을 공격했을 때
        
    for damage_text in damage_texts[:]:
        if not damage_text.draw(screen, font):
            damage_texts.remove(damage_text)  # 텍스트가 만료되면 리스트에서 제거

    # 게임 오버 체크
    if player_hp <= 0:
        running = False
        
    # 투사체 그리기
    for projectile in projectiles:
        projectile.draw(screen)

    # 적 그리기
    for enemy in enemies:
        enemy.draw(screen)
        
    if weapon_type == 'handgun':
           # 무기 회전 및 그리기
        rotated_weapon = pygame.transform.rotate(handgun_image, -angle - 90)
        weapon_rect = rotated_weapon.get_rect(center=(weapon_x+ shake_offset_x, weapon_y+ shake_offset_y))
        screen.blit(rotated_weapon, weapon_rect.topleft)
        
    # 플레이어 회전 및 그리기
    rotated_player = pygame.transform.rotate(player_image, -angle - 90)
    player_rect = rotated_player.get_rect(center=(player_x + shake_offset_x, player_y + shake_offset_y))
    screen.blit(rotated_player, player_rect.topleft)

    

    # 적 생성 경고 표시
  #  if enemy_spawn_warning_time and current_time - enemy_spawn_warning_time < 2000:  # 2초 동안 표시
   #     pygame.draw.rect(screen, WARNING_COLOR, (new_enemy_x - 15, new_enemy_y - 30, 50, 50))  # 적 생성 경고 사각형
    # 화면에 남은 탄창 수와 총알 수를 표시
    if is_reloading:
        ammo_text = ammo_font.render("재장전 중", True, WHITE)
        screen.blit(ammo_text, (player_x - 60 + shake_offset_x, player_y + shake_offset_y + 55))  # 플레이어 하단에 표시
    else:
        ammo_text = ammo_font.render(f"{current_ammo}/{max_ammo_per_magazine}", True, WHITE)
        screen.blit(ammo_text, (player_x - 48 + shake_offset_x, player_y + shake_offset_y + 55))  # 플레이어 하단에 표시
        # 체력바 그리기
    player_hp_bar_width = 180
    player_hp_bar_height = 25
        
    level_text = font.render(f"Lv. {player_level}", True, (255, 255, 255))  # 플레이어 레벨 텍스트 생성
    screen.blit(level_text, (player_x - player_hp_bar_width // 2 + (player_hp_bar_width - level_text.get_width()) // 2, player_y - 120))  # 체력바 왼쪽에 표시
    
    pygame.draw.rect(screen, (0, 0, 0), (player_x - player_hp_bar_width // 2, player_y - 85 + shake_offset_y, player_hp_bar_width, player_hp_bar_height))  # 플레이어 HP 바 배경
    pygame.draw.rect(screen, (255, 0, 0), (player_x - player_hp_bar_width // 2, player_y - 85 + shake_offset_y, player_hp_bar_width * (player_hp / player_Maxhp), player_hp_bar_height))  # 플레이어 체력

    # 플레이어 HP 텍스트 표시
    player_hp_text = font.render(f"{int(player_hp)}/{int(player_Maxhp)}", True, (255, 255, 255))  # 텍스트 생성
    screen.blit(player_hp_text, (player_x - player_hp_bar_width // 2 + (player_hp_bar_width - player_hp_text.get_width()) // 2, player_y - 89))  # 텍스트 위치
    
    experience_bar_width = player_hp_bar_width  # 체력바와 같은 너비로 설정
    experience_bar_height = 4  # 얇은 바 설정

    # 경험치 바 배경
    pygame.draw.rect(screen, (0, 0, 0), (player_x - experience_bar_width // 2, player_y - 85 + player_hp_bar_height , experience_bar_width, experience_bar_height))

    # 현재 경험치 표시
    pygame.draw.rect(screen, (0, 255, 150), (player_x - experience_bar_width // 2, player_y - 85 + player_hp_bar_height , experience_bar_width * (player_experience / experience_to_level_up), experience_bar_height))

    for enemy in enemies:
        enemy_hp_bar_width = player_hp_bar_width  # 적 HP 바의 너비를 플레이어와 동일하게 설정
        enemy_hp_bar_height = 25
        pygame.draw.rect(screen, (0, 0, 0), (enemy.x - enemy_hp_bar_width // 2, enemy.y - 85+ shake_offset_y, enemy_hp_bar_width, enemy_hp_bar_height))  # 적 HP 바 배경
        pygame.draw.rect(screen, (0, 0, 255), (enemy.x - enemy_hp_bar_width // 2, enemy.y - 85+ shake_offset_y, enemy_hp_bar_width * (enemy.hp / enemy.Maxhp), enemy_hp_bar_height))  # 적 체력

        # 적 HP 텍스트 표시
        enemy_hp_text = font.render(f"{int(enemy.hp)}/{enemy.Maxhp}", True, (255, 255, 255))  # 텍스트 생성
        screen.blit(enemy_hp_text, (enemy.x - enemy_hp_bar_width // 2 + (enemy_hp_bar_width - enemy_hp_text.get_width()) // 2, enemy.y - 89))  # 텍스트 위치
    
    # 대미지 텍스트 업데이트 및 그리기
    for damage_text in damage_texts[:]:
        if not damage_text.draw(screen, damage_font):  # 텍스트를 화면에 그리기
            damage_texts.remove(damage_text)  # 지속 시간이 끝난 텍스트 삭제
            
    if weapon_type == 'magic':
        rotated_pointer = pygame.transform.rotate(big_pointer_image, -angle - 90)
        pointer_offset_x = 0 * math.cos(math.radians(angle + 90))
        pointer_offset_y = 0 * math.sin(math.radians(angle + 90))
    else:
        rotated_pointer = pygame.transform.rotate(pointer_image, -angle - 90)
        pointer_offset_x = 35 * math.cos(math.radians(angle + 90))
        pointer_offset_y = 35 * math.sin(math.radians(angle + 90))

    # 조준점 위치 업데이트
    pointer_x = mouse_x + pointer_offset_x
    pointer_y = mouse_y + pointer_offset_y
    
    pointer_rect = rotated_pointer.get_rect(center=(pointer_x , pointer_y ))
    screen.blit(rotated_pointer, pointer_rect.topleft)
      # 조준점
    if event.type == pygame.MOUSEBUTTONDOWN:
        screen.blit(big_pointer_image, (pointer_x - 90, pointer_y - 90))
    
    pygame.display.flip()  # 화면 업데이트
    pygame.time.delay(30)  # FPS 

# 게임 오버 화면
print("Game Over!")
pygame.quit()
