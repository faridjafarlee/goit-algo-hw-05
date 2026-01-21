class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(self.size)]

    def hash_function(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        key_hash = self.hash_function(key)
        key_value = [key, value]

        if self.table[key_hash] is None:
            self.table[key_hash] = list([key_value])
            return True
        else:
            for pair in self.table[key_hash]:
                if pair[0] == key:
                    pair[1] = value
                    return True
            self.table[key_hash].append(key_value)
            return True

    def get(self, key):
        key_hash = self.hash_function(key)
        if self.table[key_hash] is not None:
            for pair in self.table[key_hash]:
                if pair[0] == key:
                    return pair[1]
        return None

    def delete(self, key):
        idx = self.hash_function(key)
        bucket = self.table[idx]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                return True
        return False


if __name__ == "__main__":
    ht = HashTable(7)
    ht.insert("a", 1)
    ht.insert("b", 2)
    ht.insert("a", 11)

    print("get(a):", ht.get("a"))
    print("delete(a):", ht.delete("a"))
    print("get(a):", ht.get("a"))
    print("delete(a) again:", ht.delete("a"))
