class Vehicle:
    def __init__(self, name, category, model, capacity, production_year, production_place, description, document=None):
        self.name = name
        self.category = category
        self.model = model
        self.capacity = capacity
        self.production_year = production_year
        self.production_place = production_place
        self.description = description
        self.document = document
