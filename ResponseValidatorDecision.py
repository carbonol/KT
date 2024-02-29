import Difficulty

# Clase de decisión de validador de respuesta
class ResponseValidatorDecision:

    # Constructor (Vacío o no vacío)
    def __init__(self, correctness:bool, next_difficulty:Difficulty.Difficulty, same_exercise:bool):
        self.__correctness = correctness
        self.__next_difficulty = next_difficulty
        self.__same_exercise = same_exercise

    # Getters
    def get_correctness(self):
        return self.__correctness

    def get_next_difficulty(self):
        return self.__next_difficulty

    def get_same_exercise(self):
        return self.__same_exercise

    # Setters
    def set_correctness(self, correctness):
        self.__correctness = correctness

    def set_next_difficulty(self, next_difficulty):
        self.__next_difficulty = next_difficulty

    def set_same_exercise(self, same_exercise):
        self.__same_exercise = same_exercise