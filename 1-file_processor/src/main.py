import tkinter as tk
from tkinter import ttk
from gui.main_window import FileProcessorGUI
from gui.styles import setup_styles

def main():
    root = tk.Tk()
    root.title("File Processor 2.2")
    setup_styles(root)
    app = FileProcessorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
