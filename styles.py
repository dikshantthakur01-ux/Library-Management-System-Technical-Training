import tkinter as tk
from tkinter import ttk

def apply_styles(root):
    """Apply modern attractive styles to the application."""
    style = ttk.Style(root)
    
    # Use 'clam' theme for better customization (works well on Windows)
    style.theme_use('clam')
    
    # Colors: Modern palette
    colors = {
        'bg': '#F8F9FA',      # Light gray bg
        'fg': '#2C3E50',      # Dark blue-gray text
        'primary': '#4A90E2', # Blue accent
        'success': '#50C878', # Green
        'danger': '#E74C3C',  # Red
        'warning': '#F39C12', # Orange
        'selectbg': '#3498DB',
        'light': '#ECF0F1'
    }
    
    # Fonts
    fonts = {
        'heading': ('Arial', 14, 'bold'),
        'label': ('Arial', 10),
        'button': ('Arial', 10, 'bold'),
        'small': ('Arial', 9)
    }
    
    # Configure root
    root.configure(bg=colors['bg'])
    
    # TLabel
    style.configure('Title.TLabel', font=fonts['heading'], foreground=colors['fg'])
    style.configure('Head.TLabel', font=fonts['heading'])
    
    # TButton
    style.configure('Accent.TButton', font=fonts['button'], background=colors['primary'], foreground='white')
    style.map('Accent.TButton',
              background=[('active', '#357ABD'), ('pressed', colors['primary'])])
    
    style.configure('Success.TButton', font=fonts['button'], background=colors['success'], foreground='white')
    style.map('Success.TButton',
              background=[('active', '#3DAE61'), ('pressed', colors['success'])])
    
    style.configure('Danger.TButton', font=fonts['button'], background=colors['danger'], foreground='white')
    style.map('Danger.TButton',
              background=[('active', '#C0392B'), ('pressed', colors['danger'])])
    
    # TEntry
    style.configure('Valid.TEntry', fieldbackground='white', borderwidth=1)
    style.configure('Invalid.TEntry', fieldbackground='#FFF5F5', borderwidth=1)
    
    # Treeview (for lists)
    style.configure('Treeview', background='white', foreground=colors['fg'], rowheight=25, fieldbackground='white')
    style.configure('Treeview.Heading', font=fonts['button'], background=colors['primary'], foreground='white')
    style.map('Treeview', background=[('selected', colors['selectbg'])])
    style.map('Treeview.Heading',
              background=[('active', '#357ABD')])
    
    # TFrame
    style.configure('Card.TFrame', relief='solid', borderwidth=1)
    
    # TNotebook
    style.configure('Notebook', tabmargins=[2, 5, 2, 0])
    style.configure('Notebook.Tab', padding=[12, 8], font=fonts['label'])
    
    return style, colors, fonts

