import DifficultyV3

# Máquina de dificultades genérica
class DifficultyMachine:

    ## Estados especiales
    # Inicio
    START_STATE = "START"
    # Fin
    END_STATE = "END"

    # Constructor (Vacío o no vacío)
    def __init__(self, difficulty_levels:list):
        if self.is_difficulty_level_list_valid(difficulty_levels) == False:
            raise ValueError('El argumento difficulty_levels debe ser una lista válida de dificultades')
        
        self.__difficulty_levels = []
        self.__difficulty_levels.append(self.START_STATE)
        self.__difficulty_levels.extend(difficulty_levels)
        self.__difficulty_levels.append(self.END_STATE)

        self.__current_state = self.__difficulty_levels[0]

    # Getters
    def get_difficulty_levels(self):
        return self.__difficulty_levels

    def get_difficulty_level_tags(self):
        difficulty_level_numbers_list = []
        for dl in self.__difficulty_levels:
            if dl == self.START_STATE or dl == self.END_STATE:
                difficulty_level_numbers_list.append(dl)
            else:
                difficulty_level_numbers_list.append(dl.get_difficulty_level())
        return difficulty_level_numbers_list

    def get_current_state(self):
        return self.__current_state

    def get_current_state_tag(self):
        if self.__current_state == self.START_STATE or self.__current_state == self.END_STATE:
            return self.__current_state
        else:
            return self.__current_state.get_difficulty_level()

    # Setters
    def set_current_state(self, state):
        self.__current_state = state

    def is_difficulty_level_list_valid(self, difficulty_levels:list):
        if type(difficulty_levels) == list:
            if len(difficulty_levels) > 0:
                for d in difficulty_levels:
                    if type(d) != DifficultyV3.Difficulty or type(d.get_difficulty_level()) != int:
                        return False
                
                for i in range(0, len(difficulty_levels) - 1):
                    for j in range(i + 1, len(difficulty_levels)):
                        if difficulty_levels[i].get_difficulty_level() == difficulty_levels[j].get_difficulty_level():
                            return False
                
                return True

        return False

    def get_superior_difficulty(self):
        index = self.get_state_index(self.get_current_state())
        if index == -1:
            return False
        elif index + 1 == len(self.get_difficulty_levels()):
            return False
        else:
            return self.get_difficulty_levels()[index + 1]

    def increase_difficulty(self):
        index = self.get_state_index(self.get_current_state())
        if index == -1:
            return False
        elif index + 1 == len(self.get_difficulty_levels()):
            return False
        else:
            self.__current_state = self.get_difficulty_levels()[index + 1]
            return True

    def get_inferior_difficulty(self):
        index = self.get_state_index(self.get_current_state())
        if index == -1:
            return False
        elif index - 1 == -1:
            return False
        else:
            return self.get_difficulty_levels()[index - 1]

    def decrease_difficulty(self):
        index = self.get_state_index(self.get_current_state())
        if index == -1:
            return False
        elif index - 1 == -1:
            return False
        else:
            self.__current_state = self.get_difficulty_levels()[index - 1]
            return True

    def get_state_index(self, state):
        if state == self.START_STATE:
            return 0
        elif state == self.END_STATE:
            return len(self.get_difficulty_levels()) - 1
        else:
            try:
                return self.get_difficulty_levels().index(state)
            except ValueError:
                return -1

    def is_on_start_state(self):
        if self.get_current_state() == self.START_STATE:
            return True
        else:
            return False
    
    def is_on_end_state(self):
        if self.get_current_state() == self.END_STATE:
            return True
        else:
            return False
