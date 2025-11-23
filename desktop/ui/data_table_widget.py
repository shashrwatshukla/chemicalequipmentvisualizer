from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QPoint
from PyQt5.QtGui import QFont, QColor, QPalette, QLinearGradient, QPainter, QBrush, QPen
import csv

class ModernCard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAutoFillBackground(True)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        shadow_rect = self.rect().adjusted(2, 2, -2, -2)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(0, 0, 0, 15))
        painter.drawRoundedRect(shadow_rect, 14, 14)
        
        card_rect = self.rect().adjusted(0, 0, -4, -4)
        painter.setBrush(QColor(255, 255, 255))
        painter.drawRoundedRect(card_rect, 12, 12)


class DataTableWidget(QWidget):
    def __init__(self, api):
        super().__init__()
        self.api = api
        self.equipment_data = []
        self.filtered_data = []
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(30)
        
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
            }
        """)
        
        header_section = QWidget()
        header_section.setStyleSheet("background: transparent;")
        header_section.setMaximumHeight(120)
        header_layout = QVBoxLayout(header_section)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(12)
        
        title_action_bar = QWidget()
        title_action_bar.setStyleSheet("background: transparent;")
        title_action_layout = QHBoxLayout(title_action_bar)
        title_action_layout.setContentsMargins(0, 0, 0, 0)
        title_action_layout.setSpacing(20)
        
        title_container = QWidget()
        title_container.setStyleSheet("background: transparent;")
        title_container_layout = QVBoxLayout(title_container)
        title_container_layout.setContentsMargins(0, 0, 0, 0)
        title_container_layout.setSpacing(5)
        
        main_title = QLabel("Equipment Data Overview")
        main_title.setFont(QFont("Segoe UI", 34, QFont.Bold))
        main_title.setStyleSheet("""
            color: #1a1a2e;
            letter-spacing: -1px;
            background: transparent;
        """)
        title_container_layout.addWidget(main_title)
        
        subtitle = QLabel("Manage and analyze your equipment parameters")
        subtitle.setFont(QFont("Segoe UI", 11))
        subtitle.setStyleSheet("""
            color: #6c757d;
            background: transparent;
            margin-top: 2px;
        """)
        title_container_layout.addWidget(subtitle)
        
        title_action_layout.addWidget(title_container)
        title_action_layout.addStretch()
        
        action_buttons_container = QWidget()
        action_buttons_container.setStyleSheet("background: transparent;")
        action_buttons_layout = QHBoxLayout(action_buttons_container)
        action_buttons_layout.setContentsMargins(0, 0, 0, 0)
        action_buttons_layout.setSpacing(12)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setMinimumSize(120, 50)
        refresh_btn.setFont(QFont("Segoe UI", 10, QFont.DemiBold))
        refresh_btn.setCursor(Qt.PointingHandCursor)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #495057;
                border: 2px solid #dee2e6;
                border-radius: 10px;
                padding: 10px 20px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #f8f9fa;
                border-color: #adb5bd;
                color: #212529;
            }
            QPushButton:pressed {
                background-color: #e9ecef;
            }
        """)
        refresh_btn.clicked.connect(self.refresh_table)
        action_buttons_layout.addWidget(refresh_btn)
        
        export_btn = QPushButton("Export Data")
        export_btn.setMinimumSize(140, 50)
        export_btn.setFont(QFont("Segoe UI", 10, QFont.Bold))
        export_btn.setCursor(Qt.PointingHandCursor)
        export_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px 24px;
                font-weight: 700;
                letter-spacing: 0.5px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5568d3, stop:1 #6a4291);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4c5bbd, stop:1 #5e3a80);
                padding-top: 14px;
                padding-bottom: 10px;
            }
        """)
        export_btn.clicked.connect(self.export_csv)
        action_buttons_layout.addWidget(export_btn)
        
        title_action_layout.addWidget(action_buttons_container)
        header_layout.addWidget(title_action_bar)
        
        main_layout.addWidget(header_section)
        
        search_stats_card = QWidget()
        search_stats_card.setMinimumHeight(85)
        search_stats_card.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 14px;
                border: 1px solid #e1e4e8;
            }
        """)
        search_stats_layout = QHBoxLayout(search_stats_card)
        search_stats_layout.setContentsMargins(25, 18, 25, 18)
        search_stats_layout.setSpacing(20)
        
        search_section = QWidget()
        search_section.setStyleSheet("background: transparent; border: none;")
        search_section_layout = QHBoxLayout(search_section)
        search_section_layout.setContentsMargins(0, 0, 0, 0)
        search_section_layout.setSpacing(12)
        
        search_icon_label = QLabel("🔍")
        search_icon_label.setFont(QFont("Segoe UI", 24))
        search_icon_label.setStyleSheet("""
            background: transparent;
            color: #6c757d;
            border: none;
            padding: 8px;
        """)
        search_icon_label.setAlignment(Qt.AlignCenter)
        search_section_layout.addWidget(search_icon_label)
        
        search_input_container = QWidget()
        search_input_container.setStyleSheet("""
            background-color: #f8f9fa;
            border-radius: 10px;
            border: 2px solid transparent;
        """)
        search_input_layout = QHBoxLayout(search_input_container)
        search_input_layout.setContentsMargins(15, 0, 15, 0)
        search_input_layout.setSpacing(8)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search equipment by name, type, or parameters...")
        self.search_input.setFont(QFont("Segoe UI", 11))
        self.search_input.setMinimumHeight(48)
        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: transparent;
                border: none;
                color: #212529;
                padding: 8px 0px;
                font-size: 11pt;
            }
            QLineEdit:focus {
                background-color: transparent;
            }
            QLineEdit::placeholder {
                color: #adb5bd;
            }
        """)
        self.search_input.textChanged.connect(self.filter_table)
        search_input_layout.addWidget(self.search_input, 1)
        
        self.clear_search_btn = QPushButton("✕")
        self.clear_search_btn.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.clear_search_btn.setCursor(Qt.PointingHandCursor)
        self.clear_search_btn.setFixedSize(32, 32)
        self.clear_search_btn.setStyleSheet("""
            QPushButton {
                background-color: #dee2e6;
                color: #495057;
                border: none;
                border-radius: 16px;
                font-weight: 700;
            }
            QPushButton:hover {
                background-color: #ced4da;
                color: #212529;
            }
            QPushButton:pressed {
                background-color: #adb5bd;
            }
        """)
        self.clear_search_btn.clicked.connect(self.clear_search)
        self.clear_search_btn.hide()
        search_input_layout.addWidget(self.clear_search_btn)
        
        search_section_layout.addWidget(search_input_container, 1)
        search_stats_layout.addWidget(search_section, 1)
        
        divider = QFrame()
        divider.setFrameShape(QFrame.VLine)
        divider.setStyleSheet("background-color: #e9ecef; max-width: 1px; border: none;")
        search_stats_layout.addWidget(divider)
        
        stats_section = QWidget()
        stats_section.setStyleSheet("background: transparent; border: none;")
        stats_section.setMinimumWidth(220)
        stats_section_layout = QVBoxLayout(stats_section)
        stats_section_layout.setContentsMargins(15, 0, 0, 0)
        stats_section_layout.setSpacing(4)
        
        stats_label_title = QLabel("RECORDS")
        stats_label_title.setFont(QFont("Segoe UI", 8, QFont.Bold))
        stats_label_title.setStyleSheet("color: #6c757d; background: transparent; letter-spacing: 1px;")
        stats_section_layout.addWidget(stats_label_title)
        
        self.stats_label = QLabel("0 Total")
        self.stats_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        self.stats_label.setStyleSheet("""
            color: #212529;
            background: transparent;
        """)
        stats_section_layout.addWidget(self.stats_label)
        
        search_stats_layout.addWidget(stats_section)
        
        main_layout.addWidget(search_stats_card)
        
        self.table_card = QWidget()
        self.table_card.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 14px;
                border: 1px solid #e1e4e8;
            }
        """)
        table_card_layout = QVBoxLayout(self.table_card)
        table_card_layout.setContentsMargins(0, 0, 0, 0)
        table_card_layout.setSpacing(0)
        
        table_header_bar = QWidget()
        table_header_bar.setMinimumHeight(60)
        table_header_bar.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
                border-top-left-radius: 14px;
                border-top-right-radius: 14px;
                border-bottom: 2px solid #dee2e6;
            }
        """)
        table_header_layout = QHBoxLayout(table_header_bar)
        table_header_layout.setContentsMargins(25, 15, 25, 15)
        
        table_title = QLabel("Equipment List")
        table_title.setFont(QFont("Segoe UI", 13, QFont.Bold))
        table_title.setStyleSheet("color: #212529; background: transparent; border: none;")
        table_header_layout.addWidget(table_title)
        
        table_header_layout.addStretch()
        
        view_mode_label = QLabel("Table View")
        view_mode_label.setFont(QFont("Segoe UI", 9))
        view_mode_label.setStyleSheet("color: #6c757d; background: transparent; border: none;")
        table_header_layout.addWidget(view_mode_label)
        
        table_card_layout.addWidget(table_header_bar)
        
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Sr.", "Equipment Name", "Type", "Flowrate (L/min)", "Pressure (bar)", "Temperature (°C)"
        ])
        
        self.table.setColumnWidth(0, 70)
        
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)
        
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setShowGrid(False)
        self.table.verticalHeader().setVisible(False)
        self.table.setMinimumHeight(550)
        self.table.setSortingEnabled(True)
        self.table.setMouseTracking(True)
        
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #ffffff;
                alternate-background-color: #f8f9fa;
                gridline-color: transparent;
                border: none;
                border-bottom-left-radius: 14px;
                border-bottom-right-radius: 14px;
                font-size: 10.5pt;
                color: #212529;
                selection-background-color: #e7f3ff;
                selection-color: #0052cc;
            }
            QTableWidget::item {
                padding: 18px 15px;
                border: none;
                border-bottom: 1px solid #f1f3f5;
            }
            QTableWidget::item:selected {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #e7f3ff, stop:1 #f0f7ff);
                color: #0052cc;
                font-weight: 600;
            }
            QTableWidget::item:hover {
                background-color: #f1f5f9;
            }
            
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2c3e50, stop:1 #34495e);
                color: white;
                padding: 16px 15px;
                font-weight: 700;
                font-size: 9.5pt;
                border: none;
                border-right: 1px solid #243342;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            QHeaderView::section:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #34495e, stop:1 #3d5266);
            }
            QHeaderView::section:first {
                border-top-left-radius: 0px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
            }
            QHeaderView::section:last {
                border-right: none;
            }
            
            QScrollBar:vertical {
                border: none;
                background-color: #f8f9fa;
                width: 14px;
                border-radius: 7px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #cbd5e0, stop:1 #a0aec0);
                border-radius: 7px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #a0aec0, stop:1 #718096);
            }
            QScrollBar::handle:vertical:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #718096, stop:1 #4a5568);
            }
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: none;
            }
            
            QScrollBar:horizontal {
                border: none;
                background-color: #f8f9fa;
                height: 14px;
                border-radius: 7px;
                margin: 0px;
            }
            QScrollBar::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #cbd5e0, stop:1 #a0aec0);
                border-radius: 7px;
                min-width: 30px;
            }
            QScrollBar::handle:horizontal:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #a0aec0, stop:1 #718096);
            }
            QScrollBar::handle:horizontal:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #718096, stop:1 #4a5568);
            }
            QScrollBar::add-line:horizontal,
            QScrollBar::sub-line:horizontal {
                width: 0px;
            }
            QScrollBar::add-page:horizontal,
            QScrollBar::sub-page:horizontal {
                background: none;
            }
        """)
        
        table_card_layout.addWidget(self.table)
        main_layout.addWidget(self.table_card, 1)
        
        self.empty_state = QWidget()
        self.empty_state.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 14px;
                border: 1px solid #e1e4e8;
            }
        """)
        empty_layout = QVBoxLayout(self.empty_state)
        empty_layout.setAlignment(Qt.AlignCenter)
        empty_layout.setSpacing(25)
        empty_layout.setContentsMargins(40, 60, 40, 60)
        
        empty_illustration = QWidget()
        empty_illustration.setFixedSize(140, 140)
        empty_illustration.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
                border: 4px dashed #ced4da;
                border-radius: 70px;
            }
        """)
        empty_illustration_layout = QVBoxLayout(empty_illustration)
        empty_illustration_layout.setAlignment(Qt.AlignCenter)
        
        empty_icon = QLabel("DATA")
        empty_icon.setFont(QFont("Segoe UI", 16, QFont.Black))
        empty_icon.setAlignment(Qt.AlignCenter)
        empty_icon.setStyleSheet("""
            color: #adb5bd;
            border: none;
            background: transparent;
            letter-spacing: 2px;
        """)
        empty_illustration_layout.addWidget(empty_icon)
        
        empty_layout.addWidget(empty_illustration, 0, Qt.AlignCenter)
        
        empty_msg = QLabel("No Equipment Data")
        empty_msg.setFont(QFont("Segoe UI", 26, QFont.Bold))
        empty_msg.setAlignment(Qt.AlignCenter)
        empty_msg.setStyleSheet("""
            color: #212529;
            background: transparent;
            border: none;
            margin-top: 15px;
        """)
        empty_layout.addWidget(empty_msg)
        
        empty_desc = QLabel("Upload a dataset to view and analyze equipment parameters.\nYour data will appear in a beautiful table format.")
        empty_desc.setFont(QFont("Segoe UI", 11))
        empty_desc.setAlignment(Qt.AlignCenter)
        empty_desc.setWordWrap(True)
        empty_desc.setStyleSheet("""
            color: #6c757d;
            background: transparent;
            border: none;
            line-height: 1.6;
        """)
        empty_layout.addWidget(empty_desc)
        
        main_layout.addWidget(self.empty_state, 1)
        
        self.table_card.hide()
        self.empty_state.show()
        
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.perform_search)
    
    def load_dataset(self, dataset_id):
        success, data = self.api.get_dataset_detail(dataset_id)
        
        if success:
            equipment = data.get('equipment', [])
            self.equipment_data = equipment
            self.filtered_data = equipment.copy()
            
            if equipment:
                self.empty_state.hide()
                self.table_card.show()
                
                self.update_stats()
                
                self.populate_table(self.filtered_data)
                
                self.search_input.clear()
    
    def populate_table(self, data):
        self.table.setSortingEnabled(False)
        self.table.setRowCount(len(data))
        
        for row, eq in enumerate(data):
            serial_item = QTableWidgetItem(str(row + 1))
            serial_item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            serial_item.setFont(QFont("Segoe UI", 10, QFont.Bold))
            serial_item.setForeground(QColor("#667eea"))
            
            name_item = QTableWidgetItem(eq['equipment_name'])
            name_item.setFont(QFont("Segoe UI", 10, QFont.DemiBold))
            
            type_item = QTableWidgetItem(eq['equipment_type'])
            
            flow_item = QTableWidgetItem('{:.2f}'.format(eq['flowrate']))
            pressure_item = QTableWidgetItem('{:.2f}'.format(eq['pressure']))
            temp_item = QTableWidgetItem('{:.2f}'.format(eq['temperature']))
            
            flow_item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            pressure_item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            temp_item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            
            self.table.setItem(row, 0, serial_item)
            self.table.setItem(row, 1, name_item)
            self.table.setItem(row, 2, type_item)
            self.table.setItem(row, 3, flow_item)
            self.table.setItem(row, 4, pressure_item)
            self.table.setItem(row, 5, temp_item)
        
        self.table.setSortingEnabled(True)
        self.table.resizeRowsToContents()
    
    def filter_table(self):
        search_text = self.search_input.text().strip()
        
        if search_text:
            self.clear_search_btn.show()
        else:
            self.clear_search_btn.hide()
        
        self.search_timer.stop()
        self.search_timer.start(300)
    
    def perform_search(self):
        search_text = self.search_input.text().strip().lower()
        
        if not search_text:
            self.filtered_data = self.equipment_data.copy()
        else:
            self.filtered_data = []
            for eq in self.equipment_data:
                if (search_text in eq['equipment_name'].lower() or
                    search_text in eq['equipment_type'].lower() or
                    search_text in str(eq['flowrate']).lower() or
                    search_text in str(eq['pressure']).lower() or
                    search_text in str(eq['temperature']).lower()):
                    self.filtered_data.append(eq)
        
        self.populate_table(self.filtered_data)
        self.update_stats()
    
    def clear_search(self):
        self.search_input.clear()
        self.search_input.setFocus()
    
    def refresh_table(self):
        if self.equipment_data:
            self.search_input.clear()
            self.filtered_data = self.equipment_data.copy()
            self.populate_table(self.filtered_data)
            self.update_stats()
    
    def update_stats(self):
        total = len(self.equipment_data)
        showing = len(self.filtered_data)
        
        if total == showing:
            self.stats_label.setText(f"{total} Total")
        else:
            self.stats_label.setText(f"{showing} of {total}")
    
    def export_csv(self):
        if not self.equipment_data:
            self.show_message(
                "No Data Available",
                "There is no data to export.",
                "Please load a dataset first before attempting to export.",
                QMessageBox.Warning
            )
            return
        
        data_to_export = self.filtered_data if self.search_input.text().strip() else self.equipment_data
        
        if not data_to_export:
            self.show_message(
                "No Results Found",
                "No data matches your current search filter.",
                "Clear the search filter to export all available data.",
                QMessageBox.Warning
            )
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save CSV File",
            "equipment_export.csv",
            "CSV Files (*.csv)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Serial No.', 'Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature'])
                    for idx, eq in enumerate(data_to_export, 1):
                        writer.writerow([
                            idx,
                            eq['equipment_name'],
                            eq['equipment_type'],
                            eq['flowrate'],
                            eq['pressure'],
                            eq['temperature']
                        ])
                
                self.show_message(
                    "Export Successful",
                    f"Successfully exported {len(data_to_export)} records!",
                    f"File saved to:\n{file_path}",
                    QMessageBox.Information
                )
                
            except Exception as e:
                self.show_message(
                    "Export Failed",
                    "An error occurred while exporting data.",
                    f"Error details: {str(e)}",
                    QMessageBox.Critical
                )
    
    def show_message(self, title, text, info_text, icon):
        msg = QMessageBox(self)
        msg.setIcon(icon)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setInformativeText(info_text)
        msg.setStandardButtons(QMessageBox.Ok)
        
        if icon == QMessageBox.Information:
            color = "#10b981"
            hover_color = "#059669"
            bg_color = "#d1fae5"
        elif icon == QMessageBox.Warning:
            color = "#f59e0b"
            hover_color = "#d97706"
            bg_color = "#fef3c7"
        else:
            color = "#ef4444"
            hover_color = "#dc2626"
            bg_color = "#fee2e2"
        
        msg.setStyleSheet(f"""
            QMessageBox {{
                background-color: white;
            }}
            QMessageBox QLabel {{
                color: #212529;
                font-size: 11pt;
                padding: 10px;
            }}
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 28px;
                font-weight: 700;
                font-size: 10pt;
                min-width: 100px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
            QPushButton:pressed {{
                padding-top: 14px;
                padding-bottom: 10px;
            }}
        """)
        msg.exec_()