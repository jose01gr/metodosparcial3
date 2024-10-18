import tkinter as tk
from tkinter import messagebox, ttk
import simpy
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Clase base para las simulaciones
# Clase base para las simulaciones
class Simulacion:
    def __init__(self, nombre):
        self.nombre = nombre

    def validar_entrada(self, valor, tipo):
        try:
            if tipo == 'int':
                return int(valor)
            elif tipo == 'float':
                return float(valor)
        except ValueError:
            messagebox.showerror("Error", f"Valor incorrecto para {tipo}")
            return None

class Peluqueria(Simulacion):
    def __init__(self):
        super().__init__('Peluquería')

    def simular(self, num_clientes, tiempo_min_atencion, tiempo_max_atencion, tiempo_llegada, num_peluqueros):
        env = simpy.Environment()
        peluqueros = simpy.Resource(env, capacity=num_peluqueros)

        tiempos_espera = []

        def cliente(env, nombre, peluqueros):
            llegada = env.now
            with peluqueros.request() as request:
                yield request
                espera = env.now - llegada
                tiempos_espera.append(espera)
                tiempo_atencion = random.uniform(tiempo_min_atencion, tiempo_max_atencion)
                yield env.timeout(tiempo_atencion)

        for i in range(num_clientes):
            env.process(cliente(env, f'Cliente {i}', peluqueros))
            yield env.timeout(random.expovariate(1.0 / tiempo_llegada))

        env.run()  # Ejecuta la simulación

        tiempo_promedio_espera = np.mean(tiempos_espera) if tiempos_espera else 0
        return float(tiempo_promedio_espera)

class Restaurante(Simulacion):
    def __init__(self):
        super().__init__('Restaurante')

    def simular(self, num_clientes, tiempo_min_atencion, tiempo_max_atencion, tiempo_llegada, num_cocineros):
        env = simpy.Environment()
        cocineros = simpy.Resource(env, capacity=num_cocineros)

        tiempos_espera = []

        def cliente(env, nombre, cocineros):
            llegada = env.now
            with cocineros.request() as request:
                yield request
                espera = env.now - llegada
                tiempos_espera.append(espera)
                tiempo_atencion = random.uniform(tiempo_min_atencion, tiempo_max_atencion)
                yield env.timeout(tiempo_atencion)

        for i in range(num_clientes):
            env.process(cliente(env, f'Cliente {i}', cocineros))
            yield env.timeout(random.expovariate(1.0 / tiempo_llegada))

        env.run()  # Ejecuta la simulación

        tiempo_promedio_espera = np.mean(tiempos_espera) if tiempos_espera else 0
        return float(tiempo_promedio_espera)

class SistemaRedes(Simulacion):
    def __init__(self):
        super().__init__('Sistema de Redes')

    def simular(self, num_paquetes, tiempo_proceso_min, tiempo_proceso_max, tiempo_llegada, num_servidores):
        env = simpy.Environment()
        servidores = simpy.Resource(env, capacity=num_servidores)

        tiempos_espera = []

        def paquete(env, nombre, servidores):
            llegada = env.now
            with servidores.request() as request:
                yield request
                espera = env.now - llegada
                tiempos_espera.append(espera)
                tiempo_proceso = random.uniform(tiempo_proceso_min, tiempo_proceso_max)
                yield env.timeout(tiempo_proceso)

        for i in range(num_paquetes):
            env.process(paquete(env, f'Paquete {i}', servidores))
            yield env.timeout(random.expovariate(1.0 / tiempo_llegada))

        env.run()  # Ejecuta la simulación

        tiempo_promedio_espera = np.mean(tiempos_espera) if tiempos_espera else 0
        return float(tiempo_promedio_espera)

# Simulación de Reacción Química (continua)
class ReaccionQuimica(Simulacion):
    def __init__(self):
        super().__init__('Reacción Química')

    def simular(self, num_moleculas, tiempo_min, tiempo_max):
        reacciones = []

        for _ in range(num_moleculas):
            tiempo_reaccion = random.uniform(tiempo_min, tiempo_max)
            reacciones.append(tiempo_reaccion)

        tiempo_promedio = np.mean(reacciones)

        # Crear gráfico
        return tiempo_promedio, reacciones

# Simulación de Reactor Nuclear (continua)
class ReactorNuclear(Simulacion):
    def __init__(self):
        super().__init__('Reactor Nuclear')

    def simular(self, num_reacciones, tiempo_min, tiempo_max):
        reacciones = []

        for _ in range(num_reacciones):
            tiempo_reaccion = random.uniform(tiempo_min, tiempo_max)
            reacciones.append(tiempo_reaccion)

        tiempo_promedio = np.mean(reacciones)

        # Crear gráfico
        return tiempo_promedio, reacciones

