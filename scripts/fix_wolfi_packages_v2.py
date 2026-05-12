#!/usr/bin/env python3
"""
Fix invalid wolfi package names across all Dockerfiles in EvergreenImageRegistry.

Categories:
  A: Debian-style lib packages → REMOVE (auto-resolved as deps in wolfi/alpine)
  B: Chainguard-specific naming → REMAP to wolfi naming
  C: Special cases requiring specific handling
"""

import glob
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
IMAGES_DIR = PROJECT_ROOT / "images"

CATEGORY_A_REMOVE = set(
    ["apt-transport-https", "chkrootkit", "cockpit", "cockpit-dashboard", "cockpit-storaged", "cockpit-system", "cockpit-ws", "conntrack", "courier-authlib", "courier-imap", "curl-openssl-dev", "cyrus-sasl2-bin", "default-php84-mysql-client", "default-php84-mysql-server", "dovecot-core", "dovecot-imapd", "dovecot-lmtpd", "dovecot-pop3d", "erlang-asn1", "erlang-base", "erlang-crypto", "erlang-eldap", "erlang-ftp", "erlang-inets", "erlang-mnesia", "erlang-os-mon", "erlang-parsetools", "erlang-public-key", "erlang-runtime-tools", "erlang-snmp", "erlang-ssl", "erlang-syntax-tools", "erlang-tftp", "erlang-tools", "erlang-xmerl", "fonts-liberation", "galera-4", "golang-go", "imagick", "imap", "java-17-runtime", "krb5-user", "ldap-utils", "libaio1", "libaio1t64", "libapache-dbi-perl", "libapache2-mod-perl2", "libapache2-mod-security2", "libasound2", "libasound2t64", "libass9", "libatk-bridge2.0-0", "libatk-bridge2.0-0t64", "libatk1.0-0", "libatspi2.0-0", "libavahi-compat-libdnssd1", "libboost-all1.74", "libboost-all1.74-dev", "libboost-filesystem1.74.0", "libboost-iostreams1.74.0", "libboost-program-options1.74.0", "libboost-system1.74.0", "libboost-thread1.74.0", "libcairo2", "libcgi-pm-perl", "libcjson4", "libcups2", "libdbd-pg-perl", "libdbi-perl", "libdbus-1-3", "libdrm2", "libedit2", "libelf1", "libevent-2.1-7", "libfdk-acct2", "libgbm1", "libgcc-s1", "libgeoip-dev", "libgeoip1", "libgl1", "libgmp10", "libgnutls30", "libgomp1", "libgrpc++1", "libgtk-3-0", "libgtk-3-0t64", "libhogweed6", "libice6", "libicu72", "libidn2-0", "libjpeg-turbo-turbo-dev", "libjson-c5", "libjson-perl", "liblua5.3-0", "libluajit-5.1-2", "liblzma5", "liblzo2-2", "libmariadb3", "libmecab2", "libmilter1.0.1", "libmnl0", "libmodsecurity3", "libmozjs-78-0", "libmp3lame0", "libmpfr6", "libncurses5", "libncurses6", "libnetfilter-conntrack3", "libnettle8", "libnspr4", "libnss3", "libnss3-tools", "libnuma1", "libodbc1", "libopenscap8", "libopus0", "libpam-sss", "libpam0g", "libpango-1.0-0", "libpcre3", "libpcre3-dev", "libpkcs11-helper1", "libprotobuf32", "libpython3.11", "libqscintilla2-qt5-15", "libqt5core5a", "libqt5core5t64", "libqt5gui5", "libqt5gui5t64", "libqt5network5t64", "libqt5svg5", "libqt5widgets5", "libqt5widgets5t64", "libqt6core6", "libqt6gui6", "libqt6multimedia6", "libqt6network6", "libqt6qml6", "libqt6quick6", "libqt6widgets6", "libre2-5", "libreadline8", "libsasl2-modules", "libseccomp2", "libsm6", "libsnappy1v5", "libsodium23", "libsqlcipher0", "libswt-gtk-4-java", "libtasn1-6", "libtemplate-perl", "libtheora0", "libusb-1.0-0", "libuv1", "libvorbis0a", "libvpx7", "libwebp7", "libwrap0", "libx11-6", "libx264-164", "libx265-199", "libxcb1", "libxcomposite1", "libxdamage1", "libxext6", "libxfixes3", "libxi6", "libxkbcommon0", "libxrandr2", "libxrender1", "libxss1", "libxtst6", "libxvidcore4", "libyajl-dev", "libyajl2", "libyaml-0-2", "libyaml-cpp0.7", "libyaml-dev", "libz1", "lsb-release", "mailutils", "mariadb-server", "mongodb-org", "mongodb-org-tools", "musl-dev", "nginx-light", "oddjob-mkhomedir", "openjdk-21-jre-headless", "openscap-utils", "openssl-libs", "postgrey", "ppp", "python3-minimal", "rkhunter", "ruby3.1", "scap-workbench", "slapd", "soap", "spamassassin", "spamc", "sssd", "sssd-tools", "syslog-ng-core", "temurin-21-jre-headless", "virtuoso-opensource", "virtuoso-opensource-7", "xz-utils", "zlib1g-dev"]
)

