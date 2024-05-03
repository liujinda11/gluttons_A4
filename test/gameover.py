

# -*- coding: utf-8 -*-
import cocos
from cocos.director import director
import define
import account

class Gameover(cocos.layer.ColorLayer):
    def __init__(self, username):
        # Get the current window size from the cocos director
        window_width, window_height = cocos.director.director.get_window_size()

        # Initialize the color layer with a semi-transparent gray background
        super(Gameover, self).__init__(
            200, 235, 235, 200,  # RGBA colors for the background
            width=window_width,
            height=window_height
        )

        # Store the username of the player
        self.username = username

        # Initially set the visibility of the game over layer to False
        self.visible = False

        # Create a score label to display the current score
        self.score = cocos.text.Label(
            '',
            font_name='SimHei',  # Font of the text
            font_size=72,  # Font size
            color=define.MAROON  # Color of the text (defined elsewhere)
        )
        # Position the score label in the center of the window, slightly offset
        self.score.position = window_width // 2 + window_width // 10, window_height // 2 + window_height // 16
        self.add(self.score)  # Add the score label to the layer

        # Create and position a static text label that reads "score:"
        text = cocos.text.Label(
            'score: ',
            font_name='SimHei',
            font_size=72,
            color=define.MAROON
        )
        text.position = window_width // 2 - window_width // 8, window_height // 2 + window_height // 16
        self.add(text)  # Add the label to the layer

        # Create a label for displaying the record score
        self.record_score = cocos.text.Label(
            '',
            font_name='SimHei',
            font_size=72,
            color=define.MAROON
        )
        # Position the record score label similarly to the score label, but further down
        self.record_score.position = window_width // 2 + window_width // 10, window_height // 2 + window_height // 8
        self.add(self.record_score)

        # Create and position a static text label that reads "record score:"
        text = cocos.text.Label(
            'record score: ',
            font_name='SimHei',
            font_size=72,
            color=define.MAROON
        )
        text.position = window_width // 2 - window_width // 8, window_height // 2 + window_height // 8
        self.add(text)

        # Instructions for restarting the game
        text = cocos.text.Label(
            '   J or Click    -    Restart Game',
            font_name='SimHei',
            font_size=48,
            color=define.MAROON
        )
        text.position = window_width // 2 - window_width // 4, window_height // 2 - window_height // 16
        self.add(text)

        # Instructions for returning to the homepage
        text = cocos.text.Label(
            'BACKSPACE - Back to Homepage',
            font_name='SimHei',
            font_size=48,
            color=define.MAROON
        )
        text.position = window_width // 2 - window_width // 4, window_height // 2 - window_height // 8
        self.add(text)
