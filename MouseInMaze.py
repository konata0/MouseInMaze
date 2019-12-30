import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QUrl, QFileInfo
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QMessageBox
import json


class MainWindow(object):
    def __init__(self):
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

        self.button_parameter = QtWidgets.QPushButton(self.centralWidget)
        self.button_parameter.setGeometry(QtCore.QRect(720, 400, 210, 30))
        self.button_parameter.setObjectName("button_add")
        self.button_parameter.setText("修改参数并初始化")
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







        self.main_window.setCentralWidget(self.centralWidget)
        self.retranslate_ui()
        QtCore.QMetaObject.connectSlotsByName(self.main_window)

    def retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.main_window.setWindowTitle(_translate("mainWindow", "Mouse In Maze"))

    def button_parameter_click(self):
        pass

    def button_start_learn_click(self):
        pass

    def button_start_run_click(self):
        pass


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = MainWindow()
    ui.setup_ui(window)
    window.show()
    sys.exit(app.exec_())