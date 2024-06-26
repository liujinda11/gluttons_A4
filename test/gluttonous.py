import cocos
from cocos.director import director
from cocos.scene import Scene
from cocos.layer import Layer, ColorLayer
from cocos.text import Label
from cocos.menu import Menu, MenuItem, EntryMenuItem, zoom_in, zoom_out
from cocos.actions import CallFunc
import pyglet
from pyglet.window import key
from pyglet.text import Label
import os
import pygame
import define
from arena import Arena
from gameover import Gameover
from snake import SkinManager
from account import current_state,change_cmode,change_music,change_volume,change_evolume, get_ranking,match_user_information,change_cust,insert_account,update_score



class GameStartScene(Scene):
    """
    This class defines the start scene for a game, handling the initial UI
    setup, animations, and transitions based on user inputs.
    """
    def __init__(self):
        # Initialize the parent Scene class
        super(GameStartScene, self).__init__()

        print("Game Start Scene...\n\n\n")

        # Labels for start and exit instructions
        self.start_label = None
        self.exit_label = None

        # Initialize the background and labels
        self.setup_background()
        self.setup_labels()

        # Setup a keyboard handler to track key states
        self.keys = pyglet.window.key.KeyStateHandler()
        cocos.director.director.window.push_handlers(self.keys)

        # Schedule periodic tasks
        self.schedule_interval(self.update_label_visibility, 0.5)
        self.schedule(self.check_input)

    def setup_background(self):
        """Set up the background image for the scene."""
        screen_width, screen_height = cocos.director.director.get_window_size()
        background_sprite = cocos.sprite.Sprite("background.jpg")
        # Adjust background image to fill screen
        background_sprite.scale_x = screen_width / background_sprite.width
        background_sprite.scale_y = screen_height / background_sprite.height
        background_sprite.position = screen_width / 2, screen_height / 2
        self.add(background_sprite, z=0)

    def setup_labels(self):
        """Create and place labels on the scene."""
        screen_width, screen_height = cocos.director.director.get_window_size()
        # Main game title
        self.create_label('Genshin Impact',
                          144,
                          (0, 255, 0, 255),
                          screen_width / 2,
                          screen_height * 3 / 5,
                          'Comic Sans MS',
                          True)
        # Start game instruction
        self.start_label = self.create_label('press space key to start',
                                             48,
                                             (127, 255, 255, 255),
                                             screen_width / 2,
                                             screen_height / 4,
                                             'Arial',
                                             False)
        # Exit game instruction
        self.exit_label = self.create_label('or press esc key to exit',
                                            48,
                                            (127, 255, 255, 255),
                                            screen_width / 2,
                                            screen_height * 3 / 16,
                                            'Arial',
                                            False)

    def create_label(self, text, font_size, color, x, y, font_name=None, bold=None):
        """Helper function to create a label."""
        label = cocos.text.Label(text,
                                 font_size=font_size,
                                 font_name=font_name,
                                 color=color,
                                 bold=bold,
                                 anchor_x='center',
                                 anchor_y='center',
                                 x=x,
                                 y=y)
        self.add(label)
        return label

    def update_label_visibility(self, dt):
        """Toggle visibility of labels to create a blinking effect."""
        self.start_label.visible = not self.start_label.visible
        self.exit_label.visible = not self.exit_label.visible
        self.check_start_game()

    def check_input(self, dt):
        """Check for key inputs to transition scenes or execute actions."""
        self.check_start_game()

    def check_start_game(self):
        """Check if the start game key (SPACE) is pressed."""
        if self.keys[pyglet.window.key.SPACE]:
            # Transition to the authentication scene
            auth_scene = AuthScene()
            cocos.director.director.replace(auth_scene)
            self.stop_scheduler()  # Stop scheduled tasks upon scene change

    def stop_scheduler(self):
        """Unschedule all scheduled tasks."""
        self.unschedule(self.update_label_visibility)
        self.unschedule(self.check_input)
        self.unschedule(self.check_start_game)

