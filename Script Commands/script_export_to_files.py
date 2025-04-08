# REMEMBER: this is python 2.7
from __future__ import print_function
import os
import shutil
import traceback

import scriptengine  # type: ignore

from communication_import_export import export_communication
from entrypoint import find_application, find_communication, get_device_entrypoints, get_src_folder
from import_export import OBJECT_TYPE_TO_EXPORT_FUNCTION
from object_type import get_object_type
from util import print_python_version, assert_project_open

def export_child(child_obj, parent_obj, parent_folder_path):
    try:
        child_obj_name = child_obj.get_name()
        child_obj_type = get_object_type(child_obj)
        print("DEBUG: Exporting child object '{}' of type '{}'".format(child_obj_name, child_obj_type))
        export_fn = OBJECT_TYPE_TO_EXPORT_FUNCTION.get(child_obj_type)
        if export_fn is not None:
            export_fn(child_obj, parent_obj, parent_folder_path, export_child)
        else:
            print("DEBUG: No export function for type: {}".format(child_obj_type))
    except Exception as e:
        print("ERROR: Exception while exporting child '{}'".format(child_obj.get_name()))
        traceback.print_exc()

def main():
    print_python_version()
    assert_project_open()

    # Get the base export folder (usually built from the project file path)
    base_folder = get_src_folder(scriptengine.projects.primary)
    print("DEBUG: Writing to base folder: " + base_folder)

    # Remove the entire export folder if it exists.
    if os.path.exists(base_folder):
        try:
            print("DEBUG: Removing existing folder: " + base_folder)
            shutil.rmtree(base_folder)
        except Exception as e:
            print("ERROR: Failed to remove folder: " + base_folder)
            traceback.print_exc()
    try:
        os.mkdir(base_folder)
        print("DEBUG: Created base folder: " + base_folder)
    except Exception as e:
        print("ERROR: Failed to create base folder: " + base_folder)
        traceback.print_exc()
        return

    # Process each device
    for device_obj in get_device_entrypoints(scriptengine.projects.primary):
        try:
            device_name = device_obj.get_name()  # e.g. "PLC_AC500_V3"
            device_folder = os.path.join(base_folder, device_name)
            print("DEBUG: Creating device folder: " + device_folder)
            os.mkdir(device_folder)
        except Exception as e:
            print("ERROR: Could not create device folder for device: " + device_name)
            traceback.print_exc()
            continue

        try:
            # Get the Application object for this device.
            application = find_application(device_obj)
            print("DEBUG: Found Application object for device: " + device_name)
        except Exception as e:
            print("ERROR: Could not find Application in device: " + device_name)
            traceback.print_exc()
            continue

        # Look for the "src" child folder inside the Application object.
        src_child = None
        try:
            for child in application.get_children():
                child_name = child.get_name()
                print("DEBUG: Found child in Application: " + child_name)
                if child_name.lower() == "src":
                    src_child = child
                    print("DEBUG: Found 'src' folder in Application.")
                    break
            if src_child is None:
                print("WARNING: No 'src' folder found in Application for device:", device_name)
                continue
        except Exception as e:
            print("ERROR: Exception while iterating children in Application for device: " + device_name)
            traceback.print_exc()
            continue

        try:
            # Build folder structure: device_folder/application/src
            application_folder = os.path.join(device_folder, "application")
            print("DEBUG: Creating application folder: " + application_folder)
            os.mkdir(application_folder)
            src_export_folder = os.path.join(application_folder, "src")
            print("DEBUG: Creating src export folder: " + src_export_folder)
            os.mkdir(src_export_folder)
        except Exception as e:
            print("ERROR: Failed to create folder structure for device: " + device_name)
            traceback.print_exc()
            continue

        try:
            # Export only the children of the src object (not the 'src' folder itself)
            for child_obj in src_child.get_children():
                print("DEBUG: Exporting child from src folder: " + child_obj.get_name())
                export_child(child_obj, src_child, src_export_folder)
        except Exception as e:
            print("ERROR: Exception during exporting children of src for device: " + device_name)
            traceback.print_exc()

        try:
            # Optionally, export Communication information as before.
            communication = find_communication(device_obj)
            print("DEBUG: Exporting Communication for device: " + device_name)
            export_communication(communication, device_folder)
        except Exception as e:
            print("ERROR: Exception during exporting Communication for device: " + device_name)
            traceback.print_exc()

    print("Export complete!")

if __name__ == "__main__":
    main()
