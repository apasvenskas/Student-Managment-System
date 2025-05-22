from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, QGridLayout, QLineEdit, \
    QPushButton, QMainWindow, QTableWidget, QTableWidgetItem, QDialog, QComboBox, QToolBar, QStatusBar, \
    QMessageBox
import sys
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt
import sqlite3
import mysql.connector


class DataBaseConection():
    def __init__(self, host="localhost", user="root", password="pythoncourse", database="school"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def connect(self):
        connection = mysql.connector.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        return connection


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Managment System")
        self.setMinimumSize(800, 600)

        file_menu_item = self.menuBar().addMenu("&file")
        help_menu_item = self.menuBar().addMenu("&help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        add_student_action = QAction(QIcon("icons/add.png"), "Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)
        about_action.triggered.connect(self.about)

        search_action = QAction(QIcon("icons/search.png"), "Search", self)
        edit_menu_item.addAction(search_action)
        search_action.triggered.connect(self.search)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)

        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)

        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        hello = QLabel("Hello There!")
        self.statusBar.addWidget(hello)

        self.table.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self):
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)

        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)

        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusBar.removeWidget(child)

        self.statusBar.addWidget(edit_button)
        self.statusBar.addWidget(delete_button)

    def load_data(self):
        try:
            connection = DataBaseConection().connect()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM students")
            result = cursor.fetchall()
            self.table.setRowCount(0)
            for row_number, row_data in enumerate(result):
                self.table.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
            connection.close()
        except Exception as e:
            QMessageBox.critical(self, "Database Error", str(e))

    def insert(self):
        dialog = InsertDialogue(self)
        dialog.exec()

    def search(self):
        dialog = SearchDialogue(self)
        dialog.exec()

    def edit(self):
        dialog = EditDialog(self)
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog(self)
        dialog.exec()

    def about(self):
        dialog = AboutDialog(self)
        dialog.exec()


class AboutDialog(QMessageBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About")
        content = """
        Student managment app created for learning experience. Primraly for practicing Python and class structures. 
        """
        self.setText(content)


class EditDialog(QDialog):
    def __init__(self, context):
        super().__init__(context)
        self.setWindowTitle("Edit Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        index = context.table.currentRow()
        if context.table.item(index, 1) is None:
            return

        student_name = context.table.item(index, 1).text()
        self.student_id = context.table.item(index, 0).text()

        self.student_name = QLineEdit(student_name)
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        course = context.table.item(index, 2).text()
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(course)
        layout.addWidget(self.course_name)

        mobile_item = context.table.item(index, 3)
        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Mobile Tel")
        if mobile_item:
            self.mobile.setText(mobile_item.text())
        layout.addWidget(self.mobile)

        button = QPushButton("Submit")
        button.clicked.connect(lambda: self.update(context))
        layout.addWidget(button)

        self.setLayout(layout)

    def update(self, context):
        connection = DataBaseConection().connect()
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name = %s, course = %s, mobile = %s WHERE ID = %s", 
                       (
                        self.student_name.text(), 
                        self.course_name.currentText(), 
                        self.mobile.text(), 
                        self.student_id
                        ))
        connection.commit()
        cursor.close()
        connection.close()
        context.load_data()


class DeleteDialog(QDialog):
    def __init__(self, context):
        super().__init__(context)
        self.setWindowTitle("Delete Student Data")

        layout = QGridLayout()
        confirmation = QLabel("Are you sure you want to delete?")
        yes = QPushButton("Yes")
        no = QPushButton("No")

        layout.addWidget(confirmation, 0, 0, 1, 2)
        layout.addWidget(yes, 1, 0)
        layout.addWidget(no, 1, 1)
        self.setLayout(layout)

        yes.clicked.connect(lambda: self.delete_student(context))
        no.clicked.connect(self.close)

    def delete_student(self, context):
        index = context.table.currentRow()
        if context.table.item(index, 0) is None:
            return

        student_id = context.table.item(index, 0).text()

        connection = DataBaseConection().connect()
        cursor = connection.cursor()
        cursor.execute("DELETE from students WHERE id = %s", (student_id, ))
        connection.commit()
        cursor.close()
        connection.close()
        context.load_data()

        self.close()

        confirmation_widget = QMessageBox(self)
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setText("The data was deleted.")
        confirmation_widget.exec()


class SearchDialogue(QDialog):
    def __init__(self, context):
        super().__init__(context)

        self.setWindowTitle("Search Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        button = QPushButton("Search")
        button.clicked.connect(lambda: self.search(context))
        layout.addWidget(button)

        self.setLayout(layout)

    def search(self, context):
        name = self.student_name.text()
        connection = DataBaseConection().connect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM students WHERE name = %s", (name,))
        rows = cursor.fetchall()
        cursor.close()
        connection.close()

        items = context.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            if item:
                context.table.item(item.row(), 1).setSelected(True)


class InsertDialogue(QDialog):
    def __init__(self, context):
        super().__init__(context)
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Mobile Tel")
        layout.addWidget(self.mobile)

        button = QPushButton("Submit")
        button.clicked.connect(lambda: self.add_student(context))
        layout.addWidget(button)

        self.setLayout(layout)

    def add_student(self, context):
        name = self.student_name.text()
        course = self.course_name.currentText()
        mobile = self.mobile.text()
        connection = DataBaseConection().connect()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (%s, %s, %s)",
                              (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()
        context.load_data()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    windowOne = MainWindow()
    windowOne.show()
    windowOne.load_data()
    sys.exit(app.exec())