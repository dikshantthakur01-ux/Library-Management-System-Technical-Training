import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import os
from library import Library
from styles import apply_styles

class LibraryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("📚 Modern Library Management System")
        self.root.geometry("1100x750")
        self.root.minsize(900, 600)
        self.root.configure(bg='#F8F9FA')

        # Center window
        self.center_window()

        self.library = Library()
        self.style, self.colors, self.fonts = apply_styles(root)

        # Main container
        main_frame = ttk.Frame(root)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Header
        header_label = ttk.Label(main_frame, text="Library Management System", style='Title.TLabel')
        header_label.pack(pady=(0, 20))

        # Notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill='both', expand=True)

        # Tabs
        self.manage_frame = ttk.Frame(self.notebook, style='Card.TFrame')
        self.notebook.add(self.manage_frame, text="📖 Manage Books")
        self.setup_manage_tab()

        self.borrow_frame = ttk.Frame(self.notebook, style='Card.TFrame')
        self.notebook.add(self.borrow_frame, text="🔄 Borrow/Return")
        self.setup_borrow_tab()

        self.search_frame = ttk.Frame(self.notebook, style='Card.TFrame')
        self.notebook.add(self.search_frame, text="🔍 Search")
        self.setup_search_tab()

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready - No books in library")
        status_bar = ttk.Label(root, textvariable=self.status_var, relief='sunken', anchor='w')
        status_bar.pack(side='bottom', fill='x')

        # Refresh on tab change
        self.notebook.bind('<<NotebookTabChanged>>', self.on_tab_change)

    def center_window(self):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1100 // 2)
        y = (self.root.winfo_screenheight() // 2) - (750 // 2)
        self.root.geometry(f"1100x750+{x}+{y}")

    def setup_manage_tab(self):
        # Input frame
        input_frame = ttk.LabelFrame(self.manage_frame, text="Add New Book", padding=15)
        input_frame.pack(fill='x', padx=15, pady=(15, 10))

        ttk.Label(input_frame, text="Title:", font=self.fonts['label']).grid(row=0, column=0, sticky='w', padx=(0, 10), pady=5)
        self.title_entry = ttk.Entry(input_frame, width=35, style='Valid.TEntry')
        self.title_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        self.title_entry.bind('<KeyRelease>', self.validate_manage_entries)

        ttk.Label(input_frame, text="Author:", font=self.fonts['label']).grid(row=1, column=0, sticky='w', padx=(0, 10), pady=5)
        self.author_entry = ttk.Entry(input_frame, width=35, style='Valid.TEntry')
        self.author_entry.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        self.author_entry.bind('<KeyRelease>', self.validate_manage_entries)

        ttk.Label(input_frame, text="ISBN:", font=self.fonts['label']).grid(row=2, column=0, sticky='w', padx=(0, 10), pady=5)
        self.isbn_entry = ttk.Entry(input_frame, width=35, style='Valid.TEntry')
        self.isbn_entry.grid(row=2, column=1, padx=5, pady=5, sticky='ew')
        self.isbn_entry.bind('<KeyRelease>', self.validate_manage_entries)

        input_frame.grid_columnconfigure(1, weight=1)

        # Buttons
        btn_frame = ttk.Frame(self.manage_frame)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="➕ Add Book", command=self.add_book, style='Accent.TButton', width=12).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="🗑 Delete Selected", command=self.delete_book, style='Danger.TButton', width=15).pack(side='left', padx=5)

        # Books Treeview
        tree_frame = ttk.Frame(self.manage_frame)
        tree_frame.pack(fill='both', expand=True, padx=15, pady=10)

        columns = ('ISBN', 'Title', 'Author', 'Status')
        self.books_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=18)
        self.books_tree.heading('ISBN', text='ISBN')
        self.books_tree.heading('Title', text='Title')
        self.books_tree.heading('Author', text='Author')
        self.books_tree.heading('Status', text='Status')
        self.books_tree.column('ISBN', width=100)
        self.books_tree.column('Title', width=300)
        self.books_tree.column('Author', width=250)
        self.books_tree.column('Status', width=100)

        # Scrollbar
        v_scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.books_tree.yview)
        self.books_tree.configure(yscrollcommand=v_scrollbar.set)

        self.books_tree.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')

        self.books_tree.bind('<ButtonRelease-1>', self.on_tree_select)

    def setup_borrow_tab(self):
        # Input frame
        input_frame = ttk.LabelFrame(self.borrow_frame, text="Borrow/Return Book", padding=15)
        input_frame.pack(fill='x', padx=15, pady=(15, 10))

        ttk.Label(input_frame, text="ISBN:", font=self.fonts['label']).grid(row=0, column=0, sticky='w', padx=(0, 10), pady=5)
        self.borrow_isbn_entry = ttk.Entry(input_frame, width=25, style='Valid.TEntry')
        self.borrow_isbn_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        self.borrow_isbn_entry.bind('<KeyRelease>', self.on_borrow_key)

        ttk.Label(input_frame, text="User ID:", font=self.fonts['label']).grid(row=1, column=0, sticky='w', padx=(0, 10), pady=5)
        self.user_entry = ttk.Entry(input_frame, width=25, style='Valid.TEntry')
        self.user_entry.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

        input_frame.grid_columnconfigure(1, weight=1)

        # Action buttons
        btn_frame = ttk.Frame(self.borrow_frame)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="📖 Borrow", command=self.borrow, style='Accent.TButton', width=12).pack(side='left', padx=(0, 5))
        ttk.Button(btn_frame, text="↩ Return", command=self.return_book_gui, style='Success.TButton', width=12).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="🔄 Clear", command=self.clear_borrow_entries, style='TButton', width=10).pack(side='left', padx=5)

        # Message label
        self.borrow_msg_label = ttk.Label(self.borrow_frame, text="", foreground=self.colors['primary'], font=self.fonts['small'])
        self.borrow_msg_label.pack(pady=5)

        # Available books tree (new)
        tree_frame = ttk.LabelFrame(self.borrow_frame, text="Available Books", padding=10)
        tree_frame.pack(fill='both', expand=True, padx=15, pady=10)

        columns = ('ISBN', 'Title', 'Author')
        self.borrow_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        self.borrow_tree.heading('ISBN', text='ISBN')
        self.borrow_tree.heading('Title', text='Title')
        self.borrow_tree.heading('Author', text='Author')
        self.borrow_tree.column('ISBN', width=120)
        self.borrow_tree.column('Title', width=350)
        self.borrow_tree.column('Author', width=300)

        v_scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.borrow_tree.yview)
        self.borrow_tree.configure(yscrollcommand=v_scrollbar.set)

        self.borrow_tree.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')

        self.borrow_tree.bind('<ButtonRelease-1>', self.on_borrow_tree_select)

    def setup_search_tab(self):
        # Search input
        search_frame = ttk.LabelFrame(self.search_frame, text="Search Books", padding=15)
        search_frame.pack(fill='x', padx=15, pady=(15, 10))

        ttk.Label(search_frame, text="Query (title/author/isbn):", font=self.fonts['label']).grid(row=0, column=0, sticky='w', pady=5)
        self.search_entry = ttk.Entry(search_frame, width=50, style='Valid.TEntry')
        self.search_entry.grid(row=0, column=1, padx=10, pady=5, sticky='ew')
        self.search_entry.bind('<KeyRelease>', lambda e: self.search())
        ttk.Button(search_frame, text="🔍 Search", command=self.search, style='Accent.TButton').grid(row=0, column=2, padx=10, pady=5)

        search_frame.grid_columnconfigure(1, weight=1)

        # Results Treeview
        tree_frame = ttk.LabelFrame(self.search_frame, text="Search Results", padding=10)
        tree_frame.pack(fill='both', expand=True, padx=15, pady=10)

        columns = ('ISBN', 'Title', 'Author', 'Status')
        self.search_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=20)
        self.search_tree.heading('ISBN', text='ISBN')
        self.search_tree.heading('Title', text='Title')
        self.search_tree.heading('Author', text='Author')
        self.search_tree.heading('Status', text='Status')
        self.search_tree.column('ISBN', width=100)
        self.search_tree.column('Title', width=300)
        self.search_tree.column('Author', width=250)
        self.search_tree.column('Status', width=100)

        v_scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.search_tree.yview)
        self.search_tree.configure(yscrollcommand=v_scrollbar.set)

        self.search_tree.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')

    def validate_manage_entries(self, event=None):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        isbn = self.isbn_entry.get().strip()
        valid = bool(title and author and isbn and len(isbn) >= 5)
        self.title_entry.configure(style='Valid.TEntry' if title else 'Invalid.TEntry')
        self.author_entry.configure(style='Valid.TEntry' if author else 'Invalid.TEntry')
        self.isbn_entry.configure(style='Valid.TEntry' if isbn else 'Invalid.TEntry')

    def on_borrow_key(self, event=None):
        isbn = self.borrow_isbn_entry.get().strip()
        if isbn:
            book = self.library.books.get(isbn)
            if book:
                self.borrow_msg_label.config(text=f"Found: {book.title} by {book.author}", foreground=self.colors['success'])
            else:
                self.borrow_msg_label.config(text="ISBN not found", foreground=self.colors['danger'])

    def on_tree_select(self, event):
        pass  # Can add selection highlight

    def on_borrow_tree_select(self, event):
        selection = self.borrow_tree.selection()
        if selection:
            item = self.borrow_tree.item(selection)
            self.borrow_isbn_entry.delete(0, tk.END)
            self.borrow_isbn_entry.insert(0, item['values'][0])

    def on_tab_change(self, event):
        if event.widget.select() == self.manage_frame:
            self.refresh_books_list()
        elif event.widget.select() == self.borrow_frame:
            self.refresh_books_list_borrow()

    def refresh_books_list(self):
        for item in self.books_tree.get_children():
            self.books_tree.delete(item)
        books = self.library.list_books()
        for book in books:
            status = "✅ Available" if book.available else "🚫 Borrowed"
            status_color = self.colors['success'] if book.available else self.colors['danger']
            self.books_tree.insert('', 'end', values=(book.isbn, book.title, book.author, status))
        self.update_status()

    def refresh_books_list_borrow(self):
        for item in self.borrow_tree.get_children():
            self.borrow_tree.delete(item)
        available_books = [b for b in self.library.list_books() if b.available]
        for book in available_books:
            self.borrow_tree.insert('', 'end', values=(book.isbn, book.title, book.author))

    def update_status(self):
        count = len(self.library.books)
        available = len([b for b in self.library.books.values() if b.available])
        self.status_var.set(f"📊 {count} total books | {available} available | Ready")

    def add_book(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        isbn = self.isbn_entry.get().strip()
        if not all([title, author, isbn]):
            messagebox.showerror("❌ Error", "All fields are required!", parent=self.root)
            return
        if len(isbn) < 5:
            messagebox.showerror("❌ Error", "ISBN must be at least 5 characters!", parent=self.root)
            return
        msg = self.library.add_book(title, author, isbn)
        messagebox.showinfo("✅ Success", msg, parent=self.root)
        self.clear_entries()
        self.refresh_books_list()

    def delete_book(self):
        selection = self.books_tree.selection()
        if not selection:
            messagebox.showerror("❌ Error", "Please select a book to delete.", parent=self.root)
            return
        item = self.books_tree.item(selection[0])
        isbn = item['values'][0]
        if messagebox.askyesno("Confirm Delete", f"Delete '{item['values'][1]}'?", parent=self.root):
            msg = self.library.remove_book(isbn)
            messagebox.showinfo("✅ Result", msg, parent=self.root)
            self.refresh_books_list()

    def clear_entries(self):
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.isbn_entry.delete(0, tk.END)
        self.validate_manage_entries()

    def clear_borrow_entries(self):
        self.borrow_isbn_entry.delete(0, tk.END)
        self.user_entry.delete(0, tk.END)
        self.borrow_msg_label.config(text="")

    def borrow(self):
        isbn = self.borrow_isbn_entry.get().strip()
        user = self.user_entry.get().strip()
        if not isbn or not user:
            messagebox.showerror("❌ Error", "ISBN and User ID required!", parent=self.root)
            return
        msg = self.library.borrow_book(isbn, user)
        self.borrow_msg_label.config(text=msg, foreground=self.colors['success'] if "success" in msg.lower() else self.colors['danger'])
        messagebox.showinfo("📖 Borrow", msg, parent=self.root)
        self.clear_borrow_entries()
        self.refresh_books_list_borrow()

    def return_book_gui(self):
        isbn = self.borrow_isbn_entry.get().strip()
        if not isbn:
            messagebox.showerror("❌ Error", "Enter ISBN to return.", parent=self.root)
            return
        msg = self.library.return_book(isbn)
        self.borrow_msg_label.config(text=msg, foreground=self.colors['success'])
        messagebox.showinfo("↩ Return", msg, parent=self.root)
        self.clear_borrow_entries()
        self.refresh_books_list_borrow()

    def search(self):
        query = self.search_entry.get().strip().lower()
        for item in self.search_tree.get_children():
            self.search_tree.delete(item)
        if not query:
            return
        results = self.library.search_book(query)
        for book in results:
            status = "✅ Available" if book.available else "🚫 Borrowed"
            self.search_tree.insert('', 'end', values=(book.isbn, book.title, book.author, status))

def main():
    root = tk.Tk()
    app = LibraryGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

