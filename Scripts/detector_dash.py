import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import numpy as np

# Importamos las funciones de lógica directamente
# from face_logic import extraer_embedding, comparar_rostros


class DetectScreen(tk.Frame):
    def __init__(self, master, funciones, recursos, controlador, root_window):
        super().__init__(master)  # Inicializa tk.Frame
        self.root_window = root_window
        self.display_title = "Detector de Ratas"
        self.controlador = controlador
        self.funciones = funciones  # Diccionario de las funciones que tenemos
        self.recursos = recursos  # Diccionario de lo recursos que pasamos como el modelo y base de datos

        # Las funciones de extraer y comparar ahora se acceden directamente del diccionario
        # y se usan en el método _buscar_coincidencias.

        self.rutas_seleccionadas = []
        self.extracted_embeddings = []
        self.current_matches_data = []
        self.current_query_index = 0

        # Variables para PhotoImage para evitar que sean recolectadas por el garbage collector
        self.imagen_tk_original = None
        self.label_detected_main_image_tk = None
        self.thumbnail_images_tk = []
        self.thumbnail_image_labels = []

        self.config(bg="#0c0c2b")
        self._crear_widgets()

    def _crear_widgets(self):
        """Crea y organiza los widgets de la interfaz."""
        top_bar_frame = tk.Frame(self, bg="#00002E")
        top_bar_frame.pack(side="top", fill="x", padx=20, pady=10)
        title_label = tk.Label(top_bar_frame, text="Detector de Ratas", font=("Verdana", 24, "bold"), bg="#00002E",
                               fg="white")
        title_label.pack(side="left")
        logout_button = tk.Button(top_bar_frame, text="Cerrar Sesión", font=("Verdana", 10), bg="lightgrey", fg="black",
                                  relief="raised", command=self._cerrar_sesion)
        logout_button.pack(side="right")
        save_faces_button = tk.Button(top_bar_frame, text="Guardar imagenes", font=("Verdana", 10), bg="lightgrey",
                                      fg="black", relief="raised", command=self._pantalla_guardar_datos)
        save_faces_button.pack(side="right", padx=(0, 10))

        main_panel = tk.Frame(self, bg="#B0C4DE", relief="sunken", bd=2)
        main_panel.pack(fill="both", expand=True, padx=20, pady=20)
        main_panel.grid_columnconfigure(0, weight=1)
        main_panel.grid_columnconfigure(1, weight=1)
        main_panel.grid_rowconfigure(0, weight=1)

        self.left_frame = tk.Frame(main_panel, bg="#B0C4DE")
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.left_frame.grid_rowconfigure(0, weight=1)
        self.detected_image_display = tk.Frame(self.left_frame, bg="lightgrey", relief="sunken", bd=1)
        self.detected_image_display.grid(row=0, column=0, columnspan=5, sticky="nsew", padx=5, pady=5)
        self.detected_image_display.grid_propagate(False)
        self.label_detected_main_image = tk.Label(self.detected_image_display, text="Rostro/Imagen de Consulta",
                                                  bg="lightgrey")
        self.label_detected_main_image.pack(expand=True)
        self.coincidence_label = tk.Label(self.left_frame, text="Nivel de coincidencia: N/A", font=("Verdana", 10),
                                          bg="#B0C4DE", anchor="w")
        self.coincidence_label.grid(row=1, column=0, columnspan=5, sticky="ew", padx=5, pady=(10, 0))
        thumbnails_nav_frame = tk.Frame(self.left_frame, bg="#B0C4DE")
        thumbnails_nav_frame.grid(row=2, column=0, columnspan=5, sticky="ew", pady=5)
        thumbnails_nav_frame.grid_columnconfigure(0, weight=0)
        thumbnails_nav_frame.grid_columnconfigure(1, weight=1)
        thumbnails_nav_frame.grid_columnconfigure(2, weight=0)
        self.arrow_left = tk.Button(thumbnails_nav_frame, text="⬅", font=("Verdana", 12),
                                    command=lambda: self._navigate_thumbnails(-1), state=tk.DISABLED)
        self.arrow_left.grid(row=0, column=0, padx=5)

        self.thumbnails_container = tk.Frame(thumbnails_nav_frame, bg="#B0C4DE")
        self.thumbnails_container.grid(row=0, column=1, sticky="ew")
        self.thumbnail_frames = []
        self.thumbnail_image_labels = []
        for i in range(4):
            thumb_frame = tk.Frame(self.thumbnails_container, bg="grey", relief="sunken", bd=1, width=80, height=80)
            thumb_frame.pack(side="left", padx=3, pady=5)
            thumb_frame.pack_propagate(False)
            self.thumbnail_frames.append(thumb_frame)
            thumb_label = tk.Label(thumb_frame, bg="grey")
            thumb_label.pack(expand=True, fill="both")
            self.thumbnail_image_labels.append(thumb_label)
        self.arrow_right = tk.Button(thumbnails_nav_frame, text="➡", font=("Verdana", 12),
                                     command=lambda: self._navigate_thumbnails(1), state=tk.DISABLED)
        self.arrow_right.grid(row=0, column=2, padx=5)
        self.detected_label = tk.Label(self.left_frame, text="Resultados de Coincidencias", font=("Verdana", 12),
                                       bg="#B0C4DE")
        self.detected_label.grid(row=3, column=0, columnspan=5, pady=5)

        right_frame = tk.Frame(main_panel, bg="#B0C4DE")
        right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
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

    # --- FUNCIONES PURAS DE UI ---
    def _clear_left_panel(self):
        self.label_detected_main_image.config(image='', text="Rostro/Imagen de Consulta")
        self.label_detected_main_image_tk = None
        self.coincidence_label.config(text="Nivel de coincidencia: N/A")
        for thumb_label in self.thumbnail_image_labels:
            thumb_label.config(image='', bg="grey")
        self.thumbnail_images_tk = []

    def _display_current_query_and_matches(self):
        if not self.current_matches_data:
            self._clear_left_panel()
            self.arrow_left.config(state=tk.DISABLED)
            self.arrow_right.config(state=tk.DISABLED)
            return

        self.current_query_index = max(0, min(self.current_query_index, len(self.current_matches_data) - 1))
        current_data = self.current_matches_data[self.current_query_index]
        query_image_path = current_data['query_image_path']
        query_face_index = current_data.get('query_face_index', None)
        comparison_result = current_data['matches']
        matches_list = comparison_result.get('matches', [])

        self._clear_left_panel()

        self.arrow_left.config(state=tk.NORMAL if self.current_query_index > 0 else tk.DISABLED)
        self.arrow_right.config(
            state=tk.NORMAL if self.current_query_index < len(self.current_matches_data) - 1 else tk.DISABLED)

        try:
            img_pil_query = Image.open(query_image_path)
            panel_width = self.detected_image_display.winfo_width()
            panel_height = self.detected_image_display.winfo_height()
            if panel_width < 100: panel_width = 600
            if panel_height < 100: panel_height = 600
            img_pil_query.thumbnail((panel_width, panel_height), Image.Resampling.LANCZOS)
            self.label_detected_main_image_tk = ImageTk.PhotoImage(img_pil_query)
            query_label_text = f"Imagen Original: {os.path.basename(query_image_path)}"
            if query_face_index is not None:
                query_label_text += f" (Rostro #{query_face_index + 1})"
            self.label_detected_main_image.config(image=self.label_detected_main_image_tk, text=query_label_text,
                                                  compound="top")
        except Exception as e:
            self.label_detected_main_image.config(image='',
                                                  text=f"Error al cargar consulta: {os.path.basename(query_image_path)}")
            print(f"Error al mostrar imagen de consulta en panel principal: {query_image_path}, Error: {e}")

        best_match_similarity = "N/A"
        if comparison_result['matches_found'] and matches_list:
            best_match_similarity = f"{matches_list[0]['similarity']:.2f}"
            self.coincidence_label.config(text=f"Nivel de coincidencia (Mejor Match): {best_match_similarity}")
            for i, match_data in enumerate(matches_list):
                if i >= len(self.thumbnail_image_labels):
                    break
                match_image_path = match_data['metadata'].get('face_image')
                if match_image_path and os.path.exists(match_image_path):
                    try:
                        img_pil_match = Image.open(match_image_path)
                        img_pil_match.thumbnail((80, 80), Image.Resampling.LANCZOS)
                        thumb_tk = ImageTk.PhotoImage(img_pil_match)
                        self.thumbnail_image_labels[i].config(image=thumb_tk, text="", bg="lightblue")
                        self.thumbnail_images_tk.append(thumb_tk)
                    except Exception as e:
                        self.thumbnail_image_labels[i].config(image='', text=f"Error {i + 1}", bg="red")
                        print(f"Error al cargar miniatura {match_image_path}: {e}")
                else:
                    self.thumbnail_image_labels[i].config(image='', text=f"No imagen {i + 1}", bg="grey")
                    print(f"Advertencia: Ruta de imagen de coincidencia no válida o no existe: {match_image_path}")
        else:
            self.coincidence_label.config(text="Nivel de coincidencia: Sin coincidencias")

    def _navigate_thumbnails(self, direction: int):
        new_index = self.current_query_index + direction
        if 0 <= new_index < len(self.current_matches_data):
            self.current_query_index = new_index
            self._display_current_query_and_matches()
        else:
            print(f"No hay más resultados en la dirección {direction}.")

    def _mostrar_imagen_en_panel(self, ruta_imagen, panel_display):
        try:
            img_pil = Image.open(ruta_imagen)
            panel_width = panel_display.winfo_width()
            panel_height = panel_display.winfo_height()
            if panel_width <= 1: panel_width = 600
            if panel_height <= 1: panel_height = 600
            img_pil.thumbnail((panel_width, panel_height), Image.Resampling.LANCZOS)
            self.imagen_tk_original = ImageTk.PhotoImage(img_pil)
            self.label_imagen_original.config(image=self.imagen_tk_original, text="")
        except Exception as e:
            messagebox.showerror("Error al cargar imagen", f"No se pudo mostrar la imagen: {ruta_imagen}\n\nError: {e}")
            self.btn_procesar.config(state=tk.DISABLED)
            self.label_imagen_original.config(image='', text="Error al cargar imagen")

    def _seleccionar_imagen_o_carpeta(self):
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

    def _manejar_subida_imagen(self):
        rutas = self._seleccionar_imagen_o_carpeta()

        if rutas:
            self.rutas_seleccionadas = rutas
            messagebox.showinfo("Éxito", f"Se han cargado {len(self.rutas_seleccionadas)} imagen(es).")
            self._mostrar_imagen_en_panel(self.rutas_seleccionadas[0], self.original_image_display)
            self._clear_left_panel()
            self.current_matches_data = []
            self.current_query_index = 0
            self.arrow_left.config(state=tk.DISABLED)
            self.arrow_right.config(state=tk.DISABLED)
            self.btn_procesar.config(state=tk.NORMAL)
        else:
            self.rutas_seleccionadas = []
            self.extracted_embeddings = []
            self.current_matches_data = []
            self.btn_procesar.config(state=tk.DISABLED)
            messagebox.showwarning("Cancelado", "No se seleccionó ninguna imagen o carpeta.")

    def _buscar_coincidencias(self):
        """
        REFACTORIZADA: Esta función ahora orquesta la lógica, llamando a las
        funciones de `face_logic.py` y actualizando la UI.
        """
        if not self.rutas_seleccionadas:
            messagebox.showwarning("Aviso", "Primero debes subir una o más imágenes.")
            return

        messagebox.showinfo("Procesando", f"Iniciando la extracción y comparación...")

        # Obtenemos el modelo y la base de datos de los recursos
        modelo = self.recursos.get("modelo")
        db = self.recursos.get("db")
        extraer_embedding_func = self.funciones['extraer_embedding']
        comparar_rostros_func = self.funciones['comparar_rostros']

        if not modelo or not db:
            messagebox.showerror("Error", "El modelo o la base de datos no están disponibles.")
            return

        self.extracted_embeddings = []
        self.current_matches_data = []
        errores = []

        # Recorremos cada imagen seleccionada
        for ruta_imagen in self.rutas_seleccionadas:
            try:
                # 1. Extraer embeddings usando la función `extraer_embedding`
                embeddings_from_current_image = extraer_embedding_func(modelo, ruta_imagen)

                if not embeddings_from_current_image:
                    errores.append(f"No se detectaron rostros en: {os.path.basename(ruta_imagen)}")
                    continue

                for face_idx, embedding in enumerate(embeddings_from_current_image):
                    self.extracted_embeddings.append(embedding)

                    # 2. Comparar el embedding usando la función `comparar_rostros`
                    comparison_result = comparar_rostros_func(db, embedding)

                    self.current_matches_data.append({
                        'query_image_path': ruta_imagen,
                        'query_face_index': face_idx,
                        'matches': comparison_result
                    })

            except Exception as e:
                errores.append(f"Error al procesar '{os.path.basename(ruta_imagen)}': {e}")

        # --- MANEJO DE ERRORES Y ACTUALIZACIÓN DE UI ---
        if errores:
            error_msg = "Se encontraron los siguientes problemas:\n" + "\n".join(errores)
            messagebox.showwarning("Problemas encontrados", error_msg)

        if not self.extracted_embeddings:
            messagebox.showwarning("Atención",
                                   "No se pudo extraer ningún embedding válido de las imágenes seleccionadas.")
            self._clear_left_panel()
            return

        if not self.current_matches_data:
            messagebox.showwarning("Resultados",
                                   "No se encontraron coincidencias para ninguna de las imágenes procesadas.")
            self._clear_left_panel()
            return

        messagebox.showinfo("Extracción y Comparación Completas",
                            f"Procesamiento finalizado. Se encontraron coincidencias para {len([d for d in self.current_matches_data if d['matches']['matches_found']])} de {len(self.current_matches_data)} rostros procesados.")

        self.current_query_index = 0
        self._display_current_query_and_matches()

    def _pantalla_guardar_datos(self):
        """Nos redirigimos a la pantalla donde guardamos los datos"""
        self.controlador("guardar")

    def _cerrar_sesion(self):
        """Usa el controlador para volver a la pantalla de login."""
        print("Cerrando sesión y volviendo al login...")
        self.controlador("login")
