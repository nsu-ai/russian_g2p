import codecs
import os
import re
import sys

import nltk
from rnnmorph.predictor import RNNMorphPredictor

from russian_g2p.Accentor import Accentor


VOWEL_LETTERS = {'а', 'о', 'у', 'э', 'ы', 'и', 'я', 'ё', 'ю', 'е'}


def get_all_prompts(init_dir_name: str) -> list:
    all_subdirs = list()
    all_prompts = set()
    re_for_filename = re.compile(r'ru\_?\d+$')
    for cur_file_name in filter(lambda cur_name: cur_name not in {'.', '..'}, os.listdir(init_dir_name)):
        full_name = os.path.join(init_dir_name, cur_file_name)
        if cur_file_name.lower().startswith('prompts-original'):
            sentences = list()
            line_ind = 1
            with codecs.open(full_name, mode='r', encoding='utf-8', errors='ignore') as fp:
                cur_line = fp.readline()
                while len(cur_line):
                    prepared_line = cur_line.strip()
                    if len(prepared_line):
                        err_msg = 'File `{0}`, line {1}: this line is wrong!'.format(full_name, line_ind)
                        words = prepared_line.split()
                        assert len(words) > 1, err_msg
                        search_res = re_for_filename.search(words[0].lower())
                        assert search_res is not None, err_msg
                        assert (search_res.start() >= 0) and (search_res.end() > 0), err_msg
                        new_sentence = ' '.join(words[1:])
                        assert len(new_sentence) > 0, err_msg
                        sentences.append(new_sentence)
                    cur_line = fp.readline()
                    line_ind += 1
            assert len(sentences) > 0, '`{0}`: this file does not contain sentences!'.format(full_name)
            all_prompts |= set(sentences)
        elif os.path.isdir(full_name):
            all_subdirs.append(full_name)
    if len(all_subdirs) > 0:
        for cur_subdir in all_subdirs:
            all_prompts |= get_all_prompts(cur_subdir)
    return all_prompts


def select_subsentences(source_prompt: str) -> list:
    all_subsentences = list()
    new_subsentence = list()
    for cur_token in nltk.tokenize.word_tokenize(source_prompt):
        if not cur_token.isalnum():
            if len(new_subsentence):
                all_subsentences.append(new_subsentence)
            else:
                new_subsentence.clear()
        else:
            new_subsentence.append(cur_token)
    if len(new_subsentence):
        all_subsentences.append(new_subsentence)
    return all_subsentences


def main():
    if sys.argv.__len__() > 1:
        init_dir_name = os.path.normpath(sys.argv[1])
        assert os.path.isdir(init_dir_name), 'Directory `{0}` does not exist!'.format(init_dir_name)
        all_prompts = sorted(list(get_all_prompts(init_dir_name)))
        accentor = Accentor()
        morpho_predictor = RNNMorphPredictor()
        i = 0
        for cur_prompt in all_prompts[:100]:
            trouble = False
            unknown_words = []
            for cur_subsentence in select_subsentences(cur_prompt):
                morphotags = ['{0} {1}'.format(cur_morpho.pos, cur_morpho.tag)
                              for cur_morpho in morpho_predictor.predict_sentence_tags(cur_subsentence)]
                accent_variants = accentor.do_accents(cur_subsentence, morphotags)
                if len(accent_variants) > 1:
                    trouble = True
                else:
                    accented_phrase = accent_variants[0]
                    for cur_word in accented_phrase:
                        vowels_counter = 0
                        for cur_char in cur_word.lower():
                            if cur_char in VOWEL_LETTERS:
                                vowels_counter += 1
                        if '+' not in cur_word and vowels_counter > 1:
                            unknown_words += [cur_word]
            if trouble:
                print('`{0}`: this phrase cannot be unambiguously accented!'.format(cur_prompt))
                i += 1
            if unknown_words:
                for unknown_word in list(set(unknown_words)):
                    print('`{0}`: word `{1}` in this this phrase is unknown!'.format(cur_prompt, unknown_word))
        print(i)
    else:
        print("Usage: input_directory_with_voxforge_ru")


if __name__ == '__main__':
    main()
