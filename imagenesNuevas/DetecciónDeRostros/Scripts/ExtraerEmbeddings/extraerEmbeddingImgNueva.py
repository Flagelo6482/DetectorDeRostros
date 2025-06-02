import cv2
import numpy as np

"""
3.PASO DONDE EXTRAEMOS EL EMBEDDING DE UNA IMAGEN NUEVA QUE PASEMOS
"""
def extraer_embedding(model, image_path: str) -> np.ndarray:
    """
    Extrae embedding de una imagen (debe contener exactamente 1 rostro)

    Args:
        model: Modelo InsightFace inicializado
        image_path: Ruta de la imagen a procesar

    Returns:
        Array numpy con el embedding facial
    """
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"No se pudo cargar la imagen: {image_path}")

    faces = model.get(img)
    if len(faces) != 1:
        raise ValueError(f"La imagen debe contener exactamente 1 rostro. Encontrados: {len(faces)}")

    return faces[0].embedding