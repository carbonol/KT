import BKT as bkt
import copy

import matplotlib.pyplot as plt
import numpy as np

# import DataSaver

def verify_bkt(bkt_model: bkt, I:float, N: int, C: float, M: int, p_l_max: float, max_iterations: int, p_l_precision: int):
    # Verifique que los valores de los parámetros p(L0), p(T), p(S), p(G) sean mayores que 0.0 y menores que 1.0.
    if are_bkt_parameters_probabilities(bkt_model) == False:
        print('Los valores de los parámetros p(L0), p(T), p(S), p(G) deben ser mayores que 0.0 y menores que 1.0')
        return False
    # Verifique que el modelo BKT no es teóricamente degenerado (p(G) y p(S) deben ser menores o iguales a 0.5)
    if is_bkt_model_not_theoretically_degenerate(bkt_model) == False:
        print('Los valores de los parámetros p(G) y p(S) deben ser menores o iguales a 0.5' +
            ' para evitar la degeneración teórica del modelo BKT')
        return False
    # Verifique que el modelo BKT no es empíricamente degenerado
    if is_bkt_model_not_empirically_degenerate(bkt_model, I, N, C, M, p_l_max, max_iterations, p_l_precision) == False:
        return False
    return True

def are_bkt_parameters_probabilities(bkt_model: bkt):    
    if are_bkt_model_parameters_non_guarantee_probabilities(bkt_model) == False:
        return False
    return True

def are_bkt_model_parameters_non_guarantee_probabilities(bkt_model: bkt):
    if is_non_guarantee_probability(bkt_model.get_p_l0()) == False:
        return False
    if is_non_guarantee_probability(bkt_model.get_p_t()) == False:
        return False
    if is_non_guarantee_probability(bkt_model.get_p_s()) == False:
        return False
    if is_non_guarantee_probability(bkt_model.get_p_g()) == False:
        return False
    return True

def is_non_guarantee_probability(probability: float):
    if (probability > 0.0 and probability < 1.0):
        return True
    return False

def is_bkt_model_not_theoretically_degenerate(bkt_model: bkt):
    if bkt_model.get_p_s() >= 0.0 and bkt_model.get_p_s() <= 0.5:
        if bkt_model.get_p_g() >= 0.0 and bkt_model.get_p_g() <= 0.5:
            return True
    return False

def is_bkt_model_not_empirically_degenerate(bkt_model: bkt, I:float, N: int, C: float, M: int, 
    p_l_max: float, max_iterations: int, p_l_precision: int):
    # if (does_bkt_model_pass_first_empirical_degeneration_test(bkt_model, N) == False):
    #     print('Cuando p(Lt) = p(L0), después de N interacciones correctas consectivas, el valor de p(Lt) no aumenta. ' 
    #     + 'Por lo tanto, este modelo BKT reprueba la primera prueba de degeneración empírica.')
    #     return False
    if (does_bkt_model_pass_first_empirical_degeneration_test_with_defined_increment(bkt_model, I, N) == False):
        print('Cuando p(Lt) = p(L0), después de N interacciones correctas consecutivas, el valor de p(Lt) no logra ' 
        + 'aumentar a un valor mayor que p(L0) + I, donde I = ' + str(I) + '. ' +
        + 'Por lo tanto, este modelo BKT reprueba la primera prueba de degeneración empírica con un incremento I ' 
        + 'y un número de intentos consecutivos N definidos por el usuario.')
        return False
    if (does_bkt_model_pass_second_empirical_degeneration_test(bkt_model, C, M) == False):
        print('Cuando p(Lt) = p(L0), después de M interacciones correctas consecutivas, el valor de p(Lt) no logra ' 
        + 'alcanzar el criterio de aceptación de dominio de la habilidad (C = ' + str(C) + '). ' 
        + 'Por lo tanto, este modelo BKT reprueba la segunda prueba de degeneración empírica con un criterio C ' 
        + 'y un número de intentos consecutivos M definidos por el usuario.')
        return False
    if (does_bkt_model_pass_third_empirical_degeneration_test(bkt_model, p_l_max, max_iterations, p_l_precision)) == False:
        print('Cuando p(Lt) = ' + str(p_l_max) + ', después de un número de interacciones incorrectas consecutivas, '
        + 'el valor de p(Lt) no logra disminuir hasta un valor p(Lt) menor que 0.5. ' 
        + 'Por lo tanto, este modelo BKT reprueba la tercera prueba de degeneración empírica con un ' 
        + 'número de iteraciones = ' + str(max_iterations) + '.')
        return False
    return True

