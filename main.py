import sys
from txt2pdf import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import qApp
from lib import *



class mainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton_txt.clicked.connect(self.openFileNameDialog)
        self.ui.pushButton_pdf_path.clicked.connect(self.saveFileDialog)
        self.ui.pushButton_convert.clicked.connect(self.goButton)
        self.ui.radioButton_liq.toggled.connect(self.onClicked)
        self.ui.radioButton_vol.toggled.connect(self.onClicked)
        self.ui.actionSalir.triggered.connect(qApp.quit)
    def openFileNameDialog(self):
        global txtfiles
        txtfiles = []
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        txtfiles, _ = QtWidgets.QFileDialog.getOpenFileNames(self, "QFileDialog.getOpenFileNames()", "",
                                                  "Archivos de Texto (*.txt);;Todos los Archivos (*)")
        if txtfiles:
            self.ui.lineEdit_txt_path.setText(';'.join(txtfiles))

    def saveFileDialog(self):
        fileName  = QtWidgets.QFileDialog.getExistingDirectory(self, "Seleccione la carpeta de destino...")

        if fileName:
            self.ui.lineEdit_pdf_path.setText(fileName)

    def onClicked(self):
        radioBtn=self.sender()
        if radioBtn.isChecked():
            self.ui.pushButton_convert.setEnabled(True)

    def exit(self):
        sys.exit()

    def goButton(self):
        from os import path
        count = 0
        pdf_path = self.ui.lineEdit_pdf_path.text()
        txt_path = self.ui.lineEdit_txt_path.text().split(';')
        if self.ui.radioButton_liq.isChecked():
            if check_dir(pdf_path) is True and check_files(txt_path) is True:
                self.ui.textBox1.clear()
                output = doPDF(txt_path,pdf_path)
                for i in output:
                    self.ui.textBox1.appendPlainText(i)
                    count += 1
                self.ui.textBox1.appendPlainText('\n{0} documentos creados.'.format(count))
        if self.ui.radioButton_vol.isChecked():
            if check_dir(pdf_path) is True and check_files(txt_path) is True:
                self.ui.textBox1.clear()
                output = doVolantes(txt_path, pdf_path)
                for i in output:
                    self.ui.textBox1.appendPlainText(i)
                    count += 1
                self.ui.textBox1.appendPlainText('\n{0} documentos creados.'.format(count))




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = mainWindow()
    ui.show()
    sys.exit(app.exec_())