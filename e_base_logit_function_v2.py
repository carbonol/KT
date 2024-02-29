import matplotlib.pyplot as plt
import numpy as np

def generate_e_base_logit_graph(precision, min_x_value, max_x_value, markersize):
    if (type(precision) != int and precision <= 0):
        raise ValueError('El valor del argumento precision debe ser un número entero (int) mayor que 0')
    if (type(min_x_value) != float and min_x_value <= 0.0):
        raise ValueError('El valor del argumento min_x_value debe ser un número real (float) mayor que 0.0')
    if (type(min_x_value) != float and max_x_value >= 1.0):
        raise ValueError('El valor del argumento max_x_value debe ser un número real (float) menor que 1.0')    
    
    print('Graficando la función logit de base Euler (e) en el intervalo [' + str(min_x_value) + '; ' 
        + str(max_x_value) + ']...')

    # [0.1; 0.9] = 0.9 - 0.1 = 0.8 * 10 = 8/10 * 10 = 8 + 1 = 9
    # [0.01; 0.99] = 0.99 - 0.01 = 0.98 * 100 = 98/100 * 100 = 98 + 1 = 99 
    n = ((max_x_value - min_x_value) * (10 ** precision)) + 1
    x = np.linspace(min_x_value, max_x_value, int(n)) # Valor mínimo, valor máximo, número de valores a considerar 
    #   entre el valor mínimo y el valor máximo
    # https://numpy.org/doc/stable/reference/generated/numpy.log.html#numpy.log
    # f(x) = ln(x / 1-x)
    y = np.log(x / (1-x))

    fig, ax = plt.subplots()
    ax.plot(x, y, 'bo--', linewidth=1, markersize=markersize)
    plt.show()

# generate_e_base_logit_graph(2, 0.05, 0.95, 5)

# 1) Gráfico de la función logit con base Euler (e) con valores en función de p, siendo p una probabilidad en 
#   el intervalo abierto (0, 1)
# generate_e_base_logit_graph(1, 0.1, 0.9, 10)
# generate_e_base_logit_graph(2, 0.01, 0.99, 5)
generate_e_base_logit_graph(3, 0.001, 0.999, 2.5)
# generate_e_base_logit_graph(4, 0.0001, 0.9999, 1.25)

# 2) Gráfico de la función logit con base Euler (e) con valores en función de p, siendo p una probabilidad en 
#   el intervalo [0.25, 0.95]
# generate_e_base_logit_graph(2, 0.25, 0.95, 5)
# generate_e_base_logit_graph(3, 0.25, 0.95, 2.5)
# generate_e_base_logit_graph(4, 0.25, 0.95, 1.25)

# Pregunta: ¿Cuáles son los valores y = f(x) si x = 0.25 y si x = 0.95?
x = np.linspace(0.25, 0.95, 2)
y = np.log(x / (1-x))
print(y)