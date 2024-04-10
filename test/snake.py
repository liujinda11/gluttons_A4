# -*- coding: utf-8 -*-
import math
import random
import cocos
from cocos.sprite import Sprite
import cocos
from cocos.director import director
import define
from dot import Dot
import account
from account import insert_account, update_score, match_user_information, get_ranking, change_cust, change_music, change_volume, change_evolume, current_state, change_cmode

class SnakeSkin:
    def __init__(self, name, color):
        self.name = name
        self.color = color

class SkinManager:
    def __init__(self, username):
        self.skins = [
            SnakeSkin('LitterSnake', (0, 0, 0)),
            SnakeSkin('FireSnake', (255, 0, 0)), 
            SnakeSkin('IceSnake', (0, 0, 255)),
            SnakeSkin('MagicSnake', random.choice(define.ALL_COLOR))
        ]
	
        self.username = username
        self.current_skin = self.get_current_skin(self.username)

    def get_current_skin(self, username):
        cust_number = self.get_current_cust_number(username)
        return self.skins[cust_number]

    def get_current_cust_number(self, username):
        state = current_state(username)
        print(f"Current state: {state}")
        if state is None or not isinstance(state, (list, tuple)) or len(state) < 10:
            return 0  # 如果状态为None或长度不足10,则默认为0
        cust_number = state[9]
        print(f"Current cust_number: {cust_number}")
        if cust_number is None:
            cust_number = 0  # 如果没有自定义皮肤,则默认为0
            change_cust(self.username, skin_number)
        return int(cust_number)


