import tree_creator, tree_predict

ds_num = "05"

max_high = 50

arr = [12, 11, 13]
for j in arr:
    if j < 10:
        ds_num = "0" + str(j)
    else:
        ds_num = str(j)
    f_prev = 0
    c = 0
    for i in range(1, max_high):
        tree_creator.tree(ds_num, i)
        (f_micro, f_macro) = tree_predict.read_tree_and_predict(ds_num)
        result = ds_num + " " + str(i) + " " + str(f_micro) + " " + str(f_macro)
        print(result)

        if f_macro == f_prev and ++c == 2:
            break
        elif f_macro == f_prev:
            c += 1
        else:
            f_prev = f_macro
            c = 0

        f = open("result_train.txt", "a+")
        f.write(result)
        f.write('\n')
        f.close()
