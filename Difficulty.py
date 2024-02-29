# Dificultad
class Difficulty:

    # Constructor (Vacío o no vacío)
    def __init__(self, difficulty_level: int, max_exercise_correct_answer_time: float=None, 
        max_exercise_attempts: int=None):
        if (type(difficulty_level) != int):
            raise TypeError('El argumento difficulty_level debe ser un número entero (int)')

        elif (max_exercise_correct_answer_time != None and type(max_exercise_correct_answer_time) != float):
            raise TypeError('El argumento max_exercise_correct_answer_time debe ser un número real (float)')
        elif (max_exercise_correct_answer_time != None and max_exercise_correct_answer_time <= 0.0):
            raise ValueError('El argumento max_exercise_correct_answer_time debe ser un número real (float) mayor ' 
                + 'que 0.0 (segundos)')
                
        elif (max_exercise_attempts != None and type(max_exercise_attempts) != int):
            raise TypeError('El argumento max_exercise_attempts debe ser un número entero (int)')
        elif (max_exercise_attempts != None and max_exercise_attempts <= 0):
            raise ValueError('El argumento max_exercise_attempts debe ser un número entero (int) mayor que 0')
        
        self.__difficulty_level = difficulty_level
        self.__max_exercise_correct_answer_time = max_exercise_correct_answer_time
        self.__max_exercise_attempts = max_exercise_attempts

    # Getters
    def get_difficulty_level(self):
        return self.__difficulty_level

    def get_max_exercise_correct_answer_time(self):
        return self.__max_exercise_correct_answer_time

    def get_max_exercise_attempts(self):
        return self.__max_exercise_attempts

    # Setters
    def set_difficulty_level(self, difficulty_level: int):
        if (type(difficulty_level) != int):
            raise TypeError('El argumento difficulty_level debe ser un número entero')
        else:
            self.__difficulty_level = difficulty_level

    def set_max_exercise_correct_answer_time(self, max_exercise_correct_answer_time: float):
        if (type(max_exercise_correct_answer_time) != float):
            raise TypeError('El argumento max_exercise_correct_answer_time debe ser un número real (float)')
        elif (max_exercise_correct_answer_time <= 0.0):
            raise ValueError('El argumento max_exercise_correct_answer_time debe ser un número real (float) mayor ' 
                + 'que 0.0 (segundos)')
        else:
            self.__max_exercise_correct_answer_time = max_exercise_correct_answer_time

    def set_max_exercise_attempts(self, max_exercise_attempts: int):
        if (type(max_exercise_attempts) != int):
            raise TypeError('El argumento max_exercise_attempts debe ser un número entero (int)')
        elif (max_exercise_attempts <= 0):
            raise ValueError('El argumento max_exercise_attempts debe ser un número entero (int) mayor que 0')
        else:
            self.__max_exercise_attempts = max_exercise_attempts