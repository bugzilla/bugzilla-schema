#             Perforce Defect Tracking Integration Project
#              <http://www.ravenbrook.com/project/p4dti/>
#
#  SCHEMA-REMARKS.PY -- REMARKS FOR BUGZILLA SCHEMA DOCUMENTATION
#
#             Nick Barnes, Ravenbrook Limited, 2003-07-07
#
#
# 1. INTRODUCTION
#
# This module contains data structures holding remarks concerning
# the Bugzilla schema.  These remarks are automatically included in the
# Bugzilla schema doc by the code in  make_schema_doc.py.
#
# The intended readership is project developers.
#
# This document is not confidential.

import string
import re

# All the strings here are going to be passed to Python's % formatting
# operator, with a dictionary on the right-hand-side containing various
# strings which can therefore be automatically inserted.
#
# %(column-foo-bar)s turns into a link "foo.bar" to column bar of table foo.
#
# %(table-foo)s turns into a link "foo" to table foo.
#
# %(the-table-foo)s turns into "the foo table" where "foo" is a link
#  to table foo.
#
# and some other special-case strings such as VERSION_STRING,
# VERSION_COLOUR, and so on.

# Bugzilla versions which we know about, in order.

version_order = [
    '2.0',
    '2.2',
    '2.4',
    '2.6',
    '2.8',
    '2.10',
    '2.12',
    '2.14',
    '2.14.1',
    '2.14.2',
    '2.14.3',
    '2.14.4',
    '2.14.5',
    '2.16rc1',
    '2.16rc2',
    '2.16',
    '2.16.1',
    '2.16.2',
    '2.16.3',
    '2.16.4',
    '2.16.5',
    '2.16.6',
    '2.16.7',
    '2.16.8',
    '2.16.9',
    '2.16.10',
    '2.16.11',
    '2.17.1',
    '2.17.3', # there was no 2.17.2, see https://www.bugzilla.org/blog/2003/01/02/status-update/
    '2.17.4',
    '2.17.5',
    '2.17.6',
    '2.17.7',
    '2.18rc1',
    '2.18rc2',
    '2.18rc3',
    '2.18',
    '2.18.1',
    '2.18.2',
    '2.18.3',
    '2.18.4',
    '2.18.5',
    '2.18.6',
    '2.19.1',
    '2.19.2',
    '2.19.3',
    '2.20rc1',
    '2.20rc2',
    '2.20',
    '2.20.1',
    '2.20.2',
    '2.20.3',
    '2.20.4',
    '2.20.5',
    '2.20.6',
    '2.20.7',
    '2.21.1',
    '2.22rc1',
    '2.22',
    '2.22.1',
    '2.22.2',
    '2.22.3',
    '2.22.4',
    '2.22.5',
    '2.22.6',
    '2.22.7',
    '2.23.1',
    '2.23.2',
    '2.23.3',
    '2.23.4',
    '3.0rc1',
    '3.0',
    '3.0.1',
    '3.0.2',
    '3.0.3',
    '3.0.4',
    '3.0.5',
    '3.0.6',
    '3.0.7',
    '3.0.8',
    '3.0.9',
    '3.0.10',
    '3.0.11',
    '3.1.1',
    '3.1.2',
    '3.1.3',
    '3.1.4',
    '3.2rc1',
    '3.2rc2',
    '3.2',
    '3.2.1',
    '3.2.2',
    '3.2.3',
    '3.2.4',
    '3.2.5',
    '3.2.6',
    '3.2.7',
    '3.2.8',
    '3.2.9',
    '3.2.10',
    '3.3.1',
    '3.3.2',
    '3.3.3',
    '3.3.4',
    '3.4rc1',
    '3.4',
    '3.4.1',
    '3.4.2',
    '3.4.3',
    '3.4.4',
    '3.4.5',
    '3.4.6',
    '3.4.7',
    '3.4.8',
    '3.4.9',
    '3.4.10',
    '3.4.11',
    '3.4.12',
    '3.4.13',
    '3.4.14',
    '3.5.1',
    '3.5.2',
    '3.5.3',
    '3.6rc1',
    '3.6',
    '3.6.1',
    '3.6.2',
    '3.6.3',
    '3.6.4',
    '3.6.5',
    '3.6.6',
    '3.6.7',
    '3.6.8',
    '3.6.9',
    '3.6.10',
    '3.6.11',
    '3.6.12',
    '3.6.13',
    '3.7.1',
    '3.7.2',
    '3.7.3',
    '4.0rc1',
    '4.0rc2',
    '4.0',
    '4.0.1',
    '4.0.2',
    '4.0.3',
    '4.0.4',
    '4.0.5',
    '4.0.6',
    '4.0.7',
    '4.0.8',
    '4.0.9',
    '4.0.10',
    '4.0.11',
    '4.0.12',
    '4.0.13',
    '4.0.14',
    '4.0.15',
    '4.0.16',
    '4.0.17',
    '4.0.18',
    '4.1.1',
    '4.1.2',
    '4.1.3',
    '4.2rc1',
    '4.2rc2',
    '4.2',
    '4.2.1',
    '4.2.2',
    '4.2.3',
    '4.2.4',
    '4.2.5',
    '4.2.6',
    '4.2.7',
    '4.2.8',
    '4.2.9',
    '4.2.10',
    '4.2.11',
    '4.2.12',
    '4.2.13',
    '4.2.14',
    '4.2.15',
    '4.2.16',
    '4.3.1',
    '4.3.2',
    '4.3.3',
    '4.4rc1',
    '4.4rc2',
    '4.4',
    '4.4.1',
    '4.4.2',
    '4.4.3',
    '4.4.4',
    '4.4.5',
    '4.4.6',
    '4.4.7',
    '4.4.8',
    '4.4.9',
    '4.4.10',
    '4.4.11',
    '4.4.12',
    '4.4.13',
    '4.4.14',
    '4.5.1',
    '4.5.2',
    '4.5.3',
    '4.5.4',
    '4.5.5',
    '4.5.6',
    '5.0rc1',
    '5.0rc2',
    '5.0rc3',
    '5.0',
    '5.0.1',
    '5.0.2',
    '5.0.3',
    '5.0.4',
    '5.0.4.1',
    '5.0.5',
    '5.0.6',
    '5.2',
    '5.1.1', # yes, 5.1 comes after 5.2 in terms of schema progression
    '5.1.2', # 5.2 was actually forked from 5.0.6 instead of 5.1
    '5.3.3', # and thus, 5.1 was renamed to 5.3, but after 5.1.2 was out
    '5.9.1',
    ]

default_first_version = '4.2'
default_last_version = '4.2.16'


# Bugzilla schema versions.  A map from Bugzilla version to
# the version which introduces the schema used in that version.

version_schema_map = {
    '2.0': '2.0',
    '2.2': '2.2',
    '2.4': '2.4',
    '2.6': '2.6',
    '2.8': '2.8',
    '2.10': '2.10',
    '2.12': '2.12',
    '2.14': '2.14',
    '2.14.1': '2.14',
    '2.14.2': '2.14.2',
    '2.14.3': '2.14.2',
    '2.14.4': '2.14.2',
    '2.14.5': '2.14.2',
    '2.16rc1': '2.16',
    '2.16rc2': '2.16',
    '2.16': '2.16',
    '2.16.1': '2.16',
    '2.16.2': '2.16',
    '2.16.3': '2.16',
    '2.16.4': '2.16',
    '2.16.5': '2.16',
    '2.16.6': '2.16',
    '2.16.7': '2.16',
    '2.16.8': '2.16',
    '2.16.9': '2.16',
    '2.16.10': '2.16',
    '2.16.11': '2.16',
    '2.17.1': '2.17.1',
    '2.17.3': '2.17.3',
    '2.17.4': '2.17.4',
    '2.17.5': '2.17.5',
    '2.17.6': '2.17.5',
    '2.17.7': '2.17.7',
    '2.18rc1': '2.18rc1',
    '2.18rc2': '2.18rc1',
    '2.18rc3': '2.18rc3',
    '2.18': '2.18rc3',
    '2.18.1': '2.18.1',
    '2.18.2': '2.18.2',
    '2.18.3': '2.18.2',
    '2.18.4': '2.18.2',
    '2.18.5': '2.18.2',
    '2.18.6': '2.18.2',
    '2.19.1': '2.19.1',
    '2.19.2': '2.19.2',
    '2.19.3': '2.19.3',
    '2.20rc1': '2.20rc1',
    '2.20rc2': '2.20rc2',
    '2.20': '2.20rc2',
    '2.20.1': '2.20rc2',
    '2.20.2': '2.20rc2',
    '2.20.3': '2.20rc2',
    '2.20.4': '2.20rc2',
    '2.20.5': '2.20rc2',
    '2.20.6': '2.20rc2',
    '2.20.7': '2.20rc2',
    '2.21.1': '2.21.1',
    '2.22rc1': '2.22rc1',
    '2.22': '2.22rc1',
    '2.22.1': '2.22rc1',
    '2.22.2': '2.22rc1',
    '2.22.3': '2.22rc1',
    '2.22.4': '2.22rc1',
    '2.22.5': '2.22rc1',
    '2.22.6': '2.22rc1',
    '2.22.7': '2.22rc1',
    '2.23.1': '2.23.1',
    '2.23.2': '2.23.2',
    '2.23.3': '2.23.3',
    '2.23.4': '2.23.4',
    '3.0rc1': '2.23.4',
    '3.0': '2.23.4',
    '3.0.1': '2.23.4',
    '3.0.2': '2.23.4',
    '3.0.3': '2.23.4',
    '3.0.4': '2.23.4',
    '3.0.5': '2.23.4',
    '3.0.6': '2.23.4',
    '3.0.7': '2.23.4',
    '3.0.8': '2.23.4',
    '3.0.9': '2.23.4',
    '3.0.10': '2.23.4',
    '3.0.11': '2.23.4',
    '3.1.1': '3.1.1',
    '3.1.2': '3.1.2',
    '3.1.3': '3.1.3',
    '3.1.4': '3.1.4',
    '3.2rc1': '3.1.4',
    '3.2rc2': '3.1.4',
    '3.2': '3.1.4',
    '3.2.1': '3.1.4',
    '3.2.2': '3.1.4',
    '3.2.3': '3.1.4',
    '3.2.4': '3.1.4',
    '3.2.5': '3.1.4',
    '3.2.6': '3.1.4',
    '3.2.7': '3.1.4',
    '3.2.8': '3.1.4',
    '3.2.9': '3.1.4',
    '3.2.10': '3.1.4',
    '3.3.1': '3.3.1',
    '3.3.2': '3.3.2',
    '3.3.3': '3.3.2',
    '3.3.4': '3.3.4',
    '3.4rc1': '3.3.4',
    '3.4': '3.3.4',
    '3.4.1': '3.3.4',
    '3.4.2': '3.3.4',
    '3.4.3': '3.3.4',
    '3.4.4': '3.3.4',
    '3.4.5': '3.3.4',
    '3.4.6': '3.3.4',
    '3.4.7': '3.3.4',
    '3.4.8': '3.3.4',
    '3.4.9': '3.3.4',
    '3.4.10': '3.3.4',
    '3.4.11': '3.3.4',
    '3.4.12': '3.3.4',
    '3.4.13': '3.3.4',
    '3.4.14': '3.3.4',
    '3.5.1': '3.5.1',
    '3.5.2': '3.5.1',
    '3.5.3': '3.5.3',
    '3.6rc1': '3.5.3',
    '3.6': '3.5.3',
    '3.6.1': '3.5.3',
    '3.6.2': '3.5.3',
    '3.6.3': '3.5.3',
    '3.6.4': '3.5.3',
    '3.6.5': '3.5.3',
    '3.6.6': '3.5.3',
    '3.6.7': '3.5.3',
    '3.6.8': '3.5.3',
    '3.6.9': '3.5.3',
    '3.6.10': '3.5.3',
    '3.6.11': '3.5.3',
    '3.6.12': '3.5.3',
    '3.6.13': '3.5.3',
    '3.7.1': '3.7.1',
    '3.7.2': '3.7.2',
    '3.7.3': '3.7.2',
    '4.0rc1': '4.0rc1',
    '4.0rc2': '4.0rc1',
    '4.0': '4.0rc1',
    '4.0.1': '4.0rc1',
    '4.0.2': '4.0rc1',
    '4.0.3': '4.0rc1',
    '4.0.4': '4.0rc1',
    '4.0.5': '4.0rc1',
    '4.0.6': '4.0rc1',
    '4.0.7': '4.0rc1',
    '4.0.8': '4.0rc1',
    '4.0.9': '4.0rc1',
    '4.0.10': '4.0rc1',
    '4.0.11': '4.0rc1',
    '4.0.12': '4.0rc1',
    '4.0.13': '4.0rc1',
    '4.0.14': '4.0rc1',
    '4.0.15': '4.0rc1',
    '4.0.16': '4.0rc1',
    '4.0.17': '4.0rc1',
    '4.0.18': '4.0rc1',
    '4.1.1': '4.1.1',
    '4.1.2': '4.1.1',
    '4.1.3': '4.1.3',
    '4.2rc1': '4.2rc1',
    '4.2rc2': '4.2rc1',
    '4.2': '4.2',
    '4.2.1': '4.2.1',
    '4.2.2': '4.2.1',
    '4.2.3': '4.2.1',
    '4.2.4': '4.2.1',
    '4.2.5': '4.2.1',
    '4.2.6': '4.2.1',
    '4.2.7': '4.2.1',
    '4.2.8': '4.2.1',
    '4.2.9': '4.2.1',
    '4.2.10': '4.2.1',
    '4.2.11': '4.2.1',
    '4.2.12': '4.2.1',
    '4.2.13': '4.2.1',
    '4.2.14': '4.2.1',
    '4.2.15': '4.2.1',
    '4.2.16': '4.2.1',
    '4.3.1': 'not-yet-loaded',
    '4.3.2': 'not-yet-loaded',
    '4.3.3': 'not-yet-loaded',
    '4.4rc1': 'not-yet-loaded',
    '4.4rc2': 'not-yet-loaded',
    '4.4': 'not-yet-loaded',
    '4.4.1': 'not-yet-loaded',
    '4.4.2': 'not-yet-loaded',
    '4.4.3': 'not-yet-loaded',
    '4.4.4': 'not-yet-loaded',
    '4.4.5': 'not-yet-loaded',
    '4.4.6': 'not-yet-loaded',
    '4.4.7': 'not-yet-loaded',
    '4.4.8': 'not-yet-loaded',
    '4.4.9': 'not-yet-loaded',
    '4.4.10': 'not-yet-loaded',
    '4.4.11': 'not-yet-loaded',
    '4.4.12': 'not-yet-loaded',
    '4.4.13': 'not-yet-loaded',
    '4.4.14': 'not-yet-loaded',
    '4.5.1': 'not-yet-loaded',
    '4.5.2': 'not-yet-loaded',
    '4.5.3': 'not-yet-loaded',
    '4.5.4': 'not-yet-loaded',
    '4.5.5': 'not-yet-loaded',
    '4.5.6': 'not-yet-loaded',
    '5.0rc1': 'not-yet-loaded',
    '5.0rc2': 'not-yet-loaded',
    '5.0rc3': 'not-yet-loaded',
    '5.0': 'not-yet-loaded',
    '5.0.1': 'not-yet-loaded',
    '5.0.2': 'not-yet-loaded',
    '5.0.3': 'not-yet-loaded',
    '5.0.4': 'not-yet-loaded',
    '5.0.4.1': 'not-yet-loaded',
    '5.0.5': 'not-yet-loaded',
    '5.0.6': 'not-yet-loaded',
    '5.2': 'not-yet-loaded',
    '5.1.1': 'not-yet-loaded',
    '5.1.2': 'not-yet-loaded',
    '5.3.3': 'not-yet-loaded',
    '5.9.1': '5.9.1',
}

version_remark = [
    ('2.0', '1998-09-19', ''),
    ('2.2', '1999-02-10', ''),
    ('2.4', '1999-04-30', ''),
    ('2.6', '1999-08-30', ''),
    ('2.8', '1999-11-19', ''),
    ('2.10', '2000-05-09', ''),
    ('2.12', '2001-04-27', ''),
    ('2.14', '2001-08-29', ''),
    ('2.14.1', '2002-01-05', 'A security patch release.'),
    ('2.16rc1', '2002-05-10', 'A release candidate.'),
    ('2.16rc2', '2002-06-07', 'A release candidate.'),
    ('2.14.2', '2002-06-07', 'A security patch release.'),
    ('2.16', '2002-07-28', ''),
    ('2.14.3', '2002-07-28', 'A security patch release.'),
    ('2.16.1', '2002-09-30', 'A security patch release.'),
    ('2.14.4', '2002-09-30', 'A security patch release.'),
    ('2.17.1', '2002-11-25', 'A development release.'),
    ('2.16.2', '2003-01-02', 'A security patch release.'),
    ('2.14.5', '2003-01-02', 'A security patch release.'),
    ('2.17.3', '2003-01-02', 'A development release.'),
    ('2.16.3', '2003-04-25', 'A security patch release.'),
    ('2.17.4', '2003-04-25', 'A development release.'),
    ('2.17.5', '2003-11-03', 'A development release.'),
    ('2.16.4', '2003-11-03', 'A security patch release'),
    ('2.17.6', '2003-11-10', 'A development release.'),
    ('2.16.5', '2004-03-03', 'A security patch release'),
    ('2.17.7', '2004-03-03', 'A development release.'),
    ('2.16.6', '2004-07-10', 'A security patch release'),
    ('2.18rc1', '2004-07-10', 'A release candidate.'),
    ('2.18rc2', '2004-07-28', 'A release candidate.'),
    ('2.16.7', '2004-10-24', 'A security patch release'),
    ('2.18rc3', '2004-10-24', 'A release candidate.'),
    ('2.19.1', '2004-10-24', 'A development release.'),
    ('2.16.8', '2005-01-15', 'A security patch release'),
    ('2.18', '2005-01-15', ''),
    ('2.19.2', '2005-01-15', 'A development release.'),
    ('2.16.9', '2005-05-12', 'A security patch release'),
    ('2.18.1', '2005-05-12', 'A security patch release'),
    ('2.19.3', '2005-05-12', 'A development release.'),
    ('2.16.10', '2005-05-19', 'A security patch release'),
    ('2.18.2', '2005-07-08', 'A security patch release'),
    ('2.20rc1', '2005-07-08', 'A release candidate'),
    ('2.18.3', '2005-07-09', 'A security patch release'),
    ('2.20rc2', '2005-08-08', 'A release candidate'),
    ('2.18.4', '2005-10-01', 'A security patch release'),
    ('2.20', '2005-10-01', ''),
    ('2.21.1', '2005-10-01', 'A development release.'),
    ('2.16.11', '2006-02-21', 'A security patch release'),
    ('2.18.5', '2006-02-21', 'A security patch release'),
    ('2.20.1', '2006-02-21', 'A security patch release'),
    ('2.22rc1', '2006-02-21', 'A release candidate'),
    ('2.20.2', '2006-04-23', 'A security patch release'),
    ('2.22', '2006-04-23', ''),
    ('2.23.1', '2006-04-23', 'A development release.'),
    ('2.23.2', '2006-07-09', 'A development release.'),
    ('2.18.6', '2006-10-15', 'A security patch release'),
    ('2.20.3', '2006-10-15', 'A security patch release'),
    ('2.22.1', '2006-10-15', 'A security patch release'),
    ('2.23.3', '2006-10-15', 'A development release'),
    ('2.20.4', '2007-02-02', 'A security patch release'),
    ('2.22.2', '2007-02-02', 'A security patch release'),
    ('2.23.4', '2007-02-02', 'A development release'),
    ('3.0rc1', '2007-02-26', 'A release candidate'),
    ('3.0', '2007-05-09', ''),
    ('2.20.5', '2007-08-23', 'A security patch release'),
    ('2.22.3', '2007-08-23', 'A security patch release'),
    ('3.0.1', '2007-08-23', 'A security patch release'),
    ('3.1.1', '2007-08-23', 'A development release'),
    ('3.0.2', '2007-09-19', 'A security patch release'),
    ('3.1.2', '2007-09-19', 'A development release'),
    ('3.0.3', '2008-01-09', 'A patch release'),
    ('3.1.3', '2008-02-02', 'A development release'),
    ('2.20.6', '2008-05-04', 'A security patch release'),
    ('2.22.4', '2008-05-04', 'A security patch release'),
    ('3.0.4', '2008-05-04', 'A security patch release'),
    ('3.1.4', '2008-05-04', 'A development release'),
    ('2.22.5', '2008-08-12', 'A security patch release'),
    ('3.0.5', '2008-08-12', 'A security patch release'),
    ('3.2rc1', '2008-08-12', 'A release candidate'),
    ('2.20.7', '2008-11-07', 'A security patch release'),
    ('2.22.6', '2008-11-07', 'A security patch release'),
    ('3.0.6', '2008-11-07', 'A security patch release'),
    ('3.2rc2', '2008-11-07', 'A release candidate'),
    ('3.2', '2008-11-30', ''),
    ('3.3.1', '2009-01-06', 'A development release'),
    ('2.22.7', '2009-02-03', 'A security patch release'),
    ('3.0.7', '2009-02-03', 'A security patch release'),
    ('3.2.1', '2009-02-03', 'A security patch release'),
    ('3.0.8', '2009-02-03', 'A security patch release'),
    ('3.2.2', '2009-02-03', 'A security patch release'),
    ('3.3.2', '2009-02-03', 'A development release'),
    ('3.3.3', '2009-02-03', 'A security patch reease'),
    ('3.2.3', '2009-03-31', 'A security patch release'),
    ('3.3.4', '2009-03-31', 'A development release'),
    ('3.2.4', '2009-07-08', 'A security patch release'),
    ('3.4rc1', '2009-07-08', 'A release candidate'),
    ('3.4', '2009-07-28', ''),
    ('3.4.1', '2009-08-01', 'A security patch release'),
    ('3.0.9', '2009-09-11', 'A security patch release'),
    ('3.2.5', '2009-09-11', 'A security patch release'),
    ('3.4.2', '2009-09-11', 'A security patch release'),
    ('3.0.10', '2009-11-05', 'A patch release'),
    ('3.4.3', '2009-11-05', 'A patch release'),
    ('3.5.1', '2009-11-05', 'A development release'),
    ('3.4.4', '2009-11-18', 'A security patch release'),
    ('3.5.2', '2009-11-18', 'A development release'),
    ('3.0.11', '2010-01-31', 'A security patch release'),
    ('3.2.6', '2010-01-31', 'A security patch release'),
    ('3.4.5', '2010-01-31', 'A security patch release'),
    ('3.5.3', '2010-01-31', 'A development release'),
    ('3.6rc1', '2010-03-08', 'A release candidate'),
    ('3.4.6', '2010-03-08', 'A patch release'),
    ('3.6', '2010-04-13', ''),
    ('3.2.7', '2010-06-24', 'A security patch release'),
    ('3.4.7', '2010-06-24', 'A security patch release'),
    ('3.6.1', '2010-06-24', 'A security patch release'),
    ('3.7.1', '2010-06-24', 'A development release'),
    ('3.7.2', '2010-07-05', 'A development release'),
    ('3.2.8', '2010-08-05', 'A security patch release'),
    ('3.4.8', '2010-08-05', 'A security patch release'),
    ('3.6.2', '2010-08-05', 'A security patch release'),
    ('3.7.3', '2010-08-05', 'A development release'),
    ('3.2.9', '2010-11-02', 'A security patch release'),
    ('3.4.9', '2010-11-02', 'A security patch release'),
    ('3.6.3', '2010-11-02', 'A security patch release'),
    ('4.0rc1', '2010-11-02', 'A release candidate'),
    ('3.2.10', '2011-01-24', 'A security patch release'),
    ('3.4.10', '2011-01-24', 'A security patch release'),
    ('3.6.4', '2011-01-24', 'A security patch release'),
    ('4.0rc2', '2011-01-24', 'A release candidate'),
    ('4.0', '2011-02-15', ''),
    ('4.1.1', '2011-03-13', 'A development release'),
    ('3.4.11', '2011-04-27', 'A patch release'),
    ('3.6.5', '2011-04-27', 'A patch release'),
    ('4.0.1', '2011-04-27', 'A patch release'),
    ('4.1.2', '2011-04-27', 'A development release'),
    ('3.4.12', '2011-08-04', 'A security patch release'),
    ('3.6.6', '2011-08-04', 'A security patch release'),
    ('4.0.2', '2011-08-04', 'A security patch release'),
    ('4.1.3', '2011-08-04', 'A development release'),
    ('3.4.13', '2011-12-28', 'A security patch release'),
    ('3.6.7', '2011-12-28', 'A security patch release'),
    ('4.0.3', '2011-12-28', 'A security patch release'),
    ('4.2rc1', '2011-12-28', 'A release candidate'),
    ('3.4.14', '2012-01-31', 'A security patch release'),
    ('3.6.8', '2012-01-31', 'A security patch release'),
    ('4.0.4', '2012-01-31', 'A security patch release'),
    ('4.2rc1', '2012-01-31', 'A release candidate'),
    ('4.0.5', '2012-02-22', 'A patch release'),
    ('4.2', '2012-02-22', ''),
    ('3.6.9', '2012-04-18', 'A security patch release'),
    ('4.0.6', '2012-04-18', 'A security patch release'),
    ('4.2.1', '2012-04-18', 'A security patch release'),
    ('4.3.1', '2012-04-18', 'A development release'),
    ('3.6.10', '2012-07-26', 'A security patch release'),
    ('4.0.7', '2012-07-26', 'A security patch release'),
    ('4.2.2', '2012-07-26', 'A security patch release'),
    ('4.3.2', '2012-07-26', 'A development release'),
    ('3.6.11', '2012-08-30', 'A security patch release'),
    ('4.0.8', '2012-08-30', 'A security patch release'),
    ('4.2.3', '2012-08-30', 'A security patch release'),
    ('4.3.3', '2012-08-30', 'A development release'),
    ('3.6.12', '2012-11-13', 'A security patch release'),
    ('4.0.9', '2012-11-13', 'A security patch release'),
    ('4.2.4', '2012-11-13', 'A security patch release'),
    ('4.4rc1', '2012-11-13', 'A release candidate'),
    ('3.6.13', '2013-02-19', 'A security patch release'),
    ('4.0.10', '2013-02-19', 'A security patch release'),
    ('4.2.5', '2013-02-19', 'A security patch release'),
    ('4.4rc2', '2013-02-19', 'A release candidate'),
    ('4.2.6', '2013-05-22', 'A patch release'),
    ('4.4', '2013-05-22', ''),
    ('4.0.11', '2013-10-16', 'A security patch release'),
    ('4.2.7', '2013-10-16', 'A security patch release'),
    ('4.4.1', '2013-10-16', 'A security patch release'),
    ('4.5.1', '2013-10-16', 'A development release'),
    ('4.4.2', '2014-01-27', 'A patch release'),
    ('4.5.2', '2014-01-27', 'A development release'),
    ('4.0.12', '2014-04-17', 'A security patch release'),
    ('4.2.8', '2014-04-17', 'A security patch release'),
    ('4.4.3', '2014-04-17', 'A security patch release'),
    ('4.5.3', '2014-04-17', 'A development release'),
    ('4.0.13', '2014-04-18', 'A patch release'),
    ('4.2.9', '2014-04-18', 'A patch release'),
    ('4.4.4', '2014-04-18', 'A patch release'),
    ('4.5.4', '2014-04-18', 'A development release'),
    ('4.0.14', '2014-07-24', 'A security patch release'),
    ('4.2.10', '2014-07-24', 'A security patch release'),
    ('4.4.5', '2014-07-24', 'A security patch release'),
    ('4.5.5', '2014-07-24', 'A development release'),
    ('4.0.15', '2014-10-06', 'A security patch release'),
    ('4.2.11', '2014-10-06', 'A security patch release'),
    ('4.4.6', '2014-10-06', 'A security patch release'),
    ('4.5.6', '2014-10-06', 'A development release'),
    ('4.0.16', '2015-01-21', 'A security patch release'),
    ('4.2.12', '2015-01-21', 'A security patch release'),
    ('4.4.7', '2015-01-21', 'A security patch release'),
    ('5.0rc1', '2015-01-21', 'A release candidate'),
    ('4.0.17', '2015-01-27', 'A patch release'),
    ('4.2.13', '2015-01-27', 'A patch release'),
    ('4.4.8', '2015-01-27', 'A patch release'),
    ('5.0rc2', '2015-01-27', 'A release candidate'),
    ('4.0.18', '2015-04-15', 'A patch release'),
    ('4.2.14', '2015-04-15', 'A patch release'),
    ('4.4.9',  '2015-04-15', 'A patch release'),
    ('5.0rc3', '2015-04-15', 'A patch release'),
    ('5.0', '2015-07-07', ''),
    ('4.2.15', '2015-09-10', 'A security patch release'),
    ('4.4.10', '2015-09-10', 'A security patch release'),
    ('5.0.1', '2015-09-10', 'A security patch release'),
    ('4.2.16', '2015-12-22', 'A security patch release'),
    ('4.4.11', '2015-12-22', 'A security patch release'),
    ('5.0.2', '2015-12-22', 'A security patch release'),
    ('4.4.12', '2016-05-16', 'A security patch release'),
    ('5.0.3', '2016-05-16', 'A security patch release'),
    ('5.1.1', '2016-05-16', 'A development release'),
    ('4.4.13', '2018-02-16', 'A security patch release'),
    ('5.0.4', '2018-02-16', 'A security patch release'),
    ('5.1.2', '2018-02-16', 'A development release'),
    ('5.0.5', '2019-01-30', 'An invasive patch release'),
    ('5.0.6', '2019-02-09', 'An invasive patch release'),
    ('4.4.14', '2024-05-??', 'A security patch release'),
    ('5.0.4.1', '2024-05-??', 'A security patch release'),
    ('5.2', '2024-05-??', 'Forked from 5.0.6 not from 5.1.'),
    ('5.3.3', '2024-05-??', 'A development release following 5.1.2 (the branch was renamed)'),
    ('5.9.1', '2024-05-??', 'A development release'),
]

