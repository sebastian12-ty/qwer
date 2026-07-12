"""
Generador de 5,000+ registros sintéticos realistas para EduSatisface.
Genera 7 CSVs — uno por cada capa del modelo E2E-BI.
Ejecutar: python data_exports/generate_data.py
"""
import csv, random, os
from datetime import datetime, timedelta

random.seed(42)
OUT = os.path.dirname(os.path.abspath(__file__))

# ── Catálogos ──────────────────────────────────────────────────────────────
CARRERAS   = ['Ingeniería de Sistemas','Ingeniería Civil','Administración','Contabilidad','Derecho','Medicina','Psicología','Arquitectura']
CURSOS_MAP = {
    'Ingeniería de Sistemas': ['Algoritmos','Bases de Datos','Redes','POO','IA y Machine Learning','Sistemas Operativos','Web Development','Big Data'],
    'Ingeniería Civil':       ['Estática','Hidráulica','Resistencia de Materiales','Topografía','Diseño Estructural'],
    'Administración':         ['Marketing','Finanzas','RRHH','Gestión de Proyectos','Emprendimiento'],
    'Contabilidad':           ['Contabilidad General','Tributación','Auditoría','Costos','Finanzas Corporativas'],
    'Derecho':                ['Derecho Civil','Derecho Penal','Procesal Civil','Constitucional','Laboral'],
    'Medicina':               ['Anatomía','Fisiología','Bioquímica','Farmacología','Patología'],
    'Psicología':             ['Psicología General','Clínica','Educativa','Social','Neuropsicología'],
    'Arquitectura':           ['Diseño Arquitectónico','Urbanismo','Estructuras','Historia del Arte','BIM'],
}
DOCENTES = [
    {'id':1,'nombre':'Dr. Carlos García',    'especialidad':'Algoritmos y IA'},
    {'id':2,'nombre':'Mg. Ana Rodríguez',    'especialidad':'Bases de Datos'},
    {'id':3,'nombre':'Dr. Luis Mendoza',     'especialidad':'Redes y Sistemas'},
    {'id':4,'nombre':'Mg. María Torres',     'especialidad':'Gestión Empresarial'},
    {'id':5,'nombre':'Dr. Jorge Quispe',     'especialidad':'Ingeniería Civil'},
    {'id':6,'nombre':'Mg. Rosa Huamán',      'especialidad':'Derecho'},
    {'id':7,'nombre':'Dr. Pedro Vargas',     'especialidad':'Medicina'},
    {'id':8,'nombre':'Mg. Elena Castillo',   'especialidad':'Psicología'},
    {'id':9,'nombre':'Dr. Roberto Silva',    'especialidad':'Arquitectura'},
    {'id':10,'nombre':'Mg. Carmen Flores',   'especialidad':'Contabilidad'},
]
SEMESTRES  = [1,2,3,4,5,6,7,8,9,10]
EMOCIONES  = ['feliz','neutral','triste','enojado','sorprendido']
SENTIMIENTOS = ['positivo','neutral','negativo']
COMENTARIOS_POS = [
    'Excelente clase, muy clara la explicación','El docente domina el tema perfectamente',
    'Aprendí mucho hoy, muy buena didáctica','La clase fue muy dinámica e interesante',
    'Me quedó muy claro el tema, gracias','Muy buena metodología del docente',
    'Clase muy bien estructurada y organizada','Excelente manejo del tiempo y ejemplos',
]
COMENTARIOS_NEU = [
    'La clase estuvo bien, aunque faltaron más ejemplos','Regular, podría mejorar el ritmo',
    'Entendí el tema pero fue un poco rápido','Más o menos, algunos conceptos poco claros',
    'El tema es interesante pero la clase fue larga','Bien en general, aunque faltó práctica',
]
COMENTARIOS_NEG = [
    'No entendí casi nada, muy confuso','El docente explicó muy rápido',
    'Faltaron ejemplos prácticos, solo teoría','La clase fue aburrida y poco dinámica',
    'No se escuchaba bien, problemas técnicos','Muy difícil seguir el ritmo de la clase',
]

def weighted_rand(weights):
    """Retorna índice según pesos."""
    r = random.random() * sum(weights)
    for i,w in enumerate(weights):
        r -= w
        if r <= 0: return i
    return len(weights)-1

def gen_emociones():
    emo = {e: round(random.uniform(0,1),3) for e in EMOCIONES}
    total = sum(emo.values()) or 1
    emo = {k: round(v/total,3) for k,v in emo.items()}
    predom = max(emo, key=emo.get)
    return emo, predom

