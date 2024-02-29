import PFAPlus as pfa_plus

import matplotlib.pyplot as plt
import numpy as np

# Definición de parámetros del modelo PFA+
kc_count = 7 # Número de habilidades

beta = []
beta_j = -1.0

gamma = []
gamma_j = 1.5

rho = []
rho_j = -1.5

gamma_t = []
gamma_t_j = 1.5

rho_t = []
rho_t_j = -0.75

for j in range(kc_count): # Por cada habilidad, haga lo siguiente:
    beta.append(beta_j)
    beta_j -= 1.0
    gamma.append(gamma_j)
    rho.append(rho_j)
    if (j == 2):
        rho_j = -0.75
    gamma_t.append(gamma_t_j)
    rho_t.append(rho_t_j)

# Creación del modelo PFA+ con base en los parámetros definidos anteriormente
#   (Esto aplica para 1 estudiante y un número kc_count de habilidades o componentes de conocimiento evaluables)
pfa_plus_model = pfa_plus.PFAPlus(kc_count, beta, gamma, rho, gamma_t, rho_t)

# Impresión en pantalla del estado inicial del modelo PFA
#   (Esto es para asegurarse de que la creación del modelo PFA funciona)
print('Se ha generado un modelo PFA+.')
print('Estado del modelo PFA+ generado:')
print('Número de habilidades o componentes de conocimiento (kc_count) =', pfa_plus_model.get_kc_count())
print()
print('---- Parámetros del modelo PFA+ ----')
print('Parámetros beta (nivel de facilidad por cada habilidad j):')
for i in range(kc_count):
    print('beta_' + str(i + 1) + ' =', pfa_plus_model.get_beta()[i])
print('Parámetros gamma (tasa de contribución de respuesta correcta al aprendizaje de la habilidad j, por cada habilidad j):')
for i in range(kc_count):
    print('gamma_' + str(i + 1) + ' =', pfa_plus_model.get_gamma()[i])
print('Parámetros rho (tasa de contribución de respuesta incorrecta al aprendizaje de la habilidad j, por cada habilidad j):')
for i in range(kc_count):
    print('rho_' + str(i + 1) + ' =', pfa_plus_model.get_rho()[i])

print('Parámetros gamma_t (tasa de contribución de la rapidez en la respuesta correcta al aprendizaje de la habilidad j,',
    'por cada habilidad j):')
for i in range(kc_count):
    print('gamma_t_' + str(i + 1) + ' =', pfa_plus_model.get_gamma_t()[i])
print('Parámetros rho_t (tasa de contribución de la lentitud en la respuesta correcta al aprendizaje de la habilidad j,',
    'por cada habilidad j):')
for i in range(kc_count):
    print('rho_t_' + str(i + 1) + ' =', pfa_plus_model.get_rho_t()[i])

print()
print('---- Valores de seguimiento del modelo PFA+ ----')
print('Valores s (número de respuestas correctas del estudiante en donde se involucra la habilidad j, por cada habilidad j):')
for i in range(kc_count):
    print('s_' + str(i + 1) + ' =', pfa_plus_model.get_s()[i])
print('Valores f (número de respuestas incorrectas del estudiante en donde se involucra la habilidad j, por cada habilidad j):')
for i in range(kc_count):
    print('f_' + str(i + 1) + ' =', pfa_plus_model.get_f()[i])

print('Valores lt (número de demostraciones de rapidez en respuestas correctas por parte del estudiante en donde se',
    'involucra la habilidad j, por cada habilidad j):')
for i in range(kc_count):
    print('lt_' + str(i + 1) + ' =', pfa_plus_model.get_lt()[i])
print('Valores ht (número de demostraciones de lentitud en respuestas correctas por parte del estudiante en donde se',
    'involucra la habilidad j, por cada habilidad j):')
for i in range(kc_count):
    print('ht_' + str(i + 1) + ' =', pfa_plus_model.get_ht()[i])

print()
print('---- Estimaciones del modelo PFA+ ----')
print('Valores logit m que representan el grado de dominio del estudiante para responder correctamente a un ítem que', 
    'involucra una habilidad j, por cada habilidad j:')
