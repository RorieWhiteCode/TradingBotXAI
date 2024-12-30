import json

class LiveDataHandler:
    def save_live_data(self, data):
        with open('data/live/current_data.json', 'w') as f:
            json.dump(data, f)
