
def f_measure(data, n, number_elements):
    f_macro = 0
    precision_micro = 0
    recall_micro = 0

    for i in range(int(n)):
        a = data[i][i]
        c = sum(data[i])
        s = 0
        for j in range(int(n)):
            s += data[j][i]

        if (s == 0):
            precision = 0
        else:
            precision = a / s

        if (c == 0):
            recall = 0
        else:
            recall = a / c

        if (precision + recall == 0):
            f = 0
        else:
            f = 2 * precision * recall / (precision + recall)
        f_macro += f * c
        precision_micro += precision * c
        recall_micro += recall * c

    precision_micro = precision_micro / number_elements
    recall_micro = recall_micro / number_elements
    f_micro = 2 * precision_micro * recall_micro / (precision_micro + recall_micro)

    f_macro = f_macro / number_elements
    return (f_micro, f_macro)
