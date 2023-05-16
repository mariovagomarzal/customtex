"""This module contains default values of the package."""
from pathlib import Path


# Main folders and files
COOKIECUTTER_TEMPLATE = Path(__file__).parent.parent / "template"
CUSTOMTEX_FOLDER = Path().home() / ".customtex"
CONFIG_FILE = "config.yaml"
TEMPLATES_FOLDER = "templates"

# Default languages
LANGUAGES = {
    "english": {
        "name": "english",
        "theorem": "Theorem",
        "proposition": "Proposition",
        "corollary": "Corollary",
        "lemma": "Lemma",
        "conjecture": "Conjecture",
        "definition": "Definition",
        "notation": "Notation",
        "example": "Example",
        "remark": "Remark",
        "problem": "Problem",
        "question": "Question",
        "exercise": "Exercise",
        "solution": "Solution"
    },
    "spanish": {
        "name": "spanish",
        "theorem": "Teorema",
        "proposition": "Proposición",
        "corollary": "Corolario",
        "lemma": "Lema",
        "conjecture": "Conjetura",
        "definition": "Definición",
        "notation": "Notación",
        "example": "Ejemplo",
        "remark": "Nota",
        "problem": "Problema",
        "question": "Custión",
        "exercise": "Ejercicio",
        "solution": "Solución"
    },
    "catalan": {
        "name": "catalan",
        "theorem": "Teorema",
        "proposition": "Proposició",
        "corollary": "Coro\\lgem{}ari",
        "lemma": "Lema",
        "conjecture": "Conjectura",
        "definition": "Definició",
        "notation": "Notació",
        "example": "Exemple",
        "remark": "Nota",
        "problem": "Problema",
        "question": "Qüestió",
        "exercise": "Exercici",
        "solution": "Solució"
    }
}

def get_langs() -> list[str]:
    """Return a list of available languages."""
    return list(LANGUAGES.keys())

def set_main_language(lang: str) -> list[dict[str, str]]:
    """Return a list of dictionaries with the main language first."""
    langs = get_langs()
    langs.remove(lang)
    langs.insert(0, lang)
    return [LANGUAGES[lang] for lang in langs]
    