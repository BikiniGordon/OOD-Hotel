import time
from typing import Optional, List
import json
from pympler import asizeof

from room import Room
from AVL import AVLTree

class HilbertHotel:
    
    def __init__(self):
        self.rooms = AVLTree()
        self.total_guests = 0
        self._room_cache = {}
        self.prime_numbers = []

    def _log_operation(self, operation: str, duration: float, details: str = "", silent: bool = False):
        if not silent:
            print(f"[{operation}] {duration * 1000:.4f}ms - {details}")
    
    def _calculate_room_number(self, visitor: int = 0, bus: int = 0, ship: int = 0, 
                             fleet: int = 0, group: int = 0) -> int:
        new_rooms = []

        if visitor and not bus and not ship and not fleet and not group:

            # shift old room by amount of passenger

            for v in range(visitor):
                new_rooms.append(Room(v + 1, visitor_path=(0, 0, 0, 0), visitor_number = v + 1))
        
        elif bus and not ship and not fleet and not group:

            # shift old room by *= bus + 1

            for b in range(bus):
                for v in range(visitor):
                    new_rooms.append(Room((bus + 1) * v + (b + 1), visitor_path = (0, 0, 0, b + 1), visitor_number = v + 1))

        elif ship and not fleet and not group:

            # shift old room by *= ship + 1

            for s in range(ship):
                for b in range(bus):
                    for v in range(visitor):
                        new_rooms.append(Room((ship + 1) * (bus * v + b) + (s + 1), visitor_path = (0, 0, s + 1, b + 1), visitor_number = v + 1))

        elif fleet and not group:

            # shift old room by *= fleet + 1

            for f in range(fleet):
                for s in range(ship):
                    for b in range(bus):
                        for v in range(visitor):
                            new_rooms.append(Room((fleet + 1) * (ship * (bus * v + b) + s) + (f + 1), visitor_path = (0, f + 1, s + 1, b + 1), visitor_number = v + 1))

        elif group:

            # shift old room by *= group + 1
            
            for g in range(group):
                for f in range(fleet):
                    for s in range(ship):
                        for b in range(bus):
                            for v in range(visitor):
                                new_rooms.append(Room((group + 1) * ((fleet * (ship * (bus * v + b) + s)) + f) + (g + 1), visitor_path = (g + 1, f + 1, s + 1, b + 1), visitor_number = v + 1))

        return new_rooms

    def _shift_existing_guests(self, n: int, method: int, silent: bool = False):
        start_time = time.time()
        self.rooms.change_room(n, method)
        self._room_cache.clear()
        end_time = time.time()
        self._log_operation("SHIFT_GUESTS", end_time - start_time, "Shifted existing guests successfully")

    def balance_insert(self, sorted_rooms):
        if not sorted_rooms:
            return
        mid_index = len(sorted_rooms) // 2
        self.rooms.insert(sorted_rooms[mid_index])
        self.balance_insert(sorted_rooms[:mid_index])
        self.balance_insert(sorted_rooms[mid_index + 1:])

    def get_prime(self, index: int) -> int:
        if index < 0:
            raise ValueError("Index must be non-negative")
        
        if index < len(self.prime_numbers):
            return self.prime_numbers[index]
        
        self._extend_primes_to_index(index)
        return self.prime_numbers[index]
    
    def _is_prime(self, n: int) -> bool:
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        
        sqrt_n = int(n ** 0.5) + 1
        for prime in self.prime_numbers:
            if prime >= sqrt_n:
                break
            if n % prime == 0:
                return False
            
        start = self.prime_numbers[-1] + 2 if self.prime_numbers else 3
        for i in range(start, sqrt_n, 2):
            if n % i == 0:
                return False
        
        return True
    
    def _extend_primes_to_index(self, target_index: int):
        candidate = self.prime_numbers[-1] + 1 if self.prime_numbers else 2

        while len(self.prime_numbers) <= target_index:
            if self._is_prime(candidate):
                self.prime_numbers.append(candidate)
            candidate += 1
        
    def add_infinite(self, hierarchy_levels: int, amount_per_level: list):
        start_time = time.time()

        if hierarchy_levels != len(amount_per_level):
            raise ValueError(f"Hierarchy levels ({hierarchy_levels}) must match amount list length ({len(amount_per_level)}).")
        
        if hierarchy_levels <= 0:
            raise ValueError("Hierarchy levels must be positive.")

        if hierarchy_levels > len(self.prime_numbers):
            self.get_prime(hierarchy_levels - 1)
        
        method = 2
        if hierarchy_levels == 1:
            shift_prime = 2
        else:
            shift_prime = self.get_prime(hierarchy_levels)
        
        if self.rooms.size() > 0:
            self._shift_existing_guests(shift_prime, method, silent=True)
        
        print(f"Adding infinite visitors with {hierarchy_levels}, with amount {amount_per_level} hierarchy levels")
        print(f"Using primes: {self.prime_numbers[:hierarchy_levels]} for room generation and {shift_prime} for shifting")
        
        new_rooms = []
        
        if hierarchy_levels == 1: # use odd even method
            visitors_count = amount_per_level[0]
            for v in range(visitors_count):
                room_number = 2 * v + 1
                new_rooms.append(Room(room_number, visitor_path=(0, 0, 0, 0), visitor_number=v + 1))
        else:
            def generate_rooms_recursive(level_index, current_path, prime_powers):
                if level_index == 0:
                    visitors_count = amount_per_level[0]
                    for v in range(visitors_count):
                        room_number = 1
                        for i, power in enumerate(prime_powers):
                            if power > 0:
                                room_number *= (self.prime_numbers[i] ** power)
                        
                        room_number *= (self.prime_numbers[0] ** (v + 1))
                        
                        new_rooms.append(Room(room_number, visitor_path=current_path, visitor_number=v + 1))
                    return
                
                current_level_count = amount_per_level[level_index]
                prime_index = level_index
                
                for unit in range(current_level_count):
                    next_path = current_path + (unit + 1,)
                    
                    new_prime_powers = prime_powers.copy()
                    new_prime_powers[prime_index] = unit + 1
                    
                    generate_rooms_recursive(level_index - 1, next_path, new_prime_powers)
            
            initial_prime_powers = [0] * hierarchy_levels
            generate_rooms_recursive(hierarchy_levels - 1, (), initial_prime_powers)

        print(f"Generated: {len(new_rooms)} rooms")

        new_rooms.sort(key=lambda r: r.room_number)

        self.balance_insert(new_rooms)

        for room in new_rooms:
            if len(self._room_cache) < 100:
                self._room_cache[room.room_number] = room
        
        self.total_guests += len(new_rooms)
        
        end_time = time.time()
        self._log_operation("ADD_INFINITE", end_time - start_time, 
                        f"Added {len(new_rooms)} visitors")
        
        return len(new_rooms)

    def add_batch_visitors(self, total_count: int = 0, visitors: int = 0, buses: int = 0, ships: int = 0, fleets: int = 0, groups: int = 0) -> int:
        
        start_time = time.time()
        method = 2
        if groups:
            n = groups+1
        elif fleets:
            n = fleets+1
        elif ships:
            n = ships+1
        elif buses:
            n = buses+1
        else:
            n = total_count
            method = 1

        if self.rooms.size() > 0:
            self._shift_existing_guests(n, method, silent=True)
        
        print(f"Adding {total_count} visitors...")
        
        new_rooms = self._calculate_room_number(visitors, buses, ships, fleets, groups)

        print(f"Expected: {total_count}, Generated: {len(new_rooms)}")
        
        new_rooms.sort(key=lambda r: r.room_number)

        self.balance_insert(new_rooms)

        for room in new_rooms:
            if len(self._room_cache) < 100:
                self._room_cache[room.room_number] = room
        
        self.total_guests += len(new_rooms)
        
        end_time = time.time()
        self._log_operation("ADD_BATCH", end_time - start_time, f"Added {len(new_rooms)} visitors")
        
        return len(new_rooms) 
    
    def add_manual(self, room_number: int, visitor_path: str = "Manual entry", 
                   visitor_number = "Empty"):
        start_time = time.time()

        room = Room(room_number, visitor_path, visitor_number)
        self.rooms.insert(room)
        if visitor_number != "Empty" and visitor_number != 0:
            self.total_guests += 1
        
        self._room_cache[room_number] = room
        
        end_time = time.time()
        self._log_operation("ADD_MANUAL", end_time - start_time, f"Added to room {room_number}")
    
    def delete_manual(self, room_number: int):
        start_time = time.time()
        
        if room_number in self._room_cache:
            del self._room_cache[room_number]

        room_to_delete = self.rooms.search(room_number)

        if room_to_delete:
            if room_to_delete.visitor_number != "Empty":
                self.total_guests -= 1
            self.rooms.delete(room_number)
            end_time = time.time()
            self._log_operation("DELETE_MANUAL", end_time - start_time, f"Deleted room {room_number}")
            return True
        else:
            end_time = time.time()
            self._log_operation("DELETE_MANUAL", end_time - start_time, f"Room {room_number} not found")
            return False
    
    def search_room(self, room_number: int) -> Optional[Room]:
        start_time = time.time()
        
        if room_number in self._room_cache:
            room = self._room_cache[room_number]
            end_time = time.time()
            self._log_operation("SEARCH_ROOM", end_time - start_time, f"Room {room_number} - Found (cached)")
            return room
        
        room = self.rooms.search(room_number)
        
        if room:
            self._room_cache[room_number] = room
        
        end_time = time.time()
        status = "Found" if room else "Not found"
        self._log_operation("SEARCH_ROOM", end_time - start_time, f"Room {room_number} - {status}")
        
        return room
    
    def get_ordered_rooms(self) -> List[Room]:
        start_time = time.time()
        count = self.rooms.print_inorder()
        end_time = time.time()
        self._log_operation("GET_ORDERED", end_time - start_time, f"Retrieved {count} rooms")

    def get_memory_usage(self) -> dict:
        usage = {
            'current_mb' : round(asizeof.asizeof(self) / (1024 * 1024), 4)
        }
        return usage
    
    def get_resource_usage(self) -> dict:
        start_time = time.time()
        
        total_rooms = self.rooms.size()
        memory_info = self.get_memory_usage()
        
        def get_max_depth(node, depth=0):
            if not node: return depth
            return max(get_max_depth(node.left, depth + 1), get_max_depth(node.right, depth + 1))
        
        max_depth = get_max_depth(self.rooms.root)
        
        usage_info = {
            'total_guests': self.total_guests,
            'total_rooms': total_rooms,
            'current_mb': memory_info['current_mb'],
            'tree_nodes': total_rooms,
            'tree_max_depth': max_depth,
            'cache_size': len(self._room_cache),
        }
        
        end_time = time.time()
        self._log_operation("RESOURCE_CHECK", end_time - start_time, f"Mem: {usage_info['current_mb']} MB")
        return usage_info
    
    def export_data(self, filename: str, format_type: str = 'json'):
        start_time = time.time()
        
        def room_generator():
            for room in self.rooms.inorder_traversal():
                yield room.to_dict()
        
        resource_usage = self.get_resource_usage()
        export_data = {
            'hotel_info': {
                'total_guests': self.total_guests,
                'export_timestamp': time.time(),
                'total_rooms': self.rooms.size()
            },
            'rooms': list(room_generator()),
            'resource_usage': f"{resource_usage['current_mb']} MB"
        }
        
        try:
            if format_type.lower() == 'json':
                with open(f"{filename}.json", 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, indent=2, ensure_ascii=False)
            else:
                raise ValueError("Unsupported format")
            
            end_time = time.time()
            self._log_operation("EXPORT_DATA", end_time - start_time, f"Exported to {filename}.{format_type}")
            return True
            
        except Exception as e:
            end_time = time.time()
            self._log_operation("EXPORT_ERROR", end_time - start_time, f"Error: {str(e)}")
            return False

