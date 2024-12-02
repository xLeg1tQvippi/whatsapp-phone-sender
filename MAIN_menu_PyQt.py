from PyQt6.QtWidgets import (
    QWidget,
    QApplication,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
)
import sys
import writer_withPyQt
import sender_withPyQt6
import ph_numbers


class Menu(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setWindowTitle("Меню")
        self.resize(300, 100)
        self.hbox = QHBoxLayout()
        self.vbox = QVBoxLayout()

        self.label = QLabel("")
        self.button_send = QPushButton("Рассылка на номера")
        self.button_add = QPushButton("Добавление номеров")

        self.button_add.clicked.connect(self.add_num)
        self.button_send.clicked.connect(self.send_num)

        self.hbox.addWidget(self.button_send)
        self.hbox.addWidget(self.button_add)
        self.vbox.addLayout(self.hbox)
        self.vbox.addWidget(self.label)

        self.setLayout(self.vbox)
        self.check_pass()

    def add_num(self):
        self.send_win = writer_withPyQt.MainWindowWriter()
        self.send_win.show()
        self.close()

    def check_pass(self):
        with open("ph_numbers.py", "r") as file:
            active_nums = file.read()
        if active_nums == "phone_numbers = []":
            self.button_send.setDisabled(True)
            self.label.setText(
                "<center>Список с номерами пуст.<br>Добавьте номера для расссылки.</center>"
            )
        elif active_nums != "phone_numbers = []":
            self.button_send.setEnabled(True)

    def num_counter(self):
        numbers = ph_numbers.phone_numbers
        count = 0
        for i in numbers:
            count += 1
        return count

    def send_num(self):
        num_amount = self.num_counter()
        self.hide()
        sender = self.send_num = sender_withPyQt6.Sender_Message(num_amount)
        self.show()


if __name__ == "__main__":
    print("Initializing Menu ...")
    app = QApplication([])

    win = Menu()
    win.show()

    sys.exit(app.exec())
