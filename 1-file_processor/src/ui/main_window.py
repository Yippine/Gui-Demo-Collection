from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, 
                             QTextEdit, QLineEdit, QComboBox, QLabel, QFileDialog, QMessageBox,
                             QApplication, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QIcon, QColor, QLinearGradient, QPainter
from .custom_widgets import CollapsibleBox, RegexToggleLineEdit
from src.core.file_processor import FileProcessor
from src.core.directory_reader import DirectoryReader
from src.utils.config import Config
from src.utils.language_presets import LanguagePresets

class WoodButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFont(QFont("微軟正黑體", 12, QFont.Bold))
        self.setCursor(Qt.PointingHandCursor)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor("#E6C9A8"))
        gradient.setColorAt(0.5, QColor("#D4A76A"))
        gradient.setColorAt(1, QColor("#C38D4E"))

        painter.setBrush(gradient)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10)

        if self.isDown():
            painter.setOpacity(0.3)
            painter.setBrush(Qt.black)
            painter.drawRoundedRect(self.rect(), 10, 10)

        painter.setPen(QColor("#4A3C31"))
        painter.drawText(self.rect(), Qt.AlignCenter, self.text())

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Processor檔案處理器 2.0")
        self.setGeometry(100, 100, 1200, 900)
        self.file_processor = FileProcessor()
        self.directory_reader = DirectoryReader()
        self.config = Config()
        self.language_presets = LanguagePresets()

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)

        # 頂部控制區域
        top_controls = QHBoxLayout()
        top_controls.setSpacing(15)
        
        self.project_dir = QLineEdit()
        self.project_dir.setPlaceholderText("專案目錄")
        self.project_dir.setFont(QFont("微軟正黑體", 12))
        self.project_dir.setStyleSheet("""
            QLineEdit {
                background-color: #F5DEB3;
                border: 2px solid #D4A76A;
                border-radius: 5px;
                padding: 5px;
                color: #4A3C31;
            }
        """)
        top_controls.addWidget(self.project_dir)

        browse_button = WoodButton("瀏覽")
        browse_button.clicked.connect(self.browse_directory)
        top_controls.addWidget(browse_button)

        self.language_selector = QComboBox()
        self.language_selector.setFont(QFont("微軟正黑體", 12))
        self.language_selector.addItem("選擇語言")
        self.language_selector.addItems(self.language_presets.get_supported_languages())
        self.language_selector.currentTextChanged.connect(self.update_language_presets)
        self.language_selector.setFixedWidth(150)
        self.language_selector.setStyleSheet("""
            QComboBox {
                background-color: #F5DEB3;
                border: 2px solid #D4A76A;
                border-radius: 5px;
                padding: 5px;
                color: #4A3C31;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 25px;
                border-left: none;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }
            QComboBox::down-arrow {
                image: url(path/to/down_arrow.png);
            }
        """)
        top_controls.addWidget(self.language_selector)

        main_layout.addLayout(top_controls)

        # 可摺疊設定區域
        settings_box = CollapsibleBox("設定")
        settings_box.toggle_button.setFont(QFont("微軟正黑體", 30, QFont.Bold))
        settings_box.toggle_button.setStyleSheet("""
            QPushButton {
                background-color: #E6C9A8;
                color: #4A3C31;
                border: none;
                padding: 10px;
                font-size: 30px;
                font-weight: bold;
            }
            QPushButton:checked {
                background-color: #D4A76A;
            }
        """)
        settings_layout = QVBoxLayout()
        settings_layout.setSpacing(15)

        for widget_name, placeholder in [
            ("exclude_dirs", "排除目錄（用逗號分隔）"),
            ("exclude_files", "排除檔案（用逗號分隔）"),
            ("include_files", "保留檔案（用逗號分隔）")
        ]:
            setattr(self, widget_name, RegexToggleLineEdit())
            widget = getattr(self, widget_name)
            widget.setFont(QFont("微軟正黑體", 12))
            widget.setPlaceholderText(placeholder)
            widget.line_edit.setStyleSheet("""
                QLineEdit {
                    background-color: #F5DEB3;
                    border: 2px solid #D4A76A;
                    border-radius: 5px;
                    padding: 5px;
                    color: #4A3C31;
                }
            """)
            widget.regex_button.setStyleSheet("""
                QPushButton {
                    background-color: #E6C9A8;
                    border: none;
                    border-radius: 15px;
                }
                QPushButton:checked {
                    background-color: #C38D4E;
                }
            """)
            label = QLabel(placeholder.split("（")[0])
            label.setFont(QFont("微軟正黑體", 12))
            settings_layout.addWidget(label)
            settings_layout.addWidget(widget)

        settings_box.setContentLayout(settings_layout)
        main_layout.addWidget(settings_box)

        # 按鈕區域
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)

        for button_text, slot in [
            ("讀取目錄", self.read_directory),
            ("讀取程式", self.read_code)
        ]:
            button = WoodButton(button_text)
            button.clicked.connect(slot)
            button_layout.addWidget(button)

        main_layout.addLayout(button_layout)

        # 結果顯示區域
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setFont(QFont("Courier", 12))
        self.result_text.setStyleSheet("""
            QTextEdit {
                background-color: #F5DEB3;
                border: 2px solid #D4A76A;
                border-radius: 5px;
                padding: 5px;
                color: #4A3C31;
            }
        """)
        main_layout.addWidget(self.result_text)

        # 底部按鈕區域
        bottom_buttons = QHBoxLayout()
        bottom_buttons.setSpacing(20)

        for button_text, slot in [
            ("清空結果", self.clear_result),
            ("複製結果", self.copy_result),
            ("儲存結果", self.save_result)
        ]:
            button = WoodButton(button_text)
            button.clicked.connect(slot)
            bottom_buttons.addWidget(button)

        main_layout.addLayout(bottom_buttons)

        # 為主佈局添加一些邊距
        main_layout.setContentsMargins(20, 20, 20, 20)

    def animate_button(self, button):
        animation = QPropertyAnimation(button, b"geometry")
        animation.setEasingCurve(QEasingCurve.OutBounce)
        animation.setDuration(300)
        start = button.geometry()
        animation.setStartValue(start)
        animation.setEndValue(start)
        animation.setKeyValueAt(0.3, start.adjusted(0, 10, 0, 10))
        animation.start()

    def browse_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "選擇專案目錄")
        if directory:
            self.project_dir.setText(directory)
        self.animate_button(self.sender())

    def update_language_presets(self, language):
        if language != "選擇語言":
            presets = self.language_presets.get_presets(language)
            self.exclude_dirs.setText(", ".join(presets.get("exclude_dirs", [])))
            self.exclude_files.setText(", ".join(presets.get("exclude_files", [])))
            self.include_files.setText(", ".join(presets.get("include_files", [])))
        else:
            self.exclude_dirs.clear()
            self.exclude_files.clear()
            self.include_files.clear()

    def read_directory(self):
        project_dir = self.project_dir.text()
        if not project_dir:
            QMessageBox.warning(self, "錯誤", "請選擇項目目錄")
            return

        exclude_dirs = [d.strip() for d in self.exclude_dirs.text().split(",") if d.strip()]
        exclude_files = [f.strip() for f in self.exclude_files.text().split(",") if f.strip()]
        include_files = [f.strip() for f in self.include_files.text().split(",") if f.strip()]

        tree = self.directory_reader.read_directory(
            project_dir, 
            exclude_dirs, 
            exclude_files, 
            include_files,
            self.exclude_dirs.is_regex(),
            self.exclude_files.is_regex(),
            self.include_files.is_regex()
        )
        self.result_text.setPlainText(tree)
        self.animate_button(self.sender())

    def read_code(self):
        project_dir = self.project_dir.text()
        if not project_dir:
            QMessageBox.warning(self, "錯誤", "請選擇項目目錄")
            return

        exclude_dirs = [d.strip() for d in self.exclude_dirs.text().split(",") if d.strip()]
        exclude_files = [f.strip() for f in self.exclude_files.text().split(",") if f.strip()]
        include_files = [f.strip() for f in self.include_files.text().split(",") if f.strip()]

        result = self.file_processor.process_files(
            project_dir, 
            exclude_dirs, 
            exclude_files, 
            include_files,
            self.exclude_dirs.is_regex(),
            self.exclude_files.is_regex(),
            self.include_files.is_regex()
        )
        prompt = f"""請透過大量的官方網站或網路資訊，為我查詢這項最推薦的具體步驟指引。你已經是經營這個領域幾十年的專家，請直接告訴我最簡單、最有效、最系統和最全面的解答，以及你的心路歷程：

\"\"\"你已經是經營這個領域幾十年的 IT 專家，請直接告訴我最簡潔、最有效能且最精美的程式碼範例和最簡單、最有效、最系統且最全面的解答，以及你的心路歷程，感謝您：

\"\"\"
{result.rstrip()}

請以業界的最佳實現來完美修復，並重複審視，排除所有潛在的漏洞、風險和臭蟲。  
提供新增或異動過的應用目錄名稱、檔案名稱、程式內容；
同時，提供應用的安裝、建置和運行指令或方式，謝謝。\"\"\"\"\"\""""
        self.result_text.setPlainText(prompt)
        self.animate_button(self.sender())

    def clear_result(self):
        self.result_text.clear()
        self.animate_button(self.sender())

    def copy_result(self):
        result = self.result_text.toPlainText().rstrip()
        QApplication.clipboard().setText(result)
        self.animate_button(self.sender())

    def save_result(self):
        result = self.result_text.toPlainText().rstrip()
        file_name, _ = QFileDialog.getSaveFileName(self, "儲存結果", "", "文字檔 (*.txt);;所有檔案 (*)")
        if file_name:
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write(result)
        self.animate_button(self.sender())