# This is a map from table name to an HTML remark concerning that
# table, which is output before the schema for that table.
#
# Tables with no attached remarks are given 'None' as a placeholder, so
# we know to add a remark later.

table_remark = {
    'attachments': 'Bug <a href="#notes-attachments">attachments</a>.',

    'attach_data': 'The content of <a href="#notes-attachments">attachments</a>.',

    'attachstatusdefs': 'Attachment status definitions.',

    'attachstatuses': 'Attachment statuses.',

    'audit_log': 'Changes to anything that subclasses Bugzilla::Object (such as users, products, components) get logged here. A class can exclude itself from being logged by including `use constant AUDIT_UPDATES => 1;` within the object .pm file. Attachments, Bugs, Comments, and Flags are excluded as they are tracked in %(table-bugs_activity)s.',

    'bug_group_map': 'Which bugs are in which groups.  See <a href="#notes-groups">the notes on groups</a>.',

    'bug_see_also': '<a href="#notes-see_also">Related bugs</a> in other Bugzillas.',

    'bug_severity': 'The severity values of bugs.',

    'bug_status': 'The status values of bugs.',

    'bugs': 'The bugs themselves.',

    'bugs_activity': '<a href="#notes-activity">Activity</a> on the bugs table.',

    'bugs_fulltext': 'All the descriptive text on bugs, to speed up searching.',

    'bz_schema': 'The database schema itself.',

    'category_group_map': 'Which groups does a user have to be in to view chart data in a given category.  See <a href="#notes-charts">the notes on charts</a>. ',

    'cc': 'Users who have asked to receive <a href="#notes-email">email</a> when a bug changes.',

    'component_cc': 'Users to put on the <a href="#notes-email">CC list</a> for a new bug in a given component.',

    'classifications': 'Product classifications. See <a href="#notes-products">the notes on products</a>.',

    'components': 'One row for each component.  See <a href="#notes-products">the notes on products and components.</a>',

    'dependencies': 'Which bugs <a href="#notes-dependencies">depend</a> on other bugs.',

    'duplicates': 'Which bugs are duplicates of which other bugs.',

    'email_setting': 'Per-user settings controlling when email is sent to that user.',

    'fielddefs': 'The properties of each bug field.',

    'field_visibility': 'Tracks when custom fields are visible based on other fields on the bug.',

    'flagexclusions': 'It may be forbidden to set a given flag on an item (bug or attachment) if that item is in a given product and/or component.  This table records such exclusions.  See the notes on <a href="#notes-flags">flags</a>.',

    'flaginclusions': 'An item (bug or attachment) may be required to be in a given product and/or component for a flag to be set.  This table records such requirements. See the notes on <a href="#notes-flags">flags</a>.',

    'flags': 'This table records the flags set on bugs or attachments. See the notes on <a href="#notes-flags">flags</a>.',

    'flagtypes': 'The types of flags available for bugs and attachments.  See the notes on <a href="#notes-flags">flags</a>.',

    'group_control_map': 'This table describes the relationship of groups to products (whether membership in a given group is required for entering or editing a bug in a given product).  See <a href="#notes-groups">the notes on groups</a>.',

    'group_group_map': 'Groups can be configured such that membership of one group automatically confers rights over some other groups.  This table records that configuration.  See <a href="#notes-groups">the notes on groups</a>.',

    'groups': 'This table describes a number of user groups.  Each group allows its members to perform a restricted activity.  See <a href="#notes-groups">the notes on groups</a>. ',

    'keyworddefs': 'Names and definitions of the keywords.  See <a href="#notes-keywords">the notes on keywords</a>.',

    'keywords': 'Bugs may have keywords.  This table defines which bugs have which keywords.  The keywords are defined in %(the-table-keyworddefs)s.',

    'logincookies': 'Bugzilla generates a cookie each time a user logs in, and uses it for subsequent authentication.  The cookies generated are stored in this table.  For more information, see <a href="#notes-authentication">the notes on authentication</a>.',

    'login_failure': 'Log of failed user login attempts. Records for a given user are cleared when they successfully log in. Users are locked out if they exceed MAX_LOGIN_ATTEMPTS in LOGIN_LOCKOUT_INTERVAL minutes (defined in Bugzilla::Constants).',

    'longdescs': 'Long bug <a href="#notes-descriptions">descriptions</a>.',

    'milestones': 'Development <a href="#notes-milestones">milestones</a>.',

    'namedqueries': 'Named <a href="#notes-namedqueries">queries</a>.',

    'namedquery_group_map': 'Controls whether a <a href="#notes-namedqueries">named query</a> is shared with other users (other members of a group).',

    'namedqueries_link_in_footer': 'Controls whether a <a href="#notes-namedqueries">named query</a> appears in a given user\'s navigation footer.',

    'op_sys': 'The possible values of the "operating system" field of a bug.',

    'priority': 'The possible values of the "priority" field of a bug.',

    'products': 'One row for each product.  See <a href="#notes-products">the notes on products.</a>',

    'profile_search': 'The most-recent SAVE_NUM_SEARCHES (defined in Bugzilla::Constants) searches a user has run are stored here, so that the Next/Prev links in a bug that was opened from a list will continue to work even if you have multiple browser tabs open with different searches.',

    'profile_setting': 'User preference settings.',

    'profiles': 'Describes Bugzilla <a href="#notes-users">users</a>.  One row per user.',

    'profiles_activity': 'This table is for recording changes to %(the-table-profiles)s. Currently it only records changes to group membership made with editusers.cgi.  This allows the administrator to track group inflation.  There is currently no code to inspect this table; only to add to it.',

    'quips': 'A table of <a href="#notes-quips">quips</a>.',

    'rep_platform': 'The possible values of the "platform" field of a bug.',

    'resolution': 'The possible values of the "resolution" field of a bug.',

    'series': 'Properties of the time-series datasets available (e.g. for plotting charts).  See <a href="#notes-charts">the notes on charts</a>.',

    'series_categories': None,

    'series_data': 'Data for plotting time-series charts.  See <a href="#notes-charts">the notes on charts</a>.',

    'setting': 'Identifies the set of user preferences.',

    'setting_value': 'Possible values for user preferences.',

    'shadowlog': 'A log of SQL activity; used for updating <a href="#notes-shadow">shadow databases</a>.',

    'status_workflow': 'Identifies allowable <a href="#notes-workflow">workflow</a> transitions.',

    'tag': None,

    'tags': None,

    'tokens': 'Tokens are sent to users to track activities such as creating new accounts and changing email addresses or passwords.  They are also sent to browsers and used to track workflow, to prevent security problems (e.g. so that one can only delete groups from a session last seen on a group management page).',

    'ts_error': 'A log of errors from TheSchwartz asynchronous job-queueing system.  Rows are aged out of this table after seven days.',

    'ts_exitstatus': 'A log of job completions from TheSchwartz asynchronous job-queueing system.',

    'ts_funcmap': 'The table of functions for TheSchwartz asynchronous job-queueing system.',

    'ts_job': 'The job queue managed by TheSchwartz asynchronous job-queueing system.',

    'ts_note': 'Notes on jobs for TheSchwartz asynchronous job-queueing system.  Apparently not used.',

    'user_group_map': 'This table records which users are members of each group, or can "bless" each group.  See <a href="#notes-groups">the notes on groups</a>.',

    'user_series_map': 'User subscriptions to time-series datasets.  See <a href="#notes-charts">the notes on charts</a>.',

    'versions': 'Product <a href="#notes-versions">versions</a>.',

    'votes': '<a href="#notes-voting">votes</a>.',

    'watch': '<a href="#notes-watchers">watchers</a>.',

    'whine_events': 'One row for each regular whine event. See <a href="#notes-whine">the notes on whining</a>.',

    'whine_queries': 'See <a href="#notes-whine">the notes on whining</a>.',

    'whine_schedules': 'See <a href="#notes-whine">the notes on whining</a>.',

}

table_added_remark = {
    'attachments': None,

    'attach_data': 'Speeding up attachment queries',

    'attachstatusdefs': None,

    'attachstatuses': None,

    'audit_log': None,

    'bug_group_map': 'Part of the new groups system',

    'bug_see_also': None,

    'bug_severity': 'Removing enumerated types',

    'bug_status': 'Removing enumerated types',

    'bug_tag': None,

    'bugs_fulltext': 'Improving full-text search speed',

    'bz_schema': None,

    'category_group_map': 'Part of the new charting system',

    'component_cc': None,

    'classifications': None,

    'dependencies': None,

    'duplicates': None,

    'email_setting': 'Replaces %(column-profiles-emailflags)s',

    'field_visibility': 'Replaced %(column-fielddefs-visibility_field_id)s',

    'fielddefs': None,

    'flagexclusions': 'Part of the new flags system',

    'flaginclusions': 'Part of the new flags system',

    'flags': 'Part of the new flags system',

    'flagtypes': 'Part of the new flags system',

    'group_control_map': 'Part of the new groups system',

    'group_group_map': 'Part of the new groups system',

    'groups': None,

    'keywords': None,

    'keyworddefs': None,

    'login_failure': 'Supporting new feature to lock out users who repeatedly fail logging in',

    'longdescs': None,

    'milestones': None,

    'namedqueries': None,

    'namedqueries_link_in_footer': 'Replacing %(column-namedqueries-linkinfooter)s',

    'namedquery_group_map': None,

    'op_sys': 'Removing enumerated types',

    'priority': 'Removing enumerated types',

    'products': None,

    'profile_search': None,

    'profile_setting': None,

    'profiles_activity': None,

    'quips': None,

    'rep_platform': 'Removing enumerated types',

    'resolution': 'Removing enumerated types',

    'series': 'Part of the new charting system',

    'series_categories': 'Part of the new charting system',

    'series_data': 'Part of the new charting system',

    'setting': None,

    'setting_value': None,

    'shadowlog': None,

    'status_workflow': 'Part of the custom workflow system',

    'tag': 'Renamed from %(table-tags)s',

    'tags': None,

    'tokens': None,

    'ts_error': 'For asynchronous mail',

    'ts_exitstatus': 'For asynchronous mail',

    'ts_funcmap': 'For asynchronous mail',

    'ts_job': 'For asynchronous mail',

    'ts_note': 'For asynchronous mail',

    'user_group_map': 'Part of the new groups system',

    'user_series_map': 'Part of the new charting system',

    'votes': None,

    'watch': None,

    'whine_events': 'Part of the new whine system',

    'whine_queries': 'Part of the new whine system',

    'whine_schedules': 'Part of the new whine system',

}

table_removed_remark = {
    'attachstatusdefs': 'replaced by the flag tables',

    'attachstatuses': ' replaced by the flag tables',

    'shadowlog': 'similar functionality now available using MySQL\'s replication facilities',

    'user_series_map': 'partially replaced by %(the-table-category_group_map)s',

    'votes': 'The Voting feature was moved to an extension. The table is not deleted on upgrade if it exists.',

    'tags': 'Was renamed to %(table-tag)s',
}

# This is a map from table name to a map from column name to HTML
# remark for that column.  At present, these remarks include schema
# change comments (which will eventually be generated automatically).
#
# Columns with no attached remarks are given 'None' as a placeholder,
# so we know to add a remark later.

