# Httpd (ARCHIVED)

Archived 2026-09-08.

Reason: the auto-generated Dockerfile claimed "Source Type:
binary-download" but pointed `curl` at `https://github.com/httpd` — an
HTML page, not a release artifact. Apache httpd is compiled C (apr,
apr-util, pcre, expat) and cannot be delivered as a static binary drop
onto a scratch base, so no correct download-only Dockerfile exists for
this layout. The image would have built "successfully" while shipping
an HTML page as the daemon binary.

Not deployed anywhere in the SimpleInfrastructureStack.

To revive: rewrite as a debian-slim based image installing `apache2`
from apt, wrapped with the health shim.
