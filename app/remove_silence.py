import pandas as pd
from pydub import AudioSegment
import os
from pydub.silence import detect_nonsilent
import shutil

class AudioProcessor:
    """
    A class to handle processing of audio files based on timestamps from a CSV.
    This includes splitting the audio into chunks, detecting silence, and merging data.
    """

    def __init__(self, audio_file: str, csv_file: str):
        self.audio_file = audio_file
        self.csv_file = csv_file

    def split_audio(self, output_dir: str = 'app/temp'):
        """
        Splits the audio file into chunks based on start and end times in the CSV file.

        Parameters:
        -----------
        output_dir : str
            Directory where the audio chunks will be saved.
        """
        # Step 1: Read the CSV file
        df = pd.read_csv(self.csv_file)

        # Step 2: Load the audio file
        audio = AudioSegment.from_wav(self.audio_file)

        # Step 3: Split the audio file into chunks
        chunks = []
        for _, row in df.iterrows():
            start_time = row['start'] * 1000  # Convert to milliseconds
            end_time = row['end'] * 1000  # Convert to milliseconds
            chunk = audio[start_time:end_time]
            chunks.append(chunk)

        # Step 4: Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Step 5: Export each chunk to a file
        for i, chunk in enumerate(chunks):
            chunk.export(os.path.join(output_dir, f"{i + 1}.wav"), format="wav")

    @staticmethod
    def find_silence_durations(path_in, format="wav"):
        """
        Finds the duration of silence at the start and end of an audio file.

        Parameters:
        -----------
        path_in : str
            Path to the audio file.

        format : str
            Format of the audio file (default is 'wav').

        Returns:
        --------
        tuple
            Start and end silence durations in seconds.
        """
        sound = AudioSegment.from_file(path_in, format=format)
        non_sil_times = detect_nonsilent(sound, min_silence_len=50, silence_thresh=sound.dBFS * 1.5)

        if len(non_sil_times) > 0:
            start_time = non_sil_times[0][0]
            end_time = non_sil_times[-1][1]
            start_silence_duration = start_time / 1000
            end_silence_duration = (len(sound) - end_time) / 1000
            return start_silence_duration, end_silence_duration
        else:
            return None, None

    def process_silence(self, temp_dir: str = 'app/temp', output_file: str = 'app/data/silence_duration.csv'):
        """
        Processes silence detection for each chunk in the temp directory and saves the results to a CSV file.

        Parameters:
        -----------
        temp_dir : str
            Directory where the audio chunks are stored.

        output_file : str
            Path to save the CSV file with silence durations.
        """
        dfs = []
        files = os.listdir(temp_dir)
        wav_files = sorted([f for f in files if f.endswith('.wav')], key=lambda x: int(os.path.splitext(x)[0]))

        for filename in wav_files:
            file_path = os.path.join(temp_dir, filename)
            start_silence, end_silence = self.find_silence_durations(file_path)
            if start_silence is not None and end_silence is not None:
                df = pd.DataFrame({'File_Name': [os.path.basename(file_path)], 
                                   'Start_Silence': [start_silence], 
                                   'End_Silence': [end_silence]})
                dfs.append(df)

        # Concatenate all DataFrames into one and save to a CSV
        df_final = pd.concat(dfs, ignore_index=True)
        df_final.to_csv(output_file, index=False, encoding='utf-8')

    def merge_data(self, silence_csv: str = 'app/data/silence_duration.csv', output_file: str = 'app/data/merged.csv'):
        """
        Merges the original timestamp data with silence durations and saves the result to a CSV file.

        Parameters:
        -----------
        silence_csv : str
            Path to the CSV file containing silence durations.

        output_file : str
            Path to save the merged CSV file.
        """
        df1 = pd.read_csv(silence_csv)
        df2 = pd.read_csv(self.csv_file)

        # Concatenate DataFrames side by side
        merged_df = pd.concat([df2, df1], axis=1)

        # Calculate adjusted start and end times
        merged_df['ini'] = merged_df['start'] + merged_df['Start_Silence']
        merged_df['fin'] = merged_df['end'] - merged_df['End_Silence']

        # Drop unnecessary columns
        merged_df = merged_df.drop(['File_Name', 'Start_Silence', 'End_Silence'], axis=1)

        # Save the final merged DataFrame to a CSV
        merged_df.to_csv(output_file, index=False)

    def clean_up(self, temp_dir: str = 'app/temp'):
        """
        Cleans up by deleting the temporary directory and its contents.

        Parameters:
        -----------
        temp_dir : str
            Directory to be removed.
        """
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

