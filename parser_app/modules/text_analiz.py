import re
from collections import Counter

import spacy
from iso639 import to_name
from langdetect import detect

from bs4 import BeautifulSoup
import requests


class TextAnalyzer:
    def __init__(self, text: str):
        self.text = text
        self.lang = detect(text)
        self.full_lang = to_name(self.lang).lower()
        self.spacy_lang_model = f'{self.lang.lower()}_core_news_sm'
        try:
            self.nlp = spacy.load(self.spacy_lang_model)
        except IOError:
            spacy.cli.download(self.spacy_lang_model)
            try:
                self.nlp = spacy.load(self.spacy_lang_model)
            except IOError:
                print('Unsupported language')

    def get_count_characters(self):
        """Количество символов"""
        count_char = len(self.text)
        return count_char

    def count_characters_without_spaces(self):
        """Количество символов без пробелов	"""
        total_characters_without_spaces = len([char for char in self.text if not char.isspace()])
        return total_characters_without_spaces

    def count_worlds(self):
        """Количество слов	"""
        word_list = re.findall(r'[^\W\d_]+', self.text)
        count_worlds = len(word_list)
        return count_worlds

    def count_unique_words(self):
        nlp = spacy.load(self.spacy_lang_model)  # Load the appropriate language model
        doc = nlp(self.text.lower())
        unique_words = set()
        for token in doc:
            if token.is_alpha:
                lemma = token.lemma_.lower()
                unique_words.add(lemma)

        return len(unique_words)

    def dict_significant_words(self):
        nlp = spacy.load(self.spacy_lang_model)
        # Получение списка стоп-слов из модели spaCy
        stop_words = nlp.Defaults.stop_words
        # Токенизация и лемматизация с помощью spaCy
        doc = nlp(self.text.lower())
        words = [token.lemma_ for token in doc if token.is_alpha and token.lemma_ not in stop_words]
        # Подсчет слов и выбор значимых слов с количеством вхождений >= 2
        word_counts = Counter(words)
        min_count = int(self.count_unique_words()/100) or 1
        significant_words_counts = {word: count for word, count in word_counts.items() if count >= min_count}
        return dict(sorted(significant_words_counts.items(), key=lambda item: item[1], reverse=True))

    def count_significant_words(self):
        return sum(self.dict_significant_words().values())

    def count_stop_words(self):
        return sum(self.dict_stop_words().values())

    def percent_stop_words(self):
        """Процент стоп слов"""
        return round(self.count_stop_words() / self.count_worlds() * 100, 2)

    def water(self):
        count_words = self.count_worlds()
        water = (count_words - self.count_significant_words()) / count_words
        return int(water * 10000) / 100

    def dict_stop_words(self):
        nlp = spacy.load(self.spacy_lang_model)  # Load the appropriate language model

        doc = nlp(self.text.lower())
        stopwords = nlp.Defaults.stop_words
        stop_words_list = [token.text for token in doc if token.text.lower() in stopwords]
        stop_words_list = Counter(stop_words_list)
        stop_words_list = sorted(dict(stop_words_list).items(), key=lambda x: x[1], reverse=True)
        return dict(stop_words_list)

    def generate_semantic_core(self):
        nlp = spacy.load(self.spacy_lang_model)  # Load the appropriate language model

        word_list = re.findall(r'[^\W\d_]+', self.text.lower())
        doc = nlp(' '.join(word_list))
        stopwords = set([token.lower() for token in nlp.Defaults.stop_words])
        words = [token.lemma_ for token in doc if token.is_alpha and token.lemma_ not in stopwords]
        doc = nlp(' '.join(words))

        filtered_words = [token.text.lower() for token in doc if
                          not token.is_stop and token.text.lower() not in stopwords]
        word_freq = Counter(filtered_words)
        min_word = int(self.count_unique_words()/100) + 1
        keywords = {word: count for word, count in word_freq.items() if count >= min_word}
        # Extract bigrams from the text using spaCy
        bigrams = [filtered_words[i] + " " + filtered_words[i + 1] for i in range(len(filtered_words) - 1)]
        # Calculate bigram frequency manually
        bigram_freq = Counter(bigrams)
        n_best_phrases = {phrase: count for phrase, count in bigram_freq.items() if count >= min_word + 1}
        # Adding phrases to the semantic core
        keywords.update(n_best_phrases)
        keywords = sorted(dict(keywords).items(), key=lambda x: x[1], reverse=True)
        return dict(keywords)

    def classic_nausea(self):
        return round(max(self.dict_significant_words().values()) ** 0.5, 2)

    def academic_nausea(self):
        return round(self.count_significant_words() / self.count_worlds() * 0.39 * 100, 2)

    def average_words_per_sentence(self):
        nlp = spacy.load("en_core_web_sm")  # Load the English model, replace with the appropriate language model

        doc = nlp(self.text)
        sentences = list(doc.sents)
        valid_sentences = [sentence.text for sentence in sentences if len(sentence.text.split()) > 1
                           and not sentence.text[:-1].isdigit()]
        # text = self.text.split()
        words_per_sentence = [len(sentence.split()) for sentence in valid_sentences]

        if len(words_per_sentence) == 0:
            return 0

        average_words = sum(words_per_sentence) / len(words_per_sentence)
        return round(average_words, 2)

    def count_paragraphs(self):
        paragraphs = re.split(r'\n\s*\n', self.text)
        # Remove leading and trailing whitespaces from each paragraph
        paragraphs = [paragraph.strip() for paragraph in paragraphs]
        # Remove empty paragraphs
        paragraphs = [paragraph for paragraph in paragraphs if paragraph]
        return len(paragraphs)


