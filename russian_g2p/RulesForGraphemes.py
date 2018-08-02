class RulesForGraphemes:
    def __init__(self, users_mode: str='Modern'):
        if users_mode == 'Classic':
            from russian_g2p.modes.Classic import ClassicMode as UsersMode
        else:
            from russian_g2p.modes.Modern import ModernMode as UsersMode

        self.mode = UsersMode()

    def apply_rule_for_vocals(self, letters_list: list, cur_pos: int) -> list:
        new_phonemes_list = list()
        case = 0
        if cur_pos == 0:
            if letters_list[cur_pos] in self.mode.double_vocals:
                new_phonemes_list.append('J0')
            if cur_pos + 1 >= len(letters_list):
                case = 1
            else:
                case = 2
        elif letters_list[cur_pos - 1] in self.mode.hard_and_soft_signs:
            if letters_list[cur_pos] in self.mode.gen_vocals_soft | {'о', 'о+'}:
                new_phonemes_list.append('J0')
            if cur_pos + 1 >= len(letters_list):
                case = 1
            else:
                case = 2
        elif letters_list[cur_pos - 1] in self.mode.vocals:
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
