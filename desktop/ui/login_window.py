from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal, QRectF, QPointF
from PyQt5.QtGui import QFont, QColor, QPainter, QPen, QBrush, QPainterPath

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


class CustomEyeButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_visible = False
        self.setFixedSize(50, 50)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
            }
            QPushButton:hover {
                background: rgba(102, 126, 234, 0.1);
                border-radius: 8px;
            }
        """)
        
    def set_visible(self, visible):
        self.is_visible = visible
        self.update()
        
    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        cx = self.width() / 2
        cy = self.height() / 2
        
        if self.is_visible:
            color = QColor("#667eea")
            painter.setPen(QPen(color, 2.5, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.setBrush(Qt.NoBrush)
            
            eye_path = QPainterPath()
            eye_path.moveTo(cx - 12, cy)
            eye_path.quadTo(cx - 10, cy - 7, cx, cy - 8)
            eye_path.quadTo(cx + 10, cy - 7, cx + 12, cy)
            eye_path.quadTo(cx + 10, cy + 7, cx, cy + 8)
            eye_path.quadTo(cx - 10, cy + 7, cx - 12, cy)
            painter.drawPath(eye_path)
            
            painter.setBrush(QBrush(color))
            painter.drawEllipse(QPointF(cx, cy), 3.5, 3.5)
            
        else:
            color = QColor("#9ca3af")
            
            if self.underMouse():
                color = QColor("#667eea")
            
            painter.setPen(QPen(color, 2.5, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.setBrush(Qt.NoBrush)
            
            eye_path = QPainterPath()
            eye_path.moveTo(cx - 12, cy)
            eye_path.quadTo(cx - 10, cy - 7, cx, cy - 8)
            eye_path.quadTo(cx + 10, cy - 7, cx + 12, cy)
            eye_path.quadTo(cx + 10, cy + 7, cx, cy + 8)
            eye_path.quadTo(cx - 10, cy + 7, cx - 12, cy)
            painter.drawPath(eye_path)
            
            painter.setBrush(QBrush(color))
            painter.drawEllipse(QPointF(cx, cy), 3.5, 3.5)
            
            painter.setPen(QPen(color, 2.5, Qt.SolidLine, Qt.RoundCap))
            painter.drawLine(int(cx - 14), int(cy - 10), int(cx + 14), int(cy + 10))


class GradientBackground(QWidget):
    def __init__(self):
        super().__init__()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        from PyQt5.QtGui import QLinearGradient
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor("#667eea"))
        gradient.setColorAt(1, QColor("#764ba2"))
        painter.fillRect(self.rect(), gradient)
        
        painter.setPen(QPen(QColor(255, 255, 255, 35), 2))
        painter.setBrush(Qt.NoBrush)
        
        beaker_path = QPainterPath()
        beaker_path.moveTo(70, 100)
        beaker_path.lineTo(70, 200)
        beaker_path.quadTo(70, 220, 90, 220)
        beaker_path.lineTo(170, 220)
        beaker_path.quadTo(190, 220, 190, 200)
        beaker_path.lineTo(190, 100)
        beaker_path.lineTo(180, 100)
        beaker_path.lineTo(180, 200)
        beaker_path.quadTo(180, 210, 170, 210)
        beaker_path.lineTo(90, 210)
        beaker_path.quadTo(80, 210, 80, 200)
        beaker_path.lineTo(80, 100)
        beaker_path.closeSubpath()
        painter.drawPath(beaker_path)
        
        painter.setBrush(QColor(255, 255, 255, 25))
        liquid1 = QPainterPath()
        liquid1.moveTo(80, 150)
        liquid1.lineTo(80, 200)
        liquid1.quadTo(80, 210, 90, 210)
        liquid1.lineTo(170, 210)
        liquid1.quadTo(180, 210, 180, 200)
        liquid1.lineTo(180, 150)
        liquid1.closeSubpath()
        painter.drawPath(liquid1)
        
        painter.setBrush(Qt.NoBrush)
        flask_x = self.width() - 220
        flask_y = 80
        
        flask_path = QPainterPath()
        flask_path.moveTo(flask_x + 40, flask_y)
        flask_path.lineTo(flask_x + 40, flask_y + 40)
        flask_path.lineTo(flask_x + 15, flask_y + 100)
        flask_path.quadTo(flask_x, flask_y + 140, flask_x + 25, flask_y + 155)
        flask_path.lineTo(flask_x + 95, flask_y + 155)
        flask_path.quadTo(flask_x + 120, flask_y + 140, flask_x + 105, flask_y + 100)
        flask_path.lineTo(flask_x + 80, flask_y + 40)
        flask_path.lineTo(flask_x + 80, flask_y)
        flask_path.closeSubpath()
        painter.drawPath(flask_path)
        
        painter.setBrush(QColor(255, 255, 255, 25))
        flask_liquid = QPainterPath()
        flask_liquid.moveTo(flask_x + 20, flask_y + 120)
        flask_liquid.quadTo(flask_x, flask_y + 140, flask_x + 25, flask_y + 155)
        flask_liquid.lineTo(flask_x + 95, flask_y + 155)
        flask_liquid.quadTo(flask_x + 120, flask_y + 140, flask_x + 100, flask_y + 120)
        flask_liquid.closeSubpath()
        painter.drawPath(flask_liquid)
        
        painter.setBrush(Qt.NoBrush)
        tube_x = self.width() - 180
        tube_y = self.height() - 280
        
        tube_path = QPainterPath()
        tube_path.moveTo(tube_x, tube_y)
        tube_path.lineTo(tube_x, tube_y + 170)
        tube_path.quadTo(tube_x, tube_y + 195, tube_x + 25, tube_y + 195)
        tube_path.quadTo(tube_x + 50, tube_y + 195, tube_x + 50, tube_y + 170)
        tube_path.lineTo(tube_x + 50, tube_y)
        tube_path.lineTo(tube_x + 43, tube_y)
        tube_path.lineTo(tube_x + 43, tube_y + 170)
        tube_path.quadTo(tube_x + 43, tube_y + 188, tube_x + 25, tube_y + 188)
        tube_path.quadTo(tube_x + 7, tube_y + 188, tube_x + 7, tube_y + 170)
        tube_path.lineTo(tube_x + 7, tube_y)
        tube_path.closeSubpath()
        painter.drawPath(tube_path)
        
        painter.setBrush(QColor(255, 255, 255, 25))
        tube_liquid = QPainterPath()
        tube_liquid.moveTo(tube_x + 7, tube_y + 110)
        tube_liquid.lineTo(tube_x + 7, tube_y + 170)
        tube_liquid.quadTo(tube_x + 7, tube_y + 188, tube_x + 25, tube_y + 188)
        tube_liquid.quadTo(tube_x + 43, tube_y + 188, tube_x + 43, tube_y + 170)
        tube_liquid.lineTo(tube_x + 43, tube_y + 110)
        tube_liquid.closeSubpath()
        painter.drawPath(tube_liquid)
        
        painter.setBrush(Qt.NoBrush)
        tube2_x = 100
        tube2_y = self.height() - 250
        
        tube2_path = QPainterPath()
        tube2_path.moveTo(tube2_x, tube2_y)
        tube2_path.lineTo(tube2_x, tube2_y + 140)
        tube2_path.quadTo(tube2_x, tube2_y + 160, tube2_x + 20, tube2_y + 160)
        tube2_path.quadTo(tube2_x + 40, tube2_y + 160, tube2_x + 40, tube2_y + 140)
        tube2_path.lineTo(tube2_x + 40, tube2_y)
        tube2_path.lineTo(tube2_x + 34, tube2_y)
        tube2_path.lineTo(tube2_x + 34, tube2_y + 140)
        tube2_path.quadTo(tube2_x + 34, tube2_y + 154, tube2_x + 20, tube2_y + 154)
        tube2_path.quadTo(tube2_x + 6, tube2_y + 154, tube2_x + 6, tube2_y + 140)
        tube2_path.lineTo(tube2_x + 6, tube2_y)
        tube2_path.closeSubpath()
        painter.drawPath(tube2_path)
        
        painter.setBrush(QColor(255, 255, 255, 25))
        tube2_liquid = QPainterPath()
        tube2_liquid.moveTo(tube2_x + 6, tube2_y + 90)
        tube2_liquid.lineTo(tube2_x + 6, tube2_y + 140)
        tube2_liquid.quadTo(tube2_x + 6, tube2_y + 154, tube2_x + 20, tube2_y + 154)
        tube2_liquid.quadTo(tube2_x + 34, tube2_y + 154, tube2_x + 34, tube2_y + 140)
        tube2_liquid.lineTo(tube2_x + 34, tube2_y + 90)
        tube2_liquid.closeSubpath()
        painter.drawPath(tube2_liquid)
        
        painter.setPen(QPen(QColor(255, 255, 255, 45), 2))
        painter.setBrush(QColor(255, 255, 255, 18))
        
        mol_y = self.height() - 180
        painter.drawEllipse(QRectF(50.0, float(mol_y), 28.0, 28.0))
        painter.drawEllipse(QRectF(88.0, float(mol_y - 18), 24.0, 24.0))
        painter.drawEllipse(QRectF(76.0, float(mol_y + 24), 26.0, 26.0))
        
        painter.drawLine(64, mol_y + 12, 88, mol_y - 6)
        painter.drawLine(70, mol_y + 22, 82, mol_y + 32)
        
        mol2_x = self.width() - 120
        mol2_y = int(self.height() / 2)
        
        painter.drawEllipse(QRectF(float(mol2_x), float(mol2_y), 22.0, 22.0))
        painter.drawEllipse(QRectF(float(mol2_x + 30), float(mol2_y + 10), 20.0, 20.0))
        painter.drawEllipse(QRectF(float(mol2_x + 15), float(mol2_y - 25), 24.0, 24.0))
        
        painter.drawLine(mol2_x + 15, mol2_y + 8, mol2_x + 30, mol2_y + 18)
        painter.drawLine(mol2_x + 18, mol2_y, mol2_x + 24, mol2_y - 12)
        
        painter.setBrush(Qt.NoBrush)
        beaker2_y = int(self.height() / 2) - 50
        
        beaker2_path = QPainterPath()
        beaker2_path.moveTo(40, beaker2_y)
        beaker2_path.lineTo(40, beaker2_y + 90)
        beaker2_path.quadTo(40, beaker2_y + 105, 55, beaker2_y + 105)
        beaker2_path.lineTo(115, beaker2_y + 105)
        beaker2_path.quadTo(130, beaker2_y + 105, 130, beaker2_y + 90)
        beaker2_path.lineTo(130, beaker2_y)
        beaker2_path.lineTo(122, beaker2_y)
        beaker2_path.lineTo(122, beaker2_y + 90)
        beaker2_path.quadTo(122, beaker2_y + 97, 115, beaker2_y + 97)
        beaker2_path.lineTo(55, beaker2_y + 97)
        beaker2_path.quadTo(48, beaker2_y + 97, 48, beaker2_y + 90)
        beaker2_path.lineTo(48, beaker2_y)
        beaker2_path.closeSubpath()
        painter.drawPath(beaker2_path)
        
        painter.setBrush(QColor(255, 255, 255, 25))
        liquid2 = QPainterPath()
        liquid2.moveTo(48, beaker2_y + 60)
        liquid2.lineTo(48, beaker2_y + 90)
        liquid2.quadTo(48, beaker2_y + 97, 55, beaker2_y + 97)
        liquid2.lineTo(115, beaker2_y + 97)
        liquid2.quadTo(122, beaker2_y + 97, 122, beaker2_y + 90)
        liquid2.lineTo(122, beaker2_y + 60)
        liquid2.closeSubpath()
        painter.drawPath(liquid2)
        
        painter.setBrush(Qt.NoBrush)
        atom_x = int(self.width() / 2) - 40
        atom_y = 120
        
        painter.setBrush(QColor(255, 255, 255, 30))
        painter.drawEllipse(QRectF(float(atom_x + 35), float(atom_y + 35), 20.0, 20.0))
        
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(QRectF(float(atom_x), float(atom_y), 90.0, 90.0))
        painter.drawEllipse(QRectF(float(atom_x + 15), float(atom_y + 15), 60.0, 60.0))
        
        painter.setBrush(QColor(255, 255, 255, 40))
        painter.drawEllipse(QRectF(float(atom_x + 85), float(atom_y + 40), 10.0, 10.0))
        painter.drawEllipse(QRectF(float(atom_x - 5), float(atom_y + 40), 10.0, 10.0))
        painter.drawEllipse(QRectF(float(atom_x + 65), float(atom_y + 20), 8.0, 8.0))
        painter.drawEllipse(QRectF(float(atom_x + 10), float(atom_y + 55), 8.0, 8.0))


class ModernLineEdit(QLineEdit):
    def __init__(self, placeholder="", is_password=False):
        super().__init__()
        self.setPlaceholderText(placeholder)
        self.is_password = is_password
        self.password_visible = False
        
        if is_password:
            self.setEchoMode(QLineEdit.Password)
            
        self.setMinimumHeight(70)
        self.update_style(False)
        
        if is_password:
            self.toggle_btn = CustomEyeButton(self)
            self.toggle_btn.clicked.connect(self.toggle_password_visibility)
            
    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.is_password:
            self.toggle_btn.move(self.width() - 60, 10)
            
    def toggle_password_visibility(self):
        self.password_visible = not self.password_visible
        if self.password_visible:
            self.setEchoMode(QLineEdit.Normal)
        else:
            self.setEchoMode(QLineEdit.Password)
        self.toggle_btn.set_visible(self.password_visible)
        
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
                    padding: 22px 65px 22px 24px;
                    border: 2px solid #667eea;
                    border-radius: 12px;
                    background: white;
                    font-size: 18px;
                    color: #1f2937;
                    font-family: 'Segoe UI';
                }
            """)
        else:
            self.setStyleSheet("""
                QLineEdit {
                    padding: 22px 65px 22px 24px;
                    border: 2px solid #e5e7eb;
                    border-radius: 12px;
                    background: #f9fafb;
                    font-size: 18px;
                    color: #1f2937;
                    font-family: 'Segoe UI';
                }
                QLineEdit:hover {
                    border: 2px solid #d1d5db;
                    background: white;
                }
            """)


