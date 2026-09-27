import sys
import timeit
import matplotlib.pyplot as plt
from functools import lru_cache

# Збільшуємо ліміт рекурсії для обчислення глибоких чисел Фібоначчі
sys.setrecursionlimit(3000)

class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None

class SplayTree:
    def __init__(self):
        self.root = None

    def _right_rotate(self, x):
        y = x.left
        x.left = y.right
        y.right = x
        return y

    def _left_rotate(self, x):
        y = x.right
        x.right = y.left
        y.left = x
        return y

    def _splay(self, root, key):
        if root is None or root.key == key:
            return root

        if root.key > key:
            if root.left is None:
                return root
            if root.left.key > key:  # Zig-Zig
                root.left.left = self._splay(root.left.left, key)
                root = self._right_rotate(root)
            elif root.left.key < key:  # Zig-Zag
                root.left.right = self._splay(root.left.right, key)
                if root.left.right is not None:
                    root.left = self._left_rotate(root.left)
            return root if root.left is None else self._right_rotate(root)
        else:
            if root.right is None:
                return root
            if root.right.key > key:  # Zag-Zig
                root.right.left = self._splay(root.right.left, key)
                if root.right.left is not None:
                    root.right = self._right_rotate(root.right)
            elif root.right.key < key:  # Zag-Zag
                root.right.right = self._splay(root.right.right, key)
                root = self._left_rotate(root)
            return root if root.right is None else self._left_rotate(root)

    def search(self, key):
        self.root = self._splay(self.root, key)
        if self.root is not None and self.root.key == key:
            return self.root.value
        return None

    def insert(self, key, value):
        if self.root is None:
            self.root = Node(key, value)
            return
        
        self.root = self._splay(self.root, key)
        if self.root.key == key:
            return  # Ключ вже існує
        
        new_node = Node(key, value)
        if self.root.key > key:
            new_node.right = self.root
            new_node.left = self.root.left
            self.root.left = None
        else:
            new_node.left = self.root
            new_node.right = self.root.right
            self.root.right = None
        self.root = new_node

@lru_cache(maxsize=None)
def fibonacci_lru(n):
    if n < 2:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)

def fibonacci_splay(n, tree):
    cached_val = tree.search(n)
    if cached_val is not None:
        return cached_val
    if n < 2:
        tree.insert(n, n)
        return n
    
    val = fibonacci_splay(n - 1, tree) + fibonacci_splay(n - 2, tree)
    tree.insert(n, val)
    return val

if __name__ == "__main__":
    n_values = list(range(0, 951, 50))
    lru_times = []
    splay_times = []
    
    # Ініціалізуємо Splay Tree один раз для збереження стану між викликами
    tree = SplayTree()

    # Збираємо дані
    for n in n_values:
        # Вимірюємо час виконання LRU
        t_lru = timeit.timeit(lambda: fibonacci_lru(n), number=10) / 10
        lru_times.append(t_lru)
        
        # Вимірюємо час виконання Splay Tree
        t_splay = timeit.timeit(lambda: fibonacci_splay(n, tree), number=10) / 10
        splay_times.append(t_splay)

    # 1. Вивід текстової таблиці
    print(f"{'n':<10}{'LRU Cache Time (s)':<20}{'Splay Tree Time (s)':<20}")
    print("-" * 50)
    for i, n in enumerate(n_values):
        print(f"{n:<10}{lru_times[i]:<20.8f}{splay_times[i]:<20.8f}")

    # 2. Побудова графіка
    plt.figure(figsize=(10, 6))
    plt.plot(n_values, lru_times, marker='o', label='LRU Cache', color='blue')
    plt.plot(n_values, splay_times, marker='s', label='Splay Tree', color='orange')
    
    plt.xlabel('Число Фібоначчі (n)')
    plt.ylabel('Середній час виконання (секунди)')
    plt.title('Порівняння часу виконання LRU Cache та Splay Tree')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.show()