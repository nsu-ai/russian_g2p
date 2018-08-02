import re
import unittest

from russian_g2p.Grapheme2Phoneme import Grapheme2Phoneme


class TestRussianG2P(unittest.TestCase):
    def setUp(self):
        self.__g2p = Grapheme2Phoneme()

    def tearDown(self):
        del self.__g2p

    """
    Rule TLP 0. If the whole word is in exclusion dictionary, it is converted in a form that will be transformed 
    correctly by following rules. The exclusion dictionary has the following format:
        автоби+знесу автоби+знэсу
        оттого+ оттово+
        здра+вствуй здра+ствуй
    """

    def test_phrase_to_phonemes_positive_tlp0_001(self):
        """ Проверка словаря фонетических исключений. """
        self.assertEqual(['A', 'F', 'T', 'A', 'B0', 'I0', 'Z', 'N', 'Y', 'S'],
                         self.__g2p.word_to_phonemes('автоби+знес'))
        self.assertEqual(['D', 'Y', 'K', 'A', 'L0', 'T', 'E0'], self.__g2p.word_to_phonemes('декольте+'))
        self.assertEqual(['M', 'A', 'D', 'E0', 'L0', 'N', 'A', 'S', 'T', 'A', 'L0', 'A0', 'R', 'N', 'Y', 'J0'],
                         self.__g2p.word_to_phonemes('моде+льно-столя+рный'))
        self.assertEqual(['I', 'N', 'T', 'Y', 'R', 'D0', 'E0', 'V', 'A', 'TSH0', 'K', 'A'],
                         self.__g2p.word_to_phonemes('интерде+вочка'))

    """
    Rule TLP 1. In combinations of letters «СТН», «СТЛ» and «НТГ» letter Т is removed.
    """

    def test_phrase_to_phonemes_positive_tlp1_001(self):
        """ Проверка правила ПБФ21. """
        self.assertEqual(['TSH0', 'A0', 'S', 'N', 'Y', 'J0'], self.__g2p.word_to_phonemes('ча+стный'))
        self.assertEqual(['SH0', 'I', 'S', 'L0', 'I0', 'V', 'Y', 'J0'], self.__g2p.word_to_phonemes('счастли+вый'))
        self.assertEqual(['R0', 'I', 'N', 'G0', 'E0', 'N'], self.__g2p.word_to_phonemes('рентге+н'))

    """
    Rule TLP 2. In combinations of letters «ЗДН», «ЗДЦ», «НДЦ», «РДЦ», «НДШ» and «ГДТ» letter Д is removed.
    """

    def test_phrase_to_phonemes_positive_tlp2_001(self):
        """ Проверка правила ПБФ22. """
        self.assertEqual(['P', 'O0', 'Z', 'N', 'A'], self.__g2p.word_to_phonemes('по+здно'))
        self.assertEqual(['U', 'S', 'TS', 'Y0'], self.__g2p.word_to_phonemes('уздцы+'))
        # self.assertEqual(['G', 'A', 'Ll', 'A0', 'N', 'TS', 'Y'], self.__g2p.word_to_phonemes('голла+ндцы'))
        self.assertEqual(['G', 'A', 'L', 'A0', 'N', 'TS', 'Y'], self.__g2p.word_to_phonemes('голла+ндцы'))
        self.assertEqual(['S0', 'E0', 'R', 'TS', 'Y'], self.__g2p.word_to_phonemes('се+рдце'))
        self.assertEqual(['L', 'A', 'N', 'SH', 'A0', 'F', 'T'], self.__g2p.word_to_phonemes('ландша+фт'))
        self.assertEqual(['J0', 'I', 'K', 'T', 'A0', 'SH'], self.__g2p.word_to_phonemes('ягдта+ш'))

    """
    Rule TLP 3. In combinations of letters «ЛНЦ» letter Л is removed.
    """

    def test_phrase_to_phonemes_positive_tlp3_001(self):
        """ Проверка правила ПБФ23. """
        self.assertEqual(['S', 'O0', 'N', 'TS', 'Y'], self.__g2p.word_to_phonemes('со+лнце'))

    """
    Rule TLP 4 (устарело). Combinations of letters  «СЧ» и «ЖЧ» go to «Щ», «ТС», «ТЬС», «ТЦ», «ДС» and «ДЦ» go to «Ц», 
    «СШ» goes to «Ш», «ЗЖ» goes to «Ж».
    Вместо него: «ТСЯ», «ТЬСЯ» на конце слова переходят в «ЦА».
    """

    def test_phrase_to_phonemes_positive_tlp4_001(self):
        """ Проверка правила ПБФ25. """
        self.assertEqual(['P0', 'I', 'R0', 'I', 'V', 'A', 'L', 'N', 'A', 'V', 'A0', 'TS', 'A'],
                         self.__g2p.word_to_phonemes('переволнова+ться'))
        self.assertEqual(['R', 'U', 'TSH0', 'A0', 'J0', 'I', 'TS', 'A'], self.__g2p.word_to_phonemes('руча+ется'))

    """
    Rule TLP 5. Affixes «ОГО», «ЕГО» or «ГО» go to «ВО», except «много», «дорого», «строго» and some other adverbs.
    """

    def test_phrase_to_phonemes_positive_tlp5_001(self):
        """ Проверка правила ПБФ26. """
        self.assertEqual(['K', 'R', 'A0', 'S', 'N', 'A', 'V', 'A'], self.__g2p.word_to_phonemes('кра+сного'))
        self.assertEqual(['S0', 'I0', 'N0', 'I', 'V', 'A'], self.__g2p.word_to_phonemes('си+него'))

    """
    Rule TLP 6.
    Modern mode:
        If i is «Н» and i+1 is one of the [J0], [TSH0], [SH0], [DZH0], [ZH0], [D0], [T0], [Z0], [S0], «Н» goes to [N].
        If i is «С», «З» and i+1 is one of the:
            1. [D0], [Z0] then i transforms to palatalized and voiced;
            2. [T0], [S0] then i transforms to palatalized and unvoiced;
            3. [N0] then i transforms to palatalized.

    Classic mode:
        If i is «Н» and i+1 is one of the [J0], [TSH0], [SH0], [DZH0], [ZH0], [D0], [T0], [Z0], [S0], [L0], [M0], [P0],
         [B0], [V0], [F0], [N0], «Н» goes to [N].
        If i is «Т», «С», «Д», «З», «П», «Б», «В», «Ф» and i+1 is one of the:
            1. [D0], [Z0], [B0] then i transforms to palatalized and voiced;
            2. [T0], [S0], [P0] then i transforms to palatalized and unvoiced;
            3. [N0], [L0], [M0], [V0], [F0] then i transforms to palatalized.
    
    """

    def test_phrase_to_phonemes_positive_tlp6_001(self):
        """ Проверка правила ПБФ6. """
        self.assertEqual(['A', 'N0', 'T0', 'I0', 'KH', 'R0', 'I', 'S', 'T'], self.__g2p.word_to_phonemes('анти+христ'))
        self.assertEqual(['B', 'A', 'N0', 'D0', 'U0', 'G', 'A'], self.__g2p.word_to_phonemes('бандю+га'))
        self.assertEqual(['K', 'O0', 'S0', 'T0'], self.__g2p.word_to_phonemes('ко+сть'))
        self.assertEqual(['U', 'S0', 'N0', 'I0'], self.__g2p.word_to_phonemes('усни+'))
        self.assertEqual(['P', 'U', 'S0', 'T0', 'A0', 'K'], self.__g2p.word_to_phonemes('пустя+к'))

    def test_phrase_to_phonemes_positive_tlp6_002(self):
        """ Проверка правила ПБФ27. """
        self.assertEqual(['V0', 'I', 'Z0', 'D0', 'E0'], self.__g2p.word_to_phonemes('везде+'))
        self.assertEqual(['S0', 'T0', 'E0', 'P0'], self.__g2p.word_to_phonemes('сте+пь'))
        self.assertEqual(['SH0', 'I', 'T', 'A0', 'L', 'S0', 'A'], self.__g2p.word_to_phonemes('счита+лся'))
        self.assertEqual(['J0', 'E0', 'S', 'L0', 'I'], self.__g2p.word_to_phonemes('е+сли'))

    """
    Rule TLP 7. Vowel transformation. Every vowel is being transformed consequently from right to left dependent on its
     context (previous and next letter). The transformation patterns are introduced in Table 1.
    """

    def test_phrase_to_phonemes_positive_tlp7_001(self):
        """ Checking line 1 for vowels."""
        self.assertEqual(['TSH0', 'J0', 'A0'], self.__g2p.phrase_to_phonemes('чья+'))
        self.assertEqual(['TSH0', 'J0', 'I0'], self.__g2p.phrase_to_phonemes('чьи+'))
        self.assertEqual(['U0', 'S0', 'T0', 'J0', 'I'], self.__g2p.phrase_to_phonemes('у+стье'))
        self.assertEqual(['M', 'A0', 'R0', 'J0', 'A'], self.__g2p.phrase_to_phonemes('Ма+рья'))
        self.assertEqual(['K', 'A', 'E0', 'L0', 'J0', 'A'], self.__g2p.phrase_to_phonemes('Коэ+льо'))
        self.assertEqual(['B', 'Y0', 'TSH0', 'J0', 'I'], self.__g2p.phrase_to_phonemes('бы+чьи'))
        self.assertEqual(['B0', 'E0', 'L', 'A', 'J0', 'A'], self.__g2p.phrase_to_phonemes('бе+лая'))
        self.assertEqual(['T', 'V', 'A', 'I0'], self.__g2p.phrase_to_phonemes('твои+'))

    def test_phrase_to_phonemes_positive_tlp7_002(self):
        """ Checking line 2 for vowels."""
        self.assertEqual(['R', 'A', 'Z', 'J0', 'O0', 'M'], self.__g2p.phrase_to_phonemes('разъё+м'))
        self.assertEqual(['P', 'A', 'D', 'J0', 'U0', 'P', 'K', 'A', 'J0'], self.__g2p.phrase_to_phonemes('под ю+бкой'))
        self.assertEqual(['B', 'U', 'L0', 'J0', 'O0', 'N'], self.__g2p.phrase_to_phonemes('бульо+н'))
        self.assertEqual(['J0', 'I', 'M', 'SH0', 'I0', 'K'], self.__g2p.phrase_to_phonemes('ямщи+к'))
        self.assertEqual(['V', 'Y0', 'B', 'A', 'R'], self.__g2p.phrase_to_phonemes('вы+бор'))
        self.assertEqual(['A', 'O0', 'R', 'T', 'A'], self.__g2p.phrase_to_phonemes('ао+рта'))

    def test_phrase_to_phonemes_positive_tlp7_003(self):
        """ Checking line 3 for vowels."""
        self.assertEqual(['TSH0', 'O0'], self.__g2p.phrase_to_phonemes('чё+'))
        self.assertEqual(['M', 'A0', 'J0', 'A'], self.__g2p.phrase_to_phonemes('ма+йя'))
        self.assertEqual(['SH0', 'I0'], self.__g2p.phrase_to_phonemes('щи+'))
        self.assertEqual(['K0', 'I', 'SH0', 'A0', 'N'], self.__g2p.phrase_to_phonemes('Кещя+н'))
        self.assertEqual(['J0', 'A0', 'R', 'TSH0', 'I'], self.__g2p.phrase_to_phonemes('я+рче'))
        self.assertEqual(['G', 'A', 'S', 'P', 'A0', 'TSH0', 'A'], self.__g2p.phrase_to_phonemes('гаспа+чо'))
        self.assertEqual(['U', 'D', 'A0', 'TSH0', 'A'], self.__g2p.phrase_to_phonemes('уда+ча'))

    def test_phrase_to_phonemes_positive_tlp7_004(self):
        """ Checking line 4 for vowels."""
        self.assertEqual(['M', 'A', 'J0', 'A0', 'M0', 'I'], self.__g2p.phrase_to_phonemes('майа+ми'))
        self.assertEqual(['TSH0', 'O0', 'R', 'N', 'Y', 'J0'], self.__g2p.phrase_to_phonemes('чё+рный'))
        self.assertEqual(['TSH0', 'I', 'S', 'T', 'O0', 'T', 'Y'], self.__g2p.phrase_to_phonemes('часто+ты'))

    def test_phrase_to_phonemes_positive_tlp7_005(self):
        """ Checking line 5 for vowels."""
        self.assertEqual(['N', 'R', 'A0', 'V0', 'I', 'TS', 'A'], self.__g2p.phrase_to_phonemes('нра+вится'))
        self.assertEqual(['S', 'T', 'R0', 'I', 'ZH', 'Y0'], self.__g2p.phrase_to_phonemes('стрижи+'))

    def test_phrase_to_phonemes_positive_tlp7_006(self):
        """ Checking line 6 for vowels."""
        self.assertEqual(['ZH', 'U', 'R0', 'I0'], self.__g2p.phrase_to_phonemes('жюри+'))
        self.assertEqual(['TS', 'E0', 'N', 'T', 'R'], self.__g2p.phrase_to_phonemes('це+нтр'))
        self.assertEqual(['L', 'U', 'TS', 'Y', 'K0', 'I0'], self.__g2p.phrase_to_phonemes('Луцяки+'))
        self.assertEqual(['SH', 'A', 'SH', 'L', 'Y0', 'K'], self.__g2p.phrase_to_phonemes('шашлы+к'))
        self.assertEqual(['SH', 'A', 'K0', 'I0', 'R', 'A', 'V', 'A', 'T0'],
                         self.__g2p.phrase_to_phonemes('шоки+ровать'))
        self.assertEqual(['SH', 'Y', 'P', 'T', 'A0', 'T0'], self.__g2p.phrase_to_phonemes('шепта+ть'))
        self.assertEqual(['ZH', 'Y', 'V', 'O0', 'J0'], self.__g2p.phrase_to_phonemes('живо+й'))

    def test_phrase_to_phonemes_positive_tlp7_007(self):
        """ Checking line 7 for vowels."""
        self.assertEqual(['V', 'A0', 'S0', 'A'], self.__g2p.phrase_to_phonemes('Ва+ся'))
        self.assertEqual(['V', 'A0', 'S0', 'I'], self.__g2p.phrase_to_phonemes('Ва+се'))
        self.assertEqual(['V', 'A0', 'S0', 'I'], self.__g2p.phrase_to_phonemes('Ва+си'))

    def test_phrase_to_phonemes_positive_tlp7_008(self):
        """ Checking line 8 for vowels."""
        self.assertEqual(['L0', 'I', 'G', 'U0', 'SH', 'K', 'A'], self.__g2p.phrase_to_phonemes('лягу+шка'))
        self.assertEqual(['M', 'A', 'R', 'O0', 'S'], self.__g2p.phrase_to_phonemes('моро+з'))

    """
    Rule TLP 8. Consonant transformation. Every consonant is being transformed consequently from right to left 
    dependent on its context (previous and next letter). The transformation patterns are introduced in the table, 
    available at GitHub russian_g2p repository.
    """

    def test_phrase_to_phonemes_positive_tlp8_001(self):
        """ Checking line 1 for consonants in the middle"""
        self.assertEqual(['M0', 'I0', 'T0', 'K', 'A'], self.__g2p.phrase_to_phonemes('Ми+тька'))

    def test_phrase_to_phonemes_positive_tlp8_002(self):
        """ Checking line 2 for consonants in the middle"""
        self.assertEqual(['D0', 'J0', 'A0', 'K', 'A', 'N'], self.__g2p.phrase_to_phonemes('дья+кон'))
        self.assertEqual(['S', 'A', 'N0', 'T0', 'J0', 'A0', 'G', 'A'], self.__g2p.phrase_to_phonemes('Сантья+го'))

    def test_phrase_to_phonemes_positive_tlp8_003(self):
        """ Checking line 3 for consonants in the middle"""
        self.assertEqual(['S', 'V', 'A0', 'D0', 'B', 'A'], self.__g2p.phrase_to_phonemes('сва+дьба'))
        self.assertEqual(['ZH', 'Y', 'N0', 'I0', 'D0', 'B', 'A'], self.__g2p.phrase_to_phonemes('жени+тьба'))

    def test_phrase_to_phonemes_positive_tlp8_004(self):
        """ Checking line 4 for consonants in the middle"""
        self.assertEqual(['D0', 'E0', 'T'], self.__g2p.phrase_to_phonemes('де+д'))
        self.assertEqual(['T0', 'E0', 'R0', 'I', 'M'], self.__g2p.phrase_to_phonemes('те+рем'))

    def test_phrase_to_phonemes_positive_tlp8_005(self):
        """ Checking line 5 for consonants in the middle"""
        self.assertEqual(['N', 'A', 'K', 'T0', 'O0', 'M'], self.__g2p.phrase_to_phonemes('ногтё+м'))
        self.assertEqual(['L', 'A', 'K', 'T0', 'O0', 'M'], self.__g2p.phrase_to_phonemes('локтё+м'))

    def test_phrase_to_phonemes_positive_tlp8_006(self):
        """ Checking line 6 for consonants in the middle"""
        self.assertEqual(['G', 'R', 'U0', 'S'], self.__g2p.phrase_to_phonemes('гру+з'))
        self.assertEqual(['K', 'R', 'U0', 'K'], self.__g2p.phrase_to_phonemes('кру+г'))

    def test_phrase_to_phonemes_positive_tlp8_007(self):
        """ Checking line 7 for consonants in the middle"""
        self.assertEqual(['G', 'D0', 'E0'], self.__g2p.phrase_to_phonemes('где+'))
        self.assertEqual(['V', 'A', 'G', 'Z', 'A0', 'L'], self.__g2p.phrase_to_phonemes('вокза+л'))

    def test_phrase_to_phonemes_positive_tlp8_008(self):
        """ Checking line 8 for consonants in the middle"""
        self.assertEqual(['G', 'O0', 'L0', 'F'], self.__g2p.phrase_to_phonemes('го+льф'))
        self.assertEqual(['K', 'O0', 'M0', 'I', 'K'], self.__g2p.phrase_to_phonemes('ко+мик'))

    def test_phrase_to_phonemes_positive_tlp8_009(self):
        """ Checking line 1 for consonants in the end"""
        self.assertEqual(['G', 'R0', 'I0', 'P'], self.__g2p.phrase_to_phonemes('гри+б'))
        self.assertEqual(['T', 'R', 'U0', 'P'], self.__g2p.phrase_to_phonemes('тру+п'))

    def test_phrase_to_phonemes_positive_tlp8_010(self):
        """ Checking line 2 for consonants in the end"""
        self.assertEqual(['S', 'K', 'O0', 'R', 'P0', 'S', 'T', 'A0', 'R', 'A', 'J0', 'A'],
                         self.__g2p.phrase_to_phonemes('ско+рбь ста+рая'))
        self.assertEqual(['G', 'R', 'U0', 'S0', 'T0', 'P', 'R0', 'I', 'SH', 'L', 'A0'],
                         self.__g2p.phrase_to_phonemes('гру+сть пришла+'))

    def test_phrase_to_phonemes_positive_tlp8_011(self):
        """ Checking line 3 for consonants in the end"""
        self.assertEqual(['S', 'K', 'O0', 'R', 'P0', 'V0', 'E0', 'TSH0', 'N', 'A', 'J0', 'A'],
                         self.__g2p.phrase_to_phonemes('ско+рбь ве+чная'))
        self.assertEqual(['G', 'R', 'U0', 'S0', 'T0', 'V0', 'E0', 'TSH0', 'N', 'A', 'J0', 'A'],
                         self.__g2p.phrase_to_phonemes('гру+сть ве+чная'))

    def test_phrase_to_phonemes_positive_tlp8_012(self):
        """ Checking line 4 for consonants in the end"""
        self.assertEqual(['S', 'K', 'O0', 'R', 'B0', 'G', 'O0', 'R0', 'K', 'A', 'J0', 'A'],
                         self.__g2p.phrase_to_phonemes('ско+рбь го+рькая'))
        self.assertEqual(['G', 'R', 'U0', 'Z0', 'D0', 'G', 'O0', 'R0', 'K', 'A', 'J0', 'A'],
                         self.__g2p.phrase_to_phonemes('гру+сть го+рькая'))

    def test_phrase_to_phonemes_positive_tlp8_013(self):
        """ Checking line 5 for consonants in the end"""
        self.assertEqual(['S', 'K', 'O0', 'R', 'P0', 'U', 'ZH', 'E0'], self.__g2p.phrase_to_phonemes('ско+рбь уже+'))
        self.assertEqual(['G', 'R', 'U0', 'S0', 'T0', 'U', 'ZH', 'E0'], self.__g2p.phrase_to_phonemes('гру+сть уже+'))

    def test_phrase_to_phonemes_positive_tlp8_014(self):
        """ Checking line 6 for consonants in the end"""
        self.assertEqual(['G', 'R0', 'I0', 'P', 'S', 'V0', 'E0', 'ZH', 'Y', 'J0'],
                         self.__g2p.phrase_to_phonemes('гри+б све+жий'))
        self.assertEqual(['T', 'R', 'U0', 'P', 'S', 'V0', 'E0', 'ZH', 'Y', 'J0'],
                         self.__g2p.phrase_to_phonemes('тру+п све+жий'))

    def test_phrase_to_phonemes_positive_tlp8_015(self):
        """ Checking line 7 for consonants in the end"""
        self.assertEqual(['G', 'R0', 'I0', 'P', 'V0', 'A0', 'L', 'Y', 'J0'],
                         self.__g2p.phrase_to_phonemes('гри+б вя+лый'))
        self.assertEqual(['T', 'R', 'U0', 'P', 'V0', 'A0', 'L', 'Y', 'J0'],
                         self.__g2p.phrase_to_phonemes('тру+п вя+лый'))

    def test_phrase_to_phonemes_positive_tlp8_016(self):
        """ Checking line 8 for consonants in the end"""
        self.assertEqual(['G', 'R0', 'I0', 'B', 'G', 'A', 'R0', 'A0', 'TSH0', 'I', 'J0'],
                         self.__g2p.phrase_to_phonemes('гри+б горя+чий'))
        self.assertEqual(['T', 'R', 'U0', 'B', 'G', 'A', 'R0', 'A0', 'TSH0', 'I', 'J0'],
                         self.__g2p.phrase_to_phonemes('тру+п горя+чий'))

    def test_phrase_to_phonemes_positive_tlp8_017(self):
        """ Checking line 9 for consonants in the end"""
        self.assertEqual(['G', 'R0', 'I0', 'P', 'U', 'ZH', 'E0'], self.__g2p.phrase_to_phonemes('гри+б уже+'))
        self.assertEqual(['T', 'R', 'U0', 'P', 'U', 'ZH', 'E0'], self.__g2p.phrase_to_phonemes('тру+п уже+'))

    """
    Rule TLP 9. If i and i+1 are the same phonemes, then they are substituted with a corresponding long variant 
    (e.g. [A0 A0] → [A0l]).
    Обновлено: A A0 -> A0l, A0 A0 -> A0l
    """

    def test_phrase_to_phonemes_positive_tlp9_001(self):
        """ Проверка правила ПБФ7. """
        # self.assertEqual(['I', 'N0', 'T0', 'I', 'L0l', 'I', 'G0', 'E0', 'N', 'T'],
        #                  self.__g2p.word_to_phonemes('интеллиге+нт'))
        self.assertEqual(['I', 'N0', 'T0', 'I', 'L0', 'I', 'G0', 'E0', 'N', 'T'],
                         self.__g2p.word_to_phonemes('интеллиге+нт'))
        # self.assertEqual(['K', 'A', 'M0', 'I0', 'S0l', 'I', 'J0', 'A'], self.__g2p.word_to_phonemes('коми+ссия'))
        self.assertEqual(['K', 'A', 'M0', 'I0', 'S0', 'I', 'J0', 'A'], self.__g2p.word_to_phonemes('коми+ссия'))
        # self.assertEqual(['M', 'A', 'S0l', 'I0', 'F'], self.__g2p.word_to_phonemes('масси+в'))
        self.assertEqual(['M', 'A', 'S0', 'I0', 'F'], self.__g2p.word_to_phonemes('масси+в'))
        # self.assertEqual(['A', 'T0l', 'A0', 'SH', 'K', 'A'], self.__g2p.word_to_phonemes('оття+жка'))
        self.assertEqual(['A', 'T0', 'A0', 'SH', 'K', 'A'], self.__g2p.word_to_phonemes('оття+жка'))
        # self.assertEqual(['A', 'S0l', 'I', 'S0', 'T0', 'E0', 'N', 'T'], self.__g2p.word_to_phonemes('ассисте+нт'))
        self.assertEqual(['A', 'S0', 'I', 'S0', 'T0', 'E0', 'N', 'T'], self.__g2p.word_to_phonemes('ассисте+нт'))

    """
    Rule TLP 10. If i is a prefix of i+1, then they are substituted with a corresponding long variant 
    of the i+1 phoneme (e.g. [Z ZH] → [ZHl]).
    Обновлено: такие тройки фонем нужно смотреть в специальном dict.
    """

    def test_phrase_to_phonemes_positive_tlp10_001(self):
        """ Проверка TLP 10. """
        self.assertEqual(['B', 'L0', 'U0', 'TS', 'Y'], self.__g2p.word_to_phonemes('блю+дце'))
        self.assertEqual(['A', 'TS', 'A0'], self.__g2p.word_to_phonemes('отца+'))
        self.assertEqual(['R', 'A', 'SH', 'Y0', 'P'], self.__g2p.word_to_phonemes('расши+б'))
        self.assertEqual(['V', 'J0', 'I', 'ZH', 'A0', 'T0'], self.__g2p.word_to_phonemes('въезжа+ть'))

    def test_word_to_phonemes_positive029(self):
        """ Проверка корректности обработки прописных букв. """
        self.assertEqual(self.__g2p.word_to_phonemes('ё+жик'), self.__g2p.word_to_phonemes('Ё+жик'))

    @unittest.skip
    def test_word_to_phonemes_positive030(self):
        """ Проверка корректности обработки ударения для буквы `ё` -- устарел. """
        self.assertEqual(self.__g2p.word_to_phonemes('ё+жик'), self.__g2p.word_to_phonemes('ёжик'))
        self.assertEqual(self.__g2p.word_to_phonemes('ё+жик'), self.__g2p.word_to_phonemes('Ёжик'))

    def test_word_to_phonemes_positive031(self):
        """ Баг https://github.com/nsu-ai/russian_g2p/issues/8 """
        self.assertEqual(['SH', 'A', 'F0', 'O0', 'R'], self.__g2p.word_to_phonemes('шофё+р'))

    def test_word_to_phonemes_positive032(self):
        """ Баг https://github.com/nsu-ai/russian_g2p/issues/8 """
        self.assertEqual(['J0', 'I0', 'TSH0', 'N0', 'I', 'TS', 'U'], self.__g2p.word_to_phonemes('яи+чницу'))

    def test_word_to_phonemes_positive033(self):
        """ Проверка, что костыль для удаления длинных фонем работает """
        self.assertEqual(['A', 'B0', 'I', 'S0', 'I0', 'N0', 'I'], self.__g2p.word_to_phonemes('абисси+нии'))

    def test_word_to_phonemes_negative001(self):
        """ Генерация исключения, если аргумент - пустая строка. """
        source_word = ''
        target_error_message = 'Checked word is empty string!'
        with self.assertRaisesRegex(AssertionError, re.escape(target_error_message)):
            self.__g2p.word_to_phonemes(source_word)

    def test_word_to_phonemes_negative002(self):
        """ Генерация исключения, если слово содержит недопустимые символы. """
        source_word = 'интерде+вочка!'
        target_error_message = '`интерде+вочка!`: this word contains inadmissible characters!'
        with self.assertRaisesRegex(AssertionError, re.escape(target_error_message)):
            self.__g2p.word_to_phonemes(source_word)

    def test_word_to_phonemes_negative003(self):
        """ Генерация исключения, если слово содержит только неалфавитные символы, хоть и допустимые. """
        source_word = '+-'
        target_error_message = '`+-`: this word is incorrect!'
        with self.assertRaisesRegex(AssertionError, re.escape(target_error_message)):
            self.__g2p.word_to_phonemes(source_word)

    def test_word_to_phonemes_negative004(self):
        """ Генерация предупреждения, если слово указано без ударения и содержит более одной гласной. """
        source_word = 'через'
        target_warning_message = '`через`: the accent for this word is unknown!'
        with self.assertWarnsRegex(UserWarning, re.escape(target_warning_message)):
            self.__g2p.word_to_phonemes(source_word)

    def test_word_to_phonemes_negative005(self):
        """ Генерация исключения, если exception_for_nonaccented, а слово - без ударения и содержит более 1 гласной. """
        g2p = Grapheme2Phoneme(exception_for_nonaccented=True)
        source_word = 'через'
        target_warning_message = '`через`: the accent for this word is unknown!'
        with self.assertRaisesRegex(ValueError, re.escape(target_warning_message)):
            g2p.word_to_phonemes(source_word)

    def test_phrase_to_phonemes_positive001(self):
        """ Проверка корректной работы правил межсловного преобразования на стыке служебного и знаменательного слова.
        Служебное слово - обычная частица. """
        self.assertEqual(['N0', 'I', 'D0', 'E0', 'L', 'A', 'T0'], self.__g2p.phrase_to_phonemes('не де+лать'))

    def test_phrase_to_phonemes_positive002(self):
        """ Проверка корректной работы правил межсловного преобразования на стыке служебного и знаменательного слова.
        Служебное слово - частица, присоединяемая дефисом. """
        self.assertEqual(['P', 'A', 'SH', 'O0', 'L', 'T', 'A', 'K0', 'I'], self.__g2p.phrase_to_phonemes('пошё+л-таки'))

    def test_phrase_to_phonemes_positive003(self):
        """ Проверка корректной работы правил межсловного преобразования на стыке служебного и знаменательного слова.
        Внутри служебного слова дефис. """
        # self.assertEqual(['I', 'Zl', 'A', 'T', 'U0', 'TSH0'], self.__g2p.phrase_to_phonemes('из-за ту+ч'))
        self.assertEqual(['I', 'Z', 'A', 'T', 'U0', 'TSH0'], self.__g2p.phrase_to_phonemes('из-за ту+ч'))

    def test_phrase_to_phonemes_positive004(self):
        """ Проверка корректной работы правил межсловного преобразования на стыке служебного и знаменательного слова.
        Для первого слова: первое слово заканчивается гласной. """
        self.assertEqual(['P', 'A', 'D', 'A', 'R', 'O0', 'G0', 'I'], self.__g2p.phrase_to_phonemes('по доро+ге'))
        self.assertEqual(['N', 'A', 'S', 'T', 'A', 'L0', 'E0'], self.__g2p.phrase_to_phonemes('на столе+'))

    def test_phrase_to_phonemes_positive005(self):
        """ Проверка корректной работы правил межсловного преобразования на стыке служебного и знаменательного слова.
        Для первого слова: первое слово заканчивается согласной, проверка ассимиляции по глухости-звонкости. """
        self.assertEqual(['F', 'S', 'A', 'D', 'U0'], self.__g2p.phrase_to_phonemes('в саду+'))
        self.assertEqual(['V', 'L0', 'I', 'S', 'U0'], self.__g2p.phrase_to_phonemes('в лесу+'))
        self.assertEqual(['Z', 'D', 'A', 'R', 'O0', 'G0', 'I'], self.__g2p.phrase_to_phonemes('с доро+ги'))
        self.assertEqual(['S', 'V', 'A0', 'S0', 'I', 'J0'], self.__g2p.phrase_to_phonemes('с Ва+сей'))

    def test_phrase_to_phonemes_positive006(self):
        """ Проверка корректной работы правил межсловного преобразования на стыке служебного и знаменательного слова.
        Для первого слова: первое слово заканчивается твёрдой согласной, которая не должна переходить в мягкую фонему
        перед гласными Я, Ё, Ю, Е, И. """
        self.assertEqual(['P', 'A', 'D', 'J0', 'O0', 'L', 'K', 'A', 'J0'], self.__g2p.phrase_to_phonemes('под ё+лкой'))

    def test_phrase_to_phonemes_positive007(self):
        """ Проверка корректной работы правил межсловного преобразования на стыке служебного и знаменательного слова.
        Для первого слова: первое слово заканчивается согласной, и она ассимилируется с последующей мягкой
        согласной, одинаковой по месту образования. """
        self.assertEqual(['B0', 'I', 'Z0', 'D0', 'E0', 'D', 'A'], self.__g2p.phrase_to_phonemes('без де+да'))

    def test_phrase_to_phonemes_positive008(self):
        """ Проверка корректной работы правил межсловного преобразования на стыке служебного и знаменательного слова.
        Для второго слова: первое слово заканчивается мягким знаком, а второе слово начинается с гласной О или с
        гласной И, и эти гласные ни в коем случае не должны переходить в сочетания фонем [J O] или [J I]
        ([J I0], если под ударением) соответственно. """
        self.assertEqual(['I', 'L0', 'O0', 'S0', 'I', 'N0'], self.__g2p.phrase_to_phonemes('иль о+сень'))  # выдает O
        self.assertEqual(['I', 'L0', 'I0', 'V', 'A', 'L', 'G', 'A'], self.__g2p.phrase_to_phonemes('иль и+волга'))

    def test_phrase_to_phonemes_positive009(self):
        """ Проверка корректной работы правил межсловного преобразования на стыке служебного и знаменательного слова.
        Для второго слова: второе слово начинается с гласной И, которая должна переходить в фонему [Y]
        (или [Y0], если под ударением) после всех согласных, кроме Й. """
        self.assertEqual(['P', 'A', 'D', 'Y0', 'V', 'A', 'J0'], self.__g2p.phrase_to_phonemes('под и+вой'))
        self.assertEqual(['S', 'Y', 'V', 'A0', 'N', 'A', 'M'], self.__g2p.phrase_to_phonemes('с Ива+ном'))
        # для второго слова: если первое слово заканчивается мягким знаком, то согласная смягчается, но не оглушается
        self.assertEqual(['V0', 'I', 'T0', 'I', 'V', 'A0', 'N'], self.__g2p.phrase_to_phonemes('ведь Ива+н'))

    def test_phrase_to_phonemes_positive010(self):
        """ Проверка корректной работы правил межсловного преобразования на стыке двух знаменательных слов.
        Для первого слова: если последняя буква первого слова - глухая согласная П, Т, К, Ф, С, Ш, Щ, Ц, Ч (либо
        предпоследняя буква, а последняя - мягкий знак), то эта глухая согласная должна озвончаться, если первой буквой
        второго слова является Б, Д, Г, З или Ж. При этом появляются "неканонические", вспомогательные фонемы, которых
        нет при обычном внутрисловном преобразовании: Щ -> [ZH0], Ц -> [DZ], Ч -> [DZH0] """
        self.assertEqual(['B', 'O0', 'R', 'ZH0', 'G', 'A', 'R0', 'A0', 'TSH0', 'I', 'J0'],
                         self.__g2p.phrase_to_phonemes('бо+рщ горя+чий'))
        self.assertEqual(['Z', 'A0', 'J0', 'I', 'DZ', 'B0', 'I', 'L0', 'A0', 'K'],
                         self.__g2p.phrase_to_phonemes('за+яц беля+к'))
        self.assertEqual(['D', 'O0', 'DZH0', 'G', 'U', 'L0', 'A0', 'J0', 'I', 'T'],
                         self.__g2p.phrase_to_phonemes('до+чь гуля+ет'))

    def test_phrase_to_phonemes_positive011(self):
        """ Проверка корректной работы правил межсловного преобразования на стыке двух знаменательных слов.
        Для первого слова: если последняя буква первого слова - звонкая согласная Б, В, Г, Д, Ж или З (либо
        предпоследняя буква, а последняя - мягкий знак), то она не оглушается тогда и только тогда, когда первой буквой
        второго слова являются Б, Д, Г, З или Ж """
        self.assertEqual(['D', 'U0', 'B', 'Z0', 'I', 'L0', 'O0', 'N', 'Y', 'J0'],
                         self.__g2p.phrase_to_phonemes('ду+б зелё+ный'))
        self.assertEqual(['B', 'R', 'O0', 'V0', 'Z', 'O0', 'I'],
                         self.__g2p.phrase_to_phonemes('бро+вь Зо+и'))
        # пример, когда правило не должно работать, поскольку первая буква второго слова не удовлетворяет условию
        self.assertEqual(['B', 'R', 'O0', 'F0', 'N0', 'I0', 'N', 'Y'],
                         self.__g2p.phrase_to_phonemes('бро+вь Ни+ны'))

    def test_phrase_to_phonemes_positive012(self):
        """ Проверка корректной работы правил межсловного преобразования на стыке двух знаменательных слов.
        Для первого слова: если последняя буква первого слова - твёрдая согласная, то она не должна переходить в мягкую
        фонему перед гласными Я, Ё, Ю, Е, И """
        self.assertEqual(['S', 'A0', 'T', 'J0', 'O0', 'L', 'A', 'K'],
                         self.__g2p.phrase_to_phonemes('са+д ё+лок'))
        self.assertEqual(['G', 'O0', 'R', 'A', 'T', 'J0', 'I', 'R0', 'I', 'V', 'A0', 'N'],
                         self.__g2p.phrase_to_phonemes('го+род Ерева+н'))

    def test_phrase_to_phonemes_positive013(self):
        """ Проверка корректной работы правил межсловного преобразования на стыке двух знаменательных слов.
        Для первого слова: если последняя буква первого слова - согласная, то она не ассимилилуется с последующей мягкой
        согласной, одинаковой по месту образования. """
        self.assertEqual(['G', 'O0', 'R', 'A', 'T', 'S0', 'I', 'M', 'B0', 'I0', 'R', 'S', 'K'],
                         self.__g2p.phrase_to_phonemes('го+род Симби+рск'))

    def test_phrase_to_phonemes_positive014(self):
        """ Проверка корректной работы правил межсловного преобразования на стыке двух знаменательных слов.
        Для второго слова: второе слово начинается с гласной И, которая должна переходить в фонему [Y]
        (или [Y0], если под ударением) после всех согласных, кроме Й """
        self.assertEqual(['L0', 'I0', 'S', 'T', 'Y0', 'V', 'Y'],
                         self.__g2p.phrase_to_phonemes('ли+ст и+вы'))
        self.assertEqual(['N', 'O0', 'S', 'Y', 'V', 'A0', 'N', 'A'],
                         self.__g2p.phrase_to_phonemes('но+с Ива+на'))
        # если первое слово заканчивается мягким знаком, то правило не должно выполняться
        self.assertEqual(['M', 'A0', 'T0', 'I', 'V', 'A0', 'N', 'A'],
                         self.__g2p.phrase_to_phonemes('ма+ть Ива+на'))

    def test_phrase_to_phonemes_positive015(self):
        """ Проверка корректной работы правил межсловного преобразования на стыке двух знаменательных слов.
        Два знаменательных слова объединены в одно через дефис. """
        self.assertEqual(['K', 'A', 'Z', 'A', 'K0', 'I0', 'R', 'A', 'Z', 'B', 'O0', 'J0', 'N0', 'I', 'K0', 'I'],
                         self.__g2p.phrase_to_phonemes('казаки+-разбо+йники'))
        self.assertEqual(['J0', 'I', 'D', 'R0', 'I0', 'T0', 'K', 'A', 'L', 'A', 'T0', 'I0', 'T0'],
                         self.__g2p.phrase_to_phonemes('едри+ть-колоти+ть'))

    def test_phrase_to_phonemes_positive016(self):
        """ Проверка корректного транскрибирования некоторых междометий. """
        self.assertEqual(['O0', 'KH', 'O0', 'KH', 'O0', 'KH'], self.__g2p.phrase_to_phonemes('о+х-о+х-о+х'))
        self.assertEqual(['B', 'A0', 'J0', 'U', 'SH', 'K0', 'I', 'B', 'A', 'J0', 'U0'],
                         self.__g2p.phrase_to_phonemes('ба+юшки-баю+'))
        self.assertEqual(['T', 'R', 'A0', 'KH', 'T', 'A0', 'KH', 'T', 'A0', 'KH'],
                         self.__g2p.phrase_to_phonemes('тра+х-та+х-та+х'))
        self.assertEqual(['T', 'R0', 'E0', 'N0', 'B', 'R0', 'E0', 'N0'], self.__g2p.phrase_to_phonemes('тре+нь-бре+нь'))

    def test_phrase_to_phonemes_positive017(self):
        """ Проверка корректности транскрибирования целых фраз, состоящих более чем из двух слов.
        Простое предложение. """
        self.assertEqual(['J0', 'O0', 'L', 'K', 'A', 'S', 'T', 'A', 'J0', 'A0', 'L', 'A', 'U', 'A', 'K', 'N', 'A0'],
                         self.__g2p.phrase_to_phonemes('ё+лка стоя+ла у окна+'))
        self.assertEqual(['SH', 'A', 'F0', 'O0', 'R', 'V0', 'I', 'D0', 'O0', 'T', 'M', 'A', 'SH', 'Y0', 'N', 'U'],
                         self.__g2p.phrase_to_phonemes('шофё+р ведё+т маши+ну'))
        self.assertEqual(['A', 'M', 'A', 'SH', 'Y0', 'N', 'A', 'N0', 'I', 'V', 'Y0', 'D0', 'I', 'R', 'ZH', 'A', 'L',
                          'A', 'P0', 'I', 'R0', 'I', 'G', 'R', 'U0', 'S', 'K0', 'I'],
                         self.__g2p.phrase_to_phonemes('а маши+на не вы+держала перегру+зки'))
        self.assertEqual(['M', 'O0', 'S', 'T', 'TSH0', 'E0', 'R0', 'I', 'Z', 'N', 'A', 'V', 'A', 'S0', 'I', 'B0', 'I0',
                          'R', 'S', 'K'],
                         self.__g2p.phrase_to_phonemes('мо+ст че+рез новосиби+рск'))

    def test_phrase_to_phonemes_positive018(self):
        """ Проверка корректности транскрибирования целых фраз, состоящих более чем из двух слов.
        Простое предложение с двумя словами-фонетическими исключениями ("мужчины" и "декольте"). """
        # self.assertEqual(
        #     ['P', 'A', 'TS', 'Y', 'L', 'U0', 'J0', 'M', 'U', 'SH0', 'I0', 'N', 'Y', 'F', 'SH0', 'E0', 'D', 'R', 'Al',
        #      'T', 'K', 'R', 'Y0', 'T', 'A', 'J0', 'I', 'ZH', 'E0', 'N', 'S', 'K', 'A', 'J0', 'I', 'D', 'Y', 'K', 'A',
        #      'L0', 'T', 'E0', 'V', 'O0', 'F', 'S0', 'I', 'N0', 'I', 'SH0', 'I', 'T', 'A0', 'L', 'S0', 'A', 'N0', 'I',
        #      'P', 'R0', 'I', 'L0', 'I0', 'TSH0', 'N', 'Y', 'M'],
        #     self.__g2p.phrase_to_phonemes('поцелу+й мужчи+ны в ще+дро откры+тое же+нское декольте+ во+все не счита+лся '
        #                                   'неприли+чным')
        # )
        self.assertEqual(
            ['P', 'A', 'TS', 'Y', 'L', 'U0', 'J0', 'M', 'U', 'SH0', 'I0', 'N', 'Y', 'F', 'SH0', 'E0', 'D', 'R', 'A',
             'T', 'K', 'R', 'Y0', 'T', 'A', 'J0', 'I', 'ZH', 'E0', 'N', 'S', 'K', 'A', 'J0', 'I', 'D', 'Y', 'K', 'A',
             'L0', 'T', 'E0', 'V', 'O0', 'F', 'S0', 'I', 'N0', 'I', 'SH0', 'I', 'T', 'A0', 'L', 'S0', 'A', 'N0', 'I',
             'P', 'R0', 'I', 'L0', 'I0', 'TSH0', 'N', 'Y', 'M'],
            self.__g2p.phrase_to_phonemes('поцелу+й мужчи+ны в ще+дро откры+тое же+нское декольте+ во+все не счита+лся '
                                          'неприли+чным')
        )

    def test_phrase_to_phonemes_positive019(self):
        """ Проверка стыка знаменательного и служебного слов в ситуации, когда служебное слово идёт вторым. """
        self.assertEqual(['J0', 'E0', 'S', 'L0', 'I', 'B', 'Y', 'N0', 'I', 'T', 'Y0'],
                         self.__g2p.phrase_to_phonemes('е+сли бы не ты+'))
        self.assertEqual(['J0', 'E0', 'S', 'L0', 'I', 'P', 'N0', 'E0', 'B', 'Y', 'L', 'A', 'T0', 'I', 'B0', 'A0'],
                         self.__g2p.phrase_to_phonemes('е+сли б не+ было тебя+'))  # "есьли" очень смущает

    def test_phrase_to_phonemes_positive020(self):
        """ Проверка стыка знаменательного и служебного слов в ситуации, когда служебное слово - частица с дефисом. """
        self.assertEqual(['D', 'A', 'V', 'A0', 'J0', 'K', 'A', 'R', 'A', 'Z', 'B0', 'I', 'R0', 'O0', 'M', 'S0', 'A'],
                         self.__g2p.phrase_to_phonemes('дава+й-ка разберё+мся'))

    def test_phrase_to_phonemes_negative001(self):
        """ Генерация исключения, если аргумент - пустая строка. """
        source_phrase = ''
        target_error_message = 'Checked phrase is empty string!'
        with self.assertRaisesRegex(AssertionError, re.escape(target_error_message)):
            self.__g2p.phrase_to_phonemes(source_phrase)

    def test_in_function_words_1_positive001(self):
        """ Проверить корректность определения функциональных слов первого рода. """
        self.assertFalse(self.__g2p.in_function_words_1('ма+ма'))
        self.assertFalse(self.__g2p.in_function_words_1('мама'))
        self.assertFalse(self.__g2p.in_function_words_1('Ма+ма'))
        self.assertTrue(self.__g2p.in_function_words_1('через'))
        self.assertTrue(self.__g2p.in_function_words_1('че+рез'))
        self.assertTrue(self.__g2p.in_function_words_1('Через'))

    def test_in_function_words_2_positive001(self):
        """ Проверить корректность определения функциональных слов второго рода. """
        self.assertFalse(self.__g2p.in_function_words_2('ма+ма'))
        self.assertFalse(self.__g2p.in_function_words_2('мама'))
        self.assertFalse(self.__g2p.in_function_words_2('Ма+ма'))
        self.assertTrue(self.__g2p.in_function_words_2('-нибудь'))
        self.assertTrue(self.__g2p.in_function_words_2('-нибу+дь'))
        self.assertFalse(self.__g2p.in_function_words_2('нибудь'))
        self.assertFalse(self.__g2p.in_function_words_2('нибу+дь'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
