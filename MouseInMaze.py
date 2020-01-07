import sys
import os
import time
import threading
import numpy as np
import math
from PyQt5 import QtCore, QtWidgets
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
        self.button_anime_switch = None
        self.button_start_learn = None
        self.button_start_run = None
        self.maze_list = None
        # 奖励参数
        self.r_normal = -0.01
        self.r_wall = -0.3
        self.r_fire = -0.5
        self.r_cake = 50
        # 缓存数据
        self.running = False
        self.anime_switch = True
        self.maze_list_string = []
        self.maze = None
        self.fire_on = 2
        self.fire_off = 2
        self.anime_speed = 5
        self.alpha = 0.5
        self.gamma = 0.9
        self.random = 0.1
        self.epoch = 10
        self.max_step = 100
        self.x = -1
        self.y = -1
        self.step = 0
        self.q_table = None


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
        self.button_parameter.setGeometry(QtCore.QRect(720, 400, 100, 30))
        self.button_parameter.setObjectName("button_add")
        self.button_parameter.setText("修改参数")
        self.button_parameter.clicked.connect(self.button_parameter_click)

        self.button_anime_switch = QtWidgets.QPushButton(self.centralWidget)
        self.button_anime_switch.setGeometry(QtCore.QRect(830, 400, 100, 30))
        self.button_anime_switch.setObjectName("button_anime_switch")
        self.button_anime_switch.setText("关闭动画")
        self.button_anime_switch.clicked.connect(self.button_anime_switch_click)

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
        if self.running:
            QMessageBox.information(self.main_window, "错误", "程序运行中，禁止修改操作！", QMessageBox.Ok)
            self.show_parameter()
            return
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
            if temp_fire_off <= 0 or temp_anime_speed > 10:
                raise Exception("wrong range!", temp_anime_speed)
        except:
            QMessageBox.information(self.main_window, "错误", "速度必须为不大于10的正整数！", QMessageBox.Ok)
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
        self.run_js_set_parameter()
        return

    def button_anime_switch_click(self):
        if self.running:
            QMessageBox.information(self.main_window, "错误", "程序运行中，禁止修改操作！", QMessageBox.Ok)
            return
        if self.anime_switch is True:
            self.anime_switch = False
            self.button_anime_switch.setText("开启动画")
        else:
            self.anime_switch = True
            self.button_anime_switch.setText("关闭动画")
        QMessageBox.information(self.main_window, "成功", "修改成功！", QMessageBox.Ok)
        return

    def button_start_learn_click(self):
        if self.running:
            QMessageBox.information(self.main_window, "错误", "程序运行中，禁止修改操作！", QMessageBox.Ok)
            return
        if self.maze is None:
            QMessageBox.information(self.main_window, "错误", "请先选择地图！", QMessageBox.Ok)
            return
        threading.Thread(target=self.thread_learn).start()

    def thread_learn(self):
        self.running = True
        # 训练epoch次
        for e in range(0, self.epoch):
            # 回到起点位置
            self.step = 0
            for i in range(0, self.maze.shape[0]):
                for j in range(0, self.maze.shape[1]):
                    if self.maze[i, j] == 1:
                        self.x = i
                        self.y = j
            action_record = []
            # 训练主循环
            while True:
                self.step += 1
                # 达到最大步数限制或者到达终点跳出
                if self.step > self.max_step:
                    break
                if self.maze[self.x, self.y] == 2:
                    break
                # 根据Q表和当前参数获取action
                # 0:up    1:down    2:left    3:right
                action = self.get_action()
                # 下一状态
                x_next = self.x
                y_next = self.y
                if action == 0:
                    x_next -= 1
                elif action == 1:
                    x_next += 1
                elif action == 2:
                    y_next -= 1
                else:
                    y_next += 1
                # 回报判断（同时撞墙返回）
                r = self.r_normal
                flag = False
                if x_next < 0:
                    x_next = 0
                    r = self.r_wall
                    flag = True
                elif x_next >= self.maze.shape[0]:
                    x_next = self.maze.shape[0] - 1
                    r = self.r_wall
                    flag = True
                elif y_next < 0:
                    y_next = 0
                    r = self.r_wall
                    flag = True
                elif y_next >= self.maze.shape[1]:
                    y_next = self.maze.shape[1] - 1
                    r = self.r_wall
                    flag = True
                elif self.maze[x_next, y_next] == -1:
                    x_next = self.x
                    y_next = self.y
                    r = self.r_wall
                    flag = True
                else:
                    pass
                if flag is True:
                    action_record.append(int(action + 10))
                else:
                    action_record.append(int(action))
                    if self.maze[x_next, y_next] == -2 and self.check_fire_on():
                        r = self.r_fire
                    if self.maze[x_next, y_next] == 2:
                        r = self.r_cake
                # 更新Q表
                t = self.gamma * (np.max(self.q_table[x_next, y_next]) - self.q_table[self.x, self.y, action])
                self.q_table[self.x, self.y, action] += self.alpha * (r + t)
                # 进入下一状态
                self.x = x_next
                self.y = y_next
            # 一次训练完成，传action记录到动画显示，主界面等待相应时间
            if self.anime_switch:
                self.run_js_set_action(action_record)
                time.sleep(len(action_record) / self.anime_speed + 0.5)
        self.run_js_alert("训练完成！")
        self.running = False
        return

    def button_start_run_click(self):
        if self.running:
            QMessageBox.information(self.main_window, "错误", "程序运行中，禁止修改操作！", QMessageBox.Ok)
            return
        if self.maze is None:
            QMessageBox.information(self.main_window, "错误", "请先选择地图！", QMessageBox.Ok)
            return
        threading.Thread(target=self.thread_run).start()

    def thread_run(self):
        self.running = True
        # 回到起点位置
        self.step = 0
        for i in range(0, self.maze.shape[0]):
            for j in range(0, self.maze.shape[1]):
                if self.maze[i, j] == 1:
                    self.x = i
                    self.y = j
        action_record = []
        found = False
        while True:
            self.step += 1
            # 达到最大步数限制或者到达终点跳出
            if self.step >= self.maze.shape[0] * self.maze.shape[1]:
                break
            if self.step >= self.max_step:
                break
            if self.maze[self.x, self.y] == 2:
                found = True
                break
            # 根据Q表获取action
            # 0:up    1:down    2:left    3:right
            action = int(np.argmax(self.q_table[self.x, self.y]))
            # 下一状态
            x_next = self.x
            y_next = self.y
            if action == 0:
                x_next -= 1
            elif action == 1:
                x_next += 1
            elif action == 2:
                y_next -= 1
            else:
                y_next += 1
            # 判断撞墙返回
            flag = False
            if x_next < 0:
                flag = True
            elif x_next >= self.maze.shape[0]:
                flag = True
            elif y_next < 0:
                flag = True
            elif y_next >= self.maze.shape[1]:
                flag = True
            elif self.maze[x_next, y_next] == -1:
                flag = True
            else:
                pass
            if flag is True:
                break
            else:
                self.x = x_next
                self.y = y_next
                action_record.append(action)
        # 计算完成，传入动画显示，主界面延迟后显示结果
        self.run_js_set_action(action_record)
        time.sleep(len(action_record) / self.anime_speed + 0.5)
        if found:
            self.run_js_alert("成功找到！")
        else:
            self.run_js_alert("训练不足或受到最大步数限制限制，未能找到！")
        self.running = False
        return

    def maze_list_click(self, index):
        if self.running:
            QMessageBox.information(self.main_window, "错误", "程序运行中，禁止修改操作！", QMessageBox.Ok)
            return
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
        self.run_js_set_maze()
        # 初始化Q表
        self.init_q_table()

    def init_q_table(self):
        self.q_table = np.zeros([self.maze.shape[0], self.maze.shape[1], 4])
        for i in range(0, self.maze.shape[0]):
            for j in range(0, self.maze.shape[1]):
                for a in range(0, 4):
                    ii = i
                    jj = j
                    if_hit_wall = False
                    if a == 0:
                        ii -= 1
                    elif a == 1:
                        ii += 1
                    elif a == 2:
                        jj -= 1
                    else:
                        jj += 1
                    if ii < 0 or ii >= self.maze.shape[0]:
                        if_hit_wall = True
                    elif jj < 0 or jj >= self.maze.shape[1]:
                        if_hit_wall = True
                    elif self.maze[ii, jj] == -1:
                        if_hit_wall = True
                    else:
                        pass
                    if if_hit_wall:
                        # 撞墙设为负无穷
                        self.q_table[i, j, a] = float("-inf")
                        pass

    def get_action(self):
        # 随机选择
        if np.random.rand(1)[0] < self.random:
            re = -1
            while True:
                re = np.argmax(np.random.rand(4))
                if not math.isinf(self.q_table[self.x, self.y, re]):
                    break
            return re
        # 从Q表选择
        else:
            return np.argmax(self.q_table[self.x, self.y])

    def check_fire_on(self):
        return ((self.step - 1) % (self.fire_on + self.fire_off)) < self.fire_on

    def run_js_set_maze(self):
        parameter_string = json.dumps(self.maze.tolist(), ensure_ascii=False)
        self.webView.page().runJavaScript("setMaze(" + parameter_string + ")")

    def run_js_set_parameter(self):
        js_string = "setParameter("
        js_string += str(self.fire_on) + ","
        js_string += str(self.fire_off) + ","
        js_string += str(self.anime_speed) + ")"
        self.webView.page().runJavaScript(js_string)

    def run_js_set_action(self, action_list):
        parameter_string = json.dumps(action_list, ensure_ascii=False)
        self.webView.page().runJavaScript("setAction(" + parameter_string + ")")

    def run_js_alert(self, string):
        self.webView.page().runJavaScript("alert('" + string + "');")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = MainWindow()
    ui.setup_ui(window)
    window.show()
    sys.exit(app.exec_())

