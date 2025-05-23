#! /usr/bin/env python3

# $Id: test_comments.py 9425 2023-06-30 14:56:47Z milde $
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

totest['comments'] = [
["""\
.. A comment

Paragraph.
""",
"""\
<document source="test data">
    <comment xml:space="preserve">
        A comment
    <paragraph>
        Paragraph.
"""],
["""\
.. A comment
   block.

Paragraph.
""",
"""\
<document source="test data">
    <comment xml:space="preserve">
        A comment
        block.
    <paragraph>
        Paragraph.
"""],
["""\
..
   A comment consisting of multiple lines
   starting on the line after the
   explicit markup start.
""",
"""\
<document source="test data">
    <comment xml:space="preserve">
        A comment consisting of multiple lines
        starting on the line after the
        explicit markup start.
"""],
["""\
.. A comment.
.. Another.

Paragraph.
""",
"""\
<document source="test data">
    <comment xml:space="preserve">
        A comment.
    <comment xml:space="preserve">
        Another.
    <paragraph>
        Paragraph.
"""],
["""\
.. A comment
no blank line

Paragraph.
""",
"""\
<document source="test data">
    <comment xml:space="preserve">
        A comment
    <system_message level="2" line="2" source="test data" type="WARNING">
        <paragraph>
            Explicit markup ends without a blank line; unexpected unindent.
    <paragraph>
        no blank line
    <paragraph>
        Paragraph.
"""],
["""\
.. A comment.
.. Another.
no blank line

Paragraph.
""",
"""\
<document source="test data">
    <comment xml:space="preserve">
        A comment.
    <comment xml:space="preserve">
        Another.
    <system_message level="2" line="3" source="test data" type="WARNING">
        <paragraph>
            Explicit markup ends without a blank line; unexpected unindent.
    <paragraph>
        no blank line
    <paragraph>
        Paragraph.
"""],
["""\
.. A comment::

Paragraph.
""",
"""\
<document source="test data">
    <comment xml:space="preserve">
        A comment::
    <paragraph>
        Paragraph.
"""],
["""\
..
   comment::

The extra newline before the comment text prevents
the parser from recognizing a directive.
""",
"""\
<document source="test data">
    <comment xml:space="preserve">
        comment::
    <paragraph>
        The extra newline before the comment text prevents
        the parser from recognizing a directive.
"""],
["""\
..
   _comment: http://example.org

The extra newline before the comment text prevents
the parser from recognizing a hyperlink target.
""",
"""\
<document source="test data">
    <comment xml:space="preserve">
        _comment: http://example.org
    <paragraph>
        The extra newline before the comment text prevents
        the parser from recognizing a hyperlink target.
"""],
["""\
..
   [comment] Not a citation.

The extra newline before the comment text prevents
the parser from recognizing a citation.
""",
"""\
<document source="test data">
    <comment xml:space="preserve">
        [comment] Not a citation.
    <paragraph>
        The extra newline before the comment text prevents
        the parser from recognizing a citation.
"""],
["""\
..
   |comment| image:: bogus.png

The extra newline before the comment text prevents
the parser from recognizing a substitution definition.
""",
"""\
<document source="test data">
    <comment xml:space="preserve">
        |comment| image:: bogus.png
    <paragraph>
        The extra newline before the comment text prevents
        the parser from recognizing a substitution definition.
"""],
["""\
.. Next is an empty comment, which serves to end this comment and
   prevents the following block quote being swallowed up.

..

    A block quote.
""",
"""\
<document source="test data">
    <comment xml:space="preserve">
        Next is an empty comment, which serves to end this comment and
        prevents the following block quote being swallowed up.
    <comment xml:space="preserve">
    <block_quote>
        <paragraph>
            A block quote.
"""],
["""\
term 1
  definition 1

  .. a comment

term 2
  definition 2
""",
"""\
<document source="test data">
    <definition_list>
        <definition_list_item>
            <term>
                term 1
            <definition>
                <paragraph>
                    definition 1
                <comment xml:space="preserve">
                    a comment
        <definition_list_item>
            <term>
                term 2
            <definition>
                <paragraph>
                    definition 2
"""],
["""\
term 1
  definition 1

.. a comment

term 2
  definition 2
""",
"""\
<document source="test data">
    <definition_list>
        <definition_list_item>
            <term>
                term 1
            <definition>
                <paragraph>
                    definition 1
    <comment xml:space="preserve">
        a comment
    <definition_list>
        <definition_list_item>
            <term>
                term 2
            <definition>
                <paragraph>
                    definition 2
"""],
["""\
+ bullet paragraph 1

  bullet paragraph 2

  .. comment between bullet paragraphs 2 and 3

  bullet paragraph 3
""",
"""\
<document source="test data">
    <bullet_list bullet="+">
        <list_item>
            <paragraph>
                bullet paragraph 1
            <paragraph>
                bullet paragraph 2
            <comment xml:space="preserve">
                comment between bullet paragraphs 2 and 3
            <paragraph>
                bullet paragraph 3
"""],
["""\
+ bullet paragraph 1

  .. comment between bullet paragraphs 1 (leader) and 2

  bullet paragraph 2
""",
"""\
<document source="test data">
    <bullet_list bullet="+">
        <list_item>
            <paragraph>
                bullet paragraph 1
            <comment xml:space="preserve">
                comment between bullet paragraphs 1 (leader) and 2
            <paragraph>
                bullet paragraph 2
"""],
["""\
+ bullet

  .. trailing comment
""",
"""\
<document source="test data">
    <bullet_list bullet="+">
        <list_item>
            <paragraph>
                bullet
            <comment xml:space="preserve">
                trailing comment
"""],
]

if __name__ == '__main__':
    unittest.main()
