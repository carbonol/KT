import WBKT as wbkt
import copy

# Simulador de actividad con el modelo WBKT

#### Parámetros para el ejercicio de sumas
# Parámetros del modelo WBKT
p_l0 = 0.01
p_t = 0.09
p_g = 0.2
p_s = 0.1

w_l0 = 1.0
w_t = 1.0
w_g = 1.0
w_s = 1.0

# Supongamos un aumento/disminución de 0.2, dependiendo de si se alcanzó un tiempo óptimo o no.

# Al aumentar los pesos, la probabilidad aumenta
# Al disminuir los pesos, la probabilidad disminuye

# Parámetros de verificación del modelo BKT: Primera y segunda prueba empírica
# C = 0.95
# I = 0.01
# N = 2
# M = 5

# Parámetros de verificación del modelo BKT: Tercera prueba empírica
# p_l_max = 0.9999999999999999
# p_l_max = 0.999
# p_l_max = 0.99
# # p_l_max = 0.961722613921628
# max_iterations = 1000
# p_l_precision = 2
# p_l_precision = 16

wbkt_model = wbkt.WBKT(p_l0, p_t, p_g, p_s, w_l0, w_t, w_g, w_s)

print('Parámetros del modelo WBKT:')
print('p(L0) = p(L,t=0) =', wbkt_model.get_p_lt())
print('p(T) =', wbkt_model.get_p_t())
print('p(G) =', wbkt_model.get_p_g())
print('p(S) =', wbkt_model.get_p_s())

print('w(L0) =', wbkt_model.get_w_l0())
print('w(T) =', wbkt_model.get_w_t())
print('w(G) =', wbkt_model.get_w_g())
print('w(S) =', wbkt_model.get_w_s())

print('Probabilidades modificadas al ajustarlas con los pesos')
print('p(L0)\' = p(L,t=0) =', wbkt_model.calculate_new_p_l0_given_weight())
print('p(T)\' =', wbkt_model.calculate_new_p_t_given_weight())
print('p(G)\' =', wbkt_model.calculate_new_p_g_given_weight())
print('p(S)\' =', wbkt_model.calculate_new_p_s_given_weight())

observations = [True, True, True, True, True]
# observations = [True, True, True, False, False, True, False, True, True, True, True, True, False, True, True, True, True, True]

obs_count = 0
for obs in observations:
    obs_count += 1
    print('Observación #', obs_count ,':')
    wbkt_model.update_model(observation=obs)
    print('p(L,t=',obs_count,') = ', wbkt_model.get_p_lt(), sep='')

# Verificación del modelo BKT: Degeneración teórica, degeneración empírica
# verify_bkt(bkt_model, I, N, C, M, p_l_max, max_iterations, p_l_precision)

# # Graficación que muestra los valores p(L) de las pruebas de degeneración empírica
# generate_empirical_degeneration_test_graphs(bkt_model, I, N, C, M, p_l_max, max_iterations, p_l_precision)

# # Hallazgo de valores de p(L) que representan cotas de aumento o disminución de valores de p(L) bajo ciertas circunstancias
# find_key_pl_values(bkt_model, p_l_max, max_iterations, p_l_precision)

# Graficación que muestra los valores p(L) que impiden el aumento o disminución de valores de p(L) bajo ciertas circunstancias
# generate_key_pl_values_graphs(bkt_model, p_l_max, max_iterations, p_l_precision)