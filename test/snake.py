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
import define
from account import insert_account, update_score, match_user_information, get_ranking, change_cust, change_music, change_volume, change_evolume, current_state, change_cmode

class SnakeSkin:
    def __init__(self, name, color):
        self.name = name
        self.color = color

class SkinManager:
    def __init__(self, username):
        # Initialize a list of possible snake skins with their names and colors
        self.skins = [
            SnakeSkin('LitterBrotherSnake', (0, 0, 0)),
            SnakeSkin('FireSnake', (255, 0, 0)), 
            SnakeSkin('IceSnake', (0, 0, 255)),
            SnakeSkin('MagicSnake', random.choice(define.ALL_COLOR))
        ]
        
        # Store the username of the snake's player
        self.username = username
        # Set the current skin based on the username
        self.current_skin = self.get_current_skin(self.username)

    def get_current_skin(self, username):
        """
        Determine the current skin for the snake based on the user's saved preferences.
        """
        # Retrieve the custom number (index for skin) for the given username
        cust_number = self.get_current_cust_number(username)
        # Return the skin object corresponding to the custom number
        return self.skins[cust_number]

    def get_current_cust_number(self, username):
        """
        Fetch the current customization number (index) from the user's saved state.
        """
        # Obtain the current state, which includes the custom skin number
        state = current_state(username)
        print(f"Current state: {state}")
        
        # Default to the first skin if the state is None, not a list/tuple, or too short
        if state is None or not isinstance(state, (list, tuple)) or len(state) < 10:
            return 0  # If state is None or not long enough, default to 0
            
        # Extract the custom number from the state
        cust_number = state[9]
        print(f"Current cust_number: {cust_number}")
        
        # Default to the first skin if no custom number is found
        if cust_number is None:
            cust_number = 0  # Default to 0 if no custom skin
            change_cust(self.username, 0)  # Update the state if no custom skin is defined
            
        return int(cust_number)  # Return the custom number as an integer


