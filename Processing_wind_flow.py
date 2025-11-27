import matplotlib.pyplot as plt
import numpy as np
import re

patternBlock = re.compile(r'\[DATA BLOCK (\d+)-(\d+)-(\d+)\]')
patternData = re.compile(r'\-?\d*\.?\d+')
patternPosition = re.compile(r'Position no\.\:\s+(\d+)')

test = '[DATA BLOCK 9-1-1]'
test1 = 'Position no.:     13'
test3 = "59.9890028 10.4804106 -0.9074075"


def reader(file_path):
    with open(file_path) as file:
        status_position = False
        status_block = False
        position_arr = []
        column_time = []
        column_speed = []
        column_arr = []
        for line in file:
            if re.search(patternPosition, line) and not status_position:
                status_position = True
                status_block = False
                position = re.findall(patternPosition, line)[0]
                position_arr.append(int(position))
                temp_time_arr = []
                temp_speed_arr = []
                temp_arr = []
                column_time.append(temp_time_arr)
                column_speed.append(temp_speed_arr)
                column_arr.append(temp_arr)

            elif re.search(patternBlock,line) and status_position:
                status_block = True


            elif re.search(patternData,line) and (status_position and status_block):
                data_1, data_2, data_3 = re.findall(patternData, line)
                temp_time_arr.append(float(data_1))
                temp_speed_arr.append(float(data_2))
                temp_arr.append(float(data_3))

            elif not re.search(patternData,line) and (status_position and status_block):
                status_position = False
    mean_speed = [float(np.mean(speed)) for speed in column_speed]
    return position_arr, column_time, mean_speed, column_arr

def reader_with_plot(file_path, name_file_to_save):
    with open(file_path) as file:
        status_position = False
        status_block = False
        position_arr = []
        column_time = []
        column_speed = []
        column_arr = []
        for line in file:
            if re.search(patternPosition, line) and not status_position:
                status_position = True
                status_block = False
                position = re.findall(patternPosition, line)[0]
                position_arr.append(int(position))
                temp_time_arr = []
                temp_speed_arr = []
                temp_arr = []
                column_time.append(temp_time_arr)
                column_speed.append(temp_speed_arr)
                column_arr.append(temp_arr)

            elif re.search(patternBlock,line) and status_position:
                status_block = True


            elif re.search(patternData,line) and (status_position and status_block):
                data_1, data_2, data_3 = re.findall(patternData, line)
                temp_time_arr.append(float(data_1))
                temp_speed_arr.append(float(data_2))
                temp_arr.append(float(data_3))

            elif not re.search(patternData,line) and (status_position and status_block):
                status_position = False

    mean_speed = [float(np.mean(speed)) for speed in column_speed]
    std_speed = [float(np.std(speed)) for speed in column_speed]
    plt.figure(figsize=(30, 20))
    plt.errorbar(mean_speed, position_arr, xerr=std_speed, fmt='o', ecolor='r', capsize=5, label='Данные с ошибками')
    plt.plot(mean_speed, position_arr)
    plt.title(name_file_to_save, fontsize=30)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.xlabel('Speed', fontsize=20)
    plt.ylabel('Position', fontsize=20)
    plt.savefig(name_file_to_save + ".pdf", format='pdf', dpi=300)
    plt.grid()
    plt.show()

    return position_arr, column_time, mean_speed, column_arr


def to_plot_result(position, speed, name):
    mean_speed = [float(np.mean(item_s)) for item_s in speed]
    std_speed = [float(np.std(item_s)) for item_s in speed]
    plt.figure(figsize=(30, 20))
    plt.errorbar(mean_speed, position, xerr=std_speed, fmt='o', ecolor='r', capsize=5, label='Данные с ошибками')
    plt.plot(mean_speed, position)
    plt.title(name, fontsize=30)
    plt.xticks(fontsize = 20)
    plt.yticks(fontsize = 20)
    plt.xlabel('Speed', fontsize = 20)
    plt.ylabel('Position', fontsize = 20)
    plt.grid()
    plt.show()

def to_plot_results(position_arr, speed_arr, name_of_graph):
    speed_2d_arr = [[float(np.mean(item_s)) for item_s in speed] for speed in speed_arr]
    plt.figure(figsize=(40, 30))
    for pos_item, item in zip(position_arr,speed_2d_arr):
        plt.plot(item,pos_item)
        plt.scatter(item,pos_item)
    plt.title(name_of_graph, fontsize=30)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.xlabel('Speed', fontsize=20)
    plt.ylabel('Position', fontsize=20)
    plt.grid()
    plt.show()

# C:/Users/mikhailm/Desktop/test/current_wind_flow/F25.txt
def to_get_velocity(file_path):
    position_arr, _ , mean_speed, _ = reader(file_path)#Сразу строит график
    mask = [item >= 15 for item in list(position_arr)]
    mean_speed = np.array(mean_speed)[mask]
    speed = np.mean(mean_speed)
    return speed


