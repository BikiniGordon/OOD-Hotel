class Room:
    __slots__ = ['room_number', 'visitor_path', 'visitor_number', 'guest_status']
    
    def __init__(self, room_number: int, visitor_path: str = "", visitor_number: int = 0, guest_status: str = "new"):
        self.room_number = room_number
        self.visitor_path = visitor_path
        self.visitor_number = visitor_number
        self.guest_status = guest_status
    
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

        status_flag = f" [{self.guest_status.upper()}]" if hasattr(self, 'guest_status') else ""
        return f"Room {rn_str}: {path_str} ({self.visitor_number}){status_flag}"
    
    # for export as JSON
    def to_dict(self):
        return {
            'room_number': self.room_number,
            'visitor_path': self.visitor_path,
            'visitor_number': self.visitor_number,
            'guest_status': getattr(self, 'guest_status', 'new')
        }
