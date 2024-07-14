from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QGridLayout, \
    QLineEdit, QPushButton, QMainWindow, QTableWidget, QTableWidgetItem, QDialog, QComboBox, \
    QToolBar, QStatusBar
import sys #system
import sqlite3
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon
from datetime import datetime


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
        connection = sqlite3.connect("database.db")
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

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)", (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()
        main.load_data()


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


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()

app = QApplication(sys.argv)
main = MainMethod()
main.show()
main.load_data()
sys.exit(app.exec())