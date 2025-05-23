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

from typing import MutableSequence

import proto  # type: ignore

from google.ads.googleads.v18.enums.types import matching_function_context_type
from google.ads.googleads.v18.enums.types import matching_function_operator


__protobuf__ = proto.module(
    package="google.ads.googleads.v18.common",
    marshal="google.ads.googleads.v18",
    manifest={
        "MatchingFunction",
        "Operand",
    },
)


class MatchingFunction(proto.Message):
    r"""Matching function associated with a
    CustomerFeed, CampaignFeed, or AdGroupFeed. The matching
    function is used to filter the set of feed items selected.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        function_string (str):
            String representation of the Function.

            Examples:

            1. IDENTITY(true) or IDENTITY(false). All or no feed items
               served.
            2. EQUALS(CONTEXT.DEVICE,"Mobile")
            3. IN(FEED_ITEM_ID,{1000001,1000002,1000003})
            4. CONTAINS_ANY(FeedAttribute[12345678,0],{"Mars
               cruise","Venus cruise"})
            5. AND(IN(FEED_ITEM_ID,{10001,10002}),EQUALS(CONTEXT.DEVICE,"Mobile"))

            For more details, visit
            https://developers.google.com/google-ads/api/docs/extensions/feeds/matching-functions

            Note that because multiple strings may represent the same
            underlying function (whitespace and single versus double
            quotation marks, for example), the value returned may not be
            identical to the string sent in a mutate request.

            This field is a member of `oneof`_ ``_function_string``.
        operator (google.ads.googleads.v18.enums.types.MatchingFunctionOperatorEnum.MatchingFunctionOperator):
            Operator for a function.
        left_operands (MutableSequence[google.ads.googleads.v18.common.types.Operand]):
            The operands on the left hand side of the
            equation. This is also the operand to be used
            for single operand expressions such as NOT.
        right_operands (MutableSequence[google.ads.googleads.v18.common.types.Operand]):
            The operands on the right hand side of the
            equation.
    """

    function_string: str = proto.Field(
        proto.STRING,
        number=5,
        optional=True,
    )
    operator: (
        matching_function_operator.MatchingFunctionOperatorEnum.MatchingFunctionOperator
    ) = proto.Field(
        proto.ENUM,
        number=4,
        enum=matching_function_operator.MatchingFunctionOperatorEnum.MatchingFunctionOperator,
    )
    left_operands: MutableSequence["Operand"] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="Operand",
    )
    right_operands: MutableSequence["Operand"] = proto.RepeatedField(
        proto.MESSAGE,
        number=3,
        message="Operand",
    )


class Operand(proto.Message):
    r"""An operand in a matching function.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        constant_operand (google.ads.googleads.v18.common.types.Operand.ConstantOperand):
            A constant operand in a matching function.

            This field is a member of `oneof`_ ``function_argument_operand``.
        feed_attribute_operand (google.ads.googleads.v18.common.types.Operand.FeedAttributeOperand):
            This operand specifies a feed attribute in
            feed.

            This field is a member of `oneof`_ ``function_argument_operand``.
        function_operand (google.ads.googleads.v18.common.types.Operand.FunctionOperand):
            A function operand in a matching function.
            Used to represent nested functions.

            This field is a member of `oneof`_ ``function_argument_operand``.
        request_context_operand (google.ads.googleads.v18.common.types.Operand.RequestContextOperand):
            An operand in a function referring to a value
            in the request context.

            This field is a member of `oneof`_ ``function_argument_operand``.
    """

    class ConstantOperand(proto.Message):
        r"""A constant operand in a matching function.

        This message has `oneof`_ fields (mutually exclusive fields).
        For each oneof, at most one member field can be set at the same time.
        Setting any member of the oneof automatically clears all other
        members.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            string_value (str):
                String value of the operand if it is a string
                type.

                This field is a member of `oneof`_ ``constant_operand_value``.
            long_value (int):
                Int64 value of the operand if it is a int64
                type.

                This field is a member of `oneof`_ ``constant_operand_value``.
            boolean_value (bool):
                Boolean value of the operand if it is a
                boolean type.

                This field is a member of `oneof`_ ``constant_operand_value``.
            double_value (float):
                Double value of the operand if it is a double
                type.

                This field is a member of `oneof`_ ``constant_operand_value``.
        """

        string_value: str = proto.Field(
            proto.STRING,
            number=5,
            oneof="constant_operand_value",
        )
        long_value: int = proto.Field(
            proto.INT64,
            number=6,
            oneof="constant_operand_value",
        )
        boolean_value: bool = proto.Field(
            proto.BOOL,
            number=7,
            oneof="constant_operand_value",
        )
        double_value: float = proto.Field(
            proto.DOUBLE,
            number=8,
            oneof="constant_operand_value",
        )

    class FeedAttributeOperand(proto.Message):
        r"""A feed attribute operand in a matching function.
        Used to represent a feed attribute in feed.


        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            feed_id (int):
                The associated feed. Required.

                This field is a member of `oneof`_ ``_feed_id``.
            feed_attribute_id (int):
                Id of the referenced feed attribute.
                Required.

                This field is a member of `oneof`_ ``_feed_attribute_id``.
        """

        feed_id: int = proto.Field(
            proto.INT64,
            number=3,
            optional=True,
        )
        feed_attribute_id: int = proto.Field(
            proto.INT64,
            number=4,
            optional=True,
        )

    class FunctionOperand(proto.Message):
        r"""A function operand in a matching function.
        Used to represent nested functions.

        Attributes:
            matching_function (google.ads.googleads.v18.common.types.MatchingFunction):
                The matching function held in this operand.
        """

        matching_function: "MatchingFunction" = proto.Field(
            proto.MESSAGE,
            number=1,
            message="MatchingFunction",
        )

    class RequestContextOperand(proto.Message):
        r"""An operand in a function referring to a value in the request
        context.

        Attributes:
            context_type (google.ads.googleads.v18.enums.types.MatchingFunctionContextTypeEnum.MatchingFunctionContextType):
                Type of value to be referred in the request
                context.
        """

        context_type: (
            matching_function_context_type.MatchingFunctionContextTypeEnum.MatchingFunctionContextType
        ) = proto.Field(
            proto.ENUM,
            number=1,
            enum=matching_function_context_type.MatchingFunctionContextTypeEnum.MatchingFunctionContextType,
        )

    constant_operand: ConstantOperand = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="function_argument_operand",
        message=ConstantOperand,
    )
    feed_attribute_operand: FeedAttributeOperand = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="function_argument_operand",
        message=FeedAttributeOperand,
    )
    function_operand: FunctionOperand = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="function_argument_operand",
        message=FunctionOperand,
    )
    request_context_operand: RequestContextOperand = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="function_argument_operand",
        message=RequestContextOperand,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
