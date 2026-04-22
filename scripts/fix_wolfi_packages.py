#!/usr/bin/env python3
"""Fixup unmapped wolfi package names in migrated Dockerfiles."""

import re
import glob

# Package name corrections for wolfi
PACKAGE_FIXES = {
    # PHP 8.2 → php84
    r'\bphp8\.2-fpm\b': 'php84-fpm',
    r'\bphp8\.2-curl\b': 'php84-curl',
    r'\bphp8\.2-cli\b': 'php84',
    r'\bphp8\.2-mbstring\b': 'php84-mbstring',
    r'\bphp8\.2-xml\b': 'php84-xml',
    r'\bphp8\.2-intl\b': 'php84-intl',
    r'\bphp8\.2-gd\b': 'php84-gd',
    r'\bphp8\.2-mysql\b': 'php84-mysql',
    r'\bphp8\.2-pgsql\b': 'php84-pgsql',
    r'\bphp8\.2-redis\b': 'php84-redis',
    r'\bphp8\.2-opcache\b': 'php84-opcache',
    r'\bphp8\.2-zip\b': 'php84-zip',
    r'\bphp8\.2-json\b': 'php84-json',
    r'\bphp8\.2-apcu\b': 'php84-apcu',
    r'\bphp8\.2\b': 'php84',
    # PHP extension short names
    r'\bmbstring\b': 'php84-mbstring',
    r'\bxml\b': 'php84-xml',  # Only in apk context
    r'\bintl\b': 'php84-intl',  # Only in apk context
    r'\bmysql\b': 'php84-mysql',  # Only in apk context
    r'\bgd\b': 'php84-gd',  # Only in apk context
    r'\bpdo\b': 'php84-pdo',  # Only in apk context
    # Common utilities
    r'\btzdata\b': 'tzdata',
    r'\bopenssl\b': 'openssl',
    r'\bjson\b': 'json-c',
    r'\bglib\b': 'glib',
    r'\bpostfix\b': 'postfix',
    r'\biptables\b': 'iptables',
    r'\biproute2\b': 'iproute2',
    r'\bsssd\b': 'sssd',
    r'\bkrb5-libs\b': 'krb5-libs',
    r'\bkeyutils\b': 'keyutils',
    r'\blibcom-err\b': 'libcom_err',
    r'\bcyrus-sasl\b': 'cyrus-sasl',
    r'\bopenldap-libs\b': 'openldap-libs',
    r'\bpython3-lxml\b': 'py3-lxml',
    r'\bpython3-pip\b': 'py3-pip',
    r'\bpython3-setuptools\b': 'py3-setuptools',
    r'\bpython3-wheel\b': 'py3-wheel',
    r'\bpython3-venv\b': 'python3',
    r'\blibssl3\b': 'openssl-libs',
    r'\blibcurl4\b': 'curl',
    r'\blibffi7\b': 'libffi',
    r'\blibxml2\b': 'libxml2',
    r'\blibxslt1\b': 'libxslt',
    r'\blibjpeg62\b': 'libjpeg-turbo',
    r'\blibpng16\b': 'libpng',
    r'\bgnupg\b': 'gnupg',
    r'\bgpg\b': 'gnupg',
    r'\bdirmngr\b': 'gnupg',
    r'\bssl-cert\b': 'ca-certificates',
    r'\blibcap-ng\b': 'libcap',
    r'\blibpq5\b': 'postgresql-libs',
    r'\blibpq-dev\b': 'postgresql-dev',
    r'\bdefault-jre-headless\b': 'java-17-runtime',
    r'\bdefault-jdk-headless\b': 'java-17',
    r'\bopenjdk-11-jre-headless\b': 'java-11-runtime',
    r'\bopenjdk-17-jre-headless\b': 'java-17-runtime',
    r'\bredis-server\b': 'redis',
    r'\bvalkey-server\b': 'valkey',
    r'\bcargo\b': 'cargo',
    r'\brustc\b': 'rust',
    r'\bclang\b': 'clang',
    r'\bmake\b': 'make',
    r'\bbuild-essential\b': 'build-base',
    r'\bcmake\b': 'cmake',
    r'\bgcc\b': 'gcc',
    r'\bg\+\+\b': 'g++',
    r'\bpkg-config\b': 'pkgconf',
    r'\bgit-core\b': 'git',
    r'\bcron\b': 'busybox-suid',
    r'\blogrotate\b': 'logrotate',
    r'\bsupervisor\b': 'supervisor',
    r'\bapache2-utils\b': 'apache2',
    r'\bgnupg2\b': 'gnupg',
    r'\bfetchmail\b': 'fetchmail',
    r'\bprocps\b': 'procps',
    r'\butil-linux-extra\b': 'util-linux',
    r'\bbusybox\b': 'busybox',
    r'\bpython3-dev\b': 'python3-dev',
    r'\bpython3-pip\b': 'py3-pip',
    r'\bpython3-requests\b': 'py3-requests',
    r'\bffmpeg\b': 'ffmpeg',
    r'\bimagemagick\b': 'imagemagick',
    r'\bghostscript\b': 'ghostscript',
    r'\bpoppler-utils\b': 'poppler-utils',
    r'\bgraphviz\b': 'graphviz',
    r'\bvirtualenv\b': 'python3',
    r'\bsqlite3\b': 'sqlite-libs',
    r'\blibsqlite3-0\b': 'sqlite-libs',
    r'\bcurl\b': 'curl',
    r'\bwget\b': 'wget',
    r'\bca-certificates\b': 'ca-certificates',
}

