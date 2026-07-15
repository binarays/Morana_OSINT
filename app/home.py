from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QFrame
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon

from sub.worker import ScanWorker
from utils.story import HistoryManager

STYLESHEET = """
QWidget {
    background-color: #1e1e1e;
    color: #e0e0e0;
    font-family: 'Segoe UI', Arial, sans-serif;
}

/* Left Panel */
#leftPanel {
    background-color: #252526;
    border-right: 1px solid #333333;
}

#logoLabel {
    font-size: 20px;
    font-weight: bold;
    color: #ffffff;
    padding: 10px;
}

#newScanBtn {
    background-color: #007acc;
    color: white;
    border: none;
    padding: 10px;
    border-radius: 5px;
    font-weight: bold;
    margin: 10px;
}
#newScanBtn:hover {
    background-color: #0098ff;
}
#newScanBtn:pressed {
    background-color: #005f9e;
}

QListWidget {
    background-color: #252526;
    border: none;
    outline: none;
}
QListWidget::item {
    padding: 10px;
    border-bottom: 1px solid #333333;
}
QListWidget::item:selected {
    background-color: #37373d;
    color: #ffffff;
}

/* Right Panel Elements */
QLineEdit {
    background-color: #3c3c3c;
    border: 1px solid #555555;
    padding: 12px;
    border-radius: 6px;
    font-size: 16px;
    color: white;
}
QLineEdit:focus {
    border: 1px solid #007acc;
}

#startScanBtn {
    background-color: #007acc;
    color: white;
    border: none;
    padding: 12px 24px;
    border-radius: 6px;
    font-size: 16px;
    font-weight: bold;
}
#startScanBtn:hover {
    background-color: #0098ff;
}
#startScanBtn:disabled {
    background-color: #555555;
    color: #888888;
}

#statusLabel {
    font-size: 18px;
    color: #cccccc;
    margin-top: 20px;
}
#spinnerLabel {
    font-size: 24px;
    color: #007acc;
    font-weight: bold;
}

QTableWidget {
    background-color: #1e1e1e;
    border: 1px solid #333333;
    gridline-color: #333333;
}
QHeaderView::section {
    background-color: #2d2d30;
    padding: 8px;
    border: 1px solid #333333;
    font-weight: bold;
    color: #ffffff;
}
QTableWidget::item {
    padding: 8px;
}

/* Scrollbars */
QScrollBar:vertical {
    background-color: #000000;
    width: 7px;
    border-radius: 4px;
    margin: 0px;
}
QScrollBar::handle:vertical {
    background-color: #444444;
    border-radius: 4px;
    min-height: 30px;
}
QScrollBar::handle:vertical:hover {
    background-color: #007acc;
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
    background-color: #000000;
    height: 7px;
    border-radius: 4px;
    margin: 0px;
}
QScrollBar::handle:horizontal {
    background-color: #444444;
    border-radius: 4px;
    min-width: 30px;
}
QScrollBar::handle:horizontal:hover {
    background-color: #007acc;
}
QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal {
    width: 0px;
}
QScrollBar::add-page:horizontal,
QScrollBar::sub-page:horizontal {
    background: none;
}
"""

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Morana OSINT - Vulnerability Scanner")
        self.resize(1000, 700)
        self.setStyleSheet(STYLESHEET)
        self.history_manager = HistoryManager()
        self.current_scan_id = None
        
        self.init_ui()
        self.load_history()

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ================= LEFT PANEL =================
        self.left_panel = QFrame()
        self.left_panel.setObjectName("leftPanel")
        self.left_panel.setFixedWidth(250)
        left_layout = QVBoxLayout(self.left_panel)
        left_layout.setContentsMargins(0, 10, 0, 0)
        
        logo_label = QLabel("Morana OSINT")
        logo_label.setObjectName("logoLabel")
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.new_scan_btn = QPushButton("+ New Scan")
        self.new_scan_btn.setObjectName("newScanBtn")
        self.new_scan_btn.clicked.connect(self.show_initial_view)
        
        history_label = QLabel("  Recent Scans")
        history_label.setStyleSheet("color: #888888; font-size: 12px; margin-top: 10px;")
        
        self.history_list = QListWidget()
        self.history_list.itemClicked.connect(self.on_history_clicked)
        
        left_layout.addWidget(logo_label)
        left_layout.addWidget(self.new_scan_btn)
        left_layout.addWidget(history_label)
        left_layout.addWidget(self.history_list)
        
        # ================= RIGHT PANEL =================
        self.right_panel = QStackedWidget()
        
        # Page 0: Initial View
        self.page_initial = QWidget()
        initial_layout = QVBoxLayout(self.page_initial)
        initial_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title_label = QLabel("Start a new scan")
        title_label.setStyleSheet("font-size: 28px; font-weight: bold; margin-bottom: 20px;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        input_layout = QHBoxLayout()
        self.domain_input = QLineEdit()
        self.domain_input.setPlaceholderText("Enter domain (e.g. example.com)")
        self.domain_input.setFixedWidth(400)
        self.domain_input.returnPressed.connect(self.start_scan)
        
        self.scan_button = QPushButton("Scan")
        self.scan_button.setObjectName("startScanBtn")
        self.scan_button.clicked.connect(self.start_scan)
        
        input_layout.addStretch()
        input_layout.addWidget(self.domain_input)
        input_layout.addWidget(self.scan_button)
        input_layout.addStretch()
        
        initial_layout.addWidget(title_label)
        initial_layout.addLayout(input_layout)
        
        # Page 1: Scanning View
        self.page_scanning = QWidget()
        scanning_layout = QVBoxLayout(self.page_scanning)
        scanning_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.spinner_label = QLabel("⚙️")
        self.spinner_label.setObjectName("spinnerLabel")
        self.spinner_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.status_label = QLabel("Initializing scan...")
        self.status_label.setObjectName("statusLabel")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        scanning_layout.addWidget(self.spinner_label)
        scanning_layout.addWidget(self.status_label)
        
        # Page 2: Results View
        self.page_results = QWidget()
        results_layout = QVBoxLayout(self.page_results)
        results_layout.setContentsMargins(40, 40, 40, 40)
        
        title_layout = QHBoxLayout()
        self.target_prefix_label = QLabel("TARGET : ")
        self.target_prefix_label.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        self.target_domain_label = QLabel("")
        self.target_domain_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #007acc;")
        
        title_layout.addWidget(self.target_prefix_label)
        title_layout.addWidget(self.target_domain_label)
        title_layout.addStretch()
        
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(2)
        self.results_table.horizontalHeader().setVisible(False)
        self.results_table.verticalHeader().setVisible(False)
        self.results_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.results_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.results_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.results_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.results_table.setWordWrap(True)
        
        results_layout.addLayout(title_layout)
        results_layout.addWidget(self.results_table)
        
        # Add pages to stack
        self.right_panel.addWidget(self.page_initial)
        self.right_panel.addWidget(self.page_scanning)
        self.right_panel.addWidget(self.page_results)
        
        main_layout.addWidget(self.left_panel)
        main_layout.addWidget(self.right_panel)

    def delete_history_item(self, scan_id):
        self.history_manager.delete_scan(scan_id)
        if self.current_scan_id == scan_id:
            self.show_initial_view()
        self.load_history()

    def load_history(self):
        self.history_list.clear()
        history = self.history_manager.get_history()
        for item in reversed(history):  # Show newest first
            result_data = item.get("result", {})
            scan_time = item.get("time", "")[:16].replace("T", " ")
            title = item.get('domain', f"Scan #{item.get('scan_id', '?')}")
            
            list_item = QListWidgetItem()
            
            item_widget = QWidget()
            item_widget.setStyleSheet("background-color: transparent;")
            item_layout = QHBoxLayout(item_widget)
            item_layout.setContentsMargins(5, 5, 5, 5)
            item_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
            
            lbl_title = QLabel(title)
            lbl_title.setStyleSheet("color: #e0e0e0; font-size: 13px; font-weight: bold;")
            lbl_title.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
            lbl_time = QLabel(scan_time)
            lbl_time.setStyleSheet("color: #888888; font-size: 11px;")
            lbl_time.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
            
            lbl_layout = QVBoxLayout()
            lbl_layout.setSpacing(1)
            lbl_layout.setContentsMargins(0, 0, 0, 0)
            lbl_layout.addWidget(lbl_title)
            lbl_layout.addWidget(lbl_time)
            
            del_btn = QPushButton()
            del_btn.setIcon(QIcon("app/icons/trash_white.svg"))
            del_btn.setIconSize(QSize(18, 18))
            del_btn.setFixedSize(30, 30)
            del_btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent; 
                    border: none;
                    padding: 4px;
                }
                QPushButton:hover {
                    background-color: #3a3a3a;
                    border-radius: 6px;
                }
            """)
            del_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            # Use default argument capture for lambda in loop
            del_btn.clicked.connect(lambda _, sid=item.get("scan_id"): self.delete_history_item(sid))
            
            item_layout.addLayout(lbl_layout)
            item_layout.addStretch()
            item_layout.addWidget(del_btn)
            
            from PyQt6.QtCore import QSize as _QSize
            list_item.setSizeHint(_QSize(230, 52))
            list_item.setData(Qt.ItemDataRole.UserRole, result_data)
            list_item.setData(Qt.ItemDataRole.UserRole + 1, item.get("scan_id"))
            list_item.setData(Qt.ItemDataRole.UserRole + 2, title)
            
            self.history_list.addItem(list_item)
            self.history_list.setItemWidget(list_item, item_widget)

    def show_initial_view(self):
        self.domain_input.clear()
        self.history_list.clearSelection()
        self.right_panel.setCurrentWidget(self.page_initial)

    def on_history_clicked(self, item):
        result_data = item.data(Qt.ItemDataRole.UserRole)
        scan_id = item.data(Qt.ItemDataRole.UserRole + 1)
        domain = item.data(Qt.ItemDataRole.UserRole + 2)
        self.display_results(result_data, domain_name=domain, scan_id=scan_id)

    def start_scan(self):
        domain = self.domain_input.text().strip()
        if not domain:
            return

        self.last_scanned_domain = domain
        self.right_panel.setCurrentWidget(self.page_scanning)
        self.scan_button.setEnabled(False)
        self.status_label.setText(f"Preparing to scan {domain}...")

        self.worker = ScanWorker(domain)
        self.worker.progress.connect(self.update_status)
        self.worker.finished.connect(self.scan_finished)
        self.worker.start()

    def update_status(self, message):
        self.status_label.setText(message)

    def scan_finished(self, result):
        self.scan_button.setEnabled(True)
        if "error" in result:
            self.status_label.setText(f"Error: {result['error']}")
            return
            
        self.display_results(result, domain_name=self.last_scanned_domain)
        self.load_history()  # Refresh history list

    def display_results(self, result_dict, domain_name="", scan_id=None):
        self.current_scan_id = scan_id
        if domain_name:
            self.target_prefix_label.show()
            self.target_domain_label.setText(domain_name.upper())
        else:
            self.target_prefix_label.hide()
            self.target_domain_label.setText("SCAN RESULTS")
            
        self.results_table.setRowCount(0)
        
        row_idx = 0
        for scanner_name, details in result_dict.items():
            display_name = scanner_name
            if display_name == "DNSLookup":
                display_name = "DNS Records"
            elif display_name == "SSLLookup":
                display_name = "SSL"
            elif display_name == "WhoisLookup":
                display_name = "WHOIS"
            elif display_name == "HeaderLookup":
                display_name = "HTTP Headers"
                
            scanner_status = "success"
            if isinstance(details, dict):
                scanner_status = details.get("status", "success")

            # Add a section header for the scanner
            self.results_table.insertRow(row_idx)
            header_item = QTableWidgetItem(display_name)
            header_item.setBackground(Qt.GlobalColor.black)
            header_item.setForeground(Qt.GlobalColor.white)
            header_item.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
            self.results_table.setItem(row_idx, 0, header_item)
            
            if scanner_status == "success" or scanner_status == "Completed":
                status_item = QTableWidgetItem("🟢")
            else:
                status_item = QTableWidgetItem("🔴")
                
            status_item.setBackground(Qt.GlobalColor.black)
            self.results_table.setItem(row_idx, 1, status_item)
            row_idx += 1
            
            # Format the output logic based on the tool
            if isinstance(details, dict):
                for k, v in details.items():
                    if k in ["target", "status", "scanner"]:
                        continue
                    if isinstance(v, dict):
                        for sub_k, sub_v in v.items():
                            if isinstance(sub_v, dict):
                                # Two-level nested: e.g. security_headers
                                self.results_table.insertRow(row_idx)
                                group_item = QTableWidgetItem(str(sub_k))
                                group_item.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
                                self.results_table.setItem(row_idx, 0, group_item)
                                self.results_table.setItem(row_idx, 1, QTableWidgetItem(""))
                                row_idx += 1
                                for deep_k, deep_v in sub_v.items():
                                    self.results_table.insertRow(row_idx)
                                    self.results_table.setItem(row_idx, 0, QTableWidgetItem(f"  {deep_k}"))
                                    dv_str = str(deep_v)
                                    dv_item = QTableWidgetItem(dv_str)
                                    if dv_str.lower() == "missing":
                                        dv_item.setForeground(Qt.GlobalColor.red)
                                    elif dv_str.lower() == "present":
                                        dv_item.setForeground(Qt.GlobalColor.green)
                                    self.results_table.setItem(row_idx, 1, dv_item)
                                    row_idx += 1
                            else:
                                self.results_table.insertRow(row_idx)
                                self.results_table.setItem(row_idx, 0, QTableWidgetItem(str(sub_k)))
                                if isinstance(sub_v, list):
                                    val_str = "\n".join(map(str, sub_v))
                                else:
                                    val_str = str(sub_v)
                                val_item = QTableWidgetItem(val_str)
                                self.results_table.setItem(row_idx, 1, val_item)
                                row_idx += 1
                        continue

                    self.results_table.insertRow(row_idx)
                    self.results_table.setItem(row_idx, 0, QTableWidgetItem(str(k)))
                    
                    if isinstance(v, list):
                        v_str = "\n".join(map(str, v))
                    else:
                        v_str = str(v)
                        
                    val_item = QTableWidgetItem(v_str)
                    if v_str.lower() in ["high", "critical", "vulnerable", "invalid", "false", "failed", "expired", "certificate expired"]:
                        val_item.setForeground(Qt.GlobalColor.red)
                    elif v_str.lower() in ["certificate valid", "valid"]:
                        val_item.setForeground(Qt.GlobalColor.green)
                    self.results_table.setItem(row_idx, 1, val_item)
                    row_idx += 1
            elif isinstance(details, list):
                self.results_table.insertRow(row_idx)
                self.results_table.setItem(row_idx, 0, QTableWidgetItem("Details"))
                self.results_table.setItem(row_idx, 1, QTableWidgetItem("\n".join(map(str, details))))
                row_idx += 1
            else:
                self.results_table.insertRow(row_idx)
                self.results_table.setItem(row_idx, 0, QTableWidgetItem("Output"))
                self.results_table.setItem(row_idx, 1, QTableWidgetItem(str(details)))
                row_idx += 1
                
        self.results_table.resizeRowsToContents()
        self.right_panel.setCurrentWidget(self.page_results)