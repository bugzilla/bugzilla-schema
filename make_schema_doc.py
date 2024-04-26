#!/usr/bin/env python3
#             Perforce Defect Tracking Integration Project
#              <http://www.ravenbrook.com/project/p4dti/>
#
#  MAKE_SCHEMA_DOC.PY -- GENERATE BUGZILLA SCHEMA DOCUMENTATION
#
#             Nick Barnes, Ravenbrook Limited, 2003-07-07
#
#
# 1. INTRODUCTION
#

# This module generates Bugzilla schema documentation.
#
# The intended readership is project developers.
#
# This document is not confidential.

import copy
import re
import types
import time
import sys

import schema_remarks
import get_schema


class BzSchemaProcessingException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
    def __str__(self):
        return '\n' + self.message

errors = []

def version_compare(v1,v2):
    # we already have the order defined in a table, let's use it
    # this also lets us make 5.1 be > 5.2 (which is actually true)
    v1idx = schema_remarks.version_order.index(v1)
    v2idx = schema_remarks.version_order.index(v2)
    return (v1idx > v2idx) - (v1idx < v2idx)

vd_cache = {}

# versioning_dict takes two bugzilla versions, first and last, and the
# list of the bugzilla_versions for which we are generating the schema
# doc.  It returns either None (if none of the versions are included
# in the range from first to last inclusive) or a dictionary with two
# keys, VERSION_COLOUR and VERSION_STRING, for use in formatting a
# part of the schema documentation which is only true from 'first' to
# 'last'.  'first' can be None (meaning since before time began).
# 'last' can be None (meaning until the end of time).  Possible
# outcomes:
# 
# V_C     V_S                           state
# 
# -       -                             no versions in range
# ''      ''                            all versions in range
# green   From <first>                  no versions after last
# red     Up to and including <last>    no versions before first
# red     In version <only>             first = last
# red     From <first> to <last>        first < last

def versioning_dict(first, last, versions):
    if versions not in vd_cache:
        vd_cache[versions] = {}
    if (first,last) in vd_cache[versions]:
        return vd_cache[versions][(first,last)]
    dict = {}
    before_first = False # any versions before first?
    inside = False       # any versions in the range?
    after_last = False   # any versions after last?
    for v in versions:
        if first and version_compare(first, v) > 0:
            before_first = True # this version is before the first
        elif last and version_compare(last, v) < 0:
            after_last = True # this version is after the last
        elif not last or version_compare(last, v) >= 0:
            inside = True # this version is inside the range
    if not inside:
        vd_cache[versions][(first,last)] = None
        return
    outside = before_first or after_last
    if not outside:
        dict['VERSION_COLOUR'] = ''
        dict['VERSION_STRING'] = ''
    elif before_first and not after_last:
        dict['VERSION_COLOUR'] = green
        dict['VERSION_STRING'] = '<b>From %s:</b> ' % first
    elif before_first and after_last:
        dict['VERSION_COLOUR'] = red
        if first == last:
            dict['VERSION_STRING'] = '<b>In version %s:</b> ' % first
        else:
            dict['VERSION_STRING'] = '<b>From %s to %s:</b> ' % (first, last)
    elif not before_first and after_last:
        dict['VERSION_COLOUR'] = red
        dict['VERSION_STRING'] = '<b>Up to and including %s:</b> ' % last
    vd_cache[versions][(first,last)] = dict
    return dict
    
# Parts of the schema description only apply to particular ranges of
# versions of Bugzilla.  For instance, only versions 2.16rc1 to 2.16.6
# include the attachment statuses.
# 
# To handle this, we allow schema remarks to be either a simple string
# or a triplet (first, last, string), in which first and last are the
# names of the first and last versions of Bugzilla for which the
# string is a true remark, or a list of such triplets.
# 
# A schema document which does not include any of those versions will
# simply omit the string.
# 
# The strings in schema are format strings which are formatted using a
# dictionary, allowing them to include named dynamically-generated
# elements. These elements include VERSION_STRING (see above) and
# VERSION_COLOUR.
#
# process() takes a schema remark and a list of bugzilla versions and
# returns the concatenated processed string


