import sys
import webbrowser
from collections.abc import Callable

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
    QMessageBox,
    QGridLayout,
)
from PyQt6.QtGui import QPalette, QImage, QBrush, QPixmap, QIcon, QCursor

import settings
from tools import PasswordManager

STACK = QStackedLayout()


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
        self.background = QWidget()
        self.background.setLayout(QHBoxLayout())
        self.background.setStyleSheet(f"background-color: {color}; color: white;")

        self.setFixedHeight(height)
        self.background.layout().addWidget(self)


class UserNameWidget(QWidget):
    user_header = "ПОЛЬЗОВАТЕЛЬ:"

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.user_name_header = QLabel(self.user_header)
        self.layout.addWidget(self.user_name_header)
        self.user_name = QLabel(settings.LOGIN)
        self.layout.addWidget(self.user_name)


class HelpWindow(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setIcon(QMessageBox.Icon.Information)
        self.setInformativeText("In develop")
        self.setWindowTitle("Info")
        self.setStandardButtons(QMessageBox.StandardButton.Ok)
        self.setDefaultButton(QMessageBox.StandardButton.Ok)


class TopPanelButtons(QWidget):
    buttons_data = (
        ("list.PNG", "упражнения", None),
        (
            "question.PNG",
            "помощь",
            lambda: webbrowser.open(
                "https://developer.mozilla.org/en-US/docs/Learn/HTML/Introduction_to_HTML/Creating_hyperlinks"
            ),
        ),
        ("info.PNG", "о программе", lambda: HelpWindow().exec()),
        ("exit.PNG", "выход", lambda: STACK.setCurrentIndex(0)),
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
            button_layout = QVBoxLayout()
            button.setLayout(button_layout)

            button_layout.addWidget(icon)
            button_layout.addWidget(text_widget)
            self.layout.addWidget(button)


class TopPanelButton(QLabel):
    size = 25
    base_dir = "icons/main_top_panel/buttons/"

    def __init__(self, file_name: str, func: Callable | None = None):
        super().__init__()
        self.func = func
        self.filename = f"{self.base_dir}{file_name}"

        self.pixmap = QPixmap(self.filename).scaled(self.size, self.size)

        self.setPixmap(self.pixmap)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

    def mousePressEvent(self, ev):
        if self.func is not None:
            self.func()


class TopPanel(QWidget):
    height = 60
    base_dir = "icons/main_top_panel/"
    logo_file_path = f"{base_dir}/logo.PNG"
    user_file_path = f"{base_dir}/user.PNG"
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

        self.left_panel = TopPanelArea(self.height, self.left_panel_color).background
        self.left_panel.layout().setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.logo = QLabel()
        self.logo.setPixmap(QPixmap(self.logo_file_path))
        self.header = QLabel(self.header)
        self.left_panel.layout().addWidget(self.logo)
        self.left_panel.layout().addWidget(self.header)

        self.right_panel = TopPanelArea(self.height, self.right_panel_color).background
        self.right_panel.layout().setAlignment(Qt.AlignmentFlag.AlignRight)

        self.user_area = QWidget()
        self.user_area.setLayout(QHBoxLayout())
        self.user_area.layout().setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.user_img = QLabel()
        self.user_img.setPixmap(QPixmap(self.user_file_path))
        self.user_name = UserNameWidget()
        self.user_area.layout().addWidget(self.user_img)
        self.user_area.layout().addWidget(self.user_name)

        self.right_panel.layout().addWidget(self.user_area)

        self.button_area = QWidget()
        self.button_area.setLayout(QHBoxLayout())
        self.button_area.layout().setAlignment(Qt.AlignmentFlag.AlignRight)
        self.button_area.layout().addWidget(TopPanelButtons())
        self.right_panel.layout().addStretch()
        self.right_panel.layout().addWidget(self.button_area)

        self.layout.addWidget(self.left_panel, stretch=1)
        self.layout.addWidget(self.right_panel, stretch=2)


class MainIcon(QLabel):
    animation_duration = 200
    start_size = 70
    end_size = 90
    base_dir = "icons/main_quests/"

    def __init__(self, file_name: str):
        super().__init__()
        self.filename = f"{self.base_dir}{file_name}"

        self.animation = QVariantAnimation()
        self.animation.setDuration(self.animation_duration)
        self.animation.valueChanged.connect(lambda value: self.update_pixmap(value))

        self.pixmap = QPixmap(self.filename).scaled(self.start_size, self.start_size)

        self.setPixmap(self.pixmap)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

    def update_pixmap(self, value):
        pixmap = QIcon(self.filename).pixmap(int(value), int(value))
        self.setPixmap(pixmap)

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
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)
        self.setFixedSize(MainIcon.end_size * 2, MainIcon.end_size * 2)

        self.label = QLabel(label)
        self.label.setStyleSheet(f"color: {self.color}")

        self.layout.addWidget(MainIcon(file_name))
        self.layout.addWidget(self.label)


class MainBlock(QWidget):
    buttons_data = (
        (
            ("brain.PNG", "Исполнительные\nфункции"),
            ("book.PNG", "Вербальная\nпамять"),
            ("church.PNG", "Визуальная\nпамять"),
            ("web.PNG", "Вербальная и\nвизуальная память"),
            ("compass.PNG", "Пространственная\nпамять"),
        ),
        (
            ("map.PNG", "Навыки зрительного и\nпространственного\nвосприятия"),
            ("picture.PNG", "Визуальное\nвнимание"),
            ("clock.PNG", "Скорость обработки\nинформации"),
            ("ear.PNG", "Слуховое\nвосприятие"),
            ("dialog.PNG", "Языковые навыки\nи словарный запас"),
        ),
    )

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("background-color: white")

        for buttons_row in self.buttons_data:
            row = QWidget()
            row_layout = QHBoxLayout()
            row.setLayout(row_layout)
            for button_data in buttons_row:
                row_layout.addWidget(MainButton(*button_data))
            self.layout.addWidget(row)
        self.layout.addWidget(InfoBlock().wrapper)


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

        self.setAutoFillBackground(True)
        self.setLayout(QVBoxLayout())
        self.setStyleSheet(
            f"padding: 10px; border-radius: 3px; border: 1px solid {TopPanel.left_panel_color}; background-color: {self.background_color}"
        )

        self.text = QTextEdit()
        self.text.setReadOnly(True)
        self.text.setHtml(
            """
            <p>{}</p>
            <p>{}</p>
        """.format(
                self.info_header, self.info
            )
        )
        self.layout().addWidget(self.text)
        self.wrapper.layout().addWidget(self)


class Texture(QWidget):
    texture_file_path = "icons/texture.jpg"
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
            f"font-size: 25px; color: {self.header_color}; letter-spacing: 1px; font-weight 500;"
        )
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
    quest_size = 3
    icons_data = {
        (0, 0): "bag.PNG",
        (1, 0): "canoe.PNG",
        (1, 1): "atom.PNG",
        (2, 0): "open_book.PNG",
        (2, 2): "timer.PNG",
    }
    button_color = "#499477"
    base_dir = "icons/main_quests/generic/"

    def __init__(self):
        super().__init__()
        self.setLayout(QVBoxLayout())
        self.header = QLabel(self.header)
        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout().addWidget(self.header)
        self.layout().setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.quest_content = QWidget()
        self.quest_content.setLayout(QGridLayout())
        self.quest_content.layout().setSpacing(0)

        for i in range(self.quest_size**2):
            x = i % self.quest_size
            y = i // self.quest_size
            file_name = self.icons_data.get((y, x))
            icon = QLabel()
            if file_name:
                icon.setPixmap(QPixmap(f"{self.base_dir}{file_name}"))
            icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
            icon.setStyleSheet(f"border: 1px solid black")
            icon.setFixedSize(QSize(300, 150))
            self.quest_content.layout().addWidget(icon, y, x)

        self.button_continue = QPushButton(self.button_text)
        self.button_continue.clicked.connect(lambda: STACK.setCurrentIndex(1))
        self.button_continue.setStyleSheet(
            f"background-color: {self.button_color}; color: white"
        )
        self.button_continue.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
        )
        self.layout().addWidget(self.quest_content)

        self.wrapper = QWidget()
        self.wrapper.setLayout(QHBoxLayout())
        self.wrapper.layout().addWidget(self)
        self.wrapper.layout().addWidget(self.button_continue)
        self.wrapper.layout().setAlignment(Qt.AlignmentFlag.AlignCenter)


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
        STACK.addWidget(QuestWindow().wrapper)
        STACK.setCurrentIndex(0)


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()


if __name__ == "__main__":
    main()
