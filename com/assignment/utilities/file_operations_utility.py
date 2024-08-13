import fnmatch
import os
import shutil
import logging


class FileOperationsUtility:
    logger = logging.getLogger(__name__)

    @staticmethod
    def find_file_in_directory(directory, filename):
        for root, dirs, files in os.walk(directory):
            if filename in files:
                return os.path.join(root, filename)
        return None

    @staticmethod
    def find_directory(directory):
        for root, dirs, files in os.walk(directory):
            if directory in dirs:
                return os.path.join(root, directory)
            else:
                if root == directory:
                    return root
        return None

    @staticmethod
    def delete_directory(directory):
        if os.path.exists(directory):
            # Remove the directory and all its contents
            try:
                shutil.rmtree(directory)
                print(f"Directory {directory} and its contents deleted successfully")
            except PermissionError:
                print(f"Error: Permission denied to delete {directory}")
            except OSError as e:
                print(f"Error: {e.strerror} - {e.filename}")

    @staticmethod
    def get_project_root():
        # Get the directory of the current file
        current_file_dir = os.path.dirname(os.path.abspath(__file__))
        # Navigate up to the project root
        project_root = os.path.abspath(os.path.join(current_file_dir, "../../.."))
        return project_root

    @staticmethod
    def find_directories_with_file_pattern(root_dir, pattern):
        matching_dirs = set()
        excluded_dirs = ['.venv']
        # Traverse the directory tree
        for dir_path, dir_names, _ in os.walk(root_dir):
            # Check if any of the filenames match the pattern
            for dir_name in dir_names:
                if fnmatch.fnmatch(dir_name, pattern):
                    matching_dirs.add(os.path.join(dir_path, dir_name))
        matching_dirs = list([dirs for dirs in matching_dirs
                              for excluded_dir in excluded_dirs
                              if not dirs.__contains__(excluded_dir)])
        FileOperationsUtility.logger.warning('Directories to be deleted are => %s', matching_dirs)
        return matching_dirs
