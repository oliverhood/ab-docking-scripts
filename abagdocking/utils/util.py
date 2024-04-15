import time
import shutil
import tempfile
import contextlib
import subprocess
from typing import List
from loguru import logger
from typing import Optional


def call_script(
    cmd_list: List[str], stdout=None, stderr=None, decode: str = None, **kwargs
):
    stdout = stdout or subprocess.PIPE
    stderr = stderr or subprocess.PIPE
    decode = decode or "utf-8"
    # run
    process = subprocess.Popen(args=cmd_list, stdout=stdout, stderr=stderr, **kwargs)
    # post-processing
    stdout, stderr = process.communicate()
    retcode = process.wait()
    if decode:
        if stdout:
            stdout = stdout.decode(decode)
        if stderr:
            stderr = stderr.decode(decode)
    # if retcode is not 0, raise an exception
    if retcode != 0:
        logger.error(f"Error running command: {cmd_list}, error info:\n{stderr}")
        raise subprocess.CalledProcessError(retcode, cmd_list)

    return {
        "stdout": stdout,
        "stderr": stderr,
        "retcode": retcode,
        "metadata": {"cmd": cmd_list},
    }


@contextlib.contextmanager
def tmpdir_manager(base_dir: Optional[str] = None):
    """Context manager that deletes a temporary directory on exit."""
    tmpdir = tempfile.mkdtemp(dir=base_dir)
    try:
        yield tmpdir
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


@contextlib.contextmanager
def timing_context(msg: str):
    logger.info(f"Started {msg}")
    tic = time.time()
    yield
    toc = time.time()
    elapsed_time = toc - tic
    hours = int(elapsed_time // 3600)
    minutes = int((elapsed_time % 3600) // 60)
    seconds = int(elapsed_time % 60)
    logger.info(f"Finished {msg} in {hours} hours, {minutes} minutes, {seconds} seconds")
