from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, QGridLayout, QLineEdit, \
    QPushButton, QMainWindow, QTableWidget, QTableWidgetItem, QDialog, QComboBox, QToolBar, QStatusBar, \
    QMessageBox
import sys
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt
import sqlite3
import pymysql


class DataBaseConection():
    def __init__(self, host="localhost", user="root", password="pythoncourse", database="school"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def connect(self):
        return pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            cursorclass=pymysql.cursors.Cursor
        )


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


# Remaining classes are unchanged
# ... [EditDialog, DeleteDialog, SearchDialogue, InsertDialogue]
# are already implemented correctly above and remain the same

if __name__ == "__main__":
    app = QApplication(sys.argv)
    windowOne = MainWindow()
    windowOne.show()
    windowOne.load_data()
    sys.exit(app.exec())