column_remark = {
    'attachments': {
        'attach_id': 'a unique ID.',

        'bug_id': 'the bug to which this is attached (foreign key %(column-bugs-bug_id)s)',

        'creation_ts': 'the creation time.',

        'description': 'a description of the attachment.',

        'mimetype': 'the MIME type of the attachment.',

        'modification_time': 'the modification time of the attachment.',

        'ispatch': 'non-zero if this attachment is a patch file.',

        'isprivate': 'Non-zero if this attachment is "private", i.e. only visible to members of the "insider" group.',

        'isobsolete': 'Non-zero if this attachment is marked as obsolete.',

        'isurl': 'Non-zero if this attachment is actually a URL.',

        'filename': 'the filename of the attachment.',

        'thedata': 'the content of the attachment.',

        'submitter_id': 'the userid of the attachment (foreign key %(column-profiles-userid)s)',

        },

    'attach_data': {
        'id': 'The attachment id (foreign key %(column-attachments-attach_id)s).',

        'thedata': 'the content of the attachment.',

        },

    'attachstatusdefs': {
        'id': 'a unique ID.',

        'name': 'the name of the attachment status.',

        'description': 'The description of the attachment status.',

        'sortkey': 'A number used to determine the order in which attachment statuses are shown.',

        'product': 'The product for which bugs can have attachments with this status (foreign key %(column-products-product)s)',

        },

    'attachstatuses': {

        'attach_id': 'The id of the attachment (foreign key %(column-attachments-attach_id)s)',

        'statusid': 'The id of the status (foreign key %(column-attachstatusdefs-id)s)',

        },

    'audit_log': {

        'user_id': '',

        'class': 'The class of the item being modified (such as Bugzilla::User)',

        'object_id': 'The ID of the item such as the userid) that was modified',

        'field': 'The name of the field being modified',

        'removed': 'The value that was removed',

        'added': 'The value that was added',

        'at_time': 'Timestamp of the change',

        },
    'bug_group_map': {

        'bug_id': 'The bug id, (foreign key %(column-bugs-bug_id)s)',

        'group_id': 'The group id, (foreign key %(column-groups-id)s)',

        },

    'bug_see_also': {

        'bug_id': 'The bug id, (foreign key %(column-bugs-bug_id)s)',

        'id': 'A unique ID for the table row',

        'class': 'The class of the object defining the remote reference. Should be a subclass of Bugzilla::BugUrl.',

        'value': 'The URL of a related bug in another Bugzilla.',

    },

    'bug_severity': {

        'value': 'A possible value of the field',

        'isactive': '1 if this value is available in the user interface, 0 otherwise',

        'sortkey': 'A number used to determine the order in which values are shown.',

        'id': 'a unique ID.',

        'visibility_value_id': 'If set, this value is only available if the chooser field (identified by %(column-fielddefs-value_field_id)s) has the value with this ID.  Foreign key &lt;field&gt;.id, for example %(column-products-id)s or <a href="#column-customfield-id">cf_&lt;field&gt;.id</a>.',

        },

    'bug_status': {

        'value': 'A possible value of the field',

        'isactive': '1 if this value is available in the user interface, 0 otherwise',

        'sortkey': 'A number used to determine the order in which values are shown.',

        'is_open': '1 if the status is "Open", 0 if it is "Closed".',

        'id': 'a unique ID.',

        'visibility_value_id': 'If set, this value is only available if the chooser field (identified by %(column-fielddefs-value_field_id)s) has the value with this ID.  Foreign key &lt;field&gt;.id, for example %(column-products-id)s or <a href="#column-customfield-id">cf_&lt;field&gt;.id</a>.',
        },

    'bug_tag': {

        'bug_id': 'A bug with this tag applied to it. (foreign key %(column-bugs-bug_id)s)',

        'tag_id': [
            (None,'4.2rc1','The tag to apply to this bug. (foreign key %(column-tags-id)s)'),
            ('4.2rc2',None,'The tag to apply to this bug. (foreign key %(column-tag-id)s)'),
            ],
        },

    'bugs': {

        'area': 'The development area of the bug.',

        'bug_id': 'The bug ID.',

        'groupset': 'The groups which this bug occupies. Each group corresponds to one bit. See %(the-table-groups)s.',

        'assigned_to': 'The current owner of the bug  (foreign key %(column-profiles-userid)s).',

        'bug_file_loc': 'A URL which points to more information about the bug.',

        'bug_severity': ['See the <a href="#notes-severity">notes</a>.',
                         ('2.19.3', None, '%(VERSION_STRING)sforeign key %(column-bug_severity-value)s.'),
                         ],

        'bug_status': ['The <a href="#notes-workflow">workflow</a> status of the bug.',
                       ('2.19.3', None, '%(VERSION_STRING)sforeign key %(column-bug_status-value)s.'),
                       ],

        'creation_ts': 'The times of the bug\'s creation.',

        'delta_ts': 'The timestamp of the last update.  This includes updates to some related tables (e.g. %(the-table-longdescs)s).',

        'long_desc': 'A long description of the bug.',

        'short_desc': 'A short description of the bug.',

        'op_sys': ['The operating system on which the bug was observed.',
                   ('2.19.3', None, '%(VERSION_STRING)sforeign key %(column-op_sys-value)s.'),
                   ],

        'priority': ['The priority of the bug.',
                     (None, '2.19.2', '%(VERSION_STRING)s: P1 = most urgent, P5 = least urgent).'),
                     ('2.19.3', None, '%(VERSION_STRING)sforeign key %(column-priority-value)s.'),
                     ],

        'product': 'The product (foreign key %(column-products-product)s)',

        'product_id': 'The product (foreign key %(column-products-id)s)',

        'rep_platform': ['The platform on which the bug was reported.',
                         ('2.19.3', None, '%(VERSION_STRING)sforeign key %(column-rep_platform-value)s.'),
                         ],

        'reporter': 'The user who reported this (foreign key %(column-profiles-userid)s)',

        'version': 'The product version (foreign key %(column-versions-value)s)',

        'component': 'The product component (foreign key %(column-components-value)s)',

        'component_id': 'The product component (foreign key %(column-components-id)s)',

        'resolution': ['The bug\'s <a href="#notes-workflow">resolution</a>',
                       ('2.19.3', None, '%(VERSION_STRING)sforeign key %(column-resolution-value)s.'),
                       ],

        'target_milestone': 'The milestone by which this bug should be resolved.  (foreign key %(column-milestones-value)s)',

        'qa_contact': 'The QA contact (foreign key %(column-profiles-userid)s)',

        'status_whiteboard': 'This seems to be just a small whiteboard field.',

        'votes': 'The number of votes.',

        'keywords': 'A set of keywords.  Note that this duplicates the information in %(the-table-keywords)s. (foreign key %(column-keyworddefs-name)s)',

        'lastdiffed': 'The time at which information about this bug changing was last emailed to the cc list.',

        'everconfirmed': '1 if this bug has ever been confirmed.  This is used for validation of some sort.',

        'reporter_accessible': '1 if the reporter can see this bug (even if in the wrong group); 0 otherwise.',

        'assignee_accessible': '1 if the assignee can see this bug (even if in the wrong group); 0 otherwise.',

        'qacontact_accessible': '1 if the QA contact can see this bug (even if in the wrong group); 0 otherwise.',

        'cclist_accessible': '1 if people on the CC list can see this bug (even if in the wrong group); 0 otherwise.',

        'estimated_time': 'The original estimate of the total effort required to fix this bug (in hours).',

        'remaining_time': 'The current estimate of the remaining effort required to fix this bug (in hours).',

        'alias': 'An alias for the bug which can be used instead of the bug number.',

        'deadline': 'The deadline for this bug (a date).',

        },

    'bugs_activity': {

        'bug_id': 'Which bug (foreign key %(column-bugs-bug_id)s)',

        'who': 'Which user (foreign key %(column-profiles-userid)s)',

        'when': 'When was the change made?',

        'bug_when': 'When was the change made?',

        'field': 'What was the field?',

        'fieldid': 'What was the fieldid? (foreign key %(column-fielddefs-id)s)',

        'attach_id': 'If the change was to an attachment, the ID of the attachment (foreign key %(column-attachments-attach_id)s)',

        'oldvalue': 'The head of the old value.',

        'newvalue': 'The head of the new value.',

        'added': 'The new value of this field, or values which have been added for multi-value fields such as %(column-bugs-keywords)s,  %(the-table-cc)s, and %(the-table-dependencies)s',

        'removed': 'The old value of this field, or values which have been removed for multi-value fields such as %(column-bugs-keywords)s, %(the-table-cc)s, and %(the-table-dependencies)s',

        'comment_id': 'The comment on the bug that was made at the same time as or most-recently previous to this change. (foreign key %(column-longdescs-comment_id)s)',

        },

    'bugs_fulltext': {

        'bug_id': 'Which bug (foreign key %(column-bugs-bug_id)s)',

        'short_desc': 'The bug\'s short description (%(column-bugs-short_desc)s)',

        'comments': 'The bug\'s comments, concatenated (%(column-longdescs-thetext)s)',

        'comments_noprivate': 'Those comments visible to non-members of the "insider" group (i.e. with %(column-longdescs-isprivate)s zero).',
        },

    'bz_schema': {

            'version': 'The version number of the abstract schema data structures.  This is <em>not</em> the schema version; it does not change as tables, columns, and indexes are added and removed.',

            'schema_data': 'A Perl Storable (serialized version) of the abstract schema.',
            },

    'category_group_map': {

        'category_id': 'The series category (foreign key %(column-series_categories-id)s)',

        'group_id': 'The group.  (foreign key %(column-groups-id)s)',

        },

    'cc': {

        'bug_id': 'The bug (foreign key %(column-bugs-bug_id)s)',

        'who': 'The user (foreign key %(column-profiles-userid)s)',

        },

    'classifications': {

        'id': 'The classification id.',

        'name': 'The classification name.',

        'description': 'A description of the classification',

        'sortkey': 'A number used to determine the order in which classifications are shown.',

        },

    'components': {

        'name': 'The component id.',

        'id': 'The component id.',

        'value': 'The component name.',

        'program': 'The product (foreign key %(column-products-product)s)',

        'product_id': 'The product (foreign key %(column-products-id)s)',

        'initialowner': ['The default initial owner of bugs in this component.  On component creation, this is set to the user who creates the component.',
                         (None,  '2.10', '%(VERSION_STRING)sforeign key %(column-profiles-login_name)s.'),
                         ('2.12', None , '%(VERSION_STRING)sforeign key %(column-profiles-userid)s.'),
                         ],

        'initialqacontact': ['The initial "qa_contact" field for bugs of this component. Note that the use of the qa_contact field is optional, parameterized by Param("useqacontact").',
                             (None,  '2.10', '%(VERSION_STRING)sforeign key %(column-profiles-login_name)s.'),
                             ('2.12', None,  '%(VERSION_STRING)sforeign key %(column-profiles-userid)s.'),
                             ],

        'description': 'A description of the component.',

        'isactive': '1 if this component is available for new bugs, 0 if not.',

        },

    'component_cc': {

        'component_id': 'The component id (foreign key %(column-components-id)s).',

        'user_id': 'The user id (foreign key %(column-profiles-userid)s).',

        },

    'dependencies': {

        'blocked': 'Which bug is blocked (foreign key %(column-bugs-bug_id)s)',

        'dependson': 'Which bug does it depend on (foreign key %(column-bugs-bug_id)s)',

        },

    'duplicates': {

        'dupe_of': 'The bug which is duplicated (foreign key %(column-bugs-bug_id)s)',

        'dupe': 'The duplicate bug (foreign key %(column-bugs-bug_id)s)',

        },

    'email_setting': {

        'user_id': 'The user to whom this setting applies (foreign key %(column-profiles-userid)s).',

        'relationship': 'The relationship between the user and the bug.  0: Assignee; 1: QA contact; 2: Reporter; 3: CC; 4: Voter; 100: for global events, which do not depend on a relationship.',

        'event': 'The event on which an email should be sent.  1: added or removed from this capacity; 2: new comments are added; 3: new attachment is added; 4: attachment data is changed; 5: severity, priority, status, or milestone are changed; 6: resolved or reopened; 7: keywords change; 8: CC list changed; 0: any other change.<br><br>These are overridden and an email is not sent in the following circumstances, unless a suitable row is also present: 50: if the bug is unconfirmed; 51: if the change was by this user.<br><br>Global events are 100: a flag has been requested of this user; 101: This user has requested a flag.',

        },

    'field_visibility': {

        'field_id': 'ID of the field to match (foreign key %(column-fielddefs-id)s)',

        'value_id': 'ID of the value to match?  TODO',

        },

    'fielddefs': {

        'id': 'primary key for this table',

        'name': 'field name or definition (some fields are names of other tables or of fields in other tables).',

        'description': 'long description',

        'mailhead': 'whether or not to send the field description in mail notifications.',

        'sortkey': 'the order of fields in mail notifications.',

        'obsolete': '1 if this field no longer exists, 0 otherwise.',

        'type': ['The field type. 0 (FIELD_TYPE_UNKNOWN) for most non-custom fields.',
                 ('2.23.1', None, '%(VERSION_STRING)s1 (FIELD_TYPE_FREETEXT) for a single-line text field. '),
                 ('2.23.3', None, '%(VERSION_STRING)s2 (FIELD_TYPE_SINGLE_SELECT) for a single-select field. '),
                 ('3.1.2', None, '%(VERSION_STRING)s3 (FIELD_TYPE_MULTI_SELECT) for a multi-select field. '),
                 ('3.1.2', None, '%(VERSION_STRING)s4 (FIELD_TYPE_TEXTAREA) for a large text box field. '),
                 ('3.1.3', None, '%(VERSION_STRING)s5 (FIELD_TYPE_DATETIME) for a date/time field. '),
                 ('3.3.1', None, '%(VERSION_STRING)s6 (FIELD_TYPE_BUG_ID) for a bug ID field. '),
                 ('3.3.2', None, '%(VERSION_STRING)s7 (FIELD_TYPE_BUG_URLS) for a list of bug URLs. '),
                 ],

        'custom': '1 for a custom field, 0 otherwise. Part of <a href="#notes-customfields">the custom fields system</a>.',

        'enter_bug': '1 for a field which is present on the bug entry form, 0 otherwise.',

        'buglist': '1 for a field which can be used as a display or order column in a bug list, 0 otherwise.',

        'value_field_id': 'If not NULL, the ID of a (single-select or multi-select) <i>chooser field</i>, which controls the visibility of individual values of this field.  Only applies to single-select and multi-select fields.  Foreign ney %(column-fielddefs-id)s.',

        'visibility_field_id': 'If not NULL, the ID of a (single-select or multi-select) <i>control field</i> which controls the visibility of this field.  Only applies to custom fields.  Foreign key %(column-fielddefs-id)s.',

        'visibility_value_id': 'If not NULL, and the control field (with ID visibility_field_id) does not have a value with this ID, this field is not visible.  Only applies to custom fields.  Foreign key &lt;field&gt;.id, for example %(column-products-id)s or <a href="#column-customfield-id">cf_&lt;field&gt;.id</a>.',

        'reverse_desc': 'Label for a list of bugs that link to a bug with this field. For example, if the description is "Is a duplicate of", the reverse description would be "Duplicates of this bug". Leave blank to disable the list for this bug.',

        'is_mandatory': '1 if the field is required on the new bug form, 0 if it is not.',

        'is_numeric': '1 if the field is numeric, 0 if it is not.',

        },

    'flagexclusions': {

    'type_id': 'The flag type.  (foreign key %(column-flagtypes-id)s)',

    'product_id': 'The product, or NULL for "any".  (foreign key %(column-products-id)s)',

    'component_id': 'The component, or NULL for "any". (foreign key %(column-components-id)s)',
    },

    'flaginclusions': {

    'type_id': 'The flag type.  (foreign key %(column-flagtypes-id)s)',

    'product_id': 'The product, or NULL for "any".  (foreign key %(column-products-id)s)',

    'component_id': 'The component, or NULL for "any". (foreign key %(column-components-id)s)',
    },

    'flags': {

    'id': 'A unique ID.' ,

    'type_id': 'The flag type.  (foreign key %(column-flagtypes-id)s)',

    'status': "'+' (granted), '-' (denied), or '?' (requested).",

    'bug_id': 'The bug.  (foreign key %(column-bugs-bug_id)s)',

    'attach_id': 'The attachment, or NULL if this flag is not on an attachment. (foreign key %(column-attachments-attach_id)s)',

    'creation_date': 'The date the flag was created.',

    'modification_date': 'The date the flag was most recently modified or created.',

    'setter_id': 'The ID of the user who created, or most recently modified, this flag (foreign key %(column-profiles-userid)s)',

    'requestee_id': 'The ID of the user to whom this request flag is addressed, or NULL for non-requestee flags (foreign key %(column-profiles-userid)s)',

    'is_active': '0 if this flag has been deleted; 1 otherwise.',
    },

    'flagtypes': {

    'id': 'The flag type ID',

    'name': 'The short flag name',

    'description': 'The description of the flag',

    'cc_list': "A string containing email addresses to which notification of requests for this flag should be sent. This is filtered using the groups system before messages are actually sent, so that users not entitled to see a bug don't receive notifications concerning it.",

    'target_type': "'a' for attachment flags, 'b' for bug flags",

    'is_active': '1 if the flag appears in the UI and can be set; 0 otherwise.',

    'is_requestable': '1 if the flag may be requested; 0 otherwise.',

    'is_requesteeble': '1 if a request for this flag may be aimed at a particular user; 0 otherwise.',

    'is_multiplicable': '1 if multiple instances of this flag may be set on the same item; 0 otherwise.',

    'sortkey': 'An integer used for sorting flags for display.',

    'request_group_id': 'Group membership required to request this flag.  (foreign key %(column-groups-id)s)',

    'grant_group_id': 'Group membership required to grant this flag.  (foreign key %(column-groups-id)s)',

    },

    'group_control_map': {

    'group_id': 'The group.  (foreign key %(column-groups-id)s)',

    'product_id': 'The product.  (foreign key %(column-products-id)s)',

    'entry': '1 if membership of this group is required to enter a bug in this product; 0 otherwise.',

    'membercontrol': 'Determines what control members of this group have over whether a bug for this product is placed in this group. 0 (NA/no control): forbidden.  1 (Shown): permitted.  2 (Default): permitted and by default.  3 (Mandatory): always.',

    'othercontrol': 'Determines what control non-group-members have over whether a new bug for this product is placed in this group.  Group membership of existing bugs can only be changed by members of the relevant group. 0 (NA/no control): forbidden. 1 (Shown): permitted.  2 (Default): permitted and by default.  3 (Mandatory): always.  Allowable values depend on the value of membercontrol.  See <a href="#notes-groups">the notes on groups</a>.',

    'canedit': '1 if membership of this group is required to edit a bug in this product; 0 otherwise.',

    'editcomponents': '1 if membership of this group enables editing product-specific configuration such as components and flagtypes; 0 otherwise.',

    'editbugs': '1 if membership of this group enables editing bugs in this product; 0 otherwise. Note: membership of all \'canedit\' groups is also required.',

    'canconfirm': '1 if membership of this group enables confirmation of bugs in this product; 0 otherwise.',
    },

    'group_group_map': {

    'member_id': 'The group whose membership grants membership or "bless" privilege for another group.(foreign key %(column-groups-id)s)',

    'grantor_id': 'The group whose membership or "bless" privilege is automatically granted.(foreign key %(column-groups-id)s)',

    'isbless': '0 if membership is granted; 1 if just "bless" privilege is granted ("bless" does not imply membership).',

    'grant_type': '0 if membership is granted; 1 if just "bless" privilege is granted ("bless" does not imply membership), 2 if visibility is granted.' ,

    },

    'groups': {

    'bit': '2^n for some n.  Assigned automatically.',

    'name': 'A short name for the group.',

    'description': 'A long description of the group.',

    'isbuggroup': '1 if this is a group controlling access to a set of bugs.',

    'userregexp': 'a regexp used to determine membership of new users.',

    'isactive': '1 if bugs can be added to this group; 0 otherwise.',

    'id': 'The group id',

    'icon_url': 'The URL of an icon for the group (e.g. to be shown next to bug comments made by members of the group).',

    'last_changed': 'A timestamp showing when this group was last changed.',

    },

    'keyworddefs': {

    'id': 'A unique number identifying this keyword.',

    'name': 'The keyword itself.',

    'description': 'The meaning of the keyword.',
    },

    'keywords': {

    'bug_id': 'The bug (foreign key %(column-bugs-bug_id)s)',

    'keywordid': 'The keyword ID (foreign key %(column-keyworddefs-id)s)',
    },

    'logincookies': {

    'cookie': 'The cookie',

    'userid': 'The user id; (foreign key %(column-profiles-userid)s)',

    'cryptpassword': 'The encrypted password used on this login.',

    'hostname': 'The CGI REMOTE_HOST for this login.',

    'ipaddr': 'The CGI REMOTE_ADDR for this login.',

    'lastused': 'The timestamp of this login.',
    },

    'longdescs': {

    'bug_id': 'the bug (foreign key %(column-bugs-bug_id)s)',

    'who': 'the user who added this text (foreign key %(column-profiles-userid)s)',

    'bug_when': 'when the text was added',

    'thetext': 'the text itself.',

    'isprivate': 'Non-zero if this comment is "private", i.e. only visible to members of the "insider" group.',

    'work_time': 'Number of hours worked on this bug (for time tracking purposes).',

    'already_wrapped': 'Non-zero if this comment is word-wrapped in the database (and so should not be wrapped for display).',

    'comment_id': 'A unique ID for this comment.',

    'type': 'The type of a comment, used to identify and localize the text of comments which are automatically added by Bugzilla. 0 for a normal comment. 1 for a comment marking this bug as a duplicate of another.  2 for a comment marking another bug as a duplicate of this.  3 for a comment recording a transition to NEW by voting.  4 for a comment recording that this bug has been moved.',

    'extra_data': 'Used in conjunction with %(column-longdescs-type)s to provide the variable data in localized text of an automatic comment.  For instance, a duplicate bug number.',

    },

    'login_failure': {

        'user_id': 'the user who failed a login (foreign key %(column-profiles-userid)s)',

        'login_time': 'when the failure occurred',

        'ip_addr': 'the IP address of the client that failed the login',

    },

    'milestones': {

        'id': 'A unique numeric ID',

        'value': 'The name of the milestone (e.g. "3.1 RTM", "0.1.37", "tweakfor BigCustomer", etc).',

        'product': 'The product (foreign key %(column-products-product)s)',

        'product_id': 'The product (foreign key %(column-products-id)s)',

        'sortkey': 'A number used for sorting milestones for a given product.',

        'isactive': '1 if this milestone is available for new bugs, 0 if not.',

    },

    'namedqueries': {

        'id': 'A unique number identifying this query.',

        'userid': 'The user whose query this is (foreign key %(column-profiles-userid)s)',

        'name': 'The name of the query.',

        'watchfordiffs': 'Unused.',

        'linkinfooter': 'Whether or not the query should appear in the foot of every page.',

        'query': 'The query (text to append to the query page URL).',

        'query_type': '1 (LIST_OF_BUGS) if the query is simply a list of bug IDs, 0 (QUERY_LIST) if it is a genuine query.',

    },

    'namedqueries_link_in_footer': {

        'namedquery_id': 'The query id (foreign key %(column-namedqueries-id)s).',

        'user_id': 'The user id (foreign key %(column-profiles-userid)s).',

        },

    'namedquery_group_map': {

        'namedquery_id': 'The query id (foreign key %(column-namedqueries-id)s).',

        'group_id': 'The group id (foreign key %(column-groups-id)s).',

        },

    'op_sys': {

        'value': 'A possible value of the field',

        'isactive': '1 if this value is available in the user interface, 0 otherwise',

        'sortkey': 'A number used to determine the order in which values are shown.',

        'id': 'a unique ID.',

        'visibility_value_id': 'If set, this value is only available if the chooser field (identified by %(column-fielddefs-value_field_id)s) has the value with this ID.  Foreign key &lt;field&gt;.id, for example %(column-products-id)s or <a href="#column-customfield-id">cf_&lt;field&gt;.id</a>.',
        },

    'priority': {

        'value': 'A possible value of the field',

        'isactive': '1 if this value is available in the user interface, 0 otherwise',

        'sortkey': 'A number used to determine the order in which values are shown.',

        'id': 'a unique ID.',

        'visibility_value_id': 'If set, this value is only available if the chooser field (identified by %(column-fielddefs-value_field_id)s) has the value with this ID.  Foreign key &lt;field&gt;.id, for example %(column-products-id)s or <a href="#column-customfield-id">cf_&lt;field&gt;.id</a>.',
        },

    'products': {

        'product': 'The name of the product.',

        'id': 'The product ID.',

        'name': 'The product name.',

        'description': 'The description of the product',

        'milestoneurl': 'The URL of a document describing the product milestones.',

        'disallownew': 'New bugs can only be created for this product if this is 0.',

        'votesperuser': 'Total votes which a single user has for bugs of this product.',

        'maxvotesperbug': 'Maximum number of votes which a bug may have.',

        'votestoconfirm': 'How many votes are required for this bug to become NEW.',

        'defaultmilestone': 'The default milestone for a new bug (foreign key %(column-milestones-value)s)',

        'classification_id': 'The classification ID (foreign key %(column-classifications-id)s).',

        'isactive': '1 if this value is available in the user interface, 0 otherwise',

        'allows_unconfirmed': '1 if new bugs can be UNCONFIRMED, 0 if they always start as NEW',

    },

    'profile_search': {

        'id': 'A unique ID for the list, specified as list_id in the URL parameters.',

        'user_id': 'The ID of the user who ran the search. (foreign key %(column-profiles-userid)s)',

        'bug_list': 'The list of bug numbers returned by the search.',

        'list_order': 'The sort order specified by the user.',

    },

    'profile_setting': {

        'setting_name': 'The name of the setting (foreign key %(column-setting-name)s).',

        'user_id': 'The user (foreign key %(column-profiles-userid)s).',

        'setting_value': 'The value (foreign key %(column-setting_value-value)s).',
    },

    'profiles': {

        'userid': 'A unique identifier for the user.  Used in other tables to identify this user.',

        'login_name': 'The user\'s email address.  Used when logging in or providing mailto: links.',

        'password': 'The user\'s password, in plaintext.',

        'cryptpassword': ['The user\'s password.',
                          (None, '2.12', '%(VERSION_STRING)sThe MySQL function <code>encrypt</code> is used to encrypt passwords.'),
                          ('2.14', None, '%(VERSION_STRING)sThe Perl function <code>crypt</code> is used.')],

        'realname': 'The user\'s real name.',

        'groupset': 'The set of groups to which the user belongs.  Each group corresponds to one bit and confers powers upon the user. See %(the-table-groups)s.',

        'emailnotification': 'Controls when email reporting bug changes is sent to this user.',

        'disabledtext': 'If non-empty, indicates that this account has been disabled and gives a reason. ',

        'newemailtech': 'is non-zero if the user wants to user the "new" email notification technique.',

        'mybugslink': 'indicates whether a "My Bugs" link should appear at the bottom of each page.',

        'blessgroupset': 'Indicates the groups into which this user is able to introduce other users.',

        'emailflags': 'Flags controlling when email messages are sent to this user.',

        'refreshed_when': 'A timestamp showing when the derived group memberships in %(the-table-user_group_map)s were last updated for this user.',

        'extern_id': 'The ID for environmental authentication (see <a href="#notes-authentication">the notes on authentication</a>).',

        'disable_mail': '1 to disable all mail to this user; 0 for mail to depend on the per-user email settings in %(table-email_setting)s.',

        'is_enabled': '1 if the account is enabled, 0 if it is disabled and prevented from logging in.',

    },

    'profiles_activity': {

        'userid': 'The profile which has changed (foreign key %(column-profiles-userid)s)',

        'who': 'The user who changed it (foreign key %(column-profiles-userid)s)',

        'profiles_when': 'When it was changed',

        'fieldid': 'The ID of the changed field (foreign key %(column-fielddefs-id)s)',

        'oldvalue': 'The old value',

        'newvalue': 'The new value.',
    },

    'quips': {

    'quipid': 'A unique ID.',

    'userid': 'The user who added this quip (foreign key %(column-profiles-userid)s)',

    'quip': 'The quip itself.',

    'approved': '1 if this quip has been approved for display, 0 otherwise.',
    },

    'rep_platform': {

        'value': 'A possible value of the field',

        'isactive': '1 if this value is available in the user interface, 0 otherwise',

        'sortkey': 'A number used to determine the order in which values are shown.',

        'id': 'a unique ID.',

        'visibility_value_id': 'If set, this value is only available if the chooser field (identified by %(column-fielddefs-value_field_id)s) has the value with this ID.  Foreign key &lt;field&gt;.id, for example %(column-products-id)s or <a href="#column-customfield-id">cf_&lt;field&gt;.id</a>.',
        },

    'resolution': {

        'value': 'A possible value of the field',

        'isactive': '1 if this value is available in the user interface, 0 otherwise',

        'sortkey': 'A number used to determine the order in which values are shown.',

        'id': 'a unique ID.',

        'visibility_value_id': 'If set, this value is only available if the chooser field (identified by %(column-fielddefs-value_field_id)s) has the value with this ID.  Foreign key &lt;field&gt;.id, for example %(column-products-id)s or <a href="#column-customfield-id">cf_&lt;field&gt;.id</a>.',
        },

    'series': {

    'series_id': 'A unique ID.',

    'creator': ['The user who created this series (foreign key %(column-profiles-userid)s).',
                (None, '2.23.2', '%(VERSION_STRING)s 0 if this series is created by checksetup when first installing Bugzilla.'),
                ('2.23.3', None, '%(VERSION_STRING)s NULL if this series is created by checksetup when first installing Bugzilla.'),],

    'category': 'The series category. (foreign key %(column-series_categories-id)s)',

    'subcategory': 'The series subcategory. (foreign key %(column-series_categories-id)s)',

    'name': 'The series name.',

    'frequency': 'The period between data samples for this series, in days.' ,

    'last_viewed': 'The time at which this dataset was last viewed.',

    'query': 'a snippet of CGI which specifies a subset of bugs, as for query.cgi',

    'public': '1 if the series is visible to all users, 0 otherwise.',
    },

    'series_categories': {

    'id': 'A unique ID.',

    'name': 'The category name.',

    },

    'series_data': {

    'series_id': 'The series ID. (foreign key %(column-series-series_id)s)',

    'date': 'The time point at which this datum was collected.',

    'value': 'The number of bugs in the dataset at this time point.',

    'series_date': 'The time point at which this datum was collected.',

    'series_value': 'The number of bugs in the dataset at this time point.',
    },

    'setting': {

        'default_value': 'the value of this setting which will apply to any user who does not change it.',

        'is_enabled': '1 if users are able to change this setting; 0 if it is automatic.',

        'name': 'The name of the setting.',

        'subclass': 'The name of the Perl subclass (of Setting) to which this setting applies.',

        },

    'setting_value': {

        'sortindex': 'A number used to determine the order in which setting values are shown',

        'name': 'The setting name. (foreign key %(column-setting-name)s)',

        'value': 'The setting value',
    },

    'shadowlog': {

    'id': 'unique id',

    'ts': 'timestamp',

    'reflected': '0',

    'command': 'SQL command',
    },

    'status_workflow': {

    'old_status': 'The old bug status, None for bug creation (foreign key %(column-bug_status-id)s)',

    'new_status': 'The new bug status (foreign key %(column-bug_status-id)s)',

    'require_comment': '1 if this transition requires a comment; 0 otherwise.',
    },

    'tag': {

        'id': 'A unique ID for the tag',

        'name': 'The name of the tag. Only unique per user.',

        'user_id': 'ID of the user this tag belongs to. (foreign key %(column-profiles-userid)s)',

    },

    'tags': {

        'id': 'A unique ID for the tag',

        'name': 'The name of the tag. Only unique per user.',

        'user_id': 'ID of the user this tag belongs to. (foreign key %(column-profiles-userid)s)',

    },

    'tokens': {

    'userid': 'The user to whom the token was issued.  (foreign key %(column-profiles-userid)s)',

    'issuedate': 'The date at which the token was issued',

    'token': 'The token itself.',

    'tokentype': "The type of the token.  Possible values: 'account' when creating a new user account, 'emailold' and 'emailnew' when changing email address, 'password' when changing a password, or 'session' for a session token.",

    'eventdata': 'The expected event, for a session token.'
    },

    'ts_error': {
            
        'error_time': 'The time at which the error occurred.',

        'jobid': 'The job ID.  Foreign key %(column-ts_job-jobid)s',

        'message': 'The error message.',

        'funcid': 'The function ID.  Foreign key %(column-ts_funcmap-funcid)s.',

    },  

    'ts_exitstatus': {

        'jobid': 'The job ID.  Foreign key %(column-ts_job-jobid)s',

        'funcid': 'The function ID.  Foreign key %(column-ts_funcmap-funcid)s.',

        'status': 'The exit status.  0 for success.',

        'completion_time': 'The time at which the job finished.',

        'delete_after': 'A time after which this row can be deleted.',

    },

    'ts_funcmap': {

        'funcid': 'A unique ID.',

        'funcname': 'A unique function name, also known as an ability or a worker class name.',

    },

    'ts_job': {

        'jobid': 'A unique ID.',

        'funcid': 'The function ID.  Foreign key %(column-ts_funcmap-funcid)s.',

        'arg': 'State data for the job, stored as a frozen reference.',

        'uniqkey': 'An arbitrary unique reference.',

        'insert_time': 'not used.',

        'run_after': 'A timestamp before which the job should not be run.',

        'grabbed_until': 'Set while a worker is attempting this job; do not retry this job until this is in the past.',

        'priority': 'Not used.',

        'coalesce': 'A string used to indicate jobs which can be usefully pipelined by a single worker.',

    },


    'ts_note': {

        'jobid': 'The job ID.  Foreign key %(column-ts_job-jobid)s',

        'notekey': 'Not used.',

        'value': 'Not used.',

    },

    'user_group_map': {

    'user_id': 'The user.  (foreign key %(column-profiles-userid)s)',

    'grant_type': '0 if this membership or privilege is explicit. 1 if it is derived from a group hierarchy (see %(the-table-group_group_map)s). 2 if it results from matching a regular expression (see %(column-groups-userregexp)s).' ,

    'group_id': 'The group.  (foreign key %(column-groups-id)s)',

    'isbless': '0 if this row records group membership; 1 if this row records group "bless" privilege.',

    'isderived': '0 if this membership or privilege is explicit.  1 if it is derived (e.g. from %(the-table-group_group_map)s or %(column-groups-userregexp)s).' ,

    },

    'user_series_map': {

    'user_id': 'The user ID. (foreign key %(column-profiles-userid)s)',

    'series_id': 'The series. (foreign key %(column-series-series_id)s)',
    },

    'versions': {

        'id': 'A unique numeric ID',

        'value': 'The name of the version',

        'program': 'The product (foreign key %(column-products-product)s)',

        'product_id': 'The product (foreign key %(column-products-id)s)',

        'isactive': '1 if the version is available for new bugs, 0 if not.',
    },

    'votes': {

    'who': 'The user (foreign key %(column-profiles-userid)s)',

    'bug_id': 'The bug (foreign key %(column-bugs-bug_id)s)',

    'count': 'How many votes.',
    },

    'watch': {

    'watcher': 'The watching user (foreign key %(column-profiles-userid)s)',

    'watched': 'The watched user (foreign key %(column-profiles-userid)s)',
    },

    'whine_events': {

        'id': 'The whine event ID, used to identify this event.',

        'owner_userid': """The user ID of the whine owner (foreign key %(column-profiles-userid)s).  Must match %(column-namedqueries-userid)s for the queries associated with this event (%(column-whine_queries-query_name)s).""",

        'subject': 'The Subject of the whine emails.',

        'body': 'Text to appear in the body of the whine emails before the bugs table.',

        'mailifnobugs': "1 is mail should be sent even if there are no results to the query. 0 if the report shouldn't be sent unless there are results.",
    },

    'whine_queries': {

    'id': 'A unique ID for this query.',

    'eventid': 'The whine event ID (foreign key %(column-whine_events-id)s).',

    'query_name': 'The query name (foreign key %(column-namedqueries-name)s).',

    'sortkey':  'A key to order the queries for a given event ID.',

    'onemailperbug': """1 if a separate email message should be sent
    for each bug matching the query; 0 if a single email should be
    sent covering all the bugs.""",

    'title': 'The title displayed for this query in the message.',

    },

    'whine_schedules': {

    'id': """a unique ID for this whine schedule.""",

    'eventid': 'The whine event ID (foreign key %(column-whine_events-id)s).',

    'run_day': """The day on which this whine should run.  'All' means
    every day.  'MF' means Monday to Friday inclusive.  A three letter
    weekday abbreviation (e.g. "Mon", "Thu") means only on that day.
    An integer indicates a particular day of the month.  'last' means
    the last day of the month.""",

    'run_time': """The time at which this whine should run.  An
    integer indicates an hour of the day.  An interval (e.g. "15min",
    "30min") indicates that the whine should run repeatedly at that
    interval.""",

    'run_next': """The time and date at which the whine should next be
    run.  NULL if the whine has been changed and not rescheduled
    yet.""",

    'mailto_userid': """The ID of the user to whom to send whine
    messages (foreign key %(column-profiles-userid)s).""",

    'mailto': "Either a user ID (foreign key %(column-profiles-userid)s) or group ID (foreign key %(column-groups-id)s) identifying the user or users to whom to send whine messages.",

    'mailto_type': "0 if the mailto field is a user ID, 1 if it is a group ID.",

    },
}

