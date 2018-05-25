from bs4 import BeautifulSoup
from os import listdir


def strip_encode(text):
    return ((text).strip()).encode('utf-8')


def add_zero(text_num):
    return_num = text_num
    if int(return_num) < 10:
        return_num = f"0{return_num}"
    return return_num


def main(input_dir, output_dir):
    for file_name in listdir(input_dir):
        if file_name.endswith(".xml"):
            split_name = file_name.split(".")[0]
            file = open("{}/{}".format(input_dir, file_name))
            soup = BeautifulSoup(file, "xml")
            abstract = soup("abstract")[0]
            sections = soup("sec")
            exclude = ["acknowledgements",
                       "competinginterests",
                       "pre-publicationhistory"]
            section_num = 0
            ab_num = 0
            new_file = open((f"{output_dir}/{split_name}_Abstract.txt"), 'wb')
            if strip_encode(abstract.text) == "":
                new_file.write("[empty]")
            else:
                new_file.write(strip_encode(abstract.text))
            new_file.close
            for section in sections:
                section_title = ((section.find("title").text)
                                 .replace(" ", "").replace(':', ''))
                if section_title.lower() not in exclude:
                    if len(section.find_parents("sec")) == 0:
                        if len(section.find_parents("abstract")):
                            ab_num = int(ab_num) + 1
                        else:
                            section_num = int(section_num) + 1
                        ab_num = add_zero(ab_num)
                        section_num = add_zero(section_num)
                        if len(section.find_parents("abstract")):
                            file_format = [output_dir, split_name,
                                           ab_num, section_title]
                            new_file = open(
                                ("{}/{}_Abstract_Section{}_{}.txt"
                                 .format(*file_format)), 'wb')
                        else:
                            file_format = [output_dir, split_name,
                                           section_num, section_title]
                            new_file = open(
                                ("{}/{}_Section{}_{}.txt"
                                 .format(*file_format)), 'wb')
                        if strip_encode(section.text) == "":
                            new_file.write("[empty]")
                        else:
                            new_file.write(strip_encode(section.text))
                        new_file.close
                    paragraphs = section("p")
                    if len(paragraphs):
                        if len(section.find_parents("abstract")) == 0:
                            for paragraph in paragraphs:
                                paragraph_num = paragraphs.index(paragraph) + 1
                                caption = ""
                                if len(paragraph.find_parents("caption")):
                                    caption = "_Caption"
                                paragraph_num = add_zero(paragraph_num)
                                file_format = [output_dir, split_name,
                                               section_num, section_title,
                                               paragraph_num, caption]
                                new_file = open(
                                    ("{}/{}_Section{}_{}_Paragraph{}{}.txt"
                                     .format(*file_format)), 'wb')
                                if strip_encode(paragraph.text) == "":
                                    new_file.write("[empty]")
                                else:
                                    new_file.write(
                                        strip_encode(paragraph.text))
                                new_file.close


if __name__ == '__main__':
    from sys import argv
    if len(argv) == 2:
        input_dir = argv[1]
        output_dir = argv[1]
        main(input_dir, output_dir)
    elif len(argv) == 3:
        input_dir = argv[1]
        output_dir = argv[2]
        main(input_dir, output_dir)
    else:
        print('python xml-text.py input_directory output_directory')
