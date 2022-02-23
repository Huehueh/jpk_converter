#!/usr/bin/python3

import argparse, os, sys
from ui import MainDialog
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainDialog()
    window.show()
    sys.exit(app.exec_())