for i in range(kc_count):
    print('m_' + str(i + 1) + ' =', pfa_plus_model.get_m()[i])
print('Probabilidades p(m) que tiene el estudiante para responder correctamente a un ítem que', 
    'involucra una habilidad j, por cada habilidad j:')
for i in range(kc_count):
    print('p(m, j=' + str(i + 1) + ')=', pfa_plus_model.get_p_m()[i])

# Impresión en pantalla del estado del modelo PFA cuando se registran nuevas observaciones
# PRUEBA 1
# implied_kcs = [1]
# kcs_success_statuses = [pfa_plus.PFAPlus.CORRECT_OUTCOME]
# pfa_plus_model.update_model(implied_kcs, kcs_success_statuses)
# pfa_plus_model.update_model(implied_kcs, kcs_success_statuses)
# pfa_plus_model.update_model(implied_kcs, kcs_success_statuses)
# PRUEBA 2
# implied_kcs = [1]
# kcs_success_statuses = [pfa_plus.PFAPlus.INCORRECT_OUTCOME]
# pfa_plus_model.update_model(implied_kcs, kcs_success_statuses)
# pfa_plus_model.update_model(implied_kcs, kcs_success_statuses)
# pfa_plus_model.update_model(implied_kcs, kcs_success_statuses)
# PRUEBA 3
# implied_kcs = [1]
# kcs_success_statuses = [pfa_plus.PFAPlus.CORRECT_OUTCOME]
# pfa_plus_model.update_model(implied_kcs, kcs_success_statuses)
# pfa_plus_model.update_model(implied_kcs, kcs_success_statuses)
# pfa_plus_model.update_model(implied_kcs, kcs_success_statuses)
# kcs_success_statuses = [pfa_plus.PFAPlus.INCORRECT_OUTCOME]
# pfa_plus_model.update_model(implied_kcs, kcs_success_statuses)
# PRUEBA 4
# implied_kcs = [1]
# kcs_success_statuses = [pfa_plus.PFAPlus.CORRECT_FAST_OUTCOME]
# pfa_plus_model.update_model(implied_kcs, kcs_success_statuses)
# pfa_plus_model.update_model(implied_kcs, kcs_success_statuses)
# pfa_plus_model.update_model(implied_kcs, kcs_success_statuses)
# PRUEBA 5
# implied_kcs = [1]
# kcs_success_statuses = [pfa_plus.PFAPlus.CORRECT_SLOW_OUTCOME]
# pfa_plus_model.update_model(implied_kcs, kcs_success_statuses)
# pfa_plus_model.update_model(implied_kcs, kcs_success_statuses)
# pfa_plus_model.update_model(implied_kcs, kcs_success_statuses)
# PRUEBA 6
implied_kcs = [1]
kcs_success_statuses = [pfa_plus.PFAPlus.CORRECT_OUTCOME]
pfa_plus_model.update_model(implied_kcs, kcs_success_statuses)
pfa_plus_model.update_model(implied_kcs, kcs_success_statuses)
kcs_success_statuses = [pfa_plus.PFAPlus.CORRECT_SLOW_OUTCOME]
pfa_plus_model.update_model(implied_kcs, kcs_success_statuses)
kcs_success_statuses = [pfa_plus.PFAPlus.INCORRECT_OUTCOME]
pfa_plus_model.update_model(implied_kcs, kcs_success_statuses)
kcs_success_statuses = [pfa_plus.PFAPlus.CORRECT_FAST_OUTCOME]
pfa_plus_model.update_model(implied_kcs, kcs_success_statuses)
print()
print('Se ha modificado el modelo PFA.')
print('---- Estimaciones del modelo PFA ----')
print('Valores logit m que representan el grado de dominio del estudiante para responder correctamente a un ítem que', 
    'involucra una habilidad j, por cada habilidad j:')
for i in range(kc_count):
    print('m_' + str(i + 1) + ' =', pfa_plus_model.get_m()[i])
