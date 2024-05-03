# -*- coding: utf-8 -*-
import random
from cocos.actions import MoveTo, CallFuncS
from cocos.sprite import Sprite

import define


def kill(spr):
    # Stop updating the sprite
    spr.unschedule(spr.update)
    arena = spr.parent.parent  # 'arena' is the grandparent of 'spr', representing the game scene
    # Check if the food is not a large piece
    if not spr.is_big:
        # For small (naturally generated) food, add basic score and regenerate
        arena.batch.add(Dot())
        spr.killer.add_score()
    else:
        # For large food, add double score
        if spr.mode == 'unlimited_firepower':
            spr.killer.add_score(2.4)  # In 'unlimited firepower' mode, score is multiplied by 2.4
        else:
            spr.killer.add_score(2)
    # Remove the eaten food from the scene
    arena.batch.remove(spr)
    if not spr.killer.is_enemy:
        # If the player ate it, update the score
        arena.parent.update_report()
    # Delete the food object completely
    del spr


class Dot(Sprite):  # Inherits from the Sprite class
    def __init__(self, pos=None, color=None, mode='classic'):
        self.mode = mode

        # Randomly assign a color to the food
        self.killer = None
        if color is None:
            color = random.choice(define.ALL_COLOR)

        # Use 'circle.png' as the sprite image
        super(Dot, self).__init__('circle.png', color=color)
        self.killed = False  # Food has not yet been eaten
        # Random generation?
        if pos is None:
            # Generate within 40 units from the edge of the map
            self.position = (random.randint(40, define.WIDTH - 40),
                             random.randint(40, define.HEIGHT - 40))
            # Normal size, scale down to 0.8
            self.is_big = False
            self.scale = 0.2  # Scale of 0.8 at 16 pixels
        else:
            # Drop near the death position
            self.position = (pos[0] + random.random() * 32 - 16,
                             pos[1] + random.random() * 32 - 16)
            self.is_big = True
            self.scale = 0.25  # Scale of 1 at 16 pixels
        # Random generation interval between 0.2s-0.4s, faster generation can lead to NPC growth, possibly causing memory issues
        # Consider game map size to prevent crashes
        self.paused = False
        if self.mode == 'unlimited_firepower':
            self.schedule_interval(self.update, random.random() * 0.15 + 0.075)
        else:
            self.schedule_interval(self.update, random.random() * 0.2 + 0.1)

    def update(self, dt): # difference in time between updates
        if not self.paused:
            arena = self.parent.parent
            snake = arena.snake  # The main snake?
            self.check_kill(snake)  # Check for eating food
            for s in arena.enemies:  # Check for killing enemies
                self.check_kill(s)

    def check_kill(self, snake):  # 'self' is the dot itself
        collision_distance = 80 + len(snake.body) * 0.1  # Assume collision distance increases by 0.2 for each body part added
        if (not self.killed and not snake.is_dead) and (
                abs(snake.x - self.x) < collision_distance and abs(snake.y - self.y) < collision_distance
        ):
            # Eat the food, reduce by length
            self.killed = True
            self.killer = snake
            is_killed_by_player = not snake.is_enemy
            self.do(MoveTo(snake.position, 0.2) + CallFuncS(kill))

