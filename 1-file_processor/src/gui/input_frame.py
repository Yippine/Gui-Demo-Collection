import tkinter as tk
from tkinter import ttk, filedialog
from src.config.language_configs import LANGUAGE_CONFIGS

class InputFrame(ttk.LabelFrame):
    def __init__(self, parent, process_callback):
        super().__init__(parent, text="設定", padding="20")
        self.process_callback = process_callback
        self.columnconfigure(1, weight=1)
        self.create_widgets()
        
    def create_widgets(self):
        # Project directory
        ttk.Label(self, text="專案目錄：").grid(row=0, column=0, sticky=tk.W, pady=10)
        self.root_dir = ttk.Entry(self)
        self.root_dir.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=10)
        ttk.Button(self, text="瀏覽", command=self.browse_directory).grid(row=0, column=2, padx=(10, 0), pady=10)
        
        # Language selection
        ttk.Label(self, text="程式語言：").grid(row=1, column=0, sticky=tk.W, pady=10)
        self.language_var = tk.StringVar(value="Please Select Language")
        self.language_combo = ttk.Combobox(self, textvariable=self.language_var, values=list(LANGUAGE_CONFIGS.keys()))
        self.language_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=10)
        self.language_combo.bind("<<ComboboxSelected>>", self.on_language_change)
        
        # Exclude directories
        ttk.Label(self, text="排除目錄：").grid(row=2, column=0, sticky=tk.W, pady=10)
        self.exclude_dirs = ttk.Entry(self)
        self.exclude_dirs.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=10)
        
        # Exclude files
        ttk.Label(self, text="排除檔案：").grid(row=3, column=0, sticky=tk.W, pady=10)
        self.exclude_files = ttk.Entry(self)
        self.exclude_files.grid(row=3, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=10)
        
        # Include files
        ttk.Label(self, text="保留檔案：").grid(row=4, column=0, sticky=tk.W, pady=10)
        self.include_files = ttk.Entry(self)
        self.include_files.grid(row=4, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=10)
        
        # Process button
        ttk.Button(self, text="處理檔案", command=self.process_callback).grid(row=5, column=1, pady=20)
        
    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.root_dir.delete(0, tk.END)
            self.root_dir.insert(0, directory)
            
    def on_language_change(self, event):
        selected_language = self.language_var.get()
        config = LANGUAGE_CONFIGS.get(selected_language, {})
        self.exclude_dirs.delete(0, tk.END)
        self.exclude_dirs.insert(0, ",".join(config.get("exclude_dirs", [])))
        self.exclude_files.delete(0, tk.END)
        self.exclude_files.insert(0, ",".join(config.get("exclude_files", [])))
        self.include_files.delete(0, tk.END)
        self.include_files.insert(0, ",".join(config.get("include_files", [])))
        
    def get_input_data(self):
        return {
            "root_dir": self.root_dir.get(),
            "exclude_dirs": self.exclude_dirs.get().split(","),
            "exclude_files": self.exclude_files.get().split(","),
            "include_files": self.include_files.get().split(","),
            "language": self.language_var.get()
        }
