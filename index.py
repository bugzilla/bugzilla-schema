import make_schema_doc
from make_schema_doc import BzSchemaProcessingException
import schema_remarks

import cgi
import os
import re
import string
import io
import sys
import time
import html
import urllib.request, urllib.parse, urllib.error

# 1. GENERIC CGI SUPPORT FOR RAVENBROOK
#
# Adapted from issue.cgi.
#
# Objects belonging to the webpage class output a web page when their
# print_page() method is called.  Methods starting print_ actually print
# to stdout whereas methods starting prepare_ only prepare some portion
# of the output.  Subclasses of webpage should override the
# prepare_body() method so that it constructs an appropriate body for
# the web page (by making a series of calls to the b() method to
# accumulate lines of body text).
#
# The reason for constructing the whole body before printing anything is
# so that errors can be handled simply gracefully.  A method that
# encounters an error should call
#
#   raise error, (status, status_message, error_message)
#
# The status and status_message arguments to the error are used to make
# the HTTP status header: for example (404, 'Not found') or (400,
# 'Missing form parameter').  See [RFC 2616] for HTTP status codes.  The
# status_message is also used to make the page's title.  The
# error_message is used for the body of the page.
#
# The script supports two behaviours for other errors:
#
# 1. Leave them uncaught, causing the script to crash and an HTTP error
# log entry to be written by Apache.
#
# 2. Generate an error page as if by raise error, (500, 'Python error',
# exc_type + ': ' + exc_value).
#
# It's a security risk to give out detailed information about errors, so
# we use (1) on the public server and (2) on the internal server.
#
# The directory_links list is used to build the list of links in the
# header and footer of the outputted web page in the usual Ravenbrook
# format.  It is a list of pairs of (directory, description).
#
# This could be separated out into a module of its own.

class BzSchemaException(Exception):
    def __init__(self, status, status_message, error_message):
        super().__init__(error_message)
        self.status = status
        self.status_message = status_message
        self.error_message = error_message
    def __str__(self):
        return self.error_message

