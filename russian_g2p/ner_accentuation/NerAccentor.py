import numpy as np
from ner_utils import load_place_stress_model, create_index_of_letters, create_morph_vector, create_index_of_con_vow


class NerAccentor:
  def __init__(self):
    self._place_stress_model = load_place_stress_model()

  def define_stress(self, word, morph_inf):
    all_word_vectors = [create_index_of_letters(word), create_morph_vector(morph_inf), create_index_of_con_vow(word)]
    stress_vector_two_list = np.asarray(self._place_stress_model.predict(all_word_vectors, verbose=1) >= 0.34,
                                        dtype=np.int32)  # список в списке
    stress_vector = stress_vector_two_list.reshape(stress_vector_two_list.shape[0], stress_vector_two_list.shape[1], )[
        0]
    stress_index = []
    for i in range(len(stress_vector)):
        if stress_vector[i] == 1:
            stress_index.append(i)

    word_with_stress = [letter for letter in word]
    words_return = []
    for index in stress_index:
        word_with_stress.insert(index + 1, '+')
        words_return.append(''.join(word_with_stress))
        word_with_stress.pop(index + 1)

    return words_return
