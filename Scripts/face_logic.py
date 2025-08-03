from sklearn.metrics.pairwise import cosine_similarity
import cv2
import os
import hashlib
from typing import Dict, List, Union
from insightface.app import FaceAnalysis
import numpy as np


def detectorDeRostros_lote(
    lista_imagenes: List[str],
    output_dir: str = "../outputs",
    save_cropped_faces: bool = True,
)-> List[Dict]:
    """
    Detectamos los rostros en una imagen y devuelve metadatos con resultados.

    Args:
        :param lista_imagenes: Ruta completa de la imagen a procesar.
        :param output_dir: Carpeta base donde se guardarán los resultados.
        :param save_cropped_faces: Si True, guarda los rostros recortados individualmente.
    Returns:
        Dict: {
            "image": np.ndarray,
            "faces": List[Dict],
            "output_paths": Dict
        }
    """
    #1.Configuración inicial de paths
    os.makedirs(output_dir, exist_ok=True)
    resultados_dir = os.path.join(output_dir, "resultados")
    rostros_dir = os.path.join(output_dir, "rostros")
    embeddings_dir = os.path.join(output_dir, "embeddings")
    os.makedirs(resultados_dir, exist_ok=True)
    os.makedirs(rostros_dir, exist_ok=True)
    os.makedirs(embeddings_dir, exist_ok=True)

    # 2. Inicializamos del modelo (¡SE HACE UNA SOLA VEZ, FUERA DEL BUCLE!)
    print("Cargando modelo de reconocimiento facial...")
    app = FaceAnalysis(name="buffalo_l", providers=['CPUExecutionProvider'])
    app.prepare(ctx_id=0, det_thresh=0.3, det_size=(320, 320))

    resultados_totales = []
    # Bucle principal para procesar cada imagen de la lista
    for img_path in lista_imagenes:
        print(f"\n--- Procesando imagen: {img_path} ---")

        # 3. Cargar imagen (CORREGIDO: Usando imdecode para evitar problemas con la ruta)
        try:
            # Leer el archivo como bytes
            with open(img_path, 'rb') as f:
                bytes_data = f.read()
            # Convertir los bytes a un array de numpy
            nparr = np.frombuffer(bytes_data, np.uint8)
            # Decodificar la imagen con OpenCV
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            if image is None:
                print(f"ADVERTENCIA: cv2.imdecode no pudo decodificar la imagen desde los bytes para: {img_path}. Saltando.")
                continue

        except Exception as e:
            print(f"ADVERTENCIA: No se pudo cargar la imagen desde la ruta {img_path}. Error: {e}. Saltando.")
            continue

        # 4. Detección de rostros
        faces = app.get(image)
        print(f"Rostros detectados: {len(faces)}")

        metadata = []
        # 5. Procesamos cada rostro detectado en ESTA imagen
        for i, face in enumerate(faces):
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
    return resultados_totales


