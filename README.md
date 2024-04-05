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

——————————————————————————————————————————————————————分割线——————————————————————————————————————————————————————

更新日志



20240404.23

更新内容
加入了开始界面、主菜单界面、暂停界面
修复了原版分数增长至约300-600时就卡死的bug，但是在分数约两三千时仍然可能卡死
优化了蛇伸长和转向的动画效果
优化了蛇的出生逻辑，使得不容易出生就死
优化了circle.png的清晰度，由16像素至64像素
优化了蛇头美术
优化了结束界面和分数面板

待修复问题：
在每次进入经典模式时，没能屏蔽暂停面板的相应（代码已作修改但是没找到问题所在），导致上下键和enter键相应的是暂停面板。
解决方法是不返回主菜单，直接重开，然后就可以正常使用上下键，并且误触enter键不会造成不良后果
经常会在arena的（0，0）坐标处生成蛇身，导致轻微卡顿。蛇身堆积很可能是在分数两三千时彻底卡死的原因。
电脑蛇在游玩时间达到一定时长后身体会有一定的分离，推断可能是上一个问题导致的间接结果，或是路径记录误差累积的结果
其他模式、商店、设置
直接按exit时会导致释放了不该释放的锁，以及内存处理等问题。



20240405.09

更新内容
修复了gluttonous.py中各个场景（scene）和层（layer）没有被恰当禁用的问题
小部分优化了gameover.py
优化了在目前每个界面按ESC键的返回、退出逻辑
更新了安装cocos2d和pyglet的描述

待修复问题：
经常会在arena的（0，0）坐标处生成蛇身，导致轻微卡顿。从约一千分起开始容易观测到。蛇身堆积很可能是在分数两三千时彻底卡死的原因。
电脑蛇在游玩时间达到一定时长后身体会有一定的分离，推断可能是上一个问题导致的间接结果，同时也有小部分路径记录误差累积的结果
总之还是要解决（0，0）坐标处生成蛇身的问题，这个add_body()中的问题是最底层的问题
也几乎是唯一的问题（目前）
视野大小的调整
其他模式、商店、设置
内存处理等问题。
在全屏模式下按ESC可能会触发释放一个已经释放的锁的问题（主要是pyglet包自身的bug）
