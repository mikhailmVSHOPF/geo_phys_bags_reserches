import Processing_data
import Data_loader
import matplotlib.pyplot as plt 
import Processing_wind_flow
import numpy as np


velocity_F25 = Processing_wind_flow.to_get_velocity("C:/Users/mikhailm/Desktop/Научная работа/test/current_wind_flow/F25.txt")
velocity_F29 = Processing_wind_flow.to_get_velocity("C:/Users/mikhailm/Desktop/Научная работа/test/current_wind_flow/F29.txt")
velocity_F33 = Processing_wind_flow.to_get_velocity("C:/Users/mikhailm/Desktop/Научная работа/test/current_wind_flow/F33.txt")
velocity_F37 = Processing_wind_flow.to_get_velocity("C:/Users/mikhailm/Desktop/Научная работа/test/current_wind_flow/F37.txt")
velocity_F41 = Processing_wind_flow.to_get_velocity("C:/Users/mikhailm/Desktop/Научная работа/test/current_wind_flow/F41.txt")
velocity_F45 = Processing_wind_flow.to_get_velocity("C:/Users/mikhailm/Desktop/Научная работа/test/current_wind_flow/F45.txt")
velocity_F49 = Processing_wind_flow.to_get_velocity("C:/Users/mikhailm/Desktop/Научная работа/test/current_wind_flow/F49.txt")

velocity_list = [velocity_F25, velocity_F29, velocity_F33, velocity_F37, velocity_F41, velocity_F45, velocity_F49]
F_list_real = np.array([25, 29, 33, 37, 41, 45, 49])
F_list = np.array([25, 27, 29, 33, 37, 41, 45, 49])
velocity_list = np.array(velocity_list)
velocity_list_interp = np.interp(F_list, F_list_real, velocity_list)

# d_25_10000 = Data_loader.DataSet("C:/Users/mikhailm/Desktop/Научная работа/test/processed_F25_10000")
# d_25_8000 = Data_loader.DataSet("C:/Users/mikhailm/Desktop/Научная работа/test/processed_F25_8000")
# d_25_5000 = Data_loader.DataSet("C:/Users/mikhailm/Desktop/Научная работа/test/processed_F25_5000")
# d_25_gen = d_25_10000 + d_25_8000 + d_25_5000
# data_25 = Processing_data.Pro_data(d_25_gen)
# print(data_25.sorted_thicknesses)


# data_25.to_return_data("F25_data.txt")
# diam_25 = np.array(data_25.diametr_result_for_processing); diam_25 = np.mean(diam_25)
# data_25.to_plot_for_all_points("F25")
# data_25.to_plot_cloud()
# data_25.to_plot_func_of_prob()
# data_25.to_plot_radius()
# print(data_25.check_wait)
# print(len(d_25_gen.unsorted_points))

# d_27_8000 = Data_loader.DataSet("C:/Users/mikhailm/Desktop/test/processed_F27_8000")
# d_27_12000 = Data_loader.DataSet("C:/Users/mikhailm/Desktop/test/processed_F27_12000")
# d_27_6000 = Data_loader.DataSet("C:/Users/mikhailm/Desktop/test/processed_F27_6000")
# data_27 = Processing_data.Pro_data(d_27_8000 + d_27_12000)
# data_27.to_return_data("F27_data.txt")
# diam_27 = np.array(data_27.diametr_result_for_processing); diam_27 = np.mean(diam_27)
# data_27.to_plot_for_all_points("F27")
# data_27.to_plot_func_of_prob()
# data_27.to_plot_cloud()
# # data_27.to_calculate_confidance_interval(0.95)

