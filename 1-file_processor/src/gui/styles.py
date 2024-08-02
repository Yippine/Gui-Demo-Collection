from tkinter import ttk
import tkinter as tk

def setup_styles(root):
    style = ttk.Style(root)
    
    # Configure colors
    style.configure(".", background="#f5f5f5", foreground="#333333")
    style.configure("TFrame", background="#f5f5f5")
    style.configure("TLabel", background="#f5f5f5", font=("Helvetica", 10))
    style.configure("TEntry", fieldbackground="white", font=("Helvetica", 10))
    style.configure("TButton", font=("Helvetica", 10, "bold"))
    
    # Configure specific styles
    style.configure("TLabelframe", background="#f5f5f5", borderwidth=2, relief=tk.GROOVE)
    style.configure("TLabelframe.Label", background="#f5f5f5", font=("Helvetica", 11, "bold"))
    
    # Configure button styles
    style.configure("TButton", padding=6, relief="flat", background="#4CAF50", foreground="black")
    style.map("TButton",
              foreground=[('pressed', 'white'), ('active', 'white')],
              background=[('pressed', '!disabled', '#45a049'), ('active', '#45a049')])
    
    # Configure Treeview
    style.configure("Treeview", background="white", fieldbackground="white", foreground="black")
    style.map('Treeview', background=[('selected', '#bfbfbf')])
