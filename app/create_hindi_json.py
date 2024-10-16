import whisper_timestamped as whisperts
import json

class AudioTranscriber:
    """
    A class to transcribe audio files using the whisper_timestamped model.

    Attributes:
    -----------
    model : object
        Loaded Whisper model used for transcription.

    Methods:
    --------
    __init__(audio_file: str, model_name: str = "vasista22/whisper-hindi-large-v2", device: str = "cpu"):
        Initializes the transcriber with an audio file and model.

    transcribe_audio():
        Transcribes the provided audio file and saves the results in a JSON file.
    """

    def __init__(self, audio_file: str, model_name: str = "vasista22/whisper-hindi-large-v2", device: str = "cpu"):
        """
        Initializes the AudioTranscriber with the audio file, model name, and device.

        Parameters:
        -----------
        audio_file : str
            The path to the audio file to be transcribed.
        model_name : str, optional
            The name of the Whisper model to load. Defaults to "vasista22/whisper-hindi-large-v2".
        device : str, optional
            The device to load the model on (e.g., "cpu" or "cuda"). Defaults to "cpu".
        """
        self.audio_file = audio_file
        self.model_name = model_name
        self.device = device
        self.model = whisperts.load_model(model_name, device=device)

    def transcribe_audio(self, output_file: str = 'app/data/result.json'):
        """
        Transcribes the audio file and saves the transcription in a JSON file.

        Parameters:
        -----------
        output_file : str, optional
            The path where the transcription result will be saved. Defaults to 'data/result.json'.
        """
        # Load the audio
        audio = whisperts.load_audio(self.audio_file)

        # Transcribe the audio
        results = whisperts.transcribe(self.model, audio)

        # Format the results to JSON and save them
        results_json = json.dumps(results, indent=2, ensure_ascii=False)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(results_json)

        print(f"Transcription complete. Results saved to {output_file}")
