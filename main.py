import sys
from PyQt5.QtWidgets import QApplication
from ui import MedicalEquipmentApp

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MedicalEquipmentApp()
    window.show()
    sys.exit(app.exec_())
