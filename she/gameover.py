# -*- coding: utf-8 -*-
import cocos
from cocos.director import director
import define

class Gameover(cocos.layer.ColorLayer):
    def __init__(self):
        window_width, window_height = cocos.director.director.get_window_size()
        # background_width, background_height = window_width // 2, window_height // 2

        super(Gameover, self).__init__(200, 235, 235, 200, width=window_width, height=window_height)

        # position_x = 0
        # position_y = 0
        # self.position = position_x, position_y

        self.visible = False
        self.score = cocos.text.Label('',
                                      font_name='SimHei',
                                      font_size=72,
                                      color=define.MAROON)
        self.score.position = window_width // 2, window_height // 2 + window_height // 16
        self.add(self.score)

        text = cocos.text.Label('score: ',
                                font_name='SimHei',
                                font_size=72,
                                color=define.MAROON)
        text.position = window_width // 2 - window_width // 8, window_height // 2 + window_height // 16
        self.add(text)
        text = cocos.text.Label('click or press J key to replay,',
                                font_name='SimHei',
                                font_size=48,
                                color=define.MAROON)
        text.position = window_width // 2 - window_width // 4, window_height // 2 - window_height // 16
        self.add(text)
        text = cocos.text.Label('or press BACKSPACE key to go back...',
                                font_name='SimHei',
                                font_size=48,
                                color=define.MAROON)
        text.position = window_width // 2 - window_width // 4, window_height // 2 - window_height // 8
        self.add(text)
