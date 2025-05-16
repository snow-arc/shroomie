import sys
import subprocess
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QLineEdit, QPushButton, QTextEdit
)


class YaySearchApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Yay Package Search")
        self.setGeometry(200, 200, 600, 400)

        self.layout = QVBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("search for pkg..")
        self.layout.addWidget(self.search_input)

        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_package)
        self.layout.addWidget(self.search_button)

        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        self.layout.addWidget(self.result_area)

        self.setLayout(self.layout)

        # Show AUR packages on startup
        self.list_aur_packages()

    def list_aur_packages(self):
        try:
            result = subprocess.run(
                ["pacman", "-Qqm"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                self.result_area.setPlainText("Installed AUR packages:\n" + result.stdout)
            else:
                self.result_area.setPlainText("Failed to get AUR packages:\n" + result.stderr)
        except FileNotFoundError:
            self.result_area.setPlainText("'pacman' not found.")

    def search_package(self):
        package_name = self.search_input.text().strip()
        if not package_name:
            self.result_area.setPlainText("write a package name")
            return

        try:
            result = subprocess.run(
                ["yay", "-Qs", package_name],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                self.result_area.setPlainText(result.stdout)
            else:
                self.result_area.setPlainText("wrong happen\n" + result.stderr)
        except FileNotFoundError:
            self.result_area.setPlainText("oh u dont have yay man? what a user dont have yay on arch?")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = YaySearchApp()
    window.show()
    sys.exit(app.exec())
