from fastapi import Body,FastAPI
app = FastAPI()

books = [{
    "name":"Atomic Habits",
    "author":"James Clear",
    "category":"Self-Help",
    "pages":320,
    "price":19.99,
    "is_available":True,
    "rating":4.5,
    "description":"A book about building good habits and breaking bad ones."
},{
    "name":"The Great Gatsby",
    "author":"James Clear",
    "category":"Fiction",
    "pages":180,
    "price":15.99,
    "is_available":True,
    "rating":4.2,
    "description":"A classic novel about the American Dream and the pursuit of happiness."
},{
    "name":"The Catcher in the Rye",
    "author":"J.D. Saling er",
    "category":"Fiction",
    "pages":224,
    "price":12.99,
    "is_available":True,
    "rating":4.7,
    "description":"A novel about the struggles of a young man in the 1950s."
},{
    "name":"The Alchemist",
    "author":"James Clear",
    "category":"Fiction",
    "pages":208,
    "price":14.99,
    "is_available":True,
    "rating":4.8,
    "description":"A novel about the journey of a young man in search of his personal legend."
},{
    "name":"The Power of Now",
    "author":"Eckhart Tolle",
    "category":"Self-Help",
    "pages":240,
    "price":16.99,
    "is_available":True,
    "rating":4.6,
    "description":"A book about the present moment and the power of mindfulness."
}]

@app.get("/books")
async def read_all_books():
        return books

@app.get("/books/")
async def read_all_books(category:str):
    if category:
        return [book for book in books if book.get("category").casefold() == category.casefold()]
    else:
        return books
    

@app.get("/books/{book_id}")
async def required_book(book_id:int):
    if book_id > len(books):
        return {"error":"Book not found"}
    return books[book_id]

@app.get("/books/bookName/{book_name}")
async def required_bookName(book_name: str):
    for x in books:
        if x.get("name").casefold() == book_name.casefold():
            return x
    return {"error":"book not found"}
    
@app.get("/books/bookName/{book_name}/")
async def required_bookName(book_name: str,category:str):
    for x in books:
        if x.get("author").casefold() == book_name.casefold() and \
            x.get("category").casefold() == category.casefold():
            return x
    return {"error":"book not found"}


@app.post("/newbook")
def Addbook(newbook: dict=Body()):
    print(newbook)
    if not newbook:
        return "no book was passed"
    else:
        books.append(newbook)
        return "book added successfully "
    
@app.put("/updatebook")
async def updateBook(book: dict=Body()):
    if not book:
        return "wrong request body is empty"
    else:
        for i,b in enumerate(books):
            if books[i].get("name").casefold() == book.get("name").casefold():
                print(books[i])
                books[i] = book;                
                return "book updated"   
            
@app.delete("/deletebook")
async def deleteBook(book_id:int):
    if book_id > len(books):
        return {"error":"Book not found"}
    else:
        books.pop(book_id)
        return "book deleted successfully"
    
@app.get("/booksAuthor/{author}")
async def authorbook(author :str):
    print(author)
    return [book for book in books if book.get('author').casefold() == author.casefold()]