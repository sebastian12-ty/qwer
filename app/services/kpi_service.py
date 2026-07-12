def calcular_kpis(encuesta: dict, emociones: dict, nlp_score: float) -> dict:
    """
    encuesta: {calidad_clase, comprension_tema, evaluacion_docente} 1-5
    emociones: {feliz, neutral, triste, enojado, sorprendido}
    nlp_score: 0-1 (sentimiento del comentario)
    """
    # Normalizar encuesta a 0-1
    cal = (encuesta.get('calidad_clase', 3) - 1) / 4
    com = (encuesta.get('comprension_tema', 3) - 1) / 4
    doc = (encuesta.get('evaluacion_docente', 3) - 1) / 4

    feliz = emociones.get('feliz', 0)
    neutral = emociones.get('neutral', 0)
    triste = emociones.get('triste', 0)
    enojado = emociones.get('enojado', 0)
    positivo_emocional = feliz + neutral * 0.5

    # KPI 1: Índice de Comprensión de Clase (0-1)
    indice_comprension = round(com * 0.6 + nlp_score * 0.25 + positivo_emocional * 0.15, 3)

    # KPI 2: Índice de Atención (0-1) — emociones positivas durante la sesión
    indice_atencion = round(feliz * 0.5 + neutral * 0.4 + (1 - enojado - triste) * 0.1, 3)
    indice_atencion = min(max(indice_atencion, 0), 1)

    # KPI 3: Índice de Coherencia Emocional (0-1) — alineación emoción vs respuesta encuesta
    coherencia_raw = 1 - abs((com + cal) / 2 - positivo_emocional)
    indice_coherencia = round(coherencia_raw, 3)

    # KPI 4: Índice de Nivelación Académica (0-1)
    indice_nivelacion = round(
        com * 0.35 + nlp_score * 0.25 + positivo_emocional * 0.25 + cal * 0.15, 3
    )

    # Satisfacción general
    satisfaccion_general = round((cal + com + doc) / 3, 3)

    # Riesgo
    if indice_nivelacion < 0.4 or satisfaccion_general < 0.4:
        riesgo = 'alto'
    elif indice_nivelacion < 0.6 or satisfaccion_general < 0.6:
        riesgo = 'medio'
    else:
        riesgo = 'bajo'

    return {
        'indice_comprension': indice_comprension,
        'indice_atencion': indice_atencion,
        'indice_coherencia_emocional': indice_coherencia,
        'indice_nivelacion': indice_nivelacion,
        'satisfaccion_general': satisfaccion_general,
        'riesgo_insatisfaccion': riesgo,
    }
