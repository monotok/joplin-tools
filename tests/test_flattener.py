import glob
import os
import re
import shutil
import tempfile
from os import mkdir

import preprocessing.flattener as flattener


def normalize_dict(data):
    """
    Recursively normalize a nested dictionary by replacing tempdir values in 'new_path'.
    """
    if isinstance(data, dict):
        result = {}
        for key, value in data.items():
            if key == 'new_path' and isinstance(value, str):
                result[key] = re.sub(r"/tmp/tmp[0-9a-zA-Z]+", "/path/to/tempdir", value)
            elif key == 'old_path' and isinstance(value, str):
                result[key] = value.split('joplin-tools')[1]
            else:
                result[key] = normalize_dict(value)
        return result
    return data  # Return non-dict values as-is


def test_move_files_to_top_level_dir():
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Copy markdown files from the resource folder to the temporary directory
        resource_folder = 'resources/notes/'

        moved_files = flattener.move_files_to_top_level_dir(resource_folder, temp_dir)

        normalised_moved_files = normalize_dict(moved_files)

        assert normalised_moved_files == {'resources/notes/linux/Clean out old kernels.md': {'new_path': '/path/to/tempdir/Clean '
                                                                'out old '
                                                                'kernels.md',
                                                    'old_path': '/tests/resources/notes/linux/Clean '
                                                                'out old '
                                                                'kernels.md'},
 'resources/notes/linux/Ubuntu/Live Patch.md': {'new_path': '/path/to/tempdir/Live '
                                                            'Patch.md',
                                                'old_path': '/tests/resources/notes/linux/Ubuntu/Live '
                                                            'Patch.md'},
 'resources/notes/linux/Ubuntu/Move home to ext Drive.md': {'new_path': '/path/to/tempdir/Move '
                                                                        'home '
                                                                        'to '
                                                                        'ext '
                                                                        'Drive.md',
                                                            'old_path': '/tests/resources/notes/linux/Ubuntu/Move '
                                                                        'home '
                                                                        'to '
                                                                        'ext '
                                                                        'Drive.md'},
 'resources/notes/linux/Ubuntu/fake_image.png': {'new_path': '/path/to/tempdir/fake_image.png',
                                                 'old_path': '/tests/resources/notes/linux/Ubuntu/fake_image.png'}}
