class Consonant:
    def __init__(self, nh=None, dh=None, vh=None, ns=None, ds=None, vs=None):
        self.forms = dict(
            # normal, deaf and voiced x soft and hard
            n_hard=nh, d_hard=dh, v_hard=vh, n_soft=ns, d_soft=ds, v_soft=vs
        )


class Vocal:
    def __init__(self, c1=None, c2=None, c3=None, c4=None, c5=None, c6=None, c7=None, c8=None):
        self.forms = dict(
            case1=c1, case2=c2, case3=c3, case4=c4, case5=c5, case6=c6, case7=c7, case8=c8
        )


class Phonetics:
    def __init__(self):
        self.vocals_phonemes = {'U0', 'U', 'O0', 'O', 'A0', 'A', 'E0', 'E', 'Y0', 'Y', 'I0', 'I',
                                'U0l', 'Ul', 'O0l', 'Ol', 'A0l', 'Al', 'E0l', 'El', 'Y0l', 'Yl', 'I0l', 'Il'}

        self.voiced_weak_phonemes = {'J0', 'V0', 'V', 'N0', 'N', 'L0', 'L', 'M0', 'M', 'R0', 'R',
                                     'J0l', 'V0l', 'Vl', 'N0l', 'Nl', 'L0l', 'Ll', 'M0l', 'Ml', 'R0l', 'Rl'}

        self.voiced_strong_phonemes = {'B', 'B0', 'G', 'G0', 'D', 'D0', 'Z', 'Z0', 'ZH', 'ZH0',
                                       'GH', 'GH0', 'DZ', 'DZ0', 'DZH', 'DZH0',
                                       'Bl', 'B0l', 'Gl', 'G0l', 'Dl', 'D0l', 'Zl', 'Z0l', 'ZHl', 'ZH0l',
                                       'GHl', 'GH0l', 'DZl', 'DZ0l', 'DZHl', 'DZH0l'}

        self.deaf_phonemes = {'K', 'K0', 'P', 'P0', 'S', 'S0', 'T', 'T0', 'F', 'F0', 'KH', 'KH0',
                              'TS', 'TS0', 'TSH', 'TSH0', 'SH', 'SH0',
                              'Kl', 'K0l', 'Pl', 'P0l', 'Sl', 'S0l', 'Tl', 'T0l', 'Fl', 'F0l', 'KHl', 'KH0l',
                              'TSl', 'TS0l', 'TSHl', 'TSH0l', 'SHl', 'SH0l'}

        self.russian_phonemes_set = self.vocals_phonemes | self.voiced_weak_phonemes | \
                                    self.voiced_strong_phonemes | self.deaf_phonemes

        self.all_russian_letters = {'а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о',
                                    'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю',
                                    'я', 'h', 'z', 'j', 'g'}

        self.hard_and_soft_signs = {'ъ', 'ь'}

        self.vocals = {'а', 'о', 'у', 'э', 'ы', 'и', 'я', 'ё', 'ю', 'е', 'а+', 'о+', 'у+', 'э+', 'ы+', 'и+', 'я+',
                       'ё+', 'ю+', 'е+'}

        self.double_vocals = {'е', 'ё', 'ю', 'я', 'е+', 'ё+', 'ю+', 'я+'}

        # назвать получше
        self.gen_vocals_hard = {'ъ', 'а', 'о', 'у', 'э', 'ы', 'а+', 'о+', 'у+', 'э+', 'ы+'}
        self.gen_vocals_soft = {'ь', 'я', 'ё', 'ю', 'е', 'и', 'я+', 'ё+', 'ю+', 'е+', 'и+'}

        self.consonants = {'б', 'в', 'г', 'д', 'ж', 'з', 'й', 'к', 'л', 'м', 'н', 'п', 'р', 'с', 'т', 'ф', 'х', 'ц',
                           'ч', 'ш', 'щ', 'h', 'z', 'j', 'g'}

        self.deaf_consonants = {'к', 'п', 'с', 'т', 'ф', 'х', 'ц', 'ч', 'ш', 'щ'}
        self.voiced_weak_consonants = {'в', 'й', 'л', 'м', 'н', 'р'}
        self.voiced_strong_consonants = {'б', 'г', 'д', 'з', 'ж', 'h', 'z', 'j', 'g'}

        # парные по звонкости согласные
        self.pair_consonants = {'б', 'в', 'г', 'д', 'ж', 'з', 'к', 'п', 'с', 'т', 'ф', 'ш', 'h', 'х',
                                'z', 'ц', 'j', 'ч', 'g', 'щ'}

        # непарные по звонкости согласные
        self.nonpair_consonants = {'й', 'м', 'н', 'р', 'л', 'ц', 'ч', 'х', 'щ'}

        self.hardsoft_consonants = {'б', 'в', 'г', 'д', 'з', 'к', 'л', 'м', 'н', 'п', 'р', 'с', 'т', 'ф', 'h', 'х',
                                    'z', 'j', 'z'}
        self.hard_consonants = {'ж', 'ш', 'ц', 'j'}
        self.soft_consonants = {'й', 'ч', 'щ', 'g'}


