import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import numpy as np
import cv2  # Necesario para cv2.imdecode en extraer_embedding si no está en otro archivo


class DetectScreen(tk.Frame):
    def __init__(self, master, funciones, recursos, controlador, root_window):
        super().__init__(master)  # Inicializa tk.Frame
        self.root_window = root_window
        self.root_window.title("Detector de ratas")
        self.controlador = controlador
        self.funciones = funciones  # Diccionario de las funciones que tenemos
        self.recursos = recursos  # Diccionario de lo recursos que pasamos como el modelo y base de datos

        self.rutas_seleccionadas = []  # Rutas de las imágenes subidas por el usuario
        self.extracted_embeddings = []  # Embeddings extraídos de las imágenes subidas
        self.current_matches_data = []  # Almacena los resultados de la comparación para cada imagen de consulta
        self.current_query_index = 0  # Índice de la imagen de consulta que se está mostrando actualmente

        # Variables para PhotoImage para evitar que sean recolectadas por el garbage collector
        self.imagen_tk_original = None
        self.label_detected_main_image_tk = None
        self.thumbnail_images_tk = []
        self.thumbnail_image_labels = []  # Nueva lista para las ETIQUETAS dentro de los frames de miniaturas

        self.config(bg="#0c0c2b")
        self._crear_widgets()

    def _crear_widgets(self):
        """Crea y organiza los widgets de la interfaz."""

        # --- 1. BARRA SUPERIOR (TÍTULO Y BOTÓN DE CERRAR SESIÓN) ---
        top_bar_frame = tk.Frame(self, bg="#00002E")
        top_bar_frame.pack(side="top", fill="x", padx=20, pady=10)

        title_label = tk.Label(top_bar_frame, text="Detector de Ratas", font=("Verdana", 24, "bold"), bg="#00002E",
                               fg="white")
        title_label.pack(side="left")

        logout_button = tk.Button(top_bar_frame, text="Cerrar Sesión", font=("Verdana", 10), bg="lightgrey", fg="black",
                                  relief="raised", command=self._cerrar_sesion)
        logout_button.pack(side="right")

        # --- 2. PANEL PRINCIPAL (CONTENEDOR DE LAS SECCIONES IZQUIERDA Y DERECHA) ---
        main_panel = tk.Frame(self, bg="#B0C4DE", relief="sunken", bd=2)
        main_panel.pack(fill="both", expand=True, padx=20, pady=20)

        # --- 3. Configuramos el grid del panel principal ---
        main_panel.grid_columnconfigure(0, weight=1)  # Columna izquierda para resultados
        main_panel.grid_columnconfigure(1, weight=1)  # Columna derecha para subir imagen
        main_panel.grid_rowconfigure(0, weight=1)

        # --- SECCION IZQUIERDA (RESULTADOS DE DETECCIÓN Y COINCIDENCIAS) ---
        self.left_frame = tk.Frame(main_panel, bg="#B0C4DE")
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.left_frame.grid_rowconfigure(0, weight=1)  # Para que la imagen principal se expanda

        # Contenedor para la imagen principal detectada/de consulta
        self.detected_image_display = tk.Frame(self.left_frame, bg="lightgrey", relief="sunken", bd=1)
        self.detected_image_display.grid(row=0, column=0, columnspan=5, sticky="nsew", padx=5, pady=5)
        self.detected_image_display.grid_propagate(False)  # Evita que el frame se encoja

        # Etiqueta para la imagen principal (se actualizará con la de consulta o el mejor match)
        self.label_detected_main_image = tk.Label(self.detected_image_display, text="Rostro/Imagen de Consulta",
                                                  bg="lightgrey")
        self.label_detected_main_image.pack(expand=True)

        # Etiqueta para "Nivel de coincidencia"
        self.coincidence_label = tk.Label(self.left_frame, text="Nivel de coincidencia: N/A", font=("Verdana", 10),
                                          bg="#B0C4DE", anchor="w")
        self.coincidence_label.grid(row=1, column=0, columnspan=5, sticky="ew", padx=5, pady=(10, 0))

        # Frame para las miniaturas y flechas de navegación (Fila 2)
        thumbnails_nav_frame = tk.Frame(self.left_frame, bg="#B0C4DE")
        thumbnails_nav_frame.grid(row=2, column=0, columnspan=5, sticky="ew", pady=5)
        thumbnails_nav_frame.grid_columnconfigure(0, weight=0)  # Flecha izquierda
        thumbnails_nav_frame.grid_columnconfigure(1, weight=1)  # Contenedor de miniaturas
        thumbnails_nav_frame.grid_columnconfigure(2, weight=0)  # Flecha derecha

        # Botón de flecha izquierda para navegar entre resultados de diferentes imágenes de consulta
        self.arrow_left = tk.Button(thumbnails_nav_frame, text="⬅", font=("Verdana", 12),
                                    command=lambda: self._navigate_thumbnails(-1), state=tk.DISABLED)
        self.arrow_left.grid(row=0, column=0, padx=5)

        # Contenedor para las miniaturas de los matches
        self.thumbnails_container = tk.Frame(thumbnails_nav_frame, bg="#B0C4DE")
        self.thumbnails_container.grid(row=0, column=1, sticky="ew")

        # Creación de los FRAMES de miniaturas y las ETIQUETAS internas
        self.thumbnail_frames = []  # Guardaremos las referencias a los frames contenedores
        self.thumbnail_image_labels = []  # Guardaremos las referencias a las etiquetas de imágenes DENTRO de los frames
        for i in range(4):  # Puedes ajustar el número de miniaturas
            # Frame contenedor para la miniatura, con tamaño fijo en píxeles
            thumb_frame = tk.Frame(self.thumbnails_container, bg="grey", relief="sunken", bd=1, width=80, height=80)
            thumb_frame.pack(side="left", padx=3, pady=5)
            thumb_frame.pack_propagate(False)  # ¡CLAVE! Evita que el FRAME se ajuste al tamaño de la imagen interna
            self.thumbnail_frames.append(thumb_frame)

            # Etiqueta de imagen dentro del frame contenedor
            thumb_label = tk.Label(thumb_frame,
                                   bg="grey")  # La etiqueta no necesita width/height aquí, solo llena el frame
            thumb_label.pack(expand=True, fill="both")  # ¡CLAVE! La etiqueta llena el FRAME contenedor
            self.thumbnail_image_labels.append(thumb_label)

        # Botón de flecha derecha para navegar entre resultados de diferentes imágenes de consulta
        self.arrow_right = tk.Button(thumbnails_nav_frame, text="➡", font=("Verdana", 12),
                                     command=lambda: self._navigate_thumbnails(1), state=tk.DISABLED)
        self.arrow_right.grid(row=0, column=2, padx=5)

        # Etiqueta "Imagenes detectadas"
        self.detected_label = tk.Label(self.left_frame, text="Resultados de Coincidencias", font=("Verdana", 12),
                                       bg="#B0C4DE")
        self.detected_label.grid(row=3, column=0, columnspan=5, pady=5)  # Ajustar la fila

        # --- SECCION DERECHA (CARGA DE IMAGEN) ---
        right_frame = tk.Frame(main_panel, bg="#B0C4DE")
        right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Panel donde se muestra la imagen original subida
        self.original_image_display = tk.Frame(right_frame, bg="lightgrey", relief="sunken", bd=1, width=600,
                                               height=600)
        self.original_image_display.pack(fill="both", expand=True, padx=5, pady=5)
        self.original_image_display.pack_propagate(False)

        self.label_imagen_original = tk.Label(self.original_image_display, text="Imagen Original", bg="lightgrey")
        self.label_imagen_original.pack(expand=True)

        tk.Label(right_frame, text="Imagen original", font=("Verdana", 12), bg="#B0C4DE").pack(pady=5)

        buttons_frame = tk.Frame(right_frame, bg="#B0C4DE")
        buttons_frame.pack(pady=10)

        self.btn_procesar = tk.Button(buttons_frame, text="Buscar Coincidencias", font=("Verdana", 10),
                                      command=self._buscar_coincidencias, state=tk.DISABLED)
        self.btn_procesar.pack(side="left", padx=10)

        tk.Button(buttons_frame, text="Subir Imagen", font=("Verdana", 10), command=self._manejar_subida_imagen).pack(
            side="left", padx=10)

    def _clear_left_panel(self):
        """Limpia el contenido del panel izquierdo antes de mostrar nuevos resultados."""
        self.label_detected_main_image.config(image='', text="Rostro/Imagen de Consulta")
        self.label_detected_main_image_tk = None  # Limpiar referencia para PhotoImage
        self.coincidence_label.config(text="Nivel de coincidencia: N/A")
        # Ahora limpiamos las etiquetas de imagen dentro de los frames de miniaturas
        for thumb_label in self.thumbnail_image_labels:
            thumb_label.config(image='', bg="grey")
        self.thumbnail_images_tk = []  # Limpiar la lista de referencias a PhotoImage

    def _display_current_query_and_matches(self):
        """Muestra la imagen de consulta actual y sus coincidencias en el panel izquierdo."""
        if not self.current_matches_data:
            self._clear_left_panel()
            self.arrow_left.config(state=tk.DISABLED)
            self.arrow_right.config(state=tk.DISABLED)
            return

        # Aseguramos que el índice esté dentro de los límites
        self.current_query_index = max(0, min(self.current_query_index, len(self.current_matches_data) - 1))

        current_data = self.current_matches_data[self.current_query_index]
        query_image_path = current_data['query_image_path']
        # 'comparison_result' es el diccionario completo devuelto por comparar_rostros
        comparison_result = current_data['matches']
        matches_list = comparison_result.get('matches', [])  # Obtener la lista real de coincidencias

        self._clear_left_panel()  # Limpiar antes de dibujar

        # Habilitar/deshabilitar botones de navegación
        self.arrow_left.config(state=tk.NORMAL if self.current_query_index > 0 else tk.DISABLED)
        self.arrow_right.config(
            state=tk.NORMAL if self.current_query_index < len(self.current_matches_data) - 1 else tk.DISABLED)

        # --- Mostrar la imagen de consulta principal ---
        try:
            img_pil_query = Image.open(query_image_path)
            # Redimensionar para el panel principal (detected_image_display)
            # winfo_width/height puede ser 1 al inicio si el widget no ha sido completamente renderizado.
            # Usamos un valor por defecto si es muy pequeño.
            panel_width = self.detected_image_display.winfo_width()
            panel_height = self.detected_image_display.winfo_height()
            if panel_width < 100: panel_width = 600
            if panel_height < 100: panel_height = 600

            img_pil_query.thumbnail((panel_width, panel_height), Image.Resampling.LANCZOS)
            self.label_detected_main_image_tk = ImageTk.PhotoImage(img_pil_query)
            self.label_detected_main_image.config(image=self.label_detected_main_image_tk, text="")
        except Exception as e:
            self.label_detected_main_image.config(image='',
                                                  text=f"Error al cargar consulta: {os.path.basename(query_image_path)}")
            print(f"Error al mostrar imagen de consulta en panel principal: {query_image_path}, Error: {e}")

        # --- Mostrar miniaturas de coincidencias ---
        best_match_similarity = "N/A"
        if comparison_result[
            'matches_found'] and matches_list:  # Verifica si se encontraron coincidencias y la lista no está vacía
            best_match_similarity = f"{matches_list[0]['similarity']:.2f}"
            self.coincidence_label.config(text=f"Nivel de coincidencia (Mejor Match): {best_match_similarity}")

            for i, match_data in enumerate(matches_list):  # Iterar sobre la lista de coincidencias
                if i >= len(self.thumbnail_image_labels):  # No exceder el número de etiquetas de miniaturas disponibles
                    break

                # Obtener la ruta de la imagen del rostro en la DB (desde el 'metadata' en 'data')
                match_image_path = match_data['metadata'].get('face_image')

                if match_image_path and os.path.exists(match_image_path):
                    try:
                        img_pil_match = Image.open(match_image_path)
                        # La imagen se redimensiona a 80x80 PÍXELES aquí.
                        img_pil_match.thumbnail((80, 80), Image.Resampling.LANCZOS)
                        thumb_tk = ImageTk.PhotoImage(img_pil_match)
                        # Asignamos la imagen a la ETIQUETA dentro del FRAME
                        self.thumbnail_image_labels[i].config(image=thumb_tk, text="", bg="lightblue")
                        self.thumbnail_images_tk.append(thumb_tk)  # Mantener referencia
                    except Exception as e:
                        self.thumbnail_image_labels[i].config(image='', text=f"Error {i + 1}", bg="red")
                        print(f"Error al cargar miniatura {match_image_path}: {e}")
                else:
                    self.thumbnail_image_labels[i].config(image='', text=f"No imagen {i + 1}", bg="grey")
                    print(f"Advertencia: Ruta de imagen de coincidencia no válida o no existe: {match_image_path}")
        else:
            self.coincidence_label.config(text="Nivel de coincidencia: Sin coincidencias")

    def _navigate_thumbnails(self, direction: int):
        """Navega entre los resultados de las diferentes imágenes de consulta."""
        new_index = self.current_query_index + direction
        if 0 <= new_index < len(self.current_matches_data):
            self.current_query_index = new_index
            self._display_current_query_and_matches()
        else:
            print(f"No hay más resultados en la dirección {direction}.")

    def _manejar_subida_imagen(self):
        """
        Función principal que se ejecuta al pulsar "Subir Imagen".
        Obtiene las rutas y, si tiene éxito, muestra la primera imagen y activa el botón de búsqueda.
        """
        rutas = self._seleccionar_imagen_o_carpeta()

        if rutas:
            self.rutas_seleccionadas = rutas
            messagebox.showinfo("Éxito", f"Se han cargado {len(self.rutas_seleccionadas)} imagen(es).")

            # Muestra la primera imagen de la lista en el panel derecho (original)
            self._mostrar_imagen_en_panel(self.rutas_seleccionadas[0], self.original_image_display)

            # Limpiar y resetear los resultados previos en el panel izquierdo
            self._clear_left_panel()
            self.current_matches_data = []  # Borrar datos de coincidencias anteriores
            self.current_query_index = 0
            self.arrow_left.config(state=tk.DISABLED)
            self.arrow_right.config(state=tk.DISABLED)

            # Activa el botón de "Buscar Coincidencias"
            self.btn_procesar.config(state=tk.NORMAL)
        else:
            self.rutas_seleccionadas = []
            self.extracted_embeddings = []
            self.current_matches_data = []
            self.btn_procesar.config(state=tk.DISABLED)
            messagebox.showwarning("Cancelado", "No se seleccionó ninguna imagen o carpeta.")

    def _seleccionar_imagen_o_carpeta(self):
        """
        Abre diálogos para seleccionar archivos o una carpeta.
        Retorna una lista de rutas de imágenes.
        """
        rutas = filedialog.askopenfilenames(
            title="Seleccionar imagen(es)",
            filetypes=[("Imágenes", "*.jpg *.jpeg *.png *.bmp")]
        )

        if rutas:
            return list(rutas)

        carpeta = filedialog.askdirectory(title="O selecciona una carpeta con imágenes")

        if not carpeta:
            return []

        extensiones_validas = (".jpg", ".jpeg", ".png", ".bmp")
        return [
            os.path.join(carpeta, archivo)
            for archivo in os.listdir(carpeta)
            if archivo.lower().endswith(extensiones_validas)
        ]

    def _mostrar_imagen_en_panel(self, ruta_imagen, panel_display):
        """
        Carga una imagen desde una ruta, la redimensiona y la muestra en el panel especificado.
        """
        try:
            img_pil = Image.open(ruta_imagen)
            # Asegurarse de que el panel tenga tamaño antes de obtener winfo_width.
            # Si aún no está renderizado, winfo_width/height pueden ser 1, por eso usamos un default.
            panel_width = panel_display.winfo_width()
            panel_height = panel_display.winfo_height()
            if panel_width <= 1: panel_width = 600
            if panel_height <= 1: panel_height = 600

            img_pil.thumbnail((panel_width, panel_height), Image.Resampling.LANCZOS)
            self.imagen_tk_original = ImageTk.PhotoImage(img_pil)
            self.label_imagen_original.config(image=self.imagen_tk_original, text="")  # Quitar texto
        except Exception as e:
            messagebox.showerror("Error al cargar imagen",
                                 f"No se pudo mostrar la imagen: {ruta_imagen}\n\nError: {e}")
            self.btn_procesar.config(state=tk.DISABLED)
            self.label_imagen_original.config(image='', text="Error al cargar imagen")  # Mostrar error en UI

    def _buscar_coincidencias(self):
        """
        Lógica para procesar las imágenes seleccionadas:
        1. Extrae los embeddings de cada imagen.
        2. Compara cada embedding extraído con la base de datos.
        3. Almacena y muestra los resultados en el panel izquierdo.
        """
        if not self.rutas_seleccionadas:
            messagebox.showwarning("Aviso", "Primero debes subir una o más imágenes.")
            return

        messagebox.showinfo("Procesando",
                            f"Iniciando la extracción y comparación de {len(self.rutas_seleccionadas)} imagen(es).")
        print(f"Procesando {len(self.rutas_seleccionadas)} imágenes...")

        extraer_func = self.funciones.get('extraer')
        comparar_func = self.funciones.get('comparar')

        if not extraer_func:
            messagebox.showerror("Error", "La función 'extraer' no está disponible.")
            return
        if not comparar_func:
            messagebox.showerror("Error", "La función 'comparar' no está disponible.")
            return

        self.extracted_embeddings = []
        self.current_matches_data = []  # Reiniciamos los datos de coincidencias

        for i, ruta_imagen in enumerate(self.rutas_seleccionadas):
            print(f"DEBUG: Intentando extraer embedding de: {ruta_imagen}")
            if not os.path.exists(ruta_imagen):
                print(f"DEBUG: ¡ADVERTENCIA! La ruta no existe en el sistema de archivos: {ruta_imagen}")

            try:
                embedding = extraer_func(ruta_imagen)
                self.extracted_embeddings.append(embedding)
                print(f"Embedding extraído con éxito de: {os.path.basename(ruta_imagen)}")

                # --- Comparar el embedding extraído con la base de datos ---
                # Tu función 'comparar_rostros' devuelve un dict con 'matches_found', 'matches' y 'query_embedding'
                comparison_result = comparar_func(embedding)

                # Almacenar la ruta de la imagen de consulta junto con sus coincidencias
                self.current_matches_data.append({
                    'query_image_path': ruta_imagen,
                    'matches': comparison_result  # Guardamos el diccionario completo de resultados
                })

                print(f"Coincidencias para {os.path.basename(ruta_imagen)}: {comparison_result.get('matches_found')}")

            except FileNotFoundError:
                messagebox.showwarning("Error de archivo",
                                       f"No se pudo encontrar la imagen: {os.path.basename(ruta_imagen)}")
                print(f"DEBUG: FileNotFoundError para: {ruta_imagen}")
            except ValueError as ve:
                messagebox.showwarning("Error de rostro",
                                       f"'{os.path.basename(ruta_imagen)}': {ve}. Se omitirá esta imagen.")
                print(f"DEBUG: ValueError (problema de rostros) para: {ruta_imagen} - Error: {e}")
            except Exception as e:
                messagebox.showerror("Error inesperado", f"Error al procesar '{os.path.basename(ruta_imagen)}': {e}")
                print(f"DEBUG: Excepción inesperada para: {ruta_imagen} - Error: {e}")

        if not self.extracted_embeddings:
            messagebox.showwarning("Atención",
                                   "No se pudo extraer ningún embedding válido de las imágenes seleccionadas.")
            print("DEBUG: No se extrajo ningún embedding válido al final.")
            return

        if not self.current_matches_data:
            messagebox.showwarning("Resultados",
                                   "No se encontraron coincidencias para ninguna de las imágenes procesadas.")
            self._clear_left_panel()
            return

        messagebox.showinfo("Extracción y Comparación Completas",
                            f"Procesamiento finalizado. Se encontraron coincidencias para {len([d for d in self.current_matches_data if d['matches']['matches_found']])} de {len(self.current_matches_data)} imágenes.")

        self.current_query_index = 0  # Mostrar el primer resultado por defecto
        self._display_current_query_and_matches()  # Actualizar la interfaz con los resultados

    def _pantalla_guardar_datos(self):
        """Nos redirigimos a la pantalla donde guardamos los datos"""
        self.controlador("guardar")

    def _cerrar_sesion(self):
        """Usa el controlador para volver a la pantalla de login."""
        print("Cerrando sesión y volviendo al login...")
        self.controlador("login")

