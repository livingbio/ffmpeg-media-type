import os
import shlex
import tempfile


def call(cmds: list[str]) -> str:
    command = " ".join(shlex.quote(part) for part in cmds)
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = f"{tmpdir}/output.txt"
        os.system(f"{command} > {output_path} 2>&1")

        with open(output_path) as ifile:
            return ifile.read()
