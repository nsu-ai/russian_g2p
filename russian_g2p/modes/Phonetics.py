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
                                    'я', 'h', 'z', 'j', 'g', 'd', 't', 'x', 's'}

        self.hard_and_soft_signs = {'ъ', 'ь'}

        self.vocals = {'а', 'о', 'у', 'э', 'ы', 'и', 'я', 'ё', 'ю', 'е', 'а+', 'о+', 'у+', 'э+', 'ы+', 'и+', 'я+',
                       'ё+', 'ю+', 'е+'}

        self.double_vocals = {'е', 'ё', 'ю', 'я', 'е+', 'ё+', 'ю+', 'я+'}

        # назвать получше
        self.gen_vocals_hard = {'ъ', 'а', 'о', 'у', 'э', 'ы', 'а+', 'о+', 'у+', 'э+', 'ы+'}
        self.gen_vocals_soft = {'ь', 'я', 'ё', 'ю', 'е', 'и', 'я+', 'ё+', 'ю+', 'е+', 'и+'}

        self.consonants = {'б', 'в', 'г', 'д', 'ж', 'з', 'й', 'к', 'л', 'м', 'н', 'п', 'р', 'с', 'т', 'ф', 'х', 'ц',
                           'ч', 'ш', 'щ', 'h', 'z', 'j', 'g', 'd', 't', 'x', 's'}

        # парные по звонкости согласные
        self.pair_consonants = {'б', 'в', 'г', 'д', 'ж', 'з', 'к', 'п', 'с', 'т', 'ф', 'ш', 'h', 'х',
                                'z', 'ц', 'j', 'ч', 'g', 'щ'}

        self.hardsoft_consonants = {'б', 'в', 'г', 'д', 'з', 'к', 'л', 'м', 'н', 'п', 'р', 'с', 'т', 'ф', 'h', 'х'}
        self.hard_consonants = {'ж', 'ш', 'ц', 'x', 's', 'z'}
        self.soft_consonants = {'й', 'ч', 'щ', 'g', 'j', 'd', 't'}

