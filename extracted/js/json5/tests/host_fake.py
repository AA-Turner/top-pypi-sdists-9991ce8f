# Copyright 2014 Dirk Pranke. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import io


class FakeHost:
    python_interpreter = 'python'

    def __init__(self):
        self.stdin = io.StringIO()
        self.stdout = io.StringIO()
        self.stderr = io.StringIO()
        self.platform = 'linux2'
        self.sep = '/'
        self.dirs = set([])
        self.files = {}
        self.written_files = {}
        self.last_tmpdir = None
        self.current_tmpno = 0
        self.cwd = '/tmp'

    def abspath(self, *comps):
        relpath = self.join(*comps)
        if relpath.startswith('/'):
            return relpath
        return self.join(self.cwd, relpath)

    def chdir(self, *comps):  # pragma: no cover
        path = self.join(*comps)
        if not path.startswith('/'):
            path = self.join(self.cwd, path)
        self.cwd = path

    def dirname(self, path):
        return '/'.join(path.split('/')[:-1])

    def getcwd(self):
        return self.cwd

    def join(self, *comps):  # pragma: no cover
        p = ''
        for c in comps:
            if c in ('', '.'):
                continue
            if c.startswith('/'):
                p = c
            elif p:
                p += '/' + c
            else:
                p = c

        # Handle ./
        p = p.replace('/./', '/')

        # Handle ../
        while '/..' in p:
            comps = p.split('/')
            idx = comps.index('..')
            comps = comps[: idx - 1] + comps[idx + 1 :]
            p = '/'.join(comps)
        return p

    def maybe_mkdir(self, *comps):  # pragma: no cover
        path = self.abspath(self.join(*comps))
        if path not in self.dirs:
            self.dirs.add(path)

    # We use `dir` as an argument name to mirror tempfile.mkdtemp.
    # pylint: disable=redefined-builtin
    def mkdtemp(self, suffix='', prefix='tmp', dir=None, **_kwargs):
        if dir is None:
            dir = self.sep + '__im_tmp'
        else:  # pragma: no cover
            pass
        curno = self.current_tmpno
        self.current_tmpno += 1
        self.last_tmpdir = self.join(dir, f'{prefix}_{curno}_{suffix}')
        self.dirs.add(self.last_tmpdir)
        return self.last_tmpdir

    # pylint: enable=redefined-builtin

    def print(self, msg='', end='\n', file=None):
        file = file or self.stdout
        file.write(msg + end)
        file.flush()

    def read_text_file(self, *comps):
        return self._read(comps)

    def _read(self, comps):
        return self.files[self.abspath(*comps)]

    def remove(self, *comps):
        path = self.abspath(*comps)
        self.files[path] = None
        self.written_files[path] = None

    def rmtree(self, *comps):
        path = self.abspath(*comps)
        for f in self.files:
            if f.startswith(path):
                self.remove(f)
            else:  # pragma: no cover
                pass
        self.dirs.remove(path)

    def write_text_file(self, path, contents):
        self._write(path, contents)

    def _write(self, path, contents):
        full_path = self.abspath(path)
        self.maybe_mkdir(self.dirname(full_path))
        self.files[full_path] = contents
        self.written_files[full_path] = contents
