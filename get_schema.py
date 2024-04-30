#             Perforce Defect Tracking Integration Project
#              <http://www.ravenbrook.com/project/p4dti/>
#
#         GET_SCHEMA.PY -- UNPICKLE AND SIMPLIFY A BUGZILLA SCHEMA
#
#             Nick Barnes, Ravenbrook Limited, 2004-11-09
#
#
# 1. INTRODUCTION
#
# This module decodes a Python pickle of a Bugzilla schema, and turns
# it into a consistent data structure which incorporates remarks from
# schema_remarks.py.  The pickles are originally put in the 'pickles'
# subdirectory by pickle_schema.py.
#
# The intended readership is project developers.
#
# This document is not confidential.

import pickle
import types
import schema_remarks
import string
import re

# 3. Obtaining a schema, and reducing it to a normal form.

# This is a map from type names (as returned by a 'describe'
# operation) to synonymous type names.

type_map = {
    'smallint(6)': 'smallint',
    'mediumint(9)': 'mediumint',
    'tinyint(4)': 'tinyint',
    'int(11)': 'int',
    'bigint(20)': 'bigint',
}

# Given output from a 'describe table' operation, return a map from
# column name to a map with the following entries:
#
# 'Name':       column name,
# 'Default':    default value (or "None"),
# 'Type':       type name,
# 'Properties': properties (e.g. auto_increment).
# 'Remarks'   : list of HTML remarks
#
# Because almost all columns are "NOT NULL", that is the default, and
# other columns are marked 'null' under 'Properties'.


def reduce_columns(table, description, errors):
    columns = {}
    if table not in schema_remarks.column_remark:
        errors.append("No column remarks for table '%s'." % table)
        schema_remarks.column_remark[table] = {}
    for dict in description:
        name = dict['Field']
        sqltype = dict['Type']
        if sqltype in type_map:
            sqltype = type_map[sqltype]
        if sqltype[0:4] == 'enum':
            sqltype = sqltype.replace("','", "', '")
        if dict['Null'] == 'YES':
            if dict['Extra']:
                extra = dict['Extra'] + ', null'
            else:
                extra = 'null'
        else:
            extra = dict['Extra']
            if extra == '':
                extra = '-'
        default = dict['Default']
        # More recent versions of Bugzilla show defaults for numeric types as '',
        # instead of (say) 0 or 0.00.  This is not an actual schema change so we
        # normalise the default values.
        if sqltype[-3:] == 'int' and default == '':
            default = '0'
        if sqltype == 'datetime' and default == '':
            default = '0000-00-00 00:00:00'
        if sqltype[:7] == 'decimal' and (
            default == '' or default == None or float(default) == 0.0
        ):
            default = "0.0"
        if default == '':
            default = "''"
        if default is None:
            default = 'None'

        if (
            table in schema_remarks.column_renamed
            and name in schema_remarks.column_renamed[table]
        ):
            canonical_name = schema_remarks.column_renamed[table][name]
        else:
            canonical_name = name
        remark = None
        if canonical_name not in schema_remarks.column_remark[table]:
            errors.append(
                "Table '%s' has no remark for column '%s'." % (table, canonical_name)
            )
        else:
            remark = schema_remarks.column_remark[table][canonical_name]
        if remark is None:
            remarks = []
        elif type(remark) == list:
            remarks = remark
        else:
            remarks = [remark]
        columns[canonical_name] = {
            'Name': name,
            'Default': default,
            'Type': sqltype,
            'Properties': extra,
            'Remarks': remarks,
        }
    return columns


# Given output from "show index", return a map from index name to a
# map with the following entries:
#
# 'Name':    Index name, 'PRIMARY' for a primary index;
# 'Fields':  A string containing the ordered column names;
# 'Properties':  A string with such properties as 'unique' and 'full text'
# 'Remarks': A list of remarks.

foreign_key_index_re = re.compile('^fk_.*')


def reduce_indexes(table, index_list, errors):
    indexes = {}
    if table not in schema_remarks.index_remark:
        errors.append("No index remarks for table '%s'." % table)
        schema_remarks.index_remark[table] = {}
    for i in index_list:
        kn = i['Key_name']
        if foreign_key_index_re.match(kn):
            # a foreign key constraint; not really an index
            continue
        if (
            table in schema_remarks.index_renamed
            and kn in schema_remarks.index_renamed[table]
        ):
            canon = schema_remarks.index_renamed[table][kn]
        else:
            canon = kn
        if canon in indexes:
            indexes[canon]['Fields'][i['Seq_in_index']] = i['Column_name']
        else:
            props = []
            if i.get('Non_unique', 1) == 0:
                props.append('unique')
            if i.get('Index_type', i.get('Comment')) == 'FULLTEXT':
                props.append('full text')
            props = str.join(', ', props)
            remark = None
            if canon not in schema_remarks.index_remark[table]:
                errors.append(
                    "Table '%s' has no remark for index '%s'." % (table, canon)
                )
            else:
                remark = schema_remarks.index_remark[table][canon]
            if remark:
                remarks = [remark]
            else:
                remarks = []
            indexes[canon] = {
                'Name': kn,
                'Fields': {i['Seq_in_index']: i['Column_name']},
                'Properties': props,
                'Remarks': remarks,
            }
    # replace the 'Fields' map with an ordered list.
    for k in list(indexes.keys()):
        f = list(indexes[k]['Fields'].items())
        f.sort()
        indexes[k]['Fields'] = str.join(', ', list(map((lambda l: l[1]), f)))
    return indexes


# Given a schema version name, get the schema for that database as a
# map from table name to (columns, indexes), where columns is a map
# produced by reduce_columns and indexes is a map produced by
# reduce_indexes.


def get_schema(schema_version, errors):
    f = None
    schema = {}
    try:
        f = open('pickles/%s' % schema_version, 'rb')
        (sv, schema) = pickle.load(f)
        f.close()
    except FileNotFoundError:
        errors.append(
            "Unable to locate schema data file for version %s" % (schema_version)
        )
    except Exception as e:
        errors.append("%s: %s" % (type(e).__name__, str(e)))
    tables = list(schema.keys())
    for table in tables:
        (columns, indexes) = schema[table]
        schema[table] = (
            reduce_columns(table, columns, errors),
            reduce_indexes(table, indexes, errors),
        )
    return schema, errors


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
