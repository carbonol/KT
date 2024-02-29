def calculate_new_probability_given_weight(original_probability:float, weight:float):
    numerator = original_probability * weight
    denominator = 1 - original_probability + (original_probability * weight)
    new_probability = numerator / denominator
    if (new_probability < 0):
        return 0.0
    elif (new_probability > 1):
        return 1.0
    else:
        return new_probability

# NOTA: Esta función no se ha usado en el programa de ejercicios de sumas, ni en el simulador de modelo WBKT,
#   ni en la clase WBKT
def calculate_weight_given_new_probability(original_probability:float, new_probability:float):
    numerator = new_probability - (original_probability * new_probability)
    denominator = original_probability - (original_probability * new_probability)
    weight = numerator / denominator
    return weight

# BKT con pesos que modifican los parámetros (probabilidades) del modelo
class WBKT:

    # Parámetros del modelo BKT tradicional    
    # p_l0 : Probabilidad inicial de aprendizaje o dominio a priori de la habilidad k
    # p_t : Probabilidad de transición de un estado de no dominio a un estado de dominio de la habilidad k
    # p_g : Probabilidad de adivinar la respuesta correcta, estando en un estado de no dominio de la habilidad k
    # p_s : Probabilidad de equivocarse, estando en un estado de dominio de la habilidad k
    # Asuma, por defecto, una probabilidad de 0.0 para cada uno de los parámetros del modelo BKT
    # t : Paso de tiempo discreto (comenzando desde t = 0)

    # Valor de referencia de la probabilidad de aprendizaje o dominio a priori de la habilidad k
    # p_lt : Probabilidad de aprendizaje o dominio a priori de la habilidad k

    # Parámetros de pesos que modifican a los parámetros del modelo BKT
    # w_l0 : Peso asociado a la probabilidad de aprendizaje o dominio a priori de la habilidad k
    # w_t : Peso asociado a la probabilidad de transición de un estado de no dominio a un estado de dominio de la habilidad k
    # w_g : Peso asociado a la probabilidad de adivinar la respuesta correcta, estando en un estado de no dominio de la 
    #   habilidad k
    # w_s : Peso asociado a la probabilidad de equivocarse, estando en un estado de dominio de la habilidad k

    # Constructor (Vacío o no vacío)
    def __init__(self, p_l0:float=0.0, p_t:float=0.0, p_g:float=0.0, p_s:float=0.0, 
        w_l0:float=1.0, w_t:float=1.0, w_g:float=1.0, w_s:float=1.0):

        # Los parámetros del modelo son probabilidades en el conjunto de los números reales 
        #   (i.e., sólo pueden estar entre 0.0 y 1.0)
        if (type(p_l0) != float or p_l0 < 0.0 or p_l0 > 1.0):
            raise TypeError('El argumento p_l0 debe ser un número real (i.e., float) que represente ' +
                'una probabilidad (i.e., un valor entre 0.0 y 1.0)')
        
        if (type(p_t) != float or p_t < 0.0 or p_t > 1.0):
            raise TypeError('El argumento p_t debe ser un número real (i.e., float) que represente ' +
                'una probabilidad (i.e., un valor entre 0.0 y 1.0)')

        if (type(p_g) != float or p_g < 0.0 or p_g > 1.0):
            raise TypeError('El argumento p_g debe ser un número real (i.e., float) que represente ' +
                'una probabilidad (i.e., un valor entre 0.0 y 1.0)')
        
        if (type(p_s) != float or p_s < 0.0 or p_s > 1.0):
            raise TypeError('El argumento p_s debe ser un número real (i.e., float) que represente ' +
                'una probabilidad (i.e., un valor entre 0.0 y 1.0)')

        # Los pesos asociados a los parámetros del modelo deben ser números reales (float)
        if (type(w_l0) != float):
            raise TypeError('El argumento w_l0 debe ser un número real (i.e., float)')
        
        if (type(w_t) != float):
            raise TypeError('El argumento w_t debe ser un número real (i.e., float)')

        if (type(w_g) != float):
            raise TypeError('El argumento w_g debe ser un número real (i.e., float)')
        
        if (type(w_s) != float):
            raise TypeError('El argumento w_s debe ser un número real (i.e., float)')

        self.__w_l0 = w_l0
        self.__w_t = w_t
        self.__w_g = w_g
        self.__w_s = w_s

        self.__p_l0 = p_l0        
        self.__p_t = p_t
        self.__p_g = p_g
        self.__p_s = p_s

        # Obtenga los valores ajustados por pesos de los parámetros del modelo
        updated_p_l0 = self.calculate_new_p_l0_given_weight()
        self.__p_l0 = updated_p_l0

        self.__t = 0
        # self.__p_lt = p_l0
        self.__p_lt = updated_p_l0
        self.__learned_state_probabilities = [self.__p_lt]
        self.__observations = [None]

    # Getters
    def get_p_l0(self):
        return self.__p_l0    

    def get_p_t(self):
        return self.__p_t

    def get_p_g(self):
        return self.__p_g

    def get_p_s(self):
        return self.__p_s

    def get_t(self):
        return self.__t

    def get_p_lt(self):
        return self.__p_lt

    def get_learned_state_probabilities(self):
        return self.__learned_state_probabilities

    def get_observations(self):
        return self.__observations

    def get_w_l0(self):
        return self.__w_l0    

    def get_w_t(self):
        return self.__w_t

    def get_w_g(self):
        return self.__w_g

    def get_w_s(self):
        return self.__w_s

    # Setters
    def set_w_l0(self, w_l0):
        self.__w_l0 = w_l0

    def set_w_t(self, w_t):
        self.__w_t = w_t

    def set_w_g(self, w_g):
        self.__w_g = w_g

    def set_w_s(self, w_s):
        self.__w_s = w_s

    #### MÉTODOS ####

    # Actualización del modelo BKT tradicional al obtener una observación
    def update_model(self, observation: bool=False):
        # Las observaciones que recibe el modelo son resultados de interacciones en donde se requiera usar la habilidad k,
        #   las cuales pueden ser correctas (True) o incorrectas (False)
        if (type(observation) != bool):
            raise TypeError('El argumento observation debe ser un valor booleano (True o False)')

        # Al obtener una observación, actualice el tiempo t
        self.__t = self.__t + 1

        # Obtenga los valores ajustados por pesos de los parámetros del modelo
        updated_p_t = self.calculate_new_p_t_given_weight()

        # Estime la probabilidad p(Ln) del dominio de la habilidad k del estudiante i para n = t
        posterior_ln = self.calculate_posterior(observation)
        # p_ln = posterior_ln + (1.0 - posterior_ln) * self.__p_t
        p_ln = posterior_ln + (1.0 - posterior_ln) * updated_p_t

        # Actualice el valor p_lt del modelo
        self.__p_lt = p_ln

        # Aañada la probabilidad p(Lt) la observación en el tiempo t, en sus respectivos arreglos
        self.__learned_state_probabilities.append(self.__p_lt)
        self.__observations.append(observation)
        
    # Calcule la probabilidad posterior de que un estudiante i esté en un estado en que ya dominó la habilidad k,
    #   dada la observación del resultado en un intento n (el último intento) hecho por el estudiante i al practicar la
    #   habilidad k.
    def calculate_posterior(self, observation):
        # Obtenga los valores ajustados por pesos de los parámetros del modelo
        updated_p_s = self.calculate_new_p_s_given_weight()
        updated_p_g = self.calculate_new_p_g_given_weight()

        # Dada una observación de resultado correcto
        previous_prior_learning_probab = self.__learned_state_probabilities[self.__t - 1]
        if (observation == True):
            # prior_learning_and_non_slip_probab = previous_prior_learning_probab * (1.0 - self.__p_s)
            prior_learning_and_non_slip_probab = previous_prior_learning_probab * (1.0 - updated_p_s)
            # non_prior_learning_and_guess_probab = (1.0 - previous_prior_learning_probab) * self.__p_g
            non_prior_learning_and_guess_probab = (1.0 - previous_prior_learning_probab) * updated_p_g
            return (prior_learning_and_non_slip_probab) / (
                prior_learning_and_non_slip_probab + non_prior_learning_and_guess_probab)
        # Dada una observación de resultado incorrecto
        else:
            # prior_learning_and_slip_probab = previous_prior_learning_probab * (self.__p_s)
            prior_learning_and_slip_probab = previous_prior_learning_probab * (updated_p_s)
            # non_prior_learning_and_non_guess_probab = (1.0 - previous_prior_learning_probab) * (1.0 - self.__p_g)
            non_prior_learning_and_non_guess_probab = (1.0 - previous_prior_learning_probab) * (1.0 - updated_p_g)
            return (prior_learning_and_slip_probab) / (
                prior_learning_and_slip_probab + non_prior_learning_and_non_guess_probab)

    def calculate_new_p_l0_given_weight(self):
        return calculate_new_probability_given_weight(self.__p_l0, self.__w_l0)

    def calculate_new_p_t_given_weight(self):
        return calculate_new_probability_given_weight(self.__p_t, self.__w_t)

    def calculate_new_p_g_given_weight(self):
        new_probability = calculate_new_probability_given_weight(self.__p_g, self.__w_g)
        # Para evitar la degeneración teórica del modelo WBKT
        if (new_probability > 0.49):
            return 0.49
        elif (new_probability < 0.01):
            return 0.01 # Esto es para evitar que la probabilidad sea exactamente 0.0
        else:
            return new_probability

    def calculate_new_p_s_given_weight(self):
        new_probability = calculate_new_probability_given_weight(self.__p_s, self.__w_s)
        # Para evitar la degeneración teórica del modelo WBKT
        if (new_probability > 0.49):
            return 0.49
        elif (new_probability < 0.01):
            return 0.01 # Esto es para evitar que la probabilidad sea exactamente 0.0
        else:
            return new_probability

    def find_pl_boundary_where_pl_cannot_decrease_with_wrong_answers(self, p_l_max: float, 
        max_iterations: int, p_l_precision: int):
        # print()
        # print('Procedimiento para encontrar el valor de p(L) a partir del cual no se puede seguir disminuyendo dicho ' 
        # + 'valor con respuestas incorrectas sucesivas:')        
        bkt_model_copy = WBKT(p_l0=p_l_max, p_t=self.get_p_t(), p_g=self.get_p_g(), p_s=self.get_p_s(), 
                              w_l0=self.get_w_l0(), w_t=self.get_w_t(), w_g=self.get_w_g(), w_s=self.get_w_s())
        starting_p_l = bkt_model_copy.get_p_lt()
        previous_p_l = starting_p_l
        # print('p(LN) = ' + str(starting_p_l))

        for i in range(1, max_iterations + 1):
            bkt_model_copy.update_model(False)
            if (round(bkt_model_copy.get_p_lt(), p_l_precision) != round(previous_p_l, p_l_precision)):
                # print('p(LN+' + str(i) + ') = ' + str(bkt_model_copy.get_p_lt())
                # + ' => ' + str(round(number=bkt_model_copy.get_p_lt(), ndigits=p_l_precision)))
                previous_p_l = bkt_model_copy.get_p_lt()
            else:
                # print('En la iteración N = ' + str(i) + ', el valor de p(Lt), con un redondeo de ' + str(p_l_precision) + 
                # ' dígitos, no sigue disminuyendo cuando se producen respuestas incorrectas sucesivas.')
                return previous_p_l
        
