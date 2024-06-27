class FFmpegMediaTypeError(Exception):
    """
    Base class for exceptions in this module.
    """


class FFMpegMediaCorruptedError(FFmpegMediaTypeError):
    """
    Exception raised when the media file is corrupted.
    """
