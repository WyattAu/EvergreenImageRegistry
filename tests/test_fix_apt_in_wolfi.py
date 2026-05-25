from scripts.fix_apt_in_wolfi import (
    classify_complexity,
    convert_packages,
    extract_apt_packages,
    find_last_from_line,
    needs_break_system_packages,
)


class TestFindLastFromLine:
    def test_single_from(self):
        lines = ["FROM scratch\n", "RUN echo hi\n"]
        assert find_last_from_line(lines) == 0

    def test_multistage(self):
        lines = ["FROM builder AS build\n", "RUN make\n", "FROM scratch\n", "COPY --from=build /out /\n"]
        assert find_last_from_line(lines) == 2

    def test_no_from(self):
        assert find_last_from_line(["# comment\n"]) == -1


class TestClassifyComplexity:
    def test_simple(self):
        assert classify_complexity("RUN apt-get update && apt-get install -y curl") == "simple"

    def test_purge_pattern(self):
        assert classify_complexity("RUN apt-get update && apt-get install -y curl && apt-get purge -y apt") == "purge_pattern"

    def test_complex_repo(self):
        text = "RUN apt-key adv --keyserver keyserver.ubuntu.com && echo deb http://repo > /etc/apt/sources.list && apt-get install -y pkg"
        assert classify_complexity(text) == "complex_repo"

    def test_multiple_updates(self):
        text = "RUN apt-get update && apt-get install -y curl && apt-get update && apt-get install -y wget"
        assert classify_complexity(text) == "complex_repo"


class TestExtractAptPackages:
    def test_basic_install(self):
        pkgs = extract_apt_packages("apt-get install -y curl wget git")
        assert "curl" in pkgs
        assert "wget" in pkgs
        assert "git" in pkgs

    def test_no_install_recommends(self):
        pkgs = extract_apt_packages("apt-get install -y --no-install-recommends curl")
        assert pkgs == ["curl"]

    def test_filters_flags(self):
        pkgs = extract_apt_packages("apt-get install -y -q curl")
        assert pkgs == ["curl"]


class TestConvertPackages:
    def test_known_packages(self):
        apk, unknown = convert_packages(["curl", "git", "bash"])
        assert "curl" in apk
        assert "git" in apk
        assert "bash" in apk
        assert unknown == []

    def test_unknown_packages(self):
        apk, unknown = convert_packages(["curl", "totally-unknown-pkg"])
        assert apk == ["curl"]
        assert unknown == ["totally-unknown-pkg"]

    def test_mapping_applied(self):
        apk, _ = convert_packages(["python3-pip"])
        assert apk == ["py3-pip"]

    def test_deduplication(self):
        apk, _ = convert_packages(["gcc", "g++"])
        assert apk == ["build-base"]


class TestNeedsBreakSystemPackages:
    def test_adds_flag_to_pip(self):
        result = needs_break_system_packages("pip install requests")
        assert "--break-system-packages" in result

    def test_adds_flag_to_pip3(self):
        result = needs_break_system_packages("pip3 install requests")
        assert "--break-system-packages" in result

    def test_already_present(self):
        cmd = "pip install --break-system-packages requests"
        assert needs_break_system_packages(cmd) == cmd

    def test_non_pip_unchanged(self):
        cmd = "npm install express"
        assert needs_break_system_packages(cmd) == cmd
