import sys, os ,subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout,QMessageBox
from PyQt5.QtCore import Qt
# from PyQt5.QtGui import QPixmap
 
def showPopUp(text,level):
    msg = QMessageBox()
    msg.setWindowTitle("qikwall")
    msg.setText(text)
    msg.setIcon(level)
    x = msg.exec_()

class ImageLabel(QLabel):
    def __init__(self):
        super().__init__()
 
        self.setAlignment(Qt.AlignCenter)
        self.setText('\nqikwall\n Drop an Image Here to set\n   wallpaper and terminal color scheme   \n')
        self.setStyleSheet('''
            QLabel{
                border: 4px dashed #aaa
            }
        ''')
 
    def setPixmap(self, image):
        super().setPixmap(image)

class qikwallInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(400, 200)
        self.setAcceptDrops(True)
 
        mainLayout = QVBoxLayout()

        # check for if pywal exists
        try:
            res = subprocess.run(['wal','--help'],stdout=subprocess.PIPE)

        except:
            showPopUp("pywal not installed! run `sudo pip3 install pywal'",QMessageBox.Critical)
            exit(1)
 
        self.photoViewer = ImageLabel()
        mainLayout.addWidget(self.photoViewer)
 
        self.setLayout(mainLayout)
 
    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()
 
    def dragMoveEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()
 
    def dropEvent(self, event):
        if event.mimeData().hasImage:
            event.setDropAction(Qt.CopyAction)
            file_path = event.mimeData().urls()[0].toLocalFile()
            self.set_image(file_path)
 
            event.accept()
        else:
            event.ignore()
 
    def set_image(self, file_path):
        is_err = 0
        # self.photoViewer.setPixmap(QPixmap(file_path))
        
        #set as wallpaper
        wallpaer_command = f'gsettings set org.gnome.desktop.background picture-uri "file://{file_path}"'
        try:
            res = subprocess.run(wallpaer_command,shell=True,stdout=subprocess.PIPE)
            # status_1 = subprocess.run('echo $?',shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            # print( "status:"+ status_1.stdout.decode('utf-8'))
            # stdout,stderr = status_1.comminicate()
            # print(status_1.stdout.decode('utf-8'))
        except:
            showPopUp("could not set wallpaper",QMessageBox.Critical)
            is_err=1
        

        pywal_command = f'wal -i "{file_path}" -n'
        try:
            subprocess.call(pywal_command,shell=True)
        except:
            showPopUp("could not set color scheme",QMessageBox.warning)
            is_err=1

        if is_err ==0:
            showPopUp("wallpaper and terminal color scheme changed",QMessageBox.Information)

            
        



app = QApplication(sys.argv)
qikwall = qikwallInterface()
qikwall.show()
sys.exit(app.exec_())