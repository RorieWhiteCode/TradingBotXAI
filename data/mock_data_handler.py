import json

class MockDataHandler:
    def __init__(self):
        with open('data/mock/mock_data.json', 'r') as f:
            self.data = json.load(f)

    def get_price(self, pair):
        return self.data[pair]["price"]

    def get_volume(self, pair):
        return self.data[pair]["volume"]
