class Room:
    __slots__ = ['room_number', 'visitor_path', 'visitor_number']
    
    def __init__(self, room_number: int, visitor_path: str = "", visitor_number: int = 0):
        self.room_number = room_number
        self.visitor_path = visitor_path
        self.visitor_number = visitor_number
    
    def __str__(self):
        return f"Room {self.room_number}: {self.visitor_path} ({self.visitor_number})"
    
    # for export as JSON
    def to_dict(self):
        return {
            'room_number': self.room_number,
            'visitor_path': self.visitor_path,
            'visitor_number': self.visitor_number
        }
