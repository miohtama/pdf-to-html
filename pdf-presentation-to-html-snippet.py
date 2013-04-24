"""

    PDF to blog post.

    Convert PDF presentation to a blog post friendly format:

    - HTML snippet

    - Series of extracted images

    - With alt tags

    Dependencies::

        sudo port install ghostscript

    Installation:

        git clone xxx
        cd pdf-presentation-to-html



"""

import os
import sys
import shutil
from StringIO import StringIO
from collections import defaultdict

from pdfminer.converter import LTTextItem, TextConverter
from pdfminer.pdfparser import PDFDocument, PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter

SLIDE_TEMPLATE = '<img src="{prefix}{src}" alt="{alt}" />'


def create_images(src, target, width=620, height=480):
    """ Create series of images from slides.

    :param src: Source PDF file

    :param target: Target folder
    """

    cmd = "gs -dNOPAUSE -sDEVICE=jpeg -sOutputFile=slide%%d.jpg" + \
          " -dJPEGQ=70 -r{width}x{height} -q {src} -c quit".format(locals())

    if os.system(cmd):
        raise RuntimeError("Command failed: %s" % cmd)


def scrape_text(src):
    """ Read PDF file and return plain text on each page.

    http://stackoverflow.com/questions/25665/python-module-for-converting-pdf-to-text

    :return: List of plain text unicode strings
    """

    pages = []

    class Scraper(TextConverter):

        def end_page(self, i):

            lines = defaultdict(lambda: {})
            for child in self.cur_item.objs:
                if isinstance(child, LTTextItem):
                    (_, _, x, y) = child.bbox
                    line = lines[int(-y)]
                    line[x] = child.text.encode(self.codec)

            for y in sorted(lines.keys()):
                line = lines[y]
                text = ("".join(line[x] for x in sorted(line.keys())))
                pages[i] = text

    rsrc = PDFResourceManager()
    outfp = StringIO()

    device = Scraper(rsrc, outfp, codec="utf-8")

    doc = PDFDocument()

    fp = open(src, 'rb')
    parser = PDFParser(fp)
    parser.set_document(doc)
    doc.set_parser(parser)
    doc.initialize('')

    interpreter = PDFPageInterpreter(rsrc, device)

    for i, page in enumerate(doc.get_pages()):
        outfp.write("START PAGE %d\n" % i)
        interpreter.process_page(page)
        outfp.write("END PAGE %d\n" % i)

    device.close()
    fp.close()


def create_index_html(target, slides, prefix):
    """
    """
    out = open(target, "wt")

    print >> out, "<!doctype html>"
    for i in xrange(0, len(slides)):
        alt = slides[i]  # ALT text for this slide
        params = dict(src="slide%d.jpg" % i, prefix=prefix, alt=alt)
        print >> out, SLIDE_TEMPLATE.format(params)


def main():
    """ """

    if len(sys.argv) < 3:
        sys.exit("Usage: pdf-presentation-to-html-snippet.py mypresentation.pdf targetfolder [image path prefix]")

    src = sys.argv[1]
    folder = sys.argv[2]

    if len(sys.argv) > 3:
        prefix = sys.argv[3]
    else:
        prefix = ""

    if not os.path.exists(folder):
        os.makedirs(folder)

    alt_texts = scrape_text(src)

    target_html = os.path.join(folder, "index.html")

    create_index_html(target_html, alt_texts, prefix)

    create_images(src, folder)


if __name__ == "__main__":
    main()