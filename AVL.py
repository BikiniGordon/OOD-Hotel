from room import Room
from typing import Optional, List

class AVLNode:
    __slots__ = ['room', 'left', 'right', 'height']
    
    def __init__(self, room: Room):
        self.room = room
        self.left = None
        self.right = None
        self.height = 1

    def get_balance(self):
        left_height = self.left.height if self.left else 0
        right_height = self.right.height if self.right else 0
        return left_height - right_height

class AVLTree: 
    def __init__(self):
        self.root = None
        self._cached_size = 0
    
    def _get_height(self, node):
        return node.height

    def _update_height(self, node):
        if node:
            node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
    
    def _right_rotate(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        self._update_height(y)
        self._update_height(x)
        return x
    
    def _left_rotate(self, x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        self._update_height(x)
        self._update_height(y)
        return y
    
    def balance(self, node):
        balance = node.get_balance()

        if balance == 2:
            if node.right and node.right.get_balance() < 0:
                node.right = self._right_rotate(node.right)
            node = self._left_rotate(node)
        elif balance == -2:
            if node.left and node.left.get_balance() > 0:
                node.left = self._left_rotate(node.left)
            node = self._right_rotate(node)
        
        node.height = self._get_height(node)
        return node
    
    def insert(self, room: Room):
        self.root = self._insert_recursive(self.root, room)
    
    def _insert_recursive(self, node, room):
        if not node:
            self._cached_size += 1
            return AVLNode(room)
        elif room.room_number > node.room.room_number:
            node.right = self._insert_recursive(node.right, room)       
        elif room.room_number < node.room.room_number:
            node.left = self._insert_recursive(node.left, room)
        node = self.balance(node)
        return node
    
    def delete(self, room_number: int):
        self.root = self._delete_recursive(self.root, room_number)
    
    def _delete_recursive(self, node, room_number):
        if not node:
            return node
        
        if room_number < node.room.room_number:
            node.left = self._delete_recursive(node.left, room_number)
        elif room_number > node.room.room_number:
            node.right = self._delete_recursive(node.right, room_number)
        else:
            self._cached_size -= 1
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            
            temp = node.right
            while temp.left:
                temp = temp.left
            
            node.room = temp.room
            node.right = self._delete_recursive(node.right, temp.room.room_number)

        node = self.balance(node)
        return node
    
    def search(self, room_number: int) -> Optional[Room]:
        node = self.root
        while node:
            if room_number == node.room.room_number:
                return node.room
            elif room_number < node.room.room_number:
                node = node.left
            else:
                node = node.right
        return None
    
    def change_room(self, n, method):
        if not self.root:
            return 
        stack = []
        current = self.root
        
        while stack or current:
            while current:
                if method == 1:
                    current.room.room_number += n
                elif method == 2:
                    current.room.room_number *= n
                stack.append(current)
                current = current.left

            current = stack.pop()
            
            current = current.right

    def inorder_traversal(self) -> List[Room]:
        if not self.root:
            return []
        
        rooms = []
        stack = []
        current = self.root
        
        while stack or current:
            while current:
                stack.append(current)
                current = current.left
            
            current = stack.pop()
            rooms.append(current.room)
            
            current = current.right
        
        return rooms
    
    def print_inorder(self):
        if not self.root:
            print("Tree is empty")
            return
        count = 0
        stack = []
        current = self.root
        while stack or current:
            while current:
                stack.append(current)
                current = current.left
            current = stack.pop()
            print(current.room)
            count += 1
            current = current.right
        return count
    
    def size(self) -> int:
        return self._cached_size