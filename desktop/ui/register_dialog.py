from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, QWidget, QScrollArea)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QPainter
from services.api_client import APIClient
from utils.helpers import show_error, show_success
import re


class PasswordStrengthWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.strength = 0
        self.label_text = ""
        self.color = QColor("#e0e0e0")
        self.setFixedHeight(35)
        
    def set_strength(self, password):
        if not password:
            self.strength = 0
            self.label_text = ""
            self.color = QColor("#e0e0e0")
            self.update()
            return
            
        strength = 0
        if len(password) >= 8:
            strength += 25
        if any(c.islower() for c in password) and any(c.isupper() for c in password):
            strength += 25
        if any(c.isdigit() for c in password):
            strength += 25
        if any(not c.isalnum() for c in password):
            strength += 25
            
        self.strength = strength
        
        if strength <= 25:
            self.label_text = "Weak"
            self.color = QColor("#ef4444")
        elif strength <= 50:
            self.label_text = "Fair"
            self.color = QColor("#f59e0b")
        elif strength <= 75:
            self.label_text = "Good"
            self.color = QColor("#3b82f6")
        else:
            self.label_text = "Strong"
            self.color = QColor("#10b981")
            
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        painter.setBrush(QColor("#e5e7eb"))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(0, 0, self.width(), 8, 4, 4)
        
        if self.strength > 0:
            strength_width = int((self.width() * self.strength) / 100)
            painter.setBrush(self.color)
            painter.drawRoundedRect(0, 0, strength_width, 8, 4, 4)
        
        if self.label_text:
            painter.setPen(self.color)
            font = QFont("Segoe UI", 9, QFont.Bold)
            painter.setFont(font)
            painter.drawText(0, 22, self.label_text)


class ModernLineEdit(QLineEdit):
    def __init__(self, placeholder="", is_password=False):
        super().__init__()
        self.setPlaceholderText(placeholder)
        self.is_password = is_password
        self.password_visible = False
        
        if is_password:
            self.setEchoMode(QLineEdit.Password)
            
        self.setMinimumHeight(60)
        self.update_style(False)
        
        if is_password:
            self.toggle_btn = QPushButton(self)
            self.toggle_btn.setFixedSize(45, 45)
            self.toggle_btn.setCursor(Qt.PointingHandCursor)
            self.toggle_btn.clicked.connect(self.toggle_password_visibility)
            self.update_toggle_button()
            
    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.is_password:
            self.toggle_btn.move(self.width() - 55, 7)
            
    def toggle_password_visibility(self):
        self.password_visible = not self.password_visible
        if self.password_visible:
            self.setEchoMode(QLineEdit.Normal)
        else:
            self.setEchoMode(QLineEdit.Password)
        self.update_toggle_button()
        
    def update_toggle_button(self):
        if self.password_visible:
            self.toggle_btn.setText("\U0001F441")
            self.toggle_btn.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    border: none;
                    color: #10b981;
                    font-size: 24px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: rgba(16, 185, 129, 0.1);
                    border-radius: 8px;
                }
            """)
        else:
            self.toggle_btn.setText("\U0001F576")
            self.toggle_btn.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    border: none;
                    color: #9ca3af;
                    font-size: 22px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: rgba(16, 185, 129, 0.1);
                    border-radius: 8px;
                    color: #10b981;
                }
            """)
        
    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.update_style(True)
        
    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.update_style(False)
        
    def update_style(self, focused):
        if focused:
            self.setStyleSheet("""
                QLineEdit {
                    padding: 18px 60px 18px 20px;
                    border: 2px solid #10b981;
                    border-radius: 10px;
                    background: white;
                    font-size: 16px;
                    color: #1f2937;
                    font-family: 'Segoe UI';
                }
            """)
        else:
            self.setStyleSheet("""
                QLineEdit {
                    padding: 18px 60px 18px 20px;
                    border: 2px solid #e5e7eb;
                    border-radius: 10px;
                    background: #f9fafb;
                    font-size: 16px;
                    color: #1f2937;
                    font-family: 'Segoe UI';
                }
                QLineEdit:hover {
                    border: 2px solid #d1d5db;
                    background: white;
                }
            """)


