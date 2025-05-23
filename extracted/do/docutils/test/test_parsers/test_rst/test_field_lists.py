#! /usr/bin/env python3

# $Id: test_field_lists.py 9425 2023-06-30 14:56:47Z milde $
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
Tests for states.py.
"""

from pathlib import Path
import sys
import unittest

if __name__ == '__main__':
    # prepend the "docutils root" to the Python library path
    # so we import the local `docutils` package.
    sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from docutils.frontend import get_default_settings
from docutils.parsers.rst import Parser
from docutils.utils import new_document


class ParserTestCase(unittest.TestCase):
    def test_parser(self):
        parser = Parser()
        settings = get_default_settings(Parser)
        settings.warning_stream = ''
        for name, cases in totest.items():
            for casenum, (case_input, case_expected) in enumerate(cases):
                with self.subTest(id=f'totest[{name!r}][{casenum}]'):
                    document = new_document('test data', settings.copy())
                    parser.parse(case_input, document)
                    output = document.pformat()
                    self.assertEqual(case_expected, output)


totest = {}

totest['field_lists'] = [
["""\
One-liners:

:Author: Me

:Version: 1

:Date: 2001-08-11

:Parameter i: integer
""",
"""\
<document source="test data">
    <paragraph>
        One-liners:
    <field_list>
        <field>
            <field_name>
                Author
            <field_body>
                <paragraph>
                    Me
        <field>
            <field_name>
                Version
            <field_body>
                <paragraph>
                    1
        <field>
            <field_name>
                Date
            <field_body>
                <paragraph>
                    2001-08-11
        <field>
            <field_name>
                Parameter i
            <field_body>
                <paragraph>
                    integer
"""],
["""\
One-liners, no blank lines:

:Author: Me
:Version: 1
:Date: 2001-08-11
:Parameter i: integer
""",
"""\
<document source="test data">
    <paragraph>
        One-liners, no blank lines:
    <field_list>
        <field>
            <field_name>
                Author
            <field_body>
                <paragraph>
                    Me
        <field>
            <field_name>
                Version
            <field_body>
                <paragraph>
                    1
        <field>
            <field_name>
                Date
            <field_body>
                <paragraph>
                    2001-08-11
        <field>
            <field_name>
                Parameter i
            <field_body>
                <paragraph>
                    integer
"""],
["""\
:field:
empty item above, no blank line
""",
"""\
<document source="test data">
    <field_list>
        <field>
            <field_name>
                field
            <field_body>
    <system_message level="2" line="2" source="test data" type="WARNING">
        <paragraph>
            Field list ends without a blank line; unexpected unindent.
    <paragraph>
        empty item above, no blank line
"""],
["""\
Field bodies starting on the next line:

:Author:
  Me
:Version:
  1
:Date:
  2001-08-11
:Parameter i:
  integer
""",
"""\
<document source="test data">
    <paragraph>
        Field bodies starting on the next line:
    <field_list>
        <field>
            <field_name>
                Author
            <field_body>
                <paragraph>
                    Me
        <field>
            <field_name>
                Version
            <field_body>
                <paragraph>
                    1
        <field>
            <field_name>
                Date
            <field_body>
                <paragraph>
                    2001-08-11
        <field>
            <field_name>
                Parameter i
            <field_body>
                <paragraph>
                    integer
"""],
["""\
One-paragraph, multi-liners:

:Authors: Me,
          Myself,
          and I
:Version: 1
          or so
:Date: 2001-08-11
       (Saturday)
:Parameter i: counter
              (integer)
""",
"""\
<document source="test data">
    <paragraph>
        One-paragraph, multi-liners:
    <field_list>
        <field>
            <field_name>
                Authors
            <field_body>
                <paragraph>
                    Me,
                    Myself,
                    and I
        <field>
            <field_name>
                Version
            <field_body>
                <paragraph>
                    1
                    or so
        <field>
            <field_name>
                Date
            <field_body>
                <paragraph>
                    2001-08-11
                    (Saturday)
        <field>
            <field_name>
                Parameter i
            <field_body>
                <paragraph>
                    counter
                    (integer)
"""],
["""\
One-paragraph, multi-liners, not lined up:

:Authors: Me,
  Myself,
  and I
:Version: 1
  or so
:Date: 2001-08-11
  (Saturday)
:Parameter i: counter
  (integer)
