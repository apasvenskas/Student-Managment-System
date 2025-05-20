from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, QGridLayout, QLineEdit, \
    QPushButton, QMainWindow, QTableWidget, QTableWidgetItem, QDialog, QComboBox, QToolBar, QStatusBar, \
    QMessageBox
import sys
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt
import sqlite3


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

        search_action = QAction(QIcon("icons/search.png"), "Search", self)
        edit_menu_item.addAction(search_action)
        search_action.triggered.connect(self.search)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        # Create toolbar
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)

        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)

        # status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        hello = QLabel("Hello There!")
        self.statusBar.addWidget(hello)

        self.table.cellClicked.connect(self.cell_clicked)
    # def status_bar(self):
    #     pass

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
        connection = sqlite3.connect("database.db")
        result = connection.execute("SELECT * FROM students")
        # print(list(result))
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        connection.close()

    def insert(self):
        dialog = InsertDialogue()
        dialog.exec()

    def search(self):
        dialog = SearchDialogue()
        dialog.exec()

    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()



class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Edit Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Get student name
        index = age_calculator.table.currentRow()
        student_name = age_calculator.table.item(index, 1).text()

        self.student_id = age_calculator.table.item(index, 0).text()

        # Student name widget
        self.student_name = QLineEdit(student_name)
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # course selection widget
        course = age_calculator.table.item(index, 2).text()
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(course)
        layout.addWidget(self.course_name)
        
        # widget for the phone
        mobile = age_calculator.table.item(index, 3).text()
        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Mobile Tel")
        layout.addWidget(self.mobile)

        button = QPushButton("Submit")
        button.clicked.connect(self.update)
        layout.addWidget(button)

        self.setLayout(layout)

    def update(self):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name = ?, course = ?, mobile = ? WHERE ID = ?", 
                       (
                        self.student_name.text(), 
                        self.course_name.itemText(self.course_name.currentIndex()), 
                        self.mobile.text(), 
                        self.student_id
                        ))
        connection.commit()
        cursor.close()
        connection.close()
        # Refresh
        age_calculator.load_data()


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Edit Student Data")

        layout = QGridLayout()
        confirmation = QLabel("Are you sure you want to delete?")
        yes = QPushButton("Yes")
        no = QPushButton("No")

        layout.addWidget(confirmation, 0, 0, 1, 2)
        layout.addWidget(yes, 1, 0)
        layout.addWidget(no, 1, 1)
        self.setLayout(layout)

        yes.clicked.connect(self.delete_student)

    def delete_student(self):
        index = age_calculator.table.currentRow()
        student_id = age_calculator.table.item(index, 0).text()

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("DELETE from students WHERE id = ?", (student_id, ))
        connection.commit()
        cursor.close()
        connection.close()
        age_calculator.load_data()

        self.close()

        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setText("The data was deleted.")
        confirmation_widget.exec()



class SearchDialogue(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Search Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        button = QPushButton("Search")
        button.clicked.connect(self.search)
        layout.addWidget(button)

        self.setLayout(layout)

    def search(self):
        name = self.student_name.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM students WHERE name = ?", (name,))
        rows = list(result)
        print(rows)
        items = age_calculator.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            print(item)
            age_calculator.table.item(item.row(), 1).setSelected(True)

        cursor.close()
        connection.close()


class InsertDialogue(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Student name widget
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # course selection widget
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)
        
        # widget for the phone
        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Mobile Tel")
        layout.addWidget(self.mobile)

        button = QPushButton("Submit")
        button.clicked.connect(self.add_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def add_student(self):
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)",
                              (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()
        age_calculator.load_data()
      

app = QApplication(sys.argv)
age_calculator = MainWindow()
age_calculator.show()
age_calculator.load_data()
app.exit(app.exec())