import numpy as np
import matplotlib.pyplot as plt
from tkinter import Frame, Tk, Label, Entry, Button, messagebox

# Constante de Coulomb
k_e = 8.99e9  # N m^2 / C^2

def calcular_campo_electrico(cargas, posiciones_cargas, punto):
    """
    Calcula el campo eléctrico resultante en un punto dado debido a varias cargas puntuales.
    """
    campo_total = np.array([0.0, 0.0])
    punto = np.array(punto)
    
    for carga, pos_carga in zip(cargas, posiciones_cargas):
        pos_carga = np.array(pos_carga)
        r_vector = punto - pos_carga
        r_magnitud = np.linalg.norm(r_vector)
        r_unitario = r_vector / r_magnitud
        E_i = (k_e * carga / r_magnitud**2) * r_unitario
        campo_total += E_i
    
    return campo_total

def potencial_electrico(cargas, posicion_cargas, punto):
    """
    Calcula el potencial electrico desde un punto dadas las cargas electricas y sus posiciones
    """
    pot_elec = 0.0
    punto = np.array(punto)

    for carga, pos_carga in zip(cargas,posicion_cargas):
        pos_carga = np.array(pos_carga)
        r_vector = punto - pos_carga
        r_magnitud = np.linalg.norm(r_vector)
        V_i = (k_e * carga) / r_magnitud
        pot_elec += V_i

    return pot_elec

def graficar_lineas_campo(cargas, posiciones_cargas):
    """
    Genera y muestra un gráfico de las líneas de campo eléctrico para las cargas dadas.
    """
    tamaño_rejilla = 0.05
    
    posiciones_array = np.array(posiciones_cargas)
    x_min, y_min = np.min(posiciones_array, axis=0)
    x_max, y_max = np.max(posiciones_array, axis=0)
    
    rango_max = max(x_max - x_min, y_max - y_min)
    margen = rango_max * 0.2

    if rango_max == 0:  # Si todas las cargas están en el mismo punto
        margen = 1.0
        rango_max = 1.0

    rango_x = (x_min - margen, x_min + rango_max + margen)
    rango_y = (y_min - margen, y_min + rango_max + margen)
    
    x = np.arange(rango_x[0], rango_x[1], tamaño_rejilla)
    y = np.arange(rango_y[0], rango_y[1], tamaño_rejilla)
    X, Y = np.meshgrid(x, y)
    
    U = np.zeros(X.shape)
    V = np.zeros(Y.shape)
    
    for i in range(X.shape[0]):
        for j in range(Y.shape[1]):
            punto = (X[i, j], Y[i, j])
            E = calcular_campo_electrico(cargas, posiciones_cargas, punto)
            U[i, j] = E[0]
            V[i, j] = E[1]
    
    fig, ax = plt.subplots(figsize=(8, 8))  # Forzar que el gráfico sea un cuadrado
    strm = ax.streamplot(X, Y, U, V, color='b', linewidth=1, density=2)
    
    for (x, y), carga in zip(posiciones_cargas, cargas):
        ax.scatter(x, y, color='r' if carga > 0 else 'b', s=100, edgecolor='k', zorder=2)
    
    ax.set_title('Líneas de Campo Eléctrico')
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_xlim(rango_x)
    ax.set_ylim(rango_y)
    ax.set_aspect('equal', 'box') #Esto fuerza proporciones iguales para x e y
    ax.grid(True)
    #plt.colorbar(strm.lines, ax=ax, label='Magnitud del Campo Eléctrico')
    
    plt.show()

def graficar_potencial_electrico(cargas, posiciones_cargas):
    """
    Genera y muestra el gráfico del potencial eléctrico basado en las cargas dadas
    """
    tamaño_rejilla = 0.05
    
    posiciones_array = np.array(posiciones_cargas)
    x_min, y_min = np.min(posiciones_array, axis=0)
    x_max, y_max = np.max(posiciones_array, axis=0)
    
    rango_max = max(x_max - x_min, y_max - y_min)
    margen = rango_max * 0.2

    if rango_max == 0:  # Si todas las cargas están en el mismo punto
        margen = 1.0
        rango_max = 1.0

    rango_x = (x_min - margen, x_min + rango_max + margen)
    rango_y = (y_min - margen, y_min + rango_max + margen)
    
    x = np.arange(rango_x[0], rango_x[1], tamaño_rejilla)
    y = np.arange(rango_y[0], rango_y[1], tamaño_rejilla)
    X, Y = np.meshgrid(x, y)
    
    # Inicializamos la matriz 2D para almacenar los valores del potencial
    pot = np.zeros(X.shape)

    # Calcular el potencial en cada punto de la rejilla
    for i in range(X.shape[0]):
        for j in range(Y.shape[1]):
            punto = (X[i, j], Y[i, j])
            pot[i, j] = potencial_electrico(cargas, posiciones_cargas, punto)
    
    # Graficar el potencial eléctrico
    fig, ax = plt.subplots(figsize=(8, 8))  # Forzar que el gráfico sea un cuadrado
    strm = ax.contourf(X, Y, pot, levels=50, cmap='RdYlBu')  # Crear el gráfico de contorno
    
    ax.set_title('Potencial Eléctrico')
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_xlim(rango_x)
    ax.set_ylim(rango_y)
    ax.set_aspect('equal', 'box')  # Esto fuerza proporciones iguales para x e y

    plt.colorbar(strm, ax=ax, label='Magnitud del Potencial Eléctrico')
    plt.show()


