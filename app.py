from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

library = []
issued_books = {}

@app.route('/')
def home():
    return render_template("index.html", page="home", library=library)

@app.route('/add', methods=['GET', 'POST'])
def add_book():
    message = None
    if request.method == 'POST':
        book_id = request.form['book_id']
        title = request.form['title']
        author = request.form['author']
        library.append({'id': book_id, 'title': title, 'author': author})
        message = "✅ Book added successfully!"
    return render_template("index.html", page="add", message=message)

@app.route('/display')
def display_books():
    return render_template("index.html", page="display", library=library)

@app.route('/remove', methods=['GET', 'POST'])
def remove_book():
    message = None
    if request.method == 'POST':
        book_id = request.form['book_id']
        for book in library:
            if book['id'] == book_id:
                library.remove(book)
                message = "❌ Book removed."
                break
        else:
            message = "Book not found."
    return render_template("index.html", page="remove", message=message)

@app.route('/update', methods=['GET', 'POST'])
def update_book():
    message = None
    if request.method == 'POST':
        book_id = request.form['book_id']
        new_title = request.form['new_title']
        new_author = request.form['new_author']
        for book in library:
            if book['id'] == book_id:
                book['title'] = new_title
                book['author'] = new_author
                message = "✅ Book updated."
                break
        else:
            message = "Book not found."
    return render_template("index.html", page="update", message=message)

@app.route('/search', methods=['GET', 'POST'])
def search_book():
    results = None
    if request.method == 'POST':
        keyword = request.form['keyword'].lower()
        results = [book for book in library if keyword in book['title'].lower() or keyword in book['author'].lower()]
    return render_template("index.html", page="search", results=results)

@app.route('/issue', methods=['GET', 'POST'])
def issue_book():
    message = None
    if request.method == 'POST':
        book_id = request.form['book_id']
        user = request.form['user']
        for book in library:
            if book['id'] == book_id and book_id not in issued_books:
                issued_books[book_id] = user
                message = f"✅ Book issued to {user}."
                break
        else:
            message = "Book not found or already issued."
    return render_template("index.html", page="issue", message=message)

@app.route('/return', methods=['GET', 'POST'])
def return_book():
    message = None
    if request.method == 'POST':
        book_id = request.form['book_id']
        if book_id in issued_books:
            issued_books.pop(book_id)
            message = "✅ Book returned successfully."
        else:
            message = "Book was not issued."
    return render_template("index.html", page="return", message=message)

if __name__ == '__main__':
    app.run(debug=True)
