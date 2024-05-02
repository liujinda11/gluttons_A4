不论原版新版，在Ubuntu上都可以这样运行：
在命令提示符中，
1. 安装python：
sudo apt update
sudo apt install python3
2. 安装各类包：
pip install pygame
pip install cocos（实际上是cocos2d）
pip install pyglet
这里给出一个能稳定导本游戏的版本的导入方法：
pip install pyglet==1.5.21 cocos2d==0.6.9
3. 解释python文件：
python3 gluttonous.py

然后用键盘、鼠标操作游戏。

注：游戏默认为全屏模式，如果需要查看控制台输出以调试代码的话，
记得在gluttonous.py的main函数中将cocos.director.director.init(width=2400, height=1600, caption="原神.exe", fullscreen=True)
中的fullscreen参数改为False



snake.io

   This is a casual game. The main game mode is to maneuver the snake to swallow the fruit to get points, grow the body, 
   avoid the head to touch the enemy and the border at the same time, the player needs to do their best to destroy all the enemies with the snake's body.

（1）login/register page

Users can create accounts and log in with existing accounts. The game stores all records of the user's previous play in a database and the player can continue their game! 
As well, the user has the option to experience our base game (only “Classic Mode”, no other features) with a “Guest Login”.

（2）Games Home

1. different mode：
   
   We have several game modes. In addition to the classic game modes, there is also an infinite mode,
   
   Classic Mode: There are three difficulties with different movement speeds, score ratios, and number of enemies, allowing users to debug according to their needs.
   
   Infinite Mode: Players need to survive as long as possible! Enemies will spawn indefinitely, try to get the highest score in a non-stop game!

2. shop：

   Players can change the skin for their game characters on this page to have a more diversified gaming experience!

3. rank：

   Users can check out the top ranked players here. Work hard to become a master of Gluttony!  

4. setting：

   Players can adjust their settings here, including sound level and background music. The database will save the settings before the user logs out.

*pause

   The user can pause the game at any time during the game. The current score can be viewed during pause, and the option to restart the game/exit the game is also available.


Regardless of the original or new version, this is how you can run it on Ubuntu: In a command prompt.

   1. Install python: sudo apt update sudo apt install python3
   2. Install various packages: pip install pygame pip install cocos (actually cocos2d) pip install pyglet Here's how to import a stable version of the game: pip install pyglet==1.5.21 cocos2d==0.6.9
   3. Interpret the python file: python3 gluttonous.py
   Then use keyboard and mouse to operate the game.

Note: 
   1. The game is in fullscreen mode by default, if you need to see the console output to debug your code, 
   remember to put cocos.director.director.init(width=2400, height=1600, caption=“ProtoGod.exe”, fullscreen=True) in the main function of gluttonous.py. fullscreen=True) in the fullscreen parameter is changed to False
   2. music：https://www.bilibili.com/video/BV12T4y1h7Zk/?spm_id_from=333.788.recommend_more_video.10&vd_source=9dd862afa0c8cef53c73256400624867
