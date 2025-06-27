import tkinter as tk
from tkinter import ttk # Para botones más modernos si se quiere, aunque usaremos tk.Button para el estilo original
def create_rat_detector_gui():
    window = tk.Tk()
    window.title("Detector de Ratas")
    window.geometry("800x600") # Tamaño inicial razonable
    window.configure(bg="#202060") # Color de fondo oscuro (azul oscuro)

    # --- 1. Barra Superior (Encabezado) ---
    header_frame = tk.Frame(window, bg="#202060", height=80) # Mismo color que la ventana
    header_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10) # Arriba, ocupa todo el ancho

    # Configurar las columnas del header_frame para el grid
    header_frame.grid_columnconfigure(0, weight=1) # Columna para el título
    header_frame.grid_columnconfigure(1, weight=0) # Columna para el botón (no se expande)

    # Título "Detector de Ratas"
    title_label = tk.Label(header_frame, text="Detector de Ratas",
                           font=("Arial", 24, "bold"), fg="white", bg="#202060")
    title_label.grid(row=0, column=0, sticky="w", padx=(50,0)) # Alineado a la izquierda, puedes ajustar el padx


    # Botón "Cerrar Sesión"
    close_button = tk.Button(header_frame, text="Cerrar Sesión",
                             font=("Arial", 10), bg="white", fg="black", padx=10, pady=5)
    close_button.grid(row=0, column=1, sticky="e", padx=(0,20)) # Alineado a la derecha



    # --- 2. Área Principal (Contenido con los dos paneles) ---
    main_content_frame = tk.Frame(window, bg="#A0D0E0", padx=20, pady=20) # Fondo azul claro
    main_content_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Configurar las columnas del main_content_frame para los dos paneles
    main_content_frame.grid_columnconfigure(0, weight=1) # Panel izquierdo
    main_content_frame.grid_columnconfigure(1, weight=1) # Panel derecho
    main_content_frame.grid_rowconfigure(0, weight=1) # Única fila para los paneles

    # --- 2.1. Panel Izquierdo ("Imágenes detectadas") ---
    left_panel_frame = tk.Frame(main_content_frame, bg="lightgray", bd=2, relief="solid")
    left_panel_frame.grid(row=0, column=0, padx=(0, 10), sticky="nsew") # padx a la derecha para separar paneles

    # Área de imagen (simulada con un Label grande)
    detected_image_area = tk.Label(left_panel_frame, text="[Área de Imagen Detectada]",
                                   bg="lightgray", fg="gray", relief="sunken", bd=1)
    detected_image_area.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

    # Nivel de coincidencia
    coincidence_label = tk.Label(left_panel_frame, text="Nivel de coincidencia:",
                                 font=("Arial", 10), bg="lightgray")
    coincidence_label.pack(side=tk.TOP, pady=(0, 5), anchor="w", padx=20) # Alineado a la izquierda

    # Contenedor para botones de navegación (flechas y cuadrados)
    navigation_frame = tk.Frame(left_panel_frame, bg="lightgray")
    navigation_frame.pack(side=tk.TOP, pady=10)

    # Botón izquierda
    left_arrow_btn = tk.Button(navigation_frame, text="<", font=("Arial", 12), width=3)
    left_arrow_btn.pack(side=tk.LEFT, padx=(0, 5))

    # Cuadrados de navegación (simulados con Labels)
    for _ in range(4):
        square = tk.Label(navigation_frame, text="", bg="gray", width=4, height=1, relief="raised", bd=1)
        square.pack(side=tk.LEFT, padx=2)

    # Botón derecha
    right_arrow_btn = tk.Button(navigation_frame, text=">", font=("Arial", 12), width=3)
    right_arrow_btn.pack(side=tk.LEFT, padx=(5, 0))

    # Etiqueta "Imágenes detectadas" en la parte inferior
    bottom_detected_label = tk.Label(left_panel_frame, text="Imágenes detectadas",
                                    font=("Arial", 12, "bold"), bg="lightgray")
    bottom_detected_label.pack(side=tk.BOTTOM, pady=10)

    # --- 2.2. Panel Derecho ("Imagen original") ---
    right_panel_frame = tk.Frame(main_content_frame, bg="lightgray", bd=2, relief="solid")
    right_panel_frame.grid(row=0, column=1, padx=(10, 0), sticky="nsew") # padx a la izquierda para separar

    # Área de imagen original (simulada con un Label grande)
    original_image_area = tk.Label(right_panel_frame, text="[Área de Imagen Original]",
                                   bg="lightgray", fg="gray", relief="sunken", bd=1)
    original_image_area.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

    # Etiqueta "Imagen original"
    original_label = tk.Label(right_panel_frame, text="Imagen original",
                              font=("Arial", 12, "bold"), bg="lightgray")
    original_label.pack(pady=(0, 10))

    # Botón "Subir Imagen"
    upload_button = tk.Button(right_panel_frame, text="Subir Imagen",
                             font=("Arial", 10), bg="white", fg="black", padx=15, pady=8)
    upload_button.pack(pady=(0, 20))


    window.mainloop()
create_rat_detector_gui()