import subprocess
import sys
import os

# Add project root to Python path for absolute imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from PyQt6.QtWidgets import QMessageBox, QWidget
from ui.dialogs.password_dialog import PasswordDialog

class SudoAuth:
    def __init__(self) -> None:
        self._auth_status: bool = False
    
    def authenticate(self, parent: QWidget | None = None, attempts: int = 2) -> bool:
        """Authenticate user with sudo"""
        for attempt in range(attempts):
            dialog = PasswordDialog(parent)
            password = dialog.get_password()
            
            if password is None:  # User clicked Cancel
                sys.exit(0)
                
            try:
                # Verify sudo access
                proc = subprocess.Popen(
                    ['sudo', '-S', 'true'],
                    stdin=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                proc.communicate(input=f"{password}\n".encode())
                
                if proc.returncode == 0:
                    self._auth_status = True
                    return True
                    
            except Exception as e:
                QMessageBox.critical(parent, "Error", str(e))
            
            remaining_attempts = attempts - attempt - 1
            if remaining_attempts > 0:
                retry = QMessageBox.question(
                    parent,
                    "Authentication Failed",
                    "Wrong password. Would you like to try again?"
                )
                if retry != QMessageBox.StandardButton.Yes:
                    sys.exit(0)  # Exit if user clicks No
            else:
                QMessageBox.critical(
                    parent,
                    "Authentication Failed",
                    "Maximum attempts reached. The program will now exit."
                )
                sys.exit(0)  # Exit after two failed attempts
        
        return False
    
    @property
    def is_authenticated(self) -> bool:
        return self._auth_status