# This is a map from table name to a map from column name to canonical
# column name.  For use when a column has been renamed but not
# otherwise changed.

column_renamed = {

    'votes': {

    'vote_count': 'count',

    },

    'series': {

    'is_public': 'public',

    },

    'series_data': {

    'series_date': 'date',

    'series_value': 'value',

    },

    'series_categories': {

    'category_id': 'id',

    },


    'fielddefs': {

    'fieldid': 'id',

    },

}

# This is a map from table name to a map from column name to HTML
# remark for that column.  At present, these remarks include schema
# change comments (which will eventually be generated automatically).
#
# Columns with no attached remarks are given 'None' as a placeholder,
# so we know to add a remark later.

column_added_remark = {
    'attachments': {
        'isobsolete': None,

        'isprivate': None,

        'isurl': None,

        'modification_time': None,

        },

    'bug_see_also': {
        'id': None,
        'class': 'Definitions for allowable types of remote bug report instances were moved into subclasses of Bugzilla::BugURL.',
    },
    'bug_severity': {
        'visibility_value_id': None,
    },

    'bug_status': {
        'is_open': None,
        'visibility_value_id': None,
        },

    'bugs': {

        'alias': None,

        'deadline': None,

        'keywords': None,

        'everconfirmed': None,

        'lastdiffed': None,

        'product_id': 'replacing "product"',

        'component_id': 'replacing "component"',

        'reporter_accessible': None,

        'assignee_accessible': None,

        'qacontact_accessible': None,

        'cclist_accessible': None,

        'estimated_time': None,

        'groupset': None,

        'qa_contact': None,

        'remaining_time': None,

        'status_whiteboard': None,

        'target_milestone': None,

        'votes': None,

        },

    'bugs_activity': {

        'attach_id': None,

        'fieldid': 'replacing "field"',

        'bug_when': 'replacing "when"',

        'added': 'replacing "newvalue"',

        'removed': 'replacing "oldvalue"',

        'comment_id': None,

        },

    'classifications': {

        'sortkey': None,

        },

    'components': {

        'description': None,

        'name': 'replacing "value"',

        'id': 'replacing "value" as the primary key',

        'initialqacontact': None,

        'product_id': 'replacing "program"',

        'isactive': None,

        },

    'fielddefs': {

        'obsolete': None,

        'custom': None,

        'type': None,

        'enter_bug': None,

        'buglist': None,

        'value_field_id': None,

        'visibility_field_id': None,

        'visibility_value_id': None,

        'reverse_desc': None,

        'is_mandatory': None,

        'is_numeric': None,

    },

    'flags': {

    'is_active': None,

    },

    'flagtypes': {

    'grant_group_id': None,

    'request_group_id': None,

    },

    'group_group_map': {

        'grant_type': 'replacing "isbless"',

        },

    'group_control_map': {

        'editbugs': None,
        'editcomponents': None,
        'canconfirm': None,

        },

    'groups': {

    'id': 'replacing "bit"',

    'isactive': None,

    'last_changed': None,

    'icon_url': None,

    },

    'logincookies': {

    'ipaddr': 'replacing hostname',

    },

    'longdescs': {

    'type': None,

    'extra_data': None,

    'comment_id': None,

    'already_wrapped': None,

    'isprivate': None,

    'work_time': None,

    },

    'milestones': {

        'product_id': 'replacing "product"',

        'id': None,

        'isactive': None,

    },

    'namedqueries': {

    'query_type': None,

    'id': None,

    },

    'op_sys': {

        'visibility_value_id': None,

    },

    'priority': {

        'visibility_value_id': None,

    },

    'products': {

        'classification_id': None,

        'votestoconfirm': None,

        'defaultmilestone': None,

        'disallownew': None,

        'maxvotesperbug': None,

        'votesperuser': None,

        'id': 'replacing "product" as the table key',

        'name': 'replacing "product" as the product name',

        'isactive': 'replacing and inverting "disallownew" for better readability',

        'allows_unconfirmed': 'Removing the relationship between votestoconfirm and whether or not the UNCONFIRMED status is available (Bug 162060)',

    },

    'profiles': {

        'blessgroupset': None,

        'groupset': None,

        'newemailtech': None,

        'emailnotification': None,

        'mybugslink': None,

        'disabledtext': None,

        'extern_id': None,

        'emailflags': None,

        'refreshed_when': None,

        'disable_mail': None,

        'is_enabled': 'For query performance reasons it was better to check a boolean than try to check if %(column-profiles-disabledtext)s was zero length or not.',

    },

    'quips': {

        'approved': None,

    },

    'rep_platform': {

        'visibility_value_id': None,

    },

    'resolution': {

        'visibility_value_id': None,

    },

    'series': {

    'public': None,

    },

    'setting': {

    'subclass': None,
    },

    'user_group_map': {

    'grant_type': 'replacing "isderived"',

    },

    'versions': {

        'product_id': 'replacing "program"',

        'id': None,

        'isactive': '1 if this version is available for new bugs, 0 if not.',

    },

    'whine_events': {
        'mailifnobugs': None,
    },

    'whine_schedules': {
        'mailto': None,
        'mailto_type': None,
    },
}

# This is a map from table name to a map from column name to HTML
# remark for that column.  At present, these remarks include schema
# change comments (which will eventually be generated automatically).
#
# Columns with no attached remarks are given 'None' as a placeholder,
# so we know to add a remark later.

column_removed_remark = {
    'attachments': {

        'thedata': 'moved to %(the-table-attach_data)s',

        'isurl': 'detection logic was added to detect URLs instead of needing to be told by the uploader.',

        },

    'bugs': {

        'area': None,

        'long_desc': 'moved to %(the-table-longdescs)s',

        'groupset': 'replaced by %(the-table-bug_group_map)s',

        'product': 'replaced by "product_id"',

        'component': 'replaced by "component_id"',

        'assignee_accessible': None,

        'qacontact_accessible': None,

        'votes': 'The Voting feature was moved to an extension. The column is not deleted on upgrade if it exists.',

        'keywords': 'This was only used for caching. Improved indexing made this field unnecessary.',

        },

    'bugs_activity': {

        'field': 'replaced by "fieldid"',

        'oldvalue': 'replaced by "removed"',

        'when': 'replaced by "bug_when"',

        'newvalue': 'replaced by "added"',

        },

    'components': {

        'value': 'replaced by "name" and "id"',

        'program': 'replaced by "product_id"',

        },

    'fielddefs': {
        'obsolete': None,
        'visibility_value_id': 'Moved to %(column-field_visibility-value_id)s',
        },

    'flags': {
        'is_active': None,
        },

    'groups': {

        'bit': 'replaced by "id"',

        'last_changed': 'redundant',

        },

    'group_group_map': {

        'isbless': 'replaced by "grant_type"',

        },

    'logincookies': {

    'cryptpassword': None,

    'hostname': 'replaced by "ipaddr"',

    },

    'milestones': {

    'product': 'replaced by "product_id"',

    },

    'namedqueries': {

        'watchfordiffs': None,

        'linkinfooter': 'replaced by %(the-table-namedqueries_link_in_footer)s.',

        'query_type': 'replaced by %(the-table-tags)s and %(the-table-bug_tag)s.',

    },

    'products': {

        'product': 'replaced with "id" and "name"',

        'disallownew': 'replaced by "isactive"',

        'milestoneurl': 'very rarely used and UI was confusing (Bug 369489)',

        'votesperuser': 'The Voting feature was moved to an extension. The column is not deleted on upgrade if it exists.',

        'maxvotesperbug': 'The Voting feature was moved to an extension. The column is not deleted on upgrade if it exists.',

        'votestoconfirm': 'The Voting feature was moved to an extension. The column is not deleted on upgrade if it exists.',
    },

    'profiles': {

    'password': None,

    'emailflags': 'replaced by %(the-table-email_setting)s',

    'groupset': 'replaced by %(the-table-user_group_map)s',

    'emailnotification': 'replaced in part by %(column-profiles-emailflags)s',

    'newemailtech': None,

    'blessgroupset': 'replaced by %(the-table-user_group_map)s',

    'refreshed_when': 'redundant',

    },

    'series': {

        'last_viewed': 'was never used, so removed. (bug 519032)',

    },

    'user_group_map': {

    'isderived': 'replaced by "grant_type"',

    },

    'versions': {

    'program': 'replaced by "product_id"',

    },

    'whine_schedules': {
        'mailto_userid': None,
    },

}

# This is a map from table name to a map from index name to HTML
# remark for that index.  At present, these remarks include schema
# change comments (which will eventually be generated automatically).
#
# Indexes with no attached remarks are given 'None' as a placeholder,
# so we know to add a remark later.

index_remark = {
    'attachments': {
        'PRIMARY': None,
        'bug_id': None,
        'creation_ts': None,
        'attachments_submitter_id_idx': None,
        'attachments_modification_time_idx': None,
        },
    'attach_data': {
        'PRIMARY': None,
        },
    'attachstatusdefs': {
        'PRIMARY': None,
        },
    'attachstatuses': {
        'PRIMARY': None,
        },
    'audit_log': {
        },
    'bug_group_map': {
        'bug_id': None,
        'group_id': None,
        },
    'bug_see_also': {
        'PRIMARY': None,
        'bug_see_also_bug_id_idx': None,
    },
    'bug_severity': {
        'PRIMARY': None,
        'bug_severity_sortkey_idx': None,
        'bug_severity_value_idx': None,
        'bug_severity_visibility_value_id_idx': None,
    },
    'bug_status': {
        'PRIMARY': None,
        'bug_status_sortkey_idx': None,
        'bug_status_value_idx': None,
        'bug_status_visibility_value_id_idx': None,
    },
    'bug_tag': {
        'bug_tag_bug_id_idx': None,
    },
    'bugs': {
        'PRIMARY': None,
        'alias': None,
        'area': None,
        'assigned_to': None,
        'creation_ts': None,
        'delta_ts': None,
        'bug_severity': None,
        'bug_status': None,
        'op_sys': None,
        'priority': None,
        'product': None,
        'product_id': None,
        'reporter': None,
        'short_desc': None,
        'version': None,
        'component': None,
        'component_id': None,
        'resolution': None,
        'target_milestone': None,
        'qa_contact': None,
        'votes': None,
        },
    'bugs_activity': {
        'bug_id': None,
        'when': None,
        'bug_when': None,
        'field': None,
        'fieldid': None,
        'bugs_activity_who_idx': None,
        'bugs_activity_added_idx': None,
        },
    'bugs_fulltext': {
        'PRIMARY': None,
        'bugs_fulltext_short_desc_idx': None,
        'bugs_fulltext_comments_idx': None,
        'bugs_fulltext_comments_noprivate_idx': None,
        },
    'bz_schema': {
    },
    'category_group_map': {
        'category_id': None,
        },
    'cc': {
        'who': None,
        'bug_id': None,
        },
    'classifications': {
        'PRIMARY': None,
        'name': None,
        },
    'components': {
        'PRIMARY': None,
        'product_id': None,
        'name': None,
        'bug_id': None,
        'bug_when': None,
        'fieldid': None,
        },
    'component_cc': {
    'component_cc_user_id_idx': None,
    },
    'dependencies': {
        'blocked': None,
        'dependson': None,
        },
    'duplicates': {
        'PRIMARY': None,
        },
    'email_setting': {
    'email_setting_user_id_idx': None,
    },
    'fielddefs': {
        'PRIMARY': None,
        'name': None,
        'sortkey': None,
        'fielddefs_value_field_id_idx': None,
        'fielddefs_is_mandatory_idx': None,
        },
    'field_visibility': {
        'field_visibility_field_id_idx': None,
        },
    'flagexclusions': {
        'type_id': None,
        },
    'flaginclusions': {
        'type_id': None,
        },
    'flags': {
        'PRIMARY': None,
        'bug_id': None,
        'setter_id': None,
        'requestee_id': None,
        'flags_type_id_idx': None,
        },
    'flagtypes': {
        'PRIMARY': None,
        },
    'group_control_map': {
        'product_id': None,
        'group_id': None,
        },
    'group_group_map': {
        'member_id': None,
        },
    'groups': {
        'PRIMARY': None,
        'bit': None,
        'name': None,
        },
    'keyworddefs': {
        'PRIMARY': None,
        'name': None,
        },
    'keywords': {
        'keywordid': None,
        'bug_id': None,
        },
    'logincookies': {
        'PRIMARY': None,
        'lastused': None,
        },
    'login_failure': {
        'login_failure_user_id_idx': None,
        },
    'longdescs': {
        'PRIMARY': None,
        'bug_id': None,
        'who': None,
        'bug_when': None,
        'thetext': None,
        },
    'milestones': {
        'PRIMARY': None,
        'product': None,
        'product_id': None,
        },
    'namedqueries': {
        'PRIMARY': None,
        'userid': None,
        'watchfordiffs': None,
        },
    'namedqueries_link_in_footer': {
        'namedqueries_link_in_footer_id_idx': None,
        'namedqueries_link_in_footer_userid_idx': None,
    },
    'namedquery_group_map': {
        'namedquery_group_map_group_id_idx': None,
        'namedquery_group_map_namedquery_id_idx': None,
    },
    'op_sys': {
    'PRIMARY': None,
    'op_sys_sortkey_idx': None,
    'op_sys_value_idx': None,
    'op_sys_visibility_value_id_idx': None,
    },
    'priority': {
    'PRIMARY': None,
    'priority_sortkey_idx': None,
    'priority_value_idx': None,
    'priority_visibility_value_id_idx': None,
    },
    'products': {
        'PRIMARY': None,
        'name': None,
        },
    'profile_search': {
        'PRIMARY': None,
        'profile_search_user_id': None,
        'profile_search_user_id_idx': None,
    },
    'profile_setting': {
    'profile_setting_value_unique_idx': None,
    },
    'profiles': {
        'PRIMARY': None,
        'login_name': None,
        'profiles_extern_id_idx': None,
        },
    'profiles_activity': {
        'userid': None,
        'profiles_when': None,
        'fieldid': None,
        },
    'quips': {
        'PRIMARY': None,
        },
    'rep_platform': {
    'PRIMARY': None,
    'rep_platform_sortkey_idx': None,
    'rep_platform_value_idx': None,
    'rep_platform_visibility_value_id_idx': None,
    },
    'resolution': {
    'PRIMARY': None,
    'resolution_sortkey_idx': None,
    'resolution_value_idx': None,
    'resolution_visibility_value_id_idx': None,
    },
    'series': {
        'PRIMARY': None,
        'creator': None,
        'creator_2': None,
        'series_category_idx': None,
        },
    'series_categories': {
        'PRIMARY': None,
        'name': None,
        },
    'series_data': {
        'series_id': None,
        },
    'setting': {
    'PRIMARY': None,
    },
    'setting_value': {
    'setting_value_ns_unique_idx': None,
    'setting_value_nv_unique_idx': None,
    },
    'shadowlog': {
        'PRIMARY': None,
        'reflected': None,
        },
    'status_workflow': {
        'status_workflow_idx': None,
        },
    'tag': {
        'PRIMARY': None,
        'tag_user_id_idx': None,
        },
    'tags': {
        'PRIMARY': None,
        'tags_user_id_idx': None,
        },
    'tokens': {
        'PRIMARY': None,
        'userid': None,
        },
    'ts_error': {
        'ts_error_funcid_idx': None,
        'ts_error_error_time_idx': None,
        'ts_error_jobid_idx': None,
    },
    'ts_exitstatus': {
        'PRIMARY': None,
        'ts_exitstatus_funcid_idx': None,
        'ts_exitstatus_delete_after_idx': None,
    },
    'ts_funcmap': {
        'PRIMARY': None,
        'ts_funcmap_funcname_idx': None,
    },
    'ts_job': {
        'PRIMARY': None,
        'ts_job_funcid_idx': None,
        'ts_job_run_after_idx': None,
        'ts_job_coalesce_idx': None,
    },
    'ts_note': {
        'ts_note_jobid_idx': None,
    },
    'user_group_map': {
        'user_id': None,
        },
    'user_series_map': {
        'user_id': None,
        'series_id': None,
        },
    'versions': {
        'PRIMARY': None,
        'versions_product_id_idx': None,
        },
    'votes': {
        'who': None,
        'bug_id': None,
        },
    'watch': {
        'watched': None,
        'watcher': None,
        },
    'whine_events': {
        'PRIMARY': None,
    },

    'whine_queries': {
        'PRIMARY': None,
        'eventid': None,
    },

    'whine_schedules': {
        'PRIMARY': None,
        'run_next': None,
        'eventid': None,
    },
}

index_renamed = {
    'attachments': {
    'attachments_bug_id_idx': 'bug_id',
    'attachments_creation_ts_idx': 'creation_ts',
    },
    'bug_group_map': {
    'bug_group_map_bug_id_idx': 'bug_id',
    'bug_group_map_group_id_idx': 'group_id',
    },
    'bugs': {
    'bugs_votes_idx': 'votes',
    'bugs_component_id_idx': 'component_id',
    'bugs_product_id_idx': 'product_id',
    'bugs_reporter_idx': 'reporter',
    'bugs_bug_status_idx': 'bug_status',
    'bugs_short_desc_idx': 'short_desc',
    'bugs_bug_severity_idx': 'bug_severity',
    'bugs_priority_idx': 'priority',
    'bugs_alias_idx': 'alias',
    'bugs_version_idx': 'version',
    'bugs_target_milestone_idx': 'target_milestone',
    'bugs_delta_ts_idx': 'delta_ts',
    'bugs_assigned_to_idx': 'assigned_to',
    'bugs_creation_ts_idx': 'creation_ts',
    'bugs_resolution_idx': 'resolution',
    'bugs_op_sys_idx': 'op_sys',
    'bugs_qa_contact_idx': 'qa_contact',
    },
    'bugs_activity': {
    'bugs_activity_bug_id_idx': 'bug_id',
    'bugs_activity_bug_when_idx': 'bug_when',
    'bugs_activity_fieldid_idx': 'fieldid',
    },
    'category_group_map': {
    'category_group_map_category_id_idx': 'category_id',
    },
    'cc': {
    'cc_bug_id_idx': 'bug_id',
    'cc_who_idx': 'who',
    },
    'classifications': {
    'classifications_name_idx': 'name',
    },
    'components': {
    'components_name_idx': 'name',
    'components_product_id_idx': 'product_id',
    },
    'dependencies': {
    'dependencies_dependson_idx': 'dependson',
    'dependencies_blocked_idx': 'blocked',
    },
    'fielddefs': {
    'fielddefs_name_idx': 'name',
    'fielddefs_sortkey_idx': 'sortkey',
    },
    'flagexclusions': {
    'flagexclusions_type_id_idx': 'type_id',
    },
    'flaginclusions': {
    'flaginclusions_type_id_idx': 'type_id',
    },
    'flags': {
    'flags_bug_id_idx': 'bug_id',
    'flags_setter_id_idx': 'setter_id',
    'flags_requestee_id_idx': 'requestee_id',
    },
    'group_control_map': {
    'group_control_map_group_id_idx': 'group_id',
    'group_control_map_product_id_idx': 'product_id',
    },
    'group_group_map': {
    'group_group_map_member_id_idx': 'member_id',
    },
    'groups': {
    'groups_name_idx': 'name',
    },
    'keyworddefs': {
    'keyworddefs_name_idx': 'name',
    },
    'keywords': {
    'keywords_bug_id_idx': 'bug_id',
    'keywords_keywordid_idx': 'keywordid',
    },
    'logincookies': {
    'logincookies_lastused_idx': 'lastused',
    },
    'longdescs': {
    'longdescs_bug_id_idx': 'bug_id',
    'longdescs_bug_when_idx': 'bug_when',
    'longdescs_thetext_idx': 'thetext',
    'longdescs_who_idx': 'who',
    },
    'milestones': {
    'milestones_product_id_idx': 'product_id',
    },
    'namedqueries': {
    'namedqueries_userid_idx': 'userid',
    },
    'products': {
    'products_name_idx': 'name',
    },
    'profiles': {
    'profiles_login_name_idx': 'login_name',
    },
    'profiles_activity': {
    'profiles_activity_profiles_when_idx': 'profiles_when',
    'profiles_activity_userid_idx': 'userid',
    'profiles_activity_fieldid_idx': 'fieldid',
    },
    'series': {
    'series_creator_idx': 'creator_2',
    },
    'series_categories': {
    'series_categories_name_idx': 'name',
    },
    'series_data': {
    'series_data_series_id_idx': 'series_id',
    },
    'tokens': {
    'tokens_userid_idx': 'userid',
    },
    'user_group_map': {
    'user_group_map_user_id_idx': 'user_id',
    },
    'votes': {
    'votes_bug_id_idx': 'bug_id',
    'votes_who_idx': 'who',
    },
    'watch': {
    'watch_watched_idx': 'watched',
    'watch_watcher_idx': 'watcher',
    },
    'whine_queries': {
    'whine_queries_eventid_idx': 'eventid',
    },
    'whine_schedules': {
    'whine_schedules_eventid_idx': 'eventid',
    'whine_schedules_run_next_idx': 'run_next',
    },
    }


