'''Backup folders.
TODO
- Add `to_json()` method
'''
from os import walk
import shutil
from pathlib import Path


class Backup:
    '''Describe a folder you want to back up.'''
    def __init__(self, folder):
        folder = Path(folder).resolve()
        if not folder.exists():
            raise FileNotFoundError(folder)
        if not folder.is_dir():
            raise NotADirectoryError(folder)
        self.path = Path(folder)

    def __repr__(self):
        return f"{type(self).__name__}(path='{self.path}')"

    def copy_to(self, folder):
        '''Copy all folders/files in backup to given folder.'''
        shutil.copytree(self.path, folder)

    def copy_missing_to(self, folder):
        '''Copy files across to `folder` if they're not there already.'''
        paste_folder = Path(folder)
        if not paste_folder.exists():
            raise FileNotFoundError(paste_folder)
        # Look for folders / files in backup that are not in `folder`
        for folder, subfolders, file_names in walk(self.path):
            folder = Path(folder)
            expected_folder_path = paste_folder / folder.relative_to(self.path)
            if not expected_folder_path.exists():
                # Copy folder across if it's not there already
                print(f'Copying folder "{folder}"')
                print(f'            to "{expected_folder_path}"')
                shutil.copytree(folder, expected_folder_path)
                # Don't look at contents of this folder as it is already copied
                subfolders[:] = []
                continue
            # Copy files across if they're not there already
            for file_name in file_names:
                expected_file_path = expected_folder_path / file_name
                if not expected_file_path.exists():
                    print(f'Copying file "{folder / file_name}"')
                    print(f'          to "{expected_file_path}"')
                    shutil.copy(folder / file_name, expected_file_path)

    def delete_missing_from(self, folder):
        '''Deletes files in `folder` that are not in `self.path`.'''
        folder = Path(folder)
        if not folder.exists():
            raise FileNotFoundError(folder)
        for folder_path, subfolders, file_names in walk(folder):
            folder_path = Path(folder_path)
            expected_folder_path = self.path / folder_path.relative_to(folder)
            if not expected_folder_path.exists():
                # Delete folder if it doesn't exist in `self.path`
                print(f'Deleting folder "{folder_path}"')
                shutil.rmtree(folder_path)
                subfolders[:] = []
                continue
            # Delete files if they don't exist in `self.path`
            for file_name in file_names:
                expected_file_path = expected_folder_path / file_name
                if not expected_file_path.exists():
                    file_to_delete = folder_path / file_name
                    print(f'Deleting file "{file_to_delete}"')
                    file_to_delete.unlink()
