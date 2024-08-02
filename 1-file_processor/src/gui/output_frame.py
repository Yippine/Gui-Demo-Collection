import tkinter as tk
from tkinter import ttk, scrolledtext

class OutputFrame(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="結果", padding="20")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.create_widgets()
        
    def create_widgets(self):
        # Buttons
        button_frame = ttk.Frame(self)
        button_frame.grid(row=0, column=0, pady=(0, 20))
        ttk.Button(button_frame, text="清空結果", command=self.clear_output).grid(row=0, column=0, padx=10)
        ttk.Button(button_frame, text="複製結果", command=self.copy_output).grid(row=0, column=1, padx=10)
        
        # Output paned window
        self.paned_window = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.paned_window.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Log text
        log_frame = ttk.LabelFrame(self.paned_window, text="處理日誌", padding="10")
        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, width=40, height=20)
        self.log_text.pack(expand=True, fill=tk.BOTH)
        self.paned_window.add(log_frame)
        
        # Result text
        result_frame = ttk.LabelFrame(self.paned_window, text="處理結果", padding="10")
        self.result_text = scrolledtext.ScrolledText(result_frame, wrap=tk.WORD, width=40, height=20)
        self.result_text.pack(expand=True, fill=tk.BOTH)
        self.paned_window.add(result_frame)
        
    def clear_output(self):
        self.log_text.delete("1.0", tk.END)
        self.result_text.delete("1.0", tk.END)
        
    def copy_output(self):
        self.master.clipboard_clear()
        self.master.clipboard_append(self.result_text.get("1.0", tk.END))
        self.log_text.insert(tk.END, "輸出結果已複製到剪貼簿。\n")
        
    def display_result(self, result, log):
        self.log_text.delete("1.0", tk.END)
        self.log_text.insert(tk.END, log)
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, result)
