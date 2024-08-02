import os
from pathlib import Path


class DirectoryReader:
    def __init__(
        self,
        root_dir,
        exclude_dirs,
        exclude_files,
        exclude_dirs_regex,
        exclude_files_regex,
    ):
        self.root_dir = Path(root_dir)
        self.exclude_dirs = exclude_dirs
        self.exclude_files = exclude_files
        self.exclude_dirs_regex = exclude_dirs_regex
        self.exclude_files_regex = exclude_files_regex

    def read_directory(self):
        return self._get_directory_structure(self.root_dir)

    def _get_directory_structure(self, directory):
        result = []
        items = sorted(directory.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))

        for i, item in enumerate(items):
            is_last = i == len(items) - 1
            prefix = "└── " if is_last else "├── "

            if item.is_dir():
                if self._should_process_directory(item):
                    result.append(f"{prefix}{item.name}/")
                    child_prefix = "    " if is_last else "│   "
                    result.extend(
                        [
                            f"{child_prefix}{child}"
                            for child in self._get_directory_structure(item)
                        ]
                    )
            else:
                if self._should_process_file(item):
                    result.append(f"{prefix}{item.name}")

        return result

    def _should_process_directory(self, dir_path):
        if self.exclude_dirs_regex:
            return not any(
                re.search(pattern.strip(), str(dir_path))
                for pattern in self.exclude_dirs
                if pattern.strip()
            )
        else:
            return not any(
                exclude_dir.strip() in dir_path.parts
                for exclude_dir in self.exclude_dirs
                if exclude_dir.strip()
            )

    def _should_process_file(self, file_path):
        if self.exclude_files_regex:
            return not any(
                re.search(pattern.strip(), file_path.name)
                for pattern in self.exclude_files
                if pattern.strip()
            )
        else:
            return file_path.name not in [
                exclude_file.strip()
                for exclude_file in self.exclude_files
                if exclude_file.strip()
            ]
