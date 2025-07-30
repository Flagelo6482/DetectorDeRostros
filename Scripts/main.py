import tkinter as tk
import glob
import os
import numpy as np
from insightface.app import FaceAnalysis
from typing import Dict

from app_controller import MainApplication
from face_logic import comparar_rostros,detectorDeRostros_lote, extraer_embedding, mostrar_coincidencias

if __name__ == "__main__":
    #Inicimos el modelo preentrenado
    """
    1.PRIMER PASO INICIAMOS EL MODELO QUE USAREMOS PARA LA COMPARACIÓN DE ROSTROS
    -FaceAnalysis:De insightface que usamos es un conjunto de modelos preentrenados de machine learning(redes neuronales profundas)
                  especializados en analisis facial
    -buffalo_l: Pack preentrenado que detecta los rostros, puntos faciales como ojo, nariz, boca, etc; genera vectores 
                numericos(embeddings) que representan rostros
    -CPUExecutionProvider: Indica que los calculos se haran en el CPU(no GPU por que no contamos con tarjeta grafica :p)
    """
    def inicializar_modelo():
        """Inicializa y devuelve el modelo de InsightFace"""
        model = FaceAnalysis(name="buffalo_l", providers=['CPUExecutionProvider'])
        model.prepare(ctx_id=0, det_size=(320, 320))
        return model

    #Iniciamos la base de datos
    def cargar_embeddings_db(db_root: str = "../outputs/") -> Dict[str, Dict]:
        """
        Carga todos los embeddings y metadatos de la base de datos

        Args:
            db_root: Directorio raíz con subcarpetas embeddings/, rostros/, resultados/

        Returns:
            Diccionario con {face_id: {embedding, face_image, result_image}}
        """
        # Rutas establecidas dentro de la carpeta "/outputs/"
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


    modelo = inicializar_modelo()
    db = cargar_embeddings_db()

    #Iniciamos la interfaz
    root = tk.Tk()

    #Llamamos a la interfaz padre que se encarga de las otras pantallas
    app = MainApplication(root, funciones={
        'comparar': lambda emb: comparar_rostros(db, emb),
        # 'detectar': detectorDeRostros_lote,
        'extraer': lambda img_path: extraer_embedding(modelo, img_path),
        # 'mostrar': mostrar_coincidencias
    },
    recursos={
        'modelo': modelo,
        'db': db
    })

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