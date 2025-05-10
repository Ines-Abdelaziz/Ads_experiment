#!/bin/bash

# === CONFIGURATION ===
START_HOUR_1=8    # 8:00 AM - 12:00 PM
END_HOUR_1=12
START_HOUR_2=13   # 1:00 PM - 5:00 PM
END_HOUR_2=17
START_HOUR_3=18   # 6:00 PM - 11:00 PM
END_HOUR_3=23
START_HOUR_4=0    # 12:00 AM - 2:00 AM
END_HOUR_4=2

# === GET CURRENT TIME IN US EASTERN TIME ===
function check_time_window {
    current_time=$(TZ="America/New_York" date +%H)
    echo "Current Eastern Time hour: $current_time"

    # Check if the current time is within the allowed time windows
    if (( current_time >= START_HOUR_1 && current_time < END_HOUR_1 )) || \
       (( current_time >= START_HOUR_2 && current_time < END_HOUR_2 )) || \
       (( current_time >= START_HOUR_3 && current_time < END_HOUR_3 )) || \
       (( current_time >= START_HOUR_4 && current_time < END_HOUR_4 )); then
        return 0  # Time is within allowed windows
    else
        return 1  # Time is outside allowed windows
    fi
}

BATCH_DIR='./'

# === CHECK IF BATCH DIRECTORY EXISTS ===
if [ ! -d "$BATCH_DIR" ]; then
    echo "Batch directory not found: $BATCH_DIR"
    exit 1
fi

# === LOOP THROUGH EACH BATCH FILE ===
for BATCH_FILE in "$BATCH_DIR"/*.csv; do
    if [ -f "$BATCH_FILE" ]; then
        echo "Running for batch file: $BATCH_FILE"

        # === PAUSE UNTIL WITHIN ALLOWED HOURS ===
        while ! check_time_window; do
            echo "Outside of allowed hours. Pausing until time window is reached..."
            sleep 3600  # Sleep for 10 minutes before checking again
        done

        echo "Within allowed time window. Running batch file."
        chmod +x Script.py  # Ensure the script is executable
        
        # Run the profile-specific script (replace with your actual task)
        ./Script.py 5 "$BATCH_FILE"
        
        # Pause briefly between batches
        sleep 300
    else
        echo "No CSV batch files found in $BATCH_DIR"
    fi
done
