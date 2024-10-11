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
import sys, time, old_numbers, ph_numbers, RegEx_Keeper, re
import menu_PyQt, sqlite3
import DeletingNums


class PlusError(Exception):
    code = "PlusError"
    text = 'Вы не поставили "+" в начале номера.'


class IncorrectNumber(Exception):
    code = "IncorrectNum"
    text = "Номер введен неверно."


class InOldListNumber(Exception):
    code = "OldListError"
    text = "На данный номер уже было отправлено сообщение."


class SpecialSignCleanerError(Exception):
    code = "SignError"
    text = "Произошла ошибка при отчистке номера."


class CheckFirstLetterError(Exception):
    code = "FirstLetterError"
    text = "Correcting FirstLetterError..."


class IncorrectNumberType(Exception):
    code = "Wrong Number"
    text = "Номер введён неверно, повторите попытку."


class InActiveListNumber(Exception):
    code = "InActiveError"
    text = "Вы уже вводили данный номер телефона."


class SavingNumError(Exception):
    code = "SaveError"
    text = "Произошла ошибка при сохранении номера."


class MainWindowSender(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.resize(300, 120)
        self.setWindowTitle("Sender")
        self.errorNum = ""
        self.labeltext = r"id: -\- <br> country: -\- <br> language: -\-"
        self.label = QLabel(self.labeltext)
        self.label_input = QLabel("<center>Система записи номеров</center>")
        self.button = QPushButton("Добавить номер")
        self.vbox = QVBoxLayout()
        self.hbox = QHBoxLayout()
        self.inputnum = QLineEdit("")
        self.backbutton = QPushButton("Меню")
        self.buttoncheck = QPushButton("Удаление номеров")

        self.button.clicked.connect(self.get_number)
        self.inputnum.returnPressed.connect(self.get_number)
        self.backbutton.clicked.connect(self.back_to_menu)
        self.inputnum.setPlaceholderText("Введите номер телефона")
        self.inputnum.textChanged.connect(self.backbutton_status)
        self.buttoncheck.clicked.connect(self.show_delete)

        self.hbox.addWidget(self.backbutton)
        self.hbox.addWidget(self.buttoncheck)

        self.vbox.addWidget(self.label_input)
        self.vbox.addWidget(self.inputnum)
        self.vbox.addWidget(self.label)
        self.vbox.addLayout(self.hbox)

        self.setLayout(self.vbox)

    def show_delete(self):
        deleting = self.show_delete = DeletingNums.Delete()
        deleting.show()
        self.close()

    def add_number_to_active(self, text):
        try:
            active = ph_numbers.phone_numbers
            active.append(text)
            with open("ph_numbers.py", "w") as file:
                file.write(f"phone_numbers = {active}")
        except:
            return False
        else:
            return True

    def oldListDef(self):
        self.inputnum.setText("")
        self.label.setText(self.labeltext)

    def backbutton_status(self):
        # Если текст введен кнопка возврата меню выключается. Если строка пуста то включается.
        status = self.inputnum.text()
        if status:
            self.backbutton.setDisabled(True)
        if not status:
            self.backbutton.setEnabled(True)

    def labelSetter(self, error):
        timer = 7000  # Таймер на время появления ошибки
        if error.code == "InActiveError":
            timer = 3200
        if error.code == "PlusError":
            timer = 1700
        if error.code == "FirstLetterError":
            timer = 1000
        if error.code == "OldListError":
            timer = 2700
        if hasattr(error, "text"):
            print("hasatr:", error.code)
            self.label.setText(error.text)
            if error.code == "OldListError":
                QTimer.singleShot(timer, self.oldListDef)
            else:
                QTimer.singleShot(timer, lambda: self.label.setText(self.labeltext))

    def get_number(self):
        number = self.inputnum.text()
        # text output
        print("text output:", number)

        # Поэтапная проверка номера
        check_status = self.check_num(number)
        if check_status == True:
            self.inputnum.setText("")
            QTimer.singleShot(3100, lambda: self.label.setText(self.labeltext))

    def pack_number(self, text, language):
        try:
            pack = []
            pack.append(text)
            pack.append(language)
        except:
            print("pack number error")  # raise error
        else:
            print("PACK:", True)
            return pack

    def show_country_info(self, id, country, lang):
        self.label.setText(f"id: {id}<br> country: {country}<br>language: {lang}")

    def check_first_letter(self, text):
        try:
            text = list(text)
            if text[0] == "8":
                # Если первое число 8 то заменяет его на +7
                text[0] = "+7"
            elif "special" in "".join(text):
                new = "".join(text)
                special = new.replace("special", "s")
                text = list(special)
            elif text[:2] == ["0", "0"]:
                # Если первые два числа в номере равны двум нулям - Заменяет их на +
                text.pop(0)
                text[0] = "+"

            elif "+" not in text[0]:
                # Если в начале нету плюса, программа ставит плюс и меняет номер.
                text.insert(0, "+")
                self.inputnum.setText("".join(text))
                # raise PlusError
            print(text[:3])

        except:
            try:
                print(text)
                if (
                    text == []
                    or text[0] == "0"
                    or text[:2] == ["0", "+"]
                    or text[:2] == ["+", "8"]
                    or text[:2] == ["+", "+"]
                ):
                    raise IncorrectNumber
            except (PlusError, IncorrectNumber) as error:
                return [False, text, error]

        else:
            text = "".join(text)
            return [True, text]

    def special_sign_cleaner(self, text):
        try:
            text = text.translate(
                str.maketrans(
                    {
                        " ": "",
                        "(": "",
                        ")": "",
                        "-": "",
                        "\\": "",
                        "/": "",
                        "[": "",
                        "]": "",
                    }
                )
            )
        except Exception as error:
            print(error)
            return [False, text]
        else:
            return [True, text]

    def check_with_old_number(self, text):
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

    def check_with_active_number(self, text):
        try:
            active = set(number[0] for number in ph_numbers.phone_numbers)
            if text in active:
                return [False, text]
            if text not in active:
                return [True, text]
        except:
            raise InActiveListNumber

    def country_checker(self, text):
        # Проверка номера если он подходит под список стран.
        # Если номер не подходит, raise invalid number
        config = RegEx_Keeper.country_configuration
        Regex_id = RegEx_Keeper.num_checker
        number = Regex_id.search(text)
        if number:
            for country in RegEx_Keeper.country_list:
                try:
                    if number.group(country) != None:
                        if text == number.group(0):
                            id = number.group(country)
                            language = config[country]
                            self.show_country_info(id, country, language)
                            packing = self.pack_number(text, language)
                            return [True, packing]
                        else:
                            raise InActiveListNumber
                except Exception as error:
                    print("Error:", error)
                    return [False, text]
        else:
            print("Номер не найден")
            return [False, text]  # raise error

    def check_num(self, number):

        try:
            # Функция проверки номеров по стадиям.
            num = self.check_first_letter(
                number
            )  # Возвращает 0 индексом - True/False; 1 индекс - номер телефона стадия 1.
            if num[0] == True:
                print("FLS:", num[0])
                # Теперь передаем номер телефона в фильтр для того чтобы убрать спец. знаки. 1 - номер. Стадия 2
                num = self.special_sign_cleaner(num[1])
                if num[0] == True:
                    print(f"SSL: {num[0]}")
                    # Проверка совпадения с старыми номерами. #Стадия 3
                    num = self.check_with_old_number(num[1])
                    if num[0] == True:
                        print(f"CWON: {num[0]}")
                        # Проверка номера в активном списке номеров.
                        num = self.check_with_active_number(num[1])
                        if num[0] == True:
                            print(f"CWAN: {num[0]}\noutput: {num[1]}")
                            # Проверка номера по шаблонам стран, если номер не подходит под шаблон, номер не сохраняется.
                            # Создать отдельный файл с базой шаблонов стран. и сравнивать regex.search(number)
                            num = self.country_checker(num[1])
                            if num[0] == True:
                                print(f"CH: {num[0]}")
                                num = self.add_number_to_active(num[1])
                                if num == True:
                                    print(f"ANTC: {num}")
                                    return True
                                if num == False:
                                    print(f"ANTC: {num}")
                                    raise SavingNumError
                            if num[0] == False:
                                print("CH:", num[0])
                                raise IncorrectNumberType
                        if num[0] == False:
                            print(f"CWAN: {num[0]}")
                            raise InActiveListNumber
                    if num[0] == False:
                        print(f"CWON: {num[0]}")
                        raise InOldListNumber
                if num[0] == False:
                    print(f"SSL: {num[0]}")
                    raise SpecialSignCleanerError
                # Если возвращается True, сделать проверку номера телефона по странам. Если номер совпадает занести в список,
                # В ином случае вывести ошибку, что номер введен неверно/не подходит под имеющийся список стран.
                # Если номер не подходит под индекс кода страны, запросить добавление в список новых стран.
                # Если не совпадает с регулярным выражением, вывести ошибку не совпадения номера с шаблонами.
            elif num[0] == False:
                print(f"FLS: {num[0]}")
                raise num[2]
        except (
            CheckFirstLetterError,
            SpecialSignCleanerError,
            InOldListNumber,
            PlusError,
            IncorrectNumber,
            IncorrectNumberType,
            InActiveListNumber,
        ) as error:
            self.labelSetter(error)
            return False

    def back_to_menu(self):
        menu = self.back_to_menu = menu_PyQt.Menu()
        menu.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindowSender()
    win.show()
    sys.exit(app.exec())
