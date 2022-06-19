import numpy as np
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Embedding, Input, Dense, GRU, TimeDistributed
from tensorflow_addons.losses import SigmoidFocalCrossEntropy


alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
char_to_int = dict((c, i) for i, c in enumerate(alphabet, start=1))  # определяем буквы алфавита в цифры

pos_list = ['ADJ', 'ADP', 'ADV', 'AUX', 'CCONJ', 'CONJ','DET', 'INTJ', 'NOUN', 'NUM', 'PART', 'PRON', 'PROPN', 'SCONJ', 'VERB', 'X']
pos = 'ADJ ADP ADV AUX CCONJ CONJ DET INTJ NOUN NUM PART PRON PROPN SCONJ VERB X'  # список частей речи
pos_to_int = dict((pos.split(' ')[i], i) for i in range(len(pos.split(' '))))  # 16

features_list = [
'Abbr=Yes',
'Gender=Masc', 'Gender=Fem', 'Gender=Neut',
'Animacy=Anim', 'Animacy=Inan',
'Number=Sing', 'Number=Plur', 'Number=Ptan', 'Number=Coll',
'Case=Nom', 'Case=Gen', 'Case=Par', 'Case=Dat', 'Case=Acc', 'Case=Loc', 'Case=Ins', 'Case=Voc',
'Degree=Pos', 'Degree=Cmp', 'Degree=Sup',
'VerbForm=Conv', 'VerbForm=Fin', 'VerbForm=Inf', 'VerbForm=Part', 'VerbForm=PartRes', 'VerbForm=Trans',
'Mood=Ind', 'Mood=Imp', 'Mood=Cnd',
'Tense=Past', 'Tense=Pres', 'Tense=Fut',
'Aspect=Imp', 'Aspect=Perf',
'Voice=Act', 'Voice=Pass', 'Voice=Mid',
'Person=1', 'Person=2', 'Person=3',
'Variant=Full', 'Variant=Brev',
]
features = " ".join(features_list)  # список морф признаков
features_to_int = dict((features.split(' ')[i], i) for i in range(len(features.split(' '))))  # 41

vowels = 'аеёиоуыэюя'
consonants = 'бвгджзйклмнпрстфхцчшщъь'


class MaskCalculator(tf.keras.layers.Layer):
    def __init__(self, output_dim, **kwargs):
        self.output_dim = output_dim
        super(MaskCalculator, self).__init__(**kwargs)

    def build(self, input_shape):
        super(MaskCalculator, self).build(input_shape)

    def call(self, inputs, **kwargs):
        return tf.keras.backend.permute_dimensions(
            x=tf.keras.backend.repeat(
                x=tf.keras.backend.cast(
                    x=tf.keras.backend.greater(
                        x=inputs,
                        y=0
                    ),
                    dtype='float32'
                ),
                n=self.output_dim
            ),
            pattern=(0, 2, 1)
        )

    def compute_output_shape(self, input_shape):
        assert len(input_shape) == 1
        shape = list(input_shape)
        shape.append(self.output_dim)
        return tuple(shape)


def create_place_stress_model():
    input_words = Input(shape=(None,), name='InputWords', dtype='int32')  # (I) Архитекрутра модели
    embedding = Embedding(input_dim=len(alphabet) + 1, output_dim=256, mask_zero=True,
                          name='EmbeddingMaskForWords')  # шаг 1: маскирование матриц Цепочек Индексов Символов
    output_mask_words = embedding(input_words)

    input_morph_inf = Input(shape=(59,), name='InputMorphInf',
                            dtype='float32')  # шаг 2: вход матрицы векторов МорфИнф и обработка его Dense-слоем
    dense_morph_inf = Dense(units=256, name='DenseMorphInf')(
        input_morph_inf)  # подаем размерность без учёта мини-батчей

    gru = GRU(units=256, return_sequences=True, name='RecurrentLayerGRU')(output_mask_words,
                                                                          initial_state=dense_morph_inf)  # шаг 3: реккурентный слой

    input_cons_vow = Input(shape=(None,), name='InputConsonantVowel', dtype='int32')  # шаг 4: маскирование согласных
    output_mask_cons_vow = MaskCalculator(output_dim=256, trainable=False, name='OutMaskCalculator')(
        input_cons_vow)  # вручной слой маски
    masked_sequence_output = tf.keras.layers.Multiply(name='OutMaskMultiplicator')([output_mask_cons_vow, gru])
    masked_sequence_output = tf.keras.layers.Masking(name='OutMasking')(masked_sequence_output)

    cls_layer = TimeDistributed(  # шаг 5: слой TimeDistributed
        Dense(units=1, activation='sigmoid'),
        name='ClassificationLayer')(masked_sequence_output)

    place_stress_model = tf.keras.Model(
        inputs=[input_words, input_morph_inf, input_cons_vow],
        outputs=cls_layer,
        name='Placement_of_stress_model')

    place_stress_model.compile(loss=SigmoidFocalCrossEntropy(), optimizer='adam')  # (II) Скомпилирование модели
    # place_stress_model.summary()

    return place_stress_model


