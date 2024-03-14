# KT
Este repositorio es una colección de módulos escritos en Python de los modelos BKT, PFA, WBKT y PFA+, y su integración con el programa de práctica de ejercicios de sumas. En particular, los modelos WBKT y PFA+ son nuevos modelos de trazabilidad de conocimiento, producto de un trabajo de tesis de maestría realizado por el autor de este mismo repositorio. A su vez, este repositorio contiene los módulos que fueron utilizados para las simulaciones y observaciones de los modelos en ese trabajo de tesis.

## Editores y Lenguajes Usados

Todos los módulos fueron originalmente implementados con Python 3.11.1, en el editor de Visual Studio Code. En los módulos empleados para simular los modelos BKT, PFA y PFA+ se usaron las librerías Matplotlib y NumPy para generar gráficos. En particular, las gráficas correspondientes a simulaciones con el modelo WBKT fueron generados en el simulador del BKT, porque se consideró que las funcionalidades de graficación de este simulador eran suficientes para ello, teniendo en cuenta que en el modelo WBKT se producen cambios en los parámetros de aprendizaje y de rendimiento (que son esencialmente parámetros de BKT), pero este aspecto puede mejorar.

## Módulos
### Módulos iniciales de práctica adaptativa de ejercicios de sumas

1. **arithmetic_ls_v1.py**: Sistema de práctica de ejercicios aritméticos - Sólo considera si la respuesta dada por el usuario es correcta o no.
2. **arithmetic_ls_v3.py**: Sistema de práctica de ejercicios aritméticos - Además de considerar si la respuesta dada por el usuario es correcta o no, también se considera el tiempo de respuesta del usuario frente al ejercicio y el número de intentos fallidos.

### Módulos BKT

1. **arithmetic_ls_v1_with_bkt.py**: Integración del modelo BKT en el sistema de práctica de ejercicios aritméticos (**arithmetic_ls_v1.py**).
2. **BKT.py**: Clase que permite generar y gestionar modelos BKT.
3. **bkt_simulator.py**: Módulo que se emplea como sandbox para hacer simulaciones o pruebas con el modelo BKT. Este módulo utiliza librerías de Matplotlib y NumPy para generar gráficos. Además, cuenta con funciones para verificar si un modelo BKT es válido o no, considerando, por ejemplo, si es teórica o empíricamente degenerado; y funciones que permiten encontrar valores mínimos y máximos de p(L) al producirse respuestas incorrectas y correctas sucesivas, respectivamente.

### Módulos PFA

1. **arithmetic_ls_v1_with_pfa.py**:  Integración del modelo PFA en el sistema de práctica de ejercicios aritméticos (**arithmetic_ls_v1.py**).
2. **PFA.py**: Clase que permite generar y gestionar modelos PFA.
3. **pfa_simulator.py**: Módulo que se emplea como sandbox para hacer simulaciones o pruebas con el modelo PFA. Este módulo utiliza librerías de Matplotlib y NumPy para generar gráficos relacionados con el número de respuestas correctas e incorrectas sucesivas requeridas para alcanzar el umbral de dominio o de refuerzo, respectivamente. Además, cuenta con funciones para hallar el número de respuestas correctas sucesivas mínimas para alcanzar el dominio en todas las habilidades (i.e., todos los niveles de dificultad, en general) a partir de un cierto valor inicial de p(m).

### Módulos WBKT

1. **arithmetic_ls_v3_with_wbkt.py**: Integración del nuevo modelo WBKT en el sistema de práctica de ejercicios aritméticos (**arithmetic_ls_v3.py**).
2. **WBKT.py**: Clase que permite generar y gestionar modelos WBKT.
3. **wbkt_simulator.py**: Módulo que se emplea como sandbox principal para hacer simulaciones o pruebas con el modelo WBKT.
4. **wbkt_simulator_paper_test.py**: Módulo de sandbox alternativo para probar el modelos WBKT. Este tiene un código y un funcionamiento muy semejante al módulo anterior.

### Módulos PFA+

1. **arithmetic_ls_v3_with_pfa_plus.py**: Integración del nuevo modelo PFA+ en el sistema de práctica de ejercicios aritméticos (**arithmetic_ls_v3.py**).
2. **PFAPlus.py**: Clase que permite generar y gestionar modelos PFA+.
3. **pfa_plus_simulator.py**: Módulo que se emplea como sandbox principal para hacer simulaciones o pruebas con el modelo PFA+. Este módulo utiliza librerías de Matplotlib y NumPy para generar gráficos relacionados con el número de respuestas correctas y rápidas (CR) sucesivas mínimas requeridas para alcanzar el umbral de dominio a partir de un valor p(m) inicial, así como el número de respuestas correctas y lentas (CL) para ello. Además, cuenta con funciones que permiten obtener simplemente el número de respuestas CR y CL sucesivas para alcanzar el dominio en todas las habilidades (i.e., niveles de dificultad).

### Módulos de graficación de las funciones logit de base Euler (e) y logística estándar (Usadas en los modelos PFA y PFA+)

1. **e_base_logit_function.py**: Módulo de soporte para graficar la función logit de base Euler (e). Este módulo utiliza librerías de Matplotlib y NumPy para generar gráficos.
2. **e_base_logit_function_v2.py**: Módulo de soporte para graficar la función logit de base Euler (e). Este módulo cumple una función similar al anterior, pero lo hace de una forma diferente. Por supuesto, este utiliza librerías de Matplotlib y NumPy para generar gráficos.
3. **standard_logistic_function.py**: Módulo de soporte para graficar la función logística estándar. Este módulo utiliza librerías de Matplotlib y NumPy para generar gráficos.

# Módulos sandbox de Matplotlib y NumPy