def does_bkt_model_pass_first_empirical_degeneration_test(bkt_model: bkt, N: int):
    print()
    print('Primera prueba de degeneración empírica del modelo BKT con un valor N = ' + str(N) + ':')
    if (N > 0):
        bkt_model_copy = copy.deepcopy(bkt_model)
        starting_p_l = bkt_model_copy.get_p_lt()
        print('p(L0) = ' + str(starting_p_l))

        for i in range(1, N + 1):
            bkt_model_copy.update_model(True)
            print('p(L' + str(i) + ') = ' + str(bkt_model_copy.get_p_lt()))

        if bkt_model_copy.get_p_lt() > starting_p_l:
            return True
        else:
            return False
    else:
        return False

def does_bkt_model_pass_first_empirical_degeneration_test_with_defined_increment(bkt_model: bkt, I: float, N: int):
    print()
    print('Primera prueba de degeneración empírica del modelo BKT con un valor N = ' + str(N) + ' y un incremento ' 
    + 'mínimo I = ' + str(I) + ', definidos por el usuario:')
    if (N > 0):
        bkt_model_copy = copy.deepcopy(bkt_model)
        starting_p_l = bkt_model_copy.get_p_lt()
        print('p(L0) = ' + str(starting_p_l))

        for i in range(1, N + 1):
            bkt_model_copy.update_model(True)
            print('p(L' + str(i) + ') = ' + str(bkt_model_copy.get_p_lt()))

        if bkt_model_copy.get_p_lt() > starting_p_l + I:
            return True
        else:
            return False
    else:
        return False

def does_bkt_model_pass_second_empirical_degeneration_test(bkt_model: bkt, C: float, M: int):
    print()
    print('Segunda prueba de degeneración empírica del modelo BKT con un criterio de alcance de dominio C = ' + str(C) 
    + ' y un número M = ' + str(M) + ' de intentos correctos consecutivos, definido por el usuario:')
    if (N > 0):
        bkt_model_copy = copy.deepcopy(bkt_model)
        starting_p_l = bkt_model_copy.get_p_lt()
        print('p(L0) = ' + str(starting_p_l))

        for i in range(1, M + 1):
            bkt_model_copy.update_model(True)
            print('p(L' + str(i) + ') = ' + str(bkt_model_copy.get_p_lt()))

        if bkt_model_copy.get_p_lt() >= C:
            return True
        else:
            return False
    else:
        return False

def does_bkt_model_pass_third_empirical_degeneration_test(bkt_model: bkt, p_l_max: float, 
    max_iterations: int, p_l_precision: int):
    print()
    print('Tercera prueba de degeneración empírica del modelo BKT con un valor p(Lt) de inicio de ' + str(p_l_max) 
    + ', una precisión de ' + str(p_l_precision) + ' dígitos, ' 
    + 'y un número máximo de iteraciones = ' + str(max_iterations)  
    + ', los cuales son definidos por el usuario:')
    if (N > 0):
        bkt_model_copy = bkt.BKT(p_l0=p_l_max, p_t=bkt_model.get_p_t(),
            p_g=bkt_model.get_p_g(), p_s=bkt_model.get_p_s())
        starting_p_l = bkt_model_copy.get_p_lt()
        previous_p_l = starting_p_l
        print('p(LN) = ' + str(starting_p_l))

        for i in range(1, max_iterations + 1):
            bkt_model_copy.update_model(False)
            # print('p(LN+' + str(i) + ') = ' + str(bkt_model_copy.get_p_lt()) 
            # + ' => ' + str(round(number=bkt_model_copy.get_p_lt(), ndigits=4)))
            # previous_p_l = bkt_model_copy.get_p_lt()
            if (round(bkt_model_copy.get_p_lt(), p_l_precision) != round(previous_p_l, p_l_precision)):
                print('p(LN+' + str(i) + ') = ' + str(bkt_model_copy.get_p_lt()) 
                + ' => ' + str(round(number=bkt_model_copy.get_p_lt(), ndigits=p_l_precision)))
                previous_p_l = bkt_model_copy.get_p_lt()
            else:
                print('En la iteración N = ' + str(i) + ', el valor de p(Lt), con un redondeo de ' + str(p_l_precision) + 
                ' dígitos, no sigue disminuyendo cuando se producen respuestas incorrectas sucesivas.')
                break

        if bkt_model_copy.get_p_lt() < 0.5:
            return True
        else:
            return False
    else:
        return False

