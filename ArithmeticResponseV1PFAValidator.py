import ArithmeticExercise
import DifficultyMachine
import ResponseValidatorDecision
import PFA as pfa

# Clase de validador de respuesta de ejercicios aritméticos
class ArithmeticResponseValidator:

    MIN_POSTERIOR_PROBABILITY_FOR_MASTERY = 0.95 # OK
    MAX_POSTERIOR_PROBABILITY_FOR_REVIEW = 0.25

    # Constructor (Vacío o no vacío)
    def __init__(self, exercise:ArithmeticExercise.ArithmeticExercise, user_response:int, pfa_model:pfa.PFA, j:int):
        self.__exercise = exercise
        self.__user_response = user_response
        self.__pfa_model = pfa_model
        self.__j = j
    
    # Getters
    def get_exercise(self):
        return self.__exercise

    def get_user_response(self):
        return self.__user_response

    def get_pfa_model(self):
        return self.__pfa_model

    def get_j(self):
        return self.__j

    # Setters
    def set_exercise(self, exercise):
        self.__exercise = exercise

    def set_user_response(self, user_response):
        self.__user_response = user_response

    def set_pfa_model(self, pfa_model):
        self.__pfa_model = pfa_model

    def set_j(self, j):
        self.__j = j

    # Validador y tomador de decisiones frente a una respuesta del usuario y 
    #   la probabilidad estimada de dominio a posteriori de la habilidad j
    def validate_response(self, dm:DifficultyMachine.DifficultyMachine):

        # Considere si la respuesta del usuario fue correcta o no
        correctness = self.get_user_response() == self.get_exercise().get_correct_response()
        # Actualice el modelo PFA, de acuerdo a si la respuesta del usuario fue correcta o no.
        implied_kcs = [self.get_j() + 1]
        kcs_correctness = [correctness]
        self.get_pfa_model().update_model(implied_kcs, kcs_correctness)

        # Obtenga el valor a posteriori de p(m)
        p_m = self.get_pfa_model().get_p_m()[self.get_j()]

        # Dependiendo de si la respuesta del usuario fue correcta o no, y de la probabilidad de respuesta correcta
        #   a posteriori de un ítem que involucra la habilidad j, decida si se mostrará un nuevo ejercicio en una 
        #   dificultad superior o inferior, o, si la dificultad es la misma,
        #   decida si se mostrará el mismo ejercicio u otro ejercicio.

        if (p_m >= self.MIN_POSTERIOR_PROBABILITY_FOR_MASTERY and correctness == True):
            # Aumente el nivel de dificultad
            return ResponseValidatorDecision.ResponseValidatorDecision(correctness, 
                dm.get_superior_difficulty(), False)

        elif (p_m <= self.MAX_POSTERIOR_PROBABILITY_FOR_REVIEW and correctness == False):
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