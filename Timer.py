import time

# Clase de cronógrafo (Medidor de tiempo transcurrido)
class Timer:

    # Constructor (Vacío o no vacío)
    def __init__(self):
        pass

    def start_new_timer(self):
        # Nota: Este tiempo es dado en segundos (float)
        self.__starting_time = time.monotonic_ns()

    def get_elapsed_time(self):
        # Nota: Este tiempo es dado en segundos (float)
        return time.monotonic_ns() - self.__starting_time

    def get_elapsed_time_in_seconds(self):
        # Nota: Este tiempo es dado en segundos (float)
        return (time.monotonic_ns() - self.__starting_time) / 1e9

# timer = Timer()
# timer.start_new_timer()
# input('Cuando quiera detener este cronógrafo, presione ENTER\n>> ')
# print(timer.get_elapsed_time_in_seconds())