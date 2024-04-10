

# -*- coding: utf-8 -*-
import cocos
from cocos.director import director
import define
import account

class Gameover(cocos.layer.ColorLayer):
    def __init__(self, username):
        window_width, window_height = cocos.director.director.get_window_size()
        # background_width, background_height = window_width // 2, window_height // 2

        super(Gameover, self).__init__(
            200, 235, 235, 200,
            width=window_width,
            height=window_height
        )

        # position_x = 0
        # position_y = 0
        # self.position = position_x, position_y
        self.username = username
        self.visible = False
        self.score = cocos.text.Label(
            '',
            font_name='SimHei',
            font_size=72,
            color=define.MAROON
        )
        self.score.position = window_width // 2, window_height // 2 + window_height // 16
        self.add(self.score)

        text = cocos.text.Label(
            'score: ',
            font_name='SimHei',
            font_size=72,
            color=define.MAROON
        )
        text.position = window_width // 2 - window_width // 8, window_height // 2 + window_height // 16
        self.add(text)

        self.record_score = cocos.text.Label(
            '',
            font_name='SimHei',
            font_size=72,
            color=define.MAROON
        )
        self.record_score.position = window_width // 2, window_height // 2 + window_height // 14
        self.add(self.record_score)

        text = cocos.text.Label(
            'record score: ',
            font_name='SimHei',
            font_size=72,
            color=define.MAROON
        )
        text.position = window_width // 2 - window_width // 8, window_height // 2 + window_height // 14
        self.add(text)



        text = cocos.text.Label(
            '   J or Click    -    Restart Game',
            font_name='SimHei',
            font_size=48,
            color=define.MAROON
        )
        text.position = window_width // 2 - window_width // 4, window_height // 2 - window_height // 16
        self.add(text)

        text = cocos.text.Label(
            'BACKSPACE - Back to Homepage',
            font_name='SimHei',
            font_size=48,
            color=define.MAROON
        )
        text.position = window_width // 2 - window_width // 4, window_height // 2 - window_height // 8
        self.add(text)
