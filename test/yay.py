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
        self.search_input.setPlaceholderText("Search for a package...")
        self.layout.addWidget(self.search_input)

        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_package)
        self.layout.addWidget(self.search_button)

        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        self.layout.addWidget(self.result_area)

        self.setLayout(self.layout)

        # Show installed packages at startup
        self.list_installed_packages()

    def list_installed_packages(self):
        try:
            result = subprocess.run(
                ["yay", "-Q"],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                self.result_area.setPlainText("Installed packages:\n" + result.stdout)
            else:
                self.result_area.setPlainText("Failed to get installed packages:\n" + result.stderr)

        except FileNotFoundError:
            self.result_area.setPlainText("Error: 'yay' not found. Please install yay.")

    def search_package(self):
        package_name = self.search_input.text().strip()
        if not package_name:
            self.result_area.setPlainText("Please enter a package name.")
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
                self.result_area.setPlainText("Error occurred:\n" + result.stderr)
        except FileNotFoundError:
            self.result_area.setPlainText("Error: 'yay' not found.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = YaySearchApp()
    window.show()
    sys.exit(app.exec())
