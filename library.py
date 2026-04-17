import json
import os
from typing import Dict, List, Optional

class Book:
    def __init__(self, title: str, author: str, isbn: str):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.available = True

    def to_dict(self) -> dict:
        return {
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'available': self.available
        }

    @classmethod
    def from_dict(cls, data: dict):
        book = cls(data['title'], data['author'], data['isbn'])
        book.available = data['available']
        return book

class Library:
    def __init__(self, data_file: str = 'data.json'):
        self.books: Dict[str, Book] = {}
        self.data_file = data_file
        self.load()

    def add_book(self, title: str, author: str, isbn: str) -> str:
        if isbn in self.books:
            return "Book with this ISBN already exists."
        book = Book(title, author, isbn)
        self.books[isbn] = book
        self.save()
        return "Book added successfully."

    def remove_book(self, isbn: str) -> str:
        if isbn not in self.books:
            return "Book not found."
        del self.books[isbn]
        self.save()
        return "Book removed successfully."

    def search_book(self, query: str) -> List[Book]:
        results = []
        query_lower = query.lower()
        for book in self.books.values():
            if (query_lower in book.title.lower() or 
                query_lower in book.author.lower() or 
                query_lower == book.isbn.lower()):
                results.append(book)
        return results

    def list_books(self, available_only: bool = False) -> List[Book]:
        books = list(self.books.values())
        if available_only:
            books = [b for b in books if b.available]
        return sorted(books, key=lambda b: b.title)

    def borrow_book(self, isbn: str, user: str) -> str:
        if isbn not in self.books:
            return "Book not found."
        if not self.books[isbn].available:
            return "Book is not available."
        self.books[isbn].available = False
        self.save()
        return f"Book '{self.books[isbn].title}' borrowed by {user}."

    def return_book(self, isbn: str) -> str:
        if isbn not in self.books:
            return "Book not found."
        if self.books[isbn].available:
            return "Book was not borrowed."
        self.books[isbn].available = True
        self.save()
        return f"Book '{self.books[isbn].title}' returned."

    def save(self):
        data = {isbn: book.to_dict() for isbn, book in self.books.items()}
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=4)

    def load(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                self.books = {isbn: Book.from_dict(book_data) for isbn, book_data in data.items()}
            except:
                self.books = {}

