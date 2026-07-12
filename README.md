# EduSatisface — Plataforma de BI, Big Data e IA para Satisfacción Estudiantil

## Arquitectura de 7 Capas

```
[1] FUENTES]         Encuestas Web | Cámara | Redes Sociales | SGA
      ↓
[2] IoT/CAPTURA]     Webcam → OpenCV → DeepFace → Emociones
      ↓
[3] ETL]             Extracción → Transformación → Limpieza → Integración
      ↓
[4] DATA WAREHOUSE]  Modelo Estrella (Fact_Satisfaccion + Dims)
      ↓
[5] IA]              Facial + NLP + Árbol Decisión + Predicción Riesgo
      ↓
[6] SEMÁNTICA]       KPIs: Comprensión | Atención | Coherencia | Nivelación
      ↓
[7] VISUALIZACIÓN]   Looker Studio | Dashboard Web
```

## Stack Técnico
| Capa       | Tecnología                          |
|------------|-------------------------------------|
| Backend    | Python Flask + SQLAlchemy           |
| Frontend   | HTML/CSS/JS + Bootstrap 5           |
| Base Datos | PostgreSQL (modelo estrella)        |
| IA Facial  | OpenCV + DeepFace                   |
| NLP        | HuggingFace Transformers + NLTK     |
| ML         | scikit-learn (Árbol de Decisión)    |
| Cloud      | Google Cloud Platform               |
| Dashboard  | Looker Studio (via API)             |

## Modelo Dimensional (Estrella)

```
           DIM_TIEMPO
               |
DIM_ESTUDIANTE — FACT_SATISFACCION — DIM_DOCENTE
               |
           DIM_CURSO
```

### FACT_SATISFACCION
- calidad_clase (1-5)
- comprension_tema (1-5)
- evaluacion_docente (1-5)
- comentario (texto)
- sentimiento_score (0-1)
- emocion_* (feliz, neutral, triste, enojado, sorprendido)
- **indice_comprension** — KPI nuevo
- **indice_atencion** — KPI nuevo
- **indice_coherencia_emocional** — KPI nuevo
- **indice_nivelacion** — KPI nuevo
- riesgo_insatisfaccion (bajo/medio/alto)

## KPIs

| KPI | Fórmula |
|-----|---------|
| Índice Comprensión | comprension×0.6 + nlp×0.25 + emoción_positiva×0.15 |
| Índice Atención | feliz×0.5 + neutral×0.4 + (1-neg)×0.1 |
| Coherencia Emocional | 1 - |encuesta_norm - emoción_positiva| |
| Nivelación Académica | comprension×0.35 + nlp×0.25 + emoción×0.25 + calidad×0.15 |

## Setup Local

```bash
# 1. Clonar y entorno
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 2. Base de datos PostgreSQL
createdb edusatisface

# 3. Variables de entorno
cp .env.example .env
# Edita DATABASE_URL en .env

# 4. Inicializar BD y seed
python migrations/seed.py

# 5. Ejecutar
python run.py
```

## Usuarios de prueba
| Email | Contraseña | Rol |
|-------|-----------|-----|
| admin@uni.edu | admin123 | Administrador |
| docente@uni.edu | docente123 | Docente |
| estudiante@uni.edu | student123 | Estudiante |

## Encuesta demo
Ir a: http://localhost:5000/survey/DEMO01

## APIs REST

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | /auth/login | Autenticación |
| GET | /survey/<codigo> | Ver encuesta por QR |
| POST | /survey/submit | Enviar respuesta |
| POST | /survey/capture_emotion | Analizar frame (base64) |
| GET | /api/v1/kpis/general | KPIs globales |
| GET | /api/v1/kpis/emociones | Distribución emocional |
| GET | /api/v1/kpis/riesgo | Conteo por nivel de riesgo |
| POST | /api/v1/survey/create | Crear encuesta |

## ETL
```bash
python etl/pipeline.py
```

## Estructura de carpetas
```
edusatisface/
├── app/
│   ├── __init__.py         # Factory Flask
│   ├── models/models.py    # SQLAlchemy models (estrella)
│   ├── routes/             # auth, survey, teacher, student, coordinator, admin, api
│   └── services/
│       ├── emotion_service.py  # OpenCV + DeepFace
│       ├── nlp_service.py      # Transformers + NLTK
│       └── kpi_service.py      # Cálculo KPIs
├── config/settings.py
├── etl/pipeline.py
├── migrations/seed.py
├── static/
│   ├── css/main.css
│   └── js/  survey.js | dashboard.js | main.js
├── templates/
│   ├── base.html
│   ├── auth/ | survey/ | teacher/ | student/ | coordinator/ | admin/
├── run.py
├── requirements.txt
└── .env.example
```
