# -*- coding: utf-8 -*-
"""Core blessed Terminal() tests."""

# std imports
import io
import os
import sys
import math
import time
import platform
import warnings

# 3rd party
import pytest

# local
from blessed._compat import StringIO
from .accessories import TestTerminal, unicode_cap, as_subprocess
from .conftest import IS_WINDOWS

try:
    from unittest import mock
except ImportError:
    import mock


# reload was a built-in in PY2, then moved to imp in PY3, then moved to importlib in PY34
if sys.version_info[:2] >= (3, 4):
    from importlib import reload as reload_module
elif sys.version_info[0] >= 3:
    from imp import reload as reload_module  # pylint: disable=deprecated-module
else:
    reload_module = reload  # pylint: disable=undefined-variable  # noqa: F821


def test_export_only_Terminal():
    "Ensure only Terminal instance is exported for import * statements."
    import blessed
    assert blessed.__all__ == ('Terminal',)


def test_null_location(all_terms):
    """Make sure ``location()`` with no args just does position restoration."""
    @as_subprocess
    def child(kind):
        t = TestTerminal(stream=StringIO(), force_styling=True)
        with t.location():
            pass
        expected_output = u''.join(
            (unicode_cap('sc'), unicode_cap('rc')))
        assert (t.stream.getvalue() == expected_output)

    child(all_terms)


def test_location_to_move_xy(all_terms):
    """``location()`` and ``move_xy()`` receive complimentary arguments."""
    @as_subprocess
    def child(kind):
        buf = StringIO()
        t = TestTerminal(stream=buf, force_styling=True)
        x, y = 12, 34
        with t.location(y, x):
            xy_val_from_move_xy = t.move_xy(y, x)
            xy_val_from_location = buf.getvalue()[len(t.sc):]
            assert xy_val_from_move_xy == xy_val_from_location

    child(all_terms)


def test_yield_keypad():
    """Ensure ``keypad()`` writes keyboard_xmit and keyboard_local."""
    @as_subprocess
    def child(kind):
        # given,
        t = TestTerminal(stream=StringIO(), force_styling=True)
        expected_output = u''.join((t.smkx, t.rmkx))

        # exercise,
        with t.keypad():
            pass

        # verify.
        assert (t.stream.getvalue() == expected_output)

    child(kind='xterm')


def test_null_fileno():
    """Make sure ``Terminal`` works when ``fileno`` is ``None``."""
    @as_subprocess
    def child():
        # This simulates piping output to another program.
        out = StringIO()
        out.fileno = None
        t = TestTerminal(stream=out)
        assert (t.save == u'')

    child()


@pytest.mark.skipif(IS_WINDOWS, reason="requires more than 1 tty")
def test_number_of_colors_without_tty():
    """``number_of_colors`` should return 0 when there's no tty."""
    if 'COLORTERM' in os.environ:
        del os.environ['COLORTERM']

    @as_subprocess
    def child_256_nostyle():
        t = TestTerminal(stream=StringIO())
        assert (t.number_of_colors == 0)

    @as_subprocess
    def child_256_forcestyle():
        t = TestTerminal(stream=StringIO(), force_styling=True)
        assert (t.number_of_colors == 256)

    @as_subprocess
    def child_8_forcestyle():
        # 'ansi' on freebsd returns 0 colors. We use 'cons25', compatible with its kernel tty.c
        kind = 'cons25' if platform.system().lower() == 'freebsd' else 'ansi'
        t = TestTerminal(kind=kind, stream=StringIO(),
                         force_styling=True)
        assert (t.number_of_colors == 8)

    @as_subprocess
    def child_0_forcestyle():
        t = TestTerminal(kind='vt220', stream=StringIO(),
                         force_styling=True)
        assert (t.number_of_colors == 0)

    @as_subprocess
    def child_24bit_forcestyle_with_colorterm():
        os.environ['COLORTERM'] = 'truecolor'
        t = TestTerminal(kind='vt220', stream=StringIO(),
                         force_styling=True)
        assert (t.number_of_colors == 1 << 24)

    child_0_forcestyle()
    child_8_forcestyle()
    child_256_forcestyle()
    child_256_nostyle()


@pytest.mark.skipif(IS_WINDOWS, reason="requires more than 1 tty")
def test_number_of_colors_with_tty():
    """test ``number_of_colors`` 0, 8, and 256."""
    @as_subprocess
    def child_256():
        t = TestTerminal()
        assert (t.number_of_colors == 256)

    @as_subprocess
    def child_8():
        # 'ansi' on freebsd returns 0 colors. We use 'cons25', compatible with its kernel tty.c
        kind = 'cons25' if platform.system().lower() == 'freebsd' else 'ansi'
        t = TestTerminal(kind=kind)
        assert (t.number_of_colors == 8)

    @as_subprocess
    def child_0():
        t = TestTerminal(kind='vt220')
        assert (t.number_of_colors == 0)

    child_0()
    child_8()
    child_256()


