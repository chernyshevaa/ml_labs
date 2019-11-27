import f_measure

def read_tree_and_predict(ds_num):
    # ds_num = "21"

    tree_file = "trees/tree_" + str(ds_num)
    f = open(tree_file, "r")
    n = int(f.readline())

    tree = {}
    j = 1
    for i in range(n):
        line = f.readline().strip().split(' ')
        node = {}
        node["id"] = j
        if (line[0] == "Q"):
            node["isLeaf"] = False
            node["attribute"] = int(line[1]) - 1
            node["threshold"] = float(line[2])
            node["left"] = int(line[3])
            node["right"] = int(line[4])
        if line[0] == "C":
            node["isLeaf"] = True
            node["class"] = int(line[1])
        tree[j] = node
        j += 1

    f.close()

    ds_test_file = "dt_data/" + str(ds_num) + "_train.txt"
    f = open(ds_test_file, "r")
    line = f.readline()

    line_int = line.split(' ')
    m = int(line_int[0])
    k = int(line_int[1])

    n = int(f.readline())

    confusion_matrix = [[0] * k for i in range(k)]

    count = 0
    for i in range(n):
        row = f.readline().strip().split(" ")
        result = predict(tree[1], row, tree)
        # confusion_matrix[int(result)-1][int(row[m]) - 1] += 1
        confusion_matrix[int(row[m]) - 1][int(result) - 1] += 1

    # for i in range(k):
    #     print(confusion_matrix[i])

    (f_micro, f_macro) = f_measure.f_measure(confusion_matrix, k, n)

    return (f_micro, f_macro)


def predict(node, row, tree):
    if (node["isLeaf"] == True):
        return node["class"]
    if (float(row[node["attribute"]]) < node["threshold"]):
        node_left = tree[node["left"]]
        if (node_left["isLeaf"] == True):
            return node_left["class"]
        else:
            return predict(node_left, row, tree)
    else:
        node_right = tree[node["right"]]
        if (node_right["isLeaf"] == True):
            return node_right["class"]
        else:
            return predict(node_right, row, tree)



