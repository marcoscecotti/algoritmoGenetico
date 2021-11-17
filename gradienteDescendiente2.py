def gradienteDescendiente2(nro_iteraciones,alpha,x_inicial,y_inicial,gradienteX,gradienteY):
    x = x_inicial
    y = y_inicial
    contador = 0
    for i in range(nro_iteraciones):
        # Actualizar "x" usando gradiente descendente
        x = x - alpha * gradienteX(x,y)
        y = y - alpha * gradienteY(x,y)

        if abs(gradienteX(x,y)) < 0.01 and abs(gradienteY(x,y)):
            print("Gradiente: (",gradienteX(x,y),",",gradienteY(x,y),")")
            break

    return x,y