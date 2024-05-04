#!/usr/bin/env python3
#             Perforce Defect Tracking Integration Project
#              <http://www.ravenbrook.com/project/p4dti/>
#
#           PICKLE_SCHEMA.PY -- MAKE PICKLES OF BUGZILLA SCHEMAS
#
#             Nick Barnes, Ravenbrook Limited, 2004-11-09
#
#
# 1. INTRODUCTION
#
# This module generates Python pickles of Bugzilla schemas, so that
# they can be included in generated schema documentation.
#
# The intended readership is project developers.
#
# This document is not confidential.

import pickle
import os

import MySQLdb

class BzSchemaPickleException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return self.message


def fetchall(cursor):
    rows = cursor.fetchall()
    # for some reason, if no rows are returned sometimes one gets () here.
    if len(rows) == 0:
        rows = []
    return rows


def select_rows(cursor, select):
    rows = cursor.execute(select)
    if cursor.description == None:
        raise BzSchemaPickleException(
            "Trying to fetch rows from non-select '%s'" % select
        )
    values = fetchall(cursor)
    if values == None:
        raise BzSchemaPickleException("Select '%s' returned unfetchable rows." % select)
    return values


def column_names(cursor):
    keys = []
    for i in range(len(cursor.description)):
        keys.append(cursor.description[i][0])
    return keys


def fetch_rows_as_list_of_dictionaries(cursor, select):
    results = []
    values = select_rows(cursor, select)
    keys = column_names(cursor)
    for value in values:
        result = {}
        if len(keys) != len(value):
            raise BzSchemaPickleException(
                "Select '%s' returns %d keys but %d columns."
                % (select, len(keys), len(value))
            )
        for j in range(len(keys)):
            result[keys[j]] = value[j]
        results.append(result)
    return results


def pickle_schema(schema_version, db_name):
    default_file = os.path.expanduser('~/.my.cnf')
    db = MySQLdb.connect(
        database=db_name,
        read_default_file=default_file,
        read_default_group='pickle_schema',
    )
    cursor = db.cursor()
    tables = [x[0] for x in select_rows(cursor, 'show tables')]
    schema = {}
    for table in tables:
        columns = fetch_rows_as_list_of_dictionaries(cursor, 'describe %s' % table)
        indexes = fetch_rows_as_list_of_dictionaries(
            cursor, 'show index from %s' % table
        )
        schema[table] = (columns, indexes)
    db.close()
    f = open('pickles/%s' % schema_version, 'wb')
    pickle.dump((schema_version, schema), f)
    f.close()


# A. REFERENCES
#
#
# B. DOCUMENT HISTORY
#
# 2004-11-11 NB  Created, partly from make_schema_doc.py.
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
