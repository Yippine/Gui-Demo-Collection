import os
from pathlib import Path
import mimetypes
import threading
from src.core.utils import convert_to_regex

class FileProcessor:
    def __init__(self, root_dir, exclude_dirs, exclude_files, include_files, language):
        self.root_dir = Path(root_dir)
        self.exclude_dirs = convert_to_regex(exclude_dirs)
        self.exclude_files = convert_to_regex(exclude_files)
        self.include_files = convert_to_regex(include_files)
        self.language = language
        
    def process_files(self):
        result = []
        log = []
        
        def process():
            for root, dirs, files in os.walk(self.root_dir, topdown=True):
                dirs[:] = [d for d in dirs if not self._should_exclude_dir(d)]
                
                for file in sorted(files):
                    file_path = Path(root) / file
                    if self._should_process_file(file_path):
                        try:
                            with open(file_path, "r", encoding="utf-8") as f:
                                content = f.read().strip()
                            if content:
                                relative_path = file_path.relative_to(self.root_dir)
                                result.append(f"{relative_path}:\n\"\"\"{content}\"\"\"\n")
                                log.append(f"處理檔案：{relative_path}")
                        except UnicodeDecodeError:
                            log.append(f"警告：無法以 UTF-8 解碼{file_path}")
                        except Exception as e:
                            log.append(f"錯誤：處理 {file_path} 時發生問題：{e}")
        
        thread = threading.Thread(target=process)
        thread.start()
        thread.join()
        formatted_result = "\n".join(result)  
        formatted_log = "".join([f"{line}\n" for line in log])  
    
        return formatted_result, formatted_log
    
    def _should_exclude_dir(self, dir_name):
        return any(pattern.match(dir_name) for pattern in self.exclude_dirs)
    
    def _should_process_file(self, file_path):
        if any(pattern.match(str(file_path)) for pattern in self.include_files):
            return True
        if any(pattern.match(str(file_path)) for pattern in self.exclude_files):
            return False
        return self._is_text_file(file_path)
    
    @staticmethod
    def _is_text_file(file_path):
        mime_type, _ = mimetypes.guess_type(str(file_path))
        return mime_type and mime_type.startswith("text")
