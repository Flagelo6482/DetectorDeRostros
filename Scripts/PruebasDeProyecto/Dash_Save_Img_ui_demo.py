# Dash_Save_Img_ui_demo.py
import tkinter as tk
# from tkinter import filedialog # Descomentar si implementas la lógica de subida aquí
# from PIL import Image, ImageTk # Descomentar para manejo de imágenes

class DashboardSavedImg(tk.Frame):
    def __init__(self, master, on_logout_callback, on_upload_callback, on_detect_callback):
        """
        Constructor de la pantalla de guardado de imágenes.

        :param master: El widget padre (la ventana o frame contenedor).
        :param on_logout_callback: Función a llamar al presionar 'Cerrar Sesión'.
        :param on_upload_callback: Función a llamar al presionar 'Subir Imagen'.
        :param on_detect_callback: Función a llamar al presionar 'Detectar rostros'.
        """
        # 1. Inicializamos el Frame padre con un color de fondo
        super().__init__(master, bg="#202060") # Azul oscuro

        # 2. Guardamos los callbacks para usarlos después
        self.on_logout_callback = on_logout_callback
        self.on_upload_callback = on_upload_callback
        self.on_detect_callback = on_detect_callback

        # --- Barra Superior (Encabezado) ---
        header_frame = tk.Frame(self, bg="#202060")
        header_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        header_frame.grid_columnconfigure(0, weight=1) # Columna del título se expande

        title_label = tk.Label(header_frame, text="Guardado de datos",
                               font=("Arial", 24, "bold"), fg="white", bg="#202060")
        title_label.grid(row=0, column=0)

        close_button = tk.Button(header_frame, text="Cerrar Sesión",
                                 font=("Arial", 10), bg="white", fg="black", padx=10, pady=5,
                                 command=self.on_logout_callback)
        close_button.grid(row=0, column=1, sticky="e", padx=(0, 20))

        # --- Área Principal de Contenido ---
        main_content_frame = tk.Frame(self, bg="#A0D0E0", padx=20, pady=20) # Azul claro
        main_content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # --- Contenido Centrado ---
        # Usamos un frame extra para agrupar y centrar los widgets fácilmente
        center_frame = tk.Frame(main_content_frame, bg="#A0D0E0")
        # Al empaquetar en el centro, los widgets dentro de este frame quedarán centrados
        center_frame.pack(expand=True)

        # Área para mostrar la imagen (simulada con un Label)
        self.image_display_area = tk.Label(
            center_frame,
            text="Imagen(es) nueva(s)",
            font=("Arial", 16),
            bg="lightgray",
            fg="gray",
            relief="sunken",
            bd=2,
            width=50, # Ancho en unidades de texto
            height=20  # Alto en unidades de texto
        )
        self.image_display_area.pack(pady=20, padx=20)

        # Botón "Subir Imagen"
        upload_button = tk.Button(
            center_frame,
            text="Subir Imagen",
            font=("Arial", 12),
            bg="white", fg="black",
            padx=15, pady=8,
            command=self.on_upload_callback
        )
        upload_button.pack(pady=(10, 5)) # Espacio arriba y abajo

        # Botón "Detectar rostros"
        detect_button = tk.Button(
            center_frame,
            text="Detectar rostros",
            font=("Arial", 12),
            bg="white", fg="black",
            padx=15, pady=8,
            command=self.on_detect_callback
        )
        detect_button.pack(pady=(5, 10))


# --- Bloque para Probar la Interfaz de Forma Aislada ---
if __name__ == "__main__":
    # 1. Creamos una ventana principal de prueba
    root = tk.Tk()
    root.title("Prueba de DashboardSavedImg")
    root.geometry("900x700")

    # 2. Definimos funciones "dummy" para simular los callbacks
    #    Esto nos permite probar los botones sin tener la aplicación completa.
    def dummy_logout():
        print("Botón 'Cerrar Sesión' presionado.")

    def dummy_upload():
        print("Botón 'Subir Imagen' presionado.")

    def dummy_detect():
        print("Botón 'Detectar rostros' presionado.")

    # 3. Creamos una instancia de nuestra nueva clase de interfaz
    #    Le pasamos la ventana de prueba y las funciones dummy.
    main_view = DashboardSavedImg(
        master=root,
        on_logout_callback=dummy_logout,
        on_upload_callback=dummy_upload,
        on_detect_callback=dummy_detect
    )

    # 4. Empaquetamos nuestra vista para que llene toda la ventana
    main_view.pack(fill="both", expand=True)

    # 5. Iniciamos el bucle de eventos para mostrar la ventana
    root.mainloop()
