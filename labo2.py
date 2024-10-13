import numpy as np
import matplotlib.pyplot as plt

tolerancia = 1e-5

def metodo_relajacion_condiciones(nx, ny, iteraciones, bornes):
    """
    Aplica el método de relajación para resolver la ecuación de Laplace con condiciones de Dirichlet y Neumann.

    Parámetros:
    nx (int): Número de puntos en la dirección x (columnas).
    ny (int): Número de puntos en la dirección y (filas).
    iteraciones (int): Número de iteraciones para el método de relajación.
    bornes (list of tuples): Lista de superficies y potenciales para los bornes.

    Retorna:
    phi (2D array): Potencial eléctrico en la malla.
    """
    #Variable para que no supere la tolerancia
    max_cambio = 0

    # Inicialización del potencial en la malla con ceros
    phi = np.zeros((nx, ny))
    
    # Aplicar condiciones de Dirichlet en los bornes (potenciales fijos en superficies específicas)
    for region, potencial in bornes:
        for x, y in region:
            phi[x, y] = potencial
    
    # Iteración del método de relajación con condiciones de Neumann en los bordes
    for _ in range(iteraciones):
        # Crear una copia del potencial actual
        phi_new = phi.copy()
        # Actualizar el potencial en cada punto del interior de la malla
        for i in range(1, nx-1):
            for j in range(1, ny-1):
                if (i, j) not in [(x, y) for region, _ in bornes for x, y in region]:  # No actualizar los bornes
                    phi_new[i, j] = 0.25 * (phi[i+1, j] + phi[i-1, j] + phi[i, j+1] + phi[i, j-1]) # hace el promedio de sus vecinos
                    max_cambio = max(max_cambio, abs(phi_new[i,j]-phi[i,j]))
        # Aplicar condiciones de Neumann en los bordes:
        # Borde superior e inferior
        phi_new[0, :] = phi_new[1, :]    # Derivada nula en el borde superior
        phi_new[-1, :] = phi_new[-2, :]  # Derivada nula en el borde inferior
        
        # Borde izquierdo y derecho
        phi_new[:, 0] = phi_new[:, 1]    # Derivada nula en el borde izquierdo
        phi_new[:, -1] = phi_new[:, -2]  # Derivada nula en el borde derecho
        
        phi = phi_new

        if max_cambio < tolerancia:
            break
    return phi

def graficar_potencial(phi):
    """
    Grafica el potencial eléctrico en una malla 2D.

    Parámetros:
    phi (2D array): Potencial eléctrico en la malla.
    """
    plt.figure(figsize=(8, 8))
    # Graficar el mapa de colores del potencial
    plt.contourf(phi, 15, cmap='coolwarm')
    # Agregar barra de color
    plt.colorbar(label='Potencial (V)')
    plt.title('Distribución del Potencial Eléctrico con Bornes y Condiciones de Neumann')
    plt.xlabel('Puntos en la dirección x')
    plt.ylabel('Puntos en la dirección y')
    plt.show()
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    X, Y = np.meshgrid(range(phi.shape[1]), range(phi.shape[0]))
    ax.plot_surface(X, Y, phi, cmap='coolwarm')
    ax.set_title('Superficie del potencial eléctrico')
    plt.show()

# Parámetros de la malla
nx = 101  # Número de puntos en la dirección x (columnas)
ny = 161  # Número de puntos en la dirección y (filas)
iteraciones = 2000  # Número de iteraciones para la convergencia

# Lista de bornes como superficies y potenciales -> Bornes con condiciones de Dirichlet
# Ejemplo de superficies:
rectangulo = [(x, y) for x in range(20, 30) for y in range(20, 40)]  # Rectángulo
circulo = [(x, y) for x in range(nx) for y in range(ny) if (x-75)**2 + (y-75)**2 < 100]  # Círculo

bornes = [(rectangulo, 5.0), (circulo, -5.0)]

# Resolver el potencial eléctrico usando el método de relajación
potencial = metodo_relajacion_condiciones(nx, ny, iteraciones, bornes)

# Graficar el potencial
graficar_potencial(potencial)