class RegisterDialog(QDialog):
    registration_successful = pyqtSignal(str)
    
    def __init__(self, api_client=None):
        super().__init__()
        self.api = api_client or APIClient()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Register - Chemical Equipment Visualizer")
        self.setMinimumSize(600, 750)
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #f0fdf4, stop:1 #ffffff);
            }
        """)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: #f3f4f6;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #10b981;
                border-radius: 5px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background: #059669;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)
        
        scroll_content = QWidget()
        layout = QVBoxLayout(scroll_content)
        layout.setSpacing(0)
        layout.setContentsMargins(50, 40, 50, 40)
        
        title = QLabel("Create Account")
        title.setFont(QFont("Segoe UI", 38, QFont.Bold))
        title.setStyleSheet("color: #10b981;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        layout.addSpacing(8)
        
        subtitle = QLabel("Join Chemical Equipment Visualizer")
        subtitle.setFont(QFont("Segoe UI", 14))
        subtitle.setStyleSheet("color: #6b7280;")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        
        layout.addSpacing(35)
        
        username_label = QLabel("Username")
        username_label.setFont(QFont("Segoe UI", 15, QFont.Bold))
        username_label.setStyleSheet("color: #374151;")
        layout.addWidget(username_label)
        
        layout.addSpacing(10)
        
        self.username_input = ModernLineEdit("Choose a unique username (3-20 characters)")
        layout.addWidget(self.username_input)
        
        layout.addSpacing(25)
        
        email_label = QLabel("Email Address")
        email_label.setFont(QFont("Segoe UI", 15, QFont.Bold))
        email_label.setStyleSheet("color: #374151;")
        layout.addWidget(email_label)
        
        layout.addSpacing(10)
        
        self.email_input = ModernLineEdit("your.email@example.com")
        layout.addWidget(self.email_input)
        
        layout.addSpacing(25)
        
        password_label = QLabel("Password")
        password_label.setFont(QFont("Segoe UI", 15, QFont.Bold))
        password_label.setStyleSheet("color: #374151;")
        layout.addWidget(password_label)
        
        layout.addSpacing(10)
        
        self.password_input = ModernLineEdit("Create a strong password", is_password=True)
        self.password_input.textChanged.connect(self.update_password_strength)
        layout.addWidget(self.password_input)
        
        layout.addSpacing(8)
        
        requirements = QLabel("Must be 8+ characters with uppercase, number, and special character")
        requirements.setFont(QFont("Segoe UI", 11))
        requirements.setStyleSheet("color: #9ca3af;")
        requirements.setWordWrap(True)
        layout.addWidget(requirements)
        
        layout.addSpacing(8)
        
        self.password_strength = PasswordStrengthWidget()
        layout.addWidget(self.password_strength)
        
        layout.addSpacing(25)
        
        confirm_label = QLabel("Confirm Password")
        confirm_label.setFont(QFont("Segoe UI", 15, QFont.Bold))
        confirm_label.setStyleSheet("color: #374151;")
        layout.addWidget(confirm_label)
        
        layout.addSpacing(10)
        
        self.confirm_input = ModernLineEdit("Re-enter your password", is_password=True)
        self.confirm_input.returnPressed.connect(self.handle_register)
        layout.addWidget(self.confirm_input)
        
        layout.addSpacing(35)
        
        button_layout = QHBoxLayout()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setMinimumHeight(58)
        cancel_btn.setCursor(Qt.PointingHandCursor)
        cancel_btn.setFont(QFont("Segoe UI", 16, QFont.Bold))
        cancel_btn.setStyleSheet("""
            QPushButton {
                background: #e5e7eb;
                color: #374151;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover {
                background: #d1d5db;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        button_layout.addSpacing(15)
        
        self.register_btn = QPushButton("Create Account")
        self.register_btn.setMinimumHeight(58)
        self.register_btn.setCursor(Qt.PointingHandCursor)
        self.register_btn.setFont(QFont("Segoe UI", 16, QFont.Bold))
        self.register_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #10b981, stop:1 #059669);
                color: white;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #059669, stop:1 #047857);
            }
        """)
        self.register_btn.clicked.connect(self.handle_register)
        button_layout.addWidget(self.register_btn)
        
        layout.addLayout(button_layout)
        
        layout.addSpacing(25)
        
        login_layout = QHBoxLayout()
        login_layout.setAlignment(Qt.AlignCenter)
        
        login_label = QLabel("Already have an account?")
        login_label.setFont(QFont("Segoe UI", 13))
        login_label.setStyleSheet("color: #6b7280;")
        login_layout.addWidget(login_label)
        
        login_btn = QPushButton("Login")
        login_btn.setFlat(True)
        login_btn.setCursor(Qt.PointingHandCursor)
        login_btn.setFont(QFont("Segoe UI", 13, QFont.Bold))
        login_btn.setStyleSheet("""
            QPushButton {
                color: #10b981;
                border: none;
                padding: 8px 12px;
            }
            QPushButton:hover {
                color: #059669;
                text-decoration: underline;
            }
        """)
        login_btn.clicked.connect(self.show_login)
        login_layout.addWidget(login_btn)
        
        layout.addLayout(login_layout)
        
        layout.addSpacing(20)
        
        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)
    
    def update_password_strength(self, text):
        self.password_strength.set_strength(text)
    
    def validate_inputs(self):
        username = self.username_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text()
        confirm = self.confirm_input.text()
        
        if not username or not email or not password or not confirm:
            show_error(self, "All fields are required")
            return False
        
        if not re.match(r'^[a-zA-Z0-9_]{3,20}$', username):
            show_error(self, "Username must be 3-20 characters (letters, numbers, underscore only)")
            self.username_input.setFocus()
            return False
        
        if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
            show_error(self, "Invalid email format")
            self.email_input.setFocus()
            return False
        
        if len(password) < 8:
            show_error(self, "Password must be at least 8 characters")
            self.password_input.setFocus()
            return False
        
        if not re.search(r'[A-Z]', password):
            show_error(self, "Password must contain at least one uppercase letter")
            self.password_input.setFocus()
            return False
        
        if not re.search(r'[0-9]', password):
            show_error(self, "Password must contain at least one number")
            self.password_input.setFocus()
            return False
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            show_error(self, "Password must contain at least one special character")
            self.password_input.setFocus()
            return False
        
        if password != confirm:
            show_error(self, "Passwords do not match")
            self.confirm_input.setFocus()
            return False
        
        return True
    
    def handle_register(self):
        if not self.validate_inputs():
            return
        
        username = self.username_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text()
        
        self.register_btn.setEnabled(False)
        self.register_btn.setText("Creating Account...")
        
        success, result = self.api.register(username, email, password)
        
        self.register_btn.setEnabled(True)
        self.register_btn.setText("Create Account")
        
        if success:
            verification_required = result.get('verification_required', True)
            email_sent = result.get('email_sent', False)
            dev_code = result.get('dev_code', None)
            
            if verification_required:
                if email_sent:
                    QMessageBox.information(
                        self,
                        "Registration Successful",
                        f"Registration successful!\n\n"
                        f"A verification code has been sent to:\n{email}\n\n"
                        f"Please check your email and enter the code below."
                    )
                else:
                    QMessageBox.information(
                        self,
                        "Registration Successful (Dev Mode)",
                        f"Registration successful!\n\n"
                        f"Email sending failed (check backend config).\n\n"
                        f"Verification code: {dev_code}\n\n"
                        f"Use this code to verify your email."
                    )
                
                code, ok = self.get_verification_code()
                
                if ok and code:
                    verify_success, verify_result = self.api.verify_email(username, code)
                    
                    if verify_success:
                        show_success(
                            self,
                            f"Email verified successfully!\n\n"
                            f"You can now login with your credentials."
                        )
                        self.registration_successful.emit(username)
                        self.accept()
                    else:
                        show_error(self, f"Verification failed:\n{verify_result}")
                else:
                    QMessageBox.warning(
                        self,
                        "Verification Pending",
                        "Registration complete but email not verified.\n\n"
                        "Please verify your email before logging in.\n\n"
                        "Check your email for the verification code."
                    )
            else:
                show_success(self, "Registration successful! You can now login.")
                self.registration_successful.emit(username)
                self.accept()
        else:
            show_error(self, f"Registration failed:\n{result}")
    
    def get_verification_code(self):
        from PyQt5.QtWidgets import QInputDialog
        
        dialog = QInputDialog(self)
        dialog.setWindowTitle("Email Verification")
        dialog.setLabelText("Enter the 6-digit verification code:")
        dialog.setInputMode(QInputDialog.TextInput)
        dialog.setTextValue("")
        dialog.setStyleSheet("""
            QInputDialog {
                background-color: white;
            }
            QLabel {
                font-size: 14px;
                color: #374151;
                font-weight: bold;
            }
            QLineEdit {
                padding: 14px;
                border: 2px solid #10b981;
                border-radius: 8px;
                font-size: 16px;
                min-width: 250px;
            }
            QPushButton {
                padding: 12px 24px;
                background-color: #10b981;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #059669;
            }
        """)
        
        ok = dialog.exec_()
        code = dialog.textValue().strip()
        
        return code, ok
    
    def show_login(self):
        from .login_window import LoginDialog
        
        self.hide()
        
        login_dialog = LoginDialog(self.api)
        
        if login_dialog.exec_() == QDialog.Accepted:
            self.accept()
        else:
            self.show()