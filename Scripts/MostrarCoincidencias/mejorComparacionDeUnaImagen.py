import cv2
import numpy as np
import os
from typing import Dict, Union


from typing import List

"""
PASO DONDE MOSTRAMOS AL USUARIO LA COMPARACIÓN ENTRE IMAGENES
"""
def mejor_comparacion(new_image_path: str, match: Dict):
    """
    Muestra visualmente la comparación entre imágenes

    Args:
        new_image_path: Ruta de la nueva imagen
        match: Diccionario de una coincidencia (con claves 'similarity', 'metadata', etc.)
    """
    # Cargar imágenes
    new_img = cv2.imread(new_image_path)
    db_img_path = match['metadata'].get('result_image') or match['metadata'].get('face_image')

    if db_img_path is None:
        print("No se encontró imagen de referencia en la base de datos")
        return

    db_img = cv2.imread(db_img_path)

    if new_img is None or db_img is None:
        print("Error al cargar imágenes para visualización")
        return

    # Redimensionar
    height = max(new_img.shape[0], db_img.shape[0])
    new_img = cv2.resize(new_img, (int(new_img.shape[1] * height / new_img.shape[0]), height))
    db_img = cv2.resize(db_img, (int(db_img.shape[1] * height / db_img.shape[0]), height))

    # Concatenar y mostrar
    comparison_img = np.hstack((db_img, new_img))

    text = f"Similitud: {match['similarity']:.2%}"
    cv2.putText(comparison_img, text, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow("Comparación Facial", comparison_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()