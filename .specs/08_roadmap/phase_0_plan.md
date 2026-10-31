This is **shell form**; Docker wraps it as `/bin/sh -c "nginx -v"`. Since `FROM scratch` has no `/bin/sh`, this
`/nginx nginx -v`; which is wrong.
In shell form, this runs `python` with arguments `curl -s localhost:8080/api/status`. This is wrong; it should run