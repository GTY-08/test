import pygame
import sys
import math
import random

# 초기화
pygame.init()

# 화면 크기 설정
screen_width = 1920
screen_height = 1000
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pygame Player with Enemies')

#폰트
font = pygame.font.Font(None, 24)

# 색상
GROUND_COLOR = (139, 69, 19)  # 땅 색상
PLAYER_COLOR = (0, 255, 0)  # 플레이어 색상
ENEMY_COLOR = (0, 0, 255)  # 적 색상
PROJECTILE_COLOR = (255, 0, 0)  # 투사체 색상
WARNING_COLOR = (255, 0, 0)  # 빨간색 느낌표 색상
WHITE = (255, 255, 255)

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
friction = 0.95  # 마찰(감속 비율)
projectile_speed = 30  # 투사체 속도
player_Maxhp = 10
player_hp = 10  # 플레이어 HP

enemy_image = pygame.image.load('C:/Users/User/Desktop/startcoding/zombie.png')  # 적 이미지 파일
enemy_image = pygame.transform.scale(enemy_image, (75, 75))  # 적 이미지 크기 조정

# 적 클래스
class Enemy:
    def __init__(self, x, y, hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.radius = 37  # 적의 크기
        self.base_speed = 2  # 적의 기본 속도
        self.noise_intensity = 0.1  # 노이즈 강도 (적의 움직임에 랜덤 변화를 주기 위함)
        self.vx = 0  # x축 속도
        self.vy = 0  # y축 속도
        self.friction = 0.95  # 감속 비율 (값이 클수록 서서히 멈춤)

    def draw(self, screen):
        screen.blit(enemy_image, (self.x - 37, self.y - 37))  # 적을 그립니다. (-37, -37)로 중앙 조정

    def hit(self):
        self.hp -= 1  # HP 감소

    def follow_player(self, player_x, player_y):
        # 플레이어와의 거리 계산
        distance = math.hypot(player_x - self.x, player_y - self.y)
        
        # 거리 기반으로 속도 조절
        if distance > 200:
            speed = self.base_speed * 1
        elif distance < 100:
            speed = self.base_speed * 1
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
        noise_x = random.uniform(-self.noise_intensity, self.noise_intensity)
        noise_y = random.uniform(-self.noise_intensity, self.noise_intensity)

        # 최종적으로 적의 위치 업데이트
        self.x += self.vx + noise_x
        self.y += self.vy + noise_y


# 투사체 발사 딜레이 설정
shoot_delay = 250  # 밀리초
last_shot_time = pygame.time.get_ticks()  # 마지막으로 발사된 시간

# 투사체 클래스
class Projectile:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = projectile_speed
        self.radius = 5

    def update(self):
        # 투사체의 방향에 따라 위치 업데이트
        self.x += self.speed * math.cos(math.radians(self.angle))
        self.y += self.speed * math.sin(math.radians(self.angle))

    def draw(self, screen):
        pygame.draw.circle(screen, PROJECTILE_COLOR, (int(self.x), int(self.y)), self.radius)

# 투사체 리스트
projectiles = []

# 적 리스트
enemies = []
enemy_spawn_time = pygame.time.get_ticks()  # 적 생성 시간
enemy_spawn_delay = 2500  # 적 생성 간격 (밀리초)

# 적 생성 경고 시간과 딜레이 설정
enemy_warning_time = 2000  # 경고를 미리 표시할 시간 (밀리초)
enemy_spawn_delay = 3000  # 적 생성 간격 (밀리초)
enemy_spawn_warning_time = None  # 생성 경고를 표시할 시간 변수
last_enemy_spawn_time = pygame.time.get_ticks()
new_enemy_x = None  # 적이 생성될 x 좌표
new_enemy_y = None  # 적이 생성될 y 좌표

# 게임 루프
running = True
while running:
    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # 마우스 클릭 시 투사체 발사
        if event.type == pygame.MOUSEBUTTONDOWN:
            current_time = pygame.time.get_ticks()
            if current_time - last_shot_time > shoot_delay:
                # 플레이어의 현재 각도에 따라 투사체 생성
                projectiles.append(Projectile(player_x, player_y, angle))
                last_shot_time = current_time  # 마지막 발사 시간을 현재 시간으로 갱신

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

    # 플레이어 감속 (마찰)
    player_speed_x *= friction
    player_speed_y *= friction

    # 플레이어 위치 업데이트
    player_x += player_speed_x
    player_y += player_speed_y

    # 마우스 위치 가져오기
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # 플레이어와 마우스 사이의 각도 계산
    angle = math.degrees(math.atan2(mouse_y - player_y, mouse_x - player_x))

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
                enemy.hit()  # 적의 HP 감소

                # 적을 플레이어의 방향으로 밀리게 함
                push_back_strength = 0.8  # 밀리는 힘 조절
                angle = math.atan2(enemy.y - player_y, enemy.x - player_x)  # 적과 플레이어 사이의 각도 계산
                enemy.vx += math.cos(angle) * push_back_strength * 7  # 밀려나는 방향으로 이동
                enemy.vy += math.sin(angle) * push_back_strength * 7  # 밀려나는 방향으로 이동

                projectiles.remove(projectile)  # 투사체 삭제
                if enemy.hp <= 0:
                    enemies.remove(enemy)  # 적을 제거
                break  # 충돌 시 더 이상의 적과의 충돌 확인을 건너뜀

      # 화면 그리기
    screen.fill(GROUND_COLOR)  # 배경을 땅 색상으로 채우기
    
    # 적 업데이트 및 생성
    current_time = pygame.time.get_ticks()
    """
    if current_time - enemy_spawn_time > enemy_spawn_delay:
        # 새로운 적 생성
        new_enemy_x = random.randint(50, screen_width - 50)
        new_enemy_y = random.randint(50, screen_height - 50)
        enemy_spawn_warning_time = current_time  # 경고 시간 갱신
        enemies.append(Enemy(new_enemy_x, new_enemy_y, 3)) # 적 체력 설정
        enemy_spawn_time = current_time  # 마지막 적 생성 시간을 현재 시간으로 갱신
    """
    # 적 생성 경고 및 생성 딜레이
    if enemy_spawn_warning_time is None and current_time - last_enemy_spawn_time > enemy_spawn_delay:
        # 새로운 적이 생성될 좌표를 미리 정함
        new_enemy_x = random.randint(50, screen_width - 50)
        new_enemy_y = random.randint(50, screen_height - 50)
        enemy_spawn_warning_time = current_time  # 경고 표시 시작 시간을 현재 시간으로 설정

    # 경고 시간이 지나면 적을 생성
    if enemy_spawn_warning_time and current_time - enemy_spawn_warning_time >= enemy_warning_time:
        # 적을 생성하고 적 리스트에 추가
        enemies.append(Enemy(new_enemy_x, new_enemy_y, 3))
        # 적이 생성된 후 다시 경고 시간을 초기화
        enemy_spawn_warning_time = None
        last_enemy_spawn_time = current_time  # 마지막 적 생성 시간을 갱신

    # 적 생성 경고 표시
    if enemy_spawn_warning_time and current_time - enemy_spawn_warning_time < enemy_warning_time:
        screen.blit(warning_image, (new_enemy_x - 37, new_enemy_y - 37)) 
         
    for enemy in enemies:
        enemy.follow_player(player_x, player_y)  # 적이 플레이어를 따라가게 함

    # 적과의 충돌 확인
    for enemy in enemies[:]:
        dist = math.hypot(enemy.x - player_x, enemy.y - player_y)
        if dist < enemy.radius + 50:  # 플레이어의 반지름
            player_hp -= 1  # 플레이어 HP 감소

            # 플레이어와 적 모두 밀리게 함
            push_back_strength = 0.8  # 밀리는 힘 조절 (기존 0.3에서 증가)

            # 플레이어 밀리기
            player_angle = math.atan2(player_y - enemy.y, player_x - enemy.x)  # 플레이어와 적의 각도
            player_speed_x += math.cos(player_angle) * push_back_strength * 9  # 플레이어를 밀어냄
            player_speed_y += math.sin(player_angle) * push_back_strength * 9  # 플레이어를 밀어냄

            # 적 밀리기
            enemy_angle = math.atan2(enemy.y - player_y, enemy.x - player_x)  # 적과 플레이어의 각도
            enemy.speed = 2  # 적의 밀려나는 속도 (기존 2에서 감소)
            enemy.x += math.cos(enemy_angle) * push_back_strength * enemy.speed * 20  # 적을 밀어냄
            enemy.y += math.sin(enemy_angle) * push_back_strength * enemy.speed * 20  # 적을 밀어냄



    # 게임 오버 체크
    if player_hp <= 0:
        running = False

  

    # 플레이어 회전 및 그리기
    rotated_player = pygame.transform.rotate(player_image, -angle)
    player_rect = rotated_player.get_rect(center=(player_x, player_y))
    screen.blit(rotated_player, player_rect.topleft)

    # 투사체 그리기
    for projectile in projectiles:
        projectile.draw(screen)

    # 적 그리기
    for enemy in enemies:
        enemy.draw(screen)

    # 적 생성 경고 표시
  #  if enemy_spawn_warning_time and current_time - enemy_spawn_warning_time < 2000:  # 2초 동안 표시
   #     pygame.draw.rect(screen, WARNING_COLOR, (new_enemy_x - 15, new_enemy_y - 30, 50, 50))  # 적 생성 경고 사각형

    # 체력바 그리기
    player_hp_bar_width = 100
    player_hp_bar_height = 15
    pygame.draw.rect(screen, (0, 0, 0), (player_x - player_hp_bar_width // 2, player_y - 70, player_hp_bar_width, player_hp_bar_height))  # 플레이어 HP 바 배경
    pygame.draw.rect(screen, (255, 0, 0), (player_x - player_hp_bar_width // 2, player_y - 70, player_hp_bar_width * (player_hp / player_Maxhp), player_hp_bar_height))  # 플레이어 체력

    # 플레이어 HP 텍스트 표시
    player_hp_text = font.render(f"{player_hp}/{player_Maxhp}", True, (255, 255, 255))  # 텍스트 생성
    screen.blit(player_hp_text, (player_x - player_hp_bar_width // 2 + (player_hp_bar_width - player_hp_text.get_width()) // 2, player_y - 70))  # 텍스트 위치

    for enemy in enemies:
        enemy_hp_bar_width = player_hp_bar_width  # 적 HP 바의 너비를 플레이어와 동일하게 설정
        enemy_hp_bar_height = 15
        pygame.draw.rect(screen, (0, 0, 0), (enemy.x - enemy_hp_bar_width // 2, enemy.y - 70, enemy_hp_bar_width, enemy_hp_bar_height))  # 적 HP 바 배경
        pygame.draw.rect(screen, (0, 0, 255), (enemy.x - enemy_hp_bar_width // 2, enemy.y - 70, enemy_hp_bar_width * (enemy.hp / 3), enemy_hp_bar_height))  # 적 체력

        # 적 HP 텍스트 표시
        enemy_hp_text = font.render(f"{enemy.hp}/3", True, (255, 255, 255))  # 텍스트 생성
        screen.blit(enemy_hp_text, (enemy.x - enemy_hp_bar_width // 2 + (enemy_hp_bar_width - enemy_hp_text.get_width()) // 2, enemy.y - 70))  # 텍스트 위치


    pygame.display.flip()  # 화면 업데이트
    pygame.time.delay(30)  # FPS 

# 게임 오버 화면
print("Game Over!")
pygame.quit()
