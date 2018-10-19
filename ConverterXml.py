from pathlib import Path
import xml.etree.ElementTree as ET
import sys

class ConverterXml:

    @staticmethod
    def convert(file_path):
        file = Path(file_path)
        if not file.exists() or not file.is_file():
            print("File doesn't exist")
            return

        extension = file.suffix

        if extension == '.txt':
            ConverterXml.__handle_txt(file)
        elif extension == '.xml':
            ConverterXml.__handle_xml(file)
        else:
            print("Wrong file extensions, expected extensions: .txt or .xml")
            return

        print("Done.")

    @staticmethod
    def __handle_txt(file):
        rows = ConverterXml.__read_txt(file.read_text())
        xml_data = ConverterXml.__to_xml(rows)
        new_file = file.with_suffix('.xml')
        new_file.write_text(xml_data)
        print("Wrote converted content to %s" % new_file.as_posix())

    @staticmethod
    def __handle_xml(file):
        rows = ConverterXml.__read_xml(file.read_text())
        txt_data = ConverterXml.__to_txt(rows)
        new_file = file.with_suffix('.txt')
        new_file.write_text(txt_data)
        print("Wrote converted content to %s" % new_file.as_posix())

    @staticmethod
    def __read_txt(data):
        rows = data.splitlines()
        for i in range(len(rows)):
            rows[i] = rows[i].split()
        return rows

    @staticmethod
    def __read_xml(data):
        xml = ET.fromstringlist(['<root>', data, '</root>'])

        rows = []
        for row in xml:
            columns = []
            for column in row:
                columns.append(column.text)
            rows.append(columns)
        return rows

    @staticmethod
    def __to_txt(rows):
        data = ""
        for row in rows:
            data += " ".join(row) + '\n'
        return data

    @staticmethod
    def __to_xml(rows):
        data = ""
        for row in rows:
            data += "<row>\n"
            for column in row:
                data += "<column>%s</column>\n" % column
            data += "</row>\n"
        return data


if len(sys.argv) != 2:
    print("Usage: %s <file>" % sys.argv[0])
    exit()

ConverterXml.convert(sys.argv[1])