index_removed_remark = {
    'bugs': {
        'area': None,
        'short_desc': 'replaced by use of LIKE',
        'product': 'replaced by "product_id"',
        'component': 'replaced by "component_id"',
        'votes': 'The Voting feature was moved to an extension.',
        },

    'bugs_activity': {
        'when': 'replaced by "bug_when"',
        'field': 'replaced by "fieldid"',
        },

    'groups': {
        'bit': 'replaced by "PRIMARY"',
        },

    'longdescs': {
        'thetext': 'replaced by %(the-table-bugs_fulltext)s',
        },

    'milestones': {
        'product': 'replaced by "product_id"',
        },

    'namedqueries': {
        'watchfordiffs': None,
        },

    'profile_search': {
        'profile_search_user_id': 'renamed to %(index-profile_search-profile_search_user_id_idx)s',
        },

    'series': {
        'creator': None,
        },

    }

index_added_remark = {
    'bugs': {
        'alias': None,
        'component_id': 'replacing "component"',
        'product_id': 'replacing "product"',
        'qa_contact': None,
        'target_milestone': None,
        'op_sys': None,
        'creation_ts': None,
        'short_desc': None,
        'votes': None,
    },

    'bug_see_also': {
        'PRIMARY': None,
    },

    'bug_severity': {
        'bug_severity_visibility_value_id_idx': None,
    },
    
    'bug_status': {
        'bug_status_visibility_value_id_idx': None,
    },
    
    'attachments': {
        'attachments_submitter_id_idx': None,
        'attachments_modification_time_idx': None,
    },

    'bugs_activity': {
        'bug_when': 'replacing "when"',
        'bugs_activity_who_idx': None,
        'bugs_activity_added_idx': None,
        'fieldid': 'replacing "field"',
        'field': None,
        },

    'cc': {
        'bug_id': None,
        'who': None,
        },

    'components': {
        'PRIMARY': None,
        'name': None,
        'product_id': None,
        },

    'fielddefs': {
        'fielddefs_value_field_id_idx': None,
        'fielddefs_is_mandatory_idx': None,
    },
    
    'flags': {
        'flags_type_id_idx': None,
    },

    'groups': {
        'PRIMARY': 'replacing "bit"',
        },

    'longdescs': {
        'PRIMARY': None,
        'who': None,
        'thetext': None,
        },

    'milestones': {
        'PRIMARY': None,
        'product_id': 'replacing "product"',
        },

    'namedqueries': {
        'PRIMARY': None,
        },

    'op_sys': {
        'op_sys_visibility_value_id_idx': None,
        },

    'priority': {
        'priority_visibility_value_id_idx': None,
        },

    'profiles': {
        'profiles_extern_id_idx': None,
        },

    'rep_platform': {
        'rep_platform_visibility_value_id_idx': None,
        },

    'resolution': {
        'resolution_visibility_value_id_idx': None,
        },

    'products': {
        'PRIMARY': None,
        'name': None,
        },

    'profile_search': {
        'profile_search_user_id_idx': 'renamed from %(index-profile_search-profile_search_user_id_idx)s',
        },

    'series': {
        'series_category_idx': None,
    },

    'versions': {
        'PRIMARY': None,
        'versions_product_id_idx': None,
    },

    }

notation_guide="""
<h3><a id="notes-colours" name="notes-colours">Schema Change Notation</a></h3>

<p>Where the Bugzilla schema has been changed between
%(FIRST_VERSION)s and %(LAST_VERSION)s, the change is noted in this
document and marked out with color.</p>

<p>In the schema tables themselves, changed fields are noted and
colored as follows:</p>

<table border="1" cellspacing="0" cellpadding="5">

  <tr bgcolor="#ffffff" valign="top" align="left">

    <td>A field whose definition and use which has not changed between
    %(FIRST_VERSION)s and %(LAST_VERSION)s.</td>

  </tr>

  <tr bgcolor="#ffcccc" valign="top" align="left">

    <td>A field which was present in some previous Bugzilla release
    but which is absent from %(LAST_VERSION)s.</td>

  </tr>

  <tr bgcolor="#ccffcc" valign="top" align="left">

    <td>A field which is present in %(LAST_VERSION)s but was absent in
    some previous Bugzilla release.</td>

  </tr>

  <tr bgcolor="#ccccff" valign="top" align="left">

    <td>A field whose definition has changed over time.</td>

  </tr>

</table>
"""

# This page header and footer are used when generating a schema doc
# standalone rather than through CGI.

header = ["""<?xml version="1.0" encoding="UTF-8"?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "DTD/xhtml1-transitional.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">

<head>

<title>Bugzilla database schema</title>

</head>

<body bgcolor="#FFFFFF" text="#000000" link="#000099" vlink="#660066" alink="#FF0000">

<div align="center">

<p>
<a href="/">Ravenbrook</a>
/ <a href="/project/">Projects</a>
/ <a href="/project/bugzilla-schema/">Bugzilla Schema</a>
/ <a href="/project/bugzilla-schema/master/">Master Code</a>
</p>

<hr />

<h1>Bugzilla database schema</h1>

<address>
<a href="http://www.ravenbrook.com/">Ravenbrook Limited</a>,
dynamically generated on %(DATE)s</address>

</div>
"""]

footer = ["""
<hr />

<p> <small>This document is copyright &copy; 2001-2003 Perforce Software, Inc.  All rights reserved.</small> </p>

<p> <small>Redistribution and use of this document in any form, with or without modification, is permitted provided that redistributions of this document retain the above copyright notice, this condition and the following disclaimer.</small> </p>

<p> <small> <strong> This document is provided by the copyright holders and contributors "as is" and any express or implied warranties, including, but not limited to, the implied warranties of merchantability and fitness for a particular purpose are disclaimed. In no event shall the copyright holders and contributors be liable for any direct, indirect, incidental, special, exemplary, or consequential damages (including, but not limited to, procurement of substitute goods or services; loss of use, data, or profits; or business interruption) however caused and on any theory of liability, whether in contract, strict liability, or tort (including negligence or otherwise) arising in any way out of the use of this document, even if advised of the possibility of such damage. </strong> </small> </p>

<div align="center">

<p>
<a href="/">Ravenbrook</a> /
<a href="/project/">Projects</a> /
<a href="/project/p4dti/">Perforce Defect Tracking Integration</a> /
<a href="/project/p4dti/version/2.2/">Version 2.2 Product Sources</a> /
<a href="/project/p4dti/version/2.2/design/">Design</a>
</p>

</div>

</body>

</html>
""",
]

# This prelude is included in the generated schema doc prior to the
# schema itself.

