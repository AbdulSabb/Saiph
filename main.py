from ar.auto_correct import get_correction_suggestions_ar
from ar.synonyms import get_synonyms_ar
from ar.inflections import get_inflections_ar
from en.auto_correct import get_correction_suggestions_en
from en.synonyms import get_synonyms_en
from en.inflections import get_inflections_en
from language_detector import detect_language


def get_result(word):
    language = detect_language(word)
    result = word + "\n"

    if language == "en":
        result += get_correction_suggestions_en(word) + "\n"
        result += get_synonyms_en(word) + "\n"
        result += get_inflections_en(word) + "\n"

    else:
        result += get_correction_suggestions_ar(word) + "\n"
        result += get_synonyms_ar(word) + "\n"
        result += get_inflections_ar(word) + "\n"

    return result