def find_key_pl_values(bkt_model: bkt, p_l_max: float, max_iterations: int, p_l_precision: int):
    
    print('Valor de p(L) a partir del cual no se puede seguir aumentando la estimación de dominio con respuestas ' 
    + 'incorrectas sucesivas: '
    + str(find_lower_pl_boundary_where_pl_cannot_increase_with_only_wrong_answers(bkt_model, max_iterations, p_l_precision)))

    # wa_pld_b = find_lower_pl_boundary_where_pl_cannot_decrease_with_wrong_answers(bkt_model, p_l_max, 
    #     max_iterations, p_l_precision)
    # print('Valor de p(L) a partir del cual no se puede seguir disminuyendo la estimación de dominio con respuestas ' 
    # + 'incorrectas sucesivas: ' + str(wa_pld_b))

    wa_pld_ub = find_pl_boundary_where_pl_cannot_decrease_with_wrong_answers(bkt_model, p_l_max, 
        max_iterations, p_l_precision)
    print('Primer valor de p(L) a partir del cual no se puede seguir disminuyendo la estimación de dominio con respuestas ' 
    + 'incorrectas sucesivas: ' + str(wa_pld_ub))

    # print(10.0 ** -2)
    # print(wa_pld_ub - (10.0 ** -p_l_precision))
    wa_pld_lb = find_pl_boundary_where_pl_cannot_decrease_with_wrong_answers(bkt_model, wa_pld_ub - (10.0 ** -p_l_precision), 
        max_iterations, p_l_precision)
    print('Segundo valor de p(L) a partir del cual no se puede seguir disminuyendo la estimación de dominio con respuestas ' 
    + 'incorrectas sucesivas: ' + str(wa_pld_lb))

    print('Valor de p(L) a partir del cual no se puede seguir aumentando la estimación de dominio con respuestas ' 
    + 'correctas sucesivas: ' 
    + str(find_upper_pl_boundary_where_pl_cannot_increase_with_right_answers(bkt_model, max_iterations, p_l_precision)))

def find_lower_pl_boundary_where_pl_cannot_increase_with_only_wrong_answers(bkt_model: bkt, 
    max_iterations: int, p_l_precision: int):
    print()
    print('Procedimiento para encontrar el valor de p(L) a partir del cual no se puede seguir aumentando dicho ' 
    + 'valor con respuestas incorrectas sucesivas:')
    if (N > 0):
        bkt_model_copy = copy.deepcopy(bkt_model)
        starting_p_l = bkt_model_copy.get_p_lt()
        previous_p_l = starting_p_l
        print('p(L0) = ' + str(starting_p_l))

        for i in range(1, max_iterations + 1):
            bkt_model_copy.update_model(False)
            if (round(bkt_model_copy.get_p_lt(), p_l_precision) != round(previous_p_l, p_l_precision)):
                # print('p(L' + str(i) + ') = ' + str(bkt_model_copy.get_p_lt())
                # + ' => ' + str(round(number=bkt_model_copy.get_p_lt(), ndigits=p_l_precision)))
                previous_p_l = bkt_model_copy.get_p_lt()
            else:
                print('En la iteración N = ' + str(i) + ', el valor de p(Lt), con un redondeo de ' + str(p_l_precision) + 
                ' dígitos, no sigue aumentando cuando se producen respuestas incorrectas sucesivas.')
                return previous_p_l
    else:
        return None

def find_pl_boundary_where_pl_cannot_decrease_with_wrong_answers(bkt_model: bkt, p_l_max: float, 
    max_iterations: int, p_l_precision: int):
    print()
    print('Procedimiento para encontrar el valor de p(L) a partir del cual no se puede seguir disminuyendo dicho ' 
    + 'valor con respuestas incorrectas sucesivas:')
    if (N > 0):
        bkt_model_copy = bkt.BKT(p_l0=p_l_max, p_t=bkt_model.get_p_t(),
            p_g=bkt_model.get_p_g(), p_s=bkt_model.get_p_s())
        starting_p_l = bkt_model_copy.get_p_lt()
        previous_p_l = starting_p_l
        print('p(LN) = ' + str(starting_p_l))

        for i in range(1, max_iterations + 1):
            bkt_model_copy.update_model(False)
            if (round(bkt_model_copy.get_p_lt(), p_l_precision) != round(previous_p_l, p_l_precision)):
                # print('p(LN+' + str(i) + ') = ' + str(bkt_model_copy.get_p_lt())
                # + ' => ' + str(round(number=bkt_model_copy.get_p_lt(), ndigits=p_l_precision)))
                previous_p_l = bkt_model_copy.get_p_lt()
            else:
                print('En la iteración N = ' + str(i) + ', el valor de p(Lt), con un redondeo de ' + str(p_l_precision) + 
                ' dígitos, no sigue disminuyendo cuando se producen respuestas incorrectas sucesivas.')
                return previous_p_l
    else:
        return None

