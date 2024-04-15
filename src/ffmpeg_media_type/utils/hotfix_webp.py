import subprocess

from .shell import call, create_temp_file_path


def check_webpmux_installed() -> str | None:
    try:
        # Attempt to run `webpmux -version` to check if webpmux is installed
        result = subprocess.run(["webpmux", "-version"], capture_output=True, text=True, check=True)
        # print("webpmux is installed. Version info:")
        # print(result.stdout)
        return result.stdout
    except subprocess.CalledProcessError as e:
        # The command was found, but it exited with an error
        # print("webpmux command failed:", e)
        return None
    except FileNotFoundError:
        # The command was not found
        # print("webpmux is not installed.")
        return None


def fix_animated_webp(uri: str) -> str:
    # HOTFIX: some webp files are not correctly handled by ffmpeg
    temp_uri = create_temp_file_path(".webp")
    webpmux_command = ["webpmux", "-get", "frame", "1", uri, "-o", temp_uri]
    call(webpmux_command)
    return temp_uri