def gen_kpis(calidad, comprension, docente, nlp_score, emociones):
    pos_emo = emociones['feliz'] + emociones['neutral']*0.5
    cal_n   = (calidad-1)/4
    com_n   = (comprension-1)/4
    doc_n   = (docente-1)/4
    idx_comprension = round(com_n*0.6 + nlp_score*0.25 + pos_emo*0.15, 3)
    idx_atencion    = round(min(1, max(0, emociones['feliz']*0.5 + emociones['neutral']*0.4 + (1-emociones['enojado']-emociones['triste'])*0.1)), 3)
    idx_coherencia  = round(1 - abs((com_n+cal_n)/2 - pos_emo), 3)
    idx_nivelacion  = round(com_n*0.35 + nlp_score*0.25 + pos_emo*0.25 + cal_n*0.15, 3)
    satisfaccion    = round((cal_n+com_n+doc_n)/3, 3)
    riesgo = 'alto' if idx_nivelacion<0.4 or satisfaccion<0.4 else 'medio' if idx_nivelacion<0.6 or satisfaccion<0.6 else 'bajo'
    return idx_comprension, idx_atencion, idx_coherencia, idx_nivelacion, satisfaccion, riesgo

# ══════════════════════════════════════════════════════════════════════════
# PASO 1 — FUENTES DE DATOS
# ══════════════════════════════════════════════════════════════════════════
print("Generando PASO 1: Fuentes de Datos...")
N_ESTUDIANTES = 500
N_RESPONSES   = 5200

estudiantes, docentes_list, encuestas = [], [], []
start_date = datetime(2024, 3, 1)

for i in range(1, N_ESTUDIANTES+1):
    carrera = random.choice(CARRERAS)
    estudiantes.append({
        'id': i, 'codigo': f'STU{i:04d}',
        'nombre': f'Estudiante {i}',
        'carrera': carrera,
        'semestre': random.choice(SEMESTRES),
        'email': f'estudiante{i}@uni.edu',
        'fecha_ingreso': (start_date - timedelta(days=random.randint(0,1095))).strftime('%Y-%m-%d'),
    })

with open(f'{OUT}/paso1_fuentes_estudiantes.csv','w',newline='',encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=estudiantes[0].keys()); w.writeheader(); w.writerows(estudiantes)

for d in DOCENTES:
    docentes_list.append({**d, 'email':f'docente{d["id"]}@uni.edu','departamento':'Ingeniería','activo':True})

with open(f'{OUT}/paso1_fuentes_docentes.csv','w',newline='',encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=docentes_list[0].keys()); w.writeheader(); w.writerows(docentes_list)

enc_id = 1
for doc in DOCENTES:
    carrera = random.choice(CARRERAS)
    cursos = CURSOS_MAP.get(carrera, ['Curso General'])
    for curso in random.sample(cursos, min(3, len(cursos))):
        encuestas.append({
            'id': enc_id, 'titulo': f'{curso} — Clase {random.randint(1,15)}',
            'codigo_qr': f'QR{enc_id:04d}', 'teacher_id': doc['id'],
            'curso': curso, 'carrera': carrera,
            'fecha_creacion': (start_date + timedelta(days=random.randint(0,300))).strftime('%Y-%m-%d'),
            'activa': random.choice([True,True,False]),
        })
        enc_id += 1

with open(f'{OUT}/paso1_fuentes_encuestas.csv','w',newline='',encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=encuestas[0].keys()); w.writeheader(); w.writerows(encuestas)

print(f"  ✅ {N_ESTUDIANTES} estudiantes, {len(DOCENTES)} docentes, {len(encuestas)} encuestas")

# ══════════════════════════════════════════════════════════════════════════
# PASO 2 — CAPTURA IoT (cámara/emociones raw)
# ══════════════════════════════════════════════════════════════════════════
print("Generando PASO 2: Capturas IoT (emociones)...")
iot_rows = []
for resp_id in range(1, N_RESPONSES+1):
    n_caps = random.randint(2, 8)
    for c in range(n_caps):
        emo, predom = gen_emociones()
        iot_rows.append({
            'captura_id': len(iot_rows)+1,
            'response_id': resp_id,
            'timestamp': (start_date + timedelta(days=random.randint(0,300), seconds=random.randint(0,3600))).strftime('%Y-%m-%d %H:%M:%S'),
            'frame_seq': c+1,
            **{f'emo_{k}': v for k,v in emo.items()},
            'emocion_predominante': predom,
            'face_detected': random.choice([True,True,True,False]),
            'eyes_detected': random.choice([True,True,False]),
            'smile_detected': random.choice([True,False,False]),
        })

