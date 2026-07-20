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
    QFrame,
    QRadioButton
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon, QColor

from sub.worker import ScanWorker
from utils.story import HistoryManager

STYLESHEET = """
QWidget {
    background-color: #1e1e1e;
    color: #e0e0e0;
    font-family: 'Poppins', 'Segoe UI', Arial, sans-serif;
}

/* Left Panel */
#leftPanel, #leftPanel QWidget {
    background-color: #252526;
}
#leftPanel {
    border-right: 1px solid #333333;
}

#logoLabel {
    font-size: 20px;
    font-weight: bold;
    color: #ffffff;
    padding: 10px;
}

#newScanBtn {
    background-color: transparent;
    color: white;
    border: none;
    padding: 10px;
    padding-left: 15px;
    text-align: left;
    font-size: 14px;
    border-radius: 0px;
    font-weight: normal;
    margin: 5px;
}
#newScanBtn:hover {
    background-color: #2d2d30;
}
#newScanBtn:pressed {
    background-color: #37373d;
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
QListWidget::item:hover {
    background-color: #2d2d30;
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
    border-radius: 0px;
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
    padding: 10px 15px;
    border-radius: 0px;
    font-size: 14px;
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
    font-size: 13px;
    color: #888888;
    margin-top: 20px;
    font-style: italic;
}

QRadioButton {
    font-size: 12px;
    color: #cccccc;
}
QRadioButton::indicator {
    width: 12px;
    height: 12px;
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

QRadioButton {
    color: #e0e0e0;
    font-size: 14px;
}
QRadioButton::indicator {
    width: 16px;
    height: 16px;
    border-radius: 8px;
    border: 2px solid #555555;
    background-color: transparent;
}
QRadioButton::indicator:checked {
    background-color: #007acc;
    border: 4px solid #1e1e1e;
}
QRadioButton::indicator:hover {
    border: 2px solid #007acc;
}
"""

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Morana")
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
        
        title_container = QWidget()
        title_hlayout = QHBoxLayout(title_container)
        title_hlayout.setContentsMargins(15, 0, 15, 0)
        
        from PyQt6.QtGui import QPixmap
        logo_png = QLabel()
        logo_pixmap = QPixmap("app/icons/morana-logo.png")
        logo_png.setPixmap(logo_pixmap.scaled(28, 28, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        logo_png.setFixedSize(28, 28)
        
        logo_label = QLabel("")
        logo_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #ffffff;")
        
        from PyQt6.QtSvgWidgets import QSvgWidget
        burger_btn = QSvgWidget("app/icons/burger-menu.svg")
        burger_btn.setFixedSize(20, 20)
        burger_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        
        title_hlayout.addWidget(logo_png)
        title_hlayout.addWidget(logo_label)
        title_hlayout.addStretch()
        title_hlayout.addWidget(burger_btn)
        
        left_layout.addWidget(title_container)
        
        # horizontal separator below header
        header_separator = QFrame()
        header_separator.setFrameShape(QFrame.Shape.HLine)
        header_separator.setFixedHeight(1)
        header_separator.setStyleSheet("background-color: #2a2a2a; border: none; margin: 8px 0px 0px 0px;")
        left_layout.addWidget(header_separator)
        
        self.new_scan_btn = QPushButton("  Scan Now")
        from PyQt6.QtGui import QIcon
        self.new_scan_btn.setIcon(QIcon("app/icons/scan-white.svg"))
        self.new_scan_btn.setObjectName("newScanBtn")
        self.new_scan_btn.clicked.connect(self.show_initial_view)
        self.new_scan_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        
        history_header_widget = QWidget()
        history_header_layout = QHBoxLayout(history_header_widget)
        history_header_layout.setContentsMargins(10, 10, 15, 6)
        
        history_label = QLabel("History")
        history_label.setStyleSheet("color: #ffffff; font-size: 12px; font-weight: normal;")
        
        from PyQt6.QtSvgWidgets import QSvgWidget
        history_icon = QSvgWidget("app/icons/history.svg")
        history_icon.setFixedSize(16, 16)
        
        history_header_layout.addWidget(history_label)
        history_header_layout.addStretch()
        history_header_layout.addWidget(history_icon)
        
        self.history_list = QListWidget()
        self.history_list.itemClicked.connect(self.on_history_clicked)
        self.history_list.setCursor(Qt.CursorShape.PointingHandCursor)
        
        legal_container = QWidget()
        legal_hlayout = QHBoxLayout(legal_container)
        legal_hlayout.setContentsMargins(0, 0, 15, 0)
        
        self.legal_btn = QPushButton("Legal information")
        self.legal_btn.setStyleSheet("background: transparent; color: #666666; border: none; font-size: 11px; text-align: left; padding: 15px;")
        self.legal_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.legal_btn.clicked.connect(self.show_legal_view)
        
        version_label = QLabel("Version 1.0")
        version_label.setStyleSheet("color: #666666; font-size: 11px;")
        
        legal_hlayout.addWidget(self.legal_btn)
        legal_hlayout.addStretch()
        legal_hlayout.addWidget(version_label)
        
        
        left_layout.addWidget(self.new_scan_btn)
        
        sep1 = QFrame()
        sep1.setFrameShape(QFrame.Shape.HLine)
        sep1.setFixedHeight(1)
        sep1.setStyleSheet("background-color: #2a2a2a; border: none;")
        left_layout.addWidget(sep1)
        
        left_layout.addWidget(history_header_widget)
        left_layout.addWidget(self.history_list)
        
        sep2 = QFrame()
        sep2.setFrameShape(QFrame.Shape.HLine)
        sep2.setFixedHeight(1)
        sep2.setStyleSheet("background-color: #2a2a2a; border: none;")
        left_layout.addWidget(sep2)
        
        left_layout.addWidget(legal_container)
        
        # ================= RIGHT PANEL =================
        self.right_panel = QStackedWidget()
        
        # Page 0: Initial View
        self.page_initial = QWidget()
        initial_layout = QVBoxLayout(self.page_initial)
        initial_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        from datetime import datetime
        _hour = datetime.now().hour
        if _hour < 12:
            _greeting = "Good Morning, Traveler!"
        elif _hour < 17:
            _greeting = "Good Afternoon, Traveler!"
        elif _hour < 21:
            _greeting = "Good Evening, Traveler!"
        else:
            _greeting = "Good Night, Traveler!"
        
        title_label = QLabel(_greeting)
        title_label.setStyleSheet("font-size: 28px; font-weight: normal; margin-bottom: 20px;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        center_container = QWidget()
        center_container.setFixedWidth(500)
        center_layout = QVBoxLayout(center_container)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(15)
        
        self.domain_input = QLineEdit()
        self.domain_input.setPlaceholderText("Enter domain (e.g. example.com)")
        self.domain_input.returnPressed.connect(self.start_scan)
        center_layout.addWidget(self.domain_input)
        
        controls_layout = QHBoxLayout()
        
        self.scan_method_label = QLabel("Port scan Type: ")
        self.scan_method_label.setStyleSheet("color: #cccccc; font-size: 12px; margin-right: 10px;")
        
        self.quick_scan_radio = QRadioButton("Quick Scan")
        self.quick_scan_radio.setChecked(True)
        self.full_scan_radio = QRadioButton("Full Scan")
        
        self.scan_button = QPushButton("  Scan Now")
        self.scan_button.setIcon(QIcon("app/icons/scan-white.svg"))
        self.scan_button.setIconSize(QSize(16, 16))
        self.scan_button.setObjectName("startScanBtn")
        self.scan_button.clicked.connect(self.start_scan)
        self.scan_button.setCursor(Qt.CursorShape.PointingHandCursor)
        
        controls_layout.addWidget(self.scan_method_label)
        controls_layout.addWidget(self.quick_scan_radio)
        controls_layout.addWidget(self.full_scan_radio)
        controls_layout.addStretch()
        controls_layout.addWidget(self.scan_button)
        
        center_layout.addLayout(controls_layout)
        
        initial_layout.addStretch()
        initial_layout.addWidget(title_label)
        initial_layout.addWidget(center_container, alignment=Qt.AlignmentFlag.AlignCenter)
        initial_layout.addStretch()
        
        # Page 1: Scanning View
        self.page_scanning = QWidget()
        scanning_layout = QVBoxLayout(self.page_scanning)
        scanning_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.status_label = QLabel("Initializing scan...")
        self.status_label.setObjectName("statusLabel")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        scanning_layout.addWidget(self.status_label)
        
        # Page 2: Results View
        self.page_results = QWidget()
        results_layout = QVBoxLayout(self.page_results)
        results_layout.setContentsMargins(40, 40, 40, 40)
        
        title_layout = QHBoxLayout()
        self.target_prefix_label = QLabel("TARGET : ")
        self.target_prefix_label.setStyleSheet("font-size: 15px; font-weight: bold; color: #888888;")
        self.target_domain_label = QLabel("")
        self.target_domain_label.setStyleSheet("font-size: 15px; font-weight: bold; color: #007acc;")
        
        title_layout.addWidget(self.target_prefix_label)
        title_layout.addWidget(self.target_domain_label)
        title_layout.addStretch()
        
        self.btn_show_results = QPushButton("Results")
        self.btn_show_findings = QPushButton("Vulnerabilities & Risks")
        
        self.active_tab_style = "background-color: #007acc; color: white; border-radius: 0px; padding: 8px 15px; font-weight: normal;"
        self.inactive_tab_style = "background-color: #2d2d2d; color: #aaaaaa; border-radius: 0px; padding: 8px 15px; font-weight: normal;"
        
        self.btn_show_results.setStyleSheet(self.active_tab_style)
        self.btn_show_findings.setStyleSheet(self.inactive_tab_style)
        self.btn_show_results.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_show_findings.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.btn_show_results.clicked.connect(self.show_results_tab)
        self.btn_show_findings.clicked.connect(self.show_findings_tab)
        
        title_layout.addWidget(self.btn_show_results)
        title_layout.addWidget(self.btn_show_findings)
        
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(2)
        self.results_table.horizontalHeader().setVisible(False)
        self.results_table.verticalHeader().setVisible(False)
        self.results_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.results_table.setColumnWidth(0, 220)
        self.results_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.results_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.results_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.results_table.setWordWrap(True)
        
        self.findings_table = QTableWidget()
        self.findings_table.setColumnCount(4)
        self.findings_table.setHorizontalHeaderLabels(["Vulnerability / Risk", "Category", "Risk Level", "Description"])
        self.findings_table.horizontalHeader().setVisible(True)
        self.findings_table.verticalHeader().setVisible(False)
        self.findings_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.findings_table.setColumnWidth(0, 220)
        self.findings_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        self.findings_table.setColumnWidth(1, 150)
        self.findings_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        self.findings_table.setColumnWidth(2, 100)
        self.findings_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.findings_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.findings_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.findings_table.setWordWrap(True)
        
        self.tables_stack = QStackedWidget()
        self.tables_stack.addWidget(self.results_table)
        self.tables_stack.addWidget(self.findings_table)
        
        results_layout.addLayout(title_layout)
        results_layout.addWidget(self.tables_stack)
        
        # Page 3: Legal Info
        self.page_legal = QWidget()
        legal_layout = QVBoxLayout(self.page_legal)
        legal_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        legal_title = QLabel("Legal Information")
        legal_title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        legal_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        legal_text = QLabel(
            "We don't collect anyone's personal information.\n"
            "We only use publicly available resources to gather information about the target.\n\n"
            "Please do not use these tools to harm anyone or perform malicious activities."
        )
        legal_text.setStyleSheet("font-size: 14px; color: #cccccc; line-height: 1.5;")
        legal_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.btn_legal_back = QPushButton(" Back to Scanner")
        self.btn_legal_back.setIcon(QIcon("app/icons/back.svg"))
        self.btn_legal_back.setStyleSheet("background-color: transparent; color: #007acc; font-weight: bold; border: 1px solid #007acc; padding: 10px 20px; font-size: 14px;")
        self.btn_legal_back.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_legal_back.clicked.connect(self.show_initial_view)
        
        legal_layout.addStretch()
        legal_layout.addWidget(legal_title)
        legal_layout.addWidget(legal_text)
        legal_layout.addWidget(self.btn_legal_back, alignment=Qt.AlignmentFlag.AlignCenter)
        legal_layout.addStretch()

        # Add pages to stack
        self.right_panel.addWidget(self.page_initial)
        self.right_panel.addWidget(self.page_scanning)
        self.right_panel.addWidget(self.page_results)
        self.right_panel.addWidget(self.page_legal)
        
        main_layout.addWidget(self.left_panel)
        main_layout.addWidget(self.right_panel)
    def show_legal_view(self):
        self.right_panel.setCurrentWidget(self.page_legal)

    def show_results_tab(self):
        self.tables_stack.setCurrentWidget(self.results_table)
        self.btn_show_results.setStyleSheet(self.active_tab_style)
        self.btn_show_findings.setStyleSheet(self.inactive_tab_style)

    def show_findings_tab(self):
        self.tables_stack.setCurrentWidget(self.findings_table)
        self.btn_show_results.setStyleSheet(self.inactive_tab_style)
        self.btn_show_findings.setStyleSheet(self.active_tab_style)

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

        port_scan_type = "full" if self.full_scan_radio.isChecked() else "quick"

        self.worker = ScanWorker(domain, port_scan_type)
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
            
        import re
        def format_key(key):
            if not isinstance(key, str): key = str(key)
            key = re.sub(r'[^a-zA-Z0-9\s]', ' ', key.replace('_', ' '))
            key = " ".join(key.split())
            if key: return key[0].upper() + key[1:].lower()
            return key

        def create_value_widget(val):
            if isinstance(val, dict):
                html = "<table cellpadding='2'>"
                for k, v in val.items():
                    html += f"<tr><td style='color:#aaaaaa; padding-right:15px; font-weight:bold;'>{format_key(k)}</td><td>{v}</td></tr>"
                html += "</table>"
                lbl = QLabel(html)
                lbl.setWordWrap(True)
                lbl.setStyleSheet("background: transparent;")
                return lbl
            elif isinstance(val, list) and any(isinstance(i, dict) for i in val):
                html = ""
                for item in val:
                    if isinstance(item, dict):
                        html += "<table cellpadding='2' style='margin-bottom:8px; border-bottom:1px solid #333; width:100%;'>"
                        for k, v in item.items():
                            html += f"<tr><td style='color:#aaaaaa; padding-right:15px; font-weight:bold; width:120px;'>{format_key(k)}</td><td>{v}</td></tr>"
                        html += "</table>"
                    else:
                        html += f"<div style='margin-bottom:8px;'>{item}</div>"
                lbl = QLabel(html)
                lbl.setWordWrap(True)
                lbl.setStyleSheet("background: transparent;")
                return lbl
            return None

        def format_value(val):
            if isinstance(val, list):
                return "\n".join(map(str, val))
            return str(val)

        self.results_table.setRowCount(0)
        self.findings_table.setRowCount(0)
        self.show_results_tab()
        
        scanner_order = {
            "DNSLookup": 1,
            "SSLLookup": 2,
            "QuickPortLookup": 3,
            "FullPortLookup": 3,
            "HeaderLookup": 4,
            "WhoisLookup": 5,
            "TechLookup": 6,
            "RobotsLookup": 7,
            "SitemapLookup": 8,
            "Crawler": 9
        }
        
        ordered_results = sorted(result_dict.items(), key=lambda x: scanner_order.get(x[0], 99))
        
        row_idx = 0
        findings_row_idx = 0
        for scanner_name, details in ordered_results:
            if scanner_name == "Findings":
                if not details:
                    self.findings_table.insertRow(findings_row_idx)
                    self.findings_table.setItem(findings_row_idx, 0, QTableWidgetItem("No vulnerabilities or risks found"))
                    for c in range(1, 4): self.findings_table.setItem(findings_row_idx, c, QTableWidgetItem(""))
                    findings_row_idx += 1
                    continue
                    
                for finding in details:
                    self.findings_table.insertRow(findings_row_idx)
                    title = finding.get("title", "")
                    category = finding.get("category", "")
                    severity = finding.get("severity", "")
                    desc = finding.get("description", "")
                    
                    self.findings_table.setItem(findings_row_idx, 0, QTableWidgetItem(title))
                    self.findings_table.setItem(findings_row_idx, 1, QTableWidgetItem(category))
                    
                    sev_item = QTableWidgetItem(severity)
                    if severity.lower() in ["high", "critical"]:
                        sev_item.setForeground(Qt.GlobalColor.red)
                    elif severity.lower() == "medium":
                        sev_item.setForeground(QColor("orange"))
                    elif severity.lower() == "low":
                        sev_item.setForeground(Qt.GlobalColor.green)
                        
                    self.findings_table.setItem(findings_row_idx, 2, sev_item)
                    self.findings_table.setItem(findings_row_idx, 3, QTableWidgetItem(desc))
                    findings_row_idx += 1
                continue

            display_name = scanner_name
            if display_name == "DNSLookup":
                display_name = "DNS Records"
            elif display_name == "SSLLookup":
                display_name = "SSL"
            elif display_name == "WhoisLookup":
                display_name = "WHOIS"
            elif display_name == "HeaderLookup":
                display_name = "HTTP Headers"
                
            # Add a section header for the scanner
            self.results_table.insertRow(row_idx)
            header_item = QTableWidgetItem(display_name)
            header_item.setBackground(Qt.GlobalColor.black)
            header_item.setForeground(Qt.GlobalColor.white)
            header_item.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
            self.results_table.setItem(row_idx, 0, header_item)
            self.results_table.setSpan(row_idx, 0, 1, 2)
            row_idx += 1
            
            # Format the output logic based on the tool
            if isinstance(details, dict):
                for k, v in details.items():
                    if k in ["target", "status", "scanner"]:
                        continue
                    if v in [None, "", [], {}]:
                        continue
                    if isinstance(v, dict):
                        for sub_k, sub_v in v.items():
                            if sub_v in [None, "", [], {}]:
                                continue
                            if sub_k == "forms":
                                continue
                            if sub_k == "page_details" and isinstance(sub_v, dict):
                                new_sub_v = {}
                                for url, info in sub_v.items():
                                    if isinstance(info, dict) and "status_code" in info:
                                        code = info["status_code"]
                                        if code == 200: text = "<span style='color:#00ff00;'>200 - OK (Available)</span>"
                                        elif code == 404: text = "<span style='color:#ff0000;'>404 - Not Found</span>"
                                        elif code == 403: text = "<span style='color:#ff0000;'>403 - Forbidden</span>"
                                        elif code >= 500: text = f"<span style='color:#ff0000;'>{code} - Server Error</span>"
                                        elif str(code).startswith('3'): text = f"<span style='color:#ffa500;'>{code} - Redirect</span>"
                                        else: text = str(code)
                                        new_sub_v[url] = text
                                    else:
                                        new_sub_v[url] = str(info)
                                sub_v = new_sub_v
                                
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
                                    if "<span" in dv_str or "<div" in dv_str:
                                        lbl = QLabel(dv_str)
                                        lbl.setWordWrap(True)
                                        lbl.setStyleSheet("background: transparent;")
                                        self.results_table.setItem(row_idx, 1, QTableWidgetItem(""))
                                        self.results_table.setCellWidget(row_idx, 1, lbl)
                                    else:
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
                                widget = create_value_widget(sub_v)
                                if widget:
                                    self.results_table.setItem(row_idx, 1, QTableWidgetItem(""))
                                    self.results_table.setCellWidget(row_idx, 1, widget)
                                else:
                                    val_str = format_value(sub_v)
                                    val_item = QTableWidgetItem(val_str)
                                    self.results_table.setItem(row_idx, 1, val_item)
                                row_idx += 1
                        continue

                    self.results_table.insertRow(row_idx)
                    self.results_table.setItem(row_idx, 0, QTableWidgetItem(str(k)))
                    
                    widget = create_value_widget(v)
                    if widget:
                        self.results_table.setItem(row_idx, 1, QTableWidgetItem(""))
                        self.results_table.setCellWidget(row_idx, 1, widget)
                    else:
                        v_str = format_value(v)
                        val_item = QTableWidgetItem(v_str)
                        if v_str.lower() in ["high", "critical", "vulnerable", "invalid", "false", "failed", "expired", "certificate expired"]:
                            val_item.setForeground(Qt.GlobalColor.red)
                        elif v_str.lower() in ["certificate valid", "valid"]:
                            val_item.setForeground(Qt.GlobalColor.green)
                        self.results_table.setItem(row_idx, 1, val_item)
                    row_idx += 1
            elif isinstance(details, list):
                if not details: continue
                self.results_table.insertRow(row_idx)
                self.results_table.setItem(row_idx, 0, QTableWidgetItem("Details"))
                widget = create_value_widget(details)
                if widget:
                    self.results_table.setItem(row_idx, 1, QTableWidgetItem(""))
                    self.results_table.setCellWidget(row_idx, 1, widget)
                else:
                    self.results_table.setItem(row_idx, 1, QTableWidgetItem(format_value(details)))
                row_idx += 1
            else:
                if details in [None, "", [], {}]: continue
                self.results_table.insertRow(row_idx)
                self.results_table.setItem(row_idx, 0, QTableWidgetItem("Output"))
                widget = create_value_widget(details)
                if widget:
                    self.results_table.setItem(row_idx, 1, QTableWidgetItem(""))
                    self.results_table.setCellWidget(row_idx, 1, widget)
                else:
                    self.results_table.setItem(row_idx, 1, QTableWidgetItem(format_value(details)))
                row_idx += 1
                
        self.results_table.resizeRowsToContents()
        self.findings_table.resizeRowsToContents()
        self.right_panel.setCurrentWidget(self.page_results)