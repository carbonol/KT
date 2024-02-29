# Dificultad
class Difficulty:

    # Constructor (Vacío o no vacío)
    def __init__(self, difficulty_level: int, min_exercise_attempts_before_next_correct_attempt_reference: int=None, 
    max_exercise_attempts_before_next_correct_attempt_reference: int=None, min_exercise_response_time_reference: float=None, 
    max_exercise_response_time_reference: float=None):

        if (type(difficulty_level) != int):
            raise TypeError('El argumento difficulty_level debe ser un número entero (int)')

        # Notas:
        # 1) Se deben especificar los valores mínimo y máximo para cada tipo de referencia.
        # Para asignar sólo un valor de referencia, se debe colocar este mismo valor en ambos valores (mínimo y máximo).
        # 2) Los tiempos de referencia deben ser números reales (float) mayores que 0.0.
        # 3) Los valores de referencia para números de intentos esperados antes de obtener una respuesta CORRECTA deben
        # ser números enteros (int) mayores o iguales que 1.
        # 4) Todo valor de referencia máximo debe ser mayor o igual que sus correspondientes valores de referencia mínimos.

        # elif (max_exercise_correct_answer_time != None and type(max_exercise_correct_answer_time) != float):
        #     raise TypeError('El argumento max_exercise_correct_answer_time debe ser un número real (float)')
        # elif (max_exercise_correct_answer_time != None and max_exercise_correct_answer_time <= 0.0):
        #     raise ValueError('El argumento max_exercise_correct_answer_time debe ser un número real (float) mayor ' 
        #         + 'que 0.0 (segundos)')
                
        # elif (max_exercise_attempts != None and type(max_exercise_attempts) != int):
        #     raise TypeError('El argumento max_exercise_attempts debe ser un número entero (int)')
        # elif (max_exercise_attempts != None and max_exercise_attempts <= 0):
        #     raise ValueError('El argumento max_exercise_attempts debe ser un número entero (int) mayor que 0')

        elif (min_exercise_attempts_before_next_correct_attempt_reference == None 
        or max_exercise_attempts_before_next_correct_attempt_reference == None
        or type(min_exercise_attempts_before_next_correct_attempt_reference) != int
        or type(max_exercise_attempts_before_next_correct_attempt_reference) != int
        or min_exercise_attempts_before_next_correct_attempt_reference < 1 
        or max_exercise_attempts_before_next_correct_attempt_reference < 1):
            raise ValueError('Los valores de referencia para establecer los números de intentos mínimo y máximo esperados ' 
            + 'antes de obtener una respuesta correcta de un ejercicio en un nivel de dificultad dado, deben ser números ' 
            + 'enteros (int) mayores o iguales que 1.')

        elif (max_exercise_attempts_before_next_correct_attempt_reference 
        < min_exercise_attempts_before_next_correct_attempt_reference):
            raise ValueError('El valor de referencia máximo para el número de intentos esperados antes de obtener ' 
            + 'la siguiente respuesta correcta de un ejercicio en un nivel de dificultad dado, debe ser mayor o igual que ' 
            + 'su valor de referencia mínimo.')

        elif (min_exercise_response_time_reference == None 
        or max_exercise_response_time_reference == None
        or type(min_exercise_response_time_reference) != float
        or type(max_exercise_response_time_reference) != float
        or min_exercise_response_time_reference <= 0.0 
        or max_exercise_response_time_reference <= 0.0):
            raise ValueError('Los tiempos de respuesta mínimo y máximo de referencia para un nivel de dificultad dado ' +
            ' deben ser números reales (float) mayores que 0.0.')

        elif (max_exercise_response_time_reference 
        < min_exercise_response_time_reference):
            raise ValueError('El valor de referencia máximo para el tiempo de respuesta en un nivel de dificultad dado ' + 
            'debe ser mayor o igual que su valor de referencia mínimo.')        
        
        self.__difficulty_level = difficulty_level
        # self.__max_exercise_correct_answer_time = max_exercise_correct_answer_time
        # self.__max_exercise_attempts = max_exercise_attempts
        self.__min_exercise_attempts_before_next_correct_attempt_reference = min_exercise_attempts_before_next_correct_attempt_reference
        self.__max_exercise_attempts_before_next_correct_attempt_reference = max_exercise_attempts_before_next_correct_attempt_reference
        self.__min_exercise_response_time_reference = min_exercise_response_time_reference
        self.__max_exercise_response_time_reference = max_exercise_response_time_reference

    # Getters
    def get_difficulty_level(self):
        return self.__difficulty_level

    # def get_max_exercise_correct_answer_time(self):
    #     return self.__max_exercise_correct_answer_time

    # def get_max_exercise_attempts(self):
    #     return self.__max_exercise_attempts

    def get_min_exercise_attempts_before_next_correct_attempt_reference(self):
        return self.__min_exercise_attempts_before_next_correct_attempt_reference

    def get_max_exercise_attempts_before_next_correct_attempt_reference(self):
        return self.__max_exercise_attempts_before_next_correct_attempt_reference

    def get_min_exercise_response_time_reference(self):
        return self.__min_exercise_response_time_reference

    def get_max_exercise_response_time_reference(self):
        return self.__max_exercise_response_time_reference

    # Setters
    def set_difficulty_level(self, difficulty_level: int):
        if (type(difficulty_level) != int):
            raise TypeError('El argumento difficulty_level debe ser un número entero')
        else:
            self.__difficulty_level = difficulty_level

    # def set_max_exercise_correct_answer_time(self, max_exercise_correct_answer_time: float):
    #     if (type(max_exercise_correct_answer_time) != float):
    #         raise TypeError('El argumento max_exercise_correct_answer_time debe ser un número real (float)')
    #     elif (max_exercise_correct_answer_time <= 0.0):
    #         raise ValueError('El argumento max_exercise_correct_answer_time debe ser un número real (float) mayor ' 
    #             + 'que 0.0 (segundos)')
    #     else:
    #         self.__max_exercise_correct_answer_time = max_exercise_correct_answer_time

    # def set_max_exercise_attempts(self, max_exercise_attempts: int):
    #     if (type(max_exercise_attempts) != int):
    #         raise TypeError('El argumento max_exercise_attempts debe ser un número entero (int)')
    #     elif (max_exercise_attempts <= 0):
    #         raise ValueError('El argumento max_exercise_attempts debe ser un número entero (int) mayor que 0')
    #     else:
    #         self.__max_exercise_attempts = max_exercise_attempts

    def set_min_exercise_attempts_before_next_correct_attempt_reference(self, 
    min_exercise_attempts_before_next_correct_attempt_reference: int):
        if (min_exercise_attempts_before_next_correct_attempt_reference == None
        or type(min_exercise_attempts_before_next_correct_attempt_reference) != int
        or min_exercise_attempts_before_next_correct_attempt_reference < 1):
            raise ValueError('El valor de referencia para establecer el número de intentos mínimo esperado ' 
            + 'antes de obtener una respuesta correcta de un ejercicio, en un nivel de dificultad dado, debe ser un número ' 
            + 'entero (int) mayor o igual que 1.')
        elif (self.__max_exercise_attempts_before_next_correct_attempt_reference 
        < min_exercise_attempts_before_next_correct_attempt_reference):
            raise ValueError('El valor de referencia máximo para el número de intentos esperados antes de obtener ' 
            + 'la siguiente respuesta correcta de un ejercicio, en un nivel de dificultad dado, debe ser mayor o igual que ' 
            + 'su valor de referencia mínimo.')
        else:
            self.__min_exercise_attempts_before_next_correct_attempt_reference = max_exercise_attempts_before_next_correct_attempt_reference

    def set_max_exercise_attempts_before_next_correct_attempt_reference(self, 
    max_exercise_attempts_before_next_correct_attempt_reference: int):
        if (max_exercise_attempts_before_next_correct_attempt_reference == None
        or type(max_exercise_attempts_before_next_correct_attempt_reference) != int
        or max_exercise_attempts_before_next_correct_attempt_reference < 1):
            raise ValueError('El valor de referencia para establecer el número de intentos máximo esperado ' 
            + 'antes de obtener una respuesta correcta de un ejercicio, en un nivel de dificultad dado, debe ser un número ' 
            + 'entero (int) mayor o igual que 1.')
        elif (max_exercise_attempts_before_next_correct_attempt_reference 
        < self.__min_exercise_attempts_before_next_correct_attempt_reference):
            raise ValueError('El valor de referencia máximo para el número de intentos esperados antes de obtener ' 
            + 'la siguiente respuesta correcta de un ejercicio, en un nivel de dificultad dado, debe ser mayor o igual que ' 
            + 'su valor de referencia mínimo.')
        else:
            self.__max_exercise_attempts_before_next_correct_attempt_reference = max_exercise_attempts_before_next_correct_attempt_reference

    def set_min_exercise_response_time_reference(self, min_exercise_response_time_reference: float):
        if (min_exercise_response_time_reference == None
        or type(min_exercise_response_time_reference) != float
        or min_exercise_response_time_reference <= 0.0):
            raise ValueError('El tiempo de respuesta mínimo de referencia para un nivel de dificultad dado ' +
            ' debe ser un número real (float) mayor que 0.0.')
        elif (self.__max_exercise_response_time_reference 
        < min_exercise_response_time_reference):
            raise ValueError('El valor de referencia máximo para el tiempo de respuesta en un nivel de dificultad dado ' + 
            'debe ser mayor o igual que su valor de referencia mínimo.')
        else:
            self.__min_exercise_response_time_reference = min_exercise_response_time_reference

    def set_max_exercise_response_time_reference(self, max_exercise_response_time_reference: float):
        if (max_exercise_response_time_reference == None
        or type(max_exercise_response_time_reference) != float
        or max_exercise_response_time_reference <= 0.0):
            raise ValueError('El tiempo de respuesta máximo de referencia para un nivel de dificultad dado ' +
            ' debe ser un número real (float) mayor que 0.0.')
        elif (max_exercise_response_time_reference 
        < self.__min_exercise_response_time_reference):
            raise ValueError('El valor de referencia máximo para el tiempo de respuesta en un nivel de dificultad dado ' + 
            'debe ser mayor o igual que su valor de referencia mínimo.')
        else:
            self.__max_exercise_response_time_reference = max_exercise_response_time_reference