def find_upper_pl_boundary_where_pl_cannot_increase_with_right_answers(bkt_model: bkt, 
    max_iterations: int, p_l_precision: int):
    print()
    print('Procedimiento para encontrar el valor de p(L) a partir del cual no se puede seguir aumentando dicho ' 
    + 'valor con respuestas correctas sucesivas:')
    if (N > 0):
        bkt_model_copy = copy.deepcopy(bkt_model)
        starting_p_l = bkt_model_copy.get_p_lt()
        previous_p_l = starting_p_l
        print('p(L0) = ' + str(starting_p_l))

        for i in range(1, max_iterations + 1):
            bkt_model_copy.update_model(True)
            if (round(bkt_model_copy.get_p_lt(), p_l_precision) != round(previous_p_l, p_l_precision)):
                # print('p(L' + str(i) + ') = ' + str(bkt_model_copy.get_p_lt())
                # + ' => ' + str(round(number=bkt_model_copy.get_p_lt(), ndigits=p_l_precision)))
                previous_p_l = bkt_model_copy.get_p_lt()
            else:
                print('En la iteración N = ' + str(i) + ', el valor de p(Lt), con un redondeo de ' + str(p_l_precision) + 
                ' dígitos, no sigue aumentando cuando se producen respuestas correctas sucesivas.')
                return previous_p_l

def generate_empirical_degeneration_test_graphs(bkt_model: bkt, I:float, N: int, C: float, M: int, 
    p_l_max: float, max_iterations: int, p_l_precision: int):
        generate_first_empirical_degeneration_test_graph(bkt_model, N)
        generate_second_empirical_degeneration_test_graph(bkt_model, C, M)
        generate_third_empirical_degeneration_test_graph(bkt_model, p_l_max, max_iterations, p_l_precision)

def generate_first_empirical_degeneration_test_graph(bkt_model: bkt, N: int):
    print()
    print('Graficación de la primera prueba de degeneración empírica del modelo BKT con un valor N = ' + str(N) + ':')

    x = np.linspace(0, N, N + 1)
    pl_list = []

    if (N > 0):
        bkt_model_copy = copy.deepcopy(bkt_model)
        starting_p_l = bkt_model_copy.get_p_lt()
        pl_list.append(starting_p_l)

        for i in range(1, N + 1):
            bkt_model_copy.update_model(True)
            pl_list.append(bkt_model_copy.get_p_lt())

    y = np.array(pl_list)

    fig, ax = plt.subplots()
    ax.plot(x, y, 'go--', linewidth=1, markersize=10)
    plt.show()

def generate_second_empirical_degeneration_test_graph(bkt_model: bkt, C: float, M: int):
    print()
    print('Graficación de la segunda prueba de degeneración empírica del modelo BKT con un criterio de alcance de dominio ' 
    + 'C = ' + str(C) + ' y un número M = ' + str(M) + ' de intentos correctos consecutivos, definido por el usuario:')

    x = np.linspace(0, M, M + 1)
    pl_list = []

    if (M > 0):
        bkt_model_copy = copy.deepcopy(bkt_model)
        starting_p_l = bkt_model_copy.get_p_lt()
        pl_list.append(starting_p_l)

        for i in range(1, M + 1):
            bkt_model_copy.update_model(True)
            pl_list.append(bkt_model_copy.get_p_lt())

    y = np.array(pl_list)

    fig, ax = plt.subplots()
    ax.plot(x, y, 'go--', linewidth=1, markersize=10)
    plt.show()

