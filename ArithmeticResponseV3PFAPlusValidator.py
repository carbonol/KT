import ArithmeticExercise
import DifficultyMachineV2
import ResponseValidatorDecisionV2
import PFAPlus as pfa_plus

# Clase de validador de respuesta de ejercicios aritméticos
class ArithmeticResponseValidator:
    
    MIN_POSTERIOR_PROBABILITY_FOR_MASTERY = 0.95 # OK
    MAX_POSTERIOR_PROBABILITY_FOR_REVIEW = 0.25

    INCREASE_DIFFICULTY = 0
    MAINTAIN_DIFFICULTY = 1
    DECREASE_DIFFICULTY = 2

    SAME_EXERCISE = True
    DIFFERENT_EXERCISE = False

    # Constructor (Vacío o no vacío)
    def __init__(self, exercise:ArithmeticExercise.ArithmeticExercise, user_response:int, 
        user_response_time: float, user_response_attempts: int, pfa_plus_model:pfa_plus.PFAPlus, j:int):
        self.__exercise = exercise
        self.__user_response = user_response
        # user_response_time: Tiempo que le tomó al usuario responder correctamente un ejercicio.
        self.__user_response_time = user_response_time
        # user_response_attempts = Número de intentos que ha hecho el usuario en un mismo ejercicio.
        self.__user_response_attempts = user_response_attempts
        self.__pfa_plus_model = pfa_plus_model
        self.__j = j
    
    # Getters
    def get_exercise(self):
        return self.__exercise

    def get_user_response(self):
        return self.__user_response

    def get_user_response_time(self):
        return self.__user_response_time

    def get_user_response_attempts(self):
        return self.__user_response_attempts

    def get_pfa_plus_model(self):
        return self.__pfa_plus_model

    def get_j(self):
        return self.__j

    # Setters
    def set_exercise(self, exercise):
        self.__exercise = exercise

    def set_user_response(self, user_response):
        self.__user_response = user_response

    def set_user_response_time(self, user_response_time):
        self.__user_response_time = user_response_time

    def set_user_response_attempts(self, user_response_attempts):
        self.__user_response_attempts = user_response_attempts

    def set_pfa_plus_model(self, pfa_plus_model):
        self.__pfa_plus_model = pfa_plus_model

    def set_j(self, j):
        self.__j = j

    # Validador y tomador de decisiones frente a una respuesta del usuario con sus características 
    # (en este caso, qué tan rápido o lento respondió correctamente) y la probabilidad estimada de dominio 
    # a posteriori de la habilidad
    def validate_response(self, dm:DifficultyMachineV2.DifficultyMachine):

        # Considere si la respuesta del usuario fue correcta o no
        correctness = self.get_user_response() == self.get_exercise().get_correct_response()

        ## Factores adicionales de la respuesta del usuario a revisar
        is_correct_response_time_superior = None
        is_correct_response_time_inferior = None

        correct_response_time_quality = None

        kcs_success_status = None

        # Si la respuesta es correcta:
        if (correctness):
            # 1) Considere si la respuesta correcta del usuario se produjo en un periodo de tiempo esperado,
            #    o en un tiempo mayor o menor al esperado en la dificultad.
            is_correct_response_time_superior = self.get_user_response_time() <= dm.get_current_state(            
                ).get_max_superior_correct_response_time() # Recuerde que este tiempo es inclusivo
            
            is_correct_response_time_inferior = self.get_user_response_time() > dm.get_current_state(            
                ).get_min_inferior_correct_response_time() # Recuerde que este tiempo NO es inclusivo

            # Si la respuesta es correcta y es realizada en un tiempo menor al esperado en la dificultad:
            if (is_correct_response_time_superior):                
                correct_response_time_quality = ResponseValidatorDecisionV2.ResponseValidatorDecision.SUPERIOR_CORRECT_RESPONSE_TIME
                kcs_success_status = pfa_plus.PFAPlus.CORRECT_FAST_OUTCOME
            # Si la respuesta es correcta y es realizada en un tiempo menor al esperado en la dificultad:
            elif (is_correct_response_time_inferior):                
                correct_response_time_quality = ResponseValidatorDecisionV2.ResponseValidatorDecision.INFERIOR_CORRECT_RESPONSE_TIME
                kcs_success_status = pfa_plus.PFAPlus.CORRECT_SLOW_OUTCOME
            # Si la respuesta es correcta y es realizada en un rango de tiempo esperado en la dificultad:
            else:
                correct_response_time_quality = ResponseValidatorDecisionV2.ResponseValidatorDecision.EXPECTED_CORRECT_RESPONSE_TIME
                kcs_success_status = pfa_plus.PFAPlus.CORRECT_OUTCOME
        else:
            kcs_success_status = pfa_plus.PFAPlus.INCORRECT_OUTCOME

        # Actualice el modelo PFA, de acuerdo a si la respuesta del usuario fue correcta o no, y a si la
        #   respuesta, en caso de ser correcta, fue lo suficientemente rápida o no.
        implied_kcs = [self.get_j() + 1]        
        kcs_success_statuses = [kcs_success_status]
        self.get_pfa_plus_model().update_model(implied_kcs, kcs_success_statuses)

        # Obtenga el valor a posteriori de p(m)
        p_m = self.get_pfa_plus_model().get_p_m()[self.get_j()]

        p_m_is_within_learned_criteria = p_m >= self.MIN_POSTERIOR_PROBABILITY_FOR_MASTERY
        # p_m_did_not_decrease = p_m >= prior_learned_probability

        p_m_is_within_review_criteria = p_m <= self.MAX_POSTERIOR_PROBABILITY_FOR_REVIEW
        # p_m_did_not_increase = p_m <= prior_learned_probability

        max_response_attempts_reached = self.get_user_response_attempts() >= dm.get_current_state(
            ).get_max_exercise_attempts_per_exercise()
        
        difficulty_verdict = None
        next_difficulty = None
        exercise_change_verdict = None
        # Decisión 1: Elección del nivel de dificultad para el próximo ejercicio
        if (p_m_is_within_learned_criteria and correctness == True):
            # Aumente el nivel de dificultad
            difficulty_verdict = self.INCREASE_DIFFICULTY
            next_difficulty = dm.get_superior_difficulty()
        elif (p_m_is_within_review_criteria and correctness == False and max_response_attempts_reached):
            # Disminuya el nivel de dificultad
            difficulty_verdict = self.DECREASE_DIFFICULTY
            next_difficulty = dm.get_inferior_difficulty()
        else:
            difficulty_verdict = self.MAINTAIN_DIFFICULTY
            next_difficulty = dm.get_current_state()

        # Decisión 2: Elección del siguiente ejercicio a mostrar al estudiante
        if (difficulty_verdict == self.INCREASE_DIFFICULTY or difficulty_verdict == self.DECREASE_DIFFICULTY):
            exercise_change_verdict = self.DIFFERENT_EXERCISE
        elif (correctness):
            exercise_change_verdict = self.DIFFERENT_EXERCISE
        elif (not max_response_attempts_reached):
            exercise_change_verdict = self.SAME_EXERCISE
        else:
            exercise_change_verdict = self.DIFFERENT_EXERCISE

        return ResponseValidatorDecisionV2.ResponseValidatorDecision(
            correctness, next_difficulty, exercise_change_verdict, correct_response_time_quality)