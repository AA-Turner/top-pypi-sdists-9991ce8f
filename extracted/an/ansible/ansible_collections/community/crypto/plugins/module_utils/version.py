# -*- coding: utf-8 -*-

# Copyright (c) 2021, Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

"""Provide version object to compare version numbers."""

from __future__ import absolute_import, division, print_function


__metaclass__ = type


# Once we drop support for Ansible 2.9, ansible-base 2.10, and ansible-core 2.11, we can
# remove the _version.py file, and replace the following import by
#
#     from ansible.module_utils.compat.version import LooseVersion

from ._version import LooseVersion  # noqa: F401, pylint: disable=unused-import
