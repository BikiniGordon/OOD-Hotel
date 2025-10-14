class Room:
    __slots__ = ['room_number', 'visitor_path', 'visitor_number']
    
    def __init__(self, room_number: int, visitor_path: str = "", visitor_number: int = 0):
        self.room_number = room_number
        self.visitor_path = visitor_path
        self.visitor_number = visitor_number
    
    def __str__(self):
        path = self.visitor_path
        if isinstance(path, (tuple, list)):
            path_str = "(" + ", ".join(str(x) for x in path) + ")"
        else:
            path_str = str(path)
        try:
            rn_str = str(self.room_number)
        except ValueError:
            digits = (self.room_number.bit_length() * 30103 // 100000) + 1 if self.room_number else 1
            rn_str = f"<int with ~{digits} digits>"

        return f"Room {rn_str}: {path_str} ({self.visitor_number})"
    
    # for export as JSON
    def to_dict(self):
        return {
            'room_number': self.room_number,
            'visitor_path': self.visitor_path,
            'visitor_number': self.visitor_number
        }