class LoginWindow(QMainWindow):
    login_successful = pyqtSignal(dict)
    
    def __init__(self, api):
        super().__init__()
        self.api = api
        self.setWindowTitle("Chemical Equipment Visualizer")
        self.setMinimumSize(1400, 800)
        self.showMaximized()
        
        central = QWidget()
        self.setCentralWidget(central)
        
        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        left = GradientBackground()
        left_layout = QVBoxLayout(left)
        left_layout.setAlignment(Qt.AlignCenter)
        left_layout.setSpacing(20)
        left_layout.setContentsMargins(60, 60, 60, 60)
        
        title1 = QLabel("CHEMICAL")
        title1.setFont(QFont("Segoe UI", 56, QFont.Bold))
        title1.setStyleSheet("color: rgba(255, 255, 255, 0.98); letter-spacing: 6px; background: transparent;")
        title1.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(title1)
        
        title2 = QLabel("EQUIPMENT")
        title2.setFont(QFont("Segoe UI", 56, QFont.Bold))
        title2.setStyleSheet("color: rgba(255, 255, 255, 0.98); letter-spacing: 6px; background: transparent;")
        title2.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(title2)
        
        title3 = QLabel("VISUALIZER")
        title3.setFont(QFont("Segoe UI", 56, QFont.Bold))
        title3.setStyleSheet("color: rgba(255, 255, 255, 0.98); letter-spacing: 6px; background: transparent;")
        title3.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(title3)
        
        left_layout.addSpacing(15)
        
        subtitle = QLabel("Professional data analysis and visualization platform")
        subtitle.setFont(QFont("Segoe UI", 14))
        subtitle.setStyleSheet("color: rgba(255, 255, 255, 0.80); background: transparent;")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setWordWrap(True)
        left_layout.addWidget(subtitle)
        
        layout.addWidget(left, 60)
        
        right = QWidget()
        right.setStyleSheet("background: #ffffff;")
        right_layout = QVBoxLayout(right)
        right_layout.setAlignment(Qt.AlignCenter)
        right_layout.setContentsMargins(50, 40, 50, 40)
        
        form_container = QWidget()
        form_container.setMinimumWidth(520)
        form_container.setMaximumWidth(620)
        
        form_layout = QVBoxLayout(form_container)
        form_layout.setContentsMargins(0, 0, 0, 0)
        
        self.stack = QStackedWidget()
        self.stack.addWidget(self.create_login_page())
        self.stack.addWidget(self.create_register_page())
        self.stack.addWidget(self.create_verify_page())
        self.stack.addWidget(self.create_forgot_page())
        self.stack.addWidget(self.create_reset_page())
        
        form_layout.addWidget(self.stack)
        
        right_layout.addWidget(form_container)
        layout.addWidget(right, 40)
        
    def create_login_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        
        title = QLabel("Welcome Back")
        title.setFont(QFont("Segoe UI", 40, QFont.Bold))
        title.setStyleSheet("color: #111827;")
        title.setAlignment(Qt.AlignLeft)
        layout.addWidget(title)
        
        layout.addSpacing(10)
        
        subtitle = QLabel("Professional data analysis and visualization")
        subtitle.setFont(QFont("Segoe UI", 15))
        subtitle.setStyleSheet("color: #6b7280;")
        subtitle.setAlignment(Qt.AlignLeft)
        layout.addWidget(subtitle)
        
        layout.addSpacing(45)
        
        tab_widget = QWidget()
        tab_layout = QHBoxLayout(tab_widget)
        tab_layout.setContentsMargins(0, 0, 0, 0)
        tab_layout.setSpacing(0)
        
        self.login_tab_btn = QPushButton("Login")
        self.register_tab_btn = QPushButton("Register")
        
        for btn in [self.login_tab_btn, self.register_tab_btn]:
            btn.setMinimumHeight(52)
            btn.setFont(QFont("Segoe UI", 17, QFont.Bold))
            btn.setCursor(Qt.PointingHandCursor)
            tab_layout.addWidget(btn)
            
        self.login_tab_btn.clicked.connect(lambda: self.switch_tab(0))
        self.register_tab_btn.clicked.connect(lambda: self.switch_tab(1))
        
        self.update_tab_styles(True)
        layout.addWidget(tab_widget)
        
        layout.addSpacing(40)
        
        username_label = QLabel("Username or Email")
        username_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        username_label.setStyleSheet("color: #374151;")
        layout.addWidget(username_label)
        
        layout.addSpacing(12)
        
        self.login_user = ModernLineEdit("Enter your username or email")
        layout.addWidget(self.login_user)
        
        layout.addSpacing(28)
        
        password_label = QLabel("Password")
        password_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        password_label.setStyleSheet("color: #374151;")
        layout.addWidget(password_label)
        
        layout.addSpacing(12)
        
        self.login_pass = ModernLineEdit("Enter your password", is_password=True)
        self.login_pass.returnPressed.connect(self.do_login)
        layout.addWidget(self.login_pass)
        
        layout.addSpacing(14)
        
        forgot_btn = QPushButton("Forgot Password?")
        forgot_btn.setFlat(True)
        forgot_btn.setCursor(Qt.PointingHandCursor)
        forgot_btn.setFont(QFont("Segoe UI", 14, QFont.Bold))
        forgot_btn.setStyleSheet("""
            QPushButton {
                color: #667eea;
                text-align: right;
                padding: 8px;
                border: none;
            }
            QPushButton:hover {
                color: #5568d3;
                text-decoration: underline;
            }
        """)
        forgot_btn.clicked.connect(lambda: self.stack.setCurrentIndex(3))
        layout.addWidget(forgot_btn, 0, Qt.AlignRight)
        
        layout.addSpacing(35)
        
        login_btn = QPushButton("Sign In")
        login_btn.setMinimumHeight(68)
        login_btn.setCursor(Qt.PointingHandCursor)
        login_btn.setFont(QFont("Segoe UI", 18, QFont.Bold))
        login_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                border: none;
                border-radius: 12px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5568d3, stop:1 #6a3f8f);
            }
            QPushButton:pressed {
                background: #4c51bf;
            }
        """)
        login_btn.clicked.connect(self.do_login)
        layout.addWidget(login_btn)
        
        layout.addStretch()
        
        return page
    
    def create_register_page(self):
        page = QWidget()
        main_layout = QVBoxLayout(page)
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
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #d1d5db;
                border-radius: 4px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background: #9ca3af;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)
        
        scroll_content = QWidget()
        layout = QVBoxLayout(scroll_content)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 10, 0)
        
        title = QLabel("Create Account")
        title.setFont(QFont("Segoe UI", 40, QFont.Bold))
        title.setStyleSheet("color: #111827;")
        title.setAlignment(Qt.AlignLeft)
        layout.addWidget(title)
        
        layout.addSpacing(10)
        
        subtitle = QLabel("Sign up to get started with the platform")
        subtitle.setFont(QFont("Segoe UI", 15))
        subtitle.setStyleSheet("color: #6b7280;")
        subtitle.setAlignment(Qt.AlignLeft)
        layout.addWidget(subtitle)
        
        layout.addSpacing(45)
        
        tab_widget = QWidget()
        tab_layout = QHBoxLayout(tab_widget)
        tab_layout.setContentsMargins(0, 0, 0, 0)
        tab_layout.setSpacing(0)
        
        login_tab = QPushButton("Login")
        register_tab = QPushButton("Register")
        
        for btn in [login_tab, register_tab]:
            btn.setMinimumHeight(52)
            btn.setFont(QFont("Segoe UI", 17, QFont.Bold))
            btn.setCursor(Qt.PointingHandCursor)
            tab_layout.addWidget(btn)
            
        login_tab.clicked.connect(lambda: self.switch_tab(0))
        register_tab.clicked.connect(lambda: self.switch_tab(1))
        
        register_tab.setStyleSheet("""
            QPushButton {
                background: white;
                color: #667eea;
                border: none;
                border-bottom: 4px solid #667eea;
            }
        """)
        login_tab.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #9ca3af;
                border: none;
                border-bottom: 4px solid #e5e7eb;
            }
            QPushButton:hover {
                color: #6b7280;
            }
        """)
        
        layout.addWidget(tab_widget)
        
        layout.addSpacing(40)
        
        username_label = QLabel("Username")
        username_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        username_label.setStyleSheet("color: #374151;")
        layout.addWidget(username_label)
        
        layout.addSpacing(12)
        
        self.reg_user = ModernLineEdit("Choose a unique username")
        layout.addWidget(self.reg_user)
        
        layout.addSpacing(25)
        
        email_label = QLabel("Email Address")
        email_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        email_label.setStyleSheet("color: #374151;")
        layout.addWidget(email_label)
        
        layout.addSpacing(12)
        
        self.reg_email = ModernLineEdit("Enter your email address")
        layout.addWidget(self.reg_email)
        
        layout.addSpacing(25)
        
        password_label = QLabel("Password")
        password_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        password_label.setStyleSheet("color: #374151;")
        layout.addWidget(password_label)
        
        layout.addSpacing(12)
        
        self.reg_pass = ModernLineEdit("Create a strong password", is_password=True)
        self.reg_pass.textChanged.connect(self.update_register_strength)
        layout.addWidget(self.reg_pass)
        
        layout.addSpacing(10)
        
        hint = QLabel("Must be 8+ characters with uppercase, number, and special character")
        hint.setFont(QFont("Segoe UI", 11))
        hint.setStyleSheet("color: #9ca3af;")
        hint.setWordWrap(True)
        layout.addWidget(hint)
        
        layout.addSpacing(10)
        
        self.reg_strength = PasswordStrengthWidget()
        layout.addWidget(self.reg_strength)
        
        layout.addSpacing(32)
        
        register_btn = QPushButton("Create Account")
        register_btn.setMinimumHeight(68)
        register_btn.setCursor(Qt.PointingHandCursor)
        register_btn.setFont(QFont("Segoe UI", 18, QFont.Bold))
        register_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #10b981, stop:1 #059669);
                color: white;
                border: none;
                border-radius: 12px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #059669, stop:1 #047857);
            }
        """)
        register_btn.clicked.connect(self.do_register)
        layout.addWidget(register_btn)
        
        layout.addSpacing(20)
        
        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)
        
        return page
    
    def create_verify_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(0, 30, 0, 0)
        
        icon_box = QWidget()
        icon_box.setFixedSize(110, 110)
        icon_box.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 55px;
            }
        """)
        icon_layout = QVBoxLayout(icon_box)
        icon_label = QLabel("@")
        icon_label.setFont(QFont("Segoe UI", 52, QFont.Bold))
        icon_label.setStyleSheet("color: white; background: transparent;")
        icon_label.setAlignment(Qt.AlignCenter)
        icon_layout.addWidget(icon_label)
        
        icon_container = QHBoxLayout()
        icon_container.addStretch()
        icon_container.addWidget(icon_box)
        icon_container.addStretch()
        layout.addLayout(icon_container)
        
        layout.addSpacing(28)
        
        title = QLabel("Verify Your Email")
        title.setFont(QFont("Segoe UI", 36, QFont.Bold))
        title.setStyleSheet("color: #111827;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        layout.addSpacing(14)
        
        subtitle = QLabel("We've sent a 6-digit verification code to your email address.\nPlease enter it below to verify your account.")
        subtitle.setFont(QFont("Segoe UI", 14))
        subtitle.setStyleSheet("color: #6b7280; line-height: 1.6;")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setWordWrap(True)
        layout.addWidget(subtitle)
        
        layout.addSpacing(40)
        
        code_label = QLabel("Verification Code")
        code_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        code_label.setStyleSheet("color: #374151;")
        layout.addWidget(code_label)
        
        layout.addSpacing(12)
        
        self.verify_code = ModernLineEdit("Enter 6-digit code")
        self.verify_code.setMaxLength(6)
        self.verify_code.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.verify_code)
        
        layout.addSpacing(35)
        
        verify_btn = QPushButton("Verify Email")
        verify_btn.setMinimumHeight(68)
        verify_btn.setCursor(Qt.PointingHandCursor)
        verify_btn.setFont(QFont("Segoe UI", 18, QFont.Bold))
        verify_btn.setStyleSheet("""
            QPushButton {
                background: #667eea;
                color: white;
                border: none;
                border-radius: 12px;
            }
            QPushButton:hover {
                background: #5568d3;
            }
        """)
        verify_btn.clicked.connect(self.do_verify)
        layout.addWidget(verify_btn)
        
        layout.addSpacing(20)
        
        back_btn = QPushButton("Back to Login")
        back_btn.setFlat(True)
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setFont(QFont("Segoe UI", 14, QFont.Bold))
        back_btn.setStyleSheet("""
            QPushButton {
                color: #667eea;
                padding: 10px;
            }
            QPushButton:hover {
                color: #5568d3;
            }
        """)
        back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        layout.addWidget(back_btn, 0, Qt.AlignCenter)
        
        layout.addStretch()
        
        return page
    
    def create_forgot_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(0, 30, 0, 0)
        
        icon_box = QWidget()
        icon_box.setFixedSize(110, 110)
        icon_box.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 55px;
            }
        """)
        icon_layout = QVBoxLayout(icon_box)
        icon_label = QLabel("?")
        icon_label.setFont(QFont("Segoe UI", 52, QFont.Bold))
        icon_label.setStyleSheet("color: white; background: transparent;")
        icon_label.setAlignment(Qt.AlignCenter)
        icon_layout.addWidget(icon_label)
        
        icon_container = QHBoxLayout()
        icon_container.addStretch()
        icon_container.addWidget(icon_box)
        icon_container.addStretch()
        layout.addLayout(icon_container)
        
        layout.addSpacing(28)
        
        title = QLabel("Forgot Password?")
        title.setFont(QFont("Segoe UI", 36, QFont.Bold))
        title.setStyleSheet("color: #111827;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        layout.addSpacing(14)
        
        subtitle = QLabel("No worries! Enter your email address and we'll send you\na code to reset your password.")
        subtitle.setFont(QFont("Segoe UI", 14))
        subtitle.setStyleSheet("color: #6b7280; line-height: 1.6;")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setWordWrap(True)
        layout.addWidget(subtitle)
        
        layout.addSpacing(40)
        
        email_label = QLabel("Email Address")
        email_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        email_label.setStyleSheet("color: #374151;")
        layout.addWidget(email_label)
        
        layout.addSpacing(12)
        
        self.forgot_email = ModernLineEdit("Enter your registered email address")
        layout.addWidget(self.forgot_email)
        
        layout.addSpacing(35)
        
        send_btn = QPushButton("Send Reset Code")
        send_btn.setMinimumHeight(68)
        send_btn.setCursor(Qt.PointingHandCursor)
        send_btn.setFont(QFont("Segoe UI", 18, QFont.Bold))
        send_btn.setStyleSheet("""
            QPushButton {
                background: #667eea;
                color: white;
                border: none;
                border-radius: 12px;
            }
            QPushButton:hover {
                background: #5568d3;
            }
        """)
        send_btn.clicked.connect(self.do_forgot_password)
        layout.addWidget(send_btn)
        
        layout.addSpacing(20)
        
        back_btn = QPushButton("Back to Login")
        back_btn.setFlat(True)
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setFont(QFont("Segoe UI", 14, QFont.Bold))
        back_btn.setStyleSheet("""
            QPushButton {
                color: #667eea;
                padding: 10px;
            }
            QPushButton:hover {
                color: #5568d3;
            }
        """)
        back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        layout.addWidget(back_btn, 0, Qt.AlignCenter)
        
        layout.addStretch()
        
        return page
    
    def create_reset_page(self):
        page = QWidget()
        main_layout = QVBoxLayout(page)
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
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #d1d5db;
                border-radius: 4px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background: #9ca3af;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)
        
        scroll_content = QWidget()
        layout = QVBoxLayout(scroll_content)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 20, 10, 0)
        
        title = QLabel("Reset Password")
        title.setFont(QFont("Segoe UI", 40, QFont.Bold))
        title.setStyleSheet("color: #111827;")
        title.setAlignment(Qt.AlignLeft)
        layout.addWidget(title)
        
        layout.addSpacing(10)
        
        subtitle = QLabel("Enter the verification code and your new password")
        subtitle.setFont(QFont("Segoe UI", 15))
        subtitle.setStyleSheet("color: #6b7280;")
        subtitle.setAlignment(Qt.AlignLeft)
        layout.addWidget(subtitle)
        
        layout.addSpacing(40)
        
        code_label = QLabel("Reset Code")
        code_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        code_label.setStyleSheet("color: #374151;")
        layout.addWidget(code_label)
        
        layout.addSpacing(12)
        
        self.reset_code = ModernLineEdit("Enter 6-digit reset code")
        self.reset_code.setMaxLength(6)
        layout.addWidget(self.reset_code)
        
        layout.addSpacing(25)
        
        password_label = QLabel("New Password")
        password_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        password_label.setStyleSheet("color: #374151;")
        layout.addWidget(password_label)
        
        layout.addSpacing(12)
        
        self.reset_pass = ModernLineEdit("Enter your new password", is_password=True)
        self.reset_pass.textChanged.connect(self.update_reset_strength)
        layout.addWidget(self.reset_pass)
        
        layout.addSpacing(10)
        
        hint = QLabel("Must be 8+ characters with uppercase, number, and special character")
        hint.setFont(QFont("Segoe UI", 11))
        hint.setStyleSheet("color: #9ca3af;")
        hint.setWordWrap(True)
        layout.addWidget(hint)
        
        layout.addSpacing(10)
        
        self.reset_strength = PasswordStrengthWidget()
        layout.addWidget(self.reset_strength)
        
        layout.addSpacing(32)
        
        reset_btn = QPushButton("Reset Password")
        reset_btn.setMinimumHeight(68)
        reset_btn.setCursor(Qt.PointingHandCursor)
        reset_btn.setFont(QFont("Segoe UI", 18, QFont.Bold))
        reset_btn.setStyleSheet("""
            QPushButton {
                background: #667eea;
                color: white;
                border: none;
                border-radius: 12px;
            }
            QPushButton:hover {
                background: #5568d3;
            }
        """)
        reset_btn.clicked.connect(self.do_reset_password)
        layout.addWidget(reset_btn)
        
        layout.addSpacing(20)
        
        back_btn = QPushButton("Back to Login")
        back_btn.setFlat(True)
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setFont(QFont("Segoe UI", 14, QFont.Bold))
        back_btn.setStyleSheet("""
            QPushButton {
                color: #667eea;
                padding: 10px;
            }
            QPushButton:hover {
                color: #5568d3;
            }
        """)
        back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        layout.addWidget(back_btn, 0, Qt.AlignCenter)
        
        layout.addSpacing(20)
        
        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)
        
        return page
    
    def switch_tab(self, index):
        self.stack.setCurrentIndex(index)
        self.update_tab_styles(index == 0)
    
    def update_tab_styles(self, login_active):
        if login_active:
            self.login_tab_btn.setStyleSheet("""
                QPushButton {
                    background: white;
                    color: #667eea;
                    border: none;
                    border-bottom: 4px solid #667eea;
                }
            """)
            self.register_tab_btn.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    color: #9ca3af;
                    border: none;
                    border-bottom: 4px solid #e5e7eb;
                }
                QPushButton:hover {
                    color: #6b7280;
                }
            """)
        else:
            self.register_tab_btn.setStyleSheet("""
                QPushButton {
                    background: white;
                    color: #667eea;
                    border: none;
                    border-bottom: 4px solid #667eea;
                }
            """)
            self.login_tab_btn.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    color: #9ca3af;
                    border: none;
                    border-bottom: 4px solid #e5e7eb;
                }
                QPushButton:hover {
                    color: #6b7280;
                }
            """)
    
    def update_register_strength(self, text):
        self.reg_strength.set_strength(text)
    
    def update_reset_strength(self, text):
        self.reset_strength.set_strength(text)
    
    def show_message(self, title, message, msg_type="info"):
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(message)
        
        if msg_type == "error":
            msg.setIcon(QMessageBox.Critical)
        elif msg_type == "success":
            msg.setIcon(QMessageBox.Information)
        elif msg_type == "warning":
            msg.setIcon(QMessageBox.Warning)
        else:
            msg.setIcon(QMessageBox.Information)
            
        msg.exec_()
    
    def do_login(self):
        user = self.login_user.text().strip()
        pwd = self.login_pass.text()
        
        if not user or not pwd:
            self.show_message("Error", "Enter username and password", "warning")
            return
        
        print("Attempting login...")
        success, result = self.api.login(user, pwd)
        
        if success:
            print("Login API call successful, emitting signal...")
            self.login_successful.emit(result['user'])
        else:
            print("Login failed: {}".format(result))
            self.show_message("Login Failed", str(result), "error")
    
    def do_register(self):
        user = self.reg_user.text().strip()
        email = self.reg_email.text().strip()
        pwd = self.reg_pass.text()
        
        if not user or not email or not pwd:
            self.show_message("Error", "All fields required", "warning")
            return
        
        success, result = self.api.register(user, email, pwd)
        
        if success:
            self.registered_username = user
            self.stack.setCurrentIndex(2)
            self.show_message("Success", "Verification code sent to your email", "success")
        else:
            self.show_message("Error", str(result), "error")
    
    def do_verify(self):
        code = self.verify_code.text().strip()
        
        if not code:
            self.show_message("Error", "Enter verification code", "warning")
            return
        
        if not hasattr(self, 'registered_username'):
            self.show_message("Error", "No username found", "error")
            return
        
        success, result = self.api.verify_email(self.registered_username, code)
        
        if success:
            self.show_message("Success", "Account verified! You can now login.", "success")
            self.stack.setCurrentIndex(0)
            self.verify_code.clear()
        else:
            self.show_message("Error", str(result), "error")
    
    def do_forgot_password(self):
        email = self.forgot_email.text().strip()
        
        if not email:
            self.show_message("Error", "Enter your email address", "warning")
            return
        
        self.reset_email = email
        self.show_message("Success", "If the email exists, a reset code has been sent", "success")
        self.stack.setCurrentIndex(4)
    
    def do_reset_password(self):
        code = self.reset_code.text().strip()
        new_pwd = self.reset_pass.text()
        
        if not code or not new_pwd:
            self.show_message("Error", "All fields required", "warning")
            return
        
        if not hasattr(self, 'reset_email'):
            self.show_message("Error", "No email found", "error")
            return
        
        self.show_message("Success", "Password reset successful! You can now login.", "success")
        self.stack.setCurrentIndex(0)
        self.reset_code.clear()
        self.reset_pass.clear()