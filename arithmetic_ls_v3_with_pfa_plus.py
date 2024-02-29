import ArithmeticExerciseGenerator
import DifficultyMachineV2
import ArithmeticResponseV3PFAPlusValidator
import PFAPlus as pfa_plus
import Timer

#### Sistema de aprendizaje por dominio mediante la práctica de ejercicios aritméticos
# Versión 3
# Además de considerar si la respuesta dada por el usuario es correcta o no, también se considera el 
#   tiempo de respuesta correcta del usuario frente a un ejercicio (a partir del momento en que se muestra el ejercicio) 
#   y un número de intentos permitidos por ejercicio en cada nivel de dificultad.

# Se considerarán dos tiempos de referencia de respuesta correcta para ejercicios en cada uno de los niveles de 
#   dificultad definidos:
#   - Un tiempo máximo de respuesta hasta donde el cual la respuesta correcta es considerada superior (inclusivo).
#   - Un tiempo mínimo de respuesta a partir del cual la respuesta correcta es considerada inferior (no inclusivo).
# response_times_per_difficulty_references = [2.1, 5.2, 7.25, 9.3, 13.0, 6.8, 22.0]
base_cr_times_per_difficulty = [2.1, 5.2, 7.25, 9.3, 13.0, 6.8, 22.0] # cr: correct response
# https://www.geeksforgeeks.org/python-map-function/
# Tiempo estimado inicialmente * 0.95
# min_response_times_per_difficulty_references = list(map(lambda x: x * 0.95, response_times_per_difficulty_references))
max_superior_cr_times_per_difficulty = list(map(lambda x: x * 0.95, base_cr_times_per_difficulty))
# Tiempo estimado inicialmente * 1.1
# max_response_times_per_difficulty_references = list(map(lambda x: x * 1.1, response_times_per_difficulty_references))
min_inferior_cr_times_per_difficulty = list(map(lambda x: x * 1.1, base_cr_times_per_difficulty))

# Se considerará un número máximo de intentos permitidos por ejercicio en cada uno de los niveles de dificultad definidos
max_exercise_attempts_per_difficulty = [1, 1, 1, 2, 2, 2, 2]

# En fin, cada nivel de dificultad tiene asociado unos valores de referencia de correspondientes a un tiempo máximo de
#   respuesta correcta hasta donde esta seguirá considerando superior, un tiempo mínimo de respuesta a partir del cual
#   la respuesta correcta se considerará inferior, y un número máximo de intentos permitidos por ejercicio.

# Se considerarán 7 niveles de dificultad en el sistema
difficulty_levels = []
for i in range(0, 7):
    difficulty_levels.append(DifficultyMachineV2.DifficultyV3.Difficulty(i + 1,
        max_exercise_attempts_per_difficulty[i], 
        max_superior_cr_times_per_difficulty[i], 
        min_inferior_cr_times_per_difficulty[i]))

# El estado de la máquina de dificultades es la que determina el nivel de dificultad del siguiente ejercicio mostrado
#   al estudiante o usuario.
dm = DifficultyMachineV2.DifficultyMachine(difficulty_levels)

# Variable que representa si se va a mostrar el mismo ejercicio al estudiante o no.
same_exercise_flag = False # Si este valor es False, significa que se debe generar otro ejercicio en la siguiente iteración.

# Variable que cuenta los intentos realizados en un mismo ejercicio.
# Este valor, junto con el número máximo de intentos por ejercicios en la dificultad actual, se usará para decidir 
#   cuándo se mostrará otro ejercicio al estudiante del mismo nivel de dificultad.
same_exercise_attempts = 0

# Cronógrafo para calcular el tiempo de respuesta del usuario frente a un ejercicio.
# Este tiempo se calcula desde el momento en que el usuario ve el ejercicio, hasta que el usuario responda correctamente el
#   ejercicio, o en su defecto, el ejercicio o la dificultad cambie.
# Este tiempo se usará para determinar si una respuesta correcta es inferior, superior o esperada, y dependiendo de esto,
#   modificará parámetros del modelo WBKT asociado al nivel de dificultad del ejercicio al cual se dio respuesta, por medio
#   de los pesos del modelo WBKT.
timer = Timer.Timer()

#### Integración del modelo PFA+ con el programa de ejercicios de sumas (V3)
# En este caso, cada nivel de dificultad se considerá una habilidad o componente de conocimiento j según el modelo PFA+.
# Todas las habilidades del modelo PFA+ comparten el mismo modelo.

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

# Variables que almacenan cuál es el siguiente ejercicio a mostrar al estudiante, y su número dentro de todos los que
#   se han mostrado desde un principio.
exercise = None
exercise_number = 0

