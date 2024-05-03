
！！！ The final version is in the main branch's test folder ！！！



snake.io

   Welcome to the Gluttonous Snake Game, a fun and engaging game where you control a snake to eat fruit, grow longer, and avoid enemies. This README provides all the necessary details to get you started, including installation instructions, game modes, controls, and more.

Game Controls

   Change Direction: Use Arrow Keys or WASD
   SPACE: Toggle pause and resume the game.
   J: Restart the game from any state.
   BACKSPACE: Return to the homepage scene from the game or pause menu.

（1）login/register page

   ·Login/Register: Create a new account or log in to access saved game data.
   
   ·Guest Login: Try the Classic Mode without creating an account.

（2）Games Home

1. different mode：
   
   We have several game modes. In addition to the classic game modes, there is also an infinite mode,
   
   · Classic Mode:
      Difficulty Levels: Easy, Medium, Hard
      Features: Adjust movement speeds, score ratios, and number of enemies.
   
   · Infinite Mode:
      Description: Survive as long as possible with continuous enemy spawns. Aim for the highest score!
   
2. shop：

   Customize your snake with various skins available for purchase in the game shop to enhance your gaming experience.

3. rank：

   Check out the leaderboard to see top scores and compete with other players.

4. setting：

   Customize game settings such as sound level and background music. Settings are saved automatically.

5. pause menu

   Pause the game at any time to view current scores or to restart/exit the game.


Regardless of the original or new version, this is how you can run it on Ubuntu: In a command prompt.

   1. Install python: sudo apt update sudo apt install python3
   2. Install various packages:

      pip install pygame

      pip install cocos (actually cocos2d)

      pip install pyglet

      pip install mysql-connector-python

      Here's how to import a stable version of the game: pip install pyglet==1.5.21 cocos2d==0.6.9
   
   3. Interpret the python file: python3 gluttonous.py
   Then use keyboard and mouse to operate the game.

Note: 
   1. The game is in fullscreen mode by default, if you need to see the console output to debug your code, 
   remember to put cocos.director.director.init(width=2400, height=1600, caption=“原神.exe”, fullscreen=True) in the main function of gluttonous.py. fullscreen=True) in the fullscreen parameter is changed to False
   2. music：https://www.bilibili.com/video/BV12T4y1h7Zk/?spm_id_from=333.788.recommend_more_video.10&vd_source=9dd862afa0c8cef53c73256400624867
