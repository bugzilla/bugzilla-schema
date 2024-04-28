How to Update
-------------

For any given release of Bugzilla, the process goes something like this:

- As of Bugzilla version 2.20, you can diff just a few files from one
  version to the next to see if there were schema changes.::

  > git diff --name-only release-2.20..release-2.22 -- Bugzilla/DB/Schema.pm Bugzilla/DB/Schema/Mysql.pm Bugzilla/Install/DB.pm

  If that gives you no output, there were no changes. If it lists files and
  you want to see the diffs, remove the ``--name-only`` flag and run it again.

- If you are *sure* there are none, just add the release to a few
  places in schema_remarks.py (``version_order``, ``version_schema_map``,
  ``version_remark``, the history section of ``afterword``, and possibly
  ``default_last_version``), and you're done.

  Search for 3.0.9 in schema_remarks.py to see the spots to update.

- If there are schema changes, or if you aren't sure, download the
  full Bugzilla release, do a vanilla install on your MySQL, then run
  ``./pickle_schema.py version db_name``.  For
  instance::

  > ./pickle_schema.py 3.8.12 bugs

  For this to work you will have to have MySQLdb (the Python MySQL interface
  library).  You can install it with ``pip install mysqlclient``.  It will use
  your database host and credentials from the ``[pickle_schema]`` section of
  ``.my.cnf`` in your home directory. For example

  .. code-block:: ini

   [pickle_schema]
   host=localhost
   user=bugs
   password=mypassword

  It will create a new pickle file in the pickles/ directory.  You should add
  that file to Git.  Note that you don't need access to MySQL on the web
  server.  You only need the pickle files.

- Then add the release to the main release tables in schema_remarks.py
  (``version_order``, ``version_schema_map``, ``version_remark``, and
  possibly ``default_last_version``).  Add a placeholder to the history
  section of ``afterword``.

- To validate that you got the version numbers entered in all the right
  spots, you can run::

  > ./make_schema_doc.py --validate

- Then get a plain schema doc, either through the CGI or by hand::

  > ./make_schema_doc.py 3.0.0 3.8.12 foo.html

  This will generate a list of errors, complaining about schema
  changes (new or removed tables, columns or indexes) which aren't
  documented in schema_remarks.py.  For *each* of these changes, you
  must look at the Bugzilla sources to figure out the effect of the
  change, add comments to schema_remarks.py accordingly, and add an
  item to the afterword section describing the change.

- The important thing here is to capture the semantics of a column or
  table.  The tool will automatically figure out its type and so on,
  but can't understand what it is *for*.  That's your job.  Use
  previous remarks as a style guide.

  In all text in schema_remarks.py, you should refer to columns using
  magic markers.  These will get converted into appropriate links,
  like this::

  %(table-bug_see_also)s                     "bug_see_also"
  %(the-table-bug_see_also)s                 "The table bug_see_also"
  %(column-fielddefs-buglist)s               "fielddefs.buglist"
  %(index-longdescs-longdescs_thetext_idx)s  "longdescs:longdescs_the_text_idx"

- Once you can generate a schema doc with no errors, you should look
  through it for schema changes which do not generate error messages.
  For instance, if a column type or default value changes, that change
  will show with colour highlighting in the automatic schema doc.  All
  such changes need to be documented.  If you generate a doc showing
  changes from the previous version to the new version, any changes
  will show up with colour, so they are easy to pick out by eye.

- At this point you have a working schema doc.  However, the ancillary
  notes might be out-of-date.  For instance, the description of the
  different kinds of custom fields, or the explanation of the groups
  system, might need updating.  You need to read through all the
  notes, making sure that they are current.  You might need to add new
  sections.

  The important part here is not to break the notes for old releases.
  If a user asks for documentation for version 2.12 (don't laugh: it
  happens) then that should still work: it shouldn't include any
  information which is only relevant to version 4.6.  Similarly, if a
  user asks for documentation showing the changes between 2.16 and
  3.4, everything relevant, and only the things relevant, to those
  versions needs to be shown, appropriately marked.
  
- Here are some examples.  Look at the "Groups" section of these:
  <http://www.ravenbrook.com/tool/bugzilla-schema/?action=range&from=2.8&to=2.12&view=View+schema#notes-groups>
  <http://www.ravenbrook.com/tool/bugzilla-schema/?action=range&from=2.8&to=3.2&view=View+schema#notes-groups>
  
  All those "From 2.10" and "Up to and including 2.8" and "From 2.12
  to 2.16" remarks, and the colours, are automatically generated and
  inserted using the magic versioning system in schema_remarks.  That
  "Groups" section, for example, is in schema_remarks.py from around
  line 3265 to around line 3565.  Wherever you have a piece of text
  which only applies to some schema versions, you need a new 3-tuple::
  
  (first_version, last_version, text)

  ``first_version`` can be None, meaning "from the beginning of time."
  ``last_version`` can be None, meaning "to the end of time".  And the
  ``text`` can contain the magic markers ``%(VERSION_STRING)s`` and/or
  ``%(VERSION_COLOUR)s``.
  
  ``%(VERSION_STRING)s`` turns into one of those remarks such as "From
  2.10".  The specific remark is constructed dynamically depending on
  the range of versions requested and also on those defined by
  ``first_version`` and ``last_version``.
  
  You will have to take care wording the notes so that it works as
  English text regardless of which version range has been requested.
