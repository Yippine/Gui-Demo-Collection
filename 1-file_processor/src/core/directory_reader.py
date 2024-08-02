import os
import re

class DirectoryReader:
    def __init__(self):
        pass

    def read_directory(self, project_dir, exclude_dirs, exclude_files, include_files, is_exclude_dirs_regex, is_exclude_files_regex, is_include_files_regex):
        tree = []
        for root, dirs, files in os.walk(project_dir):
            level = root.replace(project_dir, '').count(os.sep)
            indent = '│   ' * (level - 1) + '├── ' if level > 0 else ''
            relative_path = os.path.relpath(root, project_dir)
            
            if level == 0:
                tree.append(os.path.basename(project_dir))
            elif not self._is_excluded(relative_path, exclude_dirs, is_exclude_dirs_regex):
                tree.append(f"{indent}{os.path.basename(root)}/")
            else:
                dirs[:] = []  # 如果目錄被排除,不再遍歷其子目錄
                continue

            sub_indent = '│   ' * level + '├── '
            for file in files:
                if self._is_included(file, include_files, is_include_files_regex) and not self._is_excluded(file, exclude_files, is_exclude_files_regex):
                    tree.append(f"{sub_indent}{file}")

        return "\n".join(tree)

    def _is_excluded(self, name, exclude_list, is_regex):
        if is_regex:
            return any(re.match(pattern.strip(), name) for pattern in exclude_list)
        else:
            return name in [item.strip() for item in exclude_list]

    def _is_included(self, name, include_list, is_regex):
        if not include_list:
            return True
        if is_regex:
            return any(re.match(pattern.strip(), name) for pattern in include_list)
        else:
            return name in [item.strip() for item in include_list]