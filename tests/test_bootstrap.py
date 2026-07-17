from pathlib import Path
import importlib.util
import json


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "bootstrap.py"
SPEC = importlib.util.spec_from_file_location("bootstrap", MODULE_PATH)
assert SPEC and SPEC.loader
bootstrap = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(bootstrap)


def test_manifest_pins_full_sha() -> None:
    manifest = bootstrap.load_manifest()
    revision = manifest["toolchain"]["revision"]
    assert bootstrap.FULL_SHA.fullmatch(revision)


def test_requirement_is_immutable() -> None:
    value = bootstrap.git_requirement("TakashiSasaki/agent-policy", "a" * 40)
    assert value.endswith("@" + "a" * 40)
    assert "@main" not in value


def test_manifest_is_json_compatible_yaml() -> None:
    path = Path(__file__).resolve().parents[1] / "bootstrap-manifest.yml"
    assert json.loads(path.read_text(encoding="utf-8"))["schema_version"] == 1
