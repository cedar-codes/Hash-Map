# Hash-Map-OA-SC
# Author: Rachel Hoeferlin
# June 2024
# Data Structures Portfolio Project

This project showcases a HashMap implementation in Python, utilizing both open addressing with quadratic probing and separate chaining with linked lists for collision resolution. The goal was to create a versatile and efficient data structure that demonstrates various hashing techniques.

Features

Open Addressing with Tombstone Placement:
Collisions are resolved using quadratic probing.
Each entry in the dynamic array can store a key/value pair or a tombstone to indicate removed elements.

Separate Chaining with Linked Lists:
Each bucket of the hash map uses a linked list to handle collisions, allowing for efficient insertions and lookups.

Key Methods

- put(key, value): Inserts a key/value pair.
- resize_table(): Resizes the underlying storage array.
- table_load(): Returns the current load factor of the hash map.
- empty_buckets(): Counts and returns the number of empty buckets.
- get(key): Retrieves the value associated with a given key.
- contains_key(key): Checks if a key exists in the hash map.
- remove(key): Removes the key/value pair from the hash map.
- get_keys_and_values(): Returns a dynamic array of tuples containing all key/value pairs.
- clear(): Clears all entries in the hash map.
- find_mode(): Returns the mode(s) of the stored keys along with their frequency.
- __iter__() and __next__(): Enable iteration over active elements in the hash map.

Efficiency
All primary methods are optimized to O(1) or O(n) efficiency, ensuring rapid data retrieval and manipulation.

Installation
Clone the repository and use the following command to run the project:

bash
Copy code
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
Usage
Import the HashMap class and create an instance:

python
Copy code
from hashmap import HashMap

hash_map = HashMap()
hash_map.put('key1', 'value1')
print(hash_map.get('key1'))  # Output: value1


License
This project is licensed under the MIT License. See the LICENSE file for more details.
