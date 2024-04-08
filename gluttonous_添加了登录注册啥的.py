import cocos
from cocos.director import director
from cocos.scene import Scene
from cocos.layer import Layer, ColorLayer
from cocos.text import Label
from cocos.menu import Menu, MenuItem, EntryMenuItem, zoom_in, zoom_out
from cocos.actions import CallFunc
import pyglet
from pyglet.window import key
from pyglet.text import Label, DocumentLabel
from pyglet.text.document import UnformattedDocument
from pyglet.text.layout import IncrementalTextLayout
from pyglet.text.caret import Caret

import account
import define
from arena import Arena
from gameover import Gameover


#----------------------------------------------------------new things--------------------------------------------------------------------------#
# 注意你的gamestartscene,点击空格键后需要转到login layer，你可以去看看那行代码

class HomepageScene(Scene):
    def __init__(self, user_type):
        super(HomepageScene, self).__init__()
        main_menu_layer = MainMenu(user_type)
        self.add(main_menu_layer)

class LoginEntryLayer(Layer):
    def __init__(self, entry_type):
        super(LoginEntryLayer, self).__init__()

        # Menu for the login entries
        self.menu = LoginEntryMenu(entry_type)
        self.add(self.menu)


class LoginEntryMenu(Menu):
    def __init__(self, entry_type):
        super(LoginEntryMenu, self).__init__()

        self.font_item = {
            'font_name': 'Arial',
            'font_size': 24,
            'color': (255, 255, 255, 255),
        }

        # Create the menu items
        self.username = EntryMenuItem('Username:', self.on_username_enter, '')
        self.password = EntryMenuItem('Password:', self.on_password_enter, '')
        self.back_button = MenuItem('Back', self.on_back_pressed)  # 无论是login还是register,都创建back_button
        
        if entry_type == 'login':
            self.login_button = MenuItem('Login', self.on_login_pressed)
            menu_items = [self.username, self.password, self.login_button, self.back_button]
        elif entry_type == 'register':
            self.register_button = MenuItem('Register', self.on_register_pressed)
            menu_items = [self.username, self.password, self.register_button, self.back_button]
        
        screen_width, screen_height = director.get_window_size()
        # Create the menu with the items
        self.create_menu(menu_items,
                         layout_strategy=cocos.menu.fixedPositionMenuLayout([(screen_width // 2, screen_height // 2 + 50),
                                                                             (screen_width // 2, screen_height // 2),
                                                                             (screen_width // 2, screen_height // 2 - 50),
                                                                             (screen_width // 2, screen_height // 2 - 100)]))

    def on_username_enter(self, value):
        self.entered_username = value

    def on_password_enter(self, value):
        self.entered_password = value

    def on_login_pressed(self):
        username = self.entered_username
        password = self.entered_password

        # 检查数据库中是否有对应的账号密码
        if account.check_account(username, password):
            # 如果有，则转到Main menu
            homepage_scene = HomepageScene('regular')  # 假设登录成功的用户类型为'regular'
            director.replace(homepage_scene)
        else:
            # 如果没有，显示登录失败的提示
            print("Invalid username or password. Please try again.")

    def on_register_pressed(self):
        username = self.entered_username
        password = self.entered_password

        # 将新账号密码存入数据库
        account.insert_account(username, password)

        # 转到Main menu
        homepage_scene = HomepageScene('regular')  # 假设注册成功的用户类型为'regular'
        director.replace(homepage_scene)

    def on_back_pressed(self):
        # Handle returning to the previous menu
        login_scene = Scene(LoginLayer())
        director.replace(login_scene)


class LoginLayer(Layer):
    is_event_handler = True  # For capturing events

    def __init__(self):
        super(LoginLayer, self).__init__()

        # Menu for the login entries and buttons
        self.menu = LoginMenu()
        self.add(self.menu)


class LoginMenu(Menu):
    def __init__(self):
        super(LoginMenu, self).__init__()

        self.font_title = {
            'font_name': 'Arial',
            'font_size': 32,
            'color': (255, 255, 255, 255),
        }

        self.font_item = {
            'font_name': 'Arial',
            'font_size': 24,
            'color': (255, 255, 255, 255),
        }

        self.font_item_selected = {
            'font_name': 'Arial',
            'font_size': 24,
            'color': (255, 0, 0, 255),
        }

        # Create the menu items
        self.login_button = MenuItem('Login', self.on_login_pressed)
        self.register_button = MenuItem('Register', self.on_register_pressed)
        self.guest_button = MenuItem('Continue as Guest', self.on_guest_pressed)
        self.exit_button = MenuItem('Exit', self.on_exit_pressed)

        screen_width, screen_height = director.get_window_size()
        # Create the menu with the items
        self.create_menu([self.login_button, self.register_button, self.guest_button, self.exit_button],
                         layout_strategy=cocos.menu.fixedPositionMenuLayout([(screen_width // 2, screen_height // 2 + 75),
                                                                             (screen_width // 2, screen_height // 2 + 25),
                                                                             (screen_width // 2, screen_height // 2 - 25),
                                                                             (screen_width // 2, screen_height // 2 - 75)]))
    def on_login_pressed(self):
        # This function is called when the user presses the login button.
        print("Login button pressed")
        # Switch to the login entry scene
        login_entry_scene = Scene(LoginEntryLayer('login'))
        director.replace(login_entry_scene)

    def on_register_pressed(self):
        # This function is called when the user presses the register button.
        print("Register button pressed")
        # Switch to the register entry scene
        register_entry_scene = Scene(LoginEntryLayer('register'))
        director.replace(register_entry_scene)

    def on_guest_pressed(self):
    # This function is called when the user chooses to continue as a guest.
        print("Continue as guest")
        # Here you should implement the logic to handle guest user access
        homepage_scene = HomepageScene('guest')
        director.replace(homepage_scene)

    def on_exit_pressed(self):
        # This function is called when the user presses the exit button.
        print("Exit button pressed")
        director.window.close() 

#----------------------------------------------------------------------------------------------------------------------------#

class GameStartScene(Scene):

    def __init__(self):
        super(GameStartScene, self).__init__()

        self.start_label = None
        self.exit_label = None

        self.setup_background()
        self.setup_labels()
        self.keys = pyglet.window.key.KeyStateHandler()
        cocos.director.director.window.push_handlers(self.keys)
        self.schedule(self.check_input) 
        self.schedule_interval(self.update_label_visibility, 0.5)
        self.schedule(self.check_input)

    def setup_background(self):
        screen_width, screen_height = cocos.director.director.get_window_size()
        background_sprite = cocos.sprite.Sprite("background.jpg")
        background_sprite.scale_x = background_sprite.width / screen_width
        background_sprite.scale_y = background_sprite.height / screen_height
        background_sprite.position = screen_width / 2, screen_height / 2
        self.add(background_sprite, z=0)

    def setup_labels(self):
        screen_width, screen_height = cocos.director.director.get_window_size()
        self.create_label('Genshin Impact',
                          144,
                          (0, 255, 0, 255),
                          screen_width / 2,
                          screen_height * 3 / 5,
                          'Comic Sans MS',
                          True)
        self.start_label = self.create_label('press space key to start',
                                             48,
                                             (127, 255, 255, 255),
                                             screen_width / 2,
                                             screen_height / 4,
                                             'Arial',
                                             False)
        self.exit_label = self.create_label('or press esc key to exit',
                                            48,
                                            (127, 255, 255, 255),
                                            screen_width / 2,
                                            screen_height * 3 / 16,
                                            'Arial',
                                            False)

    def create_label(self, text, font_size, color, x, y, font_name=None, bold=None):
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
        self.start_label.visible = not self.start_label.visible
        self.exit_label.visible = not self.exit_label.visible
        self.check_start_game()

    def check_input(self, dt):
        self.check_start_game()

    def check_start_game(self):
        if self.keys[pyglet.window.key.SPACE]:
            login_scene = Scene(LoginLayer())
            cocos.director.director.replace(login_scene)
            self.stop_scheduler()

    def stop_scheduler(self):
        self.unschedule(self.update_label_visibility)
        self.unschedule(self.check_input)
        self.unschedule(self.check_start_game)

    # 自带on quit函数：
    """
    def on_quit(self):
        print("Returning to GameStartScene from MainMenu by ESC.")
        init = GameStartScene()
    """


class HomepageScene(Scene):
    def __init__(self, user_type):
        super(HomepageScene, self).__init__()
        main_menu_layer = MainMenu(user_type)
        self.add(main_menu_layer)

    # 在这里用on quit没用


class MainMenu(cocos.menu.Menu):
    def __init__(self, user_type):
        super(MainMenu, self).__init__()
        print("Home page and main menu")

        main_menu_items = [
        cocos.menu.MenuItem('Classic Mode', lambda: self.select_mode('Classic Mode')),
        cocos.menu.MenuItem('Unlimited Firepower Mode', lambda: self.select_mode('Unlimited Firepower Mode')),
        cocos.menu.MenuItem('Twisted Jungle Mode', lambda: self.select_mode('Twisted Jungle Mode')),
        cocos.menu.MenuItem('Ranking List', lambda: self.select_mode('Ranking List')),
        cocos.menu.MenuItem('Shop', lambda: self.select_mode('Shop')),
        cocos.menu.MenuItem('Settings', lambda: self.select_mode('Settings')),
        cocos.menu.MenuItem('Log Out', self.log_out)
    ]

        # 根据用户类型显示或隐藏某些菜单项
        if user_type == 'guest':
            ranking_list_item = cocos.menu.MenuItem('Ranking List', lambda: self.select_mode('Ranking List'))
            shop_item = cocos.menu.MenuItem('Shop', lambda: self.select_mode('Shop'))
            if ranking_list_item in main_menu_items:
                main_menu_items.remove(ranking_list_item)
            if shop_item in main_menu_items:
                main_menu_items.remove(shop_item)
        elif user_type == 'vip':
            # VIP用户可以访问所有菜单项
            pass

        self.create_menu(main_menu_items)

    def select_mode(self, mode_name):
        print(f"Selected item: {mode_name}")
        if mode_name == 'Classic Mode':
            classic_mode_scene = cocos.scene.Scene(ClassicMode())
            cocos.director.director.replace(classic_mode_scene)
        elif mode_name == 'Unlimited Firepower Mode':
            unlimited_firepower_mode_scene = cocos.scene.Scene(UnlimitedFirepowerMode())
            cocos.director.director.replace(unlimited_firepower_mode_scene)
        elif mode_name == 'Twisted Jungle Mode':
            twisted_jungle_mode_scene = cocos.scene.Scene(TwistedJungleMode())
            cocos.director.director.replace(twisted_jungle_mode_scene)
        elif mode_name == 'Ranking List':
            ranking_list_scene = cocos.scene.Scene(RankingList())
            cocos.director.director.replace(ranking_list_scene)
        elif mode_name == 'Shop':
            shop_scene = cocos.scene.Scene(Shop())
            cocos.director.director.replace(shop_scene)
        elif mode_name == 'Settings':
            settings_scene = cocos.scene.Scene(Settings())
            cocos.director.director.replace(settings_scene)

    def log_out(self):
        print('Log Out')
        login_scene = Scene(LoginLayer())
        cocos.director.director.replace(login_scene)

    def on_quit(self):
        print("Returning to GameStartScene from MainMenu by ESC.")
        init = GameStartScene()
        cocos.director.director.replace(init)


class ClassicMode(cocos.layer.Layer):
    is_event_handler = True

    def __init__(self):
        super(ClassicMode, self).__init__()

        print("Classic Mode...")
        self.arena = Arena(self)
        self.add(self.arena, 100)

        scores_background_color = define.CUSTOMIZED_PINK
        scores_background_margin = 300  # 背景边距
        scores_background_height = define.PLAYERS_NUM * 28 + 2 * scores_background_margin
        scores_background_width = 550

        scores_background = cocos.layer.ColorLayer(*scores_background_color,
                                                   width=scores_background_width,
                                                   height=scores_background_height)
        scores_background.position = (0, 1600 - scores_background_height + scores_background_margin)
        self.add(scores_background, 900)

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

        self.player_kills = 0
        self.player_speed = 0
        self.update_report()

        self.gameover = Gameover()
        self.add(self.gameover, 2000)

        self.pause_menu = None
        self.paused = None

        self.keyboard = key.KeyStateHandler()
        director.window.push_handlers(self.keyboard)

    def update_report(self):
        self.player_kills = self.arena.kills
        self.player_speed = self.arena.snake.speed

        self.ks_label.element.text = f" Kills: {self.player_kills}     | Speed: {int(self.player_speed)}"

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
        self.gameover.score.element.text = str(self.arena.snake.score)
        self.arena.pause_game()

    def on_mouse_press(self, x, y, buttons, modifiers):
        if self.gameover.visible:
            self.gameover.visible = False
            self.arena.unschedule(self.arena.update)
            self.remove(self.arena)
            self.arena = Arena(self)
            self.add(self.arena)
            self.update_report()
        else:
            print('only when you die can you remake')

    def toggle_pause(self):
        if self.pause_menu:
            print("resume")
            # 检查PauseMenu是否是当前层的子节点
            if self.pause_menu in self.get_children():
                self.remove(self.pause_menu)
            self.pause_menu = None
            self.arena.resume_game()
        else:
            print("pause")
            self.pause_menu = PauseMenu()
            self.add(self.pause_menu, z=500)
            self.arena.pause_game()

    def on_key_press(self, key, modifiers):
        if not self.gameover.visible:
            if key == pyglet.window.key.SPACE:
                print("\nSpace - Toggle Pause")
                self.toggle_pause()
                return True
            elif key == pyglet.window.key.J:
                print("\nJ - Restart Game")
                self.restart_game()
                return True
            elif key == pyglet.window.key.BACKSPACE:
                print("\nBackspace - Back to Homepage")
                if self.pause_menu:
                    self.remove(self.pause_menu)
                    self.pause_menu = None

                homepage_scene = HomepageScene()
                cocos.director.director.replace(homepage_scene)
                return True
        else:
            if key == pyglet.window.key.J:
                print("\nJ - Restart Game (Game Over)")
                self.restart_game()
                return True
            elif key == pyglet.window.key.BACKSPACE:
                print("\nBackspace - Back to Homepage (Game Over)")
                if self.pause_menu:
                    self.remove(self.pause_menu)
                    self.pause_menu = None
                homepage_scene = HomepageScene()
                cocos.director.director.replace(homepage_scene)
                return True

    def restart_game(self):
        if self.pause_menu:
            self.remove(self.pause_menu)
            self.pause_menu = None

        self.remove(self.arena)
        self.arena = Arena(self)
        self.add(self.arena)
        self.gameover.visible = False
        self.update_report()
        self.paused = False

    """似乎并不需要
    def on_quit(self):
        print("Returning to GameStartScene from ClassicMode by ESC.")
        init = GameStartScene()
        cocos.director.director.replace(init)
    """


class UnlimitedFirepowerMode(cocos.layer.Layer):
    is_event_handler = True

    def __init__(self):
        super(UnlimitedFirepowerMode, self).__init__()

        print("Unlimited Firepower Mode...")

        self.arena = Arena(self, mode='unlimited_firepower')
        self.add(self.arena, 100)

        scores_background_color = define.CUSTOMIZED_PINK
        scores_background_margin = 300  # 背景边距
        scores_background_height = define.PLAYERS_NUM * 28 + 2 * scores_background_margin
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

        # 游戏结束界面
        self.gameover = Gameover()
        self.add(self.gameover, z=2000)

        self.pause_menu = None
        self.paused = None

        self.keyboard = key.KeyStateHandler()
        director.window.push_handlers(self.keyboard)

    def update_report(self):
        self.player_kills = self.arena.kills
        self.player_speed = self.arena.snake.speed

        self.ks_label.element.text = f" Kills: {self.player_kills}     | Speed: {int(self.player_speed)}"

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
        self.gameover.score.element.text = str(self.arena.snake.score)
        self.arena.pause_game()

    def on_mouse_press(self, x, y, buttons, modifiers):
        if self.gameover.visible:
            self.gameover.visible = False
            self.arena.unschedule(self.arena.update)
            self.remove(self.arena)
            self.arena = Arena(self, mode='unlimited_firepower')
            self.add(self.arena)
            self.update_report()
        else:
            print('only when you die can you remake')

    def toggle_pause(self):
        if self.pause_menu:
            print("resume")
            # 检查PauseMenu是否是当前层的子节点
            if self.pause_menu in self.get_children():
                self.remove(self.pause_menu)
            self.pause_menu = None
            self.arena.resume_game()
        else:
            print("pause")
            self.pause_menu = PauseMenu()
            self.add(self.pause_menu, z=500)
            self.arena.pause_game()

    def on_key_press(self, key, modifiers):
        if not self.gameover.visible:
            if key == pyglet.window.key.SPACE:
                print("\nSpace - Toggle Pause")
                self.toggle_pause()
                return True
            elif key == pyglet.window.key.J:
                print("\nJ - Restart Game")
                self.restart_game()
                return True
            elif key == pyglet.window.key.BACKSPACE:
                print("\nBackspace - Back to Homepage")
                if self.pause_menu:
                    self.remove(self.pause_menu)
                    self.pause_menu = None

                homepage_scene = HomepageScene()
                cocos.director.director.replace(homepage_scene)
                return True
        else:
            if key == pyglet.window.key.J:
                print("\nJ - Restart Game (Game Over)")
                self.restart_game()
                return True
            elif key == pyglet.window.key.BACKSPACE:
                print("\nBackspace - Back to Homepage (Game Over)")
                if self.pause_menu:
                    self.remove(self.pause_menu)
                    self.pause_menu = None
                homepage_scene = HomepageScene()
                cocos.director.director.replace(homepage_scene)
                return True

    def restart_game(self):
        if self.pause_menu:
            self.remove(self.pause_menu)
            self.pause_menu = None

        self.remove(self.arena)
        self.arena = Arena(self, mode='unlimited_firepower')
        self.add(self.arena)
        self.gameover.visible = False
        self.update_report()
        self.paused = False


class PauseMenu(Layer):  # 暂停面板部分只解决鼠标点击的问题，不解决按键的问题
    is_event_handler = True

    def __init__(self):
        super(PauseMenu, self).__init__()

        print("pause menu called")

        window_width, window_height = cocos.director.director.get_window_size()
        background_width, background_height = window_width * 5 // 12, window_height * 5 // 12  # 背景层，的宽高

        # 创建背景色层，并将其添加到PauseMenu Layer
        background_color_layer = ColorLayer(127, 127, 31, 223,
                                            width=background_width, height=background_height)
        background_color_layer.position = (define.WIDTH * 7 // 24,
                                           define.HEIGHT * 7 // 24)
        self.add(background_color_layer)

        self.title_label = Label('Pause Menu',
                                 font_name='Arial',
                                 font_size=72,
                                 anchor_x='center', anchor_y='center')
        self.title_label.color = (255, 0, 0)  # 没用？
        self.title_label.position = background_width / 2, background_height / 2 + window_height // 16
        background_color_layer.add(self.title_label)

        pause_menu_items = [
            cocos.menu.MenuItem('Continue (Space)', self.on_resume),
            cocos.menu.MenuItem('Restart (J)', self.on_restart),
            cocos.menu.MenuItem('Main Menu (Backspace)', self.on_main_menu),
        ]

        self.menu = Menu()
        self.menu.create_menu(pause_menu_items, selected_effect=cocos.menu.zoom_in(),
                              unselected_effect=cocos.menu.zoom_out())
        self.menu.position = -background_width * 67 // 96, -background_height * 7 // 8
        background_color_layer.add(self.menu)

    def on_resume(self):
        # 此处仅允许按鼠标重开，下同
        print('\nmouse resume')
        self.parent.arena.resume_game()
        self.parent.remove(self)
        self.parent.pause_menu = None

    def on_restart(self):
        print('\nmouse restart')
        self.parent.restart_game()

    def on_main_menu(self):
        print('\nmouse go back')
        main_menu_scene = cocos.scene.Scene(MainMenu())
        cocos.director.director.replace(main_menu_scene)

    # 需要额外覆写
    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            self.on_quit()
            return True  # 阻止事件进一步传播

    def on_quit(self):  # 至于结束界面的就不用操心了，直接按
        print("Returning to GameStartScene from PauseMenu by ESC.")
        director.pop()


# 程序从这里开始


if __name__ == "__main__":
    cocos.director.director.init(width=1600, height=1000, caption="原神.exe", fullscreen=False)  # 记得改游戏界面大小
    cocos.director.director.run(GameStartScene())
