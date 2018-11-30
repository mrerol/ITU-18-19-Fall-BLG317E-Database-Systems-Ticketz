class Vehicle:
    def __init__(self, category, model, capacity, production_year, production_place, recovery_time, description, image=None):
        self.category = category
        self.model = model
        self.capacity = capacity
        self.production_year = production_year
        self.production_place = production_place
        self.recovery_time = recovery_time
        self.description = description
        self.image = image
