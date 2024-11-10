import pygame
import sys
import math
import random
import shutil
import time

# Pygame 초기화
pygame.init()
pygame.mixer.init()

FPS = 30  # 목표 프레임 속도 설정
# 폰트 설정
menu_font = pygame.font.Font('C:/Users/User/Desktop/startcoding/NeoDunggeunmoPro-Regular.ttf', 80)

# 화면 크기 설정
screen_width = 1920
screen_height = 1000
screen = pygame.display.set_mode((screen_width, screen_height), pygame.DOUBLEBUF)
pygame.display.set_caption('Pygame Player with Enemies')

#총 소리
gunshot_sound = pygame.mixer.Sound("gunshot_sound.mp3")
gun_reloading_sound = pygame.mixer.Sound("gun_reloading.mp3")

#불 마법 발사 소리
fire_sound = pygame.mixer.Sound("C:/Users/User/Desktop/startcoding/fire.mp3")
explosion_sound = pygame.mixer.Sound("C:/Users/User/Desktop/startcoding/펑.mp3")

shutil.copy("C:/Users/User/Desktop/startcoding/bow sound.mp3", ".")

#화살 발사 소리
bow_sound = pygame.mixer.Sound("bow sound.mp3")

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
Lime_Green = (50, 205, 50)

# 화면 진동 설정
shake_duration = 140 # 진동 지속 시간 (밀리초)
shake_magnitude = 3 # 진동의 강도 (화면이 흔들리는 범위)
shake_start_time = None  # 진동 시작 시간

#활 이미지
bow_image = pygame.image.load('C:/Users/User/Desktop/startcoding/bow.png')
bow_image = pygame.transform.scale(bow_image, (186, 225))

#화살 이미지
arrow_image = pygame.image.load('C:/Users/User/Desktop/startcoding/arrow.png')
arrow_image = pygame.transform.scale(arrow_image, (14, 106))

#불 이미지
fire_image = pygame.image.load('C:/Users/User/Desktop/startcoding/fire.png')
fire_image = pygame.transform.scale(fire_image, (37, 51))

#총알 이미지
bullet_image = pygame.image.load('C:/Users/User/Desktop/startcoding/bullet.png')
bullet_image = pygame.transform.scale(bullet_image, (15, 32))

#돌 이미지
stone_image = pygame.image.load('C:/Users/User/Desktop/startcoding/stone.png')
stone_image = pygame.transform.scale(stone_image, (40, 40))

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
acceleration = 0.54  # 가속도
friction = 0.97  # 마찰(감속 비율)
projectile_speed = 55  # 투사체 속도
player_Maxhp = 150
player_hp = 150  # 플레이어 HP

enemy_image = pygame.image.load('C:/Users/User/Desktop/startcoding/zombie.png')  # 적 이미지 파일
enemy_image = pygame.transform.scale(enemy_image, (75, 75))  # 적 이미지 크기 조정

fast_enemy_image = pygame.image.load('C:/Users/User/Desktop/startcoding/fast zombie.png')  # 적 이미지 파일
fast_enemy_image = pygame.transform.scale(fast_enemy_image, (75, 75))  # 적 이미지 크기 조정

giant_enemy_image = pygame.image.load('C:/Users/User/Desktop/startcoding/giant zombie.png')  # 적 이미지 파일
giant_enemy_image = pygame.transform.scale(giant_enemy_image, (100, 100))  # 적 이미지 크기 조정

invisible_enemy_image = pygame.image.load('C:/Users/User/Desktop/startcoding/invisible zombie.png')  # 적 이미지 파일
invisible_enemy_image = pygame.transform.scale(invisible_enemy_image, (75, 75))  # 적 이미지 크기 f

flash_enemy_image = pygame.image.load('C:/Users/User/Desktop/startcoding/flash zombie.png')  # 적 이미지 파일
flash_enemy_image = pygame.transform.scale(flash_enemy_image, (75, 75))  # 적 이미지 크기 조정

stone_enemy_image = pygame.image.load('C:/Users/User/Desktop/startcoding/stone zombie.png')  # 적 이미지 파일
stone_enemy_image = pygame.transform.scale(stone_enemy_image, (90, 90))  # 적 이미지 크기 조정

titan_image = pygame.image.load('C:/Users/User/Desktop/startcoding/titan.png')  # 적 이미지 파일
titan_image = pygame.transform.scale(titan_image, (100, 100))  # 적 이미지 크기 조정

suicide_enemy_image = pygame.image.load('C:/Users/User/Desktop/startcoding/suicide zombie.png')  # 적 이미지 파일
suicide_enemy_image = pygame.transform.scale(suicide_enemy_image, (75, 75))  # 적 이미지 크기 조정

mutant_enemy_image = pygame.image.load('C:/Users/User/Desktop/startcoding/mutant zombie.png')  # 적 이미지 파일
mutant_enemy_image = pygame.transform.scale(mutant_enemy_image, (75, 75))  # 적 이미지 크기 조정

#적 이미지 지정
enemy_imagenumber = [enemy_image, fast_enemy_image, giant_enemy_image, invisible_enemy_image,flash_enemy_image, stone_enemy_image,titan_image, suicide_enemy_image, mutant_enemy_image]
enemy_images = [enemy_image, fast_enemy_image, giant_enemy_image, invisible_enemy_image,flash_enemy_image, stone_enemy_image,titan_image, suicide_enemy_image, mutant_enemy_image]

mouse_clicked = False

'''def spawn_enemy(enemy_type, position, exp_reward):
    """적 유형에 따라 적을 생성하는 함수"""
    if enemy_type == enemy_images[0]:  # 일반 적
        enemy = NormalEnemy(position[0], position[1])
    elif enemy_type == enemy_images[1]:  # 빠른 적
        enemy = FastEnemy(position[0], position[1])
    elif enemy_type == enemy_images[2]:  # 거대 적
        enemy = StrongEnemy(position[0], position[1])
    elif enemy_type == enemy_images[3]:  # 투명 적
        enemy = InvisibleEnemy(position[0], position[1])
    else:
        enemy = NormalEnemy(position[0], position[1])
enemy_warning_time = 1500
                enemy_spawn_delay = 2000
    enemy.image = enemy_type  # 적 이미지 설정
    return enemy'''

