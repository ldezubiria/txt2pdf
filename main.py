import sys
from txt2pdf import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import qApp


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
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "Archivos de Texto (*.txt);;Todos los Archivos (*)")
        if fileName:
            self.ui.lineEdit_txt_path.setText(fileName)

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
        pdf_path = self.ui.lineEdit_pdf_path.text()
        txt_path = self.ui.lineEdit_txt_path.text()
        if self.ui.radioButton_liq.isChecked():
            if path.isdir(pdf_path) is True and path.isfile(txt_path) is True:
                self.ui.textBox1.clear()
                from lib import doLiquidaciones
                output = doLiquidaciones(txt_path, pdf_path)
                for i in output:
                    self.ui.textBox1.appendPlainText(i)


        if self.ui.radioButton_vol.isChecked():
            if path.isdir(pdf_path) is True and path.isfile(txt_path) is True:
                self.ui.textBox1.clear()
                from lib import doVolantes
                output = doVolantes(txt_path, pdf_path)
                for i in output:
                    self.ui.textBox1.appendPlainText(i)





if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = mainWindow()
    ui.show()
    sys.exit(app.exec_())