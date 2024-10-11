# Name: Rachel Hoeferlin
# OSU Email: hoeferlr@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 06/06/24
# Description: Implementation of a Hash Map with Open Addressing, utilizing a Dynamic Array for the underlying data
# storage, and resolves collisions where the index is occupied with Tombstones and Quadratic Probing.
# Each index in the array stores key/value pairs through the use of the HashEntry class, which have a boolean
# for Tombstone placement. Tombstones are True if an element is removed, or False if the element has an active key/value
# pair.
# Includes the following methods: put() (insert key/value), resize_table(), table_load(), empty_buckets(),
# get(), contains_key(), remove(), get_keys_and_values() (returns Dynamic Array containing tuples of key/value pairs),
# clear(), __iter__() to enable iteration and initialize an index variable, and __next__() to return active elements.


from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Inserts a new element into the hash map if the key is not in the hash map.
        If the key is in the hash map, updates the key with new value.
        Maintains table load factor of less than 0.5 by resizing the table with resize_table().
        Increases the size of the hash map when inserting a new value or if it is a Tombstone value.
        """
        if self.table_load() >= 0.5:
            self.resize_table(2 * self._capacity)

        initial_index = self._hash_function(key) % self._capacity
        new_index = initial_index
        step = 1

        while self._buckets[new_index] is not None and not self._buckets[new_index].is_tombstone and self._buckets[
            new_index].key != key:
            # quadratic probing for next available index
            new_index = (initial_index + (step ** 2)) % self._capacity
            step += 1

        # inserts new HashEntry with key, value and Tombstone to False
        if self._buckets[new_index] is None or self._buckets[new_index].is_tombstone:
            self._size += 1
            self._buckets[new_index] = HashEntry(key, value)

        # updates value and Tombstone boolean if key already in map
        elif self._buckets[new_index].key == key:
            self._buckets[new_index].value = value
            self._buckets[new_index].is_tombstone = False

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the hash map with the new capacity (integer) variable passed in,
        which is double the old capacity.
        Checks that the new capacity is a prime number, else utilizes the
        is_prime() and next_prime() methods to calculate and set that as the new capacity.
        Creates a new hash table and uses indirect recursion to insert active elements and
        their key/value by utilizing the put() method.
        """
        if new_capacity < self._size:
            return

        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        self._capacity = new_capacity
        old_table = self._buckets
        self._buckets = DynamicArray()
        self._size = 0

        for index in range(self._capacity):
            self._buckets.append(None)

        for index in range(old_table.length()):
            element = old_table[index]
            # only insert elements that have a key/value, ignore Tombstone placements
            if element is not None and not element.is_tombstone:
                self.put(element.key, element.value)

    def table_load(self) -> float:
        """
        Calculates the table load factor, the average number of elements per bucket.
        Returns a float value containing the table load factor.
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Returns the number (integer) of buckets that are either None or a Tombstone.
        """
        empty_buckets = 0
        for index in range(self._capacity):
            if self._buckets[index] is None or self._buckets[index].is_tombstone:
                empty_buckets += 1

        return empty_buckets

    def get(self, key: str) -> object:
        """
        Retrieves and returns the value (object) that corresponds with the key (string) passed in.
        Returns None if key is not in the hash map.
        """
        initial_index = self._hash_function(key) % self._capacity
        new_index = initial_index
        step = 1

        while self._buckets[new_index]:
            if self._buckets[new_index].key == key and not self._buckets[new_index].is_tombstone:
                return self._buckets[new_index].value
            new_index = (initial_index + step ** 2) % self._capacity
            step += 1
        return None

    def contains_key(self, key: str) -> bool:
        """
        Utilizes the get() method to determine if the key (string) passed in is in
        the hash map.
        Returns True if key is in the map, False otherwise.
        """
        if self._size == 0:
            return False

        if self.get(key):
            return True
        return False

    def remove(self, key: str) -> None:
        """
        Removes the key passed in (string) from the hash map, decreases the map's size by 1.
        Tombstone value is set to True to indicate the removed element.
        """
        initial_index = self._hash_function(key) % self._capacity
        new_index = initial_index
        step = 1

        if not self.contains_key(key):
            return

        while self._buckets[new_index]:
            if self._buckets[new_index].key == key and not self._buckets[new_index].is_tombstone:
                # removed values become Tombstones but key/value remains same until changed
                self._buckets[new_index].is_tombstone = True
                self._size -= 1
                return
            new_index = (initial_index + step ** 2) % self._capacity
            step += 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Retrieves the keys and values of each element in the hash map and
        returns a dynamic array with a tuple at each index (key, value).
        Order does not matter.
        """
        keys_vals = DynamicArray()
        for index in range(self._buckets.length()):
            # append only elements with key/value and not Tombstones
            if self._buckets[index] is not None and not self._buckets[index].is_tombstone:
                keys_vals.append((self._buckets[index].key, self._buckets[index].value))
        return keys_vals

    def clear(self) -> None:
        """
        Deletes all elements from the hash map, creating buckets with None.
        Size becomes 0, but underlying capacity remains the same.
        """
        self._buckets = DynamicArray()
        for index in range(self._capacity):
            self._buckets.append(None)
        self._size = 0

    def __iter__(self):
        """
        Enables iteration (for i in map) and initializes an index variable to track
        each index in the map.
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Returns the next active element, which is not None or not a Tombstone value.
        Element holds the key and value of the object.
        Increases the index based on the iterator method.
        Stops iteration with the exception raised.
        """
        try:
            element = None
            # iterates until active element (is not None or not a Tombstone)
            while element is None or element.is_tombstone:
                element = self._buckets.get_at_index(self._index)
                self._index += 1

        except DynamicArrayException:
            raise StopIteration

        return element


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