#-----------------------------------------------------------------------------------------------------------------------
# import tkinter as tk
# from tkinter import filedialog, messagebox
# import os
# from PIL import Image, ImageTk # <- Importamos Pillow
# import numpy as np
#
# class DetectScreen(tk.Frame):
#     def __init__(self, master, funciones, recursos, controlador, root_window):
#         super().__init__(master)  # Inicializa tk.Frame
#         self.root_window = root_window
#         self.root_window.title("Detector de ratas")
#         self.controlador = controlador
#         self.funciones = funciones  # Diccionario de las funciones que tenemos
#         self.recursos = recursos
#
#         self.config(bg="#0c0c2b")
#         self._crear_widgets()
#
#     def _crear_widgets(self):
#         """ACA AGREGAMOS LOS OBJETOS DE LA INTERFAZ QUE YA CREAMOS(BUSCAR)"""
#
#         # --- 1. BARRA SUPERIOR (TÍTULO Y BOTÓN DE CERRAR SESIÓN) ---
#
#         # Creamos un frame para la barra superior que contendrá el título y el botón.
#         # Se empaqueta en la parte superior ('top') y se estira horizontalmente ('x').
#         top_bar_frame = tk.Frame(self, bg="#00002E")
#         top_bar_frame.pack(side="top", fill="x", padx=20, pady=10)
#
#         """
#         Etiqueta para el título principal.
#         font: Define la fuente, tamaño y estilo.
#         bg: Color de fondo (el mismo que su contenedor).
#         fg: Color de la letra ('white' para blanco).
#         """
#         title_label = tk.Label(top_bar_frame, text="Detector de Ratas", font=("Verdana", 24, "bold"), bg="#00002E",
#                                fg="white")
#         # .pack() posiciona el widget. 'side="left"' lo alinea a la izquierda dentro de top_bar_frame.
#         title_label.pack(side="left")
#
#         """
#         Botón para cerrar sesión.
#         command: Función que se ejecuta al hacer clic.
#         relief="flat": Quita el borde del botón para un look más moderno.
#         activebackground: Color cuando el cursor está sobre el botón.
#         """
#         logout_button = tk.Button(top_bar_frame, text="Cerrar Sesión", font=("Verdana", 10), bg="lightgrey", fg="black",
#                                   relief="raised", command=self._cerrar_sesion)
#         # .pack() con 'side="right"' lo alinea a la derecha.
#         logout_button.pack(side="right")
#
#         # --- 2. PANEL PRINCIPAL (CONTENEDOR DE LAS SECCIONES IZQUIERDA Y DERECHA) ---
#
#         """
#         Creamos un frame principal que contendrá las dos columnas.
#         bg: Color de fondo celeste claro, como en la imagen.
#         relief="sunken" y bd=2 le dan un borde hundido.
#         .pack() lo posiciona. 'fill="both"' hace que ocupe todo el espacio disponible en ambas direcciones.
#         'expand=True' permite que el frame se expanda si la ventana cambia de tamaño.
#         """
#         main_panel = tk.Frame(self, bg="#B0C4DE", relief="sunken", bd=2)
#         main_panel.pack(fill="both", expand=True, padx=20, pady=20)
#
#
#         # --- 3. Configuramos el grid del panel principal para que tenga dos columnas de igual tamaño.
#         main_panel.grid_columnconfigure(0, weight=1)  # Columna izquierda
#         main_panel.grid_columnconfigure(1, weight=1)  # Columna derecha
#         # También configuramos la fila para que se expanda verticalmente.
#         main_panel.grid_rowconfigure(0, weight=1)
#
#         # --- SECCION IZQUIERDA ---
#         """
#         .grid() lo posiciona en la primera columna (column=0).
#         'sticky="nsew"' hace que se pegue a los 4 bordes de su celda, expandiéndose.
#         """
#         left_frame = tk.Frame(main_panel, bg="#B0C4DE")
#         left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
#
#         # --- Contenedor para la imagen principal detectada ---
#         """
#         Le damos un tamaño fijo inicial, pero 'fill' y 'expand' lo harán responsivo.
#         Podrías poner una etiqueta con texto inicial aquí
#         """
#         detected_image_display = tk.Frame(left_frame, bg="lightgrey", relief="sunken", bd=1)
#         detected_image_display.pack(fill="both", expand=True, padx=5, pady=5)
#         tk.Label(detected_image_display, text="Rostro detectado", bg="lightgrey").pack(expand=True)
#
#         """
#         Etiqueta para "Nivel de coincidencia".
#         'anchor="w"' (west) alinea el texto a la izquierda.
#         """
#         coincidence_label = tk.Label(left_frame, text="Nivel de coincidencia:", font=("Verdana", 10), bg="#B0C4DE",
#                                      anchor="w")
#         coincidence_label.pack(fill="x", padx=5, pady=(10, 0))
#
#         # Frame para las miniaturas y flechas de navegación.
#         thumbnails_frame = tk.Frame(left_frame, bg="#B0C4DE")
#         thumbnails_frame.pack(fill="x", pady=5)
#
#         # Botón de flecha izquierda.
#         arrow_left = tk.Button(thumbnails_frame, text="⬅", font=("Verdana", 12))
#         arrow_left.pack(side="left", padx=5)
#
#         # Creación de las 4 miniaturas de imágenes.
#         for i in range(4):
#             # Usamos un Frame para representar cada miniatura.
#             thumb_frame = tk.Frame(thumbnails_frame, bg="grey", relief="sunken", bd=1, width=60, height=60)
#             thumb_frame.pack(side="left", padx=3)
#             # Evita que el frame se encoja para ajustarse a su contenido (si lo tuviera).
#             thumb_frame.pack_propagate(False)
#
#         # Botón de flecha derecha.
#         arrow_right = tk.Button(thumbnails_frame, text="➡", font=("Verdana", 12))
#         arrow_right.pack(side="left", padx=5)
#
#         # Etiqueta "Imagenes detectadas".
#         detected_label = tk.Label(left_frame, text="Imagenes detectadas", font=("Verdana", 12))
#         detected_label.pack(pady=5)
#
#
#
#
#
#
#         # --- SECCION DERECHA ---
#         # Frame para la sección derecha.
#         right_frame = tk.Frame(main_panel, bg="#B0C4DE")
#         # .grid() la posiciona en la segunda columna (column=1).
#         right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
#
#         # Guardamos una referencia al panel de la imagen para poder modificarlo después.
#         self.original_image_display = tk.Frame(right_frame, bg="lightgrey", relief="sunken", bd=1, width=600, height=600)
#         self.original_image_display.pack(fill="both", expand=True, padx=5, pady=5)
#
#         # ¡CLAVE 2/3! Esta es la línea más importante.
#         # Le dice al Frame que NO cambie su tamaño para ajustarse a los widgets que contiene.
#         # Mantendrá los 400x400 píxeles que le asignamos.
#         self.original_image_display.pack_propagate(False)
#
#         # Etiqueta inicial que se reemplazará por la imagen.
#         self.label_imagen_original = tk.Label(self.original_image_display, text="Imagen Original", bg="lightgrey")
#         self.label_imagen_original.pack(expand=True)
#
#         # LABEL DEL BOTON "Subir Imagen" -->
#         tk.Label(right_frame, text="Imagen original", font=("Verdana", 12), bg="#B0C4DE").pack(pady=5)
#
#         buttons_frame = tk.Frame(right_frame, bg="#B0C4DE")
#         buttons_frame.pack(pady=10)
#
#         #TE QUEDASTE ACA NECESITAS APLICAR LA EXTRACCION DE EMBEDDINGS LUEGO APLICAS LA COMPARACION
#         #REVISA EL GEMINI DE LA CUENTA DE frankln6482@gmail.com
#         # Guardamos una referencia al botón "Buscar" para poder activarlo/desactivarlo.
#         self.btn_procesar = tk.Button(buttons_frame, text="Buscar Coincidencias", font=("Verdana", 10),
#                                       command=self._buscar_coincidencias, state=tk.DISABLED)
#         self.btn_procesar.pack(side="left", padx=10)
#
#         # El botón "Subir Imagen" ahora llama a nuestro manejador principal.
#         tk.Button(buttons_frame, text="Subir Imagen", font=("Verdana", 10), command=self._manejar_subida_imagen).pack(
#             side="left", padx=10)
#
#     def _manejar_subida_imagen(self):
#         """
#         Función principal que se ejecuta al pulsar "Subir Imagen".
#         Obtiene las rutas y, si tiene éxito, muestra la primera imagen y activa el botón de búsqueda.
#         """
#         # Llama a la función que abre los diálogos de selección.
#         rutas = self._seleccionar_imagen_o_carpeta()
#
#         if rutas:
#             self.rutas_seleccionadas = rutas
#             messagebox.showinfo("Éxito", f"Se han cargado {len(self.rutas_seleccionadas)} imagen(es).")
#
#             # Muestra la primera imagen de la lista en el panel derecho.
#             self._mostrar_imagen_en_panel(self.rutas_seleccionadas[0], self.original_image_display)
#
#             # Activa el botón de "Buscar Coincidencias" ya que ahora hay imágenes para procesar.
#             self.btn_procesar.config(state=tk.NORMAL)
#         else:
#             self.rutas_seleccionadas = []
#             # Desactiva el botón si no se seleccionó nada.
#             self.btn_procesar.config(state=tk.DISABLED)
#             messagebox.showwarning("Cancelado", "No se seleccionó ninguna imagen o carpeta.")
#
#     def _seleccionar_imagen_o_carpeta(self):
#         """
#         Abre diálogos para seleccionar archivos o una carpeta. Es la lógica que tú propusiste.
#         Retorna una lista de rutas de imágenes.
#         """
#         # Primero, intenta abrir el diálogo para seleccionar uno o varios archivos.
#         rutas = filedialog.askopenfilenames(
#             title="Seleccionar imagen(es)",
#             filetypes=[("Imágenes", "*.jpg *.jpeg *.png *.bmp")]
#         )
#
#         if rutas:
#             return list(rutas)
#
#         # Si el usuario canceló, le damos la opción de seleccionar una carpeta.
#         carpeta = filedialog.askdirectory(title="O selecciona una carpeta con imágenes")
#
#         if not carpeta:
#             return []
#
#         # Busca todos los archivos de imagen válidos dentro de la carpeta.
#         extensiones_validas = (".jpg", ".jpeg", ".png", ".bmp")
#         return [
#             os.path.join(carpeta, archivo)
#             for archivo in os.listdir(carpeta)
#             if archivo.lower().endswith(extensiones_validas)
#         ]
#
#     def _mostrar_imagen_en_panel(self, ruta_imagen, panel_display):
#         """
#         Carga una imagen desde una ruta, la redimensiona y la muestra en el panel especificado.
#         """
#         try:
#             # Abrir la imagen usando Pillow.
#             img_pil = Image.open(ruta_imagen)
#
#             # ¡CLAVE 3/3! Usamos el tamaño fijo del panel (400x400) como referencia
#             # para redimensionar la imagen. Esto asegura que la imagen siempre
#             # se escale para caber dentro del contenedor, sin importar su tamaño original.
#             img_pil.thumbnail((600, 600), Image.Resampling.LANCZOS)
#
#             self.imagen_tk_original = ImageTk.PhotoImage(img_pil)
#
#             # Actualizamos la etiqueta para que muestre la nueva imagen.
#             self.label_imagen_original.config(image=self.imagen_tk_original)
#
#         except Exception as e:
#             messagebox.showerror("Error al cargar imagen",
#                                  f"No se pudo mostrar la imagen: {ruta_imagen}\n\nError: {e}")
#             self.btn_procesar.config(state=tk.DISABLED)
#
#     def _buscar_coincidencias(self):
#         """Lógica para procesar las imágenes seleccionadas."""
#         if not self.rutas_seleccionadas:
#             messagebox.showwarning("Aviso", "Primero debes subir una o más imágenes.")
#             return
#
#         messagebox.showinfo("Procesando",
#                             f"Iniciando la extracción de embeddings de {len(self.rutas_seleccionadas)} imagen(es).")
#         print(f"Procesando {len(self.rutas_seleccionadas)} imágenes...")
#
#         # Obtenemos la función necesaria del diccionario 'funciones'
#         extraer_func = self.funciones.get('extraer')
#
#         if not extraer_func:
#             messagebox.showerror("Error", "La función 'extraer' no está disponible.")
#             return
#
#         self.extracted_embeddings = []  # Reiniciamos la lista de embeddings extraídos
#         # Iteramos sobre cada ruta de imagen seleccionada
#         for i, ruta_imagen in enumerate(self.rutas_seleccionadas):
#             # --- IMPRESIÓN DE DEPURACIÓN CLAVE ---
#             # Verifica que la ruta de la imagen sea correcta y accesible.
#             print(f"DEBUG: Intentando extraer embedding de: {ruta_imagen}")
#             if not os.path.exists(ruta_imagen):
#                 print(f"DEBUG: ¡ADVERTENCIA! La ruta no existe en el sistema de archivos: {ruta_imagen}")
#
#             try:
#                 # Extraemos el embedding de la imagen actual
#                 # La función extraer_embedding espera una única ruta de imagen
#                 embedding = extraer_func(ruta_imagen)
#                 self.extracted_embeddings.append(embedding)
#                 print(f"Embedding extraído con éxito de: {os.path.basename(ruta_imagen)}")
#
#             except FileNotFoundError:
#                 messagebox.showwarning("Error de archivo",
#                                        f"No se pudo encontrar la imagen: {os.path.basename(ruta_imagen)}")
#                 print(f"DEBUG: FileNotFoundError para: {ruta_imagen}")
#             except ValueError as ve:
#                 # Este error se lanza si la imagen no tiene 1 rostro (0 o más de 1)
#                 messagebox.showwarning("Error de rostro",
#                                        f"'{os.path.basename(ruta_imagen)}': {ve}. Se omitirá esta imagen.")
#                 print(f"DEBUG: ValueError (problema de rostros) para: {ruta_imagen} - Error: {ve}")
#             except Exception as e:
#                 messagebox.showerror("Error inesperado", f"Error al procesar '{os.path.basename(ruta_imagen)}': {e}")
#                 print(f"DEBUG: Excepción inesperada para: {ruta_imagen} - Error: {e}")
#
#         if not self.extracted_embeddings:
#             messagebox.showwarning("Atención",
#                                    "No se pudo extraer ningún embedding válido de las imágenes seleccionadas.")
#             print("DEBUG: No se extrajo ningún embedding válido al final.")
#             return
#
#         messagebox.showinfo("Extracción Completa",
#                             f"Se extrajeron {len(self.extracted_embeddings)} embedding(s) con éxito. Ahora puedes proceder con la comparación.")
#         print(f"DEBUG: Extracción completa. Total de embeddings extraídos: {len(self.extracted_embeddings)}")
#
#
#     def _pantalla_guardar_datos(self):
#         """Nos redirigimos a la pantalla donde guardamos los datos"""
#         self.controlador("guardar")  # <<-- Nos vamos a la otra pantalla
#
#     def _cerrar_sesion(self):
#         """Usa el controlador para volver a la pantalla de login."""
#         print("Cerrando sesión y volviendo al login...")
#         self.controlador("login")