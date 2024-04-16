import os
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


# write a context function to change the working directory
@contextlib.contextmanager
def temporarily_change_dir(new_dir: str = None):
    """Context manager that changes the working directory temporarily."""
    old_dir = os.getcwd()
    new_dir = new_dir or old_dir
    os.chdir(new_dir)
    try:
        yield
    finally:
        os.chdir(old_dir)


@contextlib.contextmanager
def skip_if_output_exists(output_path: str):
    """
    Context manager that skips the block of code if the output file already exists.
    # Example usage
    output_path = 'path/to/your/output/file.txt'

    with skip_if_output_exists(output_path) as execute:
        if execute:
            # Place the code you want to skip if the output file exists here
            logger.info(f"Creating output file at {output_path}...")
            # Simulate creating a file
            with open(output_path, 'w') as f:
                f.write("Some data")
        else:
            # This else block is optional and can be omitted if not needed
            logger.info("Skipped file creation.")
    """
    if os.path.exists(output_path):
        logger.info(f"Output file {output_path} already exists, skipped.")
        yield False  # return False to indicate that the block of code is skipped
    else:
        yield True   # return True to indicate that the block of code is run