
"""merkury

Usage:
    merkury [options] <script_path>
    merkury [options] batch <dir_path>

Options:
    -h --help                       Show this screen.
    -p <count>, --parallel <count>  Parallel processes (if missing, cpu cores).
    -o <file>, --output <file>      Specify report file (if missing, <script_name>.<format>).
    -f <format>, --format <format>  Specify report format: html (default), md.
    -a <author>, --author <author>  Specify author (if missing, user name).
    -t <title>, --title <title>     Specify report title (if missing, script file name).
    -d, --timestamp                 Add timestamp to default report file name.
    -i, --no-input                  Hide input blocks in generated report.
    -c, --toc                       Generate Table of Contents.
    -l, --debug                     Print debug messages.
    -v, --version                   Show version and exit.

Source:
    https://github.com/ppatrzyk/merkury
"""

import logging
import multiprocessing
from .renderer import generate_report
from .runner_py import execute_python
from .utils import get_default_path, get_default_file_name, VERSION

from docopt import docopt
from os import getlogin
from pathlib import Path

FORMATS = ("html", "md", )

def get_report(path: Path, report_file_path: Path, template_data: dict) -> bool:
    if template_data.get("title") is None:
        template_data = {**template_data, "title": path.name}
    duration_ms, code = execute_python(path)
    template_data = {
        **template_data,
        "duration_ms": duration_ms,
        "file_name": path.name,
    }
    report = generate_report(code, template_data)
    with report_file_path.open("w") as out:
        out.write(report)
    logging.debug(f"Report written to {report_file_path}")
    return True

def main(argv=None):
    """
    Program entrypoint
    """
    args = docopt(__doc__, argv=argv, version=f"merkury v{VERSION}")
    if bool(args.get("--debug")):
        logging.basicConfig(level=logging.DEBUG)
    batch = bool(args.get("batch"))
    output_format = (args.get("--format") or "html").lower()
    assert output_format in FORMATS, f"Unknown format: {output_format}. Options: html, md"
    add_timestamp = bool(args.get("--timestamp"))
    template_data = {
        "output_format": output_format,
        "show_input_blocks": not bool(args.get("--no-input")),
        "toc": bool(args.get("--toc")),
        "author": (args.get("--author") or getlogin()),
        "title": args.get("--title"),
    }
    specified_output = args.get("--output")
    specified_output_is_dir = False
    if specified_output is not None:
        specified_output = Path(specified_output).resolve()
        if specified_output.exists():
            if specified_output.is_dir():
                specified_output_is_dir = True
        else:
            if specified_output.suffix.lower().strip(".") in FORMATS:
                specified_output.parent.mkdir(parents=True, exist_ok=True)
                specified_output.touch()
            else:
                specified_output_is_dir = True
                specified_output.mkdir(parents=True, exist_ok=True)
    if batch:
        path: Path = Path(args.get("<dir_path>")).resolve()
        assert path.is_dir(), f"directory must be passed in batch mode, got {path}"
        assert (specified_output is None) or (not specified_output.is_file()), "Cannot write to single file in batch mode, pass directory instead"
        sub_paths = tuple(found_path for found_path in path.rglob("*") if (found_path.is_file() and found_path.suffix.lower() == ".py"))
        if sub_paths:
            parallel = int(args.get("--parallel") or multiprocessing.cpu_count())
            with multiprocessing.Pool(processes=parallel) as pool:
                get_report_args = list()
                for sub_path in sub_paths:
                    if specified_output is None:
                        report_file_path = get_default_path(sub_path, output_format, add_timestamp)
                    else:
                        if specified_output_is_dir:
                            file_name = get_default_file_name(sub_path, output_format, add_timestamp)
                            report_file_path = Path(specified_output, file_name)
                        else:
                            report_file_path = specified_output # /dev/null etc cases
                    get_report_args.append(
                        (sub_path, report_file_path, template_data)
                    )
                pool.starmap(get_report, get_report_args)
        else:
            logging.warning(f"no python files found inside {path}")
    else:
        path: Path = Path(args.get("<script_path>")).resolve()
        assert path.is_file() and (path.suffix.lower() == ".py"), f"path {path} is not a python file"
        if specified_output is None:
            report_file_path = get_default_path(path, output_format, add_timestamp)
        else:
            if specified_output_is_dir:
                file_name = get_default_file_name(path, output_format, add_timestamp)
                report_file_path = Path(specified_output, file_name)
            else:
                report_file_path = specified_output # /dev/null etc cases
        get_report(path, report_file_path, template_data)
    return 0

if __name__ == "__main__":
    main()
