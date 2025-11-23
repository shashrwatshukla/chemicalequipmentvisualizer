from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal, QRectF, QTimer, QPointF, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt5.QtGui import (QFont, QColor, QPainter, QPainterPath, QLinearGradient, 
                         QRadialGradient, QPen, QBrush, QPolygonF)
import math
import random

def add_soft_shadow(widget, radius=20, opacity=100, offset=(0, 5)):
    shadow = QGraphicsDropShadowEffect(widget)
    shadow.setBlurRadius(radius)
    shadow.setColor(QColor(0, 0, 0, opacity))
    shadow.setOffset(*offset)
    widget.setGraphicsEffect(shadow)

class ChemicalFlaskWidget(QWidget):
    def __init__(self, color="#ffffff", parent=None):
        super().__init__(parent)
        self.color = QColor(color)
        self.setFixedSize(70, 85)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        path = QPainterPath()
        path.moveTo(27, 8)
        path.lineTo(27, 27)
        path.lineTo(17, 39)
        path.lineTo(17, 66)
        path.quadTo(17, 78, 35, 78)
        path.lineTo(53, 78)
        path.quadTo(53, 78, 53, 66)
        path.lineTo(53, 39)
        path.lineTo(43, 27)
        path.lineTo(43, 8)
        path.closeSubpath()
        
        painter.setPen(QPen(self.color, 2.5))
        painter.drawPath(path)
        
        painter.setPen(QPen(self.color, 1.5))
        for i in range(3):
            y = 47 + i * 9
            painter.drawLine(21, y, 25, y)
            painter.drawLine(45, y, 49, y)

class BeakerWidget(QWidget):
    def __init__(self, color="#ffffff", parent=None):
        super().__init__(parent)
        self.color = QColor(color)
        self.setFixedSize(65, 80)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        painter.setPen(QPen(self.color, 2.5))
        painter.setBrush(Qt.NoBrush)
        painter.drawLine(18, 20, 18, 60)
        painter.drawLine(47, 20, 47, 60)
        painter.drawArc(14, 56, 37, 14, 0, -180 * 16)
        painter.drawLine(47, 20, 52, 16)
        
        painter.setPen(QPen(self.color, 1.5))
        for i in range(3):
            y = 28 + i * 10
            painter.drawLine(22, y, 26, y)

class TestTubeWidget(QWidget):
    def __init__(self, color="#ffffff", parent=None):
        super().__init__(parent)
        self.color = QColor(color)
        self.setFixedSize(55, 85)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        painter.setPen(QPen(self.color, 2.5))
        painter.setBrush(Qt.NoBrush)
        painter.drawLine(17, 14, 17, 68)
        painter.drawLine(38, 14, 38, 68)
        painter.drawArc(14, 64, 27, 14, 0, -180 * 16)
        
        painter.drawLine(14, 14, 17, 14)
        painter.drawLine(38, 14, 41, 14)

class MoleculeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(80, 80)
        self.rotation = 0
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        timer = QTimer(self)
        timer.timeout.connect(self.rotate)
        timer.start(30)
        
    def rotate(self):
        self.rotation += 1
        if self.rotation >= 360:
            self.rotation = 0
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        painter.translate(40, 40)
        painter.rotate(self.rotation)
        
        atoms = [
            (0, -18, 7),
            (16, -9, 6),
            (16, 9, 6),
            (0, 18, 7),
            (-16, 9, 6),
            (-16, -9, 6),
        ]
        
        painter.setPen(QPen(QColor("#ffffff"), 2))
        center = (0, 0)
        for x, y, _ in atoms:
            painter.drawLine(int(center[0]), int(center[1]), int(x), int(y))
        
        for x, y, size in atoms:
            painter.setPen(QPen(QColor("#ffffff"), 2.5))
            painter.setBrush(Qt.NoBrush)
            painter.drawEllipse(QRectF(float(x-size), float(y-size), float(size*2), float(size*2)))

class AtomWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(80, 80)
        self.angle = 0
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        timer = QTimer(self)
        timer.timeout.connect(self.update_orbit)
        timer.start(40)
        
    def update_orbit(self):
        self.angle += 3
        if self.angle >= 360:
            self.angle = 0
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        center_x, center_y = 40, 40
        
        painter.setPen(QPen(QColor("#ffffff"), 2.5))
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(center_x - 8, center_y - 8, 16, 16)
        
        painter.setPen(QPen(QColor("#ffffff"), 1.5, Qt.DashLine))
        painter.drawEllipse(center_x - 22, center_y - 22, 44, 44)
        painter.drawEllipse(center_x - 15, center_y - 15, 30, 30)
        
        for orbit_radius, offset in [(22, 0), (15, 180)]:
            angle_rad = math.radians(self.angle + offset)
            x = center_x + orbit_radius * math.cos(angle_rad)
            y = center_y + orbit_radius * math.sin(angle_rad)
            
            painter.setPen(QPen(QColor("#ffffff"), 2))
            painter.setBrush(Qt.NoBrush)
            painter.drawEllipse(QRectF(float(x - 4), float(y - 4), 8.0, 8.0))

class DNAHelixWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(70, 90)
        self.offset = 0
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        timer = QTimer(self)
        timer.timeout.connect(self.animate_helix)
        timer.start(50)
        
    def animate_helix(self):
        self.offset += 0.15
        if self.offset > 2 * math.pi:
            self.offset = 0
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        center_x = 35
        
        for strand_offset in [0, math.pi]:
            points = []
            for y in range(12, 80, 3):
                angle = (y - 12) / 10 + self.offset + strand_offset
                x = center_x + 17 * math.sin(angle)
                points.append(QPointF(float(x), float(y)))
            
            painter.setPen(QPen(QColor("#ffffff"), 2.5))
            painter.setBrush(Qt.NoBrush)
            
            path = QPainterPath()
            if points:
                path.moveTo(points[0])
                for point in points[1:]:
                    path.lineTo(point)
            painter.drawPath(path)
        
        painter.setPen(QPen(QColor("#ffffff"), 1.5))
        for y in range(20, 80, 14):
            angle1 = (y - 12) / 10 + self.offset
            angle2 = angle1 + math.pi
            x1 = center_x + 17 * math.sin(angle1)
            x2 = center_x + 17 * math.sin(angle2)
            painter.drawLine(QPointF(float(x1), float(y)), QPointF(float(x2), float(y)))

class BubbleWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(60, 80)
        self.bubbles = []
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        for i in range(4):
            self.bubbles.append({
                'x': random.randint(15, 45),
                'y': random.randint(0, 80),
                'size': random.randint(4, 8),
                'speed': random.uniform(0.5, 1.5)
            })
        
        timer = QTimer(self)
        timer.timeout.connect(self.animate_bubbles)
        timer.start(40)
        
    def animate_bubbles(self):
        for bubble in self.bubbles:
            bubble['y'] -= bubble['speed']
            if bubble['y'] < -10:
                bubble['y'] = 90
                bubble['x'] = random.randint(15, 45)
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        painter.setPen(QPen(QColor("#ffffff"), 2))
        painter.setBrush(Qt.NoBrush)
        
        for bubble in self.bubbles:
            painter.drawEllipse(QRectF(
                float(bubble['x'] - bubble['size']/2),
                float(bubble['y'] - bubble['size']/2),
                float(bubble['size']),
                float(bubble['size'])
            ))

