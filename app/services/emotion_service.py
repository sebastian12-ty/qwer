import base64
import os
import random

try:
    import cv2
    import numpy as np
    CV2_AVAILABLE = True
except Exception:
    cv2 = None
    np = None
    CV2_AVAILABLE = False

_DeepFace = None
_deepface_checked = False

if CV2_AVAILABLE:
    CASCADE_DIR = cv2.data.haarcascades
    face_cascade = cv2.CascadeClassifier(os.path.join(CASCADE_DIR, 'haarcascade_frontalface_default.xml'))
    eye_cascade = cv2.CascadeClassifier(os.path.join(CASCADE_DIR, 'haarcascade_eye.xml'))
    smile_cascade = cv2.CascadeClassifier(os.path.join(CASCADE_DIR, 'haarcascade_smile.xml'))
else:
    face_cascade = eye_cascade = smile_cascade = None


def _get_deepface():
    global _DeepFace, _deepface_checked
    if _deepface_checked:
        return _DeepFace
    _deepface_checked = True
    try:
        from deepface import DeepFace
        _DeepFace = DeepFace
    except Exception:
        _DeepFace = None
    return _DeepFace


def analyze_frame_base64(b64_image: str) -> dict:
    """
    Analiza un frame base64 con OpenCV y, si esta disponible, DeepFace.
    Retorna emociones y metadata de tracking facial.
    """
    if not CV2_AVAILABLE:
        return _empty_result()

    try:
        img_data = base64.b64decode(b64_image.split(',')[-1])
        nparr = np.frombuffer(img_data, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if frame is None:
            return _empty_result()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))
        tracking = {
            'face_detected': len(faces) > 0,
            'face_count': int(len(faces)),
            'eyes_detected': False,
            'smile_detected': False,
            'face_position': None,
        }

        if len(faces) > 0:
            x, y, w, h = sorted(faces, key=lambda f: f[2] * f[3], reverse=True)[0]
            tracking['face_position'] = {
                'x': int(x), 'y': int(y),
                'w': int(w), 'h': int(h),
                'cx': int(x + w // 2), 'cy': int(y + h // 2),
            }
            roi_gray = gray[y:y + h, x:x + w]
            eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=5, minSize=(20, 20))
            smiles = smile_cascade.detectMultiScale(roi_gray, scaleFactor=1.7, minNeighbors=22, minSize=(25, 25))
            tracking['eyes_detected'] = len(eyes) >= 1
            tracking['smile_detected'] = len(smiles) > 0
            tracking['eye_count'] = int(len(eyes))

        deepface = _get_deepface()
        if deepface and tracking['face_detected']:
            emotions = _deepface_emotions(frame, deepface)
        else:
            emotions = _mock_emotions(tracking)

        return {**emotions, 'tracking': tracking}

    except Exception as e:
        print(f"[EmotionService] Error: {e}")
        return _empty_result()


def _deepface_emotions(frame, deepface) -> dict:
    try:
        result = deepface.analyze(
            frame,
            actions=['emotion'],
            enforce_detection=False,
            detector_backend='opencv',
            silent=True,
        )
        raw = result[0]['emotion'] if isinstance(result, list) else result['emotion']
        em = {
            'feliz': round(raw.get('happy', 0) / 100, 3),
            'neutral': round(raw.get('neutral', 0) / 100, 3),
            'triste': round((raw.get('sad', 0) + raw.get('fear', 0)) / 100, 3),
            'enojado': round((raw.get('angry', 0) + raw.get('disgust', 0)) / 100, 3),
            'sorprendido': round(raw.get('surprise', 0) / 100, 3),
        }
        em['predominante'] = max(em, key=em.get)
        return em
    except Exception:
        return _mock_emotions({})


def _mock_emotions(tracking: dict) -> dict:
    if not tracking.get('face_detected'):
        return {'feliz': 0, 'neutral': 0, 'triste': 0, 'enojado': 0, 'sorprendido': 0, 'predominante': 'neutral'}
    smile = tracking.get('smile_detected', False)
    eyes = tracking.get('eyes_detected', False)
    base_feliz = 0.6 if smile else 0.15
    base_neutral = 0.6 if (eyes and not smile) else 0.2
    vals = {
        'feliz': max(0, base_feliz + random.uniform(-0.1, 0.1)),
        'neutral': max(0, base_neutral + random.uniform(-0.1, 0.1)),
        'triste': max(0, 0.1 + random.uniform(-0.05, 0.05)),
        'enojado': max(0, 0.05 + random.uniform(-0.03, 0.03)),
        'sorprendido': max(0, 0.05 + random.uniform(-0.03, 0.03)),
    }
    total = sum(vals.values()) or 1
    em = {k: round(v / total, 3) for k, v in vals.items()}
    em['predominante'] = max(em, key=em.get)
    return em


def aggregate_emotions(captures: list) -> dict:
    if not captures:
        return {'feliz': 0, 'neutral': 1, 'triste': 0, 'enojado': 0, 'sorprendido': 0, 'predominante': 'neutral'}
    keys = ['feliz', 'neutral', 'triste', 'enojado', 'sorprendido']
    agg = {k: round(sum(c.get(k, 0) for c in captures) / len(captures), 3) for k in keys}
    agg['predominante'] = max(agg, key=agg.get)
    return agg


def _empty_result() -> dict:
    return {
        'feliz': 0, 'neutral': 1, 'triste': 0, 'enojado': 0, 'sorprendido': 0, 'predominante': 'neutral',
        'tracking': {'face_detected': False, 'face_count': 0, 'eyes_detected': False, 'smile_detected': False, 'face_position': None},
    }
