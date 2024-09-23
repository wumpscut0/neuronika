import sys
import webbrowser
from collections.abc import Callable
from pathlib import Path
from os.path import dirname, join

from PyQt6.QtCore import Qt, QVariantAnimation, QSize
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QHBoxLayout,
    QSizePolicy,
    QLineEdit,
    QStackedLayout,
    QTextEdit,
    QGridLayout,
    QGraphicsPixmapItem,
    QGraphicsView,
    QGraphicsScene, QSpacerItem,
)
from PyQt6.QtGui import QPalette, QImage, QBrush, QPixmap, QIcon, QCursor

import settings
from tools import PasswordManager

STACK = QStackedLayout()
BASEDIR = dirname(__file__)

try:
    from ctypes import windll
    myappid = 'mycompany.myproduct.subproduct.version'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass


class Input(QVBoxLayout):
    def __init__(self, label: str, secret=False):
        super().__init__()
        self.setSpacing(0)
        label = QLabel(label)
        self._input = QLineEdit()
        self._input.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._input.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        if secret:
            self._input.setEchoMode(QLineEdit.EchoMode.Password)
        self.addWidget(label)
        self.addWidget(self._input)

    @property
    def value(self):
        return self._input.text()


class LoginWindow(QWidget):
    error_mgs = "Неверный логин или пароль"
    login_text = "Логин:"
    password_text = "Пароль:"
    button_text = "Войти"

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addStretch(1)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.error_span = QLabel(self.error_mgs)
        self.error_span.hide()
        self.login_input = Input(self.login_text)
        self.password_input = Input(self.password_text, True)
        self.enter = QPushButton(self.button_text)
        self.enter.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.enter.clicked.connect(self._login_process)

        self.layout.addWidget(self.error_span)
        self.layout.addLayout(self.login_input)
        self.layout.addLayout(self.password_input)
        self.layout.addWidget(self.enter)
        self.layout.addStretch(1)

    def _login_process(self):
        if PasswordManager.verify(self.password_input.value, settings.PASSWORD):
            STACK.setCurrentIndex(1)
        else:
            self.error_span.show()


class TopPanelArea(QWidget):
    def __init__(self, height, color):
        super().__init__()
        self.wrapper = QWidget()
        self.wrapper.setLayout(QHBoxLayout())
        self.wrapper.setStyleSheet(f"background-color: {color}; color: white;")

        self.setFixedHeight(height)
        self.wrapper.layout().addWidget(self)
        self.wrapper.layout().setContentsMargins(0, 0, 0, 0)


class UserNameWidget(QWidget):
    user_header = "ПОЛЬЗОВАТЕЛЬ:"
    user_name_color = "#8c7c44"

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.user_name_header = QLabel(self.user_header)
        self.user_name_header.setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.layout.addWidget(self.user_name_header)
        self.user_name = QLabel(settings.LOGIN)
        self.user_name.setStyleSheet(f"color: {self.user_name_color}")
        self.user_name.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.addWidget(self.user_name)


class TopPanelButtons(QWidget):
    buttons_data = (
        ("list.png", "упражнения", None),
        (
            "question.png",
            "помощь",
            lambda: webbrowser.open(
                "https://developer.mozilla.org/en-US/docs/Learn/HTML/Introduction_to_HTML/Creating_hyperlinks"
            ),
        ),
        ("info.png", "о программе", lambda: webbrowser.open(
                "https://www.pythonguis.com/pyqt6-tutorial/"
            )),
        ("exit.png", "выход", lambda: STACK.setCurrentIndex(0)),
    )

    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        for button_data in self.buttons_data:
            filename, text, func = button_data
            button = QWidget()
            icon = TopPanelButton(filename, func)
            text_widget = QLabel(text)
            text_widget.setAlignment(Qt.AlignmentFlag.AlignTop)
            button_layout = QVBoxLayout()
            button.setLayout(button_layout)

            button_layout.addWidget(icon)
            button_layout.addWidget(text_widget)
            self.layout.addWidget(button)


