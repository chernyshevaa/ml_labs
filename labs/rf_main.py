import rf_tree_creator, rf_predict

ds_num = "05"

max_high = 50

arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
for j in arr:
    if j < 10:
        ds_num = "0" + str(j)
    else:
        ds_num = str(j)
    f_prev = 0
    c = 0

    for i in range(10):
        rf_tree_creator.tree(ds_num, i)
    (f_micro, f_macro) = rf_predict.read_tree_and_predict(ds_num)
    result = ds_num + " " + str(i) + " " + str(f_micro) + " " + str(f_macro)
    print(result)

    if f_macro == f_prev and ++c == 2:
        break
    elif f_macro == f_prev:
        c += 1
    else:
        f_prev = f_macro
        c = 0

    f = open("result_rf_n.txt", "a+")
    f.write(result)
    f.write('\n')
    f.close()
