import xml.etree.cElementTree as ET
from docx import Document
from tools import get_delimiter, word_tokenize, get_punctuation, get_key
from book import Book, Chapter, Verse, Word
from keys import get_rows


def create_xml(file_path):
    try:
        document = Document(f'{file_path}')
    except:
        print("Given filepath is incorrect. Try again...")

    # ვქმნით XML თეგებს
    tei = ET.Element('tei', dict(xmlns_http='//www.tei-c.org/ns/1.0', xmlns_vg='http://www.vangoghletters.org/ns/'))
    teiheader = ET.SubElement(tei, 'teiheader', xmlns_xsi='http://www.w3.org/2001/XMLSchema-instance')
    facsimile = ET.SubElement(tei, 'facsimile', xmlns_xsi='http://www.w3.org/2001/XMLSchema-instance')
    text = ET.SubElement(tei, 'text')
    body = ET.SubElement(text, 'body', dict(xmlns_xsi='http://www.w3.org/2001/XMLSchema-instance'))
    div = ET.SubElement(body, 'div', dict(type="original", xml_lang="ka"))
    pb = ET.SubElement(div, 'pb', dict(f="1r", n="1", xml_id="pb-orig-1r-1", facs="#zone-pb-1r-1"))
    chapters_list = []
    chapter_num = ''


    # გამოყოფს თავებს დოკუმენტის პარაგრაფებიდან
    for chapter_text in document.paragraphs:

        if chapter_text.text.startswith('თავი'):
            # ვინახავთ თავების სათაურებს XML თეგებში
            ab = ET.SubElement(div, 'ab', dict(rend="indent")).text = chapter_text.text
            chapter_num = chapter_text.text.replace('თავი', '')

        if not chapter_text.text.startswith('თავი') and chapter_text.text != '' and chapter_text.text != ' ' and chapter_text.text != '\n' and chapter_text.text != '\t' and chapter_text.text != '\xa0' and chapter_text.text != '\n\xa0':
            try:
                print(f'Enter annotations file path for chapter {chapter_num}')
                anot_file_path = input()
            except:
                print("Given filepath is incorrect. Try again...")

            try:
                print(f'Enter the last key')
                count = int(input())
            except:
                print("Key value must be a number. Try again...")
            keys, count = get_rows(anot_file_path, count)
            print(f'Last generated key was: {count}')

            # ვამატებთ თითოეული თავის XML თეგს
            ab = ET.SubElement(div, 'ab', dict(rend="indent"))
            verses_list = []
            if chapter_text.text is not None:
                # ვიყენებთ დელიმიტერის ფუნქციას მუხლების გამოსაყოფად და ვყოფთ თავს მუხლებად
                delimiter = get_delimiter(chapter_text.text)
                verses = chapter_text.text.split(delimiter)

                for v in verses:
                    words_list = []
                    if delimiter is not None and v != "\n" and v and v != "":

                        # ვიღებთ მუხლს თითოეული თავიდან და ვამატებთ XML თეგს
                        verse_text = f'{delimiter}{v}'

                        # ვიყენებთ ფუნქციას თითოეული მუხლის რიგითი ნომრის წამოსაღებად
                        key = get_key(verse_text)

                        if key == "":
                            continue
                        else:
                            verse_numbers = key.split(',')
                            lb = ET.SubElement(div, 'lb', dict(n=verse_numbers[1], xml_id=f"l-{verse_numbers[1]}"))
                            ab = ET.SubElement(div, 'ab')

                            # ვიყენებთ nltk ბიბლიოთეკის ფუნქციას სიტყვების ტოკენიზაციისთვის
                            words = word_tokenize(verse_text)
                            for word_text in words:
                                if word_text != ' ' and word_text != '':
                                    if word_text != key:
                                        word = Word()
                                        if word_text.startswith('['):
                                            rs = ET.SubElement(ab, 'rs', type="pers")
                                            supplied = ET.SubElement(rs, 'supplied', reason="damaged")
                                            damaged_words = word_text.split(']')
                                            supplied.text = damaged_words[0].replace('[', '')
                                            supplied_list = []
                                            supplied_list.append(damaged_words[0].replace('[', ''))
                                            word.supplied = supplied_list
                                            supplied.tail = damaged_words[1]

                                        else:
                                            punc = get_punctuation(word_text)
                                            if punc:
                                                word_text = word_text.replace(punc, '')
                                            rs = ET.SubElement(ab, 'rs')

                                            rs.text = word_text
                                            word.value = word_text
                                            for dict_item in keys:
                                                for k, list_item in dict_item.items():
                                                    if word_text in list_item[3] and key.replace(',', '.') == list_item[0] and word_text not in list_item[7]:
                                                        word.key = k
                                                        rs.attrib = dict(type="pers", key=f'{k}')
                                                        list_item[7] += f'{word_text}'
                                                        break
                                                else:
                                                    continue
                                                break
                                            rs.tail = punc
                                        words_list.append(word)

                        verse = Verse()
                        verse.verse_number = key
                        verse.words = words_list
                        verses_list.append(verse)

            chapter = Chapter()
            chapter.chapter_number = key
            chapter.verses = verses_list
            chapters_list.append(chapter)

    book = Book()
    book.name = 'ტობის წიგნი'
    book.chapters = chapters_list
    tree = ET.ElementTree(tei)

    tree.write("tobit-oshki.xml", encoding='utf-8')
    return book


