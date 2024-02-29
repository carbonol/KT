import ArithmeticExerciseGenerator
import DifficultyMachine
import ArithmeticResponseV3Validator
import Timer

#### Sistema de aprendizaje por dominio mediante la práctica de ejercicios aritméticos
# Versión 3
# Además de considerar si la respuesta dada por el usuario es correcta o no, también se considera el 
#   tiempo de respuesta del usuario frente al ejercicio y el número de intentos fallidos

#### Niveles de dificultad en el sistema
# Se considerarán 7 niveles de dificultad en el sistema
difficulty_numbers = []
for i in range(1, 8):
    difficulty_numbers.append(i)

# Se considerará un tiempo máximo de respuesta correcta para ejercicios en cada uno de los niveles de dificultad definidos
max_exercise_correct_answer_times_per_difficulty = [2.1, 5.2, 6.0, 9.3, 13.0, 6.8, 22.0]

# Se considerará un número máximo de intentos para ejercicios en cada uno de los niveles de dificultad definidos
max_exercise_attempts_per_difficulty = [1, 1, 1, 2, 2, 2, 2]

# Cada nivel de dificultad tiene asociado un tiempo máximo de respuesta correcta para ejercicios de ese nivel de dificultad y
#   un número máximo de intentos para ejercicios de ese nivel de dificultad
# Se considerarán 7 niveles de dificultad en el sistema
difficulty_levels = []
for i in range(0, 7):
    difficulty_levels.append(DifficultyMachine.Difficulty.Difficulty(i + 1, 
        max_exercise_correct_answer_times_per_difficulty[i], max_exercise_attempts_per_difficulty[i]))

dm = DifficultyMachine.DifficultyMachine(difficulty_levels)
# print(dm.get_difficulty_levels())
# print(dm.get_difficulty_level_tags())
# print(dm.get_current_state())

same_exercise_flag = False
timer = Timer.Timer()

exercise_number = 0
exercise = None

exercise_attempts = 0

while (not dm.is_on_end_state()):
    # print(dm.get_current_state_tag())
    if (dm.is_on_start_state()):
        dm.increase_difficulty()
        continue

    # Si el ejercicio a mostrar al estudiante NO es el mismo
    if same_exercise_flag == False:
        exercise = ArithmeticExerciseGenerator.ArithmeticExerciseGenerator().generate_exercise(dm.get_current_state())
        exercise_number += 1

        if exercise_number == 1:
            print('---- Ejercicios Aritméticos ----')

        exercise_attempts = 0

    print('-- Ejercicio # ' + str(exercise_number) + ' --')
    print('Escriba la respuesta para el siguiente ejercicio: ')
    print(exercise.get_description())

    # En este punto, se asume que el usuario puede comenzar a identificar el ejercicio
    # Si el ejercicio a mostrar al estudiante NO es el mismo
    if same_exercise_flag == False:
        timer.start_new_timer()

    response = input('>> ')

    # En este punto, ya se ha recibido una respuesta al ejercicio por parte del usuario
    exercise_response_time_in_seconds = timer.get_elapsed_time_in_seconds()

    try:
        response = int(response)

        # Aquí ya se ha enviado una respuesta válida por parte del usuario; registre un intento más para el ejercicio.
        exercise_attempts += 1

        response_validator = ArithmeticResponseV3Validator.ArithmeticResponseValidator(exercise, response, 
            exercise_response_time_in_seconds, exercise_attempts)
        response_validator_decision = response_validator.validate_response(dm)
        if (response_validator_decision.get_correctness() == True):
            print('Correcto')
            print('El tiempo de respuesta correcta del ejercicio fue de:', exercise_response_time_in_seconds, "segundos.")
            print('El número total de respuestas enviadas en este ejercicio fue de:', exercise_attempts, "intento(s).")
        else:
            print('Incorrecto')
            print('El número total de respuestas enviadas hasta ahora en este ejercicio es de:', 
                exercise_attempts, "intento(s).")

        dm.set_current_state(response_validator_decision.get_next_difficulty())
        same_exercise_flag = response_validator_decision.get_same_exercise()

        print()

    except ValueError:
        print('El formato de la respuesta no es el adecuado. Por favor ingrese un número para responder el ejercicio.')
        print()
        same_exercise_flag = True   