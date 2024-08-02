import tkinter as tk
from tkinter import ttk
from src.gui.input_frame import InputFrame
from src.gui.output_frame import OutputFrame
from src.core.file_processor import FileProcessor

class FileProcessorGUI:
    def __init__(self, master):
        self.master = master
        master.title("File Processor 2.2")
        master.geometry("1200x800")
        
        self.create_widgets()
        
    def create_widgets(self):
        main_frame = ttk.Frame(self.master, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        
        self.input_frame = InputFrame(main_frame, self.process_files)
        self.input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        
        self.output_frame = OutputFrame(main_frame)
        self.output_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
    def process_files(self):
        input_data = self.input_frame.get_input_data()
        processor = FileProcessor(**input_data)
        result, log = processor.process_files()
        self.output_frame.display_result(result, log)
