import cv2
import os
import numpy as np
import hashlib
from typing import Dict, List, Union
from insightface.app import FaceAnalysis
"""
Paso 1 para detectar los rostros de una imagen, luego guarda los resultados
"""

def detectorDeRostros(
        img: str,
        output_dir: str = "../outputs",
        save_cropped_faces: bool = True,
    )-> Dict[str, Union[List[Dict], str, np.ndarray]]:
    """
    Detectamos los rostros en una imagen y devuelve metadatos con resultados.

    Args:
        :param img: Ruta completa de la imagen a procesar.
        :param output_dir: Carpeta base donde se guardarán los resultados.
        :param save_cropped_faces: Si True, guarda los rostros recortados individualmente.
    Returns:
        Dict: {
            "image": np.ndarray,  # Imagen con detecciones
            "faces": List[Dict],  # Metadatos de cada rostro
            "output_paths": Dict  # Rutas de archivos guardados
        }

    Ejemplo:
        resultados = detectorDeRostros(
            image_path="imagenes/familia.jpg",
            output_dir="resultados",
            save_cropped_faces=True
        )
    """


    #1.Configuración inicial de paths
    os.makedirs(output_dir, exist_ok=True)
    resultados_dir = os.path.join(output_dir, "resultados")
    rostros_dir = os.path.join(output_dir, "rostros")
    embeddings_dir = os.path.join(output_dir, "embeddings")  # Nuevo directorio
    os.makedirs(resultados_dir, exist_ok=True)
    os.makedirs(rostros_dir, exist_ok=True)
    os.makedirs(embeddings_dir, exist_ok=True)  # Asegurar que existe

    #2.Inicializamos del modelo (parametros fijos)
    app = FaceAnalysis(name="buffalo_l", providers=['CPUExecutionProvider'])
    app.prepare(ctx_id=0, det_thresh=0.3, det_size=(320, 320))  # Parámetros sensibles
    """
        Configuración del modelo

        buffalo_l: Modelo preentrenado para detección y análisis facial.
        det_thresh=0.3: Umbral bajo para detectar rostros incluso con poca confianza (útil para rostros parciales o pequeños).
        det_size=(320, 320): Tamaño de procesamiento (menor = más sensible a rostros pequeños).
    """

    #3.Cargar imagen(usando la ruta proporcionada "'../imagenes/familia2.jpg'")
    image = cv2.imread(img)  # Asegúrate de que la imagen esté en la misma carpeta
    if image is None:
        raise FileNotFoundError(f"No se pudo cargar la imagen en {img}")

    #4.Deteccion de rostros
    """
        Detectar rostros

        bbox: Coordenadas del cuadro delimitador [x1, y1, x2, y2].
        landmark: Puntos clave (ojos, nariz, boca).
        embedding: Vector de características (no usado en este script).
        """
    faces = app.get(image)
    print(f"Rostros detectados: {len(faces)}")
    output_paths = {}
    metadata = []

    #5.Procesamos cada rostro detectado
    for i, face in enumerate(faces):
        try:
            bbox = face.bbox.astype(int)

            # Validación del bounding box
            if (bbox[0] >= bbox[2]) or (bbox[1] >= bbox[3]):
                continue

            bbox = [
                max(0, bbox[0]), max(0, bbox[1]),
                min(image.shape[1], bbox[2]), min(image.shape[0], bbox[3])
            ]

            # Generar hash único basado en el rostro
            rostro = image[bbox[1]:bbox[3], bbox[0]:bbox[2]]
            if rostro.size == 0:
                continue

            hash_obj = hashlib.md5(rostro.tobytes())
            hash_str = hash_obj.hexdigest()

            # Guardar embedding con nombre único
            embedding_path = os.path.join(embeddings_dir, f"embedding_{hash_str}.npy")
            np.save(embedding_path, face.embedding)

            # Guardar rostro recortado
            if save_cropped_faces:
                rostro_path = os.path.join(rostros_dir, f"rostro_{hash_str}.jpg")
                cv2.imwrite(rostro_path, rostro)

            metadata.append({
                "bbox": bbox,
                "confidence": float(face.det_score),
                "face_id": hash_str,  # Usamos el hash como ID único
                "embedding": face.embedding.tolist(),
                "embedding_path": embedding_path,
                "crop_path": rostro_path if save_cropped_faces else None
            })

            cv2.rectangle(image, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)

        except Exception as e:
            print(f"Error procesando rostro: {str(e)}")
            continue

    #6.Guardamos imagen con detecciones
    nombre_de_archivo = os.path.basename(img)
    resultado_path = os.path.join(resultados_dir, f"detectados_{nombre_de_archivo}")
    cv2.imwrite(resultado_path, image)
    output_paths["result_image"] = resultado_path

    #7.Mostrar resultados(opcional)
    cv2.imshow("Deteccion de Rostros", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return {
        "image": img,
        "faces": metadata,
        "output_paths":{
            **output_paths,
            "embeddings_dir": embeddings_dir    #Añadir la ruta del directorio
        }
    }