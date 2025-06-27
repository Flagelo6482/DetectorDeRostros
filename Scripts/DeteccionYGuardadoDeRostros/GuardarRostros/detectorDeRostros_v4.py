import cv2
import os
import numpy as np
import hashlib
from typing import Dict, List, Union
from insightface.app import FaceAnalysis
"""
Paso 1 para detectar los rostros de una imagen, luego guarda los resultados
"""

def detectorDeRostros_lote(
        lista_imagenes: List[str],
        output_dir: str = "../outputs",
        save_cropped_faces: bool = True,
    )-> List[Dict]: # Ahora devuelve una lista de diccionarios, uno por imagen
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

    # 2. Inicializamos del modelo (¡SE HACE UNA SOLA VEZ, FUERA DEL BUCLE!)
    print("Cargando modelo de reconocimiento facial...")
    app = FaceAnalysis(name="buffalo_l", providers=['CPUExecutionProvider'])
    app.prepare(ctx_id=0, det_thresh=0.3, det_size=(320, 320))

    resultados_totales = [] #Lista para guardar los resultados de todas las imagenes
    # Bucle principal para procesar cada imagen de la lista
    for img_path in lista_imagenes:
        print(f"\n--- Procesando imagen: {img_path} ---")

        # 3. Cargar imagen
        image = cv2.imread(img_path)
        if image is None:
            print(f"ADVERTENCIA: No se pudo cargar la imagen en {img_path}. Saltando.")
            continue  # Salta a la siguiente imagen

        # 4. Detección de rostros
        faces = app.get(image)
        print(f"Rostros detectados: {len(faces)}")

        metadata = []
        # 5. Procesamos cada rostro detectado en ESTA imagen
        for i, face in enumerate(faces):
            # (El resto de tu lógica para procesar un rostro va aquí)
            # Es casi idéntica, solo ajustamos las rutas de salida
            try:
                bbox = face.bbox.astype(int)
                if (bbox[0] >= bbox[2]) or (bbox[1] >= bbox[3]): continue
                bbox = [max(0, bbox[0]), max(0, bbox[1]), min(image.shape[1], bbox[2]), min(image.shape[0], bbox[3])]

                rostro_recortado = image[bbox[1]:bbox[3], bbox[0]:bbox[2]]
                if rostro_recortado.size == 0: continue

                hash_obj = hashlib.md5(rostro_recortado.tobytes())
                hash_str = hash_obj.hexdigest()

                embedding_path = os.path.join(embeddings_dir, f"embedding_{hash_str}.npy")
                np.save(embedding_path, face.embedding)

                rostro_path = None
                if save_cropped_faces:
                    rostro_path = os.path.join(rostros_dir, f"rostro_{hash_str}.jpg")
                    cv2.imwrite(rostro_path, rostro_recortado)

                metadata.append({
                    "bbox": bbox,
                    "confidence": float(face.det_score),
                    "face_id": hash_str,
                    "embedding_path": embedding_path,
                    "crop_path": rostro_path
                })
                cv2.rectangle(image, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)
            except Exception as e:
                print(f"Error procesando un rostro en {img_path}: {str(e)}")
                continue

        # 6. Guardamos imagen con detecciones
        nombre_de_archivo = os.path.basename(img_path)
        resultado_path = os.path.join(resultados_dir, f"detectados_{nombre_de_archivo}")
        cv2.imwrite(resultado_path, image)

        # 7. Guardar los resultados de ESTA imagen
        resultados_totales.append({
            "source_image": img_path,
            "faces": metadata,
            "output_image_path": resultado_path
        })

    # Nota: He quitado cv2.imshow() porque no es práctico para procesar lotes.

    return resultados_totales