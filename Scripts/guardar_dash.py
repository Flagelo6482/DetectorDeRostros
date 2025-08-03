import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os


class SaveScreen(tk.Frame):
    """
    Pantalla para subir imágenes, detectar rostros y guardar los embeddings y recortes
    en la base de datos.
    """

    def __init__(self, master, funciones, recursos, controlador, root_window):
        super().__init__(master)
        self.root_window = root_window
        self.display_title = "Guardado de datos"
        self.controlador = controlador
        self.funciones = funciones
        self.recursos = recursos

        # Estado de la pantalla
        self.rutas_seleccionadas = []
        self.imagen_tk_preview = None

        self.config(bg="#0c0c2b")
        self._crear_widgets()

    def _crear_widgets(self):
        """Crea y organiza los widgets de la interfaz."""
        # Top Bar con botones de navegación
        top_bar_frame = tk.Frame(self, bg="#00002E")
        top_bar_frame.pack(side="top", fill="x", padx=20, pady=10)
        title_label = tk.Label(top_bar_frame, text="Guardado de datos", font=("Verdana", 24, "bold"), bg="#00002E",
                               fg="white")
        title_label.pack(side="left")

        logout_button = tk.Button(top_bar_frame, text="Cerrar Sesión", font=("Verdana", 10), bg="lightgrey", fg="black",
                                  relief="raised", command=self._cerrar_sesion)
        logout_button.pack(side="right")

        detect_button = tk.Button(top_bar_frame, text="Comparar imagenes", font=("Verdana", 10), bg="lightgrey",
                                  fg="black",
                                  relief="raised", command=self._pantalla_detector_rostros)
        detect_button.pack(side="right", padx=(0, 10))

        # Contenedor principal de la interfaz
        main_panel = tk.Frame(self, bg="#B0C4DE", relief="sunken", bd=2)
        main_panel.pack(fill="both", expand=True, padx=20, pady=20)
        main_panel.grid_columnconfigure(0, weight=1)
        main_panel.grid_rowconfigure(0, weight=1)

        # Frame central para la imagen de previsualización
        center_frame = tk.Frame(main_panel, bg="#B0C4DE")
        center_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        center_frame.grid_columnconfigure(0, weight=1)
        center_frame.grid_rowconfigure(0, weight=1)

        self.image_display_frame = tk.Frame(center_frame, bg="white", relief="sunken", bd=1, width=400, height=500)
        self.image_display_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.image_display_frame.grid_propagate(False)
        self.label_preview = tk.Label(self.image_display_frame, text="Imagen(es) nueva(s)", font=("Verdana", 14),
                                      bg="white")
        self.label_preview.pack(expand=True)

        # Frame para los botones
        buttons_frame = tk.Frame(center_frame, bg="#B0C4DE")
        buttons_frame.grid(row=1, column=0, pady=10)

        tk.Button(buttons_frame, text="Subir Imagen(es)/Carpeta de Imágenes", font=("Verdana", 10),
                  command=self._seleccionar_imagen_o_carpeta).pack(pady=(0, 10))

        self.btn_guardar = tk.Button(buttons_frame, text="Detectar rostros", font=("Verdana", 10),
                                     command=self._guardar_datos_en_db, state=tk.DISABLED)
        self.btn_guardar.pack(pady=10)

    def _seleccionar_imagen_o_carpeta(self):
        """Permite al usuario seleccionar imágenes o una carpeta."""
        rutas = filedialog.askopenfilenames(
            title="Seleccionar imagen(es)",
            filetypes=[("Imágenes", "*.jpg *.jpeg *.png *.bmp")]
        )
        if rutas:
            self.rutas_seleccionadas = list(rutas)
        else:
            carpeta = filedialog.askdirectory(title="O selecciona una carpeta con imágenes")
            if carpeta:
                extensiones_validas = (".jpg", ".jpeg", ".png", ".bmp")
                self.rutas_seleccionadas = [
                    os.path.join(carpeta, archivo)
                    for archivo in os.listdir(carpeta)
                    if archivo.lower().endswith(extensiones_validas)
                ]
            else:
                self.rutas_seleccionadas = []
                self.label_preview.config(image='', text="Imagen(es) nueva(s)")
                self.btn_guardar.config(state=tk.DISABLED)
                return

        if self.rutas_seleccionadas:
            messagebox.showinfo("Éxito", f"Se han cargado {len(self.rutas_seleccionadas)} imagen(es).")
            self._mostrar_imagen_de_ejemplo(self.rutas_seleccionadas[0])
            self.btn_guardar.config(state=tk.NORMAL)
        else:
            self.label_preview.config(image='', text="Imagen(es) nueva(s)")
            self.btn_guardar.config(state=tk.DISABLED)
            messagebox.showwarning("Aviso", "No se seleccionó ninguna imagen o carpeta.")

    def _mostrar_imagen_de_ejemplo(self, ruta_imagen):
        """Muestra una imagen de la lista de selección como previsualización."""
        try:
            img_pil = Image.open(ruta_imagen)
            frame_width = self.image_display_frame.winfo_width()
            frame_height = self.image_display_frame.winfo_height()

            img_pil.thumbnail((frame_width, frame_height), Image.Resampling.LANCZOS)
            self.imagen_tk_preview = ImageTk.PhotoImage(img_pil)
            self.label_preview.config(image=self.imagen_tk_preview, text="")
        except Exception as e:
            messagebox.showerror("Error al cargar imagen",
                                 f"No se pudo mostrar la imagen de ejemplo: {ruta_imagen}\n\nError: {e}")
            self.label_preview.config(image='', text="Error al cargar imagen")

    def _guardar_datos_en_db(self):
        """
        Llama a la función `detectorDeRostros_lote` para procesar y guardar los datos.
        """
        if not self.rutas_seleccionadas:
            messagebox.showwarning("Aviso", "Primero debes subir una o más imágenes.")
            return

        messagebox.showinfo("Procesando",
                            f"Iniciando la detección y guardado de {len(self.rutas_seleccionadas)} imágenes...")

        # Obtenemos la función del diccionario `self.funciones`
        detector_func = self.funciones['detector_lote']

        try:
            resultados = detector_func(self.rutas_seleccionadas, output_dir="../outputs")
            messagebox.showinfo("Éxito",
                                f"Procesamiento finalizado. Se detectaron y guardaron datos de rostros en {len(resultados)} imágenes.")
            # Limpiamos la selección y la UI después de guardar
            self.rutas_seleccionadas = []
            self.label_preview.config(image='', text="Imagen(es) nueva(s)")
            self.btn_guardar.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al guardar los datos: {e}")

    def _pantalla_detector_rostros(self):
        """Nos vamos a la pantalla de detección de rostros"""
        self.controlador("detectar")

    def _cerrar_sesion(self):
        """Usa el controlador para volver a la pantalla de login."""
        print("Cerrando sesión y volviendo al login...")
        self.controlador("login")

