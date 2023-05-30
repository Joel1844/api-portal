from dataclasses import dataclass


def diacritic_sensitive(text: str) -> str:
    """Add diacritics to regex"""
    return text.lower().translate(str.maketrans(
        {
            'a': '[aá]',
            'e': '[eé]',
            'i': '[ií]',
            'o': '[oó]',
            'u': '[uúü]',
            # 'ñ': '[nñ]',
        }
    ))


@dataclass
class SearchQuery:
    def diacritic(self, text) -> str:
        return diacritic_sensitive(text)

    @property
    def search(self):
        return {}
