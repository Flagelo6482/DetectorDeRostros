import tkinter as tk
import glob
import os
from CargarEmbeddings.cargaDeEmbeddings import cargar_embeddings_db
from ComparaciónDeRostros.comparacionDeRostros import comparar_rostros
from ExtraerEmbeddings.extraerEmbeddingImgNueva import extraer_embedding
from MostrarCoincidencias.mostrarCoincidencias import mostrar_coincidencias
from ModeloParaDetección.inicioDeModelo import inicializar_modelo
from DeteccionYGuardadoDeRostros.GuardarRostros.detectorDeRostros_v4 import detectorDeRostros_lote
from Interface_UI.main_ui import MainApplication

# # 1.Iniciamos el modelo
modelo = inicializar_modelo()
# # 2.Cargamos la base de datos
db = cargar_embeddings_db("../outputs")
# # # 3.Cargamos las imagenes nuevas
# carpeta_imagenes = "../imagenesNuevas"
# rutas_imagenes = glob.glob(os.path.join(carpeta_imagenes, "*.jpg"))
#
# #PARA EL GUARDADO DE ROSTROS
#
# #Si la lista de imagenes no esta vacia llamamos a la función
# if rutas_imagenes:
#     print(f"Se encontraron {len(rutas_imagenes)} imágenes para procesar >:D")
#     resultados_lote = detectorDeRostros_lote(rutas_imagenes)
#     print("\nProcesamiento completado mire sus imagenes viejo pendejo")
# else:
#     print("No se encontraron imagenes pepepepepe")


# 4.Extramos el embedding de la imagen nueva y pasamos el modelo
img_new = "../imagenesNuevas/nueva_2.jpg"
img_new_embedding = extraer_embedding(modelo, img_new)
resultado_final = comparar_rostros(db, img_new_embedding, threshold=0.6)

mostrar_coincidencias(img_new, resultado_final['matches'])