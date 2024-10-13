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
import remove_menu


class Delete(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.init_ui()
        self.objects()
        self.connections()
        self.layouts_connect()

    def init_ui(self):
        self.resize(300, 100)
        self.setWindowTitle("Функция удаления номеров")

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
        self.line.textChanged.connect(self.turn_button)
        self.line.returnPressed.connect(self.preparing)
        self.buttonleave.clicked.connect(self.back_to_write)

    def search_base(self, text):
        try:
            con = sqlite3.connect("old_number.db")
            cursor = con.cursor()
            check_request = """ 
            SELECT EXISTS(SELECT 1 FROM numbers WHERE old = ?)
            """
            cursor.execute(check_request, (text,))
            exists = cursor.fetchone()[0]
            if exists:
                con.close()
                return [False, text]
            else:
                con.close()
                return [True, text]
        except:
            return [False, text]

    def remove_number(self, text):
        try:
            con = sqlite3.connect("old_number.db")
            cursor = con.cursor()
            cursor.execute("""DELETE FROM numbers WHERE old = ?""", (text,))
            con.commit()
            con.close()
        except:
            print("Unsuccesful func. removing")
            return False
        else:
            return True

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

    def turn_button(self):
        self.ltext = self.line.text()
        if self.ltext:
            self.buttonleave.setDisabled(True)
        elif not self.ltext:
            self.buttonleave.setEnabled(True)

    def preparing(self):
        numb = self.line.text()
        number = numb.translate(
            str.maketrans({" ": "", "_": "", "-": "", ",": "", "/": "", "\\": ""})
        )
        print("number:", number)
        status = self.search_base(number)
        if status[0] == False:  # Номер существует
            delstatus = self.remove_number(status[1])
            if delstatus == True:
                time = 2500
                text = self.statusline + "Номер успешно удален!"
                self.status.setText(text)
                QTimer.singleShot(time, lambda: self.status.setText(self.statusline))
                self.line.setText("")
            else:
                print("Unsuccess!")
        elif status[0] == True:  # Номер не существует
            time = 2500
            text = self.statusline + "Номер не найден!"
            self.status.setText(text)
            QTimer.singleShot(time, lambda: self.status.setText(self.statusline))

    def back_to_write(self):
        self.back_to_write = remove_menu.Menu()
        self.back_to_write.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Delete()
    win.show()
    sys.exit(app.exec())
