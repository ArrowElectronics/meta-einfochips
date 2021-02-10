#! /bin/sh

# Copyright (c) 2016-2018 Basler AG. All rights reserved.

# Enable pylon logging for this run. The logfile will be created in /tmp/pylonLog.txt.
# You can use other pylon-based applications as a parameter to this script file to run it with logging enabled.
# If you just start this script with no args the pylonViewer will be started.

# Determine the directory this script resides in
this_script_full_path=`readlink -f "$0"` # Absolute path this script
this_script_directory=`dirname "$this_script_full_path"` # the directory

app_to_start="$1"
if [ -z "$app_to_start" ]; then
    app_to_start="${this_script_directory}/PylonViewerApp"
fi

# Start pylonViewer with logging script
"${this_script_directory}/pylon-start-with-logging" "$app_to_start"
