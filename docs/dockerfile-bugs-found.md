RUN wget https://.../v${VERSION}/...   # REMOVED; double v
RUN wget https://.../${VERSION}/...   # CORRECT; v already in VERSION
`v${VERSION` or `vv` in URLs; these are almost always bugs.