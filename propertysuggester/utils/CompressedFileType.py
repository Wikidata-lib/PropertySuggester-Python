
import argparse
import gzip
import bz2


class CompressedFileType(argparse.FileType):
    """
    Helper class for argparse. Automatically creates gzip or bz2 reader/writer if a file ends with .gz or .bz2
    """
    def __call__(self, string):
        try:
            if string.endswith('.gz'):
                return gzip.open(string, self._mode)
            if string.endswith('.bz2'):
                return bz2.BZ2File(string, self._mode)
        except IOError as e:
            message = "can't open '%s': %s"
            raise argparse.ArgumentTypeError(message % (string, e))
        return super(CompressedFileType, self).__call__(string)