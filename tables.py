class Hotel:
    def __init__(self, name, email, description, city, address, phone, website):
        self.name = name
        self.email = email
        self.description = description
        self.city = city
        self.address = address
        self.phone = phone
        self.website = website

class Drivers:
    def __init__(self, name, gender, email, score , vote_number, city, address, phone):
        self.name = name
        self.gender = gender
        self.email = email
        self.city = city
        self.address = address
        self.phone = phone
        self.vote_number = vote_number
        self.score = score

class Firms:
    def __init__(self, name,password,website, logo, email, description , city, address, phone):
        self.name = name
        self.password = password
        self.description = description
        self.email = email
        self.city = city
        self.address = address
        self.phone = phone
        self.logo = logo
        self.website = website

class Vehicles:
    def __init__(self, category, capacity, production_year, production_place, image , recovery_time, model, description):
        self.category = category
        self.description = description
        self.production_year = production_year
        self.production_place = production_place
        self.image = image
        self.recovery_time = recovery_time
        self.model = model
        self.capacity = capacity