prelude=["""

<center>
<p>Quick links to <a href="#notes-tables">table definitions</a>:</p>

%(QUICK_TABLES_TABLE)s</center>

<h2><a id="section-1" name="section-1">1. Introduction</a></h2>

<p>This document describes the Bugzilla database schema for Bugzilla
%(BUGZILLA_VERSIONS)s.</p>

<p>This document is generated automatically by a Python script which
constructs and colors the schema tables from the stored results of
MySQL queries.  For more information about the scripts, see <a
href="code.html"><code>code.html</code></a>.</p>

<p>The purpose of this document is to act as a reference for
developers of Bugzilla and of code which interacts with Bugzilla
(e.g. P4DTI).</p>

<p>The intended readership is P4DTI developers and Bugzilla developers
and administrators.</p>

<p>This document is not confidential.</p>

<p>Please send any comments to <a
href="mailto:p4dti-comments@ravenbrook.com">&lt;p4dti-comments@ravenbrook.com&gt;</a>,
and problem reports to <a
href="mailto:p4dti-support@ravenbrook.com">&lt;p4dti-support@ravenbrook.com&gt;</a>.</p>

<h2><a id="section-2" name="section-2">2. Bugzilla overview</a></h2>

<p>Bugzilla is a defect tracking system, written in Perl with a CGI
web GUI.  By default it uses MySQL to store its tables.""",

('2.22', None, """%(VERSION_STRING)s PostgreSQL is also supported."""),

"""</p>

%(NOTATION_GUIDE)s

<h3><a id="notes-bugs" name="notes-bugs">Bugs</a></h3>

<p>Each defect is called a <b>bug</b> and corresponds to one row in
%(the-table-bugs)s.  It is identified by its number,
%(column-bugs-bug_id)s.</p>

<h3><a id="notes-products" name="notes-products">Products and components</a></h3>

<p>The work managed by Bugzilla is divided into products.  The work
for each product is in turn divided into the components of that
product.  Several properties of a new bug (e.g. ownership) are
determined by the product and component to which it belongs.  Each
component is represented by a row in %(the-table-components)s.""",

('2.2', None, """ %(VERSION_STRING)sEach product is represented by a
row in %(the-table-products)s."""),

"""</p>""",

("2.19.1", None, """

<p>%(VERSION_STRING)sProducts are grouped by "classification".  This
is optional and controlled by the parameter 'useclassification'.  The
classifications are used to help in finding bugs and in constructing
meaningful time series, but have no other semantics in Bugzilla.
There is a default classification, with ID 1, meaning
"Unclassified".</p> """),

"""<h3><a id="notes-workflow" name="notes-workflow">Workflow</a></h3>

<p>Each bug has a status (%(column-bugs-bug_status)s).  If a bug has a
status which shows it has been resolved, it also has a resolution
(%(column-bugs-resolution)s), otherwise the resolution field is empty.</p>""",

('3.1.1', None, """<p>%(VERSION_STRING)sWorkflow is configurable.  The
possible status values are stored in %(the-table-bug_status)s; the
transitions in %(the-table-status_workflow)s.</p>"""),

"""<p>This table shows the possible values and valid transitions of
the status field in the default workflow.</p>

<table border="1" cellspacing="0" cellpadding="5">
  <tr valign="top" align="left">

    <th>Status</th>

    <th>Resolved?</th>

    <th>Description</th>

    <th>Transitions</th>

  </tr>

""",
('2.10', '3.6.13',
"""<tr%(VERSION_COLOUR)s valign="top" align="left">

    <td>UNCONFIRMED</td>

    <td>No</td>

    <td>%(VERSION_STRING)sA new bug, when a product has voting</td>

    <td>to NEW by voting or confirmation<br />
        to ASSIGNED by acceptance<br />
        to RESOLVED by resolution<br />
    </td>

  </tr>"""),
('3.7.1', None,
"""<tr%(VERSION_COLOUR)s valign="top" align="left">

    <td>UNCONFIRMED</td>

    <td>No</td>

    <td>%(VERSION_STRING)sA new bug, when a product allows UNCONFIRMED</td>

    <td>to NEW by confirmation<br />
        to ASSIGNED by acceptance<br />
        to RESOLVED by resolution<br />
    </td>

  </tr>"""),

"""<tr valign="top" align="left">

    <td>NEW</td>

    <td>No</td>

    <td>Recently added or confirmed</td>

    <td>to ASSIGNED by acceptance<br />
        to RESOLVED by analysis and maybe fixing<br />
        to NEW by reassignment<br />
    </td>

  </tr>

  <tr valign="top" align="left">

    <td>ASSIGNED</td>

    <td>No</td>

    <td>Has been assigned</td>

    <td>to NEW by reassignment<br />
        to RESOLVED by analysis and maybe fixing<br />
    </td>

  </tr>

  <tr valign="top" align="left">

    <td>REOPENED</td>

    <td>No</td>

    <td>Was once resolved but has been reopened</td>

    <td>to NEW by reassignment<br />
        to ASSIGNED by acceptance<br />
        to RESOLVED by analysis and maybe fixing<br />
    </td>

  </tr>

  <tr valign="top" align="left">

    <td>RESOLVED</td>

    <td>Yes</td>

    <td>Has been resolved (e.g. fixed, deemed unfixable, etc.  See "resolution" column)</td>

    <td>to REOPENED by reopening<br />
        to VERIFIED by verification<br />
        to CLOSED by closing<br />
    </td>

  </tr>

  <tr valign="top" align="left">

    <td>VERIFIED</td>

    <td>Yes</td>

    <td>The resolution has been approved by QA</td>

    <td>to CLOSED when the product ships<br />
        to REOPENED by reopening<br />
    </td>

  </tr>

  <tr valign="top" align="left">

    <td>CLOSED</td>

    <td>Yes</td>

    <td>Over and done with</td>

    <td>to REOPENED by reopening</td>

  </tr>
</table>

<p>This table shows the allowable values of the resolution field.  The
values "FIXED", "MOVED", and "DUPLICATE" have special meaning for
Bugzilla.  The other values may be changed, """,
(None, '2.19.2', """%(VERSION_STRING)sby editing the schema of %(the-table-bugs)s, """),
('2.19.3', '2.23.2', """%(VERSION_STRING)sby manually updating %(the-table-resolution)s, """),
('2.23.3', None, """%(VERSION_STRING)sby using editvalues.cgi, """),

"""to add, remove, or rename values as necessary.</p>

<table border="1" cellspacing="0" cellpadding="5">
  <tr valign="top" align="left">

    <th>Resolution</th>

    <th>Meaning</th>

  </tr>

  <tr>

    <td>FIXED</td>

    <td>The bug has been fixed.</td>

  </tr>

  <tr>

    <td>INVALID</td>

    <td>The problem described is not a bug.</td>

  </tr>

  <tr>

    <td>WONTFIX</td>

    <td>This bug will never be fixed.</td>

  </tr>

  <tr>

    <td>LATER</td>

    <td>This bug will not be fixed in this version.</td>

  </tr>

  <tr>

    <td>REMIND</td>

    <td>This bug probably won't be fixed in this version.</td>

  </tr>

  <tr>

    <td>DUPLICATE</td>

    <td>This is a duplicate of an existing bug A description comment
        is added to this effect""",

        ('2.12', None, """, and %(VERSION_STRING)sa record is added to
        %(the-table-duplicates)s"""),

""".</td> </tr>

  <tr>

    <td>WORKSFORME</td>

    <td>This bug could not be reproduced.</td>

  </tr>

""",
('2.12', None,
"""  <tr%(VERSION_COLOUR)s>

    <td>MOVED</td>

    <td>%(VERSION_STRING)sThis bug has been moved to another database.</td>

</tr>
"""),
"""</table>

<h3><a id="notes-users" name="notes-users">Users</a></h3>

<p>Bugzilla has users.  Each user is represented by one row in
%(the-table-profiles)s.  Each user is referred by a number
(%(column-profiles-userid)s) and an email address
(%(column-profiles-login_name)s).</p>

<h3><a id="notes-authentication" name="notes-authentication">Authentication</a></h3>

""",

('2.19.1', None,"""<p>%(VERSION_STRING)sThere are various
authentication mechanisms, including "environment variable
authentication" (Bugzilla/Auth/Login/WWW/Env.pm) which uses
environment variables to pass an external user ID
(%(column-profiles-extern_id)s) to the Bugzilla CGI.  The rest of this
section describes the password-based authentication which has always
been in Bugzilla and which is still widely used.</p>"""),

"""<p>Each user has a password, used to authenticate that user to
Bugzilla.  The password is stored in %(column-profiles-cryptpassword)s in
encrypted form.""",

(None, '2.12', """  %(VERSION_STRING)s it is also stored in
%(column-profiles-password)s as plaintext."""),

"""</p>

<p>On a successful login, Bugzilla generates a pair of cookies for the
user's browser.  On subsequent accesses, a user gets access if these
cookie checks pass:</p>

<ul>

  <li>they have both Bugzilla_login and Bugzilla_logincookie cookies;</li>""",

(None, '2.17.3',"""<li>%(VERSION_STRING)sTheir Bugzilla_login is the
  %(column-profiles-login_name)s of a row in
  %(the-table-profiles)s;</li>"""),

('2.17.4', None,"""<li>%(VERSION_STRING)sTheir Bugzilla_login is the
  %(column-profiles-userid)s of a row in
  %(the-table-profiles)s;</li>"""),

"""
  <li>their Bugzilla_logincookie matches a row in %(the-table-logincookies)s;</li>

  <li>the userids of these two rows match;</li>

""",

(None, '2.14.5',
"""<li>%(VERSION_STRING)sthe cryptpasswords of these two rows match;</li>

  """),

(None, '2.14.1',
"""<li>%(VERSION_STRING)s%(column-logincookies-hostname)s matches the CGI REMOTE_HOST;</li>

  """),

('2.14.2', None,
"""<li>%(VERSION_STRING)s%(column-logincookies-ipaddr)s matches the CGI REMOTE_ADDR;</li>

  """),

('2.10', '4.1.2',
"""<li>%(VERSION_STRING)s%(column-profiles-disabledtext)s is empty.</li>
  """),

('4.1.3', None,
"""<li>%(VERSION_STRING)s%(column-profiles-is_enabled)s is 1.</li>
  """),

"""</ul>

<p>If the cookie checks fail, the user has to login (with their
password), in which case a new row is added to
%(the-table-logincookies)s and the user gets a new pair of
cookies.</p>

<p>Rows in %(the-table-logincookies)s are deleted after 30 days (at
user login time).</p>""",

('2.8', '3.6.13', """<h3><a id="notes-voting" name="notes-voting">Voting</a></h3>

<p>%(VERSION_STRING)sUsers may vote for bugs which they think are
important.  A user can vote for a bug more than once.  Votes are
recorded in %(the-table-votes)s.</p>"""),

('2.10', '3.6.13', """%(VERSION_STRING)sThe maximum number of votes per
bug per user is product-dependent.  Whether or not project managers
pay any attention to votes is up to them, apart from the "confirmation
by acclamation" process, which is as follows:</p>

<p>New bugs have the status UNCONFIRMED.  To enter the main workflow,
they need the status NEW.  To get the status NEW, they need a
particular number of votes which is product-dependent.</p>"""),

('2.10', None, """<h3><a id="notes-milestones" name="notes-milestones">Milestones</a></h3>

<p>%(VERSION_STRING)sProducts may have "milestones" defined.  The
intention is that a milestone should be a point in a project at which
a set of bugs has been resolved.  An example might be a product
release or a QA target.  Milestones may be turned on and off with the
parameter "usetargetmilestone".</p>

<p>If milestones are on, each bug has a "target milestone" (by which
it should be fixed).  A product may have a URL associated with it
which locates a document describing the milestones for that product.
This document itself is entirely outside Bugzilla.  A product may also
have a default target milestone, which is given to new bugs.</p>

<p>Milestones for a product have a "sort key", which allows them to be
presented in a specific order in the user interface.</p>

<p>Milestones are kept in %(the-table-milestones)s.</p>"""),

"""<h3><a id="notes-versions" name="notes-versions">Versions</a></h3>

<p>Products may have versions.  This allows more accurate bug
reporting: "we saw it in 1.3.7b3".""", ('2.10', None, """Versions are
totally independent of milestones."""),

"""</p>

<h3><a id="notes-parameters" name="notes-parameters">Parameters</a></h3>

<p>The operation of Bugzilla is controlled by parameters.  These are
set in editparams.cgi.  The current values are stored in data/params.
They are <b>not</b> stored in the database.</p>
<p>""",
(None, '2.21.1', """%(VERSION_STRING)sThe set of parameters is defined in defparams.pl."""),
('2.22rc1',None,"""%(VERSION_STRING)sThe set of parameters is defined in the modules in Bugzilla/Config/."""),
"""</p>

""",

('2.4', None, """<h3><a id="notes-groups" name="notes-groups">Groups</a></h3>

<p>%(VERSION_STRING)sBugzilla has "groups" of users.  Membership of a
group allows a user to perform certain tasks.  Each group is
represented by a row of %(the-table-groups)s.</p>

<p>There are a number of built-in groups, as follows:</p>

<table border="1" cellspacing="0" cellpadding="5">
  <tr align="left" valign="top">

    <th>Name</th>

    <th>Description</th>

  </tr>

"""),

('2.17.1', None, """  <tr %(VERSION_COLOUR)s align="left" valign="top">

    <td>admin</td>

    <td>%(VERSION_STRING)s Can administer all aspects of Bugzilla</td>

  </tr>

"""),

('2.4', None, """ <tr align="left" valign="top">

    <td>tweakparams</td>

    <td>Can tweak operating parameters</td>

  </tr>"""),

('2.4', '2.8', """<tr %(VERSION_COLOUR)s align="left" valign="top">

    <td>editgroupmembers</td>

    <td>%(VERSION_STRING)sCan put people in and out of groups</td>

  </tr>"""),

('2.10', None, """<tr %(VERSION_COLOUR)s align="left" valign="top">

    <td>editusers</td>

    <td>Can edit or disable users</td>

  </tr>"""),

('2.4', None, """<tr align="left" valign="top">

    <td>creategroups</td>

    <td>Can create and destroy groups</td>

  </tr>

  <tr align="left" valign="top">

    <td>editcomponents</td>

    <td>Can create, destroy, and edit components and other controls (e.g. flagtypes).</td>

  </tr>"""),

  ('2.10', None, """<tr %(VERSION_COLOUR)s align="left" valign="top">

    <td>editkeywords</td>

    <td>%(VERSION_STRING)sCan create, destroy, and edit keywords</td>

  </tr>

  <tr %(VERSION_COLOUR)salign="left" valign="top">

    <td>editbugs</td>

    <td>%(VERSION_STRING)sCan edit all aspects of any bug</td>

  </tr>

  <tr %(VERSION_COLOUR)salign="left" valign="top">

    <td>canconfirm</td>

    <td>%(VERSION_STRING)sCan confirm a bug</td>

  </tr>"""),

('2.19.1', None, """  <tr %(VERSION_COLOUR)s align="left" valign="top">

    <td>editclassifications</td>

    <td>%(VERSION_STRING)s Can edit classifications</td>

  </tr>

  <tr %(VERSION_COLOUR)s align="left" valign="top">

    <td>bz_canusewhines</td>

    <td>%(VERSION_STRING)s Can configure whine reports for self</td>

  </tr>

  <tr %(VERSION_COLOUR)s align="left" valign="top">

    <td>bz_canusewhineatothers</td>

    <td>%(VERSION_STRING)s Can configure whine reports for other users</td>

  </tr>

"""),

('2.22rc1', None, """  <tr %(VERSION_COLOUR)s align="left" valign="top">

    <td>bz_sudoers</td>

    <td>%(VERSION_STRING)s Can impersonate another user</td>

  </tr>

  <tr %(VERSION_COLOUR)s align="left" valign="top">

    <td>bz_sudo_protect</td>

    <td>%(VERSION_STRING)s Cannot be impersonated</td>

  </tr>

"""),

('2.4', None, """</table>

<p>New groups may be added and used to control access to sets of bugs.
These "bug groups" have %(column-groups-isbuggroup)s set to 1.  A bug
may be in any number of bug groups.  To see a bug, a user must be a
member of all the bug groups which the bug is in.</p>"""),

('2.10', None, """<p>%(VERSION_STRING)sIf the parameter "usebuggroups"
is on, each product automatically has a bug group associated with it.
If the parameter "usebuggroupsentry" is also on, a user must be in the
product's bug group in order to create new bugs for the
product.</p>"""),

('2.10', None, """<p>%(VERSION_STRING)sUsers may be added to a group
by any user who has the "bless" property for that group.  The "bless"
property itself may only be conferred by an administrator.</p>"""),

('2.4', None, """<p>Group membership for new users and new groups is
determined by matching %(column-groups-userregexp)s against the user's
email address."""),

('2.10', None, """%(VERSION_STRING)sThe default configuration has
universal regexps for the "editbugs" and "canconfirm" groups."""),

('2.4', None, """</p>

<p>"""),

('2.4', '2.16.7', """%(VERSION_STRING)sEach group corresponds to a bit
in a 64-bit bitset, %(column-groups-bit)s.  User
membership in a group is conferred by the bit being set in %(column-profiles-groupset)s.  Bug
membership in a bug group is conferred by the bit being set in %(column-bugs-groupset)s."""),

('2.10', '2.16.7', """%(VERSION_STRING)sThe bless
privilege for a group is conferred by the bit being set in %(column-profiles-blessgroupset)s."""),

('2.17.1', None, """%(VERSION_STRING)sUser membership in a group is
conferred by a row in %(the-table-user_group_map)s, with
%(column-user_group_map-isbless)s set to 0.  The bless privilege for a
group is conferred by a row with %(column-user_group_map-isbless)s set
to 1.  Bug membership in a bug group is conferred by a row in
%(the-table-bug_group_map)s."""),

('2.4', None, """</p>"""),

('2.17.1', None, """<p>%(VERSION_STRING)sGroups may be configured so
that membership in one group automatically confers membership or the
"bless" privilege for another group.  This is controlled by
%(the-table-group_group_map)s.</p>"""),

('2.19.1', None, """<p>%(VERSION_STRING)sGroups may be configured so
that the existence of a group is not visible to members of another
group. This is controlled by %(the-table-group_group_map)s.</p>"""),

('2.17.3', None, """<p>%(VERSION_STRING)sA product may be configured
so that membership in one or more groups is required to perform
certain actions on bugs in the product.  Whether or not a new bug for
the product is placed in a group is also configurable (note that user
membership in a group is required to place an existing bug in that
group).  All this is controlled by %(the-table-group_control_map)s.</p>

<p>The %(column-group_control_map-membercontrol)s and
%(column-group_control_map-othercontrol)s
columns of that table determine the treatment of a given group for a
new bug in a given product, depending on whether the bug is being
created by a member or non-member of that group respectively.  The
possible values of these columns are as follows:</p>

<table border="1" cellspacing="0" cellpadding="5">
<tr>
  <th>value</th>
  <th>name</th>
  <th>meaning</th>
</tr>

<tr>
  <td>0</td>
  <td>NA</td>
  <td>A bug for this product cannot be placed in this group.</td>
</tr>

<tr>
  <td>1</td>
  <td>Shown</td>
  <td>A bug for this product may be placed in this group, but will not be by default.</td>
</tr>

<tr>
  <td>2</td>
  <td>Default</td>
  <td>A bug for this product may be placed in this group, and is by default.</td>
</tr>

<tr>
  <td>3</td>
  <td>Mandatory</td>
  <td>A bug for this product is always placed in this group.</td>
</tr>
</table>

<p>Only certain combinations of membercontrol/othercontrol are
permitted, as follows:</p>

<table border="1" cellspacing="0" cellpadding="5">
 <tr>
  <th>membercontrol</th>
  <th>othercontrol</th>
  <th>Notes</th>
</tr>
<tr>
  <td>0(NA)</td>
  <td>0(NA)</td>
  <td>A bug for this product can never be placed in this group (so the
  option isn't presented).</td>

</tr>

<tr>
  <td rowspan="4">1 (Shown)</td>
  <td>0(NA)</td>
  <td>Only members can place a bug in this group.<b>This is the default setting.</b></td>
</tr>

<tr>
  <td>1 (Shown)</td>
  <td>Anyone can place a new bug in this group.</td>
</tr>

<tr>
  <td>2 (Default)</td>
  <td>Anyone can place a bug in this group, and
  non-members will do so by default.</td>
</tr>

<tr>
  <td>3 (Mandatory)</td>
  <td>Anyone can place a bug in this group, and non-members will always do so.</td>
</tr>

<tr>
  <td rowspan="3">2 (Default)</td>
  <td>0(NA)</td>
  <td>Only members can place a bug in this group, and do so by default.</td>
</tr>

<tr>
  <td>2 (Default)</td>
  <td>Anyone can place a bug in this group, and does so by default.</td>
</tr>

<tr>
  <td>3 (Mandatory)</td>
  <td>Members can place a bug in this group, and do so by default.
  Non-members always place a bug in this group.</td>
</tr>

<tr>
  <td>3(Mandatory)</td>
  <td>3(Mandatory)</td>
  <td>A bug for this product can never be removed from this group (so
  the option isn't presented).</td>
</tr>
</table>

"""),

('2.6', None, """<h3><a id="notes-attachments" name="notes-attachments">Attachments</a></h3>

<p>%(VERSION_STRING)sUsers can upload attachments to bugs.  An
attachments can be marked as a patch.  Attachments are stored in
%(the-table-attachments)s."""),

('2.16rc1', '2.16.7', """%(VERSION_STRING)sAttachments can be marked as
"obsolete"."""),

('2.6', '2.20.7', """%(VERSION_STRING)sAttachment data is stored in
%(column-attachments-thedata)s."""),

('2.21.1', None, """%(VERSION_STRING)sAttachment data is stored in
%(the-table-attach_data)s."""),

('2.22rc1', None, """%(VERSION_STRING)sAttachments can be URLs, marked
by the flag %(column-attachments-isurl)s.  The URL itself is stored in
%(column-attach_data-thedata)s."""),

"""</p>""",

('2.16rc1', '2.16.7', """<p>%(VERSION_STRING)sEach attachment may have
one of a number of "status" keywords associated with it.  The status
keywords are user-defined on a per-product basis.  The set of status
keywords is defined in %(the-table-attachstatusdefs)s.  Whether a
given attachment has a given status keyword is defined by
%(the-table-attachstatuses)s.</p>"""),

('2.17.1', None, """<p>%(VERSION_STRING)sAttachment statuses are
implemented with the <a href="#notes-flags">flags</a> system.</p>"""),

('2.17.1', None, """

<h3><a id="notes-flags" name="notes-flags">Flags</a></h3>

<p>%(VERSION_STRING)sBugs and attachments may be marked with "flags".
The set of flag types is user-defined (using editflagtypes.cgi).  For
instance, a flag type might be "candidate for version 7.3 triage", or
"7.3" for short.  Flag types are recorded in %(the-table-flagtypes)s.
Each flag type is either for bugs or for attachments, not both.</p>

<p>Actual flags are recorded in %(the-table-flags)s.  Each flag has a
status of "+" ("granted"), "-" ("denied") or "?" ("requested").  For
instance, one bug might have flag "7.3+", and another might have flag
"7.3-".</p>

<p>A status of "?" indicates that a user has requested that this item
be given this flag.  There is an special interface for viewing request
flags (request.cgi).  A request flag may be marked for the attention
of a particular user, the "requestee".</p>

<p>A flag type may have a "CC list" of email addresses, of people to
notify when a flag is requested.</p>

<p>By default, a single bug or attachment may receive several flags of
the same type, with the same or different statuses and the same or
different requestees.  This may be disabled for any given flag
type.</p>

<p>Particular flag types may only be available to bugs in certain
products and components (or their attachments).  This is recorded in
%(the-table-flaginclusions)s.  Particular flag types may <em>not</em>
be available to bugs in certain products and components (or their
attachments).  This is recorded in %(the-table-flagexclusions)s.</p>

<p>Various features of flag types may be disabled: they can be made
inactive, not requestable, not "requesteeable", not "multiplicable".</p>

"""),

('2.10', None, """

<h3><a id="notes-keywords" name="notes-keywords">Keywords</a></h3>

<p>%(VERSION_STRING)sBugzilla users can define a number of keywords,
and then give each bug a set of keywords.  This is mainly for use in
finding related bugs.  The keywords are stored in
%(the-table-keyworddefs)s, and the one-to-many mapping from bugs to
keywords is stored in %(the-table-keywords)s, and also in
%(column-bugs-keywords)s.</p>

"""),

('2.6', None, """<h3><a id="notes-dependencies" name="notes-dependencies">Dependencies</a></h3>

<p>%(VERSION_STRING)sBugs may depend on other bugs being fixed.  That
is, it may be impossible to fix one bug until another one is fixed.
Bugzilla records and displays such information and uses it to notify
users when a bug changes (all contacts for all dependent bugs are
notified when a bug changes).</p>

<p>Dependencies are recorded in %(the-table-dependencies)s.</p>"""),

"""<h3><a id="notes-activity" name="notes-activity">Activity</a></h3>

<p>Bugzilla keeps a record of changes made to bugs.  This record is in
%(the-table-bugs_activity)s.  Each row in this table records a change
to a field in %(the-table-bugs)s.""",

('2.10', None, """%(VERSION_STRING)sThe fields are referred to by a
number which is looked up in %(the-table-fielddefs)s.  This table
records the name of the field and also a longer description used to
display activity tables."""),

"""</p>

<h3><a id="notes-severity" name="notes-severity">Severity</a></h3>

<p>Each bug has a "severity" field, %(column-bugs-bug_severity)s,
indicating the severity of the impact of the bug.  There is no code in
Bugzilla which distinguishes the values of this field, although it may
naturally be used in queries.""",

('2.19.3', None, """%(VERSION_STRING)sThe set of values available for
this field is stored in %(table-bug_severity)s and can be controlled
by the administrator. """),

"""The intended meanings of the built-in values of this field are as
follows:</p>

<table border="1" cellspacing="0" cellpadding="5">
  <tr align="left" valign="top">

    <th>Value</th>

    <th>Intended meaning</th>

  </tr>

  <tr align="left" valign="top">

    <td>Blocker</td>

    <td>Blocks development and/or testing work</td>

  </tr>

  <tr align="left" valign="top">

    <td>Critical</td>

    <td>Crashes, loss of data, severe memory leak</td>

  </tr>

  <tr align="left" valign="top">

    <td>Major</td>

    <td>Major loss of function</td>

  </tr>

  <tr align="left" valign="top">

    <td>Minor</td>

    <td>Minor loss of function, or other problem where easy workaround is present</td>

  </tr>

  <tr align="left" valign="top">

    <td>Trivial</td>

    <td>Cosmetic problem</td>

  </tr>

  <tr align="left" valign="top">

    <td>Enhancement</td>

    <td>Request for enhancement</td>

  </tr>
</table>

<h3><a id="notes-email" name="notes-email">Email notification</a></h3>

<p>When a bug changes, email notification is sent out to a number of
users:</p>

<ul>
  <li>The bug's owner (%(column-bugs-assigned_to)s)</li>
  <li>The bug's reporter (%(column-bugs-reporter)s)</li>
  <li>The bug's QA contact, if the "useqacontact" parameter is set (%(column-bugs-qa_contact)s)</li>
  <li>All the users who have explicitly asked to be notified when the bug changes (these users are stored in %(the-table-cc)s).</li>
  <li>All the users who have voted for this bug (recorded in %(the-table-votes)s).</li>
</ul>

<p>""",

('2.12', None , """%(VERSION_STRING)sIndividual users may filter
these messages according to the way in which the bug changes and their
relationship to the bug.
"""),

('2.12', '2.19.2' , """%(VERSION_STRING)sThese filtering preferences are
recorded in %(column-profiles-emailflags)s.
"""),

('2.19.3', None , """%(VERSION_STRING)sThese filtering preferences are
recorded in the %(table-email_setting)s table.
"""),

('2.12', None, """</p>

<p>"""),

(None, '2.17.3', """%(VERSION_STRING)sThis is handled by the "processmail" script.  """),

('2.17.4', None, """%(VERSION_STRING)sThis is handled by the
Bugzilla::Bugmail module, which is invoked by the template system
(from Bugzilla::Template) when it encounters a call to SendBugMail()
in a template.  """),

('3.3.1', None, """</p>%(VERSION_STRING)sIf the parameter
"use_mailer_queue" is set, all email is queued to be sent
asynchronously.  This is managed by a third-party general-purpose Perl
job queueing system called TheSchwartz, using several database tables
of its own (%(table-ts_error)s, %(table-ts_exitstatus)s,
%(table-ts_funcmap)s, %(table-ts_job)s, and %(table-ts_note)s)."""),

"""</p>

<h3><a id="notes-descriptions" name="notes-descriptions">Long descriptions</a></h3>

<p>Each bug has a number of comments associated with it. """,

(None, '2.8', """%(VERSION_STRING)sThese are stored concatenated in
%(column-bugs-long_desc)s"""),

('2.10', None, """%(VERSION_STRING)sThese are stored individually in
%(the-table-longdescs)s."""),

"""</p>

<p>They are displayed as the "Description" on the bug form, ordered by
date and annotated with the user and date.  Users can add new comments
with the "Additional comment" field on the bug form.</p>""",

('2.10', None, """<h3><a id="notes-namedqueries" name="notes-namedqueries">Named queries</a></h3>

<p>%(VERSION_STRING)sUsers can name queries.  Links to named query
pages appear in a navigation footer bar on most Bugzilla pages.  A
query named "(Default query)" is a user's default query.  Named
queries are stored in %(the-table-namedqueries)s.</p>

"""),

('2.23.3', None, """<p>%(VERSION_STRING)sIf the parameter
"querysharegroup" is set, it names a group of users who are empowered
to share named queries.  An empowered user can share a given named
query they create with all the members of a group, as long as he or
she has the "bless" property for that group.  A query can only be
shared with a single group.  Sharing is recorded in
%(the-table-namedquery_group_map)s.</p>

<p>%(VERSION_STRING)sAny user able to use a given named query can
control whether or not that query appears in his or her navigation
footer bar.  This is recorded in
%(the-table-namedqueries_link_in_footer)s.</p>

"""),

('2.17.5', None,

"""<h3><a id="notes-charts" name="notes-charts">Charts</a></h3>

<p>%(VERSION_STRING)sBugzilla can draw general time-series charts.
There are a number of default time series.  Each product has a default
series for each bug status or resolution (for instance "how many bugs
are INVALID in product Foo") and each component has a default series
for all open bugs (UNCONFIRMED/NEW/ASSIGNED/REOPENED) and one for all
closed bugs (RESOLVED/VERIFIED/CLOSED).  A user can also define a new
time series based on any query, and give it a "frequency" (actually a
period, measured in days).  The set of series is stored in
%(the-table-series)s.</p>

<p>To collect the data for the time series, the Bugzilla administrator
needs to arrange for the collectstats.pl script to be run every day.
This script stores the data in %(the-table-series_data)s.</p>

<p>Series have categories and subcategories, which are provided in
order to make it easier to manage large numbers of series.  They are
normalized in %(the-table-series_categories)s.</p>
"""),

('2.17.5', None, """<p>By default, a time series is "private": only
visible to the user who created it. An administrator may make a time
series "public", or visible to other users."""),

('2.17.5', '2.18rc2', """%(VERSION_STRING)s this is determined by the
"subscription" system (see below)."""),

('2.18rc3', None, """%(VERSION_STRING)sthis is determined by
%(column-series-public)s."""),

('2.17.5', None, """</p>

"""),

('2.17.5', '2.18rc2', """<p>%(VERSION_STRING)sIf a series is "private"
(not "public") then users may "subscribe" to it.  Each user is
automatically subscribed to any series created by that user.  The
subscription is recorded in %(the-table-user_series_map)s.  If all
users unsubscribe from a time series, data will stop being collected
on it (by setting the period to 0 days).  A series is "public" if
%(column-user_series_map-user_id)s is zero.</p> """),

('2.18rc3', None, """<p>%(VERSION_STRING)sVisibility of a time series
to a user is determined on a per-category basis using the groups
system.  The group memberships required to see a time series in a
given category are recorded in %(the-table-category_group_map)s.  A
user may see a time series if they are in all the groups for the
category <em>and</em> either ths user created the series or it is
public.</p>

"""),

('2.10', None, """<h3><a id="notes-watchers"
name="notes-watchers">Watchers</a></h3>

<p>%(VERSION_STRING)sBugzilla lets users "watch" each other; receiving
each other's Bugzilla email.  For instance, if Sam goes on holiday,
Phil can "watch" her, receiving all her Bugzilla email.  This is set
up by the user preferences (userprefs.cgi), recorded in
%(the-table-watch)s and handled by the <a href="#notes-email">email
subsystem</a>.</p>

"""),

('2.10', '2.17.1', """
<h3><a id="notes-shadow" name="notes-shadow">Shadow database</a></h3>

<p>%(VERSION_STRING)s: Bugzilla can maintain a shadow, read-only copy
of everything in another database (with the parameter "shadowdb").  If
the parameter "queryagainstshadowdb" is on, queries were run against
the shadow.  A record of SQL activity since the last reflection is
kept in %(the-table-shadowlog)s.</p>"""),

('2.17.1', None, """
<h3><a id="notes-time-tracking" name="notes-time-tracking">Time tracking</a></h3>

<p>%(VERSION_STRING)s Bugzilla can track time for each bug, if the
"timetrackinggroup" parameter is set.  Members of that group get the
ability to estimate the amount of effort (measured in hours) a bug
will take to fix, either when creating or when editing the bug.
Members of that group are also permitted to record hours of effort
spent on the bug</p>

<p>%(column-longdescs-work_time)s
records each increment of work.  The sum of this column for a bug is
computed to display as "Hours Worked" for the bug.</p>

<p>%(column-bugs-estimated_time)s is
the estimate for how much time the bug will take in total, displayed
as "Orig. Est.".  This can be changed by members of the
timetrackinggroup.</p>

<p>%(column-bugs-remaining_time)s is
the current estimate for how much more time the bug will take to fix,
displayed as "Hours Left".  This can be changed by members of the
timetrackinggroup.</p>

<p>The total of "Hours Left" and "Hours Worked" is shown as "Current
Est.": the current estimate of the total effort required to fix the
bug. "Hours Worked" as a percentage of "Current Est" is shown as "%%
Complete". "Current Est" deducted from "Orig. Est" is shown as
"Gain"</p>"""),

('2.19.3', None, """
<p>%(VERSION_STRING)s%(column-bugs-deadline)s records a calendar deadline for the bug.</p>"""),

"""<h3><a id="notes-whine" name="notes-whine">The Whine System</a></h3>

<p>Bugzilla has a system for sending "whine" email messages to
specified users on a regular basis.  This system relies on the
administrator configuring the Bugzilla server to run a script at
regular intervals (e.g. by using crontab).</p>

<p>The <code>whineatnews.pl</code> script should be run once a day.
For each bug which has status NEW or REOPENED, and which has not
changed for a certain number of days, it sends a message to the bug's
owner.  The number of days is controlled by a Bugzilla parameter
called "whinedays".  The content of the email message is controlled by
a Bugzilla parameter called "whinemail".</p>""",

('2.19.1', None, """<p>%(VERSION_STRING)sThe <code>whine.pl</code>
script runs a separate whine system, which allows a number of whine
schedules to be established with varying frequency (up to every 15
minutes), criteria, and content of whine messages.  It is configured
with <code>editwhines.cgi</code>.  Obviously, <code>whine.pl</code>
needs to be run every 15 minutes in order to send the most frequent
messages.</p>

<p>Users must be in the bz_canusewhines group to configure whine
messages.  Users must be in the bz_canusewhineatothers group to
configure whine messages <em>to be sent to other users</em>.  These
restrictions are checked when configuring whine messages and also
before messages are sent, so removing a user from one of these groups
will disable any whines which that user has configured.</p>

<p>A whine schedule, stored in %(the-table-whine_schedules)s,
specifies the frequency with which an email should be sent to a
particular user.  The email is specified with a whine event (see
below).  There is a variety of ways of specifying the frequency: both
days (every day, a particular day of the week, weekdays only, a
particular day of the month, the last day of the month) and times (a
particular hour, or every 15, 30, or 60 minutes).</p>

"""),

('2.19.3', None, """
<p>%(VERSION_STRING)sWhines may be scheduled for groups as well as users.</p>"""),

('2.19.1', None, """
<p>A whine schedule, stored in %(the-table-whine_schedules)s,
specifies the frequency with which an email should be sent to a
particular user.  The email is specified with a whine event (see
below).  There is a variety of ways of specifying the frequency: both
days (every day, a particular day of the week, weekdays only, a
particular day of the month, the last day of the month) and times (a
particular hour, or every 15, 30, or 60 minutes).</p>

<p>A whine event, stored in %(the-table-whine_events)s, describes an
email message: subject line and some body text to precede query
results.  A message may consist of more than one whine query.</p>

<p>A whine query, stored in %(the-table-whine_queries)s is a <a
href="#notes-namedqueries">named query</a>, to which a title is given
for use in email messages.  Whine queries are stored in
%(the-table-whine_queries)s.  A whine query may specify that a
separate message is to be sent for each bug found.</p>
"""),

('2.19.3', None, """
<h3><a id="notes-settings" name="notes-settings">Settings</a></h3>

<p>%(VERSION_STRING)sThere are several user-interface preferences,
each of which can take a number of values.  Each preference has a row
in the %(table-setting)s table, and possible values in the
%(table-setting_value)s table.  The administrator may set a default
value for each preference (%(column-setting-default_value)s) and
determine whether users are able to override the default
(%(column-setting-is_enabled)s).  The user's individual preferences
are recorded in the %(table-profile_setting)s table.</p>"""),

"""

<h3><a id="notes-quips" name="notes-quips">Quips</a></h3>

<p>Bugzilla supports "quips": small text messages, often humorous,
which appear along with search results.  The quips are selected at
random from a set.</p>""",

(None, '2.16.7', """<p>%(VERSION_STRING)sThe quips are stored in a
file called "data/comments"."""),

('2.17.1', None, """ %(VERSION_STRING)sThe quips are stored in
%(the-table-quips)s.</p>"""),

('2.14', None, """<p>%(VERSION_STRING)sQuips may be entered or deleted
using <code>quips.cgi</code>.</p>"""),

('2.17.4', None, """<p>%(VERSION_STRING)sQuips may be entered by any
user but must be approved by an administrator before they can be
displayed.</p>"""),

('3.3.2', None, """
<h3><a id="notes-see_also" name="notes-see_also">References to other Bugzillas</a></h3>

<p>%(VERSION_STRING)sBugzilla can record connections to bugs in other
instances of Bugzilla, if the parameter "use_see_also" is set.  The
connections are displayed as clickable URLs and are stored as URLs in
%(the-table-bug_see_also)s.  They are validated according to the
system's notion of a valid form for Bugzilla URLs.</p> """),

('2.23.1', None, """
<h3><a id="notes-customfields" name="notes-customfields">Custom Fields</a></h3>

<p>%(VERSION_STRING)sBugzilla supports custom fields.  Each custom
field is a new column in %(the-table-bugs)s, with a name beginning
<code>cf_</code>.  The presence of each custom field is indicated by a
row in %(the-table-fielddefs)s, with %(column-fielddefs-custom)s set
to 1.  The type of each custom field is specified by
%(column-fielddefs-type)s:

<p>The value 1 (FIELD_TYPE_FREETEXT) indicates a free-form text field
(type varchar(255)).</p>

"""),

('2.23.3', None, """

<p>%(VERSION_STRING)sThe value 2 (FIELD_TYPE_SINGLE_SELECT) indicates
a single-select field (type varchar(64), not null, default '---').
The allowable values of that field are stored in a special table with
the same <code>cf_&lt;name&gt;</code> name as the field, and a schema
like this:</p>

<table border="1" cellpadding="5" cellspacing="0">

<tbody>
<a id="table-customfield" name="table-customfield"><tr align="left" valign="top">
<th>Field</th>
<th>Type</th>
<th>Default</th>
<th>Properties</th>
<th>Remarks</th>
</tr></a>

<tr align="left" valign="top">
<th><a id="column-customfield-id" name="column-customfield-id">id</a></th>
<td>smallint</td>
<td>0</td>
<td>auto_increment</td>
<td>a unique ID.</td>
</tr>

<tr align="left" valign="top">
<th><a id="column-customfield-value" name="column-customfield-value">value</a></th>
<td>varchar(64)</td>
<td>''</td>
<td>-</td>
<td>the text value</td>
</tr>

<tr align="left" valign="top">
<th><a id="column-customfield-sortkey" name="column-customfield-sortkey">sortkey</a></th>
<td>smallint</td>
<td>0</td>
<td>-</td>
<td>a number determining the order in which values appear.</td>
</tr>

<tr align="left" valign="top">
<th><a id="column-customfield-isactive" name="column-customfield-isactive">isactive</a></th>
<td>tinyint</td>
<td>1</td>
<td>-</td>
<td>1 if this value is currently available, 0 otherwise</td>
</tr>
"""),

('3.3.1', None, """
<tr %(VERSION_COLOUR)s align="left" valign="top">
<th><a id="column-customfield-visibility_value_id" name="column-customfield-visibility_value_id">visibility_value_id</a></th>
<td>smallint</td>
<td>0</td>
<td>-</td>
<td>If set, this value is only available if the chooser field (identified by %(column-fielddefs-value_field_id)s) has the value with this ID.  Foreign key &lt;field&gt;.id, for example %(column-products-id)s or <a href="#column-customfield-id">cf_&lt;field&gt;.id</a>.</td>
</tr>
"""),

('2.23.3', None, """

</tbody></table>

<p>Indexes:</p>

<table border="1" cellpadding="5" cellspacing="0">

<tbody>
<tr align="left" valign="top">
<th>Name</th>
<th>Fields</th>
<th>Properties</th>
<th>Remarks</th>
</tr>

<tr align="left" valign="top">
<th><a id="index-customfield-PRIMARY" name="index-customfield-PRIMARY">PRIMARY</a></th>
<td>id</td>
<td>unique</td>
<td>-</td>
</tr>

<tr align="left" valign="top">
<th><a id="index-customfield-cf_field_value_idx" name="index-customfield-cf_field_value_idx">cf_&lt;field&gt;_value_idx</a></th>
<td>value</td>
<td>unique</td>
<td>-</td>
</tr>

<tr align="left" valign="top">
<th><a id="index-customfield-cf_field_sortkey_idx" name="index-customfield-cf_field_sortkey_idx">cf_&lt;field&gt;_sortkey_idx</a></th>
<td>sortkey</td>
 <td>-</td>
<td>-</td>
</tr>

"""),

('3.3.1', None, """
<tr %(VERSION_COLOUR)s align="left" valign="top">
<th><a id="index-customfield-cf_field_visibility_value_id_idx" name="index-customfield-cf_field_visibility_value_id_idx">cf_&lt;field&gt;_visibility_value_id_idx</a></th>
<td>visibility_value_id</td>
<td>-</td>
<td>-</td>
</tr>
"""),

('2.23.3', None, '</tbody></table>'),

('3.1.2', None,

"""<p>%(VERSION_STRING)sThe value 3 (FIELD_TYPE_MULTI_SELECT)
indicates a multi-select field.  The allowable values of that field
are stored in a <code>cf_&lt;name&gt;</code> table as for
FIELD_TYPE_SINGLE_SELECT, above.  The actual values of the field are
not stored in %(the-table-bugs)s, unlike other custom fields, Instead
they are stored in another table, with the name
<code>bug_cf_&lt;name&gt;</code>, and a schema like this:</p>

<table border="1" cellpadding="5" cellspacing="0">

<tbody>
<a id="table-multiselect" name="table-multiselect"><tr align="left" valign="top">
<th>Field</th>
<th>Type</th>
<th>Default</th>
<th>Properties</th>
<th>Remarks</th>
</tr></a>

<tr align="left" valign="top">
<th><a id="column-multiselect-bug_id" name="column-multiselect-bug_id">bug_id</a></th>
<td>mediumint</td>
<td>0</td>
<td></td>
<td>The bug ID (foreign key %(column-bugs-bug_id)s).</td>
</tr>

<tr align="left" valign="top">
<th><a id="column-multiselect-value" name="column-multiselect-value">value</a></th>
<td>varchar(64)</td>
<td>''</td>
<td>-</td>
<td>the value (foreign key <a href="#column-customfield-value">cf_&lt;name&gt;.value</a>).</td>
</tr>
</tbody></table>

<p>Indexes:</p>

<table border="1" cellpadding="5" cellspacing="0">

<tbody>
<tr align="left" valign="top">
<th>Name</th>
<th>Fields</th>
<th>Properties</th>
<th>Remarks</th>
</tr>

<tr align="left" valign="top">
<th><a id="index-multiselect-cf_field_bug_id_idx" name="index-multiselect-cf_field_bug_id_idx">cf_&lt;field&gt;_bug_id_idx</a></th>
<td>bug_id, value</td>
<td>unique</td>
<td>-</td>
</tr>

</tbody></table>

<p>%(VERSION_STRING)sThe value 4 (FIELD_TYPE_TEXTAREA)
indicates a large text-box field (type mediumtext).</p>
"""),

('3.1.3', None,

"""<p>%(VERSION_STRING)sThe value 5 (FIELD_TYPE_DATETIME)
indicates a date/time field (type datetime).</p>
"""),

('3.3.1', None,

"""<p>%(VERSION_STRING)sThe value 6 (FIELD_TYPE_BUG_ID)
indicates a bug ID field (type mediumint).</p>
"""),

('2.23.1', '2.23.2', """<p>%(VERSION_STRING)sCustom fields are
manipulated from the command-line with the <code>customfield.pl</code>
script.</p>"""),

('2.23.3', None, """<p>%(VERSION_STRING)sCustom fields are configured
using <code>editfield.cgi</code>.</p>"""),

"""<h3><a id="notes-tables" name="notes-tables">List of tables</a></h3>

%(TABLES_TABLE)s

<h2><a id="section-3" name="section-3">3. The schema</a></h2>

""",
]

