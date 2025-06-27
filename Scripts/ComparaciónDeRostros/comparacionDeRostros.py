from typing import Dict, Union
import numpy as np
from typing import List
from sklearn.metrics.pairwise import cosine_similarity

"""
4. PASO DONDE COMPARAMOS UNA IMAGEN NUEVA CON LAS IMAGENES DE NUESTRA BASE DE DATOS
PARA OBTENER UNA O MULTIPLES COINCIDENCIAS
"""

def comparar_rostros(
        db: Dict,
        new_embedding: np.ndarray,
        threshold: float = 0.6,
        top_n: int = None
) -> Dict[str, Union[bool, List[Dict]]]:
    """
    Compara un nuevo embedding con la base de datos y devuelve múltiples coincidencias

    Args:
        db: Base de datos de embeddings
        new_embedding: Embedding a comparar
        threshold: Umbral mínimo de similitud (0-1)
        top_n: Máximo número de coincidencias a devolver (None para todas)

    Returns:
        Dict: {
            'matches_found': bool,  # True si al menos una coincidencia, si la lista no esta vacia osea es mayor a 0,
            encontro almenos una coincidencia que supero el umbral, es false si no se encontro ninguna coincidencia
            'matches': List[Dict],  # Lista ordenada de coincidencias que superaron el umbral(o las top_n mejores si se
            especifico)
            'query_embedding': np.ndarray  # Embedding de consulta (opcional)
        }
    """
    matches = []

    for face_id, data in db.items():
        similarity = cosine_similarity([new_embedding], [data['embedding']])[0][0]

        if similarity >= threshold:
            matches.append({
                'face_id': face_id,
                'similarity': similarity,
                'metadata': data  # Diccionario que Incluye toda la información relevante del rostro(embedding, ruta, ruta del corte)
            })

    # Ordenar coincidencias por similitud (de mayor a menor)
    matches.sort(key=lambda x: x['similarity'], reverse=True)

    # Limitar resultados si se especificó top_n
    if top_n is not None and top_n > 0:
        matches = matches[:top_n]

    return {
        'matches_found': len(matches) > 0,
        'matches': matches,
        'query_embedding': new_embedding
    }