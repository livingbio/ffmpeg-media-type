import typer

from ffmpeg_media_type.utils.cache import save

from .utils.ffmpeg import list_support_format

app = typer.Typer()


@app.command()
def generate(cmds: list[str] = ["ffmpeg"]) -> None:
    """

    Generate cache for supported formats by ffmpeg and save it to cache directory.

    Args:
        cmds: Defaults to ["ffmpeg"].
    """
    for support_info in list_support_format(cmds):
        save(support_info, support_info.codec)


if __name__ == "__main__":
    app()