def process(x, bugzilla_versions, dict):
    if type(x) == bytes or type(x) == str:
        return x % dict
    elif type(x) == list:
        return str.join('', list(map(lambda i, bv = bugzilla_versions, d = dict: process(i, bv, d), x)))
    else:
        (first, last, text) = x
        vd = versioning_dict(first, last, bugzilla_versions)
        if vd:
            dict.update(vd)
            return text % dict
        else:
            return ''

# 5. Generating HTML

body=[]

def add(s):
    body.append(s)

# output a coloured anchored table row, with a <th> in the first
# column.

def output_row(anchor, name, dict, keys, colours):
    add('  <tr%s valign="top" align="left">\n\n' % colours[''])
    add('    <th%s><a id="%s" name="%s">%s</a></th>\n\n' %
        (colours['Name'], anchor, anchor, dict['Name']))
    for k in keys:
        add('    <td%s>%s</td>\n\n' % (colours[k], dict[k]))
    add('  </tr>\n\n')

# output the main schema table for a table.    

def output_description(table, colour, remark, columns, colours, dict, bv):
    if remark:
        add('<p>%s</p>\n\n' % remark)
    add('<table%s border="1" cellspacing="0" cellpadding="5">\n\n' % colour)

    add('  <tr valign="top" align="left">\n\n')
    add('    <th>Field</th>\n\n')
    add('    <th>Type</th>\n\n')
    add('    <th>Default</th>\n\n')
    add('    <th>Properties</th>\n\n')
    add('    <th>Remarks</th>\n\n')
    add('  </tr>\n\n')
    cs = list(columns.keys())
    cs.sort()
    for c in cs:
        d = columns[c]
        if d['Remarks']:
            d['Remarks'] = str.join(' ',
              list(map(lambda r,bv=bv,d=dict: process(r,bv,d),d['Remarks'])))
        else:
            d['Remarks'] = '-'
        output_row('column-%s-%s' % (table, c), c, d, ['Type',
                                                       'Default',
                                                       'Properties',
                                                       'Remarks'],
                   colours[c])
    add('</table>\n\n')

# output the indexes table for a table    

def output_indexes(table, colour, indexes, colours, dict, bv):
    add('<table%s border="1" cellspacing="0" cellpadding="5">\n\n' % colour)
    # order the indexes: PRIMARY first, then alphabetical.
    inames = list(indexes.keys())
    if 'PRIMARY' in inames:
        inames.remove('PRIMARY')
        inames.sort()
        inames = ['PRIMARY'] + inames
    add('  <tr valign="top" align="left">\n\n')
    add('    <th>Name</th>\n\n')
    add('    <th>Fields</th>\n\n')
    add('    <th>Properties</th>\n\n')
    add('    <th>Remarks</th>\n\n')
    add('  </tr>\n\n')
    for iname in inames:
        l = indexes[iname]
        if l['Remarks']:
            l['Remarks'] = str.join(' ',
              list(map(lambda r,bv=bv,d=dict: process(r,bv,d),l['Remarks'])))
        else:
            l['Remarks'] = '-'
        output_row("index-%s-%s" % (table, iname), iname, l, ['Fields',
                                                              'Properties',
                                                              'Remarks'],
                   colours[iname])
    add ('</table>\n\n')

