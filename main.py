from ar.auto_correct import get_correction_suggestions_ar
from ar.synonyms import get_synonyms_ar
from ar.inflections import get_inflections_ar
from en.auto_correct import get_correction_suggestions_en
from en.synonyms import get_synonyms_en
from en.inflections import get_inflections_en
from language_detector import detect_language

from ar.auto_correct import get_correction_suggestions_ar
from ar.synonyms import get_synonyms_ar
from ar.inflections import get_inflections_ar
from en.auto_correct import get_correction_suggestions_en
from en.synonyms import get_synonyms_en
from en.inflections import get_inflections_en
from language_detector import detect_language


def get_result(word):
    language = detect_language(word)
    result = {"exact": word}

    if language == "en":
        result["corrections"] = get_correction_suggestions_en(word)
        result["synonyms"] = get_synonyms_en(word)
        result["inflections"] = get_inflections_en(word)
        result["lang"] = 'en'

    else:
        result["corrections"] = get_correction_suggestions_ar(word)
        result["synonyms"] = get_synonyms_ar(word)
        result["inflections"] = get_inflections_ar(word)
        result["lang"] = 'ar'

    return str(result)




