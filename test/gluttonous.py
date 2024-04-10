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
# from sys import platform
import os
import pygame

import define
from arena import Arena
from gameover import Gameover
from snake import SkinManager
from account import current_state,change_cmode,change_music,change_volume,change_evolume, get_ranking,match_user_information,change_cust,insert_account
"""
def get_screen_size():
    if platform == "linux" or platform == "linux2":
        # linux平台
        return cocos.director.director.get_window_size()
    elif platform == "darwin":
        # macOS平台
        from AppKit import NSScreen
        frame = NSScreen.mainScreen().frame()
        return frame.size.width, frame.size.height
    elif platform == "win32":
        # Windows平台
        from win32api import GetSystemMetrics
        return GetSystemMetrics(0), GetSystemMetrics(1)
    else:
        # 其他平台
        return 800, 600  # 返回默认值


screen_width, screen_height = get_screen_size()
"""



class GameStartScene(Scene):

    def __init__(self):
        super(GameStartScene, self).__init__()

        print("Game Start Scene...\n\n\n")

        self.start_label = None
        self.exit_label = None

        self.setup_background()
        self.setup_labels()
        self.keys = pyglet.window.key.KeyStateHandler()
        cocos.director.director.window.push_handlers(self.keys)
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
            auth_scene = AuthScene()
            cocos.director.director.replace(auth_scene)
            # 这是之前不经验证的版本
            # homepage_scene = HomepageScene()
            # cocos.director.director.replace(homepage_scene)
            self.stop_scheduler()

    def stop_scheduler(self):
        self.unschedule(self.update_label_visibility)
        self.unschedule(self.check_input)
        self.unschedule(self.check_start_game)

    # 自带on quit函数：
    """
    def on_quit(self):
        print("Returning to GameStartScene from MainMenu by ESC...\n.")
        init = GameStartScene()
    """

