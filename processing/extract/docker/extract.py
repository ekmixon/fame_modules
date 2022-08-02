#!/usr/local/bin/python3
import os
import sys

try:
    import libarchive.public
except ImportError:
    raise Exception("Missing dependency: libarchive")

# Syntax:
# Arg1 : '--' (from Dockerfile)
# Arg2 : ACE file
# Arg3 : Maximum extracted files
# Arg4 : Maximum automatic analyzis

if len(sys.argv) != 5:
    raise Exception(f"Incorrect number of arguments ({len(sys.argv)})")

target = sys.argv[2]
maximum_extracted_files = int(sys.argv[3])
maximum_automatic_analyses = int(sys.argv[4])

password_candidates = [""]
entries = []

if os.path.exists("/data/passwords_candidates.txt"):
    with open("/data/passwords_candidates.txt", "r") as f:
        password_candidates.extend(line.strip() for line in f)
try:
    with libarchive.public.file_reader(target, passphrases=password_candidates) as ar:
        entries.extend(entry.pathname for entry in ar if entry.filetype.IFREG)
except libarchive.exception.ArchiveError:
    print("Cannot read archive content")

should_extract = len(entries) <= maximum_extracted_files
should_analyze = len(entries) <= maximum_automatic_analyses

if should_extract:
    try:
        with libarchive.public.file_reader(target, passphrases=password_candidates) as ar:
            for entry in ar:
                if entry.pathname == ".":
                    continue
                abspath = os.path.join('/data/output/', entry.pathname)
                if entry.filetype.IFDIR and not os.path.exists(abspath):
                    os.makedirs(abspath)
                elif entry.filetype.IFREG:
                    dirname = os.path.dirname(abspath)
                    if not os.path.exists(dirname):
                        os.makedirs(dirname)
                    with open(abspath, "wb") as o:
                        for block in entry.get_blocks():
                            o.write(block)
                    print(f"should_analyze: {abspath}")
    except libarchive.exception.ArchiveError:
        print("warning: Unable to extract the archive (password not known)")
    except ValueError:
        print("warning: Unable to extract the archive (password not known ?)")
    if not should_analyze:
        print(
            f"warning: Archive contains more than {maximum_automatic_analyses} files ({len(entries)}), so no analysis was automatically created."
        )

else:
    print(
        f"warning: Archive contains more than {maximum_extracted_files} files ({len(entries)}), so they were not extracted."
    )
