# 10 4 3
# 1 2 3 4 1 2 3 1 2 1

n, m, k = input().split(' ')
data = input().split(' ')

res = []
for i in range(int(k)):
    res.append([])

d = {(a + 1, data[a]): data[a] for a in range(int(n))}

i = 0
for key, value in sorted(d.items(), key=lambda item: item[1]):
    index = key[0]
    val = key[1]
    res[i].append(index)
    i = (i + 1) % int(k)

for i in range(int(k)):
    print(str(len(res[i])) + ' ' + ''.join(str(x) + ' ' for x in res[i]))
