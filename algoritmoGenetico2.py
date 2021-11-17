import random
import numpy as np

def binario_a_decimal(numero_binario):
    numero_decimal = 0
    if numero_binario[0] == '-':
        numero_binario = numero_binario.replace("-","")
    #print(numero_binario)
    for posicion, digito_string in enumerate(numero_binario[::-1]):
        numero_decimal += int(digito_string) * 2 ** posicion
    return numero_decimal

def inicializarPoblacion(nro_poblacion,nro_bits_individuo,min_rango,max_rango):
    fenotipo = [str(round(random.uniform(min_rango,max_rango),2)) for i in range(nro_poblacion)]
    genotipo = ["" for i in range(nro_poblacion)]

    for i in range(nro_poblacion):
        if fenotipo[i][0] == '-':
            separadorDecimal = fenotipo[i].find('.')
            binarioEntero = bin(int(fenotipo[i][1:separadorDecimal]))
            binarioDecimal = bin(int(fenotipo[i][separadorDecimal+1:]))
            binarioEntero = str(binarioEntero[2:])
            binarioDecimal = str(binarioDecimal[2:])
            binario = "-" + binarioEntero + "." + binarioDecimal
        else:
            separadorDecimal = fenotipo[i].find('.')
            binarioEntero = bin(int(fenotipo[i][0:separadorDecimal]))
            binarioDecimal = bin(int(fenotipo[i][separadorDecimal+1:]))
            binarioEntero = str(binarioEntero[2:])
            binarioDecimal = str(binarioDecimal[2:])
            binario = binarioEntero + "." + binarioDecimal

        cantidadCerosDecimal = 7 - len(binarioDecimal)
        cantBitsEntero = nro_bits_individuo - 7
        cantidadCerosEntero = cantBitsEntero - len(binarioEntero)
        agregarCerosEntero = ''
        for j in range(cantidadCerosEntero):
            agregarCerosEntero = agregarCerosEntero + '0'
        agregarCerosDecimal = ''
        for j in range(cantidadCerosDecimal):
            agregarCerosDecimal = agregarCerosDecimal + '0'
        genotipo[i] = genotipo[i] + agregarCerosEntero + binario + agregarCerosDecimal
    return genotipo,fenotipo

def evaluarFitness(nro_poblacion, fenotipoX, fenotipoY, funcion):
    fitness = np.zeros(nro_poblacion)
    for i in range(nro_poblacion):
        fitness[i] = funcion(float(fenotipoX[i]), float(fenotipoY[i]))

    fitness = -fitness
    idx_mejor_fitness = np.argmax(fitness,axis=None)
    mejor_fitness = fitness[idx_mejor_fitness]
    return fitness,mejor_fitness,idx_mejor_fitness

def decodificar(nro_poblacion, genotipo):
    fenotipo = ["" for i in range(nro_poblacion)]
    for i in range(nro_poblacion):
        signoMenos = genotipo[i].find('-')
        separadorDecimal = genotipo[i].find('.')
        parteEntera = genotipo[i][0:separadorDecimal]
        parteDecimal = genotipo[i][separadorDecimal + 1:]
        if signoMenos != -1:
            parteEntera = parteEntera.replace('-', "")
            parteEntera = "-" + str(binario_a_decimal(parteEntera))
        else:
            parteEntera = str(binario_a_decimal(parteEntera))
        parteDecimal = str(binario_a_decimal(parteDecimal))
        fenotipo[i] = parteEntera + "." + parteDecimal
    return fenotipo

def seleccionProgenitor(nro_poblacion, fitness, metodo_seleccion, nro_seleccion, nro_competencia):
    cromosomaElegido = np.zeros(nro_seleccion)
    # Selección de progenitores
    # Ruleta
    if metodo_seleccion == 0:
        p = np.zeros(nro_poblacion)
        q = np.zeros(nro_poblacion)
        # Probabilidad para el cromosoma i
        for i in range(nro_poblacion):
            p[i] = fitness[i] / sum(fitness)
            for k in range(0, i):
                q[i] = q[i] + p[k]
        for j in range(nro_seleccion):
            r = random.random()
            for i in range(1, nro_poblacion):
                if q[i - 1] < r <= q[i]:
                    cromosomaElegido[j] = i

    # Ventanas
    if metodo_seleccion == 1:
        contador = 0
        idx_sortFitness = np.argsort(fitness, axis=None)
        saltos_ventana = int(nro_poblacion / nro_seleccion)
        for i in range(nro_poblacion, 0, -saltos_ventana):
            idx_sortFitness = idx_sortFitness[0:i]
            cromosomaElegido[contador] = random.choice(idx_sortFitness)
            contador = contador + 1

    # Competencias
    if metodo_seleccion == 2:
        for i in range(nro_seleccion):
            # Elijo "nro_competencia" competidores al azar
            idx_competencia = np.random.randint(nro_poblacion, size=nro_competencia)
            # Elijo el de mejor fitness
            fitness_competencia = np.zeros(nro_competencia)
            for k in range(nro_competencia):
                fitness_competencia[k] = fitness[idx_competencia[k]]
            maxIndice = np.argmax(fitness_competencia)
            cromosomaElegido[i] = idx_competencia[maxIndice]

    cromosomaElegido = cromosomaElegido.astype(int)
    return cromosomaElegido