def make_output_dict(schema, bugzilla_versions):
    dict={}
    dict['FIRST_VERSION'] = bugzilla_versions[0]
    dict['LAST_VERSION'] = bugzilla_versions[-1]
    if len(bugzilla_versions) == 1:
        dict['NOTATION_GUIDE'] = ''
        dict['BUGZILLA_VERSIONS'] = "version " +  bugzilla_versions[0]
    else:
        dict['NOTATION_GUIDE'] = schema_remarks.notation_guide % dict
        dict['BUGZILLA_VERSIONS'] = "versions " +  str.join(', ', bugzilla_versions[:-1]) + ' and ' + bugzilla_versions[-1]
    tables = list(schema.keys())
    for table in tables:
        dict['the-table-%s' % table] = 'the <a href="#table-%s">%s</a> table' % (table, table)
        dict['table-%s' % table] = '<a href="#table-%s">%s</a>' % (table,table)
        (versions, columns, indexes) = schema[table]
        for c in list(columns.keys()):
            dict['column-%s-%s' % (table, c)] = '<a href="#column-%s-%s">%s.%s</a>' % (table, c, table, c)
        for i in list(indexes.keys()):
            dict['index-%s-%s' % (table, i)] = '<a href="#index-%s-%s">%s:%s</a>' % (table, i, table, i)
    for t in list(schema_remarks.table_remark.keys()):
        k = 'the-table-%s' % t
        if k not in dict:
            dict[k] = 'the %s table' % t
            dict['table-%s' % t] = t
        if t in schema_remarks.column_renamed:
            for (alt,canon) in list(schema_remarks.column_renamed[t].items()):
                kcanon = 'column-%s-%s' % (t, canon)
                kalt = 'column-%s-%s' % (t, alt)
                if kcanon in dict and kalt not in dict: # the canonical name is in the schema
                    dict[kalt] = '<a href="#column-%s-%s">%s.%s</a>' % (t, canon, t, alt)
                else:
                    dict[kalt] = '%s.%s' % (t,alt)
        if t in schema_remarks.index_renamed:
            for (alt,canon) in list(schema_remarks.index_renamed[t].items()):
                kcanon = 'index-%s-%s' % (t, canon)
                kalt = 'index-%s-%s' % (t, alt)
                if kcanon in dict and kalt not in dict: # the canonical name is in the schema
                    dict[kalt] = '<a href="#index-%s-%s">%s:%s</a>' % (t, canon, t, alt)
                else:
                    dict[kalt] = '%s:%s' % (t,alt)
        for c in list(schema_remarks.column_remark[t].keys()):
            k = 'column-%s-%s' % (t,c)
            if k not in dict:
                dict[k] = '%s.%s' % (t,c)
        for i in list(schema_remarks.index_remark[t].keys()):
            k = 'index-%s-%s' % (t,i)
            if k not in dict:
                dict[k] = '%s:%s' % (t,i)
                
    return dict

def tables_tables(tables_table_rows, quick_tables_table_rows, dict):
    n = len(tables_table_rows)
    TABLES_TABLE_COLS = 2
    per_col = int((n + TABLES_TABLE_COLS - 1)/TABLES_TABLE_COLS)
    tables_table = ('<table border="0" cellpadding="10">\n\n' +
                    '<tr valign="top" align="left">\n\n')
    for i in range(0, TABLES_TABLE_COLS):
        tables_table += ('<td><table border="1" cellspacing="0" cellpadding="5">\n\n'
                         '<tr valign="top" align="left">\n\n'
                         '<th>Name</th><th>Description</th>\n\n')
        for j in range(0, per_col):
            k = i * per_col + j
            if k < n:
                tables_table += ('<tr valign="top" align="left">\n\n' +
                                 tables_table_rows[k] +
                                 '</tr>\n')
        tables_table += '</table></td>\n\n'
    tables_table += '</tr></table>\n\n'

    n = len(quick_tables_table_rows)
    QUICK_TABLES_TABLE_COLS = 4
    remainder = n % QUICK_TABLES_TABLE_COLS
    if (remainder > 0):
        while (remainder < QUICK_TABLES_TABLE_COLS):
            quick_tables_table_rows.append('<td>&nbsp;</td>')
            remainder = remainder + 1
            n = n + 1

    quick_tables_table = '<table border="0" cellspacing="0" cellpadding="1">\n\n'
    rows = int(n / QUICK_TABLES_TABLE_COLS)
    for i in range(0, rows):
        quick_tables_table += '<tr valign="top" align="left">\n\n'
        for k in range(0,QUICK_TABLES_TABLE_COLS):
            quick_tables_table += quick_tables_table_rows[k * rows + i]
        quick_tables_table += '</tr>\n\n'
    quick_tables_table += '</table>'
    dict['QUICK_TABLES_TABLE'] = quick_tables_table
    dict['TABLES_TABLE'] = tables_table

