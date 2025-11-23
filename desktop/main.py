import os
import sys
os.environ['MPLBACKEND'] = 'Qt5Agg'
os.environ['QT_API'] = 'pyqt5'

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

print("=" * 80)
print("Starting Chemical Equipment Visualizer...")
print("=" * 80)

import config
from services.api_client import APIClient
from ui.login_window import LoginWindow

class App:
    """Application holder"""
    def __init__(self):
        print("[App] Creating QApplication...")
        self.app = QApplication(sys.argv)
        self.app.setStyle('Fusion')
        self.app.setFont(QFont("Segoe UI", 10))
        
    
        sys.excepthook = self.exception_handler
        
        print("[App] QApplication created")
        
        print("[App] Creating API client...")
        self.api = APIClient()
        print("[App] API client created")
        
        self.login_window = None
        self.main_window = None
        
        self.show_login()
    
    def exception_handler(self, exc_type, exc_value, exc_traceback):
        """Global exception handler"""
        print("=" * 80)
        print("UNCAUGHT EXCEPTION!")
        print("=" * 80)
        print("Type:", exc_type)
        print("Value:", exc_value)
        print("Traceback:")
        import traceback
        traceback.print_tb(exc_traceback)
        print("=" * 80)
        
        QMessageBox.critical(
            None, "Fatal Error",
            "Application crashed:\n\n{}: {}".format(exc_type.__name__, str(exc_value))
        )
    
    def show_login(self):
        """Show login window"""
        print("[App] Creating login window...")
        self.login_window = LoginWindow(self.api)
        self.login_window.login_successful.connect(self.on_login_success)
        print("[App] Login window created")
        
        print("[App] Showing login window...")
        self.login_window.show()
        print("[App] Login window shown")
    
    def on_login_success(self, user_data):
        """Handle successful login"""
        print("=" * 80)
        print("[App] Login successful callback triggered")
        print("[App] User: {}".format(user_data.get('username')))
        print("=" * 80)
        
        try:
            print("[App] Hiding login window...")
            self.login_window.hide()
            print("[App] Login window hidden")
            
            print("[App] Importing MainWindow...")
            from ui.main_window import MainWindow
            print("[App] MainWindow imported")
            
            print("[App] Creating MainWindow instance...")
            self.main_window = MainWindow(self.api, user_data)
            print("[App] MainWindow instance created")
            
            print("[App] Showing MainWindow...")
            self.main_window.show()
            print("[App] MainWindow shown")
            
            print("=" * 80)
            print("[App] Main window displayed successfully!")
            print("=" * 80)
            
        except Exception as e:
            print("=" * 80)
            print("[App] ERROR in on_login_success:")
            print(str(e))
            import traceback
            traceback.print_exc()
            print("=" * 80)
            
            QMessageBox.critical(None, "Error", "Failed to create main window:\n{}".format(str(e)))
    
    def run(self):
        """Run application"""
        print("[App] Starting event loop...")
        return self.app.exec_()


if __name__ == '__main__':
    try:
        print("[Main] Creating App instance...")
        application = App()
        print("[Main] App instance created")
        
        print("[Main] Running application...")
        exit_code = application.run()
        
        print("[Main] Application exited with code: {}".format(exit_code))
        sys.exit(exit_code)
        
    except Exception as e:
        print("=" * 80)
        print("[Main] FATAL ERROR:")
        print(str(e))
        print("=" * 80)
        import traceback
        traceback.print_exc()
        print("=" * 80)
        input("Press Enter to exit...")
        sys.exit(1)