in_txt = 'in.txt'
out_txt = 'out.txt'

original_c = []
c = []
s = 0
t = 0
n = 0
with open(in_txt, 'r') as f:
    n = int(f.readline())
    for _ in range(n):
        line = f.readline()
        original_c.append([int(i) for i in line.split()])
        c.append([int(i) for i in line.split()])
    s = int(f.readline()) - 1
    t = int(f.readline()) - 1


def get_residual_network(graph):
    return graph.copy()


def get_path(s, t, graph):
    visited = [s]
    queue = [(s, [s])]
    while len(queue) > 0:
        v, path = queue.pop(0)
        for j in range(len(graph[v])):
            w = graph[v][j]
            if w <= 0 or j in visited:
                continue
            if j == t:
                return path + [t]
            queue.append((j, path + [j]))
            visited.append(j)


def get_min_c(path, graph):
    m = graph[path[0]][path[1]]
    for i in range(1, len(path)):
        if graph[path[i - 1]][path[i]] < m:
            m = graph[path[i - 1]][path[i]]
    return m


p = get_path(s, t, c)
f = [[0] * n for _ in range(n)]
while p != None:
    min_c = get_min_c(p, c)
    for i in range(1, len(p)):
        u = p[i - 1]
        v = p[i]
        f[u][v] = f[u][v] + min_c
        f[v][u] = f[v][u] - min_c
        c[u][v] = original_c[u][v] - f[u][v]
        c[v][u] = f[u][v]
    p = get_path(s, t, c)

for row in f:
    for i in range(len(row)):
        if row[i] < 0:
            row[i] = 0
stream_val = 0
for x in f[0]:
    stream_val += x

with open(out_txt, 'w') as write_f:
    for row in f:
        write_f.write(' '.join(map(str, row)) + '\n')
    write_f.write(str(stream_val))
