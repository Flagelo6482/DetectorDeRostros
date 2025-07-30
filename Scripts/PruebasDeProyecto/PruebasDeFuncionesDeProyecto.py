#Prueba 1
from ModeloParaDetección.inicioDeModelo import inicializar_modelo
from CargarEmbeddings.cargaDeEmbeddings import cargar_embeddings_db
from ExtraerEmbeddings.extraerEmbeddingImgNueva import extraer_embedding
from ComparaciónDeRostros.comparacionDeRostros import comparar_rostros
from MostrarCoincidencias.mejorComparacionDeUnaImagen import mejor_comparacion

import os
import numpy as np

# 1.Iniciamos el modelo
modelo = inicializar_modelo()

# 2.Cargamos la base de datos
db = cargar_embeddings_db("../outputs")

# 2.1Cargamos una imagen nueva
img_new = "../imagenesNuevas/nueva_2.jpg"
# 3.Extramos el embedding de la imagen nueva y pasamos el modelo
img_new_embedding = extraer_embedding(modelo, img_new)

# 5.Comparamos la imagen nueva con los datos de nuestra base de datos
resultado = comparar_rostros(db, img_new_embedding, threshold=0.6)

# 6.Mostramos los resultados
if resultado['matches_found']:
    print("\n" + "=" * 50)
    print(f"🔍 {len(resultado['matches'])} COINCIDENCIAS ENCONTRADAS")
    print("=" * 50)

    # Top 3 coincidencias
    print("\n🏆 MEJORES COINCIDENCIAS:")
    for i, match in enumerate(resultado['matches'][:3], 1):
        print(f"\n  🥇 #{i} (Similitud: {match['similarity']:.2%})")
        print(f"  • ID: {match['face_id']}")
        print(f"  • Archivo: {os.path.basename(match['metadata']['face_image'])}")

    # Estadísticas
    similitudes = [m['similarity'] for m in resultado['matches']]
    print("\n📊 ESTADÍSTICAS:")
    print(f"  - Total de coincidencias: {len(resultado['matches'])}")
    print(f"  - Rango: {min(similitudes):.2%} - {max(similitudes):.2%}")
    print(f"  - Promedio: {np.mean(similitudes):.2%}")

    # Visualización
    mejor_comparacion(img_new, resultado['matches'][0])
else:
    print("\n🔍 NO SE ENCONTRARON COINCIDENCIAS SIGNIFICATIVAS")
    # print(f"El umbral actual es: {umbral * 100:.0f}% de similitud")

