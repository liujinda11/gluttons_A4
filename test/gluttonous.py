import cocos
from cocos.director import director
from cocos.scene import Scene
from cocos.layer import Layer, ColorLayer
from cocos.text import Label
from cocos.menu import Menu, MenuItem, zoom_in, zoom_out
from cocos.actions import CallFunc
import pyglet
from pyglet.window import key
from sys import platform
#from account import insert_account,update_score,match_user_information,get_ranking,change_cust,change_music,change_volume,change_evolume,current_state,change_cmode
import define
from arena import Arena
from gameover import Gameover
# hqc 20240408.21新增
from snake import SkinManager
#import account
#from account import insert_account,update_score,match_user_information,get_ranking,change_cust,change_music,change_volume,change_evolume,current_state,change_cmode


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
            homepage_scene = HomepageScene()
            cocos.director.director.replace(homepage_scene)
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


class HomepageScene(Scene):
    def __init__(self):
        super(HomepageScene, self).__init__()
        # self.is_event_handler = True  # 设置为 True 以处理事件（默认）

        self.skin_manager = SkinManager
        main_menu_layer = MainMenu()
        self.add(main_menu_layer)

    # 在这里用on quit没用


class MainMenu(cocos.menu.Menu):
    def __init__(self):
        super(MainMenu, self).__init__()
        self.skin_manager = SkinManager

        main_menu_items = [
            cocos.menu.MenuItem('Classic Mode', lambda: self.select_mode('Classic Mode')),
            cocos.menu.MenuItem('Unlimited Firepower Mode', lambda: self.select_mode('Unlimited Firepower Mode')),
            cocos.menu.MenuItem('Twisted Jungle Mode', lambda: self.select_mode('Twisted Jungle Mode')),
            cocos.menu.MenuItem('Ranking list', lambda: self.select_mode('Ranking List')),
            cocos.menu.MenuItem('Shop', lambda: self.select_mode('Shop')),
            cocos.menu.MenuItem('Settings', lambda: self.select_mode('Settings')),
            cocos.menu.MenuItem('Exit the game', lambda: self.select_mode('Exit the game'))
        ]
        self.create_menu(main_menu_items)

    def select_mode(self, mode_name):
        print(f"Selected item: {mode_name}...")
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
            shop_scene = cocos.scene.Scene(Shop(self.skin_manager))
            cocos.director.director.replace(shop_scene)
        elif mode_name == 'Settings':
            settings_scene = cocos.scene.Scene(Settings())
            cocos.director.director.replace(settings_scene)
        elif mode_name == 'Exit the game':
            cocos.director.director.pop()
            print('Successfully exited...\n')

    def on_quit(self):
        print("Returning to GameStartScene from MainMenu by ESC...\n.")
        init = GameStartScene()
        cocos.director.director.replace(init)


class ClassicMode(cocos.layer.Layer):
    is_event_handler = True

    def __init__(self):
        super(ClassicMode, self).__init__()

        print("Classic Mode...\n\n\n")
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
            print('   ###   only when you die can you remake...')

    def toggle_pause(self):
        if self.pause_menu:
            print(" # resume\n")
            # 检查PauseMenu是否是当前层的子节点
            if self.pause_menu in self.get_children():
                self.remove(self.pause_menu)
            self.pause_menu = None
            self.arena.resume_game()
        else:
            print(" # pause")
            self.pause_menu = PauseMenu()
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

                homepage_scene = HomepageScene()
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
        print("Returning to GameStartScene from ClassicMode by ESC...\n")
        init = GameStartScene()
        cocos.director.director.replace(init)
    """


class UnlimitedFirepowerMode(cocos.layer.Layer):
    is_event_handler = True

    def __init__(self):
        super(UnlimitedFirepowerMode, self).__init__()

        print("Unlimited Firepower Mode...\n\n\n")

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
            print('   ###   only when you die can you remake...\n')

    def toggle_pause(self):
        if self.pause_menu:
            print(" # resume\n")
            # 检查PauseMenu是否是当前层的子节点
            if self.pause_menu in self.get_children():
                self.remove(self.pause_menu)
            self.pause_menu = None
            self.arena.resume_game()
        else:
            print(" # pause")
            self.pause_menu = PauseMenu()
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

                homepage_scene = HomepageScene()
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

        print("pause menu called\n")

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
        print(' # menu resume\n')
        self.parent.arena.resume_game()
        self.parent.remove(self)
        self.parent.pause_menu = None

    def on_restart(self):
        print(' # menu restart\n')
        self.parent.restart_game()

    def on_main_menu(self):
        print(' # menu go back...\n\n\n')
        main_menu_scene = cocos.scene.Scene(MainMenu())
        cocos.director.director.replace(main_menu_scene)

    # 需要额外覆写
    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            self.on_quit()
            return True  # 阻止事件进一步传播

    def on_quit(self):  # 至于结束界面的就不用操心了，直接按
        print("Returning to GameStartScene from PauseMenu by ESC...\n")
        director.pop()

class Shop(Scene):
    def __init__(self, skin_manager):
        super(Shop, self).__init__()

        self.selected_skin = None
        #self.username = username
        self.username = 'user1'
        self.skin_manager = skin_manager(self.username)

        window_width, window_height = director.get_window_size()

        # 加载背景图片并设置透明度
        background = cocos.sprite.Sprite('background.jpg')
        background.opacity = 128  # 设置透明度,范围是0到255,数值越小越透明
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
        self.selected_skin = skin
        print(f"skin: {skin.name}")
        self.skin_manager.current_skin = skin

        self.selected_skin_label.element.text = f"Selected: {skin.name}"
        # 调用更新函数change_cust更新数据库中的皮肤选择
        change_cust(self.username, skin_number)


    def on_back(self):
        
        homepage_scene = HomepageScene()
        director.replace(homepage_scene)


'''
class Shop(Scene):
    def __init__(self, skin_manager):
        super(Shop, self).__init__()
        shop_menu_layer = ShopMenu(skin_manager)
        self.add(shop_menu_layer)
'''

# 程序从这里开始


if __name__ == "__main__":
    cocos.director.director.init(width=2000, height=1200, caption="原神.exe", fullscreen= False)  # 记得改游戏界面大小
    cocos.director.director.run(GameStartScene())

# width=screen_width, height=screen_height