# 화면 깜빡임 설정
damage_flash_duration = 200  # 깜빡임 지속 시간 (밀리초)
damage_flash_timer = 0  # 현재 깜빡임 타이머

# 플레이어가 공격받을 때 호출되는 함수
def player_take_damage():
    global damage_flash_timer
    damage_flash_timer = damage_flash_duration

# 화면 업데이트 함수 수정
def update_screen():
    # 기존 화면 그리기 로직 ...

    # 빨간색 깜빡임 효과 적용
    if damage_flash_timer > 0:
        flash_surface = pygame.Surface(screen.get_size())
        flash_surface.fill((255, 0, 0))  
        flash_surface.set_alpha(78)  
        screen.blit(flash_surface, (0, 0))
        
# 함수: 화면 진동 시작
def start_screen_shake():
    global shake_start_time
    shake_start_time = pygame.time.get_ticks()  # 진동 시작 시간 기록

def reset_game():
    global player_x, player_y, player_hp, enemies, projectiles, current_ammo, total_magazines, is_reloading, start_time, wave,enemy_spawn_warning_time,experience_to_level_up
    global player_experience, player_level, player_Maxhp, damage_up, last_enemy_spawn_time, enemy_spawn_delay , enemy_warning_time, player_speed_x, player_speed_y,wave_start_time, wave_duration, last_skill_use_time

    # 플레이어 위치 및 상태 초기화
    player_x, player_y = screen_width // 2, screen_height // 2
    player_speed_x = 0
    player_speed_y = 0
    start_time = time.time()
    wave_start_time = pygame.time.get_ticks()
    player_Maxhp = 150
    player_hp = player_Maxhp
    player_experience = 0
    player_level = 1
    damage_up = 1.0
    experience_to_level_up = 100
    enemy_warning_time = 1500
    enemy_spawn_delay = 2000
    wave = 1
    last_enemy_spawn_time = 0
    enemy_spawn_warning_time = None
    wave_duration = 20000

    # 적과 투사체 초기화
    enemies.clear()
    projectiles.clear()
    enemy_projectiles.clear()
    current_ammo = max_ammo_per_magazine
    total_magazines = 5
    is_reloading = False
    
    # 특수 스킬 쿨타임 초기화
    current_time = pygame.time.get_ticks()
    last_skill_use_time = {
        weapon: current_time - skill_data["cooldown"]
        for weapon, skill_data in weapon_special_skills.items()
    }
    #last_enemy_spawn_time = pygame.time.get_ticks()  # 적 생성 시간 초기화
    
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

def reset_wave():
    global wave_start_time
    # 웨이브 관련 변수 초기화
    wave_start_time = pygame.time.get_ticks()  # 웨이브 시작 시간 갱신
    
# 무기별 특수 스킬 설정
weapon_special_skills = {
    "bow": {"cooldown": 4000, "damage": 50, "radius": 50, "skill": "multi_arrow"},
    "handgun": {"cooldown": 6000, "damage": 200, "radius": 0, "skill": "rapid_fire"},
    "magic": {"cooldown": 10000, "damage": 100, "radius": 150, "skill": "fire_blast"},
}

# 게임 시작 시간 초기화
game_start_time = pygame.time.get_ticks()
is_rapid_firing = False
rapid_fire_end_time = 0  # 연속 발사 종료 시간

last_skill_use_time = {
    weapon: game_start_time - skill_data["cooldown"]
    for weapon, skill_data in weapon_special_skills.items()
}

def use_special_skill(weapon_type, weapon_x, weapon_y, angle):
    global last_skill_use_time, is_rapid_firing, rapid_fire_end_time, current_ammo
    current_time = pygame.time.get_ticks()
    skill_data = weapon_special_skills.get(weapon_type, None)

    # 무기 타입별로 특수 스킬이 없을 경우
    if skill_data is None:
        return

    # 스킬 쿨타임 검사
    if current_time - last_skill_use_time[weapon_type] >= skill_data["cooldown"]:
        last_skill_use_time[weapon_type] = current_time  # 쿨타임 초기화

        # 무기별 스킬 발동
        if skill_data["skill"] == "multi_arrow":
            # 다중 화살 발사 (활)
            projectiles.append(Arrow(weapon_x, weapon_y, angle - 20))
            bow_sound.play()
            projectiles.append(Arrow(weapon_x, weapon_y, angle - 10))
            bow_sound.play()
            projectiles.append(Arrow(weapon_x, weapon_y, angle))
            bow_sound.play()
            projectiles.append(Arrow(weapon_x, weapon_y, angle + 10))
            bow_sound.play()
            projectiles.append(Arrow(weapon_x, weapon_y, angle + 20))
            bow_sound.play()

        elif skill_data["skill"] == "rapid_fire":
            # 남은 총알을 빠르게 발사
            is_rapid_firing = True
            rapid_fire_end_time = current_time + 1000  # 연속 발사 1초 지속

        elif skill_data["skill"] == "fire_blast":
            # 넓은 범위 불 마법 (마법)
            pygame.draw.circle(screen, (255, 69, 0), (player_x, player_y), skill_data["radius"], 0)
            for enemy in enemies:
                if math.hypot(enemy.x - player_x, enemy.y - player_y) <= skill_data["radius"]:
                    enemy.hit(skill_data["damage"])
                    
# Damage Text 클래스
class DamageText:
    def __init__(self, x, y, damage):
        self.x = x + random.choice([random.randint(-70, -50), random.randint(50, 70)]) - 50 
        self.y = y + random.choice([random.randint(-70, -50), random.randint(50, 70)]) - 75 
        self.damage = damage
        self.lifetime = 250  
        self.hold_time = 220
        self.start_time = pygame.time.get_ticks()
        self.initial_font_size = 50  # 초기 폰트 크기

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
            font = pygame.font.Font('NeoDunggeunmoPro-Regular.ttf', font_size)
            damage_text = font.render(str(int(self.damage)), True, (0, 0, 0))
            screen.blit(damage_text, (self.x, self.y))
            return True
        return False

damage_texts = []

def apply_damage(target, damage, color):
    damage_texts.append(DamageText(target.x, target.y, damage, color))  # 대미지 텍스트 생성

player_experience = 0
experience_to_level_up = 100
player_level = 1
damage_up = 1