class webpage:
    body = ''                 # Page body
    body = None               # Body of page: list of strings.
    directory_links = None    # Directories to link to in header, footer
    h1 = None                 # Top-level header (if None, use title)
    status = 200              # HTTP status of output
    status_message = 'OK'     # Message to go with the status
    title = 'Web page'        # Page title
    debug_messages = []       # no debug messages yet!
    debug_level = 0           # don't accumulate any debug messages

    def __init__(self):
        self.body = []
        self.title = "Default webpage title"
        self.debug_messages = []
        self.debug_level = 0
        self.directory_links = [
            ]

    # Append a line of HTML to the body of the webpage.
    def b(self, s):
        self.body.append(s)

    # Check that the form parameters are correct.  This is a placeholder
    # that should be overridden in subclasses of webpage.
    def check_form_parameters(self):
        pass

    # Check and obtain the debugging level. This is a placeholder that
    # should be overridden in subclasses of webpage.
    def check_debug_level(self):
        pass

    # Print an 'Expires' header [RFC 2616, 14.21] specifying that the
    # page expires at midnight tonight.  The reason for expiring the
    # output is that the same query to this script (e.g., action=list)
    # may generate different output each time it's called.  Pages
    # lasting for a day means that people won't be misled by a cached
    # result from a long time ago.  The format for the date is specified
    # in [RFC 822, 5.1] and modified by [RFC 1123, 5.2.14]; a date looks
    # like "Thu, 01 Dec 1994 16:00:00 GMT".
    def print_expires(self):
        print('Expires:', end=' ')
        print(time.strftime("%a, %d %b %Y 00:00:00 GMT",
                            time.gmtime(time.time() + 60*60*24)))

    # Prepare the body of the webpage by making calls to the b() method.
    # This is a placeholder that should be overridden in subclasses of
    # webpage.
    def prepare_body(self):
        pass

    # Print the directory links that go at the top and bottom of the
    # page.
    def print_directory_links(self):
        print('<p>')
        url = ''
        separator = ''
        for dir, name in self.directory_links:
            url = url + dir + '/'
            print('%s<a href="%s">%s</a>' % (separator, url, name))
        separator = '/ '
        print('</p>')

    # Print the start of the webpage: the HTTP headers, the XML
    # declaration, the XHTML document type, the HTML <head/> element,
    # the directory links and the title.
    def print_header(self):
        print('Status:', self.status, self.status_message)
        print('Content-Type: text/html')
        print()
        print('<?xml version="1.0" encoding="UTF-8"?>')
        print ('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 '
               'Transitional//EN" "DTD/xhtml1-transitional.dtd">')
        print ('<html xmlns="http://www.w3.org/1999/xhtml" '
               'xml:lang="en" lang="en">')
        print('<head>')
        print('<title>', html.escape(self.title), '</title>')
        print('</head>')
        print ('<body bgcolor="#FFFFFF" text="#000000" link="#000099" '
               'vlink="#660066" alink="#FF0000">')
        print ('<a href="https://github.com/Ravenbrook/bugzilla-schema">'
               '<img style="position: absolute; top: 0; right: 0; border: 0;"'
               'src="https://s3.amazonaws.com/github/ribbons/forkme_right_red_aa0000.png"'
               'alt="Fork me on GitHub"></a>')
        print('<div align="center">')
        self.print_directory_links()
        print('<hr />')
        if self.h1:
            print('<h1>', self.h1, '</h1>')
        else:
            print('<h1>', html.escape(self.title), '</h1>')
        print('</div>')

    # Print the coyright message and the license conditions.
    def print_copyright(self):
        print ('<p><small>This document is copyright &copy; 2001-2013 '
               'Perforce Software, Inc.  All rights reserved.</small></p>\n')

        print ('<p><small>Redistribution and use of this document in any form, '
               'with or without modification, is permitted provided that '
               'redistributions of this document retain the above copyright '
               'notice, this condition and the following disclaimer.</small></p>\n')

        print('<p><small><strong>This document is provided by the copyright '
              'holders and contributors "as is" and any express or implied '
              'warranties, including, but not limited to, the implied warranties '
              'of merchantability and fitness for a particular purpose are '
              'disclaimed. In no event shall the copyright holders and '
              'contributors be liable for any direct, indirect, incidental, '
              'special, exemplary, or consequential damages (including, but '
              'not limited to, procurement of substitute goods or services; '
              'loss of use, data, or profits; or business interruption) '
              'however caused and on any theory of liability, whether in '
              'contract, strict liability, or tort (including negligence or '
              'otherwise) arising in any way out of the use of this document, '
              'even if advised of the possibility of such damage. '
              '</strong></small></p>\n')

    def log(self, level, message):
        if level <= self.debug_level:
            self.debug_messages.append(message)

    # Print any accumulated debugging log.
    def print_debug(self):
        if self.debug_level > 0:
            if self.debug_messages:
                print('<h3>Debugging Log:</h3>')
                print('<small>')
                for m in self.debug_messages:
                    print(self.format_text(m))
                    print('<br />')
                print('</small>')
            else:
                print('<h3>No Debugging Messages</h3>')
            print('<hr />')

    # Print the bottom of the webpage: the time the page was generated
    # (the is important because the contents may depend on the time the
    # page was created, and if the page is archived or printed readers
    # will need to know when the contents apply), the script that
    # generated the page, directory links, and closing tags.
    def print_footer(self):
        print('<hr />')
        self.print_debug()
        self.print_copyright()
        print('<div align="center">')
        self.print_directory_links()
        print('</div>')
        print('</body>')
        print('</html>')

    # Print the page by calling the check_form_parameters and
    # prepare_body methods, then printing the header, body and footer.
    # If an error occurs in check_form_parameters or prepare_body, an
    # error page is produced instead.
    def print_page(self):
        try:
            self.check_debug_level()
            self.check_form_parameters()
            self.prepare_body()
        except BzSchemaException as e:
            self.status = e.status
            self.status_message = e.status_message
            error_message = e.error_message
            self.title = self.status_message
            self.h1 = self.title
            self.body = ['<p>%s</p>' % error_message]
        except BzSchemaProcessingException as e:
            self.status = 500
            self.status_message = "Schema processing error"
            error_message = str(e)
            self.title = self.status_message
            self.h1 = self.title
            self.body = ['<p>%s</p>' % error_message]
        except Exception as e:
            error_type = type(e).__name__
            error_value = str(e)
            self.status = 500
            error_message = '%s: %s' % (error_type, error_value)
            self.status_message = 'Python error'
            self.title = self.status_message
            self.h1 = self.title
            self.body = ['<p>%s</p>' % error_message]
        self.print_header()
        for b in self.body:
            print(b)
        self.print_footer()

# 2. SCHEMA WEBPAGE CLASS
#
# This is a base class for all the schema webpage classes in section 3.

class schema_webpage(webpage):
    def __init__(self, form, action):
        # Call superclass method.
        webpage.__init__(self)
        self.action = action
        self.form = form
        self.directory_links.append(( '', 'Bugzilla Schema' ))

    # Return the form parameter named by parameter, as a string.  Return
    # None if there is no such parameter or if the parameter is the
    # empty string.
    def param(self, parameter):
        if parameter in self.form:
            if self.form[parameter].file:
                self.log(8, "Parameter %s: file type" % parameter)
                return None
            v = self.form[parameter].value
            if v:
                self.log(8, "Parameter %s: %s." % (parameter, str(v)))
                return str(v)
            else:
                self.log(8, "Parameter %s has no value." % parameter)
        self.log(6, "No parameter %s." % parameter)
        return None

    def check_bugzilla_version(self, param):
        version = self.param(param)
        if not version:
            raise BzSchemaException(400, 'Bad form parameters',
                          'No %s parameter.' % param)
        if not (version in schema_remarks.version_order):
            raise BzSchemaException(404, 'No such Bugzilla version',
                          'No such Bugzilla version: %s.'
                          % version)
        return version

    def check_bugzilla_from(self):
        self.from_version = self.check_bugzilla_version('from')

    def check_bugzilla_to(self):
        v = self.check_bugzilla_version('to')
        if (schema_remarks.version_order.index(v) >=
            schema_remarks.version_order.index(self.from_version)):
            self.to_version = v
        else:
            self.to_version = self.from_version
            self.from_version = v

    def check_bugzilla_single(self):
        self.version = self.check_bugzilla_version('version')

    # Get and check the debugging level.
    def check_debug_level(self):
        level = self.param('debug')
        if not level:
            level = '0'
        try:
            debug_level = int(level)
        except ValueError:
            raise BzSchemaException(404, 'Bad debugging level',
                          'Bad debugging level: %s.' % level)
        if debug_level < 0:
            level = 0
        self.debug_level = debug_level
        self.log(10, "Logging at debug level %d." % debug_level)


