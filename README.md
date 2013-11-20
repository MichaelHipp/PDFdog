PDFDog
======
This is a small utility program that will bring up the default viewer for
a pdf file, and then watch the file for any changes. When the file is modified
it restarts the viewer to show the updated pdf.

    pdfdog myfile.pdf

It will then "dog" that pdf.

Rationale
---------
I routinely write applications in Django or wxPython that produce lots of
complicated pdf layouts via ReportLab.  The design and layout is an iterative
process (ready, fire, aim!). So I needed a pdf viewer that would automatically
show the updated pdf every time I run it.

I develop mostly on Windows and Adobe Reader is the defacto standard viewer -
but it has an annoying habit of locking whatever file it's showing. So before
you can do a run to produce a new pdf, you must remember to close Reader, and
then immediately restart it once the new file is created. It really slows
down the work flow. PDFDog works around this problem by first copying the pdf
to a temp file and displaying that, then when the target pdf changes it
copies that one and restarts.

It tries to remove the temp files when they are no longer needed.

Usage
-----

    Usage:
        pdfdog [-q|-l] <filename>
        pdfdog (-h | --help)
        pdfdog --version

    Options:
        -h --help     Show this screen.
        -q            Quiet. Don't print informative messages. The default.
        -l            Log informative messages to stdout.
        --version     Show version.

It is intended to be run from the CLI. Just hit CTRL-C to exit the program.

Limitations
-----------
Works only on Windows for now. It tries really hard to find the default viewer
from the Windows registry and use that; there shouldn't be problems if the
viewer is properly installed. To date I've only tested it on Windws 7 and using
Adobe Reader 11 ... but that will change.

Downloads
---------
There is a Windows binary available here:
It does not need to be installed, just put the executable somewhere in your path.

Otherwise, grab the code from github. The only dependency is docopt. I have only
run it on Python 2.7 so far.

License
-------
License: MIT license (see LICENSE.txt).

Social
------
Drop me a note if you find it useful. Or suggest any obvious improvements
that should be made.
