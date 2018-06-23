from argparse import ArgumentParser
import codecs
import os

import pymorphy2
from russian_tagsets import converters

from russian_g2p.Accentor import Accentor
from russian_g2p.Grapheme2Phoneme import Grapheme2Phoneme


def transcribe_words(source_words_list):
    n_words = len(source_words_list)
    n_parts = 100
    part_size = n_words // n_parts
    while (part_size * n_parts) < n_words:
        part_size += 1
    transcriptions = []
    bad_words = []
    to_ud2 = converters.converter('opencorpora-int', 'ud20')
    morph = pymorphy2.MorphAnalyzer()
    accentor = Accentor(exception_for_unknown=True, use_wiki=False)
    g2p = Grapheme2Phoneme(exception_for_nonaccented=True)
    russian_letters = set('АаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя')
    russian_consonants = set('БбВвГгДдЖжЗзЙйКкЛлМмНнПпРрСсТтФфХхЦцЧчШшЩщЪъЬь')
    part_counter = 0
    for word_idx in range(len(source_words_list)):
        cur_word = source_words_list[word_idx].strip().lower()
        err_msg = 'Word {0} is wrong!'.format(word_idx)
        assert len(cur_word) > 0, err_msg + ' It is empty!'
        assert set(cur_word) <= (russian_letters | {'-'}), \
            err_msg + ' "{0}" contains an inadmissible characters.'.format(cur_word)
        assert set(cur_word) != {'-'}, err_msg + ' It is empty!'
        if (len(cur_word) > 1) and (set(cur_word) <= russian_consonants):
            bad_words.append(cur_word)
        else:
            morpho_variants = set([to_ud2(str(it.tag)) for it in morph.parse(cur_word)])
            try:
                accentuation_variants = []
                for it in morpho_variants:
                    accentuation_variants += accentor.do_accents([[cur_word, it]])[0]
                variants_of_transcriptions = list(set(
                    filter(
                        lambda it2: len(it2) > 0,
                        map(
                            lambda it: tuple(g2p.word_to_phonemes(it)),
                            accentuation_variants
                        )
                    )
                ))
                if len(variants_of_transcriptions) > 0:
                    transcriptions.append((cur_word, ' '.join(variants_of_transcriptions[0])))
                    if len(variants_of_transcriptions) > 1:
                        for variant_idx in range(1, len(variants_of_transcriptions)):
                            transcriptions.append(('{0}({1})'.format(cur_word, variant_idx + 1),
                                                   ' '.join(variants_of_transcriptions[variant_idx])))
                else:
                    bad_words.append(cur_word)
            except:
                bad_words.append(cur_word)
        if ((word_idx + 1) % part_size) == 0:
            part_counter += 1
            print('{0:.2%} of words have been processed...'.format(part_counter / float(n_parts)))
    if part_counter < n_parts:
        print('100.00% of words have been processed...')
    return transcriptions, bad_words


def main():
    parser = ArgumentParser()
    parser.add_argument('-s', '--src', dest='source_word_list', type=str, required=True,
                        help='Source file with words for which phonetical transcirptions will be calculated.')
    parser.add_argument('-d', '--dst', dest='destination_dictionary', type=str, required=True,
                        help='Destination file into which all words with their calculated transcriptions will be '
                             'written.')
    parser.add_argument('-b', '--bad', dest='bad_word_list', type=str, required=True,
                        help='Special file into which bad words will be written '
                             '(transcriptions for bad words cannot be calculated).')
    args = parser.parse_args()

    src_name = os.path.normpath(args.source_word_list)
    assert os.path.isfile(src_name), 'File "{0}" does not exist!'.format(src_name)

    dst_name = os.path.normpath(args.destination_dictionary)
    dst_dir = os.path.dirname(dst_name)
    if len(dst_dir) > 0:
        assert os.path.isdir(dst_dir), 'Directory "{0}" does not exist!'.format(dst_dir)

    bad_name = os.path.normpath(args.bad_word_list)
    bad_dir = os.path.dirname(bad_name)
    if len(bad_dir) > 0:
        assert os.path.isdir(bad_dir), 'Directory "{0}" does not exist!'.format(bad_dir)

    source_words = list()
    with codecs.open(src_name, mode='r',  encoding='utf-8', errors='ignore') as fp:
        cur_line = fp.readline()
        while len(cur_line) > 0:
            prep_line = cur_line.strip()
            if len(prep_line) > 0:
                source_words.append(prep_line)
            cur_line = fp.readline()
    assert len(source_words) > 0, 'The source word list "{0}" is empty!'.format(src_name)
    print('Source words have been successfully loaded...')

    transcriptions, bad_words = transcribe_words(sorted(source_words))
    with codecs.open(dst_name, mode='w', encoding='utf-8', errors='ignore') as fp:
        for cur in transcriptions:
            fp.write('{0} {1}\n'.format(cur[0], cur[1]))

    if len(bad_words) > 0:
        with codecs.open(bad_name, mode='w', encoding='utf-8', errors='ignore') as fp:
            for cur in sorted(bad_words):
                fp.write('{0}\n'.format(cur))


if __name__ == '__main__':
    main()
