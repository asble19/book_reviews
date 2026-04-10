from pymongo import MongoClient

MONGO_URI = "mongodb+srv://asble19:kianlawley2004@cluster0.ukwzfcn.mongodb.net/book_reviews_db?retryWrites=true&w=majority"

# Connect to MongoDB
client = MongoClient(MONGO_URI)

# Select database
db = client["book_reviews_db"]

# Select collection
reviews_collection = db["reviews"]

# Delete all reviews
result = reviews_collection.delete_many({})

print(f"Deleted {result.deleted_count} reviews")