import cocos
from cocos.director import director
from cocos.text import Label
from cocos.layer import Layer, ColorLayer
from cocos.scene import Scene
from cocos.actions import CallFunc
from cocos.menu import Menu, MenuItem, zoom_in, zoom_out

import pyglet

import define
from arena import Arena
from gameover import Gameover


class ClassicMode(cocos.layer.Layer):
    is_event_handler = True

    def __init__(self):
        super(ClassicMode, self).__init__()
        self.pause_menu = PauseMenu()
        self.main_menu = MainMenu()
        self.add(self.pause_menu, 500)
        self.arena = Arena(self)
        self.add(self.arena, 100)
        print("Classic Mode...")

        self.paused = False
        self.pause_menu.set_enabled(False)
        self.main_menu.set_enabled(False)
        """
        # 暂停按钮
        self.pause_label = cocos.text.Label('Pause', font_size=24, x=100, y=700, color = define.SKY_BLUE)
        self.add(self.pause_label, 5000)
        """

        # 初始化得分面板 自定义字号什么的
        self.score = cocos.text.Label('Score: 30',
                                      font_name='Arial',
                                      font_size=108,
                                      color=define.GOLD)
        self.score.position = 0, 600
        self.add(self.score, 1000)
        # 在第10000个图层上显示（几乎是顶置)

        # 结束界面
        self.gameover = Gameover()
        self.add(self.gameover, 2000)
        # 更顶置

    def update_score(self):
        # 更新分数
        self.score.element.text = "Score: " + str(self.arena.snake.score)

    def end_game(self):
        # 显示游戏结束界面
        self.paused = False
        self.pause_menu.set_enabled(False)
        self.gameover.visible = True
        self.gameover.score.element.text = str(self.arena.snake.score)
        # 暂停游戏
        self.arena.pause_game()

    def on_mouse_press(self, x, y, buttons, modifiers):
        if self.gameover.visible:
            self.gameover.visible = False
            self.arena.unschedule(self.arena.update)
            self.remove(self.arena)
            self.arena = Arena(self)
            self.add(self.arena)
            self.update_score()
        else:
            print('only when you die can you remake')

    def on_key_press(self, key, modifiers):
        if self.paused or self.gameover.visible:
            # 按 J 键重启游戏，允许在游戏暂停或游戏结束时重启
            if key == pyglet.window.key.J:
                self.pause_menu.visible = False  # 隐藏游戏暂停界面
                self.gameover.visible = False  # 隐藏游戏结束界面
                self.paused = False  # 确保游戏不再是暂停状态
                self.arena.resume_game()  # 恢复游戏
                self.reset_game()
                return True
            # 按 Backspace 键返回主菜单，仅当游戏暂停或结束时有效
            elif key == pyglet.window.key.BACKSPACE:
                self.on_back_to_main_menu()
                return True

        if not self.gameover.visible:
            # 按 Space 键暂停/恢复游戏
            if key == pyglet.window.key.SPACE:
                if self.paused:
                    print('resumed')
                    self.resume_game()
                    self.arena.resume_game()
                else:
                    print('paused')
                    self.pause_game()
                    self.arena.pause_game()
                return True

        return False  # 如果按键没有被处理，则返回 False

    def pause_game(self):
        self.pause_menu.set_enabled(True)
        # self.pause_menu.visible = True  # 显示暂停菜单
        self.paused = not self.paused

    def resume_game(self):
        self.pause_menu.set_enabled(False)
        # self.pause_menu.visible = False
        self.paused = not self.paused

    def reset_game(self):
        # 移除当前的游戏场景
        self.remove(self.arena)
        # 创建并添加新的游戏场景
        self.arena = Arena(self)
        self.add(self.arena)
        # 重置得分和其他必要的状态
        self.update_score()
        # 确保游戏不是在暂停状态
        self.paused = False

    def on_back_to_main_menu(self):
        # 返回主菜单
        main_menu_scene = cocos.scene.Scene(MainMenu())
        cocos.director.director.replace(main_menu_scene)
        MainMenu.set_enabled(self.main_menu, True)
        # main_menu = MainMenu()
        # cocos.director.director.replace(main_menu)
        # self.reset_game() ??????????