def output_schema(schema, remarks, colours, bugzilla_versions):
    global body
    body=[]
    dict= make_output_dict(schema, bugzilla_versions)
    tables_table_rows = []
    quick_tables_table_rows = []
    tables = list(schema.keys())
    tables.sort()
    for table in tables:
        (versions, columns, indexes) = schema[table]
        colour = colours[table]['']
        thisremarks = remarks[table]
        if not isinstance(thisremarks, list): thisremarks = [thisremarks]
        remark = str.join(' ',
                  [process(r,bugzilla_versions,dict) for r in thisremarks])
        tables_table_rows.append(('<th%s><a href="#table-%s">%s</a></th>\n\n' % (colour, table, table)) +
                                 ('    <td%s>%s</td>\n\n' % (colour, remark)))
        quick_tables_table_rows.append('<th%s><a href="#table-%s">%s</a></th>\n\n' % (colour, table, table))
        add('<h3><a id="table-%s" name="table-%s">The "%s" table</a></h3>\n\n\n' % (table, table, table))
        output_description(table, colour, remark, columns,
                           colours[table]['column'], dict, bugzilla_versions)
        if indexes:
            add('<p>Indexes:</p>\n\n')
            output_indexes(table, colour, indexes,
                           colours[table]['index'], dict, bugzilla_versions)
        else:
            add('<p>The "%s" table has no indexes.</p>' % table)
    tables_tables(tables_table_rows, quick_tables_table_rows, dict)
    return (dict, body)

# 6. Code to read all the database schemas and figure out the history
# from that.

# colours of tables, and rows, and entries                

red = ' bgcolor="#ffcccc"'          # no longer present
green = ' bgcolor="#ccffcc"'        # no longer absent
blue = ' bgcolor="#ccccff"'         # changed
white = ''                          # no colour

# colours: {table: {'': table colour,
#                    'column': {column: {'': column colour,
#                                        field: field colour}},
#                    'index': {index:   {'': index colour,
#                                        field: field colour}),
#                   }}

def init_colours(colours, t, cols, inds):
    if t not in colours:
        colours[t] = {'': white}
        colours[t]['column'] = {}
        colours[t]['index'] = {}
    for c in cols:
        if c not in colours[t]['column']:
            colours[t]['column'][c] = {}
            for k in ['', 'Name', 'Default', 'Type', 'Properties', 'Remarks']:
                colours[t]['column'][c][k] = white
    for i in inds:
        if i not in colours[t]['index']:
            colours[t]['index'][i] = {'': white}
            for k in ['', 'Name', 'Fields', 'Properties', 'Remarks']:
                colours[t]['index'][i][k] = white

# any table can omit an entry at any level, meaning 'the same as other
# entries at this level'.

# For a field which can change (e.g. the Type of a column), we store
# it during processing as a list of pairs:
# 
#    [(first bugzilla version, value), ...]
# 
# So list[-1][1] is the current value.  When we're done figuring out
# the schema history, we replace this list with a single value.

# Make the initial pair lists for a column.

def pair_up_column_entries(bz, column):
    for k in ['Name', 'Type', 'Default', 'Properties']:
        column[k] = [(bz, column[k])]

# Make the initial pair lists for an index.

def pair_up_index_entries(bz, index):
    for k in ['Name', 'Fields', 'Properties']:
        index[k] = [(bz, index[k])]

# Make all the initial pair lists for a table.
    
def pair_up_table_entries(bz, schema, table):
    (columns, indexes) = schema[table]
    for c in list(columns.values()):
        pair_up_column_entries(bz, c)
    for i in list(indexes.values()):
        pair_up_index_entries(bz, i)

def pair_up_schema(bz, schema):
    for t in list(schema.keys()):
        pair_up_table_entries(bz, schema, t)

# Given a pair list, make a single value which explains the history.
# I've tried various ways of showing this; this is the best I've come
# up with.

def reduce_pair_list(pl):
    current = None
    last_change = None
    changes = []
    for p in pl:
        if p[1] == current:
            continue
        current = p[1]
        last_change = p[0]
        changes.append((last_change, current))
    return changes
    
def stringify_pairs(pl):
    changes = reduce_pair_list(pl)
    if len(changes) == 1:
        return changes[0][1]
    else:
        s = []
        for c in changes:
            s.append('<b>%s: </b>%s'% (c[0], c[1]))
        return str.join('; <br />\n', s)

# Special treatment for types, as we want enum types to show up
# nicely.

enum_re = re.compile("^enum *\\( *(.*) *\\) *$")

