import ArithmeticExercise
import DifficultyMachineV2
import ResponseValidatorDecisionV2
import WBKT as wbkt

def find_current_WBKT_weight_increment_factor(current_WBKT_parameter_weight):
    if (current_WBKT_parameter_weight > 1.0):
        return int(round((current_WBKT_parameter_weight - 1.0) / 0.2, 2))
    elif (current_WBKT_parameter_weight < 1.0):
        return int(round((1.0 - current_WBKT_parameter_weight) * -10.0, 2))
    else:
        return 0

def find_WBKT_weight_from_increment_factor(WBKT_weight_increment_factor):
    if (WBKT_weight_increment_factor > 5):
        WBKT_weight_increment_factor = 5
    elif (WBKT_weight_increment_factor < -5):
        WBKT_weight_increment_factor = -5

    if (WBKT_weight_increment_factor > 0):
        return (WBKT_weight_increment_factor * 0.2) + 1.0
    elif (WBKT_weight_increment_factor < 0):
        return -((WBKT_weight_increment_factor / -10.0) - 1.0)
    else:
        return 1.0

def calculate_new_WBKT_parameter_weight(current_WBKT_parameter_weight, weight_increment_factor_to_add):
    cwwif = find_current_WBKT_weight_increment_factor(current_WBKT_parameter_weight)
    return find_WBKT_weight_from_increment_factor(cwwif + weight_increment_factor_to_add)

