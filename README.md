**Note: The final version of the game is in the "test" folder of main branch**



**snake.io: Gluttonous**

   Welcome to the Gluttonous! Dive into a world where you control a snake to eat fruit, grow longer, dodge and try to block to eliminate enemies by your body. This README file provides all the details you need to start playing, including control method, game process, installation instructions, and other information.

**Control Method**

   ·Change Direction: Use the Arrow Keys.
   
   ·Pause/Resume: Press SPACE or use the mouse to select the appropriate option on the pause panel to pause or resume the game.
   
   ·Restart: Press 'J' key or use the mouse to select the appropriate option on the pause panel to restart the game.
   
   ·Exit the arena: Press BACKSPACE or use the mouse to select the appropriate option on the pause panel to return to the homepage.
   
   ·Return to previous page: Press BACKSPACE or use the mouse to select the appropriate option to return to previous page from current page.

   ·Login/Register: Create a new account or log in to access saved game data in the login/register page.
   
   ·Guest Login: Try Classic Mode without creating an account in the login/register page.

**Game Process**

   **Main Menu**
   
   **1. Select Game Mode**
   
   We have several game modes. In addition to the Classic modes, there is also an infinite mode (Unlimited Firepower Mode),
   
   · Classic Mode:
      Difficulty Levels: Easy, Normal, Hard
      Features: Adjustable movement speeds, score ratios, and enemy counts.
   
   · Unlimited Firepower Mode:
      Description: Continuously evade enemies and aim for the highest score in an endless survival challenge.
   
   **2. Shop**

   Customize your snake with various skins available for purchase in the game shop to enhance your gaming experience.

   **3. Ranking**

   Check out the leaderboard to see top scores and compete with other players.

   **4. Settings**

   Adjust game settings like sound level and background music. Settings are saved automatically.

   **Arena**
   
   **Pause Menu**

   Pause the game in the arena at any time to restart/exit the game.

   **Scoreboard**
   View the current attributes of the snake controlled by the player and the score ranking of all players in real time.

**Installation (Ubuntu)**

   To run the game on Ubuntu, follow these steps in a command prompt:

   1. Install Python:

      sudo apt update sudo

      apt install python3
      
   2. Install Required Packages:

      pip install pygame

      pip install cocos2d

      pip install pyglet

      pip install mysql-connector-python

      Here is how to import a stable version of the game: pip install pyglet==1.5.21 cocos2d==0.6.9
   
   3. Run the Game:

      python3 gluttonous.py
   
   Then use keyboard and/or mouse to operate the game.

**Other Notes**
   1. The game is in fullscreen mode by default, if you need to see the console output to debug your code, remember to modify the fullscreen parameter in cocos.director.director.init(width=2560, height=1600, caption=“GluttonousGame.exe”, fullscreen=True) in the main function of gluttonous.py to False
   2. music source：https://www.bilibili.com/video/BV12T4y1h7Zk/?spm_id_from=333.788.recommend_more_video.10&vd_source=9dd862afa0c8cef53c73256400624867
