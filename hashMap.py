"""
The HashMap class holds all Package objects and hashes each Package to the Package ID. The HashMap is initialized with
a capacity of 10, but when a HashMap object is created it can be initialized to a different size. This is a chaining
HashMap, with each Package object held in a separate bucket. If the HashMap needed to be scaled upward, buckets could
hold multiple Package objects.

Each key is hashed by the size of the table. The insert method hashes the ID to find the correct bucket and adds the
Package to that bucket. The lookup method returns the key / Package ID.
"""


class HashMap:
    def __init__(self, initial_capacity=10):
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    def get_hash(self, key):
        bucket = key % len(self.table)
        bucket_list = self.table[bucket]
        return bucket_list

    def insert(self, package):
        # find bucket where this package will go
        bucket = self.get_hash(package.pack_id)

        # put package in bucket_list
        bucket.append(package)

    def lookup(self, key):
        bucket = self.get_hash(key)

        # search for key
        for key in bucket:
            pack_index = bucket.index(key)
            return bucket[pack_index]
        return None


