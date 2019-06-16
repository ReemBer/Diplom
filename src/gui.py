import sys

from PyQt5.QtGui import QIcon, QPixmap, QMovie
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QMessageBox, QDesktopWidget, QLabel, QSizePolicy, \
    QGraphicsItem
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QByteArray, Qt

from src.gui_controller import GuiController


class MainWindow(QMainWindow):
    inference_computed_signal = pyqtSignal()
    @property
    def IMAGES_PATH(self):
        return './images'

    def __init__(self):
        super().__init__()
        self.pianoroll_img = None
        self.play_btn = None
        self.pause_btn = None
        self.stop_btn = None
        self.init_ui()
        self.center()
        self.show()

    def init_ui(self):
        self.init_central_widget()
        self.init_status_bar()
        self.init_actions()
        self.setGeometry(600, 600, 600, 300)
        self.setWindowTitle('Neural composer')

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def init_central_widget(self):
        self.pianoroll_img = QPixmap('./exp/default/results/inference/images/fake_x_hard_thresholding_colored/fake_x_hard_thresholding_colored_0.png')
        self.pianoroll_lbl = QLabel(self)
        self.pianoroll_lbl.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.pianoroll_lbl.setAlignment(Qt.AlignCenter)
        self.pianoroll_lbl.setPixmap(self.pianoroll_img)
        self.setCentralWidget(self.pianoroll_lbl)

    def init_status_bar(self):
        self.statusBar().showMessage('Ready')

    def init_actions(self):
        menu_folders = {}
        tool_bar_actions = {}
        self.init_file_actions(menu_folders, tool_bar_actions)
        self.init_gan_actions(menu_folders, tool_bar_actions)
        self.init_playback_actions(menu_folders, tool_bar_actions)
        self.init_menu_bar(menu_folders)
        self.init_tool_bar(tool_bar_actions)

    def init_file_actions(self, menu_folders, tool_bar_actions):
        menu_folders['&File'] = []
        tool_bar_actions['File'] = []
        self.init_exit_action(menu_folders, tool_bar_actions)

    def init_exit_action(self, menu_folders, tool_bar_actions):
        exitAction = QAction(QIcon(self.IMAGES_PATH + '/exit.jpg'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)
        menu_folders['&File'].append(exitAction)
        tool_bar_actions['File'].append(exitAction)

    def init_gan_actions(self, menu_folders, tool_bar_actions):
        menu_folders['&GAN'] = []
        tool_bar_actions['GAN'] = []
        self.init_loading_animation()
        self.init_run_inference_button(menu_folders, tool_bar_actions)

    def init_loading_animation(self):
        self.loading_gif = QMovie(self.IMAGES_PATH + '/loading.gif', QByteArray(), self)

    def init_run_inference_button(self, menu_folders, tool_bar_actions):
        run_inference = QAction(QIcon(self.IMAGES_PATH + '/run_inference.png'), 'Run &Inference', self)
        run_inference.setShortcut('Ctrl+I')
        run_inference.setStatusTip('Run inference')
        self.inference_computed_signal.connect(self.inference_computed_callback)
        run_inference.triggered.connect(self.run_inference_pressed)
        menu_folders['&GAN'].append(run_inference)
        tool_bar_actions['GAN'].append(run_inference)

    @pyqtSlot()
    def run_inference_pressed(self):
        self.pianoroll_lbl.clear()
        self.pianoroll_lbl.setMovie(self.loading_gif)
        self.loading_gif.start()
        self.stop_button_slot()
        self.play_btn.setEnabled(False)
        GuiController.run_inference(self.inference_computed_signal)

    @pyqtSlot()
    def inference_computed_callback(self):
        self.init_central_widget()
        self.play_btn.setEnabled(True)

    def init_playback_actions(self, menu_folders, tool_bar_actions):
        menu_folders['&Player'] = []
        tool_bar_actions['Player'] = []
        self.init_play_button(menu_folders, tool_bar_actions)
        self.init_pause_button(menu_folders, tool_bar_actions)
        self.init_stop_button(menu_folders, tool_bar_actions)
        pass

    def play_button_slot(self):
        if self.stop_btn.isEnabled():
            GuiController.resume()
        else:
            GuiController.play()
        self.pause_btn.setEnabled(True)
        self.stop_btn.setEnabled(True)
        self.play_btn.setEnabled(False)

    def init_play_button(self, menu_folders, tool_bar_actions):
        play = QAction(QIcon(self.IMAGES_PATH + '/play.png'), 'Play', self)
        play.setShortcut('Ctrl+S')
        play.setStatusTip('Play')
        play.triggered.connect(lambda: self.play_button_slot())
        self.play_btn = play
        menu_folders['&Player'].append(play)
        tool_bar_actions['Player'].append(play)

    def pause_button_slot(self):
        self.play_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)
        GuiController.pause()

    def init_pause_button(self, menu_folders, tool_bar_actions):
        pause = QAction(QIcon(self.IMAGES_PATH + '/pause.png'), 'Pause', self)
        pause.setShortcut('Ctrl+P')
        pause.setStatusTip('Pause')
        pause.triggered.connect(lambda: self.pause_button_slot())
        pause.setEnabled(False)
        self.pause_btn = pause
        menu_folders['&Player'].append(pause)
        tool_bar_actions['Player'].append(pause)

    def stop_button_slot(self):
        GuiController.stop()
        self.stop_btn.setEnabled(False)
        self.pause_btn.setEnabled(False)
        self.play_btn.setEnabled(True)

    def init_stop_button(self, menu_folders, tool_bar_actions):
        stop = QAction(QIcon(self.IMAGES_PATH + '/stop.svg'), 'Stop', self)
        stop.setShortcut('Ctrl+T')
        stop.setStatusTip('Stop')
        stop.triggered.connect(lambda: self.stop_button_slot())
        stop.setEnabled(False)
        self.stop_btn = stop
        menu_folders['&Player'].append(stop)
        tool_bar_actions['Player'].append(stop)

    def init_menu_bar(self, menu_folders):
        menubar = self.menuBar()
        for k in menu_folders:
            file_menu = menubar.addMenu(k)
            file_menu.addActions(menu_folders.get(k, []))

    def init_tool_bar(self, tool_bar_actions):
        toolbar = self.addToolBar('Toolbar')
        for k in tool_bar_actions:
            toolbar.addActions(tool_bar_actions.get(k, []))
            self.addToolBarBreak()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', 'Are you sure to quit?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

def main():
    app = QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec_())
    pass


if __name__ == '__main__':
    main()
