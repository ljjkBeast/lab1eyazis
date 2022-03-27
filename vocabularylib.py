import numpy as np
import nltk
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from string import punctuation
from nltk import pos_tag
from dataclasses import dataclass

pos_tags_definitions = {"CC"	:   "Coordinating conjunction",
                        "CD"	:   "Cardinal number",
                        "DT"	:   "Determiner",
                        "EX"	:   "Existential there",
                        "FW"	:   "Foreign word",
                        "IN"	:   "Preposition or subordinating conjunction",
                        "JJ"	:   "Adjective",
                        "JJR"	:   "Adjective",    #, comparative
                        "JJS"	:   "Adjective",    #, superlative
                        "LS"	:   "List item marker",
                        "MD"	:   "Modal",
                        "NN"	:   "Noun",    #, singular or mass
                        "NNS"	:   "Noun",    #, plural
                        "NNP"	:   "Proper noun, singular",
                        "NNPS"	:   "Proper noun, plural",
                        "PDT"	:   "Predeterminer",
                        "POS"	:   "Possessive ending",
                        "PRP"	:   "Personal pronoun",
                        "PRP$"	:   "Possessive pronoun",
                        "RB"	:   "Adverb",
                        "RBR"	:   "Adverb",    #, comparative
                        "RBS"	:   "Adverb",    #, superlative
                        "RP"	:   "Particle",
                        "SYM"	:   "Symbol",
                        "TO"	:   "to",
                        "UH"	:   "Interjection",
                        "VB"	:   "Verb",    #, base form
                        "VBD"	:   "Verb",    #, past tense
                        "VBG"	:   "Verb",    #, gerund or present participle
                        "VBN"	:   "Verb",    #, past participle
                        "VBP"	:   "Verb",    #, non-3rd person singular present
                        "VBZ"	:   "Verb",    #, 3rd person singular present
                        "WDT"	:   "Wh-determiner",
                        "WP"	:   "Wh-pronoun",
                        "WP$"	:   "Possessive wh-pronoun",
                        "WRB"	:   "Wh-adverb"}

@dataclass(eq=True, order=True, unsafe_hash=True)
class Lexeme:
    lemma: str
    part_of_speech: str
    endings: str
	
def get_words_from_text(text):
    words = []
    for sentence in nltk.sent_tokenize(text):
        for word in nltk.word_tokenize(sentence):
            if word not in punctuation:
                words.append(word)
    return words


def pos_tag_to_wordnet_tag(tag):
    if tag.startswith("J"):
        return "a"
    elif tag.startswith("N"):
        return "n"
    elif tag.startswith("V"):
        return "v"
    elif tag.startswith("RB"):
        return "r"
    else:
        return "-"


def get_lemmas_from_words_with_pos_tag(words_with_pos_tag):
    lemmas = []
    lemmatizer = WordNetLemmatizer()
    for word in words_with_pos_tag:
        wordnet_tag = pos_tag_to_wordnet_tag(word[1]) 
        if wordnet_tag == "-":
            wordnet_tag = "n"
        lemma = lemmatizer.lemmatize(word[0], wordnet_tag)
        lemmas.append((lemma, word[1]))
    return list(set(lemmas))


def generate_noun_endings(noun):
    endings = "'s (possessive), s (plural)"    # притяжательное, множественное число 
    return endings
    
    
def generate_verb_ending(verb):
    endings = "ing (gerund), ed (passive voice)"    # герундий, страдательный залог
    return endings


def generate_endings_for_words_with_pos_tag(words_with_pos_tag):
    endings = []
    for word in words_with_pos_tag:
        wordnet_tag = pos_tag_to_wordnet_tag(word[1])
        if wordnet_tag == "n":
            endings.append(generate_noun_endings(word[0]))
        elif wordnet_tag == "v":
            endings.append(generate_verb_ending(word[0]))
        else:
            endings.append("")
    return endings
	
def create_vocabulary_from_text(text):
    words = get_words_from_text(text)
    words_with_pos_tag = pos_tag(words)
    lemmas_with_pos_tag = get_lemmas_from_words_with_pos_tag(words_with_pos_tag)
    endings = generate_endings_for_words_with_pos_tag(lemmas_with_pos_tag)
    vocabulary = []
    for i in range(0, len(lemmas_with_pos_tag)):
        lexeme = Lexeme(lemmas_with_pos_tag[i][0].lower(), pos_tags_definitions[lemmas_with_pos_tag[i][1]].lower(), endings[i])
        vocabulary.append(lexeme)
    return vocabulary
	
def create_forms(lexeme):
    if lexeme.lemma == "be":
        return lexeme.lemma
    result = lexeme.lemma
    if lexeme.endings != "":
        endings = lexeme.endings.split(',')
        for ending in endings:
            ending = ending.strip()
            if ending.startswith("ing"):
                if lexeme.lemma.endswith("ie"):
                    result += ', ' + lexeme.lemma[:-2] + "ying"
                elif lexeme.lemma.endswith("e"):
                    result += ', ' + lexeme.lemma[:-1] + "ing"
                else:
                    result += ', ' + lexeme.lemma + "ing"
            elif ending.startswith("ed"):
                if lexeme.lemma.endswith("e"):
                    result += ', ' + lexeme.lemma[:-1] + "d"
                else:
                    result += ', ' + lexeme.lemma + "ed"
            elif ending.startswith("s"):
                if lexeme.lemma.endswith("ss") or lexeme.lemma.endswith("x") or lexeme.lemma.endswith("z") or lexeme.lemma.endswith("ch") or lexeme.lemma.endswith("sh") or lexeme.lemma.endswith("o"):
                    result += ', ' + lexeme.lemma + "es"
                else:
                    result += ', ' + lexeme.lemma + "s"
            else:
                result += ', ' + lexeme.lemma + ending.split(' ')[0]
    return result