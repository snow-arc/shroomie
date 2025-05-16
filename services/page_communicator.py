from PyQt6.QtCore import QObject, pyqtSignal

class PageCommunicator(QObject):
    # Signals
    packageDeleted = pyqtSignal(str)
    packageInstalled = pyqtSignal(str)
    packageUpdated = pyqtSignal(dict)  # Emit package info dictionary
    refreshNeeded = pyqtSignal()  # New signal for refresh
    
    # Class instance
    _instance = None
    
    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def __init__(self):
        if PageCommunicator._instance is not None:
            raise Exception("Use PageCommunicator.instance() instead")
        super().__init__()
        PageCommunicator._instance = self
    
    def request_refresh(self):
        """Request all pages to refresh their data"""
        self.refreshNeeded.emit()
