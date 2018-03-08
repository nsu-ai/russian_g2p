import codecs
import copy
import os
import re
import warnings

from russian_g2p.RulesForGraphemes import RulesForGraphemes


class Grapheme2Phoneme(RulesForGraphemes):
    def __init__(self, users_mode='Modern'):
        RulesForGraphemes.__init__(self, users_mode)

        self.__re_for_phrase_split = None

        self.__silence_name = 'sil'

        self.__function_words_1 = {'без', 'безо', 'близ', 'в', 'во', 'вне', 'для', 'до', 'за', 'из', 'изо', 'к', 'ко',
                                   'меж', 'на', 'над', 'о', 'об', 'обо', 'от', 'ото', 'по', 'под', 'подо', 'пред',
                                   'предо', 'при', 'про', 'с', 'со', 'у', 'чрез', 'через', 'не', 'ни', 'из-за',
                                   'из-подо', 'из-под', 'а-ля', 'по-над', 'по-за'}
        self.__function_words_2 = {'бы', 'б', 'де', 'ли', 'же', '-то', '-ка', '-либо', '-нибудь', '-таки'}

        self.__exclusions_dictionary = None
        exclusions_dictionary_name = os.path.join(os.path.dirname(__file__), 'data', 'Phonetic_Exclusions.txt')
        assert os.path.isfile(exclusions_dictionary_name), \
            'File `{0}` does not exist!'.format(exclusions_dictionary_name)
        self.__exclusions_dictionary = self.load_exclusions_dictionary(exclusions_dictionary_name)
        self.__re_for_phrase_split = re.compile(r'[\s\-]+', re.U)

    @property
    def russian_letters(self) -> list:
        return sorted(list(self.all_russian_letters))

    @property
    def russian_phonemes(self) -> list:
        return sorted(list(self.russian_phonemes_set))

    @property
    def silence_name(self) -> str:
        return self.__silence_name

    def load_exclusions_dictionary(self, file_name: str) -> dict:
        words_and_transcriptions = dict()
        with codecs.open(file_name, mode='r', encoding='utf-8', errors='ignore') as dictionary_file:
            cur_line = dictionary_file.readline()
            cur_line_index = 1
            while len(cur_line):
                error_message = "File `{0}`, line {1}: description of this word and its transcription is " \
                                "incorrect!".format(file_name, cur_line_index)
                prepared_line = cur_line.strip()
                if len(prepared_line):
                    words_of_line = prepared_line.split()
                    nwords = len(words_of_line)
                    assert nwords >= 2, error_message
                    word_name = words_of_line[0].lower()
                    assert any([c in (self.all_russian_letters | {'-', '+'}) for c in word_name]), error_message
                    assert word_name not in words_and_transcriptions, error_message
                    word_transcription = list()
                    for cur_phoneme in words_of_line[1:]:
                        prepared_phoneme = cur_phoneme.upper()
                        # переписать исключения
                        # assert prepared_phoneme in self.__russian_phonemes_set, error_message
                        word_transcription.append(prepared_phoneme)
                    words_and_transcriptions[word_name] = copy.copy(word_transcription)
                cur_line = dictionary_file.readline()
                cur_line_index += 1
        assert len(words_and_transcriptions) > 0, \
            "File `{0}`: there are no words and their transcriptions!".format(file_name)
        return words_and_transcriptions

    def check_word(self, checked_word: str):
        assert len(checked_word) > 0, 'Checked word is empty string!'
        assert all([c in (self.all_russian_letters | {'+', '-'}) for c in checked_word.lower()]), \
            '`{0}`: this word contains inadmissible characters!'.format(checked_word)
        assert len(list(filter(lambda c: c in self.all_russian_letters, checked_word.lower()))) > 0, \
            '`{0}`: this word is incorrect!'.format(checked_word)

    def check_phrase(self, checked_phrase: str):
        assert len(checked_phrase) > 0, 'Checked phrase is empty string!'
        assert all([c in (self.all_russian_letters | {' ', '+', '-'} | {'s', 'i', 'l'})
                    for c in checked_phrase.lower()]), \
            '`{0}`: this phrase contains inadmissible characters!'.format(checked_phrase)
        for cur_word in self.__re_for_phrase_split.split(checked_phrase.lower()):
            assert (len(list(filter(lambda c: c in self.all_russian_letters, cur_word))) > 0) \
                   or (cur_word.lower() == 'sil'), '`{0}`: this phrase is incorrect!'.format(checked_phrase)

    def word_to_phonemes(self, source_word: str) -> list:
        self.check_word(source_word)
        error_message = '`{0}`: this word is incorrect!'.format(source_word)
        prepared_word = source_word.lower()
        if prepared_word in self.__exclusions_dictionary:
            return self.__exclusions_dictionary[prepared_word]
        if '+' not in prepared_word:
            counter = len(prepared_word) - len(re.sub(r'[аоуэыияёею]', '', prepared_word))
            if counter > 1:
                warnings.warn('`{0}`: the accent for this word is unknown!'.format(source_word))
        if prepared_word in self.__exclusions_dictionary:
            return self.__exclusions_dictionary[prepared_word]
        if '\'' in prepared_word:
            prepared_word = prepared_word.replace('\'', '')
        if '-' in prepared_word:
            if (not self.in_function_words_1(prepared_word)) and (not self.in_function_words_2(prepared_word)):
                word_parts = list(filter(lambda a: len(a) > 0, map(lambda b: b.strip(), prepared_word.split('-'))))
                assert len(word_parts) > 0, error_message
                prepared_word_parts = [word_parts[0]]
                for cur_part in word_parts[1:]:
                    if self.in_function_words_1('-' + cur_part) or self.in_function_words_2('-' + cur_part):
                        prepared_word_parts.append('-' + cur_part)
                    else:
                        prepared_word_parts.append(cur_part)
                return self.phrase_to_phonemes(' '.join(prepared_word_parts))
            prepared_word = self.__remove_character(prepared_word, '-')
        letters_list = self.__word_to_letters_list(self.__prepare_word(prepared_word))
        n = len(letters_list)
        assert n > 0, error_message
        ind = n - 1
        next_phoneme = ''
        # начинаем формировать транскрипцию
        transcription = list()
        while ind >= 0:
            if ind > 0 and letters_list[ind] in self.hard_and_soft_signs:
                ind -= 1
                continue
            old_ind = ind
            if letters_list[ind] in self.vocals:
                new_phonemes, ind = self.apply_rule_for_vocals(letters_list, ind)
            else:
                assert letters_list[ind] in self.consonants, error_message
                new_phonemes, ind = self.apply_rule_for_consonants(letters_list, next_phoneme, ind)
            transcription = new_phonemes + transcription
            next_phoneme = new_phonemes[0]
            # assert ind <= old_ind, error_message # ?
        assert len(transcription) > 0, '`{0}`: this word cannot be transcribed!'.format(source_word)
        return self.__remove_repeats_from_transcription(transcription)

    def phrase_to_phonemes(self, source_phrase: str) -> list:
        error_message = '`{0}`: this phrase is incorrect!'.format(source_phrase)
        words_in_phrase = list()
        source_phrase = source_phrase.lower()
        source_phrase = source_phrase.replace('\'', '')
        source_phrase = source_phrase.replace('-', ' ')
        #self.check_phrase(source_phrase)
        words_in_phrase = source_phrase.split()
        l = len(words_in_phrase)
        long_word = words_in_phrase[0]
        for i in range(1, l):
            if words_in_phrase[i][0] in self.gen_vocals_soft:
                if words_in_phrase[i][0] == 'и' and long_word[-1] in self.consonants | {'ъ'} - {'й', 'ь'}:
                    words_in_phrase[i] = 'ы' + words_in_phrase[i][1:]
                if words_in_phrase[i - 1].replace('+', '') in self.__function_words_1 | self.__function_words_2:
                    if words_in_phrase[i][0] in self.double_vocals:
                        long_word += 'ъ'
                    else:
                        long_word += ''
                else:
                    long_word += 'ъъ'
            elif words_in_phrase[i][0] in self.gen_vocals_hard:
                long_word += ''
            elif words_in_phrase[i][0] in self.deaf_consonants:
                long_word += 'ъ'
            elif words_in_phrase[i][0] in self.voiced_weak_consonants:
                long_word += 'ъ'
            elif words_in_phrase[i][0] in self.voiced_strong_consonants:
                long_word += ''
            else:
                assert 0 == 1, "Incorrect word! " + words_in_phrase[i]
            long_word += words_in_phrase[i]
        phrase_transcription = self.word_to_phonemes(long_word)
        return phrase_transcription

    def in_function_words_1(self, source_word: str) -> bool:
        return self.__remove_character(source_word, '+').lower() in self.__function_words_1

    def in_function_words_2(self, source_word: str) -> bool:
        return self.__remove_character(source_word, '+').lower() in self.__function_words_2

    def __remove_character(self, source_word: str, removed_char: str) -> str:
        return ''.join(list(filter(lambda a: a != removed_char, source_word.lower())))

    def __prepare_word(self, cur_word: str) -> str:
        # правила 21-24
        prepared_word = cur_word.lower().strip()
        # добавить для других дифтонгов
        replace_pairs = [('стн', 'сн'), ('стл', 'сл'), ('нтг', 'нг'), ('здн', 'зн'), ('здц', 'зц'),
                         ('ндц', 'нц'), ('рдц', 'рц'), ('ндш', 'нш'), ('гдт', 'гт'), ('лнц', 'нц'),
                         ('сч', 'щ'), ('жч', 'щ'), ('сш', 'ш'), ('зж', 'ж'),
                         ('тс', 'ц'), ('тьс', 'ц'), ('тц', 'ц'), ('дс', 'ц'), ('дц', 'ц'),
                         ('дз', 'z'), ('дж', 'j')]
        if len(prepared_word) > 2 and prepared_word[-2:] == 'го':
            prepared_word = prepared_word[:-2] + 'ва'
        for repl_from, repl_to in replace_pairs:
            prepared_word = prepared_word.replace(repl_from, repl_to)
        return prepared_word

    def __word_to_letters_list(self, cur_word: str) -> list:
        vocal_letters = set(filter(lambda letter: not letter.endswith('+'), self.vocals))
        error_message = "`{0}`: this word is incorrect!".format(cur_word)
        letters_list = list()
        new_letter = ''
        for ind in range(len(cur_word)):
            if cur_word[ind] == '+':
                assert new_letter in vocal_letters, error_message
                new_letter += cur_word[ind]
            else:
                assert cur_word[ind] in self.all_russian_letters, error_message
                if len(new_letter):
                    letters_list.append(new_letter)
                new_letter = cur_word[ind]
        if len(new_letter):
            letters_list.append(new_letter)
        del vocal_letters
        return letters_list

    def __remove_repeats_from_transcription(self, source_transcription: list) -> list:
        prepared_transcription = list()
        previous_phoneme = ''
        for current_phoneme in source_transcription:
            if re.sub(r'[0l]', '', current_phoneme) != re.sub(r'[0l]', '', previous_phoneme):
                prepared_transcription.append(current_phoneme)
            else:
                prepared_transcription[-1] = current_phoneme + 'l'
            previous_phoneme = current_phoneme
        return prepared_transcription