print('Probabilidades p(m) que tiene el estudiante para responder correctamente a un ítem que', 
    'involucra una habilidad j, por cada habilidad j:')
for i in range(kc_count):
    print('p(m, j=' + str(i + 1) + ')=', pfa_plus_model.get_p_m()[i])

# Pregunta 1: ¿Cuántas respuestas correctas requiere un estudiante en cada habilidad j para alcanzar un valor p(m) de por lo 
#   menos 0.95 (estimación de probabilidad de dominio) en todas las habilidades?
# def generate_sucessive_correct_answer_graphs(pfa_model:pfa.PFA):
#     kc_count = pfa_model.get_kc_count()
#     for j in range(kc_count):
#         generate_sucessive_correct_answer_graph(pfa_model, j)

# def generate_sucessive_correct_answer_graph(pfa_model:pfa.PFA, j:int):
#     # Paso 1: Calcule cuántas respuestas correctas se requiere en una habilidad j para alcanzar el valor p(m) 
#     #   de por lo menos 0.95.
#     n = 0
#     m_values = [pfa_model.get_m()[j]]
#     p_m_values = [pfa_model.get_p_m()[j]]
#     while (pfa_model.get_p_m()[j] < 0.95):
#         implied_kcs = [j + 1]
#         kcs_correctness = [True]
#         pfa_model.update_model(implied_kcs, kcs_correctness)
#         n += 1
#         m_values.append(pfa_model.get_m()[j])
#         p_m_values.append(pfa_model.get_p_m()[j])

#     if (n == 0):
#         x = np.array(0)
#         y1 = np.array(m_values)
#         y2 = np.array(p_m_values)
#     elif (n >= 1):
#         x = np.linspace(0, n, n + 1)
#         y1 = np.array(m_values)
#         y2 = np.array(p_m_values)
#         fig, ax = plt.subplots()
#         ax.plot(x, y1, 'go--', linewidth=1, markersize=5)
#         plt.show()
#         fig, ax = plt.subplots()
#         ax.plot(x, y2, 'ko--', linewidth=1, markersize=5)
#         plt.show()

# def get_sucessive_correct_answers_needed_to_reach_mastery_in_all_skills(pfa_model:pfa.PFA):
#     kc_count = pfa_model.get_kc_count()
#     n_values = []
#     for j in range(kc_count):
#         n_values.append(get_sucessive_correct_answers_needed_to_reach_mastery(pfa_model, j))
#     return n_values

# def get_sucessive_correct_answers_needed_to_reach_mastery(pfa_model:pfa.PFA, j:int):
#     # Paso 1: Calcule cuántas respuestas correctas se requiere en una habilidad j para alcanzar el valor p(m) 
#     #   de por lo menos 0.95.
#     n = 0
#     while (pfa_model.get_p_m()[j] < 0.95):
#         implied_kcs = [j + 1]
#         kcs_correctness = [True]
#         pfa_model.update_model(implied_kcs, kcs_correctness)
#         n += 1
#     return n

# Pregunta 2: Cuando se tiene una probabilidad de 95% de responder un ítem en donde está involucrado una habilidad j cualquiera, 
#   ¿cuántas respuestas incorrectas se necesitan al practicar cada una de las habilidades, para alcanzar un valor p(m) 
#   en cada una de ellas de por lo menos 0.25 (estimación de probabilidad de refuerzo)?
# def generate_sucessive_incorrect_answer_graphs(pfa_model:pfa.PFA, n_values:list):
#     kc_count = pfa_model.get_kc_count()
#     for j in range(kc_count):
#         generate_sucessive_incorrect_answer_graph(pfa_model, n_values, j)

# def generate_sucessive_incorrect_answer_graph(pfa_model:pfa.PFA, n_values:list, j:int):
#     n0 = n_values[j]
#     for i in range(n0):
#         implied_kcs = [j + 1]
#         kcs_correctness = [True]
#         pfa_model.update_model(implied_kcs, kcs_correctness)

