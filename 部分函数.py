在你想用的类中定义：

def setup_background(self):
    screen_width, screen_height = cocos.director.director.get_window_size()
    background_sprite = cocos.sprite.Sprite("background.jpg")
    background_sprite.scale_x = background_sprite.width / screen_width
    background_sprite.scale_y = background_sprite.height / screen_height
    background_sprite.position = screen_width / 2, screen_height / 2
    background_sprite.opacity = 128
    self.add(background_sprite, z=0)

并且在类的任意函数（视情况而定，一般是init）调用：
self.setup_background()
以添加背景
其中background_sprite.opacity参数代表了透明度，0，255
位置正中，缩放填充。