def test_init_descriptor_always_initted(all_terms):
    """Test height and width with non-tty Terminals."""
    @as_subprocess
    def child(kind):
        t = TestTerminal(kind=kind, stream=StringIO())
        assert t._init_descriptor == sys.__stdout__.fileno()
        assert (isinstance(t.height, int))
        assert (isinstance(t.width, int))
        assert t.height == t._height_and_width()[0]
        assert t.width == t._height_and_width()[1]

    child(all_terms)


def test_force_styling_none(all_terms):
    """If ``force_styling=None`` is used, don't ever do styling."""
    @as_subprocess
    def child(kind):
        t = TestTerminal(kind=kind, force_styling=None)
        assert (t.save == '')
        assert (t.color(9) == '')
        assert (t.bold('oi') == 'oi')

    child(all_terms)


def test_setupterm_singleton_issue_33():
    """A warning is emitted if a new terminal ``kind`` is used per process."""
    @as_subprocess
    def child():
        warnings.filterwarnings("error", category=UserWarning)

        # instantiate first terminal, of type xterm-256color
        term = TestTerminal(force_styling=True)
        first_kind = term.kind
        next_kind = 'xterm'

        try:
            # a second instantiation raises UserWarning
            term = TestTerminal(kind=next_kind, force_styling=True)
        except UserWarning as err:
            assert (err.args[0].startswith(
                    'A terminal of kind "' + next_kind + '" has been requested')
                    ), err.args[0]
            assert ('a terminal of kind "' + first_kind + '" will '
                    'continue to be returned' in err.args[0]), err.args[0]
        else:
            # unless term is not a tty and setupterm() is not called
            assert not term.is_a_tty, 'Should have thrown exception'
        warnings.resetwarnings()

    child()


def test_setupterm_invalid_issue39():
    """A warning is emitted if TERM is invalid."""
    # https://bugzilla.mozilla.org/show_bug.cgi?id=878089
    #
    # if TERM is unset, defaults to 'unknown', which should
    # fail to lookup and emit a warning on *some* systems.
    # freebsd actually has a termcap entry for 'unknown'
    @as_subprocess
    def child():
        warnings.filterwarnings("error", category=UserWarning)

        try:
            term = TestTerminal(kind='unknown', force_styling=True)
        except UserWarning as err:
            assert err.args[0] in (
                "Failed to setupterm(kind='unknown'): "
                "setupterm: could not find terminal",
                "Failed to setupterm(kind='unknown'): "
                "Could not find terminal unknown",
            )
        else:
            if platform.system().lower() != 'freebsd':
                assert not term.is_a_tty and not term.does_styling, (
                    'Should have thrown exception')
        warnings.resetwarnings()

    child()


def test_setupterm_invalid_has_no_styling():
    """An unknown TERM type does not perform styling."""
    # https://bugzilla.mozilla.org/show_bug.cgi?id=878089

    # if TERM is unset, defaults to 'unknown', which should
    # fail to lookup and emit a warning, only.
    @as_subprocess
    def child():
        warnings.filterwarnings("ignore", category=UserWarning)

        term = TestTerminal(kind='xxXunknownXxx', force_styling=True)
        assert term.kind is None
        assert not term.does_styling
        assert term.number_of_colors == 0
        warnings.resetwarnings()

    child()


def test_python3_2_raises_exception(monkeypatch):
    """Test python version 3.0 through 3.2 raises an exception."""
    import blessed

    monkeypatch.setattr('sys.version_info', (3, 2, 2, 'final', 0))

    try:
        reload_module(blessed)
    except ImportError as err:
        assert err.args[0] == (
            'Blessed needs Python 3.2.3 or greater for Python 3 '
            'support due to http://bugs.python.org/issue10570.')
        monkeypatch.undo()
        reload_module(blessed)
    else:
        assert False, 'Exception should have been raised'


def test_without_dunder():
    """Ensure dunder does not remain in module (py2x InterruptedError test."""
    import blessed.terminal
    assert '_' not in dir(blessed.terminal)


def test_IOUnsupportedOperation():
    """Ensure stream that throws IOUnsupportedOperation results in non-tty."""
    @as_subprocess
    def child():

        def side_effect():
            raise io.UnsupportedOperation

        mock_stream = mock.Mock()
        mock_stream.fileno = side_effect

        term = TestTerminal(stream=mock_stream)
        assert term.stream == mock_stream
        assert not term.does_styling
        assert not term.is_a_tty
        assert term.number_of_colors == 0

    child()


@pytest.mark.skipif(IS_WINDOWS, reason="has process-wide side-effects")
def test_winsize_IOError_returns_environ():
    """When _winsize raises IOError, defaults from os.environ given."""
    @as_subprocess
    def child():
        def side_effect(fd):
            raise IOError

        term = TestTerminal()
        term._winsize = side_effect
        os.environ['COLUMNS'] = '1984'
        os.environ['LINES'] = '1888'
        assert term._height_and_width() == (1888, 1984, None, None)

    child()