# Interfaz gráfica con Tkinter
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simulador de Sistemas")
        self.geometry("400x300")

        self.simulaciones = {
            'Peluquería': Peluqueria(),
            'Restaurante': Restaurante(),
            'Sistema de Redes': SistemaRedes(),
            'Reacción Química': ReaccionQuimica(),
            'Reactor Nuclear': ReactorNuclear()
        }

        self.crear_widgets()

    def crear_widgets(self):
        label = tk.Label(self, text="Selecciona una simulación:")
        label.pack(pady=10)

        self.combo_simulaciones = ttk.Combobox(self, values=list(self.simulaciones.keys()))
        self.combo_simulaciones.pack(pady=5)

        btn_simular = tk.Button(self, text="Simular", command=self.mostrar_dialogo)
        btn_simular.pack(pady=10)

    def mostrar_dialogo(self):
        simulacion = self.combo_simulaciones.get()
        if simulacion in self.simulaciones:
            SimulacionDialog(self, self.simulaciones[simulacion])

class SimulacionDialog(tk.Toplevel):
    def __init__(self, parent, simulacion):
        super().__init__(parent)
        self.simulacion = simulacion
        self.title(f"Simulación - {simulacion.nombre}")
        self.geometry("400x400")
        self.crear_widgets()

    def crear_widgets(self):
        self.inputs = []

        parametros = self.obtener_parametros()
        for i, (param, tipo) in enumerate(parametros):
            label = tk.Label(self, text=f"{param}:")
            label.grid(row=i, column=0, padx=10, pady=5)
            entry = tk.Entry(self)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.inputs.append((entry, tipo))

        btn_ejecutar = tk.Button(self, text="Ejecutar", command=self.ejecutar)
        btn_ejecutar.grid(row=len(parametros), columnspan=2, pady=10)

        self.resultado_frame = tk.Frame(self)
        self.resultado_frame.grid(row=len(parametros) + 1, columnspan=2, pady=10)

        # Label para mostrar el resultado
        self.resultado_label = tk.Label(self.resultado_frame, text="")
        self.resultado_label.pack()

    def obtener_parametros(self):
        if isinstance(self.simulacion, Peluqueria) or isinstance(self.simulacion, Restaurante) or isinstance(self.simulacion, SistemaRedes):
            return [("Número de clientes/paquetes", "int"), ("Tiempo mínimo atención/proceso", "int"),
                    ("Tiempo máximo atención/proceso", "int"), ("Tiempo entre llegadas", "int"),
                    ("Número de servidores/peluqueros/cocineros", "int")]
        elif isinstance(self.simulacion, ReaccionQuimica) or isinstance(self.simulacion, ReactorNuclear):
            return [("Número de moléculas/reacciones", "int"), ("Tiempo mínimo de reacción", "int"),
                    ("Tiempo máximo de reacción", "int")]

    def ejecutar(self):
        params = []
        for entry, tipo in self.inputs:
            valor = self.simulacion.validar_entrada(entry.get(), tipo)
            if valor is not None:
                params.append(valor)
            else:
                return

        # Ejecutar simulación
        if isinstance(self.simulacion, (ReaccionQuimica, ReactorNuclear)):
            resultado, reacciones = self.simulacion.simular(*params)
            self.mostrar_resultado(resultado, reacciones)
        else:
            resultado = self.simulacion.simular(*params)
            resultadolista = list(resultado)
            # Mostrar el tiempo promedio de espera en el Label
            self.resultado_label.config(text=f"Tiempo promedio de espera: {resultadolista}")

    def mostrar_resultado(self, resultado, reacciones):
        for widget in self.resultado_frame.winfo_children():
            widget.destroy()

        label = tk.Label(self.resultado_frame, text=f"Tiempo promedio de reacción: {resultado:.2f}")
        label.pack()

        fig, ax = plt.subplots(figsize=(5, 4))
        ax.plot(reacciones, marker='o', linestyle='-', label='Tiempo de Reacción')
        ax.axhline(np.mean(reacciones), color='r', linestyle='--', label='Promedio de Reacción')
        ax.set_title('Gráfico de Tiempos de Reacción')
        ax.set_xlabel('Número de Reacciones')
        ax.set_ylabel('Tiempo de Reacción')
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=self.resultado_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

if __name__ == "__main__":
    app = App()
    app.mainloop()
