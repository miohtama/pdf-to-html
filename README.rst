.. contents :: :local:

Introduction
----------------

This is a Python script to convert a PDF to series of images with alt texts.
It makes the presentation suitable embedded for a blog post and reading on a mobile device and such.

My workflow:

* Export presentation from Keynote to PDF. On Export dialog untick *include date* and *add borders around slides*.

* Convert PDFs to JPEGs using Ghostscript

* Scrape `<img>` alt texts using

* Insert optional image full URL prefix, so you don't need to manually link images to the hosting service

* Copy-paste generated HTML to your blog post

Tested with Apple Keynote exported PDFs, but the approach should work for any PDF content.

Installation
--------------

Dependencies (OSX)::

    sudo port install ghostscript

Please note that Ghostscript 9.06 crashed for me during the export. Please upgrade to 9.07.

Setting up virtualenv and insllating the code:

    git clone xxx
    cd pdf-presentation-to-html
    curl -L -o virtualenv.py https://raw.github.com/pypa/virtualenv/master/virtualenv.py
    python virtualenv.py venv
    . venv/bin/activate
    pip install pyPdf

Usage
----------

Example::

    . venv/bin/activate
    python pdf2html.py test.pdf output

Advanced example::

    . venv/bin/activate
    python pdf2html.py test.pdf output


Author
--------------

Mikko Ohtamaa (`blog <https://opensourcehacker.com>`_, `Facebook <https://www.facebook.com/?q=#/pages/Open-Source-Hacker/181710458567630>`_, `Twitter <https://twitter.com/moo9000>`_, `Google+ <https://plus.google.com/u/0/103323677227728078543/>`_)


