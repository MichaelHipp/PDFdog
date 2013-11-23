PDFdog
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
down the work flow. PDFdog works around this problem by first copying the pdf
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

Bugs
----
 - If, before PDFdog is run, there is an existing pdf open in Adobe Reader,
then PDFdog will not be able to kill the appropriate pid and it will seem to do 
nothing when the pdf of interest changes.
 - If, after PDFdog is run, there is another Adobe Reader window opened, when
PDFdog terminates its window, that other Reader screen will also terminate.

This would seem to indicate Adobe Reader shouldn't be used for much of anything
else when PDFdog is running.

Downloads
---------
There is a Windows binary available in [Releases](https://github.com/MichaelHipp/PDFdog/releases).
It does not need to be installed, just put the executable somewhere in your path.

Otherwise, grab the code from github. The only dependency is docopt. I have only
run it on Python 2.7 so far.

License
-------
License: MIT license (see LICENSE.txt).

Future Enhancements
-------------------
A few things that might be good to implement:

 - Fix the aforementioned bug(s) above.
 - Get it working on Linux and Mac. How badly is it needed on these platforms
given that a big part of its reason for existing stems from the bad behavior
of Adobe Reader on Windows?
 - Enable an option to give it a python module and method to call to produce the
pdf.
 - Implement the excellent pdfviewer module from wxPython so this program could
show the pdf without needing an outside viewer (if nothing else, this improves
performance and reduces the amount of distracting screen activity).
