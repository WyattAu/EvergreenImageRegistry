# Varnish (ARCHIVED)

Archived 2026-09-08.

Reason: the auto-generated Dockerfile claimed "Source Type:
binary-download" but pointed `curl` at `https://github.com/varnish` —
an HTML page, not a release artifact. Varnish Cache is compiled C and
cannot be delivered as a static binary drop onto a scratch base, so no
correct download-only Dockerfile exists for this layout. The image
would have built "successfully" while shipping an HTML page as the
daemon binary.

Not deployed anywhere in the SimpleInfrastructureStack.

To revive: rewrite as a debian-slim based image installing `varnish`
from apt, wrapped with the health shim.