class StatisticCard(QWidget):
    def __init__(self, title, icon_widget, color, parent=None):
        super().__init__(parent)
        self.color = color
        self.setup_ui(title, icon_widget)
        add_soft_shadow(self, radius=25, opacity=30)
        
    def setup_ui(self, title, icon_widget):
        self.setStyleSheet(f"""
            StatisticCard {{
                background: white;
                border-radius: 20px;
            }}
            QLabel {{
                border: none;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)
        
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        icon_container = QWidget()
        icon_container.setFixedSize(icon_widget.width(), icon_widget.height())
        
        icon_bg = QColor(self.color)
        icon_bg.setAlpha(25)
        icon_container.setStyleSheet(f"background-color: {icon_bg.name(QColor.HexArgb)}; border-radius: 12px;")
        
        icon_layout = QVBoxLayout(icon_container)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        icon_layout.addWidget(icon_widget)
        header_layout.addWidget(icon_container)
        
        header_layout.addSpacing(15)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 13, QFont.Bold))
        title_label.setStyleSheet(f"color: #8898aa; letter-spacing: 1px;")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        layout.addWidget(header)
        
        divider = QWidget()
        divider.setFixedHeight(1)
        divider.setStyleSheet(f"background: #f0f0f0;")
        layout.addWidget(divider)
        
        self.stats_container = QWidget()
        self.stats_layout = QVBoxLayout(self.stats_container)
        self.stats_layout.setSpacing(10)
        self.stats_layout.setContentsMargins(0, 5, 0, 0)
        layout.addWidget(self.stats_container)
        
    def add_stat(self, label, value, is_highlight=False):
        stat_widget = QWidget()
        stat_layout = QHBoxLayout(stat_widget)
        stat_layout.setContentsMargins(12, 8, 12, 8)
        
        if is_highlight:
            stat_widget.setStyleSheet(f"""
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {QColor(self.color).lighter(175).name()},
                    stop:1 {QColor(self.color).lighter(165).name()});
                border-radius: 10px;
            """)
            label_color = QColor(self.color).darker(150).name()
            value_color = QColor(self.color).darker(150).name()
        else:
            stat_widget.setStyleSheet("""
                background: transparent;
                border-radius: 8px;
            """)
            label_color = "#718096"
            value_color = "#2d3748"
        
        label_widget = QLabel(label)
        label_widget.setFont(QFont("Segoe UI", 10, QFont.DemiBold))
        label_widget.setStyleSheet(f"color: {label_color};")
        stat_layout.addWidget(label_widget)
        
        stat_layout.addStretch()
        
        value_widget = QLabel(value)
        value_widget.setFont(QFont("Segoe UI", 11, QFont.Bold))
        value_widget.setStyleSheet(f"color: {value_color};")
        stat_layout.addWidget(value_widget)
        
        self.stats_layout.addWidget(stat_widget)
        return stat_widget

class HeroWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(200)
        self.floating_widgets = []
        self.setup_ui()
        add_soft_shadow(self, radius=30, opacity=40, offset=(0, 10))
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor("#667eea"))
        gradient.setColorAt(0.5, QColor("#764ba2"))
        gradient.setColorAt(1, QColor("#6B8DD6"))
        
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 24, 24)
        
    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 30, 40, 25)
        
        title_container = QWidget()
        title_container.setStyleSheet("background: transparent;")
        title_layout = QVBoxLayout(title_container)
        title_layout.setSpacing(2)
        title_layout.setContentsMargins(0, 0, 0, 0)
        
        title = QLabel("CHEMICAL EQUIPMENT VISUALIZER")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet("color: white; background: transparent; letter-spacing: 1px;")
        title.setAlignment(Qt.AlignCenter)
        add_soft_shadow(title, radius=10, opacity=50, offset=(0,2))
        title_layout.addWidget(title)
        
        subtitle = QLabel("DASHBOARD ANALYTICS")
        subtitle.setFont(QFont("Segoe UI", 14, QFont.DemiBold))
        subtitle.setStyleSheet("color: rgba(255, 255, 255, 0.85); background: transparent; letter-spacing: 4px;")
        subtitle.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(subtitle)
        
        main_layout.addStretch()
        main_layout.addWidget(title_container)
        main_layout.addStretch()
        
    def showEvent(self, event):
        super().showEvent(event)
        if not self.floating_widgets:
            self.create_floating_widgets()
    
    def create_floating_widgets(self):
        width = self.width()
        
        positions = [
            (ChemicalFlaskWidget, 40, 30, -15),
            (MoleculeWidget, 100, 100, 12),
            (TestTubeWidget, 160, 25, 8),
            (BubbleWidget, 220, 60, -10),
            (BeakerWidget, width - 190, 35, 15),
            (AtomWidget, width - 140, 95, -8),
            (DNAHelixWidget, width - 250, 55, 10),
            (MoleculeWidget, width - 310, 20, -12),
            (TestTubeWidget, width - 90, 90, 18),
        ]
        
        for widget_class, x, y, rotation in positions:
            widget = widget_class(parent=self)
            widget.move(x, y)
            widget.show()
            self.floating_widgets.append(widget)

class DragDropUploadWidget(QWidget):
    file_selected = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.is_dragging = False
        self._hover_opacity = 0.0
        self.setup_ui()
        self.setup_animation()
        
    def setup_ui(self):
        self.setMinimumHeight(360)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(50, 40, 50, 40)
        layout.setSpacing(30)
        
        icon_container = QWidget()
        icon_container.setFixedSize(110, 110)
        icon_container.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 rgba(102, 126, 234, 0.1),
                stop:1 rgba(118, 75, 162, 0.1));
            border-radius: 55px;
            border: 1px solid rgba(102, 126, 234, 0.2);
        """)
        
        icon_layout = QVBoxLayout(icon_container)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        
        upload_icon = QLabel("↑")
        upload_icon.setFont(QFont("Arial", 52, QFont.Bold))
        upload_icon.setAlignment(Qt.AlignCenter)
        upload_icon.setStyleSheet("color: #667eea; background: transparent; border: none;")
        icon_layout.addWidget(upload_icon)
        
        layout.addWidget(icon_container, 0, Qt.AlignCenter)
        
        upload_text = QLabel("Drag & Drop CSV File Here")
        upload_text.setFont(QFont("Segoe UI", 28, QFont.Bold))
        upload_text.setAlignment(Qt.AlignCenter)
        upload_text.setStyleSheet("color: #4a5568; background: transparent;")
        layout.addWidget(upload_text)
        
        divider_container = QWidget()
        divider_container.setStyleSheet("background: transparent;")
        divider_layout = QHBoxLayout(divider_container)
        divider_layout.setContentsMargins(40, 0, 40, 0)
        divider_layout.setSpacing(20)
        
        left_line = QWidget()
        left_line.setFixedHeight(2)
        left_line.setStyleSheet("background: #e2e8f0;")
        divider_layout.addWidget(left_line, 1)
        
        or_label = QLabel("OR")
        or_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        or_label.setStyleSheet("color: #cbd5e0; background: transparent;")
        divider_layout.addWidget(or_label, 0)
        
        right_line = QWidget()
        right_line.setFixedHeight(2)
        right_line.setStyleSheet("background: #e2e8f0;")
        divider_layout.addWidget(right_line, 1)
        
        layout.addWidget(divider_container)
        
        browse_btn = QPushButton("Click to Browse Files")
        browse_btn.setFont(QFont("Segoe UI", 14, QFont.Bold))
        browse_btn.setCursor(Qt.PointingHandCursor)
        browse_btn.setMinimumHeight(60)
        browse_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                border: none;
                border-radius: 30px;
                padding: 10px 60px;
                letter-spacing: 0.5px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5a67d8, stop:1 #6B46C1);
            }
            QPushButton:pressed {
                background: #5a32a3;
            }
        """)
        add_soft_shadow(browse_btn, radius=15, opacity=40, offset=(0, 4))
        browse_btn.clicked.connect(self.browse_file)
        layout.addWidget(browse_btn, 0, Qt.AlignCenter)
        
        format_container = QWidget()
        format_container.setStyleSheet("background: transparent;")
        format_layout = QHBoxLayout(format_container)
        format_layout.setContentsMargins(0, 0, 0, 0)
        format_layout.addStretch()
        
        info_icon = QLabel("ⓘ")
        info_icon.setFont(QFont("Segoe UI", 12))
        info_icon.setStyleSheet("color: #a0aec0; background: transparent;")
        format_layout.addWidget(info_icon)
        
        format_label = QLabel("Supported Format: CSV files only")
        format_label.setFont(QFont("Segoe UI", 11))
        format_label.setStyleSheet("color: #a0aec0; background: transparent; padding-left: 5px;")
        format_layout.addWidget(format_label)
        
        format_layout.addStretch()
        layout.addWidget(format_container)
        
    def setup_animation(self):
        self.anim = QPropertyAnimation(self, b"hoverOpacity")
        self.anim.setDuration(200)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)
    
    def get_hover_opacity(self):
        return self._hover_opacity
    
    def set_hover_opacity(self, value):
        self._hover_opacity = value
        self.update()
    
    hoverOpacity = pyqtProperty(float, get_hover_opacity, set_hover_opacity)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        rect = self.rect().adjusted(10, 10, -10, -10)
        
        if self.is_dragging:
            pen = QPen(QColor("#667eea"), 3, Qt.SolidLine)
            pen.setJoinStyle(Qt.RoundJoin)
            painter.setPen(pen)
            
            gradient = QLinearGradient(0, 0, self.width(), self.height())
            gradient.setColorAt(0, QColor(102, 126, 234, 30))
            gradient.setColorAt(1, QColor(118, 75, 162, 30))
            painter.setBrush(QBrush(gradient))
        else:
            pen = QPen(QColor("#cbd5e0"), 2.5, Qt.DashLine)
            pen.setDashPattern([8, 6])
            pen.setJoinStyle(Qt.RoundJoin)
            painter.setPen(pen)
            
            if self._hover_opacity > 0:
                gradient = QLinearGradient(0, 0, self.width(), self.height())
                gradient.setColorAt(0, QColor(102, 126, 234, int(15 * self._hover_opacity)))
                gradient.setColorAt(1, QColor(118, 75, 162, int(15 * self._hover_opacity)))
                painter.setBrush(QBrush(gradient))
            else:
                painter.setBrush(QColor("#f8fafc"))
        
        painter.drawRoundedRect(rect, 30, 30)
        
    def enterEvent(self, event):
        self.anim.stop()
        self.anim.setStartValue(self._hover_opacity)
        self.anim.setEndValue(1.0)
        self.anim.start()
        
    def leaveEvent(self, event):
        self.anim.stop()
        self.anim.setStartValue(self._hover_opacity)
        self.anim.setEndValue(0.0)
        self.anim.start()
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if len(urls) == 1:
                file_path = urls[0].toLocalFile()
                if file_path.lower().endswith('.csv'):
                    event.acceptProposedAction()
                    self.is_dragging = True
                    self.update()
                    return
        event.ignore()
                
    def dragLeaveEvent(self, event):
        self.is_dragging = False
        self.update()
        
    def dropEvent(self, event):
        self.is_dragging = False
        self.update()
        
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls:
                file_path = urls[0].toLocalFile()
                if file_path.lower().endswith('.csv'):
                    event.acceptProposedAction()
                    self.file_selected.emit(file_path)
                    return
        event.ignore()
                
    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select CSV File",
            "",
            "CSV Files (*.csv);;All Files (*)"
        )
        
        if file_path:
            self.file_selected.emit(file_path)

class DashboardWidget(QWidget):
    dataset_uploaded = pyqtSignal(dict)
    
    def __init__(self, api):
        super().__init__()
        self.api = api
        self.current_dataset_id = None
        self.stat_widgets = {}
        self.setup_ui()
        
    def setup_ui(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: #f4f7f6;
            }
            QScrollBar:vertical {
                border: none;
                background: transparent;
                width: 8px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background: #d1d5db;
                border-radius: 4px;
                min-height: 40px;
            }
            QScrollBar::handle:vertical:hover {
                background: #9ca3af;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)
        
        self.scroll_content = QWidget()
        self.scroll_content.setStyleSheet("background: transparent;")
        
        main_layout = QVBoxLayout(self.scroll_content)
        main_layout.setContentsMargins(40, 30, 40, 60)
        main_layout.setSpacing(40)
        
        self.hero = HeroWidget()
        main_layout.addWidget(self.hero)
        
        self.upload_section = self.create_upload_section()
        main_layout.addWidget(self.upload_section)
        
        self.buttons_container = QWidget()
        self.buttons_container.setStyleSheet("background: transparent;")
        buttons_layout = QHBoxLayout(self.buttons_container)
        buttons_layout.setContentsMargins(0, 10, 0, 10)
        buttons_layout.setSpacing(25)
        
        def get_btn_style(color, hover_color):
            return f"""
                QPushButton {{
                    background: white;
                    color: {color};
                    border: 2px solid {color};
                    border-radius: 20px;
                    padding: 15px 40px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background: {color};
                    color: white;
                }}
                QPushButton:pressed {{
                    background: {hover_color};
                    border-color: {hover_color};
                }}
            """

        self.upload_another_btn = QPushButton("+ Upload Another Dataset")
        self.upload_another_btn.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.upload_another_btn.setCursor(Qt.PointingHandCursor)
        self.upload_another_btn.setMinimumHeight(65)
        self.upload_another_btn.setStyleSheet(get_btn_style("#667eea", "#5a67d8"))
        add_soft_shadow(self.upload_another_btn, radius=15, opacity=20)
        self.upload_another_btn.clicked.connect(self.reset_to_upload)
        buttons_layout.addWidget(self.upload_another_btn)
        
        self.download_btn = QPushButton("Download PDF Report")
        self.download_btn.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.download_btn.setCursor(Qt.PointingHandCursor)
        self.download_btn.setMinimumHeight(65)
        self.download_btn.setStyleSheet(get_btn_style("#10b981", "#059669"))
        add_soft_shadow(self.download_btn, radius=15, opacity=20)
        self.download_btn.clicked.connect(self.download_report)
        buttons_layout.addWidget(self.download_btn)
        
        main_layout.addWidget(self.buttons_container)
        self.buttons_container.hide()
        
        self.status_section = self.create_status_section()
        main_layout.addWidget(self.status_section)
        self.status_section.hide()
        
        self.statistics_section = self.create_statistics_section()
        main_layout.addWidget(self.statistics_section)
        self.statistics_section.hide()
        
        main_layout.addStretch()
        
        scroll.setWidget(self.scroll_content)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(scroll)
    
    def create_upload_section(self):
        section = QWidget()
        section.setStyleSheet("background: transparent;")
        
        layout = QVBoxLayout(section)
        layout.setSpacing(25)
        layout.setContentsMargins(0, 10, 0, 10)
        
        title = QLabel("Upload Your Dataset")
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title.setStyleSheet("color: #2d3748; background: transparent;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        subtitle = QLabel("Import a CSV file containing chemical equipment parameters to begin comprehensive analysis")
        subtitle.setFont(QFont("Segoe UI", 12))
        subtitle.setStyleSheet("color: #718096; background: transparent;")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setWordWrap(True)
        layout.addWidget(subtitle)
        
        self.drag_drop_widget = DragDropUploadWidget()
        self.drag_drop_widget.file_selected.connect(self.handle_file_upload)
        layout.addWidget(self.drag_drop_widget)
        
        return section
    
    def create_status_section(self):
        section = QWidget()
        section.setStyleSheet("background: transparent;")
        
        layout = QVBoxLayout(section)
        layout.setSpacing(20)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.status_card = QWidget()
        add_soft_shadow(self.status_card, radius=30, opacity=30)
        self.status_card.setMinimumHeight(320)
        self.status_card_layout = QVBoxLayout(self.status_card)
        self.status_card_layout.setContentsMargins(50, 45, 50, 45)
        self.status_card_layout.setSpacing(30)
        
        self.status_title = QLabel()
        self.status_title.setFont(QFont("Segoe UI", 26, QFont.Bold))
        self.status_title.setAlignment(Qt.AlignCenter)
        self.status_title.setStyleSheet("background: transparent; border: none;")
        self.status_card_layout.addWidget(self.status_title)
        
        self.status_details = QLabel()
        self.status_details.setFont(QFont("Segoe UI", 16))
        self.status_details.setAlignment(Qt.AlignCenter)
        self.status_details.setWordWrap(True)
        self.status_details.setStyleSheet("background: transparent; border: none;")
        self.status_card_layout.addWidget(self.status_details)
        
        layout.addWidget(self.status_card)
        
        return section
    
    def handle_file_upload(self, file_path):
        self.upload_section.hide()
        self.status_section.show()
        self.update_status_display("processing")
        QApplication.processEvents()
        
        success, result = self.api.upload_dataset(file_path)
        
        if success:
            dataset = result.get('dataset', {})
            self.current_dataset_id = dataset.get('id')
            
            self.update_status_display("success", dataset)
            self.buttons_container.show()
            self.load_statistics(self.current_dataset_id)
            self.dataset_uploaded.emit(result)
            
        else:
            self.update_status_display("error", result)
    
    def update_status_display(self, state, data=None):
        if state == "processing":
            self.status_card.setStyleSheet("""
                QWidget {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #fffbeb, stop:1 #fff7ed);
                    border-radius: 24px;
                    border: 1px solid #fcd34d;
                }
            """)
            
            self.status_title.setStyleSheet("color: #b45309; background: transparent; border: none;")
            self.status_title.setText("Processing Your Dataset")
            
            self.status_details.setStyleSheet("color: #d97706; background: transparent; border: none;")
            self.status_details.setText("Please wait while we analyze your chemical equipment data...")
            
        elif state == "success" and data:
            self.status_card.setStyleSheet("""
                QWidget {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #ecfdf5, stop:1 #d1fae5);
                    border-radius: 24px;
                    border: 1px solid #6ee7b7;
                }
            """)
            
            self.status_title.setStyleSheet("color: #047857; background: transparent; border: none;")
            self.status_title.setText("Dataset Processed Successfully")
            
            details_html = f"""
            <div style='line-height: 3.2; margin-top: 20px;'>
                <p style='color: #047857; font-size: 18px; font-weight: bold; margin-bottom: 8px;'>
                    Dataset Name: <span style='color: #059669; font-family: "Segoe UI"; font-weight: normal;'>{data.get('name', 'N/A')}</span>
                </p>
                <p style='color: #047857; font-size: 20px; font-weight: bold; margin-bottom: 8px;'>
                    Total Equipment: <span style='color: #059669; font-family: "Segoe UI"; font-weight: normal;'>{data.get('total_equipment', 0)}</span>
                </p>
                <p style='color: #047857; font-size: 18px; font-weight: bold; margin-bottom: 8px;'>
                    Average Flowrate: <span style='color: #059669; font-family: "Segoe UI"; font-weight: normal;'>{data.get('avg_flowrate', 0):.2f} m³/h</span>
                </p>
                <p style='color: #047857; font-size: 18px; font-weight: bold; margin-bottom: 8px;'>
                    Average Pressure: <span style='color: #059669; font-family: "Segoe UI"; font-weight: normal;'>{data.get('avg_pressure', 0):.2f} bar</span>
                </p>
                <p style='color: #047857; font-size: 18px; font-weight: bold; margin-bottom: 8px;'>
                    Average Temperature: <span style='color: #059669; font-family: "Segoe UI"; font-weight: normal;'>{data.get('avg_temperature', 0):.2f} °C</span>
                </p>
            </div>
            """
            self.status_details.setStyleSheet("color: #064e3b; background: transparent; border: none;")
            self.status_details.setText(details_html)
            
        elif state == "error":
            self.status_card.setStyleSheet("""
                QWidget {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #fef2f2, stop:1 #fee2e2);
                    border-radius: 24px;
                    border: 1px solid #fca5a5;
                }
            """)
            
            self.status_title.setStyleSheet("color: #b91c1c; background: transparent; border: none;")
            self.status_title.setText("Upload Failed")
            
            self.status_details.setStyleSheet("color: #ef4444; background: transparent; border: none;")
            self.status_details.setText(str(data) if data else "An error occurred. Please try again.")
    
    def reset_to_upload(self):
        self.upload_section.show()
        self.status_section.hide()
        self.buttons_container.hide()
        self.statistics_section.hide()
        self.current_dataset_id = None
    
    def create_statistics_section(self):
        section = QWidget()
        section.setStyleSheet("background: transparent;")
        
        layout = QVBoxLayout(section)
        layout.setSpacing(25)
        
        title = QLabel("COMPREHENSIVE ANALYSIS")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setStyleSheet("color: #4a5568; background: transparent; letter-spacing: 1px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        grid = QWidget()
        grid.setStyleSheet("background: transparent;")
        grid_layout = QGridLayout(grid)
        grid_layout.setSpacing(25)
        grid_layout.setContentsMargins(5, 5, 5, 5)
        
        self.flowrate_card = StatisticCard(
            "FLOWRATE",
            ChemicalFlaskWidget("#3b82f6"),
            "#3b82f6"
        )
        
        self.pressure_card = StatisticCard(
            "PRESSURE",
            BeakerWidget("#10b981"),
            "#10b981"
        )
        
        self.temp_card = StatisticCard(
            "TEMPERATURE",
            TestTubeWidget("#f59e0b"),
            "#f59e0b"
        )
        
        grid_layout.addWidget(self.flowrate_card, 0, 0)
        grid_layout.addWidget(self.pressure_card, 0, 1)
        grid_layout.addWidget(self.temp_card, 0, 2)
        
        layout.addWidget(grid)
        
        return section
    
    def download_report(self):
        if not self.current_dataset_id:
            self.show_message_dialog(
                "Warning",
                "No Dataset Loaded",
                "Please upload a dataset first.",
                "#f59e0b"
            )
            return
        
        save_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save PDF Report",
            "chemical_equipment_report.pdf",
            "PDF Files (*.pdf);;All Files (*)"
        )
        
        if not save_path:
            return
        
        success, message = self.api.download_report(self.current_dataset_id, save_path)
        
        if success:
            self.show_message_dialog(
                "Success",
                "Report Downloaded",
                f"Report saved to:\n{save_path}",
                "#10b981"
            )
        else:
            self.show_message_dialog(
                "Error",
                "Download Failed",
                message,
                "#ef4444"
            )
    
    def show_message_dialog(self, dialog_type, title, message, color):
        msg = QMessageBox(self)
        
        if dialog_type == "Success":
            msg.setIcon(QMessageBox.Information)
        elif dialog_type == "Error":
            msg.setIcon(QMessageBox.Critical)
        elif dialog_type == "Warning":
            msg.setIcon(QMessageBox.Warning)
        
        msg.setWindowTitle(dialog_type)
        msg.setText(title)
        msg.setInformativeText(message)
        
        msg.setStyleSheet(f"""
            QMessageBox {{
                background-color: white;
            }}
            QLabel {{
                color: #2d3748;
                font-family: "Segoe UI";
                font-size: 13px;
                min-width: 300px;
            }}
            QPushButton {{
                background: {color};
                color: white;
                border: none;
                padding: 8px 20px;
                border-radius: 6px;
                font-weight: bold;
                min-width: 80px;
            }}
            QPushButton:hover {{
                background: {QColor(color).darker(110).name()};
            }}
            QPushButton:pressed {{
                background: {QColor(color).darker(120).name()};
            }}
        """)
        
        msg.exec_()
    
    def load_dataset(self, dataset_id):
        self.current_dataset_id = dataset_id
        success, summary = self.api.get_dataset_summary(dataset_id)
        
        if success:
            self.upload_section.hide()
            self.status_section.show()
            
            dataset_info = {
                'name': f"Dataset #{dataset_id}",
                'total_equipment': summary.get('total_equipment', 0),
                'avg_flowrate': summary.get('averages', {}).get('flowrate', 0),
                'avg_pressure': summary.get('averages', {}).get('pressure', 0),
                'avg_temperature': summary.get('averages', {}).get('temperature', 0),
            }
            
            self.update_status_display("success", dataset_info)
            self.buttons_container.show()
            self.load_statistics(dataset_id)
    
    def load_statistics(self, dataset_id):
        success, summary = self.api.get_dataset_summary(dataset_id)
        
        if not success:
            return
        
        self.statistics_section.show()
        
        ranges = summary.get('ranges', {})
        avg = summary.get('averages', {})
        
        for card in [self.flowrate_card, self.pressure_card, self.temp_card]:
            for i in reversed(range(card.stats_layout.count())):
                card.stats_layout.itemAt(i).widget().setParent(None)
        
        flow = ranges.get('flowrate', {})
        self.flowrate_card.add_stat("Average", f"{avg.get('flowrate', 0):.2f} m³/h")
        self.flowrate_card.add_stat("Minimum", f"{flow.get('min', 0):.2f} m³/h")
        self.flowrate_card.add_stat("Maximum", f"{flow.get('max', 0):.2f} m³/h")
        self.flowrate_card.add_stat("Range", f"{(flow.get('max', 0) - flow.get('min', 0)):.2f} m³/h")
        self.flowrate_card.add_stat("Std. Deviation", f"{flow.get('std', 0):.2f}")
        self.flowrate_card.add_stat("Variance", f"{flow.get('var', 0):.2f}")
        self.flowrate_card.add_stat("CV", f"{flow.get('cv', 0):.2f}%", is_highlight=True)
        
        press = ranges.get('pressure', {})
        self.pressure_card.add_stat("Average", f"{avg.get('pressure', 0):.2f} bar")
        self.pressure_card.add_stat("Minimum", f"{press.get('min', 0):.2f} bar")
        self.pressure_card.add_stat("Maximum", f"{press.get('max', 0):.2f} bar")
        self.pressure_card.add_stat("Range", f"{(press.get('max', 0) - press.get('min', 0)):.2f} bar")
        self.pressure_card.add_stat("Std. Deviation", f"{press.get('std', 0):.2f}")
        self.pressure_card.add_stat("Variance", f"{press.get('var', 0):.2f}")
        self.pressure_card.add_stat("CV", f"{press.get('cv', 0):.2f}%", is_highlight=True)
        
        temp = ranges.get('temperature', {})
        self.temp_card.add_stat("Average", f"{avg.get('temperature', 0):.2f} °C")
        self.temp_card.add_stat("Minimum", f"{temp.get('min', 0):.2f} °C")
        self.temp_card.add_stat("Maximum", f"{temp.get('max', 0):.2f} °C")
        self.temp_card.add_stat("Range", f"{(temp.get('max', 0) - temp.get('min', 0)):.2f} °C")
        self.temp_card.add_stat("Std. Deviation", f"{temp.get('std', 0):.2f}")
        self.temp_card.add_stat("Variance", f"{temp.get('var', 0):.2f}")
        self.temp_card.add_stat("CV", f"{temp.get('cv', 0):.2f}%", is_highlight=True)