"""

    PDF to blog post.

    Convert PDF presentation to a blog post friendly format:

    - HTML snippet

    - Series of extracted images

    - With alt tags

    Dependencies (OSX)::

        sudo port install ghostscript

    Installation:

        git clone xxx
        cd pdf-presentation-to-html
        curl -L -o virtualenv.py https://raw.github.com/pypa/virtualenv/master/virtualenv.py
        python virtualenv.py venv
        . venv/bin/activate
        pip install pyPdf



"""

import os
import sys
import shutil
from StringIO import StringIO
from collections import defaultdict

import pyPdf

from pyPdf.pdf import ContentStream
from pyPdf.pdf import TextStringObject


SLIDE_TEMPLATE = u'<div class="slide"><img src="{prefix}{src}" alt="{alt}" /></div>'


def create_images(src, target, width=620, height=480):
    """ Create series of images from slides.

    http://right-sock.net/linux/better-convert-pdf-to-jpg-using-ghost-script/

    :param src: Source PDF file

    :param target: Target folder
    """

    if target.endswith("/"):
        target = target[0:-1]

    ftemplate = "%(target)s/slide%%d.jpg" % locals()

    cmd = "gs -dNOPAUSE -dPDFFitPage -sDEVICE=jpeg -sOutputFile=" + ftemplate + \
          " -dJPEGQ=70 -dDEVICEWIDTH=800 -dDEVICEHEIGHT=600  %(src)s -c quit" % locals()

    print "Executing: %s" % cmd
    if os.system(cmd):
        raise RuntimeError("Command failed: %s" % cmd)


def extract_text(self):
    """ Patched extractText() from pyPdf to put spaces between different text snippets.
    """
    text = u""
    content = self["/Contents"].getObject()
    if not isinstance(content, ContentStream):
        content = ContentStream(content, self.pdf)
    # Note: we check all strings are TextStringObjects.  ByteStringObjects
    # are strings where the byte->string encoding was unknown, so adding
    # them to the text here would be gibberish.
    for operands, operator in content.operations:
        if operator == "Tj":
            _text = operands[0]
            if isinstance(_text, TextStringObject):
                text += _text
        elif operator == "T*":
            text += "\n"
        elif operator == "'":
            text += "\n"
            _text = operands[0]
            if isinstance(_text, TextStringObject):
                text += operands[0]
        elif operator == '"':
            _text = operands[2]
            if isinstance(_text, TextStringObject):
                text += "\n"
                text += _text
        elif operator == "TJ":
            for i in operands[0]:
                if isinstance(i, TextStringObject):
                    text += i

        if text and not text.endswith(" "):
            text += " "  # Don't let words concatenate

    return text


def scrape_text(src):
    """ Read PDF file and return plain text on each page.

    http://stackoverflow.com/questions/25665/python-module-for-converting-pdf-to-text

    :return: List of plain text unicode strings
    """

    pages = []

    pdf = pyPdf.PdfFileReader(open(src, "rb"))
    for page in pdf.pages:
        text = extract_text(page)
        pages.append(text)

    return pages


def create_index_html(target, slides, prefix):
    """
    """

    out = open(target, "wt")

    print >> out, "<!doctype html>"
    for i in xrange(0, len(slides)):
        alt = slides[i]  # ALT text for this slide
        params = dict(src=u"slide%d.jpg" % i, prefix=prefix, alt=alt)
        line = SLIDE_TEMPLATE.format(**params)
        print >> out, line.encode("utf-8")

    out.close()


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

    print "Creating: " + target_html
    create_index_html(target_html, alt_texts, prefix)

    create_images(src, folder)


if __name__ == "__main__":
    main()