def test_yield_fullscreen(all_terms):
    """Ensure ``fullscreen()`` writes enter_fullscreen and exit_fullscreen."""
    @as_subprocess
    def child(kind):
        t = TestTerminal(stream=StringIO(), force_styling=True)
        t.enter_fullscreen = u'BEGIN'
        t.exit_fullscreen = u'END'
        with t.fullscreen():
            pass
        expected_output = u''.join((t.enter_fullscreen, t.exit_fullscreen))
        assert (t.stream.getvalue() == expected_output)

    child(all_terms)


def test_yield_hidden_cursor(all_terms):
    """Ensure ``hidden_cursor()`` writes hide_cursor and normal_cursor."""
    @as_subprocess
    def child(kind):
        t = TestTerminal(stream=StringIO(), force_styling=True)
        t.hide_cursor = u'BEGIN'
        t.normal_cursor = u'END'
        with t.hidden_cursor():
            pass
        expected_output = u''.join((t.hide_cursor, t.normal_cursor))
        assert (t.stream.getvalue() == expected_output)

    child(all_terms)


@pytest.mark.skipif(IS_WINDOWS, reason="windows doesn't work like this")
def test_no_preferredencoding_fallback():
    """Ensure empty preferredencoding value defaults to ascii."""
    @as_subprocess
    def child():
        with mock.patch('locale.getpreferredencoding') as get_enc:
            get_enc.return_value = u''
            t = TestTerminal()
            assert t._encoding == 'UTF-8'

    child()


@pytest.mark.skipif(IS_WINDOWS, reason="requires fcntl")
def test_unknown_preferredencoding_warned_and_fallback():
    """Ensure a locale without a codec emits a warning."""
    @as_subprocess
    def child():
        with mock.patch('locale.getpreferredencoding') as get_enc:
            get_enc.return_value = '---unknown--encoding---'
            with pytest.warns(UserWarning, match=(
                    'LookupError: unknown encoding: ---unknown--encoding---, '
                    'defaulting to UTF-8 for keyboard.')):
                t = TestTerminal()
                assert t._encoding == 'UTF-8'

    child()


@pytest.mark.skipif(IS_WINDOWS, reason="requires fcntl")
def test_win32_missing_tty_modules(monkeypatch):
    """Ensure dummy exception is used when io is without UnsupportedOperation."""
    @as_subprocess
    def child():
        OLD_STYLE = False
        try:
            original_import = getattr(__builtins__, '__import__')
            OLD_STYLE = True
        except AttributeError:
            original_import = __builtins__['__import__']

        tty_modules = ('termios', 'fcntl', 'tty')

        def __import__(name, *args, **kwargs):  # pylint: disable=redefined-builtin
            if name in tty_modules:
                raise ImportError
            return original_import(name, *args, **kwargs)

        for module in tty_modules:
            sys.modules.pop(module, None)

        warnings.filterwarnings("error", category=UserWarning)
        try:
            if OLD_STYLE:
                __builtins__.__import__ = __import__
            else:
                __builtins__['__import__'] = __import__
            try:
                import blessed.terminal
                reload_module(blessed.terminal)
            except UserWarning as err:
                assert err.args[0] == blessed.terminal._MSG_NOSUPPORT

            warnings.filterwarnings("ignore", category=UserWarning)
            import blessed.terminal
            reload_module(blessed.terminal)
            assert not blessed.terminal.HAS_TTY
            term = blessed.terminal.Terminal('ansi')
            # https://en.wikipedia.org/wiki/VGA-compatible_text_mode
            # see section '#PC_common_text_modes'
            assert term.height == 25
            assert term.width == 80

        finally:
            if OLD_STYLE:
                setattr(__builtins__, '__import__', original_import)
            else:
                __builtins__['__import__'] = original_import
            warnings.resetwarnings()
            import blessed.terminal
            reload_module(blessed.terminal)

    child()


def test_time_left():
    """test '_time_left' routine returns correct positive delta difference."""
    from blessed.keyboard import _time_left

    # given stime =~ "10 seconds ago"
    stime = (time.time() - 10)

    # timeleft(now, 15s) = 5s remaining
    timeout = 15
    result = _time_left(stime=stime, timeout=timeout)

    # we expect roughly 4.999s remain
    assert math.ceil(result) == 5.0


def test_time_left_infinite_None():
    """keyboard '_time_left' routine returns None when given None."""
    from blessed.keyboard import _time_left
    assert _time_left(stime=time.time(), timeout=None) is None


@pytest.mark.skipif(IS_WINDOWS, reason="cant multiprocess")
def test_termcap_repr():
    """Ensure ``hidden_cursor()`` writes hide_cursor and normal_cursor."""

    given_ttype = 'vt220'
    given_capname = 'cursor_up'
    expected = [r"<Termcap cursor_up:'\x1b\\[A'>",
                r"<Termcap cursor_up:'\\\x1b\\[A'>",
                r"<Termcap cursor_up:u'\\\x1b\\[A'>"]

    @as_subprocess
    def child():
        import blessed
        term = blessed.Terminal(given_ttype)
        given = repr(term.caps[given_capname])
        assert given in expected

    child()
