import xml.etree.cElementTree as ET
from docx import Document
from tools import get_delimiter, word_tokenize, get_punctuation, get_key


def create_xml(file_path):
    document = Document(f'{file_path}')

    # ვქმნით XML თეგებს
    tei = ET.Element('tei', dict(xmlns_http='//www.tei-c.org/ns/1.0', xmlns_vg='http://www.vangoghletters.org/ns/'))
    teiheader = ET.SubElement(tei, 'teiheader', xmlns_xsi='http://www.w3.org/2001/XMLSchema-instance')
    facsimile = ET.SubElement(tei, 'facsimile', xmlns_xsi='http://www.w3.org/2001/XMLSchema-instance')
    text = ET.SubElement(tei, 'text')
    body = ET.SubElement(text, 'body', dict(xmlns_xsi='http://www.w3.org/2001/XMLSchema-instance'))
    div = ET.SubElement(body, 'div', dict(type="original", xml_lang="ka"))
    pb = ET.SubElement(div, 'pb', dict(f="1r", n="1", xml_id="pb-orig-1r-1", facs="#zone-pb-1r-1"))

    # გამოყოფს თავებს დოკუმენტის პარაგრაფებიდან
    for chapter in document.paragraphs:

        if chapter.text.startswith('თავი'):
            # ვინახავთ თავების სათაურებს XML თეგებში
            ab = ET.SubElement(div, 'ab', dict(rend="indent")).text = chapter.text

        if not chapter.text.startswith('თავი') and chapter.text != '' and chapter.text != ' ' and chapter.text != '\n' and chapter.text != '\t' and chapter.text != '\xa0':

            # ვამატებთ თითოეული თავის XML თეგს
            ab = ET.SubElement(div, 'ab', dict(rend="indent"))

            if chapter.text is not None:
                # ვიყენებთ დელიმიტერის ფუნქციას მუხლების გამოსაყოფად და ვყოფთ თავს მუხლებად
                delimiter = get_delimiter(chapter.text)
                verses = chapter.text.split(delimiter)

                for v in verses:
                    if delimiter is not None and v != "\n" and v and v != "":

                        # ვიღებთ მუხლს თითოეული თავიდან და ვამატებთ XML თეგს
                        verse = f'{delimiter}{v}'

                        # ვიყენებთ ფუნქციას თითოეული მუხლის რიგითი ნომრის წამოსაღებად
                        key = get_key(verse)
                        if key == "":
                            continue
                        else:
                            verse_numbers = key.split(',')
                            lb = ET.SubElement(div, 'lb', dict(n=verse_numbers[1], xml_id=f"l-{verse_numbers[1]}"))
                            ab = ET.SubElement(div, 'ab')

                            # ვიყენებთ nltk ბიბლიოთეკის ფუნქციას სიტყვების ტოკენიზაციისთვის
                            words = word_tokenize(verse)
                            for word in words:
                                if word != ' ' and word != '':
                                    if word != key:
                                        # if word.startswith('['):
                                        #     rs = ET.SubElement(ab, 'rs', type="pers")
                                        #     supplied = ET.SubElement(rs, 'supplied', reason="damaged")
                                        #     damaged_word = word.split(']')
                                        #     supplied.text = damaged_word[0].replace('[', '')
                                        #     supplied.tail = damaged_word[1]
                                        # else:
                                        punc = get_punctuation(word)
                                        if punc:
                                            word = word.replace(punc, '')
                                        rs = ET.SubElement(ab, 'rs', type="pers")
                                        rs.text = word
                                        rs.tail = punc

    tree = ET.ElementTree(tei)

    tree.write("tobit-oshki.xml", encoding='utf-8')
