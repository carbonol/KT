# BKT tradicional
class BKT:

    # Parámetros del modelo BKT tradicional
    # p_lt : Probabilidad de aprendizaje o dominio a priori de la habilidad k
    # p_t : Probabilidad de transición de un estado de no dominio a un estado de dominio de la habilidad k
    # p_g : Probabilidad de adivinar la respuesta correcta, estando en un estado de no dominio de la habilidad k
    # p_s : Probabilidad de equivocarse, estando en un estado de dominio de la habilidad k
    # Asuma, por defecto, una probabilidad de 0.0 para cada uno de los parámetros del modelo BKT
    # t : Paso de tiempo discreto (comenzando desde t = 0)

    # Constructor (Vacío o no vacío)
    def __init__(self, p_l0:float=0.0, p_t:float=0.0, p_g:float=0.0, p_s:float=0.0):

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

        self.__p_l0 = p_l0
        self.__p_lt = p_l0
        self.__p_t = p_t
        self.__p_g = p_g
        self.__p_s = p_s

        self.__t = 0
        self.__learned_state_probabilities = [self.__p_lt]
        self.__observations = [None]

    # Getters
    def get_p_l0(self):
        return self.__p_l0

    def get_p_lt(self):
        return self.__p_lt

    def get_p_t(self):
        return self.__p_t

    def get_p_g(self):
        return self.__p_g

    def get_p_s(self):
        return self.__p_s

    def get_t(self):
        return self.__t

    def get_learned_state_probabilities(self):
        return self.__learned_state_probabilities

    def get_observations(self):
        return self.__observations

    # # Setters
    # def set_p_lt(self, p_lt):
    #     self.__p_lt = p_lt

    # Actualización del modelo BKT tradicional al obtener una observación
    def update_model(self, observation: bool=False):
        # Las observaciones que recibe el modelo son resultados de interacciones en donde se requiera usar la habilidad k,
        #   las cuales pueden ser correctas (True) o incorrectas (False)
        if (type(observation) != bool):
            raise TypeError('El argumento observation debe ser un valor booleano (True o False)')

        # Al obtener una observación, actualice el tiempo t
        self.__t = self.__t + 1

        # Estime la probabilidad p(Ln) del dominio de la habilidad k del estudiante i para n = t
        posterior_ln = self.calculate_posterior(observation)
        p_ln = posterior_ln + (1.0 - posterior_ln) * self.__p_t

        # Actualice el valor p_lt del modelo
        self.__p_lt = p_ln

        # Aañada la probabilidad p(Lt) la observación en el tiempo t, en sus respectivos arreglos
        self.__learned_state_probabilities.append(self.__p_lt)
        self.__observations.append(observation)
        
    # Calcule la probabilidad posterior de que un estudiante i esté en un estado en que ya dominó la habilidad k,
    #   dada la observación del resultado en un intento n (el último intento) hecho por el estudiante i al practicar la
    #   habilidad k.
    def calculate_posterior(self, observation):
        # Dada una observación de resultado correcto
        previous_prior_learning_probab = self.__learned_state_probabilities[self.__t - 1]
        if (observation == True):
            prior_learning_and_non_slip_probab = previous_prior_learning_probab * (1.0 - self.__p_s)
            non_prior_learning_and_guess_probab = (1.0 - previous_prior_learning_probab) * self.__p_g
            return (prior_learning_and_non_slip_probab) / (
                prior_learning_and_non_slip_probab + non_prior_learning_and_guess_probab)
        # Dada una observación de resultado incorrecto
        else:
            prior_learning_and_slip_probab = previous_prior_learning_probab * (self.__p_s)
            non_prior_learning_and_non_guess_probab = (1.0 - previous_prior_learning_probab) * (1.0 - self.__p_g)
            return (prior_learning_and_slip_probab) / (
                prior_learning_and_slip_probab + non_prior_learning_and_non_guess_probab)