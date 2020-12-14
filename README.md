# books_rest_api

The application is used to catalog books from your home library. 
    You can add books to the list, delete them or modify their data
    
    User attributes:
        - id (int) - unique identifier of the book, assigned automatically in the process of creating a new item on the list
        - author (str) - author of the book
        - title (str) - title of the book
        - publisher (str) - publisher name
        - description (str) - book description
        - rating (int) - evaluation of the book on a scale from 1 to 10
        - read (bool) - whether the book has been read
        - genre (str) - book genre
        - lend (dic) - whether the book was lent to someone
        - lent (bool) - whether the book was lent to someone
        - who (str) - to whom the book was lent
        - return (bool) - whether the book was returned
        - key (str) - the key by which the book list will be sorted
        - reverse (bool) - optionally, reverse sort



# Allowed HTTP requests:
  GET: Get a list of home library books -> Content-Type: application/json

    example:
    GET http://localhost:5000/api/books/ -> returns a list of all books
    
    GET http://localhost:5000/api/books/<int:id>  -> returns a book with id = <id> 
        HTTP response status codes 200 if the book is on the list
        HTTP response status codes 404 if the book is not listed

  DELETE: To delete resource -> Content-Type: application/json

    example:
    DELETE http://localhost:5000/api/books/<int:id> -> removes the book from id = <id>
        HTTP response status codes 200 if the book was removed
        HTTP response status codes 404 if the book is not listed
        
      Response(200):
        {
        "result": true
        }


  PUT: To update resource -> Content-Type: application/json 
  
    example:
	PUT http://localhost:5000/api/books/<int:id> request.json{"rating": 10, "read": true, "description": "its a damn good book"}
	    HTTP response status codes 200 if the update was successful
	    HTTP response status codes 404 if the book is not listed
	    HTTP response status codes 400 if bad request
        
     Response(200):
        {
         "book": {
             "author": "Tomasz Somajlik",
             "description": "its a damn good book",
             "genre": "not entered",
             "id": 6,
             "lend": {
                 "lent": false
             }
             "publisher": "not entered",
             "rating": 10,
             "read": true,
             "title": "Ryjówka przeznaczenia"
           }
         }
        
    updateable attributes:
        - author (str) - author of the book
        - title (str) - title of the book
        - publisher (str) - publisher name
        - description (str) - book description
        - rating (int) - evaluation of the book on a scale from 1 to 10
        - read (bool) - whether the book has been read
        - genre (str) - book genre
        
  POST: To create or update resource -> Content-Type: application/json 
  
    example (create a new book):
    POST http://localhost:5000/api/books/ request.json{"author": "Tomasz Samojlik", "title": "Ryjówka przeznaczenia"}
        HTTP response status codes 201 if the new book has been created correctly
        HTTP response status codes 400 if bad request
        
    Response(201):
        {
         "book": {
             "author": "Tomasz Somajlik",
             "description": "",
             "genre": "not entered",
             "id": 6,
             "lend": {
                 "lent": false
             }
             "publisher": "not entered",
             "rating": 0,
             "read": false,
             "title": "Ryjówka przeznaczenia"
           }
         }
        
    possible attributes:
        - author (str) - author of the book, if not specified, creating a book is not possible
        - title (str) - title of the book, if not specified, creating a book is not possible
        - publisher (str) - publisher name, if no default setting given: str('not entered')
        - description (str) - book description, if no default setting given: empty str('')                             
        - rating (int) - evaluation of the book on a scale from 1 to 10, if no default setting given: int(0) 
        - read (bool) - whether the book has been read, if no default setting given: bool(false)
        - genre (str) - book genre, if no default setting given: str('not entered')
    attributes added automatically:
        - id (int) - unique identifier of the book, added if book is created
        - lend (dic) - if book is created, set to: {"lent": false}
        
     example (sort book lists):
     POST http://localhost:5000/api/books/sort request.json{"key": "lend"}
         HTTP response status codes 200 if the list is sorted
         HTTP response status codes 400 if bad request
         
     possible attributes:
        - key (str) - the key by which the book list will be sorted, possible keys: id, author, title, publisher, rating, read, genre, lend
        - reverse (bool) - optionally, if {"reverse": true} reverse sort, default setting {"reverse": false}
        
      example (lend the book):
      POST http://localhost:5000/api/lend/<int:id> request.json{"who": "Kamil"}
         HTTP response status codes 200 if lend was successful
	     HTTP response status codes 404 if the book is not listed
	     HTTP response status codes 400 if bad request
         
     Response(200):
        {
         "book": {
             "author": "Tomasz Somajlik",
             "description": "",
             "genre": "not entered",
             "id": 6,
             "lend": {
                 "lent": true,
                 "who": "Kamil"
             }
             "publisher": "not entered",
             "rating": 0,
             "read": false,
             "title": "Ryjówka przeznaczenia"
           }
         }
         
      possible attributes:  
        - who (str) - to whom the book was lent, added if lend succeeded, if the book is already borrowed: HTTP response status codes 400
      attributes added automatically:
        - lent (bool) -if lent succeeded, set to {"lent": true}
        
      example (return the book):
      POST http://localhost:5000/api/return/<int:id> request.json{"return": true}
         HTTP response status codes 200 if return was successful
	     HTTP response status codes 404 if the book is not listed
	     HTTP response status codes 400 if bad request
         
    Response(200):
        {
         "book": {
             "author": "Tomasz Somajlik",
             "description": "",
             "genre": "not entered",
             "id": 6,
             "lend": {
                 "lent": false
             }
             "publisher": "not entered",
             "rating": 0,
             "read": false,
             "title": "Ryjówka przeznaczenia"
           }
         }
         
      possible attributes:  
        - return (bool) - to whom the book was lent, if the book is already borrowed: HTTP response status codes 400
      attributes added automatically:
        - lent (bool) - if return succeeded, set to {"lent": false}
        - who (str) - if return succeeded, removed from lent
