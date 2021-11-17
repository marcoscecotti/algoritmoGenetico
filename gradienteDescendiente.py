def gradienteDescendiente(nro_iteraciones,alpha,x_inicial,gradiente):
    x = x_inicial
    for i in range(nro_iteraciones):
        # Actualizar "x" usando gradiente descendente
        x = x - alpha * gradiente(x)

        if abs(gradiente(x)) < 0.01:
            print("Gradiente: ",gradiente(x))
            break

    return x