class AuthScene(cocos.scene.Scene):
    def __init__(self):
        super().__init__()

        # Creating background sprites
        background = cocos.sprite.Sprite('background.jpg')
        background.position = (cocos.director.director.get_window_size()[0] // 2, cocos.director.director.get_window_size()[1] // 2)
        background.opacity = 50  # Set the background transparency to 50
        self.add(background, z=0)

        # Creating title tags
        title_label = cocos.text.Label('HELLOW!', font_name='Arial', font_size=64, anchor_x='center', anchor_y='center')
        title_label.position = (cocos.director.director.get_window_size()[0] // 2, cocos.director.director.get_window_size()[1] * 0.8)
        self.add(title_label, z=1)

        # add AuthLayer
        self.add(AuthLayer(), z=2)

# this 2 classes is to display the login/register page
class AuthLayer(cocos.menu.Menu):
    """
    AuthLayer is a subclass of cocos.menu.Menu, which provides a menu interface for user authentication options.
    """
    def __init__(self):
        super().__init__(" ")
	
        # Define menu items with their corresponding callback functions
        items = [
            cocos.menu.MenuItem('Login', self.login),
            cocos.menu.MenuItem('Register', self.register),
            cocos.menu.MenuItem('Guest Access', self.guest),
            cocos.menu.MenuItem('Exit the game', self.quit)
        ]
        
        # Create the menu with special effects for item selection and deselection
        self.create_menu(items, cocos.menu.shake(), cocos.menu.shake_back())

    def login(self):
        """
        Transition to the login authentication method scene.
        """
        auth_method_scene = cocos.scene.Scene(AuthMethodLayer('login'))
        cocos.director.director.replace(auth_method_scene)

    def register(self):
        """
        Transition to the registration authentication method scene.
        """
        auth_method_scene = cocos.scene.Scene(AuthMethodLayer('register'))
        cocos.director.director.replace(auth_method_scene)

    def guest(self):
        """
        Continue as a guest user, transitioning to the homepage scene.
        """
        print("Continue as Guest selected...\n")
        homepage_scene = HomepageScene('','guest')
        cocos.director.director.replace(homepage_scene)

    def quit(self):
        """
        Exit the menu and return to the previous scene.
        """
        print("Exit from user auth option scene...\n")
        cocos.director.director.pop()


class AuthMethodLayer(cocos.layer.Layer):
    """
    AuthMethodLayer handles the specific authentication method either for login or registration.
    """
    def __init__(self, type_):
        super().__init__()
        
        # Setup the background with semi-transparency
        background = cocos.sprite.Sprite('background.jpg')
        background.position = (cocos.director.director.get_window_size()[0] // 2, cocos.director.director.get_window_size()[1] // 2)
        background.opacity = 50  # Set the background transparency to 50
        self.add(background, z=0)

        # Setup the title label for the authentication layer
        title_label = cocos.text.Label('Authentication', font_name='Arial', font_size=64, anchor_x='center', anchor_y='center')
        title_label.position = (cocos.director.director.get_window_size()[0] // 2, cocos.director.director.get_window_size()[1] * 0.8)
        self.add(title_label, z=1)

        # Add the menu for the authentication method
        self.add(AuthMethodMenu(type_), z=2)

#In this class, we define the interface we need in login/register page
class AuthMethodMenu(Menu):
    def __init__(self, entry_type):
        super(AuthMethodMenu, self).__init__()

        menu_items = None

        self.username = EntryMenuItem('Username:', self.on_username_enter, '')
        self.password = EntryMenuItem('Password:', self.on_password_enter, '')
        self.back_button = MenuItem('Back', self.on_back_pressed)

        if entry_type == 'login':
            self.login_button = MenuItem('Login', self.on_login_pressed)
            menu_items = [self.username, self.password, self.login_button, self.back_button]
        elif entry_type == 'register':
            self.register_button = MenuItem('Register', self.on_register_pressed)
            menu_items = [self.username, self.password, self.register_button, self.back_button]

        self.create_menu(menu_items)
	
    def on_username_enter(self, value):
        self.entered_username = value

    def on_password_enter(self, value):
        self.entered_password = value

    def on_login_pressed(self):
        username = self.entered_username
        password = self.entered_password

        # check whether the account input by user exist in database (the functions we used here are defined in account.py)
        if match_user_information(username, password):
            # if it is valid,transform to Main menu
            homepage_scene = HomepageScene(username, 'regular')  # assume that the succesful login called 'regular'
            director.replace(homepage_scene)
        else:
            # else, we output warning message
            print("Invalid username or password. Please try again.")

    def on_register_pressed(self):
        username = self.entered_username
        password = self.entered_password

        # store the new account into the database
        insert_account(username, password)

        # transforme to Main menu
        homepage_scene = HomepageScene(username,'regular' )  # Assuming that the user type registered successfully is 'regular'
        director.replace(homepage_scene)

    def on_back_pressed(self):
        # Handle returning to the previous menu
        login_scene = Scene(AuthScene())
        director.replace(login_scene)

class HomepageScene(Scene):
    def __init__(self, username, user_type=None):
        super(HomepageScene, self).__init__()
        self.username = username
        print(f"Received username: {self.username}")
        # Creating background sprites
        background = cocos.sprite.Sprite('background.jpg')
        background.position = (cocos.director.director.get_window_size()[0] // 2, cocos.director.director.get_window_size()[1] // 2)
        background.opacity = 50  # Set the background transparency to 50
        self.add(background, z=0)

        # Creating title tags
        title_label = cocos.text.Label('Homepage', font_name='Arial', font_size=64, anchor_x='center', anchor_y='center')
        title_label.position = (cocos.director.director.get_window_size()[0] // 2, cocos.director.director.get_window_size()[1] * 0.8)
        self.add(title_label, z=1)

	
        main_menu_layer = MainMenu(username, user_type)
        self.add(main_menu_layer,z=2)

class MainMenu(cocos.menu.Menu):
    def __init__(self, username, user_type):
        super(MainMenu, self).__init__()
        self.username = username
        self.user_type = user_type
        print("Home page and main menu...\n\n\n")
        print(f"Received username: {self.username}")
        print(f"Received user_type: {self.user_type}")
        
        #Music playback section
        if self.user_type == 'guest':
            music_file = 'VCR.mp3'
            self.music_volume = 0.5
        else:
            state = current_state(self.username)
            
            if state is not None:
                self.music_volume = state[4]
                

                if state[3] == 0:
                    music_file = 'VCR.mp3'
                else:
                    music_file = 'happy.mp3'
            else:
                self.music_volume = 0.5
                change_volume(self.username,self.music_volume)
                music_file = 'VCR.mp3'
                
                

        pygame.init()
        pygame.mixer.init()
        if os.path.exists(music_file):
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(-1)

	# That we name the buttons in main menu here.    
        main_menu_items = [
            cocos.menu.MenuItem('Easy Mode', lambda: self.select_mode('Easy Mode')),
            cocos.menu.MenuItem('Classic Mode', lambda: self.select_mode('Classic Mode')),

            cocos.menu.MenuItem('Hard Mode', lambda: self.select_mode('Hard Mode')),
            cocos.menu.MenuItem('Unlimited Firepower Mode', lambda: self.select_mode('Unlimited Firepower Mode')),
            cocos.menu.MenuItem('Ranking list', lambda: self.select_mode('Ranking List')),
            cocos.menu.MenuItem('Shop', lambda: self.select_mode('Shop')),
            cocos.menu.MenuItem('Settings', lambda: self.select_mode('Settings')),
            cocos.menu.MenuItem('Log out', lambda: self.select_mode('Log out'))
        ]

        if user_type == 'guest':
            print("66666")
            main_menu_items = [item for item in main_menu_items if item.label not in ('Ranking list', 'Shop','Settings','Easy Mode','Hard Mode','Unlimited Firepower Mode')]
        else:
            print("?")

        self.create_menu(main_menu_items)

    def select_mode(self, mode_name):
        print(f"Selected item: {mode_name}...")
        if mode_name == 'Classic Mode':
            classic_mode_scene = cocos.scene.Scene(ClassicMode(self.username, self.user_type))
            cocos.director.director.replace(classic_mode_scene)
        elif mode_name == 'Easy Mode':
            easy_mode_scene = cocos.scene.Scene(EasyMode(self.username, self.user_type))
            cocos.director.director.replace(easy_mode_scene)
        elif mode_name == 'Hard Mode':
            hard_mode_scene = cocos.scene.Scene(HardMode(self.username, self.user_type))
            cocos.director.director.replace(hard_mode_scene)
        elif mode_name == 'Unlimited Firepower Mode':
            unlimited_firepower_mode_scene = cocos.scene.Scene(UnlimitedFirepowerMode(self.username, self.user_type))
            cocos.director.director.replace(unlimited_firepower_mode_scene)
        elif mode_name == 'Ranking List':
            ranking_list_scene = cocos.scene.Scene(RankingList(self.username, self.user_type))
            cocos.director.director.replace(ranking_list_scene)
        elif mode_name == 'Shop':
            shop_scene = cocos.scene.Scene(商店(self.username, self.user_type))
            cocos.director.director.replace(shop_scene)
        elif mode_name == 'Settings':
            pygame.mixer.music.stop()
            settings_scene = cocos.scene.Scene(设置(self.username, self.user_type))
            cocos.director.director.replace(settings_scene)
        elif mode_name == 'Log out':
            pygame.mixer.music.stop()
            auth_scene = cocos.scene.Scene(AuthScene())
            cocos.director.director.replace(auth_scene)
            print('Log out...\n')

    def on_quit(self):
        print("Returning to GameStartScene from MainMenu by ESC...\n.")
        init = GameStartScene()
        cocos.director.director.replace(init)
	    
class ClassicMode(cocos.layer.Layer):  # The logic of other game modes is the same as here and no special explanation there.
    """
    The Classic Mode of the game.
    """
	
    is_event_handler = True

    def __init__(self, username, user_type):
	"""
        Initializes the ClassicMode object.

        Args:
            username (str): The username of the player.
            user_type (str): The type of user, e.g., 'guest' or 'registered'.
        """
        super(ClassicMode, self).__init__()
        self.username = username
        self.user_type = user_type

        print("Classic Mode...\n\n\n")
	# Create the arena for the game.
        self.arena = Arena(self, username,'classic')
        self.add(self.arena, 100)

	# Configure the background for displaying scores.
        scores_background_color = define.CUSTOMIZED_PINK
        scores_background_margin = 300  # 背景边距
        scores_background_height = define.PLAYERS_NUM * 28 + 2 * scores_background_margin + 120  # Increase background height to accommodate how-to guides
        scores_background_width = 550

        scores_background = cocos.layer.ColorLayer(*scores_background_color,
                                                   width=scores_background_width,
                                                   height=scores_background_height)
        scores_background.position = (0, 1600 - scores_background_height + scores_background_margin)
        self.add(scores_background, 900)

	# Labels for displaying game status and scores.
        self.your_status_label = cocos.text.Label('    Classic Mode',
                                                  font_name='Arial',
                                                  font_size=48,
                                                  color=define.MAROON)
        self.your_status_label.position = 25, 1525
        self.add(self.your_status_label, 1000)

        self.your_status_label = cocos.text.Label('         Your Status',
                                                  font_name='Arial',
                                                  font_size=36,
                                                  color=define.CUSTOMIZED_RED)
        self.your_status_label.position = 25, 1475
        self.add(self.your_status_label, 1000)

        self.ks_label = cocos.text.Label('',
                                         font_name='Courier New',
                                         font_size=24,
                                         color=define.CUSTOMIZED_ORANGE)
        self.ks_label.position = 25, 1425
        self.add(self.ks_label, 1000)

        self.scores_and_rank_label = cocos.text.Label('       Scores & Rank',
                                                      font_name='Arial',
                                                      font_size=36,
                                                      color=define.CUSTOMIZED_RED)
        self.scores_and_rank_label.position = 25, 1350
        self.add(self.scores_and_rank_label, 1000)

        self.sr_labels = []
        for i in range(define.PLAYERS_NUM):
            label = cocos.text.Label(f'Player {i + 1}:',
                                     font_name='Courier New',
                                     font_size=24,
                                     color=define.CUSTOMIZED_ORANGE)
            label.position = 25, 1300 - i * 28
            self.add(label, 1000)
            self.sr_labels.append(label)

        # Adding how-to guides to reports
        self.guide_label = cocos.text.Label(
                                            'Classic Mode, Classic Snake!\n'
                                            'Using Direction Keys to Control,\n'
                                            'Press SPACE to Pause',
                                            font_name='Arial',
                                            font_size=18,
                                            color=(255, 0, 0, 255),  # red font
                                            width=scores_background_width - 40,
                                            multiline=True,
                                            anchor_x='left',
                                            anchor_y='bottom')
        self.guide_label.position = 25, 600
        self.add(self.guide_label, 1000)

        # Initialize player status.
	self.player_kills = 0
        self.player_speed = 0
        self.update_report()

	# Initialize game over screen.
        self.gameover = Gameover(self.username)
        self.add(self.gameover, 2000)

        self.pause_menu = None
        self.paused = False

	# Register keyboard events.
        self.keyboard = key.KeyStateHandler()
        director.window.push_handlers(self.keyboard)    

    def update_report(self):
	"""
        Update the report of player status and scores.
        """
	# Update player kills and speed from the arena
        self.player_kills = self.arena.kills
        self.player_speed = self.arena.snake.speed

	# Update the label showing player's life and speed
        self.ks_label.element.text = f" Your life: 1 | Speed: {int(self.player_speed)}"

	# Retrieve scores from the arena and sort them
        scores = self.arena.get_scores()
        scores.sort(key=lambda x: x[1], reverse=True)

	# Determine the maximum widths for rank, name, and score
        max_rank_width = len(str(max(i + 1 for i in range(len(scores)))))
        max_name_width = max(len(name) for name, _ in scores)
        max_score_width = max(len(f"Score: {score}") for _, score in scores)

	# Update score labels with formatted data
        for i, (name, score) in enumerate(scores):
            rank = i + 1
            formatted_rank = str(rank).rjust(max_rank_width)
            formatted_name = name.ljust(max_name_width)
            formatted_score = f"Score: {score}".ljust(max_score_width)

            if i < len(self.sr_labels):
                self.sr_labels[i].element.text = f"{formatted_rank} | {formatted_name} | {formatted_score}"

    def end_game(self):
	"""
	End the game and display final scores.
	 """
	# Set game over state and display final score
        self.paused = False
        self.gameover.visible = True

        self.current_score = self.arena.snake.score

	# Set record score based on current user type
        if self.user_type == 'guest':
            self.record_score = 0
        else:
            self.record_score = current_state(self.username)[2]
            if self.record_score is None:
                self.record_score = 0

	# Update record score if current score is higher
        if self.current_score >= self.record_score:
            self.record_score = self.current_score
            if self.user_type != 'guest':
                update_score(self.username, self.current_score)

	# Update gameover screen with scores and pause game
        self.gameover.score.element.text = str(self.current_score)
        self.gameover.record_score.element.text = str(self.record_score)
        self.arena.pause_game()

    def on_mouse_press(self, x, y, buttons, modifiers):
	"""
  	Handle mouse press events.
	"""
	# Restart game if game over, otherwise print message
        if self.gameover.visible:
            self.gameover.visible = False
            self.arena.unschedule(self.arena.update)
            self.remove(self.arena)
            self.arena = Arena(self, self.username)  # 将username传递给Arena
            self.add(self.arena)
            self.update_report()
        else:
            print('   ###   only when you die can you remake...')

    def toggle_pause(self):
	"""
  	Toggle the pause state of the game.
	"""
	# Toggle pause state and manage PauseMenu
        if self.paused:
            print(" # resume\n")
        # Check if PauseMenu is a child node of the current layer
            if self.pause_menu in self.get_children():
                self.paused = False
                self.remove(self.pause_menu)
                self.pause_menu = None
                self.arena.resume_game()
        else:
            print(" # pause")
            print("111")
            if self.pause_menu is None:
                self.paused = True
                self.pause_menu = PauseMenu(self.username, self.user_type)  # Make sure the PauseMenu is created the right way, and pass the username.
                self.add(self.pause_menu, z=500)
                self.arena.pause_game()

    def on_key_press(self, key, modifiers):
	"""
  	Handle key press events.
	"""
        if not self.gameover.visible:
	# Handle key presses during gameplay
            if key == pyglet.window.key.SPACE:
                print("Space - Toggle Pause")
                self.toggle_pause()
                return True
            elif key == pyglet.window.key.J:
                print("J - Restart Game...\n")
                self.restart_game()
                return True
            elif key == pyglet.window.key.BACKSPACE:
                print("Backspace - Back to Homepage...\n")
                if self.pause_menu:
                    self.remove(self.pause_menu)
                    self.pause_menu = None

                homepage_scene = HomepageScene(self.username, self.user_type)  # Pass username to HomepageScene
                cocos.director.director.replace(homepage_scene)
                return True
        else:
	# Handle key presses when game is over
            if key == pyglet.window.key.J:
                print("J - Restart Game (Game Over)...\n")
                self.restart_game()
                return True
            elif key == pyglet.window.key.BACKSPACE:
                print("Backspace - Back to Homepage (Game Over)...\n")
                if self.pause_menu:
                    self.remove(self.pause_menu)
                    self.pause_menu = None
                homepage_scene = HomepageScene(self.username, self.user_type)  # Pass username to HomepageScene
                cocos.director.director.replace(homepage_scene)
                return True

        
    
    def restart_game(self):
	"""
  	Restart the game.
  	"""
        if self.pause_menu:
            self.remove(self.pause_menu)
            self.pause_menu = None

        self.remove(self.arena)
        self.arena = Arena(self, self.username,'classic')  # Pass self and self.username to the initialization method of the Arena class.
        self.add(self.arena)
        self.gameover.visible = False
        self.update_report()
        self.paused = False

class EasyMode(cocos.layer.Layer):  # The game logic is the same as the classic mode, so there will be no further comments here.
    is_event_handler = True

    def __init__(self, username, user_type):
        super(EasyMode, self).__init__()
        self.username = username
        self.user_type = user_type

        print("Easy Mode...\n\n\n")
        self.arena = Arena(self, username, mode='easy')  # Pass username and difficulty to Arena
        self.add(self.arena, 100)

        scores_background_color = define.CUSTOMIZED_PINK
        scores_background_margin = 300  # background margin
        scores_background_height = define.PLAYERS_NUM * 28 + 2 * scores_background_margin + 160
        scores_background_width = 550

        scores_background = cocos.layer.ColorLayer(*scores_background_color,
                                                   width=scores_background_width,
                                                   height=scores_background_height)
        scores_background.position = (0, 1600 - scores_background_height + scores_background_margin)
        self.add(scores_background, 900)

        self.your_status_label = cocos.text.Label('    Easy Mode',
                                                  font_name='Arial',
                                                  font_size=48,
                                                  color=define.MAROON)
        self.your_status_label.position = 25, 1525
        self.add(self.your_status_label, 1000)

        self.your_status_label = cocos.text.Label('         Your Status',
                                                  font_name='Arial',
                                                  font_size=36,
                                                  color=define.CUSTOMIZED_RED)
        self.your_status_label.position = 25, 1475
        self.add(self.your_status_label, 1000)

        self.ks_label = cocos.text.Label('',
                                         font_name='Courier New',
                                         font_size=24,
                                         color=define.CUSTOMIZED_ORANGE)
        self.ks_label.position = 25, 1425
        self.add(self.ks_label, 1000)

        self.scores_and_rank_label = cocos.text.Label('       Scores & Rank',
                                                      font_name='Arial',
                                                      font_size=36,
                                                      color=define.CUSTOMIZED_RED)
        self.scores_and_rank_label.position = 25, 1350
        self.add(self.scores_and_rank_label, 1000)

        self.sr_labels = []
        for i in range(define.PLAYERS_NUM):
            label = cocos.text.Label(f'Player {i + 1}:',
                                     font_name='Courier New',
                                     font_size=24,
                                     color=define.CUSTOMIZED_ORANGE)
            label.position = 25, 1300 - i * 28
            self.add(label, 1000)
            self.sr_labels.append(label)



        # Adding how-to guides to reports
        self.guide_label = cocos.text.Label(
                                            'Easy Mode, Lower Score\n'
                                            'Lower Speed, Less Enemy & Food\n'
                                            'Using Direction Keys to Control,\n'
                                            'Press SPACE to Pause',
                                            font_name='Arial',
                                            font_size=18,
                                            color=(255, 0, 0, 255),  # red font
                                            width=scores_background_width - 40,
                                            multiline=True,
                                            anchor_x='left',
                                            anchor_y='bottom')
        self.guide_label.position = 25, 600
        self.add(self.guide_label, 1000)

        self.player_kills = 0
        self.player_speed = 0
        self.update_report()

        self.gameover = Gameover(self.username)
        self.add(self.gameover, 2000)

        self.pause_menu = None
        self.paused = False

        self.keyboard = key.KeyStateHandler()
        director.window.push_handlers(self.keyboard)

    def update_report(self):
        self.player_kills = self.arena.kills
        self.player_speed = self.arena.snake.speed

        self.ks_label.element.text = f" Your life: 1 | Speed: {int(self.player_speed)}"

        scores = self.arena.get_scores()
        scores.sort(key=lambda x: x[1], reverse=True)

        max_rank_width = len(str(max(i + 1 for i in range(len(scores)))))
        max_name_width = max(len(name) for name, _ in scores)
        max_score_width = max(len(f"Score: {score}") for _, score in scores)

        for i, (name, score) in enumerate(scores):
            rank = i + 1
            formatted_rank = str(rank).rjust(max_rank_width)
            formatted_name = name.ljust(max_name_width)
            formatted_score = f"Score: {score}".ljust(max_score_width)

            if i < len(self.sr_labels):
                self.sr_labels[i].element.text = f"{formatted_rank} | {formatted_name} | {formatted_score}"

    def end_game(self):
        self.paused = False
        self.gameover.visible = True

        self.current_score = self.arena.snake.score
        self.record_score = current_state(self.username)[2]


        if self.record_score is None:
            self.record_score = 0
            

        if self.current_score >= self.record_score:
            self.record_score = self.current_score
            update_score(self.username, self.current_score)

        self.gameover.score.element.text = str(self.current_score)
        self.gameover.record_score.element.text = str(self.record_score)
        self.arena.pause_game()



    def on_mouse_press(self, x, y, buttons, modifiers):
        if self.gameover.visible:
            self.gameover.visible = False
            self.arena.unschedule(self.arena.update)
            self.remove(self.arena)
            self.arena = Arena(self, self.username, mode='easy')  # Pass username and difficulty to Arena
            self.add(self.arena)
            self.update_report()
        else:
            print('   ###   only when you die can you remake...')

    def toggle_pause(self):
        if self.paused:
            print(" # resume\n")
            # 检查PauseMenu是否是当前层的子节点
            if self.pause_menu in self.get_children():
                self.paused = False
                self.remove(self.pause_menu)
                self.pause_menu = None
                self.arena.resume_game()
        else:
            print(" # pause")
            print("111")
            if self.pause_menu is None:
                self.paused = True
                self.pause_menu = PauseMenu(self.username, self.user_type)  # Make sure the PauseMenu is created the right way, and pass the username.
                self.add(self.pause_menu, z=500)
                self.arena.pause_game()

    def on_key_press(self, key, modifiers):
        if not self.gameover.visible:
            if key == pyglet.window.key.SPACE:
                print("Space - Toggle Pause")
                self.toggle_pause()
                return True
            elif key == pyglet.window.key.J:
                print("J - Restart Game...\n")
                self.restart_game()
                return True
            elif key == pyglet.window.key.BACKSPACE:
                print("Backspace - Back to Homepage...\n")
                if self.pause_menu:
                    self.remove(self.pause_menu)
                    self.pause_menu = None

                homepage_scene = HomepageScene(self.username, self.user_type)  # Pass username to HomepageScene
                cocos.director.director.replace(homepage_scene)
                return True
        else:
            if key == pyglet.window.key.J:
                print("J - Restart Game (Game Over)...\n")
                self.restart_game()
                return True
            elif key == pyglet.window.key.BACKSPACE:
                print("Backspace - Back to Homepage (Game Over)...\n")
                if self.pause_menu:
                    self.remove(self.pause_menu)
                    self.pause_menu = None
                homepage_scene = HomepageScene(self.username, self.user_type)  # Pass username to HomepageScene
                cocos.director.director.replace(homepage_scene)
                return True

    def restart_game(self):
        if self.pause_menu:
            self.remove(self.pause_menu)
            self.pause_menu = None

        self.remove(self.arena)
        self.arena = Arena(self, self.username,'easy')  # Pass self and self.username to the initialization method of the Arena class.
        self.add(self.arena)
        self.gameover.visible = False
        self.update_report()
        self.paused = False      

class HardMode(cocos.layer.Layer):  # The game logic is the same as the classic mode, so there will be no further comments here.
    is_event_handler = True

    def __init__(self, username, user_type):
        super(HardMode, self).__init__()
        self.username = username
        self.user_type = user_type

        print("Hard Mode...\n\n\n")
        self.arena = Arena(self, username, mode='hard')  # Pass username and difficulty to Arena
        self.add(self.arena, 100)

        scores_background_color = define.CUSTOMIZED_PINK
        scores_background_margin = 300  # background margin
        scores_background_height = define.PLAYERS_NUM * 28 + 2 * scores_background_margin + 160
        scores_background_width = 550

        scores_background = cocos.layer.ColorLayer(*scores_background_color,
                                                   width=scores_background_width,
                                                   height=scores_background_height)
        scores_background.position = (0, 1600 - scores_background_height + scores_background_margin)
        self.add(scores_background, 900)

        self.your_status_label = cocos.text.Label('    Hard Mode',
                                                  font_name='Arial',
                                                  font_size=48,
                                                  color=define.MAROON)
        self.your_status_label.position = 25, 1525
        self.add(self.your_status_label, 1000)

        self.your_status_label = cocos.text.Label('         Your Status',
                                                  font_name='Arial',
                                                  font_size=36,
                                                  color=define.CUSTOMIZED_RED)
        self.your_status_label.position = 25, 1475
        self.add(self.your_status_label, 1000)

        self.ks_label = cocos.text.Label('',
                                         font_name='Courier New',
                                         font_size=24,
                                         color=define.CUSTOMIZED_ORANGE)
        self.ks_label.position = 25, 1425
        self.add(self.ks_label, 1000)

        self.scores_and_rank_label = cocos.text.Label('       Scores & Rank',
                                                      font_name='Arial',
                                                      font_size=36,
                                                      color=define.CUSTOMIZED_RED)
        self.scores_and_rank_label.position = 25, 1350
        self.add(self.scores_and_rank_label, 1000)
        
        
        # Adding how-to guides to reports
        self.guide_label = cocos.text.Label(
                                            'Hard Mode, More Score\n'
                                            'Higher Speed, More Enemy & Food\n'
                                            'Using Direction Keys to Control,\n'
                                            'Press SPACE to Pause',
                                            font_name='Arial',
                                            font_size=18,
                                            color=(255, 0, 0, 255),  # 红色字体
                                            width=scores_background_width - 40,
                                            multiline=True,
                                            anchor_x='left',
                                            anchor_y='bottom')
        self.guide_label.position = 25, 600
        self.add(self.guide_label, 1000)


        self.sr_labels = []
        for i in range(define.PLAYERS_NUM):
            label = cocos.text.Label(f'Player {i + 1}:',
                                     font_name='Courier New',
                                     font_size=24,
                                     color=define.CUSTOMIZED_ORANGE)
            label.position = 25, 1300 - i * 28
            self.add(label, 1000)
            self.sr_labels.append(label)

        self.player_kills = 0
        self.player_speed = 0
        self.update_report()

        self.gameover = Gameover(self.username)
        self.add(self.gameover, 2000)

        self.pause_menu = None
        self.paused = False

        self.keyboard = key.KeyStateHandler()
        director.window.push_handlers(self.keyboard)

    def update_report(self):
        self.player_kills = self.arena.kills
        self.player_speed = self.arena.snake.speed

        self.ks_label.element.text = f" Your life: 1 | Speed: {int(self.player_speed)}"

        scores = self.arena.get_scores()
        scores.sort(key=lambda x: x[1], reverse=True)

        max_rank_width = len(str(max(i + 1 for i in range(len(scores)))))
        max_name_width = max(len(name) for name, _ in scores)
        max_score_width = max(len(f"Score: {score}") for _, score in scores)

        for i, (name, score) in enumerate(scores):
            rank = i + 1
            formatted_rank = str(rank).rjust(max_rank_width)
            formatted_name = name.ljust(max_name_width)
            formatted_score = f"Score: {score}".ljust(max_score_width)

            if i < len(self.sr_labels):
                self.sr_labels[i].element.text = f"{formatted_rank} | {formatted_name} | {formatted_score}"

    def end_game(self):
        self.paused = False
        self.gameover.visible = True

        self.current_score = self.arena.snake.score
        self.record_score = current_state(self.username)[2]


        if self.record_score is None:
            self.record_score = 0
            

        if self.current_score >= self.record_score:
            self.record_score = self.current_score
            update_score(self.username, self.current_score)

        self.gameover.score.element.text = str(self.current_score)
        self.gameover.record_score.element.text = str(self.record_score)
        self.arena.pause_game()

    def on_mouse_press(self, x, y, buttons, modifiers):
        if self.gameover.visible:
            self.gameover.visible = False
            self.arena.unschedule(self.arena.update)
            self.remove(self.arena)
            self.arena = Arena(self, self.username, mode='hard')  # Pass username and difficulty to Arena
            self.add(self.arena)
            self.update_report()
        else:
            print('   ###   only when you die can you remake...')

    def toggle_pause(self):
        if self.paused:
            print(" # resume\n")
            # Check if PauseMenu is a child node of the current layer
            if self.pause_menu in self.get_children():
                self.paused = False
                self.remove(self.pause_menu)
                self.pause_menu = None
                self.arena.resume_game()
        else:
            print(" # pause")
            print("111")
            if self.pause_menu is None:
                self.paused = True
                self.pause_menu = PauseMenu(self.username, self.user_type)  # Make sure the PauseMenu is created the right way, and pass the username.
                self.add(self.pause_menu, z=500)
                self.arena.pause_game()

    def on_key_press(self, key, modifiers):
        if not self.gameover.visible:
            if key == pyglet.window.key.SPACE:
                print("Space - Toggle Pause")
                self.toggle_pause()
                return True
            elif key == pyglet.window.key.J:
                print("J - Restart Game...\n")
                self.restart_game()
                return True
            elif key == pyglet.window.key.BACKSPACE:
                print("Backspace - Back to Homepage...\n")
                if self.pause_menu:
                    self.remove(self.pause_menu)
                    self.pause_menu = None

                homepage_scene = HomepageScene(self.username, self.user_type)  # Pass username to HomepageScene
                cocos.director.director.replace(homepage_scene)
                return True
        else:
            if key == pyglet.window.key.J:
                print("J - Restart Game (Game Over)...\n")
                self.restart_game()
                return True
            elif key == pyglet.window.key.BACKSPACE:
                print("Backspace - Back to Homepage (Game Over)...\n")
                if self.pause_menu:
                    self.remove(self.pause_menu)
                    self.pause_menu = None
                homepage_scene = HomepageScene(self.username, self.user_type)  # Pass username to HomepageScene
                cocos.director.director.replace(homepage_scene)
                return True

    def restart_game(self):
        if self.pause_menu:
            self.remove(self.pause_menu)
            self.pause_menu = None

        self.remove(self.arena)
        self.arena = Arena(self, self.username, 'hard')  # Pass self and self.username to the initialization method of the Arena class.
        self.add(self.arena)
        self.gameover.visible = False
        self.update_report()
        self.paused = False      


class UnlimitedFirepowerMode(cocos.layer.Layer):  # The game logic is the same as the classic mode, so there will be no further comments here.
    is_event_handler = True

    def __init__(self, username, user_type):
        super(UnlimitedFirepowerMode, self).__init__()
        self.username = username
        self.user_type = user_type

        print("Unlimited Firepower Mode...\n\n\n")

        self.arena = Arena(self, username, mode='unlimited_firepower')  # Pass username to Arena
        self.add(self.arena, 100)

        scores_background_color = define.CUSTOMIZED_PINK
        scores_background_margin = 300  # background margin
        scores_background_height = define.PLAYERS_NUM * 28 + 2 * scores_background_margin + 160
        scores_background_width = 550

        scores_background = cocos.layer.ColorLayer(*scores_background_color,
                                                   width=scores_background_width,
                                                   height=scores_background_height)
        scores_background.position = (0, 1600 - scores_background_height + scores_background_margin)
        self.add(scores_background, 900)

        self.your_status_label = cocos.text.Label('  Unlimited Firepower',
                                                  font_name='Arial',
                                                  font_size=42,
                                                  color=define.MAROON)
        self.your_status_label.position = 0, 1525
        self.add(self.your_status_label, 1000)

        self.your_status_label = cocos.text.Label('         Your Status',
                                                  font_name='Arial',
                                                  font_size=36,
                                                  color=define.CUSTOMIZED_RED)
        self.your_status_label.position = 25, 1475
        self.add(self.your_status_label, 1000)

        self.ks_label = cocos.text.Label('',
                                         font_name='Courier New',
                                         font_size=24,
                                         color=define.CUSTOMIZED_ORANGE)
        self.ks_label.position = 25, 1425
        self.add(self.ks_label, 1000)

        self.scores_and_rank_label = cocos.text.Label('       Scores & Rank',
                                                      font_name='Arial',
                                                      font_size=36,
                                                      color=define.CUSTOMIZED_RED)
        self.scores_and_rank_label.position = 25, 1350
        self.add(self.scores_and_rank_label, 1000)
        # Adding how-to guides to reports
        self.guide_label = cocos.text.Label(
                                            'Unlimited Power Mode\n'
                                            'Infinity Enermy!\n'
                                            'Using Direction Keys to Control,\n'
                                            'Press SPACE to Pause',
                                            font_name='Arial',
                                            font_size=18,
                                            color=(255, 0, 0, 255),  # red font
                                            width=scores_background_width - 40,
                                            multiline=True,
                                            anchor_x='left',
                                            anchor_y='bottom')
        self.guide_label.position = 25, 600
        self.add(self.guide_label, 1000)
        self.sr_labels = []
        for i in range(define.PLAYERS_NUM):
            label = cocos.text.Label(f'Player {i + 1}:',
                                     font_name='Courier New',
                                     font_size=24,
                                     color=define.CUSTOMIZED_ORANGE)
            label.position = 25, 1300 - i * 28
            self.add(label, 1000)
            self.sr_labels.append(label)

        self.player_kills = 0
        self.player_speed = 0
        self.update_report()

        # Game over screen
        self.gameover = Gameover(self.username)
        self.add(self.gameover, z=2000)

        self.pause_menu = None
        self.paused = False

        self.keyboard = key.KeyStateHandler()
        director.window.push_handlers(self.keyboard)

    def update_report(self):
        self.player_kills = self.arena.kills
        self.player_speed = self.arena.snake.speed

        self.ks_label.element.text = f"Your life: 1 | Speed: {int(self.player_speed)}"

        scores = self.arena.get_scores()
        scores.sort(key=lambda x: x[1], reverse=True)

        max_rank_width = len(str(max(i + 1 for i in range(len(scores)))))
        max_name_width = max(len(name) for name, _ in scores)
        max_score_width = max(len(f"Score: {score}") for _, score in scores)

        for i, (name, score) in enumerate(scores):
            rank = i + 1
            formatted_rank = str(rank).rjust(max_rank_width)
            formatted_name = name.ljust(max_name_width)
            formatted_score = f"Score: {score}".ljust(max_score_width)

            if i < len(self.sr_labels):
                self.sr_labels[i].element.text = f"{formatted_rank} | {formatted_name} | {formatted_score}"

    def end_game(self):
        self.paused = False
        self.gameover.visible = True

        self.current_score = self.arena.snake.score
        self.record_score = current_state(self.username)[2]


        if self.record_score is None:
            self.record_score = 0
            

        if self.current_score >= self.record_score:
            self.record_score = self.current_score
            update_score(self.username, self.current_score)

        self.gameover.score.element.text = str(self.current_score)
        self.gameover.record_score.element.text = str(self.record_score)
        self.arena.pause_game()

    def on_mouse_press(self, x, y, buttons, modifiers):
        if self.gameover.visible:
            self.gameover.visible = False
            self.arena.unschedule(self.arena.update)
            self.remove(self.arena)
            self.arena = Arena(self, self.username, mode='unlimited_firepower')  # Pass username to Arena
            self.add(self.arena)
            self.update_report()
        else:
            print('   ###   only when you die can you remake...\n')

    def toggle_pause(self):
        if self.pause_menu:
            print(" # resume\n")
            # Check if PauseMenu is a child node of the current layer
            if self.pause_menu in self.get_children():
                self.paused = False
                self.remove(self.pause_menu)
                self.pause_menu = None
                self.arena.resume_game()
        else:
            print(" # pause")
            if self.pause_menu is None:
                self.paused = True
                self.pause_menu = PauseMenu(self.username, self.user_type)  # Make sure the PauseMenu is created the right way, and pass the username.
                self.add(self.pause_menu, z=500)
                self.arena.pause_game()

    def on_key_press(self, key, modifiers):
        if not self.gameover.visible:
            if key == pyglet.window.key.SPACE:
                print("Space - Toggle Pause\n")
                self.toggle_pause()
                return True
            elif key == pyglet.window.key.J:
                print("J - Restart Game...\n")
                self.restart_game()
                return True
            elif key == pyglet.window.key.BACKSPACE:
                print("Backspace - Back to Homepage...\n")
                if self.pause_menu:
                    self.remove(self.pause_menu)
                    self.pause_menu = None

                homepage_scene = HomepageScene(self.username, self.user_type)  # Pass username to HomepageScene
                cocos.director.director.replace(homepage_scene)
                return True
        else:
            if key == pyglet.window.key.J:
                print("J - Restart Game (Game Over)...\n")
                self.restart_game()
                return True
            elif key == pyglet.window.key.BACKSPACE:
                print("Backspace - Back to Homepage (Game Over)...\n")
                if self.pause_menu:
                    self.remove(self.pause_menu)
                    self.pause_menu = None
                homepage_scene = HomepageScene(self.username, self.user_type)  # Pass username to HomepageScene
                cocos.director.director.replace(homepage_scene)
                return True


    def restart_game(self):
        if self.pause_menu:
            self.remove(self.pause_menu)
            self.pause_menu = None

        self.remove(self.arena)
        self.arena = Arena(self, self.username, mode='unlimited_firepower')  # Pass username to Arena
        self.add(self.arena)
        self.gameover.visible = False
        self.update_report()
        self.paused = False


class PauseMenu(Layer):  # The pause panel section only solves the problem of mouse clicks, not keystrokes.
    is_event_handler = True

    def __init__(self, user_type, username):
        super(PauseMenu, self).__init__()

        self.user_type = user_type
        self.username = username
        self.is_event_handler = True

        print("pause menu called\n")

        window_width, window_height = cocos.director.director.get_window_size()
        background_width, background_height = window_width * 5 // 12, window_height * 5 // 12  # The width and height of the background layer.

        # Create a background color layer and add it to the PauseMenu Layer.
        background_color_layer = ColorLayer(127, 127, 31, 223,
                                            width=background_width, height=background_height)
        background_color_layer.position = (define.WIDTH * 7 // 24,
                                           define.HEIGHT * 7 // 24)
        self.add(background_color_layer)

        self.title_label = cocos.text.Label('Pause Menu',
                                 font_name='Arial',
                                 font_size=72,
                                 anchor_x='center', anchor_y='center')

        self.title_label.position = background_width / 2, background_height / 2 + window_height // 16
        background_color_layer.add(self.title_label)

        pause_menu_items = [
            cocos.menu.MenuItem('Continue (Space)', lambda: self.on_resume()),
            cocos.menu.MenuItem('Restart (J)', lambda: self.on_restart()),
            cocos.menu.MenuItem('Main Menu (Backspace)', lambda: self.on_main_menu()),
        ]

        self.menu = Menu()
        self.menu.create_menu(pause_menu_items, selected_effect=cocos.menu.zoom_in(),
                              unselected_effect=cocos.menu.zoom_out())
        self.menu.position = -background_width * 67 // 96, -background_height * 7 // 8
        background_color_layer.add(self.menu)

    def on_resume(self):
        # This is only allowed to reopen by pressing the mouse, the same as below.
        print(' # menu resume\n')
        self.parent.paused = False
        self.parent.arena.resume_game()
        self.parent.remove(self)
        self.parent.pause_menu = None

    def on_restart(self):
        print(' # menu restart\n')
        self.parent.restart_game()

    def on_main_menu(self):
        print(' # menu go back...\n\n\n')
        homepage_scene = HomepageScene(self.username, self.user_type)
        director.replace(homepage_scene)

    # Requires additional overrides
    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            self.on_quit()
            return True  # Stopping further dissemination of the incident

    def on_quit(self):  # Don't worry about the end of the screen, just press the ESC
        print("Returning to GameStartScene from PauseMenu by ESC...\n")
        director.pop()

class Shop(Scene):
    def __init__(self, username, user_type):
        super(Shop, self).__init__()

        self.selected_skin = None
        self.username = username
        self.user_type = user_type  # Assigning user_type to an instance variable
        print(f"Received username: {self.username}")
        print(f"Received user_type: {self.user_type}")

        self.user_type = user_type        

        self.skin_manager = SkinManager(self.username)

        window_width, window_height = director.get_window_size()

        # Load background image and set transparency
        background = cocos.sprite.Sprite('background.jpg')
        background.opacity = 50  # Set the transparency, the range is 0 to 255, the smaller the value the more transparent
        background.position = (window_width * 0.5, window_height * 0.5)
        self.add(background, z=-1)  # Add the background image to the scene and set the z value to -1 to make sure it's below the other elements.

        self.title_label = Label('Shop',
                                 font_name='Times New Roman',
                                 font_size=72,
                                 anchor_x='center', anchor_y='center')
        self.title_label.position = (window_width * 0.5, window_height * 0.75)
        self.add(self.title_label, z=0)

        # Get the snake skin currently selected by the user
        current_skin = self.skin_manager.current_skin
        self.selected_skin_label = Label(f"Selected: {current_skin.name}",
                                         font_name='Times New Roman',
                                         font_size=36,
                                         anchor_x='center', anchor_y='center')
        self.selected_skin_label.position = (window_width * 0.5, window_height * 0.685)
        self.add(self.selected_skin_label, z=1)

        skin_options = [
            MenuItem('LitteBrotherSnake', lambda: self.on_skin_selected(self.skin_manager.skins[0], 0)),
            MenuItem('FireSnake', lambda: self.on_skin_selected(self.skin_manager.skins[1], 1)),
            MenuItem('IceSnake', lambda: self.on_skin_selected(self.skin_manager.skins[2], 2)),
            MenuItem('MagicSnake', lambda: self.on_skin_selected(self.skin_manager.skins[3], 3)),
            MenuItem('Goback', self.on_back)
        ]

        self.menu = Menu()
        self.menu.create_menu(skin_options, selected_effect=zoom_in(),
                              unselected_effect=zoom_out())
        self.menu.position = (0, window_height * 0.05)
        self.add(self.menu, z=3)

    def on_skin_selected(self, skin, skin_number):
        print(f"Selected skin_number: {skin_number}")
        self.selected_skin = skin
        print(f"skin: {skin.name}")
        self.skin_manager.current_skin = skin

        self.selected_skin_label.element.text = f"Selected: {skin.name}"
        # Call the update function change_cust to update the skin selection in the database
        change_cust(self.username, skin_number)

    def on_back(self):
        homepage_scene = HomepageScene(self.username, self.user_type)
        director.replace(homepage_scene)


class RankingList(Scene):
    is_event_handler = True  # Allow layers to receive events

    def __init__(self, username, user_type):
        super(RankingList, self).__init__()
        self.username = username
        self.user_type = user_type
        self.ranking_items = get_ranking()# Retrieve ranking data
        
        window_width, window_height = director.get_window_size()
        
        # Add a background image, set the transparency to 50
        background = cocos.sprite.Sprite('background.jpg')
        background.opacity = 50
        background.position = (window_width * 0.5, window_height * 0.5)
        self.add(background, z=0)
        
        self.build_menu()# Build the menu interface

    def build_menu(self):
        line = 0
        
        # Add title
        title = cocos.text.Label('Ranking List', font_name='Times New Roman', font_size=56, anchor_x='center', anchor_y='center')
        title.position = director.window.width // 2, director.window.height // 5 * 4.5
        self.add(title, z=2)

	# Initialize column titles for username, highest score, and ranking
        self.title1 = Label('username', position=(director.window.width // 5, director.window.height // 5 * 4),
                            font_size=32, anchor_x='center', anchor_y='center')
        self.title2 = Label('highest score', position=(director.window.width // 5 * 2, director.window.height // 5 * 4),
                            font_size=32, anchor_x='center', anchor_y='center')
        self.title3 = Label('ranking', position=(director.window.width // 5 * 4, director.window.height // 5 * 4),
                            font_size=32, anchor_x='center', anchor_y='center')
        self.add(self.title1, z=2)
        self.add(self.title2, z=2)
        self.add(self.title3, z=2)

	 # Add individual ranking items
        for rank in self.ranking_items:
            line += 1
            username, highest_score, ranking = rank

	
            # Display username, score, and rank with dynamic positioning based on line number
	    username_label = Label(username, position=(
            director.window.width // 5, director.window.height // 5 * 4 - line * director.window.height // 10),
                                   font_size=32, anchor_x='center', anchor_y='center')

            highest_score_label = Label(str(highest_score), position=(
            director.window.width // 5 * 2, director.window.height // 5 * 4 - line * director.window.height // 10),
                                        font_size=32, anchor_x='center', anchor_y='center')
            ranking_label = Label(str(ranking), position=(
            director.window.width // 5 * 4, director.window.height // 5 * 4 - line * director.window.height // 10),
                                  font_size=32, anchor_x='center', anchor_y='center')

            self.add(username_label, z=2)
            self.add(highest_score_label, z=2)
            self.add(ranking_label, z=2)

        return_item = MenuItem("Return to Homepage", self.on_return)
        items = [return_item]
        positions = [(director.window.width // 2, director.window.width // 10)]
        self.menu = Menu()
        self.menu.create_menu(items, layout_strategy=cocos.menu.fixedPositionMenuLayout(positions),
                              selected_effect=zoom_in(), unselected_effect=zoom_out())  # Disable automatic layout.
        self.add(self.menu, z=2)

    def on_return(self):
        homepage_scene = HomepageScene(self.username, self.user_type)
        director.replace(homepage_scene)
	    
class Settings(Scene):
    is_event_handler = True  # Allow layers to receive events

    def __init__(self, username, user_type):
        super(Settings, self).__init__()

        self.username = username
        self.user_type = user_type
        state = current_state(self.username)# Get the current state settings for the user

	# Set initial settings based on saved state or defaults    
	if state is not None and len(state) >= 13:
            self.music_volume = state[4]
            self.effect_volume = state[11]
            if state[3] == 0:
                self.music_file = 'VCR.mp3'
            else:
                self.music_file = 'happy.mp3'
            if state[12] == 0:
                self.control_mode = 'Keyboard'
            else:
                self.control_mode = 'Mouse'
        else:
	    # Default settings if no state is saved
            self.music_volume = 0.5
            change_volume(self.username, self.music_volume)# Set default music volume
            self.effect_volume = 0.5
            change_evolume(self.username, self.effect_volume)# Set default effect volume
            self.music_file = 'VCR.mp3'
            change_music(self.username, 0)# Set default music file
            self.control_mode = 'Keyboard'
            change_cmode(self.username, 0) # Set default control mode

        self.build_menu()# Build the settings menu

    def build_menu(self):
        # Add background image
        background = cocos.sprite.Sprite('background.jpg')
        background.position = (director.window.width // 2, director.window.height // 2)
        background.opacity = 50  # Set background transparency
        self.add(background, z=0)

        # Add settings page title
        title_label = Label('Settings',
                            position=(director.window.width // 2, director.window.height * 0.8),
                            font_size=48,
                            anchor_x='center', anchor_y='center')
        self.add(title_label, z=1)

        # Section for settings adjustment buttons
        increase_effect_volume_item = MenuItem("+", self.on_increase_effect_volume)
        decrease_effect_volume_item = MenuItem("-", self.on_decrease_effect_volume)
        increase_music_volume_item = MenuItem("+", self.on_increase_music_volume)
        decrease_music_volume_item = MenuItem("-", self.on_decrease_music_volume)
        change_mode_item = MenuItem("Change Control Mode", self.on_change_control_mode)
        change_music_item = MenuItem("Change Music", self.on_change_music)
        return_item = MenuItem("Return to Homepage", self.on_return)
        items = [increase_effect_volume_item, decrease_effect_volume_item,
                 increase_music_volume_item, decrease_music_volume_item,
                 change_mode_item, change_music_item, return_item]

        # Arranging Components Using Relative Positions
        positions = [(director.window.width * 0.625, director.window.height * 0.6),
                     (director.window.width * 0.575, director.window.height * 0.6),
                     (director.window.width * 0.625, director.window.height * 0.5),
                     (director.window.width * 0.575, director.window.height * 0.5),
                     (director.window.width * 0.6, director.window.height * 0.4),
                     (director.window.width * 0.6, director.window.height * 0.3),
                     (director.window.width * 0.5, director.window.height * 0.2)]

        self.menu = Menu()
        self.menu.create_menu(items, layout_strategy=cocos.menu.fixedPositionMenuLayout(positions),
                              selected_effect=zoom_in(), unselected_effect=zoom_out())
        self.add(self.menu, z=2)

        # Display labels for current volume and mode settings
        self.effect_volume_label = Label('Effect Volume:{:.1f}'.format(self.effect_volume),
                                         position=(director.window.width * 0.2, director.window.height * 0.6),
                                         font_size=32,
                                         anchor_x='left', anchor_y='center')
        self.music_volume_label = Label('Music Volume:{:.1f}'.format(self.music_volume),
                                        position=(director.window.width * 0.2, director.window.height * 0.5),
                                        font_size=32,
                                        anchor_x='left', anchor_y='center')
        self.control_mode_label = Label('Control Mode: {}  '.format(self.control_mode),
                                        position=(director.window.width * 0.2, director.window.height * 0.4),
                                        font_size=32,
                                        anchor_x='left', anchor_y='center')
        self.music_name_label = Label('Music Name: {}       '.format(self.music_file),
                                      position=(director.window.width * 0.2, director.window.height * 0.3),
                                      font_size=32,
                                      anchor_x='left', anchor_y='center')

        self.add(self.effect_volume_label, z=1)
        self.add(self.music_volume_label, z=1)
        self.add(self.control_mode_label, z=1)
        self.add(self.music_name_label, z=1)

        # Music playback section
        pygame.init()
        pygame.mixer.init()
        if os.path.exists(self.music_file):
            pygame.mixer.music.load(self.music_file)
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(-1)

    def on_increase_effect_volume(self):
        if self.effect_volume <= 0.9:
            self.effect_volume += 0.1
        self.update_ui()

    def on_decrease_effect_volume(self):
        if self.effect_volume >= 0.1:
            self.effect_volume -= 0.1
        self.update_ui()

    def on_increase_music_volume(self):
        if self.music_volume <= 0.9:
            self.music_volume += 0.1
            pygame.mixer.music.set_volume(self.music_volume)
        self.update_ui()

    def on_decrease_music_volume(self):
        if self.music_volume >= 0.1:
            self.music_volume -= 0.1
            pygame.mixer.music.set_volume(self.music_volume)
        self.update_ui()

    def on_change_control_mode(self):
        if self.control_mode == 'Keyboard':
            self.control_mode = 'Mouse'
        else:
            self.control_mode = 'Keyboard'
        self.update_ui()

    def on_change_music(self):
        if self.music_file == 'VCR.mp3':
            self.music_file = 'happy.mp3'
            pygame.mixer.music.stop()
            pygame.mixer.music.load(self.music_file)
            pygame.mixer.music.play(-1)
        else:
            self.music_file = 'VCR.mp3'
            pygame.mixer.music.stop()
            pygame.mixer.music.load(self.music_file)
            pygame.mixer.music.play(-1)
        self.update_ui()

    def update_ui(self):
        self.effect_volume_label.element.text = 'Effect Volume:            {:.1f}'.format(self.effect_volume)
        self.music_volume_label.element.text = 'Music Volume:            {:.1f}'.format(self.music_volume)
        self.control_mode_label.element.text = 'Control Mode: {}  '.format(self.control_mode)
        self.music_name_label.element.text = 'Music Name: {}       '.format(self.music_file)


    def on_return(self):
        # 存储self.music_volume, self.effect_volume, self.music_name, self.control_mode
        change_volume(self.username, self.music_volume)
        change_evolume(self.username, self.effect_volume)
        if self.music_file == 'VCR.mp3':
            change_music(self.username, 0)
        else:
            change_music(self.username, 1)
        if self.control_mode == 'Keyboard':
            change_cmode(self.username, 0)
        else:
            change_cmode(self.username, 1)
        pygame.mixer.music.stop()
        homepage_scene = HomepageScene(self.username, self.user_type)
        director.replace(homepage_scene)
        

# Main execution point, initialize the director and start the game
if __name__ == "__main__":
    cocos.director.director.init(width=2560, height=1600, caption="GluttonousGame.exe", fullscreen=True)  # if you wanna chage the size of the window , adjust the width and height here as you like!
    cocos.director.director.run(GameStartScene())

# width=screen_width, height=screen_height