def reproduccion(progenitores,genotipo,nro_bits_individuo,nro_poblacion,prob_cruza,prob_mutacion,min_rango,max_rango,puntoInicialCruzayMuta):
    hijos = ["" for i in range(nro_poblacion)]
    padres = ["" for i in range(2)]
    cantProgenitores = len(progenitores)
    for i in range(0,nro_poblacion,2):
        # Selecciono los padres de a pares
        # Elijo 2 padres al azar
        idx_padre1 = random.randint(0,cantProgenitores-1)
        idx_padre2 = random.randint(0,cantProgenitores-1)
        padres[0] = genotipo[idx_padre1]
        padres[1] = genotipo[idx_padre2]

        # Cruza
        prob = random.random()
        hijos[i] = padres[0]
        hijos[i+1] = padres[1]
        puntoInicialCruzayMuta = 6
        if prob < prob_cruza:
            puntoCruza = random.randint(puntoInicialCruzayMuta,nro_poblacion-1)
            padre1 = padres[0]
            padre2 = padres[1]
            signoMenos1 = padre1.find('-')
            signoMenos2 = padre2.find('-')
            padre1 = padre1.replace("-","")
            padre2 = padre2.replace("-","")
            padre1_primerParte = padre1[0:puntoCruza]
            padre1_segundaParte = padre1[puntoCruza:]
            padre2_primerParte = padre2[0:puntoCruza]
            padre2_segundaParte = padre2[puntoCruza:]
            hijos[i] = padre1_primerParte+padre2_segundaParte
            hijos[i+1] = padre2_primerParte+padre1_segundaParte
            if signoMenos1 != -1:
                hijos[i] = '-' + hijos[i]
            if signoMenos2 != -1:
                hijos[i+1] = '-' + hijos[i+1]

        # Mutación
        if prob < prob_mutacion:
            puntoMutacion = random.randint(puntoInicialCruzayMuta,nro_poblacion-1)
            hijo1 = hijos[i]
            hijo2 = hijos[i+1]
            while(hijo1[puntoMutacion]=='.'): #Si el punto de mutacion es justo el ".", elegir otro punto
                puntoMutacion = random.randint(puntoInicialCruzayMuta, nro_poblacion - 1)
            if hijo1[puntoMutacion] == '0':
                hijo1 = hijo1[0:puntoMutacion] + '1' + hijo1[puntoMutacion+1:]
            else:
                hijo1 = hijo1[0:puntoMutacion] + '0' + hijo1[puntoMutacion+1:]
            if hijo2[puntoMutacion] == '0':
                hijo2 = hijo2[0:puntoMutacion] + '1' + hijo2[puntoMutacion+1:]
            else:
                hijo2 = hijo2[0:puntoMutacion] + '0' + hijo2[puntoMutacion+1:]
            hijos[i] = hijo1
            hijos[i+1] = hijo2

    return hijos

def reemplazoPoblacional(nro_poblacion, hijosX, hijosY, idx_mejor_fitness, genotipoX, genotipoY):
    # Elitismo: Busco el mejor individuo y lo paso directamente
    # Tengo que eliminar un individuo para mantener el tamaño de la poblacion,
    # para eso elimino uno al azar
    nuevaGeneracionX = hijosX
    nuevaGeneracionY = hijosY
    eliminarHijo = random.randint(0, nro_poblacion - 1)
    nuevaGeneracionX[eliminarHijo] = genotipoX[idx_mejor_fitness]
    nuevaGeneracionY[eliminarHijo] = genotipoY[idx_mejor_fitness]
    return nuevaGeneracionX, nuevaGeneracionY



def algoritmoGenetico2(nro_poblacion, nro_bits_individuo, nro_seleccion, nro_competencia, prob_cruza, prob_mutacion,
                      it_max, min_rango, max_rango, funcion, metodo_seleccion, fitness_buscado, puntoInicialCruzayMuta):

    # Inicializar problación
    genotipoX, fenotipoX = inicializarPoblacion(nro_poblacion,nro_bits_individuo,min_rango,max_rango)
    genotipoY, fenotipoY = inicializarPoblacion(nro_poblacion,nro_bits_individuo,min_rango,max_rango)
    #print(fenotipo)
    #print(genotipo)

    # Evaluar función de Fitness
    fitness, mejor_fitness, idx_mejor_fitness = evaluarFitness(nro_poblacion, fenotipoX, fenotipoY, funcion)
    #print(fitness)

    it = 0
    while it < it_max and mejor_fitness < fitness_buscado:
        # print(it)
        # Seleccionar progenitores
        progenitores = seleccionProgenitor(nro_poblacion, fitness, metodo_seleccion, nro_seleccion, nro_competencia)

        # Reproducción
        hijosX = reproduccion(progenitores, genotipoX, nro_bits_individuo, nro_poblacion, prob_cruza, prob_mutacion,
                             min_rango, max_rango, puntoInicialCruzayMuta)
        hijosY = reproduccion(progenitores, genotipoY, nro_bits_individuo, nro_poblacion, prob_cruza, prob_mutacion,
                             min_rango, max_rango, puntoInicialCruzayMuta)

        # Reemplazo poblacional (Elitismo)
        genotipoX, genotipoY = reemplazoPoblacional(nro_poblacion, hijosX, hijosY, idx_mejor_fitness, genotipoX, genotipoY)

        # Evaluar población
        fenotipoX = decodificar(nro_poblacion, genotipoX)
        fenotipoY = decodificar(nro_poblacion, genotipoY)
        fitness, mejor_fitness, idx_mejor_fitness = evaluarFitness(nro_poblacion, fenotipoX, fenotipoY, funcion)

        it = it + 1

    return mejor_fitness, fenotipoX[idx_mejor_fitness], fenotipoY[idx_mejor_fitness]