def text_analiz_pars(link):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(link, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    text = TextAnalyzer(text=str(soup.text))

    lst = []
    semantic_core = []
    significant_words = []
    stop_words = []

    lst.append(["Язык", f"{text.lang} {text.full_lang}"])
    lst.append(["Количество символов", text.get_count_characters()])
    lst.append(["Количество символов без пробелов", text.count_characters_without_spaces()])
    lst.append(["Количество слов", text.count_worlds()])
    lst.append(["Количество уникальных слов", text.count_unique_words()])
    lst.append(["Количество значимых слов", text.count_significant_words()])
    lst.append(["Количество стоп-слов", text.count_stop_words()])
    lst.append(["Процент стоп-слов", text.percent_stop_words()])
    lst.append(["Вода (%)", text.water()])
    lst.append(["Классическая тошнота документа", text.classic_nausea()])
    lst.append(["Академическая тошнота документа (%)", text.academic_nausea()])
    # lst.append(["Среднее количество слов в предложении", text.average_words_per_sentence()])
    lst.append(["Количество параграфов", text.count_paragraphs()])
    semantic_core.append(["Семантическое ядро", text.generate_semantic_core()])
    significant_words.append(["Значемые слова", text.dict_significant_words()])
    stop_words.append(["Словарь стоп-слов", text.dict_stop_words()])

    return lst, semantic_core, significant_words, stop_words


if __name__ == '__main__':
    import test_text

    text = test_text.text
    text = TextAnalyzer(text=str(text))
    print('Язык: ', text.lang, text.full_lang)
    print('Количество символов: ', text.get_count_characters())
    print('Количество символов без пробелов: ', text.count_characters_without_spaces())
    print('Количество слов: ', text.count_worlds())
    print('Количество уникальных слов: ', text.count_unique_words())
    print('Количество значимых слов: ', text.count_significant_words())
    print('Количество стоп-слов: ', text.count_stop_words())
    print('Процент стоп-слов: ', text.percent_stop_words())
    print('Вода (%): ', text.water())
    print('Классическая тошнота документа: ', text.classic_nausea())
    print('Академическая тошнота документа (%): ', text.academic_nausea())
    # print('Среднее количество слов в предложении: ', text.average_words_per_sentence())
    print('Количество параграфов: ', text.count_paragraphs())
    print('Семантическое ядро: ', text.generate_semantic_core())
    print('Значемые слова: ', text.dict_significant_words())
    print('Словарь стоп-слов: ', text.dict_stop_words())
