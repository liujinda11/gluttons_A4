import cocos
from cocos.director import director

import define
from snake import Snake
from dot import Dot
import random
import string
from account import update_score

class Arena(cocos.layer.ColorLayer):
    is_event_handler = True

    def __init__(self, parent, username, mode):
        super(Arena, self).__init__(250, 255, 255, 255, define.WIDTH, define.HEIGHT)

        self.mode = mode
        self.parent = parent
        self.food_limit = 200
        self.current_food_count = 0

        initial_food_count = 50
        if self.mode == 'unlimited_firepower':
            self.initial_food_count = 150


        # 根据模式设置食物数量限制
        if self.mode == 'easy':
            self.food_limit = 150
        elif self.mode == 'classic':
            self.food_limit = 100
        elif self.mode == 'hard':
            self.food_limit = 50
        elif self.mode == 'unlimited_firepower':
            self.food_limit = 200

        self.center = (director.get_window_size()[0] / 2, director.get_window_size()[1] / 2)
        self.batch = cocos.batch.BatchNode()
        self.add(self.batch)

        self.snake = Snake(username, mode=self.mode)  # 将username传递给Snake
        self.add(self.snake, 10000)
        self.snake.init_body()
        self.kills = 0

        self.enemies = []
        for i in range(define.PLAYERS_NUM - 1):
            self.add_enemy()

        self.keys_pressed = set()

        # 根据模式设置初始食物数量
        if self.mode == 'easy':
            initial_food_count = 100
        elif self.mode == 'classic':
            initial_food_count = 50
        elif self.mode == 'hard':
            initial_food_count = 25
        elif self.mode == 'unlimited_firepower':
            initial_food_count = 150

        for _ in range(min(initial_food_count, self.food_limit)):
            self.add_food()

        self.schedule(self.update)

    def add_enemy(self):
        # 生成一个随机的用户名
        username = 'Enemy_' + ''.join(random.choices(string.ascii_letters + string.digits, k=5))
        enemy = Snake(username, mode=self.mode, is_enemy=True)  # 将随机生成的用户名传递给Snake
        self.add(enemy, 10000)
        enemy.init_enemy_position()  # 在添加到场景后进行敌人位置的初始化
        enemy.init_body()
        self.enemies.append(enemy)

    def pause_dots(self):
        for child in self.batch.children:
            if isinstance(child, Dot):
                child.paused = True

    def resume_dots(self):
        for child in self.batch.children:
            if isinstance(child, Dot):
                child.paused = False

    def pause_game(self):
        self.unschedule(self.update)  # 暂停主循环更新
        self.snake.pause()  # 暂停蛇的动作
        for enemy in self.enemies:
            enemy.pause()  # 暂停所有敌人的动作
        self.pause_dots()  # 暂停所有点的动作

    def resume_game(self):
        self.schedule(self.update)  # 恢复主循环更新
        self.snake.resume()  # 恢复蛇的动作
        for enemy in self.enemies:
            enemy.resume()  # 恢复所有敌人的动作
        self.resume_dots()  # 恢复所有点的动作

    def pause_scheduler(self):
        super().pause_scheduler()
        self.pause_dots()

    def resume_scheduler(self):
        super().resume_scheduler()
        self.resume_dots()

    def update(self, dt):
        if not self.parent.paused:
            self.x = self.center[0] - self.snake.x
            self.y = self.center[1] - self.snake.y

    def on_key_press(self, key, modifiers):
        if not self.parent.paused:
            self.keys_pressed.add(key)
            self.snake.update_angle(self.keys_pressed)

    def on_key_release(self, key, modifiers):
        if not self.parent.paused:
            self.keys_pressed.discard(key)
            self.snake.update_angle(self.keys_pressed)

    def get_scores(self):
        scores = [(self.snake.username, self.snake.score)]  # 使用蛇的username作为玩家名称
        scores.extend(('Enemy {}'.format(i + 1), enemy.score) for i, enemy in enumerate(self.enemies))
        return scores

    def add_food(self):
        if self.current_food_count < self.food_limit:
            self.batch.add(Dot(mode=self.mode))
            self.current_food_count += 1