def mejor_comparacion(new_image_path: str, match: Dict):
    """
    Muestra visualmente la comparación entre imágenes
    """
    new_img = cv2.imread(new_image_path)
    db_img_path = match['metadata'].get('result_image') or match['metadata'].get('face_image')

    if db_img_path is None:
        print("No se encontró imagen de referencia en la base de datos")
        return

    db_img = cv2.imread(db_img_path)

    if new_img is None or db_img is None:
        print("Error al cargar imágenes para visualización")
        return

    height = max(new_img.shape[0], db_img.shape[0])
    new_img = cv2.resize(new_img, (int(new_img.shape[1] * height / new_img.shape[0]), height))
    db_img = cv2.resize(db_img, (int(db_img.shape[1] * height / db_img.shape[0]), height))

    comparison_img = np.hstack((db_img, new_img))

    text = f"Similitud: {match['similarity']:.2%}"
    cv2.putText(comparison_img, text, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow("Comparación Facial", comparison_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def extraer_embedding(model, image_path: str) -> List[np.ndarray]:
    """
    Extrae embeddings de una imagen (puede contener 0, 1 o múltiples rostros).
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"El archivo no existe en la ruta especificada: {image_path}")
    try:
        with open(image_path, 'rb') as f:
            bytes_data = f.read()
        nparr = np.frombuffer(bytes_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    except Exception as e:
        raise IOError(f"No se pudo cargar o decodificar la imagen: {image_path}. Error: {e}")

    if img is None:
        raise ValueError(
            f"No se pudo cargar la imagen. Es posible que el archivo esté corrupto o no sea una imagen válida: {image_path}")

    faces = model.get(img)
    return [face.embedding for face in faces]

def comparar_rostros(
    db: Dict,
    new_embedding: np.ndarray,
    threshold: float = 0.6,
    top_n: int = None
) -> Dict[str, Union[bool, List[Dict]]]:
    """
    Compara un nuevo embedding con la base de datos y devuelve múltiples coincidencias
    """
    matches = []
    # Convertir el embedding a una forma compatible con cosine_similarity
    new_embedding_2d = new_embedding.reshape(1, -1)

    for face_id, data in db.items():
        if 'embedding' in data and isinstance(data['embedding'], np.ndarray):
            db_embedding_2d = data['embedding'].reshape(1, -1)
            similarity = cosine_similarity(new_embedding_2d, db_embedding_2d)[0][0]

            if similarity >= threshold:
                matches.append({
                    'face_id': face_id,
                    'similarity': similarity,
                    'metadata': data
                })

    matches.sort(key=lambda x: x['similarity'], reverse=True)

    if top_n is not None and top_n > 0:
        matches = matches[:top_n]

    return {
        'matches_found': len(matches) > 0,
        'matches': matches,
        'query_embedding': new_embedding
    }

MAX_DISPLAY_WIDTH = 800
MAX_DISPLAY_HEIGHT = 600

def resize_image_for_display_cv2(image: np.ndarray, max_width: int, max_height: int) -> np.ndarray:
    """
    Redimensiona una imagen de OpenCV para que se ajuste dentro de un tamaño máximo,
    manteniendo su relación de aspecto.
    """
    h, w = image.shape[:2]
    current_aspect_ratio = w / h
    if w > max_width or h > max_height:
        scale_width = max_width / w
        scale_height = max_height / h
        scale = min(scale_width, scale_height)
        new_w = int(w * scale)
        new_h = int(h * scale)
        if new_w != w or new_h != h:
            return cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
    return image

def mostrar_coincidencias(query_image_path: str, matches: List[Dict]):
    """Muestra la imagen de consulta junto a las coincidencias encontradas"""
    query_img = cv2.imread(query_image_path)
    if query_img is None:
        print("Error al cargar imagen de consulta")
        return
    query_img_resized = resize_image_for_display_cv2(query_img, MAX_DISPLAY_WIDTH, MAX_DISPLAY_HEIGHT)
    match_images_resized = []
    for match in matches:
        img_path = match['metadata'].get('crop_path')
        if not img_path:
            img_path = match['metadata'].get('face_image')
        if not img_path:
            img_path = match['metadata'].get('result_image')
        if not img_path or not os.path.exists(img_path):
            print(f"Advertencia: No se encontró una ruta de imagen válida o el archivo no existe para la coincidencia con ID {match.get('face_id', 'N/A')}. Ruta intentada: {img_path}")
            continue
        img = cv2.imread(img_path)
        if img is None:
            print(f"Advertencia: Error al cargar imagen de coincidencia en {img_path}. cv2.imread devolvió None.")
            continue
        img_resized = resize_image_for_display_cv2(img, MAX_DISPLAY_WIDTH, MAX_DISPLAY_HEIGHT)
        text = f"Sim: {match['similarity']:.2f}"
        text_pos_x = 10
        text_pos_y = img_resized.shape[0] - 10
        cv2.putText(img_resized, text, (text_pos_x, text_pos_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        match_images_resized.append(img_resized)

    if not match_images_resized:
        print("No hay imágenes coincidentes para mostrar.")
        return
    min_height = min([img.shape[0] for img in [query_img_resized] + match_images_resized])
    final_query_img = cv2.resize(query_img_resized, (
    int(query_img_resized.shape[1] * min_height / query_img_resized.shape[0]), min_height))
    final_match_images = [cv2.resize(img, (int(img.shape[1] * min_height / img.shape[0]), min_height))
                          for img in match_images_resized]
    combined = np.hstack([final_query_img] + final_match_images)
    cv2.imshow(f"Consulta + {len(match_images_resized)} Coincidencias", combined)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def cosine_similarity_func(emb1: np.ndarray, emb2: np.ndarray) -> float:
    """Calcula la similitud coseno entre dos embeddings."""
    if isinstance(emb1, list) and isinstance(emb2, list):
        emb1 = emb1[0]
        emb2 = emb2[0]
    return np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
