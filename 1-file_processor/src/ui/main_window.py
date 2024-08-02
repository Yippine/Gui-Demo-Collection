from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QTextEdit, QLineEdit, QComboBox, QLabel, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt
from src.ui.custom_widgets import CollapsibleBox, RegexToggleLineEdit
from src.core.file_processor import FileProcessor
from src.core.directory_reader import DirectoryReader
from src.utils.config import Config
from src.utils.language_presets import LanguagePresets

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Processor 2.0")
        self.setGeometry(100, 100, 800, 600)
        self.file_processor = FileProcessor()
        self.directory_reader = DirectoryReader()
        self.config = Config()
        self.language_presets = LanguagePresets()

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        # 頂部控制區
        top_controls = QHBoxLayout()
        
        self.project_dir = QLineEdit()
        self.project_dir.setPlaceholderText("項目目錄")
        top_controls.addWidget(self.project_dir)

        browse_button = QPushButton("瀏覽")
        browse_button.clicked.connect(self.browse_directory)
        top_controls.addWidget(browse_button)

        self.language_selector = QComboBox()
        self.language_selector.addItem("--")
        self.language_selector.addItems(self.language_presets.get_supported_languages())
        self.language_selector.currentTextChanged.connect(self.update_language_presets)
        top_controls.addWidget(self.language_selector)

        main_layout.addLayout(top_controls)

        # 可折疊的設置區
        settings_box = CollapsibleBox("設置")
        settings_layout = QVBoxLayout()

        self.exclude_dirs = RegexToggleLineEdit()
        self.exclude_dirs.setPlaceholderText("排除目錄 (用逗號分隔)")
        settings_layout.addWidget(QLabel("排除目錄:"))
        settings_layout.addWidget(self.exclude_dirs)

        self.exclude_files = RegexToggleLineEdit()
        self.exclude_files.setPlaceholderText("排除文件 (用逗號分隔)")
        settings_layout.addWidget(QLabel("排除文件:"))
        settings_layout.addWidget(self.exclude_files)

        self.include_files = RegexToggleLineEdit()
        self.include_files.setPlaceholderText("保留文件 (用逗號分隔)")
        settings_layout.addWidget(QLabel("保留文件:"))
        settings_layout.addWidget(self.include_files)

        settings_box.setContentLayout(settings_layout)
        main_layout.addWidget(settings_box)

        # 按鈕區
        button_layout = QHBoxLayout()
        read_dir_button = QPushButton("讀取目錄")
        read_dir_button.clicked.connect(self.read_directory)
        button_layout.addWidget(read_dir_button)

        read_code_button = QPushButton("讀取程式")
        read_code_button.clicked.connect(self.read_code)
        button_layout.addWidget(read_code_button)

        main_layout.addLayout(button_layout)

        # 結果顯示區
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        main_layout.addWidget(self.result_text)

        # 底部按鈕區
        bottom_buttons = QHBoxLayout()
        clear_button = QPushButton("清空結果")
        clear_button.clicked.connect(self.clear_result)
        bottom_buttons.addWidget(clear_button)

        copy_button = QPushButton("複製結果")
        copy_button.clicked.connect(self.copy_result)
        bottom_buttons.addWidget(copy_button)

        save_button = QPushButton("保存結果")
        save_button.clicked.connect(self.save_result)
        bottom_buttons.addWidget(save_button)

        main_layout.addLayout(bottom_buttons)

    def browse_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "選擇項目目錄")
        if directory:
            self.project_dir.setText(directory)

    def update_language_presets(self, language):
        if language != "--":
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

        exclude_dirs = self.exclude_dirs.text().split(",") if self.exclude_dirs.text() else []
        exclude_files = self.exclude_files.text().split(",") if self.exclude_files.text() else []
        include_files = self.include_files.text().split(",") if self.include_files.text() else []

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

    def read_code(self):
        project_dir = self.project_dir.text()
        if not project_dir:
            QMessageBox.warning(self, "錯誤", "請選擇項目目錄")
            return

        exclude_dirs = self.exclude_dirs.text().split(",") if self.exclude_dirs.text() else []
        exclude_files = self.exclude_files.text().split(",") if self.exclude_files.text() else []
        include_files = self.include_files.text().split(",") if self.include_files.text() else []

        result = self.file_processor.process_files(
            project_dir, 
            exclude_dirs, 
            exclude_files, 
            include_files,
            self.exclude_dirs.is_regex(),
            self.exclude_files.is_regex(),
            self.include_files.is_regex()
        )
        self.result_text.setPlainText(result)

    def clear_result(self):
        self.result_text.clear()

    def copy_result(self):
        result = self.result_text.toPlainText().rstrip()
        QApplication.clipboard().setText(result)

    def save_result(self):
        result = self.result_text.toPlainText().rstrip()
        file_name, _ = QFileDialog.getSaveFileName(self, "保存結果", "", "Text Files (*.txt);;All Files (*)")
        if file_name:
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write(result)