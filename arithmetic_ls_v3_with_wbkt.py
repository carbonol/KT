import ArithmeticExerciseGenerator
import DifficultyMachineV2
import ArithmeticResponseV3WBKTValidator
import WBKT as wbkt
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

# COMENTARIO NO VIGENTE:
# Se considerarán unos valores de referencia de números de intentos esperados para responder CORRECTAMENTE a 
#   ejercicios en cada uno de los niveles de dificultad definidos.
# Los valores de referencia de números de intentos realizados antes de respuesta correcta están constituidos por un número 
#   de intentos mínimo, y uno máximo (siendo este número máximo de intentos mayor al mínimo), y los números de intentos que
#   estén dentro de este rango constituyen los números de intentos esperados, antes de obtener la siguiente respuesta
#   correcta, para los ejercicios del nivel de dificultad al cual fueron asignados estos valores.
# exercise_attempts_per_difficulty_references = [1, 1, 1, 2, 2, 2, 2]
# min_exercise_attempts_per_difficulty_references = [1, 1, 1, 2, 2, 2, 2]
# max_exercise_attempts_per_difficulty_references = [1, 1, 1, 2, 2, 2, 2]

# COMENTARIO VIGENTE:
# Se considerará un número máximo de intentos permitidos por ejercicio en cada uno de los niveles de dificultad definidos
max_exercise_attempts_per_difficulty = [1, 1, 1, 2, 2, 2, 2]

# COMENTARIO NO VIGENTE:
# Cada nivel de dificultad tiene asociado unos valores de referencia de tiempos de respuesta (CORRECTA O INCORRECTA) y 
#   unos números de intentos antes de obtener la siguiente respuesta CORRECTA, para ejercicios de ese nivel de dificultad.

# COMENTARIO VIGENTE:
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
# exercise_attempts = 0
same_exercise_attempts = 0

# Cronógrafo para calcular el tiempo de respuesta del usuario frente a un ejercicio.
# Este tiempo se calcula desde el momento en que el usuario ve el ejercicio, hasta que el usuario responda correctamente el
#   ejercicio, o en su defecto, el ejercicio o la dificultad cambie.
# Este tiempo se usará para determinar si una respuesta correcta es inferior, superior o esperada, y dependiendo de esto,
#   modificará parámetros del modelo WBKT asociado al nivel de dificultad del ejercicio al cual se dio respuesta, por medio
#   de los pesos del modelo WBKT.
timer = Timer.Timer()

#### Implementación del WBKT
# En este caso, cada nivel de dificultad se considerá una habilidad según el modelo BKT.
# Es decir, cada nivel de dificultad tendrá su propio modelo WBKT.
# Los valores de los parámetros p(L0), p(T), p(G), p(S) del modelo BKT deberían seleccionarse siguiendo una 
#   heurística razonable, a menos que existan datos de la realidad que puedan usarse para construir el modelo.
# Los valores de los pesos w(L0), w(T), w(G) y w(S) se inicializarán en 1.0, lo que hace que, inicialmente, el modelo
#   WBKT funcione exactamente como un modelo BKT, pero, a medida que se vaya modificando dinámicamente estos pesos en la
#   ejecución del programa, las estimaciones debido a los pesos que modifican los valores de p(L0), p(T), p(G) y p(S).
wbkt_models = []
for i in range(1, 8):
    # bkt_models.append(wbkt.WBKT(p_l0=0.02, p_t=0.05, p_g=0.3, p_s=0.01, w_l0=1.0, w_t=1.0, w_g=1.0, w_s=1.0))
    # Modelo WBKT para ejercicios de sumas
    wbkt_models.append(wbkt.WBKT(p_l0=0.01, p_t=0.01, p_g=0.2, p_s=0.1, w_l0=1.0, w_t=1.0, w_g=1.0, w_s=1.0))

# Datos adicionales a almacenar para tomar decisiones frente a cambios a realizar en los pesos del modelo WBKT de la
#   dificultad actual, dependiendo de ciertas características adicionales de respuestas del usuario 
#   (e.g., tiempo de respuesta correcta)
# NOTA: Estos datos se deben almacenar por cada modelo WBKT o por cada dificultad, por separado.
current_consecutive_superior_time_response_count_per_dl = []
current_consecutive_inferior_time_response_count_per_dl = []
for dl in difficulty_levels:
    current_consecutive_superior_time_response_count_per_dl.append(0)
    current_consecutive_inferior_time_response_count_per_dl.append(0)

# VARIABLES NO VIGENTES:
# # Número de intentos correctos consecutivos y los tiempos de respuesta de estos intentos.
# consecutive_correct_attempts_per_difficulty_level = []
# # Número de intentos incorrectos consecutivos y los tiempos de respuesta de estos intentos.
# consecutive_incorrect_attempts_per_difficulty_level = []
# # Si el último intento fue correcto o no.
# is_last_attempt_correct_flag_per_difficulty_level = [] 
# for dl in difficulty_levels:
#     consecutive_correct_attempts_per_difficulty_level.append([])
#     consecutive_incorrect_attempts_per_difficulty_level.append([])
#     is_last_attempt_correct_flag_per_difficulty_level.append(None)