class PauseMenu(Layer):
    def __init__(self):
        super(PauseMenu, self).__init__()

        self.visible = False  # 初始设置菜单不可见
        self.enabled = False  # 添加一个属性来跟踪是否启用菜单

        window_width, window_height = cocos.director.director.get_window_size()
        center_x, center_y = window_width // 2, window_height // 2
        # print(center_x, center_y)

        # 设置背景层的大小
        background_width, background_height = window_width // 2, window_height // 2  # 自定义背景层的宽高

        # 创建背景色层，并将其添加到PauseMenu Layer
        background_color_layer = ColorLayer(128, 128, 32, 128,
                                            width=background_width, height=background_height)
        background_color_layer.position = (define.WIDTH / 2 - background_width / 2,
                                           define.HEIGHT / 2 - background_height / 2)
        self.add(background_color_layer)

        # 创建标题标签并添加到背景色层上
        self.title_label = Label('Pause Menu',
                                 font_name='Arial',
                                 font_size=72,
                                 anchor_x='center', anchor_y='center')
        self.title_label.color = (255, 0, 0)  # 设置文本颜色为红色
        self.title_label.position = background_width / 2, background_height / 2 + window_height // 16
        background_color_layer.add(self.title_label)

        # 创建菜单项
        pause_menu_items = [
            ColorMenuItem('Continue (Space)', self.on_continue, color=(255, 0, 0)),  # 红色
            ColorMenuItem('Restart (J)', self.on_restart, color=(0, 255, 0)),  # 绿色
            ColorMenuItem('Main Menu (Backspace)', self.on_main_menu, color=(0, 0, 255)),  # 蓝色
        ]

        # 创建菜单并设置位置
        self.menu = Menu()
        self.menu.create_menu(pause_menu_items, selected_effect=cocos.menu.zoom_in(),
                              unselected_effect=cocos.menu.zoom_out())
        self.menu.position = -background_width // 2, -background_height // 2 - background_height // 8
        background_color_layer.add(self.menu)

    def on_key_press(self, key, modifiers):
        # 如果菜单被禁用，则不处理按键事件
        if not self.enabled:
            return False
        # 处理按键事件...
        return True  # 或者在某些情况下返回 False

    def on_mouse_press(self, x, y, buttons, modifiers):
        # 如果菜单被禁用，则不处理鼠标事件
        if not self.enabled:
            return False
        # 处理鼠标事件...
        return True

    # 可能还需要为其他事件如 on_mouse_release 等添加类似的检查

    def set_enabled(self, enabled):
        self.enabled = enabled
        self.visible = enabled

    def on_continue(self):
        print('resumed')
        self.parent.resume_game()
        self.parent.arena.resume_game()

    def on_restart(self):
        self.parent.reset_game()

    def on_main_menu(self):
        self.parent.on_back_to_main_menu()


class MainMenu(cocos.menu.Menu):
    def __init__(self):
        super(MainMenu, self).__init__()
        self._handlers_enabled = False
        self.enabled = True

        # 主菜单选项
        main_menu_items = [cocos.menu.MenuItem('Classic Mode', self.on_classic_mode),
                           cocos.menu.MenuItem('Other Mode1', self.on_mode1),
                           cocos.menu.MenuItem('Other Mode2', self.on_mode2),
                           cocos.menu.MenuItem('Ranking list', self.on_ranking_list),
                           cocos.menu.MenuItem('Shop', self.on_shop),
                           cocos.menu.MenuItem('Settings', self.on_settings),
                           cocos.menu.MenuItem('Exit the game', self.on_exit_the_game)]
        # 没有字体等参数
        # custom_menu = CustomMenu(items)
        # 创建选项
        self.create_menu(main_menu_items)
        self.selected_item = None  # 添加selected_item属性并初始化为None

    def set_enabled(self, enabled):
        self.enabled = enabled

    def on_classic_mode(self):
        # 进入经典模式界面
        # import pdb
        # pdb.set_trace()
        self.selected_item = 'Classic Mode'
        print("Selected item:", self.selected_item)
        self.set_enabled(False)
        classic_mode_scene = cocos.scene.Scene(ClassicMode())
        cocos.director.director.replace(classic_mode_scene)
        # cocos.director.director.run(cocos.scene.Scene(ClassicMode()))
        # cocos.director.director.pop()

    def on_mode1(self):
        # 进入模式1
        self.selected_item = 'mode1'
        print("Selected item:", self.selected_item)

    def on_mode2(self):
        # 进入模式2
        self.selected_item = 'mode2'
        print("Selected item:", self.selected_item)

    def on_ranking_list(self):
        # 进入排行榜
        self.selected_item = 'Ranking List'
        print("Selected item:", self.selected_item)

    def on_shop(self):
        # 进入商店（看情况删了）
        self.selected_item = 'Shop'
        print("Selected item:", self.selected_item)

    def on_settings(self):
        # 进入设置界面
        self.selected_item = 'Settings'
        print("Selected item:", self.selected_item)

    def on_exit_the_game(self):
        # 退出游戏
        # import pdb
        # pdb.set_trace()
        self.selected_item = 'Exit'
        print("Selected item:", self.selected_item)
        if self.selected_item == 'Exit':
            cocos.director.director.pop()
            print('successfully exited')
            pass

    def on_quit(self):
        pass


