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


class RulesForGraphemes:
    def __init__(self):
        self.cons = {
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
            'h': Consonant('GH', 'KH', 'GH', 'GH0', 'KH0', 'GH0'),
            'х': Consonant('KH', 'KH', 'GH', 'KH0', 'KH0', 'GH0'),
            'z': Consonant('DS', 'TS', 'DZ', 'DS', 'TS', 'DZ'),
            'ц': Consonant('TS', 'TS', 'DZ', 'TS', 'TS', 'DZ'),
            'j': Consonant('DZH0', 'TSH0', 'DZH0', 'DZH0', 'TSH0', 'DZH0'),
            'ч': Consonant('TSH0', 'TSH0', 'DZH0', 'TSH0', 'TSH0', 'DZH0'),
            'g': Consonant('ZH0', 'SH0', 'ZH0', 'ZH0', 'SH0', 'ZH0'),
            'щ': Consonant('SH0', 'SH0', 'ZH0', 'SH0', 'SH0', 'ZH0')
        }

        self.vocs = {
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
            'и': Vocal('I', 'I', 'I', 'I', 'Y', 'Y', 'I', 'I')}
