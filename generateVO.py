import random
import requests
from dataclasses import dataclass
from typing import Optional

@dataclass
class VoiceSettings:
    stability: float = 0.5              # Range: 0-1 (Higher value = more stable, consistent output)
    similarity_boost: float = 0.75      # Range: 0-1 (Higher value = more similar to original voice)
    style: float = 0.0                  # Range: 0-1 (Higher value = more stylized speech)
    use_speaker_boost: bool = True      # Enhances speaker clarity
    
def generate_output_filename(text: str, voice_id: str, voice_settings: VoiceSettings, seed: int) -> str:
    """
    Generates a unique output filename based on the provided parameters.
    
    Parameters:
    - text (str): The script name for the output file.
    - voice_id (str): The unique identifier for the voice.
    - voice_settings (VoiceSettings): The settings for the voice.
    - seed (int): The seed value for the voiceover generation.
    
    Returns:
    - str: A unique filename based on the provided parameters.
    """
    # Extracting parameters from VoiceSettings
    stability = voice_settings.stability
    similarity_boost = voice_settings.similarity_boost
    style = voice_settings.style
    use_speaker_boost = voice_settings.use_speaker_boost
    
    # Creating a unique filename based on parameters
    filename = f"{text}_{voice_id}_{stability}_{similarity_boost}_{style}_{use_speaker_boost}_{seed}.mp3"
    
    return filename
    
def generate_voiceover(
    text: str,
    output_file: str,
    api_key: str,
    voice_id: str = "EXAVITQu4vr4xnSDxMaL",  # Default voice (Bella)
    model_id: str = "eleven_multilingual_v2",  # Latest model
    optimize_streaming_latency: int = 0,       # Range: 0-4 (0 = disabled, 4 = highest optimization)
    voice_settings: Optional[VoiceSettings] = None,
    seed: Optional[int] = None                 # Optional seed for deterministic generation
) -> None:
    """
    Generate a voiceover using ElevenLabs API with all available parameters
    
    Args:
        text (str): The text to convert to speech
        output_file (str): Path to save the generated audio file
        api_key (str): Your ElevenLabs API key
        voice_id (str): The ID of the voice to use
        model_id (str): The ID of the model to use
        optimize_streaming_latency (int): Latency optimization level (0-4)
        voice_settings (VoiceSettings): Voice configuration settings
        seed (int): Optional seed for consistent voice generation
    """
    
    if voice_settings is None:
        voice_settings = VoiceSettings()
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": api_key
    }
    
    data = {
        "text": text,
        "model_id": model_id,
        "voice_settings": {
            "stability": voice_settings.stability,
            "similarity_boost": voice_settings.similarity_boost,
            "style": voice_settings.style,
            "use_speaker_boost": voice_settings.use_speaker_boost
        },
        "optimize_streaming_latency": optimize_streaming_latency
    }
    
    # Add seed if provided
    if seed is not None:
        data["seed"] = seed
    
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        
        # Save the audio file
        with open(output_file, 'wb') as f:
            f.write(response.content)
        print(f"Successfully generated voiceover: {output_file}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error generating voiceover: {str(e)}")
        if response.status_code != 200:
            print(f"API Response: {response.text}")

# Example usage with different multiline text formats
if __name__ == "__main__":
    
   
    # Method 2: Using line breaks with \n
    sample_text2 = "First line\nSecond line\nThird line"

    # Method 3: Using a list of lines and joining them
    lines = [
        "Introduction: Welcome everyone!",
        "Today we'll discuss something exciting.",
        "Point 1: The first important thing",
        "Point 2: Another crucial aspect",
        "Conclusion: Thank you for listening!"
    ]
    sample_text3 = "\n".join(lines)

    # Method 4: Reading from a script file
    def read_script_from_file(file_path: str) -> str:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            print(f"Error reading script file: {str(e)}")
            return ""

    # Example script.txt content:
    """
    Welcome to our presentation!
    
    Today's agenda:
    1. Introduction
    2. Main topics
    3. Q&A session
    
    Let's begin...
    """
    
    # Generate voiceovers with different text formats

    sample_text1 = """
Unexpected layover? No worries! 

Quick booking, instant check-in only on "My 6" App! 

Even when plans change, we'll leave the light on for you.

Download the "My 6" app now! 

"""

    voice_settings = VoiceSettings(
        stability=0.41,
        similarity_boost=0.77,
        style=1,
        use_speaker_boost=True
    )

    voice_id = "XN5MUfNpmfCV6rvigVhs"
    Scriptname = "Video_8_Female"
    seed = 3200 #random.randint(1, 5000) #4294967295)  # Generate a random seed
    output_file = generate_output_filename(Scriptname, voice_id, voice_settings, seed)
    # Using triple-quoted text
    generate_voiceover(
        text=sample_text1,
        output_file=output_file,
        voice_id=voice_id,
        api_key=API_KEY,
        voice_settings=voice_settings,
        seed=seed
    )

    # # Using text from file
    # script_text = read_script_from_file("script.txt")  # Make sure this file exists
    # if script_text:
    #     generate_voiceover(
    #         text=script_text,
    #         output_file="output_from_file.mp3",
    #         api_key=API_KEY,
    #         voice_settings=voice_settings
    #     )

    # # Using joined lines
    # generate_voiceover(
    #     text=sample_text3,
    #     output_file="output_presentation.mp3",
    #     api_key=API_KEY,
    #     voice_settings=voice_settings
    # )