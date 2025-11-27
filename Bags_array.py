import re
import os 
import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt 
import math as mt

class Bags_array(object):
    #читает по отдельности каждый файл из папки, полученные данные сохраняет в массивы -> на выходе получаем массив бэгов
    #причем получаем в результате 3х мерный массив структура которого (массив бэгов(точка разрыва, линии))
    def points_of_gap(self, path):
        regex_r =  re.compile(r'.+r(\d+)\t(\d+)\t(\d+,\d+)\t(\d+,\d+)')
        self.rad_dict = {}
        with open(self.folder_path + "/" + path) as file:
            for line in file:
                if re.search(regex_r, line):
                    data = re.findall(regex_r, line)[0]
                    name = str(data[0])
                    t = float(data[1])*(1/self.fps) - self.t_p
                    x = float(data[2].replace(',', '.'))*self.dx - self.x_p
                    y = float(data[3].replace(',', '.'))*self.dx - self.y_p
                    if (t not in self.rad_dict): 
                        self.rad_dict[t] = []
                        self.rad_dict[t].append((y, x))
                    else:
                        self.rad_dict[t].append((y, x))

    
    def point_finder(self, path):
                  regex_point = re.compile(r'^(point)\t+(\d+)*\t+(\d+,*\d*)\t+(\d+,*\d*)\t+(\d+,*\d*)')
                  with open(self.folder_path + "/" + path) as file:
                      for line in file:
                          if re.search(regex_point, line):
                              data = re.findall(regex_point, line)[0]
                              self.x_p = float(data[3].replace(',', '.'))*self.dx
                              self.y_p = float(data[4].replace(',', '.'))*self.dx
                              self.t_p = float(data[2])*(1/self.fps)
                              break;
                  return  self.x_p, self.y_p, self.t_p
      
    def rim_velocity(self, path):
                  self.rim_dict = {}
                  regex_rim =  re.compile(r'^.+\t(rim(\d+))\t(?:(\d+,\d+|\d+)|None)\t(?:(\d+,\d+|\d+)|None)\t(?:(\d+,\d+|\d+)|None)\t(?:(\d+,\d+|\d+)|None)\t(?:(\d+,\d+|\d+)|None)\t(?:(\d+,\d+|\d+)|None)')
                  with open(self.folder_path + "/" + path) as file:
                      for line in file:
                          if re.search(regex_rim, line):
                              data = re.findall(regex_rim, line)[0]
                              t_s = float(data[2])*(1/self.fps) - self.t_p
                              t_e = float(data[3])*(1/self.fps) - self.t_p
                              x_s = float(data[4].replace(',', '.'))*self.dx - self.x_p#перевели в м
                              y_s = float(data[5].replace(',', '.'))*self.dx - self.y_p
                              x_e = float(data[6].replace(',', '.'))*self.dx - self.x_p
                              y_e = float(data[7].replace(',', '.'))*self.dx - self.y_p
                              dy = y_e - y_s; dx = x_e - x_s; dt = t_e - t_s; t_m = (t_e + t_s)/2
                              v_x = dx/dt; v_y = dy/dt
                              if (t_m not in self.rim_dict): 
                                  self.rim_dict[t_m] = []
                                  self.rim_dict[t_m].append((v_y, v_x))
                              else:
                                  self.rim_dict[t_m].append((v_y, v_x))
                  return self.rim_dict
                                  
    def line_velocity(self, path):
                  self.l_vel_dict = {}
                  regex_line = re.compile(r'^.+\t(\d+)\t(?:(\d+,\d+|\d+)|None)\t(?:(\d+,\d+|\d+)|None)\t(?:(\d+,\d+|\d+)|None)\t(?:(\d+,\d+|\d+)|None)\t(?:(\d+,\d+|\d+)|None)\t(?:(\d+,\d+|\d+)|None)')
                  with open(self.folder_path + "/" + path) as file:
                    for line in file:
                          if re.search(regex_line, line):
                              data = re.findall(regex_line, line)[0]
                              name = str(data[0])
                              t_s = float(data[1])*(1/self.fps) - self.t_p
                              t_e = float(data[2])*(1/self.fps) - self.t_p
                              x_s = (float(data[3].replace(',', '.')))*self.dx - self.x_p #перевели в систему отчета, связанную с подвижной точкой разрыва
                              y_s = (float(data[4].replace(',', '.')))*self.dx - self.y_p
                              x_e = (float(data[5].replace(',', '.')))*self.dx - self.x_p
                              y_e = (float(data[6].replace(',', '.')))*self.dx - self.y_p
                              dy = y_e - y_s; dx = x_e - x_s; dt = t_e - t_s;  t_m = (t_e + t_s)/2
                              v_x = dx/dt; v_y = dy/dt
                              if (t_m not in self.l_vel_dict): 
                                  self.l_vel_dict[t_m] = []
                                  self.l_vel_dict[t_m].append((v_y, v_x))
                              else:
                                  self.l_vel_dict[t_m].append((v_y, v_x))
                  return self.l_vel_dict
                                      
    def to_count_velocity(self):
                      rim_dict = self.rim_dict
                      l_dict = self.l_vel_dict
                      for key_vel in rim_dict.keys():
                           temp_vel_x = []; temp_vel_y = []
                           for vel in rim_dict[key_vel]:
                               temp_vel_x.append(vel[1])
                               temp_vel_y.append(vel[0])
                           np_temp_vel_x = float(np.sum(np.array(temp_vel_x)))/len(temp_vel_x)
                           np_temp_vel_y = float(np.sum(np.array(temp_vel_y)))/len(temp_vel_y)
                           rim_dict[key_vel] = (np_temp_vel_y, np_temp_vel_x)
                      t_l = np.array(list(l_dict.keys())); t_r = np.array(list(rim_dict.keys()))
                      v_l = list(l_dict.values()); v_r = list(rim_dict.values())
                      v_r_x = np.array([vel[1] for vel in v_r ]); v_r_y = np.array([vel[0] for vel in v_r ])
                      v_l_x = np.array([vel[0][1] for vel in v_l ]); v_l_y = np.array([vel[0][0] for vel in v_l ])
                      vel_interp_x = [float(np.interp(time, t_r, v_r_x)) for time in t_l]
                      vel_interp_y = [float(np.interp(time, t_r, v_r_y)) for time in t_l]
                      temp = zip(vel_interp_y, vel_interp_x, v_l_y, v_l_x, t_l)
                      result = [(float(self.calculate_thikness(((v_i_x - v_l_x)**2 + (v_i_y - v_l_y)**2)**(1/2))), float(time)) for v_i_y,v_i_x,v_l_y,v_l_x,time in temp] #ИЗМЕНЕНО НЕМНОГО
                      
                      return result
        
    def calculate_thikness(self, velocity):
        return 2*self.sigma/((velocity**2)*self.rho)
    
    def find_paths_to_files(self):
        regex_config_file = re.compile(r'config_file')
        regex_file = re.compile(r'.*F\d+.*\.dat')
        files_path = os.listdir(str(self.folder_path))
        files_path_np = np.array(files_path)
        files_config_mask = np.array([ bool(re.match(regex_config_file, path)) for path in files_path])
        self.сonfig_file_path = str(list(files_path_np[files_config_mask])[0])
        files_path_mask = np.array([ bool(re.match(regex_file, path)) for path in files_path])
        self.files_path = list(files_path_np[files_path_mask])
    
    def read_config_file(self):
        try:
            with open(self.folder_path + '/' + self.сonfig_file_path) as file:
                regex_config_file_info = re.compile(r'^(\w+)=(\d+.*\d*|\w+)')
                data = [re.findall(regex_config_file_info, line) for line in file]
                self.dx = float(data[0][0][1])/100#м/кол-во пикселей
                self.fps = float(data[1][0][1])#кадров/секунду
                self.type = str(data[2][0][1])
                self.rho = float(data[4][0][1])
                self.sigma = float(data[3][0][1]) 
        except Exception as e:
            print(e)
            
        
    
    def __init__(self, folder_path):
        self.result = []
        self.x_p = None; self.y_p = None
        self.folder_path = folder_path
            
