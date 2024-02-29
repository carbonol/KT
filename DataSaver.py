import os

# Clase para almacenar datos
class DataSaver:

    # Constructor (Vacío o no vacío)
    def __init__(self, saved_data_files_dir_name:str, data_file_name:str, enable_messages:bool=False):
        if saved_data_files_dir_name == None or data_file_name == None:
            raise ValueError('No se proporcionaron valores de tipo str para los argumentos saved_data_files_dir_name ' +  
                'y data_file_name')
        elif type(saved_data_files_dir_name) != str or type(data_file_name) != str:
            raise TypeError('Los valores para los argumentos saved_data_files_dir_name y data_file_name deben ser cadenas ' +
                'de caracteres (str)')
        # Valida si el directorio indicado por el usuario para almacenar los datos existe o no en el sistema operativo.
        else:
            # if not os.path.exists(saved_data_files_dir_name):
            #     # Crea el directorio para almacenar los datos, según la ruta de directorio indicada por el usuario.
            #     os.makedirs(saved_data_files_dir_name)
            self.__saved_data_files_dir = saved_data_files_dir
            self.__data_file_name = data_file_name
            self.__enable_messages = enable_messages

    # Getters
    def get_saved_data_files_dir(self):
        return self.__saved_data_files_dir

    def get_data_file_name(self):
        return self.__data_file_name

    def get_enable_messages(self):
        return self.__enable_messages

    # Setters
    def set_saved_data_files_dir(self, saved_data_files_dir):
        self.__saved_data_files_dir = saved_data_files_dir

    def set_data_file_name(self, data_file_name):
        self.__data_file_name = data_file_name

    def set_enable_messages(self, enable_messages):
        self.__enable_messages = enable_messages

    # Métodos
    def write_data_in_data_file(self, data):
        with open(self.__saved_data_files_dir + '/' + self.__data_file_name, "w") as file_to_write:
            if data_array_index != len(data_array) - 1:
                file_to_write.write(data + '\n')

    def write_data_array_in_data_file(self, data_array, data_delimiter):
        with open(self.__saved_data_files_dir + '/' + self.__data_file_name, "w") as file_to_write:
            data_text_line = ''
            data_array_index = 0
            for data in data_array:
                if data_array_index != len(data_array) - 1:
                    file_to_write.write(data + data_delimiter)
                else:
                    file_to_write.write(data + '\n')
                data_array_index += 1
        
    def write_data_arrays_in_data_file(self, data_arrays, data_delimiter):
        with open(self.__saved_data_files_dir + '/' + self.__data_file_name, "w") as file_to_write:
            for data_array in data_arrays:
                data_text_line = ''
                data_array_index = 0
                for data in data_array:
                    if data_array_index != len(data_array) - 1:
                        file_to_write.write(data + data_delimiter)
                    else:
                        file_to_write.write(data + '\n')
                    data_array_index += 1  