Here's a raw README file for your code:

```
# Audio Processing Script

This script processes an audio file (`test1.wav`), performs transcription, transliteration, silence processing, and generates frame data based on timestamps and phonemes. It utilizes multiple modules to achieve these tasks.

## Prerequisites

- Python 3.x
- Required Python packages (ensure you have installed the necessary packages)

## Folder Structure

```
.
├── main.py
└── app/
    ├── create_hindi_json.py
    ├── create_csv_with_roman_words.py
    ├── remove_silence.py
    ├── per_frames_data.py
    └── data/
        ├── result.json
        ├── original_timestamp_from_whisper.csv
        └── merged.csv
```

## How to Run

1. Place your audio file (`test1.wav`) in the root directory.
2. Run the script by executing the following command in the terminal:

   ```bash
   python main.py
   ```

The script will process the audio file and generate the final frame data. The resulting CSV files will be saved in the `app/data/` folder.

## Modules Overview

1. **create_hindi_json.py**: Handles the transcription of the audio file into a JSON format.
2. **create_csv_with_roman_words.py**: Converts the JSON file into a CSV format with Hindi words transliterated to Roman script.
3. **remove_silence.py**: Processes the audio file by splitting it into chunks, analyzing silence, and merging relevant data.
4. **per_frames_data.py**: Generates the final frames and phoneme data from the processed CSV.

## Output Files

- `original_timestamp_from_whisper.csv`: Transcription timestamps generated from the audio.
- `merged.csv`: Audio data with silence analysis.
- `final_frames.csv`: Final frame data with phoneme and frame number adjustments.
```

This README explains how to run your script, gives a folder structure, and briefly describes each module.