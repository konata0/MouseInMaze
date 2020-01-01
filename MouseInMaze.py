import sys
import os
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QUrl, QFileInfo
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QMessageBox
import json


class MainWindow(object):
    def __init__(self):
        # UI
        self.main_window = None
        self.centralWidget = None
        self.webView = None
        self.label_parameter = None
        self.label_fire_on_period = None
        self.edit_fire_on_period = None
        self.label_fire_off_period = None
        self.edit_fire_off_period = None
        self.label_anime_speed = None
        self.edit_anime_speed = None
        self.label_alpha = None
        self.edit_alpha = None
        self.label_gamma = None
        self.edit_gamma = None
        self.label_random = None
        self.edit_random = None
        self.label_epoch = None
        self.edit_epoch = None
        self.label_max_step = None
        self.edit_max_step = None
        self.button_parameter = None
        self.button_start_learn = None
        self.button_start_run = None
        self.maze_list = None
        # 缓存数据
        self.maze_list_string = []
        self.maze = None
        self.fire_on = 2
        self.fire_off = 2
        self.anime_speed = 1
        self.alpha = 0.5
        self.gamma = 0.9
        self.random = 0.1
        self.epoch = 10
        self.max_step = 100

    def setup_ui(self, main_window):
        self.main_window = main_window
        self.main_window.setObjectName("mainWindow")
        self.main_window.setWindowModality(QtCore.Qt.WindowModal)
        self.main_window.setFixedSize(960, 720)
        self.main_window.setStyleSheet("#mainWindow{background-color: #f6f6f6}")
        self.centralWidget = QtWidgets.QWidget(self.main_window)
        self.centralWidget.setObjectName("centralWidget")

        # web动画显示迷宫
        self.webView = QWebEngineView(self.centralWidget)
        self.webView.setGeometry(QtCore.QRect(30, 30, 660, 660))
        self.webView.load(QUrl(QFileInfo("./anime.html").absoluteFilePath()))

        # 参数设置
        self.label_parameter = QtWidgets.QLabel(self.centralWidget)
        self.label_parameter.setGeometry(QtCore.QRect(720, 30, 210, 30))
        self.label_parameter.setObjectName("label_parameter")
        self.label_parameter.setText("参数设置：")

        self.label_fire_on_period = QtWidgets.QLabel(self.centralWidget)
        self.label_fire_on_period.setGeometry(QtCore.QRect(720, 70, 100, 30))
        self.label_fire_on_period.setObjectName("label_fire_on_period")
        self.label_fire_on_period.setText("火焰生成时长：")
        self.edit_fire_on_period = QtWidgets.QLineEdit(self.centralWidget)
        self.edit_fire_on_period.setGeometry(QtCore.QRect(850, 70, 80, 30))
        self.edit_fire_on_period.setObjectName("edit_fire_on_period")
        self.edit_fire_on_period.setAlignment(QtCore.Qt.AlignCenter)

        self.label_fire_off_period = QtWidgets.QLabel(self.centralWidget)
        self.label_fire_off_period.setGeometry(QtCore.QRect(720, 110, 100, 30))
        self.label_fire_off_period.setObjectName("label_fire_off_period")
        self.label_fire_off_period.setText("火焰停歇时长：")
        self.edit_fire_off_period = QtWidgets.QLineEdit(self.centralWidget)
        self.edit_fire_off_period.setGeometry(QtCore.QRect(850, 110, 80, 30))
        self.edit_fire_off_period.setObjectName("edit_fire_off_period")
        self.edit_fire_off_period.setAlignment(QtCore.Qt.AlignCenter)

        self.label_anime_speed = QtWidgets.QLabel(self.centralWidget)
        self.label_anime_speed.setGeometry(QtCore.QRect(720, 150, 100, 30))
        self.label_anime_speed.setObjectName("label_anime_speed")
        self.label_anime_speed.setText("速度(tick/s)：")
        self.edit_anime_speed = QtWidgets.QLineEdit(self.centralWidget)
        self.edit_anime_speed.setGeometry(QtCore.QRect(850, 150, 80, 30))
        self.edit_anime_speed.setObjectName("edit_anime_speed")
        self.edit_anime_speed.setAlignment(QtCore.Qt.AlignCenter)

        self.label_alpha = QtWidgets.QLabel(self.centralWidget)
        self.label_alpha.setGeometry(QtCore.QRect(720, 190, 100, 30))
        self.label_alpha.setObjectName("label_alpha")
        self.label_alpha.setText("学习效率：")
        self.edit_alpha = QtWidgets.QLineEdit(self.centralWidget)
        self.edit_alpha.setGeometry(QtCore.QRect(850, 190, 80, 30))
        self.edit_alpha.setObjectName("edit_alpha")
        self.edit_alpha.setAlignment(QtCore.Qt.AlignCenter)

        self.label_gamma = QtWidgets.QLabel(self.centralWidget)
        self.label_gamma.setGeometry(QtCore.QRect(720, 230, 100, 30))
        self.label_gamma.setObjectName("label_gamma")
        self.label_gamma.setText("折现因子：")
        self.edit_gamma = QtWidgets.QLineEdit(self.centralWidget)
        self.edit_gamma.setGeometry(QtCore.QRect(850, 230, 80, 30))
        self.edit_gamma.setObjectName("edit_gamma")
        self.edit_gamma.setAlignment(QtCore.Qt.AlignCenter)

        self.label_random = QtWidgets.QLabel(self.centralWidget)
        self.label_random.setGeometry(QtCore.QRect(720, 270, 100, 30))
        self.label_random.setObjectName("label_random")
        self.label_random.setText("随机选择概率：")
        self.edit_random = QtWidgets.QLineEdit(self.centralWidget)
        self.edit_random.setGeometry(QtCore.QRect(850, 270, 80, 30))
        self.edit_random.setObjectName("edit_random")
        self.edit_random.setAlignment(QtCore.Qt.AlignCenter)

        self.label_epoch = QtWidgets.QLabel(self.centralWidget)
        self.label_epoch.setGeometry(QtCore.QRect(720, 310, 100, 30))
        self.label_epoch.setObjectName("label_epoch")
        self.label_epoch.setText("训练次数：")
        self.edit_epoch = QtWidgets.QLineEdit(self.centralWidget)
        self.edit_epoch.setGeometry(QtCore.QRect(850, 310, 80, 30))
        self.edit_epoch.setObjectName("edit_epoch")
        self.edit_epoch.setAlignment(QtCore.Qt.AlignCenter)

        self.label_max_step = QtWidgets.QLabel(self.centralWidget)
        self.label_max_step.setGeometry(QtCore.QRect(720, 350, 100, 30))
        self.label_max_step.setObjectName("label_epoch")
        self.label_max_step.setText("最大步数限制：")
        self.edit_max_step = QtWidgets.QLineEdit(self.centralWidget)
        self.edit_max_step.setGeometry(QtCore.QRect(850, 350, 80, 30))
        self.edit_max_step.setObjectName("edit_max_step")
        self.edit_max_step.setAlignment(QtCore.Qt.AlignCenter)

        self.show_parameter()

        # button
        self.button_parameter = QtWidgets.QPushButton(self.centralWidget)
        self.button_parameter.setGeometry(QtCore.QRect(720, 400, 210, 30))
        self.button_parameter.setObjectName("button_add")
        self.button_parameter.setText("修改参数")
        self.button_parameter.clicked.connect(self.button_parameter_click)

        self.button_start_learn = QtWidgets.QPushButton(self.centralWidget)
        self.button_start_learn.setGeometry(QtCore.QRect(720, 440, 100, 30))
        self.button_start_learn.setObjectName("button_start_learn")
        self.button_start_learn.setText("开始训练")
        self.button_start_learn.clicked.connect(self.button_start_learn_click)

        self.button_start_run = QtWidgets.QPushButton(self.centralWidget)
        self.button_start_run.setGeometry(QtCore.QRect(830, 440, 100, 30))
        self.button_start_run.setObjectName("button_start_run")
        self.button_start_run.setText("开始运行")
        self.button_start_run.clicked.connect(self.button_start_run_click)

        # 迷宫选择
        self.maze_list = QtWidgets.QListView(self.centralWidget)
        self.maze_list.setGeometry(QtCore.QRect(720, 490, 210, 200))
        self.maze_list.setObjectName("maze_list")
        self.set_maze_list()

        self.main_window.setCentralWidget(self.centralWidget)
        self.retranslate_ui()
        QtCore.QMetaObject.connectSlotsByName(self.main_window)

    def retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.main_window.setWindowTitle(_translate("mainWindow", "Mouse In Maze"))

    def show_parameter(self):
        self.edit_fire_on_period.setText(str(self.fire_on))
        self.edit_fire_off_period.setText(str(self.fire_off))
        self.edit_anime_speed.setText(str(self.anime_speed))
        self.edit_alpha.setText(str(self.alpha))
        self.edit_gamma.setText(str(self.gamma))
        self.edit_random.setText(str(self.random))
        self.edit_epoch.setText(str(self.epoch))
        self.edit_max_step.setText(str(self.max_step))

    def set_maze_list(self):
        dirs = os.listdir("./maze")
        self.maze_list_string = []
        for file_name in dirs:
            if file_name.endswith(".json"):
                self.maze_list_string.append(file_name[0: -5])
        slm = QtCore.QStringListModel()
        slm.setStringList(self.maze_list_string)
        self.maze_list.setModel(slm)
        self.maze_list.clicked.connect(self.maze_list_click)
        self.maze_list.doubleClicked.connect(self.maze_list_click)

    def button_parameter_click(self):
        temp_fire_on = self.edit_fire_on_period.text()
        temp_fire_off = self.edit_fire_off_period.text()
        temp_anime_speed = self.edit_anime_speed.text()
        temp_alpha = self.edit_alpha.text()
        temp_gamma = self.edit_gamma.text()
        temp_random = self.edit_random.text()
        temp_epoch = self.edit_epoch.text()
        temp_max_step = self.edit_max_step.text()
        try:
            temp_fire_on = int(temp_fire_on)
            if temp_fire_on < 0:
                raise Exception("wrong range!", temp_fire_on)
        except:
            QMessageBox.information(self.main_window, "错误", "火焰生成时间必须为非负整数！", QMessageBox.Ok)
            self.show_parameter()
            return
        try:
            temp_fire_off = int(temp_fire_off)
            if temp_fire_off < 0:
                raise Exception("wrong range!", temp_fire_off)
        except:
            QMessageBox.information(self.main_window, "错误", "火焰停歇时间必须为非负整数！", QMessageBox.Ok)
            self.show_parameter()
            return
        try:
            temp_anime_speed = int(temp_anime_speed)
            if temp_fire_off <= 0 or temp_anime_speed > 100:
                raise Exception("wrong range!", temp_anime_speed)
        except:
            QMessageBox.information(self.main_window, "错误", "速度必须为不大于100的正整数！", QMessageBox.Ok)
            self.show_parameter()
            return
        try:
            temp_alpha = float(temp_alpha)
            if temp_fire_off <= 0 or temp_alpha >= 1:
                raise Exception("wrong range!", temp_anime_speed)
        except:
            QMessageBox.information(self.main_window, "错误", "学习速率大小必须在(0, 1)！", QMessageBox.Ok)
            self.show_parameter()
            return
        try:
            temp_gamma = float(temp_gamma)
            if temp_gamma < 0 or temp_gamma > 1:
                raise Exception("wrong range!", temp_gamma)
        except:
            QMessageBox.information(self.main_window, "错误", "折现因子大小必须在[0, 1]！", QMessageBox.Ok)
            self.show_parameter()
            return
        try:
            temp_random = float(temp_random)
            if temp_random < 0 or temp_random > 1:
                raise Exception("wrong range!", temp_gamma)
        except:
            QMessageBox.information(self.main_window, "错误", "随机概率大小必须在[0, 1]！", QMessageBox.Ok)
            self.show_parameter()
            return
        try:
            temp_epoch = int(temp_epoch)
            if temp_epoch <= 0 or temp_epoch > 30:
                raise Exception("wrong range!", temp_epoch)
        except:
            QMessageBox.information(self.main_window, "错误", "训练次数必须为[1, 30]的整数！", QMessageBox.Ok)
            self.show_parameter()
            return
        try:
            temp_max_step = int(temp_max_step)
            if temp_max_step <= 0 or temp_max_step > 400:
                raise Exception("wrong range!", temp_max_step)
        except:
            QMessageBox.information(self.main_window, "错误", "最大步数限制必须为[1, 400]的整数！", QMessageBox.Ok)
            self.show_parameter()
            return
        self.fire_on = temp_fire_on
        self.fire_off = temp_fire_off
        self.anime_speed = temp_anime_speed
        self.alpha = temp_alpha
        self.gamma = temp_gamma
        self.random = temp_random
        self.epoch = temp_epoch
        self.max_step = temp_max_step
        self.show_parameter()
        QMessageBox.information(self.main_window, "成功", "修改参数成功！", QMessageBox.Ok)
        print("参数修改完成！")
        return

    def button_start_learn_click(self):
        pass

    def button_start_run_click(self):
        pass

    def maze_list_click(self, index):
        maze_file_name = "./maze/" + self.maze_list_string[index.row()] + ".json"
        file = open(maze_file_name, encoding='utf-8')
        temp_maze = np.array(json.loads(file.read()))
        file.close()
        # 迷宫数据格式内容验证
        flag = True
        if temp_maze.ndim != 2:
            flag = False
        elif temp_maze.shape[0] != temp_maze.shape[1]:
            flag = False
        elif temp_maze.shape[0] < 3:
            flag = False
        else:
            start_number = 0
            end_number = 0
            for element in temp_maze.flat:
                if element == 1:
                    start_number += 1
                if element == 2:
                    end_number += 1
            if start_number != 1 or end_number != 1:
                flag = False
        if flag is False:
            QMessageBox.information(self.main_window, "错误", "迷宫数据格式错误！", QMessageBox.Ok)
            return
        self.maze = temp_maze
        for i in range(0, self.maze.shape[0]):
            for j in range(0, self.maze.shape[1]):
                if self.maze[i, j] != -2 and self.maze[i, j] != -1 and self.maze[i, j] != 1 and self.maze[i, j] != 2:
                    self.maze[i, j] = 0
        print("已选择迷宫：")
        print(self.maze)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = MainWindow()
    ui.setup_ui(window)
    window.show()
    sys.exit(app.exec_())

