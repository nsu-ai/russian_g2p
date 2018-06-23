from argparse import ArgumentParser
import codecs
import os
import re

from russian_g2p.Transcription import Transcription


def iterate_by_texts(file_name):
    batch_size = 1000
    re_for_russian_letters = re.compile(
        r'[^АаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя]+',
        re.U
    )
    source_lines_v1 = []
    source_lines_v2 = []
    with codecs.open(file_name, mode='r', encoding='utf-8', errors='ignore') as src_fp:
        cur_line = src_fp.readline()
        while len(cur_line) > 0:
            prep_line_v1 = cur_line.strip()
            if len(prep_line_v1) > 0:
                source_lines_v1.append(prep_line_v1)
                prep_line_v2 = ' '.join(
                    filter(
                        lambda it2: len(it2) > 0,
                        map(lambda it1: it1.strip(), re_for_russian_letters.split(prep_line_v1))
                    )
                )
                source_lines_v2.append(prep_line_v2)
            cur_line = src_fp.readline()
            if len(source_lines_v1) >= batch_size:
                print('')
                print('{0} texts have been prepared for processing...'.format(len(source_lines_v1)))
                yield source_lines_v1, source_lines_v2
                source_lines_v1 = []
                source_lines_v2 = []
    if len(source_lines_v1) > 0:
        print('')
        print('{0} texts have been prepared for processing...'.format(len(source_lines_v1)))
        yield source_lines_v1, source_lines_v2


def main():
    parser = ArgumentParser()
    parser.add_argument('-s', '--src', dest='source_data_file', type=str, required=True,
                        help='Source file with phrases list to the g2p transforming.')
    parser.add_argument('-d', '--dst', dest='destination_data_file', type=str, required=True,
                        help='Destination file into which texts and created phonetical pronunciations, corresponding '
                             'to these texts, will be written.')
    parser.add_argument('-o', '--order', dest='pair_order', type=str, required=False,
                        choices=['text-pronunciation', 'pronunciation-text'], default='pronunciation-text',
                        help='Order of each pair: text and its pronunciation or pronunciation and corresponding text?')
    args = parser.parse_args()

    src_name = os.path.normpath(args.source_data_file)
    assert os.path.isfile(src_name), 'File "{0}" does not exist!'.format(src_name)

    dst_name = os.path.normpath(args.destination_data_file)
    dst_dir = os.path.dirname(dst_name)
    if len(dst_dir) > 0:
        assert os.path.isdir(dst_dir), 'Directory "{0}" does not exist!'.format(dst_dir)

    transcriptor = Transcription(raise_exceptions=True, verbose=False, batch_size=256, use_wiki=False)
    silence = '<sil>'
    with codecs.open(dst_name, mode='w', encoding='utf-8', errors='ignore') as dst_fp:
        for source_lines_v1, source_lines_v2 in iterate_by_texts(src_name):
            pronunciations_v1 = transcriptor.transcribe(source_lines_v1)
            pronunciations_v2 = transcriptor.transcribe(source_lines_v2)
            for line_idx in range(len(source_lines_v1)):
                pronunciation_v1 = pronunciations_v1[line_idx]
                if len(pronunciation_v1) > 0:
                    transcription_v1 = [silence]
                    for cur_part in pronunciation_v1:
                        transcription_v1 += cur_part
                        transcription_v1.append(silence)
                else:
                    transcription_v1 = []
                pronunciation_v2 = pronunciations_v2[line_idx]
                if len(pronunciation_v2) > 0:
                    transcription_v2 = [silence]
                    for cur_part in pronunciation_v2:
                        transcription_v2 += cur_part
                        transcription_v2.append(silence)
                else:
                    transcription_v2 = []
                source_text = source_lines_v2[line_idx]
                if (len(transcription_v1) > 0) and (len(transcription_v2) > 0):
                    if args.pair_order == 'text-pronunciation':
                        dst_fp.write('{0}\t{1}\n'.format(source_text.lower(), ' '.join(transcription_v1)))
                    else:
                        dst_fp.write('{0}\t{1}\n'.format(' '.join(transcription_v1), source_text.lower()))
                    if transcription_v2 != transcription_v1:
                        if args.pair_order == 'text-pronunciation':
                            dst_fp.write('{0}\t{1}\n'.format(source_text.lower(), ' '.join(transcription_v2)))
                        else:
                            dst_fp.write('{0}\t{1}\n'.format(' '.join(transcription_v2), source_text.lower()))
            print('{0} texts have been processed...'.format(len(source_lines_v1)))
            del pronunciations_v1
            del pronunciations_v2
            del source_lines_v1
            del source_lines_v2


if __name__ == '__main__':
    main()