with open(f'{OUT}/paso2_iot_capturas.csv','w',newline='',encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=iot_rows[0].keys()); w.writeheader(); w.writerows(iot_rows)
print(f"  ✅ {len(iot_rows)} capturas IoT generadas")

# ══════════════════════════════════════════════════════════════════════════
# PASO 3 — ETL (datos limpios y transformados)
# ══════════════════════════════════════════════════════════════════════════
print("Generando PASO 3: ETL — respuestas limpias...")
etl_rows = []
for i in range(1, N_RESPONSES+1):
    est  = random.choice(estudiantes)
    enc  = random.choice(encuestas)
    doc  = next(d for d in DOCENTES if d['id']==enc['teacher_id'])
    fecha= start_date + timedelta(days=random.randint(0,300), hours=random.randint(7,18))

    cal  = random.choices([1,2,3,4,5], weights=[3,7,20,40,30])[0]
    comp = random.choices([1,2,3,4,5], weights=[4,8,22,38,28])[0]
    doce = random.choices([1,2,3,4,5], weights=[2,6,18,42,32])[0]
    sent_idx = weighted_rand([55,25,20])
    sent_lbl = SENTIMIENTOS[sent_idx]
    nlp_score= round(random.uniform(0.65,0.95) if sent_lbl=='positivo' else
                     random.uniform(0.35,0.55) if sent_lbl=='neutral'  else
                     random.uniform(0.05,0.35), 3)
    coment_pool = COMENTARIOS_POS if sent_lbl=='positivo' else COMENTARIOS_NEU if sent_lbl=='neutral' else COMENTARIOS_NEG
    emo, predom = gen_emociones()
    ic,ia,ico,ini,sat,riesgo = gen_kpis(cal,comp,doce,nlp_score,emo)

    etl_rows.append({
        'response_id': i, 'survey_id': enc['id'], 'student_id': est['id'],
        'fecha': fecha.strftime('%Y-%m-%d %H:%M:%S'),
        'anio': fecha.year, 'mes': fecha.month, 'semana': fecha.isocalendar()[1],
        'dia_semana': fecha.weekday(), 'hora': fecha.hour,
        'calidad_clase': cal, 'comprension_tema': comp, 'evaluacion_docente': doce,
        'comentario': random.choice(coment_pool),
        'sentimiento_label': sent_lbl, 'sentimiento_score': nlp_score,
        **{f'emo_{k}': v for k,v in emo.items()},
        'emocion_predominante': predom,
        # Campos limpiados/transformados
        'calidad_normalizada': round((cal-1)/4, 3),
        'comprension_normalizada': round((comp-1)/4, 3),
        'docente_normalizado': round((doce-1)/4, 3),
        'datos_completos': True,
        'outlier_flag': False,
    })

with open(f'{OUT}/paso3_etl_respuestas.csv','w',newline='',encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=etl_rows[0].keys()); w.writeheader(); w.writerows(etl_rows)
print(f"  ✅ {len(etl_rows)} respuestas ETL")

# ══════════════════════════════════════════════════════════════════════════
# PASO 4 — DATA WAREHOUSE (modelo estrella)
# ══════════════════════════════════════════════════════════════════════════
print("Generando PASO 4: Data Warehouse (modelo estrella)...")

# Dimensión tiempo
dim_tiempo = []
for row in etl_rows:
    fecha = datetime.strptime(row['fecha'], '%Y-%m-%d %H:%M:%S')
    dt = {
        'time_id': row['response_id'],
        'fecha_completa': row['fecha'],
        'anio': fecha.year, 'mes': fecha.month,
        'mes_nombre': fecha.strftime('%B'), 'trimestre': (fecha.month-1)//3+1,
        'semana': row['semana'], 'dia': fecha.day,
        'dia_semana': row['dia_semana'],
        'dia_nombre': fecha.strftime('%A'), 'hora': fecha.hour,
        'turno': 'Mañana' if fecha.hour<13 else 'Tarde' if fecha.hour<18 else 'Noche',
    }
    dim_tiempo.append(dt)

with open(f'{OUT}/paso4_dim_tiempo.csv','w',newline='',encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=dim_tiempo[0].keys()); w.writeheader(); w.writerows(dim_tiempo)

