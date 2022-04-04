class Node:
    def __init__(self, number: int, come_from):
        self.number = number
        self.come_from = come_from


def find_cycles_bfs(matrix: [[]]):
    node_to_come_from_node = {0: -1}
    queue = []
    queue.append(Node(0, -1))
    visited = set()
    while (len(queue) > 0):
        current = queue.pop(0)
        if current.number in visited:
            return build_cycle(node_to_come_from_node, current.number,
                               current.come_from)
        visited.add(current.number)
        node_to_come_from_node[current.number] = current.come_from
        for i in get_incident(matrix, current.number):
            if i != current.come_from:
                queue.append(Node(int(i), current.number))


def get_incident(matrix, node_num):
    incident = []
    for i in range(len(matrix[node_num])):
        if matrix[node_num][i] == '1':
            incident.append(i)

    return incident


def build_cycle(node_to_come_from_dict, intersection_point, come_from_point):
    first_path: [int] = build_path(node_to_come_from_dict, intersection_point)
    second_path = build_path(node_to_come_from_dict, come_from_point)
    intersection = -1
    for i in first_path:
        if i in second_path:
            intersection = i
            break

    first_path.reverse()
    return first_path[first_path.index(intersection):] + second_path[
                                                         :second_path.index(
                                                             intersection)]


def build_path(node_to_come_from_point, i) -> []:
    path = []
    while i != -1:
        path.append(i)
        i = node_to_come_from_point[i]
    return path


def get_input(filename) -> [[]]:
    with open(filename, 'r') as f:
        n = int(f.readline())
        matrix = []
        for i in range(n):
            matrix.append(f.readline().split())

    return matrix


def write(filename, text):
    with open(filename, 'w') as f:
        f.write(text)


if __name__ == '__main__':
    input = get_input('in.txt')
    cycle = find_cycles_bfs(input)
    if cycle is None:
        write('out.txt', 'A')
    else:
        write('out.txt',
              'N ' + ' '.join(([str(i + 1) for i in sorted(cycle)])))