class TopPanelButton(QLabel):
    size = 25
    base_dir = Path(BASEDIR, "icons", "main_top_panel", "buttons")

    def __init__(self, file_name: str, func: Callable | None = None):
        super().__init__()
        self.func = func

        self.setPixmap(
            QPixmap(str(self.base_dir / file_name)).scaled(self.size, self.size)
        )
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

    def mousePressEvent(self, ev):
        if self.func is not None:
            self.func()


class TopPanel(QWidget):
    height = 1
    base_dir = Path(BASEDIR, "icons", "main_top_panel")
    logo_file_path = str(base_dir / "logo.png")
    user_file_path = str(base_dir / "user.png")
    header = "КОГНИТИВНАЯ РЕАБИЛИТАЦИЯ"
    left_panel_color = "#446c7c"
    right_panel_color = "#365b66"

    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.left_panel = TopPanelArea(self.height, self.left_panel_color).wrapper
        self.left_panel.layout().setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.logo = QLabel()
        self.logo.setPixmap(QPixmap(self.logo_file_path).scaled(50, 50))
        self.header = QLabel(self.header)
        self.header.setStyleSheet("font-size: 23px;")
        self.left_panel.layout().addWidget(self.logo)
        self.left_panel.layout().addWidget(self.header)

        self.right_panel = TopPanelArea(self.height, self.right_panel_color).wrapper
        self.right_panel.layout().setAlignment(Qt.AlignmentFlag.AlignRight)

        self.user_area = QWidget()
        self.user_area.setLayout(QHBoxLayout())
        self.user_area.layout().setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.user_img = QLabel()
        self.user_img.setPixmap(QPixmap(self.user_file_path).scaled(20, 20))
        self.user_name = UserNameWidget()
        self.user_area.layout().addWidget(self.user_img)
        self.user_area.layout().addWidget(self.user_name)

        self.right_panel.layout().addWidget(self.user_area)

        self.button_area = QWidget()
        self.button_area.setLayout(QHBoxLayout())
        self.button_area.layout().setAlignment(Qt.AlignmentFlag.AlignRight)
        self.button_area.layout().addWidget(TopPanelButtons())
        self.button_area.layout().setContentsMargins(0, 0, 0, 0)
        self.right_panel.layout().addStretch()
        self.right_panel.layout().addWidget(self.button_area)

        self.layout.addWidget(self.left_panel, stretch=1)
        self.layout.addWidget(self.right_panel, stretch=2)


class MainIcon(QGraphicsView):
    animation_duration = 200
    start_size = 120
    end_size = round(start_size * 1.1)
    base_dir = Path(BASEDIR, "icons", "main_quests")

    def __init__(self, file_name: str):
        super().__init__()
        self.setStyleSheet("border: none")
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        self.filename = str(self.base_dir / file_name)

        self.pixmap_item = QGraphicsPixmapItem()
        self.scene.addItem(self.pixmap_item)
        pixmap = QIcon(self.filename).pixmap(self.start_size, self.start_size)
        self.pixmap_item.setPixmap(pixmap)
        
        self.animation = QVariantAnimation()
        self.animation.setDuration(self.animation_duration)
        self.animation.valueChanged.connect(lambda value: self.update_pixmap(value))
        self.animation.setStartValue(self.start_size)
        self.animation.setEndValue(self.end_size)

        self.pixmap_item.setPos(-self.start_size / 2, -self.start_size / 2)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

    def update_pixmap(self, value):
        pixmap = QIcon(self.filename).pixmap(int(value), int(value))
        pixmap_scaled = pixmap.scaled(int(value), int(value), Qt.AspectRatioMode.KeepAspectRatio,
                                      Qt.TransformationMode.SmoothTransformation)
        self.pixmap_item.setPixmap(pixmap_scaled)
        self.pixmap_item.setPos(-value / 2, -value / 2)

    def enterEvent(self, event):
        self.animation.setStartValue(self.start_size)
        self.animation.setEndValue(self.end_size)
        self.animation.start()

    def leaveEvent(self, event):
        self.animation.setStartValue(self.end_size)
        self.animation.setEndValue(self.start_size)
        self.animation.start()

    def mousePressEvent(self, ev):
        STACK.setCurrentIndex(2)