# Fact table
fact_rows = []
for row in etl_rows:
    est = next(e for e in estudiantes if e['id']==row['student_id'])
    enc = next(e for e in encuestas   if e['id']==row['survey_id'])
    doc = next(d for d in DOCENTES    if d['id']==enc['teacher_id'])
    emo = {k.replace('emo_',''): row[k] for k in row if k.startswith('emo_')}
    ic,ia,ico,ini,sat,riesgo = gen_kpis(
        row['calidad_clase'], row['comprension_tema'], row['evaluacion_docente'],
        row['sentimiento_score'], emo
    )
    fact_rows.append({
        'fact_id':          row['response_id'],
        'survey_id':        row['survey_id'],
        'student_id':       row['student_id'],
        'teacher_id':       enc['teacher_id'],
        'time_id':          row['response_id'],
        'fecha':            row['fecha'],
        # Dimensiones desnormalizadas para Looker
        'estudiante_nombre': est['nombre'],
        'carrera':           est['carrera'],
        'semestre':          est['semestre'],
        'curso':             enc['curso'],
        'docente_nombre':    doc['nombre'],
        'especialidad':      doc['especialidad'],
        'anio':              row['anio'], 'mes': row['mes'],
        'trimestre':         (int(row['mes'])-1)//3+1,
        'turno':             'Mañana' if int(row['hora'])<13 else 'Tarde',
        # Métricas encuesta
        'calidad_clase':        row['calidad_clase'],
        'comprension_tema':     row['comprension_tema'],
        'evaluacion_docente':   row['evaluacion_docente'],
        'comentario':           row['comentario'],
        # Métricas sentimiento
        'sentimiento_label':    row['sentimiento_label'],
        'sentimiento_score':    row['sentimiento_score'],
        # Emociones
        'emocion_feliz':        row['emo_feliz'],
        'emocion_neutral':      row['emo_neutral'],
        'emocion_triste':       row['emo_triste'],
        'emocion_enojado':      row['emo_enojado'],
        'emocion_sorprendido':  row['emo_sorprendido'],
        'emocion_predominante': row['emocion_predominante'],
        # KPIs calculados
        'indice_comprension':          ic,
        'indice_atencion':             ia,
        'indice_coherencia_emocional': ico,
        'indice_nivelacion':           ini,
        'satisfaccion_general':        sat,
        'riesgo_insatisfaccion':       riesgo,
    })

with open(f'{OUT}/paso4_fact_satisfaccion.csv','w',newline='',encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=fact_rows[0].keys()); w.writeheader(); w.writerows(fact_rows)
print(f"  ✅ {len(fact_rows)} filas en Fact_Satisfaccion")

# ══════════════════════════════════════════════════════════════════════════
# PASO 5 — IA (resultados de modelos)
# ══════════════════════════════════════════════════════════════════════════
print("Generando PASO 5: IA — resultados de modelos...")
ia_rows = []
for row in fact_rows:
    # Árbol de decisión simulado
    nivel = row['indice_nivelacion']
    risk  = row['riesgo_insatisfaccion']
    ia_rows.append({
        'ia_id':            row['fact_id'],
        'student_id':       row['student_id'],
        'fecha':            row['fecha'],
        'modelo_emocion':   'DeepFace+OpenCV',
        'modelo_nlp':       'BERT-multilingual',
        'modelo_riesgo':    'DecisionTree',
        'prediccion_riesgo':risk,
        'confianza_riesgo': round(random.uniform(0.72, 0.97), 3),
        'indice_nivelacion':nivel,
        'nivel_categorico': 'Alto' if nivel>=0.7 else 'Medio' if nivel>=0.5 else 'Bajo',
        'accion_recomendada': (
            'Continuar metodología actual' if risk=='bajo' else
            'Reforzar con ejemplos prácticos' if risk=='medio' else
            'Tutoría urgente recomendada'
        ),
        'emocion_predominante': row['emocion_predominante'],
        'sentimiento_nlp':      row['sentimiento_label'],
        'coherencia_emocional': row['indice_coherencia_emocional'],
    })

with open(f'{OUT}/paso5_ia_resultados.csv','w',newline='',encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=ia_rows[0].keys()); w.writeheader(); w.writerows(ia_rows)
print(f"  ✅ {len(ia_rows)} predicciones IA")

# ══════════════════════════════════════════════════════════════════════════
# PASO 6 — SEMÁNTICA / KPIs agregados
# ══════════════════════════════════════════════════════════════════════════
print("Generando PASO 6: KPIs semánticos agregados...")
from collections import defaultdict
kpi_carrera = defaultdict(list)
for row in fact_rows:
    kpi_carrera[row['carrera']].append(row)

