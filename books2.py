from fastapi import FastAPI, Body, Path, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from starlette import status

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    pages: int
    is_Available: bool

    def __init__(self,id,title,author,pages,is_Available):
        self.id = id
        self.title = title
        self.author = author
        self.pages = pages
        self.is_Available = is_Available

class BookRequest(BaseModel):
    '''id: Optional[int] = None'''
    id: Optional[int] = Field(description='no need to put id', default=None)
    title: str =  Field(min_length=3)
    author: str = Field(min_length=1)
    pages: int = Field(gt=0,lt=1000)
    is_Available: bool

    model_config = {
        "json_schema_extra":{
            "example":{
                "title": "new book",
                "author": "Aman Jain",
                "pages": 100,
                "is_Available": True
            }
        }
    }
    
BOOKS = [
    Book(101,"Who moved my cheese","Robin Thomus",256,True),
    Book(102,"Atomic Habit","Robin Thomus",2506,True),
    Book(103,"Focus on what matter","Rohit Shrivastav",856,True),
    Book(104,"Let us C","Aman Jain",597,True),
    Book(105,"Delhi boy","Robin Thomus",341,True)
]

@app.get("/books",status_code=status.HTTP_200_OK)
async def Books():
    return BOOKS

@app.post("/books/new-book",status_code=status.HTTP_201_CREATED)
async def NewBook(newbook = Body()):
    BOOKS.append(newbook)


@app.get("/books/{book_id}",status_code=status.HTTP_200_OK)
async def RequiredBook(book_id: int = Path(gt=100)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404,detail="Item not found!")

@app.delete("/books/{book_id}",status_code=status.HTTP_204_NO_CONTENT)
def Deletebook(book_id: int = Path(gt=100)):
    for book in BOOKS:
        if book.id == book_id:
            BOOKS.remove(book)
            
    raise HTTPException(status_code=404,detail='book with requested id not found')

#validation for QueryParameter:
@app.get("/books/",status_code=status.HTTP_200_OK)
async def RequiredAuthorbook(author: str = Query(min_length=3)):
    return [book for book in BOOKS if book.author.casefold() == author.casefold()]



#doing post with pydantic 

@app.post("/books/add-book",status_code=status.HTTP_201_CREATED)
async def AddBook(newbook: BookRequest):
    book = Book(**newbook.model_dump())
    BOOKS.append(book_id_for_newbook(book))

@app.put("/books/update-book",status_code=status.HTTP_204_NO_CONTENT)
async def UpdateBook(updatedbook: BookRequest):
    for i,book in enumerate(BOOKS):
        if book.id == updatedbook.id:
            BOOKS[i]=updatedbook
    raise HTTPException(status_code=404,detail="book with that id not found")
    

def book_id_for_newbook(book:Book):
    book.id = 1 if len(BOOKS)==0 else BOOKS[-1].id + 1
    return book 