class Snake(cocos.cocosnode.CocosNode):
    no = 0

    def __init__(self, username, is_enemy=False, mode='classic'):
        super(Snake, self).__init__()

        # Game mode can affect certain properties of the snake
        self.mode = mode
        # Speed multiplier adjusts based on the game mode
        self.speed_multiplier = 1.2 if self.mode == 'unlimited_firepower' else 1

        # Initialize basic snake properties
        self.score = None
        self.length = None
        self.body = None
        self.speed = 0
        self.updated_speed = 0
        self.is_dead = False
        self.paused = False
        self.angle = random.randrange(360)  # Current angle of the snake
        self.angle_dest = self.angle  # Target angle the snake is turning towards
        self.username = username

        # If the snake is not an enemy, set up its skin and color
        if not is_enemy:
            self.skin_manager = SkinManager(self.username)
            self.color = self.skin_manager.current_skin.color
        else:
            # Randomly assign a color if it's an enemy snake
            self.color = random.choice(define.ALL_COLOR)

        # Increment the count of snakes
        Snake.no += 1

        # Set the initial position of the snake if it is not an enemy
        if not is_enemy:
            self.position = random.randrange(define.WIDTH // 2 - 100, define.WIDTH // 2 + 100), \
                random.randrange(define.HEIGHT // 2 - 50, define.HEIGHT // 2 + 50)

        self.is_enemy = is_enemy

        # Create the snake's head sprite with the assigned color
        self.head = Sprite('circle.png', color=self.color)
        self.scale = 0.375  # Adjust scale based on pixel size (higher scale for lower resolution)

        # Create the left eye
        eye = Sprite('circle.png')
        eye.x = 15  # Offset for the eye from center
        eye.y = 15
        eye.scale = 0.375
        eyeball = Sprite('circle.png', color=define.BLACK)
        eyeball.scale = 0.375
        eye.add(eyeball)
        self.head.add(eye)

        # Create the right eye
        eye = Sprite('circle.png')
        eye.x = 15
        eye.y = -15
        eye.scale = 0.375
        eyeball = Sprite('circle.png', color=define.BLACK)
        eyeball.scale = 0.375
        eye.add(eyeball)
        self.head.add(eye)

        # Add head to the snake's sprite group
        self.add(self.head)

        # Set initial speed based on the game mode
        if self.mode == 'easy':
            self.init_speed = 100
        elif self.mode == 'classic':
            self.init_speed = 150
        elif self.mode == 'hard':
            self.init_speed = 250
        elif self.mode == 'unlimited_firepower':
            self.init_speed = 150
        if not is_enemy:
            self.init_speed += 30  # Increase speed for player-controlled snakes

        # Calculate the updated speed based on the multiplier
        self.updated_speed = self.init_speed * self.speed_multiplier
        self.speed = self.updated_speed

        # Initialize the path where the snake has been
        self.path = [self.position] * 100

        # Schedule regular updates for the snake's movement
        self.schedule(self.update)
        # If an enemy, schedule AI behavior updates at random intervals
        if self.is_enemy:
            self.schedule_interval(self.ai, random.random() * 0.1 + 0.05)


    def init_enemy_position(self):
        safe_distance = 300  # safe distance
        max_attempts = 100  # Maximum number of attempts to avoid infinite loops
        for _ in range(max_attempts):
            potential_position = random.randrange(100, define.WIDTH - 100), \
                random.randrange(100, define.HEIGHT - 100)
            # print("potential position: ", potential_position[0], potential_position[1])  # Added print statement
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
                break  # found a safe location

    def add_body(self):
        # Create a new body part
        new_body_part = Sprite('circle.png', color=self.color)
        new_body_part.position = self.position  # Place the new body part at the current location of the snake's head

        # Add new body part to draw list
        # Use a calculated z-index to ensure that the snake body parts are drawn in the correct order
        if self.x == 0:
            print(self.position)
        new_body_part.position = self.position
        try:
            new_body_part.scale = 0.375 + (self.score - 30) * 0.0005  # self.head.scale
            self.parent.batch.add(new_body_part, 999 + 100 * self.no - len(self.body))
        except:
            print(999 + 100 * self.no - len(self.body))

        # Updated snake body list to include new body parts
        # """
        if not self.is_enemy:
            # print(new_body_part.scale)
            # print("player's body extended")
            pass
        # """
        self.body.append(new_body_part)
        # Update header size
        self.head.scale += 0.0075  # Assume that head size increases by a ratio of 0.0125 for each body part <-16 pixels

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

        # Update body position
        base_lag = 6  # base interval
        increment_per_length = 0.0001  # The amount by which the interval increases for each additional unit of body length
        smooth_factor = 0.1  # Smoothing factor, used to smooth the growth of intervals

        # Calculate the current total interval increment, using smoothing factors to reduce mutations
        total_increment = increment_per_length * len(self.body) * smooth_factor

        # Dynamically adjust the density of path records based on the length of the snake
        path_record_frequency = int(1 + len(self.body) / 10)  # Assume that every time the snake body increases by 5 units, the frequency of path recording increases
        if len(self.path) % path_record_frequency == 0:
            self.path.append(self.position)

        for i, b in enumerate(self.body):
            # Calculate the actual separation of each body part using the smoothed total separation delta
            lag = base_lag + total_increment * (i / len(self.body))
            idx = (i + 1) * int(lag)
            if len(self.path) > idx:
                b.position = self.path[-idx]

            new_scale = 0.375 + (self.score - 30) * 0.0005  # Assume that for every additional point, scale increases by 0.0015
            b.scale = new_scale

        # Make sure the path length accommodates the increase in body length
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
            if self.mode == 'easy':
                self.speed = self.updated_speed + math.sqrt((self.score - 30)) * 1.5
            elif self.mode == 'classic':
                self.speed = self.updated_speed + math.sqrt((self.score - 30)) * 2
            elif self.mode == 'hard':
                self.speed = self.updated_speed + math.sqrt((self.score - 30)) * 2.5
            elif self.mode == 'unlimited_firepower':
                self.speed = self.updated_speed + math.sqrt((self.score - 30)) * 2
        else:
            if self.mode == 'easy':
                self.speed = self.updated_speed + math.sqrt((self.score - 30)) * 1.5
            elif self.mode == 'classic':
                self.speed = self.updated_speed + math.sqrt((self.score - 30)) * 2
            elif self.mode == 'hard':
                self.speed = self.updated_speed + math.sqrt((self.score - 30)) * 2.5
            elif self.mode == 'unlimited_firepower':
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

        # adjust the score increasing ratio according to the difficulty/mode
        if self.mode == 'easy':
            self.score += s * 1
        elif self.mode == 'classic':
            self.score += s * 2
        elif self.mode == 'hard':
            self.score += s * 3
        elif self.mode == 'unlimited_firepower':
            self.score += s * 1

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
	    # If either snake is already marked as dead, exit the function to avoid further processing
	    if self.is_dead or other.is_dead:
	        return
	
	    # Check if the snake's head has moved out of the defined game boundaries
	    if (self.x < 0 or self.x > define.WIDTH) or (
	            self.y < 0 or self.y > define.HEIGHT):
	        self.crash(None)  # Initiate crash logic if the snake hits the boundary
	        return
	
	    # Commented out: Previous version of the collision detection logic
	    """
	    collision_distance = 24 + len(self.body) * 0.5  # Assuming each additional body part increases collision distance by 0.5
	    for b in other.body:
	        dis = math.sqrt((b.x - self.x) ** 2 + (b.y - self.y) ** 2)
	        if dis < collision_distance:
	            self.crash()
	            return
	    """
	
	    # Loop through each body part of the other snake
	    for b in other.body:
	        # Base size of the snake parts' images is 16 pixels in the original design
	        base_size = 16
	        # Calculate the actual radii of the snake's head and the body part it might collide with
	        head_radius = (self.head.scale * base_size) / 2
	        body_radius = (b.scale * base_size) / 2
	        # Collision distance is the sum of the radii of the snake head and the body part
	        collision_distance = head_radius + body_radius
	
	        # Calculate the distance between the snake's head and the body part of the other snake
	        dis = math.sqrt((b.x - self.x) ** 2 + (b.y - self.y) ** 2)
	        if dis < collision_distance:
	            self.crash(other)  # Initiate crash logic if a collision is detected
	            return

    
	def crash(self, other):
	    # Check if the snake is already dead to avoid processing the death multiple times
	    if not self.is_dead:
	        self.is_dead = True  # Mark the snake as dead
	
	        # Unschedule the update and AI methods to stop the snake's movement and AI behavior
	        self.unschedule(self.update)
	        self.unschedule(self.ai)
	
	        arena = self.parent  # Get the arena where the snake is located
	
	        # Convert the snake's body parts into dots that remain in the arena after death
	        for b in self.body:
	            arena.batch.add(Dot(b.position, b.color))
	            arena.batch.add(Dot(b.position, b.color))
	            arena.batch.remove(b)  # Remove the actual body part from the rendering batch
	
	        print("1")  # Debugging print statement
	
	        # Remove the snake from the arena
	        arena.remove(self)
	
	        # If the game mode is 'unlimited_firepower', add a new enemy snake
	        if self.mode == 'unlimited_firepower':
	            arena.add_enemy()
	
	        # Clear the path array to free up memory and other resources
	        del self.path
	
	        print("2")  # Debugging print statement
	        print(f"self.is_enemy: {self.is_enemy}")  # Output whether the snake is an enemy
	
	        # Specific handling if the snake is an enemy
	        if self.is_enemy:
	            arena.enemies.remove(self)  # Remove the snake from the list of enemies
	            print("3")  # Debugging print statement
	
	            self.parent.kills += 1  # Increment the kill count of the player
	            print("   ###   You has slain an enemy!!!")  # Celebration message
	
	            # If the game mode is not 'unlimited_firepower' and the player has killed enough enemies:
	            if self.mode != 'unlimited_firepower' and self.parent.kills == 20:
	                print("4")  # Debugging print statement
	                arena.parent.end_game()  # End the game if conditions are met
	
	            # Clean up the body list and delete the snake object to free up resources
	            del self.body
	            del self
	
	        else:
	            # If the snake is not an enemy (i.e., the player's snake), end the game
	            arena.parent.end_game()



'''
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
            if self.mode == 'unlimited_firepower':
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
            print("1")
            arena.remove(self)
            if self.mode == 'unlimited_firepower':
                arena.add_enemy()  # If mode is 'unlimited_firepower', add new enemy snake
            del self.path
            print("2")
            print(f"self.is_enemy: {self.is_enemy}")  # Output the value of self.is_enemy
            if self.is_enemy:
                arena.enemies.remove(self)
                print("3")

                self.parent.kills += 1
                print("   ###   You has slain an enemy!!!")
                if self.mode != 'unlimited_firepower' and self.parent.kills == 20:
                    # If it is not 'unlimited_firepower' mode and the number of snakes killed is equal to PLAYERS_NUM, the game will end
                    
                    print("4")
                                        
                    arena.parent.end_game()
                del self.body
                del self
            else:
                arena.parent.end_game()

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
            print("1")
            arena.remove(self)
            if self.mode == 'unlimited_firepower':
                arena.add_enemy()  # If mode is 'unlimited_firepower', add new enemy snake
            del self.path
            print("2")
            print(f"self.is_enemy: {self.is_enemy}")  # Output the value of self.is_enemy
            if self.is_enemy:
                arena.enemies.remove(self)
                print("3")
                if not other == None:
                    print(f"other.is_enemy: {other.is_enemy}")  # Output the value of other.is_enemy
                if not other == None and other.is_enemy:
                    self.parent.kills += 1
                    print("   ###   You has slain an enemy!!!")
                    if self.mode != 'unlimited_firepower' and self.parent.kills == PLAYERS_NUM:
                    # If it is not 'unlimited_firepower' mode and the number of snakes killed is equal to PLAYERS_NUM, the game will end
                        del self.body
                        print("4")
                        del self                    
                        arena.parent.end_game()
                del self.body
                del self
            else:
                arena.parent.end_game()




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
            print("1")
            arena.remove(self)
            if self.mode == 'unlimited_firepower':
                arena.add_enemy()  # If mode is 'unlimited_firepower', add new enemy snake
            del self.path
            print("2")
            if self.is_enemy:
                arena.enemies.remove(self)
                print("3")
                if not other == None and other.is_enemy:
                    self.parent.kills += 1

                    print("   ###   You has slain an enemy!!!")
                    if self.mode != 'unlimited_firepower' and self.parent.kills == 1:
                        # If it is not 'unlimited_firepower' mode and the number of snakes killed is equal to PLAYERS_NUM, the game will end
                        del self.body
                        print("1")
                        del self                    
                        arena.parent.end_game()
                del self.body
                del self
            else:
                arena.parent.end_game()

'''






