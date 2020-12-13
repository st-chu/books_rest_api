import json
from typing import Union, Dict, List


class Books:
    def __init__(self):
        try:
            with open("books.json", "r") as f:
                self.books = json.load(f)
        except FileNotFoundError:
            self.books = []

    def all(self) -> List[Dict[str, Union[str, int, bool, Dict[str, Union[str, bool]]]]]:
        return self.books

    def get(self, _id: int) -> Union[List, Dict[str, Union[str, int, bool, Dict[str, Union[str, bool]]]]]:
        book = [book for book in self.all() if book['id'] == _id]
        if book:
            return book[0]
        return []

    def save_all(self) -> None:
        with open("books.json", "w") as f:
            json.dump(self.books, f)

    def create(self, _data: Dict[str, Union[str, int, bool, Dict[str, Union[str, bool]]]]) -> None:
        self.books.append(_data)
        self.save_all()

    def update(self, _id: int, _data: Dict[str, Union[str, int, bool, Dict[str, Union[str, bool]]]]) -> bool:
        book = self.get(_id)
        if book:
            index = self.books.index(book)
            self.books[index] = _data
            self.save_all()
            return True
        return False

    def delete(self, _id: int) -> bool:
        book = self.get(_id)
        if book:
            self.books.remove(book)
            self.save_all()
            return True
        return False

    def sort_books(self, _key: str, reverse: bool) \
            -> List[Dict[str, Union[str, int, bool, Dict[str, Union[str, bool]]]]]:
        if _key == "lend":
            sorted_books = sorted(self.all(), key=lambda given_key: given_key[_key]['lent'], reverse=reverse)
            return sorted_books
        sorted_books = sorted(self.all(), key=lambda given_key: given_key[_key], reverse=reverse)
        return sorted_books

    def lend_book(self, _book: Dict[str, Union[str, int, bool, Dict[str, Union[str, bool]]]], _who: str) -> None:
        index = self.books.index(_book)
        lend = _book['lend']
        lend['lent'] = True
        lend['who'] = _who
        _book.get('lend', lend)
        self.books[index] = _book
        self.save_all()

    def return_book_(self, _book: Dict[str, Union[str, int, bool, Dict[str, Union[str, bool]]]]) -> None:
        index = self.books.index(_book)
        lend = _book['lend']
        lend['lent'] = False
        del lend['who']
        _book.get('lend', lend)
        self.books[index] = _book
        self.save_all()


def is_request_correct(_request: Dict[str, Union[str, int, bool, Dict[str, Union[str, bool]]]]) -> bool:
    try:
        if any([
            'author' in _request and not isinstance(_request.get('author'), str),
            'title' in _request and not isinstance(_request.get('title'), str),
            'publisher' in _request and not isinstance(_request.get('publisher'), str),
            'description' in _request and not isinstance(_request.get('description'), str),
            'rating' in _request and not isinstance(_request['rating'], int),
            'rating' in _request and _request['rating'] not in range(1, 11),
            'read' in _request and not isinstance(_request.get('read'), bool),
            'genre' in _request and not isinstance(_request.get('genre'), str),
            'lend' in _request
        ]):
            return True
    except TypeError:
        return True


def create_new_book(_id: int, _data: Dict[str, Union[str, int, bool, Dict[str, Union[str, bool]]]])\
        -> Dict[str, Union[str, int, bool, Dict[str, Union[str, bool]]]]:
    _book = {
        'id': _id,
        'author': _data.get('author'),
        'title': _data.get('title'),
        'publisher': _data.get('publisher', 'not entered'),
        'description': _data.get('description', ''),
        'rating': _data.get('rating', 0),
        'read': _data.get('read', False),
        'genre': _data.get('genre', 'not entered'),
        'lend': {'lent': False}
    }
    return _book


books = Books()