kpi_rows = []
for carrera, rows in kpi_carrera.items():
    kpi_rows.append({
        'carrera': carrera,
        'total_respuestas': len(rows),
        'kpi_satisfaccion_general':    round(sum(r['satisfaccion_general']    for r in rows)/len(rows),3),
        'kpi_comprension':             round(sum(r['indice_comprension']      for r in rows)/len(rows),3),
        'kpi_atencion':                round(sum(r['indice_atencion']         for r in rows)/len(rows),3),
        'kpi_nivelacion':              round(sum(r['indice_nivelacion']       for r in rows)/len(rows),3),
        'kpi_coherencia':              round(sum(r['indice_coherencia_emocional'] for r in rows)/len(rows),3),
        'pct_riesgo_alto':             round(sum(1 for r in rows if r['riesgo_insatisfaccion']=='alto')/len(rows)*100,1),
        'pct_riesgo_medio':            round(sum(1 for r in rows if r['riesgo_insatisfaccion']=='medio')/len(rows)*100,1),
        'pct_riesgo_bajo':             round(sum(1 for r in rows if r['riesgo_insatisfaccion']=='bajo')/len(rows)*100,1),
        'pct_sentimiento_positivo':    round(sum(1 for r in rows if r['sentimiento_label']=='positivo')/len(rows)*100,1),
        'pct_sentimiento_negativo':    round(sum(1 for r in rows if r['sentimiento_label']=='negativo')/len(rows)*100,1),
        'emocion_predominante_global': max(EMOCIONES, key=lambda e: sum(r[f'emocion_{e}'] for r in rows)),
        'brecha_satisfaccion':         round(max(r['satisfaccion_general'] for r in rows)-min(r['satisfaccion_general'] for r in rows),3),
    })

with open(f'{OUT}/paso6_kpis_semanticos.csv','w',newline='',encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=kpi_rows[0].keys()); w.writeheader(); w.writerows(kpi_rows)
print(f"  ✅ {len(kpi_rows)} KPIs por carrera")

# ══════════════════════════════════════════════════════════════════════════
# PASO 7 — VISUALIZACIÓN (resumen para Looker Studio)
# ══════════════════════════════════════════════════════════════════════════
print("Generando PASO 7: Dataset maestro para Looker Studio...")
# Este es el CSV principal que se sube a Looker — contiene todo
with open(f'{OUT}/paso7_looker_dataset_maestro.csv','w',newline='',encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=fact_rows[0].keys())
    w.writeheader(); w.writerows(fact_rows)

# Resumen ejecutivo
resumen = {
    'total_respuestas':      len(fact_rows),
    'total_estudiantes':     N_ESTUDIANTES,
    'total_docentes':        len(DOCENTES),
    'total_encuestas':       len(encuestas),
    'total_capturas_iot':    len(iot_rows),
    'kpi_satisfaccion_prom': round(sum(r['satisfaccion_general'] for r in fact_rows)/len(fact_rows),3),
    'kpi_nivelacion_prom':   round(sum(r['indice_nivelacion']    for r in fact_rows)/len(fact_rows),3),
    'kpi_comprension_prom':  round(sum(r['indice_comprension']   for r in fact_rows)/len(fact_rows),3),
    'kpi_atencion_prom':     round(sum(r['indice_atencion']      for r in fact_rows)/len(fact_rows),3),
    'pct_riesgo_alto':       round(sum(1 for r in fact_rows if r['riesgo_insatisfaccion']=='alto')/len(fact_rows)*100,1),
    'pct_riesgo_bajo':       round(sum(1 for r in fact_rows if r['riesgo_insatisfaccion']=='bajo')/len(fact_rows)*100,1),
    'pct_sentimiento_pos':   round(sum(1 for r in fact_rows if r['sentimiento_label']=='positivo')/len(fact_rows)*100,1),
}
with open(f'{OUT}/resumen_ejecutivo.csv','w',newline='',encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=resumen.keys()); w.writeheader(); w.writerow(resumen)

print(f"\n{'='*55}")
print(f"  GENERACIÓN COMPLETA — 7 PASOS E2E-BI")
print(f"{'='*55}")
print(f"  Paso 1 — Fuentes:       estudiantes + docentes + encuestas")
print(f"  Paso 2 — IoT:           {len(iot_rows):,} capturas emocionales")
print(f"  Paso 3 — ETL:           {len(etl_rows):,} respuestas limpias")
print(f"  Paso 4 — Data Warehouse: {len(fact_rows):,} filas Fact_Satisfaccion")
print(f"  Paso 5 — IA:            {len(ia_rows):,} predicciones")
print(f"  Paso 6 — Semántica:     {len(kpi_rows)} KPIs por carrera")
print(f"  Paso 7 — Looker Studio: dataset_maestro.csv listo para subir")
print(f"{'='*55}")
print(f"  📊 TOTAL REGISTROS: {len(fact_rows)+len(iot_rows)+len(etl_rows):,}+")
