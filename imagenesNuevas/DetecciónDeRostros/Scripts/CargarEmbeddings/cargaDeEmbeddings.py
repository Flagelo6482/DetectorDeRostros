import os
import numpy as np
from typing import Dict, Union

"""
2.CARGAMOS LOS DATOS DE NUESTRA BASE DE DATOS 
"""
def cargar_embeddings_db(db_root: str = "../outputs/") -> Dict[str, Dict]:
    """
    Carga todos los embeddings y metadatos de la base de datos

    Args:
        db_root: Directorio raíz con subcarpetas embeddings/, rostros/, resultados/

    Returns:
        Diccionario con {face_id: {embedding, face_image, result_image}}
    """
    #Rutas establecidas dentro de la carpeta "/outputs/"
    embeddings_dir = os.path.join(db_root, "embeddings")
    faces_dir = os.path.join(db_root, "rostros")
    results_dir = os.path.join(db_root, "resultados")

    """
    db: diccionario vacio
    Iteramos en la ruta "embeddings_dir" los archivos de embeddings guardados con NumPy
    face_id: Extramos un nombre del archivo
    """
    db = {}
    for emb_file in os.listdir(embeddings_dir):
        if emb_file.endswith('.npy'):
            face_id = os.path.splitext(emb_file)[0].split('_')[-1]
            emb_path = os.path.join(embeddings_dir, emb_file)

            """
            Guardamos los rostros en "rostro-face_img_path" en "faces_dir"
            Guardamos los resultados de "result_img_path" en "results_dir"
            """
            face_img_path = os.path.join(faces_dir, f"rostro_{face_id}.jpg")
            result_img_path = os.path.join(results_dir, f"detectados_{face_id}.jpg")

            """
            Agregamos al diccionario "db" una entrada con "face_id" como clave y con el contenido
            El "embedding" cargado
            La ruta hacia la imagen del ROSTRO
            La ruta a la imagen de RESULTADOS
            """
            db[face_id] = {
                'embedding': np.load(emb_path),
                'face_image': face_img_path if os.path.exists(face_img_path) else None,
                'result_image': result_img_path if os.path.exists(result_img_path) else None
            }
    return db