# Clase de validador de respuesta de ejercicios aritméticos
class ArithmeticResponseValidator:
    
    MIN_LEARNED_PROBABILITY_FOR_MASTERY_CRITERIA = 0.95 # OK
    
    # Parametrización dinámica
    # Parámetros para la búsqueda del valor de p(L) a partir del cual el valor posteriori de p(L) no decrece con
    #   respuestas incorrectas sucesivas => Esto se realiza para hallar el criterio mínimo de p(L) para que el estudiante
    #   o usuario aplique a un refuerzo (nivel de dificultad - 1) si este responde incorrectamente.
    P_L_MAX = 0.99
    MAX_ITERATIONS = 1100
    P_L_PRECISION = 4

    INCREASE_DIFFICULTY = 0
    MAINTAIN_DIFFICULTY = 1
    DECREASE_DIFFICULTY = 2

    SAME_EXERCISE = True
    DIFFERENT_EXERCISE = False

    # Parametrización estática
    # MIN_LEARNED_PROBABILITY_FOR_REVIEW_CRITERIA = 0.2557174101125822

    # Constructor (Vacío o no vacío)
    def __init__(self, exercise:ArithmeticExercise.ArithmeticExercise, user_response:int, 
        user_response_time: float, user_response_attempts: int, skill_wbkt_model:wbkt.WBKT,
        current_consecutive_superior_time_response_count: int, 
        current_consecutive_inferior_time_response_count: int):
        self.__exercise = exercise
        self.__user_response = user_response
        # user_response_time: Tiempo que le tomó al usuario responder correctamente un ejercicio.
        self.__user_response_time = user_response_time
        # user_response_attempts = Número de intentos que ha hecho el usuario en un mismo ejercicio.
        self.__user_response_attempts = user_response_attempts
        self.__skill_wbkt_model = skill_wbkt_model
        self.__current_consecutive_superior_time_response_count = current_consecutive_superior_time_response_count
        self.__current_consecutive_inferior_time_response_count = current_consecutive_inferior_time_response_count
    
    # Getters
    def get_exercise(self):
        return self.__exercise

    def get_user_response(self):
        return self.__user_response

    def get_user_response_time(self):
        return self.__user_response_time

    def get_user_response_attempts(self):
        return self.__user_response_attempts

    def get_skill_wbkt_model(self):
        return self.__skill_wbkt_model

    def get_current_consecutive_superior_time_response_count(self):
        return self.__current_consecutive_superior_time_response_count

    def get_current_consecutive_inferior_time_response_count(self):
        return self.__current_consecutive_inferior_time_response_count

    # Setters
    def set_exercise(self, exercise):
        self.__exercise = exercise

    def set_user_response(self, user_response):
        self.__user_response = user_response

    def set_user_response_time(self, user_response_time):
        self.__user_response_time = user_response_time

    def set_user_response_attempts(self, user_response_attempts):
        self.__user_response_attempts = user_response_attempts

    def set_skill_wbkt_model(self, skill_wbkt_model):
        self.__skill_wbkt_model = skill_wbkt_model

    def set_current_consecutive_superior_time_response_count(self, current_consecutive_superior_time_response_count):
        self.__current_consecutive_superior_time_response_count = current_consecutive_superior_time_response_count

    def set_current_consecutive_inferior_time_response_count(self, current_consecutive_inferior_time_response_count):
        self.__current_consecutive_inferior_time_response_count = current_consecutive_inferior_time_response_count

    # Validador y tomador de decisiones frente a una respuesta del usuario con sus características 
    # (en este caso, qué tan rápido o lento respondió correctamente) y la probabilidad estimada de dominio 
    # a posteriori de la habilidad
    def validate_response(self, dm:DifficultyMachineV2.DifficultyMachine):
        # Considere si la respuesta del usuario fue correcta o no
        correctness = self.get_user_response() == self.get_exercise().get_correct_response()

        ## Factores adicionales de la respuesta del usuario a revisar
        is_correct_response_time_superior = None
        is_correct_response_time_inferior = None
        ccstrc = 0
        ccitrc = 0

        correct_response_time = None
        # Si la respuesta es correcta:
        if (correctness):
            # 1) Considere si la respuesta correcto del usuario se produjo en un periodo de tiempo esperado,
            #    o en un tiempo mayor o menor al esperado en la dificultad.
            is_correct_response_time_superior = self.get_user_response_time() <= dm.get_current_state(            
                ).get_max_superior_correct_response_time() # Recuerde que este tiempo es inclusivo
            
            is_correct_response_time_inferior = self.get_user_response_time() > dm.get_current_state(            
                ).get_min_inferior_correct_response_time() # Recuerde que este tiempo NO es inclusivo

            # Si la respuesta es correcta y es realizada en un tiempo menor al esperado en la dificultad:
            if (is_correct_response_time_superior):
                # 2a) Considere cuál es el número de intentos correctos y con un tiempo menor al esperado que ha sido
                #   logrado de forma consecutiva que incluye a este último intento correcto con un tiempo superior
                #   al esperado.
                ccstrc = self.__current_consecutive_superior_time_response_count + 1
                correct_response_time = ResponseValidatorDecisionV2.ResponseValidatorDecision.SUPERIOR_CORRECT_RESPONSE_TIME
            # Si la respuesta es correcta y es realizada en un tiempo menor al esperado en la dificultad:
            elif (is_correct_response_time_inferior):
                # 2b) Considere cuál es el número de intentos correctos y con un tiempo mayor al esperado que ha sido
                #   logrado de forma consecutiva que incluye a este último intento correcto con un tiempo inferior
                #   al esperado.
                ccitrc = self.__current_consecutive_inferior_time_response_count + 1
                correct_response_time = ResponseValidatorDecisionV2.ResponseValidatorDecision.INFERIOR_CORRECT_RESPONSE_TIME
            else:
                correct_response_time = ResponseValidatorDecisionV2.ResponseValidatorDecision.EXPECTED_CORRECT_RESPONSE_TIME

        # Estime el cambio al peso w(G) dependiendo de la calidad de la respuesta del usuario
        w_g_incr_factor = 0 # Este factor de incremento es el que determinará al final cuál será el cambio en el peso w(G),
        #   el cual puede ser un incremento, decremento, o ningún cambio.
        if (is_correct_response_time_superior):
            w_g_incr_factor -= ccstrc
        elif (is_correct_response_time_inferior):
            w_g_incr_factor += ccitrc
        else:
            w_g_incr_factor = 0

        # Halle el nuevo peso w(G) a asignar al modelo WBKT relevante
        new_w_g = calculate_new_WBKT_parameter_weight(self.__skill_wbkt_model.get_w_g(), w_g_incr_factor)

        # Actualice el modelo WBKT asignando el nuevo valor de w(G):
        self.__skill_wbkt_model.set_w_g(new_w_g)

        # Almacene el valor de p(L), t=n-1
        prior_learned_probability = self.__skill_wbkt_model.get_p_lt()
        # Actualice el valor a posteriori de p(L), según el nuevo valor t=n, 
        #   y dependiendo de si la respuesta fue correcta o no
        if correctness == True:
            self.__skill_wbkt_model.update_model(observation=True)
        else:
            self.__skill_wbkt_model.update_model(observation=False)
        # Almacene el nuevo valor de p(L), t=n
        posterior_learned_probability = self.__skill_wbkt_model.get_p_lt()

        p_lt_is_within_learned_criteria = posterior_learned_probability >= self.MIN_LEARNED_PROBABILITY_FOR_MASTERY_CRITERIA
        p_lt_did_not_decrease = posterior_learned_probability >= prior_learned_probability

        # Calcular dinámicamente el criterio para disminuir el nivel de dificultad:
        review_criteria = self.__skill_wbkt_model.find_pl_boundary_where_pl_cannot_decrease_with_wrong_answers(
            p_l_max=self.P_L_MAX, max_iterations=self.MAX_ITERATIONS, p_l_precision=self.P_L_PRECISION)
        
        # p_lt_is_within_review_criteria = posterior_learned_probability >= self.MIN_LEARNED_PROBABILITY_FOR_REVIEW_CRITERIA
        # REVISAR ESTO:
        # p_lt_is_within_review_criteria = posterior_learned_probability >= review_criteria
        p_lt_is_within_review_criteria = posterior_learned_probability <= review_criteria        
        p_lt_did_not_increase = posterior_learned_probability <= prior_learned_probability

        max_response_attempts_reached = self.get_user_response_attempts() >= dm.get_current_state(
            ).get_max_exercise_attempts_per_exercise()
        
        difficulty_verdict = None
        next_difficulty = None
        exercise_change_verdict = None
        # Decisión 1: Elección del nivel de dificultad para el próximo ejercicio
        if (p_lt_is_within_learned_criteria and p_lt_did_not_decrease):
            # Aumente el nivel de dificultad
            difficulty_verdict = self.INCREASE_DIFFICULTY
            next_difficulty = dm.get_superior_difficulty()
        elif (p_lt_is_within_review_criteria and p_lt_did_not_increase and max_response_attempts_reached):
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
            correctness, next_difficulty, exercise_change_verdict, correct_response_time)