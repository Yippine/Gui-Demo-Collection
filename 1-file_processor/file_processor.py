import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, font
import os
import mimetypes
from pathlib import Path
import threading


class FileProcessorGUI:
    def __init__(self, master):
        self.master = master
        master.title("File Processor 文件處理器")
        master.geometry("1000x800")
        master.configure(bg="#f0f0f0")

        # 設置字體
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(size=12)
        self.master.option_add("*Font", default_font)

        self.create_widgets()

    def create_widgets(self):
        # 主框架
        main_frame = ttk.Frame(self.master, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

        # 輸入欄位
        input_frame = ttk.LabelFrame(main_frame, text="設置", padding="20")
        input_frame.grid(
            row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20)
        )
        input_frame.columnconfigure(1, weight=1)

        ttk.Label(input_frame, text="專案目錄：").grid(
            row=0, column=0, sticky=tk.W, pady=10
        )
        self.root_dir = ttk.Entry(input_frame)
        self.root_dir.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=10)
        ttk.Button(input_frame, text="瀏覽", command=self.browse_directory).grid(
            row=0, column=2, padx=(10, 0), pady=10
        )

        ttk.Label(input_frame, text="排除目錄：").grid(row=1, column=0, sticky=tk.W, pady=10)
        self.exclude_dirs = ttk.Entry(input_frame)
        self.exclude_dirs.grid(
            row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=(10, 0), pady=10
        )
        self.exclude_dirs.insert(0, ".git,.vscode,dist,build,node_modules")

        ttk.Label(input_frame, text="排除檔案：").grid(row=2, column=0, sticky=tk.W, pady=10)
        self.exclude_files = ttk.Entry(input_frame)
        self.exclude_files.grid(
            row=2, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=(10, 0), pady=10
        )
        self.exclude_files.insert(0, ".DS_Store,print_files.py,package-lock.json")

        ttk.Label(input_frame, text="包含檔案：").grid(row=3, column=0, sticky=tk.W, pady=10)
        self.include_files = ttk.Entry(input_frame)
        self.include_files.grid(
            row=3, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=(10, 0), pady=10
        )
        self.include_files.insert(0, "package.json,.gitignore,.env.example")

        # 按鈕
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        ttk.Button(button_frame, text="執行", command=self.process_files).grid(
            row=0, column=0, padx=10
        )
        ttk.Button(button_frame, text="清空輸出", command=self.clear_output).grid(
            row=0, column=1, padx=10
        )
        ttk.Button(button_frame, text="複製輸出", command=self.copy_output).grid(
            row=0, column=2, padx=10
        )

        # 輸出區域
        output_frame = ttk.LabelFrame(main_frame, text="輸出", padding="20")
        output_frame.grid(
            row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S)
        )
        output_frame.columnconfigure(0, weight=1)
        output_frame.columnconfigure(1, weight=1)
        output_frame.rowconfigure(0, weight=1)

        # 處理日誌
        log_frame = ttk.LabelFrame(output_frame, text="處理日誌", padding="10")
        log_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)

        self.log_text = scrolledtext.ScrolledText(
            log_frame, wrap=tk.WORD, width=40, height=20
        )
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 結果輸出
        result_frame = ttk.LabelFrame(output_frame, text="處理結果", padding="10")
        result_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)

        self.result_text = scrolledtext.ScrolledText(
            result_frame, wrap=tk.WORD, width=40, height=20
        )
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 設置权重
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.root_dir.delete(0, tk.END)
            self.root_dir.insert(0, directory)

    def is_text_file(self, file_path):
        text_mimes = [
            "text/",
            "application/json",
            "application/javascript",
            "application/xml",
        ]
        mime_type, _ = mimetypes.guess_type(str(file_path))
        return any(mime_type and mime_type.startswith(prefix) for prefix in text_mimes)

    def should_process_directory(self, dir_path):
        exclude_dirs = set(self.exclude_dirs.get().split(","))
        return not any(
            exclude_dir.strip() in dir_path.parts for exclude_dir in exclude_dirs
        )

    def should_process_file(self, file_path):
        exclude_files = set(self.exclude_files.get().split(","))
        include_files = set(self.include_files.get().split(","))
        if file_path.name in include_files:
            return True
        if file_path.name in exclude_files or (
            file_path.name.startswith(".") and file_path.name not in include_files
        ):
            return False
        return True

    def process_files(self):
        directory = self.root_dir.get()
        if not directory:
            self.log_text.insert(tk.END, "請選擇專案目錄。\n")
            return

        def process():
            self.log_text.delete("1.0", tk.END)
            self.result_text.delete("1.0", tk.END)
            self.log_text.insert(tk.END, "處理中...\n")

            result = []
            for root, dirs, files in os.walk(directory, topdown=True):
                root_path = Path(root)
                if not self.should_process_directory(root_path):
                    dirs[:] = []  # 清空子目錄列表，阻止遍歷
                    continue
                for file in sorted(files):
                    file_path = root_path / file
                    if self.should_process_file(file_path):
                        if self.is_text_file(file_path):
                            try:
                                with open(file_path, "r", encoding="utf-8") as f:
                                    content = f.read().strip()
                                    if content:
                                        relative_path = os.path.relpath(
                                            file_path, directory
                                        )
                                        result.append(
                                            f'{relative_path}:\n"""{content}"""\n'
                                        )
                                        self.log_text.insert(
                                            tk.END, f"處理文件: {relative_path}\n"
                                        )
                            except UnicodeDecodeError:
                                self.log_text.insert(
                                    tk.END, f"警告: 無法以 UTF-8 解碼 {file_path}\n"
                                )
                            except Exception as e:
                                self.log_text.insert(
                                    tk.END, f"錯誤: 處理 {file_path} 時發生問題: {e}\n"
                                )
                        else:
                            self.log_text.insert(tk.END, f"跳過非文本文件: {file_path}\n")
                    else:
                        self.log_text.insert(tk.END, f"排除文件: {file_path}\n")

            # 將結果顯示在結果框中
            self.result_text.insert(tk.END, "\n".join(result))
            self.log_text.insert(tk.END, "處理完成\n")

        threading.Thread(target=process, daemon=True).start()

    def clear_output(self):
        self.log_text.delete("1.0", tk.END)
        self.result_text.delete("1.0", tk.END)

    def copy_output(self):
        self.master.clipboard_clear()
        self.master.clipboard_append(self.result_text.get("1.0", tk.END))
        self.log_text.insert(tk.END, "輸出結果已複製到剪貼板。\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = FileProcessorGUI(root)
    root.mainloop()