""",
"""\
<document source="test data">
    <paragraph>
        One-paragraph, multi-liners, not lined up:
    <field_list>
        <field>
            <field_name>
                Authors
            <field_body>
                <paragraph>
                    Me,
                    Myself,
                    and I
        <field>
            <field_name>
                Version
            <field_body>
                <paragraph>
                    1
                    or so
        <field>
            <field_name>
                Date
            <field_body>
                <paragraph>
                    2001-08-11
                    (Saturday)
        <field>
            <field_name>
                Parameter i
            <field_body>
                <paragraph>
                    counter
                    (integer)
"""],
["""\
Multiple body elements:

:Authors: - Me
          - Myself
          - I

:Abstract:
    This is a field list item's body,
    containing multiple elements.

    Here's a literal block::

        def f(x):
            return x**2 + x

    Even nested field lists are possible:

    :Date: 2001-08-11
    :Day: Saturday
    :Time: 15:07
""",
"""\
<document source="test data">
    <paragraph>
        Multiple body elements:
    <field_list>
        <field>
            <field_name>
                Authors
            <field_body>
                <bullet_list bullet="-">
                    <list_item>
                        <paragraph>
                            Me
                    <list_item>
                        <paragraph>
                            Myself
                    <list_item>
                        <paragraph>
                            I
        <field>
            <field_name>
                Abstract
            <field_body>
                <paragraph>
                    This is a field list item's body,
                    containing multiple elements.
                <paragraph>
                    Here's a literal block:
                <literal_block xml:space="preserve">
                    def f(x):
                        return x**2 + x
                <paragraph>
                    Even nested field lists are possible:
                <field_list>
                    <field>
                        <field_name>
                            Date
                        <field_body>
                            <paragraph>
                                2001-08-11
                    <field>
                        <field_name>
                            Day
                        <field_body>
                            <paragraph>
                                Saturday
                    <field>
                        <field_name>
                            Time
                        <field_body>
                            <paragraph>
                                15:07
"""],
["""\
Nested field lists on one line:

:field1: :field2: :field3: body
:field4: :field5: :field6: body
                  :field7: body
         :field8: body
         :field9: body line 1
           body line 2
""",
"""\
<document source="test data">
    <paragraph>
        Nested field lists on one line:
    <field_list>
        <field>
            <field_name>
                field1
            <field_body>
                <field_list>
                    <field>
                        <field_name>
                            field2
                        <field_body>
                            <field_list>
                                <field>
                                    <field_name>
                                        field3
                                    <field_body>
                                        <paragraph>
                                            body
        <field>
            <field_name>
                field4
            <field_body>
                <field_list>
                    <field>
                        <field_name>
                            field5
                        <field_body>
                            <field_list>
                                <field>
                                    <field_name>
                                        field6
                                    <field_body>
                                        <paragraph>
                                            body
                                <field>
                                    <field_name>
                                        field7
                                    <field_body>
                                        <paragraph>
                                            body
                    <field>
                        <field_name>
                            field8
                        <field_body>
                            <paragraph>
                                body
                    <field>
                        <field_name>
                            field9
                        <field_body>
                            <paragraph>
                                body line 1
                                body line 2
"""],
["""\
:Parameter i j k: multiple arguments
""",
"""\
<document source="test data">
    <field_list>
        <field>
            <field_name>
                Parameter i j k
            <field_body>
                <paragraph>
                    multiple arguments
"""],
["""\
:Field *name* `with` **inline** ``markup``: inline markup in
                                            field name is parsed.
""",
"""\
<document source="test data">
    <field_list>
        <field>
            <field_name>
                Field \n\
                <emphasis>
                    name
                 \n\
                <title_reference>
                    with
                 \n\
                <strong>
                    inline
                 \n\
                <literal>
                    markup
            <field_body>
                <paragraph>
                    inline markup in
                    field name is parsed.
"""],
["""\
:Field name with *bad inline markup: should generate warning.
""",
"""\
<document source="test data">
    <field_list>
        <field>
            <field_name>
                Field name with \n\
                <problematic ids="problematic-1" refid="system-message-1">
                    *
                bad inline markup
            <field_body>
                <system_message backrefs="problematic-1" ids="system-message-1" level="2" line="1" source="test data" type="WARNING">
                    <paragraph>
                        Inline emphasis start-string without end-string.
                <paragraph>
                    should generate warning.
"""],
[r"""Some edge cases:

:Empty:
:Author: Me
No blank line before this paragraph.

: Field: marker must not begin with whitespace.

:Field : marker must not end with whitespace.