class MainButton(QWidget):
    color = "#bfaca3"

    def __init__(self, file_name: str, label: str):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.button_header = QLabel(label)
        self.button_header.setAlignment(
            Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter
        )
        self.button_header.setStyleSheet(f"color: {self.color}")

        self.icon = MainIcon(file_name)
        self.icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout.addWidget(self.icon)
        self.layout.addWidget(self.button_header)


class MainBlock(QWidget):
    buttons_data = (
        (
            ("brain.PNG", "Исполнительные\nфункции"),
            ("map.PNG", "Навыки зрительного и\nпространственного\nвосприятия"),
        ),
        (
            ("book.PNG", "Вербальная\nпамять"),
            ("picture.PNG", "Визуальное\nвнимание"),
        ),
        (
            ("church.PNG", "Визуальная\nпамять"),
            ("clock.PNG", "Скорость обработки\nинформации"),
        ),
        (
            ("web.PNG", "Вербальная и\nвизуальная память"),
            ("ear.PNG", "Слуховое\nвосприятие"),
        ),
        (
            ("compass.PNG", "Пространственная\nпамять"),
            ("dialog.PNG", "Языковые навыки\nи словарный запас"),
        ),
    )

    def __init__(self):
        super().__init__()
        self.setLayout(QVBoxLayout())
        self.layout().setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("background-color: white")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        self.buttons_widget = QWidget()
        self.buttons_widget.setLayout(QHBoxLayout())
        self.layout().setAlignment(Qt.AlignmentFlag.AlignTop)
        
        for buttons_column in self.buttons_data:
            column = QWidget()
            column_layout = QVBoxLayout()
            column.setLayout(column_layout)
            for button_data in buttons_column:
                button = MainButton(*button_data)
                column_layout.addWidget(button)
            self.buttons_widget.layout().addWidget(column)
        
        self.info_widget = InfoBlock().wrapper
        
        self.layout().addWidget(self.buttons_widget)
        self.layout().addWidget(self.info_widget)


class InfoBlock(QWidget):
    info_header = "ДОБРО ПОЖАЛОВАТЬ"
    info = (
        "Программа когнитивной реабилитации позволяет снизить, восстановить и максимально возможно улучшить степень когнитивного "
        "дефицита у пациентов с применением различных восстановительных программ и технологий. Программа когнитивной реабилитации "
        "направлена на тренировку когнитивных функций, восстановление функции внимания, памяти, мышления, исполнительных функций и "
        "на помощь пациентам в развитии построения стратегии для решения сложных задач. Методика основана на стандартных и "
        "специализированных упражнениях, которые состоят из интерактивных интересных заданий."
    )
    background_color = "#ececf4"

    def __init__(self):
        super().__init__()
        self.wrapper = QWidget()
        self.wrapper.setLayout(QVBoxLayout())
        self.wrapper.setStyleSheet("background-color: white")
        
        self.setLayout(QVBoxLayout())
        self.setStyleSheet(
            f"padding: 10px; border-radius: 3px; border: 1px solid {TopPanel.left_panel_color}; background-color: {self.background_color}"
        )
        
        self.text = QTextEdit()
        self.text.setFixedSize(1000, 150)
        self.text.setStyleSheet("padding: 10px")
        self.text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.text.setReadOnly(True)
        self.text.setHtml(
            """
                <p>{}</p>
                <p>{}</p>
            """.format(
                self.info_header, self.info
            )
        )
        
        h_layout = QHBoxLayout()
        h_layout.addStretch(1)
        h_layout.addWidget(self.text)
        h_layout.addStretch(1)
        
        self.layout().addLayout(h_layout)
        self.wrapper.layout().addWidget(self)


class Texture(QWidget):
    texture_file_path = str(Path(BASEDIR, "icons", "texture.jpg").resolve())
    header = "ГРУППЫ УПРАЖНЕНИЙ"
    header_color = TopPanel.left_panel_color

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.setAutoFillBackground(True)
        palette = QPalette()
        palette.setBrush(
            QPalette.ColorRole.Window, QBrush(QImage(self.texture_file_path))
        )
        self.setPalette(palette)
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )

        self.header_widget = QLabel(self.header)
        self.header_widget.setStyleSheet(
            f"font-size: 25px; color: {self.header_color}; font-weight 500;"
        )
        self.header_widget.setContentsMargins(0, 30, 0, 0)
        self.layout.addWidget(self.header_widget, alignment=Qt.AlignmentFlag.AlignTop)
        self.layout.addWidget(MainBlock())


class MenuWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

        self.layout.addWidget(TopPanel())
        self.layout.addWidget(Texture(), stretch=1)


class QuestWindow(QWidget):
    header = "Запомните изображения и их расположение"
    button_text = "Продолжить"
    back_text = "Назад"
    quest_size = 3
    icons_data = {
        (0, 0): "bag.PNG",
        (1, 0): "canoe.PNG",
        (1, 1): "atom.PNG",
        (2, 0): "open_book.PNG",
        (2, 2): "timer.PNG",
    }
    button_color = "#499477"
    base_dir = Path(BASEDIR, "icons", "main_quests", "generic")
    arrow_icon_path = str(Path(base_dir, "left-arrow.png").resolve())
    
    def __init__(self):
        super().__init__()
        self.setLayout(QVBoxLayout())
        self.header = QLabel(self.header)
        self.header.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        self.layout().addWidget(self.header)
        self.layout().setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.quest_content = QWidget()
        self.quest_content.setLayout(QGridLayout())
        self.quest_content.layout().setSpacing(0)
        
        for i in range(self.quest_size ** 2):
            x = i % self.quest_size
            y = i // self.quest_size
            file_name = self.icons_data.get((y, x))
            icon = QLabel()
            if file_name:
                icon.setPixmap(QPixmap(str(self.base_dir / file_name)))
            icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
            icon.setStyleSheet(f"border: 1px solid black")
            icon.setFixedSize(QSize(300, 150))
            self.quest_content.layout().addWidget(icon, y, x)
        
        self.back = QWidget()
        self.back.setLayout(QHBoxLayout())
        self.back.layout().setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.arrow_widget = QLabel()
        self.arrow_widget.setFixedSize(20, 20)
        self.arrow_widget.setPixmap(QPixmap(self.arrow_icon_path).scaled(20, 20))

        self.arrow_widget.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.back.layout().addWidget(self.arrow_widget)
        self.back_button = QPushButton(self.back_text)
        self.back_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.back_button.setStyleSheet(f"border: none")
        self.back_button.setFixedSize(50, 20)
        self.back_button.clicked.connect(lambda: STACK.setCurrentIndex(1))
        self.back.layout().addWidget(self.back_button)
        
        self.button_continue = QPushButton(self.button_text)
        self.button_continue.clicked.connect(lambda: STACK.setCurrentIndex(1))
        self.button_continue.setStyleSheet(
            f"background-color: {self.button_color}; color: white"
        )
        self.layout().addWidget(self.quest_content)
        
        self.wrapper = QWidget()
        self.wrapper.setLayout(QHBoxLayout())
        self.wrapper.setStyleSheet("background-color: white")
        self.wrapper.layout().addWidget(self)
        self.wrapper.layout().addWidget(self.button_continue)
        self.wrapper.layout().setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.wrapper_2 = QWidget()
        self.wrapper_2.setLayout(QVBoxLayout())
        self.wrapper_2.layout().setAlignment(Qt.AlignmentFlag.AlignTop)

        self.wrapper_2.layout().addWidget(self.back)
        self.wrapper_2.layout().addWidget(self.wrapper)


class MainWindow(QMainWindow):
    window_name = "Neuronika"

    def __init__(self):
        super().__init__()
        self.setWindowTitle(self.window_name)
        self.index = QWidget()
        self.index.setLayout(STACK)
        self.setCentralWidget(self.index)
        STACK.addWidget(LoginWindow())
        STACK.addWidget(MenuWindow())
        STACK.addWidget(QuestWindow().wrapper_2)
        STACK.setCurrentIndex(0)


def main():
    app = QApplication(sys.argv)

    app.setWindowIcon(QIcon(str(Path(BASEDIR, "app.ico").resolve())))

    window = MainWindow()
    window.show()

    app.exec()


if __name__ == "__main__":
    main()