def obtener_datos():
    """
    Obtiene los datos ingresados en la interfaz gráfica y muestra la gráfica.
    """
    try:
        num_cargas = int(entry_num_cargas.get())
        
        cargas = []
        posiciones_cargas = []
        
        for i in range(num_cargas):
            carga = float(entries_cargas[i].get())
            cargas.append(carga)
            x, y = map(float, entries_posiciones[i].get().split())
            posiciones_cargas.append((x, y))
        
        # Obtener el punto donde se quiere calcular el campo
        punto_x, punto_y = map(float, entry_punto.get().split())
        punto = (punto_x, punto_y)

        # Calcular el campo eléctrico total en el punto dado
        campo_total = calcular_campo_electrico(cargas, posiciones_cargas, punto)
        
        # Mostrar el campo total en la interfaz
        label_resultado.config(text=f"Campo Eléctrico Total en ({punto_x}, {punto_y}):\n({campo_total[0]:.3e} î + {campo_total[1]:.3e} ĵ) N/C", font=("Helvatica",14), fg="black")

        # Graficar las líneas de campo eléctrico
       # graficar_lineas_campo(cargas, posiciones_cargas)

        #Graficar el potencial eléctrico
        graficar_potencial_electrico(cargas, posiciones_cargas)
    
    except ValueError:
        messagebox.showerror("Entrada Inválida", "Por favor, ingrese valores válidos.")

def crear_campos():
    """
    Crea los campos para ingresar las cargas y posiciones, basado en el número de cargas.
    """
    try:
        num_cargas = int(entry_num_cargas.get())
        
        if num_cargas < 3:
            messagebox.showerror("Número de Cargas Inválido", "Debe ingresar al menos 3 cargas.")
            return
        
        for widget in frame_cargas.winfo_children():
            widget.destroy()
        
        global entries_cargas, entries_posiciones
        entries_cargas = []
        entries_posiciones = []
        
        for i in range(num_cargas):
            Label(frame_cargas, text=f"Carga {i+1}:").grid(row=i, column=0, padx=5, pady=5)
            entry_carga = Entry(frame_cargas)
            entry_carga.grid(row=i, column=1, padx=5, pady=5)
            entries_cargas.append(entry_carga)
            
            Label(frame_cargas, text=f"Posición {i+1} (x y):").grid(row=i, column=2, padx=5, pady=5)
            entry_posicion = Entry(frame_cargas)
            entry_posicion.grid(row=i, column=3, padx=5, pady=5)
            entries_posiciones.append(entry_posicion)

    except ValueError:
        messagebox.showerror("Entrada Inválida", "Por favor, ingrese un número válido de cargas.")

def crear_interfaz():
    """
    Crea la interfaz gráfica para solicitar datos al usuario.
    """
    global entry_num_cargas, entries_cargas, entries_posiciones, entry_punto, label_resultado, frame_cargas
    
    root = Tk()
    root.title("Datos para Cálculo del Campo Eléctrico y Potencial")
    
    Label(root, text="Número de Cargas:").grid(row=0, column=0, padx=10, pady=10)
    entry_num_cargas = Entry(root)
    entry_num_cargas.grid(row=0, column=1, padx=10, pady=10)
    
    Button(root, text="Cargar Valores", command=crear_campos).grid(row=0, column=2, padx=10, pady=10)
    
    Label(root, text="Cargas (en Coulombs):").grid(row=1, column=0, padx=10, pady=10)
    
    
    frame_cargas = Frame(root)
    frame_cargas.grid(row=1, column=1, columnspan=2, padx=10, pady=10)
    
    Label(root, text="Punto (x y):").grid(row=3, column=0, padx=10, pady=10)
    entry_punto = Entry(root)
    entry_punto.grid(row=3, column=1, padx=10, pady=10)
    
    Button(root, text="Calcular y Graficar", command=obtener_datos).grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    # Etiqueta para mostrar el resultado del campo eléctrico
    label_resultado = Label(root, text="",font=('Arial', 20), fg= '#0000FF')
    label_resultado.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

    root.mainloop()

# Ejecutar la interfaz gráfica
crear_interfaz()
