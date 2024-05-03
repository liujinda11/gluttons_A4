
！！！ The final version is in the main branch's test folder ！！！



**snake.io:Gluttonous Snake Game**

   Welcome to the Gluttonous Snake Game! Dive into a world where you control a snake to eat fruit, grow longer, and dodge enemies. This README provides all the details you need to start playing, including installation instructions, game modes, controls, and more.

**Game Controls**

   ·Change Direction: Use the Arrow Keys or WASD.
   
   ·Pause/Resume: Press SPACE to toggle pause and resume.
   
   ·Restart: Press 'J' to restart the game from any state.
   
   ·Home: Press BACKSPACE to return to the homepage from the game or pause menu.
   
   ·BACKSPACE: Return to the homepage scene from the game or pause menu.

（1）login/register page

   ·Login/Register: Create a new account or log in to access saved game data.
   
   ·Guest Login: Try the Classic Mode without creating an account.

（2）Games Home

**1. different mode：**
   
   We have several game modes. In addition to the classic game modes, there is also an infinite mode,
   
   · Classic Mode:
      Difficulty Levels: Easy, Medium, Hard
      Features: Adjustable movement speeds, score ratios, and enemy counts.
   
   · Infinite Mode:
      Description: Continuously evade enemies and aim for the highest score in an endless survival challenge.
   
**2. Shop：**

   Customize your snake with various skins available for purchase in the game shop to enhance your gaming experience.

**3. Rankings：**

   Check out the leaderboard to see top scores and compete with other players.

**4. Settings：**

   Adjust game settings like sound level and background music. Settings are saved automatically.

**5. Pause Menu：**

   Pause the game at any time to view current scores or to restart/exit the game.


**Installation (Ubuntu):**

   To run the game on Ubuntu, follow these steps in a command prompt:

   1. Install Python:

      sudo apt update sudo

      apt install python3
      
   2. Install Required Packages:

      pip install pygame

      pip install cocos (actually cocos2d)

      pip install pyglet

      pip install mysql-connector-python

      Here's how to import a stable version of the game: pip install pyglet==1.5.21 cocos2d==0.6.9
   
   3. Run the Game:

      python3 gluttonous.py
   
   Then use keyboard and mouse to operate the game.

**Note: **
   1. The game is in fullscreen mode by default, if you need to see the console output to debug your code, 
   remember to put cocos.director.director.init(width=2400, height=1600, caption=“GluttonousGame.exe”, fullscreen=True) in the main function of gluttonous.py. fullscreen=True) in the fullscreen parameter is changed to False
   2. music：https://www.bilibili.com/video/BV12T4y1h7Zk/?spm_id_from=333.788.recommend_more_video.10&vd_source=9dd862afa0c8cef53c73256400624867
