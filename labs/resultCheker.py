import matplotlib.pyplot as plt
f = open("result.txt","r")

ds = {}

lines = f.readlines()
data = {}
for l in lines:
    line = l.split(' ')
    ds_num = line[0]
    high = line[1]
    f_micro = line[2]
    f_macro = line[3]

    d = {}
    d["ds_num"] = ds_num
    d["high"] = high
    d["f"] = f_macro

    if ds.get(ds_num) != None:
        ds[ds_num] += 1
        data[ds_num].append(d)
    else:
        ds[ds_num] = 1
        data[ds_num] = []
        data[ds_num].append(d)

def find_max_and_index(array):
    index = -1
    max = -1
    for a in array:
        if (float(a["f"]) > max):
            max = float(a["f"])
            index = a["high"]

    return (index,max)

d_h = {}

print("Optimal hights:")
for d in data.keys():
    arr = data[d]
    (high,f) = find_max_and_index(arr)
    d_h[d] = high
    print(d+": "+str(high)+" "+str(f))
print()

def find_max(dict):
    max = -1
    h = -1
    for d in dict.keys():
        if (float(dict[d]) > max):
            max = float(dict[d])
            h = d
    return h

def find_min(dict):
    min = 2
    h = -1
    for d in dict.keys():
        if (float(dict[d]) < min):
            min = float(dict[d])
            h = d
    return h

def find_medium(dict):
    # dict.sort()
    sorted_dict = sorted(dict.items(), key=lambda kv: kv[1])
    medium = sorted_dict.pop(int((len(sorted_dict)-1)/2))
    # t = dict.values().sort()
    return medium[0]

tree_with_greatesе_optimal_high = find_max(d_h)
print("max "+tree_with_greatesе_optimal_high)
tree_with_lowest_optimal_high = find_min(d_h)
print("min "+tree_with_lowest_optimal_high)
tree_with_medium_optimal_high = find_medium(d_h)
print("medium: "+tree_with_medium_optimal_high)

def plot_h_f(data, title):
    hights = []
    fs = []
    for m in data:
        hights.append(float(m["high"]))
        fs.append(float(m["f"]))

    plt.plot(hights,fs)
    plt.title(title)
    plt.show()


plot_h_f(data[tree_with_greatesе_optimal_high],"Dataset "+tree_with_greatesе_optimal_high+": greatest optimal high")
plot_h_f(data[tree_with_lowest_optimal_high], "Dataset "+tree_with_lowest_optimal_high+": lowest optimal high")
plot_h_f(data[tree_with_medium_optimal_high], "Dataset "+tree_with_medium_optimal_high+": medium optimal high")
