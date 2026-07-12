import os
import re
from typing import Tuple

_sentiment_pipeline = None
_transformers_checked = False

try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    NLTK_AVAILABLE = True
except Exception:
    NLTK_AVAILABLE = False

POSITIVE_WORDS = {'excelente','bueno','genial','claro','entendi','entendí','aprendi','aprendí','motivador','interesante','util','útil'}
NEGATIVE_WORDS = {'malo','aburrido','confuso','dificil','difícil','no entendi','no entendí','perdido','lento','monotono','monótono','pesimo','pésimo'}


def _get_sentiment_pipeline():
    global _sentiment_pipeline, _transformers_checked
    if _transformers_checked:
        return _sentiment_pipeline
    _transformers_checked = True

    if os.getenv('EDUSATISFACE_ENABLE_TRANSFORMERS', '').lower() not in {'1', 'true', 'yes'}:
        _sentiment_pipeline = None
        return _sentiment_pipeline

    try:
        from transformers import pipeline
        _sentiment_pipeline = pipeline(
            'sentiment-analysis',
            model='nlptown/bert-base-multilingual-uncased-sentiment',
            local_files_only=True,
        )
    except Exception:
        _sentiment_pipeline = None
    return _sentiment_pipeline


def analyze_sentiment(text: str) -> Tuple[float, str, list]:
    """
    Returns: (score 0-1, label, keywords)
    """
    if not text or len(text.strip()) < 3:
        return 0.5, 'neutral', []

    text_lower = text.lower()

    sentiment_pipeline = _get_sentiment_pipeline()
    if sentiment_pipeline:
        try:
            result = sentiment_pipeline(text[:512])[0]
            stars = int(result['label'][0])
            score = (stars - 1) / 4.0
            label = 'positivo' if score >= 0.6 else 'negativo' if score <= 0.4 else 'neutral'
            keywords = _extract_keywords(text)
            return round(score, 3), label, keywords
        except Exception:
            pass

    return _rule_based_sentiment(text_lower)


def _rule_based_sentiment(text: str) -> Tuple[float, str, list]:
    pos = sum(1 for w in POSITIVE_WORDS if w in text)
    neg = sum(1 for w in NEGATIVE_WORDS if w in text)
    total = pos + neg or 1
    score = pos / total
    label = 'positivo' if score >= 0.6 else 'negativo' if score <= 0.4 else 'neutral'
    keywords = [w for w in POSITIVE_WORDS | NEGATIVE_WORDS if w in text]
    return round(score, 3), label, keywords


def _extract_keywords(text: str) -> list:
    if not NLTK_AVAILABLE:
        return re.findall(r'\b\w{4,}\b', text.lower())[:10]
    try:
        tokens = word_tokenize(text.lower(), language='spanish')
        stop = set(stopwords.words('spanish'))
        return [t for t in tokens if t.isalpha() and t not in stop][:10]
    except LookupError:
        return re.findall(r'\b\w{4,}\b', text.lower())[:10]
