# Interfaz_UI/dashboard_ui.py
from PIL import Image, ImageTk  #Ver si tenemos Pillow instalado (pip install Pillow)
from tkinter import filedialog # Para abrir el explorador de archivos
from tkinter import messagebox # Para mostrar mensajes al usuario
import tkinter as tk

class DashboardScreen:
    def __init__(self, master, on_close_callback):
        self.master = master
        self.on_close_callback = on_close_callback  # Callback para cerrar la aplicación
        self.frame = tk.Frame(master, bg="#0c0c2b", padx=20, pady=20) # Un frame para contener los widgets


        tk.Label(self.frame, text="¡Bienvenido al Dashboard!", font=("Arial", 18)).pack(pady=20)
        tk.Label(self.frame, text="Aquí es donde irá el contenido principal de tu proyecto.").pack()
        # Puedes añadir más widgets aquí para tu proyecto.

        #Frame para contener los elementos en este caso una imagen que cargaremos(a la derecha)
        self.image_display_frame = tk.Frame(self.frame, bg="#AADDFF", bd=2, relief="groove", width=700, height=750) #Tamaños ideales por el momento
        self.image_display_frame.pack(side="right", padx=10, pady=10)
        # self.image_display_frame.pack_propagate(False)  # puedes usar pack_propagate(False) en el frame. Esto es opcional y depende de tu diseño deseado.

        # Configuración del grid dentro de image_display_frame
        # Esto define cómo se distribuye el espacio en filas y columnas

        # self.image_display_frame.grid_rowconfigure(0, weight=0)  # Fila del título, no se expande
        # self.image_display_frame.grid_rowconfigure(1, weight=0)  # Fila del botón, no se expande
        # self.image_display_frame.grid_rowconfigure(2, weight=1)  # Fila de la imagen, se expande verticalmente
        # self.image_display_frame.grid_columnconfigure(0, weight=1)  # Única columna, se expande horizontalmente
        # Etiquetas y Botones dentro de image_display_frame usando grid
        tk.Label(self.image_display_frame, text="Vista de Imagen", font=("Arial", 12), bg="#AADDFF").grid(row=0,
                                                                                                          column=0,
                                                                                                          pady=5)

        tk.Button(self.image_display_frame, text="Cargar Imagen", command=self._load_image_from_file).grid(row=1,
                                                                                                           column=0,
                                                                                                           pady=5)

        # Label para mostrar la imagen (se expandirá para llenar su celda grid)
        self.image_label = tk.Label(self.image_display_frame, bg="#DDDDDD")
        self.image_label.grid(row=2, column=0, pady=10, padx=10,
                              sticky="nsew")  # 'sticky' hace que ocupe todo el espacio de la celda

        # Añadir un botón para cerrar la aplicación
        tk.Button(self.frame, text="Cerrar Aplicación", command=self.on_close_callback).pack(pady=20)


    def _load_image_from_file(self):
        """Abre un diálogo de archivo para seleccionar una imagen y la muestra."""
        file_path = filedialog.askopenfilename(
            title="Seleccionar Imagen",
            filetypes=(("Archivos de imagen", "*.png *.jpg *.jpeg *.gif *.bmp"), ("Todos los archivos", "*.*"))
        )
        if file_path:
            try:
                # Abrir la imagen con PIL
                img = Image.open(file_path)

                # Actualizar las tareas pendientes de Tkinter para obtener las dimensiones correctas del label
                self.image_label.update_idletasks()
                label_width = self.image_label.winfo_width()
                label_height = self.image_label.winfo_height()

                # Fallback si las dimensiones no están listas (ej. al inicio de la app)
                # Usamos el tamaño del frame de la imagen menos un margen para el label
                if label_width == 0 or label_height == 0:
                    label_width = self.image_display_frame.winfo_width() - 20 # Restar padding horizontal
                    label_height = self.image_display_frame.winfo_height() - (5 + 5 + 10 + 5) - 20 # Restar alturas de otros widgets y padding vertical

                # Asegurarse de que las dimensiones no sean negativas
                label_width = max(1, label_width)
                label_height = max(1, label_height)


                # Redimensionar la imagen para que quepa en el Label dinámicamente
                max_size_for_label = (label_width, label_height)
                img.thumbnail(max_size_for_label, Image.Resampling.LANCZOS)

                # Convertir la imagen de PIL a un formato que Tkinter pueda usar
                self.tk_image = ImageTk.PhotoImage(img)

                # Mostrar la imagen en el Label
                self.image_label.config(image=self.tk_image)
                self.image_label.image = self.tk_image  # Mantener una referencia para evitar que sea recolectada por el GC
            except Exception as e:
                messagebox.showerror("Error al Cargar Imagen", f"No se pudo cargar la imagen: {e}")

    def show(self):
        """Muestra esta pantalla."""
        self.frame.pack(expand=True, fill="both") # Empaqueta el frame para que sea visible

    def hide(self):
        """Oculta esta pantalla."""
        self.frame.pack_forget() # Desempaqueta el frame para que no sea visible
