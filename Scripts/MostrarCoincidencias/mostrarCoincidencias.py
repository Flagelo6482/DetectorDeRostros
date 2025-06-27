from typing import Dict, Union
import cv2
import os
from typing import List
import numpy as np


# --- Constantes para el tamaño de las imágenes ---
# Define un tamaño máximo deseado para el ANCHO y ALTO de las imágenes mostradas.
# Ajusta estos valores según el tamaño de tu pantalla y lo que consideres visible.
MAX_DISPLAY_WIDTH = 800  # Ancho máximo en píxeles
MAX_DISPLAY_HEIGHT = 600 # Alto máximo en píxeles

def resize_image_for_display_cv2(image: np.ndarray, max_width: int, max_height: int) -> np.ndarray:
    """
    Redimensiona una imagen de OpenCV para que se ajuste dentro de un tamaño máximo,
    manteniendo su relación de aspecto.
    """
    h, w = image.shape[:2]
    current_aspect_ratio = w / h

    # Calcula nuevas dimensiones manteniendo la relación de aspecto
    if w > max_width or h > max_height:
        # Calcular la escala necesaria para ajustarse al ancho máximo
        scale_width = max_width / w
        # Calcular la escala necesaria para ajustarse al alto máximo
        scale_height = max_height / h

        # Usar la escala más pequeña para asegurar que la imagen quepa completamente
        scale = min(scale_width, scale_height)

        new_w = int(w * scale)
        new_h = int(h * scale)

        # Solo redimensionar si las nuevas dimensiones son diferentes a las originales
        if new_w != w or new_h != h:
            return cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
    return image



"""
PASO DONDE MUESTRA LA IMAGEN NUEVA CON LAS COINCIDENCIAS ENCONTRADAS >:D
"""
def mostrar_coincidencias(query_image_path: str, matches: List[Dict]):
    """Muestra la imagen de consulta junto a las coincidencias encontradas"""
    query_img = cv2.imread(query_image_path)
    if query_img is None:
        print("Error al cargar imagen de consulta")
        return

    # Redimensionar la imagen de consulta
    query_img_resized = resize_image_for_display_cv2(query_img, MAX_DISPLAY_WIDTH, MAX_DISPLAY_HEIGHT)

    # 2. Crear lista de imágenes coincidentes, redimensionarlas y añadir texto
    match_images_resized = []
    for match in matches:
        # Como hemos discutido, asegúrate de que la clave 'crop_path' sea la correcta
        # según cómo tu detectorDeRostros_v4 guarda los datos.
        img_path = match['metadata'].get('crop_path')  # Preferir 'crop_path' si guarda rostros recortados

        # Fallback a otras claves si 'crop_path' no existe o está vacío
        if not img_path:
            img_path = match['metadata'].get('face_image')
        if not img_path:
            img_path = match['metadata'].get(
                'result_image')  # Este suele ser la imagen completa detectada, no solo el rostro

        if not img_path or not os.path.exists(img_path):
            print(
                f"Advertencia: No se encontró una ruta de imagen válida o el archivo no existe para la coincidencia con ID {match.get('face_id', 'N/A')}. Ruta intentada: {img_path}")
            continue  # Salta a la siguiente coincidencia

        img = cv2.imread(img_path)
        if img is None:
            print(f"Advertencia: Error al cargar imagen de coincidencia en {img_path}. cv2.imread devolvió None.")
            continue

        # Redimensionar la imagen de coincidencia
        img_resized = resize_image_for_display_cv2(img, MAX_DISPLAY_WIDTH, MAX_DISPLAY_HEIGHT)

        # Añadir texto con similitud. Asegúrate de que la posición del texto sea visible
        text = f"Sim: {match['similarity']:.2f}"
        # Ajusta la posición del texto para que siempre esté dentro de la imagen redimensionada
        text_pos_x = 10
        text_pos_y = img_resized.shape[0] - 10  # Cerca del borde inferior

        # Asegúrate de que la fuente y escala son adecuadas para el tamaño redimensionado
        cv2.putText(img_resized, text, (text_pos_x, text_pos_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        match_images_resized.append(img_resized)

    if not match_images_resized:
        print("No hay imágenes coincidentes para mostrar.")
        # Podrías mostrar solo la imagen de consulta si no hay coincidencias
        # cv2.imshow("Imagen de Consulta", query_img_resized)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        return

    # 3. Normalizar el alto de todas las imágenes combinadas para que hstack funcione
    # Encuentra la altura mínima entre todas las imágenes redimensionadas (incluyendo la de consulta)
    # Esto asegura que todas las imágenes tengan la misma altura antes de concatenarlas horizontalmente.
    min_height = min([img.shape[0] for img in [query_img_resized] + match_images_resized])

    # Re-redimensionar al alto mínimo (si es necesario)
    final_query_img = cv2.resize(query_img_resized, (
    int(query_img_resized.shape[1] * min_height / query_img_resized.shape[0]), min_height))
    final_match_images = [cv2.resize(img, (int(img.shape[1] * min_height / img.shape[0]), min_height))
                          for img in match_images_resized]

    # 4. Combinar imágenes horizontalmente
    combined = np.hstack([final_query_img] + final_match_images)

    # 5. Mostrar resultados
    cv2.imshow(f"Consulta + {len(match_images_resized)} Coincidencias", combined)
    cv2.waitKey(0)
    cv2.destroyAllWindows()