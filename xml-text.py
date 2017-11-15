from bs4 import BeautifulSoup
from os import listdir

def main(inputDir, outputDir):
    for fileName in listdir(inputDir):
        if fileName.endswith(".xml"):
            file = open("{}/{}".format(inputDir, fileName))
            soup = BeautifulSoup(file, "xml")
            abstract = soup("abstract")[0]
            sections = soup("sec")
            exclude = ["acknowledgements","competinginterests","pre-publicationhistory"]
            sectionNum = 0
            abNum = 0
            newFile = open(("{}/{}_Abstract.txt".format(outputDir, fileName.split(".")[0])), 'w')
            if ((abstract.text).strip()).encode('utf-8') == "":
                newFile.write("[empty]")
            else:
                newFile.write(((abstract.text).strip()).encode('utf-8'))
            newFile.close
            for section in sections:
                sectionTitle = (section.find("title").text).replace(" ", "")
                if sectionTitle.lower() not in exclude:
                    if len(section.find_parents("sec")) == 0:
                            if len(section.find_parents("abstract")) > 0:
                                abNum = int(abNum) + 1
                            else:
                                sectionNum = int(sectionNum) + 1
                            if abNum < 10:
                                abNum = "0{}".format(abNum)
                            if sectionNum < 10:
                                sectionNum = "0{}".format(sectionNum)
                            if len(section.find_parents("abstract")) > 0:
                                newFile = open(("{}/{}_Abstract_Section{}_{}.txt".format(outputDir, fileName.split(".")[0], str(abNum), sectionTitle)), 'w')
                            else:
                                newFile = open(("{}/{}_Section{}_{}.txt".format(outputDir, fileName.split(".")[0], str(sectionNum), sectionTitle)), 'w')
                            if ((section.text).strip()).encode('utf-8') == "":
                                newFile.write("[empty]")
                            else:
                                newFile.write(((section.text).strip()).encode('utf-8'))
                            newFile.close
                    paragraphs = section("p")
                    if len(paragraphs) > 0:
                        if len(section.find_parents("abstract")) == 0:
                            for paragraph in paragraphs:
                                paragraphNum = paragraphs.index(paragraph) + 1
                                caption = ""
                                if len(paragraph.find_parents("caption")) > 0:
                                    caption = "_Caption"
                                if paragraphNum < 10:
                                    paragraphNum = "0{}".format(paragraphNum)
                                fileFormat = [outputDir, fileName.split(".")[0], sectionNum, sectionTitle, str(paragraphNum), caption]
                                newFile = open(("{}/{}_Section{}_{}_Paragraph{}{}.txt".format(*fileFormat)), 'w')
                                if ((paragraph.text).strip()).encode('utf-8') == "":
                                    newFile.write("[empty]")
                                else:
                                    newFile.write(((paragraph.text).strip()).encode('utf-8'))
                                newFile.close
if __name__ == '__main__':
    from sys import argv
    if len(argv) == 2:
        inputDir = argv[1]
        outputDir = argv[1]
        main(inputDir, outputDir)
    elif len(argv) == 3:
        inputDir = argv[1]
        outputDir = argv[2]
        main(inputDir, outputDir)
    else:
        print('python xml-text.py data_path')