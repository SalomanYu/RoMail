from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtCore import QFile, QPoint, QRect, QSize, QUrl
from PyQt5.QtGui import QIcon, QPixmap, QCursor
import sys,os
import email_sender
from functools import partial


class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.widget = QWidget()
        self.setCentralWidget(self.widget)
        self.setWindowTitle('RoMail')
        self.resize(1123,658)

        self.pos_x, self.pos_y = 0, 0
        self.filesList = []
        self.filesPath = {}

        # self.layout = QVBoxLayout()
        # self.widget.setLayout(self.layout)

        self.setupUI()


    def setupUI(self):
        self.title = QLabel('Новое письмо', objectName='title',parent=self.widget)
        self.title.setGeometry(QRect(30,10,261,41))

        self.line = QFrame(self.widget, objectName='line')
        self.line.setFrameShape(QFrame.HLine)
        self.line.setGeometry(QRect(30,60,1050,3))

        self.addressLabel = QLabel('Кому', self.widget)
        self.addressLabel.setGeometry(QRect(10,80,51,31))
        self.addressField = QLineEdit(self.widget)
        self.addressField.setGeometry(QRect(80,80,1021,31))

        self.fromLabel = QLabel('От кого', self.widget)
        self.fromLabel.setGeometry(QRect(10,130,51,31))
        self.fromField = QLineEdit(self.widget)
        self.fromField.setGeometry(QRect(80,130,1021,31))

        self.themeLabel = QLabel('Тема', self.widget)
        self.themeLabel.setGeometry(QRect(10,180,51,31))
        self.themeField = QLineEdit(self.widget)
        self.themeField.setGeometry(QRect(80,180,1021,31))

        self.messageField = QTextEdit(self.widget)
        self.messageField.setGeometry(QRect(10,240,1091,321))
        self.messageField.setPlaceholderText('Напишите что-нибудь')

        self.sendButton = QPushButton('Отправить', self.widget, objectName='sendButton')
        self.sendButton.setGeometry(QRect(20,580,111,41))
        self.sendButton.setCursor(QtCore.Qt.PointingHandCursor)

        self.insertButton = QPushButton('', self.widget, objectName='insertButton', iconSize=QSize(24,24))
        self.insertButton.setGeometry(QRect(140,590,31,27))
        self.insertButton.setCursor(QtCore.Qt.PointingHandCursor)
        self.insertButton.setIcon(QIcon('media/insert.png'))

        self.frame = QFrame(self.widget)
        self.frame.setGeometry(QRect(190, 580, 921, 61))

        self.sendButton.clicked.connect(self.send)
        self.insertButton.clicked.connect(self.select_files)


    def select_files(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileTypes = 'All Files (*);; MP3(*.mp3);; TXT(*.txt);;Python(*.py);; PDF(*.pdf)'
        filenames, _ = QFileDialog.getOpenFileNames(self, 'Прикрепить файл', '',
                fileTypes, options=options)
            
        if filenames:
            self.pos_x, self.pos_y = 0, 0
            for widget in self.frame.children():
                widget.deleteLater()
                widget = None
            self.filesList = list(set(self.filesList+filenames))
            self.add_files(self.filesList)
            


    def add_files(self, array):
        for file in array:
            name = os.path.basename(file)
            self.filesPath[file] = name

            attachment = QLabel(name, self.frame)
            attachment.setStyleSheet('color:black')
            attachment.move(self.pos_x, self.pos_y)
            attachment.adjustSize()
            
            removeButton = QPushButton('', self.frame, icon=QIcon('media/delete.png'), iconSize=QSize(15,15))
            removeButton.setStyleSheet('border:none')
            removeButton.setCursor(QtCore.Qt.PointingHandCursor)
            removeButton.clicked.connect(partial(self.delete_item, array, file))
            removeButton.move(self.pos_x+ attachment.width() +5, self.pos_y)

            attachment.show()
            removeButton.show()

            if self.pos_x > self.frame.width() - 200:
                self.pos_y += 30
                self.pos_x = 0
            else:
                self.pos_x += attachment.width() + 30

    
    def delete_item(self, itemList:list, item):
        self.pos_x, self.pos_y = 0, 0
        frameChildrens = self.frame.children()
        for widget in frameChildrens:
            widget.deleteLater()
            widget = None
        itemList.remove(item)
        del self.filesPath[item]
        self.add_files(itemList)


    def send(self):
        to_email = self.addressField.text()
        sender_email = self.fromField.text()
        theme = self.themeField.text()
        message = self.messageField.toPlainText()
        if '@' in sender_email and '@' in to_email:
            dialog = QInputDialog(self.widget)
            dialog.setHidden(True)
            sender_password, response= dialog.getText(self.widget, 'Введите пароль', 'Пароль от почты:', QLineEdit.Password)
            
            self.messageBoxes('Информация', 'Отправляем...')
            result = email_sender.send_email(FROM=sender_email, TO=to_email, MESSAGE=message, THEME=theme, PASSWORD=sender_password, attachment=self.filesPath)
            if result == 'The message was sent successfully!':
                self.addressField.clear()
                self.fromField.clear()
                self.themeField.clear()
                self.messageField.clear()
                self.filesPath = {}
                self.pos_x, self.pos_y = 0, 0
                for widget in self.frame.children():
                    widget.deleteLater()
                    widget = None
                self.messageBoxes('Успешно!', f'Ваше сообщение было успешно доставлено по адресу: {to_email}')
            else:
                self.messageBoxes('Ошибка', 'Неправильно введен пароль или логин!')

        else:
            self.messageBoxes('Ошибка', 'Проверьте свой email')


    def messageBoxes(self, title, text):
        QMessageBox.about(self.widget, title, text)

app = QApplication(sys.argv)
window = App()
with open('style.css') as file:
    style = file.read()
window.setStyleSheet(style)
window.show()
sys.exit(app.exec_())
