import importlib


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

        self.russian_phonemes_set = self.vocals_phonemes | self.voiced_weak_phonemes |\
                                    self.voiced_strong_phonemes | self.deaf_phonemes | {'sil'}

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


class RulesForGraphemes:
    def __init__(self, users_mode: str='Modern'):
        if users_mode == 'Modern':
            from russian_g2p.modes.Modern import ModernMode as UsersMode
        elif users_mode == 'Classic':
            from russian_g2p.modes.Classic import ClassicMode as UsersMode

        self.mode = UsersMode()

    def apply_rule_for_vocals(self, letters_list: list, cur_pos: int) -> list:
        new_phonemes_list = list()
        case = 0
        if (cur_pos == 0) or (letters_list[cur_pos - 1] in self.mode.vocals | self.mode.hard_and_soft_signs) \
                or (letters_list[cur_pos - 1] not in self.mode.all_russian_letters):
            if letters_list[cur_pos] in self.mode.double_vocals:
                new_phonemes_list.append('J0')
            if cur_pos + 1 >= len(letters_list):
                case = 1
            else:
                case = 2
        elif letters_list[cur_pos - 1] in self.mode.soft_consonants:
            if cur_pos + 1 >= len(letters_list):
                case = 3
            else:
                case = 4
        elif letters_list[cur_pos - 1] in self.mode.hard_consonants:
            if cur_pos + 1 >= len(letters_list):
                case = 5
            else:
                case = 6
        elif letters_list[cur_pos - 1] in self.mode.hardsoft_consonants:
            if cur_pos + 1 >= len(letters_list):
                case = 7
            else:
                case = 8
        else:
            assert 0 == 1, "Incorrect word! " + ''.join(letters_list)
        new_phonemes_list.append(self.mode.TableG2P[letters_list[cur_pos]].forms['case' + str(case)])
        return new_phonemes_list

    def apply_rule_for_consonants(self, letters_list: list, next_phoneme: str, cur_pos: int) -> list:
        new_phonemes_list = list()
        n = len(letters_list)
        # твердость / мягкость
        if cur_pos < n - 1 and letters_list[cur_pos + 1] in self.mode.gen_vocals_soft:
            hardsoft = 'soft'
        else:
            hardsoft = 'hard'
        if letters_list[-1] in self.mode.hard_and_soft_signs:
            n -= 1
        # конец слова
        if cur_pos == n - 1:
            if next_phoneme == 'sil':
                voice = 'd'
            elif next_phoneme in self.mode.deaf_phonemes:
                voice = 'd'
            elif next_phoneme in self.mode.voiced_weak_phonemes:
                voice = 'd'
            elif next_phoneme in self.mode.voiced_strong_phonemes:
                voice = 'v'
            elif next_phoneme in self.mode.vocals_phonemes:
                voice = 'd'
            else:
                voice = ''
                assert 0 == 1, "Incorrect word! " + ' '.join(letters_list)
            case = voice + '_' + hardsoft
        # внутри слова
        else:
            case = self.mode.rule_27(letters_list, next_phoneme, cur_pos)
            if len(case) == 0:
                if next_phoneme == 'sil':
                    voice = ''
                    assert 0 == 1, "Incorrect word! " + ' '.join(letters_list)
                elif next_phoneme in self.mode.deaf_phonemes:
                    voice = 'd'
                elif next_phoneme in self.mode.voiced_weak_phonemes:
                    voice = 'n'
                elif next_phoneme in self.mode.voiced_strong_phonemes:
                    voice = 'v'
                elif next_phoneme in self.mode.vocals_phonemes:
                    voice = 'n'
                else:
                    voice = ''
                    assert 0 == 1, "Incorrect word! " + ' '.join(letters_list)
                case = voice + '_' + hardsoft
        new_phonemes_list.append(self.mode.TableG2P[letters_list[cur_pos]].forms[case])
        return new_phonemes_list
