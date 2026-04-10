from pymongo import MongoClient
from flask import Flask, jsonify, render_template, request
import sqlite3
import os
from dotenv import load_dotenv

# ---------------------- MongoDB Setup ----------------------

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise Exception("MONGO_URI environment variable not set")

client = MongoClient(MONGO_URI)
mongo_db = client["book_reviews_db"]
reviews_collection = mongo_db["reviews"]

app = Flask(__name__)

# Path to SQLite database
DATABASE = 'db/books.db'

# ---------------------- Helper Function ----------------------
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# ---------------------- API Routes ----------------------

# Get all books
@app.route('/api/books', methods=['GET'])
def get_all_books():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT b.book_id, b.title, b.publication_year, b.image_url, a.name AS author
            FROM Books b
            LEFT JOIN book_author ba ON b.book_id = ba.book_id
            LEFT JOIN Authors a ON ba.author_id = a.author_id
        """)
        books = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return jsonify({'books': books})
    except Exception as e:
        return jsonify({'error': str(e)})

# Add a book manually
@app.route('/api/add', methods=['POST'])
def add_book():
    try:
        data = request.get_json()
        title = data.get('title')
        publication_year = data.get('publication_year')
        author_name = data.get('author')
        image_url = data.get('image_url', '')

        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert book
        cursor.execute(
            "INSERT INTO Books (title, publication_year, image_url) VALUES (?, ?, ?)",
            (title, publication_year, image_url)
        )
        book_id = cursor.lastrowid

        # Handle author
        cursor.execute("SELECT author_id FROM Authors WHERE name = ?", (author_name,))
        row = cursor.fetchone()
        if row:
            author_id = row['author_id']
        else:
            cursor.execute("INSERT INTO Authors (name) VALUES (?)", (author_name,))
            author_id = cursor.lastrowid

        # Link book and author
        cursor.execute(
            "INSERT INTO book_author (book_id, author_id) VALUES (?, ?)",
            (book_id, author_id)
        )

        conn.commit()
        conn.close()
        return jsonify({'message': 'Book added successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})

# Search books by title or author
@app.route('/api/search')
def search_books():
    query = request.args.get('q', '')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT b.title, b.image_url, a.name AS author
        FROM Books b
        LEFT JOIN book_author ba ON b.book_id = ba.book_id
        LEFT JOIN Authors a ON ba.author_id = a.author_id
        WHERE b.title LIKE ? OR a.name LIKE ?
    """, (f"%{query}%", f"%{query}%"))

    books = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify({"books": books})

# API to get all reviews from MongoDB
@app.route('/api/reviews', methods=['GET'])
def get_all_reviews():
    try:
        reviews = list(reviews_collection.find({}, {'_id': 0}))  # Get all reviews from MongoDB
        return jsonify({'reviews': reviews})
    except Exception as e:
        return jsonify({'error': str(e)})

# API to add a new review to MongoDB
@app.route('/api/add_review', methods=['POST'])
def add_review():
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data received'}), 400

        review = {
            'book_id': data.get('book_id'),
            'book_title': data.get('book_title'),
            'user': data.get('user'),
            'rating': data.get('rating'),
            'comment': data.get('comment')
        }

        if not review['book_title'] or not review['user']:
            return jsonify({'error': 'Missing required fields'}), 400

        reviews_collection.insert_one(review)

        return jsonify({'message': 'Review added successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

# Optional: Get all authors
@app.route('/api/authors', methods=['GET'])
def get_all_authors():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Authors")
        authors = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return jsonify(authors)
    except Exception as e:
        return jsonify({'error': str(e)})

# Render homepage
@app.route('/')
def index():
    return render_template('index.html')

# ---------------------- Run App ----------------------
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))