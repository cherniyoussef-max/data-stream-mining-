from .sampling import positive_int


class DGIM:
    """Exponential buckets, newest first, with bounded modulo timestamps."""

    def __init__(self, N: int):
        positive_int(N, "N")
        self.N = N
        self.timestamp = 0
        self._modulus = N + 1
        self.buckets: list[tuple[int, int]] = []
        self.merges: list[tuple[int, int]] = []

    def age(self, timestamp: int) -> int:
        return (self.timestamp - timestamp) % self._modulus

    def add(self, bit: int) -> None:
        if type(bit) not in (int, bool) or bit not in (0, 1):
            raise ValueError("Un bit doit valoir 0 ou 1.")
        self.timestamp = (self.timestamp + 1) % self._modulus
        self.merges.clear()
        if self.buckets and self.age(self.buckets[-1][0]) == self.N:
            self.buckets.pop()
        if not bit:
            return
        self.buckets.insert(0, (self.timestamp, 1))
        index = 0
        while index + 2 < len(self.buckets):
            size = self.buckets[index][1]
            if self.buckets[index + 2][1] != size:
                break
            timestamp = self.buckets[index + 1][0]
            self.buckets[index + 1:index + 3] = [(timestamp, 2 * size)]
            self.merges.append((size, 2 * size))
            index += 1

    def count(self) -> int:
        if not self.buckets:
            return 0
        sizes = [size for _, size in self.buckets]
        return sum(sizes[:-1]) + max(1, sizes[-1] // 2)

    def num_buckets(self) -> int:
        return len(self.buckets)
