import requests

review_data = {
    "book_title": "King in Yellow",
    "user": "Ashley",
    "rating": 5,
    "review_text": "I like the Signalis reference."
}

response = requests.post("http://127.0.0.1:5000/api/add_review", json=review_data)
print(response.json())