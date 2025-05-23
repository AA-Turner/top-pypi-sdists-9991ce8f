#! /usr/bin/env python3

# $Id: test_role.py 9425 2023-06-30 14:56:47Z milde $
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
Tests for misc.py "role" directive.
"""

from pathlib import Path
import sys
import unittest

if __name__ == '__main__':
    # prepend the "docutils root" to the Python library path
    # so we import the local `docutils` package.
    sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from docutils.frontend import get_default_settings
from docutils.parsers.rst import Parser, roles
from docutils.utils import new_document


class ParserTestCase(unittest.TestCase):
    def test_parser(self):
        parser = Parser()
        settings = get_default_settings(Parser)
        settings.warning_stream = ''
        for name, cases in totest.items():
            for casenum, (case_input, case_expected) in enumerate(cases):
                # Language-specific roles and roles added by the
                # "default-role" and "role" directives are currently stored
                # globally in the roles._roles dictionary.  This workaround
                # empties that dictionary.
                roles._roles = {}
                with self.subTest(id=f'totest[{name!r}][{casenum}]'):
                    document = new_document('test data', settings.copy())
                    parser.parse(case_input, document)
                    output = document.pformat()
                    self.assertEqual(case_expected, output)


totest = {}

totest['role'] = [
["""\
.. role:: custom
.. role:: special

:custom:`interpreted` and :special:`interpreted`
""",
"""\
<document source="test data">
    <paragraph>
        <inline classes="custom">
            interpreted
         and \n\
        <inline classes="special">
            interpreted
"""],
["""\
.. role:: custom
   :class: custom-class
.. role:: special
   :class: special-class

:custom:`interpreted` and :special:`interpreted`
""",
"""\
<document source="test data">
    <paragraph>
        <inline classes="custom-class">
            interpreted
         and \n\
        <inline classes="special-class">
            interpreted
"""],
["""\
Must define :custom:`interpreted` before using it.

.. role:: custom

Now that it's defined, :custom:`interpreted` works.
""",
"""\
<document source="test data">
    <paragraph>
        Must define \n\
        <problematic ids="problematic-1" refid="system-message-1">
            :custom:`interpreted`
         before using it.
    <system_message level="1" line="1" source="test data" type="INFO">
        <paragraph>
            No role entry for "custom" in module "docutils.parsers.rst.languages.en".
            Trying "custom" as canonical role name.
    <system_message backrefs="problematic-1" ids="system-message-1" level="3" line="1" source="test data" type="ERROR">
        <paragraph>
            Unknown interpreted text role "custom".
    <paragraph>
        Now that it's defined, \n\
        <inline classes="custom">
            interpreted
         works.
"""],
["""\
.. role:: custom(emphasis)

:custom:`text`
""",
"""\
<document source="test data">
    <paragraph>
        <emphasis classes="custom">
            text
"""],
["""\
.. role:: custom ( emphasis )

:custom:`text`
""",
"""\
<document source="test data">
    <paragraph>
        <emphasis classes="custom">
            text
"""],
["""\
.. role:: custom(emphasis)
   :class: special

:custom:`text`
""",
"""\
<document source="test data">
    <paragraph>
        <emphasis classes="special">
            text
"""],
["""\
.. role:: custom(unknown-role)
""",
"""\
<document source="test data">
    <system_message level="1" line="1" source="test data" type="INFO">
        <paragraph>
            No role entry for "unknown-role" in module "docutils.parsers.rst.languages.en".
            Trying "unknown-role" as canonical role name.
    <system_message level="3" line="1" source="test data" type="ERROR">
        <paragraph>
            Unknown interpreted text role "unknown-role".
        <literal_block xml:space="preserve">
            .. role:: custom(unknown-role)
"""],
["""\
.. role:: custom
   :class: 1
""",
"""\
<document source="test data">
    <system_message level="3" line="1" source="test data" type="ERROR">
        <paragraph>
            Error in "role" directive:
            invalid option value: (option: "class"; value: '1')
            cannot make "1" into a class name.
        <literal_block xml:space="preserve">
            .. role:: custom
               :class: 1
"""],
["""\
.. role:: 1
""",
"""\
<document source="test data">
    <system_message level="3" line="1" source="test data" type="ERROR">
        <paragraph>
            Invalid argument for "role" directive:
            cannot make "1" into a class name.
        <literal_block xml:space="preserve">
            .. role:: 1
"""],
["""\
.. role:: (error)
""",
"""\
<document source="test data">
    <system_message level="3" line="1" source="test data" type="ERROR">
        <paragraph>
            "role" directive arguments not valid role names: "(error)".
        <literal_block xml:space="preserve">
            .. role:: (error)
"""],
["""\
.. role::
""",
"""\
<document source="test data">
    <system_message level="3" line="1" source="test data" type="ERROR">
        <paragraph>
            "role" directive requires arguments on the first line.
        <literal_block xml:space="preserve">
            .. role::
"""],
["""\
Test
----

.. role:: fileref(emphasis)

Testing a :fileref:`role` in a nested parse.
""",
"""\
<document source="test data">
    <section ids="test" names="test">
        <title>
            Test
        <paragraph>
            Testing a \n\
            <emphasis classes="fileref">
                role
             in a nested parse.
"""],
["""\
.. role:: custom
.. role:: special

Empty :custom:`\\ ` and empty `\\ `:special:
""",
"""\
<document source="test data">
    <paragraph>
        Empty \n\
        <inline classes="custom">
         and empty \n\
        <inline classes="special">
"""],
["""\
.. role:: CaSiNg

Role names are :cAsInG:`case-insensitive`.
""",
"""\
<document source="test data">
    <paragraph>
        Role names are \n\
        <inline classes="casing">
            case-insensitive
        .
"""],
]

totest['raw_role'] = [
["""\
.. role:: html(raw)
   :format: html

Here's some :html:`<i>raw HTML data</i>`.
""",
"""\
<document source="test data">
    <paragraph>
        Here's some \n\
        <raw classes="html" format="html" xml:space="preserve">
            <i>raw HTML data</i>
        .
"""],
["""\
.. role:: itex(raw)
   :format: latex html

Here's some itex markup: :itex:`$x^\\infty$`.
""",
"""\
<document source="test data">
    <paragraph>
        Here's some itex markup: \n\
        <raw classes="itex" format="latex html" xml:space="preserve">
            $x^\\infty$
        .
"""],
["""\
Can't use the :raw:`role` directly.
""",
"""\
<document source="test data">
    <paragraph>
        Can't use the \n\
        <problematic ids="problematic-1" refid="system-message-1">
            :raw:`role`
         directly.
    <system_message backrefs="problematic-1" ids="system-message-1" level="3" line="1" source="test data" type="ERROR">
        <paragraph>
            No format (Writer name) is associated with this role: "raw".
            The "raw" role cannot be used directly.
            Instead, use the "role" directive to create a new role with an associated format.
"""],
]


if __name__ == '__main__':
    unittest.main()
