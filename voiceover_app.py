import streamlit as st
import requests
from generateVO import generate_voiceover, VoiceSettings, generate_output_filename
import random
import os
import json

def get_available_voices(api_key):
    """Fetch available voices from ElevenLabs API"""
    url = "https://api.elevenlabs.io/v1/voices"
    headers = {
        "Accept": "application/json",
        "xi-api-key": api_key
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        voices = response.json()["voices"]
        return {voice["name"]: voice["voice_id"] for voice in voices}
    except Exception as e:
        st.error(f"Error fetching voices: {str(e)}")
        return {}

def main():
    st.set_page_config(page_title="Voice Generation App", layout="wide")
    st.title("Voice Generation App")
    
    # Initialize session state for API key
    if "api_key" not in st.session_state:
        st.session_state.api_key = ""
    
    # Tabs for main content and settings
    tab1, tab2 = st.tabs(["Generate Voice", "Settings"])
    
    with tab2:
        st.header("Settings")
        api_key = st.text_input("ElevenLabs API Key", 
                               value=st.session_state.api_key,
                               type="password",
                               help="Enter your ElevenLabs API key")
        if api_key:
            st.session_state.api_key = api_key
    
    with tab1:
        if not st.session_state.api_key:
            st.warning("Please enter your API key in the Settings tab")
            return
        
        # Fetch available voices
        voices = get_available_voices(st.session_state.api_key)
        if not voices:
            st.error("Unable to fetch voices. Please check your API key.")
            return
        
        # Text input
        text = st.text_area("Enter your text", height=200)
        
        # Create two columns for settings
        col1, col2 = st.columns(2)
        
        with col1:
            # Script name input
            script_name = st.text_input("Script Name", value="Video_Female", 
                                      help="Enter a name for your script (e.g., Video_1_Female)")
            
            # Voice selection
            selected_voice_name = st.selectbox("Select Voice", list(voices.keys()))
            voice_id = voices[selected_voice_name]
            
            # Seed settings
            seed_type = st.radio("Seed Type", ["Random", "Specific"])
            if seed_type == "Random":
                seed = random.randint(1, 4294967295)
            else:
                seed = st.number_input("Enter Seed", 
                                     min_value=1, 
                                     max_value=4294967295, 
                                     value=1000)
        
        with col2:
            # Voice settings
            st.subheader("Voice Settings")
            stability = st.slider("Stability", 0.0, 1.0, 0.5, 0.01)
            similarity_boost = st.slider("Similarity Boost", 0.0, 1.0, 0.75, 0.01)
            style = st.slider("Style", 0.0, 1.0, 0.0, 0.01)
            use_speaker_boost = st.checkbox("Use Speaker Boost", value=True)
        
        if st.button("Generate Voice"):
            if not text:
                st.warning("Please enter some text")
                return
            
            # Create voice settings
            voice_settings = VoiceSettings(
                stability=stability,
                similarity_boost=similarity_boost,
                style=style,
                use_speaker_boost=use_speaker_boost
            )
            
            # Generate filename using the original function
            filename = generate_output_filename(script_name, voice_id, voice_settings, seed)
            
            try:
                # Generate voiceover
                generate_voiceover(
                    text=text,
                    output_file=filename,
                    api_key=st.session_state.api_key,
                    voice_id=voice_id,
                    voice_settings=voice_settings,
                    seed=seed
                )
                
                # Display audio and download button
                st.audio(filename)
                
                with open(filename, "rb") as file:
                    st.download_button(
                        label="Download Audio",
                        data=file,
                        file_name=filename,
                        mime="audio/mpeg"
                    )
                    
            except Exception as e:
                st.error(f"Error generating voice: {str(e)}")
            finally:
                # Clean up the file after download
                if os.path.exists(filename):
                    os.remove(filename)

if __name__ == "__main__":
    main() 