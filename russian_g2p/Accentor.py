import codecs
import copy
import json
import os
import re
import warnings
import urllib.request
import urllib.parse
import lxml.html
import itertools
import dawg
import logging


class Accentor:
    def __init__(self, mode='one', debug='no', exception_for_unknown=False, use_wiki=True):
        if debug == 'no':
            logging.basicConfig()
        else:
            logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger()
        self.logger.debug('Setting up the Accentor...')
        self.mode = mode
        self.__all_russian_letters = {'а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о',
                                      'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю',
                                      'я'}
        self.__russian_vowels = {'а', 'о', 'у', 'э', 'ы', 'и', 'я', 'ё', 'ю', 'е'}
        self.exception_for_unknown = exception_for_unknown
        self.use_wiki = use_wiki
        self.__homonyms = None
        self.__simple_words_dawg = None
        self.__function_words = None
        self.__new_homonyms = {}
        self.__new_simple_words = set()
        self.__bad_words = []
        self.__re_for_morphosplit = re.compile(r'[\,\s\|]+', re.U)
        self.__re_for_morphotag = re.compile(r'^(\w+|\w+[\-\=]\w+)$', re.U)
        assert mode in ('one', 'many'), 'Set either "one" or "many" variant mode!'
        assert debug in ('yes', 'no'), 'Set either "yes" or "no" variant mode!'
        homograph_dictionary_name = os.path.join(os.path.dirname(__file__), 'data', 'homographs.json')
        assert os.path.isfile(homograph_dictionary_name), f'File `{homograph_dictionary_name}` does not exist!'
        simple_words_dawg_name = os.path.join(os.path.dirname(__file__), 'data', 'simple_words.dawg')
        assert os.path.isfile(simple_words_dawg_name), f'File `{simple_words_dawg_name}` does not exist!'
        function_words_name = os.path.join(os.path.dirname(__file__), 'data', 'Function_words.json')
        assert os.path.isfile(function_words_name), f'File `{function_words_name}` does not exist!'
        data = None
        try:
            d = dawg.IntDAWG()
            self.__simple_words_dawg = d.load(simple_words_dawg_name)
            ###
            with codecs.open(homograph_dictionary_name, mode='r', encoding='utf-8', errors='ignore') as fp:
                data = json.load(fp)
            error_message_homographs = f'File `{homograph_dictionary_name}` contains incorrect data!'
            assert isinstance(data, dict), error_message_homographs
            self.__homonyms = dict()
            for cur_wordform in data:
                assert self.check_source_wordform(cur_wordform), \
                    error_message_homographs + f' Word `{cur_wordform}` is inadmissible!'
                assert (cur_wordform not in self.__homonyms) and (cur_wordform.lower() not in self.__simple_words_dawg), \
                    error_message_homographs + f' Word `{cur_wordform}` is repeated!'
                assert isinstance(data[cur_wordform], dict), \
                    error_message_homographs + f' Word `{cur_wordform}` has incorrect description of accents!'
                for cur_key in data[cur_wordform]:
                    assert self.check_morphotag(cur_key), \
                        error_message_homographs + f' Word `{cur_wordform}` has incorrect description of accents!'
                    assert self.check_accented_wordform(data[cur_wordform][cur_key]), \
                        error_message_homographs + f' Word `{cur_wordform}` has incorrect description of accents!'
                values = [data[cur_wordform][it] for it in data[cur_wordform]]
                self.__homonyms[cur_wordform] = copy.deepcopy(data[cur_wordform])
            ###
            self.__function_words = None
            with codecs.open(function_words_name, mode='r', encoding='utf-8', errors='ignore') as fp:
                function_words = json.load(fp)
            error_message_function_words = f'File `{function_words_name}` contains incorrect data!'
            assert isinstance(function_words, list), error_message_function_words
            assert isinstance(function_words[0], str), error_message_function_words
            self.__function_words = function_words
        finally:
            if data is not None:
                del data

    def __del__(self):
        if self.__homonyms is not None:
            del self.__homonyms
        if self.__simple_words_dawg is not None:
            del self.__simple_words_dawg
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
                if result.replace('ё', 'е́').find('') != -1:
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
            elif (header.text_content().lower().find(morphotag.split()[0].lower()) != -1):
                acc_word = header.getparent().getnext()
                result = ''
                for part in acc_word.find_class('Cyrl headword'):
                    result += part.text_content()
                results.add(result)
        #print(shallow_vars)
        if len(list(shallow_vars)) == 1:
            if list(shallow_vars)[0].replace('ё', 'е+').replace('', '') == cur_word:
                return [list(shallow_vars)[0].replace('ё', 'ё+').replace('', '+').replace('', '+')]
        #print(results)
        if len(list(results)) != 1:
            return []
        best_results = [variant.replace('', '+') for variant in results]
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
            header_text_best = header.text_content().replace('ё', 'ё+').replace('', '+')
            if header_text.replace('', '') == form:
                if header_text.find('') != -1:
                    rel_forms.add(header_text_best)
        for mention in root.findall('.//i[@class="Cyrl mention"][@lang="ru"]'):
            mention_text = mention.text_content().replace('ё', 'е́')
            mention_text_best = mention.text_content().replace('ё', 'ё+').replace('', '+')
            if mention_text.replace('', '') == form:
                if mention_text.replace('ё', 'е́').find('') != -1:
                    rel_forms.add(mention_text_best)
        for mention in root.findall('.//b[@class="Cyrl"][@lang="ru"]'):
            mention_text = mention.text_content().replace('ё', 'е́')
            mention_text_best = mention.text_content().replace('ё', 'ё+').replace('', '+')
            if mention_text.replace('', '') == form:
                if mention_text.replace('ё', 'е́').find('') != -1:
                    rel_forms.add(mention_text_best)
            elif mention_text.find('(') != -1:
                if mention_text.replace('', '').find(form) != -1:
                    if mention_text.find('') != -1:
                        rel_forms.add(mention_text_best[mention_text.replace('', '').find(form):])
                elif re.sub(r'[\(\)́]', '', mention_text) == form:
                    rel_forms.add(re.sub(r'[\(\)]', '', mention_text_best))
        for target in root.xpath('.//span[@class="Cyrl"][@lang="ru"]'):
            one_form = target.text_content()
            if one_form.replace('ё', 'е́').replace('', '') == form:
                if one_form.replace('ё', 'е́').find('') != -1:
                    rel_forms.add(one_form.replace('ё', 'ё́').replace('', '+'))
        results = list(rel_forms)
        if len(results) == 2:
            if results[0].replace('ё', 'е') == results[1].replace('ё', 'е'):
                rel_forms = set()
                for var in results:
                    if var.find('ё') != -1:
                        rel_forms.add(var)
        return list(rel_forms)

    def load_wiki_page(self, cur_form):
        if not self.use_wiki:
            if self.exception_for_unknown:
                raise ValueError(f'Word `{cur_form}` is unknown!')
            return
        query = urllib.parse.urlencode({ 'title' : cur_form })
        try:
            http_exception_type = urllib.error.HTTPError
        except:
            http_exception_type = urllib.request.HTTPError
        try:
            with urllib.request.urlopen(f'https://en.wiktionary.org/w/index.php?{query}&#printable=yes') as f:
                root_text = f.read().decode('utf-8')
                return root_text
        except http_exception_type:
            return

    def do_accents(self, source_phrase_and_morphotags: list) -> list:
        self.logger.debug('Checking the source phrase...')
        error_message = f'`{source_phrase_and_morphotags}`: the phrase should be of a "list of lists" format!\nExample: [["word1","morphotag1"], ["word2","morphotag2"]] or [["word1"], ["word2"]]'
        assert isinstance(source_phrase_and_morphotags, list), error_message
        try:
            assert isinstance(source_phrase_and_morphotags[0], list), error_message
        except IndexError:
            assert len(source_phrase_and_morphotags) > 0, 'Source phrase is empty!'
        try:
            source_phrase, morphotags_of_phrase = list(zip(*source_phrase_and_morphotags))
        except (ValueError, TypeError):
            source_phrase = list(zip(*source_phrase_and_morphotags))[0]
            morphotags_of_phrase = None
        for pair in source_phrase_and_morphotags:
            assert len(pair) == len(source_phrase_and_morphotags[0]), \
                f"`{' '.join(source_phrase)}`: morphotags do not correspond to words!"
        prepared_phrase = []
        for cur_word in source_phrase:
            assert len(cur_word.strip()) > 0, f'`{source_phrase}`: this phrase is wrong!'
            prepared_phrase.append(cur_word.strip().lower())
        if morphotags_of_phrase is not None:
            assert len(prepared_phrase) == len(morphotags_of_phrase), \
                f"`{' '.join(source_phrase)}`: morphotags do not correspond to words!"
        assert len(prepared_phrase) > 0, 'Source phrase is empty!'
        try:
            res = self.__do_accents(prepared_phrase, morphotags_of_phrase)
        except Exception as e:
            err_msg = str(e)
            ok = False
            res = []
            for modified_phrase in self.__generate_phrases_with_jo(prepared_phrase, []):
                try:
                    res = self.__do_accents(modified_phrase, morphotags_of_phrase)
                    ok = True
                except Exception as e:
                    ok = False
                    err_msg = str(e)
                if ok:
                    break
            if not ok:
                raise ValueError(err_msg)
        return res

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

    def __generate_phrases_with_jo(self, old_phrase, new_phrase):
        if len(old_phrase) == 0:
            yield new_phrase
        else:
            found_pos = old_phrase[0].find('е')
            while found_pos >= 0:
                new_word = old_phrase[0][:found_pos] + 'ё' + old_phrase[0][(found_pos + 1):]
                yield from self.__generate_phrases_with_jo(old_phrase[1:], new_phrase + [new_word])
                found_pos = old_phrase[0].find('е', found_pos + 1)
            yield from self.__generate_phrases_with_jo(old_phrase[1:], new_phrase + [old_phrase[0]])

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
            accented_wordforms_many = [cur_token]
        else:
            accented_wordforms = []
            accented_wordforms_many = []
            separate_tokens = [cur_token] + cur_token.split('-')
            for i, cur_word in enumerate(separate_tokens):
                vowels_counter = 0
                for cur in cur_word:
                    if cur in self.__russian_vowels:
                        vowels_counter += 1
                if (cur_word in self.__function_words) or (vowels_counter == 0) or (('-' + cur_word) in self.__function_words) or ((cur_word + '-') in self.__function_words):
                    self.logger.debug(f'The word `{cur_word}` is in the list of function words')
                    accented_wordforms += [cur_word]
                    accented_wordforms_many.append([cur_word])
                elif vowels_counter == 1:
                    self.logger.debug(f'The word `{cur_word}` has one vowel: accented automatically')
                    cur_vowel = list(set(cur_word) & self.__russian_vowels)[0]
                    pos = cur_word.find(cur_vowel)
                    try:
                        accented_wordforms += [cur_word[:(pos+1)] + '+' + cur_word[(pos+1):]]
                        accented_wordforms_many.append([cur_word[:(pos+1)] + '+' + cur_word[(pos+1):]])
                    except IndexError:
                        accented_wordforms += [cur_word[:pos] + '+']
                        accented_wordforms_many.append([cur_word[:pos] + '+'])
                elif cur_word in self.__simple_words_dawg:
                    self.logger.debug(f'The word `{cur_word}` is in the dictionary of simple words')
                    accented_wordform = cur_word[:self.__simple_words_dawg[cur_word]] + '+' + cur_word[self.__simple_words_dawg[cur_word]:]
                    accented_wordforms += [accented_wordform]
                    accented_wordforms_many.append([accented_wordform])
                elif cur_word in self.__homonyms:
                    self.logger.debug(f'The word `{cur_word}` is in the dictionary of homonyms')
                    if (morphotags_list is None) or morphotags_list[0].isdigit():
                        accented_wordforms += [cur_word]
                        accented_wordforms_many.append(sorted([self.__homonyms[cur_word][it] for it in self.__homonyms[cur_word]]))
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
                            accented_wordforms_many.append([self.__homonyms[cur_word][morpho_variants[best_ind]]])
                        else:
                            root_text = self.load_wiki_page(cur_word)
                            if root_text != None:
                                #print('am I even here?')
                                cur_accented_wordforms = sorted(self.get_correct_omograph_wiki(root_text, cur_word, morphotags_list[0]))
                                if len(cur_accented_wordforms) == 1:
                                    accented_wordforms += [cur_accented_wordforms[0]]
                                    accented_wordforms_many.append([cur_accented_wordforms[0]])
                                    self.__new_homonyms[cur_word] = {morphotags_list[0] : cur_accented_wordforms[0]}
                                elif len(cur_accented_wordforms) > 1:
                                    accented_wordforms += [cur_word]
                                    accented_wordforms_many.append([cur_accented_wordforms])
                                    warn = 'many'
                                else:
                                    accented_wordforms += [cur_word]
                                    accented_wordforms_many.append(sorted([self.__homonyms[cur_word][it] for it in self.__homonyms[cur_word]]))
                                    warn = 'many'
                            else:
                                accented_wordforms += [cur_word]
                                accented_wordforms_many.append(sorted([self.__homonyms[cur_word][it] for it in self.__homonyms[cur_word]]))
                                warn = 'many'
                else:
                    self.logger.debug(f'The word `{cur_word}` was not found in any of the dictionaries\nTrying to parse wictionary page...')
                    root_text = self.load_wiki_page(cur_word)
                    if root_text != None:
                        cur_accented_wordforms = sorted(self.get_simple_form_wiki(root_text, cur_word))
                        if len(cur_accented_wordforms) == 1:
                            accented_wordforms += [cur_accented_wordforms[0]]
                            accented_wordforms_many.append([cur_accented_wordforms[0]])
                            self.__new_simple_words.add(cur_accented_wordforms[0])
                        elif len(cur_accented_wordforms) == 0:
                            accented_wordforms += [cur_word]
                            accented_wordforms_many.append([cur_word])
                            warn = 'no'
                        else:
                            cur_accented_wordforms = sorted(self.get_correct_omograph_wiki(root_text, cur_word, morphotags_list[0]))
                            if len(cur_accented_wordforms) == 1:
                                accented_wordforms += [cur_accented_wordforms[0]]
                                accented_wordforms_many.append([cur_accented_wordforms[0]])
                                self.__new_homonyms[cur_word] = {morphotags_list[0] : cur_accented_wordforms[0]}
                            else:
                                accented_wordforms += [cur_word]
                                accented_wordforms_many.append(sorted([self.__homonyms[cur_word][it] for it in self.__homonyms[cur_word]]))
                                warn = 'many'

                    else:
                        accented_wordforms += [cur_word]
                        accented_wordforms_many.append([cur_word])
                        warn = 'no'
                if i == 0:
                    if (accented_wordforms[0].find('+') != -1) or (len(separate_tokens) == 2):
                        break
                    else:
                        accented_wordforms = []
        if (len(accented_wordforms) != 1) or (len(accented_wordforms_many) != 1):
            accented_wordforms = ['-'.join(accented_wordforms)]
            new_accented_wordforms_many = []
            for combination in list(itertools.product(*accented_wordforms_many[1:])):
                new_accented_wordforms_many.append('-'.join(combination))
            accented_wordforms_many = new_accented_wordforms_many
        else:
            accented_wordforms = [accented_wordforms[0]]
            accented_wordforms_many = accented_wordforms_many[0]
        if cur_token in accented_wordforms:
            accented_wordforms = [accented_wordforms[accented_wordforms.index(cur_token)]]
            if warn != '':
                if warn == 'many':
                    err_msg = f'Word `{cur_token}` has too many accent variants!'
                else:  # warn == 'no':
                    err_msg = f'Word `{cur_token}` is unknown!'
                if self.exception_for_unknown:
                    raise ValueError(err_msg)
                self.__bad_words.append(cur_token)
                warnings.warn(err_msg)
        accented_phrases = []
        if n > 1:
            if self.mode == 'one':
                for vt in self.__do_accents(words_list[1:], None if morphotags_list is None else morphotags_list[1:]):
                    accented_phrases.append([accented_wordforms[0]] + vt)
            else:
                for cur_accent in accented_wordforms_many:
                    for vt in self.__do_accents(words_list[1:], None if morphotags_list is None else morphotags_list[1:]):
                        accented_phrases.append([cur_accent] + vt)
        else:
            if self.mode == 'one':
                accented_phrases.append([accented_wordforms[0]])
            else:
                for cur_accent in accented_wordforms_many:
                    accented_phrases.append([cur_accent])
        return accented_phrases
