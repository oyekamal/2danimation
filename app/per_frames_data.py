import pandas as pd
from pydub import AudioSegment
import numpy as np
from g2p_en import G2p
import math
import hashlib

class FrameExploder:
    """
    A class to handle audio processing, dataframe manipulation, and phoneme frame distribution.
    """

    def __init__(self, audio_file: str, csv_file: str):
        self.audio_file = audio_file
        self.csv_file = csv_file
        self.g2p = G2p()

    def get_audio_duration(self):
        """
        Returns the duration of the audio file in seconds.
        """
        audio = AudioSegment.from_wav(self.audio_file)
        return len(audio) / 1000  # Convert milliseconds to seconds

    def load_csv(self):
        """
        Loads the CSV file and initializes new columns for character, head direction, emotion, etc.
        """
        df = pd.read_csv(self.csv_file)
        new_columns = {
            'character': 'character_1',
            'head_direction': 'M',
            'emotion': 'happy',
            'eye_direction': 'M',
            'eye_blinking': False,
            'mouth_phonems': '',
            'body': '01',
            'mode': '1',
            'background': 'Plain',
            'hash': ''
        }
        df = df.assign(**new_columns)
        return df

    def find_missing_timestamps(self, df):
        """
        Finds missing timestamps in the dataframe and adds rows for those gaps.
        """
        new_rows = []
        for i in range(len(df) - 1):
            current_fin = df.loc[i, 'fin']
            next_ini = df.loc[i + 1, 'ini']

            if next_ini - current_fin > 0.001:
                new_row = {
                    'text': '', 'start': '', 'end': '',
                    'ini': round(current_fin + 0.001, 3), 
                    'fin': round(next_ini - 0.001, 3),
                    'character': 'character_1', 'head_direction': 'M', 'emotion': 'happy',
                    'eye_direction': 'M', 'eye_blinking': False, 'mouth_phonems': 'M',
                    'body': '01', 'mode': '1', 'background': 'Plain', 'hash': ''
                }
                new_rows.append(new_row)
        
        if new_rows:
            df = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)
            df = df.sort_values(by='ini').reset_index(drop=True)
        return df

    def get_phonemes(self, text):
        """
        Converts text to phonemes using g2p and returns them as a comma-separated string.
        """
        phonemes = self.g2p(text)
        return ','.join(phonemes).replace(' ', ',')

    def add_phonemes(self, df):
        """
        Applies the phoneme extraction to the dataframe text column.
        """
        df['mouth_phonems'] = np.where(df['text'] != '', df['text'].apply(self.get_phonemes), df['mouth_phonems'])
        return df

    def adjust_frame_numbers(self, df):
        """
        Adjusts the ini and fin columns to frame numbers based on a frame rate of 24.
        """
        df['ini_frm'] = round(df['ini'] * 24, 0)
        df['fin_frm'] = round(df['fin'] * 24, 0) - 1
        df = df.drop(['ini', 'fin', 'start', 'end'], axis=1)
        return df

    def add_initial_row(self, df):
        """
        Adds an initial row if the first frame does not start at 0.
        """
        first_row = df.iloc[0]
        new_rows = []

        if first_row['ini_frm'] != 0:
            new_rows.append({
                'ini_frm': 1, 'fin_frm': first_row['ini_frm'] - 1,
                'character': 'character_1', 'head_direction': 'M', 'eye_direction': 'M', 
                'mouth_phonems': 'M', 'emotion': 'happy', 'eye_blinking': False, 
                'body': '01', 'mode': '1', 'background': 'Plain', 'hash': None
            })

        if new_rows:
            df_new = pd.DataFrame(new_rows)
            df = pd.concat([df_new, df], ignore_index=True)
        
        df['ini_frm'] = df['ini_frm'].astype(int)
        df['fin_frm'] = df['fin_frm'].astype(int)
        return df

    def distribute_and_explode(self, df):
        """
        Distributes frames evenly among phonemes and explodes rows accordingly.
        """
        rows = []

        for idx, row in df.iterrows():
            ini_frm = row['ini_frm']
            fin_frm = row['fin_frm']
            phonemes = row['mouth_phonems'].split(',')

            total_frames = fin_frm - ini_frm + 1
            num_phonemes = len(phonemes)

            frames_per_phoneme = total_frames // num_phonemes
            remainder = total_frames % num_phonemes

            frames_list = [frames_per_phoneme] * num_phonemes

            middle_idx = num_phonemes // 2
            if remainder > 0:
                frames_list[middle_idx] += remainder

            frame_start = ini_frm
            for phoneme, frames in zip(phonemes, frames_list):
                for _ in range(frames):
                    new_row = row.copy()
                    new_row['mouth_phonems'] = phoneme
                    new_row['frame'] = frame_start
                    rows.append(new_row)
                    frame_start += 1

        return pd.DataFrame(rows)

    def create_hash(self, row):
        """
        Creates a SHA-256 hash for the combined features in a row.
        """
        combined_str = f"{row['character']}{row['head_direction']}{row['eye_direction']}{row['mouth_phonems']}{row['emotion']}{row['eye_blinking']}{row['body']}{row['mode']}{row['background']}"
        return hashlib.sha256(combined_str.encode()).hexdigest()

    def generate_final_frames(self, df, output_file='final_frames.csv'):
        """
        Generates the final frame dataset, applies hashing, and saves it to a CSV.
        """
        df_exploded = self.distribute_and_explode(df)
        df_exploded['hash'] = df_exploded.apply(self.create_hash, axis=1)
        df_exploded = df_exploded.drop(['ini_frm', 'fin_frm'], axis=1)
        df_exploded.to_csv(output_file, index=False)

