from typing import List
import time


class BacktrackingBinPacking:
    def __init__(self, item_sizes: List[int], bin_capacity: int):
        self.original_items = item_sizes[:]
        self.bin_capacity = bin_capacity

        self.best_solution = None
        self.best_bin_count = float('inf')

        indexed = list(enumerate(item_sizes))
        indexed.sort(key=lambda x: x[1], reverse=True)

        self.sorted_indices = [i for i, _ in indexed]
        self.sorted_sizes = [s for _, s in indexed]

    def solve(self):
        start = time.perf_counter()

        initial_bins = self.first_fit_decreasing()
        self.best_solution = [b[:] for b in initial_bins]
        self.best_bin_count = len(initial_bins)

        self._backtrack(0, [], [])

        elapsed = time.perf_counter() - start

        result = []
        for b in self.best_solution:
            result.append([self.sorted_indices[i] for i in b])

        return {
            "bins": result,
            "time": elapsed
        }

    def first_fit_decreasing(self):
        bins = []
        loads = []

        for i, size in enumerate(self.sorted_sizes):
            placed = False

            for j in range(len(bins)):
                if loads[j] + size <= self.bin_capacity:
                    bins[j].append(i)
                    loads[j] += size
                    placed = True
                    break

            if not placed:
                bins.append([i])
                loads.append(size)

        return bins

    def _backtrack(self, idx, bins, loads):

        if len(bins) >= self.best_bin_count:
            return

        if idx == len(self.sorted_sizes):
            self.best_bin_count = len(bins)
            self.best_solution = [b[:] for b in bins]
            return

        size = self.sorted_sizes[idx]
        used = set()

        for i in range(len(bins)):
            if loads[i] + size <= self.bin_capacity:

                if loads[i] in used:
                    continue
                used.add(loads[i])

                bins[i].append(idx)
                loads[i] += size

                self._backtrack(idx + 1, bins, loads)

                loads[i] -= size
                bins[i].pop()

        bins.append([idx])
        loads.append(size)

        self._backtrack(idx + 1, bins, loads)

        bins.pop()
        loads.pop()