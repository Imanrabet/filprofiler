"""
Command-line tools. Because of LD_PRELOAD, it's actually a two stage setup:

1. Sets ups the necessary environment variables, and then execve() stage 2.
2. Run the actual profiler CLI script.
"""

import sys
from os import environ, execv
from os.path import abspath, dirname, join
from argparse import ArgumentParser
import runpy

from ._utils import library_path
from ._tracer import start_tracing, stop_tracing


def stage_1():
    """Setup environment variables, re-execute this script."""
    environ["RUST_BACKTRACE"] = "1"
    environ["PYTHONMALLOC"] = "malloc"
    environ["LD_PRELOAD"] = library_path("_filpreload")
    environ["FIL_API_LIBRARY"] = library_path("libpymemprofile_api")
    execv(sys.executable, [sys.argv[0], "-m", "filprofiler._script"] + sys.argv[1:])


def stage_2():
    """Main CLI interface. Presumes LD_PRELOAD etc. has been set by stage_1()."""
    usage = "fil-profile [-m module | path-to-py-script ] [arg] ..."
    parser = ArgumentParser(usage=usage)
    parser.add_argument(
        "-m",
        dest="module",
        action="store",
        help="Profile a module, equivalent to running with 'python -m <module>'",
        default="",
    )
    parser.add_argument("args", metavar="ARG", nargs="*")
    arguments = parser.parse_args()
    if arguments.module:
        # Not quite the same as what python -m does, but pretty close:
        sys.argv = [arguments.module] + arguments.args
        code = "run_module(module_name, run_name='__main__')"
        globals = {"run_module": runpy.run_module, "module_name": arguments.module}
    else:
        sys.argv = args = arguments.args
        script = args[0]
        # Make directory where script is importable:
        sys.path.insert(0, dirname(abspath(script)))
        with open(script, "rb") as script_file:
            code = compile(script_file.read(), script, "exec")
        globals = {
            "__file__": script,
            "__name__": "__main__",
            "__package__": None,
            "__cached__": None,
        }
    start_tracing()
    try:
        exec(code, globals, None)
    finally:
        stop_tracing()


if __name__ == "__main__":
    stage_2()
