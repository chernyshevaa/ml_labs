# 2 4 2
# 8
# 1 2 1
# 2 1 1
# 3 1 2
# 4 2 2
# 3 4 3
# 4 3 3
# 1 3 4
# 2 4 4

# data preprocessing

import math
import random

line = input()
line_int = line.split(' ')
m   = int(line_int[0])
k = int(line_int[1])
h = int(line_int[2])

n = int(input())
classes = []
data_arr = []

for i in range(n):
    line_int = input().split(' ')

    row = []
    for x in line_int:
        row.append(int(x))

    classes.append(line_int[m])
    data_arr.append(row)

num_attributes = m
num_classes = k
tree_high = h + 1

attributes = []
for i in range(m):
    attributes.append(i)

class Node:
    def __init__(self, isLeaf, label, threshold):
        self.label = label
        self.isLeaf = isLeaf
        self.threshold = threshold
        self.children = []


def isSameClass(data):
    first_class = data[0][num_attributes]
    for row in data:
        if row[num_attributes] != first_class:
            return False
    return first_class


def getClass(data):
    classes_freq = []
    for i in range(num_classes):
        classes_freq.append(0)

    for row in data:
        classes_freq[row[num_attributes] - 1] += 1

    max_freq = classes_freq.index(max(classes_freq))
    return (max_freq + 1)


def getRandomThresholds(t_range, number):
    thresholds = []
    for ii in range(number):
        t = random.randint(0, t_range-1)
        thresholds.append(t)
    return thresholds


def createTree(data, attributes, high):
    sameClass = isSameClass(data)

    if (len(data) == 0):

        return Node(True, "Empty", None)
    elif (sameClass != False):
        return Node(True, int(sameClass) - 1, None)
    elif (len(attributes) == 0):
        return Node(True, int(getClass(data)) - 1, None)
    elif (high >= tree_high):
        return Node(True, int(getClass(data)) - 1, None)
    else:
        (best_attribute, best_threshold, splitted) = split_attributes(data, attributes)
        remaining_attributes = attributes[:]
        remaining_attributes.remove(best_attribute)
        node = Node(False, best_attribute, best_threshold)
        node.children = [createTree(subset, remaining_attributes, high + 1) for subset in splitted]
        if (node.children[0].isLeaf == True & node.children[1].isLeaf == True & node.children[1].label == node.children[
            0].label):
            return Node(True, node.children[0].label, None)
            # return Node(True, node.children[0].label, None)
        else:
            return node


def gain(subsets, impurityBefore):
    s = len(subsets[0]) + len(subsets[1])

    weights = [len(subset) / s for subset in subsets]
    impurityAfter = 0
    for i in range(len(subsets)):
        # impurityAfter += weights[i] * entropy(subsets[i])
        impurityAfter += weights[i] * random.random()

    gain = impurityBefore - impurityAfter

    return gain


def entropy(dataSet):
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


def split_attributes(current_data, current_attributes):
    splitted = []
    max_entropy = -1 * float("inf")
    best_attribute = -1
    best_threshold = None

    for attribute in current_attributes:
        # 1
        attribute_index = attribute

        # current_data.sort(key=lambda x: x[attribute_index])

        # random_thresholds = getRandomThresholds(len(current_data)-1, 1)

        # fullset_entrophy = entropy(current_data)

        for i in range(len(current_data) - 1):
        # for i in random_thresholds:
            if current_data[i][attribute_index] != current_data[i + 1][attribute_index]:
                threshold = (current_data[i][attribute_index] + current_data[i + 1][attribute_index]) / 2
                less = []
                greater = []

                for row in current_data:
                    if (row[attribute_index] > threshold):
                        greater.append(row)
                    else:
                        less.append(row)


                # e = gain([less, greater], fullset_entrophy)
                e = random.random()
                if e > max_entropy:
                    splitted = [less, greater]
                    max_entropy = e
                    best_attribute = attribute
                    best_threshold = threshold

    return (best_attribute, best_threshold, splitted)


print_tree = []


def printTree(node, count):
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
        first_count = printTree(node.children[0], count + 1)
        second_count = printTree(node.children[1], first_count + 1)

        string = print_tree[count - 1]
        string += (" " + str(count + 1))
        string += (" " + str(first_count + 1))
        print_tree[count - 1] = string

        count = second_count

    return count


root = createTree(data_arr, attributes, 1)
printTree(root, 1)
print(len(print_tree))
for node_str in print_tree:
    print(node_str)
