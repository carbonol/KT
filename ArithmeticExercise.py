import Difficulty

# Clase de ejercicios de aritmética
class ArithmeticExercise:

    # Constructor (Vacío o no vacío)
    def __init__(self, description:str, difficulty:Difficulty.Difficulty, correct_response:int):
        self.__description = description
        self.__difficulty = difficulty
        self.__correct_response = correct_response

    # Getters
    def get_description(self):
        return self.__description

    def get_difficulty(self):
        return self.__difficulty

    def get_correct_response(self):
        return self.__correct_response

    # Setters
    def set_description(self, description):
        self.__description = description

    def set_difficulty(self, difficulty):
        self.__difficulty = difficulty

    def set_correct_response(self, correct_response):
        self.__correct_response = correct_response