# d_F29_6000 = Data_loader.DataSet("C:/Users/mikhailm/Desktop/Научная работа/test/processed_F29_6000")
# d_F29_6000_1 = Data_loader.DataSet("C:/Users/mikhailm/Desktop/Научная работа/test/processed_F29_6000_1")
# d_F29_8000 = Data_loader.DataSet("C:/Users/mikhailm/Desktop/Научная работа/test/processed_F29_8000")
# d_F29_12000 = Data_loader.DataSet("C:/Users/mikhailm/Desktop/Научная работа/test/processed_F29_12000")
# d_F29_20000 = Data_loader.DataSet("C:/Users/mikhailm/Desktop/Научная работа/test/processed_F29_20000")
# data_29 = Processing_data.Pro_data(d_F29_6000 + d_F29_6000_1 + d_F29_8000 + d_F29_12000 + d_F29_20000)
# print(data_29.thicknesses_arr, data_29.times_arr)
# data_29.to_return_data("F29_data.txt")
# diam_29 = np.array(data_29.diametr_result_for_processing); diam_29 = np.mean(diam_29)
# data_29.to_plot_for_all_points("F29")
# data_29.to_plot_cloud()
# data_29.to_plot_func_of_prob()
# print(data_29.unsorted_thicknesses)
# # print(data_29.check_wait)


# d_F33_12000 = Data_loader.DataSet("C:/Users/mikhailm/Desktop/Научная работа/test/processed_F33_12000")
# d_F33_6000 = Data_loader.DataSet("C:/Users/mikhailm/Desktop/Научная работа/test/processed_F33_6000")
# d_F33_20000 = Data_loader.DataSet("C:/Users/mikhailm/Desktop/Научная работа/test/processed_F33_20000")
# d_33_gen = d_F33_12000 + d_F33_6000 + d_F33_20000
# data_33 = Processing_data.Pro_data(d_33_gen)
# print(data_33.thicknesses_arr, data_33.times_arr)
# data_33.to_return_data("F33_data.txt")
# diam_33 = np.array(data_33.diametr_result_for_processing); diam_33 = np.mean(diam_33)
# data_33.to_plot_for_all_points()
# data_33.to_plot_cloud("F33")
# data_33.to_plot_func_of_prob()
# data_33.to_plot_radius()
# print(data_33.check_wait)

# d_F37_20000 = Data_loader.DataSet("C:/Users/mikhailm/Desktop/Научная работа/test/processed_F37_20000")
# data_37 = Processing_data.Pro_data(d_F37_20000)
# print(data_37.thicknesses_arr, data_37.times_arr)
# data_37.to_return_data("F37_data.txt")
# diam_37 = np.array(data_37.diametr_arr); diam_37 = np.mean(diam_37)
# data_37.to_plot_for_all_points("F37")
# data_37.to_plot_cloud()
# print(len(d_F37_20000.unsorted_points))


# d_F41_20000 = Data_loader.DataSet("C:/Users/mikhailm//Desktop/Научная работа/test/processed_F41_20000")
# data_41 = Processing_data.Pro_data(d_F41_20000)
# print(data_41.thicknesses_arr, data_41.times_arr)
# data_41.to_return_data("F41_data.txt")
# diam_41 = np.array(data_41.diametr_result_for_processing); diam_41 = np.mean(diam_41)
# data_41.to_plot_for_all_points("F41")
# data_41.to_plot_cloud()
# data_41.to_plot_func_of_prob()
# data_41.to_plot_radius()
# print(data_41.check_wait)

# d_F45_25000 = Data_loader.DataSet("C:/Users/mikhailm/Desktop/Научная работа/test/processed_F45_25000")
# d_F45_30000 = Data_loader.DataSet("C:/Users/mikhailm/Desktop/Научная работа/test/processed_F45_30000")
# d_F45_20000 = Data_loader.DataSet("C:/Users/mikhailm/Desktop/Научная работа/test/processed_F45_20000")
# data_45 = Processing_data.Pro_data(d_F45_25000 + d_F45_30000 + d_F45_20000)
# print(data_45.thicknesses_arr, data_45.times_arr)
# data_45.to_return_data("F45_data.txt")
# diam_45 = np.array(data_45.diametr_result_for_processing); diam_45 = np.mean(diam_45)
# data_45.to_plot_cloud()
# data_45.to_plot_for_all_points("F45")
# print(data_45.confidance_interval)
# data_45.to_plot_func_of_prob()
# data_45.to_plot_radius()

