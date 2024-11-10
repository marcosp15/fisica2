import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sympy as sp

def campo_alambre(I, L, P):
    """Calcula el campo magnético de un alambre recto en un punto P."""
    mu0 = 4 * np.pi * 10**-7
    x, y, z = P
    r = np.sqrt(x**2 + y**2)

    if r == 0:
        return np.array([0, 0, 0])
    
    B_x = mu0 * I / (2 * np.pi * r) * (L / (np.sqrt(r**2 + (L/2)**2)))
    return np.array([B_x, 0, 0])

def campo_espira(I, a, P):
    """Calcula el campo magnético de una espira circular en un punto P."""
    mu0 = 4 * np.pi * 10**-7
    x, y, z = P
    r = np.sqrt(x**2 + y**2)

    def integrando(theta):
        x_s = a * np.cos(theta)
        y_s = a * np.sin(theta)
        dl = np.array([-a * np.sin(theta), a * np.cos(theta), 0])
        r_vec = np.array([x - x_s, y - y_s, z])
        r_hat = r_vec / np.linalg.norm(r_vec)
        dB = (mu0 * I / (4 * np.pi)) * np.cross(dl, r_hat) / np.linalg.norm(r_vec)**2
        return dB

    B = np.zeros(3)
    for theta in np.linspace(0, 2 * np.pi, 1000):
        B += integrando(theta)
    return B

def campo_total(B1, B2):
    """Suma vectorial de dos campos magnéticos."""
    return B1 + B2

def graficar_campo(B_func, rango, title=""):
    """Grafica el campo magnético en 3D y la componente Z en 2D."""
    x = np.linspace(rango[0][0], rango[0][1], 10)
    y = np.linspace(rango[1][0], rango[1][1], 10)
    z = np.linspace(rango[2][0], rango[2][1], 10)
    X, Y, Z = np.meshgrid(x, y, z)

    Bx, By, Bz = np.zeros(X.shape), np.zeros(Y.shape), np.zeros(Z.shape)
    for i in range(X.shape[0]):
        for j in range(Y.shape[1]):
            for k in range(Z.shape[2]):
                B = B_func((X[i, j, k], Y[i, j, k], Z[i, j, k]))
                Bx[i, j, k], By[i, j, k], Bz[i, j, k] = B

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.quiver(X, Y, Z, Bx, By, Bz, length=0.5, normalize=True)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(title)
    plt.show()

    plt.figure()
    plt.contourf(X[:, :, 0], Y[:, :, 0], Bz[:, :, 0], cmap='viridis')
    plt.colorbar()
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(f"{title} - Componente Z")
    plt.show()

# Parámetros
I1, L = 1, 2  # Alambre
I2, a = 2, 1  # Espira
rango = [(-3, 3), (-3, 3), (-3, 3)]

# Graficar campos individuales
graficar_campo(lambda P: campo_alambre(I1, L, P), rango, "Campo magnético del alambre")
graficar_campo(lambda P: campo_espira(I2, a, P), rango, "Campo magnético de la espira")
graficar_campo(lambda P: campo_total(campo_alambre(I1, L, P), campo_espira(I2, a, P)), rango, "Campo magnético total")

# Cálculo simbólico en un punto genérico (x1, y1, z1)
x1, y1, z1 = sp.symbols('x1 y1 z1')
P_simb = (x1, y1, z1)
# Campo del alambre en forma simbólica
B_alambre_simb = campo_alambre(I1, L, P_simb)
# Campo de la espira en forma simbólica
B_espira_simb = campo_espira(I2, a, P_simb)
print("Campo magnético del alambre en forma simbólica:", B_alambre_simb)
print("Campo magnético de la espira en forma simbólica:", B_espira_simb)

# Bobinas de Helmholtz
def campo_bobinas_helmholtz(I, a, P):
    B1 = campo_espira(I, a, (P[0], P[1], P[2] - a/2))
    B2 = campo_espira(I, a, (P[0], P[1], P[2] + a/2))
    return campo_total(B1, B2)

graficar_campo(lambda P: campo_bobinas_helmholtz(I2, a, P), rango, "Campo magnético de Bobinas de Helmholtz")
