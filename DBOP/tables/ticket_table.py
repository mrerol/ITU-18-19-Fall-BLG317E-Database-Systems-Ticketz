class Ticket:
    def __init__(self, expedition_id, user_id, seat_number, firm_id, price, extra_baggage = False, is_cancelable = False, bought_at = None, edited_at = None):
        self.expedition_id = expedition_id
        self.user_id = user_id
        self.seat_number = seat_number
        self.extra_baggage = extra_baggage
        self.is_cancelable = is_cancelable
        self.bought_at = bought_at
        self.edited_at = edited_at
        self.firm_id = firm_id
        self.price = price
