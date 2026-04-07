from datetime import datetime


class HistoryEntry:
    def __init__(self, url, title):
        self.url = url
        self.title = title
        self.visited_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "url": self.url,
            "title": self.title,
            "visited_at": self.visited_at,
        }