crosses = []
last_cross_time = 0
cross_delay = 25  # 25ms 간격으로 십자가 생성
cross_spawn_times = []

# 회복 함수
def heal_player(healing_amount):
    global player_hp
    if player_hp < player_Maxhp:
        player_hp += healing_amount
    if player_hp > player_Maxhp:
        player_hp = player_Maxhp

    # 나머지 십자가 생성 시간 기록
    current_time = pygame.time.get_ticks()
    for i in range(13):
        cross_spawn_times.append(current_time + i * cross_delay)

# 회복 효과 함수 (초록 십자가)
def draw_heal_effect():
    offset_x = random.randint(-40, 80)
    offset_y = random.randint(-40, 80)
    cross_pos = (player_x + offset_x, player_y + offset_y)
    crosses.append({"pos": cross_pos, "transparency": 255, "cross_size": 75})  # 초기 투명도 255, 크기 75으로 저장      

# 레벨업 텍스트 표시 시간과 레벨업 여부 확인용 변수
level_up_display_time = 1500  # 2초 동안 표시
last_level_up_time = None
      
# 경험치 추가 함수
def add_experience(amount):
    global player_experience, player_level, experience_to_level_up, player_hp, player_Maxhp, weapon_damage, damage_up, last_level_up_time, weapon_type
    player_experience += amount
    if player_experience >= experience_to_level_up:
        player_experience -= experience_to_level_up
        player_level += 1
        experience_to_level_up = int(experience_to_level_up * 1.5)  # 레벨업 시 필요한 경험치 증가
        last_level_up_time = pygame.time.get_ticks() # 레벨업 시간을 기록
        print(last_level_up_time)
        player_Maxhp *= 1.1
        heal_player(int(player_Maxhp / 10))  
        damage_up *= 1.1
        
        # 레벨에 따른 무기 변경
        if player_level < 3:
            weapon_type = 'bow'
        elif player_level < 6:
            weapon_type = 'handgun'
        else:
            weapon_type = 'magic'
        
# 적 클래스
class Enemy:
    def __init__(self, x, y, hp, speed, size, number, enemy_weight, damage):
        self.x = x
        self.y = y
        self.hp = hp
        self.Maxhp = hp
        self.radius = size  # 적의 크기
        self.speed = speed *1.5 # 적의 기본 속도
        self.base_speed = speed * 1.5# base_speed 추가
        self.weight = enemy_weight  #무게(밀려나는 정도)
        self.damage = damage #공격력
        self.color = (0, 0, 0)  # 적의 색상
        self.angle = math.atan2(player_y - self.y, player_x - self.x)
        self.vx = 0
        self.vy = 0
        self.knockback_vx, self.knockback_vy = 0, 0  # 밀려나는 속도 초기화
        self.num = number
        self.invisible = False
        
    def draw(self, screen):
        if not getattr(self, 'invisible', False):
            angle = math.degrees(math.atan2(player_y - self.y, player_x - self.x))
            rotated_enemy = pygame.transform.rotate(enemy_imagenumber[self.num], -angle)  # 적 이미지를 회전
            enemy_rect = rotated_enemy.get_rect(center=(self.x + shake_offset_x, self.y + shake_offset_y))
            screen.blit(rotated_enemy, enemy_rect.topleft) 
        
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
            self.speed = self.base_speed * 6  # 가까이 있을 때 속도 증가
        else:
            self.speed = self.base_speed

        if abs(self.knockback_vx) > 0.01 and abs(self.knockback_vy) > 0.01 :
            # 밀려나는 효과가 남아있는 동안 감속만 적용
            self.x += self.knockback_vx
            self.y += self.knockback_vy
            self.knockback_vx *= self.knockback_friction
            self.knockback_vy *= self.knockback_friction
            return  # 밀려나는 동안은 플레이어를 추적하지 않음

        # 플레이어를 향한 기본 이동 로직 (밀려나지 않는 경우)
        self.angle = math.atan2(player_y - self.y, player_x - self.x)
        self.vx = self.base_speed * math.cos(self.angle)
        self.vy = self.base_speed * math.sin(self.angle)
        
        # 위치 업데이트
        self.x += self.vx
        self.y += self.vy
        
    def apply_knockback(self, force, angle):
        # 밀려나는 초기 속도 설정
        initial_knockback_speed = (6 + force) / self.weight  # 초기 속도를 높게 설정하여 빠르게 밀려나게 함
        self.knockback_vx = initial_knockback_speed * math.cos(angle)
        self.knockback_vy = initial_knockback_speed * math.sin(angle)
        
        # 감속 비율을 강하게 적용하여 짧은 시간에 멈추도록 설정
        self.knockback_friction = 0.3  # 감속 비율을 강하게 설정하여 빠르게 줄어들게 함

#숫자 : 체력, 속도, 크기(반지름), 번호,무게, 공격력

class MutantEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, 750, 6, 37, 8, 1, 35)
        self.exp_reward = 270
        self.area_damage_radius = 175  # 장판의 반지름
        self.last_area_time = pygame.time.get_ticks()  # 마지막 장판 생성 시간
        self.area_duration = 4500  # 장판이 유지되는 시간 (밀리초)
        self.area_active = False
        self.area_position = None  # 장판 위치

    def create_area_damage(self):
        current_time = pygame.time.get_ticks() + 2500

        if current_time - self.last_area_time >= 5000:
            self.area_active = True
            self.last_area_time = current_time
            self.area_position = (int(self.x), int(self.y))  # 장판 위치 고정
            
    def update(self):
        global player_hp
        # 3초마다 장판 생성
        self.create_area_damage()

        # 장판이 활성화되면 고정된 위치에 장판을 그리기
        if self.area_active and self.area_position:
            area_surface = pygame.Surface((self.area_damage_radius * 2, self.area_damage_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(area_surface, (50, 205, 50, 128), (self.area_damage_radius, self.area_damage_radius), self.area_damage_radius)

            # 화면에 장판 서피스를 그리기
            screen.blit(area_surface, (self.area_position[0] - self.area_damage_radius, self.area_position[1] - self.area_damage_radius))

             # 플레이어가 장판 안에 있으면 피해를 입힘
            if math.hypot(player_x - self.area_position[0], player_y - self.area_position[1]) <= self.area_damage_radius:
                player_hp -= 1
                player_take_damage()  # 플레이어에게 피해를 입힘

            # 장판이 생성된 지 3초가 지나면 비활성화
            if pygame.time.get_ticks() - self.last_area_time >= self.area_duration:
                self.area_active = False
                self.area_position = None  # 장판 위치 초기화
    
# 자폭 적 클래스
class SuicideEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, 350, 9, 37, 7, 1.25, 60) 
        self.exp_reward = 200
    
    def explode(self):
        # 폭발 시 대미지 적용
        pygame.draw.circle(screen, (128, 0, 128), (self.x, self.y), 150)
        # 적 제거
        enemies.remove(self)
        
    def update(self):
        pass  # 빈 update 메서드
        
# 타이탄 클래스
class Titan(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, 1250, 3.5, 50, 6, 1.75, 80)  
        self.exp_reward = 225
        
    def update(self):
        pass  # 빈 update 메서드
    
# 돌 던지는 적 클래스
class StoneEnemy(Enemy):  # Enemy 클래스를 상속받음
    def __init__(self, x, y):
        super().__init__(x, y, 500, 5, 37, 5, 1, 25)
        self.exp_reward = 170
        self.throw_delay = 2000  # 돌 던지기 딜레이 (초)
        self.last_throw_time = pygame.time.get_ticks()  # 마지막 돌 던진 시간 초기화

    def throw_stone(self, player_x, player_y):
        current_time = pygame.time.get_ticks()
        distance = math.hypot(player_x - self.x, player_y - self.y)

        # 던지기 조건 확인 후 돌 생성
        if distance <= 1000 and current_time - self.last_throw_time >= self.throw_delay:
            stone_speed = 40  # 돌의 속도 설정
            stone_angle = math.atan2(player_y - self.y, player_x - self.x)
            stone_vx = stone_speed * math.cos(stone_angle)
            stone_vy = stone_speed * math.sin(stone_angle)

            # Stone 객체를 생성하여 enemy_projectiles에 추가 (속도를 직접 전달)
            enemy_projectiles.append(Stone(self.x, self.y, stone_vx, stone_vy))
            self.last_throw_time = current_time

    def update(self):
        self.throw_stone(player_x, player_y)
        
enemy_projectiles = []       
# 점멸 적 클래스
class FlashEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, 450, 6, 37, 4, 1, 30)
        self.exp_reward = 135
        self.invisible = False
        self.last_toggle_time = time.time()
        self.alpha = 255
        self.x = x
        self.y = y
        self.last_teleport_time = pygame.time.get_ticks()  # 마지막 순간이동 시간을 기록
        
    def teleport_toward_player(self, player_x, player_y):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_teleport_time >= random.randint(400,800): 
            # 플레이어 방향으로 각도 계산
            angle = math.atan2(player_y - self.y, player_x - self.x)
            # 각도에 따라 100만큼 이동
            self.x += random.randint(-50,150) * math.cos(angle)
            self.y += random.randint(-50,150) * math.sin(angle)
            # 순간이동 시간 갱신
            self.last_teleport_time = current_time
            
    def update(self):
        self.teleport_toward_player(player_x, player_y)
            
# 은신 적 클래스
class InvisibleEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, 300, 7, 37, 3, 1, 25)
        self.exp_reward = 100
        self.invisible = False
        self.last_toggle_time = time.time()
        self.invisible_duration = 2.5
        self.visible_duration = 2
        self.alpha = 255

    def update(self):
        current_time = time.time()
        elapsed_time = current_time - self.last_toggle_time

        if self.invisible and elapsed_time > self.invisible_duration:
            self.invisible = False
            self.alpha = 255
            self.last_toggle_time = current_time
        elif not self.invisible and elapsed_time > self.visible_duration:
            self.invisible = True
            self.alpha = 255
            self.last_toggle_time = current_time

        if self.invisible:
            self.alpha = max(0, self.alpha - 20)  # 점진적 투명화

    def draw(self, screen):
        if self.alpha > 0:
            enemy_image = enemy_imagenumber[self.num].copy()
            enemy_image.set_alpha(self.alpha)
            angle = math.degrees(math.atan2(player_y - self.y, player_x - self.x))
            rotated_enemy = pygame.transform.rotate(enemy_image, -angle)
            enemy_rect = rotated_enemy.get_rect(center=(self.x, self.y))
            screen.blit(rotated_enemy, enemy_rect.topleft)


    
# 강력한 적 클래스
class StrongEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, 500, 4, 50, 2, 1.5, 40)  # 큰 적
        self.exp_reward = 50
        
    def update(self):
        pass  # 빈 update 메서드
    
# 빠른 적 클래스
class FastEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, 100, 9, 37, 1, 1, 20)  # 빠른 적
        self.exp_reward = 30
        
    def update(self):
        pass  # 빈 update 메서드
# 일반 적 클래스
class NormalEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, 150, 5, 37, 0, 1, 10)  # 일반 적
        self.exp_reward = 20
        
    def update(self):
        pass  # 빈 update 메서드

start_time = time.time()

# 웨이브 관련 변수
wave_duration = 20000  # 웨이브의 총 지속 시간 (밀리초 단위)
wave_start_time = pygame.time.get_ticks()  # 웨이브 시작 시간

# 랜덤으로 적을 생성하는 함수
def spawn_random_enemy(number):
    x = random.randint(50, screen_width - 50)
    y = random.randint(50, screen_height - 50)
    
    enemy_type = number
    return enemy_type(x, y)

# 적 리스트
enemies = []
enemy_spawn_delay = 3000
last_enemy_spawn_time = pygame.time.get_ticks()

# 투사체 발사 딜레이 설정
shoot_delay = 200  # 밀리초
last_shot_time = pygame.time.get_ticks()  # 마지막으로 발사된 시간

# 플레이어가 검을 휘두를 때를 위한 변수 설정
is_swinging_sword = False
sword_swing_duration = 300  # 휘두르는 시간 (밀리초)
sword_last_swing_time = 0  # 마지막 휘두른 시간

