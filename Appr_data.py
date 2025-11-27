import numpy as np
from scipy.optimize import curve_fit
from scipy.stats import lognorm
from scipy.optimize import minimize


def erf_func_fit(data_x, data_y):
    def erf_func(x, sigma, mu):
        return lognorm.cdf(x, sigma, scale=mu)
    params = curve_fit(erf_func, data_x, data_y)
    sigma_fit, mu_fit = params[0]; sigma, mu = float(sigma_fit), float(mu_fit)
    try:
        check_wait = np.exp(mu + (sigma ** 2) / 2); dispersion = (np.exp(sigma ** 2) - 1) * np.exp(2 * mu + sigma ** 2)
        return check_wait, dispersion, sigma, mu
    except Exception as e: print(e); return 0, 0, sigma, mu

def to_get_funk_of_prob_for_all(normalize_data_list):
    result = [to_get_funk_of_prob(sublist) for sublist in normalize_data_list]
    y_funk_of_probability_list = [item[0] for item in result]
    x_funk_of_probability_list = [item[1] for item in result]
    check_wait_list = [item[2] for item in result]
    dispersion_list = [item[3] for item in result]
    sigma_list = [item[4] for item in result]
    nu_list = [item[5] for item in result]
    return y_funk_of_probability_list, x_funk_of_probability_list, check_wait_list, dispersion_list, sigma_list, nu_list

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

def to_get_funk_of_prob(normalize_data): #IN ARGS HAVE TO BE NORMALIZE DATA
    bins = 2000
    n_data = normalize_data
    max_value = max(normalize_data)
    edges = np.linspace(0, max_value, num=bins)
    num_points_into_interval = np.histogram(n_data, bins=edges)[0]
    total_sum_of_points = np.sum(num_points_into_interval)
    probability_to_be_in_interval = num_points_into_interval / total_sum_of_points
    y_funk_of_probability = np.cumsum(probability_to_be_in_interval); x_funk_of_probability = edges[:-1]
    check_wait, dispersion, sigma, nu = erf_func_fit(x_funk_of_probability, y_funk_of_probability)
    return y_funk_of_probability, x_funk_of_probability, check_wait, dispersion, sigma, nu