class GameStart(cocos.scene.Scene):

    def __init__(self):
        super(GameStart, self).__init__()
        self.start_label = None
        self.exit_label = None
        print("Homepage...")

        screen_width, screen_height = cocos.director.director.get_window_size()

        # 背景图的精灵
        # 背景图的精灵
        background_sprite = cocos.sprite.Sprite("background.jpg")
        # 调整背景图的尺寸以填充整个窗口
        background_sprite.scale_x = background_sprite.width / screen_width
        background_sprite.scale_y = background_sprite.height / screen_height
        background_sprite.position = (screen_width // 2, screen_height // 2)  # 图的中心坐标
        # background_sprite.scale = 0.5
        self.add(background_sprite, z=0)  # 图层为最底

        # 添加 '贪吃蛇' 的 label
        snake_label = cocos.text.Label('Genshin Impact',
                                       font_size=144,
                                       font_name='Comic Sans MS',
                                       color=(0, 255, 0, 127),
                                       anchor_x='center',
                                       anchor_y='center',
                                       x=screen_width // 2,
                                       y=screen_height * 3 // 5)
        self.add(snake_label)

        # 创建并显示点击任意键开始游戏的提示
        self.start_label = cocos.text.Label('press space key to start',
                                            font_size=48,
                                            anchor_x='center',
                                            anchor_y='center',
                                            x=screen_width // 2,
                                            y=screen_height // 4)
        self.add(self.start_label)

        self.exit_label = cocos.text.Label('or press esc key to exit',
                                           font_size=48,
                                           anchor_x='center',
                                           anchor_y='center',
                                           x=screen_width // 2,
                                           y=screen_height * 3 // 16)
        self.add(self.exit_label)

        self.keys = pyglet.window.key.KeyStateHandler()
        cocos.director.director.window.push_handlers(self.keys)  # 将KeyStateHandler对象添加到窗口

        self.schedule_interval(self.update_label_visibility, 0.5)  # 每0.5秒切换文字可见性

        self.schedule(self.check_input)

    def update_label_visibility(self, dt):
        self.start_label.visible = not self.start_label.visible
        self.exit_label.visible = not self.exit_label.visible
        self.check_start_game()

    def check_input(self, dt):
        self.check_start_game()

    def check_start_game(self):
        if self.keys[pyglet.window.key.SPACE]:
            # 按下空格键开始游戏

            main_menu = MainMenu()
            cocos.director.director.replace(main_menu)
            # main_menu_scene = cocos.scene.Scene(MainMenu())
            # cocos.director.director.replace(main_menu_scene)
            # cocos.director.director.pop()
            self.stop_scheduler()

    def stop_scheduler(self):
        self.unschedule(self.update_label_visibility)
        self.unschedule(self.check_input)
        self.unschedule(self.check_start_game)

    def on_exit(self):
        pass


class ColorMenuItem(MenuItem):
    def __init__(self, label, callback, color=(255, 255, 255)):
        super(ColorMenuItem, self).__init__(label, callback)
        self.color = color  # 设置文本颜色

    def generate_label(self):
        # 调用父类的generate_label函数来生成label
        super(ColorMenuItem, self).generate_label()
        # 设置label的颜色
        if self.label is not None:
            self.label.element.color = self.color


# 程序从这里开始


if __name__ == "__main__":
    cocos.director.director.init(width=2400, height=1600, caption="原神.exe", fullscreen=True)  # 记得改游戏界面大小
    cocos.director.director.run(GameStart())
