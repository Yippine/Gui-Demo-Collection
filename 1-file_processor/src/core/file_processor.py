import os
import re

class FileProcessor:
    def __init__(self):
        pass

    def process_files(self, project_dir, exclude_dirs, exclude_files, include_files, is_exclude_dirs_regex, is_exclude_files_regex, is_include_files_regex):
        result = []
        for root, dirs, files in os.walk(project_dir):
            # Apply directory exclusions
            dirs[:] = [d for d in dirs if not self._is_excluded(d, exclude_dirs, is_exclude_dirs_regex)]

            for file in files:
                if self._is_included(file, include_files, is_include_files_regex) and not self._is_excluded(file, exclude_files, is_exclude_files_regex):
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, project_dir)
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    result.append(f"{relative_path}:\n\"\"\"{content}\n\"\"\"\n")
        
        return "\n".join(result)

    def _is_excluded(self, name, exclude_list, is_regex):
        if is_regex:
            return any(re.match(pattern.strip(), name) for pattern in exclude_list if pattern.strip())
        else:
            return name in [item.strip() for item in exclude_list if item.strip()]

    def _is_included(self, name, include_list, is_regex):
        if not include_list:
            return True
        if is_regex:
            return any(re.match(pattern.strip(), name) for pattern in include_list if pattern.strip())
        else:
            return name in [item.strip() for item in include_list if item.strip()]
