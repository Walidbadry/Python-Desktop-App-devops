import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox
import updater

APP_VERSION = "1.0.0"  # Update when releasing a new version


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"MyApp v{APP_VERSION}")
        self.setGeometry(100, 100, 400, 200)

        self.update_btn = QPushButton("Check for Updates", self)
        self.update_btn.setGeometry(120, 80, 160, 40)
        self.update_btn.clicked.connect(self.check_updates)

    def check_updates(self):
        try:
            if updater.check_for_update(APP_VERSION):
                reply = QMessageBox.question(
                    self,
                    "Update Available",
                    "A new version is available. Do you want to update?",
                    QMessageBox.Yes | QMessageBox.No
                )
                if reply == QMessageBox.Yes:
                    updater.download_and_replace()
                    QMessageBox.information(self, "Update", "Update complete! Restart the app.")
                    sys.exit(0)
            else:
                QMessageBox.information(self, "No Update", "You're using the latest version.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Update check failed:\n{e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
