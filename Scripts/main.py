import tkinter as tk
import os
import numpy as np
from insightface.app import FaceAnalysis
from typing import Dict

from app_controller import MainApplication
from face_logic import comparar_rostros, detectorDeRostros_lote, extraer_embedding, mostrar_coincidencias

if __name__ == "__main__":
    def inicializar_modelo():
        """Inicializa y devuelve el modelo de InsightFace"""
        model = FaceAnalysis(name="buffalo_l", providers=['CPUExecutionProvider'])
        model.prepare(ctx_id=0, det_size=(320, 320))
        return model

    def cargar_embeddings_db(db_root: str = "../outputs/") -> Dict[str, Dict]:
        """
        Carga todos los embeddings y metadatos de la base de datos.
        """
        embeddings_dir = os.path.join(db_root, "embeddings")
        faces_dir = os.path.join(db_root, "rostros")
        results_dir = os.path.join(db_root, "resultados")

        db = {}
        # Cargamos los archivos .npy
        for emb_file in os.listdir(embeddings_dir):
            if emb_file.endswith('.npy'):
                face_id = os.path.splitext(emb_file)[0].split('_')[-1]
                emb_path = os.path.join(embeddings_dir, emb_file)

                face_img_path = os.path.join(faces_dir, f"rostro_{face_id}.jpg")
                result_img_path = os.path.join(results_dir, f"detectados_{face_id}.jpg")

                db[face_id] = {
                    'embedding': np.load(emb_path),
                    'face_image': face_img_path if os.path.exists(face_img_path) else None,
                    'result_image': result_img_path if os.path.exists(result_img_path) else None
                }
        return db

    # Inicializamos el modelo y la base de datos una sola vez
    modelo = inicializar_modelo()
    db = cargar_embeddings_db()

    # Preparamos los diccionarios de recursos y funciones para la aplicación
    recursos = {
        'modelo': modelo,
        'db': db
    }

    funciones = {
        'detector_lote': detectorDeRostros_lote,
        'mostrar_coincidencias': mostrar_coincidencias,
        'extraer_embedding': extraer_embedding,
        'comparar_rostros': comparar_rostros
        # Las funciones de 'extraer' y 'comparar' ya no se pasan aquí,
        # ya que se importan directamente en `detector_dash.py`.
    }

    # Iniciamos la interfaz
    root = tk.Tk()
    app = MainApplication(root, funciones, recursos)
    root.mainloop()









# # # 1.Iniciamos el modelo
#
# # # 2.Cargamos la base de datos
# db = cargar_embeddings_db("../outputs")
# # # # 3.Cargamos las imagenes nuevas
# carpeta_imagenes = "../imagenesNuevas"
# rutas_imagenes = glob.glob(os.path.join(carpeta_imagenes, "*.jpg"))
# #
# # #PARA EL GUARDADO DE ROSTROS
# #
# # #Si la lista de imagenes no esta vacia llamamos a la función
# # if rutas_imagenes:
# #     print(f"Se encontraron {len(rutas_imagenes)} imágenes para procesar >:D")
# #     resultados_lote = detectorDeRostros_lote(rutas_imagenes)
# #     print("\nProcesamiento completado mire sus imagenes viejo pendejo")
# # else:
# #     print("No se encontraron imagenes pepepepepe")
#
#
# # 4.Extramos el embedding de la imagen nueva y pasamos el modelo
# # img_new = "../imagenesNuevas/nueva_2.jpg"
# # img_new_embedding = extraer_embedding(modelo, img_new)
# # resultado_final = comparar_rostros(db, img_new_embedding, threshold=0.6)
# #
# # mostrar_coincidencias(img_new, resultado_final['matches'])
#
# #INICIAMOS LA VENTANA PRINCIPAL DE LA INTERFAZ PARA MOSTRARLA
# root = tk.Tk()  #Ventana principal
# app = MainApplication(root, modelo, db)
# root.mainloop()