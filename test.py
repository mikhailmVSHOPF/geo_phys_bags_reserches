import numpy as np
import matplotlib.pyplot as plt
import Data_loader as ds

def pdf(data):
    num = 15
    temp_data = data.thicknesses_arr
    temp_data = np.array(temp_data)
    temp_data = np.log(temp_data)
    temp_data = sorted((temp_data - min(temp_data))/(max(temp_data) - min(temp_data)))
    temp_data = temp_data[1:]

    hist, bins = np.histogram(temp_data, bins = np.linspace(min(temp_data), max(temp_data), num))
    sum = np.sum(hist)
    hist = hist/sum
    plt.bar(x=bins[:-1],height=hist, width = np.diff(bins), alpha=0.5)

def cdf(data, name):
    num = 50
    temp_data = data.thicknesses_arr
    print(len(temp_data))
    temp_data = np.array(temp_data)
    temp_data = np.log(temp_data)
    temp_data = sorted((temp_data - min(temp_data))/(max(temp_data) - min(temp_data)))
    temp_data = temp_data[1:]

    hist, bins = np.histogram(temp_data, bins = np.linspace(min(temp_data), max(temp_data), num))
    sum = np.sum(hist)
    hist = hist/sum
    cumulitive = np.cumsum(hist)
    plt.plot(bins[:-1], cumulitive, label = name)

list_general_name = ["F25","F27","F29","F33","F37","F41","F45"]
def f(general_name):
    folder = ds.DataFolder("/home/mikhailm/Desktop/data_26_11_2025/" + general_name)
    file_paths, data = folder.folder_path_list, folder.folder_data
    general_data = data[0]
    for ind in range(1,len(data)):
        general_data += data[ind]
    
    for item, name in zip(data, file_paths):
        cdf(item, name); pdf(item)
    plt.title(f"{general_name}")
    plt.legend()
    plt.savefig("separeted_pdf_cdf" + general_name +".png")
    plt.close('all')





d_29_12_25_exp1 = ds.DataSet("/home/mikhailm/Desktop/data_29_12_25/exp1")
d_29_12_25_exp2 = ds.DataSet("/home/mikhailm/Desktop/data_29_12_25/exp2")

cdf(d_29_12_25_exp1,"exp1"); cdf(d_29_12_25_exp2, "exp2"); plt.savefig('my_plot.png')