CATEGORY_B_REMAP = {
    "php84-php84-gd": "php-8.4-gd",
    "php84-php84-intl": "php-8.4-intl",
    "php84-php84-mbstring": "php-8.4-mbstring",
    "php84-php84-mysql": "php-8.4-mysql",
    "php84-php84-xml": "php-8.4-xml",
    "php84-bcmath": "php-8.4-bcmath",
    "php84-curl": "php-8.4-curl",
    "php84-fpm": "php-8.4-fpm",
    "php84-gd": "php-8.4-gd",
    "php84-intl": "php-8.4-intl",
    "php84-mbstring": "php-8.4-mbstring",
    "php84-mysql": "php-8.4-mysql",
    "php84-pdo": "php-8.4-pdo",
    "php84-pgsql": "php-8.4-pgsql",
    "php84-redis": "php-8.4-redis",
    "php84-sqlite-libs": "php-8.4-sqlite",
    "php84-xml": "php-8.4-xml",
    "php84-zip": "php-8.4-zip",
    "php84": "php-8.4",
}

CATEGORY_C_REMAP = {
    "redis": None,
    "postgresql-16-postgis-3": "postgis3",
    "postgresql-16-timescaledb": "timescaledb",
    "postgresql-libs": "libpq",
    "postgresql-client-17": "postgresql-client",
}


def parse_apk_add_blocks(lines):
    """
    Parse lines into logical blocks, joining multi-line 'apk add' commands.
    Returns list of (start_line_idx, end_line_idx, is_apk_add_block, full_text).
    """
    blocks = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.rstrip()

        if re.search(r"\brun\b", stripped, re.IGNORECASE) and "apk add" in stripped:
            start = i
            full = stripped
            while full.endswith("\\") and i + 1 < len(lines):
                i += 1
                next_stripped = lines[i].rstrip()
                full = full[:-1] + " " + next_stripped.lstrip()
            blocks.append((start, i, True, full))
        else:
            blocks.append((start := i, i, False, stripped))
        i += 1

    return blocks


def process_apk_add_line(full_text):
    """
    Process a single (joined) apk add line.
    Returns (new_text, removed_count, remapped_list, comments).
    """
    removed = 0
    remapped = []

    match = re.match(
        r"^(\s*RUN\s+apk\s+add\s+--no-cache\s+)(.*?)(\s*(?:\|\|.*)?|\s*#.*)?$",
        full_text,
        re.DOTALL,
    )
    if not match:
        return full_text, 0, [], []

    prefix = match.group(1)
    pkg_part = match.group(2).strip()
    suffix = match.group(3) or ""

    tokens = re.split(r"\s+", pkg_part)
    new_tokens = []
    comments = []

    for token in tokens:
        token_stripped = token.strip()
        if not token_stripped or token_stripped.startswith("#"):
            continue

        if token_stripped in CATEGORY_A_REMOVE:
            removed += 1
            continue

        if token_stripped in CATEGORY_B_REMAP:
            new_name = CATEGORY_B_REMAP[token_stripped]
            remapped.append((token_stripped, new_name))
            new_tokens.append(new_name)
            continue

        if token_stripped in CATEGORY_C_REMAP:
            new_name = CATEGORY_C_REMAP[token_stripped]
            if new_name is None:
                comments.append(
                    f"# NOTE: {token_stripped} server not available in wolfi; uses pre-compiled binary"
                )
                removed += 1
            else:
                remapped.append((token_stripped, new_name))
                new_tokens.append(new_name)
            continue

        new_tokens.append(token_stripped)

    deduped = []
    seen = set()
    for t in new_tokens:
        if t not in seen:
            deduped.append(t)
            seen.add(t)
    new_tokens = deduped

    if not new_tokens:
        return None, removed, remapped, comments

    new_pkg_part = " ".join(new_tokens)
    new_text = prefix + new_pkg_part + suffix

    return new_text, removed, remapped, comments


