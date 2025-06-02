from insightface.app import FaceAnalysis

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