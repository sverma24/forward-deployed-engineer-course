# J13 practice: be a polite client of a flaky service

1. Write `call_with_retry(fn, attempts=4, base=0.5)`. It calls `fn()`. If `fn` raises `TemporaryError`,
   wait `base * 2**(try-1)` seconds plus a little random jitter, then try again. After the last try,
   raise the error. Any other error is raised straight away, because retrying won't help.
2. Write a `RateLimiter(per_second)` with `acquire()` that blocks just long enough that callers
   never make more than `per_second` calls in any one-second window.

Say why jitter matters, and which errors you'd never retry.
