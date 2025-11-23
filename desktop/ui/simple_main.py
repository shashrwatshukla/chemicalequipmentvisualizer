from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class SimpleMainWindow(QMainWindow):
    def __init__(self, api, user):
        super().__init__()
        self.api = api
        self.user = user
        self.current_dataset_id = None
        
        self.setWindowTitle("Chemical Equipment Visualizer")
        self.showMaximized()
        
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        sidebar = QWidget()
        sidebar.setFixedWidth(280)
        sidebar.setStyleSheet("background-color: #2c3e50;")
        
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)
        
        app_header = QWidget()
        app_header.setStyleSheet("background-color: #1a252f; padding: 20px;")
        header_layout = QVBoxLayout(app_header)
        
        app_name = QLabel("ChemViz")
        app_name.setFont(QFont("Segoe UI", 28, QFont.Bold))
        app_name.setStyleSheet("color: white;")
        app_name.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(app_name)
        
        sidebar_layout.addWidget(app_header)
        
        user_info = QWidget()
        user_info.setStyleSheet("background-color: #34495e; padding: 15px;")
        user_layout = QVBoxLayout(user_info)
        user_layout.setSpacing(5)
        
        user_label = QLabel("Logged in as:")
        user_label.setFont(QFont("Segoe UI", 10))
        user_label.setStyleSheet("color: #95a5a6;")
        user_layout.addWidget(user_label)
        
        username = QLabel(user.get('username', 'User'))
        username.setFont(QFont("Segoe UI", 14, QFont.Bold))
        username.setStyleSheet("color: #ecf0f1;")
        user_layout.addWidget(username)
        
        sidebar_layout.addWidget(user_info)
        
        nav_style = """
            QPushButton {
                text-align: left;
                padding: 18px 25px;
                border: none;
                color: #ecf0f1;
                font-size: 15px;
                font-weight: bold;
                background-color: transparent;
                border-left: 4px solid transparent;
            }
            QPushButton:hover {
                background-color: #34495e;
                border-left: 4px solid #3498db;
            }
            QPushButton:checked {
                background-color: #3498db;
                border-left: 4px solid #2ecc71;
            }
        """
        
        self.nav_buttons = []
        
        dashboard_btn = QPushButton("   Dashboard")
        dashboard_btn.setCheckable(True)
        dashboard_btn.setChecked(True)
        dashboard_btn.setStyleSheet(nav_style)
        dashboard_btn.clicked.connect(lambda: self.switch_page(0))
        sidebar_layout.addWidget(dashboard_btn)
        self.nav_buttons.append(dashboard_btn)
        
        table_btn = QPushButton("   Data Table")
        table_btn.setCheckable(True)
        table_btn.setStyleSheet(nav_style)
        table_btn.clicked.connect(lambda: self.switch_page(1))
        sidebar_layout.addWidget(table_btn)
        self.nav_buttons.append(table_btn)
        
        charts_btn = QPushButton("   Charts")
        charts_btn.setCheckable(True)
        charts_btn.setStyleSheet(nav_style)
        charts_btn.clicked.connect(lambda: self.switch_page(2))
        sidebar_layout.addWidget(charts_btn)
        self.nav_buttons.append(charts_btn)
        
        history_btn = QPushButton("   History")
        history_btn.setCheckable(True)
        history_btn.setStyleSheet(nav_style)
        history_btn.clicked.connect(lambda: self.switch_page(3))
        sidebar_layout.addWidget(history_btn)
        self.nav_buttons.append(history_btn)
        
        sidebar_layout.addStretch()
        
        settings_btn = QPushButton("   Settings")
        settings_btn.setStyleSheet("""
            QPushButton {
                text-align: left; padding: 18px 25px; border: none;
                color: #ecf0f1; font-size: 15px; font-weight: bold;
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: #34495e;
            }
        """)
        settings_btn.clicked.connect(self.open_settings)
        sidebar_layout.addWidget(settings_btn)
        
        logout_btn = QPushButton("Logout")
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 18px;
                font-size: 15px;
                font-weight: bold;
                margin: 10px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        logout_btn.clicked.connect(self.do_logout)
        sidebar_layout.addWidget(logout_btn)
        
        main_layout.addWidget(sidebar)
        
        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet("background-color: #ecf0f1;")
        
        self.dashboard_page = self.create_dashboard_page()
        self.table_page = self.create_table_page()
        self.charts_page = self.create_charts_page()
        self.history_page = self.create_history_page()
        
        self.content_stack.addWidget(self.dashboard_page)
        self.content_stack.addWidget(self.table_page)
        self.content_stack.addWidget(self.charts_page)
        self.content_stack.addWidget(self.history_page)
        
        main_layout.addWidget(self.content_stack)
    
    def switch_page(self, index):
        self.content_stack.setCurrentIndex(index)
        for i, btn in enumerate(self.nav_buttons):
            btn.setChecked(i == index)
    
    def create_dashboard_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        
        title = QLabel("Dashboard")
        title.setFont(QFont("Segoe UI", 36, QFont.Bold))
        title.setStyleSheet("color: #2c3e50;")
        layout.addWidget(title)
        
        upload_btn = QPushButton("Upload CSV Dataset")
        upload_btn.setMinimumHeight(80)
        upload_btn.setFont(QFont("Segoe UI", 16, QFont.Bold))
        upload_btn.setCursor(Qt.PointingHandCursor)
        upload_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #11998e, stop:1 #38ef7d);
                color: white; border: none; border-radius: 15px;
            }
            QPushButton:hover { background: #0e8a7f; }
        """)
        upload_btn.clicked.connect(self.upload_csv)
        layout.addWidget(upload_btn)
        
        self.download_btn = QPushButton("Download PDF Report")
        self.download_btn.setMinimumHeight(80)
        self.download_btn.setFont(QFont("Segoe UI", 16, QFont.Bold))
        self.download_btn.setCursor(Qt.PointingHandCursor)
        self.download_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #667eea, stop:1 #764ba2);
                color: white; border: none; border-radius: 15px;
            }
            QPushButton:hover { background: #5568d3; }
            QPushButton:disabled { background: #95a5a6; color: #bdc3c7; }
        """)
        self.download_btn.clicked.connect(self.download_report)
        self.download_btn.setEnabled(False)
        layout.addWidget(self.download_btn)
        
        self.status = QLabel("No dataset loaded. Upload a CSV file to get started.")
        self.status.setFont(QFont("Segoe UI", 14))
        self.status.setWordWrap(True)
        self.status.setStyleSheet("""
            background-color: white; padding: 30px; border-radius: 15px;
            border: 2px solid #bdc3c7; color: #2c3e50;
        """)
        layout.addWidget(self.status)
        
        layout.addStretch()
        
        return page
    
    def create_table_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        
        title = QLabel("Equipment Data Table")
        title.setFont(QFont("Segoe UI", 36, QFont.Bold))
        title.setStyleSheet("color: #2c3e50;")
        layout.addWidget(title)
        
        export_btn = QPushButton("Export to CSV")
        export_btn.setMinimumHeight(50)
        export_btn.setFont(QFont("Segoe UI", 14, QFont.Bold))
        export_btn.setCursor(Qt.PointingHandCursor)
        export_btn.setStyleSheet("""
            QPushButton {
                background: #11998e; color: white; border: none; border-radius: 10px;
            }
            QPushButton:hover { background: #0e8a7f; }
        """)
        export_btn.clicked.connect(self.export_csv)
        layout.addWidget(export_btn)
        
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Equipment Name", "Type", "Flowrate", "Pressure", "Temperature"
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white; gridline-color: #bdc3c7;
                border: 2px solid #bdc3c7; border-radius: 10px;
                font-size: 13px;
            }
            QHeaderView::section {
                background-color: #34495e; color: white;
                padding: 15px; font-weight: bold; font-size: 14px;
            }
            QTableWidget::item {
                padding: 10px;
            }
        """)
        layout.addWidget(self.table)
        
        self.table_empty = QLabel("No data available. Upload a dataset from Dashboard.")
        self.table_empty.setFont(QFont("Segoe UI", 16))
        self.table_empty.setAlignment(Qt.AlignCenter)
        self.table_empty.setStyleSheet("color: #7f8c8d; padding: 50px;")
        layout.addWidget(self.table_empty)
        
        self.table.hide()
        
        return page
    
    def create_charts_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        
        title = QLabel("Data Visualization")
        title.setFont(QFont("Segoe UI", 36, QFont.Bold))
        title.setStyleSheet("color: #2c3e50;")
        layout.addWidget(title)
        
        try:
            import matplotlib
            matplotlib.use('Qt5Agg')
            from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
            from matplotlib.figure import Figure
            
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            scroll.setStyleSheet("border: none;")
            
            scroll_widget = QWidget()
            scroll_layout = QVBoxLayout(scroll_widget)
            scroll_layout.setSpacing(20)
            
            chart1_container = QGroupBox("Equipment Type Distribution")
            chart1_container.setFont(QFont("Segoe UI", 16, QFont.Bold))
            chart1_container.setStyleSheet("""
                QGroupBox {
                    background: white; border-radius: 15px;
                    padding: 20px; border: 2px solid #bdc3c7;
                }
            """)
            chart1_layout = QVBoxLayout(chart1_container)
            
            self.chart1_fig = Figure(figsize=(10, 5))
            self.chart1_canvas = FigureCanvasQTAgg(self.chart1_fig)
            self.chart1_ax = self.chart1_fig.add_subplot(111)
            chart1_layout.addWidget(self.chart1_canvas)
            
            scroll_layout.addWidget(chart1_container)
            
            chart2_container = QGroupBox("Parameter Averages")
            chart2_container.setFont(QFont("Segoe UI", 16, QFont.Bold))
            chart2_container.setStyleSheet("""
                QGroupBox {
                    background: white; border-radius: 15px;
                    padding: 20px; border: 2px solid #bdc3c7;
                }
            """)
            chart2_layout = QVBoxLayout(chart2_container)
            
            self.chart2_fig = Figure(figsize=(10, 5))
            self.chart2_canvas = FigureCanvasQTAgg(self.chart2_fig)
            self.chart2_ax = self.chart2_fig.add_subplot(111)
            chart2_layout.addWidget(self.chart2_canvas)
            
            scroll_layout.addWidget(chart2_container)
            
            scroll.setWidget(scroll_widget)
            layout.addWidget(scroll)
            
            self.charts_available = True
            
        except ImportError:
            error_label = QLabel("Matplotlib not installed.\n\nRun: pip install matplotlib")
            error_label.setFont(QFont("Segoe UI", 18))
            error_label.setAlignment(Qt.AlignCenter)
            error_label.setStyleSheet("color: #e74c3c; padding: 50px;")
            layout.addWidget(error_label)
            
            self.charts_available = False
        
        return page
    
    def create_history_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        
        title = QLabel("Upload History")
        title.setFont(QFont("Segoe UI", 36, QFont.Bold))
        title.setStyleSheet("color: #2c3e50;")
        layout.addWidget(title)
        
        btn_layout = QHBoxLayout()
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setMinimumHeight(50)
        refresh_btn.setFont(QFont("Segoe UI", 14, QFont.Bold))
        refresh_btn.setCursor(Qt.PointingHandCursor)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background: #3498db; color: white; border: none; border-radius: 10px;
            }
            QPushButton:hover { background: #2980b9; }
        """)
        refresh_btn.clicked.connect(self.load_history)
        btn_layout.addWidget(refresh_btn)
        
        self.delete_history_btn = QPushButton("Delete Selected")
        self.delete_history_btn.setMinimumHeight(50)
        self.delete_history_btn.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.delete_history_btn.setCursor(Qt.PointingHandCursor)
        self.delete_history_btn.setStyleSheet("""
            QPushButton {
                background: #e74c3c; color: white; border: none; border-radius: 10px;
            }
            QPushButton:hover { background: #c0392b; }
            QPushButton:disabled { background: #95a5a6; }
        """)
        self.delete_history_btn.clicked.connect(self.delete_from_history)
        self.delete_history_btn.setEnabled(False)
        btn_layout.addWidget(self.delete_history_btn)
        
        layout.addLayout(btn_layout)
        
        self.history_list = QListWidget()
        self.history_list.setStyleSheet("""
            QListWidget {
                background: white; border: 2px solid #bdc3c7;
                border-radius: 10px; font-size: 14px;
            }
            QListWidget::item {
                padding: 20px; border-bottom: 1px solid #ecf0f1;
            }
            QListWidget::item:hover {
                background: #ecf0f1;
            }
            QListWidget::item:selected {
                background: #3498db; color: white;
            }
        """)
        self.history_list.itemClicked.connect(lambda: self.delete_history_btn.setEnabled(True))
        self.history_list.itemDoubleClicked.connect(self.load_from_history)
        layout.addWidget(self.history_list)
        
        self.history_empty = QLabel("No upload history. Upload a dataset to see it here.")
        self.history_empty.setFont(QFont("Segoe UI", 16))
        self.history_empty.setAlignment(Qt.AlignCenter)
        self.history_empty.setStyleSheet("color: #7f8c8d; padding: 50px;")
        layout.addWidget(self.history_empty)
        
        self.history_list.hide()
        
        self.load_history()
        
        return page
    
    def upload_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select CSV", "", "CSV Files (*.csv)")
        if not file_path:
            return
        
        self.status.setText("Uploading... Please wait.")
        QApplication.processEvents()
        
        success, result = self.api.upload_dataset(file_path)
        
        if success:
            dataset = result.get('dataset', {})
            self.current_dataset_id = dataset.get('id')
            
            status_html = """
            <h2 style='color: #27ae60;'>Dataset Uploaded Successfully!</h2>
            <p><b>Name:</b> {}</p>
            <p><b>Total Equipment:</b> {}</p>
            <p><b>Average Flowrate:</b> {:.2f}</p>
            <p><b>Average Pressure:</b> {:.2f}</p>
            <p><b>Average Temperature:</b> {:.2f}</p>
            """.format(
                dataset.get('name'),
                dataset.get('total_equipment'),
                dataset.get('avg_flowrate', 0),
                dataset.get('avg_pressure', 0),
                dataset.get('avg_temperature', 0)
            )
            self.status.setText(status_html)
            self.download_btn.setEnabled(True)
            
            self.load_table_data(self.current_dataset_id)
            self.load_charts_data(self.current_dataset_id)
            self.load_history()
            
            QMessageBox.information(self, "Success", "Dataset uploaded successfully!")
        else:
            self.status.setText("<h3 style='color: #e74c3c;'>Upload Failed</h3><p>{}</p>".format(result))
            QMessageBox.critical(self, "Error", str(result))
    
    def load_table_data(self, dataset_id):
        success, data = self.api.get_dataset_detail(dataset_id)
        
        if not success:
            return
        
        equipment = data.get('equipment', [])
        
        if equipment:
            self.table_empty.hide()
            self.table.show()
            self.table.setRowCount(len(equipment))
            
            for row, eq in enumerate(equipment):
                self.table.setItem(row, 0, QTableWidgetItem(eq['equipment_name']))
                self.table.setItem(row, 1, QTableWidgetItem(eq['equipment_type']))
                self.table.setItem(row, 2, QTableWidgetItem('{:.2f}'.format(eq['flowrate'])))
                self.table.setItem(row, 3, QTableWidgetItem('{:.2f}'.format(eq['pressure'])))
                self.table.setItem(row, 4, QTableWidgetItem('{:.2f}'.format(eq['temperature'])))
    
    def load_charts_data(self, dataset_id):
        if not self.charts_available:
            return
        
        success, summary = self.api.get_dataset_summary(dataset_id)
        
        if not success:
            return
        
        dist = summary.get('type_distribution', {})
        if dist:
            self.chart1_ax.clear()
            self.chart1_ax.bar(dist.keys(), dist.values(), color='#3498db', alpha=0.8)
            self.chart1_ax.set_title('Equipment Type Distribution', fontsize=14, fontweight='bold')
            self.chart1_ax.set_xlabel('Equipment Type', fontsize=12)
            self.chart1_ax.set_ylabel('Count', fontsize=12)
            self.chart1_ax.grid(axis='y', alpha=0.3)
            self.chart1_fig.tight_layout()
            self.chart1_canvas.draw()
        
        avg = summary.get('averages', {})
        if avg:
            self.chart2_ax.clear()
            params = ['Flowrate', 'Pressure', 'Temperature']
            values = [avg.get('flowrate', 0), avg.get('pressure', 0), avg.get('temperature', 0)]
            self.chart2_ax.plot(params, values, marker='o', linewidth=3, markersize=12, color='#27ae60')
            self.chart2_ax.set_title('Parameter Averages', fontsize=14, fontweight='bold')
            self.chart2_ax.set_ylabel('Value', fontsize=12)
            self.chart2_ax.grid(True, alpha=0.3)
            self.chart2_fig.tight_layout()
            self.chart2_canvas.draw()
    
    def export_csv(self):
        if self.table.rowCount() == 0:
            QMessageBox.warning(self, "Error", "No data to export")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(self, "Save CSV", "export.csv", "CSV Files (*.csv)")
        
        if not file_path:
            return
        
        try:
            import csv
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature'])
                
                for row in range(self.table.rowCount()):
                    row_data = []
                    for col in range(5):
                        item = self.table.item(row, col)
                        row_data.append(item.text() if item else '')
                    writer.writerow(row_data)
            
            QMessageBox.information(self, "Success", "Data exported to:\n{}".format(file_path))
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
    
    def download_report(self):
        if not self.current_dataset_id:
            return
        
        save_path, _ = QFileDialog.getSaveFileName(self, "Save Report", "report.pdf", "PDF Files (*.pdf)")
        
        if not save_path:
            return
        
        success, message = self.api.download_report(self.current_dataset_id, save_path)
        
        if success:
            QMessageBox.information(self, "Success", "Report saved to:\n{}".format(save_path))
        else:
            QMessageBox.critical(self, "Error", message)
    
    def load_history(self):
        success, datasets = self.api.get_datasets()
        
        if not success:
            return
        
        self.history_list.clear()
        
        if not datasets:
            self.history_empty.show()
            self.history_list.hide()
            return
        
        self.history_empty.hide()
        self.history_list.show()
        
        for dataset in datasets:
            item_text = "{} - {} equipment - {}".format(
                dataset.get('name', 'Unknown'),
                dataset.get('total_equipment', 0),
                dataset.get('uploaded_at', '')[:19]
            )
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, dataset.get('id'))
            self.history_list.addItem(item)
    
    def load_from_history(self, item):
        dataset_id = item.data(Qt.UserRole)
        self.current_dataset_id = dataset_id
        
        success, summary = self.api.get_dataset_summary(dataset_id)
        
        if success:
            status_html = """
            <h2 style='color: #3498db;'>Dataset Loaded from History</h2>
            <p><b>Name:</b> {}</p>
            <p><b>Total Equipment:</b> {}</p>
            <p><b>Average Flowrate:</b> {:.2f}</p>
            <p><b>Average Pressure:</b> {:.2f}</p>
            <p><b>Average Temperature:</b> {:.2f}</p>
            """.format(
                summary.get('name'),
                summary.get('total_equipment'),
                summary.get('averages', {}).get('flowrate', 0),
                summary.get('averages', {}).get('pressure', 0),
                summary.get('averages', {}).get('temperature', 0)
            )
            self.status.setText(status_html)
            self.download_btn.setEnabled(True)
            
            self.load_table_data(dataset_id)
            self.load_charts_data(dataset_id)
            
            self.switch_page(0)
    
    def delete_from_history(self):
        current_item = self.history_list.currentItem()
        if not current_item:
            return
        
        reply = QMessageBox.question(self, "Confirm Delete", 
                                     "Are you sure you want to delete this dataset?",
                                     QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            dataset_id = current_item.data(Qt.UserRole)
            success, message = self.api.delete_dataset(dataset_id)
            
            if success:
                QMessageBox.information(self, "Success", "Dataset deleted")
                self.load_history()
                self.delete_history_btn.setEnabled(False)
            else:
                QMessageBox.critical(self, "Error", message)
    
    def open_settings(self):
        QMessageBox.information(self, "Settings", "Settings feature coming soon!\n\nYou can add:\n- Change password\n- Account settings\n- Preferences")
    
    def do_logout(self):
        reply = QMessageBox.question(self, "Logout", "Are you sure you want to logout?", 
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.api.logout()
            QApplication.quit()
    
    def closeEvent(self, event):
        reply = QMessageBox.question(self, "Exit", "Are you sure you want to exit?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()