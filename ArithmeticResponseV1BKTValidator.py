import ArithmeticExercise
import DifficultyMachine
import ResponseValidatorDecision
import BKT as bkt

# Clase de validador de respuesta de ejercicios aritméticos
class ArithmeticResponseValidator:

    MIN_PRIOR_LEARNED_PROBABILITY_FOR_MASTERY = 0.95 # OK
    MIN_PRIOR_LEARNED_PROBABILITY_FOR_REVIEW = 0.35
    MAX_ATTEMPTS_PER_EXERCISE = 2

    # Constructor (Vacío o no vacío)
    def __init__(self, exercise:ArithmeticExercise.ArithmeticExercise, user_response:int, skill_bkt_model:bkt.BKT):
        self.__exercise = exercise
        self.__user_response = user_response
        self.__skill_bkt_model = skill_bkt_model
    
    # Getters
    def get_exercise(self):
        return self.__exercise

    def get_user_response(self):
        return self.__user_response

    def get_skill_bkt_model(self):
        return self.__skill_bkt_model

    # Setters
    def set_exercise(self, exercise):
        self.__exercise = exercise

    def set_user_response(self, user_response):
        self.__user_response = user_response

    def set_skill_bkt_model(self, skill_bkt_model):
        self.__skill_bkt_model = skill_bkt_model

    # Validador y tomador de decisiones frente a una respuesta del usuario y 
    #   la probabilidad estimada de dominio a priori de la habilidad
    def validate_response(self, dm:DifficultyMachine.DifficultyMachine):
        # Considere si la respuesta del usuario fue correcta o no
        correctness = self.get_user_response() == self.get_exercise().get_correct_response()
        # Almacene el valor de p(L), t=n-1
        prior_learning_probability = self.__skill_bkt_model.get_p_lt()
        # Actualice el valor de p(L), según el nuevo valor t=n, y dependiendo de si la respuesta fue correcta o no
        if correctness == True:
            self.__skill_bkt_model.update_model(observation=True)
        else:
            self.__skill_bkt_model.update_model(observation=False)
        # Almacene el nuevo valor de p(L), t=n
        updated_prior_learning_probability = self.__skill_bkt_model.get_p_lt()

        # Dependiendo del nuevo valor de p(L, t=n), y de si este valor aumentó o no con respecto al valor p(L, t=n-1),
        #   decida si se mostrará un nuevo ejercicio en una dificultad superior o inferior, o, si la dificultad es la misma,
        #   decida si se mostrará el mismo ejercicio u otro ejercicio.
        is_prior_learning_probability_not_decreased = False
        if (updated_prior_learning_probability >= prior_learning_probability):
            is_prior_learning_probability_not_decreased = True

        if (updated_prior_learning_probability >= self.MIN_PRIOR_LEARNED_PROBABILITY_FOR_MASTERY
            and is_prior_learning_probability_not_decreased == True):
            # Aumente el nivel de dificultad
            return ResponseValidatorDecision.ResponseValidatorDecision(correctness, 
                dm.get_superior_difficulty(), False)

        elif (updated_prior_learning_probability < self.MIN_PRIOR_LEARNED_PROBABILITY_FOR_REVIEW
            and is_prior_learning_probability_not_decreased == False):
            # Disminuya el nivel de dificultad
            return ResponseValidatorDecision.ResponseValidatorDecision(correctness, 
                dm.get_inferior_difficulty(), False)

        else:
            # Mantenga el nivel de dificultad
            # Si la respuesta al ejercicio es correcta, cambie de ejercicio
            if (correctness == True):
                return ResponseValidatorDecision.ResponseValidatorDecision(correctness, 
                    dm.get_current_state(), False)
            else:
                # Si la respuesta al ejercicio es incorrecta, mantenga el mismo ejercicio
                # Aunque el ejercicio debería cambiar, dependiendo de otros parámetros como el número de intentos fallidos.
                return ResponseValidatorDecision.ResponseValidatorDecision(correctness, 
                    self.__exercise.get_difficulty(), True)