
'''
private formas (ingredientes, maxCasillas):


Aproximacion por prototipos:
- primero tomar puntos semi azar (heuristico) y combinar las formas posibles segun min ingredientes y max casillas por trozo (multiplos??)
- segundo tomar el perimetro y estudiarlo
- intentar optimizar la correcta combinacion de formas continuas

situacion inicial:

- zonas con muchos tipos iguales (en este caso abajo a la izq)

heuristico:

-score final
-minimizar huecos
-evitar zonas conflictivas 


distribución:
24T
18M

valores manejados:
tipo: char
T= 1
M= 0
Ya tomado= -1

estructura de datos

-numpy matrix.py (datos) 
-guardar en formato de score (grupos ya tomados)

numero max grupos:
42/5 +- 9

limitacion de forma:

-horizontal/vertical
1) ---

2) ----

3) --

4) --
   --

5)-----

'''