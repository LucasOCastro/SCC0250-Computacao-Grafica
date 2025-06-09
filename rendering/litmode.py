from enum import Enum

class LitMode(Enum):
    LIT = 0
    'Modo padrão, aplica todos os efeitos.'
    UNLIT = 1
    'Renderiza apenas a textura, sem aplicar iluminação.'
    LIT_BACKFACES = 2
    'Ilumina sem ignorar backfaces.'