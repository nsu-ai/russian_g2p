import codecs
import copy
import json
import os
import re
import warnings
import urllib.request
import urllib.parse
import lxml.html


class Accentor:
    def __init__(self):
        self.__all_russian_letters = {'а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о',
                                      'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю',
                                      'я'}
        self.__russian_vowels = {'а', 'о', 'у', 'э', 'ы', 'и', 'я', 'ё', 'ю', 'е'}
        self.__homonyms = None
        self.__simple_words = None
        self.__new_homonyms = set()
        self.__new_simple_words = set()
        self.__bad_words = []
        self.__re_for_morphosplit = re.compile(r'[\,\s\|]+', re.U)
        self.__re_for_morphotag = re.compile(r'^(\w+|\w+[\-\=]\w+)$', re.U)
        accents_dictionary_name = os.path.join(os.path.dirname(__file__), 'data', 'Accents.json')
        assert os.path.isfile(accents_dictionary_name), 'File `{0}` does not exist!'.format(accents_dictionary_name)
        function_words_name = os.path.join(os.path.dirname(__file__), 'data', 'Function_words.json')
        assert os.path.isfile(accents_dictionary_name), 'File `{0}` does not exist!'.format(function_words_name)
        data = None
        try:
            with codecs.open(accents_dictionary_name, mode='r', encoding='utf-8', errors='ignore') as fp:
                data = json.load(fp)
            with codecs.open(function_words_name, mode='r', encoding='utf-8', errors='ignore') as fp:
                self.__function_words = json.load(fp)
            error_message = 'File `{0}` contains incorrect data!'.format(accents_dictionary_name)
            assert isinstance(data, list), error_message
            assert len(data) == 2, error_message
            assert isinstance(data[0], dict), error_message
            assert isinstance(data[1], list), error_message
            self.__simple_words = dict()
            accented_wordforms = set()
            for cur_wordform in data[1]:
                assert self.check_accented_wordform(cur_wordform), \
                    error_message + ' Word `{0}` is inadmissible!'.format(cur_wordform)
                assert cur_wordform.lower() not in accented_wordforms, \
                    error_message + ' Accented wordform `{0}` already exists!'.format(cur_wordform)
                accented_wordforms.add(cur_wordform.lower())
                wordform_without_accent = ''.join(list(filter(lambda a: a != '+', cur_wordform.lower())))
                assert wordform_without_accent not in self.__simple_words, \
                    error_message + ' Wordform `{0}` already exists!'.format(wordform_without_accent)
                self.__simple_words[wordform_without_accent] = cur_wordform.lower()
            self.__homonyms = dict()
            for cur_wordform in data[0]:
                assert self.check_source_wordform(cur_wordform), \
                    error_message + ' Word `{0}` is inadmissible!'.format(cur_wordform)
                assert (cur_wordform not in self.__homonyms) and (cur_wordform.lower() not in self.__simple_words), \
                    error_message + ' Word `{0}` is repeated!'.format(cur_wordform)
                assert isinstance(data[0][cur_wordform], dict), \
                    error_message + ' Word `{0}` has incorrect description of accents!'.format(cur_wordform)
                for cur_key in data[0][cur_wordform]:
                    assert self.check_morphotag(cur_key), \
                        error_message + ' Word `{0}` has incorrect description of accents!'.format(cur_wordform)
                    assert self.check_accented_wordform(data[0][cur_wordform][cur_key]), \
                        error_message + ' Word `{0}` has incorrect description of accents!'.format(cur_wordform)
                values = [data[0][cur_wordform][it] for it in data[0][cur_wordform]]
                #print(data[0][cur_wordform],values)
                #assert len(values) == len(set(values)), \
                #    error_message + ' Word `{0}` has incorrect description of accents!'.format(cur_wordform)
                self.__homonyms[cur_wordform] = copy.deepcopy(data[0][cur_wordform])
            del accented_wordforms
        finally:
            if data is not None:
                del data

    def __del__(self):
        if self.__homonyms is not None:
            del self.__homonyms
        if self.__simple_words is not None:
            del self.__simple_words
        del self.__all_russian_letters
        del self.__russian_vowels
        del self.__re_for_morphosplit
        del self.__re_for_morphotag
        del self.__new_homonyms
        del self.__new_simple_words
        del self.__bad_words
        del self.__function_words

    def get_correct_omograph_wiki(self, root_text, cur_word, morphotag='X'):

        '''
        Разбор омографии.
        Использование морфологической информации о 
        слове для их разграничения.
        '''
        langs = root_text.split('<hr />')
        #print('hello?')
        root = None
        for lang in langs:
            #print(lang)
            head_pos = lang.find('<h2><span class="mw-headline" id="Russian">Russian</span>')
            if head_pos != -1:
                root = lxml.html.document_fromstring(lang[head_pos:])
        if root == None:
            #print(':^(')
            return []
        good_headers = []
        shallow_vars = set()
        results = set()
        for header in root.findall('.//*[@class="mw-headline"]'):
            #print(cur_word, morphotag)
            if header.text_content() in ['Noun', 'Verb', 'Adjective', 'Adverb', 'Conjunction', 'Determiner', 'Interjection',
    'Morpheme', 'Numeral', 'Particle', 'Predicative', 'Preposition', 'Pronoun']:
                good_headers.append(header.text_content())
                acc_word = header.getparent().getnext()
                while acc_word.tag != 'p':
                    acc_word = acc_word.getnext()
                #print(acc_word)
                result = []
                hyphen = 0
                for part in acc_word.find_class('Cyrl headword'):
                    result += [part.text_content()]
                    if part.text_content().find('-') != -1:
                        hyphen = 1
                #print(result)
                if (hyphen == 1) or (len(result) == 1):
                    result = ''.join(result)
                else:
                    continue
                if result.replace('ё', 'е́').find('́') != -1:
                    shallow_vars.add(result)
                if header.text_content()[0] == morphotag[0]:
                    #print('The tags are equal')
                    if header.text_content()[0] == 'N':
                        gramm_info = acc_word.getnext()
                        if gramm_info.text_content().find('of') != -1:
                            for variant in gramm_info.find_class('form-of-definition'):
                                info = variant.findall('a')
                                #print(variant.text_content())
                                try:
                                    if info[0].text_content()[0] == 'p':
                                        case = 'l'
                                    else:
                                        case = info[0].text_content()[0]
                                    #print(case)
                                    number = info[1].text_content()[0]
                                    #print(number + case, morphotag)
                                    if case == morphotag[morphotag.find('Case=') + 5].lower():
                                        results.add(result)
                                except IndexError:
                                    continue
                        else:
                            if morphotag[morphotag.find('Case=') + 5].lower() == 'n':
                                results.add(result)
                    elif header.text_content()[0] == 'V':
                        gramm_info = acc_word.getnext()
                        if morphotag.find('Mood=Inf') != -1:
                            results.add(result)
                            #print('Wut',morphotag, results)
                        for variant in gramm_info.find_class('form-of-definition'):
                            #print(variant.text_content())
                            t = 0
                            if (variant.text_content().find('indicative') != -1) and (morphotag.find('Mood=Ind') != -1):                          
                                if ((variant.text_content().find('future') != -1) or (variant.text_content().find('present') != -1)) and (morphotag.find('Tense=Notpast') != -1):
                                    #print('I should be here')
                                    results.add(result)
                                    #print(1, results)
                                elif (variant.text_content().find('past') != -1) and (morphotag.find('Tense=Past') != -1):
                                    results.add(result)
                                    #print(2, results)
                            elif (variant.text_content().find('imperative') != -1) and (morphotag.find('Mood=Imp') != -1):
                                results.add(result)
                    else:
                        results.add(result)
            elif (header.text_content()[0] == 'D') and (morphotag.find('PRON') != -1):
                acc_word = header.getparent().getnext()
                result = ''
                for part in acc_word.find_class('Cyrl headword'):
                    result += part.text_content()
                results.add(result)
            elif (header.text_content() == 'Numeral') and (morphotag.find('NUM') != -1):
                acc_word = header.getparent().getnext()
                result = ''
                for part in acc_word.find_class('Cyrl headword'):
                    result += part.text_content()
                results.add(result)
            elif (header.text_content()[0] == 'P') and (morphotag.find('PART') != -1):
                acc_word = header.getparent().getnext()
                result = ''
                for part in acc_word.find_class('Cyrl headword'):
                    result += part.text_content()
                results.add(result)
            elif (header.text_content()[0] == 'Adverb') and (morphotag.find('ADV') != -1):
                acc_word = header.getparent().getnext()
                result = ''
                for part in acc_word.find_class('Cyrl headword'):
                    result += part.text_content()
                results.add(result)
            elif (header.text_content()[0] == 'Adjective') and (morphotag.find('ADJ') != -1):
                acc_word = header.getparent().getnext()
                result = ''
                for part in acc_word.find_class('Cyrl headword'):
                    result += part.text_content()
                results.add(result)
        #print(shallow_vars)
        if len(list(shallow_vars)) == 1:
            if list(shallow_vars)[0].replace('ё', 'е+').replace('́', '') == cur_word:
                return [list(shallow_vars)[0].replace('ё', 'ё+').replace('́', '+').replace('́', '+')]
        #print(results)
        if len(list(results)) != 1:
            return []
        best_results = [variant.replace('́', '+') for variant in results]

        return list(best_results)

    def get_simple_form_wiki(self, root_text, form):

        '''
        Непосредственное нахождение релевантной формы
        и ударение без морфологической информации.
        '''
        root = lxml.html.document_fromstring(root_text)
        rel_forms = set()
        for header in root.findall('.//*[@class="Cyrl headword"][@lang="ru"]'):
            header_text = header.text_content().replace('ё', 'е́')
            header_text_best = header.text_content().replace('ё', 'ё+').replace('́', '+')
            if header_text.replace('́', '') == form:
                if header_text.find('́') != -1:
                    rel_forms.add(header_text_best)
        for mention in root.findall('.//i[@class="Cyrl mention"][@lang="ru"]'):
            mention_text = mention.text_content().replace('ё', 'е́')
            mention_text_best = mention.text_content().replace('ё', 'ё+').replace('́', '+')
            if mention_text.replace('́', '') == form:
                if mention_text.replace('ё', 'е́').find('́') != -1:
                    rel_forms.add(mention_text_best)
        for mention in root.findall('.//b[@class="Cyrl"][@lang="ru"]'):
            mention_text = mention.text_content().replace('ё', 'е́')
            mention_text_best = mention.text_content().replace('ё', 'ё+').replace('́', '+')
            if mention_text.replace('́', '') == form:
                if mention_text.replace('ё', 'е́').find('́') != -1:
                    rel_forms.add(mention_text_best)
            elif mention_text.find('(') != -1:
                if mention_text.replace('́', '').find(form) != -1:
                    if mention_text.find('́') != -1:
                        rel_forms.add(mention_text_best[mention_text.replace('́', '').find(form):])
                elif re.sub('[\(\)́]', '', mention_text) == form:
                    rel_forms.add(re.sub('[\(\)]', '', mention_text_best))
        for target in root.xpath('.//span[@class="Cyrl"][@lang="ru"]'):
            one_form = target.text_content()
            if one_form.replace('ё', 'е́').replace('́', '') == form:
                if one_form.replace('ё', 'е́').find('́') != -1:
                    rel_forms.add(one_form.replace('ё', 'ё́').replace('́', '+'))
        results = list(rel_forms)
        if len(results) == 2:
            if results[0].replace('ё', 'е') == results[1].replace('ё', 'е'):
                rel_forms = set()
                for var in results:
                    if var.find('ё') != -1:
                        rel_forms.add(var)
        return list(rel_forms)

    def load_wiki_page(self, cur_form):
        query = urllib.parse.urlencode({ 'title' : cur_form })
        try:
            with urllib.request.urlopen('https://en.wiktionary.org/w/index.php?{}&#printable=yes'.format(query)) as f:
                root_text = f.read().decode('utf-8')
                return root_text
        except urllib.error.HTTPError:
            return

    def do_accents(self, source_phrase: list, morphotags_of_phrase: list=None) -> list:
        prepared_phrase = []
        for cur_word in source_phrase:
            assert len(cur_word.strip()) > 0, '`{0}`: this phrase is wrong!'.format(source_phrase)
            prepared_phrase.append(cur_word.strip().lower())
        if morphotags_of_phrase is not None:
            assert len(prepared_phrase) == len(morphotags_of_phrase), \
                '`{0}`: morphotags do not correspond to words!'.format(' '.join(source_phrase))
        assert len(prepared_phrase) > 0, 'Source phrase is empty!'
        return self.__do_accents(prepared_phrase, morphotags_of_phrase)

    def check_source_wordform(self, checked: str) -> bool:
        if len(checked.strip()) == 0:
            return False
        res = len(self.__all_russian_letters | {'-'}) \
              == len((self.__all_russian_letters | {'-'}) | set(checked.lower()))
        if not res:
            return False
        if '-' not in checked:
            return True
        for cur_part in checked.split('-'):
            if len(cur_part) == 0:
                res = False
                break
        return res

    def check_accented_wordform(self, checked: str) -> bool:
        if len(checked.strip()) == 0:
            return False
        res = len(self.__all_russian_letters | {'-', '+'}) \
              == len((self.__all_russian_letters | {'-', '+'}) | set(checked.lower()))
        if not res:
            return False
        if '-' in checked:
            parts = list()
            for cur_part in checked.split('-'):
                parts.append(cur_part.lower().strip())
        else:
            parts = [checked.lower().strip()]
        for cur_part in parts:
            filtered_part = ''.join(list(filter(lambda c: c != '+', cur_part)))
            if len(filtered_part) == 0:
                res = False
                break
        return res

    def check_morphotag(self, morphotag: str) -> bool:
        if len(morphotag.strip()) == 0:
            return False
        if morphotag.isdigit():
            return True
        ind1 = morphotag.find('(')
        ind2 = morphotag.find(')')
        if (ind1 < 0) and (ind2 < 0):
            ok = len(morphotag.strip()) > 0
        else:
            if (ind1 >= 0) and (ind1 >= ind2):
                ok = False
            elif len(morphotag[:ind1].strip()) == 0:
                ok = False
            elif len(morphotag[(ind1 + 1):ind2].strip()) == 0:
                ok = False
            elif not morphotag[(ind1 + 1):ind2].strip().isdigit():
                ok = False
            else:
                ok = (len(morphotag[(ind2 + 1):].strip()) == 0)
        if ok:
            if ind1 < 0:
                ind1 = len(morphotag)
            for cur_part in self.__re_for_morphosplit.split(morphotag[:ind1].strip()):
                if len(cur_part.strip()) == 0:
                    ok = False
                    break
                if cur_part.strip().isdigit():
                    ok = False
                    break
                search_res = self.__re_for_morphotag.search(cur_part.strip())
                if search_res is None:
                    ok = False
                    break
                if (search_res.start() < 0) or (search_res.end() < 0):
                    ok = False
                    break
        return ok

    def calculate_morpho_similarity(self, morphotags_1: str, morphotags_2: str) -> float:
        if morphotags_1.isdigit() or morphotags_2.isdigit():
            return 0.0
        prepared_morpotags_1 = set(filter(
            lambda a: len(a) > 0,
            map(lambda b: b.strip(), self.__re_for_morphosplit.split(morphotags_1))
        ))
        prepared_morpotags_2 = set(filter(
            lambda a: len(a) > 0,
            map(lambda b: b.strip(), self.__re_for_morphosplit.split(morphotags_2))
        ))
        if (len(prepared_morpotags_1) == 0) and (len(prepared_morpotags_2) == 0):
            return 0.0
        return len(prepared_morpotags_1 & prepared_morpotags_2) / len(prepared_morpotags_1 | prepared_morpotags_2)

    def prepare_morphotag(self, source_morphotag: str) -> str:
        ind1 = source_morphotag.find('(')
        ind2 = source_morphotag.find(')')
        if ind1 < 0:
            if ind2 >= 0:
                res = source_morphotag[:ind2].strip()
            else:
                res = source_morphotag.strip()
        else:
            if ind2 >= 0:
                res = source_morphotag[:(ind2 if ind2 < ind1 else ind1)].strip()
            else:
                res = source_morphotag[:ind1].strip()
        return res

    def get_new_dics(self):
        return self.__new_homonyms, sorted(list(self.__new_simple_words))

    def get_bad_words(self):
        return self.__bad_words

    def __do_accents(self, words_list: list, morphotags_list: list=None) -> list:
        n = len(words_list)
        if morphotags_list is not None:
            assert n == len(morphotags_list), 'Morphotags do not correspond to words!'
        if n < 1:
            return []
        cur_token = words_list[0].lower()
        warn = ''
        if '+' in cur_token:
            accented_wordforms = [cur_token]
        else:
            accented_wordforms = []
            for i, cur_word in enumerate([cur_token] + cur_token.split('-')):
                vowels_counter = 0
                for cur in cur_word:
                    if cur in self.__russian_vowels:
                        vowels_counter += 1
                if (cur_word in self.__function_words) or (vowels_counter == 0) or (('-' + cur_word) in self.__function_words) or ((cur_word + '-') in self.__function_words):
                    accented_wordforms += [cur_word]
                elif vowels_counter == 1:
                    cur_vowel = list(set(cur_word) & self.__russian_vowels)[0]
                    pos = cur_word.find(cur_vowel)
                    try:
                        accented_wordforms += [cur_word[:(pos+1)] + '+' + cur_word[(pos+1):]]
                    except IndexError:
                        accented_wordforms += [cur_word[:pos] + '+']
                elif 'ё' in cur_word:
                    yo_ind = cur_word.find('ё')
                    try:
                        accented_wordforms += [cur_word[:(yo_ind+1)] + '+' + cur_word[(yo_ind+1):]]
                    except IndexError:
                        accented_wordforms += [cur_word[:yo_ind] + '+']
                elif cur_word in self.__simple_words:
                    accented_wordforms += [self.__simple_words[cur_word]]
                elif cur_word in self.__homonyms:
                    if (morphotags_list is None) or morphotags_list[0].isdigit():
                        #accented_wordforms = sorted([self.__homonyms[cur_word][it] for it in self.__homonyms[cur_word]])
                        accented_wordforms += [cur_word]
                        warn = 'many'
                    else:
                        best_ind = -1
                        best_similarity = 0.0
                        morpho_variants = list(self.__homonyms[cur_word].keys())
                        for ind in range(len(morpho_variants)):
                            similarity = self.calculate_morpho_similarity(morpho_variants[ind], morphotags_list[0])
                            if similarity > best_similarity:
                                best_similarity = similarity
                                best_ind = ind
                        if best_ind >= 0:
                            accented_wordforms += [self.__homonyms[cur_word][morpho_variants[best_ind]]]
                        else:
                            root_text = self.load_wiki_page(cur_word)
                            if root_text != None:
                                #print('am I even here?')
                                cur_accented_wordforms = sorted(self.get_correct_omograph_wiki(root_text, cur_word, morphotags_list[0]))
                                if len(cur_accented_wordforms) == 1:
                                    accented_wordforms += [cur_accented_wordforms[0]]
                                    self.__new_homonyms[cur_word] = {morphotags_list[0] : cur_accented_wordforms[0]}
                                else:
                                    accented_wordforms += [cur_word]
                                    warn = 'many'
                            else:
                                accented_wordforms += [cur_word]
                                warn = 'many'
                else:
                    root_text = self.load_wiki_page(cur_word)
                    if root_text != None:
                        cur_accented_wordforms = sorted(self.get_simple_form_wiki(root_text, cur_word))
                        if len(cur_accented_wordforms) == 1:
                            accented_wordforms += [cur_accented_wordforms[0]]
                            self.__new_simple_words.add(cur_accented_wordforms[0])
                        elif len(cur_accented_wordforms) == 0:
                            accented_wordforms += [cur_word]
                            warn = 'no'
                        else:
                            cur_accented_wordforms = sorted(self.get_correct_omograph_wiki(root_text, cur_word, morphotags_list[0]))
                            if len(cur_accented_wordforms) == 1:
                                accented_wordforms += [cur_accented_wordforms[0]]
                                self.__new_homonyms[cur_word] = {morphotags_list[0] : cur_accented_wordforms[0]}
                            else:
                                accented_wordforms += [cur_word]
                                warn = 'many'

                    else:
                        accented_wordforms += [cur_word]
                        warn = 'no'
                if (i == 0):
                    if (accented_wordforms[0].find('+') != -1):
                        break
                    else:
                        accented_wordforms = []
        if len(accented_wordforms) != 1:
            accented_wordforms = ['-'.join(accented_wordforms)]
        else:
            accented_wordforms = [accented_wordforms[0]]
        if cur_token in accented_wordforms:
            accented_wordforms = [accented_wordforms[accented_wordforms.index(cur_token)]]
            if warn != '':
                self.__bad_words.append(cur_token)
                if warn == 'many':
                    warnings.warn('Word `{0}` has too many accent variants!'.format(cur_token))
                elif warn == 'no':
                    warnings.warn('Word `{0}` is unknown!'.format(cur_word))

        accented_phrases = []
        if n > 1:
            for cur_accent in accented_wordforms:
                for vt in self.__do_accents(words_list[1:], None if morphotags_list is None else morphotags_list[1:]):
                    accented_phrases.append([cur_accent] + vt)
        else:
            for cur_accent in accented_wordforms:
                accented_phrases.append([cur_accent])
        return accented_phrases