class Bags_array_with_radius(Bags_array):
    def __init__(self, folder_path):
       super().__init__(folder_path)
       self.R_circle_result = []; self.time_result = []; self.diametr_result = []; self.diametr_result_for_processing = []
       self.find_paths_to_files()
       self.read_config_file()
       for file in self.files_path:
           self.point_finder(file)
           self.points_of_gap(file)
           self.line_velocity(file)
           self.point_of_diametr(file)
           self.center_coordinates()
           res = self.to_count_velocity_with_radius()
           for line in res:
               self.result.append(line)
               self.diametr_result.append(self.diametr)
           self.diametr_result_for_processing.append(self.diametr)
            
               
           for R, t in zip(self.R_circle, self.time):
               self.R_circle_result.append(R)
               self.time_result.append(t)
        
               
    
    def point_of_diametr(self, path):
        regex_d =  re.compile(r'point\td\t(\d+)\t(-*\d+,*\d+)\t(-*\d+,*\d+)')
        diametr_x =  []; diametr_y = []; frame = []
        with open(self.folder_path + "/" + path) as file:
            for line in file:
                if re.search(regex_d, line):
                    data = re.findall(regex_d, line)[0]
                    t = float(data[0])*(1/self.fps)
                    x = float(data[1].replace(',', '.'))*self.dx
                    y = float(data[2].replace(',', '.'))*self.dx
                    diametr_x.append(x); diametr_y.append(y); frame.append(t)
            unique, counts = np.unique(np.array(frame), return_counts=True)
            duplicate_values = unique[counts > 1]
            mask = np.isin(frame, duplicate_values)
            diametr_x = np.array(diametr_x)[mask]; diametr_y = np.array(diametr_y)[mask]
        try:
            self.diametr = ((diametr_x[0] - diametr_x[1])**2 + (diametr_y[0] - diametr_y[1])**2)**(1/2)
        except:
            self.diametr = None
               
    def center_coordinates(self):
        bags = self.rad_dict
        b_keys = bags.keys()
        self.x_center = []; self.y_center = []; self.R_circle =[]; self.time = []; self.R_circle_error = []
        for key in list(b_keys): 
            x_arr = []; y_arr = []; self.time.append(key)
            for line in bags[key]:
                x, y = line
                x_arr.append(x); y_arr.append(y)
            x_arr_np = np.array(x_arr); y_arr_np = np.array(y_arr)
            res_general = self.appr_circle(x_arr_np, y_arr_np)
            res = res_general.x
            dR_error = res_general.fun
            self.x_center.append(res[0]); self.y_center.append(res[1]); self.R_circle.append(res[2])
            self.R_circle_error.append(dR_error)
        len_time_arr = len(self.time)
        
        dt = [(self.time[index + 1] - self.time[index]) for index in range(0,len_time_arr - 1)]
        t = [(self.time[index + 1] + self.time[index])/2 for index in range(0,len_time_arr - 1)]
        dx = [(self.x_center[index + 1] - self.x_center[index]) for index in range(0,len_time_arr - 1)]
        dy = [(self.y_center[index + 1] - self.y_center[index]) for index in range(0,len_time_arr - 1)]
        dR = [( self.R_circle[index + 1] -  self.R_circle[index]) for index in range(0,len_time_arr - 1)]
        self.center_velocity = [((dy[index])/(dt[index]) , (dx[index])/(dt[index])) for index in range(0,len_time_arr - 1)]
        self.modul_center_velocity = [(vel_x**2 + vel_y**2)**(1/2) for (vel_x, vel_y) in self.center_velocity]
        self.radius_velocity = [(dR[index])/(dt[index])for index in range(0,len_time_arr - 1)]
        self.center_time = t
        
    def circle_residuals(self,params, x, y):
          x0, y0, R = params
          distances = np.sqrt((x - x0)**2 + (y - y0)**2)
          return np.sum(abs((distances - R)))

    def appr_circle(self, x_data, y_data): 
          x0_guess = np.mean(x_data)
          y0_guess = np.mean(y_data)
          R_guess = np.mean(np.sqrt((x_data - x0_guess)**2 + (y_data - y0_guess)**2))
          initial_guess = [x0_guess, y0_guess, R_guess]
          result = minimize(self.circle_residuals, initial_guess, args=(x_data, y_data))
          return result
    
    def to_count_velocity_with_radius(self):
                      center_vel = self.center_velocity
                      
                      l_dict = self.l_vel_dict
                      center_v_x  = [vel[1] for vel in center_vel]
                      center_v_y  = [vel[0] for vel in center_vel]
                      t_r = self.center_time
                      
                      t_l = np.array(list(l_dict.keys()))
                      v_l = list(l_dict.values())
                      
                      vel_interp_x = [float(np.interp(time, t_r, center_v_x)) for time in t_l]
                      vel_interp_y = [float(np.interp(time, t_r, center_v_y)) for time in t_l]
                      v_l_x = [[item[1] for item in vel] for vel in v_l ]; v_l_y = [[item[0] for item in vel] for vel in v_l ]

                      for ind_1 in range(0,len(t_l)):
                          v_l_x_temp = v_l_x[ind_1]; v_l_y_temp = v_l_y[ind_1]
                          vel_interp_x_temp = vel_interp_x[ind_1]; vel_interp_y_temp = vel_interp_y[ind_1]
                          for ind in range(0, len(v_l_x_temp)):
                              v_l_x[ind_1][ind] = v_l_x_temp[ind] - vel_interp_x_temp; 
                              v_l_y[ind_1][ind] = v_l_y_temp[ind] - vel_interp_y_temp
                              
                      result = []
                      for ind in range(0, len(t_l)):
                          time = t_l[ind]; v_l_x_list = v_l_x[ind];  v_l_y_list = v_l_y[ind]
                          for ind_vel in range(0, len(v_l_x_list)):
                              result.append((float(self.calculate_thikness(((v_l_x_list[ind_vel])**2 + (v_l_y_list[ind_vel])**2)**(1/2))), float(time)))
                      return result
     
               
               
    
               
           
           
        

    