def stringify_type(pl):
    pl = reduce_pair_list(pl)
    newpl = []
    items = []
    for p in pl:
        if not enum_re.match(p[1]):
            # not an enum
            items = []
            newpl.append(p)
        else:
            if items == []:
                # first enum
                newpl.append(p)
                items = list(map(str.strip, str.split(enum_re.match(p[1]).groups()[0], ",")))
            else:
                # enum following an enum
                new_items = list(map(str.strip, str.split(enum_re.match(p[1]).groups()[0], ",")))
                add = []
                delete = []
                for i in items:
                    if i not in new_items:
                        delete.append(i)
                for i in new_items:
                    if i not in items:
                        add.append(i)
                say = ''
                if add:
                    say += '<b>Added: </b> %s. ' % str.join(', ', add)
                if delete:
                    say += '<b>Removed: </b> %s. ' % str.join(', ', delete)
                newpl.append((p[0], say))
                items = new_items
    return stringify_pairs(newpl)

# Given a schema, fix up all the pair lists.    

def stringify_schema(schema):
    for table in list(schema.keys()):
        (versions, columns, indexes) = schema[table]
        for c in list(columns.values()):
            c['Type'] = stringify_type(c['Type'])
            for k in ['Name', 'Default', 'Properties']:
                c[k] = stringify_pairs(c[k])
        for i in list(indexes.values()):
            for k in ['Name', 'Fields', 'Properties']:
                i[k] = stringify_pairs(i[k])

def make_annotation(base, note):
    if note:
        return (' <b>%s (%s).</b>\n' % (base, note))
    else:
        return (' <b>%s.</b>\n' % base)

# Given a list of schemas, produce a single versioned schema, fill in
# the colour tables and add to all the remarks reflecting schema
# versions in which particular tables/columns/indexes are added and/or
# removed.

