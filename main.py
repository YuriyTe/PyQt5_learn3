# Второй способ вызова интерфейса tracker.py, как модуль. НЕ как в документации к PyQt5
# from tracker import *
# import sys
#
# app = QtWidgets.QApplication(sys.argv)
# MainWindow = QtWidgets.QMainWindow()
# ui = Ui_MainWindow()
# ui.setupUi(MainWindow)
# MainWindow.show()
# ui.label.setText("alkdfjlakjfos9ifj0")
# sys.exit(app.exec_())

# способ вызова интерфейса как в документации
import pickle
from PyQt5 import uic
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QApplication
import os


print(os.path.realpath(__file__))
dirname, filename = os.path.split(os.path.realpath(__file__))
print(dirname)
Form, Window = uic.loadUiType(dirname+"\\tracker.ui")
app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.show()


def save_to_file():
    global start_date, calc_date, description, dirname
    # start_date = QDate(2021, 12, 1)
    data_to_save = {"start": start_date, "end": calc_date, "descr": description}
    file1 = open(dirname + '\\config.txt', "wb")
    pickle.dump(data_to_save, file1)
    file1.close()
    task = """schtasks /create /tr "python """ + os.path.realpath(
        __file__) + """" /tn "Трекер события" /sc MINUTE /mo 120 /ed 31/12/2020 /F"""
    task = """schtasks /create /tr "python """ + os.path.realpath(
        __file__) + """" /tn "Трекер события" /sc MINUTE /mo 120 /ed """ + calc_date.toString("dd/MM/yyyy") + """ /F"""
    print(task)
    os.system('chcp 65001')
    os.system(task)


def read_from_file():
    global start_date, calc_date, description, now_date, dirname
    try:
        file1 = open(dirname+"\\config.txt", "rb")
        data_to_load = pickle.load(file1)
        file1.close()
        start_date = data_to_load["start"]
        calc_date = data_to_load["end"]
        description = data_to_load["descr"]
        # print(start_date.toString('dd-MM-yyyy'), calc_date.toString('dd-MM-yyyy'), description)
        form.calendarWidget.setSelectedDate(calc_date)
        form.dateEdit.setDate(calc_date)
        form.plainTextEdit.setPlainText(description)
        delta_days_left = start_date.daysTo(now_date)  # прошло дней
        delta_days_right = now_date.daysTo(calc_date)  # осталось дней
        total_days = start_date.daysTo(calc_date)  # всего дней
        print("s###", delta_days_left, delta_days_right, total_days)
        procent = int(delta_days_left * 100 / total_days)
        form.progressBar.setProperty("value", procent)
    except:
        print("Не могу прочитать файл")


def on_click():
    global start_date, calc_date, description, now_date
    start_date = now_date
    description = form.plainTextEdit.toPlainText()
    calc_date = form.calendarWidget.selectedDate()
    # print(form.plainTextEdit.toPlainText())
    # print(form.dateEdit.dateTime().toString('dd-MM-yyyy'))
    print("Clicked!!!")
    save_to_file()
    # print(form.calendarWidget.selectedDate().toString('dd-MM-yyyy'))
    # date = QDate(2022, 1, 55)
    # form.calendarWidget.setSelectedDate(date)


def on_click_calendar():
    global start_date, calc_date
    # print(form.calendarWidget.selectedDate().toString('dd-MM-yyyy'))
    form.dateEdit.setDate(form.calendarWidget.selectedDate())
    calc_date = form.calendarWidget.selectedDate()
    delta_date = start_date.daysTo(calc_date)
    # print(delta_date, " - days left")
    form.label_3.setText("До наступления события осталось: %s дней" % delta_date)


def on_date_edit_change():
    global start_date, calc_date
    form.calendarWidget.setSelectedDate(form.dateEdit.date())
    calc_date = form.dateEdit.date()
    delta_date = start_date.daysTo(calc_date)
    # print(delta_date, " - days")
    form.label_3.setText("До наступления события осталось: %s дней" % delta_date)


form.pushButton.clicked.connect(on_click)
form.calendarWidget.clicked.connect(on_click_calendar)
form.dateEdit.dateChanged.connect(on_date_edit_change)

description = form.plainTextEdit.toPlainText()
start_date = form.calendarWidget.selectedDate()
now_date = form.calendarWidget.selectedDate()
calc_date = form.calendarWidget.selectedDate()
read_from_file()
form.label.setText("Трекер события от %s " % start_date.toString('dd-MM-yyyy'))
on_click_calendar()
app.exec()
