# REMEMBER: this is python 2.7
from __future__ import print_function
import os

import scriptengine  # type: ignore

from communication_import_export import import_communication
from entrypoint import find_application, find_communication, get_device_entrypoints, get_src_folder
from import_from_files import import_directory  # assuming import_directory is defined here
from util import print_python_version, assert_project_open, assert_path_exists

# If remove_tracked_objects is not defined in your project, define a no-op.
try:
    from util import remove_tracked_objects
except ImportError:
    def remove_tracked_objects(obj_list):
        pass

def remove_existing_children(parent_obj):
    """
    Remove all children of a given Codesys object.
    We assume that each child object has a .remove() method.
    """
    children = list(parent_obj.get_children())
    for child in children:
        try:
            print("Removing existing object:", child.get_name())
            child.remove()
        except Exception as e:
            print("Error removing object '{}':".format(child.get_name()))
            print(e)

def main():
    print_python_version()
    assert_project_open()

    # Get the base folder used during export.
    base_folder = get_src_folder(scriptengine.projects.primary)
    print("Reading from base folder: " + base_folder)
    assert_path_exists(base_folder)

    # Process each device in the project.
    for device_obj in get_device_entrypoints(scriptengine.projects.primary):
        device_name = device_obj.get_name()  # e.g., "PLC_AC500_V3"
        device_folder = os.path.join(base_folder, device_name)
        assert_path_exists(device_folder)

        # Get the Application object for this device.
        application = find_application(device_obj)
        # Look for the 'src' folder among the children of the Application object.
        src_folder_obj = None
        for child in application.get_children():
            if child.get_name().lower() == "src":
                src_folder_obj = child
                break
        if src_folder_obj is None:
            print("Warning: No 'src' folder found in Application for device:", device_name)
            continue

        # The exported files reside in device_folder/application/src.
        src_import_folder = os.path.join(device_folder, "application", "src")
        assert_path_exists(src_import_folder)

        # Optionally, remove tracked objects from the Application.
        remove_tracked_objects(application.get_children())

        # Remove all existing objects under the src Codesys object.
        remove_existing_children(src_folder_obj)

        # Now import the directory structure from the exported src folder
        # into the (now empty) src object.
        import_directory(src_import_folder, src_folder_obj)

        # Optionally, import Communication information as before.
        communication = find_communication(device_obj)
        import_communication(communication, device_folder)

    print("Import complete!")

if __name__ == "__main__":
    main()