1. **matplotlib_test.py**: Módulo sandbox para probar la librería Matplotlib. Note que Matplotlib requiere NumPy.
2. **numpy_test.py**: Módulo sandbox para probar la librería NumPy

### Otros módulos

1. **ArithmeticExercise.py**: Clase que define a un ejercicio aritmético.
2. **ArithmeticExerciseGenerator.py**: Clase que permite generar ejercicios de sumas de forma aleatoria, teniendo en cuenta reglas definidas por nivel de dificultad.
3. **ArithmeticResponseV1Validator.py**: Evaluador automático de respuestas ante ejercicios de sumas usado en  **arithmetic_ls_v1.py**.
4. **ArithmeticResponseV1BKTValidator.py**: Evaluador automático de respuestas ante ejercicios de sumas usado en **arithmetic_ls_v1_with_bkt.py**.
5. **ArithmeticResponseV1PFAValidator.py**: Evaluador automático de respuestas ante ejercicios de sumas usado en **arithmetic_ls_v1_with_pfa.py**.
6. **ArithmeticResponseV3Validator.py**: Evaluador automático de respuestas ante ejercicios de sumas usado en  **arithmetic_ls_v3.py**.
7. **ArithmeticResponseV3BKTValidator.py**: Actualmente, no está en uso. De hecho, su código fuente es exactamente igual al de **ArithmeticResponseV3Validator.py**, así que se recomienda ignorarlo o eliminarlo.
8. **ArithmeticResponseV3WBKTValidator.py**: Evaluador automático de respuestas ante ejercicios de sumas usado en **arithmetic_ls_v3_with_wbkt.py**.
9. **ArithmeticResponseV3PFAPlusValidator.py**: Evaluador automático de respuestas ante ejercicios de sumas usado en **arithmetic_ls_v3_with_pfa_plus.py**.
10. **DataSaver.py**: Actualmente, no está en uso, y contiene errores. Este fue un intento para establecer una clase que permitiese almacenar los datos producidos en una simulación con los modelos PFA, BKT, WBKT o PFA+.
11. **Difficulty.py**: Clase que representa un nivel de dificultad. Esta es empleada en **arithmetic_ls_v1.py**, **arithmetic_ls_v3.py**, **arithmetic_ls_v1_with_bkt.py** y **arithmetic_ls_v1_with_pfa.py**, entre otros módulos.
12. **DifficultyV2.py**: Clase que representa un nivel de dificultad, pero no está en uso actualmente, y contiene errores.
13. **DifficultyV3.py**: Clase que representa un nivel de dificultad. Esta es empleada en **arithmetic_ls_v3_with_wbkt.py** y **arithmetic_ls_v3_with_pfa_plus.py**, entre otros módulos.
14. **DifficultyMachine.py**: Clase correspondiente a una máquina de estado que gestiona estados y transiciones entre niveles de dificultad. Esta es empleada en **arithmetic_ls_v1.py**, **arithmetic_ls_v3.py**, **arithmetic_ls_v1_with_bkt.py** y **arithmetic_ls_v1_with_pfa.py**, entre otros módulos.
15. **DifficultyMachineV2.py**: Clase correspondiente a una máquina de estado que gestiona estados y transiciones entre niveles de dificultad. Esta es empleada en **arithmetic_ls_v3_with_wbkt.py** y **arithmetic_ls_v3_with_pfa_plus.py**, entre otros módulos.
16. **ResponseValidatorDecision.py**: Clase que representa la decisión o el veredicto tomado por el evaluador automático ante la respuesta de un usuario. Esta clase es utilizada en **ArithmeticResponseV1Validator.py**, **ArithmeticResponseV1BKTValidator.py**,  **ArithmeticResponseV1PFAValidator.py** y **ArithmeticResponseV3Validator.py**.
17. **ResponseValidatorDecisionV2.py**: Clase que representa la decisión o el veredicto tomado por el evaluador automático ante la respuesta de un usuario. Esta clase es empleada en **ArithmeticResponseV3WBKTValidator.py** y **ArithmeticResponseV3PFAPlusValidator.py**; es decir, en los nuevos modelos WBKT y PFA+.
18. **Timer.py**: Clase que permite medir el tiempo transcurrido en segundos, semejante a un cronógrafo. Esta es empleada en **arithmetic_ls_v3.py**,  **arithmetic_ls_v3_with_wbkt.py** y **arithmetic_ls_v3_with_pfa_plus.py**.

## Cómo usar estos módulos

Estos módulos se pueden ejecutar con un intérprete de Python. En general, para usar o probar el programa de ejercicios de sumas, los modelos BKT, PFA, WBKT y PFA+, o su integración en el programa de ejercicios de sumas, se puede ejecutar directamente cualquiera de los módulos que no estén incluidos en el listado de **Otros módulos**, dependiendo de lo que se quiera revisar.

Por supuesto, también se recomienda revisar el código fuente de los módulos incluidos en **Otros módulos**, para entender mejor cómo funcionan los sistemas construidos en este repositorio.

Sin embargo, en el caso de aquellos módulos que requieran Matplotlib o NumPy, se recomienda el uso de ambientes virtuales (venv) en Python. Para ello, se puede seguir la documentación escrita a manera de comentarios en los archivos **numpy_test.py** y **matplotlib_test.py**, los cuales se encuentran en este repositorio. En particular, recomienda ver especialmente el [video en YouTube](https://www.youtube.com/watch?v=q6dnyS-Ailo "video en YouTube")  incluido en el primero de los dos archivos. En ambos archivos también se encuentra información básica sobre cómo comenzar a usar Matplotlib y NumPy en Python.

### Licencia

MIT.

### Autor

Leandro Alejandro Niebles Carbonó (GitHub: carbonol).
