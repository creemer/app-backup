# coding: utf-8

import sys
import traceback
import re


class Stacktrace:
    def __init__(self):
        pass

    @staticmethod
    def unbackslash_ru(ustring):
        if ustring is None:
            return None
        u = ustring

        # abc
        u = re.sub(r"\\xd0\\xb0", "а", u)
        u = re.sub(r"\\xd0\\xb1", "б", u)
        u = re.sub(r"\\xd0\\xb2", "в", u)
        u = re.sub(r"\\xd0\\xb3", "г", u)
        u = re.sub(r"\\xd0\\xb4", "д", u)
        u = re.sub(r"\\xd0\\xb5", "е", u)
        u = re.sub(r"\\xd1\\x91", "ё", u)
        u = re.sub(r"\\xd0\\xb6", "ж", u)
        u = re.sub(r"\\xd0\\xb7", "з", u)
        u = re.sub(r"\\xd0\\xb8", "и", u)
        u = re.sub(r"\\xd0\\xb9", "й", u)
        u = re.sub(r"\\xd0\\xba", "к", u)
        u = re.sub(r"\\xd0\\xbb", "л", u)
        u = re.sub(r"\\xd0\\xbc", "м", u)
        u = re.sub(r"\\xd0\\xbd", "н", u)
        u = re.sub(r"\\xd0\\xbe", "о", u)
        u = re.sub(r"\\xd0\\xbf", "п", u)
        u = re.sub(r"\\xd1\\x80", "р", u)
        u = re.sub(r"\\xd1\\x81", "с", u)
        u = re.sub(r"\\xd1\\x82", "т", u)
        u = re.sub(r"\\xd1\\x83", "у", u)
        u = re.sub(r"\\xd1\\x84", "ф", u)
        u = re.sub(r"\\xd1\\x85", "х", u)
        u = re.sub(r"\\xd1\\x86", "ц", u)
        u = re.sub(r"\\xd1\\x87", "ч", u)
        u = re.sub(r"\\xd1\\x88", "ш", u)
        u = re.sub(r"\\xd1\\x89", "щ", u)
        u = re.sub(r"\\xd1\\x8a", "ъ", u)
        u = re.sub(r"\\xd1\\x8b", "ы", u)
        u = re.sub(r"\\xd1\\x8c", "ь", u)
        u = re.sub(r"\\xd1\\x8d", "э", u)
        u = re.sub(r"\\xd1\\x8e", "ю", u)
        u = re.sub(r"\\xd1\\x8f", "я", u)

        # ABC
        u = re.sub(r"\\xd0\\x90", "А", u)
        u = re.sub(r"\\xd0\\x91", "Б", u)
        u = re.sub(r"\\xd0\\x92", "В", u)
        u = re.sub(r"\\xd0\\x93", "Г", u)
        u = re.sub(r"\\xd0\\x94", "Д", u)
        u = re.sub(r"\\xd0\\x95", "Е", u)
        u = re.sub(r"\\xd0\\x81", "Ё", u)
        u = re.sub(r"\\xd0\\x96", "Ж", u)
        u = re.sub(r"\\xd0\\x97", "З", u)
        u = re.sub(r"\\xd0\\x98", "И", u)
        u = re.sub(r"\\xd0\\x99", "Й", u)
        u = re.sub(r"\\xd0\\x9a", "К", u)
        u = re.sub(r"\\xd0\\x9b", "Л", u)
        u = re.sub(r"\\xd0\\x9c", "М", u)
        u = re.sub(r"\\xd0\\x9d", "Н", u)
        u = re.sub(r"\\xd0\\x9e", "О", u)
        u = re.sub(r"\\xd0\\x9f", "П", u)
        u = re.sub(r"\\xd0\\xa0", "Р", u)
        u = re.sub(r"\\xd0\\xa1", "С", u)
        u = re.sub(r"\\xd0\\xa2", "Т", u)
        u = re.sub(r"\\xd0\\xa3", "У", u)
        u = re.sub(r"\\xd0\\xa4", "Ф", u)
        u = re.sub(r"\\xd0\\xa5", "Х", u)
        u = re.sub(r"\\xd0\\xa6", "Ц", u)
        u = re.sub(r"\\xd0\\xa7", "Ч", u)
        u = re.sub(r"\\xd0\\xa8", "Ш", u)
        u = re.sub(r"\\xd0\\xa9", "Щ", u)
        u = re.sub(r"\\xd0\\xaa", "Ъ", u)
        u = re.sub(r"\\xd0\\xab", "Ы", u)
        u = re.sub(r"\\xd0\\xac", "Ь", u)
        u = re.sub(r"\\xd0\\xad", "Э", u)
        u = re.sub(r"\\xd0\\xae", "Ю", u)
        u = re.sub(r"\\xd0\\xaf", "Я", u)

        # special

        u = re.sub(r"\\xe2\\x84\\x96", "№", u)
        return u

    @staticmethod
    def unbackslash_ru2(ustring):
        if ustring is None:
            return None
        u = ustring

        # abc
        u = re.sub(r"\\xe0", "а", u)
        u = re.sub(r"\\xe1", "б", u)
        u = re.sub(r"\\xe2", "в", u)
        u = re.sub(r"\\xe3", "г", u)
        u = re.sub(r"\\xe4", "д", u)
        u = re.sub(r"\\xe5", "е", u)
        u = re.sub(r"\\xb8", "ё", u)
        u = re.sub(r"\\xe6", "ж", u)
        u = re.sub(r"\\xe7", "з", u)
        u = re.sub(r"\\xe8", "и", u)
        u = re.sub(r"\\xe9", "й", u)
        u = re.sub(r"\\xea", "к", u)
        u = re.sub(r"\\xeb", "л", u)
        u = re.sub(r"\\xec", "м", u)
        u = re.sub(r"\\xed", "н", u)
        u = re.sub(r"\\xee", "о", u)
        u = re.sub(r"\\xef", "п", u)
        u = re.sub(r"\\xf0", "р", u)
        u = re.sub(r"\\xf1", "с", u)
        u = re.sub(r"\\xf2", "т", u)
        u = re.sub(r"\\xf3", "у", u)
        u = re.sub(r"\\xf4", "ф", u)
        u = re.sub(r"\\xf5", "х", u)
        u = re.sub(r"\\xf6", "ц", u)
        u = re.sub(r"\\xf7", "ч", u)
        u = re.sub(r"\\xf8", "ш", u)
        u = re.sub(r"\\xf9", "щ", u)
        u = re.sub(r"\\xfa", "ъ", u)
        u = re.sub(r"\\xfb", "ы", u)
        u = re.sub(r"\\xfc", "ь", u)
        u = re.sub(r"\\xfd", "э", u)
        u = re.sub(r"\\xfe", "ю", u)
        u = re.sub(r"\\xff", "я", u)

        # ABC
        u = re.sub(r"\\xc0", "А", u)
        u = re.sub(r"\\xc1", "Б", u)
        u = re.sub(r"\\xc2", "В", u)
        u = re.sub(r"\\xc3", "Г", u)
        u = re.sub(r"\\xc4", "Д", u)
        u = re.sub(r"\\xc5", "Е", u)
        u = re.sub(r"\\xa8", "Ё", u)
        u = re.sub(r"\\xc6", "Ж", u)
        u = re.sub(r"\\xc7", "З", u)
        u = re.sub(r"\\xc8", "И", u)
        u = re.sub(r"\\xc9", "Й", u)
        u = re.sub(r"\\xca", "К", u)
        u = re.sub(r"\\xcb", "Л", u)
        u = re.sub(r"\\xcc", "М", u)
        u = re.sub(r"\\xcd", "Н", u)
        u = re.sub(r"\\xce", "О", u)
        u = re.sub(r"\\xcf", "П", u)
        u = re.sub(r"\\xd0", "Р", u)
        u = re.sub(r"\\xd1", "С", u)
        u = re.sub(r"\\xd2", "Т", u)
        u = re.sub(r"\\xd3", "У", u)
        u = re.sub(r"\\xd4", "Ф", u)
        u = re.sub(r"\\xd5", "Х", u)
        u = re.sub(r"\\xd6", "Ц", u)
        u = re.sub(r"\\xd7", "Ч", u)
        u = re.sub(r"\\xd8", "Ш", u)
        u = re.sub(r"\\xd9", "Щ", u)
        u = re.sub(r"\\xda", "Ъ", u)
        u = re.sub(r"\\xdb", "Ы", u)
        u = re.sub(r"\\xdc", "Ь", u)
        u = re.sub(r"\\xdd", "Э", u)
        u = re.sub(r"\\xde", "Ю", u)
        u = re.sub(r"\\xdf", "Я", u)

        # special

        u = re.sub(r"\\xb9", "№", u)
        return u

    @staticmethod
    def get():
        exc_type, exc_value, exc_traceback = sys.exc_info()
        if exc_type is None:
            return None
        u = repr(traceback.format_exception(exc_type, exc_value, exc_traceback))

        #exc_value = str(exc_value.decode('utf8'))
        u = "Type: %s\nMessage: %s\n%s" % (exc_type, exc_value, u)

        u = Stacktrace.unbackslash_ru(u)
        u = Stacktrace.unbackslash_ru2(u)

        # fix
        u = re.sub(r"(?m)^\['Traceback \(most recent call last\)", "Stacktrace", u)
        u = re.sub(r"\\n", "\n", u)
        u = re.sub(r"\\'", "'", u)

        u = re.sub(r"(?m)^',\s+'", " ", u)
        u = re.sub(r"(?m)\n^'\]$", "'\n\n", u)

        u = re.sub(r"(?m)^',\s\"", " \"", u)
        u = re.sub(r"(?m)\n^\"\]$", "\"\n\n", u)

        return u

    @staticmethod
    def getn():
        return '\n' + Stacktrace.get()
