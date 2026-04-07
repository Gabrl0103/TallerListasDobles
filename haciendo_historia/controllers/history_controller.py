from models.doubly_linked_list import DoublyLinkedList
from models.history_entry import HistoryEntry


class BrowserHistoryController:
    def __init__(self):
        self.history = DoublyLinkedList()

    def add_entry(self, url, title):
        entry = HistoryEntry(url, title)
        self.history.append(entry)
        return entry.to_dict()

    def add_entry_at_start(self, url, title):
        entry = HistoryEntry(url, title)
        self.history.prepend(entry)
        return entry.to_dict()

    def insert_entry(self, index, url, title):
        entry = HistoryEntry(url, title)
        self.history.insert(index, entry)
        return entry.to_dict()

    def remove_entry(self, index):
        removed = self.history.remove(index)
        if removed is not None:
            return removed.to_dict()
        return None

    def get_all_entries(self):
        return [entry.to_dict() for entry in self.history.to_list()]

    def get_all_entries_reversed(self):
        return [entry.to_dict() for entry in self.history.to_list_reversed()]

    def search_entry(self, keyword):
        current_node = self.history.head
        index = 0
        results = []
        while current_node is not None:
            entry = current_node.value
            if keyword.lower() in entry.url.lower() or keyword.lower() in entry.title.lower():
                results.append({"index": index, **entry.to_dict()})
            current_node = current_node.next
            index += 1
        return results

    def get_length(self):
        return self.history.length

    def get_entry_at(self, index):
        if index < 0 or index >= self.history.length:
            return None
        node = self.history.traverse_to_index(index)
        return node.value.to_dict()
