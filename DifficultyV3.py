# Dificultad
class Difficulty:

    # Constructor (Vacío o no vacío)
    def __init__(self, 
    difficulty_level: int, 
    max_exercise_attempts_per_exercise: int=None, 
    max_superior_correct_response_time: float=None, 
    min_inferior_correct_response_time: float=None):
        # Notas de validación de atributos de la clase Difficulty (V3):
        # 1) Se deben especificar todos los valores de los argumentos requeridos por la clase Difficulty.
        # 1a) max_superior_correct_response_time es inclusivo
        # 1b) min_inferior_correct_response_time es no inclusivo (i.e., no incluye a este tiempo en sí como un 
        #   tiempo de respuesta correcta que determina que una respuesta es inferior - aunque correcta)
        # 2) difficulty_level debe ser un número entero (int).
        # 3) max_exercise_attempts_per_exercise debe ser un número entero (int) mayor o igual a 1.
        # 4) max_superior_correct_response_time y min_inferior_correct_response_time deben ser números reales (float) 
        #   mayores que 0.0.
        # 5) min_inferior_correct_response_time debe ser mayor o igual a max_superior_correct_response_time.

        if (type(difficulty_level) != int):
            raise TypeError('El argumento difficulty_level debe ser un número entero (int)')

        elif (max_exercise_attempts_per_exercise == None
        or type(max_exercise_attempts_per_exercise) != int
        or max_exercise_attempts_per_exercise < 1):
            raise ValueError('El número máximo de intentos permitidos por ejercicio en cualquier nivel de dificultad ' 
            + 'antes de forzar un cambio de ejercicio en ese nivel de dificultad debe ser un entero (int) mayor o igual a 1.')

        elif (max_superior_correct_response_time == None 
        or min_inferior_correct_response_time == None
        or type(max_superior_correct_response_time) != float
        or type(min_inferior_correct_response_time) != float
        or max_superior_correct_response_time <= 0.0 
        or min_inferior_correct_response_time <= 0.0):
            raise ValueError('Los tiempos de respuesta correcta máximo y mínimo de referencia para determinar que una ' 
            + 'respuesta correcta es superior o inferior, respectivamente, en cualquier nivel de dificultad dado, ' 
            + 'deben ser números reales (float) mayores que 0.0.')

        elif (min_inferior_correct_response_time 
        < max_superior_correct_response_time):
            raise ValueError('El tiempo mínimo de respuesta correcta (no inclusivo) para determinar que una respuesta correcta ' 
            + 'es inferior debe ser mayor o igual que el tiempo máximo de respuesta correcta (inclusivo) para determinar que ' 
            + 'una respuesta correcta es superior, en cualquier nivel de dificultad dado.')
        
        self.__difficulty_level = difficulty_level
        self.__max_exercise_attempts_per_exercise = max_exercise_attempts_per_exercise
        self.__max_superior_correct_response_time = max_superior_correct_response_time
        self.__min_inferior_correct_response_time = min_inferior_correct_response_time

    # Getters
    def get_difficulty_level(self):
        return self.__difficulty_level

    def get_max_exercise_attempts_per_exercise(self):
        return self.__max_exercise_attempts_per_exercise

    def get_max_superior_correct_response_time(self):
        return self.__max_superior_correct_response_time

    def get_min_inferior_correct_response_time(self):
        return self.__min_inferior_correct_response_time

    # Setters
    def set_difficulty_level(self, difficulty_level: int):
        if (type(difficulty_level) != int):
            raise TypeError('El argumento difficulty_level debe ser un número entero')
        else:
            self.__difficulty_level = difficulty_level

    def set_max_exercise_attempts_per_exercise(self, max_exercise_attempts_per_exercise: int):
        if (max_exercise_attempts_per_exercise == None
        or type(max_exercise_attempts_per_exercise) != int
        or max_exercise_attempts_per_exercise < 1):
            raise ValueError('El número máximo de intentos permitidos por ejercicio en cualquier nivel de dificultad ' 
            + 'antes de forzar un cambio de ejercicio en ese nivel de dificultad debe ser un entero (int) mayor o igual a 1.')
        else:
            self.__max_exercise_attempts_per_exercise = max_exercise_attempts_per_exercise

    def set_max_superior_correct_response_time(self, max_superior_correct_response_time: float):
        if (max_superior_correct_response_time == None
        or type(max_superior_correct_response_time) != float
        or max_superior_correct_response_time <= 0.0):
            raise ValueError('El tiempo máximo de respuesta correcta para determinar que una ' 
            + 'respuesta correcta es superior, en cualquier nivel de dificultad dado, ' 
            + 'debe ser un número real (float) mayor que 0.0.')
        elif (self.__min_inferior_correct_response_time 
        < max_superior_correct_response_time):
            raise ValueError('El tiempo máximo de respuesta correcta (inclusivo) para determinar que una ' 
            + 'respuesta correcta es superior debe ser menor o igual al tiempo mínimo de respuesta correcta ' 
            + '(no inclusivo) para determinar que una respuesta correcta ' 
            + 'es inferior, en cualquier nivel de dificultad dado.')
        else:
            self.__max_superior_correct_response_time = max_superior_correct_response_time

    def set_min_inferior_correct_response_time(self, min_inferior_correct_response_time: float):
        if (min_inferior_correct_response_time == None
        or type(min_inferior_correct_response_time) != float
        or min_inferior_correct_response_time <= 0.0):
            raise ValueError('El tiempo mínimo de respuesta correcta para determinar que una ' 
            + 'respuesta correcta es inferior, en cualquier nivel de dificultad dado, ' 
            + 'debe ser un número real (float) mayor que 0.0.')
        elif (min_inferior_correct_response_time 
        < self.__max_superior_correct_response_time):
            raise ValueError('El tiempo mínimo de respuesta correcta (no inclusivo) para determinar que una respuesta correcta ' 
            + 'es inferior debe ser mayor o igual que el tiempo máximo de respuesta correcta (inclusivo) para determinar que una ' 
            + 'respuesta correcta es superior, en cualquier nivel de dificultad dado.')
        else:
            self.__min_inferior_correct_response_time = min_inferior_correct_response_time