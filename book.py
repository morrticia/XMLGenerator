from dataclasses import dataclass


@dataclass
class Word:
    def __init__(self):
        self.value = str
        self.key = str
        self.supplied = []

    def add_supplied(self, value):
        self.supplied.append(value)


@dataclass
class Verse:
    def __init__(self):
        self.verse_number = 0
        self.words = []

    def __repr__(self):
        return (f'{self.__class__.__name__}'
                f'(rank={self.verse_number!r}, suit={self.words!r})')

    def add_word(self, key, word):
        word_dict = {key: word}
        self.words.append(word_dict)


@dataclass
class Chapter:
    def __init__(self):
        self.chapter_number = ""
        self.verses = []

    def add_verse(self, key, verse):
        verse_dict = {key: verse}
        self.verses.append(verse_dict)


@dataclass
class Book:
    def __init__(self):
        self.name = ""
        self.chapters = []

    def add_chapter(self, key, chapter):
        chapter_dict = {key: chapter}
        self.chapters.append(chapter_dict)