def process_dockerfile(filepath):
    """
    Process a single Dockerfile.
    Returns (modified, removed_count, remapped_list, comments, emptied_blocks_info).
    """
    with open(filepath) as f:
        original_lines = f.readlines()

    original_content = "".join(original_lines)
    lines = original_lines[:]

    blocks = parse_apk_add_blocks(lines)

    total_removed = 0
    all_remapped = []
    all_comments = []
    emptied_blocks = []
    modified = False

    line_replacements = {}

    for start_idx, end_idx, is_apk, full_text in blocks:
        if not is_apk:
            continue

        new_text, removed, remapped, comments = process_apk_add_line(full_text)

        if new_text is None:
            emptied_blocks.append((start_idx, end_idx, full_text))
            total_removed += removed
            all_remapped.extend(remapped)
            all_comments.extend(comments)
            line_replacements[(start_idx, end_idx)] = None
            modified = True
        elif removed > 0 or remapped or comments:
            total_removed += removed
            all_remapped.extend(remapped)
            all_comments.extend(comments)
            line_replacements[(start_idx, end_idx)] = new_text
            modified = True

    if not modified:
        return False, 0, [], [], []

    new_lines = []
    i = 0
    while i < len(lines):
        found = False
        for (s, e), replacement in line_replacements.items():
            if i == s:
                found = True
                if replacement is not None:
                    if s == e:
                        new_lines.append(lines[i].rstrip()[:0] + replacement + "\n")
                        indent_match = re.match(r"^(\s*)", lines[i])
                        indent = indent_match.group(1) if indent_match else ""
                        if all_comments:
                            for c in all_comments:
                                new_lines.append(f"{indent}{c}\n")
                    else:
                        indent_match = re.match(r"^(\s*)", lines[i])
                        indent = indent_match.group(1) if indent_match else ""
                        new_lines.append(f"{indent}{replacement}\n")
                        if all_comments:
                            for c in all_comments:
                                new_lines.append(f"{indent}{c}\n")
                i = e + 1
                break
        if not found:
            new_lines.append(lines[i])
            i += 1

    new_content = "".join(new_lines)

    if new_content != original_content:
        with open(filepath, "w") as f:
            f.write(new_content)
        return True, total_removed, all_remapped, all_comments, emptied_blocks

    return False, 0, [], [], []


def main():
    dockerfiles = sorted(glob.glob(str(IMAGES_DIR / "*/Dockerfile")))

    if not dockerfiles:
        print("No Dockerfiles found!")
        sys.exit(1)

    print(f"Found {len(dockerfiles)} Dockerfiles to process")

    total_modified = 0
    total_removed = 0
    total_remapped = 0
    all_remapped_details = defaultdict(list)
    all_unhandled = set()
    all_emptied = []

    for dfpath in dockerfiles:
        rel = os.path.relpath(dfpath, PROJECT_ROOT)
        modified, removed, remapped, comments, emptied = process_dockerfile(dfpath)
        if modified:
            total_modified += 1
            total_removed += removed
            total_remapped += len(remapped)
            for old, new in remapped:
                all_remapped_details[old].append(rel)
            if comments:
                for c in comments:
                    print(f"  {rel}: {c}")
            if emptied:
                for s, e, full in emptied:
                    all_emptied.append((rel, full.strip()[:120]))

    print(f"\n{'=' * 70}")
    print("SUMMARY")
    print(f"{'=' * 70}")
    print(f"Total Dockerfiles scanned: {len(dockerfiles)}")
    print(f"Total Dockerfiles modified: {total_modified}")
    print(f"Total packages removed (Category A + C): {total_removed}")
    print(f"Total packages remapped (Category B + C): {total_remapped}")

    if all_remapped_details:
        print("\nRemapping details:")
        for old_name in sorted(all_remapped_details.keys()):
            files = all_remapped_details[old_name]
            print(
                f"  {old_name} -> (see map) in {len(files)} file(s): {', '.join(files[:5])}{'...' if len(files) > 5 else ''}"
            )

    if all_emptied:
        print("\nDockerfiles where apk add became empty (RUN removed):")
        for rel, text in all_emptied:
            print(f"  {rel}: removed '{text}...'")
    else:
        print("\nNo Dockerfiles had empty apk add lines.")

    print("\nDone.")


if __name__ == "__main__":
    main()
