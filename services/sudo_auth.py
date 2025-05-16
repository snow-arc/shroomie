import subprocess
from PyQt6.QtWidgets import QMessageBox
from ui.dialogs.password_dialog import PasswordDialog

class SudoAuth:
    def __init__(self):
        self._auth_status = False
    
    def authenticate(self, parent=None, attempts=3):
        """Authenticate user with sudo"""
        for _ in range(attempts):
            dialog = PasswordDialog(parent)
            if password := dialog.get_password():
                try:
                    # Verify sudo access
                    proc = subprocess.Popen(
                        ['sudo', '-S', 'true'],
                        stdin=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                    _, error = proc.communicate(input=f"{password}\n".encode())
                    
                    if proc.returncode == 0:
                        self._auth_status = True
                        return True
                        
                except Exception as e:
                    QMessageBox.critical(parent, "Error", str(e))
            
            if _ < attempts - 1:
                retry = QMessageBox.question(
                    parent,
                    "Authentication Failed",
                    "Wrong password. Would you like to try again?"
                )
                if retry != QMessageBox.StandardButton.Yes:
                    break
        
        return False
    
    @property
    def is_authenticated(self):
        return self._auth_status
