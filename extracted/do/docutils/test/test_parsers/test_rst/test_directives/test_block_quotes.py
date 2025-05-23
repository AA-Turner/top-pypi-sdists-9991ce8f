#! /usr/bin/env python3

# $Id: test_block_quotes.py 9425 2023-06-30 14:56:47Z milde $
# Author: Lea Wiemann <LeWiemann@gmail.com>
# Copyright: This module has been placed in the public domain.

"""
Tests for the block quote directives "epigraph", "highlights", and
"pull-quote".
"""

from pathlib import Path
import sys
import unittest

if __name__ == '__main__':
    # prepend the "docutils root" to the Python library path
    # so we import the local `docutils` package.
    sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

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


generic_tests = [
["""\
.. %(type)s::

   This is a block quote.

   -- Attribution

   This is another block quote.

   -- Another Attribution,
      Second Line
""",
"""\
<document source="test data">
    <block_quote classes="%(type)s">
        <paragraph>
            This is a block quote.
        <attribution>
            Attribution
    <block_quote classes="%(type)s">
        <paragraph>
            This is another block quote.
        <attribution>
            Another Attribution,
            Second Line
"""],
# TODO: Add class option.
["""\
.. %(type)s::
""",
"""\
<document source="test data">
    <system_message level="3" line="1" source="test data" type="ERROR">
        <paragraph>
            Content block expected for the "%(type)s" directive; none found.
        <literal_block xml:space="preserve">
            .. %(type)s::
"""],
]

totest = {}
for block_quote_type in ('epigraph', 'highlights', 'pull-quote'):
    totest[block_quote_type] = [
        [text % {'type': block_quote_type} for text in pair]
        for pair in generic_tests]


if __name__ == '__main__':
    unittest.main()
