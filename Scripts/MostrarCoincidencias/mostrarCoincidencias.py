from typing import Dict, Union
import cv2
import os
from typing import List
import numpy as np

"""
PASO DONDE MUESTRA LA IMAGEN NUEVA CON LAS COINCIDENCIAS ENCONTRADAS >:D
"""
def mostrar_coincidencias(query_image_path: str, matches: List[Dict]):
    """Muestra la imagen de consulta junto a las coincidencias encontradas"""
    query_img = cv2.imread(query_image_path)
    if query_img is None:
        print("Error al cargar imagen de consulta")
        return

    # Crear lista de imágenes coincidentes
    match_images = []
    for match in matches:
        img_path = match['metadata']['face_image'] or match['metadata']['result_image']
        if img_path and os.path.exists(img_path):
            img = cv2.imread(img_path)
            # Añadir texto con similitud
            text = f"Sim: {match['similarity']:.2f}"
            cv2.putText(img, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            match_images.append(img)

    if not match_images:
        print("No hay imágenes para mostrar")
        return

    # Redimensionar todas las imágenes al mismo alto
    h = query_img.shape[0]
    resized_matches = [cv2.resize(img, (int(img.shape[1] * h / img.shape[0]), h))
                       for img in match_images]

    # Combinar imágenes horizontalmente
    combined = np.hstack([query_img] + resized_matches)

    # Mostrar resultados
    cv2.imshow(f"Consulta + {len(match_images)} Coincidencias", combined)
    cv2.waitKey(0)
    cv2.destroyAllWindows()