import ArithmeticExercise
import random

# Generador de ejercicios de aritmética
class ArithmeticExerciseGenerator:

    # Constructor (Vacío o no vacío)
    def __init__(self):
        pass

    def generate_exercise(self, difficulty:ArithmeticExercise.Difficulty.Difficulty):
        description = None
        correct_response = None

        if difficulty.get_difficulty_level() == 1:
            digit_1 = random.randint(0, 9)
            digit_2 = random.randint(0, 9)
            description = str(digit_1) + ' + ' + str(digit_2) + ' = '
            correct_response = digit_1 + digit_2

        elif difficulty.get_difficulty_level() == 2:
            digit_1 = random.randint(10, 99)
            digit_2 = random.randint(0, 9)
            order = random.randint(0, 1)
            if order == 0:
                temp = digit_1
                digit_1 = digit_2
                digit_2 = temp
            description = str(digit_1) + ' + ' + str(digit_2) + ' = '
            correct_response = digit_1 + digit_2

        elif difficulty.get_difficulty_level() == 3:
            digit_1 = random.randint(10, 99)
            digit_2 = random.randint(10, 99)
            description = str(digit_1) + ' + ' + str(digit_2) + ' = '
            correct_response = digit_1 + digit_2

        elif difficulty.get_difficulty_level() == 4:
            digit_1 = random.randint(100, 999)
            digit_2 = random.randint(10, 99)
            order = random.randint(0, 1)
            if order == 0:
                temp = digit_1
                digit_1 = digit_2
                digit_2 = temp
            description = str(digit_1) + ' + ' + str(digit_2) + ' = '
            correct_response = digit_1 + digit_2

        elif difficulty.get_difficulty_level() == 5:
            digit_1 = random.randint(100, 999)
            digit_2 = random.randint(100, 999)
            description = str(digit_1) + ' + ' + str(digit_2) + ' = '
            correct_response = digit_1 + digit_2

        elif difficulty.get_difficulty_level() == 6:
            digit_1 = random.randint(0, 9)
            digit_2 = random.randint(0, 9)
            description = str(digit_1) + ' * ' + str(digit_2) + ' = '
            correct_response = digit_1 * digit_2

        elif difficulty.get_difficulty_level() == 7:
            digit_1 = random.randint(10, 99)
            digit_2 = random.randint(0, 9)
            order = random.randint(0, 1)
            if order == 0:
                temp = digit_1
                digit_1 = digit_2
                digit_2 = temp
            description = str(digit_1) + ' * ' + str(digit_2) + ' = '
            correct_response = digit_1 * digit_2

        else:
            return None

        return ArithmeticExercise.ArithmeticExercise(description, difficulty, correct_response)

        