def make_versioned_schema(schema_list,
                          colours,
                          table_remarks):
    # Pivot so we get a map from table/column/index to paired lists of
    # properties and lists of BZ versions.  Fill in blue cells while
    # we're doing this.
    tables = {}
    bzs = []
    for (bz, schema) in schema_list:
        bzs.append(bz)
        for t in list(schema.keys()):
            if t not in tables:
                tables[t] = ([],{},{})
                if t in schema_remarks.table_remark:
                    remark = schema_remarks.table_remark[t]
                    if remark is None:
                        remark = []
                    elif type(remark) == bytes:
                        remark = [remark]
                    else:
                        remark = remark[:]
                else:
                    remark = []
                table_remarks[t] = remark
            tables[t][0].append(bz)
            (cols,inds) = schema[t]
            init_colours(colours, t, list(cols.keys()), list(inds.keys()))
            for c in list(cols.keys()):
                crec = tables[t][1].get(c,{'versions': []})
                tables[t][1][c] = crec
                crec['versions'].append(bz)
                for k in ['Name', 'Default', 'Type', 'Properties']:
                    if (k in crec and
                        crec[k][-1][1] != cols[c][k][0][1]):
                        colours[t]['column'][c][k] = blue
                    crec[k] = crec.get(k,[])
                    crec[k] += cols[c][k]
                    crec['Remarks'] = cols[c]['Remarks']
            for i in list(inds.keys()):
                irec = tables[t][2].get(i,{'versions': []})
                tables[t][2][i] = irec
                irec['versions'].append(bz)
                for k in ['Name', 'Fields', 'Properties']:
                    if (k in irec and
                        irec[k][-1][1] != inds[i][k][0][1]):
                        colours[t]['index'][i][k] = blue
                    irec[k] = irec.get(k, [])
                    irec[k] += inds[i][k]
                    irec['Remarks'] = inds[i]['Remarks']

    # Now we know all the tables, columns, indexes in our report,
    # and what versions of bugzilla each one appears in.
    # Figure out all the colours and remarks accordingly.
    first_bz = schema_list[0][0]
    last_bz = schema_list[-1][0]
    for t in list(tables.keys()):
        v = tables[t][0]
        if last_bz not in v:     # not in last version: red
            colours[t][''] = red
        elif first_bz not in v:  # not in first version: green
            colours[t][''] = green
        # don't colour tables blue, so we're done
        present = (first_bz in v)
        for bz in bzs:
            if present and (bz not in v): # removed in this version
                present = False
                if t in schema_remarks.table_removed_remark:
                    note = schema_remarks.table_removed_remark[t]
                    note = make_annotation('Removed in %s' % bz, note)
                    table_remarks[t].append(note)
                else:
                    errors.append('No remark to remove table %s' % t)
            elif (not present) and (bz in v): # added in this version
                present = True
                if t in schema_remarks.table_added_remark:
                    note = schema_remarks.table_added_remark[t]
                    note = make_annotation('Added in %s' % bz, note)
                    if not isinstance(table_remarks[t], list): table_remarks[t] = [table_remarks[t]]
                    table_remarks[t].append(note)
                else:
                    errors.append('No remark to add table %s' % t)

        # now the columns:
        for c in list(tables[t][1].keys()):
            v = tables[t][1][c]['versions']
            if last_bz not in v:
                colours[t]['column'][c][''] = red
            elif first_bz not in v:
                colours[t]['column'][c][''] = green
            # don't colour whole column rows blue, so we're done
            present = tables[t][0][0] in v
            for bz in tables[t][0]:
                if present and (bz not in v):
                    # removed in this version
                    present = False
                    if (t in schema_remarks.column_removed_remark and
                        c in schema_remarks.column_removed_remark[t]):
                        note = schema_remarks.column_removed_remark[t][c]
                    else:
                        errors.append("No remark to remove %s.%s." %(t, c))
                        note = None
                    note = make_annotation('Removed in %s' % bz, note)
                    tables[t][1][c]['Remarks'].append(note)
                elif (not present) and (bz in v):
                    # added in this version
                    present = True
                    if (t in schema_remarks.column_added_remark and
                        c in schema_remarks.column_added_remark[t]):
                        note = schema_remarks.column_added_remark[t][c]
                    else:
                        errors.append("No remark to add %s.%s." % (t,c))
                        note = None
                    note = make_annotation('Added in %s' % bz, note)
                    tables[t][1][c]['Remarks'].append(note)

        # now the indexes:
        for i in list(tables[t][2].keys()):
            v = tables[t][2][i]['versions']
            if last_bz not in v:
                colours[t]['index'][i][''] = red
            elif first_bz not in v:
                colours[t]['index'][i][''] = green
            # don't colour whole index rows blue, so we're done
            present = tables[t][0][0] in v
            for bz in tables[t][0]:
                if present and (bz not in v):
                    # removed in this version
                    present = False
                    if (t in schema_remarks.index_removed_remark and
                        i in schema_remarks.index_removed_remark[t]):
                        note = schema_remarks.index_removed_remark[t][i]
                    else:
                        errors.append("No remark to remove %s:%s." %(t, i))
                        note = None
                    note = make_annotation('Removed in %s' % bz, note)
                    tables[t][2][i]['Remarks'].append(note)
                elif (not present) and (bz in v):
                    # added in this version
                    present = True
                    if (t in schema_remarks.index_added_remark and
                        i in schema_remarks.index_added_remark[t]):
                        note = schema_remarks.index_added_remark[t][i]
                    else:
                        errors.append("No remark to add %s:%s." % (t, i))
                        note = None
                    note = make_annotation('Added in %s' % bz, note)
                    tables[t][2][i]['Remarks'].append(note)
    return tables

# get all the schemas and combine them.

def get_versioned_tables(first, last):
    global errors
    errors = []
    if not first in schema_remarks.version_order:
        raise BzSchemaProcessingException("I don't know about version '%s'." % last)
    if not last in schema_remarks.version_order:
        raise BzSchemaProcessingException("I don't know about version '%s'." % last)
    if not (schema_remarks.version_order.index(last) >= schema_remarks.version_order.index(first)):
        raise BzSchemaProcessingException("Version '%s' comes before version '%s'." % (last, first))
    colours = {}
    tr = {}
    if not first in schema_remarks.version_schema_map:
        raise BzSchemaProcessingException("I know version '%s' exists, but I seem to be missing the data for it." % last)
    if not last in schema_remarks.version_schema_map:
        raise BzSchemaProcessingException("I know version '%s' exists, but I seem to be missing the data for it." % last)
    schema_name = schema_remarks.version_schema_map[first]
    schema, errors = get_schema.get_schema(schema_name, errors)
    # turn fields into lists connecting Bugzilla version to value
    pair_up_schema(first, schema)
    schemas = [(first, schema)]
    bugzilla_versions = schema_remarks.version_order[(schema_remarks.version_order.index(first)) : (schema_remarks.version_order.index(last)+1)]
    for bz_name in bugzilla_versions[1:]:
        new_schema_name = schema_remarks.version_schema_map[bz_name]
        if new_schema_name == schema_name:
            continue
        schema_name = new_schema_name
        new_schema, errors = get_schema.get_schema(schema_name, errors)
        pair_up_schema(bz_name, new_schema)
        schemas.append((bz_name, new_schema))
    schema = make_versioned_schema(schemas,
                                   colours,
                                   tr)
    stringify_schema(schema)
    return (schema, tr, colours, tuple(bugzilla_versions), errors)

