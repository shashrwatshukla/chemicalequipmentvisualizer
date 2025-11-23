from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from datetime import datetime


class HistoryWidget(QWidget):
    dataset_selected = pyqtSignal(int)
    
    def __init__(self, api):
        super().__init__()
        self.api = api
        self.datasets = []
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(30)
        
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
            }
        """)
        
        header_container = QFrame()
        header_container.setMinimumHeight(160)
        header_container.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4a90e2, stop:0.5 #357abd, stop:1 #4a90e2);
                border-radius: 20px;
            }
        """)
        header_shadow = QGraphicsDropShadowEffect()
        header_shadow.setBlurRadius(35)
        header_shadow.setColor(QColor(74, 144, 226, 100))
        header_shadow.setOffset(0, 8)
        header_container.setGraphicsEffect(header_shadow)
        
        header_layout = QVBoxLayout(header_container)
        header_layout.setContentsMargins(50, 40, 50, 40)
        header_layout.setSpacing(12)
        
        title = QLabel("Dataset Upload History")
        title.setFont(QFont("Segoe UI", 38, QFont.Bold))
        title.setWordWrap(True)
        title.setStyleSheet("color: white; letter-spacing: 1px; background: transparent;")
        header_layout.addWidget(title)
        
        subtitle = QLabel("View and manage your last 5 uploaded chemical equipment datasets")
        subtitle.setFont(QFont("Segoe UI", 14))
        subtitle.setWordWrap(True)
        subtitle.setStyleSheet("color: rgba(255, 255, 255, 0.95); letter-spacing: 0.5px; background: transparent;")
        header_layout.addWidget(subtitle)
        
        layout.addWidget(header_container)
        
        buttons_container = QFrame()
        buttons_container.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 18px;
            }
        """)
        buttons_shadow = QGraphicsDropShadowEffect()
        buttons_shadow.setBlurRadius(20)
        buttons_shadow.setColor(QColor(0, 0, 0, 25))
        buttons_shadow.setOffset(0, 4)
        buttons_container.setGraphicsEffect(buttons_shadow)
        
        btn_layout = QHBoxLayout(buttons_container)
        btn_layout.setContentsMargins(30, 25, 30, 25)
        btn_layout.setSpacing(20)
        
        refresh_btn = QPushButton("Refresh History")
        refresh_btn.setMinimumHeight(60)
        refresh_btn.setFont(QFont("Segoe UI", 15, QFont.Bold))
        refresh_btn.setCursor(Qt.PointingHandCursor)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4a90e2, stop:1 #357abd);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 0px 40px;
                letter-spacing: 0.5px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #357abd, stop:1 #2a5f8f);
            }
            QPushButton:pressed {
                background: #2a5f8f;
            }
        """)
        refresh_btn.clicked.connect(self.load_history)
        btn_layout.addWidget(refresh_btn)
        
        self.delete_btn = QPushButton("Delete Selected Dataset")
        self.delete_btn.setMinimumHeight(60)
        self.delete_btn.setFont(QFont("Segoe UI", 15, QFont.Bold))
        self.delete_btn.setCursor(Qt.PointingHandCursor)
        self.delete_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #e74c3c, stop:1 #c0392b);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 0px 40px;
                letter-spacing: 0.5px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #c0392b, stop:1 #a93226);
            }
            QPushButton:pressed {
                background: #a93226;
            }
            QPushButton:disabled {
                background: #bdc3c7;
                color: #7f8c8d;
            }
        """)
        self.delete_btn.clicked.connect(self.delete_selected)
        self.delete_btn.setEnabled(False)
        btn_layout.addWidget(self.delete_btn)
        
        layout.addWidget(buttons_container)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                background: #dee2e6;
                width: 12px;
                border-radius: 6px;
                margin: 2px;
            }
            QScrollBar::handle:vertical {
                background: #4a90e2;
                border-radius: 6px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background: #357abd;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        self.list_container = QWidget()
        self.list_container.setStyleSheet("background: transparent;")
        self.list_layout = QVBoxLayout(self.list_container)
        self.list_layout.setSpacing(20)
        self.list_layout.setContentsMargins(5, 5, 5, 5)
        
        self.scroll_area.setWidget(self.list_container)
        layout.addWidget(self.scroll_area)
        
        self.empty_state = QFrame()
        self.empty_state.setMinimumHeight(450)
        self.empty_state.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 20px;
            }
        """)
        empty_shadow = QGraphicsDropShadowEffect()
        empty_shadow.setBlurRadius(25)
        empty_shadow.setColor(QColor(0, 0, 0, 20))
        empty_shadow.setOffset(0, 4)
        self.empty_state.setGraphicsEffect(empty_shadow)
        
        empty_layout = QVBoxLayout(self.empty_state)
        empty_layout.setAlignment(Qt.AlignCenter)
        empty_layout.setSpacing(25)
        
        empty_title = QLabel("No Upload History")
        empty_title.setFont(QFont("Segoe UI", 32, QFont.Bold))
        empty_title.setAlignment(Qt.AlignCenter)
        empty_title.setStyleSheet("color: #495057; background: transparent;")
        empty_layout.addWidget(empty_title)
        
        empty_text = QLabel("Upload your first CSV file from the Dashboard\nto see it appear in the history")
        empty_text.setFont(QFont("Segoe UI", 16))
        empty_text.setAlignment(Qt.AlignCenter)
        empty_text.setStyleSheet("color: #868e96; line-height: 1.6; background: transparent;")
        empty_text.setWordWrap(True)
        empty_layout.addWidget(empty_text)
        
        layout.addWidget(self.empty_state)
        
        self.scroll_area.hide()
        self.selected_dataset_id = None
        self.selected_item_container = None
        
        print("  History widget created")
    
    def load_history(self):
        print("  Loading history...")
        
        try:
            success, datasets = self.api.get_datasets()
            
            if not success:
                print(f"  Failed to load history: {datasets}")
                QMessageBox.critical(self, "Error", f"Failed to load history:\n{datasets}")
                return
            
            while self.list_layout.count():
                child = self.list_layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
            
            self.datasets = datasets
            
            if not datasets:
                self.empty_state.show()
                self.scroll_area.hide()
                print("  No datasets found")
                return
            
            self.empty_state.hide()
            self.scroll_area.show()
            
            for dataset in datasets:
                item = self.create_dataset_item(dataset)
                self.list_layout.addWidget(item)
            
            self.list_layout.addStretch()
            
            print(f"  History loaded: {len(datasets)} datasets")
            
        except Exception as e:
            print(f"  ERROR in load_history: {str(e)}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Failed to load history:\n{str(e)}")
    
    def create_dataset_item(self, dataset):
        item_container = QFrame()
        item_container.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 16px;
                border: 2px solid #dee2e6;
            }
            QFrame:hover {
                border: 2px solid #4a90e2;
            }
        """)
        
        item_shadow = QGraphicsDropShadowEffect()
        item_shadow.setBlurRadius(15)
        item_shadow.setColor(QColor(0, 0, 0, 30))
        item_shadow.setOffset(0, 3)
        item_container.setGraphicsEffect(item_shadow)
        
        item_container.dataset_id = dataset.get('id')
        item_container.dataset_name = dataset.get('name', 'Unknown')
        item_container.is_selected = False
        
        main_layout = QVBoxLayout(item_container)
        main_layout.setContentsMargins(40, 35, 40, 35)
        main_layout.setSpacing(25)
        
        name_label = QLabel(dataset.get('name', 'Unknown'))
        name_label.setFont(QFont("Segoe UI", 26, QFont.Bold))
        name_label.setStyleSheet("color: #212529; background: transparent; border: none; padding: 0px;")
        name_label.setWordWrap(True)
        main_layout.addWidget(name_label)
        
        date_str = dataset.get('uploaded_at', '')
        try:
            date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            formatted_date = date_obj.strftime("%B %d, %Y at %I:%M %p")
        except:
            formatted_date = date_str[:19] if len(date_str) >= 19 else date_str
        
        time_label = QLabel(f"Uploaded on {formatted_date}")
        time_label.setFont(QFont("Segoe UI", 14))
        time_label.setStyleSheet("color: #6c757d; background: transparent; border: none; padding: 0px;")
        main_layout.addWidget(time_label)
        
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setStyleSheet("background: #dee2e6; max-height: 1px; border: none;")
        main_layout.addWidget(divider)
        
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(50)
        
        total_layout = QVBoxLayout()
        total_layout.setSpacing(8)
        total_label = QLabel("Total Equipment")
        total_label.setFont(QFont("Segoe UI", 13))
        total_label.setStyleSheet("color: #6c757d; background: transparent; border: none; padding: 0px;")
        total_layout.addWidget(total_label)
        total_value = QLabel(str(dataset.get('total_equipment', 0)))
        total_value.setFont(QFont("Segoe UI", 30, QFont.Bold))
        total_value.setStyleSheet("color: #212529; background: transparent; border: none; padding: 0px;")
        total_layout.addWidget(total_value)
        stats_layout.addLayout(total_layout)
        
        v_sep1 = QFrame()
        v_sep1.setFrameShape(QFrame.VLine)
        v_sep1.setStyleSheet("background: #dee2e6; max-width: 1px; border: none;")
        stats_layout.addWidget(v_sep1)
        
        flow_layout = QVBoxLayout()
        flow_layout.setSpacing(8)
        flow_label = QLabel("Average Flowrate")
        flow_label.setFont(QFont("Segoe UI", 13))
        flow_label.setStyleSheet("color: #6c757d; background: transparent; border: none; padding: 0px;")
        flow_layout.addWidget(flow_label)
        flow_value = QLabel(f"{dataset.get('avg_flowrate', 0):.2f}")
        flow_value.setFont(QFont("Segoe UI", 30, QFont.Bold))
        flow_value.setStyleSheet("color: #212529; background: transparent; border: none; padding: 0px;")
        flow_layout.addWidget(flow_value)
        stats_layout.addLayout(flow_layout)
        
        v_sep2 = QFrame()
        v_sep2.setFrameShape(QFrame.VLine)
        v_sep2.setStyleSheet("background: #dee2e6; max-width: 1px; border: none;")
        stats_layout.addWidget(v_sep2)
        
        press_layout = QVBoxLayout()
        press_layout.setSpacing(8)
        press_label = QLabel("Average Pressure")
        press_label.setFont(QFont("Segoe UI", 13))
        press_label.setStyleSheet("color: #6c757d; background: transparent; border: none; padding: 0px;")
        press_layout.addWidget(press_label)
        press_value = QLabel(f"{dataset.get('avg_pressure', 0):.2f}")
        press_value.setFont(QFont("Segoe UI", 30, QFont.Bold))
        press_value.setStyleSheet("color: #212529; background: transparent; border: none; padding: 0px;")
        press_layout.addWidget(press_value)
        stats_layout.addLayout(press_layout)
        
        v_sep3 = QFrame()
        v_sep3.setFrameShape(QFrame.VLine)
        v_sep3.setStyleSheet("background: #dee2e6; max-width: 1px; border: none;")
        stats_layout.addWidget(v_sep3)
        
        temp_layout = QVBoxLayout()
        temp_layout.setSpacing(8)
        temp_label = QLabel("Average Temperature")
        temp_label.setFont(QFont("Segoe UI", 13))
        temp_label.setStyleSheet("color: #6c757d; background: transparent; border: none; padding: 0px;")
        temp_layout.addWidget(temp_label)
        temp_value = QLabel(f"{dataset.get('avg_temperature', 0):.2f}")
        temp_value.setFont(QFont("Segoe UI", 30, QFont.Bold))
        temp_value.setStyleSheet("color: #212529; background: transparent; border: none; padding: 0px;")
        temp_layout.addWidget(temp_value)
        stats_layout.addLayout(temp_layout)
        
        stats_layout.addStretch()
        
        main_layout.addLayout(stats_layout)
        
        divider2 = QFrame()
        divider2.setFrameShape(QFrame.HLine)
        divider2.setStyleSheet("background: #dee2e6; max-height: 1px; border: none;")
        main_layout.addWidget(divider2)
        
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(15)
        
        view_container = QWidget()
        view_container.setStyleSheet("background: transparent;")
        view_container_layout = QVBoxLayout(view_container)
        view_container_layout.setContentsMargins(0, 0, 0, 0)
        view_container_layout.setSpacing(5)
        view_container_layout.setAlignment(Qt.AlignTop)
        
        view_btn = QPushButton("Click Here to View in Detail")
        view_btn.setMinimumHeight(60)
        view_btn.setMaximumHeight(60)
        view_btn.setFont(QFont("Segoe UI", 15, QFont.Bold))
        view_btn.setCursor(Qt.PointingHandCursor)
        view_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4a90e2, stop:1 #357abd);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 0px 35px;
                letter-spacing: 0.5px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #357abd, stop:1 #2a5f8f);
            }
            QPushButton:pressed {
                background: #2a5f8f;
            }
        """)
        view_btn.clicked.connect(lambda checked, did=dataset.get('id'): self.view_details(did))
        view_container_layout.addWidget(view_btn)
        
        view_subtitle = QLabel("(This action may take ~10 seconds to complete.)")
        view_subtitle.setFont(QFont("Segoe UI", 10))
        view_subtitle.setAlignment(Qt.AlignCenter)
        view_subtitle.setStyleSheet("color: #868e96; background: transparent; border: none; padding: 0px;")
        view_container_layout.addWidget(view_subtitle)
        
        actions_layout.addWidget(view_container)
        
        download_container = QWidget()
        download_container.setStyleSheet("background: transparent;")
        download_container_layout = QVBoxLayout(download_container)
        download_container_layout.setContentsMargins(0, 0, 0, 0)
        download_container_layout.setSpacing(0)
        download_container_layout.setAlignment(Qt.AlignTop)
        
        download_btn = QPushButton("Download Report")
        download_btn.setMinimumHeight(60)
        download_btn.setMaximumHeight(60)
        download_btn.setFont(QFont("Segoe UI", 15, QFont.Bold))
        download_btn.setCursor(Qt.PointingHandCursor)
        download_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #27ae60, stop:1 #229954);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 0px 35px;
                letter-spacing: 0.5px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #229954, stop:1 #1e8449);
            }
            QPushButton:pressed {
                background: #1e8449;
            }
        """)
        download_btn.clicked.connect(lambda checked, did=dataset.get('id'), dname=dataset.get('name', 'Unknown'): self.download_report_for_dataset(did, dname))
        download_container_layout.addWidget(download_btn)
        download_container_layout.addStretch()
        
        actions_layout.addWidget(download_container)
        
        select_container = QWidget()
        select_container.setStyleSheet("background: transparent;")
        select_container_layout = QVBoxLayout(select_container)
        select_container_layout.setContentsMargins(0, 0, 0, 0)
        select_container_layout.setSpacing(0)
        select_container_layout.setAlignment(Qt.AlignTop)
        
        select_btn = QPushButton("Select for Deletion")
        select_btn.setMinimumHeight(60)
        select_btn.setMaximumHeight(60)
        select_btn.setFont(QFont("Segoe UI", 15, QFont.Bold))
        select_btn.setCursor(Qt.PointingHandCursor)
        select_btn.setStyleSheet("""
            QPushButton {
                background: white;
                color: #e74c3c;
                border: 2px solid #e74c3c;
                border-radius: 12px;
                padding: 0px 35px;
                letter-spacing: 0.5px;
            }
            QPushButton:hover {
                background: #e74c3c;
                color: white;
            }
            QPushButton:pressed {
                background: #c0392b;
                border-color: #c0392b;
            }
        """)
        select_btn.clicked.connect(lambda checked, container=item_container, btn=select_btn: self.toggle_selection(container, btn))
        select_container_layout.addWidget(select_btn)
        select_container_layout.addStretch()
        
        actions_layout.addWidget(select_container)
        
        item_container.select_btn = select_btn
        
        main_layout.addLayout(actions_layout)
        
        return item_container
    
    def view_details(self, dataset_id):
        print(f"  Loading dataset ID: {dataset_id}")
        self.dataset_selected.emit(dataset_id)
    
    def toggle_selection(self, item_container, select_btn):
        if item_container.is_selected:
            item_container.is_selected = False
            item_container.setStyleSheet("""
                QFrame {
                    background: white;
                    border-radius: 16px;
                    border: 2px solid #dee2e6;
                }
                QFrame:hover {
                    border: 2px solid #4a90e2;
                }
            """)
            select_btn.setText("Select for Deletion")
            select_btn.setStyleSheet("""
                QPushButton {
                    background: white;
                    color: #e74c3c;
                    border: 2px solid #e74c3c;
                    border-radius: 12px;
                    padding: 0px 35px;
                    letter-spacing: 0.5px;
                }
                QPushButton:hover {
                    background: #e74c3c;
                    color: white;
                }
                QPushButton:pressed {
                    background: #c0392b;
                    border-color: #c0392b;
                }
            """)
            self.selected_dataset_id = None
            self.selected_dataset_name = None
            self.selected_item_container = None
            self.delete_btn.setEnabled(False)
            print(f"  Deselected: {item_container.dataset_name}")
        else:
            for i in range(self.list_layout.count()):
                item = self.list_layout.itemAt(i)
                if item and item.widget() and hasattr(item.widget(), 'dataset_id'):
                    widget = item.widget()
                    if widget.is_selected:
                        widget.is_selected = False
                        widget.setStyleSheet("""
                            QFrame {
                                background: white;
                                border-radius: 16px;
                                border: 2px solid #dee2e6;
                            }
                            QFrame:hover {
                                border: 2px solid #4a90e2;
                            }
                        """)
                        widget.select_btn.setText("Select for Deletion")
                        widget.select_btn.setStyleSheet("""
                            QPushButton {
                                background: white;
                                color: #e74c3c;
                                border: 2px solid #e74c3c;
                                border-radius: 12px;
                                padding: 0px 35px;
                                letter-spacing: 0.5px;
                            }
                            QPushButton:hover {
                                background: #e74c3c;
                                color: white;
                            }
                            QPushButton:pressed {
                                background: #c0392b;
                                border-color: #c0392b;
                            }
                        """)
            
            item_container.is_selected = True
            item_container.setStyleSheet("""
                QFrame {
                    background: white;
                    border-radius: 16px;
                    border: 3px solid #e74c3c;
                }
            """)
            select_btn.setText("Unselect")
            select_btn.setStyleSheet("""
                QPushButton {
                    background: #e74c3c;
                    color: white;
                    border: 2px solid #e74c3c;
                    border-radius: 12px;
                    padding: 0px 35px;
                    letter-spacing: 0.5px;
                }
                QPushButton:hover {
                    background: #c0392b;
                    border-color: #c0392b;
                }
                QPushButton:pressed {
                    background: #a93226;
                }
            """)
            self.selected_dataset_id = item_container.dataset_id
            self.selected_dataset_name = item_container.dataset_name
            self.selected_item_container = item_container
            self.delete_btn.setEnabled(True)
            print(f"  Selected: {item_container.dataset_name}")
    
    def delete_selected(self):
        if not self.selected_dataset_id:
            return
        
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete the dataset:\n\n{self.selected_dataset_name}\n\nThis action cannot be undone.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                success, message = self.api.delete_dataset(self.selected_dataset_id)
                
                if success:
                    QMessageBox.information(
                        self,
                        "Success",
                        f"Dataset deleted successfully:\n{self.selected_dataset_name}"
                    )
                    self.selected_dataset_id = None
                    self.delete_btn.setEnabled(False)
                    self.load_history()
                else:
                    QMessageBox.critical(
                        self,
                        "Error",
                        f"Failed to delete dataset:\n{message}"
                    )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"An error occurred:\n{str(e)}"
                )
    
    def download_report_for_dataset(self, dataset_id, dataset_name):
        try:
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save Report",
                f"{dataset_name}_report.pdf",
                "PDF Files (*.pdf)"
            )
            
            if file_path:
                success, message = self.api.download_report(dataset_id, file_path)
                
                if success:
                    QMessageBox.information(
                        self,
                        "Success",
                        f"Report downloaded successfully to:\n{file_path}"
                    )
                else:
                    QMessageBox.critical(
                        self,
                        "Error",
                        f"Failed to download report:\n{message}"
                    )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"An error occurred:\n{str(e)}"
            )