# 3. SCHEMA WEBPAGES
#
# Each subclass of schema_webpage implements a particular kind of report.

class range_webpage(schema_webpage):
    def check_form_parameters(self):
        self.check_bugzilla_from()
        self.check_bugzilla_to()

    def prepare_body(self):
        if self.from_version == self.to_version:
            self.title = ('Bugzilla Schema for Version %s' % self.from_version)
        else:
            self.title = ('Bugzilla Schema for Versions %s to %s' % (self.from_version,
                                                                     self.to_version))
        self.h1 = self.title
        self.b(make_schema_doc.make_body(self.from_version, self.to_version))
        
class single_webpage(schema_webpage):
    def check_form_parameters(self):
        self.check_bugzilla_single()

    def prepare_body(self):
        self.title = ('Bugzilla Schema for Version %s' % self.version)
        self.h1 = self.title
        self.b(make_schema_doc.make_body(self.version, self.version))

class index_webpage(schema_webpage):
    def prepare_body(self):
        # Page title.
        self.title = 'Bugzilla Schema Documentation'
        self.b('<div align="center">')

        self.b('<p>This service generates documentation for the database schema of '
               '<a href="http://bugzilla.org/">Bugzilla</a> defect-tracking software. '
               'It can produce documentation for the schema of any historical version, '
               'or of the schema changes between any two versions.</p>'
               '<p>It was written by staff at <a href="http://www.ravenbrook.com/">Ravenbrook '
               'Limited</a>, as part of the <a href="http://www.ravenbrook.com/project/p4dti">'
               'P4DTI</a> project under contract to <a href="http://www.perforce.com">Perforce, Inc.</a> '
               'The source code and data for this service are open source and available '
               'at <a href="http://github.com/Ravenbrook/bugzilla-schema">GitHub</a>.</p>')

        self.b('<table>')
        self.b('<tr><td>')
        self.b('<form action="" method="get">')
        self.b('<input name="action" value="single" type="hidden" />')
        self.b('<fieldset><legend>Schema for a single version</legend>')
        self.b('<select name="version">')
        self.options(schema_remarks.version_order, schema_remarks.default_last_version)
        self.b('</select>')
        self.b('<input name="view" value="View schema" type="submit" />')
        self.b('</fieldset>')
        self.b('</form>')
        self.b('</td></tr>')
        ####
        self.b('<tr><td>')
        self.b('<form action="" method="get">')
        self.b('<fieldset><legend>Schema for a range of versions</legend>')
        self.b('<input name="action" value="range" type="hidden" />')
        self.b('<select name="from">')
        self.options(schema_remarks.version_order, schema_remarks.default_first_version)
        self.b('</select>')
        self.b('<select name="to">')
        self.options(schema_remarks.version_order, schema_remarks.default_last_version)
        self.b('</select>')
        self.b('<input name="view" value="View schema" type="submit" />')
        self.b('</fieldset>')
        self.b('</form>')
        self.b('</td></tr>')
        ####
        self.b('</table>')
        self.b(f'<p>Note that this tool was just recently resurrected and is still in the process of being updated. While the version numbers are loaded for every version that currently exists, much of the schema data has not yet been loaded. The newest version currently available is {schema_remarks.default_last_version}.</p>')
        self.b('</div>')

    def options(self, options, selected = None):
        if selected == None:
            selected = options[-1]
        for o in options:
            l = '<option'
            if o == selected:
                l = l + ' selected="selected"'
            l = l + ' value="%s">%s</option>' % (o, o)
            self.b(l)


# 6. OUTPUT THE PAGE

action_class_map = {
    'single': single_webpage,
    'range': range_webpage,
    'index': index_webpage,
    }

def show_page():
    form = cgi.FieldStorage()
    if 'action' in form:
        action = form['action'].value
    else:
        action = 'index'
    if action in action_class_map:
        action_class = action_class_map[action]
    else:
        action_class = index_webpage
    action_class(form, action).print_page()

# A. REFERENCES
#
#
# B. DOCUMENT HISTORY
#
# 2004-11-12 NB  Adapted from issue.cgi.
# 
#
# C. COPYRIGHT AND LICENSE
#
# This file is copyright (c) 2004 Perforce Software, Inc.  All rights
# reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# 1.  Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#
# 2.  Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in
#     the documentation and/or other materials provided with the
#     distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDERS AND CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
# OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR
# TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
# DAMAGE.
#
#
# $Id$
