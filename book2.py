from typing import Optional
from fastapi import FastAPI,Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status
app= FastAPI()


class Book:
    id: int
    title:str
    author:str
    description:str
    rating:int
    published_date:int

    def __init__(self, id, title, author, description,rating,published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date=published_date

class BookRequest(BaseModel):
    id: Optional[int]=Field(description="Do not need an ID", default=None)
    title:str = Field(min_length=3 )
    author:str = Field(min_length=1 )
    description:str = Field(min_length=1, max_length=100 )
    rating:int = Field(gt=-1,lt=6 )
    published_date:int=Field()


    model_config={
        "json_schema_extra":{
            "example":{
                "title":"Mathematics",
                "author":"RD Sharma",
                "description":"Deep understanding for advanced mathematics",
                "rating":4,
                "published_date":2012
            }
        }
    }

BOOKS=[
    Book(1, "Python Crash Course", "Eric Matthes", "A beginner-friendly introduction to Python programming.", 4, 2012),
    Book(2, "Automate the Boring Stuff with Python", "Al Sweigart", "Learn how to automate repetitive tasks using Python.", 3,2012),
    Book(3, "Fluent Python", "Luciano Ramalho", "Advanced techniques and best practices for Python developers.", 5, 2011),
    Book(4, "Effective Python", "Brett Slatkin", "59 specific ways to improve your Python code.", 5,2015),
    Book(5, "Python Crash Course 2nd Edition", "Eric Matthes", "Updated edition with modern Python examples and projects.", 4,2015),
    Book(6, "Beyond the Basic Stuff with Python", "Al Sweigart", "Intermediate Python concepts for improving coding skills.", 2,2010)
]

@app.get("/book/{book_id}",status_code=status.HTTP_200_OK)
async def get_specific_book(book_id:int=Path(gt=0)):
    for book in BOOKS:
        if book.id==book_id:
            return book
    raise HTTPException(status_code=404, detail="Item not found")

@app.get("/books/")
async def book_by_rating(book_rating:int=Query(gt=0,lt=6)):
    books_to_return=[]
    for book in BOOKS:
        if book.rating==book_rating:
            books_to_return.append(book)
    return books_to_return

@app.get("/books",status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS

@app.post("/books/create-book",status_code=status.HTTP_201_CREATED)
async def create_book(book_request:BookRequest):
    new_book=Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))

def find_book_id(book:Book):
    if len(BOOKS)>0:
        book.id=BOOKS[-1].id +1
    else:
        book.id=1
    return book

@app.put("/books/update_book",status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book:BookRequest):
    bookchange=False
    for i in range(len(BOOKS)):
        if book.id==BOOKS[i].id:
            BOOKS[i]=book 
            bookchange=True
    if bookchange==False:
        raise HTTPException(status_code=404,detail="Book of that id not found")



@app.get("/books/publish",status_code=status.HTTP_200_OK)
async def book_by_published_date(published_date:int=Query(gt=1999,lt=2031)):
    books_to_return=[]
    for book in BOOKS:
        if book.published_date==published_date:
            books_to_return.append(book)
    return books_to_return


@app.delete("/books/delete_book",status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id:int=Query(gt=0)):
    book_changed=False
    for i in range(len(BOOKS)):
        if BOOKS[i].id==book_id:
            BOOKS.pop(i)
            book_changed=True
            break
    if book_changed==False:
        raise HTTPException(status_code=404,detail="book of that id not found")