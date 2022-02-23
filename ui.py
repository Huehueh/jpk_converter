from PyQt5.QtWidgets import *

from convert import convert_and_check_xml


class MainDialog(QWidget):
    def __init__(self, parent=None):
        super(MainDialog, self).__init__(parent)

        self.filenames = []

        layout = QVBoxLayout()

        self.btn = QPushButton("Wybierz pliki")
        self.btn.clicked.connect(self.getfiles)
        layout.addWidget(self.btn)

        self.messageTextEdit = QTextEdit()
        layout.addWidget(self.messageTextEdit)

        self.setLayout(layout)
        self.setWindowTitle("kinole demo")
    
    def displayMessage(self, message: str):
        prev = self.messageTextEdit.setText(message)
        #TODO: append text

    def process_file(self, input_file: str):
        self.displayMessage(f"Konwersja pliku {input_file}...")
        ok = convert_and_check_xml(input_file=input_file)
        if ok == None:
            self.displayMessage(f"Nie można sprawdzić poprawności pliku!")
        else:
            self.displayMessage(
                "Wygenerowano poprawny plik!"
                if ok
                else "Plik niepoprawny:("
            )

    def getfiles(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.ExistingFiles)
        # dlg.setFilter("XML files (*.xml)")
        if dlg.exec_():
            filenames = dlg.selectedFiles()
            for file in filenames:
                self.process_file(file)