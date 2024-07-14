from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QGridLayout, \
    QLineEdit, QPushButton, QMainWindow, QTableWidget, QTableWidgetItem, QDialog, QComboBox, \
    QToolBar, QStatusBar, QMessageBox
import sys #system
import sqlite3
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon
from datetime import datetime

class DatabaseConnection:
    def __init__(self, db_file = "database.db"):
        self.database_file = db_file

    def connect(self):
        connection = sqlite3.connect(self.database_file)
        return connection
class MainMethod(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management App")
        self.setMinimumSize(800, 600)

        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        search_menu_item = self.menuBar().addMenu("&Edit")


        add_student_action = QAction(QIcon("icons/add.png"),"Add student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.triggered.connect(self.about)


        search_action = QAction(QIcon("icons/search.png"),"Search", self)
        search_action.triggered.connect(self.search_student)
        search_menu_item.addAction(search_action)

        #Create Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        #Create Toolbar
        toolBar = QToolBar()
        toolBar.setMovable(True)
        self.addToolBar(toolBar)

        toolBar.addAction(add_student_action)
        toolBar.addAction(search_action)

        #Create Statusbar

        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        self.table.cellClicked.connect(self.status_widget)

    def status_widget(self):
        edit_button = QPushButton("Edit Button")
        edit_button.clicked.connect(self.edit)

        delete_button = QPushButton("Delete Button")
        delete_button.clicked.connect(self.delete)

        children = self.findChildren(QPushButton)

        for child in children:
            self.statusBar.removeWidget(child)

        self.statusBar.addWidget(edit_button)
        self.statusBar.addWidget(delete_button)
    def load_data(self):
        connection = DatabaseConnection().connect()
        data = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(data):
            self.table.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(column_data)))

        connection.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def search_student(self):
        dialog = SearchDialog()
        dialog.exec()

    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()

    def about(self):
        dialog = AboutDialog()
        dialog.exec()

class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        content = f"""
This app is for student data management created while learning python. 
"""
        self.setText(content)
class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        self.name = QLineEdit()
        self.name.setPlaceholderText("Name")
        layout.addWidget(self.name)

        self.course = QComboBox()
        self.course.addItems(["Bio", "Math", "Astrology"])
        layout.addWidget(self.course)

        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)

        print("Add new student details window opened")

        button = QPushButton("Register")
        button.clicked.connect(self.add_student)
        layout.addWidget(button)

        self.setLayout(layout)


    def add_student(self):
        name = self.name.text()
        mobile = self.mobile.text()
        course = self.course.itemText(self.course.currentIndex())

        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)", (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()
        main.load_data()
        self.accept()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        self.name = QLineEdit()
        self.name.setPlaceholderText("Name")
        layout.addWidget(self.name)

        button = QPushButton("Search")
        button.clicked.connect(self.search_student)
        layout.addWidget(button)

        self.setLayout(layout)


    def search_student(self):
        name = self.name.text()

        # connection = sqlite3.connect("database.db")
        # cursor = connection.cursor()
        # column = cursor.execute("Select name from students where name = ?", (name,))
        # result = list(column)
        items = main.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            print(item)
            main.table.item(item.row(),1).setSelected(True)

        # cursor.close()
        # connection.close()


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        index = main.table.currentRow()
        student_name = main.table.item(index, 1).text()

        self.name = QLineEdit(student_name)
        self.name.setPlaceholderText("Name")
        layout.addWidget(self.name)

        student_course = main.table.item(index, 2).text()
        self.course = QComboBox()
        self.course.addItems(["Bio", "Math", "Astrology"])
        self.course.setCurrentText(student_course)
        layout.addWidget(self.course)

        student_mobile = main.table.item(index, 3).text()
        self.mobile = QLineEdit(student_mobile)
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)

        button = QPushButton("Update")
        button.clicked.connect(self.update)
        layout.addWidget(button)

        self.setLayout(layout)

        self.student_id = main.table.item(index, 0).text()

    def update(self):
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("Update students SET name = ?,  course = ?, mobile = ? Where id = ?",
                       (self.name.text(), self.course.currentText(), self.mobile.text(), self.student_id))
        connection.commit()
        cursor.close()
        connection.close()
        main.load_data()

class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(100)

        layout = QGridLayout()

        confirmation_label = QLabel("Do you want to delete the selected student data?")
        yes_button = QPushButton("Yes")
        no_button = QPushButton("No")
        layout.addWidget(confirmation_label, 0, 0, 1, 2)
        layout.addWidget(yes_button,1,0)
        layout.addWidget(no_button, 1, 1)

        yes_button.clicked.connect(self.delete)
        no_button.clicked.connect(self.close)

        self.setLayout(layout)

    def delete(self):
        index = main.table.currentRow()
        student_id = main.table.item(index, 0).text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("DELETE from students where id = ?",(student_id,))
        connection.commit()
        cursor.close()
        connection.close()
        main.load_data()
        self.close()

        message = QMessageBox()
        message.setWindowTitle("Success")
        message.setText("Record successfully deleted!")
        message.exec()

app = QApplication(sys.argv)
main = MainMethod()
main.show()
main.load_data()
sys.exit(app.exec())