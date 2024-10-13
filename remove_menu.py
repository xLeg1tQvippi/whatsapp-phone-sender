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
import writer_withPyQt
import remove_number_activeList
import remove_number_db

""" 
this file is up to deleting function of numbers.
"""


class Menu(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.init_ui()
        self.objects()
        self.connections()

    def init_ui(self):
        self.resize(300, 100)
        self.setWindowTitle("Меню удаления номеров")

    def objects(self):
        self.Vlayout = QVBoxLayout()
        self.Hlayout = QHBoxLayout()

        self.menu_text = QLabel("<center>Меню удаления номеров</center>")
        self.db_button = QPushButton("Старые номера")
        self.active_button = QPushButton("Активные номера")
        self.back_to_writer = QPushButton("Вернуться")
        self.Vlayout.addWidget(self.menu_text)
        self.Hlayout.addWidget(self.db_button)
        self.Hlayout.addWidget(self.active_button)

        self.Vlayout.addLayout(self.Hlayout)

        self.Vlayout.addWidget(self.back_to_writer)

        self.setLayout(self.Vlayout)

    def connections(self):
        self.db_button.clicked.connect(self.database_numbers)
        self.active_button.clicked.connect(self.active_numbers)
        self.back_to_writer.clicked.connect(self.back_write)

    def database_numbers(self):
        self.database_numbers = remove_number_db.Delete()
        self.database_numbers.show()
        self.close()

    def active_numbers(self):
        self.active_numbers = remove_number_activeList.delete_number()
        self.active_numbers.show()
        self.close()

    def back_write(self):
        self.backWrite = writer_withPyQt.MainWindowWriter()
        self.backWrite.show()
        self.close()


if "__main__" == __name__:
    app = QApplication(sys.argv)
    win = Menu()
    win.show()
    sys.exit(app.exec())