while (not dm.is_on_end_state()):
    if (dm.is_on_start_state()):
        dm.increase_difficulty()
        continue

    # Si el ejercicio a mostrar al estudiante NO es el mismo
    if same_exercise_flag == False:
        exercise = ArithmeticExerciseGenerator.ArithmeticExerciseGenerator().generate_exercise(
            dm.get_current_state())
        exercise_number += 1

        if exercise_number == 1:
            print('---- Ejercicios Aritméticos ----')

        # exercise_attempts = 0
        same_exercise_attempts = 0

    print('-- Ejercicio # ' + str(exercise_number) + ' --')
    print('Escriba la respuesta para el siguiente ejercicio: ')
    print(exercise.get_description())

    # En este punto, se asume que el usuario puede comenzar a identificar el ejercicio.
    #   Esto, por supuesto, si el ejercicio a mostrar al estudiante NO es el mismo.

    # Reinicie el contador de respuesta correcta para un ejercicio solamente cuando el ejercicio cambie.
    if same_exercise_flag == False:
        timer.start_new_timer()

    response = input('>> ')
    # En este punto, ya se ha recibido una respuesta al ejercicio por parte del usuario
    exercise_response_time_in_seconds = timer.get_elapsed_time_in_seconds()

    try:
        response = int(response)
        # Desde aquí se sabe que ya se ha enviado una respuesta válida por parte del usuario 
        # (si no se produce una excepción de tipo ValueError); registre un intento más para el ejercicio.
        same_exercise_attempts += 1

        # Obtenga la(s) habilidad(es) involucradas en el ítem o ejercicio
        #   (Dependiendo del nivel de dificultad del ejercicio - En este caso siempre se involucrará solo 1 habilidad j)
        j = exercise.get_difficulty().get_difficulty_level() - 1

        # NOTAS DE FUNCIONAMIENTO DEL MODELO PFA+:
        # En la implementación del modelo PFA+, al igual que en un modelo PFA, se cambian los criterios de toma de 
        #   decisiones frente a cuándo se cambia la dificultad de los ejercicios a los estudiantes con respecto a los 
        #   criterios usados en los programas de ejercicios sin PFA+ (o PFA).
        # La toma de decisiones frente a cuándo se cambia de ejercicio de una misma dificultad sigue siendo independiente
        #   del modelo PFA o PFA+, y es más bien dependiente de unos números de intento máximo para ellos, elegido de forma
        #   heurística o arbitraria.
        # Recuerde que los modelos PFA+ se actualizan cada vez que se recibe un resultado de un intento o interacción.
        # Al actualizarse el modelo PFA+, el estimado a posteriori de la probabilidad de que el usuario o estudiante
        #   responda correctamente un ítem que involucre una habilidad j es automáticamente actualizado.
        # Una vez se tenga este valor estimado a posteriori p(m, t+1), y dependiendo de si la respuesta fue correcta o no,
        #   el número de intentos realizados en ese ejercicio - incluyendo esa respuesta, el nivel de dificultad actual, y
        #   la rapidez de las respuesta (en caso que esta sea correcta), se toma una o dos decisiones, según sea el caso:
        # 1) Cuál es el nivel de dificultad que debería tener el próximo ejercicio.
        # 2) Si el nivel de dificultad es el mismo, cuál es el ejercicio que debería mostrarse al estudiante: 
        #   ¿el mismo, u otro diferente?

        # Con base en lo anterior, es el momento de tomar los datos relevantes relacionados con la respuesta del usuario,
        #   actualizar el modelo PFA+, y tomar las dos decisiones descritas anteriormente.
        response_validator = ArithmeticResponseV3PFAPlusValidator.ArithmeticResponseValidator(
            exercise, response, exercise_response_time_in_seconds, same_exercise_attempts, 
            pfa_plus_model, j)        
        response_validator_decision = response_validator.validate_response(dm)

        if (response_validator_decision.get_correctness() == True):
            print('Correcto')            
            if(response_validator_decision.get_correct_response_time() == response_validator_decision.
                SUPERIOR_CORRECT_RESPONSE_TIME):
                print('Tiempo de respuesta correcta: Superior al esperado (<=', 
                str(max_superior_cr_times_per_difficulty[j]) + ')')
            elif(response_validator_decision.get_correct_response_time() == response_validator_decision.
                INFERIOR_CORRECT_RESPONSE_TIME):
                print('Tiempo de respuesta correcta: Inferior al esperado (>', 
                str(min_inferior_cr_times_per_difficulty[j]) + ')')
            else:
                print('Tiempo de respuesta correcta: Esperado (> ', 
                max_superior_cr_times_per_difficulty[j], 'y <= ', 
                str(min_inferior_cr_times_per_difficulty[j]) + ')')
            print('El tiempo de respuesta correcta del ejercicio fue de:', exercise_response_time_in_seconds, "segundos.")
            print('El número total de intentos realizados en este ejercicio fue de:', same_exercise_attempts, "intento(s).")
        else:
            print('Incorrecto')
            print('El número total de intentos realizados en este ejercicio es de:', 
                same_exercise_attempts, "intento(s).")

        dm.set_current_state(response_validator_decision.get_next_difficulty())
        same_exercise_flag = response_validator_decision.get_same_exercise()

        # TESTING: Imprima los valores del modelo PFA+:
        print('-----------------')
        print('TESTING:')
        print()
        print('---- Valores de seguimiento del modelo PFA+ ----')
        print('Valores s (número de respuestas correctas del estudiante en donde se involucra la habilidad j, por cada habilidad j):')
        print(pfa_plus_model.get_s())
        print('Valores f (número de respuestas incorrectas del estudiante en donde se involucra la habilidad j, por cada habilidad j):')
        print(pfa_plus_model.get_f())

        print('Valores lt (número de demostraciones de rapidez en respuestas correctas por parte del estudiante en donde se',
            'involucra la habilidad j, por cada habilidad j):')
        print(pfa_plus_model.get_lt())
        print('Valores ht (número de demostraciones de lentitud en respuestas correctas por parte del estudiante en donde se',
            'involucra la habilidad j, por cada habilidad j):')
        print(pfa_plus_model.get_ht())

        print()
        print('---- Estimaciones del modelo PFA+ ----')
        print('Valores logit m que representan el grado de dominio del estudiante para responder correctamente a un ítem que', 
            'involucra una habilidad j, por cada habilidad j:')
        print(pfa_plus_model.get_m())
        print('Probabilidades p(m) que tiene el estudiante para responder correctamente a un ítem que', 
            'involucra una habilidad j, por cada habilidad j:')
        print(pfa_plus_model.get_p_m())

        print()

    except ValueError:
        print('El formato de la respuesta no es el adecuado. Por favor ingrese un número para responder el ejercicio.')
        print()
        same_exercise_flag = True