# This afterword is included in the generated schema doc after the
# schema itself.

afterword = ["""

<h2><a id="section-4" name="section-4">4. Bugzilla History</a></h2>

<h3><a id="history-release-table" name="history-release-table">Bugzilla releases</a></h3>

<p>This table gives the dates of all the Bugzilla releases since 2.0.</p>

<table border="1" cellspacing="0" cellpadding="5">

<thead>

  <tr align="left">

    <th>Date</th>

    <th>Release</th>

    <th>Notes</th>
  </tr>

</thead>

<tbody>
%(VERSIONS_TABLE)s
</tbody>
</table>

<h3><a id="history-schema-changes" name="history-schema-changes">Bugzilla Schema Changes</a></h3>

""",
('2.2', '2.2', """<p>In Bugzilla release 2.2, the following schema
changes were made:</p>

<ul>

  <li>%(the-table-products)s was added.</li>

  <li>%(column-bugs-qa_contact)s, %(column-bugs-status_whiteboard)s,
  and %(column-bugs-target_milestone)s were added.</li>

  <li>%(column-bugs-op_sys)s changed from tinytext to a non-null enum,
  default All.</li>

  <li>'X-Windows' was removed from %(column-bugs-rep_platform)s.</li>

  <li>%(column-components-description)s and
  %(column-components-initialqacontact)s were added.</li>

  <li>%(column-components-initialowner)s became non-null default ''.</li>

  <li>Indexes %(index-bugs-op_sys)s, %(index-bugs-qa_contact)s, and
  %(index-bugs-target_milestone)s were added.</li>

  <li>Indexes %(index-cc-bug_id)s and %(index-cc-who)s were added.</li>

</ul>

"""),
('2.4', '2.4', """<p>In Bugzilla release 2.4, the following schema
changes were made:</p>

<ul>

  <li>%(the-table-groups)s, %(column-profiles-groupset)s, and
  %(column-bugs-groupset)s were added, introducing <a
  href="#notes-groups ">groups</a>.</li>

  <li>%(the-table-dependencies)s was added, introducing <a
  href="#notes-dependencies">dependencies</a>.</li>

  <li>The value 'blocker' was added to %(column-bugs-bug_severity)s and the default was change from 'critical' to 'blocker'.</li>

  <li>%(column-bugs-creation_ts)s became non-null, with default 0000-00-00 00:00:00, and was added as the index %(index-bugs-creation_ts)s.</li>

  <li>%(column-profiles-emailnotification)s was added.</li>

  <li>Additional values were permitted in %(column-bugs-op_sys)s.</li>

</ul>

"""),
('2.6', '2.6', """<p>In Bugzilla release 2.6, the following schema
changes were made:</p>

<ul>

  <li>%(the-table-attachments)s was added, introducing <a
  href="#notes-attachments ">attachments</a>.</li>

  <li>%(the-table-dependencies)s was added, introducing <a
  href="#notes-dependencies ">dependencies</a>.</li>

  <li>The value 'blocker' was added to %(column-bugs-bug_severity)s and the default was change from 'critical' to 'blocker'.</li>

  <li>%(column-bugs-creation_ts)s became non-null, with default 0000-00-00 00:00:00, and was added as the index %(index-bugs-creation_ts)s.</li>

  <li>%(column-profiles-emailnotification)s was added.</li>

  <li>Additional values were permitted in %(column-bugs-op_sys)s.</li>

</ul>

"""),
('2.8', '2.8', """<p>In Bugzilla release 2.8, the following schema
changes were made:</p>

<ul>

  <li>%(the-table-votes)s, %(column-bugs-votes)s, and
  %(column-products-votesperuser)s were added, introducing <a
  href="#notes-voting">voting</a>.</li>

  <li>%(column-bugs-product)s was changed from varchar(16) to varchar(64), and %(column-products-product)s, %(column-versions-program)s, and %(column-components-program)s were all changed from tinytext to varchar(64), lengthening product names.</li>

  <li>%(column-bugs-area)s was removed.</li>

  <li>%(column-bugs_activity-when)s was renamed as %(column-bugs_activity-bug_when)s .</li>

</ul>

"""),

('2.10', '2.10', """<p>In Bugzilla release 2.10, the following schema changes were
made:</p>

<ul>

  <li>%(the-table-keywords)s, %(the-table-keyworddefs)s, and
  %(column-bugs-keywords)s were added, giving <a
  href="#notes-keywords">keywords</a> to bugs.</li>

  <li>%(the-table-milestones)s and
  %(column-products-defaultmilestone)s were added, to implement <a
  href="#notes-milestones">milestones</a>.</li>

  <li>%(the-table-fielddefs)s was added, and
  %(column-bugs_activity-field)s was changed to
  %(column-bugs_activity-fieldid)s, decoupling bug history from field
  names and providing longer field descriptions in bug change
  reports.</li>

  <li>%(the-table-longdescs)s was added, and %(column-bugs-long_desc)s
  was removed, allowing multiple comments per bug.</li>

  <li>%(the-table-namedqueries)s was added, for <a
  href="#notes-named-queries">named queries</a>.</li>

  <li>%(the-table-profiles_activity)s was added, recording activity in
  %(the-table-profiles)s.</li>

  <li>%(the-table-shadowlog)s was added, recording SQL activity for
  reflection into a <a href="#notes-shadow">shadow database</a>.</li>

  <li>%(the-table-watch)s was added, allowing <a
  href="#notes-watchers">watchers</a>.</li>

  <li>%(column-bugs-everconfirmed)s,
  %(column-products-maxvotesperbug)s, and
  %(column-products-votestoconfirm)s was added, and UNCONFIRMED was
  added to %(column-bugs-bug_status)s, introducing <a
  href="#notes-voting">bug confirmation by voting</a>.</li>

  <li>%(column-bugs-lastdiffed)s was added.</li>

  <li>%(column-profiles-blessgroupset)s was added.</li>

  <li>%(column-profiles-disabledtext)s was added.</li>

  <li>%(column-profiles-mybugslink)s was added.</li>

  <li>%(column-profiles-newemailtech)s was added.</li>

  <li>Additional values were permitted in %(column-bugs-op_sys)s.</li>

  <li>The default value of %(column-bugs-target_milestone)s changed from '' to '---'.</li>

  <li>%(column-versions-program)s changed from "null default None" to "non-null default ''".</li>

  <li>%(column-cc-who)s was added to the index %(index-cc-bug_id)s.</li>

  <li>The index %(index-profiles-login_name)s was made unique.</li>

</ul>

"""),
('2.12', '2.12', """<p>In Bugzilla release 2.12, the following schema changes were
made:</p>

<ul>
  <li>%(the-table-duplicates)s was added.</li>

  <li>%(column-profiles-emailflags)s was added.</li>

  <li>The %(column-bugs-resolution)s value <b>MOVED</b> was
  added.</li>

  <li>A number of additional values were permitted in %(column-bugs-op_sys)s.</li>

  <li>%(column-components-initialowner)s and
  %(column-components-initialqacontact)s changed from "tinytext"
  (foreign key %(column-profiles-login_name)s) to "mediumint" (foreign
  key %(column-profiles-userid)s), default 0.</li>

  <li>%(column-profiles-disabledtext)s
  changed from "not null" to "null".</li>

  <li>The default value of %(column-profiles-newemailtech)s
  changed from 0 to 1.</li>

</ul>

"""),
('2.14', '2.14', """<p>In Bugzilla release 2.14, the following schema changes were
made:</p>

<ul>
  <li>%(the-table-tokens)s was added.</li>

  <li>%(column-profiles-password)s was
  removed.</li>

  <li>%(column-profiles-cryptpassword)s and
  %(column-logincookies-cryptpassword)s
  were both changed from varchar(64) to varchar(32).</li>

  <li>%(column-profiles-newemailtech)s was
  removed.</li>

  <li>%(column-profiles-emailnotification)s
  was removed.</li>

  <li>%(column-bugs-reporter_accessible)s,
  %(column-bugs-assignee_accessible)s,
  %(column-bugs-qacontact_accessible)s,
  and %(column-bugs-cclist_accessible)s
  were added.</li>

  <li>%(column-bugs-version)s changed from
  varchar(16) to varchar(64).</li>

  <li>%(column-bugs_activity-oldvalue)s and
  %(column-bugs_activity-newvalue)s
  were replaced by %(column-bugs_activity-removed)s and
  %(column-bugs_activity-added)s.</li>

  <li>%(column-groups-isactive)s was
  added.</li>

  <li>%(column-longdescs-who)s became an
  index field.</li>

  <li>%(column-profiles-disabledtext)s
  changed back to "not null".</li>

</ul>"""),

('2.14', '2.14.1', """<p>The schema is identical in Bugzilla releases 2.14 and 2.14.1.</p>

"""),
('2.14.2', '2.14.2', """<p>In Bugzilla release 2.14.2, the following schema change was
made:</p>

<ul>

  <li>%(column-logincookies-hostname)s was
  replaced by %(column-logincookies-ipaddr)s.</li>

</ul>

"""),

('2.14.2', '2.14.5', """<p>The schema is identical in Bugzilla releases 2.14.2, 2.14.3,
2.14.4, and 2.14.5.</p>

"""),

('2.16rc1', '2.16', """<p>In Bugzilla release 2.16 (and the release candidates 2.16rc1 and
2.16rc2), the following schema changes were made:</p>

<ul>

  <li>The %(table-attachstatuses)s and %(table-attachstatusdefs)s
  tables were added.</li>

  <li>%(column-attachments-isobsolete)s was
  added.</li>

  <li>The values permitted in %(column-bugs-op_sys)s changed.</li>

  <li>%(column-bugs-assignee_accessible)s
  and %(column-bugs-qacontact_accessible)s
  were removed.</li>

  <li>%(column-bugs_activity-attach_id)s
  was added.</li>

  <li>%(column-logincookies-cryptpassword)s
  was removed.</li>

  <li>The possible values of %(column-tokens-tokentype)s changed, to
  include 'emailold' and 'emailnew' (used when changing the email
  address of a Bugzilla user).</li>

</ul>

"""),

('2.16rc1', '2.16.11', """<p>The schema is identical in Bugzilla releases 2.16rc1, 2.16rc2,
2.16, 2.16.1, 2.16.2, 2.16.3, 2.16.4, 2.16.5, 2.16.6, 2.16.7, 2.16.8, 2.16.9, 2.16.10, and 2.16.11.</p>

"""),

('2.17.1', '2.17.1', """<p>In Bugzilla release 2.17.1, the following schema changes were
made:</p>

<ul>

  <li><p>The groups system was radically changed.  This included the
  following detailed schema changes:</p>
    <ul>

      <li>The %(table-bug_group_map)s, %(table-user_group_map)s,
      and %(table-group_group_map)s tables were added.</li>

      <li>%(column-groups-bit)s was replaced
      with %(column-groups-id)s.</li>

      <li>%(column-groups-last_changed)s was
      added.</li>

      <li>%(column-bugs-groupset)s, %(column-profiles-groupset)s and %(column-profiles-blessgroupset)s
      were dropped.</li> </ul> </li>

  <li>A new <a href="#notes-flags">flags</a> system was introduced,
  adding the tables %(table-flags)s, %(table-flagtypes)s,
  %(table-flaginclusions)s, and %(table-flagexclusions)s.  This allows
  status flags to be defined and used on both attachments and bugs.
  This replaces the "attachment statuses" feature, so the
  %(table-attachstatuses)s and %(table-attachstatusdefs)s tables were
  removed.</li>

  <li>%(the-table-quips)s was added.</li>

  <li>Products got IDs in addition to names, and product name columns
  were replaced with product ID columns: %(column-bugs-product)s was
  replaced with %(column-bugs-product_id)s,
  %(column-components-program)s was replaced with
  %(column-components-product_id)s, %(column-milestones-product)s was
  replaced with %(column-milestones-product_id)s,
  %(column-versions-program)s was replaced with
  %(column-versions-product_id)s, and %(column-products-product)s was
  replaced with %(column-products-id)s and
  %(column-products-name)s.</li>

  <li>Components got IDs in addition to names, and the component name
  column was replaced with a component ID column: %(column-bugs-component)s was replaced with
  %(column-bugs-component_id)s, and %(column-components-value)s was replaced
  with %(column-components-id)s and %(column-components-name)s.</li>

  <li>%(column-bugs-estimated_time)s, %(column-bugs-remaining_time)s, and %(column-longdescs-work_time)s were
  added.</li>

  <li>%(column-attachments-isprivate)s and
  %(column-longdescs-isprivate)s were
  added.</li>

  <li>%(column-attachments-creation_ts)s
  changed from a timestamp to a datetime, default '0000-00-00
  00:00:00'.</li>

  <li>%(column-attachments-filename)s
  changed from a mediumtext to a varchar(100).</li>

  <li>The values permitted in %(column-bugs-op_sys)s changed.</li>

  <li>%(column-bugs-alias)s was added.</li>

  <li>The unused column %(column-namedqueries-watchfordiffs)s
  was removed.</li>

  <li>%(column-profiles-refreshed_when)s
  was added.</li>

</ul>

"""),

('2.17.3', '2.17.3', """<p>In Bugzilla release 2.17.3, the following schema changes were
made:</p>

<ul>

  <li>%(the-table-group_control_map)s was added.</li>

  <li>%(the-table-shadowlog)s was removed.</li>

</ul>

"""),

('2.17.4', '2.17.4', """<p>In Bugzilla release 2.17.4, the following schema changes were
made:</p>

<ul>

  <li>%(column-quips-approved)s was added.</li>

</ul>

"""),
('2.17.5', '2.17.5', """<p>In Bugzilla release 2.17.5, the following schema changes were
made:</p>

<ul>

  <li>The %(table-series)s, %(table-series_categories)s,
  %(table-series_data)s, and %(table-user_series_map)s tables were
  added, to support <a href="#notes-charts">the new charts
  system</a>.</li>

  <li>%(column-votes-count)s was renamed as %(column-votes-vote_count)s.</li>

  <li>The values permitted in %(column-bugs-op_sys)s changed.</li>

  <li>%(column-bugs-short_desc)s and %(column-longdescs-thetext)s became
  fulltext index fields, allowing quicker full text searching.</li>

</ul>

"""),

('2.17.5', '2.17.6', """<p>The schema is identical in Bugzilla releases 2.17.5 and 2.17.6.</p>

"""),

('2.17.7', '2.17.7', """<p>In Bugzilla 2.17.7, the following schema changes were made:</p>

<ul>

  <li>%(column-bugs-short_desc)s
  changed to "not null".</li>

</ul>
"""),

('2.18rc1', '2.18rc1', """<p>In Bugzilla 2.18rc1, the following schema changes were made:</p>

<ul>

  <li>The values permitted in %(column-bugs-op_sys)s changed.</li>

  <li>%(column-user_group_map-isderived)s
  was replaced by %(column-user_group_map-grant_type)s.</li>
  <li>%(column-flags-is_active)s was
  added.</li>

</ul>
"""),

('2.18rc2', '2.18rc2', """<p>The schema is identical in Bugzilla releases 2.18rc1 and 2.18rc2.</p>

"""),

('2.18rc3', '2.18rc3', """<p>In Bugzilla 2.18rc3, the following schema changes were made:</p>

<ul>

  <li>%(the-table-user_series_map)s was removed, replaced in part by
  %(column-series-public)s.</li>

  <li>%(the-table-category_group_map)s was added, providing
  group-level access control for time-series charts.</li>

  <li>%(column-series_categories-category_id)s was renamed as
  %(column-series_categories-id)s.</li>

  <li>%(column-series_data-date)s was renamed as
  %(column-series_data-series_date)s, and %(column-series_data-value)s
  was renamed as %(column-series_data-series_value)s.</li>

</ul>
"""),

('2.18', '2.18', """<p>The schema is identical in Bugzilla releases 2.18rc3 and 2.18.</p>

"""),

('2.18.1', '2.18.1', """<p>In Bugzilla 2.18.1, the following schema changes were made:</p>

<ul>

  <li>%(column-fielddefs-obsolete)s was added.</li>

  <li>%(column-quips-userid)s was changed from "not null default 0" to "null".</li>

</ul>
"""),

('2.18.2', '2.18.2', """<p>In Bugzilla 2.18.2, the following schema changes were made:</p>

<ul>

  <li>%(column-bugs-creation_ts)s changed from "not null" to "null".</li>

</ul>
"""),

('2.18.3', '2.18.6', """<p>The schema is identical in Bugzilla releases 2.18.2, 2.18.3, 2.18.4, 2.18.5, and 2.18.6.</p>

"""),

('2.19.1', '2.19.1', """<p>In Bugzilla 2.19.1, the following schema changes were made:</p>

<ul>

  <li>Because 2.19.1 predates the 2.18 series of releases, the changes
  made in that series are "undone" in 2.19.1 (and redone later in the
  2.19/2.20rc series):

    <ul>
      <li>%(column-fielddefs-obsolete)s was removed again.</li>

      <li>%(column-bugs-creation_ts)s returned to being "not null".</li>

      <li>%(column-quips-userid)s returned to being "not null default 0".</li>
    </ul>

  <li>%(the-table-classifications)s and
  %(column-products-classification_id)s were added, to support <a
  href="#notes-products">the new classifications
  system</a>.</li>

  <li>%(column-group_group_map-isbless)s was replaced by
  %(column-group_group_map-grant_type)s.</li>

  <li>%(column-logincookies-lastused)s changed from a timestamp to a
  datetime, default '0000-00-00 00:00:00'.</li>

  <li>%(column-profiles-extern_id)s was added.</li>

  <li>The %(table-whine_events)s, %(table-whine_queries)s, and <a
  %(the-table-whine_schedules)s tables were added, to support <a
  href="#notes-whine">the new whining system</a>.</li>

</ul>
"""),

('2.19.2', '2.19.2', """<p>In Bugzilla 2.19.2, the following schema changes were made:</p>

<ul>

  <li>%(column-flagtypes-grant_group_id)s and
  %(column-flagtypes-request_group_id)s were added.</li>

</ul>
"""),

('2.19.3', '2.19.3', """<p>In Bugzilla 2.19.3, the following schema changes were made:</p>

<ul>

  <li>All the secondary indexes were given new names, based on the
  names of the table and first indexed column.</li>

  <li>The %(table-bug_severity)s, %(table-bug_status)s,
  %(table-op_sys)s, %(table-priority)s, %(table-rep_platform)s, and
  %(table-resolution)s tables were added, and the matching bug fields
  (%(column-bugs-bug_severity)s, %(column-bugs-bug_status)s,
  %(column-bugs-op_sys)s, %(column-bugs-priority)s,
  %(column-bugs-rep_platform)s, and %(column-bugs-resolution)s) were
  changed from enumerated types into varchar(64) foreign keys for
  these new tables.  The effect of this is to remove all enumerated
  types from the schema (improving portability to other DBMSes), and
  in principle to allow the administrator to modify the set of
  allowable values.</li>

  <li>The table %(table-bz_schema)s was added.</li>

  <li>The tables %(table-profile_setting)s, %(table-setting)s, and
  %(table-setting_value)s were added, for <a
  href="#notes-settings">the settings system</a>.</li>

  <li>The table %(table-email_setting)s was added, replacing
  %(column-profiles-emailflags)s.</li>

  <li>The indexes %(index-bugs_activity-bugs_activity_who_idx)s,
  %(index-attachments-attachments_submitter_id_idx)s,
  %(index-versions-versions_product_id_idx)s, and
  %(index-flags-flags_type_id_idx)s were added.</li>

  <li>%(column-bugs-deadline)s was added.</li>

  <li>%(column-bugs-delta_ts)s changed from a timestamp to a datetime.</li>

  <li>%(column-bugs-lastdiffed)s changed from "not null" to "null".</li>

  <li>%(column-bugs-qa_contact)s and
  %(column-components-initialqacontact)s changed from "not null" to
  "null".</li>

  <li>%(column-fielddefs-obsolete)s was added.</li>

  <li>%(column-longdescs-already_wrapped)s was added.</li>

  <li>%(column-profiles-cryptpassword)s was changed from varchar(34)
  to varchar(128).</li>

  <li>%(column-quips-approved)s and %(column-series-public)s changed
  from tinyint(1) to tinyint.</li>

  <li>%(column-versions-value)s changed from "tinytext null" to
  "varchar(64) not null".</li>

  <li>%(column-whine_schedules-mailto_userid)s was replaced by
  %(column-whine_schedules-mailto)s and
  %(column-whine_schedules-mailto_type)s.</li>

  <li>The index %(index-series-creator)s was removed.</li>

  <li>%(column-quips-userid)s was changed from "not null default 0" to "null".</li>

  </ul>
"""),

('2.20rc1', '2.20rc1', """<p>In Bugzilla 2.20rc1, the following schema changes were made:</p>

<ul>

  <li>%(column-bugs-creation_ts)s changed from "not null" to "null".</li>

</ul>
"""),

('2.20rc2', '2.20rc2', """<p>In Bugzilla 2.20rc2, the following schema changes were made:</p>

<ul>

  <li>%(column-attachments-bug_id)s was added to the index %(index-attachments-attachments_submitter_id_idx)s.</li>

</ul>
"""),

('2.20', '2.20.7', """<p>The schema is identical in Bugzilla releases 2.20rc2, 2.20, 2.20.1, 2.20.2, 2.20.3, 2.20.4, 2.20.5, 2.20.6, and 2.20.7.</p>

"""),

('2.21.1', '2.21.1', """<p>In Bugzilla 2.21.1, the following schema changes were made:</p>

<ul>

  <li>The table %(table-attach_data)s was added, replacing
  %(column-attachments-thedata)s.  This makes SQL queries on %(the-table-attachments)s go faster.</li>

  <li>%(column-series-public)s was renamed %(column-series-is_public)s ("public" is a keyword in Oracle).</li>

</ul>
"""),

('2.22rc1', '2.22rc1', """<p>In Bugzilla 2.22rc1, the following schema changes were made:</p>

<ul>

  <li>%(column-attachments-isurl)s was added.</li>

  <li>%(column-namedqueries-query_type)s was added.</li>

  <li>%(column-logincookies-cookie)s was changed from "mediumint
  auto_increment" to "varchar(16)", to hold a randomly-generated
  (and therefore harder-to-guess) cookie.</li>

</ul>
"""),

('2.22', '2.22.7', """<p>The schema is identical in Bugzilla releases 2.22rc1, 2.22, 2.22.1, 2.22.2, 2.22.3, 2.22.4, 2.22.5, 2.22.6, and 2.22.7.</p>

"""),

('2.23.1', '2.23.1', """<p>In Bugzilla 2.23.1, the following schema changes were made:</p>

<ul>

  <li><b>Custom fields</b> were added: columns named <code>cf_&lt;name&gt;</code> in %(the-table-bugs)s.</li>

  <li>%(column-fielddefs-custom)s and %(column-fielddefs-type)s were added.</li>

  <li>%(column-flags-id)s became "auto_increment" and
  %(column-flags-is_active)s was removed.  Dead flags are now removed
  from the database instead of being marked inactive.</li>

  <li>%(column-longdescs-comment_id)s was added, as a primary key on %(table-longdescs)s.</li>

</ul>
"""),

('2.23.2', '2.23.2', """<p>In Bugzilla 2.23.2, the following schema change was made:</p>

<ul>

  <li>%(column-bugs-short_desc)s changed from mediumtext to varchar(255).</li>

</ul>
"""),

('2.23.3', '2.23.3', """<p>In Bugzilla 2.23.3, the following schema changes were made:</p>

<ul>

  <li>Single-select <b>custom fields</b> were added; allowable values
  are stored in tables named <code>cf_&lt;name&gt;</code>.</li>

  <li>Shared named queries were added, by adding tables
  %(table-namedqueries_link_in_footer)s and
  %(table-namedquery_group_map)s, column %(column-namedqueries-id)s,
  and index %(index-namedqueries-PRIMARY)s, and removing
  %(column-namedqueries-linkinfooter)s.</li>

  <li>%(the-table-component_cc)s was added.</li>

  <li>%(column-classifications-sortkey)s was added.</li>

  <li>%(column-setting-subclass)s was added.</li>

  <li>%(column-fielddefs-enter_bug)s was added.</li>

  <li>%(column-fielddefs-fieldid)s was renamed to %(column-fielddefs-id)s.</li>

  <li>%(column-flagtypes-id)s and %(column-keyworddefs-id)s became "auto_increment".</li>

  <li>%(column-longdescs-thetext)s became "not null".</li>

  <li>%(column-longdescs-bug_id)s was added to the index %(index-longdescs-longdescs_who_idx)s.</li>

  <li>%(column-profiles-realname)s became "not null".</li>

  <li>%(column-series-creator)s changed from "not null" to "null".</li>

  <li>%(column-tokens-userid)s changed from "not null" to "null".</li>

  <li>%(column-profiles-disable_mail)s was added.</li>

  <li>The index %(index-bugs-bugs_short_desc_idx)s was removed.</li>

  <li>%(column-profiles-refreshed_when)s and %(column-groups-last_changed)s were removed.</li>

</ul>"""),
('2.23.4', '2.23.4', """<p>In Bugzilla 2.23.4, the following schema changes were made:</p>

<ul>

    <li>%(column-milestones-id)s and %(column-versions-id)s were
    added, as PRIMARY indexes (increasing consistency: no objects are
    now identified solely by user-specified strings, although some
    cross-table references are still by string IDs rather than
    auto-generated integer IDs).</li>

    <li>%(column-group_control_map-canconfirm)s, %(column-group_control_map-editbugs)s, and
    %(column-group_control_map-editcomponents)s were added.</li>

    <li>%(column-longdescs-type)s and %(column-longdescs-extra_data)s were added.</li>

</ul>
"""),

('3.0rc1', '3.0.9', """<p>The schema is identical in Bugzilla releases 2.23.4, 3.0rc1, 3.0, 3.0.1, 3.0.2, 3.0.3, 3.0.4, 3.0.5, 3.0.6, 3.0.7, 3.0.8, and 3.0.9.</p>

"""),

('3.1.1', '3.1.1', """<p>In Bugzilla 3.1.1, the following schema changes were made:</p>

<ul>

<li>%(the-table-status_workflow)s, and %(column-bug_status-is_open)s,
were added, to provide configurable <a href="#notes-workflow">workflow</a>.</li>

<li>%(column-groups-icon_url)s was added.</li>

</ul>

"""),

('3.1.2', '3.1.2', """<p>In Bugzilla 3.1.2, the following schema change was made:</p>

<ul>

<li>Multi-select custom fields were added, with <a href="#table-multiselect">this schema</a>;</li>

<li>Large text box custom fields were added.</li>

</ul>

"""),

('3.1.3', '3.1.3', """<p>In Bugzilla 3.1.3, the following schema changes were made:</p>

<ul>

<li>%(column-attachments-modification_time)s and
%(index-attachments-attachments_modification_time_idx)s were
added.</li>

<li>Date/time custom fields were added;</li>

<li>These fields changed from mediumtext to tinytext:
%(column-attachments-description)s, %(column-attachments-mimetype)s,
%(column-fielddefs-description)s.</li>

<li>These fields changed from text to mediumtext:
%(column-bugs-bug_file_loc)s, %(column-flagtypes-description)s,
%(column-groups-description)s, and %(column-quips-quip)s.</li>

<li>%(column-flagtypes-description)s became "not null".</li>

</ul>

"""),

('3.1.4', '3.1.4', """<p>In Bugzilla 3.1.4, the following schema change was made:</p>

<ul>

<li>%(the-table-bugs_fulltext)s was added and the index
%(index-longdescs-longdescs_thetext_idx)s was removed, improving the
performance of full-text searching.</li>

</ul>

"""),

('3.2rc1', '3.2.5', """<p>The schema is identical in Bugzilla releases 3.1.4, 3.2rc1, 3.2rc2, 3.2, 3.2.1, 3.2.2, 3.2.3, 3.2.4, and 3.2.5.</p>

"""),

('3.3.1', '3.3.1', """<p>In Bugzilla 3.3.1, the following schema changes were made:</p>

<ul>

<li>Bug ID custom fields were added;</li>

<li>The tables %(table-ts_error)s, %(table-ts_exitstatus)s,
%(table-ts_funcmap)s, %(table-ts_job)s, and %(table-ts_note)s were
added.  These tables are created and used by TheSchwartz job queue
system, to run the background email sending system.</li>

<li>%(column-fielddefs-visibility_field_id)s and
%(column-fielddefs-visibility_value_id)s were added, to allow the display of
each custom field to depend on the value of a select field.</li>

<li>%(column-fielddefs-value_field_id)s, %(column-bug_severity-visibility_value_id)s,
%(column-bug_status-visibility_value_id)s, %(column-op_sys-visibility_value_id)s,
%(column-priority-visibility_value_id)s, %(column-rep_platform-visibility_value_id)s,
%(column-resolution-visibility_value_id)s, and <a href="#column-customfield-visibility_value_id">
cf_&lt;field&gt;.visibility_value_id</a> were added, to
allow the availability of individual values of single-select and multi-select fields to depend on the value of another select field.</li>

<li>New indexes %(index-fielddefs-fielddefs_value_field_id_idx)s,
%(index-bug_severity-bug_severity_visibility_value_id_idx)s,
%(index-bug_status-bug_status_visibility_value_id_idx)s,
%(index-op_sys-op_sys_visibility_value_id_idx)s,
%(index-priority-priority_visibility_value_id_idx)s,
%(index-rep_platform-rep_platform_visibility_value_id_idx)s,
%(index-resolution-resolution_visibility_value_id_idx)s, and
<a href="#index-customfield-cf_field_visibility_value_id">cf_&lt;field&gt;:cf_&lt;field&gt;_visibility_value_id_idx</a> were added, to support use of the above new fields.</li>
<li>%(column-group_control_map-product_id)s changed from mediumint to smallint.</li>

</ul>

"""),

('3.3.2', '3.3.2', """<p>In Bugzilla 3.3.2, the following schema changes were made:</p>

<ul>

<li>%(the-table-bug_see_also)s was added.</li>

<li>%(column-fielddefs-buglist)s was added.</li>

</ul>

"""),

('3.3.3', '3.3.3', """<p>The schema is identical in Bugzilla releases 3.3.2 and 3.3.3.</p>

"""),

('3.3.4', '3.3.4', """<p>In Bugzilla 3.3.4, the following schema changes were made:</p>

<ul>

<li>The index %(index-profiles-profiles_extern_id_idx)s was added.</li>

</ul>

"""),

('3.4rc1', '3.4.1', """<p>The schema is identical in Bugzilla releases 3.3.4, 3.4rc1, 3.4, 3.4.1, and 3.4.2.</p>

"""),

"""<h2><a id="section-5" name="section-5">5. Example queries</a></h2>

<p>To select bug number <em>n</em>:</p>

<blockquote><code>
select * from bugs where bug_id = <em>n</em>
</code></blockquote>

<p>To get a complete list of user ids and email addresses:</p>

<blockquote><code>
select userid, login_name from profiles
</code></blockquote>

<p>To get the email address of user <em>n</em>:</p>

<blockquote><code>
select login_name from profiles where userid = <em>n</em>
</code></blockquote>

<p>To get the set of cc addresses of bug <em>n</em>:</p>

<blockquote><code>
select login_name from cc, profiles
 where cc.bug_id = <em>n</em>
   and profiles.userid = cc.who
</code></blockquote>

""",

('2.10', None, """<p>%(VERSION_STRING)sTo select the long descriptions
of bug <em>n</em>, together with the name and email address of the
commenters:</p>

<blockquote><code>
select profiles.login_name, profiles.realname,
       longdescs.bug_when, longdescs.thetext
  from longdescs, profiles
 where profiles.userid = longdescs.who
   and longdescs.bug_id = <em>n</em>
 order by longdescs.bug_when
</code></blockquote>"""),

('2.4', None, """<p>To find out the groups of user <em>n</em>:</p>"""),

('2.4', '2.16.7', """<p>%(VERSION_STRING)s</p>

<blockquote><code>
select groupset from profiles where userid = <em>n</em>
</code></blockquote>"""),

('2.17.1', None, """<p>%(VERSION_STRING)s</p>

<blockquote><code>
select group_id from user_group_map where userid = <em>n</em> and isbless=0
</code></blockquote>"""),

"""<h2><a id="section-A" name="section-A">A. References</a></h2>


<h2><a id="section-B" name="section-B">B. Document History</a></h2>

<table>

  <tr valign="top">

    <td>2000-11-14</td>

    <td><a href="mailto:nb@ravenbrook.com">NB</a></td>

    <td>Created.</td>

  </tr>

  <tr valign="top">

    <td> 2001-03-02 </td>

    <td> <a href="mailto:rb@ravenbrook.com">RB</a> </td>

    <td> Transferred copyright to Perforce under their license. </td>

  </tr>

  <tr valign="top">

    <td> 2001-04-06 </td>

    <td> <a href="mailto:nb@ravenbrook.com">NB</a> </td>

    <td> Added sample queries. </td>

  </tr>

  <tr valign="top">

    <td>2001-09-12</td>

    <td><a href="mailto:nb@ravenbrook.com">NB</a></td>

    <td>Updated to reflect schema updates in Bugzilla 2.12 and 2.14</td>

  </tr>

  <tr valign="top">

    <td>2002-01-31</td>

    <td><a href="mailto:nb@ravenbrook.com">NB</a></td>

    <td>Added notes on Bugzilla 2.14.1.</td>

  </tr>

  <tr valign="top">

    <td>2002-05-31</td>

    <td><a href="mailto:nb@ravenbrook.com">NB</a></td>

    <td>Updated for Bugzilla 2.16 (based on 2.16rc1).</td>

  </tr>

  <tr valign="top">

    <td>2002-09-26</td>

    <td><a href="mailto:nb@ravenbrook.com">NB</a></td>

    <td>Updated for Bugzilla 2.16/2.14.2/2.14.3.</td>

  </tr>

  <tr valign="top">

    <td>2002-10-04</td>

    <td><a href="mailto:nb@ravenbrook.com">NB</a></td>

    <td>Added notes on Bugzilla 2.14.4 and 2.16.1, and on identical schemas.</td>

  </tr>

  <tr valign="top">

    <td>2003-05-14</td>

    <td><a href="mailto:nb@ravenbrook.com">NB</a></td>

    <td>Added extensive notes on schema changes, in section 2.</td>

  </tr>

  <tr valign="top">

    <td>2003-06-06</td>

    <td><a href="mailto:nb@ravenbrook.com">NB</a></td>

    <td>Added table of Bugzilla releases showing release date and support status.</td>

  </tr>

  <tr valign="top">

    <td>2003-06-06</td>

    <td><a href="mailto:nb@ravenbrook.com">NB</a></td>

    <td>Added notes on schema changes in 2.17.x.</td>

  </tr>

  <tr valign="top">

    <td>2003-06-13</td>

    <td><a href="mailto:nb@ravenbrook.com">NB</a></td>

    <td>Added first cut at description of new Bugzilla tables.</td>

  </tr>

  <tr valign="top">

    <td>2003-06-27</td>

    <td><a href="mailto:nb@ravenbrook.com">NB</a></td>

    <td>Added more on recent schema changes.  Colour-coded all schema
  changes.</td>

  </tr>

  <tr valign="top">

    <td>2003-07-09</td>

    <td><a href="mailto:nb@ravenbrook.com">NB</a></td>

    <td>Completely changed the way this document is produced.  The
    schema tables themselves are now created and coloured
    automatically by querying MySQL.</td>

  </tr>

  <tr valign="top">

    <td>2003-11-04</td>

    <td><a href="mailto:nb@ravenbrook.com">NB</a></td>

    <td>Add Bugzilla 2.16.4 and 2.17.5.</td>

  </tr>

  <tr valign="top">

    <td>2003-11-10</td>

    <td><a href="mailto:nb@ravenbrook.com">NB</a></td>

    <td>Add Bugzilla 2.17.6.</td>

  </tr>

  <tr valign="top">

    <td>2004-03-19</td>

    <td><a href="mailto:nb@ravenbrook.com">NB</a></td>

    <td>Add Bugzilla 2.17.7; improve documentation of the groups system; improve automated schema change descriptions.</td>

  </tr>

  <tr valign="top">

    <td>2004-03-26</td>

    <td><a href="mailto:nb@ravenbrook.com">NB</a></td>

    <td>Add documentation of the flags system, the time series system, and the time tracking system.</td>

  </tr>

  <tr valign="top">

    <td>2004-04-30</td>

    <td><a href="mailto:nb@ravenbrook.com">NB</a></td>

    <td>Correct some documentation of the time series system based on feedback from the author.</td>

  </tr>

  <tr valign="top">

    <td>2004-07-14</td>

    <td><a href="mailto:nb@ravenbrook.com">NB</a></td>

    <td>Add 2.16.6 and 2.18rc1.</td>

  </tr>

  <tr valign="top">

    <td>2004-07-28</td>

    <td><a href="mailto:nb@ravenbrook.com">NB</a></td>

    <td>Add 2.18rc2.</td>

  </tr>

  <tr valign="top">

    <td>2004-11-11</td>

    <td><a href="mailto:nb@ravenbrook.com">NB</a></td>

    <td>Add 2.16.7, 2.18rc3, 2.19.1.  Change document-generation code
    to improve colouring, link consistency, control, and
    robustness.</td>

  </tr>

  <tr valign="top">

    <td>2004-11-12</td>

    <td><a href="mailto:nb@ravenbrook.com">NB</a></td>

    <td>Turn into CGI, using schemas stored in Python pickles.</td>

  </tr>

  <tr valign="top">

    <td>2004-11-13</td>

    <td><a href="mailto:nb@ravenbrook.com">NB</a></td>

    <td>Add 2.0, 2.2, 2.4, 2.6. 2.8, for completeness.</td>

  </tr>

  <tr valign="top">

    <td>2004-12-03</td>

    <td><a href="mailto:nb@ravenbrook.com">NB</a></td>

    <td>Add notes on quips and a few missing foreign key links.</td>

  </tr>

  <tr valign="top">

    <td>2005-01-18</td>

    <td><a href="mailto:nb@ravenbrook.com">NB</a></td>

    <td>Add 2.16.8, 2.18, and 2.19.2.</td>

  </tr>

  <tr valign="top">

    <td>2005-05-19</td>

    <td><a href="mailto:nb@ravenbrook.com">NB</a></td>

    <td>Add 2.16.9, 2.16.10, 2.18.1, and (preliminarily) 2.19.3.</td>

  </tr>

  <tr valign="top">

    <td>2005-09-15</td>

    <td><a href="mailto:nb@ravenbrook.com">NB</a></td>

    <td>Add 2.18.2, 2.18.3, 2.20rc1, 2.20rc2, and complete remarks for 2.19.3.</td>

  </tr>

  <tr valign="top">

    <td>2005-10-03</td>

    <td><a href="mailto:nb@ravenbrook.com">NB</a></td>

    <td>Add 2.18.4, 2.20, 2.21.1</td>

  </tr>

  <tr valign="top">

    <td>2006-05-18</td>

    <td><a href="mailto:nb@ravenbrook.com">NB</a></td>

    <td>Add 2.16.11, 2.18.5, 2.20.1, 2.22rc1, 2.20.2, 2.22, 2.23.1.</td>

  </tr>

  <tr valign="top">

    <td>2006-10-31</td>

    <td><a href="mailto:nb@ravenbrook.com">NB</a></td>

    <td>Add recent releases, to 2.18.6, 2.20.3, 2.22.1, 2.23.3.</td>

  </tr>

  <tr valign="top">

    <td>2007-05-11</td>

    <td><a href="mailto:nb@ravenbrook.com">NB</a></td>

    <td>Add recent releases 2.20.4, 2.22.2, 2.23.4, 3.0rc1, 3.0.</td>

  </tr>

  <tr valign="top">

    <td>2008-02-29</td>

    <td><a href="mailto:nb@ravenbrook.com">NB</a></td>

    <td>Add recent releases 3.0.1, 3.0.2, 3.0.3, 3.1.1, 3.1.2, 3.1.3.</td>

  </tr>

  <tr valign="top">

    <td>2009-07-31</td>

    <td><a href="mailto:nb@ravenbrook.com">NB</a></td>

    <td>Add recent releases 2.20.7, 2.22.5, 2.22.6, 2.22.7, 3.0.5, 3.0.6, 3.0.7, 3.0.8, 3.2rc1, 3.2rc2, 3.2, 3.2.1, 3.2.2, 3.2.3, 3.2.4, 3.3.1, 3.3.2, 3.3.3, 3.3.4, 3.4rc1, and 3.4.</td>

  </tr>

  <tr valign="top">

    <td>2024-04-26</td>

    <td><a href="https://github.com/justdave">justdave</a></td>

    <td>Add ancient releases 3.0.10, 3.0.11, 3.2.6, 3.2.7, 3.2.8, 3.2.9, 3.2.10, 3.4.3, 3.4.4, 3.4.5, 3.4.6, 3.4.7, 3.4.8, 3.4.9, 3.4.10, 3.4.11, 3.4.12, 3.4.13, 3.4.14, 3.5.1, and 3.5.2.</td>

  </tr>

  <tr valign="top">

    <td>2024-04-27</td>

    <td><a href="https://github.com/justdave">justdave</a></td>

    <td>Add ancient releases 3.5.3, 3.6rc1, 3.6, 3.6.1, 3.6.2, 3.6.3, 3.6.4, 3.6.5, 3.6.6, 3.6.7, 3.6.8, 3.6.9, 3.6.10, 3.6.11, 3.6.12, 3.6.13, 3.7.1, 3.7.2, 3.7.3, 4.0rc1, 4.0rc2, 4.0, 4.0.1, 4.0.2, 4.0.3, 4.0.4, 4.0.5, 4.0.6, 4.0.7, 4.0.8, 4.0.9, 4.0.10, 4.0.11, 4.0.12, 4.0.13, 4.0.14, 4.0.15, 4.0.16, 4.0.17, 4.0.18, 4.1.1, 4.1.2, 4.1.3, and 4.2rc1.</td>

  </tr>

  <tr valign="top">

    <td>2024-04-28</td>

    <td><a href="https://github.com/justdave">justdave</a></td>

    <td>Add ancient releases 4.2rc1, 4.2rc2, 4.2, 4.2.1, 4.2.2, 4.2.3, 4.2.4, 4.2.5, 4.2.6, 4.2.7, 4.2.8, 4.2.9, 4.2.10, 4.2.11, 4.2.12, 4.2.13, 4.2.14, 4.2.15, and 4.2.16.</td>

  </tr>

</table>

<hr/>

<div align="center">
<p><small>Generated at %(TIME)s<br/>
by <code>%(SCRIPT_ID)s</code><br/>
from <code>%(REMARKS_ID)s</code></small></p>
</div>

""",]

remarks_id = '$Id$'

# A. REFERENCES
#
#
# B. DOCUMENT HISTORY
#
# 2003-07-08 NB Created.
# 2003-07-09 NB See the history section of the "afterword" for
#               subsequent history items.
#
#
# C. COPYRIGHT AND LICENSE
#
# This file is copyright (c) 2003 Perforce Software, Inc.  All rights
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
