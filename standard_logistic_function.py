import matplotlib.pyplot as plt
import numpy as np

def generate_standard_logistic_function_graph(precision, min_x_value, max_x_value, markersize):
    if (type(precision) != int and precision < 0):
        raise ValueError('El valor del argumento precision debe ser un número entero (int) mayor o igual a 0')
    if (type(min_x_value) != float and min_x_value <= 0.0):
        raise ValueError('El valor del argumento min_x_value debe ser un número real (float) mayor que 0.0')
    if (type(min_x_value) != float and max_x_value >= 1.0):
        raise ValueError('El valor del argumento max_x_value debe ser un número real (float) menor que 1.0')    
    
    print('Graficando la función logística estándar en el intervalo [' + str(min_x_value) + '; ' 
        + str(max_x_value) + ']...')

    # [-7, 7] = 7 - (-7) = 14 * 1 = 14 + 1 = 15
    # [-7.0, 7.0] = 14 * 10 = 140 + 1 = 141

    # [0.1; 0.9] = 0.9 - 0.1 = 0.8 * 10 = 8/10 * 10 = 8 + 1 = 9
    # [0.01; 0.99] = 0.99 - 0.01 = 0.98 * 100 = 98/100 * 100 = 98 + 1 = 99 
    n = ((max_x_value - min_x_value) * (10 ** precision)) + 1
    x = np.linspace(min_x_value, max_x_value, int(n)) # Valor mínimo, valor máximo, número de valores a considerar 
    #   entre el valor mínimo y el valor máximo
    # https://numpy.org/doc/stable/reference/generated/numpy.exp.html
    y = 1 / (1 + np.exp(-x))

    fig, ax = plt.subplots()
    ax.plot(x, y, 'yo--', linewidth=1, markersize=markersize)
    plt.show()

# 1) Gráfico de la función logística estándar con valores en función de m, siendo m un valor logit en 
#   el intervalo cerrado [-7, 7]
generate_standard_logistic_function_graph(0, -7.0, 7.0, 10)
generate_standard_logistic_function_graph(1, -7.0, 7.0, 10)
generate_standard_logistic_function_graph(2, -7.0, 7.0, 5)
generate_standard_logistic_function_graph(3, -7.0, 7.0, 2.5)
generate_standard_logistic_function_graph(4, -7.0, 7.0, 1.25)

# 2) Gráfico de la función logística estándar con valores en función de m, siendo m un valor logit en 
#   el intervalo cerrado [-1.09861229, 2.94443898]
# PELIGRO: EL TIEMPO Y LOS RECURSOS COMPUTACIONALES REQUERIDOS PARA EJECUTAR ESTA LÍNEA DE CÓDIGO SON DEMASIADO ALTOS
# generate_standard_logistic_function_graph(8, -1.09861229, 2.94443898, 1)
generate_standard_logistic_function_graph(4, -1.09861229, 2.94443898, 1)