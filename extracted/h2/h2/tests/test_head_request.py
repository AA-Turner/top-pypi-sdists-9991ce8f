from __future__ import annotations

import pytest

import h2.connection

EXAMPLE_REQUEST_HEADERS_BYTES = [
    (b":authority", b"example.com"),
    (b":path", b"/"),
    (b":scheme", b"https"),
    (b":method", b"HEAD"),
]

EXAMPLE_REQUEST_HEADERS = [
    (":authority", "example.com"),
    (":path", "/"),
    (":scheme", "https"),
    (":method", "HEAD"),
]


class TestHeadRequest:
    example_response_headers = [
        (b":status", b"200"),
        (b"server", b"fake-serv/0.1.0"),
        (b"content_length", b"1"),
    ]

    @pytest.mark.parametrize("headers", [EXAMPLE_REQUEST_HEADERS, EXAMPLE_REQUEST_HEADERS_BYTES])
    def test_non_zero_content_and_no_body(self, frame_factory, headers) -> None:
        c = h2.connection.H2Connection()
        c.initiate_connection()
        c.send_headers(1, headers, end_stream=True)

        f = frame_factory.build_headers_frame(
            self.example_response_headers,
            flags=["END_STREAM"],
        )
        events = c.receive_data(f.serialize())

        assert len(events) == 2
        event = events[0]

        assert isinstance(event, h2.events.ResponseReceived)
        assert event.stream_id == 1
        assert event.headers == self.example_response_headers

    @pytest.mark.parametrize("headers", [EXAMPLE_REQUEST_HEADERS, EXAMPLE_REQUEST_HEADERS_BYTES])
    def test_reject_non_zero_content_and_body(self, frame_factory, headers) -> None:
        c = h2.connection.H2Connection()
        c.initiate_connection()
        c.send_headers(1, headers)

        headers = frame_factory.build_headers_frame(
            self.example_response_headers,
        )
        data = frame_factory.build_data_frame(data=b"\x01")

        c.receive_data(headers.serialize())
        with pytest.raises(h2.exceptions.InvalidBodyLengthError):
            c.receive_data(data.serialize())
