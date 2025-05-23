# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from __future__ import annotations


import proto  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v18.enums",
    marshal="google.ads.googleads.v18",
    manifest={
        "MessagePlaceholderFieldEnum",
    },
)


class MessagePlaceholderFieldEnum(proto.Message):
    r"""Values for Message placeholder fields."""

    class MessagePlaceholderField(proto.Enum):
        r"""Possible values for Message placeholder fields.

        Values:
            UNSPECIFIED (0):
                Not specified.
            UNKNOWN (1):
                Used for return value only. Represents value
                unknown in this version.
            BUSINESS_NAME (2):
                Data Type: STRING. The name of your business.
            COUNTRY_CODE (3):
                Data Type: STRING. Country code of phone
                number.
            PHONE_NUMBER (4):
                Data Type: STRING. A phone number that's
                capable of sending and receiving text messages.
            MESSAGE_EXTENSION_TEXT (5):
                Data Type: STRING. The text that will go in
                your click-to-message ad.
            MESSAGE_TEXT (6):
                Data Type: STRING. The message text
                automatically shows in people's messaging apps
                when they tap to send you a message.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        BUSINESS_NAME = 2
        COUNTRY_CODE = 3
        PHONE_NUMBER = 4
        MESSAGE_EXTENSION_TEXT = 5
        MESSAGE_TEXT = 6


__all__ = tuple(sorted(__protobuf__.manifest))
