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

#F41_15000_20_11_2025 = ds.DataSet("/home/mikhailm/Desktop/data_26_11_2025/F41_15000_20_11_2025")
#F41_10000_21_11_2025 = ds.DataSet("/home/mikhailm/Desktop/data_26_11_2025/F41_10000_21_11_2025")
#F41 = F41_15000_20_11_2025
#cdf(F41); pdf(F41); plt.title("general"); plt.savefig("general.png")
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

    pdf(item); plt.title(f"general pdf {general_name}, amount of {len(general_data.thicknesses_arr)}"); plt.savefig(f"general_pdf_{general_name}.png"); plt.close('all')
    cdf(item, name); plt.title(f"general cdf {general_name}, amount of {len(general_data.thicknesses_arr)}"); plt.savefig(f"general_cdf_{general_name}.png"); plt.close('all')


for name in list_general_name:
    f(name)