class Rule27:
    def __init__(self):
        self.mode = dict(
            Classic=self.rule_27_classic,
            Modern=self.rule_27_modern
        )

    def rule_27_classic(self, letters_list: list, next_phoneme: str, cur_pos: int) -> str:
        letters_for_rule_27 = {'н', 'т', 'с', 'д', 'з', 'л', 'м', 'п', 'б', 'в', 'ф'}
        gen_vocals_soft = {'ь', 'я', 'ё', 'ю', 'е', 'и', 'я+', 'ё+', 'ю+', 'е+', 'и+'}
        n = len(letters_list)
        if cur_pos < n - 2 and letters_list[cur_pos] in {'н', 'т', 'с', 'д', 'з'} and \
                letters_list[cur_pos + 1] in letters_for_rule_27 and \
                letters_list[cur_pos + 2] in gen_vocals_soft:
            case = 'n_soft'
        elif letters_list[cur_pos] == 'н' and letters_list[cur_pos + 1] in {'ч', 'щ'}:
            case = 'n_soft'
        else:
            case = ''
        return case

    def rule_27_modern(self, letters_list: list, next_phoneme: str, cur_pos: int) -> str:
        n = len(letters_list)
        case = ''
        if letters_list[cur_pos] == 'н':
            if next_phoneme in {'J0', 'TSH0', 'SH0', 'DZH0', 'ZH0', 'D0', 'T0', 'Z0', 'C0'}:
                case = 'n_soft'
        elif letters_list[cur_pos] in {'с', 'з'}:
            if next_phoneme in {'N0', 'D0', 'T0', 'Z0', 'C0'}:
                case = 'n_soft'
        return case


