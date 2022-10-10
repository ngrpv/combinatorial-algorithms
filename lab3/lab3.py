import sys


def get_next_and_previous_lists(n: int, matrix: list[list[int]]) -> (
        list[int], list[int]):
    next = [[] for _ in range(n)]
    prev = [[] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if matrix[i][j] != -32768:
                next[i].append(j)
                prev[j].append(i)
    return next, prev


def parse_from_file(filename: str) -> (list[list[int]], int):
    matrix = []
    with open(filename, 'r') as f:
        n = int(f.readline())
        for i in range(n):
            matrix.append([int(k) for k in f.readline().split()])
        start = int(f.readline()) - 1
        end = int(f.readline()) - 1
    return matrix, n, start, end


def tarian_sort(prev: list[list[int]], next: list[list[int]]) -> list[int]:
    n = len(prev)
    white = list(range(n))
    grey = []
    black = []

    def step(current):
        if current in black:
            return
        if current in grey:
            raise Exception
        if current in white:
            grey.append(current)
            for i in next[current]:
                step(i)
            black.append(current)

    for i in range(n):
        step(i)
    return black


def get_path(start: int, end: int, top_sorted: list[int],
             prev: list[list[int]], next: list[list[int]],
             matrix: list[list[int]]) -> (list[int], int):
    start_index = top_sorted.index(start)
    n = len(top_sorted)
    reachable = {start}
    max_paths = [-sys.maxsize] * n
    max_paths[start] = 0
    prev_path = [start] * n
    for i in range(start_index + 1, n):
        node = top_sorted[i]
        for p in prev[node]:
            if (p in reachable and
                    matrix[p][node] + max_paths[p] > max_paths[node]):
                max_paths[node] = matrix[p][node] + max_paths[p]
                prev_path[node] = p
                reachable.add(node)
        if node == end:
            return get_path_from_prev_list(prev_path, start, end), max_paths[node]


def get_path_from_prev_list(prev: list[int], start: int, end: int) -> list[
    int]:
    reversed_path = [end]
    current = end
    for _ in range(len(prev)):
        reversed_path.append(prev[current])
        current = prev[current]
        if current == start:
            reversed_path.reverse()
            return reversed_path


def write_out(filename, path, sum):
    with open(filename, 'w') as f:
        if path is None:
            f.write("N")
            return
        result = "Y\n"
        result += " ".join([str(j) for j in path])
        result += "\n" + str(sum)
        f.write(result)


if __name__ == '__main__':
    matrix, n, start, end = parse_from_file('in.txt')
    next, prev = get_next_and_previous_lists(n, matrix)
    top_sorted = tarian_sort(prev, next)
    top_sorted.reverse()
    path_and_sum = get_path(start, end, top_sorted, prev, next, matrix)
    if path_and_sum is None:
        write_out("out.txt", None, 0)
    else:
        write_out("out.txt", [i + 1 for i in path_and_sum[0]], path_and_sum[1])
