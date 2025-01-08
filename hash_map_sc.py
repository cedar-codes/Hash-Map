# Name: Rachel Hoeferlin
# Date: 06/06/24
# Description: Implementation of a Hash Map utilizing a Dynamic Array for the underlying data storage, and
# Separate Chaining with Linked Lists to resolve collisions where the index is occupied.
# Array stores key/value pairs through the use of Linked Lists for each element in the buckets of the Hash Map.
# Includes the following methods: put() (insert key/value), resize_table(), table_load(), empty_buckets(),
# get(), contains_key(), remove(), get_keys_and_values() (returns Dynamic Array containing tuples of key/value pairs),
# clear(), and find_mode() (returns tuple: (Dynamic Array of mode(s)'s key, frequency)).


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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
        Inserts a new element (key, value) into the hash map if the key is not in the hash map.
        If the key is in the hash map, updates the key with new value.
        Maintains table load factor of less than 1.0 by resizing the table using resize_table().
        Increases the underlying size of the hash map by 1 when inserting a new element.
        """
        if self.table_load() >= 1.0:
            self.resize_table(2 * self._capacity)
        # compute bucket
        table_index = self._hash_function(key) % self._capacity
        # search at that bucket for key
        node = self._buckets.get_at_index(table_index)

        # key already in hash map update its value
        if node.contains(key):
            element = node.contains(key)
            element.value = value

        # key not in hash map, add new key/value node
        else:
            node.insert(key, value)
            self._size += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the hash map with the new capacity (integer) variable passed in,
        which is double the old capacity.
        Checks that the new capacity is a prime number, else utilizes the
        is_prime() and next_prime() methods to calculate and set that as the new capacity.
        Creates a new hash table and uses indirect recursion to insert active elements and
        their key/value by utilizing the put() method.
        """
        if new_capacity < 1:
            return

        if new_capacity >= 1:
            if not self._is_prime(new_capacity):
                new_capacity = self._next_prime(new_capacity)

        self._capacity = new_capacity
        old_table = self._buckets
        self._buckets = DynamicArray()
        self._size = 0

        # create new, empty hash map
        for index in range(self._capacity):
            self._buckets.append(LinkedList())

        # use logic of put() to insert elements into new hash map
        for index in range(old_table.length()):
            node = old_table.get_at_index(index)
            for element in node:
                self.put(element.key, element.value)

    def table_load(self) -> float:
        """
        Calculates the table load factor, the average number of elements per bucket.
        Returns a float value containing the table load factor.
        """
        # number of elements divided by table size
        table_load = self._size / self._capacity
        return table_load

    def empty_buckets(self) -> int:
        """
        Returns the number (integer) of buckets that have no nodes/elements.
        """
        empty_buckets = 0
        for index in range(self._buckets.length()):
            # no chains = empty bucket
            if self._buckets.get_at_index(index).length() == 0:
                empty_buckets += 1

        return empty_buckets

    def get(self, key: str):
        """
        Retrieves and returns the value (object) that corresponds with the key (string) passed in.
        Returns None if key is not in the hash map.
        """
        table_index = self._hash_function(key) % self._capacity
        search_node = self._buckets.get_at_index(table_index)

        # contains() returns SLNode to retrieve its value
        if search_node.contains(key):
            return search_node.contains(key).value
        else:
            return None

    def contains_key(self, key: str) -> bool:
        """
        Utilizes the contains(key) method in the LinkedList class to determine if the key (string)
        passed in is in the hash map.
        Returns True if key is in the map, False otherwise.
        """
        if self._size == 0:
            return False

        table_index = self._hash_function(key) % self._capacity
        search_node = self._buckets.get_at_index(table_index)

        if search_node.contains(key):
            return True
        else:
            return False

    def remove(self, key: str) -> None:
        """
        Removes the key passed in (string) from the hash map, decreases the hash map's size by 1.
        Utilizes the remove(key) method in the LinkedList class to remove the node.
        """
        table_index = self._hash_function(key) % self._capacity
        bucket = self._buckets.get_at_index(table_index)

        if not bucket.contains(key):
            return

        if bucket.contains(key):
            self._size -= 1

        for index in range(self._buckets.length()):
            if self._buckets.get_at_index(index):
                node = self._buckets.get_at_index(index)
                node.remove(key)

        if self._size < 0:
            self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        Retrieves the keys and values of each element in the hash map and
        returns a dynamic array with a tuple at each index (key, value).
        Order does not matter.
        """
        keys_vals = DynamicArray()
        for index in range(self._buckets.length()):
            # if there are chains/is not None
            if self._buckets.get_at_index(index).length():
                # buckets at indices hold linked list nodes
                for node in self._buckets.get_at_index(index):
                    keys_vals.append((node.key, node.value))

        return keys_vals

    def clear(self) -> None:
        """
        Deletes all elements from the hash map, creating empty LinkedList() buckets at each index.
        Size becomes 0, but underlying capacity remains the same.
        """
        for index in range(self._buckets.length()):
            self._buckets.set_at_index(index, LinkedList())
        self._size = 0


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Calculates and returns a tuple with a Dynamic Array of the mode(s) (most occurring element/key)
    from the Dynamic Array passed in, with its frequency (count).
    Initializes an empty HashMap to put() the values from the DynamicArray passed in,
    counting 1 for each and adding 1 when there is a duplicate.
    """
    map = HashMap()
    frequency = 0
    mode_array = DynamicArray()

    for index in range(da.length()):
        if not map.contains_key(da[index]):
            # if element (da[index]) not in map, frequency is 1
            map.put(da[index], 1)
        else:
            # element is duplicate, increase frequency by 1
            map.put(da[index], map.get(da[index]) + 1)

    element_array = map.get_keys_and_values()
    # update frequency to be the highest value
    for index in range(element_array.length()):
        #   value = element_array.get_at_index(index)[1]
        if frequency < element_array[index][1]:
            frequency = element_array[index][1]

    # append key(s) with the highest value (mode(s))
    for index in range(element_array.length()):
        if element_array[index][1] == frequency:
            mode_array.append(element_array[index][0])

    return mode_array, frequency


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
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

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
    m = HashMap(53, hash_function_1)
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

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
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

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
