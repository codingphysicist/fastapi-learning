from typing import Optional
from fastapi import FastAPI,Body
from pydantic import BaseModel, Field

app= FastAPI()


class Book:
    id: Optional[int]=None
    title:str
    author:str
    description:str
    rating:int

    def __init__(self, id, title, author, description,rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating

class BookRequest(BaseModel):
    id:int
    title:str = Field(min_length=3 )
    author:str = Field(min_length=1 )
    description:str = Field(min_length=1, max_length=100 )
    rating:int = Field(gt=-1,lt=6 )


BOOKS=[
    Book(1, "Python Crash Course", "Eric Matthes", "A beginner-friendly introduction to Python programming.", 4),
    Book(2, "Automate the Boring Stuff with Python", "Al Sweigart", "Learn how to automate repetitive tasks using Python.", 3),
    Book(3, "Fluent Python", "Luciano Ramalho", "Advanced techniques and best practices for Python developers.", 5),
    Book(4, "Effective Python", "Brett Slatkin", "59 specific ways to improve your Python code.", 5),
    Book(5, "Python Crash Course 2nd Edition", "Eric Matthes", "Updated edition with modern Python examples and projects.", 4),
    Book(6, "Beyond the Basic Stuff with Python", "Al Sweigart", "Intermediate Python concepts for improving coding skills.", 2)
]

@app.get("/books")
async def read_all_books():
    return BOOKS

@app.post("/books/create-book")
async def create_book(book_request:BookRequest):
    new_book=Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))

def find_book_id(book:Book):
    if len(BOOKS)>0:
        book.id=BOOKS[-1].id +1
    else:
        book.id=1
    return book
