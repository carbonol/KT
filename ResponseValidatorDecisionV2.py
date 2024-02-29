import DifficultyV3

# Clase de decisión de validador de respuesta
class ResponseValidatorDecision:

    EXPECTED_CORRECT_RESPONSE_TIME = 0
    SUPERIOR_CORRECT_RESPONSE_TIME = 1
    INFERIOR_CORRECT_RESPONSE_TIME = 2

    # Constructor (Vacío o no vacío)
    def __init__(self, correctness:bool, next_difficulty:DifficultyV3.Difficulty, same_exercise:bool, 
    correct_response_time: int):
        self.__correctness = correctness
        self.__next_difficulty = next_difficulty
        self.__same_exercise = same_exercise
        self.__correct_response_time = correct_response_time

    # Getters
    def get_correctness(self):
        return self.__correctness

    def get_next_difficulty(self):
        return self.__next_difficulty

    def get_same_exercise(self):
        return self.__same_exercise

    def get_correct_response_time(self):
        return self.__correct_response_time

    # Setters
    def set_correctness(self, correctness):
        self.__correctness = correctness

    def set_next_difficulty(self, next_difficulty):
        self.__next_difficulty = next_difficulty

    def set_same_exercise(self, same_exercise):
        self.__same_exercise = same_exercise

    def set_correct_response_time(self, correct_response_time):
        self.__correct_response_time = correct_response_time