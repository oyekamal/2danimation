import json
import pandas as pd

# Hindi to Latin transliteration dictionary
hindi_to_latin = {
    'अ': 'a', 'आ': 'aa', 'इ': 'i', 'ई': 'ee', 'उ': 'u', 'ऊ': 'oo', 'ऋ': 'ri',
    'ए': 'e', 'ऐ': 'ai', 'ओ': 'o', 'औ': 'au', 'ं': 'n', 'ः': 'h',
    'क': 'k', 'ख': 'kh', 'ग': 'g', 'घ': 'gh', 'ङ': 'n',
    'च': 'ch', 'छ': 'chh', 'ज': 'j', 'झ': 'jh', 'ञ': 'n',
    'ट': 't', 'ठ': 'th', 'ड': 'd', 'ढ': 'dh', 'ण': 'n',
    'त': 't', 'थ': 'th', 'द': 'd', 'ध': 'dh', 'न': 'n',
    'प': 'p', 'फ': 'ph', 'ब': 'b', 'भ': 'bh', 'म': 'm',
    'य': 'y', 'र': 'r', 'ल': 'l', 'व': 'v', 'श': 'sh', 'ष': 'sh', 'स': 's', 'ह': 'h',
    'क्ष': 'ksh', 'त्र': 'tra', 'ज्ञ': 'gya',
    'ा': 'a', 'ि': 'i', 'ी': 'ee', 'ु': 'u', 'ू': 'oo', 'े': 'e', 'ै': 'ai', 'ो': 'o', 'ौ': 'au',
    '्': '', 'ं': 'n', 'ँ': 'n', 'ः': 'h', 'ॉ': 'o',
    '१': '1', '२': '2', '३': '3', '४': '4', '५': '5', '६': '6', '७': '7', '८': '8', '९': '9', '०': '0'
}

class HindiTransliterator:
    """
    A class that handles the transliteration of Hindi text from a JSON file
    and saves the extracted information in a CSV file.

    Methods:
    --------
    transliterate_hindi(text):
        Transliterate Hindi text to Latin using the hindi_to_latin dictionary.

    process_json_to_csv(json_file, csv_file):
        Read the JSON file, transliterate the text, extract relevant data, and save it to a CSV file.
    """

    @staticmethod
    def transliterate_hindi(text):
        """
        Transliterate Hindi text to Latin using the hindi_to_latin dictionary.

        Parameters:
        -----------
        text : str
            The Hindi text to be transliterated.

        Returns:
        --------
        str
            The transliterated Latin text.
        """
        transliterated = ""
        for char in text:
            transliterated += hindi_to_latin.get(char, char)  # Default to the original character if not in the dictionary
        return transliterated

    def process_json_to_csv(self, json_file: str, csv_file: str):
        """
        Read the JSON file, transliterate the text, extract the required data, and save it as a CSV.

        Parameters:
        -----------
        json_file : str
            Path to the input JSON file.

        csv_file : str
            Path where the output CSV will be saved.
        """
        # Step 1: Read the JSON file
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Step 2: Extract the required data
        words_data = []
        for segment in data.get('segments', []):
            for word in segment.get('words', []):
                # Transliterate the word text using the transliterate_hindi method
                transliterated_text = self.transliterate_hindi(word['text'])
                
                # Append the data to the words_data list
                words_data.append({
                    'text': transliterated_text,
                    'start': word['start'],
                    'end': word['end']
                })

        # Step 3: Create a DataFrame
        df = pd.DataFrame(words_data)

        # Step 4: Write to CSV
        df.to_csv(csv_file, index=False, encoding='utf-8')

        print(f"Data has been processed and saved to {csv_file}")
