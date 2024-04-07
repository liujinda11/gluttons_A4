# -*- coding: utf-8 -*-
import random
from cocos.actions import MoveTo, CallFuncS
from cocos.sprite import Sprite

import define


# 吃的函数
def kill(spr):
    # 停止生成
    spr.unschedule(spr.update)
    arena = spr.parent.parent  # arena场景对象是spr的爷爷节点
    # 是否是大块的食物
    if not spr.is_big:
        # 吃了小的（自然生成的）就只加基础分数，并且重新生成
        arena.batch.add(Dot())
        spr.killer.add_score()
    else:
        # 吃了大的就双倍加分
        if spr.mode == 'unlimited_firepower':
            spr.killer.add_score(2.4)  # unlimited firepower 模式加分调整为2.4倍
        else:
            spr.killer.add_score(2)
    # 只是在场景中移除被吃的食物
    arena.batch.remove(spr)
    if not spr.killer.is_enemy:
        # 自己吃了就加分
        arena.parent.update_report()
    # 移除被吃的食物的整个对象
    del spr


class Dot(Sprite):  # 继承自Sprite类
    def __init__(self, pos=None, color=None, mode='classic'):

        self.mode = mode

        # 随机分配食物的颜色
        self.killer = None
        if color is None:
            color = random.choice(define.ALL_COLOR)

        # 素材：circle.png
        super(Dot, self).__init__('circle.png', color=color)
        self.killed = False # 还没被吃
        # 是否随机生成？
        if pos is None:
            # 在地图边缘40个单位内生成
            self.position = (random.randint(40, define.WIDTH - 40),
                             random.randint(40, define.HEIGHT - 40))
            # 普通大小 0.8的缩放比例
            self.is_big = False
            self.scale = 0.2  # 16像素时是0.8
        else:
            # 死亡位置附近掉落
            self.position = (pos[0] + random.random() * 32 - 16,
                             pos[1] + random.random() * 32 - 16)
            self.is_big = True
            self.scale = 0.25  # 16像素时是1
        # 在0.2s-0.4s间随机生成 注意 生成越快 npc成长就越快 就越容易因为内存不足卡死
        # 另外估计可以考虑游戏地图的大小以防卡死
        self.paused = False
        if self.mode == 'unlimited_firepower':
            self.schedule_interval(self.update, random.random() * 0.15 + 0.075)
        else:
            self.schedule_interval(self.update, random.random() * 0.2 + 0.1)

    def update(self, dt): # difference of time 两次更新之间的时间差
        if not self.paused:
            arena = self.parent.parent
            snake = arena.snake  # 本体蛇？
            self.check_kill(snake)  # 吃食物检测
            for s in arena.enemies:  # 杀敌检测
                self.check_kill(s)

    def check_kill(self, snake): # self是dot本身
        collision_distance = 80 + len(snake.body) * 0.1  # 假设每增加一个身体部分，碰撞距离增加0.2
        if (not self.killed and not snake.is_dead) and (
                abs(snake.x - self.x) < collision_distance and abs(snake.y - self.y) < collision_distance
        ):
            # 吃掉 边长
            self.killed = True
            self.killer = snake
            is_killed_by_player = not snake.is_enemy
            self.do(MoveTo(snake.position, 0.2) + CallFuncS(kill))