# Variables que almacenan cuál es el siguiente ejercicio a mostrar al estudiante, y su número dentro de todos los que
#   se han mostrado desde un principio.
exercise = None
exercise_number = 0

# VARIABLE NO VIGENTE:
# Variable de control que dice si el formato de respuesta del usuario fue válido o no
# is_valid_response_flag = True

while (not dm.is_on_end_state()):
    # print(dm.get_current_state_tag())
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

    # En este punto, se asume que el usuario puede comenzar a identificar el ejercicio
    # Si el ejercicio a mostrar al estudiante NO es el mismo

    # COMENTARIO NO VIGENTE: Ya no se calculará el tiempo de respuesta correcta, sino el tiempo de respuesta
    # COMENTARIO NO VIGENTE: Ahora se calculará el tiempo de respuesta de un ejercicio
    # CÓDIGO NO VIGENTE
    # if (is_valid_response_flag):
    #     # Reinicie el contador de tiempo de respuesta únicamente si el formato de respuesta del usuario es válido
    #     #   (o si es el primer ejercicio que se muestra)
    #     timer.start_new_timer() 

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

        # is_valid_response_flag = True
        # exercise_attempts += 1        

        # Obtenga el modelo WBKT correcto a considerar (dependiendo del nivel de dificultad del ejercicio)
        exercise_dl_index = exercise.get_difficulty().get_difficulty_level() - 1
        dl_wbkt_model = wbkt_models[exercise_dl_index]

        # NOTAS DE FUNCIONAMIENTO DEL MODELO WBKT:
        # En la implementación de WBKT, al igual que en un modelo BKT, se cambian los criterios de toma de decisiones frente
        #   a cuándo se cambia la dificultad de los ejercicios a los estudiantes con respecto a los criterios usados en los
        #   programas de ejercicios sin BKT (o WBKT).
        # No obstante, en un modelo WBKT, se añade un paso previo a la actualización de la estimación del dominio de la
        #   habilidad: Antes de esta actualización, se modifican los pesos de algunos parámetros (e.g., p(T), p(G) o p(S))
        #   según la calidad del rendimiento observado del estudiante. En este caso, según la calidad de las respuestas
        #   correctas, dependiendo de si estas fueron alcanzadas en un tiempo esperado, o en uno mayor o menor al esperado.
        # La toma de decisiones frente a cuándo se cambia un ejercicio de una misma dificultad sigue siendo independiente
        #   del modelo BKT o WBKT, y es más bien dependiente de unos números de intento máximo para ellos, elegido de forma
        #   heurística o arbitraria.

        # Recuerde que los modelos BKT se actualizan cada vez que se recibe un resultado de un intento o interacción.
        # En este caso, después de actualizar los pesos del modelo WBKT, se debe actualizar ese modelo de la siguiente forma,
        #   tal como sucede con los modelos BKT:
        # 1) Actualice el valor a priori p(L,t) con base en la evidencia observada.
        #   - i.e., EN ESTE CASO, la respuesta del usuario ante un ejercicio, si este es correcto o no -, 
        # 2) Obtenga el valor a posteriori p(L,t+1) con base en la actualización del valor anterior p(L,t)

        # Una vez se tenga el valor a posteriori p(L,t+1), y dependiendo de si la respuesta fue correcta o no,
        #   el número de intentos realizados en ese ejercicio - incluyendo esa respuesta, y el nivel de dificultad actual,
        #   se toma una o dos decisiones, según sea el caso:
        # 1) Cuál es el nivel de dificultad que debería tener el próximo ejercicio.
        # 2) Si el nivel de dificultad es el mismo, cuál es el ejercicio que debería mostrarse al estudiante: 
        #   ¿el mismo, u otro diferente?

        # CÓDIGO NO VIGENTE
        # # IMPORTANTE: Estos cambios en p(G) son inferencias realizadas con algunos datos obtenidos, 
        # #   pero no son garantías.

        # # Note que el índice que representa el nivel de dificultad actual ya ha sido seleccionado anteriormente por medio
        # #   de la variable exercise_difficulty_level_index

        # # Aumentos/disminuciones acumuladas en los pesos (Estos se podrán ir actualizando conforme se vayan detectando eventos)
        # delta_w_g = 0.0
        # delta_w_s = 0.0

        # # No obstante, es necesario saber primero si la respuesta actual fue correcta o no, antes de detectar eventos
         
        # # Revisión de eventos
        # # I) Al obtener un intento correcto
        # # 1) El número de intentos realizados hasta obtener el próximo intento correcto es MENOR que el número de intentos
        # #   esperados para ello.
        # # 2) El número de intentos realizados hasta obtener el próximo intento correcto es MAYOR que el número de intentos
        # #   esperados para ello.
        # attempts_until_next_correct_response = None
        # is_last_attempt_correct = is_last_attempt_correct_flag_per_difficulty_level[exercise_difficulty_level_index]
        # if (is_last_attempt_correct == None or is_last_attempt_correct == True):
        #     attempts_until_next_correct_response = 1
        # elif (is_last_attempt_correct == False):
        #     attempts_until_next_correct_response = consecutive_incorrect_attempts_per_difficulty_level
        #     [exercise_difficulty_level_index] + 1

        ccstrc = current_consecutive_superior_time_response_count_per_dl[exercise_dl_index]
        ccitrc = current_consecutive_inferior_time_response_count_per_dl[exercise_dl_index]

        # Con base en lo anterior, es el momento de tomar los datos relevantes relacionados con la respuesta del usuario,
        #   y realizar el procedimiento anterior, hasta tomar las dos decisiones descritas anteriormente.
        response_validator = ArithmeticResponseV3WBKTValidator.ArithmeticResponseValidator(
            exercise, response, exercise_response_time_in_seconds, same_exercise_attempts, 
            dl_wbkt_model, ccstrc, ccitrc)        
        response_validator_decision = response_validator.validate_response(dm)

        # Actualice los valores de:
        #   current_consecutive_superior_time_response_count_per_dl
        #   current_consecutive_inferior_time_response_count_per_dl
        # dependiendo de la calidad de la respuesta alcanzada, para el nivel de dificultad actual.
        if (response_validator_decision.get_correctness() == True):
            print('Correcto')            
            if(response_validator_decision.get_correct_response_time() == response_validator_decision.
                SUPERIOR_CORRECT_RESPONSE_TIME):
                print('Tiempo de respuesta correcta: Superior al esperado (<=', 
                str(max_superior_cr_times_per_difficulty[exercise_dl_index]) + ')')
                current_consecutive_superior_time_response_count_per_dl[exercise_dl_index] += 1
                current_consecutive_inferior_time_response_count_per_dl[exercise_dl_index] = 0
            elif(response_validator_decision.get_correct_response_time() == response_validator_decision.
                INFERIOR_CORRECT_RESPONSE_TIME):
                print('Tiempo de respuesta correcta: Inferior al esperado (>', 
                str(min_inferior_cr_times_per_difficulty[exercise_dl_index]) + ')')
                current_consecutive_inferior_time_response_count_per_dl[exercise_dl_index] += 1
                current_consecutive_superior_time_response_count_per_dl[exercise_dl_index] = 0
            else:
                print('Tiempo de respuesta correcta: Esperado (> ', 
                max_superior_cr_times_per_difficulty[exercise_dl_index], 'y <= ', 
                str(min_inferior_cr_times_per_difficulty[exercise_dl_index]) + ')')
                current_consecutive_superior_time_response_count_per_dl[exercise_dl_index] = 0
                current_consecutive_inferior_time_response_count_per_dl[exercise_dl_index] = 0
            print('El tiempo de respuesta correcta del ejercicio fue de:', exercise_response_time_in_seconds, "segundos.")
            print('El número total de intentos realizados en este ejercicio fue de:', same_exercise_attempts, "intento(s).")
        else:
            print('Incorrecto')
            print('El número total de intentos realizados en este ejercicio es de:', 
                same_exercise_attempts, "intento(s).")

        dm.set_current_state(response_validator_decision.get_next_difficulty())
        same_exercise_flag = response_validator_decision.get_same_exercise()

        # TESTING 1: Imprima los valores de los contadores de intentos consecutivos
        print('-----------------')
        print('TESTING 1:')
        print('Número de respuestas correctas consecutivas de tiempo superior al esperado :' 
        , str(current_consecutive_superior_time_response_count_per_dl[exercise_dl_index]))
        print('Número de respuestas correctas consecutivas de tiempo inferior al esperado :' 
        , str(current_consecutive_inferior_time_response_count_per_dl[exercise_dl_index]))

        # TESTING 2: Imprima los valores del modelo WBKT:
        print('-----------------')
        print('TESTING 2:')
        print('Estado actual del modelo WBKT de la dificultad ' + str(exercise_dl_index + 1) + ':')
        print('t = ', dl_wbkt_model.get_t())
        print('p(Lt) = ', dl_wbkt_model.get_p_lt(), ' | p(T) =', dl_wbkt_model.get_p_t(), 
        ' | p(G) =', dl_wbkt_model.get_p_g(), ' | p(S) =', dl_wbkt_model.get_p_s())
        # print('w(L0) =', dl_wbkt_model.get_w_l0())
        # print('w(T) =', dl_wbkt_model.get_w_t())
        print('w(G) =', dl_wbkt_model.get_w_g())
        # print('w(S) =', dl_wbkt_model.get_w_s())

        print()

    except ValueError:
        print('El formato de la respuesta no es el adecuado. Por favor ingrese un número para responder el ejercicio.')
        print()
        same_exercise_flag = True
        # is_valid_response_flag = False