# Copyright 2010 New Relic, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from newrelic.common.object_wrapper import function_wrapper, transient_function_wrapper


def validate_serverless_data(expected_methods=(), forgone_methods=()):
    @function_wrapper
    def _validate_wrapper(wrapped, instance, args, kwargs):
        payloads = []

        @transient_function_wrapper("newrelic.common.agent_http", "ServerlessModeClient.finalize")
        def _capture(wrapped, instance, args, kwargs):
            payload = wrapped(*args, **kwargs)
            payloads.append(payload)
            return payload

        def _validate():
            assert payloads

            for payload in payloads:
                assert "metric_data" in payload

                for method in expected_methods:
                    assert method in payload

                    # Verify the method is not a byte string
                    assert isinstance(payload[method], (dict, list))

                for method in forgone_methods:
                    assert method not in payload

        capture_wrapped = _capture(wrapped)
        result = capture_wrapped(*args, **kwargs)
        _validate()
        return result

    return _validate_wrapper