class TableG2P:
    def __init__(self):
        self.mode1 = dict(
            Classic={
                    'й': Consonant('J0', 'J0', 'J0', 'J0', 'J0', 'J0'),

                    'л': Consonant('L', 'L', 'L', 'L0', 'L0', 'L0'),
                    'м': Consonant('M', 'M', 'M', 'M0', 'M0', 'M0'),
                    'н': Consonant('N', 'N', 'N', 'N0', 'N0', 'N0'),
                    'р': Consonant('R', 'R', 'R', 'R0', 'R0', 'R0'),

                    'б': Consonant('B', 'P', 'B', 'B0', 'P0', 'B0'),
                    'п': Consonant('P', 'P', 'B', 'P0', 'P0', 'B0'),
                    'в': Consonant('V', 'F', 'V', 'V0', 'F0', 'V0'),
                    'ф': Consonant('F', 'F', 'V', 'F0', 'F0', 'V0'),
                    'г': Consonant('G', 'K', 'G', 'G0', 'K0', 'G0'),
                    'к': Consonant('K', 'K', 'G', 'K0', 'K0', 'G0'),
                    'д': Consonant('D', 'T', 'D', 'D0', 'T0', 'D0'),
                    'т': Consonant('T', 'T', 'D', 'T0', 'T0', 'D0'),
                    'з': Consonant('Z', 'S', 'Z', 'Z0', 'S0', 'Z0'),
                    'с': Consonant('S', 'S', 'Z', 'S0', 'S0', 'Z0'),
                    'ж': Consonant('ZH', 'SH', 'ZH', 'ZH', 'SH', 'ZH'),
                    'ш': Consonant('SH', 'SH', 'ZH', 'SH', 'SH', 'ZH'),
                    'h': Consonant('GH', 'KH', 'GH', 'GH0', 'KH0', 'GH0'),  # боh, аhа, буhалтер
                    'х': Consonant('KH', 'KH', 'GH', 'KH0', 'KH0', 'GH0'),
                    'z': Consonant('DZ', 'TS', 'DZ', 'DZ0', 'TS0', 'DZ0'),  # zета, гоzилла
                    'ц': Consonant('TS', 'TS', 'DZ', 'TS', 'TS', 'DZ'),
                    'j': Consonant('DZH', 'TSH', 'DZH', 'DZH', 'TSH', 'DZH'),  # маjонг, лоjия
                    'ч': Consonant('TSH0', 'TSH0', 'DZH0', 'TSH0', 'TSH0', 'DZH0'),
                    'g': Consonant('ZH0', 'SH0', 'ZH0', 'ZH0', 'SH0', 'ZH0'),  # доggи
                    'щ': Consonant('SH0', 'SH0', 'ZH0', 'SH0', 'SH0', 'ZH0'),

                    # считаем, что J0 уже добавили, где нужно
                    'ё+': Vocal('O0', 'O0', 'O0', 'O0', 'O0', 'O0', 'O0', 'O0'),
                    'ю+': Vocal('U0', 'U0', 'U0', 'U0', 'U0', 'U0', 'U0', 'U0'),
                    'я+': Vocal('A0', 'A0', 'A0', 'A0', 'A0', 'A0', 'A0', 'A0'),
                    'е+': Vocal('E0', 'E0', 'E0', 'E0', 'E0', 'E0', 'E0', 'E0'),

                    'о+': Vocal('O0', 'O0', 'O0', 'O0', 'O0', 'O0', 'O0', 'O0'),
                    'у+': Vocal('U0', 'U0', 'U0', 'U0', 'U0', 'U0', 'U0', 'U0'),
                    'а+': Vocal('A0', 'A0', 'A0', 'A0', 'A0', 'A0', 'A0', 'A0'),
                    'э+': Vocal('E0', 'E0', 'E0', 'E0', 'E0', 'E0', 'E0', 'E0'),
                    'ы+': Vocal('Y0', 'Y0', 'Y0', 'Y0', 'Y0', 'Y0', 'Y0', 'Y0'),
                    'и+': Vocal('I0', 'I0', 'I0', 'I0', 'Y0', 'Y0', 'I0', 'I0'),

                    'ё': Vocal('O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'),
                    'ю': Vocal('U', 'U', 'U', 'U', 'U', 'U', 'U', 'U'),
                    'я': Vocal('A', 'I', 'A', 'I', 'A', 'Y', 'A', 'I'),
                    'е': Vocal('I', 'I', 'I', 'I', 'Y', 'Y', 'I', 'I'),

                    'о': Vocal('A', 'A', 'A', 'I', 'A', 'A', 'A', 'A'),
                    'у': Vocal('U', 'U', 'U', 'U', 'U', 'U', 'U', 'U'),
                    'а': Vocal('A', 'A', 'A', 'I', 'A', 'A', 'A', 'A'),
                    'э': Vocal('Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y'),
                    'ы': Vocal('Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y'),
                    'и': Vocal('I', 'I', 'I', 'I', 'Y', 'Y', 'I', 'I')
            },
            Modern={
                    'й': Consonant('J0', 'J0', 'J0', 'J0', 'J0', 'J0'),

                    'л': Consonant('L', 'L', 'L', 'L0', 'L0', 'L0'),
                    'м': Consonant('M', 'M', 'M', 'M0', 'M0', 'M0'),
                    'н': Consonant('N', 'N', 'N', 'N0', 'N0', 'N0'),
                    'р': Consonant('R', 'R', 'R', 'R0', 'R0', 'R0'),

                    'б': Consonant('B', 'P', 'B', 'B0', 'P0', 'B0'),
                    'п': Consonant('P', 'P', 'B', 'P0', 'P0', 'B0'),
                    'в': Consonant('V', 'F', 'V', 'V0', 'F0', 'V0'),
                    'ф': Consonant('F', 'F', 'V', 'F0', 'F0', 'V0'),
                    'г': Consonant('G', 'K', 'G', 'G0', 'K0', 'G0'),
                    'к': Consonant('K', 'K', 'G', 'K0', 'K0', 'G0'),
                    'д': Consonant('D', 'T', 'D', 'D0', 'T0', 'D0'),
                    'т': Consonant('T', 'T', 'D', 'T0', 'T0', 'D0'),
                    'з': Consonant('Z', 'S', 'Z', 'Z0', 'S0', 'Z0'),
                    'с': Consonant('S', 'S', 'Z', 'S0', 'S0', 'Z0'),
                    'ж': Consonant('ZH', 'SH', 'ZH', 'ZH', 'SH', 'ZH'),
                    'ш': Consonant('SH', 'SH', 'ZH', 'SH', 'SH', 'ZH'),
                    'h': Consonant('GH', 'KH', 'GH', 'GH0', 'KH0', 'GH0'),  # боh, аhа, буhалтер
                    'х': Consonant('KH', 'KH', 'GH', 'KH0', 'KH0', 'GH0'),
                    'z': Consonant('DZ', 'TS', 'DZ', 'DZ0', 'TS0', 'DZ0'),  # zета, гоzилла
                    'ц': Consonant('TS', 'TS', 'DZ', 'TS', 'TS', 'DZ'),
                    'j': Consonant('DZH', 'TSH', 'DZH', 'DZH', 'TSH', 'DZH'),  # маjонг, лоjия
                    'ч': Consonant('TSH0', 'TSH0', 'DZH0', 'TSH0', 'TSH0', 'DZH0'),
                    'g': Consonant('ZH0', 'SH0', 'ZH0', 'ZH0', 'SH0', 'ZH0'),  # доggи
                    'щ': Consonant('SH0', 'SH0', 'ZH0', 'SH0', 'SH0', 'ZH0'),

                    # считаем, что J0 уже добавили, где нужно
                    'ё+': Vocal('O0', 'O0', 'O0', 'O0', 'O0', 'O0', 'O0', 'O0'),
                    'ю+': Vocal('U0', 'U0', 'U0', 'U0', 'U0', 'U0', 'U0', 'U0'),
                    'я+': Vocal('A0', 'A0', 'A0', 'A0', 'A0', 'A0', 'A0', 'A0'),
                    'е+': Vocal('E0', 'E0', 'E0', 'E0', 'E0', 'E0', 'E0', 'E0'),

                    'о+': Vocal('O0', 'O0', 'O0', 'O0', 'O0', 'O0', 'O0', 'O0'),
                    'у+': Vocal('U0', 'U0', 'U0', 'U0', 'U0', 'U0', 'U0', 'U0'),
                    'а+': Vocal('A0', 'A0', 'A0', 'A0', 'A0', 'A0', 'A0', 'A0'),
                    'э+': Vocal('E0', 'E0', 'E0', 'E0', 'E0', 'E0', 'E0', 'E0'),
                    'ы+': Vocal('Y0', 'Y0', 'Y0', 'Y0', 'Y0', 'Y0', 'Y0', 'Y0'),
                    'и+': Vocal('I0', 'I0', 'I0', 'I0', 'Y0', 'Y0', 'I0', 'I0'),

                    'ё': Vocal('O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'),
                    'ю': Vocal('U', 'U', 'U', 'U', 'U', 'U', 'U', 'U'),
                    'я': Vocal('A', 'I', 'A', 'I', 'A', 'Y', 'A', 'I'),
                    'е': Vocal('I', 'I', 'I', 'I', 'Y', 'Y', 'I', 'I'),

                    'о': Vocal('A', 'A', 'A', 'I', 'A', 'A', 'A', 'A'),
                    'у': Vocal('U', 'U', 'U', 'U', 'U', 'U', 'U', 'U'),
                    'а': Vocal('A', 'A', 'A', 'I', 'A', 'A', 'A', 'A'),
                    'э': Vocal('Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y'),
                    'ы': Vocal('Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y'),
                    'и': Vocal('I', 'I', 'I', 'I', 'Y', 'Y', 'I', 'I')
            }
        )


