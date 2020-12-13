from flask import Flask, jsonify, request, abort, make_response
from models import books, is_request_correct, create_new_book


app = Flask(__name__)
app.config["SECRET_KEY"] = "Verysecretkey!"


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)


@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad Request ', 'status_code': 400}), 400)


@app.route("/api/books/", methods=['GET'])
def books_list_api():
    return jsonify(books.all()), 200


@app.route("/api/books/<int:book_id>", methods=['GET'])
def get_book(book_id):
    book = books.get(book_id)
    if not book:
        abort(404)
    return jsonify({"book": book}), 200


@app.route("/api/books/", methods=['POST'])
def create_book():
    _data = request.json
    if any([
        not 'author' in request.json,
        not 'title' in request.json,
    ]):
        abort(400)
    if is_request_correct(_data):
        abort(400)
    if len(books.all()) == 0:
        _id = 1
    else:
        _id = books.all()[-1]['id'] + 1
    _book = create_new_book(_id, request.json)
    books.create(_book)
    return jsonify({'book': _book}), 201


@app.route("/api/books/<int:book_id>", methods=['DELETE'])
def delete_book(book_id):
    result = books.delete(book_id)
    if not result:
        abort(404)
    return jsonify({'result': result}), 200


@app.route("/api/books/<int:book_id>", methods=['PUT'])
def update_book(book_id):
    _book = books.get(book_id)
    if not _book:
        abort(404)
    if not request.json:
        abort(400)
    _data = request.json
    if is_request_correct(request.json):
        abort(400)
    _book = {
        'id': book_id,
        'author': _data.get('author', _book['author']),
        'title': _data.get('title', _book['title']),
        'publisher': _data.get('publisher', _book['publisher']),
        'description': _data.get('description', _book['description']),
        'rating': _data.get('rating', _book['rating']),
        'read': _data.get('read', _book['read']),
        'genre': _data.get('genre', _book['genre']),
        'lend': _book['lend']
    }
    books.update(book_id, _book)
    return jsonify({'book': _book}), 200


@app.route("/api/books/sort", methods=['POST'])
def sort_books_list():
    key_list = ['id', 'author', 'title', 'publisher', 'rating', 'read', 'genre', 'lend']
    if any([
        not request.json,
        not 'key' in request.json,
        'key' in request.json and not isinstance(request.json['key'], str),
        'reverse' in request.json and not isinstance(request.json['reverse'], bool),
        'key' in request.json and not request.json['key'] in key_list
    ]):
        abort(400)
    if 'reverse' not in request.json:
        reverse = False
    else:
        reverse = request.json['reverse']
    sort_books = books.sort_books(request.json['key'], reverse)
    return jsonify({f"sorted by key {request.json['key']}": sort_books}), 200


@app.route("/api/books/lend/<int:book_id>", methods=['POST'])
def lend(book_id: int):
    book = books.get(book_id)
    if not book:
        abort(404)
    if any([
        'lent' in request.json and not isinstance(request.json['lent'], bool),
        'who' in request.json and not isinstance(request.json['who'], str),
        not 'who' in request.json
    ]):
        abort(400)
    if book['lend']['lent'] is True:
        abort(400)
    books.lend_book(book, request.json['who'])
    return jsonify({"lend": books.get(book_id)}), 200


@app.route("/api/books/return/<int:book_id>", methods=['POST'])
def return_book(book_id):
    book = books.get(book_id)
    if not book:
        abort(404)
    if any({
        not 'return' in request.json,
        'return' in request.json and not isinstance(request.json['return'], bool)
    }):
        print('??')
        abort(400)
    if request.json['return'] is True:
        if book['lend']['lent'] is True:
            books.return_book_(book)
            return jsonify({"return": books.get(book_id)}), 200
        else:
            abort(400)
    else:
        abort(400)


if '__name__' == '__main__':
    app.run(debug=True)
