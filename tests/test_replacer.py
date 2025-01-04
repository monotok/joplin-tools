import glob
import os
import shutil
import tempfile

import preprocessing.replacer as replacer


def test_find_all_images_with_spaces():
    expected_list_of_images = {'3_Understanding and improvin.png': '3_Understanding_and_improvin.png'}

    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:

        # Copy markdown files from the resource folder to the temporary directory
        resource_folder = 'resources/test_mds/'
        for file in glob.glob(os.path.join(resource_folder, '*.png')):
            shutil.copy(file, temp_dir)

        actual_list_of_images = replacer.find_all_files_with_spaces(temp_dir, ['png'])

        assert expected_list_of_images == actual_list_of_images


def test_replace_image_spaces_no_match():
    list_of_images = {'1_How to scan all files in ocis .png': '1_How_to_scan_all_files_in_ocis_.png'}
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:

        # Copy markdown files from the resource folder to the temporary directory
        resource_folder = 'resources/test_mds/'
        for file in glob.glob(os.path.join(resource_folder, '*.md')):
            shutil.copy(file, temp_dir)

        result = replacer.replace_file_spaces_markdown(temp_dir, list_of_images)

        assert result == []

def test_replace_image_spaces_match():
    list_of_images = {'3_Understanding and improvin.png': '3_Understanding_and_improvin.png'}

    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:

        # Copy markdown files from the resource folder to the temporary directory
        resource_folder = 'resources/test_mds/'
        for file in glob.glob(os.path.join(resource_folder, '*.md')):
            shutil.copy(file, temp_dir)

        result = replacer.replace_file_spaces_markdown(temp_dir, list_of_images)

        assert result == ['3_Understanding and improvin.png']


