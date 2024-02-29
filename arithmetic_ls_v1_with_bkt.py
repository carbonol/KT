import ArithmeticExerciseGenerator
import DifficultyMachine
import ArithmeticResponseV1BKTValidator
import BKT as bkt

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

#### Implementación del BKT
# En este caso, cada nivel de dificultad se considerá una habilidad según el modelo BKT.
# Es decir, cada nivel de dificultad tendrá su propio modelo BKT.
## No obstante:
# Por simplicidad, asumamos esta vez que cada nivel de dificultad tendrá los mismos parámetros de BKT.
bkt_models = []
for i in range(1, 8):
    # bkt_models.append(bkt.BKT(p_l0=0.02, p_t=0.01, p_g=0.3, p_s=0.01))
    bkt_models.append(bkt.BKT(p_l0=0.02, p_t=0.05, p_g=0.3, p_s=0.01))

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
        # En este momento ya se cuenta con una respuesta o interacción válida por parte del usuario.

        # Obtenga el modelo BKT correcto a considerar (dependiendo del nivel de dificultad del ejercicio)
        exercise_difficulty_level_index = exercise.get_difficulty().get_difficulty_level() - 1
        difficulty_skill_bkt_model = bkt_models[exercise_difficulty_level_index]

        # En la implementación de BKT, es importante cambiar los criterios de toma de decisiones frente a cuándo se cambiará
        #   la dificultad de los ejercicios.
        # En este caso, se debe actualizar el modelo BKT (i.e., actualizar el valor p(L,t)), y revisar el valor de p(L,t) para
        #   tomar una decisión al respecto.
        response_validator = ArithmeticResponseV1BKTValidator.ArithmeticResponseValidator(exercise, 
            response, difficulty_skill_bkt_model)
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