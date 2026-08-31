"""merkury

Usage:
    merkury [options] <script_path>
    merkury [options] batch <dir_path>
    merkury [options] server <dir_path>

Options:
    -h --help                         Show this screen.
    -o <file>, --output <file>        Specify report file (if missing, <script_name>.<format>).
    -f <format>, --format <format>    Specify report format: html (default), md.
    -a <author>, --author <author>    Specify author (if missing, user name).
    -t <title>, --title <title>       Specify report title (if missing, script file name).
    -p <count>, --parallel <count>    Parallel processes (if missing, cpu cores).
    -s <address>, --server <address>  Server address (if missing, localhost:8000).
    -d, --timestamp                   Add timestamp to default report file name.
    -i, --no-input                    Hide input blocks in generated report.
    -c, --toc                         Generate Table of Contents.
    -l, --debug                       Print debug messages.
    -v, --version                     Show version and exit.

Source:
    https://github.com/ppatrzyk/merkury
"""

import logging
import multiprocessing
from os import getlogin
from pathlib import Path

from docopt import docopt

from .runner_py import get_report
from .server import run_server
from .utils import (
    FORMATS,
    VERSION,
    get_python_files,
    get_report_path,
    process_output_path,
)

logger = logging.getLogger(__name__)


def main(argv=None):
    """
    Program entrypoint
    """
    args = docopt(__doc__, argv=argv, version=f"merkury v{VERSION}")
    if bool(args.get("--debug")):
        logging.basicConfig(level=logging.DEBUG)
    output_format = (args.get("--format") or "html").lower()
    assert output_format in FORMATS, (
        f"Unknown format: {output_format}. Options: html, md"
    )
    add_timestamp = bool(args.get("--timestamp"))
    template_data = {
        "output_format": output_format,
        "show_input_blocks": not bool(args.get("--no-input")),
        "toc": bool(args.get("--toc")),
        "author": (args.get("--author") or getlogin()),
        "title": args.get("--title"),
    }
    specified_output = process_output_path(args.get("--output"))
    batch = bool(args.get("batch"))
    server = bool(args.get("server"))
    if batch or server:
        path: Path = Path(args.get("<dir_path>")).resolve()
        assert path.is_dir(), (
            f"directory must be passed in batch/server mode, got {path}"
        )
        assert (specified_output is None) or (not specified_output.is_file()), (
            "Cannot write to single file in batch/server mode, pass directory instead"
        )
    else:
        path: Path = Path(args.get("<script_path>")).resolve()
        assert path.is_file() and (path.suffix.lower() == ".py"), (
            f"path {path} is not a python file"
        )
    # execution
    if batch:
        sub_paths = get_python_files(path)
        if sub_paths:
            parallel = int(args.get("--parallel") or multiprocessing.cpu_count())
            with multiprocessing.Pool(processes=parallel) as pool:
                get_report_args = []
                for sub_path in sub_paths:
                    report_file_path = get_report_path(
                        sub_path, specified_output, output_format, add_timestamp
                    )
                    get_report_args.append((sub_path, report_file_path, template_data))
                pool.starmap(get_report, get_report_args)
        else:
            logger.warning(f"no python files found inside {path}")
    elif server:
        assert output_format == "html", "Server can output html only"
        server_raw = args.get("--server") or "localhost:8000"
        server_host, server_port = server_raw.strip().split(":")
        sub_paths = get_python_files(path)
        if sub_paths:
            assert len(sub_paths) == len({sub_path.name for sub_path in sub_paths}), (
                "duplicate file names not allowed in server mode"
            )
            run_server(
                server_host,
                int(server_port),
                sub_paths,
                specified_output,
                template_data,
            )
        else:
            logger.warning(f"no python files found inside {path}")
    else:
        report_file_path = get_report_path(
            path, specified_output, output_format, add_timestamp
        )
        get_report(path, report_file_path, template_data)
    return 0


if __name__ == "__main__":
    main()
