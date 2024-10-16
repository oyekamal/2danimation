from app.create_hindi_json import AudioTranscriber
from app.create_csv_with_roman_words import HindiTransliterator
from app.remove_silence import AudioProcessor   
from app.per_frames_data import FrameExploder

# Create an instance of the AudioTranscriber class
transcriber = AudioTranscriber("test1.wav")

# Transcribe the audio and save the result
transcriber.transcribe_audio()

# Create an instance of the HindiTransliterator class
transliterator = HindiTransliterator()

# Process the JSON file and save the result to a CSV file
transliterator.process_json_to_csv('app/data/result.json', 'app/data/original_timestamp_from_whisper.csv')

# Create an instance of AudioProcessor
processor = AudioProcessor(audio_file='test1.wav', csv_file='app/data/original_timestamp_from_whisper.csv')

# Step 1: Split the audio into chunks
processor.split_audio()

# Step 2: Process silence durations for each chunk
processor.process_silence()

# Step 3: Merge the data and save to a CSV
processor.merge_data()

# Step 4: Clean up the temporary directory
processor.clean_up()



# Initialize the processor
exploder = FrameExploder(audio_file='test1.wav', csv_file='app/data/merged.csv')

# Get audio duration (optional)
duration = exploder.get_audio_duration()
print(f"Audio duration: {duration:.2f} seconds")

# Load CSV and process data
df = exploder.load_csv()
df = exploder.find_missing_timestamps(df)
df = exploder.add_phonemes(df)
df = exploder.adjust_frame_numbers(df)
df = exploder.add_initial_row(df)

# Generate final frames and save to CSV
exploder.generate_final_frames(df, output_file='app/data/final_frames.csv')
