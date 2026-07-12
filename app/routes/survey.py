from flask import Blueprint, render_template, request, jsonify
from app import db
from app.models.models import Survey, SurveyResponse, Student, EmotionCapture
from app.services.emotion_service import analyze_frame_base64, aggregate_emotions
from app.services.nlp_service import analyze_sentiment
from app.services.kpi_service import calcular_kpis
from datetime import datetime

survey_bp = Blueprint('survey', __name__)

@survey_bp.route('/<codigo>', methods=['GET'])
def show_survey(codigo):
    survey = Survey.query.filter_by(codigo_qr=codigo, activa=True).first_or_404()
    return render_template('survey/survey.html', survey=survey)

@survey_bp.route('/submit', methods=['POST'])
def submit_survey():
    data = request.get_json(force=True) or {}

    comentario = data.get('comentario', '')
    nlp_score, nlp_label, keywords = analyze_sentiment(comentario)

    captures = data.get('emotion_captures', [])
    emociones = aggregate_emotions(captures)

    encuesta = {
        'calidad_clase':      int(data.get('calidad_clase', 3)),
        'comprension_tema':   int(data.get('comprension_tema', 3)),
        'evaluacion_docente': int(data.get('evaluacion_docente', 3)),
    }
    kpis = calcular_kpis(encuesta, emociones, nlp_score)
    # Remove satisfaccion_general — not a model field
    kpis.pop('satisfaccion_general', None)

    resp = SurveyResponse(
        survey_id  = int(data.get('survey_id', 1)),
        student_id = int(data.get('student_id', 1)),
        fecha      = datetime.utcnow(),
        calidad_clase      = encuesta['calidad_clase'],
        comprension_tema   = encuesta['comprension_tema'],
        evaluacion_docente = encuesta['evaluacion_docente'],
        comentario         = comentario,
        sentimiento_score  = nlp_score,
        sentimiento_label  = nlp_label,
        nlp_keywords       = keywords,
        emocion_feliz        = emociones.get('feliz', 0),
        emocion_neutral      = emociones.get('neutral', 0),
        emocion_triste       = emociones.get('triste', 0),
        emocion_enojado      = emociones.get('enojado', 0),
        emocion_sorprendido  = emociones.get('sorprendido', 0),
        emocion_predominante = emociones.get('predominante', 'neutral'),
        indice_comprension          = kpis.get('indice_comprension'),
        indice_atencion             = kpis.get('indice_atencion'),
        indice_coherencia_emocional = kpis.get('indice_coherencia_emocional'),
        indice_nivelacion           = kpis.get('indice_nivelacion'),
        riesgo_insatisfaccion       = kpis.get('riesgo_insatisfaccion'),
    )
    db.session.add(resp)
    db.session.commit()

    for cap in captures:
        ec = EmotionCapture(
            response_id  = resp.id,
            feliz        = cap.get('feliz', 0),
            neutral      = cap.get('neutral', 0),
            triste       = cap.get('triste', 0),
            enojado      = cap.get('enojado', 0),
            sorprendido  = cap.get('sorprendido', 0),
        )
        db.session.add(ec)
    db.session.commit()

    return jsonify({'status': 'ok', 'response_id': resp.id, 'kpis': kpis})

@survey_bp.route('/capture_emotion', methods=['POST'])
def capture_emotion():
    data = request.get_json(force=True) or {}
    result = analyze_frame_base64(data.get('image', ''))
    return jsonify(result)
