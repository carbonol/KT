import ArithmeticExerciseGenerator
import DifficultyMachine
import ArithmeticResponseV1PFAValidator
import PFA as pfa

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

#### Integración del PFA con el programa de ejercicios de sumas (V1)
# En este caso, cada nivel de dificultad se considerá una habilidad o componente de conocimiento j según el modelo PFA.
# Todas las habilidades del modelo PFA comparten el mismo modelo.

# Definición de parámetros del modelo PFA
kc_count = 7 # Número de habilidades

beta = []
beta_j = -1.0

gamma = []
gamma_j = 1.5

rho = []
rho_j = -1.5

for j in range(kc_count): # Por cada habilidad, haga lo siguiente:
    beta.append(beta_j)
    beta_j -= 1.0
    gamma.append(gamma_j)
    rho.append(rho_j)
    if (j == 2):
        rho_j = -0.75

# Creación del modelo PFA con base en los parámetros definidos anteriormente
#   (Esto aplica para 1 estudiante y un número kc_count de habilidades o componentes de conocimiento evaluables)
pfa_model = pfa.PFA(kc_count, beta, gamma, rho)

exercise_number = 0
exercise = None

while (not dm.is_on_end_state()):
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

        # Obtenga la(s) habilidad(es) involucradas en el ítem o ejercicio
        #   (Dependiendo del nivel de dificultad del ejercicio - En este caso siempre se involucrará solo 1 habilidad j)
        j = exercise.get_difficulty().get_difficulty_level() - 1

        # En la integración con PFA, es importante cambiar un poco los criterios de toma de decisiones frente a 
        #   cuándo se cambiará la dificultad de los ejercicios, y cuándo se seguirá mostrando o no un ejercicio de una misma 
        #   dificultad.
        # En este caso, se debe actualizar el modelo PFA (i.e., actualizar los valores m y p(m), 
        #   y revisar el valor a posteriori de p(m) para tomar una decisión al respecto.
        response_validator = ArithmeticResponseV1PFAValidator.ArithmeticResponseValidator(exercise, 
            response, pfa_model, j)
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