class RulesForGraphemes(Phonetics, TableG2P, Rule27):
    def __init__(self, users_mode: str):
        Phonetics.__init__(self)
        TableG2P.__init__(self)
        Rule27.__init__(self)
        self.users_mode = users_mode

    def apply_rule_for_vocals(self, letters_list: list, cur_pos: int) -> tuple:
        new_phonemes_list = list()
        case = 0
        if (cur_pos == 0) or (letters_list[cur_pos - 1] in self.vocals | self.hard_and_soft_signs) \
                or (letters_list[cur_pos - 1] not in self.all_russian_letters):
            if letters_list[cur_pos] in self.double_vocals:
                new_phonemes_list.append('J0')
            if cur_pos + 1 >= len(letters_list):
                case = 1
            else:
                case = 2
        elif letters_list[cur_pos - 1] in self.soft_consonants:
            if cur_pos + 1 >= len(letters_list):
                case = 3
            else:
                case = 4
        elif letters_list[cur_pos - 1] in self.hard_consonants:
            if cur_pos + 1 >= len(letters_list):
                case = 5
            else:
                case = 6
        elif letters_list[cur_pos - 1] in self.hardsoft_consonants:
            if cur_pos + 1 >= len(letters_list):
                case = 7
            else:
                case = 8
        else:
            assert 0 == 1, "Incorrect word! " + ''.join(letters_list)
        new_phonemes_list.append(self.mode1[self.users_mode][letters_list[cur_pos]].forms['case' + str(case)])
        return new_phonemes_list, cur_pos - 1

    def apply_rule_for_consonants(self, letters_list: list, next_phoneme: str, cur_pos: int) -> tuple:
        new_phonemes_list = list()
        n = len(letters_list)
        if cur_pos == n - 1:
            case = 'd_hard'
        else:
            case = self.mode[self.users_mode](letters_list, next_phoneme, cur_pos)
            if len(case) > 0:
                pass
            elif letters_list[cur_pos + 1] == 'ь':
                if next_phoneme == '':
                    case = 'd_soft'
                else:
                    if cur_pos < n - 2 and letters_list[cur_pos + 2] == 'ъ':
                        case = 'd_soft'
                    elif next_phoneme in self.deaf_phonemes:
                        case = 'd_soft'
                    elif next_phoneme in self.vocals_phonemes:
                        case = 'd_soft'
                    elif next_phoneme in self.voiced_weak_phonemes:
                        case = 'n_soft'
                    elif next_phoneme in self.voiced_strong_phonemes:
                        case = 'v_soft'
                    else:
                        assert 0 == 1, "Incorrect word! " + letters_list[cur_pos]
            elif letters_list[cur_pos + 1] == 'ъ':
                if next_phoneme == '':
                    case = 'd_hard'
                else:
                    if cur_pos < n - 2 and letters_list[cur_pos + 2] == 'ъ':
                        case = 'd_hard'
                    elif next_phoneme in self.deaf_phonemes:
                        case = 'd_hard'
                    elif next_phoneme in self.vocals_phonemes:
                        case = 'd_hard'
                    elif next_phoneme in self.voiced_weak_phonemes:
                        case = 'n_hard'
                    elif next_phoneme in self.voiced_strong_phonemes:
                        case = 'v_hard'
                    else:
                        assert 0 == 1, "Incorrect word! " + letters_list[cur_pos]
            elif next_phoneme in self.deaf_phonemes:
                case = 'd_hard'
            elif next_phoneme in self.voiced_weak_phonemes:
                case = 'n_hard'
            elif next_phoneme in self.voiced_strong_phonemes:
                case = 'v_hard'
            elif letters_list[cur_pos + 1] in self.gen_vocals_soft - {'ь'}:
                case = 'n_soft'
            elif letters_list[cur_pos + 1] in self.gen_vocals_hard - {'ъ'}:
                case = 'n_hard'
            else:
                assert 0 == 1, "Incorrect word! " + ''.join(letters_list)
        new_phonemes_list.append(self.mode1[self.users_mode][letters_list[cur_pos]].forms[case])
        return new_phonemes_list, cur_pos - 1