def load_place_stress_model():
  place_stress_model = create_place_stress_model()
  place_stress_model.load_weights(filepath='russian_g2p/ner_accentuation/Placement_of_stress_best_model.h5')  # russian_g2p/

  return place_stress_model


def create_index_of_letters(word):
  integer_encoded = []
  integer_encoded.append([char_to_int[char] for char in word if char != '-'])  # Integer Encoding: проводим для заданного слова целочисленное кодирование

  return np.array(integer_encoded, dtype='int32')


def create_morph_vector(morph_inf):
    if ' ' not in morph_inf:  # случай, если указана только половина информации: только часть речи / только морф инф
        if morph_inf in pos_list:
            integer_encoded_pos = pos_to_int[morph_inf.split(' ')[0]]  # созадаем вектор для части речи
            pos_vector = [0 for _ in range(len(pos.split(' ')))]  # 15
            pos_vector[integer_encoded_pos] = 1

            features_vector = [0 for _ in range(len(features.split(' ')))]
        else:
            pos_vector = [0 for _ in range(len(pos.split(' ')))]

            integer_encoded_features = []
            for char in morph_inf.split('|'):
                if '(2)' in char or '(3)' in char:
                    char = char[:-3]
                if char in features_list:
                    integer_encoded_features.append(features_to_int[char])
                else:
                    print(char, '1) эта морф информация отсутствует в ', morph_inf)
            features_vector = [0 for _ in range(len(features.split(' ')))]
            for value in integer_encoded_features:
                features_vector[value] = 1

    else:

        if morph_inf.split(' ')[0] in pos_list:
            integer_encoded_pos = pos_to_int[morph_inf.split(' ')[0]]  # созадаем вектор для части речи
            pos_vector = [0 for _ in range(len(pos.split(' ')))]  # 15
            pos_vector[integer_encoded_pos] = 1
        else:
            print('Нет такой части речи в списке: ', morph_inf.split(' ')[0])
            pos_vector = [0 for _ in range(len(pos.split(' ')))]

        if morph_inf.split(' ')[1] == '_' or morph_inf.split(' ')[
            1] == '_(2)':  # случай, в которых не указана морф инф, а только часть речи
            features_vector = [0 for _ in range(len(features.split(' ')))]
        else:
            integer_encoded_features = []
            for char in morph_inf.split(' ')[1].split('|'):
                if '(2)' in char or '(3)' in char:
                    char = char[:-3]
                if char in features_list:
                    integer_encoded_features.append(features_to_int[char])
                else:
                    print(char, 'эта морф информация отсутствует в ', morph_inf)
            features_vector = [0 for _ in range(len(features.split(' ')))]
            for value in integer_encoded_features:
                features_vector[value] = 1

    morph_inf_vector = pos_vector + features_vector

    morph_inf_vector_list = []
    morph_inf_vector_list.append(morph_inf_vector)
    return np.array(morph_inf_vector_list, dtype='float32')


def create_index_of_con_vow(word):
  one_hot_encoded = []
  for char in word:
     if char != '-':
       if char in vowels:
         one_hot_encoded.append(1)
       elif char in consonants:
         one_hot_encoded.append(0)

  one_hot_encoded_list = []
  one_hot_encoded_list.append(one_hot_encoded)
  return np.array(one_hot_encoded_list, dtype='int32')
