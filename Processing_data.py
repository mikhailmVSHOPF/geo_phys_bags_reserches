import numpy as np
import matplotlib.pyplot as plt

import Normalize_data
import Appr_data
from scipy.stats import lognorm
from scipy.optimize import minimize


class Pro_data(object):
   def __init__(self, object_data):
      self.Data_loader_object = object_data
      self.mixed_arr, self.thicknesses_arr, self.times_arr,self.R_circle_arr, self.time_circle_arr, self.diametr_arr_txt, self.diametr_arr, self.fps = object_data.get_data()
      temp_dict = {}
      # plt.hist(self.thicknesses_arr, 200)
      for line in self.mixed_arr:
            time = line[1]; thikness = line[0];
            if(time not in temp_dict):
                temp_dict[time] = []; temp_dict[time].append(thikness)
            else:
                temp_dict[time].append(thikness)
      temp_sorted_times = list(temp_dict.keys()); temp_sorted_points = list(temp_dict.values())
      times, points = list(zip(*(sorted(zip(temp_sorted_times, temp_sorted_points)))))
      if(len(times) == 0 and len(points) == 0):
            self.sorted_times, self.sorted_thicknesses = None
      else:
            self.sorted_times, self.sorted_thicknesses = list(zip(*(sorted(zip(temp_sorted_times, temp_sorted_points)))))
      
      mask = [diametr is not None for diametr in self.diametr_arr]
      self.diametr_arr = np.array(self.diametr_arr)[mask]
      self.diametr_arr = [float(diametr) for diametr in self.diametr_arr]
      self.mean_for_all_points = float(np.mean(np.array(self.thicknesses_arr)))
      
      self.merge_close_values()
      mask = [len(thickness) > 2 for thickness in self.sorted_thicknesses]
      temp_sorted_points = []; temp_sorted_times = []
      for mask_bool, thickness, time in zip(mask, self.sorted_thicknesses, self.sorted_times):
          if(mask_bool == True):
              temp_sorted_points.append(thickness); temp_sorted_times.append(time)
      self.sorted_thicknesses = temp_sorted_points; self.sorted_times = temp_sorted_times
      
      
      self.processing_the_result()
   
   def to_return_data(self, name):
       self.Data_loader_object.to_return_data(name)
       
   
   def merge_close_values(self):
    dt = 1 / (self.fps)
    times = self.sorted_times
    thicknesses = self.sorted_thicknesses  # двумерный массив
    min_t, max_t = min(times), max(times)
    result_times = []
    result_thicknesses = []  # будет содержать одномерные массивы
    N = 1
    while min_t + (N-1) * dt < max_t:
        curr_times = []
        curr_thicknesses = []  # одномерный массив для объединенных толщин
        t_start = min_t + (N-1) * dt
        t_end = min_t + N * dt
        for i, time in enumerate(times):
            if t_start < time < t_end:
                curr_times.append(time)
                # Объединяем массивы в один одномерный
                curr_thicknesses.extend(thicknesses[i])  # extend вместо append!
        # Если в интервале есть точки
        if curr_times:
            # Среднее время
            avg_time = float(np.mean(curr_times))
            result_times.append(avg_time)
            # Добавляем объединенный одномерный массив
            result_thicknesses.append(curr_thicknesses)
        N += 1
    self.sorted_times = result_times
    self.sorted_thicknesses = result_thicknesses  # теперь это список одномерных массивов
   
   def to_calculate_confidance_interval(self, alpha, check_wait, mu, sigma):
       dist = lognorm(s=sigma, scale=np.exp(mu))
       def integr(d):
           area = dist.cdf(check_wait + d) - dist.cdf(check_wait - d)
           return (area - (1 - alpha))**2
       initial_d = check_wait * 0.0001
       result = minimize(integr, 
                     x0=[initial_d], 
                     method='L-BFGS-B',
                     bounds=[(1e-10, None)])
       return result.x
   
   def processing_the_result(self):
           alpha = 0.95
           # min_sorted_thickness = min(self.sorted_thicknesses); max_sorted_thickness = max(self.sorted_thicknesses)
           # sorted_thicknesses_arr_norm = list((self.sorted_thicknesses - min_sorted_thickness)/(max_sorted_thickness - min_sorted_thickness))
           np_thicknesses_arr = np.array(self.thicknesses_arr)
           min_thickness = min(np_thicknesses_arr); max_thickness = max(np_thicknesses_arr)
           thicknesses_arr_norm = list((np_thicknesses_arr - min_thickness)/(max_thickness - min_thickness))
           
           
           # y_funk_of_probability_list, x_funk_of_probability_list, check_wait_list, dispersion_list, sigma_list, nu_list = Appr_data.to_get_funk_of_prob_for_all(sorted_thicknesses_arr_norm)
           # check_wait_list = np.array(check_wait_list); dispersion_list = np.array(dispersion_list); sigma_list = np.array(sigma_list)
           
           # check_wait_list_correct = (max_thickness - min_thickness)*check_wait_list + min_thickness
           # standard_deviation_list = dispersion_list**2
         
           
           y_funk_of_probability_list_of_all_into_one_arr, x_funk_of_probability_list_of_all_into_one_arr, check_wait_all, dispersion_all, sigma_all, mu_all = Appr_data.to_get_funk_of_prob(thicknesses_arr_norm)
           
           check_wait_all_corr = (max_thickness - min_thickness)*check_wait_all + min_thickness
           standard_deviation_corr = (max_thickness - min_thickness)*(dispersion_all)**(1/2)
           
           self.y_funk_of_probability_list_of_all_into_one_arr = y_funk_of_probability_list_of_all_into_one_arr
           self.x_funk_of_probability_list_of_all_into_one_arr = x_funk_of_probability_list_of_all_into_one_arr
           
           self.confidance_interval = self.to_calculate_confidance_interval(alpha, check_wait_all, mu_all, sigma_all)
           
           self.check_wait_all = check_wait_all_corr #ПРИМЕНЯЕМ К МАТОЖИДАНИЮ обратное преобразование 
           self.sigma_all = sigma_all; self.mu_all = mu_all
           
           # self.y_func_prob = y_funk_of_probability_list; self.x_func_prob = x_funk_of_probability_list
           # self.check_wait = np.array(check_wait_list_correct)
           # self.sigma = np.array(sigma_list)
           # self.nu = np.array(nu_list)
       
        
   def to_plot(self, name = 'name'):
       plt.figure(figsize=(10,6))
       plt.scatter(self.sorted_times, self.check_wait)
       try:
          plt.title("plot of " + str(name) +f" thick(time) array of {len(self.thicknesses_arr)} points")
       except:
           plt.title("plot of " + str(name) + f" thick(time)")
       plt.grid()
       plt.show()
       
   def to_plot_for_all_points(self, name = 'name'):
       plt.figure(figsize=(10,6))
       plt.plot(self.x_funk_of_probability_list_of_all_into_one_arr, self.y_funk_of_probability_list_of_all_into_one_arr);
       plt.grid()
       
       plt.title(f"amount of points {len(self.thicknesses_arr)}")
       x = np.arange(0, max(self.x_funk_of_probability_list_of_all_into_one_arr), 0.01)
       y = np.array([lognorm.cdf(item, self.sigma_all, scale=(self.mu_all)) for item in x])
       print(f"The value of check_wait is {self.check_wait_all}\n")
       print(f"The value of mean for all is {self.mean_for_all_points}\n")
       plt.plot(x,y)
       plt.grid()
       plt.show()

   def to_plot_radius(self, name = "radius"):
       plt.figure(figsize=(10,6))
       np_R_time = np.array(self.R_time); np_R_cirlce = np.array(self.R_circle)
       liner_f = np.polyfit(np_R_time, np_R_cirlce, 1)
       coefficients = np.polyfit(np_R_time, np_R_cirlce, 1)
    
       max_t = max(self.R_time)
       min_t = min(self.R_time)
       time = np.linspace(min_t, max_t, 100)  # исправил на 100 точек
    # СПОСОБ 1: Создаем функцию из коэффициентов
       linear_function = np.poly1d(coefficients)
       R_circle_linear = linear_function(time)
       print(coefficients[0])
    # ИЛИ СПОСОБ 2: Вычисляем вручную y = k*x + b
    # R_circle_linear = coefficients[0] * time + coefficients[1]
       plt.plot(time, R_circle_linear)
       plt.scatter(self.R_time, self.R_circle)
       plt.title(name)
       plt.xlabel('Time')
       plt.ylabel('Radius')
       plt.grid()
       plt.show()

   def to_plot_cloud(self, name = 'name'):
       plt.figure(figsize=(10,6))
       plt.scatter(self.unsorted_times, self.unsorted_thicknesses)
       # plt.scatter(self.sorted_times, self.check_wait, label = "check wait", c = "orange")
       plt.scatter(self.sorted_times, [np.mean(np.array(points)) for points in self.sorted_thicknesses], label = "mean", marker= "x")
       plt.xlabel("time[seconds]"); plt.ylabel("thickness[metrs]")
       print(f"means:{[np.mean(np.array(points)) for points in self.sorted_thicknesses]}\n")
       print(f"check_waits:{[np.mean(np.array(points)) for points in self.check_wait]}\n")
       # plt.errorbar(self.sorted_times, self.check_wait, yerr=self.standard_deviation, fmt='o', capsize=10, ecolor= "orange")
       plt.title(name)
       plt.legend()
       plt.grid()
       plt.show()

   def to_plot_func_of_prob(self):
       for y_f, x_f, p, s, n in zip(self.y_func_prob, self.x_func_prob, self.sorted_thicknesses, self.sigma, self.nu):
           plt.figure(figsize=(10,6))
           plt.plot(x_f, y_f); plt.grid(); plt.title(f"amount of points {len(p)}")
           x = np.arange(0, max(x_f), 0.01)
           y = np.array([Appr_data.erf_func(item, s, n) for item in x])
           plt.plot(x,y)
           plt.grid()
           plt.show()
