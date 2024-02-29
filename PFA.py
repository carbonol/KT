import copy
import math
# Modelo Performance Factors Analysis (PFA)
class PFA:

    # Un modelo PFA aplica para un solo estudiante i y uno o varios componentes de conocimiento j.

    # Parámetros del modelo PFA
    # a) Número kc_count de componentes de conocimiento (knowledge components, los cuales también pueden considerarse 
    #   habilidades evaluables)
    # b) Los valores beta (nivel de facilidad o dificultad) para cada componente de conocimiento j
    # c) Los valores gamma (contribución de una interacción correcta a priori al aprendizaje del componente de conocimiento j) 
    #   para cada componente de conocimiento j
    # d) Los valores rho (contribución de una interacción incorrecta a priori al aprendizaje del componente de conocimiento j) 
    #   para cada componente de conocimiento j

    # Variables de trazabilidad
    # a) Trazabilidad del número de interacciones correctas a priori realizadas por el estudiante i al practicar cada 
    #   componente de conocimiento j (Estos son valores s_ij)
    # b) Trazabilidad del número de interacciones incorrectas a priori realizadas por el estudiante i al practicar cada 
    #   componente de conocimiento j (Estos son valores f_ij)

    # Resultados a obtener del modelo PFA
    # m : Valor logit que representa al aprendizaje acumulado del estudiante i, utilizando una o más habilidades o
    #   componentes de conocimiento j (Nota: Este valor m NO es una probabilidad).
    # p : Estimación de predicción de probabilidad a posteriori observada que está relacionada con el valor m

    # Constructor (Vacío o no vacío)
    # def __init__(self, kc_count:int=0, beta:list=[], gamma:list=[], rho:list=[], s:list=[], f:list=[]):
    def __init__(self, kc_count:int=0, beta:list=[], gamma:list=[], rho:list=[]):

        # El parámetro kc_count del modelo PFA es un número entero que debería ser mayor que 0.
        if (type(kc_count) != int):
            raise TypeError('El argumento kc_count debe ser un número entero')
        elif (kc_count <= 0):
            raise ValueError('El argumento kc_count debe ser un número entero mayor que 0')

        # Los demás parámetros del modelo PFA son conjuntos de kc_count elementos.
        # Los conjuntos beta, gamma y rho son números reales (los cuales pueden ser representados de forma exacta 
        #   o aproximada por un valor punto flotante).
        if (type(beta) != list):
            raise TypeError('El argumento beta debe ser una lista (list)')
        elif (len(beta) != kc_count):
            raise ValueError('El argumento beta debe ser una lista (list) con kc_count (', kc_count, ') elementos')
        else:
            for i in range(kc_count):
                if (type(beta[i]) != float):
                    raise TypeError('Todos los elementos de la lista beta deben ser números reales (float)')

        if (type(gamma) != list):
            raise TypeError('El argumento gamma debe ser una lista (list)')
        elif (len(gamma) != kc_count):
            raise ValueError('El argumento gamma debe ser una lista (list) con kc_count (', kc_count, ') elementos')
        else:
            for i in range(kc_count):
                if (type(gamma[i]) != float):
                    raise TypeError('Todos los elementos de la lista gamma deben ser números reales (float)')

        if (type(rho) != list):
            raise TypeError('El argumento rho debe ser una lista (list)')
        elif (len(rho) != kc_count):
            raise ValueError('El argumento rho debe ser una lista (list) con kc_count (', kc_count, ') elementos')
        else:
            for i in range(kc_count):
                if (type(rho[i]) != float):
                    raise TypeError('Todos los elementos de la lista rho deben ser números reales (float)')

        # Los conjuntos s y f son números enteros.

        # if (type(s) != list):
        #     raise TypeError('El argumento s debe ser una lista (list)')
        # elif (len(s) != kc_count):
        #     raise ValueError('El argumento s debe ser una lista (list) con kc_count (', kc_count, ') elementos')
        # else:
        #     for i in range(kc_count):
        #         if (type(s[i]) != int):
        #             raise TypeError('Todos los elementos de la lista s deben ser números enteros (int)')

        # if (type(f) != list):
        #     raise TypeError('El argumento f debe ser una lista (list)')
        # elif (len(f) != kc_count):
        #     raise ValueError('El argumento f debe ser una lista (list) con kc_count (', kc_count, ') elementos')
        # else:
        #     for i in range(kc_count):
        #         if (type(f[i]) != int):
        #             raise TypeError('Todos los elementos de la lista f deben ser números enteros (int)')

        self.__kc_count = kc_count
        self.__beta = copy.deepcopy(beta)
        self.__gamma = copy.deepcopy(gamma)
        self.__rho = copy.deepcopy(rho)

        # self.__s = copy.deepcopy(s)
        # self.__f = copy.deepcopy(f)

        s = []
        f = []
        for i in range(self.__kc_count):
            s.append(0)
            f.append(0)
        self.__s = s
        self.__f = f

        self.__m = self.calculate_current_logit_values()
        self.__p_m = self.calculate_posterior_correct_answer_probabilities()

    # Getters
    def get_kc_count(self):
        return self.__kc_count

    def get_beta(self):
        return self.__beta

    def get_gamma(self):
        return self.__gamma

    def get_rho(self):
        return self.__rho

    def get_s(self):
        return self.__s

    def get_f(self):
        return self.__f

    def get_m(self):
        return self.__m

    def get_p_m(self):
        return self.__p_m

    # Actualización del modelo PFA al obtener una observación (respuesta correcta o incorrecta para una habilidad j)
    def update_model(self, kc:list=[], correctness:list=[]):
        if (type(kc) != list or type(correctness) != list):
            raise TypeError('Los argumentos kc y correctness de la función update_model deben ser listas (list)')
        if (len(kc) != len(correctness)):
            raise ValueError('Las listas de los argumentos kc y correctness de la función update_model deben tener ', 
                'el mismo número de elementos.')
        
        for kc_elem in kc:
            if (type(kc_elem) != int or kc_elem < 0 or kc_elem > self.__kc_count):
                raise TypeError('Los elementos de la lista kc de la función update_model deben ser números enteros (int) ', 
                    'mayores que 0 y menores que kc_count (' , self.__kc_count , ')')

        for correctness_elem in correctness:
            if (type(correctness_elem) != bool):
                raise TypeError('Los elementos de la lista correctness de la función update_model deben ser booleanos (bool)')

        for i in range(len(kc)):
            j = kc[i] - 1
            c = correctness[i]
            if (c):
                self.__s[j] += 1
            else:
                self.__f[j] += 1

        self.__m = self.calculate_current_logit_values()
        self.__p_m = self.calculate_posterior_correct_answer_probabilities()

    def calculate_logit_value_m(self, kc:list=[]):
        m = 0.0
        for j in kc:
            m += self.__beta[j] + (self.__gamma[j] * self.__s[j]) + (self.__rho[j] * self.__f[j])
        return m

    def calculate_current_logit_values(self):
        m_list = []
        for j in range(self.__kc_count):
            m_list.append(self.__beta[j] + (self.__gamma[j] * self.__s[j]) + (self.__rho[j] * self.__f[j]))
        return m_list

    def calculate_posterior_correct_answer_probability(self, m:float):
        return 1.0 / (1.0 + math.exp(-m))

    def calculate_posterior_correct_answer_probabilities(self):
        p_list = []
        for j in range(self.__kc_count):
            p_list.append(self.calculate_posterior_correct_answer_probability(self.__m[j]))
        return p_list