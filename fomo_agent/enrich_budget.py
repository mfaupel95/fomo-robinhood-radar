"""Cooperative enrichment budget; the collector's independent 120s kill stays authoritative."""
from __future__ import annotations

import time
from contextvars import ContextVar
from typing import Any

import httpx

current: ContextVar[Any] = ContextVar('enrich_budget', default=None)


class Deadline(TimeoutError):
    pass


class EnrichBudget:
    def __init__(self, seconds: float = 90, *, clock=time.monotonic, sleep=time.sleep, persist=None):
        self.clock, self.sleep_fn = clock, sleep
        self.started = clock()
        self.deadline = self.started + min(90, max(0, seconds))
        self.persist = persist
        self.events = []

    def remaining(self):
        return max(0, self.deadline - self.clock())

    def check(self):
        if self.remaining() <= 0:
            raise Deadline('enrich deadline')

    def record(self, source, operation, outcome, **fields):
        self.events.append(dict(source=source, operation=operation, outcome=outcome,
                                elapsed_s=round(self.clock()-self.started, 3),
                                remaining_s=round(self.remaining(), 3), **fields))
        if self.persist:
            self.persist()

    def sleep(self, seconds):
        self.check()
        if seconds >= self.remaining():
            raise Deadline('enrich wait exceeds remaining budget')
        self.sleep_fn(seconds)
        self.check()

    def get(self, client, path, *, source, params=None):
        return self.request(client, 'GET', path, source=source, params=params or {})

    def post(self, client, path, *, json):
        return self.request(client, 'POST', path, source='rpc', json=json)

    def request(self, client, method, path, *, source, **kwargs):
        self.check()
        self.record(source, 'request', 'attempt')
        from .config import settings
        request_deadline = min(self.deadline, self.clock() + max(0.01, min(10, settings.enrich_request_budget_s)))
        def check_request():
            self.check()
            if self.clock() >= request_deadline:
                raise Deadline('enrich request deadline')
        try:
            # Each phase <=2s. Check every body chunk, including a trickling response.
            timeout = min(2.0, (request_deadline-self.clock())/4)
            with client.stream(method, path, timeout=timeout, **kwargs) as response:
                body = bytearray()
                for chunk in response.iter_bytes():
                    check_request()
                    body.extend(chunk)
                    if len(body) > 8_000_000:
                        raise ValueError('enrich response too large')
                check_request()
                result = httpx.Response(response.status_code, content=bytes(body),
                                        request=response.request)
            self.record(source, 'request', 'success' if result.is_success else f'http_{result.status_code}')
            return result
        except Exception as exc:
            self.record(source, 'request', 'deadline' if isinstance(exc, Deadline) else 'failure',
                        error_type=type(exc).__name__)
            raise

    def snapshot(self):
        return {'events': self.events, 'deadline_s': self.deadline-self.started,
                'failures': sum(e['outcome'] == 'failure' or e['outcome'].startswith('http_') for e in self.events),
                'attempts': sum(e['outcome'] == 'attempt' and e['operation'] == 'request' for e in self.events),
                'successes': sum(e['outcome'] == 'success' and e['operation'] == 'request' for e in self.events)}
