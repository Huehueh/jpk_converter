#!/usr/bin/python3

from check import is_xml_correct
from convert import convert_file
import argparse, os, sys
from PyQt5.QtWidgets import *

class MainDialog(QWidget):
    def __init__(self, parent=None):
        super(MainDialog, self).__init__(parent)

        self.filenames = []


        layout = QVBoxLayout()

        self.btn = QPushButton("Wybierz pliki")
        self.btn.clicked.connect(self.getfiles)
        layout.addWidget(self.btn)

        self.message = QTextEdit()
        layout.addWidget(self.message)

        self.setLayout(layout)
        self.setWindowTitle("kinole demo")

    def get_converted_name(self, name):
        elements = list(os.path.splitext(name))
        elements.insert(len(elements)-1, "converted")
        return ".".join(elements)

    def convert_and_check_xml(self, input_file: str):
        output_file = self.get_converted_name(input_file)
        convert_file(input_file, output_file)
        self.message.setText(f"Przetwarzono {input_file}")
        good = is_xml_correct(output_file)
        if good == None:
            self.message.setText(f"Nie można sprawdzić poprawności pliku {input_file}!")
        else:
             self.message.setText(f"Wygenerowano poprawny {output_file}!" if good else f"{output_file} niepoprawny:(")

    def getfiles(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.ExistingFiles)
        # dlg.setFilter("XML files (*.xml)")
        if dlg.exec_():
            filenames = dlg.selectedFiles()
            self.message.setText("Przetwarzam " + " ".join(filenames))
            for file in filenames:
                self.convert_and_check_xml(file)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainDialog()
    window.show()
    sys.exit(app.exec_())
