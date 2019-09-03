import numpy as np
import matplotlib.pyplot as plt

path = "/Users/lfish/Downloads/1904055ca752dbcbdfe/"
file_name = "ttl.txt"

def collect_process_data():
    """
    读取文件所有数字的拼接而成的字符串 以及 int型数组
    :return:
    """
    file = path + file_name
    data_str = ""
    data_num = []
    with open(file, "r") as f:
        for str in f.readlines():
            data_str += str[4:-1]
            data_num.append(int(str[ 4: -1]))
    return data_str, data_num

def draw_analyse(data_num):
    ar = np.array(data_num)
    plt.figure(figsize=(15,5))
    plt.plot(ar[150:300])
    plt.show()

def binary_analyse(data_num):
    bi_str = ""
    bi = "00"
    for n in data_num:
        if n == 63:
            bi = "00"
        elif n == 127:
            bi = "01"
        elif n == 191:
            bi = "10"
        elif n == 255:
            bi = "1"
        bi_str += bi
    with open(path+"bin_analyse.txt", "w+") as f:
        f.write(bi_str)
    return bi_str




if __name__ == "__main__":
    data_str, data_num = collect_process_data()
    draw_analyse(data_num)
    bi_str = binary_analyse(data_num)

