offsets_for_knight = [

    (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), ]
offsets_for_pawn = [(-1, -1), (1, -1)]


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return (self.x, self.y).__hash__()


class LinkedList:
    def __init__(self, value: Point, tail):
        self.value = value
        self.tail = tail


def get_steps_from(start_x, start_y, offsets):
    for (dx, dy) in offsets:
        yield Point(dx + start_x, dy + start_y)


def get_steps_on_bounds(max_coordinates: Point, start: Point, offsets):
    for p in get_steps_from(start.x, start.y, offsets):
        if p.x >= 0 and p.x <= max_coordinates.x and p.y >= 0 and p.y <= max_coordinates.y:
            yield p


def get_steps_without_under_attack(pawn: Point, knight: Point):
    under_pawn_attack_coordinates = list(get_steps_on_bounds(Point(7, 7), pawn,
                                                             offsets_for_pawn))
    for p in get_steps_on_bounds(Point(7, 7), knight, offsets_for_knight):
        if not p in under_pawn_attack_coordinates:
            yield p


def dfs_knight_to_pawn(start_knight: Point, end: Point):
    stack = [LinkedList(start_knight, None)]
    visited = set()
    while stack:
        current = stack.pop()
        if current.value in visited:
            continue
        visited.add(current.value)
        if current.value == end:
            return get_way_from_linked_list(current)

        for p in get_steps_without_under_attack(end, current.value):
            if p not in visited:
                neighbour = Point(p.x, p.y)
                stack.append(LinkedList(neighbour, current))


def chess_notation_to_coordinates(n):
    return Point(ord(n[0]) - ord('a'), int(n[1]) - 1)


def coordinate_to_chess_notation(p: Point):
    return chr(p.x + ord('a')) + str(p.y + 1)


def get_way_from_linked_list(node):
    path = []
    while node != None:
        path.append(node.value)
        node = node.tail
    path.reverse()
    return path


def get_input(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return [f.readline(), f.readline()]


def write(filename, out_stream):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('\n'.join(out_stream))


if __name__ == '__main__':
    (knight_start, end) = [chess_notation_to_coordinates(i) for i in
                           get_input('in.txt')]
    path = dfs_knight_to_pawn(knight_start, end)

    out = [coordinate_to_chess_notation(i) for i in path]
    write('out.txt', out)