"""
class AuthScene(cocos.scene.Scene):
    def __init__(self):
        super().__init__()
        self.add(AuthLayer())


class AuthLayer(cocos.menu.Menu):
    def __init__(self):
        super().__init__("Authentication Menu")

        items = [
            cocos.menu.MenuItem('Login', self.login),
            cocos.menu.MenuItem('Register', self.register),
            cocos.menu.MenuItem('Guest Access', self.guest),
            cocos.menu.MenuItem('Exit the game', self.quit)
        ]
        self.create_menu(items, cocos.menu.shake(), cocos.menu.shake_back())

    def login(self):
        auth_method_scene = cocos.scene.Scene(AuthMethodLayer('login'))
        cocos.director.director.replace(auth_method_scene)

    def register(self):
        auth_method_scene = cocos.scene.Scene(AuthMethodLayer('register'))
        cocos.director.director.replace(auth_method_scene)

    def guest(self):
        print("Continue as Guest selected...\n")
        homepage_scene = HomepageScene('guest')
        cocos.director.director.replace(homepage_scene)

    def quit(self):
        print("Exit from user auth option scene...\n")
        cocos.director.director.pop()


class AuthMethodLayer(cocos.layer.Layer):
    def __init__(self, type_):
        super().__init__()
        self.add(AuthMethodMenu(type_))


class AuthMethodMenu(Menu):
    def __init__(self, entry_type):
        super(AuthMethodMenu, self).__init__()

        self.account = None
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

    '''
    def on_username_enter(self, value):
        self.entered_username = value

    def on_password_enter(self, value):
        self.entered_password = value

    def on_login_pressed(self):

        self.account = Account()

        username = self.entered_username
        password = self.entered_password

        # 检查数据库中是否有对应的账号密码
        if self.account.authenticate_user(password):
            # 如果有，则转到Main menu
            homepage_scene = HomepageScene('regular')
            director.replace(homepage_scene)
        else:
            # 如果没有，显示登录失败的提示
            print("Invalid username or password. Please try again.")

    def on_register_pressed(self):
        username = self.entered_username
        password = self.entered_password

        self.account.insert_account(password)

        homepage_scene = HomepageScene('regular')  # 假设注册成功的用户类型为'regular'
        director.replace(homepage_scene)

    def on_back_pressed(self):
        user_auth_scene = Scene(AuthScene())
        director.replace(user_auth_scene)
        
    
'''
    # 测试
    def on_username_enter(self, value):
        self.entered_username = value

    def on_password_enter(self, value):
        self.entered_password = value

    def on_login_pressed(self):
        username = self.entered_username
        password = self.entered_password

        # 检查数据库中是否有对应的账号密码
        self.account = Account(self.entered_username)
        if self.account.match_user_information(password):
            # 如果有，则转到Main menu
            homepage_scene = HomepageScene('regular')  # 假设登录成功的用户类型为'regular'
            director.replace(homepage_scene)
        else:
            # 如果没有，显示登录失败的提示
            print("Invalid username or password. Please try again.")

    def on_register_pressed(self):
        username = self.entered_username
        password = self.entered_password

        self.account = Account(self.entered_username)

        # 将新账号密码存入数据库
        self.account.insert_account(password)

        # 转到Main menu
        homepage_scene = HomepageScene('regular')  # 假设注册成功的用户类型为'regular'
        director.replace(homepage_scene)

    def on_back_pressed(self):
        # Handle returning to the previous menu
        login_scene = Scene(AuthScene())
        director.replace(login_scene)
'''
"""
class AuthScene(cocos.scene.Scene):
    def __init__(self):
        super().__init__()

        # 创建背景精灵
        background = cocos.sprite.Sprite('background.jpg')
        background.position = (cocos.director.director.get_window_size()[0] // 2, cocos.director.director.get_window_size()[1] // 2)
        background.opacity = 50  # 设置背景透明度为50
        self.add(background, z=0)

        # 创建标题标签
        title_label = cocos.text.Label('Authentication', font_name='Arial', font_size=32, anchor_x='center', anchor_y='center')
        title_label.position = (cocos.director.director.get_window_size()[0] // 2, cocos.director.director.get_window_size()[1] * 0.8)
        self.add(title_label, z=1)

        # 添加 AuthLayer
        self.add(AuthLayer(), z=2)

class AuthLayer(cocos.menu.Menu):
    def __init__(self):
        super().__init__(" ")

        items = [
            cocos.menu.MenuItem('Login', self.login),
            cocos.menu.MenuItem('Register', self.register),
            cocos.menu.MenuItem('Guest Access', self.guest),
            cocos.menu.MenuItem('Exit the game', self.quit)
        ]
        self.create_menu(items, cocos.menu.shake(), cocos.menu.shake_back())

    def login(self):
        auth_method_scene = cocos.scene.Scene(AuthMethodLayer('login'))
        cocos.director.director.replace(auth_method_scene)

    def register(self):
        auth_method_scene = cocos.scene.Scene(AuthMethodLayer('register'))
        cocos.director.director.replace(auth_method_scene)

    def guest(self):
        print("Continue as Guest selected...\n")
        homepage_scene = HomepageScene('','guest')
        cocos.director.director.replace(homepage_scene)

    def quit(self):
        print("Exit from user auth option scene...\n")
        cocos.director.director.pop()


class AuthMethodLayer(cocos.layer.Layer):
    def __init__(self, type_):
        super().__init__()
        self.add(AuthMethodMenu(type_))


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

        # 检查数据库中是否有对应的账号密码
        if match_user_information(username, password):
            # 如果有,则转到Main menu
            homepage_scene = HomepageScene(username, 'regular')  # 假设登录成功的用户类型为'regular'
            director.replace(homepage_scene)
        else:
            # 如果没有,显示登录失败的提示
            print("Invalid username or password. Please try again.")

    def on_register_pressed(self):
        username = self.entered_username
        password = self.entered_password

        # 将新账号密码存入数据库
        insert_account(username, password)

        # 转到Main menu
        homepage_scene = HomepageScene(username,'regular' )  # 假设注册成功的用户类型为'regular'
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

	
        main_menu_layer = MainMenu(username, user_type)
        self.add(main_menu_layer)


class MainMenu(cocos.menu.Menu):
    def __init__(self, username, user_type):
        super(MainMenu, self).__init__()
        self.username = username
        self.user_type = user_type
        print("Home page and main menu...\n\n\n")
        print(f"Received username: {self.username}")
        print(f"Received user_type: {self.user_type}")

        main_menu_items = [
            cocos.menu.MenuItem('Classic Mode', lambda: self.select_mode('Classic Mode')),
            cocos.menu.MenuItem('Unlimited Firepower Mode', lambda: self.select_mode('Unlimited Firepower Mode')),
            cocos.menu.MenuItem('Twisted Jungle Mode', lambda: self.select_mode('Twisted Jungle Mode')),
            cocos.menu.MenuItem('Ranking list', lambda: self.select_mode('Ranking List')),
            cocos.menu.MenuItem('Shop', lambda: self.select_mode('Shop')),
            cocos.menu.MenuItem('Settings', lambda: self.select_mode('Settings')),
            cocos.menu.MenuItem('Log out', lambda: self.select_mode('Log out'))
        ]

        if user_type == 'guest':
            print("66666")
            main_menu_items = [item for item in main_menu_items if item.label not in ('Ranking list', 'Shop')]
        else:
            print("?")

        self.create_menu(main_menu_items)

    def select_mode(self, mode_name):
        print(f"Selected item: {mode_name}...")
        if mode_name == 'Classic Mode':
            classic_mode_scene = cocos.scene.Scene(ClassicMode(self.username, self.user_type))
            cocos.director.director.replace(classic_mode_scene)
        elif mode_name == 'Unlimited Firepower Mode':
            unlimited_firepower_mode_scene = cocos.scene.Scene(UnlimitedFirepowerMode(self.username, self.user_type))
            cocos.director.director.replace(unlimited_firepower_mode_scene)
        elif mode_name == 'Twisted Jungle Mode':
            twisted_jungle_mode_scene = cocos.scene.Scene(TwistedJungleMode(self.username, self.user_type))
            cocos.director.director.replace(twisted_jungle_mode_scene)
        elif mode_name == 'Ranking List':
            ranking_list_scene = cocos.scene.Scene(RankingList(self.username, self.user_type))
            cocos.director.director.replace(ranking_list_scene)
        elif mode_name == 'Shop':
            shop_scene = cocos.scene.Scene(Shop(self.username, self.user_type))
            cocos.director.director.replace(shop_scene)
        elif mode_name == 'Settings':
            settings_scene = cocos.scene.Scene(Settings(self.username, self.user_type))
            cocos.director.director.replace(settings_scene)
        elif mode_name == 'Log out':
            auth_scene = cocos.scene.Scene(AuthScene())
            cocos.director.director.replace(auth_scene)
            print('Log out...\n')

    def on_quit(self):
        print("Returning to GameStartScene from MainMenu by ESC...\n.")
        init = GameStartScene()
        cocos.director.director.replace(init)

class ClassicMode(cocos.layer.Layer):
    is_event_handler = True

    def __init__(self, username, user_type):
        super(ClassicMode, self).__init__()
        self.username = username
        self.user_type = user_type

        print("Classic Mode...\n\n\n")
        self.arena = Arena(self, username)  # 将username传递给Arena
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
        self.paused = False

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
            self.arena = Arena(self, self.username)  # 将username传递给Arena
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
                self.pause_menu = PauseMenu(self.username, self.user_type)  # 确保PauseMenu是以正确的方式创建的,并传递username
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

                homepage_scene = HomepageScene(self.username, self.user_type)  # 将username传递给HomepageScene
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
                homepage_scene = HomepageScene(self.username, self.user_type)  # 将username传递给HomepageScene
                cocos.director.director.replace(homepage_scene)
                return True

        
    
    def restart_game(self):
        if self.pause_menu:
            self.remove(self.pause_menu)
            self.pause_menu = None

        self.remove(self.arena)
        self.arena = Arena(self, self.username)  # 传递 self 和 self.username 给 Arena 类的初始化方法
        self.add(self.arena)
        self.gameover.visible = False
        self.update_report()
        self.paused = False
        


class UnlimitedFirepowerMode(cocos.layer.Layer):
    is_event_handler = True

    def __init__(self, username, user_type):
        super(UnlimitedFirepowerMode, self).__init__()
        self.username = username
        self.user_type = user_type

        print("Unlimited Firepower Mode...\n\n\n")

        self.arena = Arena(self, username, mode='unlimited_firepower')  # 将username传递给Arena
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
        self.paused = False

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
            self.arena = Arena(self, self.username, mode='unlimited_firepower')  # 将username传递给Arena
            self.add(self.arena)
            self.update_report()
        else:
            print('   ###   only when you die can you remake...\n')

    def toggle_pause(self):
        if self.pause_menu:
            print(" # resume\n")
            # 检查PauseMenu是否是当前层的子节点
            if self.pause_menu in self.get_children():
                self.paused = False
                self.remove(self.pause_menu)
                self.pause_menu = None
                self.arena.resume_game()
        else:
            print(" # pause")
            if self.pause_menu is None:
                self.paused = True
                self.pause_menu = PauseMenu(self.username, self.user_type)  # 确保PauseMenu是以正确的方式创建的,并传递username
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

                homepage_scene = HomepageScene(self.username, self.user_type)  # 将username传递给HomepageScene
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
                homepage_scene = HomepageScene(self.username, self.user_type)  # 将username传递给HomepageScene
                cocos.director.director.replace(homepage_scene)
                return True


    def restart_game(self):
        if self.pause_menu:
            self.remove(self.pause_menu)
            self.pause_menu = None

        self.remove(self.arena)
        self.arena = Arena(self, self.username, mode='unlimited_firepower')  # 将username传递给Arena
        self.add(self.arena)
        self.gameover.visible = False
        self.update_report()
        self.paused = False


class PauseMenu(Layer):  # 暂停面板部分只解决鼠标点击的问题,不解决按键的问题
    is_event_handler = True

    def __init__(self, user_type, username):
        super(PauseMenu, self).__init__()

        self.user_type = user_type
        self.username = username
        self.is_event_handler = True

        print("pause menu called\n")

        window_width, window_height = cocos.director.director.get_window_size()
        background_width, background_height = window_width * 5 // 12, window_height * 5 // 12  # 背景层,的宽高

        # 创建背景色层,并将其添加到PauseMenu Layer
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
        # 此处仅允许按鼠标重开,下同
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
        main_menu_scene = cocos.scene.Scene(MainMenu(self.user_type, self.username))
        cocos.director.director.replace(main_menu_scene)

    # 需要额外覆写
    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            self.on_quit()
            return True  # 阻止事件进一步传播

    def on_quit(self):  # 至于结束界面的就不用操心了,直接按
        print("Returning to GameStartScene from PauseMenu by ESC...\n")
        director.pop()

class Shop(Scene):
    def __init__(self, username, user_type):
        super(Shop, self).__init__()

        self.selected_skin = None
        self.username = username
        self.user_type = user_type  # 将 user_type 赋值给实例变量
        print(f"Received username: {self.username}")
        print(f"Received user_type: {self.user_type}")

        self.user_type = user_type        

        self.skin_manager = SkinManager(self.username)

        window_width, window_height = director.get_window_size()

        # 加载背景图片并设置透明度
        background = cocos.sprite.Sprite('background.jpg')
        background.opacity = 50  # 设置透明度,范围是0到255,数值越小越透明
        background.position = (window_width * 0.5, window_height * 0.5)
        self.add(background, z=-1)  # 将背景图片添加到场景中,设置z值为-1确保它在其他元素下面

        self.title_label = Label('Shop',
                                 font_name='Times New Roman',
                                 font_size=72,
                                 anchor_x='center', anchor_y='center')
        self.title_label.position = (window_width * 0.5, window_height * 0.75)
        self.add(self.title_label, z=0)

        # 获取用户当前选择的蛇皮肤
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
        # 调用更新函数change_cust更新数据库中的皮肤选择
        change_cust(self.username, skin_number)

    def on_back(self):
        homepage_scene = HomepageScene(self.username, self.user_type)
        director.replace(homepage_scene)


import cocos
from cocos.director import director
from cocos.menu import Menu, MenuItem, zoom_in, zoom_out
from cocos.scene import Scene
from cocos.text import Label
import pygame
import os

class RankingList(Scene):
    is_event_handler = True  # 允许层接收事件

    def __init__(self, username, user_type):
        super(RankingList, self).__init__()
        self.username = username
        self.user_type = user_type
        self.ranking_items = get_ranking()
        self.build_menu()

    def build_menu(self):
        line = 0
        self.title1 = Label('username', position=(director.window.width // 5, director.window.height // 5 * 4),
                            font_size=32, anchor_x='center', anchor_y='center')
        self.title2 = Label('highest score', position=(director.window.width // 5 * 2, director.window.height // 5 * 4),
                            font_size=32, anchor_x='center', anchor_y='center')
        self.title3 = Label('ranking', position=(director.window.width // 5 * 4, director.window.height // 5 * 4),
                            font_size=32, anchor_x='center', anchor_y='center')
        self.add(self.title1)
        self.add(self.title2)
        self.add(self.title3)

        for rank in self.ranking_items:
            line += 1
            username, highest_score, ranking = rank

            username_label = Label(username, position=(
            director.window.width // 5, director.window.height // 5 * 4 - line * director.window.height // 10),
                                   font_size=32, anchor_x='center', anchor_y='center')

            highest_score_label = Label(str(highest_score), position=(
            director.window.width // 5 * 2, director.window.height // 5 * 4 - line * director.window.height // 10),
                                        font_size=32, anchor_x='center', anchor_y='center')
            ranking_label = Label(str(ranking), position=(
            director.window.width // 5 * 4, director.window.height // 5 * 4 - line * director.window.height // 10),
                                  font_size=32, anchor_x='center', anchor_y='center')

            self.add(username_label)
            self.add(highest_score_label)
            self.add(ranking_label)

        return_item = MenuItem("Return to Homepage", self.on_return)
        items = [return_item]
        positions = [(director.window.width // 2, director.window.width // 10)]
        self.menu = Menu()
        self.menu.create_menu(items, layout_strategy=cocos.menu.fixedPositionMenuLayout(positions),
                              selected_effect=zoom_in(), unselected_effect=zoom_out())  # Disable automatic layout.
        self.add(self.menu, z=1)

    def on_return(self):
        main_menu_scene = cocos.scene.Scene(MainMenu(self.username, self.user_type))
        cocos.director.director.replace(main_menu_scene)
class Settings(Scene):
    is_event_handler = True  # 允许层接收事件

    def __init__(self, username, user_type):
        super(Settings, self).__init__()

        self.username = username
        self.user_type = user_type
        self.music_volume = current_state(self.username)[4]
        self.effect_volume = current_state(self.username)[11]
        if current_state(self.username)[3] == 0:
            self.music_name = 'VCR'
        else:
            self.music_name = 'happy'
        if current_state(self.username)[12] == 0:
            self.control_mode = 'Keyboard'
        else:
            self.control_mode = 'Mouse'
        self.build_menu()

    def build_menu(self):
        # 添加背景图片
        background = cocos.sprite.Sprite('background.jpg')
        background.position = (director.window.width // 2, director.window.height // 2)
        background.opacity = 50  # 设置背景图片的透明度为 200
        self.add(background, z=0)

        # 添加设置页面标题
        title_label = Label('Settings',
                            position=(director.window.width // 2, director.window.height * 0.8),
                            font_size=48,
                            anchor_x='center', anchor_y='center')
        self.add(title_label, z=1)

        # 按键部分
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

        # 使用相对位置安排组件
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

        # 一般显示标签部分
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
        self.music_name_label = Label('Music Name: {}       '.format(self.music_name),
                                      position=(director.window.width * 0.2, director.window.height * 0.3),
                                      font_size=32,
                                      anchor_x='left', anchor_y='center')

        self.add(self.effect_volume_label, z=1)
        self.add(self.music_volume_label, z=1)
        self.add(self.control_mode_label, z=1)
        self.add(self.music_name_label, z=1)

        # 音乐播放部分
        pygame.init()
        pygame.mixer.init()
        music_file = 'VCR.mp3'
        if os.path.exists(music_file):
            pygame.mixer.music.load(music_file)
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
        if self.music_name == 'VCR':
            self.music_name = 'happy'
            pygame.mixer.music.stop()
            pygame.mixer.music.load('happy.mp3')
            pygame.mixer.music.play(-1)
        else:
            self.music_name = 'VCR'
            pygame.mixer.music.stop()
            pygame.mixer.music.load('VCR.mp3')
            pygame.mixer.music.play(-1)
        self.update_ui()

    def update_ui(self):
        self.effect_volume_label.element.text = 'Effect Volume:            {:.1f}'.format(self.effect_volume)
        self.music_volume_label.element.text = 'Music Volume:            {:.1f}'.format(self.music_volume)
        self.control_mode_label.element.text = 'Control Mode: {}  '.format(self.control_mode)
        self.music_name_label.element.text = 'Music Name: {}       '.format(self.music_name)


    def on_return(self):
        # 存储self.music_volume, self.effect_volume, self.music_name, self.control_mode
        change_volume(self.username, self.music_volume)
        change_evolume(self.username, self.effect_volume)
        if self.music_name == 'VCR':
            change_music(self.username, 0)
        else:
            change_music(self.username, 1)
        if self.control_mode == 'Keyboard':
            change_cmode(self.username, 0)
        else:
            change_cmode(self.username, 1)
        main_menu_scene = cocos.scene.Scene(MainMenu(self.username, self.user_type))
        cocos.director.director.replace(main_menu_scene)
        

# 程序从这里开始


if __name__ == "__main__":
    cocos.director.director.init(width=2400, height=1600, caption="原神.exe", fullscreen=False)  # 记得改游戏界面大小
    cocos.director.director.run(GameStartScene())

# width=screen_width, height=screen_height