def generate_third_empirical_degeneration_test_graph(bkt_model: bkt, p_l_max: float, 
    max_iterations: int, p_l_precision: int):
    print()
    print('Graficación de la tercera prueba de degeneración empírica del modelo BKT con un número de iteraciones = ' 
    + str(max_iterations) + ' definido por el usuario:')

    # x_data_points = 1
    full_precision_x_data_points = 1
    partial_precision_x_data_points = 1

    full_precision_pl_list = []
    partial_precision_pl_list = []

    if (N > 0):
        bkt_model_copy = bkt.BKT(p_l0=p_l_max, p_t=bkt_model.get_p_t(),
            p_g=bkt_model.get_p_g(), p_s=bkt_model.get_p_s())
        starting_p_l = bkt_model_copy.get_p_lt()
        previous_p_l = starting_p_l
        full_precision_pl_list.append(starting_p_l)
        partial_precision_pl_list.append(round(starting_p_l, p_l_precision))

        no_more_rounded_values = False

        # for i in range(1, max_iterations + 1):
        #     bkt_model_copy.update_model(False)
        #     if (round(bkt_model_copy.get_p_lt(), p_l_precision) != round(previous_p_l, p_l_precision)):
        #         full_precision_pl_list.append(bkt_model_copy.get_p_lt())
        #         partial_precision_pl_list.append(round(number=bkt_model_copy.get_p_lt(), ndigits=p_l_precision))
        #         previous_p_l = bkt_model_copy.get_p_lt()
        #         x_data_points += 1

        for i in range(1, max_iterations + 1):
            bkt_model_copy.update_model(False)

            if (not no_more_rounded_values):
                if (round(bkt_model_copy.get_p_lt(), p_l_precision) != round(previous_p_l, p_l_precision)):
                    full_precision_pl_list.append(bkt_model_copy.get_p_lt())
                    partial_precision_pl_list.append(round(number=bkt_model_copy.get_p_lt(), ndigits=p_l_precision))
                    previous_p_l = bkt_model_copy.get_p_lt()
                    # x_data_points += 1
                    full_precision_x_data_points += 1
                    partial_precision_x_data_points += 1
                else:
                    no_more_rounded_values = True
            else:
                full_precision_pl_list.append(bkt_model_copy.get_p_lt())
                previous_p_l = bkt_model_copy.get_p_lt()
                full_precision_x_data_points += 1

    # x = np.linspace(0, x_data_points - 1, x_data_points)
    x = np.linspace(0, full_precision_x_data_points - 1, full_precision_x_data_points)
    y = np.array(full_precision_pl_list)
    fig, ax = plt.subplots()
    ax.plot(x, y, 'ro--', linewidth=1, markersize=10)
    plt.show()

    x = np.linspace(0, partial_precision_x_data_points - 1, partial_precision_x_data_points)
    y = np.array(partial_precision_pl_list)
    fig, ax = plt.subplots()
    ax.plot(x, y, 'ro--', linewidth=1, markersize=10)
    plt.show()

def generate_key_pl_values_graphs(bkt_model: bkt, p_l_max: float, max_iterations: int, p_l_precision: int):
    pass

def generate_lower_pl_boundary_where_pl_cannot_increase_with_only_wrong_answers_finding_procedure_graph():
    pass

def generate_lower_pl_boundary_where_pl_cannot_decrease_with_wrong_answers_finding_procedure_graph():
    pass

def generate_upper_pl_boundary_where_pl_cannot_decrease_with_wrong_answers_finding_procedure_graph():
    pass

def generate_upper_pl_boundary_where_pl_cannot_increase_with_right_answers_finding_procedure_graph():
    pass


# def generate_alternate_responses_graph(bkt_model: bkt, C: float):
#     print()
#     print('Graficación del comportamiento de p(Lt) con resultados alternos de interacciones '
#     + '(correcto, incorrecto, correcto, ...) del modelo BKT con un criterio de alcance de dominio ' 
#     + 'C = ' + str(C) + ' definido por el usuario:')

# Simulador de actividad con el modelo BKT

# Parámetros de prueba
# p_l0 = 0.02
# p_t = 0.05
# p_g = 0.3
# p_s = 0.01

#### Parámetros para el ejercicio de sumas
# Parámetros del modelo BKT
# p_g = 0.3
# p_g = 0.25

# p_l0 = 0.01
# p_t = 0.01
# p_g = 0.2
# p_s = 0.1

# PARÁMETROS EJERCICIO DE SUMAS p(G) = 0.2
p_l0 = 0.01
p_t = 0.01
p_g = 0.2
p_s = 0.1

