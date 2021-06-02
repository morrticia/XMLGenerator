from docx import Document
import xml.etree.cElementTree as ET


def get_rows(anot_file_path, count):
    doc = Document(f'{anot_file_path}')
    count += 1
    # "C:\\Users\\Pc\\Desktop\\F-13-anot.docx"
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

    columns_list = []
    headers = ['', 'Gr', 'Arm', 'O', 'Lemma', 'Gram', 'Eng', False]

    used_key = False
    used_word = ""
    for table in doc.tables:
        for row in table.rows:

            columns = []
            for cell in row.cells:
                text = cell.text
                text = text.replace('\xa0', '')
                text = text.replace('\n', '')
                columns.append(text)
            columns.append(used_word)
            item = {count: columns}
            if columns == headers:
                continue

            columns_list.append(item)

            word_id = 'P' + f'{count}'
            word = ET.SubElement(listperson, "word", id=word_id)
            lemma = ET.SubElement(word, 'lemma').text = f'ლემ. {columns[4]}'
            note = ET.SubElement(word, 'note')
            note.text = f'| {columns[3]} {columns[5]} | {columns[1]}'
            ref = ET.SubElement(note, 'ref').text = f'{columns[2]}'

            count += 1
    tree = ET.ElementTree(tei_words)

    tree.write("words.xml", encoding='utf-8')
    return columns_list, count
