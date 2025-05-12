from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QMainWindow, QTableWidget, QTableWidgetItem
import sys
from PyQt6.QtGui import QAction
import sqlite3

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Managment System")

        file_menu_item = self.menuBar().addMenu("&file")
        help_menu_item = self.menuBar().addMenu("&help")

        add_student_action = QAction("Add Student", self)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

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


app = QApplication(sys.argv)
age_calculator = MainWindow()
age_calculator.show()
age_calculator.load_data()
app.exit(app.exec())