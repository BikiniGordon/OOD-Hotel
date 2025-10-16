from HilbertHotel import *

# CLI Interface
class HilbertHotelCLI:
    def __init__(self):
        self.hotel = HilbertHotel()
    
    def display_menu(self):
        print("\n" + "="*60)
        print("HILBERT HOTEL MANAGEMENT SYSTEM")
        print("="*60)
        print("1.  Add Batch Visitors")
        print("2.  Add Room Manually")
        print("3.  Delete Room Manually")
        print("4.  Search Room")
        print("5.  Display All Rooms")
        print("6.  Resource Usage")
        print("7.  Export Data")
        print("0.  Exit")
        print("="*60)
    
    # int input validation
    def get_int_input(self, prompt: str, min_val: int = 0, max_val: int = None) -> int:
        while True:
            try:
                value = int(input(prompt))
                if value < min_val:
                    print(f"Value must be at least {min_val}")
                    continue
                if max_val is not None and value > max_val:
                    print(f"Value must be at most {max_val}")
                    continue
                return value
            except ValueError:
                print("Please enter a valid number")

    # string input validation
    def get_string_input(self, prompt: str) -> str:
        return input(prompt).strip()
    
    # add room manually
    def add_manual_room(self):
        print("\nAdd Room Manually")
        print("-" * 30)
        print("Please enter room number you want to add manually.")
        while True:
            room_number = self.get_int_input("Room number (0 to cancel): ", 0)
            if room_number == 0:
                print("Process Canceled")
                return
            room_number_exist = self.hotel.rooms.search(room_number)
            if room_number_exist:
                print(f"Room {room_number} already exists. Please enter a different room number.")
                continue
            else:
                break
        guest_number = self.get_int_input("Visitor number (default: 1): ", 0)
        if guest_number == 0: 
            guest_number = 1 # default to 1
        self.hotel.add_manual(room_number, "Manual entry", guest_number)

        print("Room added successfully.")

    # add batch visitors
    def add_batch_visitors(self):
        print("\nAdd Batch Visitors")
        print("-" * 30)

        infinity_sel = self.get_int_input("Choose calculation method (1-2):\n1. Normal Calculation\n2. Infinity Calculation\nYour choice: ")

        if infinity_sel == 1:
            infinity = False
        elif infinity_sel == 2:
            infinity = True

        if infinity:
            amount_per_level = []
            hierarchy_amount = self.get_int_input("\nEnter the number of hierarchy levels: ", 1)
            
            for level_index in range(hierarchy_amount - 1, -1, -1):
                level_num = level_index + 1
                
                if level_index == hierarchy_amount - 1:
                    count = self.get_int_input(f"Units at level {level_num}: ", 1)
                    amount_per_level.insert(0, count)
                else:
                    print(f"\nLevel {level_num}:")
                    parent_count = amount_per_level[0] if level_index == hierarchy_amount - 2 else amount_per_level[hierarchy_amount - 2 - level_index]
                    
                    if isinstance(parent_count, list):
                        parent_count = len(parent_count)
                    
                    amounts_list = []
                    print(f"Enter amount for each of the {parent_count} parent units:")
                    
                    for i in range(parent_count):
                        while True:
                            try:
                                amount = self.get_int_input(f"  Parent unit {i+1}: ", 1)
                                amounts_list.append(amount)
                                break
                            except:
                                print("Please enter a valid positive number.")
                    
                    amount_per_level.insert(0, amounts_list)
                    print(f"Level {level_num}: {amounts_list}")
            
            bottom_level = amount_per_level[0] 
            if isinstance(bottom_level, list):
                total = sum(bottom_level)
            else:
                if len(amount_per_level) > 1:
                    upper_level = amount_per_level[1]
                    if isinstance(upper_level, list):
                        total = bottom_level * len(upper_level)
                    else:
                        total = bottom_level * upper_level
                else:
                    total = bottom_level
               
        else:
            choice = self.get_int_input("\nChoose hierarchy level (1-5):\n1. Visitors only\n2. Visitors + Buses\n3. Visitors + Buses + Ships\n4. Visitors + Buses + Ships + Fleets\n5. Visitors + Buses + Ships + Fleets + Groups\nYour choice: ", 1, 5)

            if choice == 1:
                visitors = self.get_int_input("Visitors: ")
                buses = ships = fleets = groups = 0

            elif choice == 2:
                visitors = self.get_int_input("Visitors: ")
                buses = self.get_int_input("Buses: ")
                ships = fleets = groups = 0

            elif choice == 3:
                visitors = self.get_int_input("Visitors: ")
                buses = self.get_int_input("Buses: ")
                ships = self.get_int_input("Ships: ")
                fleets = groups = 0

            elif choice == 4:
                visitors = self.get_int_input("Visitors: ")
                buses = self.get_int_input("Buses: ")
                ships = self.get_int_input("Ships: ")
                fleets = self.get_int_input("Fleets: ")
                groups = 0
                
            elif choice == 5:
                visitors = self.get_int_input("Visitors: ")
                buses = self.get_int_input("Buses: ")
                ships = self.get_int_input("Ships: ")
                fleets = self.get_int_input("Fleets: ")
                groups = self.get_int_input("Groups: ")

            # total visitors
            total = visitors
            if buses > 0:
                total *= buses
            if ships > 0:
                total *= ships
            if fleets > 0:
                total *= fleets
            if groups > 0:
                total *= groups
        
        # Display summary for infinity calculation
        if infinity:
            print(f"\nSummary of hierarchy structure:")
            for i, level_amount in enumerate(amount_per_level):
                level_num = i + 1
                if i == 0:
                    # Bottom level - actual visitors/people
                    if isinstance(level_amount, list):
                        print(f"  Level {level_num} (visitors): {len(level_amount)} units with {level_amount} people respectively (total: {sum(level_amount)} visitors)")
                    else:
                        print(f"  Level {level_num} (visitors): {level_amount} people per unit")
                else:
                    # Upper levels - containers (buses, ships, etc.)
                    if isinstance(level_amount, list):
                        print(f"  Level {level_num} (containers): {len(level_amount)} units")
                    else:
                        print(f"  Level {level_num} (containers): {level_amount} units")
        
        print(f"\nThis will add {total} visitors. Continue? (y/n): ", end="")
        confirm = input().lower()
        
        if confirm == 'y' and not infinity:
            rooms = self.hotel.add_batch_visitors(total, visitors, buses, ships, fleets, groups)
            print(f"Added {rooms} visitors successfully!")
        elif confirm == 'y' and infinity:
            rooms = self.hotel.add_infinite(hierarchy_amount, amount_per_level)
            print(f"Added {rooms} visitors successfully!")
        else:
            print("Operation cancelled")
    
    # delete room manually
    def delete_room(self):
        print("\nDelete Room Manually")
        print("-" * 30)
        
        room_number = self.get_int_input("Room number to delete: ", 1)
        
        if self.hotel.delete_manual(room_number):
            print(f"Room {room_number} deleted successfully")
        else:
            print(f"Room {room_number} not found")
    
    # search room number
    def search_room(self):
        print("\nSearch Room")
        print("-" * 30)
        
        room_number = self.get_int_input("Room number to search: ", 1)
        room = self.hotel.search_room(room_number)
        
        if room:
            print(f"Found: {room}")
        else:
            print(f"Room {room_number} not found")

    # display all room in hotel
    def display_all_rooms(self):
        print("\nDisplay All Rooms")
        print("-" * 30)
        
        self.hotel.get_ordered_rooms()
        print("Output format: [Room Number: (guest visitor path) (visitor number)]")


    # show resource usage and memory analysis
    def show_resource_usage(self):
        print("\nResource Usage & Memory Analysis")
        print("-" * 50)
        
        usage = self.hotel.get_resource_usage()
        
        print(f"\nHotel Stat:")
        print(f"  Total Guests: {usage['total_guests']}")
        print(f"  Total Rooms: {usage['total_rooms']}")
        
        print(f"\nMemory Usage:")
        print(f"  Current Memory Usage: {usage['current_mb']} MB")

        print(f"\nAVL Tree Stat:")
        print(f"  Tree Nodes: {usage['tree_nodes']}")
        print(f"  Tree Max Depth: {usage['tree_max_depth']}")
        print(f"  Cache Size: {usage['cache_size']}")
        
    # export data to JSON
    def export_data(self):
        print("\nExport Data")
        print("-" * 30)
        
        filename = self.get_string_input("Filename: ")
        if not filename:
            filename = f"hilbert_hotel_{int(time.time())}"
        
        if self.hotel.export_data(filename, format_type='json'):
            print(f"Data exported to {filename}.json")
        else:
            print("Export failed")
    
    # main input manager
    def run(self):
        print("Hotel Management System")
        
        while True:
            self.display_menu()
            choice = self.get_int_input("Enter your choice (0-7): ", 0, 7)
            
            try:
                if choice == 0:
                    print("\nExited")
                    break
                elif choice == 1:
                    self.add_batch_visitors()
                elif choice == 2:
                    self.add_manual_room()
                elif choice == 3:
                    self.delete_room()
                elif choice == 4:
                    self.search_room()
                elif choice == 5:
                    self.display_all_rooms()
                elif choice == 6:
                    self.show_resource_usage()
                elif choice == 7:
                    self.export_data()
                
                input("\nPress Enter to continue...")
                
            except KeyboardInterrupt:
                print("\n\nExited")
                break

if __name__ == "__main__":
    cli = HilbertHotelCLI()
    cli.run()