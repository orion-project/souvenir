# souvenir

Set of small unrelated tools for different routine tasks

## `compare_dirs.py` 

This tool compares two directories and issues a list of files which are contained in the one directory but not in the other. The first directory is the source containing original files. The second directory is the target (backup), to that files should be placed if they arer not in, or removed if they are not in the source.

The tool doesn't perform any modify operation. It doesn't move or copy any files. It only reads directories and optionally can generate commands those should be run manually to bring directories in sync.