def make_version_table(versions):
    table = ''
    for (v, date, remark) in schema_remarks.version_remark:
        if v not in versions:
            remark += ' Not described in this document.'
        table += ('  <tr valign="top" align="left">\n\n'
                  '    <td>%s</td>\n\n'
                  '    <td>%s</td>\n\n'
                  '    <td>%s</td>\n\n' % (date, v, remark))
    return table

def strip_p4_id(id):
    if id[:5] == '$Id: ':
        id = id[5:]
    if id[-2:] == ' $':
        id = id[:-2]
    return id

# Write the versioned schema document, including prelude and
# afterword, to a named file.  This is the function we call to
# generate our Bugzilla schema doc.  Note that although it will
# generate schema diffs for various version ranges, the prelude and
# afterword it adds are specific to certain Bugzilla versions.

def make_tables(first, last):
    global errors
    (schema, tr, colours, bv, errors) = get_versioned_tables(first, last)
    (dict, html) = output_schema(schema, tr, colours, bv)
    dict['VERSIONS_TABLE'] = make_version_table(bv)
    dict['TIME'] = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))
    dict['DATE'] = time.strftime("%Y-%m-%d", time.gmtime(time.time()))
    dict['SCRIPT_ID'] = strip_p4_id('$Id$')
    dict['REMARKS_ID'] = strip_p4_id(schema_remarks.remarks_id)
    body = (process(schema_remarks.prelude, bv, dict) +
            process(html, bv, dict) + 
            process(schema_remarks.afterword, bv, dict))
    header = process(schema_remarks.header, bv, dict)
    footer = process(schema_remarks.footer, bv, dict)
    if errors:
        e = str.join('<br/>\n', errors)
        raise BzSchemaProcessingException(e)
    return (header, body, footer)

def write_file(first, last, filename):
    file = open(filename, 'w')
    (header, body, footer) = make_tables(first, last)
    file.write(header)
    file.write(body)
    file.write(footer)
    file.close()

def make_body(first, last):
    (header, body, footer) = make_tables(first, last)
    return body

def validate_schema_remarks():
    for v in schema_remarks.version_order:
        if not v in schema_remarks.version_schema_map:
            errors.append(f"Version {v} found in version_order is not listed in version_schema_map")
        if len([item for item in schema_remarks.version_remark if item[0] == v]) < 1:
            errors.append(f"Version {v} found in version_order is not listed in version_remark")
    for v in schema_remarks.version_schema_map.keys():
        if not v in schema_remarks.version_order:
            errors.append(f"Version {v} found in version_schema_map is not listed in version_order")
        if len([item for item in schema_remarks.version_remark if item[0] == v]) < 1:
            errors.append(f"Version {v} found in version_schema_map is not listed in version_remark")
    for item in schema_remarks.version_remark:
        v = item[0];
        if not v in schema_remarks.version_order:
            errors.append(f"Version {v} found in version_remark is not listed in version_order")
        if not v in schema_remarks.version_schema_map:
            errors.append(f"Version {v} found in version_remark is not listed in version_schema_map")
    if errors:
        e = str.join('<br/>\n', errors)
        raise BzSchemaProcessingException(e)
    print("Versions validated.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--validate':
        validate_schema_remarks()
    else:
        try:
            (first, last, filename) = sys.argv[1:]
        except ValueError:
            print("Please pass the starting and ending schema versions and a filename to output to,")
            print("or pass --validate to check for version number sanity.")
            sys.exit()
        write_file(first, last, filename)

# A. REFERENCES
#
#
# B. DOCUMENT HISTORY
#
# 2001-03-08 NB Created.
#
#
# C. COPYRIGHT AND LICENSE
#
# This file is copyright (c) 2001 Perforce Software, Inc.  All rights
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