# 돌 클래스
class Stone:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.speed = 40
        self.radius = 20
        self.to_remove = False 
        
    def update(self):
        # x와 y 좌표를 속도에 따라 업데이트하여 이동시킴
        self.x += self.vx
        self.y += self.vy

    def draw(self, screen):
        screen.blit(stone_image, (self.x, self.y))  # 화면에 그리기

# 화살 클래스
class Arrow:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = projectile_speed
        self.radius = 15
        self.to_remove = False 

    def update(self):
        # 투사체의 방향에 따라 위치 업데이트
        self.x += self.speed * math.cos(math.radians(self.angle))
        self.y += self.speed * math.sin(math.radians(self.angle))

    def draw(self, screen):
        # 무기 회전 및 그리기
        rotated_arrow = pygame.transform.rotate((arrow_image), -self.angle - 90)  # 투사체 회전  
        arrow_rect = rotated_arrow.get_rect(center=(self.x+ shake_offset_x, self.y+ shake_offset_y))
        screen.blit(rotated_arrow, arrow_rect.topleft)  # 화면에 그리기
        
# 총알 클래스
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
        rotated_projectile = pygame.transform.rotate((bullet_image), -self.angle - 90)  # 투사체 회전  
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
        self.explosion_radius = 200  # 폭발 반경
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
        explosion_sound.play()
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
current_warnings = []  # 경고 리스트ssss
enemy_spawn_time = pygame.time.get_ticks()  # 적 생성 시간
# 적 생성 경고 시간과 딜레이 설정
enemy_warning_time = 1500  # 경고를 미리 표시할 시간 (밀리초)
enemy_spawn_delay = 1000  # 적 생성 간격 (밀리초)
enemy_spawn_warning_time = None  # 생성 경고를 표시할 시간 변수
last_enemy_spawn_time = pygame.time.get_ticks()
new_enemy_x = None  # 적이 생성될 x 좌표
new_enemy_y = None  # 적이 생성될 y 좌표
wave = 1

# 총알 관련 변수
max_ammo_per_magazine = 20  # 한 탄창당 최대 총알 수
current_ammo = max_ammo_per_magazine  # 현재 탄창의 총알 수
total_magazines = 5  # 가지고 있는 탄창 수
reload_time = 1100  # 재장전 시간 (밀리초)
is_reloading = False  # 재장전 상태인지 확인
last_reload_time = 0  # 마지막 재장전 시간

#마법 관련 변수
hand_select = 0

# 무기 리스트
weapons = ["Sword", "HandGun", "Magic", "Bow"]
selected_weapon_index = 0

