from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTimer, QRectF, QPointF
from PyQt5.QtGui import QFont, QColor, QPainter, QPen, QPainterPath, QLinearGradient
import math

class LogoWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(200)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor("#667eea"))
        gradient.setColorAt(1, QColor("#764ba2"))
        painter.fillRect(self.rect(), gradient)
        
        painter.setPen(QPen(QColor(255, 255, 255, 220), 4))
        
        w = self.width()
        h = self.height()
        
        painter.setBrush(Qt.NoBrush)
        painter.save()
        flask1_x = 25
        flask1_y = 25
        
        painter.translate(flask1_x + 25, flask1_y + 35)
        painter.rotate(-12)
        painter.translate(-(flask1_x + 25), -(flask1_y + 35))
        
        flask1 = QPainterPath()
        flask1.moveTo(flask1_x + 20, flask1_y)
        flask1.lineTo(flask1_x + 20, flask1_y + 18)
        flask1.lineTo(flask1_x + 6, flask1_y + 48)
        flask1.quadTo(flask1_x, flask1_y + 62, flask1_x + 12, flask1_y + 70)
        flask1.lineTo(flask1_x + 38, flask1_y + 70)
        flask1.quadTo(flask1_x + 50, flask1_y + 62, flask1_x + 44, flask1_y + 48)
        flask1.lineTo(flask1_x + 30, flask1_y + 18)
        flask1.lineTo(flask1_x + 30, flask1_y)
        painter.drawPath(flask1)
        
        painter.setBrush(QColor(255, 255, 255, 80))
        flask1_liquid = QPainterPath()
        flask1_liquid.moveTo(flask1_x + 10, flask1_y + 54)
        flask1_liquid.quadTo(flask1_x, flask1_y + 62, flask1_x + 12, flask1_y + 70)
        flask1_liquid.lineTo(flask1_x + 38, flask1_y + 70)
        flask1_liquid.quadTo(flask1_x + 50, flask1_y + 62, flask1_x + 40, flask1_y + 54)
        flask1_liquid.closeSubpath()
        painter.drawPath(flask1_liquid)
        
        painter.restore()
        
        painter.setBrush(Qt.NoBrush)
        flask2_x = w / 2 - 20
        flask2_y = 15
        
        flask2 = QPainterPath()
        flask2.moveTo(flask2_x + 15, flask2_y)
        flask2.lineTo(flask2_x + 15, flask2_y + 25)
        flask2.lineTo(flask2_x + 25, flask2_y + 25)
        flask2.lineTo(flask2_x + 25, flask2_y)
        flask2.moveTo(flask2_x + 10, flask2_y + 25)
        flask2.lineTo(flask2_x + 30, flask2_y + 25)
        flask2.quadTo(flask2_x + 38, flask2_y + 35, flask2_x + 38, flask2_y + 50)
        flask2.quadTo(flask2_x + 38, flask2_y + 65, flask2_x + 20, flask2_y + 68)
        flask2.quadTo(flask2_x + 2, flask2_y + 65, flask2_x + 2, flask2_y + 50)
        flask2.quadTo(flask2_x + 2, flask2_y + 35, flask2_x + 10, flask2_y + 25)
        painter.drawPath(flask2)
        
        painter.setBrush(QColor(255, 255, 255, 80))
        flask2_liquid = QPainterPath()
        flask2_liquid.moveTo(flask2_x + 10, flask2_y + 45)
        flask2_liquid.quadTo(flask2_x + 5, flask2_y + 58, flask2_x + 20, flask2_y + 65)
        flask2_liquid.quadTo(flask2_x + 35, flask2_y + 58, flask2_x + 30, flask2_y + 45)
        flask2_liquid.closeSubpath()
        painter.drawPath(flask2_liquid)
        
        painter.setBrush(Qt.NoBrush)
        beaker_x = w - 75
        beaker_y = 20
        
        beaker = QPainterPath()
        beaker.moveTo(beaker_x, beaker_y)
        beaker.lineTo(beaker_x, beaker_y + 60)
        beaker.quadTo(beaker_x, beaker_y + 72, beaker_x + 10, beaker_y + 72)
        beaker.lineTo(beaker_x + 45, beaker_y + 72)
        beaker.quadTo(beaker_x + 55, beaker_y + 72, beaker_x + 55, beaker_y + 60)
        beaker.lineTo(beaker_x + 55, beaker_y)
        painter.drawPath(beaker)
        
        painter.drawLine(beaker_x + 5, beaker_y + 20, beaker_x + 15, beaker_y + 20)
        painter.drawLine(beaker_x + 5, beaker_y + 40, beaker_x + 15, beaker_y + 40)
        
        painter.setBrush(QColor(255, 255, 255, 80))
        beaker_liquid = QPainterPath()
        beaker_liquid.moveTo(beaker_x + 4, beaker_y + 35)
        beaker_liquid.lineTo(beaker_x + 4, beaker_y + 60)
        beaker_liquid.quadTo(beaker_x + 4, beaker_y + 68, beaker_x + 10, beaker_y + 68)
        beaker_liquid.lineTo(beaker_x + 45, beaker_y + 68)
        beaker_liquid.quadTo(beaker_x + 51, beaker_y + 68, beaker_x + 51, beaker_y + 60)
        beaker_liquid.lineTo(beaker_x + 51, beaker_y + 35)
        beaker_liquid.closeSubpath()
        painter.drawPath(beaker_liquid)
        
        painter.setBrush(Qt.NoBrush)
        painter.save()
        tube1_x = 30
        tube1_y = 115
        
        painter.translate(tube1_x + 9, tube1_y + 35)
        painter.rotate(15)
        painter.translate(-(tube1_x + 9), -(tube1_y + 35))
        
        tube1 = QPainterPath()
        tube1.moveTo(tube1_x, tube1_y)
        tube1.lineTo(tube1_x, tube1_y + 58)
        tube1.quadTo(tube1_x, tube1_y + 70, tube1_x + 9, tube1_y + 70)
        tube1.quadTo(tube1_x + 18, tube1_y + 70, tube1_x + 18, tube1_y + 58)
        tube1.lineTo(tube1_x + 18, tube1_y)
        painter.drawPath(tube1)
        
        painter.setBrush(QColor(255, 255, 255, 80))
        tube1_liquid = QPainterPath()
        tube1_liquid.moveTo(tube1_x + 3, tube1_y + 30)
        tube1_liquid.lineTo(tube1_x + 3, tube1_y + 58)
        tube1_liquid.quadTo(tube1_x + 3, tube1_y + 67, tube1_x + 9, tube1_y + 67)
        tube1_liquid.quadTo(tube1_x + 15, tube1_y + 67, tube1_x + 15, tube1_y + 58)
        tube1_liquid.lineTo(tube1_x + 15, tube1_y + 30)
        tube1_liquid.closeSubpath()
        painter.drawPath(tube1_liquid)
        
        painter.restore()
        
        painter.setPen(QPen(QColor(255, 255, 255, 200), 3))
        painter.setBrush(QColor(255, 255, 255, 60))
        
        mol_x = w / 2 - 30
        mol_y = 125
        
        painter.drawEllipse(QRectF(float(mol_x + 20), float(mol_y + 20), 20.0, 20.0))
        
        painter.drawEllipse(QRectF(float(mol_x), float(mol_y), 16.0, 16.0))
        painter.drawEllipse(QRectF(float(mol_x + 44), float(mol_y + 5), 14.0, 14.0))
        painter.drawEllipse(QRectF(float(mol_x + 10), float(mol_y + 44), 15.0, 15.0))
        painter.drawEllipse(QRectF(float(mol_x + 38), float(mol_y + 40), 13.0, 13.0))
        
        painter.drawLine(int(mol_x + 12), int(mol_y + 12), int(mol_x + 24), int(mol_y + 24))
        painter.drawLine(int(mol_x + 36), int(mol_y + 28), int(mol_x + 46), int(mol_y + 16))
        painter.drawLine(int(mol_x + 22), int(mol_y + 38), int(mol_x + 20), int(mol_y + 48))
        painter.drawLine(int(mol_x + 38), int(mol_y + 34), int(mol_x + 42), int(mol_y + 42))
        
        painter.setPen(QPen(QColor(255, 255, 255, 220), 4))
        painter.setBrush(Qt.NoBrush)
        painter.save()
        
        conical_x = w - 70
        conical_y = 120
        
        painter.translate(conical_x + 22, conical_y + 35)
        painter.rotate(-10)
        painter.translate(-(conical_x + 22), -(conical_y + 35))
        
        conical = QPainterPath()
        conical.moveTo(conical_x + 18, conical_y)
        conical.lineTo(conical_x + 18, conical_y + 15)
        conical.lineTo(conical_x + 4, conical_y + 50)
        conical.lineTo(conical_x + 4, conical_y + 60)
        conical.quadTo(conical_x + 4, conical_y + 68, conical_x + 12, conical_y + 68)
        conical.lineTo(conical_x + 32, conical_y + 68)
        conical.quadTo(conical_x + 40, conical_y + 68, conical_x + 40, conical_y + 60)
        conical.lineTo(conical_x + 40, conical_y + 50)
        conical.lineTo(conical_x + 26, conical_y + 15)
        conical.lineTo(conical_x + 26, conical_y)
        painter.drawPath(conical)
        
        painter.setBrush(QColor(255, 255, 255, 80))
        conical_liquid = QPainterPath()
        conical_liquid.moveTo(conical_x + 8, conical_y + 55)
        conical_liquid.lineTo(conical_x + 8, conical_y + 60)
        conical_liquid.quadTo(conical_x + 8, conical_y + 65, conical_x + 12, conical_y + 65)
        conical_liquid.lineTo(conical_x + 32, conical_y + 65)
        conical_liquid.quadTo(conical_x + 36, conical_y + 65, conical_x + 36, conical_y + 60)
        conical_liquid.lineTo(conical_x + 36, conical_y + 55)
        conical_liquid.closeSubpath()
        painter.drawPath(conical_liquid)
        
        painter.restore()


