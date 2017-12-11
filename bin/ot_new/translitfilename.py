# coding: utf-8

import re


class TranslitFilename:
    def __init__(self):
        pass

    alfavit = {
        u'а': u'a',
        u'б': u'b',
        u'в': u'v',
        u'г': u'g',
        u'д': u'd',
        u'е': u'e',
        u'ё': u'yo',
        u'ж': u'zh',
        u'з': u'z',
        u'и': u'i',
        u'й': u'j',
        u'к': u'k',
        u'л': u'l',
        u'м': u'm',
        u'н': u'n',
        u'о': u'o',
        u'п': u'p',
        u'р': u'r',
        u'с': u's',
        u'т': u't',
        u'у': u'u',
        u'ф': u'f',
        u'х': u'x',
        u'ц': u'cz',
        u'ч': u'ch',
        u'ш': u'logger_root_fh',
        u'щ': u'shh',
        u'ъ': u'_',
        u'ы': u'y',
        u'ь': u'_',
        u'э': u'eh',
        u'ю': u'yu',
        u'я': u'ya',

        u'А': u'A',
        u'Б': u'B',
        u'В': u'V',
        u'Г': u'G',
        u'Д': u'D',
        u'Е': u'E',
        u'Ё': u'YO',
        u'Ж': u'ZH',
        u'З': u'Z',
        u'И': u'I',
        u'Й': u'J',
        u'К': u'K',
        u'Л': u'L',
        u'М': u'M',
        u'Н': u'N',
        u'О': u'O',
        u'П': u'P',
        u'Р': u'R',
        u'С': u'S',
        u'Т': u'T',
        u'У': u'u',
        u'Ф': u'F',
        u'Х': u'X',
        u'Ц': u'CZ',
        u'Ч': u'CH',
        u'Ш': u'SH',
        u'Щ': u'SHH',
        u'Ъ': u'_',
        u'Ы': u'Y',
        u'Ь': u'_',
        u'Э': u'EH',
        u'Ю': u'Yu',
        u'Я': u'YA',

        u'№': u'N',
    }

    @staticmethod
    def translit(ru_name):
        if ru_name is None:
            return None
        ret = ''
        for c in ru_name:
            cx = c.decode('utf-8')
            if cx in TranslitFilename.alfavit:
                ret += TranslitFilename.alfavit[cx]
            else:
                ret += cx
        ret = re.sub(r'(?i)[^a-z0-9_\-.]', '_', ret)
        return ret
