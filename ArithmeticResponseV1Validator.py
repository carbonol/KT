import ArithmeticExercise
import DifficultyMachine
import ResponseValidatorDecision

# Clase de validador de respuesta de ejercicios aritméticos
class ArithmeticResponseValidator:
    # Constructor (Vacío o no vacío)
    def __init__(self, exercise:ArithmeticExercise.ArithmeticExercise, user_response:int):
        self.__exercise = exercise
        self.__user_response = user_response
    
    # Getters
    def get_exercise(self):
        return self.__exercise

    def get_user_response(self):
        return self.__user_response

    # Setters
    def set_exercise(self, exercise):
        self.__exercise = exercise

    def set_user_response(self, user_response):
        self.__user_response = user_response

    # Validador y tomador de decisiones frente a una respuesta del usuario
    def validate_response(self, difficulty_machine:DifficultyMachine.DifficultyMachine):
        if self.get_user_response() == self.get_exercise().get_correct_response():
            return ResponseValidatorDecision.ResponseValidatorDecision(True, 
                difficulty_machine.get_superior_difficulty(), False)
        else:
            return ResponseValidatorDecision.ResponseValidatorDecision(False, 
                self.__exercise.get_difficulty(), True)