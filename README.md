# MouseInMaze
人工智能基础第三次大作业，强化训练老鼠走迷宫

## 语言
UI界面和强化学习主要逻辑由python3.7实现，动画由html实现

## 使用的python库
sys，os，time，threading，numpy，math，json，PyQt5    
其中，需要：    
from PyQt5.QtWebEngineWidgets import QWebEngineView    
可能会因为pyqt5的版本出现问题，如果出现没有yQt5.QtWebEngineWidgets模块，可尝试安装pyqt5.7.1    
pip install PyQt5==5.7.1    
或是直接安装    
pip install PyQtWebEngine

## 迷宫格式
迷宫以json文件存储在maze文件夹下，具体内容由二维数组表示，如：    
[[1,0,0,-1],    
[0,-1,-2,0],    
[0,-1,0,-1],    
[0,0,0,2]]    
其中：    
1为老鼠起点位置，2为蛋糕（终点）位置，-1为墙壁，-2为周期性火焰，0为正常通路    