# MODIFICACIÓN 1 AL p(G) -> w(G) = 0.5
# p_g = 0.11111111111111112
# # MODIFICACIÓN 2 AL p(G) -> w(G) = 0.6
# p_g = 0.13043478260869565
# # MODIFICACIÓN 2 AL p(G) -> w(G) = 0.7
# p_g = 0.14893617021276592
# # MODIFICACIÓN 2 AL p(G) -> w(G) = 0.8
# p_g = 0.16666666666666669
# # MODIFICACIÓN 2 AL p(G) -> w(G) = 0.9
# p_g = 0.1836734693877551

# # MODIFICACIÓN 2 AL p(G) -> w(G) = 1.2
# p_g = 0.23076923076923075
# # MODIFICACIÓN 2 AL p(G) -> w(G) = 1.4
# p_g = 0.2592592592592592
# # MODIFICACIÓN 2 AL p(G) -> w(G) = 1.6
# p_g = 0.28571428571428575
# # MODIFICACIÓN 2 AL p(G) -> w(G) = 1.8
# p_g = 0.3103448275862069
# # MODIFICACIÓN 2 AL p(G) -> w(G) = 2.0
# p_g = 0.3333333333333333

# Parámetros de verificación del modelo BKT: Primera y segunda prueba empírica
C = 0.95
I = 0.01
N = 2

M = 5 # => Ejercicio de sumas: 5 => OK
# M = 14 # p(L0) = 0.01, p(T) = 0.01, p(G) = 0.38, p(S) = 0.38 => OK
# M = 91 # p(L0) = 0.01, p(T) = 0.01, p(G) = 0.49, p(S) = 0.49 => OK
# M = 2 # p(L0) = 0.01, p(T) = 0.01, p(G) = 0.01, p(S) = 0.01 => OK

# PARA w(G) = 1.2 en adelante - Prueba WBKT del caso de estudio.
# M = 6

# PARA w(G) = 1.6 en adelante - Prueba WBKT del caso de estudio.
# M = 7

# PARA w(G) = 2.0 - Prueba WBKT del caso de estudio.
# M = 8

# Parámetros de verificación del modelo BKT: Tercera prueba empírica
# p_l_max = 0.99999999999999999
# p_l_max = 0.9999999999999999
# p_l_max = 0.999
# p_l_max = 0.961722613921628
# p_l_precision = 16

p_l_max = 0.99
# max_iterations = 1000
# p_l_precision = 2
# max_iterations = 2000
# p_l_precision = 17 # Precisión máxima = 17
max_iterations = 1100 # Número de iteraciones máximo observado
p_l_precision = 4 # Precisión mínima aceptable = 4

bkt_model = bkt.BKT(p_l0, p_t, p_g, p_s)

print('Parámetros del modelo BKT:')
print('p(L0) = p(L,t=0) =', bkt_model.get_p_lt())
print('p(T) =', bkt_model.get_p_t())
print('p(G) =', bkt_model.get_p_g())
print('p(S) =', bkt_model.get_p_s())

# observations = [True, True, True, True, True]
# observations = [True, True, True, False, False, True, False, True, True, True, True, True, False, True, True, True, True, True]

# obs_count = 0
# for obs in observations:
#     obs_count += 1
#     print('Observación #', obs_count ,':')
#     bkt_model.update_model(observation=obs)
#     print('p(L,t=',obs_count,') = ', bkt_model.get_p_lt(), sep='')

# Verificación del modelo BKT: Degeneración teórica, degeneración empírica
verify_bkt(bkt_model, I, N, C, M, p_l_max, max_iterations, p_l_precision)

# Graficación que muestra los valores p(L) de las pruebas de degeneración empírica
generate_empirical_degeneration_test_graphs(bkt_model, I, N, C, M, p_l_max, max_iterations, p_l_precision)

# Hallazgo de valores de p(L) que representan cotas de aumento o disminución de valores de p(L) bajo ciertas circunstancias
find_key_pl_values(bkt_model, p_l_max, max_iterations, p_l_precision)

# Graficación que muestra los valores p(L) que impiden el aumento o disminución de valores de p(L) bajo ciertas circunstancias
# generate_key_pl_values_graphs(bkt_model, p_l_max, max_iterations, p_l_precision)

# Cálculo manual de punto medio entre dos puntos
# print((0.5 + 0.011434820225164358) / 2)
# print((0.5 + 0.025919173740869397) / 2)
# print((0.5 + 0.25794899311785086) / 2)
# print((0.5 + 0.010103092025795178) / 2)