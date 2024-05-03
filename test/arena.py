import cocos
from cocos.director import director

import define
from snake import Snake
from dot import Dot
import random
import string
from account import update_score

class Arena(cocos.layer.ColorLayer):
    is_event_handler = True  # This makes the class capable of handling events like keyboard inputs.

    def __init__(self, parent, username, mode):
        # Initialize the Arena as a ColorLayer with a white background
        super(Arena, self).__init__(250, 255, 255, 255, define.WIDTH, define.HEIGHT)

        self.mode = mode
        self.parent = parent
        self.food_limit = 200  # Maximum number of food dots allowed at one time
        self.current_food_count = 0  # Current number of food dots

        initial_food_count = 50  # Default initial number of food dots
        if self.mode == 'unlimited_firepower':
            initial_food_count = 150  # Increased initial food for this mode

        # Set food limit based on the game mode
        if self.mode == 'easy':
            self.food_limit = 150
        elif self.mode == 'classic':
            self.food_limit = 100
        elif self.mode == 'hard':
            self.food_limit = 50
        elif self.mode == 'unlimited_firepower':
            self.food_limit = 200

        # Calculate center of the screen
        self.center = (cocos.director.get_window_size()[0] / 2, cocos.director.get_window_size()[1] / 2)
        self.batch = cocos.batch.BatchNode()  # A batch node to manage multiple children as a single drawing operation
        self.add(self.batch)

        # Initialize the player's snake
        self.snake = Snake(username, mode=self.mode)
        self.add(self.snake, 10000)  # Add with a high z-order to ensure it's drawn on top
        self.snake.init_body()

        self.kills = 0  # Number of enemy snakes killed by the player

        self.enemies = []
        # Add enemy snakes
        for i in range(define.PLAYERS_NUM - 1):
            self.add_enemy()

        self.keys_pressed = set()  # Track keys pressed for controlling the snake

        # Adjust initial food count based on the game mode
        for _ in range(min(initial_food_count, self.food_limit)):
            self.add_food()

        self.schedule(self.update)  # Schedule regular updates

    def add_enemy(self):
        # Generate a random username for enemy snakes
        username = 'Enemy_' + ''.join(random.choices(string.ascii_letters + string.digits, k=5))
        enemy = Snake(username, mode=self.mode, is_enemy=True)
        self.add(enemy, 10000)
        enemy.init_enemy_position()
        enemy.init_body()
        self.enemies.append(enemy)

    def pause_dots(self):
        # Pause all food dots
        for child in self.batch.children:
            if isinstance(child, Dot):
                child.paused = True

    def resume_dots(self):
        # Resume all food dots
        for child in self.batch.children:
            if isinstance(child, Dot):
                child.paused = False

    def pause_game(self):
        # Pause the game update loop and all game elements
        self.unschedule(self.update)
        self.snake.pause()
        for enemy in self.enemies:
            enemy.pause()
        self.pause_dots()

    def resume_game(self):
        # Resume the game update loop and all game elements
        self.schedule(self.update)
        self.snake.resume()
        for enemy in our.enemies:
            enemy.resume()
        self.resume_dots()

    def update(self, dt):
        # Update game state, called regularly by the scheduler
        if not self.parent.paused:
            # Center the arena on the snake
            self.x = self.center[0] - self.snake.x
            self.y = self.center[1] - self.snake.y

    def on_key_press(self, key, modifiers):
        # Handle key press events
        if not self.parent.paused:
            self.keys_pressed.add(key)
            self.snake.update_angle(self.keys_pressed)

    def on_key_release(self, key, modifiers):
        # Handle key release events
        if not self.parent.paused:
            self.keys_pressed.discard(key)
            self.snake.update_angle(self.keys_pressed)

    def get_scores(self):
        # Collect scores from all snakes
        scores = [(self.snake.username, self.snake.score)]
        scores.extend(('Enemy {}'.format(i + 1), enemy.score) for i, enemy in enumerate(self.enemies))
        return scores

   def add_food(self):
        # Add a food dot to the game if below the food limit
        if self.current_food_count < self.food_limit:
            self.batch.add(Dot(mode=self.mode))  # Add a new Dot to the batch
            self.current_food_count += 1  # Increment the food count


