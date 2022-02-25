from xdrlib import ConversionError
from PyQt5.QtWidgets import *

from convert import ConversionException, convert_and_check_xml


class MainDialog(QWidget):
    def __init__(self, parent=None):
        super(MainDialog, self).__init__(parent)

        self.filenames = []

        layout = QVBoxLayout()

        self.btn = QPushButton("Wybierz pliki")
        self.btn.clicked.connect(self.selectXMLFilesToConvert)
        layout.addWidget(self.btn)

        self.messageTextEdit = QTextEdit()
        layout.addWidget(self.messageTextEdit)

        self.setLayout(layout)
        self.setWindowTitle("kinole demo")
    
    def displayMessage(self, message: str):
        text = self.messageTextEdit.toPlainText()
        text += message
        self.messageTextEdit.setText(text)

    def convertXMLFile(self, input_file: str):
        self.displayMessage(f"Konwersja pliku {input_file}...")
        try:
            ok = convert_and_check_xml(input_file=input_file)
        except ConversionException:
            self.displayMessage("Nie można przekonwertować pliku!")
            return

        if not ok:
            self.displayMessage(f"Nie można sprawdzić poprawności pliku!")
        else:
            self.displayMessage(
                "Konwersja się udała!"
                if ok
                else "Plik niepoprawny:("
            )

    def selectXMLFilesToConvert(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.ExistingFiles)
        # dlg.setFilter("XML files (*.xml)")
        if dlg.exec_():
            filenames = dlg.selectedFiles()
            for file in filenames:
                self.convertXMLFile(file)