# 메뉴 표시 함수
def draw_menu():
    global selected_weapon_index
    while True:
        screen.fill((0, 0, 100))  # 배경 색상

        # 제목 텍스트
        title_text = menu_font.render("Select Your Weapon", True, (255, 255, 255))
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 100))

        # 무기 리스트 표시
        for i, weapon in enumerate(weapons):
            color = (255, 0, 0) if i == selected_weapon_index else (255, 255, 255)
            weapon_text = menu_font.render(weapon, True, color)
            screen.blit(weapon_text, (screen_width // 2 - weapon_text.get_width() // 2, 300 + i * 150))

        pygame.display.flip()

        # 이벤트 처리
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
                    return weapons[selected_weapon_index]  # 선택된 무기 반환

while True :
    
    # 메뉴 루프
    running = True
    while running:
        selected_weapon = draw_menu()  # 메뉴 표시 및 무기 선택
        weapon_type = selected_weapon.lower()  # 선택된 무기 타입 설정
        player_hp = player_Maxhp  # 플레이어의 체력 초기화
        running = False

    # 선택한 무기 출력 (게임 시작 전 무기 선택 결과를 사용)
    print(f"Selected Weapon: {selected_weapon}")

    # 기존 게임 코드에 선택된 무기 반영
    weapon_type = selected_weapon.lower()  # 무기 타입을 소문자로 변환하여 사용


    # 파일을 현재 작업 디렉토리로 복사

    #shutil.copy("C:/Users/User/Desktop/startcoding/NeoDunggeunmoPro-Regular.ttf", ".")


    reset_game()
    
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
        elif weapon_type == 'bow':
            weapon_damage = 30 * damage_up
            shoot_delay = 800  
                    
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

        current_time = pygame.time.get_ticks()
        
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
        elif weapon_type == 'bow':
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
                mouse_clicked = True
                '''if is_reloading and current_time - last_reload_time < reload_time:
                    continue  # 재장전 중이면 발사할 수 없음
                if weapon_type == 'handgun' : 
                    if current_ammo > 0:  # 남은 총알이 있을 때만 발사
                        if current_time - last_shot_time > shoot_delay:
                            # 플레이어의 현재 각도에 따라 투사체 생성
                            projectiles.append(Projectile(weapon_x, weapon_y, angle))  # 무기 끝에서 발사
                            current_ammo -= 1
                            gunshot_sound.play()  # 총쏘는 소리 재생
                            last_shot_time = current_time  # 마지막 발사 시간을 현재 시간으로 갱신'''
                if weapon_type == 'sword':
                    if current_time - sword_last_swing_time > sword_swing_duration:
                        is_swinging_sword = True
                        sword_last_swing_time = current_time
                elif weapon_type == 'magic':
                    if current_time - last_shot_time > shoot_delay:
                        # 발사할 손 결정 (왼손과 오른손 번갈아 가며 발사)
                        target_x, target_y = pygame.mouse.get_pos()
                        angle_to_pointer = math.degrees(math.atan2(target_y - weapon_y, target_x - weapon_x))
                        fire_sound.play()
                        if hand_select == 0:
                            # 왼손 발사
                            offset_distance = 70 # 손 사이의 거리
                            hand_x = weapon_x - offset_distance * math.cos(math.radians(angle_to_pointer + 90))
                            hand_y = weapon_y - offset_distance * math.sin(math.radians(angle_to_pointer + 90))
                            hand_select = 1
                        else:
                            # 오른손 발사
                            offset_distance = 70  # 손 사이의 거리
                            hand_x = weapon_x + offset_distance * math.cos(math.radians(angle_to_pointer + 90))
                            hand_y = weapon_y + offset_distance * math.sin(math.radians(angle_to_pointer + 90))
                            hand_select= 0
                            
                        # 손에서 발사체 생성
                        projectiles.append(FireProjectile(hand_x, hand_y, pointer_x, pointer_y))
                    
                        last_shot_time = current_time
                elif weapon_type == 'bow' :  
                    if current_time - last_shot_time > shoot_delay:
                        # 플레이어의 현재 각도에 따라 투사체 생성
                        projectiles.append(Arrow(weapon_x, weapon_y, angle))
                        bow_sound.play()  
                        last_shot_time = current_time  # 마지막 발사 시간을 현재 시간으로 갱신
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    use_special_skill(weapon_type, weapon_x, weapon_y, angle)
                    
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_clicked = False
        
        # 연속 발사 상태일 때 빠르게 총알 발사
        if is_rapid_firing and current_ammo > 0:
            if current_time < rapid_fire_end_time:
                projectiles.append(Projectile(weapon_x , weapon_y , angle + random.randint(-2, 2)))
                gunshot_sound.play()  # 총쏘는 소리 재생
                current_ammo -= 1  # 남은 총알 감소
            else:
                is_rapid_firing = False  # 연속 발사 종료   
            # 게임 루프에서 총기 발사 처리
        if pygame.mouse.get_pressed()[0] and not (is_reloading and current_time - last_reload_time < reload_time):  # 왼쪽 마우스 버튼이 눌린 상태
            if weapon_type == 'handgun' : 
                if current_ammo > 0:  # 남은 총알이 있을 때만 발사
                    if current_time - last_shot_time > shoot_delay:
                        # 플레이어의 현재 각도에 따라 투사체 생성
                        projectiles.append(Projectile(weapon_x, weapon_y, angle))  # 무기 끝에서 발사
                        current_ammo -= 1
                        gunshot_sound.play()  # 총쏘는 소리 재생
                        last_shot_time = current_time  # 마지막 발사 시간을 현재 시간으로 갱신
                    
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
            
    # 적 투사체 업데이트
        for enemy_projectile in enemy_projectiles[:]:
            enemy_projectile.update()
            # 투사체가 화면 밖으로 나가면 삭제
            if (enemy_projectile.x < 0 or enemy_projectile.x > screen_width or
                    enemy_projectile.y < 0 or enemy_projectile.y > screen_height):
                enemy_projectiles.remove(enemy_projectile)
                continue  # 다음 투사체로 넘어감

           
            p_dist = math.hypot(player_x - enemy_projectile.x, player_y - enemy_projectile.y)
            if p_dist < 37 + enemy_projectile.radius :
                player_hp -= enemy.damage  # 적의 HP 감소
                player_take_damage()
                start_screen_shake()
                
                # 플레이어 밀리기
                player_angle = math.atan2(player_y - enemy_projectile.y, player_x - enemy_projectile.x)  # 플레이어와 적의 각도
                player_speed_x += math.cos(player_angle)  * 11  # 플레이어를 밀어냄
                player_speed_y += math.sin(player_angle) * 11  # 플레이어를 밀어냄
                
                enemy_projectile.to_remove = True  # 투사체 삭제 플래그 설정
                break  # 충돌 시 더 이상의 적과의 충돌 확인을 건너뜀
                
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
                    
                    enemy.apply_knockback(force=5, angle=math.atan2(enemy.y - player_y, enemy.x - player_x))
                    
                    if isinstance(projectile, FireProjectile):
                        projectile.explode(enemies)  # 불 투사체 폭발
                    
                    projectile.to_remove = True  # 투사체 삭제 플래그 설정
                    break  # 충돌 시 더 이상의 적과의 충돌 확인을 건너뜀

        # 삭제 플래그가 설정된 투사체와 적 제거
        enemy_projectiles = [ep for ep in enemy_projectiles if not ep.to_remove]
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
                    enemy.apply_knockback(force=5, angle=math.atan2(enemy.y - player_y, enemy.x - player_x))
                    if enemy.hp <= 0:
                        enemies.remove(enemy)
                    break  # 충돌 시 더 이상의 적과의 충돌 확인을 건너뜀

        # 일정 시간이 지나면 휘두르기 중지
        if pygame.time.get_ticks() - sword_last_swing_time > sword_swing_duration:
            is_swinging_sword = False
        
        '''
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
            screen.blit(warning_image, (new_enemy_x - 37, new_enemy_y - 37))'''
            # 게임 루프 내에 아래 코드를 추가
        wave_current_time = (time.time() - start_time) * 1000
        # 적 생성 경고 및 생성 딜레이
        if enemy_spawn_warning_time is None and wave_current_time - last_enemy_spawn_time > enemy_spawn_delay and wave_current_time > 2500:
            # 적이 생성될 좌표를 미리 설정
            new_enemy_x = random.randint(50, screen_width - 50)
            new_enemy_y = random.randint(50, screen_height - 50)
            enemy_spawn_warning_time = wave_current_time  # 경고 표시 시작 시간 설정

        # 경고 시간이 지나면 특정 적 생성
        if enemy_spawn_warning_time and wave_current_time - enemy_spawn_warning_time >= enemy_warning_time and wave_current_time > 4000:
            # 시간대에 따라 생성되는 적 유형 결정
            print(wave_current_time)
            if wave_current_time < 20000:
                wave = 1
                new_enemy = spawn_random_enemy(NormalEnemy)
                enemy_spawn_delay = 3000
                wave_duration = 20000       
            elif 20000 <= wave_current_time < 40000:
                new_enemy = spawn_random_enemy(random.choice([NormalEnemy,FastEnemy]))
                enemy_spawn_delay = 1500
                wave_duration = 20000
            elif 40000 <= wave_current_time < 55000:
                new_enemy = spawn_random_enemy(FastEnemy)
                enemy_spawn_delay = 1000
                wave_duration = 15000
            elif 55000 <= wave_current_time < 85000:
                new_enemy = spawn_random_enemy(StrongEnemy)
                enemy_warning_time = 2000
                enemy_spawn_delay = 4000
                wave_duration = 30000
            elif 85000 <= wave_current_time < 130000:
                
                new_enemy = spawn_random_enemy(random.choice([NormalEnemy,FastEnemy,StrongEnemy]))
                enemy_warning_time = 1000
                enemy_spawn_delay = 1000
                wave_duration = 45000
            elif 130000 <= wave_current_time < 160000:
                
                new_enemy = spawn_random_enemy(InvisibleEnemy)
                enemy_warning_time = 1500
                enemy_spawn_delay = 2000
                wave_duration = 30000
            elif 160000 <= wave_current_time < 180000:

                new_enemy = spawn_random_enemy(random.choice([InvisibleEnemy,FastEnemy]))
                enemy_warning_time = 1500
                enemy_spawn_delay = 1500
                wave_duration = 20000
            elif 180000 <= wave_current_time < 200000:
            
                new_enemy = spawn_random_enemy(random.choice([InvisibleEnemy,FastEnemy, StrongEnemy]))
                enemy_warning_time = 1500
                enemy_spawn_delay = 1000
                wave_duration = 20000
            elif 200000 <= wave_current_time < 240000:
         
                new_enemy = spawn_random_enemy(random.choice([FlashEnemy, InvisibleEnemy]))
                enemy_warning_time = 1500
                enemy_spawn_delay = 1500
                wave_duration = 40000
            elif 240000 <= wave_current_time < 270000:
         
                new_enemy = spawn_random_enemy(random.choice([StoneEnemy, StrongEnemy, FlashEnemy]))
                enemy_warning_time = 1500
                enemy_spawn_delay = 2000
                wave_duration = 30000
            elif 270000 <= wave_current_time < 300000:
          
                new_enemy = spawn_random_enemy(random.choice([StoneEnemy, Titan]))
                enemy_warning_time = 2000
                enemy_spawn_delay = 1500
                wave_duration = 30000
            elif 300000 <= wave_current_time < 340000:
         
                new_enemy = spawn_random_enemy(random.choice([StoneEnemy, FlashEnemy, SuicideEnemy]))
                enemy_warning_time = 1500
                enemy_spawn_delay = 1500
                wave_duration = 40000
            elif 340000 <= wave_current_time < 380000:
                new_enemy = spawn_random_enemy(random.choice([MutantEnemy, SuicideEnemy]))
                enemy_warning_time = 1500
                enemy_spawn_delay = 2500
                wave_duration = 40000
            elif 340000 <= wave_current_time < 400000:
                new_enemy = spawn_random_enemy(random.choice([MutantEnemy, StoneEnemy, Titan, FlashEnemy]))
                enemy_warning_time = 1500
                enemy_spawn_delay = 2000
                wave_duration = 60000
            
                
                       
            # 적 위치 설정 및 리스트에 추가
            new_enemy.x = new_enemy_x
            new_enemy.y = new_enemy_y
            enemies.append(new_enemy)

            # 경고 시간 초기화
            enemy_spawn_warning_time = None
            last_enemy_spawn_time = wave_current_time
            
        # 적 생성 경고 표시
        if enemy_spawn_warning_time and wave_current_time - enemy_spawn_warning_time < enemy_warning_time:
            # 경고 이미지 표시 (미리 정한 좌표에 표시)
            screen.blit(warning_image, (new_enemy_x - 37, new_enemy_y - 37))
            
        # 적 이동 및 그리기
        for enemy in enemies:  # enemies는 적 객체들의 리스트로 가정합니다.
            enemy.follow_player(player_x, player_y)

        #플레이어와 적과의 충돌 확인
        for enemy in enemies[:]:
            dist = math.hypot(enemy.x - player_x, enemy.y - player_y)
            
            if dist < enemy.radius + 37:  # 플레이어의 반지름
                if isinstance(enemy, SuicideEnemy) :
                    enemy.explode()  # 플레이어와 가까워지면 폭발
                    
                player_hp -= enemy.damage  # 플레이어 HP 감소
                player_take_damage()
                start_screen_shake()
                damage_texts.append(DamageText(player_x, player_y, enemy.damage))

                # 플레이어와 적 모두 밀리게 함
                push_back_strength = 0.8  # 밀리는 힘 조절 (기존 0.3에서 증가)

                # 플레이어 밀리기
                player_angle = math.atan2(player_y - enemy.y, player_x - enemy.x)  # 플레이어와 적의 각도
                player_speed_x += math.cos(player_angle) * push_back_strength * 22  # 플레이어를 밀어냄
                player_speed_y += math.sin(player_angle) * push_back_strength * 22  # 플레이어를 밀어냄

                # 적 밀리기
                enemy.apply_knockback(force=10, angle=math.atan2(enemy.y - player_y, enemy.x - player_x))
                
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
            
        # 투사체 그리기
        for enemy_projectile in enemy_projectiles:
            enemy_projectile.draw(screen)
            
        # 적 그리기
        for enemy in enemies:
            enemy.update()  # 적 상태 업데이트 (투명도 등)sssss
            enemy.draw(screen)
            
        if weapon_type == 'handgun':
            # 무기 회전 및 그리기
            rotated_weapon = pygame.transform.rotate(handgun_image, -angle - 90)
            weapon_rect = rotated_weapon.get_rect(center=(weapon_x+ shake_offset_x, weapon_y+ shake_offset_y))
            screen.blit(rotated_weapon, weapon_rect.topleft)
        elif weapon_type == 'bow':
            rotated_bow = pygame.transform.rotate(bow_image, -angle - 90)
            bow_rect = rotated_bow.get_rect(center=(weapon_x+ shake_offset_x, weapon_y+ shake_offset_y))
            screen.blit(rotated_bow, bow_rect.topleft)
            
        # 플레이어 회전 및 그리기
        rotated_player = pygame.transform.rotate(player_image, -angle - 90)
        player_rect = rotated_player.get_rect(center=(player_x + shake_offset_x, player_y + shake_offset_y))
        screen.blit(rotated_player, player_rect.topleft)

        

        # 적 생성 경고 표시
    #  if enemy_spawn_warning_time and current_time - enemy_spawn_warning_time < 2000:  # 2초 동안 표시
    #     pygame.draw.rect(screen, WARNING_COLOR, (new_enemy_x - 15, new_enemy_y - 30, 50, 50))  # 적 생성 경고 사각형
        # 화면에 남은 탄창 수와 총알 수를 표시
        if weapon_type == 'handgun':
            if is_reloading:
                ammo_text = ammo_font.render("재장전 중", True, WHITE)
                screen.blit(ammo_text, (player_x - 60 + shake_offset_x, player_y + shake_offset_y + 55))  # 플레이어 하단에 표시
            else:
                ammo_text = ammo_font.render(f"{current_ammo}/{max_ammo_per_magazine}", True, WHITE)
                screen.blit(ammo_text, (player_x - 48 + shake_offset_x, player_y + shake_offset_y + 55))  # 플레이어 하단에 표시
            # 체력바 그리기
        player_hp_bar_width = 180
        player_hp_bar_height = 25
        
        if last_level_up_time and current_time - last_level_up_time < level_up_display_time:
            level_up_text = font.render("Level Up!", True, (255, 215, 0))  # 황금색 텍스트
            screen.blit(level_up_text, (player_x - level_up_text.get_width() // 2, player_y - 150))
              
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
            if not isinstance(enemy, InvisibleEnemy) or not enemy.invisible:
                enemy_hp_bar_width = player_hp_bar_width  # 적 HP 바의 너비를 플레이어와 동일하게 설정
                enemy_hp_bar_height = 25
                pygame.draw.rect(screen, (0, 0, 0), (enemy.x - enemy_hp_bar_width // 2, enemy.y - 85+ shake_offset_y, enemy_hp_bar_width, enemy_hp_bar_height))  # 적 HP 바 배경
                pygame.draw.rect(screen, (0, 0, 255), (enemy.x - enemy_hp_bar_width // 2, enemy.y - 85+ shake_offset_y, enemy_hp_bar_width * (enemy.hp / enemy.Maxhp), enemy_hp_bar_height))  # 적 체력

                # 적 HP 텍스트 표시
                enemy_hp_text = font.render(f"{int(enemy.hp)}/{enemy.Maxhp}", True, (255, 255, 255))  # 텍스트 생성
                screen.blit(enemy_hp_text, (enemy.x - enemy_hp_bar_width // 2 + (enemy_hp_bar_width - enemy_hp_text.get_width()) // 2, enemy.y - 89))  # 텍스트 위치
               
        # 힐링 중일 때 일정 간격으로 십자가 생성
        for spawn_time in cross_spawn_times[:]:
            if current_time >= spawn_time:
                draw_heal_effect()
                cross_spawn_times.remove(spawn_time)
                             
        # 저장된 모든 십자가 그리기
        for cross in crosses[:]:
            cross_pos = cross["pos"]
            transparency = cross["transparency"]
            cross_size = cross["cross_size"]

            # 십자가 그리기용 표면 생성 및 투명도 설정
            cross_surface = pygame.Surface((cross_size * 2, cross_size * 2), pygame.SRCALPHA)
            cross_surface.set_alpha(transparency)

            # 십자가 그리기
            pygame.draw.line(cross_surface, Lime_Green, (cross_size - 40, cross_size), (cross_size + 40, cross_size), 30)
            pygame.draw.line(cross_surface, Lime_Green, (cross_size, cross_size - 40), (cross_size, cross_size + 40), 30)

            # 십자가 화면에 블릿
            screen.blit(cross_surface, (cross_pos[0] - cross_size, cross_pos[1] - cross_size))

            # 투명도 값 감소시키기 (점점 사라짐)
            cross["transparency"] -= 7
            if cross["transparency"] <= 0:
                crosses.remove(cross)  # 투명도 값이 0 이하일 경우 리스트에서 제거
            
        # 대미지 텍스트 업데이트 및 그리기
        for damage_text in damage_texts[:]:
            if not damage_text.draw(screen, damage_font):  # 텍스트를 화면에 그리기
                damage_texts.remove(damage_text)  # 지속 시간이 끝난 텍스트 삭제
                
          
        
        if weapon_type == 'magic':
            rotated_pointer = pygame.transform.rotate(big_pointer_image, -angle - 90)
            pointer_offset_x = 0 * math.cos(math.radians(angle + 90))
            pointer_offset_y = 0 * math.sin(math.radians(angle + 90))
        elif weapon_type == 'bow':
            rotated_pointer = pygame.transform.rotate(pointer_image, -angle - 90)
            pointer_offset_x = 0 * math.cos(math.radians(angle + 90))
            pointer_offset_y = 0 * math.sin(math.radians(angle + 90))
        else :
            rotated_pointer = pygame.transform.rotate(pointer_image, -angle - 90)
            pointer_offset_x = 35 * math.cos(math.radians(angle + 90))
            pointer_offset_y = 35 * math.sin(math.radians(angle + 90))
            
        wave_text = menu_font.render(f"Wave {wave}", True, (255, 255, 255))  
        screen.blit(wave_text, (850, 30))  # 텍스트 위치
        
        time_elapsed = current_time - wave_start_time
        time_remaining = max(0, wave_duration - time_elapsed)
        
        if time_remaining == 0:
            reset_wave()
            heal_player(int(player_Maxhp / 5))
            wave += 1

        # 웨이브 타이머 바 그리기
        timer_bar_width = 400  # 타이머 바의 총 너비
        timer_bar_height = 30  # 타이머 바의 높이
        timer_bar_x = 761  # 타이머 바의 X 위치
        timer_bar_y = 135  # 타이머 바의 Y 위치
        timer_bar_filled_width = int((time_remaining / wave_duration) * timer_bar_width)

        
        pygame.draw.rect(screen, (100, 100, 100), (timer_bar_x, timer_bar_y, timer_bar_width, timer_bar_height))
    
        pygame.draw.rect(screen, (240, 0, 0), (timer_bar_x, timer_bar_y, timer_bar_filled_width, timer_bar_height))

        # 조준점 위치 업데이트
        pointer_x = mouse_x + pointer_offset_x
        pointer_y = mouse_y + pointer_offset_y
        
        pointer_rect = rotated_pointer.get_rect(center=(pointer_x , pointer_y ))
        screen.blit(rotated_pointer, pointer_rect.topleft)
        # 조준점
        if mouse_clicked:
            screen.blit(big_pointer_image, (pointer_x - 90, pointer_y - 90))
        
        if damage_flash_timer > 0:
            damage_flash_timer -= 50  # 프레임 시간만큼 감소
            if damage_flash_timer < 0:
                damage_flash_timer = 0  # 타이머가 음수가 되지 않도록 보정

        update_screen()
        
        pygame.display.flip()  # 화면 업데이트
        pygame.time.delay(FPS)  # FPS 



