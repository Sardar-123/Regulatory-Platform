from pymongo import MongoClient

class MongoDB:
    def __init__(self, db_name, collection_name):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def insert_one(self, data):
        result = self.collection.insert_one(data)
        return result.inserted_id

    def find_one(self, query):
        result = self.collection.find_one(query)
        return result

    def find_many(self, query):
        results = self.collection.find(query)
        return list(results)

    def update_one(self, query, new_values):
        result = self.collection.update_one(query, {"$set": new_values})
        return result.modified_count

    def delete_one(self, query):
        result = self.collection.delete_one(query)
        return result.deleted_count

    def delete_many(self, query):
        result = self.collection.delete_many(query)
        return result.deleted_count

# Example usage
if __name__ == "__main__":
    db = MongoDB("RegulatoryPlatform", "collection_name")
    db.insert_one({"name": "example"})
