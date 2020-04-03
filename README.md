[![Tests](https://github.com/openfinch/lyrical/workflows/Tests/badge.svg)](https://github.com/openfinch/lyrical/actions?workflow=Tests)
# Lyrical
## A lyrics corpus analysis tool

## Notes on Concurrency

### Musicbrainz

Initially I had intended to run the request-loop for recordings as a multi-worker concurrent process using the request_futures library, however I found during testing that the browse API for Musicbrainz is sufficiently performant, and their rate-limiting sufficiently strict, that it saved very little time (approx. 2 seconds). The screenshot below illustrates this problem (the first run is a single worker, the second run is with five; both on a large search):

![Concurrency](docs/img/pointless_concurrency.png)

I have opted to keep the futures-based code, and it's associated retry logic, in-place should we move to a higher rate limit. I am unable to find an effective way to speed this process up without breaking the Musicbrainz terms of use.

### Lyrics.ovh

We can see, that by adding the same concurrency logic to the Lyrics.ovh API request, we see a significant improvement:

**Batch size 1**

![Concurrency2](docs/img/not_concurrency.png)



**Batch size 10**

![Concurrency3](docs/img/not_pointless_concurrency.png)

This test was run with both a small corpus (`Sunn O)))`) and a larger corpus (`The Cure`). Batch size refers to the number of parallel workers processing requests concurrently.

## Ideas for Improvements
 - **MED** Move all presentation logic into a single module
 - **LOW** Add type annotations to tests/ and noxfile.py
 - **LOW** Add docstrings to test suite.
 - **LOW** Move to a string-table system for a11y.
