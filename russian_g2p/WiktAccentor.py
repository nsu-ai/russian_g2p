import urllib.parse
import pymorphy2
import re
from treetagger import TreeTagger
import lxml.html
import time
import random
import json
import codecs
import numpy as np


def get_correct_acc_morf(cur_word, morphotag, accented_wordforms):
    """
    Разбор омографии.
    Использование морфологической информации о
    слове для их разграничения.
    """
    query = urllib.parse.urlencode({'title': cur_word})

    try:
        with urllib.request.urlopen('https://en.wiktionary.org/w/index.php?{}&printable=yes'.format(query)) as f:
            langs = f.read().decode('utf-8').split('<hr />')
    except urllib.error.HTTPError:
        print('Troubles with connection :(')
        return accented_wordforms

    root = None

    for lang in langs:
        head_pos = lang.find('<h2><span class="mw-headline" id="Russian">Russian</span></h2>')
        if head_pos != -1:
            root = lxml.html.document_fromstring(lang[head_pos:])

    if root is None:
        print('Did not find the word in wiktionary :(')
        return accented_wordforms

    good_headers = []

    shallow_vars = set()

    results = set()

    parts_of_speech = ['Noun', 'Verb', 'Adjective', 'Adverb', 'Conjunction', 'Determiner', 'Interjection',
                       'Morpheme', 'Numeral', 'Particle', 'Predicative', 'Preposition', 'Pronoun']

    for header in root.findall('.//*[@class="mw-headline"]'):
        # print(header.text_content())
        if header.text_content() in parts_of_speech:
            good_headers.append(header.text_content())
            acc_word = header.getparent().getnext()
            while acc_word.tag != 'p':
                acc_word = acc_word.getnext()
            result = acc_word.find_class('Cyrl headword')[0].text_content()
            if result.replace('ё', 'е́').find('́') != -1:
                shallow_vars.add(result)
            if header.text_content()[0] == morphotag[0]:
                print('The tags are equal')
                if header.text_content()[0] == 'N':
                    gramm_info = acc_word.getnext()
                    if gramm_info.text_content().find('of') != -1:
                        for variant in gramm_info.find_class('form-of-definition'):
                            info = variant.findall('a')
                            # print(variant.text_content())
                            try:
                                if info[0].text_content()[0] == 'p':
                                    case = 'l'
                                else:
                                    case = info[0].text_content()[0]
                                # print(case)
                                number = info[1].text_content()[0]
                                # print(number + case, treetagged_sentence[i][1][3:5])
                                if number + case == treetagged_sentence[i][1][3:5]:
                                    results.add(result)
                            except IndexError:
                                try:
                                    if case == treetagged_sentence[i][1][4]:
                                        results.add(result)
                                except NameError:
                                    continue
                    else:
                        if treetagged_sentence[i][1][4] == 'n':
                            results.add(result)
                elif header.text_content()[0] == 'V':
                    gramm_info = acc_word.getnext()
                    if treetagged_sentence[i][1][3] == 'n':
                        results.add(result)

                    def variant_fits(form_to_find: str, ind, chars: list) -> bool:
                        return (variant.text_content().find(form_to_find) != -1) and (
                                treetagged_sentence[i][1][ind] in chars)

                    for variant in gramm_info.find_class('form-of-definition'):
                        t = 0
                        if variant_fits('indicative', 2, ['i', '-']):
                            t += variant_fits('future', 3, ['f', '-']) or \
                                 variant_fits('present', 3, ['p', '-']) or \
                                 variant_fits('past', 3, ['s', '-'])
                        else:
                            t += variant_fits('imperative', 2, ['m', '-'])
                        t += variant_fits('imperfective', 9, ['e', 'b', '-']) or \
                             variant_fits('perfective', 9, ['p', '-'])
                        if t == 2:
                            results.add(result)
                else:
                    results.add(result)
            else:
                pairs_of_pos_tags = [('Numeral', 'M'), ('Adverb', 'R')]
                for tag_1, tag_2 in pairs_of_pos_tags:
                    if (header.text_content() == tag_1) and (treetagged_sentence[i][1][0] == tag_2):
                        acc_word = header.getparent().getnext()
                        result = acc_word.find_class('Cyrl headword')[0].text_content()
                        results.add(result)
                pairs_of_tags = [('D', 'P'), ('P', 'S'), ('A', 'P')]
                for tag_1, tag_2 in pairs_of_tags:
                    if (header.text_content()[0] == tag_1) and (treetagged_sentence[i][1][0] == tag_2):
                        acc_word = header.getparent().getnext()
                        result = acc_word.find_class('Cyrl headword')[0].text_content()
                        results.add(result)

    # print(list(shallow_vars))

    if len(list(shallow_vars)) == 1:
        # print(list(shallow_vars)[0].replace('ё', 'е́'), treetagged_sentence[i][0])
        if list(shallow_vars)[0].replace('ё', 'е́').replace('́', '') == treetagged_sentence[i][0]:
            return 0, list({list(shallow_vars)[0].replace('ё', 'ё́')})

    # print(list(results))

    if len(list(results)) != 1:
        # print('\t!!!Sentence in line {} contains a word "{}" that has too many variants (or zero)!!!\n\tCouldn\'t work out the appropriate.\n\tThe tags that couldn\'t be matched: {} => {}\n\tReturning word without accent (please correct!).\n\tAdded to log.'.format(sent_id + 1, treetagged_sentence[i][0], treetagged_sentence[i][1], ', '.join(good_headers)))
        with open(error_log_filename, 'a') as wr_file:
            wr_file.writelines(
                '/Code 2/ line {}: {} ({}) ### {} => {}\n'.format(sent_id + 1, treetagged_sentence[i][0], i,
                                                                  treetagged_sentence[i][1], ', '.join(good_headers)))

    return 0, list(results)