Field: marker is missing its open-colon.

:Field marker is missing its close-colon.

:Field\: names\: with\: colons\:: are possible.

:\\Field\  names with backslashes\\: are possible, too.

:\\: A backslash.

:Not a\\\: field list.

:Not a \: field list either.

:\: Not a field list either.

:\:
    A definition list, not a field list.
""",
"""\
<document source="test data">
    <paragraph>
        Some edge cases:
    <field_list>
        <field>
            <field_name>
                Empty
            <field_body>
        <field>
            <field_name>
                Author
            <field_body>
                <paragraph>
                    Me
    <system_message level="2" line="5" source="test data" type="WARNING">
        <paragraph>
            Field list ends without a blank line; unexpected unindent.
    <paragraph>
        No blank line before this paragraph.
    <paragraph>
        : Field: marker must not begin with whitespace.
    <paragraph>
        :Field : marker must not end with whitespace.
    <paragraph>
        Field: marker is missing its open-colon.
    <paragraph>
        :Field marker is missing its close-colon.
    <field_list>
        <field>
            <field_name>
                Field: names: with: colons:
            <field_body>
                <paragraph>
                    are possible.
        <field>
            <field_name>
                \\Field names with backslashes\\
            <field_body>
                <paragraph>
                    are possible, too.
        <field>
            <field_name>
                \\
            <field_body>
                <paragraph>
                    A backslash.
    <paragraph>
        :Not a\\: field list.
    <paragraph>
        :Not a : field list either.
    <paragraph>
        :: Not a field list either.
    <definition_list>
        <definition_list_item>
            <term>
                ::
            <definition>
                <paragraph>
                    A definition list, not a field list.
"""],
[r"""
:first: field
:field:name:with:embedded:colons: unambiguous, no need for escapes

..

:embedded:colons: in first field name
:field:\`:name: not interpreted text
:field:\`name: not interpreted text
""",
"""\
<document source="test data">
    <field_list>
        <field>
            <field_name>
                first
            <field_body>
                <paragraph>
                    field
        <field>
            <field_name>
                field:name:with:embedded:colons
            <field_body>
                <paragraph>
                    unambiguous, no need for escapes
    <comment xml:space="preserve">
    <field_list>
        <field>
            <field_name>
                embedded:colons
            <field_body>
                <paragraph>
                    in first field name
        <field>
            <field_name>
                field:`:name
            <field_body>
                <paragraph>
                    not interpreted text
        <field>
            <field_name>
                field:`name
            <field_body>
                <paragraph>
                    not interpreted text
"""],
[r"""
Edge cases involving embedded colons and interpreted text.

Recognized as field list items:

:field\:`name`: interpreted text (standard role) requires
                escaping a leading colon in a field name

:field:name: unambiguous, no need for escapes

:field::name: double colons are OK, too

:field:\`name`: not interpreted text

:`field name`:code:: interpreted text with role in the field name
                     works only when the role follows the text

:a `complex`:code:\  field name: field body

Not recognized as field list items:

::code:`not a field name`: paragraph with interpreted text

:code:`not a field name`: paragraph with interpreted text
""",
"""\
<document source="test data">
    <paragraph>
        Edge cases involving embedded colons and interpreted text.
    <paragraph>
        Recognized as field list items:
    <field_list>
        <field>
            <field_name>
                field:
                <title_reference>
                    name
            <field_body>
                <paragraph>
                    interpreted text (standard role) requires
                    escaping a leading colon in a field name
        <field>
            <field_name>
                field:name
            <field_body>
                <paragraph>
                    unambiguous, no need for escapes
        <field>
            <field_name>
                field::name
            <field_body>
                <paragraph>
                    double colons are OK, too
        <field>
            <field_name>
                field:`name`
            <field_body>
                <paragraph>
                    not interpreted text
        <field>
            <field_name>
                <literal classes="code">
                    field name
            <field_body>
                <paragraph>
                    interpreted text with role in the field name
                    works only when the role follows the text
        <field>
            <field_name>
                a \n\
                <literal classes="code">
                    complex
                 field name
            <field_body>
                <paragraph>
                    field body
    <paragraph>
        Not recognized as field list items:
    <paragraph>
        :
        <literal classes="code">
            not a field name
        : paragraph with interpreted text
    <paragraph>
        <literal classes="code">
            not a field name
        : paragraph with interpreted text
"""],
]

if __name__ == '__main__':
    unittest.main()
