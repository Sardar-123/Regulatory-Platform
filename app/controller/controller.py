from app.model.database import MongoDB

class Controller:
    def __init__(self):
        self.db = MongoDB("RegulatoryPlatform", "collection_name")

    def add_record(self, data):
        return self.db.insert_one(data)

    def get_record(self, query):
        return self.db.find_one(query)

    def get_records(self, query):
        return self.db.find_many(query)

    def modify_record(self, query, new_values):
        return self.db.update_one(query, new_values)

    def remove_record(self, query):
        return self.db.delete_one(query)

    def remove_records(self, query):
        return self.db.delete_many(query)

# Example usage
if __name__ == "__main__":
    controller = Controller()
    new_id = controller.add_record({"name": "John Doe"})
    print(f"Inserted record ID: {new_id}")
