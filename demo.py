from argparse import ArgumentParser
import codecs
import os
import re

from russian_g2p import Transcription


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

    src_fp = None
    dst_fp = None
    counter = 0
    transcriptor = Transcription(exception_for_unknown=True)
    silence = '<sil>'
    re_for_russian_letters = re.compile(r'[^АаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя]+')
    try:
        src_fp = codecs.open(src_name, mode='r', encoding='utf-8', errors='ignore')
        dst_fp = codecs.open(dst_name, mode='w', encoding='utf-8', errors='ignore')
        cur_line = src_fp.readline()
        while len(cur_line) > 0:
            prep_line = cur_line.strip()
            if len(prep_line) > 0:
                try:
                    pronunciation = transcriptor.transcribe(prep_line)
                except:
                    pronunciation = None
                if pronunciation is not None:
                    if len(pronunciation) > 0:
                        transcription_v1 = [silence]
                        for cur_part in pronunciation:
                            transcription_v1 += cur_part
                            transcription_v1.append(silence)
                    else:
                        transcription_v1 = None
                else:
                    transcription_v1 = None
                source_text = ' '.join(filter(lambda it: len(it) > 0, re_for_russian_letters.split(prep_line)))
                try:
                    pronunciation = transcriptor.transcribe(source_text)
                except:
                    pronunciation = None
                if pronunciation is not None:
                    if len(pronunciation) > 0:
                        transcription_v2 = [silence]
                        for cur_part in pronunciation:
                            transcription_v2 += cur_part
                            transcription_v2.append(silence)
                    else:
                        transcription_v2 = None
                else:
                    transcription_v2 = None
                if (transcription_v1 is not None) and (transcription_v2 is not None):
                    if args.pair_order == 'text-pronunciation':
                        dst_fp.write('{0}\t{1}\n'.format(source_text.lower(), ' '.join(transcription_v1)))
                    else:
                        dst_fp.write('{0}\t{1}\n'.format(' '.join(transcription_v1), source_text.lower()))
                    if transcription_v2 != transcription_v1:
                        if args.pair_order == 'text-pronunciation':
                            dst_fp.write('{0}\t{1}\n'.format(source_text.lower(), ' '.join(transcription_v2)))
                        else:
                            dst_fp.write('{0}\t{1}\n'.format(' '.join(transcription_v2), source_text.lower()))
            cur_line = src_fp.readline()
            counter += 1
            if (counter % 1000) == 0:
                print('{0} texts...'.format(counter))
        if (counter % 1000) != 0:
            print('{0} texts...'.format(counter))
    finally:
        if src_fp is not None:
            src_fp.close()
        if dst_fp is not None:
            dst_fp.close()


if __name__ == '__main__':
    main()
