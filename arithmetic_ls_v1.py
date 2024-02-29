import ArithmeticExerciseGenerator
import DifficultyMachine
import ArithmeticResponseV1Validator

# Sistema de aprendizaje por dominio mediante la práctica de ejercicios aritméticos
# Versión 1
# Sólo se considera si la respuesta dada por el usuario es correcta o no

# Niveles de dificultad en el sistema
# Se considerarán 7 niveles de dificultad
difficulty_levels = []
for i in range(1, 8):
    difficulty_levels.append(DifficultyMachine.Difficulty.Difficulty(i))

same_exercise_flag = False

dm = DifficultyMachine.DifficultyMachine(difficulty_levels)
# print(dm.get_difficulty_levels())
# print(dm.get_difficulty_level_tags())
# print(dm.get_current_state())

exercise_number = 0
exercise = None

while (not dm.is_on_end_state()):
    # print(dm.get_current_state_tag())
    if (dm.is_on_start_state()):
        dm.increase_difficulty()
        continue

    if same_exercise_flag == False:
        exercise = ArithmeticExerciseGenerator.ArithmeticExerciseGenerator().generate_exercise(dm.get_current_state())
        exercise_number += 1

        if exercise_number == 1:
            print('---- Ejercicios Aritméticos ----')

    print('-- Ejercicio # ' + str(exercise_number) + ' --')
    print('Escriba la respuesta para el siguiente ejercicio: ')
    print(exercise.get_description())
    response = input('>> ')
    try:
        response = int(response)
        response_validator = ArithmeticResponseV1Validator.ArithmeticResponseValidator(exercise, response)
        response_validator_decision = response_validator.validate_response(dm)
        if (response_validator_decision.get_correctness() == True):
            print('Correcto')
        else:
            print('Incorrecto')

        dm.set_current_state(response_validator_decision.get_next_difficulty())
        same_exercise_flag = response_validator_decision.get_same_exercise()

        print()

    except ValueError:
        print('El formato de la respuesta no es el adecuado. Por favor ingrese un número para responder el ejercicio.')
        print()
        same_exercise_flag = True   