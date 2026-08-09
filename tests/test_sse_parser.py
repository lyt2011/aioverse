from __future__ import annotations

import json
import unittest
import asyncio

from aioverse.OpenAI import OpenAIClient
from aioverse.errors import SSEParseError
from aioverse.models import Request


class _Content:

    def __init__(self, chunks):
        self._chunks = chunks

    async def iter_chunked(self, _size):
        for chunk in self._chunks:
            yield chunk


class _Response:

    def __init__(self, chunks, *, status=200, text=""):
        self.content = _Content(chunks)
        self.status = status
        self._text = text

    async def text(self):
        return self._text


class _PostContext:

    def __init__(self, response):
        self.response = response
        self.closed = False

    async def __aenter__(self):
        return self.response

    async def __aexit__(self, *_args):
        self.closed = True


class _Session:

    def __init__(self, response):
        self.post_context = _PostContext(response)

    def post(self, **_kwargs):
        return self.post_context


def _chunk_json(content="answer"):
    return json.dumps({
        "id": "chunk-1",
        "created": 1,
        "model": "demo",
        "object": "chat.completion.chunk",
        "choices": [{
            "index": 0,
            "delta": {"content": content},
            "finish_reason": None,
        }],
    }, ensure_ascii=False)


async def _collect(client, response):
    return [chunk async for chunk in client._iter_sse_chunks(response)]


class SseParserTests(unittest.IsolatedAsyncioTestCase):

    async def test_parser_handles_multiline_data_and_done_event(self):
        data = _chunk_json("answer")
        prefix, choices = data.split('"choices":', 1)
        payload = (
            f"data: {prefix}\n"
            f"data: \"choices\":{choices}\n\n"
            "data: [DONE]\n\n"
        ).encode()

        chunks = await _collect(OpenAIClient(session=None), _Response([payload]))

        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0].choices[0].delta.content, "answer")

    async def test_parser_preserves_utf8_when_codepoint_is_split_between_chunks(self):
        payload = f"data: {_chunk_json(chr(0x4f60) + chr(0x597d))}\n\n".encode()
        split_at = payload.index(chr(0x4f60).encode()) + 1

        chunks = await _collect(
            OpenAIClient(session=None),
            _Response([payload[:split_at], payload[split_at:]]),
        )

        self.assertEqual(chunks[0].choices[0].delta.content, chr(0x4f60) + chr(0x597d))

    async def test_parser_processes_event_left_in_eof_buffer(self):
        payload = f"data: {_chunk_json('eof')}".encode()

        chunks = await _collect(OpenAIClient(session=None), _Response([payload]))

        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0].choices[0].delta.content, "eof")

    async def test_parser_raises_after_three_consecutive_invalid_events(self):
        payload = b"data: {bad}\n\ndata: {also bad}\n\ndata: {still bad}\n\n"

        with self.assertRaises(SSEParseError):
            await _collect(OpenAIClient(session=None), _Response([payload]))

    async def test_call_stream_applies_chunk_idle_timeout(self):
        class HangingContent:
            async def iter_chunked(self, _size):
                await asyncio.Event().wait()
                yield b""

        response = _Response([])
        response.content = HangingContent()
        session = _Session(response)
        client = OpenAIClient(session=session)
        request = Request(url="https://example.invalid")
        request.stream_idle_timeout = 0.01

        with self.assertRaises(asyncio.TimeoutError):
            async for _ in client.call_stream(request=request):
                pass

        self.assertTrue(session.post_context.closed)

    async def test_call_stream_preserves_json_error_body(self):
        response = _Response([], status=429, text='{"error":"rate limited"}')
        session = _Session(response)
        client = OpenAIClient(session=session)
        request = Request(url="https://example.invalid")

        with self.assertRaises(Exception) as context:
            async for _ in client.call_stream(request=request):
                pass

        self.assertEqual(context.exception.code, 429)
        self.assertEqual(context.exception.response, {"error": "rate limited"})


    async def test_call_stream_closes_response_when_explicitly_closed(self):
        payload = f"data: {_chunk_json('partial')}\n\n".encode()
        response = _Response([payload])
        session = _Session(response)
        client = OpenAIClient(session=session)
        request = Request(url="https://example.invalid")
        stream = client.call_stream(request=request)

        await anext(stream)
        self.assertFalse(session.post_context.closed)
        await stream.aclose()

        self.assertTrue(session.post_context.closed)


if __name__ == "__main__":
    unittest.main()
