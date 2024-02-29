import ArithmeticExercise
import DifficultyMachine
import ResponseValidatorDecision

# Clase de validador de respuesta de ejercicios aritméticos
class ArithmeticResponseValidator:
    # Constructor (Vacío o no vacío)
    def __init__(self, exercise:ArithmeticExercise.ArithmeticExercise, user_response:int, 
        user_response_time: float, user_response_attempts: int):
        self.__exercise = exercise
        self.__user_response = user_response
        self.__user_response_time = user_response_time
        self.__user_response_attempts = user_response_attempts
    
    # Getters
    def get_exercise(self):
        return self.__exercise

    def get_user_response(self):
        return self.__user_response

    def get_user_response_time(self):
        return self.__user_response_time

    def get_user_response_attempts(self):
        return self.__user_response_attempts

    # Setters
    def set_exercise(self, exercise):
        self.__exercise = exercise

    def set_user_response(self, user_response):
        self.__user_response = user_response

    def set_user_response_time(self, user_response_time):
        self.__user_response_time = user_response_time

    def set_user_response_attempts(self, user_response_attempts):
        self.__user_response_attempts, user_response_attempts

    # Validador y tomador de decisiones frente a una respuesta del usuario
    def validate_response(self, dm:DifficultyMachine.DifficultyMachine):
        # Respuesta correcta
        if self.get_user_response() == self.get_exercise().get_correct_response():
            # Tiempo de respuesta adecuado según la dificultad del ejercicio
            if self.get_user_response_time() <= dm.get_current_state().get_max_exercise_correct_answer_time():
                # Muestre otro ejercicio de una dificultad superior
                return ResponseValidatorDecision.ResponseValidatorDecision(True, 
                    dm.get_superior_difficulty(), False)
            # Tiempo de respuesta excesivo según la dificultad del ejercicio
            else:
                # Muestre otro ejercicio de la misma dificultad
                return ResponseValidatorDecision.ResponseValidatorDecision(True, 
                    self.__exercise.get_difficulty(), False)
        # Respuesta incorrecta
        else:
            # El número de intentos excede el límite establecido para la dificultad
            if self.get_user_response_attempts() >= dm.get_current_state().get_max_exercise_attempts():
                # Muestre otro ejercicio de una dificultad inferior
                return ResponseValidatorDecision.ResponseValidatorDecision(False, 
                    dm.get_inferior_difficulty(), False)
            # El número de intentos aún no excede el límite establecido para la dificultad
            else:
                # Muestre el mismo ejercicio
                return ResponseValidatorDecision.ResponseValidatorDecision(False, 
                    self.__exercise.get_difficulty(), True)