class SidebarButton(QPushButton):
    def __init__(self, text):
        super().__init__()
        self.main_text = text
        self.setText(f"   {text}")
        self.setCheckable(True)
        self.setMinimumHeight(54)
        self.setMaximumHeight(54)
        self.setCursor(Qt.PointingHandCursor)
        
        button_font = QFont("Segoe UI", 17, QFont.Bold)
        self.setFont(button_font)
        
        self.update_style(False)
    
    def update_style(self, checked):
        if checked:
            self.setStyleSheet("""
                QPushButton {
                    text-align: left;
                    padding: 16px 20px;
                    border: none;
                    color: white;
                    font-weight: bold;
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #667eea, stop:1 #764ba2);
                    border-left: 5px solid #10b981;
                    border-radius: 0px;
                    min-height: 54px;
                    max-height: 54px;
                }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    text-align: left;
                    padding: 16px 20px;
                    border: none;
                    color: #bdc3c7;
                    font-weight: bold;
                    background: transparent;
                    border-left: 5px solid transparent;
                    min-height: 54px;
                    max-height: 54px;
                }
                QPushButton:hover {
                    background: rgba(52, 73, 94, 0.8);
                    color: white;
                    border-left: 5px solid #667eea;
                }
            """)


class MainWindow(QMainWindow):
    def __init__(self, api, user):
        super().__init__()
        self.api = api
        self.user = user
        self.current_dataset_id = None
        
        self.setWindowTitle("Chemical Equipment Visualizer")
        self.showMaximized()
        
        print("Creating main window widgets...")
        
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar)
        
        self.stack = QStackedWidget()
        self.stack.setStyleSheet("""
            QStackedWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
            }
        """)
        
        main_layout.addWidget(self.stack)
        
        print("Main window widgets created")
        
        loading = QLabel("Loading application...")
        loading.setAlignment(Qt.AlignCenter)
        loading.setFont(QFont("Segoe UI", 28, QFont.Bold))
        loading.setStyleSheet("color: #667eea; background: transparent;")
        self.stack.addWidget(loading)
        
        print("Main window layout complete")
        
        self.dashboard = None
        self.data_table = None
        self.charts = None
        self.history = None
        
        QTimer.singleShot(100, self.load_widgets)
    
    def load_widgets(self):
        print("Loading widgets...")
        
        while self.stack.count() > 0:
            widget = self.stack.widget(0)
            self.stack.removeWidget(widget)
            widget.deleteLater()
        
        try:
            from ui.dashboard_widget import DashboardWidget
            print("  Dashboard imported")
            self.dashboard = DashboardWidget(self.api)
            self.stack.addWidget(self.dashboard)
            print("  Dashboard loaded")
        except Exception as e:
            print("  ERROR loading Dashboard: {}".format(str(e)))
            import traceback
            traceback.print_exc()
            error_widget = QLabel("Dashboard failed to load")
            error_widget.setAlignment(Qt.AlignCenter)
            error_widget.setFont(QFont("Segoe UI", 18))
            error_widget.setStyleSheet("color: #e74c3c; background: transparent;")
            self.stack.addWidget(error_widget)
        
        try:
            from ui.data_table_widget import DataTableWidget
            print("  DataTable imported")
            self.data_table = DataTableWidget(self.api)
            self.stack.addWidget(self.data_table)
            print("  DataTable loaded")
        except Exception as e:
            print("  ERROR loading DataTable: {}".format(str(e)))
            import traceback
            traceback.print_exc()
            error_widget = QLabel("Data Table failed to load")
            error_widget.setAlignment(Qt.AlignCenter)
            error_widget.setFont(QFont("Segoe UI", 18))
            error_widget.setStyleSheet("color: #e74c3c; background: transparent;")
            self.stack.addWidget(error_widget)
        
        try:
            from ui.charts_widget import ChartsWidget
            print("  Charts imported")
            self.charts = ChartsWidget(self.api)
            self.stack.addWidget(self.charts)
            print("  Charts loaded")
        except Exception as e:
            print("  ERROR loading Charts: {}".format(str(e)))
            import traceback
            traceback.print_exc()
            error_widget = QLabel("Charts failed to load")
            error_widget.setAlignment(Qt.AlignCenter)
            error_widget.setFont(QFont("Segoe UI", 18))
            error_widget.setStyleSheet("color: #e74c3c; background: transparent;")
            self.stack.addWidget(error_widget)
        
        try:
            from ui.history_widget import HistoryWidget
            print("  History imported")
            self.history = HistoryWidget(self.api)
            self.stack.addWidget(self.history)
            print("  History loaded")
        except Exception as e:
            print("  ERROR loading History: {}".format(str(e)))
            import traceback
            traceback.print_exc()
            error_widget = QLabel("History failed to load")
            error_widget.setAlignment(Qt.AlignCenter)
            error_widget.setFont(QFont("Segoe UI", 18))
            error_widget.setStyleSheet("color: #e74c3c; background: transparent;")
            self.stack.addWidget(error_widget)
        
        try:
            if self.dashboard:
                self.dashboard.dataset_uploaded.connect(self.on_dataset_uploaded)
            if self.history:
                self.history.dataset_selected.connect(self.on_dataset_selected)
            
            self.stack.setCurrentIndex(0)
            
            if self.history:
                self.history.load_history()
            
            print("All widgets loaded successfully!")
        except Exception as e:
            print("ERROR connecting signals: {}".format(str(e)))
            import traceback
            traceback.print_exc()
    
    def create_sidebar(self):
        sidebar = QWidget()
        sidebar.setFixedWidth(300)
        sidebar.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2c3e50, stop:1 #1a252f);
            }
        """)
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        logo_widget = LogoWidget()
        layout.addWidget(logo_widget)
        
        user_info = QWidget()
        user_info.setStyleSheet("""
            QWidget {
                background: rgba(52, 73, 94, 0.6);
                padding: 18px;
                border-bottom: 2px solid rgba(255, 255, 255, 0.1);
            }
        """)
        user_layout = QVBoxLayout(user_info)
        user_layout.setSpacing(6)
        
        user_label = QLabel("LOGGED IN AS")
        user_label.setFont(QFont("Segoe UI", 9, QFont.Bold))
        user_label.setStyleSheet("color: #95a5a6; background: transparent; letter-spacing: 1px;")
        user_layout.addWidget(user_label)
        
        username = QLabel(self.user.get('username', 'User'))
        username.setFont(QFont("Segoe UI", 16, QFont.Bold))
        username.setStyleSheet("color: #ecf0f1; background: transparent;")
        user_layout.addWidget(username)
        
        layout.addWidget(user_info)
        
        layout.addSpacing(20)
        
        nav_label = QLabel("  NAVIGATION")
        nav_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        nav_label.setStyleSheet("color: #7f8c8d; background: transparent; padding: 8px; letter-spacing: 1px;")
        layout.addWidget(nav_label)
        
        layout.addSpacing(5)
        
        self.nav_buttons = []
        
        dash_btn = SidebarButton("Dashboard")
        dash_btn.setChecked(True)
        dash_btn.clicked.connect(lambda: self.switch_page(0))
        layout.addWidget(dash_btn)
        self.nav_buttons.append(dash_btn)
        
        layout.addSpacing(10)
        
        table_btn = SidebarButton("Data Table")
        table_btn.clicked.connect(lambda: self.switch_page(1))
        layout.addWidget(table_btn)
        self.nav_buttons.append(table_btn)
        
        layout.addSpacing(10)
        
        charts_btn = SidebarButton("Charts")
        charts_btn.clicked.connect(lambda: self.switch_page(2))
        layout.addWidget(charts_btn)
        self.nav_buttons.append(charts_btn)
        
        layout.addSpacing(10)
        
        history_btn = SidebarButton("History")
        history_btn.clicked.connect(lambda: self.switch_page(3))
        layout.addWidget(history_btn)
        self.nav_buttons.append(history_btn)
        
        layout.addStretch()
        
        logout_container = QWidget()
        logout_container.setStyleSheet("background: transparent;")
        logout_layout = QVBoxLayout(logout_container)
        logout_layout.setContentsMargins(15, 15, 15, 20)
        
        logout_btn = QPushButton("Logout")
        logout_btn.setFont(QFont("Segoe UI", 17, QFont.Bold))
        logout_btn.setMinimumHeight(54)
        logout_btn.setMaximumHeight(54)
        logout_btn.setCursor(Qt.PointingHandCursor)
        logout_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #e74c3c, stop:1 #c0392b);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px 20px;
                font-weight: bold;
                min-height: 54px;
                max-height: 54px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #c0392b, stop:1 #a93226);
            }
            QPushButton:pressed {
                background: #922b21;
            }
        """)
        logout_btn.clicked.connect(self.do_logout)
        logout_layout.addWidget(logout_btn)
        
        layout.addWidget(logout_container)
        
        return sidebar
    
    def switch_page(self, index):
        if self.stack.count() > index:
            self.stack.setCurrentIndex(index)
            for i, btn in enumerate(self.nav_buttons):
                is_active = i == index
                btn.setChecked(is_active)
                btn.update_style(is_active)
    
    def on_dataset_uploaded(self, result):
        if not self.data_table or not self.charts or not self.history:
            return
        
        dataset = result.get('dataset', {})
        self.current_dataset_id = dataset.get('id')
        
        if self.current_dataset_id:
            self.data_table.load_dataset(self.current_dataset_id)
            self.charts.load_dataset(self.current_dataset_id)
            self.history.load_history()
    
    def on_dataset_selected(self, dataset_id):
        if not self.dashboard or not self.data_table or not self.charts:
            return
        
        self.current_dataset_id = dataset_id
        self.dashboard.load_dataset(dataset_id)
        self.data_table.load_dataset(dataset_id)
        self.charts.load_dataset(dataset_id)
        self.switch_page(0)
    
    def do_logout(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Confirm Logout")
        msg.setText("Are you sure you want to logout?")
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        
        yes_btn = msg.button(QMessageBox.Yes)
        yes_btn.setStyleSheet("""
            QPushButton {
                background: #e74c3c;
                color: white;
                padding: 8px 20px;
                border-radius: 5px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background: #c0392b;
            }
        """)
        
        no_btn = msg.button(QMessageBox.No)
        no_btn.setStyleSheet("""
            QPushButton {
                background: #95a5a6;
                color: white;
                padding: 8px 20px;
                border-radius: 5px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background: #7f8c8d;
            }
        """)
        
        reply = msg.exec_()
        
        if reply == QMessageBox.Yes:
            self.api.logout()
            QApplication.quit()
    
    def closeEvent(self, event):
        msg = QMessageBox(self)
        msg.setWindowTitle("Confirm Exit")
        msg.setText("Are you sure you want to exit the application?")
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        
        yes_btn = msg.button(QMessageBox.Yes)
        yes_btn.setStyleSheet("""
            QPushButton {
                background: #e74c3c;
                color: white;
                padding: 8px 20px;
                border-radius: 5px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background: #c0392b;
            }
        """)
        
        no_btn = msg.button(QMessageBox.No)
        no_btn.setStyleSheet("""
            QPushButton {
                background: #95a5a6;
                color: white;
                padding: 8px 20px;
                border-radius: 5px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background: #7f8c8d;
            }
        """)
        
        reply = msg.exec_()
        
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()