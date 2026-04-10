import requests

reviews = [
    {
        "book_title": "King in Yellow",
        "user": "Ashley",
        "rating": 5,
        "comment": "I like the Signalis reference."
    },
    {
        "book_title": "Dune",
        "user": "Ashley",
        "rating": 4,
        "comment": "Timuoxi Cha le mei."
    }
]

for review in reviews:
    response = requests.post(
        "http://127.0.0.1:5000/api/add_review",
        json=review
    )
    print(response.json())