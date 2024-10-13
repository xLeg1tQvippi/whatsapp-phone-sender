from PyQt6.QtWidgets import (
    QWidget,
    QPushButton,
    QLineEdit,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QApplication,
)
from PyQt6.QtCore import QTimer
from PyQt6 import QtWidgets
import sys, sqlite3
import ph_numbers
import remove_menu
import importlib

""" 
Суть данного файла создать новое окно при нажатии на кнопку "Удаление номеров", должно появится окно, с выбором:
Удаление из Активного списка
Удаление из базы данных
"""


class delete_number(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.init_ui()
        self.objects()
        self.connections()
        self.layouts_connect()

    def init_ui(self):
        self.resize(300, 100)
        self.setWindowTitle("Удаление из Активного списка")

    def objects(self):
        self.statusline = "Статус: "
        self.line = QLineEdit()
        self.line.setPlaceholderText("Введите номер")
        self.label = QLabel(
            "Удаление номеров\nВведите полный номер, учитывая +\nПробелы разрешены."
        )
        self.status = QLabel(self.statusline)
        self.buttonleave = QPushButton("Вернуться")

    def connections(self):
        # self.line.textChanged.connect(self.turn_button)
        # self.line.returnPressed.connect(self.preparing)
        self.buttonleave.clicked.connect(self.back_to_write)
        self.line.returnPressed.connect(self.preparing)

    def layouts_connect(self):
        self.vbox = QVBoxLayout()
        self.vbox1 = QVBoxLayout()
        self.hbox = QHBoxLayout()

        self.vbox.addWidget(self.label)
        self.vbox.addWidget(self.line)
        self.vbox.addWidget(self.status)
        self.vbox.addWidget(self.buttonleave)

        self.hbox.addLayout(self.vbox)
        self.hbox.addLayout(self.vbox1)

        self.setLayout(self.hbox)

    def back_to_write(self):
        self.back_to_write = remove_menu.Menu()
        self.back_to_write.show()
        self.close()

    def update_phone_numbers(self, numbers):
        with open("ph_numbers.py", "w") as file:
            file.write(f"phone_numbers = {numbers}")
        print("updated!")

    def preparing(self):
        number = self.line.text()
        numbers_list = ph_numbers.phone_numbers
        for active_number in numbers_list:
            if number == active_number[0]:
                time = 2400
                default = active_number
                pos = numbers_list.index(default)
                numbers_list.pop(pos)
                self.update_phone_numbers(numbers_list)
                importlib.reload(ph_numbers)
                self.status.setText(self.statusline + "Успешно удален")
                self.line.setText("")
                QTimer.singleShot(
                    time,
                    lambda: self.status.setText(self.statusline),
                )
                break
        else:
            time = 3200
            self.status.setText(self.statusline + "Номер не найден")
            QTimer.singleShot(
                time,
                lambda: self.status.setText(self.statusline),
            )


if "__main__" == __name__:
    app = QApplication(sys.argv)
    win = delete_number()
    win.show()
    sys.exit(app.exec())
