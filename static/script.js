// Array to store book data
const books = [];
// Function to add a book to the list and send it to the server
function addBook() {
    const bookTitle = document.getElementById('bookTitle').value;
    const publicationYear = document.getElementById('publicationYear').value;
    const authorName = document.getElementById('authorName').value;
    const imageURL = document.getElementById('imageURL').value;

    console.log(bookTitle, publicationYear, authorName, imageURL)

    // Create a JSON object with book data
    const bookData = {
        title: bookTitle,
        publication_year: publicationYear,
        author: authorName,
        image_url: imageURL
    };

    console.log(bookData)
    // Send the book data to the server via POST request
    fetch('/api/add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(bookData)
    })
        .then(response => response.json())
        .then(data => {
            // Display a success message or handle errors if needed
            console.log(data.message);

            // Add the new book data to the books array
            books.push(bookData);
            console.log(books)

            // Refresh the book list
            displayBooks();
        })
        .catch(error => {
            console.error('Error adding book:', error);
        });
}

// Function to display books in the list
function displayBooks() {
    const bookList = document.getElementById('bookList');
    bookList.innerHTML = ''; // Clear existing book list

    books.forEach(book => {
        const bookElement = document.createElement('div');
        bookElement.innerHTML = `
            <h2>Added Successfully :${book.title}</h2>
            <p>Publication Year: ${book.publication_year}</p>
        `;
        bookList.appendChild(bookElement);
    });
}

// Function to fetch and display all books from the server
function showAllBooks() {
    const bookList = document.getElementById('bookshelf');
    bookList.innerHTML = '';

    fetch('/api/books')
        .then(response => response.json())
        .then(data => {
            data.books.forEach(book => {
                const bookElement = document.createElement('div');
                bookElement.className = "book-card";

                bookElement.innerHTML = `
                    <img src="${book.image_url}" class="book-cover">
                    <h3>${book.title}</h3>
                    <p class="author">${book.author}</p>
                `;

                bookList.appendChild(bookElement);
            });
        })
        .catch(error => {
            console.error('Error fetching all books:', error);
        });
}

function searchBooks(){

    const query = document.getElementById("searchBox").value;

    fetch(`/api/search?q=${query}`)
    .then(response => response.json())
    .then(data => {

        const bookList = document.getElementById("bookshelf");
        bookList.innerHTML = "";

        data.books.forEach(book => {

            const bookElement = document.createElement("div");
            bookElement.className = "book-card";

            bookElement.innerHTML = `
                <img src="${book.image_url}" class="book-cover">
                <h3>${book.title}</h3>
                <p>${book.author}</p>
            `;

            bookList.appendChild(bookElement);

        });

    });

}

// Function to fetch and display reviews
function showReviews() {
    fetch('/api/reviews')
        .then(response => response.json())
        .then(data => {
            const reviewsDiv = document.getElementById('reviewsList');
            reviewsDiv.innerHTML = ''; // clear old reviews

            if (data.reviews.length === 0) {
                reviewsDiv.innerHTML = '<p>No reviews found.</p>';
                return;
            }

            data.reviews.forEach(review => {
                const reviewElement = document.createElement('div');
                reviewElement.className = "review-card";

                reviewElement.innerHTML = `
                    <h4>Book: ${review.book_title}</h4>
                    <p><strong>User:</strong> ${review.user}</p>
                    <p><strong>Rating:</strong> ${review.rating}</p>
                    <p>${review.comment}</p>
                    <hr>
                `;

                reviewsDiv.appendChild(reviewElement);
            });
        })
        .catch(error => {
            console.error('Error fetching reviews:', error);
        });
}

// -------------------- REVIEWS --------------------
let reviewsVisible = false;

// toggle reviews (no duplicate buttons, no old function)
function toggleReviews() {
    reviewsVisible = !reviewsVisible;
    loadReviews();
}

// load reviews
function loadReviews() {
    const reviewList = document.getElementById("reviewsList");

    fetch("/api/reviews")
        .then(res => res.json())
        .then(data => {
            reviewList.innerHTML = "";

            if (!data.reviews || data.reviews.length === 0) {
                reviewList.innerHTML = "<p>No reviews found.</p>";
                return;
            }

            data.reviews.forEach(review => {
                const div = document.createElement("div");
                div.className = "review-card";

                div.innerHTML = `
                    <h4>${review.book_title}</h4>
                    <p><b>User:</b> ${review.user}</p>
                    <p><b>Rating:</b> ${review.rating}</p>
                    <p>${review.comment}</p>
                    <hr>
                `;

                reviewList.appendChild(div);
            });
        });
}

// submit review
function submitReview() {
    const reviewData = {
        book_title: document.getElementById("reviewBookTitle").value,
        user: document.getElementById("reviewUser").value,
        rating: document.getElementById("reviewRating").value,
        comment: document.getElementById("reviewComment").value
    };

    fetch("/api/add_review", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(reviewData)
    })
    .then(res => res.json())
    .then(() => {
        if (reviewsVisible) loadReviews();
    });
}