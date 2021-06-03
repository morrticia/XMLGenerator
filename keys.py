from docx import Document
import xml.etree.cElementTree as ET


def get_rows(anot_file_path, count):
    doc = Document(f'{anot_file_path}')
    # ინკრემენტი სიტყვებისთვის, key
    count += 1

    # ამატებს ძირითად XML თეგებს
    tei_words = ET.Element('tei', dict(xmlns_http='//www.tei-c.org/ns/1.0)'))
    teiheader_words = ET.SubElement(tei_words, 'teiheader')
    filedesc = ET.SubElement(teiheader_words, 'filedesc')
    titlestmt = ET.SubElement(filedesc, 'titlestmt')
    title = ET.SubElement(titlestmt, 'title').text = 'სიტყვების ანოტაციები'
    publicationstmt = ET.SubElement(filedesc, 'publicationstmt')
    p = ET.SubElement(publicationstmt, 'p')
    sourcedesc = ET.SubElement(filedesc, 'sourcedesc')
    p_source = ET.SubElement(sourcedesc, 'p')
    profiledesc = ET.SubElement(teiheader_words, 'profiledesc')
    listperson = ET.SubElement(profiledesc, 'listperson ')

    # ანოტაციების ცხრილიდან წამოღებული ყოველი რიგის ლისტისა და key-ის ლექსიკონების ლისტი
    columns_list = []
    # სვეტების სათაურები
    headers = ['', 'Gr', 'Arm', 'O', 'Lemma', 'Gram', 'Eng', False]
    # გამოყენებული სიტყვის სტრინგი, რომელიც ინახავს უკვე key მინიჭებულ სიტყვებს,
    # რათა მუხლში სიტყვის განმეორებისას იმგივე key არ მიანიჭოს სიტყვას
    used_word = ""
    for table in doc.tables:
        for row in table.rows:
            # თითოეული რიგიდან წამოღებული ანოტაცები
            columns = []
            for cell in row.cells:
                text = cell.text
                text = text.replace('\xa0', '')
                text = text.replace('\n', '')
                columns.append(text)
            columns.append(used_word)
            # key და value_ანოტაციებისგან შემდგარი ლექსიკონის შექმნა
            item = {count: columns}
            if columns == headers:
                continue

            columns_list.append(item)
            try:
                # XML თეგების დამატება words.xml-ში
                word_id = 'P' + f'{count}'
                word = ET.SubElement(listperson, "word", id=word_id)
                lemma = ET.SubElement(word, 'lemma').text = f'ლემ. {columns[4]}'
                note = ET.SubElement(word, 'note')
                note.text = f'| {columns[3]} {columns[5]} | {columns[1]}'
                ref = ET.SubElement(note, 'ref').text = f'{columns[2]}'
            except:
                print("Columns amount is not as expected: \n Chapter Number, Gr, Arm, O, Lemma, Gram, Eng")

            count += 1
    tree = ET.ElementTree(tei_words)

    tree.write("words.xml", encoding='utf-8')
    return columns_list, count
