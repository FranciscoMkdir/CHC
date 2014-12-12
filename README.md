Algoritmo Genético CHC
===

Para el aprendizaje de los clasificadores es fundamental proporcionar un conjunto de entrenamiento T, 
el cual algunas ocasiones tiene una gran mayoría de ejemplos de ciertas clases; en este caso, se dice que T es 
un conjunto desbalanceado.

El siguiente Algoritmo genético (CHC) encuentra un subconjunto balanceado, la función a utilizar para guiar la 
búsqueda del conjunto balanceado es la precisión (calidad de clasificación) obtenida con Naive Bayes 
al evaluar un conjunto de validación para cuantificar la calidad de los cromosomas.

Entrada
===
- Conjunto de datos (archivo .txt) a balancear, (N elementos, cada uno con
M atributos).
- Conjunto de validación (archivo) para guiar la búsqueda.

Salida
===
- Precisión de clasificación obtenida con T.
- Precisión de clasificación considerando el cromosoma inicial.
- Precisión de clasificación obtenida con conjunto balanceado.
- Índices (separados por “,”) del subconjunto de elementos que forman el
conjunto balanceado.
