import numpy as np
import matplotlib.pyplot as plt
from tkinter import Frame, Tk, Label, Entry, Button, messagebox

# Constante de Coulomb
k_e = 8.99e9  # N m^2 / C^2

def calcular_campo(cargas, posiciones_cargas, punto):
    """
    Campo eléctrico resultante en un punto dado debido a varias cargas puntuales.
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

def calcular_potencial(cargas, posicion_cargas, punto):
    """
    Potencial electrico desde un punto dadas las cargas electricas y sus posiciones
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

def graficar_campo_y_potencial(cargas, posiciones_cargas):
    """
    Gráfico combinado de las líneas de campo eléctrico
    y el potencial eléctrico para las cargas dadas, aplicando una transformación
    logarítmica al potencial para mejorar la visibilidad de los detalles.
    """
    tamaño_rejilla = 0.005
    
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
    
    # Inicializamos matrices para campo y potencial
    U = np.zeros(X.shape)
    V = np.zeros(Y.shape)
    pot = np.zeros(X.shape)

    # Calculo del campo eléctrico y el potencial en cada punto de la rejilla
    for i in range(X.shape[0]):
        for j in range(Y.shape[1]):
            punto = (X[i, j], Y[i, j])
            E = calcular_campo(cargas, posiciones_cargas, punto)
            U[i, j] = E[0]
            V[i, j] = E[1]
            pot[i, j] = calcular_potencial(cargas, posiciones_cargas, punto)

    # Aplicamos una transformación logarítmica al potencial eléctrico para mejorar detalles
    pot_transformado = np.log(np.abs(pot) + 1e-9)

    # Define los niveles para el contorno basados en el rango del potencial transformado
    pot_min, pot_max = np.min(pot_transformado), np.max(pot_transformado)
    niveles = np.linspace(pot_min, pot_max, 100)
    
    # Grafico de las líneas de campo y el potencial eléctrico transformado
    fig, ax = plt.subplots(figsize=(8, 8))  # Forzar que el gráfico sea un cuadrado

    # Contorno del potencial eléctrico
    strm_pot = ax.contour(X, Y, pot_transformado, levels=niveles, cmap='RdYlBu', alpha=0.75)

    # Líneas de campo eléctrico
    strm_campo = ax.streamplot(X, Y, U, V, color='k', linewidth=0.1, density=2)  # Aumentar densidad

    # Dibujo de las cargas
    for (x, y), carga in zip(posiciones_cargas, cargas):
        ax.scatter(x, y, color='r' if carga > 0 else 'b', s=100, edgecolor='k', zorder=2)
    
    ax.set_title('Líneas de Campo Eléctrico y Potencial Eléctrico ')
    ax.set_xlabel('X ')
    ax.set_ylabel('Y ')
    ax.set_xlim(rango_x)
    ax.set_ylim(rango_y)
    ax.set_aspect('equal', 'box')  # Esto fuerza proporciones iguales para x e y
 
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
        
        # Obtiene el punto donde se quiere calcular el campo
        punto_x, punto_y = map(float, entry_punto.get().split())
        punto = (punto_x, punto_y)

        # Calcula el campo eléctrico total en el punto dado
        campo_total = calcular_campo(cargas, posiciones_cargas, punto)
        
        # Muestra el campo total en la interfaz
        label_resultado.config(text=f"Campo Eléctrico Total en ({punto_x}, {punto_y}):\n({campo_total[0]:.3e} î + {campo_total[1]:.3e} ĵ) N/C", font=("Helvatica",14), fg="black")

        # Grafico de las líneas de campo eléctrico y el potencial eléctrico
        graficar_campo_y_potencial(cargas, posiciones_cargas)
        
    except ValueError:
        messagebox.showerror("Entrada Inválida", "Por favor, ingrese valores válidos.")

def crear_campos():
    """
    Campos para ingresar las cargas y posiciones, basado en el número de cargas.
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
    Interfaz gráfica para solicitar datos al usuario.
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

    
    label_resultado = Label(root, text="",font=('Arial', 20), fg= '#0000FF') # resultado del campo eléctrico
    label_resultado.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

    root.mainloop()


crear_interfaz()
