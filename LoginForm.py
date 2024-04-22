import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QMessageBox
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class LoginForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle('Personal Informatics')
        self.resize(500, 120)
        layout = QGridLayout(self)

        label_name = QLabel('Username')
        self.lineEdit_username = QLineEdit()
        self.lineEdit_username.setPlaceholderText('Please enter your username')
        label_password = QLabel('Password')
        self.lineEdit_password = QLineEdit()
        self.lineEdit_password.setPlaceholderText('Please enter your password')
        self.lineEdit_password.setEchoMode(QLineEdit.Password)

        button_login = QPushButton('Login')
        button_login.clicked.connect(self.check_password)

        layout.addWidget(label_name, 0, 0)
        layout.addWidget(self.lineEdit_username, 0, 1)
        layout.addWidget(label_password, 1, 0)
        layout.addWidget(self.lineEdit_password, 1, 1)
        layout.addWidget(button_login, 2, 0, 1, 2)
        layout.setRowMinimumHeight(2, 75)

    def check_password(self):
        username = self.lineEdit_username.text()
        password = self.lineEdit_password.text()
        if username == 'Username' and password == '000':
            self.open_success_form()
        else:
            msg = QMessageBox()
            msg.setText('Incorrect Password')
            msg.exec_()

    def open_success_form(self):
        self.success_form = SuccessForm()
        self.success_form.show()
        self.close()

class SuccessForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle('Dashboard')
        self.resize(500, 400)
        layout = QGridLayout(self)

        success_label = QLabel('User Data:')
        layout.addWidget(success_label, 0, 0)

        figure = Figure()
        canvas = FigureCanvas(figure)
        axes = figure.add_subplot(111)
        axes.plot([1, 2, 3, 4, 5], [10, 1, 20, 5, 15], 'r-')
        axes.set_title('Sample Plot')
        axes.set_ylabel('Values')
        axes.set_xlabel('Time')

        layout.addWidget(canvas, 1, 0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_form = LoginForm()
    login_form.show()
    sys.exit(app.exec_())