#     n = 0
#     m_values = [pfa_model.get_m()[j]]
#     p_m_values = [pfa_model.get_p_m()[j]]
#     while (pfa_model.get_p_m()[j] > 0.25):
#         implied_kcs = [j + 1]
#         kcs_correctness = [False]
#         pfa_model.update_model(implied_kcs, kcs_correctness)
#         n += 1
#         m_values.append(pfa_model.get_m()[j])
#         p_m_values.append(pfa_model.get_p_m()[j])

#     if (n == 0):
#         x = np.array(0)
#         y1 = np.array(m_values)
#         y2 = np.array(p_m_values)
#     elif (n >= 1):
#         x = np.linspace(0, n, n + 1)
#         y1 = np.array(m_values)
#         y2 = np.array(p_m_values)
#         fig, ax = plt.subplots()
#         ax.plot(x, y1, 'ro--', linewidth=1, markersize=5)
#         plt.show()
#         fig, ax = plt.subplots()
#         ax.plot(x, y2, 'mo--', linewidth=1, markersize=5)
#         plt.show()

# Pregunta 3: ¿Cuántas respuestas correctas y de un tiempo lo suficientemente rápido requiere un estudiante para 
#   alcanzar un valor p(m) de por lo menos 0.95 (estimación de probabilidad de dominio)?
def generate_sucessive_correct_fast_answer_graphs(pfa_plus_model:pfa_plus.PFAPlus):
    kc_count = pfa_plus_model.get_kc_count()
    for j in range(kc_count):
        generate_sucessive_correct_fast_answer_graph(pfa_plus_model, j)

def generate_sucessive_correct_fast_answer_graph(pfa_plus_model:pfa_plus.PFAPlus, j:int):
    n = 0
    m_values = [pfa_plus_model.get_m()[j]]
    p_m_values = [pfa_plus_model.get_p_m()[j]]
    while (pfa_plus_model.get_p_m()[j] < 0.95):
        implied_kcs = [j + 1]
        kcs_success_statuses = [pfa_plus.PFAPlus.CORRECT_FAST_OUTCOME]
        pfa_plus_model.update_model(implied_kcs, kcs_success_statuses)
        n += 1
        m_values.append(pfa_plus_model.get_m()[j])
        p_m_values.append(pfa_plus_model.get_p_m()[j])

    if (n == 0):
        x = np.array(0)
        y1 = np.array(m_values)
        y2 = np.array(p_m_values)
    elif (n >= 1):
        x = np.linspace(0, n, n + 1)
        y1 = np.array(m_values)
        y2 = np.array(p_m_values)
        fig, ax = plt.subplots()
        ax.plot(x, y1, 'go--', linewidth=1, markersize=5)
        plt.show()
        fig, ax = plt.subplots()
        ax.plot(x, y2, 'bo--', linewidth=1, markersize=5)
        plt.show()

def get_sucessive_correct_fast_answers_needed_to_reach_mastery_in_all_skills(pfa_plus_model:pfa_plus.PFAPlus):
    kc_count = pfa_plus_model.get_kc_count()
    n_values = []
    for j in range(kc_count):
        n_values.append(get_sucessive_correct_fast_answers_needed_to_reach_mastery(pfa_plus_model, j))
    return n_values

def get_sucessive_correct_fast_answers_needed_to_reach_mastery(pfa_plus_model:pfa_plus.PFAPlus, j:int):
    # Paso 1: Calcule cuántas respuestas correctas se requiere en una habilidad j para alcanzar el valor p(m) 
    #   de por lo menos 0.95.
    n = 0
    while (pfa_plus_model.get_p_m()[j] < 0.95):
        implied_kcs = [j + 1]
        kcs_success_statuses = [pfa_plus.PFAPlus.CORRECT_FAST_OUTCOME]
        pfa_plus_model.update_model(implied_kcs, kcs_success_statuses)
        n += 1
    return n

