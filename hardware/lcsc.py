import argparse
import os
import shutil
import subprocess
import sys
from typing import List, Tuple


def resolve_python_executable(python_exec: str) -> str:
    python_exec = (python_exec or "").strip() or sys.executable
    expanded = os.path.expanduser(python_exec)
    is_path_like = os.path.sep in expanded or (os.path.altsep and os.path.altsep in expanded)

    if is_path_like:
        if os.path.exists(expanded):
            return expanded
        return ""

    found = shutil.which(expanded)
    return found or ""


def load_lcsc_ids(input_file: str) -> List[str]:
    ids: List[str] = []
    with open(input_file, "r", encoding="utf-8") as handle:
        for line in handle:
            item = line.strip()
            if not item or item.startswith("#"):
                continue
            ids.append(item)
    return ids


def run_command(cmd: List[str]) -> Tuple[int, str, str]:
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def ensure_easyeda2kicad(python_exec: str) -> Tuple[bool, str]:
    code, _, err = run_command([python_exec, "-m", "easyeda2kicad", "--help"])
    if code == 0:
        return True, ""

    # Most common failure: module is missing in this Python environment.
    hint = (
        "easyeda2kicad is not available for this Python interpreter.\n"
        f"Install it with:\n  {python_exec} -m pip install easyeda2kicad"
    )
    details = f"{hint}\n\nTool output:\n{err}" if err else hint
    return False, details


def convert_lcsc_ids(
    lcsc_ids: List[str],
    output_dir: str,
    python_exec: str,
    use_full: bool,
    overwrite: bool,
    stop_on_error: bool,
    dry_run: bool,
) -> int:
    failures: List[str] = []
    total = len(lcsc_ids)

    for idx, lcsc_id in enumerate(lcsc_ids, start=1):
        cmd = [
            python_exec,
            "-m",
            "easyeda2kicad",
        ]
        if use_full:
            cmd.append("--full")
        if overwrite:
            cmd.append("--overwrite")
        cmd.extend([f"--lcsc_id={lcsc_id}", f"--output={output_dir}"])

        print(f"[{idx}/{total}] {lcsc_id}")
        print("  Command:", " ".join(cmd))

        if dry_run:
            continue

        code, out, err = run_command(cmd)
        if code == 0:
            print("  OK")
            if out:
                print(out)
            continue

        print("  FAILED")
        if out:
            print("  stdout:")
            print(out)
        if err:
            print("  stderr:")
            print(err)

        failures.append(lcsc_id)
        if stop_on_error:
            break

    print()
    print("Summary")
    print(f"  Total IDs   : {total}")
    print(f"  Successes   : {total - len(failures)}")
    print(f"  Failures    : {len(failures)}")
    if failures:
        print("  Failed IDs  :", ", ".join(failures))
        return 1
    return 0


def run_easyeda2kicad_from_file(
    input_file: str,
    output_dir: str = "./lib/lcsc",
    python_exec: str = "",
    use_full: bool = True,
    overwrite: bool = False,
    stop_on_error: bool = False,
    dry_run: bool = False,
) -> int:
    script_dir = os.path.dirname(os.path.abspath(__file__))

    input_file = os.path.expanduser(input_file)
    output_dir = os.path.expanduser(output_dir)
    if not os.path.isabs(input_file):
        input_file = os.path.join(script_dir, input_file)
    if not os.path.isabs(output_dir):
        output_dir = os.path.join(script_dir, output_dir)

    input_file = os.path.abspath(input_file)
    output_dir = os.path.abspath(output_dir)

    if not os.path.isfile(input_file):
        print(f"Error: input file not found: {input_file}")
        return 2

    resolved_python = resolve_python_executable(python_exec)
    if not resolved_python:
        print(f"Error: Python executable not found: {python_exec or '(default)'}")
        print("Tip: pass --python with a full path to python.exe")
        return 3

    ok, message = ensure_easyeda2kicad(resolved_python)
    if not ok:
        print("Error:")
        print(message)
        return 4

    os.makedirs(output_dir, exist_ok=True)

    lcsc_ids = load_lcsc_ids(input_file)
    if not lcsc_ids:
        print("No LCSC IDs found (empty file or only comments).")
        return 0

    return convert_lcsc_ids(
        lcsc_ids=lcsc_ids,
        output_dir=output_dir,
        python_exec=resolved_python,
        use_full=use_full,
        overwrite=overwrite,
        stop_on_error=stop_on_error,
        dry_run=dry_run,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convert LCSC IDs from a text file into KiCad assets using easyeda2kicad."
    )
    parser.add_argument(
        "input_file",
        nargs="?",
        default="./lcsc.txt",
        help="Text file with one LCSC ID per line. Lines starting with # are ignored.",
    )
    parser.add_argument(
        "output_dir",
        nargs="?",
        default="./lib/lcsc",
        help="Output directory where KiCad files are written.",
    )
    parser.add_argument(
        "--python",
        dest="python_exec",
        default=sys.executable,
        help="Python executable to run easyeda2kicad (default: current interpreter).",
    )
    parser.add_argument(
        "--no-full",
        action="store_true",
        help="Do not pass --full to easyeda2kicad.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing symbol/footprint/3D files in output directory.",
    )
    parser.add_argument(
        "--stop-on-error",
        action="store_true",
        help="Stop at first failed LCSC ID.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print commands without executing them.",
    )
    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return run_easyeda2kicad_from_file(
        input_file=args.input_file,
        output_dir=args.output_dir,
        python_exec=args.python_exec,
        use_full=not args.no_full,
        overwrite=args.overwrite,
        stop_on_error=args.stop_on_error,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    raise SystemExit(main())