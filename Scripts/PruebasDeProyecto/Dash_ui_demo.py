# dashboard_ui.py
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from click import command


# Convertimos la función en una clase que HEREDA de tk.Frame
# Ahora es un componente, no una aplicación completa.
class DashboardScreen(tk.Frame):
    def __init__(self, master, on_logout_callback):
        """
        El constructor ahora recibe el 'master' (la ventana principal)
        y un callback para cuando se presione 'Cerrar Sesión'.
        """
        # 1. Llamamos al constructor de la clase padre (tk.Frame)
        super().__init__(master, bg="#202060")
        self.on_logout_callback = on_logout_callback
        # Variable para seleccionar una imagen al buscar con el boton "upload_button"
        self.selected_image = None
        self.image_path = ""

        # 2. Toda la lógica de la UI ahora se construye sobre 'self' (el Frame)
        # en lugar de sobre una nueva 'window'.

        # --- Barra Superior (Encabezado) ---
        header_frame = tk.Frame(self, bg="#202060", height=80)
        header_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.grid_columnconfigure(1, weight=0)

        # Titulo del label
        title_label = tk.Label(header_frame, text="Detector de Ratas",
                               font=("Arial", 24, "bold"), fg="white", bg="#202060")
        title_label.grid(row=0, column=0, sticky="w", padx=(50, 0))

        # El botón ahora usa el callback que le pasamos
        close_button = tk.Button(header_frame, text="Cerrar Sesión",
                                 font=("Arial", 10), bg="white", fg="black", padx=10, pady=5,
                                 command=self.on_logout_callback)
        close_button.grid(row=0, column=1, sticky="e", padx=(0, 20))



        # --- Área Principal (Contenido con los dos paneles) ---
        main_content_frame = tk.Frame(self, bg="#A0D0E0", padx=20, pady=20)
        main_content_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
        main_content_frame.grid_columnconfigure(0, weight=1)
        main_content_frame.grid_columnconfigure(1, weight=1)
        main_content_frame.grid_rowconfigure(0, weight=1)

        # ... El resto de tu código de la UI del dashboard es exactamente igual,
        # solo asegúrate de que el 'master' de cada widget sea el frame correcto.
        # Por ejemplo, 'left_panel_frame = tk.Frame(main_content_frame, ...)'
        # lo cual ya es correcto.

        # --- 2.1. Panel Izquierdo ---
        left_panel_frame = tk.Frame(main_content_frame, bg="lightgray", bd=2, relief="solid")
        left_panel_frame.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
        detected_image_area = tk.Label(left_panel_frame, text="[Área de Imagen Detectada]", bg="lightgray", fg="gray",
                                       relief="sunken", bd=1)
        detected_image_area.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        # Nivel de coincidencia
        coincidence_label = tk.Label(left_panel_frame, text="Nivel de coincidencia:",
                                 font=("Arial", 10), bg="lightgray")
        coincidence_label.pack(side=tk.TOP, pady=(0, 5), anchor="w", padx=20)  # Alineado a la izquierda

        # Contenedor para botones de navegación(felchas y cuadrados)
        navigation_frame = tk .Frame(left_panel_frame, bg="lightgray")
        navigation_frame.pack(side=tk.TOP, pady=10)
        # Boton izquierdo
        left_arrow_btn = tk.Button(navigation_frame, text="<", font=("Arial", 12), width=3)
        left_arrow_btn.pack(side=tk.LEFT, padx=(0, 5))
        # Cuadrado de navegación con Label
        for _ in range(4):
            square = tk.Label(navigation_frame, text="", bg="gray", width=4, height=1, relief="raised", bd=1)
            square.pack(side=tk.LEFT, padx=2)
        # Boton derecho
        right_arrow_btn = tk.Button(navigation_frame, text=">", font=("Arial", 12), width=3)
        right_arrow_btn.pack(side=tk.LEFT, padx=(5, 0))

        # Etiqueta "Imágenes detectadas" en la parte inferior
        bottom_detected_label = tk.Label(left_panel_frame, text="Imágenes detectadas",
                                         font=("Arial", 12, "bold"), bg="lightgray")
        bottom_detected_label.pack(side=tk.BOTTOM, pady=10)




        # --- 2.2. Panel Derecho ---
        right_panel_frame = tk.Frame(main_content_frame, bg="lightgray", bd=2, relief="solid")
        right_panel_frame.grid(row=0, column=1, padx=(10, 0), sticky="nsew")

        #CORECCION!!
        #Desactivamos la propagación del frame derecho, para evitar que se ajuste al tamaño de sus hijos
        right_panel_frame.pack_propagate(False)


        # Cambiamos a un Label que podremos actualizar
        self.original_image_area = tk.Label(right_panel_frame, text="[Área de Imagen Original]", bg="lightgray",
                                            fg="gray",
                                            relief="sunken", bd=1)
        #Importante: aca no usamos "True" para que el label no fuerce el tamaño
        self.original_image_area.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        # Etiqueta "Imagen original"
        original_label = tk.Label(right_panel_frame, text="Imagen original",
                                  font=("Arial", 12, "bold"), bg="lightgray")
        original_label.pack(pady=(0, 10))

        # Botón "Subir Imagen"
        upload_button = tk.Button(right_panel_frame, text="Subir Imagen",
                                  font=("Arial", 10), bg="white", fg="black", padx=15, pady=8,
                                  command=self.upload_image)
        #Boton "Busqueda de coincidencias"
        search_button = tk.Button(right_panel_frame, text="Buscar coincidencias",
                                  font=("Arial", 10), bg="white", fg="black", padx=15, pady=8,
                                  command=self.upload_image)

        upload_button.pack(pady=(0, 20))

    def upload_image(self):
        """Abre el explorador de archivos para seleccionar una imagen y la muestra"""
        # Abrir el explorador de archivos
        file_path = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[("Imágenes", "*.jpg *.jpeg *.png *.bmp *.gif"), ("Todos los archivos", "*.*")]
        )

        if file_path:  # Si se seleccionó un archivo
            self.image_path = file_path  # Guardamos la ruta

            try:
                # Abrir la imagen con PIL
                image = Image.open(file_path)

                # ### PASO 2: REDIMENSIONAR DINÁMICAMENTE ###
                # Obtenemos el tamaño actual del Label donde irá la imagen.
                # 'update_idletasks' asegura que las dimensiones estén calculadas.
                self.original_image_area.update_idletasks()
                width = self.original_image_area.winfo_width()
                height = self.original_image_area.winfo_height()

                # Usamos el tamaño del Label como el tamaño máximo para la imagen.
                max_size = (width, height)
                image.thumbnail(max_size, Image.LANCZOS)

                # Convertir para tkinter
                self.selected_image = ImageTk.PhotoImage(image)

                # Mostrar la imagen en el área correspondiente
                self.original_image_area.config(image=self.selected_image, text="")
                self.original_image_area.image = self.selected_image  # Mantener referencia

            except Exception as e:
                print(f"Error al cargar la imagen: {e}")
                self.original_image_area.config(text="Error al cargar la imagen", image=None)



        # 3. YA NO HAY window.mainloop()     AQUÍ.
        # El control lo tiene el script principal.