# Pregunta 4: ¿Cuántas respuestas correctas pero de un tiempo demasiado lento requiere un estudiante para alcanzar un 
#   valor p(m) de por lo menos 0.95 (estimación de probabilidad de dominio)?
def generate_sucessive_correct_slow_answer_graphs(pfa_plus_model:pfa_plus.PFAPlus):
    kc_count = pfa_plus_model.get_kc_count()
    for j in range(kc_count):
        generate_sucessive_correct_slow_answer_graph(pfa_plus_model, j)

def generate_sucessive_correct_slow_answer_graph(pfa_plus_model:pfa_plus.PFAPlus, j:int):
    n = 0
    m_values = [pfa_plus_model.get_m()[j]]
    p_m_values = [pfa_plus_model.get_p_m()[j]]
    while (pfa_plus_model.get_p_m()[j] < 0.95):
        implied_kcs = [j + 1]
        kcs_success_statuses = [pfa_plus.PFAPlus.CORRECT_SLOW_OUTCOME]
        pfa_plus_model.update_model(implied_kcs, kcs_success_statuses)
        n += 1
        m_values.append(pfa_plus_model.get_m()[j])
        p_m_values.append(pfa_plus_model.get_p_m()[j])

    if (n == 0):
        x = np.array(0)
        y1 = np.array(m_values)
        y2 = np.array(p_m_values)
    elif (n >= 1):
        x = np.linspace(0, n, n + 1)
        y1 = np.array(m_values)
        y2 = np.array(p_m_values)
        fig, ax = plt.subplots()
        ax.plot(x, y1, 'ro--', linewidth=1, markersize=5)
        plt.show()
        fig, ax = plt.subplots()
        ax.plot(x, y2, 'co--', linewidth=1, markersize=5)
        plt.show()

def get_sucessive_correct_slow_answers_needed_to_reach_mastery_in_all_skills(pfa_plus_model:pfa_plus.PFAPlus):
    kc_count = pfa_plus_model.get_kc_count()
    n_values = []
    for j in range(kc_count):
        n_values.append(get_sucessive_correct_slow_answers_needed_to_reach_mastery(pfa_plus_model, j))
    return n_values

def get_sucessive_correct_slow_answers_needed_to_reach_mastery(pfa_plus_model:pfa_plus.PFAPlus, j:int):
    # Paso 1: Calcule cuántas respuestas correctas se requiere en una habilidad j para alcanzar el valor p(m) 
    #   de por lo menos 0.95.
    n = 0
    while (pfa_plus_model.get_p_m()[j] < 0.95):
        implied_kcs = [j + 1]
        kcs_success_statuses = [pfa_plus.PFAPlus.CORRECT_SLOW_OUTCOME]
        pfa_plus_model.update_model(implied_kcs, kcs_success_statuses)
        n += 1
    return n


# pfa_model = pfa.PFA(kc_count, beta, gamma, rho)
# generate_sucessive_correct_answer_graphs(pfa_model)
# pfa_model = pfa.PFA(kc_count, beta, gamma, rho)
# pfa_model_n_values = get_sucessive_correct_answers_needed_to_reach_mastery_in_all_skills(pfa_model)
# pfa_model = pfa.PFA(kc_count, beta, gamma, rho)
# generate_sucessive_incorrect_answer_graphs(pfa_model, pfa_model_n_values)



pfa_plus_model = pfa_plus.PFAPlus(kc_count, beta, gamma, rho, gamma_t, rho_t)
generate_sucessive_correct_fast_answer_graphs(pfa_plus_model)
pfa_plus_model = pfa_plus.PFAPlus(kc_count, beta, gamma, rho, gamma_t, rho_t)
generate_sucessive_correct_slow_answer_graphs(pfa_plus_model)

# pfa_plus_model = pfa_plus.PFAPlus(kc_count, beta, gamma, rho, gamma_t, rho_t)
# print(get_sucessive_correct_fast_answers_needed_to_reach_mastery_in_all_skills(pfa_plus_model))
# pfa_plus_model = pfa_plus.PFAPlus(kc_count, beta, gamma, rho, gamma_t, rho_t)
# print(get_sucessive_correct_slow_answers_needed_to_reach_mastery_in_all_skills(pfa_plus_model))