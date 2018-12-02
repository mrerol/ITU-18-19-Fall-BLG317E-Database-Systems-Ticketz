class Expedition:
    def __init__(self, from_, from_ter, to, to_ter, dep_time, arr_time, date, price, selected_plane, total_cap, current_cap = 0, document = None):
        self.from_ = from_
        self.from_ter = from_ter
        self.to = to
        self.to_ter = to_ter
        self.dep_time = dep_time
        self.arr_time = arr_time
        self.date = date
        self.price = price
        self.selected_plane = selected_plane
        self.total_cap = total_cap
        self.current_cap = current_cap
        self.document = document

