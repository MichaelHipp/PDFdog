"""PDF Dog. Show a pdf and track changes.

Usage:
  pdfdog [-q|-l] <filename>
  pdfdog (-h | --help)
  pdfdog --version

Options:
  -h --help     Show this screen.
  -q            Quiet. Don't print informative messages. The default.
  -l            Log informative messages to stdout.
  --version     Show version.
"""
from __future__ import print_function
import os
import time
import sys
import tempfile
import subprocess
import shlex
import shutil
import datetime

from docopt import docopt

from version import __VERSION__


POLL_INTERVAL = 0.100  # how often to poll for pdf changes


def log(*args):
    """Simple logging routine that can be silenced by cli argument."""
    global QUIET
    if not QUIET:
        print(*args)

def copy_file(filename):
    """Copy the given file (a pdf hopefully), to a temporary file so it can
    be opened by the pdf viewer without locking the source pdf file. Return
    the name (full path) of the temporary file."""
    with open(filename, 'r') as infile, \
        tempfile.NamedTemporaryFile(suffix='.pdf', prefix='pdfdog_',
                                    delete=False, mode='w') as outfile:
        shutil.copyfileobj(infile, outfile, -1)
    return outfile.name  # temp file name

def get_launch_cmd():
    """Get the executable spec for the default viewer for pdfs. This varies by
    platform. Currently only Windows."""
    # TODO see http://stackoverflow.com/questions/434597/open-document-with-default-application-in-python

    # this is for Windows
    # Get the file type associated with file extension .pdf, returns
    #  something like '.pdf=AcroExch.Document.11\r\n'
    a = subprocess.check_output('assoc .pdf', shell=True)
    b = a.strip().split('=')[1]  # get file type, like 'AcroExch.Document.11'
    # Get the executable with full path for that file type, returns like
    #  'AcroExch.Document.11="C:\\Program Files (x86)\\Adobe\\Reader 11.0\\Reader\\AcroRd32.exe" "%1"\r\n'
    c = subprocess.check_output('ftype %s' % b, shell=True)
    d = c.split('=')[1]  # get the string to the right of '='
    launch_cmd = shlex.split(d)[0]  # get just executable with full path
    log("Command: %s" % launch_cmd)
    return launch_cmd

def terminate(viewer, temp_file):
    # If viewer currently showing a file, end it
    if viewer:
        log("Terminate.")
        viewer.terminate()
    # if existing temp file, delete it
    #TODO find some clever way to not let this loop forever
    while True:
        try:
            # if the temp file exists, delete it
            if temp_file and os.path.isfile(temp_file):
                os.remove(temp_file)
            break  # temp file deleted
        except WindowsError:
            # keep trying to kill the viewer
            viewer.terminate()
            viewer.kill()
            continue  # try again to delete temp file

def launch(cmd, filename):
    """Launches the pdf viewer (given by cmd) on the given file name. Returns
    the Popen object for the pdf viewer process."""
    log("View: %s" % filename)
    viewer = subprocess.Popen((cmd, filename))
    log("Viewer PID: %s" % viewer.pid)
    return viewer

def poll(filename, old_mtime):
    """Polls the given filename and waits for it to come into existence and for
    the modification time to advance
    Return:
     Modification time if file is ready to view
     None if file does not exist or not ready to view
    """
    if os.path.isfile(filename):
        mtime = datetime.datetime.fromtimestamp(os.stat(filename).st_mtime)
        if mtime > old_mtime:
            return True, mtime
    time.sleep(POLL_INTERVAL)
    return False, old_mtime

def main(arguments):
    """The main loop."""
    # extract file name
    filename = arguments['<filename>']
    # make sure we got something resembling a file name string
    if not filename:
        log("***Must specify a valid file name, got: %s" % filename)
        sys.exit(1)
    log("Filename: %s" % filename)

    # determine the executable to use to launch/view the pdf (platform specific)
    cmd = get_launch_cmd()

    # set modification time to the far past to guarantee good comparison
    mtime = datetime.datetime.min

    temp_file = None  # no temp file to view initially
    viewer = None  # no pdf viewer initially active

    while True:
        try:
            # poll for changes in the pdf file or wait for it to appear
            view, mtime = poll(filename, mtime)
            # if ready to view (file updated, came into existence)
            if view:
                # terminate existing viewer, if any, and delete temp file
                terminate(viewer, temp_file)
                # copy pdf file to temp file
                temp_file = copy_file(filename)
                # show the file in the pdf viewer
                viewer = launch(cmd, temp_file)
        except KeyboardInterrupt:
            # we got a ctrl-c, this indicates normal termination
            terminate(viewer, temp_file)  # get rid of viewer and temp file
            break
        except:
            # something unexpected happened, clean up and pass the error along
            terminate(viewer, temp_file)  # get rid of viewer and temp file
            raise


if __name__ == '__main__':
    # parse command line args
    arguments = docopt(__doc__, version='PDF Dog %s' % __VERSION__)
    QUIET = arguments['-q'] or not arguments['-l']
    log("Args:", arguments)
    main(arguments)
