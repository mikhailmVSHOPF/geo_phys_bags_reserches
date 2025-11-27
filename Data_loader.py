import Bags_array
import os 

class DataSet(object):
    def __init__(self, data_file_path = None, mixed_arr = None, thicknesses_arr = None, times_arr = None, R_circle_arr = None, time_circle_arr = None, diametr_arr_txt = None, diametr_arr = None, fps = None):
        self.data_file_path = data_file_path; self.times_arr = times_arr; self.thicknesses_arr = thicknesses_arr
        self.R_circle_arr = R_circle_arr; self.time_circle_arr = time_circle_arr; self.diametr_arr_txt = diametr_arr_txt
        self.diametr_arr = diametr_arr; self.fps = fps; self.mixed_arr = mixed_arr
        if data_file_path is not None:
            self._load_file(data_file_path, thicknesses_arr, times_arr)

    def __add__(self, other):
        mixed_arr = self.mixed_arr + other.mixed_arr
        thicknesses_arr = self.thicknesses_arr + other.thicknesses_arr; times_arr = self.times_arr + other.times_arr;
        R_circle_arr = self.R_circle_arr + other.R_circle_arr; time_circle_arr = self.time_circle_arr + other.time_circle_arr;
        diametr_arr = self.diametr_arr + other.diametr_arr; diametr_arr_txt = self.diametr_arr_txt + other.diametr_arr_txt; 
        fps = min([self.fps, other.fps])
        return DataSet([self.data_file_path, other.data_file_path], mixed_arr, thicknesses_arr, times_arr, R_circle_arr, time_circle_arr, diametr_arr_txt, diametr_arr, fps)

    def return_paths(self):
        return self.data_file_path

    def get_data(self):
        return  self.mixed_arr, self.thicknesses_arr, self.times_arr,self.R_circle_arr, self.time_circle_arr, self.diametr_arr_txt, self.diametr_arr, self.fps
    
    def _load_file(self, file_path, thicknesses_arr, times_arr):
        if thicknesses_arr is None and  times_arr is None:
            bag = (Bags_array.Bags_array_with_radius(file_path))
            type_of_processing = bag.type
            self.mixed_arr = bag.result
            self.fps = bag.fps
            self.diametr_arr_txt = bag.diametr_result #массив диаметров бэга одного размера с unsorted_thicknesses. Если у одного из бэгов нельзя определить diametr -> None
            self.R_circle_arr = bag.R_circle_result
            self.time_circle_arr = bag.time_result
            self.diametr_arr = bag.diametr_result_for_processing#массив для построения распределений
            self.thicknesses_arr =  [thickness[0] for thickness in self.mixed_arr]
            self.times_arr =  [time[1] for time in self.mixed_arr]
            #Здесь вместо file_path должна стоять ссылка на папку
            
    def to_return_data(self, name_of_file):
        with open(name_of_file, "w") as file:
            for unsorted_points, unsorted_times, diametr  in zip(self.thicknesses_arr, self.times_arr,  self.diametr_arr_txt):
                file.write(str(unsorted_points) + "\t" + str(unsorted_times) + "\t" + str(diametr) + "\n")

class DataFolder(object):
    def __init__(self, folder_path):
        self.folder_path_list = os.listdir(str(folder_path))
        self.folder_data = [DataSet(folder_path + "/" + path) for path in self.folder_path_list]

