import copy
import math
# Modelo Performance Factors Analysis Plus (PFA+)
class PFAPlus:

    INCORRECT_OUTCOME = 0
    CORRECT_FAST_OUTCOME = 1
    CORRECT_OUTCOME = 2
    CORRECT_SLOW_OUTCOME = 3

    # Un modelo PFA que considera tiempos de respuesta como factores de rendimiento relevantes en el aprendizaje de
    #   componentes de conocimiento o habilidades, y, tal como en un modelo PFA tradicional, aplica para un solo estudiante i 
    #   y uno o varios componentes de conocimiento j.

    # Parámetros del modelo PFA
    # a) Número kc_count de componentes de conocimiento (knowledge components, los cuales también pueden considerarse 
    #   habilidades evaluables)
    # b) Los valores beta (nivel de facilidad o dificultad) para cada componente de conocimiento j
    # c) Los valores gamma (contribución de una interacción correcta a priori al aprendizaje del componente de conocimiento j) 
    #   para cada componente de conocimiento j
    # d) Los valores rho (contribución de una interacción incorrecta a priori al aprendizaje del componente de conocimiento j) 
    #   para cada componente de conocimiento j

    # Parámetros del modelo PFA+
    # e) Los valores gamma_t (contribución de una interacción correcta (a priori) realizada en un tiempo superior al esperado 
    #   - según el componente de conocimiento j - al aprendizaje del componente de conocimiento j) 
    #   para cada componente de conocimiento j
    # f) Los valores rho_t (contribución de una interacción correcta (a priori) realizada en un tiempo inferior al esperado 
    #   - según el componente de conocimiento j - al aprendizaje del componente de conocimiento j) 
    #   para cada componente de conocimiento j

    # Variables de trazabilidad del modelo PFA
    # a) Trazabilidad del número de interacciones correctas a priori realizadas por el estudiante i al practicar cada 
    #   componente de conocimiento j (Estos son valores s_ij)
    # b) Trazabilidad del número de interacciones incorrectas a priori realizadas por el estudiante i al practicar cada 
    #   componente de conocimiento j (Estos son valores f_ij)

    # Variables de trazabilidad del modelo PFA+
    # c) Trazabilidad del número de interacciones correctas (a priori) realizadas en un tiempo superior al esperado 
    #   - según el componente de conocimiento j - por el estudiante i al practicar cada componente de conocimiento j 
    #   (Estos son valores lt_ij)
    # d) Trazabilidad del número de interacciones incorrectas (a priori) realizadas en un tiempo inferior al esperado 
    #   - según el componente de conocimiento j - por el estudiante i al practicar cada componente de conocimiento j 
    #   (Estos son valores ht_ij)

    # Resultados a obtener del modelo PFA (De igual manera aplica para el modelo PFA+, aunque el cálculo de m y p(m) 
    #   es diferente)
    # m : Valor logit que representa al aprendizaje acumulado del estudiante i, utilizando una o más habilidades o
    #   componentes de conocimiento j (Nota: Este valor m NO es una probabilidad).
    # p : Estimación de predicción de probabilidad a posteriori observada que está relacionada con el valor m

    # Constructor (Vacío o no vacío)
    # def __init__(self, kc_count:int=0, beta:list=[], gamma:list=[], rho:list=[], gamma_t:list=[], rho_t:list=[], 
    #     s:list=[], f:list=[], lt:list=[], ht:list=[]):
    def __init__(self, kc_count:int=0, beta:list=[], gamma:list=[], rho:list=[], gamma_t:list=[], rho_t:list=[]):

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

        # Parámetros del modelo PFA+
        if (type(gamma_t) != list):
            raise TypeError('El argumento gamma_t debe ser una lista (list)')
        elif (len(gamma_t) != kc_count):
            raise ValueError('El argumento gamma_t debe ser una lista (list) con kc_count (', kc_count, ') elementos')
        else:
            for i in range(kc_count):
                if (type(gamma_t[i]) != float):
                    raise TypeError('Todos los elementos de la lista gamma_t deben ser números reales (float)')

        if (type(rho_t) != list):
            raise TypeError('El argumento rho_t debe ser una lista (list)')
        elif (len(rho_t) != kc_count):
            raise ValueError('El argumento rho_t debe ser una lista (list) con kc_count (', kc_count, ') elementos')
        else:
            for i in range(kc_count):
                if (type(rho_t[i]) != float):
                    raise TypeError('Todos los elementos de la lista rho_t deben ser números reales (float)')

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

        # Variables de trazabilidad del modelo PFA+
        # Los conjuntos lt y ht son números enteros.
        # if (type(lt) != list):
        #     raise TypeError('El argumento lt debe ser una lista (list)')
        # elif (len(lt) != kc_count):
        #     raise ValueError('El argumento lt debe ser una lista (list) con kc_count (', kc_count, ') elementos')
        # else:
        #     for i in range(kc_count):
        #         if (type(lt[i]) != int):
        #             raise TypeError('Todos los elementos de la lista lt deben ser números enteros (int)')

        # if (type(ht) != list):
        #     raise TypeError('El argumento ht debe ser una lista (list)')
        # elif (len(ht) != kc_count):
        #     raise ValueError('El argumento ht debe ser una lista (list) con kc_count (', kc_count, ') elementos')
        # else:
        #     for i in range(kc_count):
        #         if (type(ht[i]) != int):
        #             raise TypeError('Todos los elementos de la lista ht deben ser números enteros (int)')

        self.__kc_count = kc_count
        self.__beta = copy.deepcopy(beta)
        self.__gamma = copy.deepcopy(gamma)
        self.__rho = copy.deepcopy(rho)

        self.__gamma_t = copy.deepcopy(gamma_t)
        self.__rho_t = copy.deepcopy(rho_t)

        # self.__s = copy.deepcopy(s)
        # self.__f = copy.deepcopy(f)

        s = []
        f = []
        for i in range(self.__kc_count):
            s.append(0)
            f.append(0)
        self.__s = s
        self.__f = f

        # self.__lt = copy.deepcopy(lt)
        # self.__ht = copy.deepcopy(ht)
        
        lt = []
        ht = []
        for i in range(self.__kc_count):
            lt.append(0)
            ht.append(0)
        self.__lt = lt
        self.__ht = ht

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

    def get_gamma_t(self):
        return self.__gamma_t

    def get_rho_t(self):
        return self.__rho_t

    def get_s(self):
        return self.__s

    def get_f(self):
        return self.__f

    def get_lt(self):
        return self.__lt

    def get_ht(self):
        return self.__ht

    def get_m(self):
        return self.__m

    def get_p_m(self):
        return self.__p_m

    # Actualización del modelo PFA al obtener una observación (respuesta correcta o incorrecta para una habilidad j, y si es
    #   una respuesta correcta, si esta respuesta fue más rápida o lenta de lo esperada)
    def update_model(self, kc:list=[], success_status:list=[]):
        if (type(kc) != list or type(success_status) != list):
            raise TypeError('Los argumentos kc y success_status de la función update_model deben ser listas (list)')
        if (len(kc) != len(success_status)):
            raise ValueError('Las listas de los argumentos kc y success_status de la función update_model ', 
                'deben tener el mismo número de elementos.')

        for kc_elem in kc:
            if (type(kc_elem) != int or kc_elem < 0 or kc_elem > self.__kc_count):
                raise TypeError('Los elementos de la lista kc de la función update_model deben ser números enteros (int) ', 
                    'mayores que 0 y menores que kc_count (' , self.__kc_count , ')')

        for success_status_elem in success_status:
            if (type(success_status_elem) != int):
                raise TypeError('Los elementos de la lista correctness de la función success_status deben ser números ', 
                    'enteros (int)')

        for i in range(len(kc)):
            j = kc[i] - 1
            status = success_status[i]
            if (status == PFAPlus.INCORRECT_OUTCOME):
                self.__f[j] += 1
            else:
                self.__s[j] += 1
                if (status == PFAPlus.CORRECT_FAST_OUTCOME):
                    self.__lt[j] += 1
                elif (status == PFAPlus.CORRECT_SLOW_OUTCOME):
                    self.__ht[j] += 1

        self.__m = self.calculate_current_logit_values()
        self.__p_m = self.calculate_posterior_correct_answer_probabilities()

    def calculate_logit_value_m(self, kc:list=[]):
        m = 0.0
        for j in kc:
            m += self.__beta[j] + (self.__gamma[j] * self.__s[j]) + (self.__rho[j] * self.__f[j]) \
                + (self.__gamma_t[j] * self.__lt[j]) + (self.__rho_t[j] * self.__ht[j])
        return m

    def calculate_current_logit_values(self):
        m_list = []
        for j in range(self.__kc_count):
            m_list.append(self.__beta[j] + (self.__gamma[j] * self.__s[j]) + (self.__rho[j] * self.__f[j])
                + (self.__gamma_t[j] * self.__lt[j]) + (self.__rho_t[j] * self.__ht[j]))
        return m_list

    def calculate_posterior_correct_answer_probability(self, m:float):
        return 1.0 / (1.0 + math.exp(-m))

    def calculate_posterior_correct_answer_probabilities(self):
        p_list = []
        for j in range(self.__kc_count):
            p_list.append(self.calculate_posterior_correct_answer_probability(self.__m[j]))
        return p_list