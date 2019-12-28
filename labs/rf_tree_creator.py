import math
import random


# num_attributes = 0
# num_classes = 0
# tree_high = 0
#
# classes = []

def tree(ds_num, h):
    overall_tree_high = 1

    dataset_file = "dt_data/" + ds_num + "_train.txt"
    f = open(dataset_file, 'r')
    line = f.readline()

    line_int = line.split(' ')
    m = int(line_int[0])
    k = int(line_int[1])

    n = int(f.readline())

    data = {}
    classes = []
    data_arr = []

    sqrt_n = int(math.sqrt(n))
    random_n = []
    for i in range(sqrt_n):
        random_n.append(random.randint(1, n-1))


    new_number = 0
    for i in range(n):
        if i in random_n:
            line = f.readline()
            line_int = line.split(' ')

            row = []
            for x in line_int:
                row.append(int(x))

            obj = {}
            obj["c"] = line_int[m]
            line_int.pop(m)
            obj["f"] = line_int

            data[i] = obj

            classes.append(obj["c"])
            data_arr.append(row)
            new_number += 1

    f.close()

    n = new_number

    num_attributes = m
    num_classes = k
    # tree_high = h + 1
    tree_high = 50

    attributes = []
    for i in range(m):
        attributes.append(i)

    root = createTree(data_arr, attributes, 1, overall_tree_high, tree_high, classes, num_attributes, num_classes)
    print_tree = []

    printTree(root, 1, print_tree)
    # print(len(print_tree))
    # for node_str in print_tree:
    #     print(node_str)

    f = open("rf/tree_" + ds_num + "_" + str(h), "w+")
    f.write(str(len(print_tree)))
    f.write('\n')
    for node_str in print_tree:
        f.write(node_str)
        f.write('\n')

    # print("high: " + str(overall_tree_high))


class Node:
    def __init__(self, isLeaf, label, threshold):
        self.label = label
        self.isLeaf = isLeaf
        self.threshold = threshold
        self.children = []


def isSameClass(data, num_attributes):
    first_class = data[0][num_attributes]
    for row in data:
        if row[num_attributes] != first_class:
            return False
    return first_class


def getClass(data, num_classes, num_attributes):
    classes_freq = []
    for i in range(num_classes):
        classes_freq.append(0)

    for row in data:
        classes_freq[row[num_attributes] - 1] += 1

    max_freq = classes_freq.index(max(classes_freq))
    return (max_freq + 1)


def createTree(data, attributes, high, overall_tree_high, tree_high, classes, num_attributes, num_classes):
    if (int(high) > int(overall_tree_high)):
        overall_tree_high = high
    sameClass = isSameClass(data, num_attributes)

    if (len(data) == 0):

        return Node(True, "Empty", None)
    elif (sameClass != False):
        return Node(True, int(sameClass) - 1, None)
    elif (len(attributes) == 0):
        return Node(True, int(getClass(data, num_classes, num_attributes)) - 1, None)
    elif (high >= tree_high):
        return Node(True, int(getClass(data, num_classes, num_attributes)) - 1, None)
    else:
        (best_attribute, best_threshold, splitted) = split_attributes(data, attributes, classes, num_attributes)
        remaining_attributes = attributes[:]
        if (best_attribute == -1):
            return Node(True, int(getClass(data, num_classes, num_attributes)) - 1, None)
        remaining_attributes.remove(best_attribute)
        node = Node(False, best_attribute, best_threshold)
        node.children = [
            createTree(subset, remaining_attributes, high + 1, overall_tree_high, tree_high, classes, num_attributes,
                       num_classes) for subset in splitted]
        # if get majority class in both cases are the same
        if (node.children[0].isLeaf == True & node.children[1].isLeaf == True & node.children[1].label == node.children[
            0].label):
            return Node(True, node.children[0].label, None)
            # return Node(True, node.children[0].label, None)
        else:
            return node


def gain(fullSet, subsets, classes, num_attributes):
    s = len(fullSet)
    impurityBefore = entropy(fullSet, classes, num_attributes)

    weights = [len(subset) / s for subset in subsets]
    impurityAfter = 0
    for i in range(len(subsets)):
        impurityAfter += weights[i] * entropy(subsets[i], classes, num_attributes)

    gain = impurityBefore - impurityAfter

    return gain


def entropy(dataSet, classes, num_attributes):
    s = len(dataSet)
    if s == 0:
        return 0
    n_c = [0 for j in classes]

    for row in dataSet:
        class_index = row[num_attributes]
        n_c[class_index - 1] += 1

    n_c = [x / s for x in n_c]

    ent = 0
    for n in n_c:
        ent += n * log(n)

    return ent * (-1)


def log(x):
    if (x == 0):
        return 0
    else:
        return math.log(x, 2)


def getRandomThresholds(t_range, number):
    thresholds = []
    for ii in range(number):
        t = random.randint(0, t_range - 1)
        thresholds.append(t)
    return thresholds


def split_attributes(current_data, current_attributes, classes, num_attributes):
    splitted = []
    max_entropy = -1 * float("inf")
    best_attribute = -1
    best_threshold = None

    for attribute in current_attributes:
        # attribute_index = attributes.index(attribute)
        attribute_index = attribute

        current_data.sort(key=lambda x: x[attribute_index])

        middle_threshold = int((len(current_data) - 1) / 2)
        random_thresholds = []
        random_thresholds.append(middle_threshold)

        # random 10, 20, ... thresholds index
        # save previous class distribution to compute less
        # for zz in range(10):
        #     random_thresholds = getRandomThresholds(len(current_data) - 1, 20)

        # for i in range(len(current_data) -1):
        for i in random_thresholds:
            if current_data[i][attribute_index] != current_data[i + 1][attribute_index]:
                threshold = (current_data[i][attribute_index] + current_data[i + 1][attribute_index]) / 2
                less = []
                greater = []

                for row in current_data:
                    if (row[attribute_index] > threshold):
                        greater.append(row)
                    else:
                        less.append(row)

                e = gain(current_data, [less, greater], classes, num_attributes)
                if e > max_entropy:
                    splitted = [less, greater]
                    max_entropy = e
                    best_attribute = attribute
                    best_threshold = threshold


        return (best_attribute, best_threshold, splitted)


def printTree(node, count, print_tree):
    node_type = ""
    if node.isLeaf == True:
        node_type = "C"
    else:
        node_type = "Q"

    n_attribute = str(int(node.label) + 1)

    t = ""
    if node.threshold != None:
        t = str(node.threshold)

    node_str = node_type + " " + n_attribute + " " + t

    print_tree.append(node_str)
    if (node.children):
        first_count = printTree(node.children[0], count + 1, print_tree)
        second_count = printTree(node.children[1], first_count + 1, print_tree)

        string = print_tree[count - 1]
        string += (" " + str(count + 1))
        string += (" " + str(first_count + 1))
        print_tree[count - 1] = string

        count = second_count

    return count