class Snake(cocos.cocosnode.CocosNode):
    no = 0

    def __init__(self, username, is_enemy=False, mode='classic'):
        super(Snake, self).__init__()

        self.mode = mode
        self.speed_multiplier = 1.2 if self.mode == 'unlimited_firepower' else 1

        self.score = None
        self.length = None
        self.body = None
        self.speed = 0
        self.updated_speed = 0
        self.is_dead = False
        self.paused = False
        self.angle = random.randrange(360)  # 目前角度
        self.angle_dest = self.angle  # 目标角度
        self.username = username

        if not is_enemy:
            self.skin_manager = SkinManager(self.username)
            self.color = self.skin_manager.current_skin.color
        else:
            self.color = random.choice(define.ALL_COLOR)

        Snake.no += 1

        if is_enemy:
            pass
        else:
            self.position = random.randrange(define.WIDTH // 2 - 100, define.WIDTH // 2 + 100), \
                random.randrange(define.HEIGHT // 2 - 50, define.HEIGHT // 2 + 50)

        self.is_enemy = is_enemy

        self.head = Sprite('circle.png', color=self.color)
        self.scale = 0.375  # 64像素的超分图是0.75，16像素时是1.5

        # 左眼
        eye = Sprite('circle.png')
        eye.x = 15  # 原先0
        eye.y = 15  # 原先5
        eye.scale = 0.375  # 16像素时是0.5
        eyeball = Sprite('circle.png', color=define.BLACK)
        eyeball.scale = 0.375  # 16像素时是0.5
        eye.add(eyeball)
        self.head.add(eye)

        # 右眼
        eye = Sprite('circle.png')
        eye.x = 15
        eye.y = -15
        eye.scale = 0.375  # 16像素时是0.5
        eyeball = Sprite('circle.png', color=define.BLACK)
        eyeball.scale = 0.375  # 16像素时是0.5
        eye.add(eyeball)
        self.head.add(eye)

        self.add(self.head)

        self.init_speed = 150
        if not is_enemy:
            self.init_speed = 180

        self.updated_speed = self.init_speed * self.speed_multiplier
        self.speed = self.updated_speed

        self.path = [self.position] * 100

        self.schedule(self.update)
        if self.is_enemy:
            self.schedule_interval(self.ai, random.random() * 0.1 + 0.05)

    # ... (其他方法保持不变)

# ... (其他代码保持不变)

    def init_enemy_position(self):
        safe_distance = 300  # 安全距离
        max_attempts = 100  # 最大尝试次数以避免无限循环
        for _ in range(max_attempts):
            potential_position = random.randrange(100, define.WIDTH - 100), \
                random.randrange(100, define.HEIGHT - 100)
            # print("potential position: ", potential_position[0], potential_position[1])  # 添加的打印语句
            player_head_pos = self.parent.snake.position
            player_body_positions = [b.position for b in self.parent.snake.body]

            dx = potential_position[0] - player_head_pos[0]
            dy = potential_position[1] - player_head_pos[1]
            distance_to_head = math.sqrt(dx ** 2 + dy ** 2)

            too_close_to_body = False
            for pos in player_body_positions:
                distance_to_body = math.sqrt(
                    (potential_position[0] - pos[0]) ** 2 + (potential_position[1] - pos[1]) ** 2)
                if distance_to_body < safe_distance:
                    too_close_to_body = True
                    # print("too close\n")
                    break

            if distance_to_head >= safe_distance and not too_close_to_body:
                self.position = potential_position
                # print("safely generate an enemy, ^^^ as position\n")
                break  # 找到了一个安全的位置

    def add_body(self):
        # 创建一个新的身体部分
        new_body_part = Sprite('circle.png', color=self.color)
        new_body_part.position = self.position  # 将新身体部分放置在蛇头的当前位置

        # 将新身体部分添加到绘制列表中
        # 使用一个计算得来的z-index确保蛇身部分按正确顺序绘制
        if self.x == 0:
            print(self.position)
        new_body_part.position = self.position
        try:
            new_body_part.scale = 0.375 + (self.score - 30) * 0.0005  # self.head.scale
            self.parent.batch.add(new_body_part, 999 + 100 * self.no - len(self.body))
        except:
            print(999 + 100 * self.no - len(self.body))

        # 更新蛇的身体列表，加入新的身体部分
        # """
        if not self.is_enemy:
            # print(new_body_part.scale)
            # print("player's body extended")
            pass
        # """
        self.body.append(new_body_part)
        # 更新头部大小
        self.head.scale += 0.0075  # 假设头部大小每增加一个身体部分，增加0.0125的比例 <-16像素

    def init_body(self):
        self.score = 30
        self.length = 4
        self.body = []
        for i in range(self.length):
            self.add_body()

    def update(self, dt):

        if self.paused:
            return

        self.angle = (self.angle + 360) % 360

        arena = self.parent
        if self.is_enemy:
            self.check_crash(arena.snake)
        for s in arena.enemies:
            if s != self and not s.is_dead:
                self.check_crash(s)
        if self.is_dead:
            return

        if abs(self.angle - self.angle_dest) < 2:
            self.angle = self.angle_dest
        else:
            if (0 < self.angle - self.angle_dest < 180) or (
                    self.angle - self.angle_dest < -180):
                self.angle -= 500 * dt
            else:
                self.angle += 500 * dt
        self.head.rotation = -self.angle

        self.x += math.cos(self.angle * math.pi / 180) * dt * self.speed
        self.y += math.sin(self.angle * math.pi / 180) * dt * self.speed
        self.path.append(self.position)

        # 更新身体位置
        base_lag = 6  # 基础间隔
        increment_per_length = 0.0001  # 每增加一个身体长度单位，间隔增加的量
        smooth_factor = 0.1  # 平滑因子，用于平滑间隔的增长

        # 计算当前的总间隔增量，使用平滑因子减少突变
        total_increment = increment_per_length * len(self.body) * smooth_factor

        # 根据蛇的长度动态调整路径记录的密度
        path_record_frequency = int(1 + len(self.body) / 10)  # 假设蛇身体每增加5个单位，路径记录的频率增加
        if len(self.path) % path_record_frequency == 0:
            self.path.append(self.position)

        for i, b in enumerate(self.body):
            # 使用平滑后的总间隔增量计算每个身体部分的实际间隔
            lag = base_lag + total_increment * (i / len(self.body))
            idx = (i + 1) * int(lag)
            if len(self.path) > idx:
                b.position = self.path[-idx]

            new_scale = 0.375 + (self.score - 30) * 0.0005  # 假设每增加一分，scale增加0.0015
            b.scale = new_scale

        # 确保路径长度适应身体长度的增加
        required_path_length = (len(self.body) + 1) * (base_lag + total_increment)
        if len(self.path) > required_path_length:
            self.path = self.path[-int(required_path_length):]

            """
            body_offsets = [(0, 0)] * len(self.body)

            prev_point = self.path[-min(idx, len(self.path))]  # 前一个点
            current_point = self.path[-min(idx - lag, len(self.path))]  # 当前点
            direction = math.atan2(current_point[1] - prev_point[1], current_point[0] - prev_point[0])

            # 根据方向和距离计算身体部分的位置
            body_distance = i * 5  # 身体部分之间的距离
            new_x = current_point[0] - body_distance * math.cos(direction)
            new_y = current_point[1] - body_distance * math.sin(direction)

            # 计算相对偏移量
            if i > 0:
                body_offsets[i] = (new_x - self.body[i - 1].position[0], new_y - self.body[i - 1].position[1])

            # 更新身体部分的位置
            self.body[i].position = (new_x, new_y)
            """

            """            
            if self.body[i].x == 0:
                print(self.body[i].position)

            m_l = max(self.length * lag * 2, 60)
            if len(self.path) > m_l:
                self.path = self.path[int(-m_l * 2):]
                
            """

        if self.is_enemy:
            self.speed = self.updated_speed + math.sqrt((self.score - 30)) * 2  # 速度会增长得越来越慢
        if not self.is_enemy:
            self.speed = self.updated_speed + math.sqrt((self.score - 30)) * 2

    def update_angle(self, keys):
        x, y = 0, 0
        if 65361 in keys:  # 左
            x -= 1
        if 65362 in keys:  # 上
            y += 1
        if 65363 in keys:  # 右
            x += 1
        if 65364 in keys:  # 下
            y -= 1
        directs = ((225, 180, 135), (270, None, 90), (315, 0, 45))
        direct = directs[x + 1][y + 1]
        if direct is None:
            self.angle_dest = self.angle
        else:
            self.angle_dest = direct

    def add_score(self, s=1):
        if self.is_dead:
            return
        self.score += s
        l = (self.score - 6) // 6
        if l > self.length:
            self.length = l
            self.add_body()

    def ai(self, dt):

        if self.paused:
            return

        self.angle_dest = (self.angle_dest + 360) % 360
        if (self.x < 100 and 90 < self.angle_dest < 270) or (
                self.x > define.WIDTH - 100 and (
                self.angle_dest < 90 or self.angle_dest > 270)
        ):
            self.angle_dest = 180 - self.angle_dest
        elif (self.y < 100 and self.angle_dest > 180) or (
                self.y > define.HEIGHT - 100 and self.angle_dest < 180
        ):
            self.angle_dest = -self.angle_dest
        else:
            arena = self.parent
            self.collision_detect(arena.snake)
            for s in arena.enemies:
                if s != self:
                    self.collision_detect(s)

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def collision_detect(self, other):
        if self.is_dead or other.is_dead:
            return
        for b in other.body:
            d_y = b.y - self.y
            d_x = b.x - self.x
            if abs(d_x) > 200 or abs(d_y) > 200:
                return
            if d_x == 0:
                if d_y > 0:
                    angle = 90
                else:
                    angle = -90
            else:
                angle = math.atan(d_y / d_x) * 180 / math.pi
                if d_x < 0:
                    angle += 180
            angle = (angle + 360) % 360
            if abs(angle - self.angle_dest) < 5:
                self.angle_dest += random.randrange(90, 270)

    def check_crash(self, other):
        if self.is_dead or other.is_dead:
            return
        if (self.x < 0 or self.x > define.WIDTH) or (
                self.y < 0 or self.y > define.HEIGHT
        ):
            self.crash(None)
            return
        """
        collision_distance = 24 + len(self.body) * 0.5  # 假设每增加一个身体部分，碰撞距离增加0.5
        for b in other.body:
            dis = math.sqrt((b.x - self.x) ** 2 + (b.y - self.y) ** 2)
            if dis < collision_distance:
                self.crash()
                return
        """
        for b in other.body:
            # 超清后的蛇头和蛇身部分的图片尺寸基准是64像素
            # 原图16像素
            base_size = 16
            # 计算蛇头和蛇身部分的实际半径
            head_radius = (self.head.scale * base_size) / 2
            body_radius = (b.scale * base_size) / 2
            # 碰撞距离为蛇头半径与这节蛇身半径之和
            collision_distance = head_radius + body_radius

            dis = math.sqrt((b.x - self.x) ** 2 + (b.y - self.y) ** 2)
            if dis < collision_distance:
                self.crash(other)
                return

    def crash(self, other):
        if not self.is_dead:
            self.is_dead = True
            self.unschedule(self.update)
            self.unschedule(self.ai)
            arena = self.parent
            for b in self.body:
                arena.batch.add(Dot(b.position, b.color))
                arena.batch.add(Dot(b.position, b.color))
                arena.batch.remove(b)

            arena.remove(self)
            arena.add_enemy()
            del self.path
            if self.is_enemy:
                arena.enemies.remove(self)
                if not other == None and other.is_enemy:
                    self.parent.kills += 1
                    print("   ###   You has slain an enemy!!!")
                del self.body
                del self
            else:
                arena.parent.end_game()