# d_F49_20000 = Data_loader.DataSet("C:/Users/mikhailm/Desktop/Научная работа/test/processed_F49_20000")
# d_F49_25000 = Data_loader.DataSet("C:/Users/mikhailm/Desktop/Научная работа/test/processed_F49_25000")
# d_F49_30000 = Data_loader.DataSet("C:/Users/mikhailm/Desktop/Научная работа/test/processed_F49_30000")
# data_49 = Processing_data.Pro_data(d_F49_20000 + d_F49_30000 + d_F49_25000)
# print(data_49.thicknesses_arr, data_49.times_arr)
# data_49.to_return_data("F49_data.txt")
# diam_49 = np.array(data_49.diametr_result_for_processing); diam_49 = np.mean(diam_49)
# data_49.to_plot_cloud()
# data_49.to_plot_func_of_prob()
# data_49.to_plot_for_all_points("F49")

# d_list = [data_25.check_wait_all, data_27.check_wait_all, data_29.check_wait_all, data_33.check_wait_all, data_37.check_wait_all, data_41.check_wait_all, data_45.check_wait_all, data_49.check_wait_all]
# conf_inter = [data_25.confidance_interval, data_27.confidance_interval, data_29.confidance_interval, data_33.confidance_interval, data_37.confidance_interval, data_41.confidance_interval, data_45.confidance_interval, data_49.confidance_interval]

# mean_list = [data_25.mean_for_all_points, data_27.mean_for_all_points, data_29.mean_for_all_points, data_33.mean_for_all_points, data_37.mean_for_all_points, data_41.mean_for_all_points, data_45.mean_for_all_points, data_49.mean_for_all_points]
# diam = [diam_25, diam_27, diam_29, diam_33, diam_37, diam_41, diam_45, diam_49]
# print(d_list); print(conf_inter); print(velocity_list_interp); print(mean_list); print(diam)
print(velocity_list_interp)
# plt.figure(figsize=(10,6))
# plt.xlabel("velocity")
# plt.ylabel("Thickness")
# plt.title("Thickness(velocity)")
# plt.scatter(velocity_list_interp, d_list)
# plt.errorbar(velocity_list_interp, d_list, yerr = conf_inter, marker='s', capsize=10)
# plt.grid()
# plt.show()

# plt.figure(figsize=(10,6))
# plt.xlabel("velocity")
# plt.ylabel("Thickness")
# plt.title("Thickness(velocity)")
# plt.scatter(velocity_list_interp, mean_list)
# plt.errorbar(velocity_list_interp, mean_list, yerr = conf_inter, marker='s', capsize=10)
# plt.grid()
# plt.show()


# plt.figure(figsize=(10,6))
# plt.xlabel("velocity")
# plt.ylabel("Thickness")
# plt.title("Thickness(velocity)")
# plt.scatter(diam, mean_list)
# plt.grid()
# plt.show()

# mean = [6.979745885007965e-06, 1.2625436709776708e-05, 5.815067756319698e-06, 7.526124282367984e-06, 5.619672309703243e-06, 2.881100346811374e-07, 3.474862846249739e-06, 3.21399143133843e-06]
# conf_interval = [1.450413437782915e-06, 2.5317750861898418e-06, 8.293378949264633e-07, 2.1068152599476887e-06, 1.0795186937377741e-06, 2.8732639039234566e-07, 6.189688594570536e-07, 6.427830959128281e-07]
# velocity = [11.51295153, 12.38721642, 13.26148131, 14.96311587, 16.55681941, 18.0851029, 19.34060755, 20.6757457 ]
# thickness = [6.621512697842937e-06, 1.2722373407905671e-05, 5.738602901358587e-06, 1.1510956457086105e-05, 4.921112053426023e-06, 6.27355827744813e-06, 3.3899750844964824e-06, 3.479955530896237e-06]
# diam = [0.023227466003474646, 0.018901946092835804, 0.015220783742347624, 0.012471341311042057, 0.011444340168493354, 0.013440973718103688, 0.011887191719166381, 0.012348072447455661]









