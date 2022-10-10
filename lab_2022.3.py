def read_inp_list():
    n = int(input())
    input_arr = []
    cur_inp = [int(i) for i in input().split()]
    i = 0
    while cur_inp[i] != 32767:
        input_arr.append(cur_inp[i])
        i += 1
        if i == 10:
            cur_inp = [int(i) for i in input().split()]
            i = 0
    input_arr.append(32767)
    return input_arr


def b_k_alg(w_start_end_arr, n):
    w_start_end_arr.sort(key=lambda x: x[0])
    comp = [i for i in range(n)]
    result = {}
    all_weight = 0
    for weight, start, end in w_start_end_arr:
        if comp[start] != comp[end]:
            a = comp[start]
            b = comp[end]
            all_weight += weight
            if start in result.keys():
                result[start].append(end)
            else:
                result[start] = [end]

            if end in result:
                result[end].append(start)
            else:
                result[end] = [start]
            for i in range(n):
                if comp[i] == b:
                    comp[i] = a
    return result, all_weight


inp_arr = read_inp_list()
w_start_end_arr = []
added = set()
for i in range(inp_arr[0]):
    if inp_arr[inp_arr[i] - 1] == 32767:
        break
    for j in range(inp_arr[i] - 1, inp_arr[i + 1] - 1, 2):
        if (inp_arr[j], i + 1) in added:
            continue
        w_start_end_arr.append([inp_arr[j + 1], i, inp_arr[j] - 1])
        added.add((i + 1, inp_arr[j]))

result, w = b_k_alg(w_start_end_arr, inp_arr[0] - 2)

for k in range(inp_arr[0] - 2):
    print(' '.join(map(lambda x: str(x + 1), sorted(result[k]))), 0)
print(w)