# Patterns that indicate the line should be removed entirely (not packages)
REMOVE_PATTERNS = [
    r'\bapt-transport-https\b',
    r'\becho\b\s+(main|stable|test)',
    r'\bhttps\b://',  # URL fragments, not packages
    r'\bkeyserver\b',  # GPG keyserver operations
    r'\bapt-key\b',
    r'\bdirmngr\b',
]

count = 0
modified = 0

for df in sorted(glob.glob('images/*/Dockerfile')):
    content = open(df).read()
    
    # Only process wolfi-based images
    froms = re.findall(r'^FROM\s+(.+?)(?:\s+AS\s+\w+)?\s*$', content, re.MULTILINE)
    if not froms or 'wolfi' not in froms[-1]:
        continue
    
    original = content
    
    # Get final stage
    if len(froms) > 1:
        stages = re.split(r'(^FROM\s+.+$)', content, re.MULTILINE)
        final = stages[-1]
        prefix = ''.join(stages[:-1])
    else:
        prefix = ''
        final = content
    
    # Apply package name fixes
    for pattern, replacement in PACKAGE_FIXES.items():
        final = re.sub(pattern, replacement, final)
    
    # Remove lines that contain only non-package tokens
    lines = final.split('\n')
    cleaned = []
    for line in lines:
        # Skip lines that are RUN commands with only non-package content
        if re.match(r'^\s*RUN\s+', line):
            # Check if line has any actual package after cleaning
            stripped = line
            for rp in REMOVE_PATTERNS:
                stripped = re.sub(rp, '', stripped)
            # Check if anything resembling a package name remains
            remaining = re.sub(r'(RUN|apk\s+add|--no-cache|&&|\\|\|\|true|;|rm|-rf|/var|/tmp|/etc|/usr|update-ca-certificates)', '', stripped).strip()
            if not remaining or remaining.startswith('#'):
                continue  # Skip this RUN line entirely
        cleaned.append(line)
    final = '\n'.join(cleaned)
    
    # Clean up multiple blank lines
    final = re.sub(r'\n{3,}', '\n\n', final)
    
    content = prefix + final
    
    if content != original:
        with open(df, 'w') as f:
            f.write(content)
        modified += 1
    
    count += 1

print(f"Scanned: {count} wolfi-based Dockerfiles")
print(f"Modified: {modified}")
