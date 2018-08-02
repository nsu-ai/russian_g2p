from russian_g2p.modes.Phonetics import Consonant, Vocal, Phonetics


class ClassicMode(Phonetics):
    def __init__(self):
        Phonetics.__init__(self)
        self.TableG2P = {
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

            'h': Consonant('GH', 'KH', 'GH', 'GH0', 'KH0', 'GH0'),  # боh, аhа, буhалтер
            'х': Consonant('KH', 'KH', 'GH', 'KH0', 'KH0', 'GH0'),

            'д': Consonant('D', 'T', 'D', 'D0', 'T0', 'D0'),
            'т': Consonant('T', 'T', 'D', 'T0', 'T0', 'D0'),

            'з': Consonant('Z', 'S', 'Z', 'Z0', 'S0', 'Z0'),
            'с': Consonant('S', 'S', 'Z', 'S0', 'S0', 'Z0'),

            'ж': Consonant('ZH', 'SH', 'ZH', 'ZH', 'SH', 'ZH'),
            'ш': Consonant('SH', 'SH', 'ZH', 'SH', 'SH', 'ZH'),

            'z': Consonant('DZ', 'TS', 'DZ', 'DZ', 'TS', 'DZ'),  # zета, Zагоев
            'ц': Consonant('TS', 'TS', 'DZ', 'TS', 'TS', 'DZ'),

            'j': Consonant('DZH0', 'TSH0', 'DZH0', 'DZH0', 'TSH0', 'DZH0'),
            'ч': Consonant('TSH0', 'TSH0', 'DZH0', 'TSH0', 'TSH0', 'DZH0'),

            'g': Consonant('ZH0', 'SH0', 'ZH0', 'ZH0', 'SH0', 'ZH0'),  # доggи, приеggать
            'щ': Consonant('SH0', 'SH0', 'ZH0', 'SH0', 'SH0', 'ZH0'),

            'd': Consonant('DZ0', 'TS0', 'DZ0', 'DZ0', 'TS0', 'DZ0'),  # Dюба
            't': Consonant('TS0', 'TS0', 'DZ0', 'TS0', 'TS0', 'DZ0'),

            'x': Consonant('DZH', 'TSH', 'DZH', 'DZH', 'TSH', 'DZH'),  # маxонг, лоxия
            's': Consonant('TSH', 'TSH', 'DZH', 'TSH', 'TSH', 'DZH'),  # поsтанники

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

    def rule_27(self, letters_list: list, next_phoneme: str, cur_pos: int) -> str:
        case = ''
        if letters_list[cur_pos] == 'н':
            if next_phoneme in {'J0', 'TSH0', 'SH0', 'DZH0', 'ZH0', 'D0', 'T0', 'Z0', 'S0', 'L0', 'M0', 'P0', 'B0', 'V0', 'F0', 'N0'}:
                case = 'n_soft'
        elif letters_list[cur_pos] in {'т', 'с', 'д', 'з', 'п', 'б', 'в', 'ф'}:
            if next_phoneme in {'D0', 'Z0', 'B0'}:
                case = 'v_soft'
            elif next_phoneme in {'T0', 'S0', 'P0'}:
                case = 'd_soft'
            elif next_phoneme in {'N0', 'L0', 'M0', 'V0', 'F0'}:
                case = 'n_soft'
        return case
