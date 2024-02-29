# def find_current_WBKT_weight_increment_factor(current_WBKT_parameter_weight):
#     if (current_WBKT_parameter_weight > 1.0):
#         return int(round((current_WBKT_parameter_weight - 1.0) / 0.2, 2))
#     elif (current_WBKT_parameter_weight < 1.0):
#         return int(round((1.0 - current_WBKT_parameter_weight) * -10.0, 2))
#     else:
#         return 0

# for i in range(5, 21, 1):
#     print(i/10.0, ' => ', find_current_WBKT_weight_increment_factor(i/10.0))

# def find_WBKT_weight_from_increment_factor(WBKT_weight_increment_factor):
#     if (WBKT_weight_increment_factor > 5):
#         WBKT_weight_increment_factor = 5
#     elif (WBKT_weight_increment_factor < -5):
#         WBKT_weight_increment_factor = -5

#     if (WBKT_weight_increment_factor > 0):
#         return (WBKT_weight_increment_factor * 0.2) + 1.0
#     elif (WBKT_weight_increment_factor < 0):
#         return -((WBKT_weight_increment_factor / -10.0) - 1.0)
#     else:
#         return 1.0

# for i in range(-10, 11, 1):
#     print(i, ' => ', find_WBKT_weight_from_increment_factor(i))

# import numpy as np

# def find_current_WBKT_weight_increment_factor(current_WBKT_parameter_weight):
#     if (current_WBKT_parameter_weight > 1.0):
#         return int(round((current_WBKT_parameter_weight - 1.0) / 0.2, 2))
#     elif (current_WBKT_parameter_weight < 1.0):
#         return int(round((1.0 - current_WBKT_parameter_weight) * -10.0, 2))
#     else:
#         return 0
    
# # float step
# for i in np.arange(0.2, 2.6, 0.1):
#     print(i, ' => ', find_current_WBKT_weight_increment_factor(i))


def calculate_new_probability_given_weight(original_probability:float, weight:float):
    numerator = original_probability * weight
    denominator = 1 - original_probability + (original_probability * weight)
    new_probability = numerator / denominator
    if (new_probability < 0):
        return 0.0
    elif (new_probability > 1):
        return 1.0
    else:
        return new_probability


p_g = 0.2
# w_g = 1.0

# w_g_data = [1.0, 1.2, 1.0, 0.8, 0.5, 0.9, 0.7, 0.5, 0.5, 0.9, 0.9, 0.8, 0.6, 0.5, 0.9, 0.7, 0.5, 0.5, 0.9, 0.7, 0.5, 0.5, 0.9, 0.7, 0.5, 0.5, 0.9, 0.7, 0.5, 0.5]
w_g_data = [0.5, 0.6, 0.7, 0.8, 0.9, 1.2, 1.4, 1.6, 1.8, 2.0]
# resulting_p_g_data = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

# for w_g in w_g_data:
#     print(w_g)

for w_g in w_g_data:
    new_probability = calculate_new_probability_given_weight(p_g, w_g)
    # Para evitar la degeneración teórica del modelo WBKT
    if (new_probability > 0.49):
        print(0.49)
    elif (new_probability < 0.01):
        print(0.01) # Esto es para evitar que la probabilidad sea exactamente 0.0
    else:
        print(new_probability)


    


