import streamlit as st
import requests
import tempfile
import os
import base64
import json
from datetime import datetime
import io
import google.generativeai as genai

# Page configuration
st.set_page_config(
    page_title="AI Video Generator",
    page_icon="🎬",
    layout="wide"
)

# Title and description
st.title("🎬 AI Video Generator from Audio")
st.markdown("Upload your audio narration and generate video concepts using AI")

def setup_sidebar():
    with st.sidebar:
        st.header("🔧 Configuration")
        
        # API Key
        api_key = st.text_input("Google AI Studio API Key:", type="password")
        st.markdown("[Get your API key](https://aistudio.google.com/)")
        
        # Video settings
        st.subheader("🎥 Video Settings")
        video_style = st.selectbox(
            "Style",
            ["Realistic", "Cinematic", "Animated", "Artistic", "Documentary", "Fantasy"]
        )
        
        st.subheader("🎨 Advanced")
        creativity = st.slider("Creativity", 0.1, 1.0, 0.7)
        
        return api_key, {
            "style": video_style,
            "creativity": creativity
        }

def transcribe_audio_simulation(audio_file):
    """Simulate audio transcription - in production, use actual speech-to-text"""
    return "A person narrating a story about creating amazing content with artificial intelligence."

def generate_video_concept(transcription, user_prompt, settings, api_key):
    """Generate video concept using Gemini"""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"""
        Create a detailed video concept based on this audio transcription and user description.
        
        AUDIO TRANSCRIPTION: {transcription}
        
        USER DESCRIPTION: {user_prompt}
        
        STYLE: {settings['style']}
        
        Please provide:
        1. A compelling video title
        2. Detailed scene-by-scene description
        3. Visual style guidance
        4. Color palette suggestions
        5. Recommended camera angles and movements
        
        Make it creative and engaging!
        """
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        st.error(f"Gemini API error: {str(e)}")
        return None

def create_concept_display(concept_text):
    """Create a beautiful display for the video concept"""
    st.subheader("🎬 Generated Video Concept")
    
    # Split the concept into sections
    lines = concept_text.split('\n')
    
    with st.container():
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Display the main concept
            st.markdown("### 📋 Video Plan")
            concept_display = ""
            for line in lines:
                if line.strip():
                    if any(keyword in line.lower() for keyword in ['title:', 'scene', 'palette', 'angles']):
                        st.markdown(f"**{line}**")
                    else:
                        st.markdown(line)
            
        with col2:
            # Create a visual representation
            st.markdown("### 🎨 Visual Elements")
            
            # Color palette simulation
            st.markdown("**Color Palette:**")
            colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7"]
            color_html = "<div style='display: flex; gap: 5px; margin: 10px 0;'>"
            for color in colors[:3]:
                color_html += f"<div style='width: 30px; height: 30px; background-color: {color}; border-radius: 4px;'></div>"
            color_html += "</div>"
            st.markdown(color_html, unsafe_allow_html=True)
            
            # Style indicators
            st.markdown("**Style Tags:**")
            tags = ["Cinematic", "Dynamic", "Emotional", "Professional"]
            tags_html = "<div style='display: flex; flex-wrap: wrap; gap: 5px; margin: 10px 0;'>"
            for tag in tags:
                tags_html += f"<span style='background: #4ECDC4; color: white; padding: 4px 8px; border-radius: 12px; font-size: 12px;'>{tag}</span>"
            tags_html += "</div>"
            st.markdown(tags_html, unsafe_allow_html=True)

def main():
    # Setup sidebar
    api_key, settings = setup_sidebar()
    
    # Main content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🎤 Upload Audio")
        audio_file = st.file_uploader(
            "Choose an audio file",
            type=['mp3', 'wav', 'm4a', 'ogg'],
            help="Upload your narration audio file"
        )
        
        if audio_file:
            st.audio(audio_file, format=audio_file.type)
            
            # Audio info
            file_size = len(audio_file.getvalue()) / 1024  # KB
            st.info(f"File size: {file_size:.1f} KB")
        
        st.subheader("📝 Video Description")
        video_prompt = st.text_area(
            "Describe your video:",
            placeholder="Describe the scenes, mood, characters, and style you want...",
            height=120,
            help="This will be combined with your audio transcription"
        )

    with col2:
        st.subheader("🎬 Video Concept")
        
        if audio_file and video_prompt:
            if not api_key:
                st.error("🔑 Please enter your Google AI Studio API key")
                return
                
            if st.button("🚀 Generate Video Concept", use_container_width=True):
                with st.spinner("Creating your video concept..."):
                    try:
                        # Step 1: Simulate audio transcription
                        transcription = transcribe_audio_simulation(audio_file)
                        
                        # Step 2: Generate video concept
                        concept = generate_video_concept(
                            transcription, 
                            video_prompt, 
                            settings, 
                            api_key
                        )
                        
                        if concept:
                            st.success("✅ Video concept generated successfully!")
                            create_concept_display(concept)
                            
                            # Download concept as text file
                            st.download_button(
                                "📥 Download Concept",
                                concept,
                                file_name=f"video_concept_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                                mime="text/plain",
                                use_container_width=True
                            )
                        else:
                            st.error("❌ Failed to generate concept. Please try again.")
                            
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
        
        elif not audio_file:
            # Show instructions
            st.info("""
            ## 🎯 How to use:
            1. **Upload** your audio narration
            2. **Describe** the video you want
            3. **Enter** your Google AI Studio API key
            4. **Generate** your video concept!
            
            ### What you'll get:
            - 📝 Detailed scene descriptions
            - 🎨 Visual style guidance  
            - 🎬 Camera angle suggestions
            - 🌈 Color palette ideas
            - ✨ Creative direction
            """)

# Add examples section
def add_examples():
    st.markdown("---")
    st.subheader("🎨 Example Prompts")
    
    examples = st.columns(3)
    
    example_prompts = {
        "🌅 Scenic Landscape": "A beautiful sunset over mountains, cinematic style, warm colors, peaceful atmosphere",
        "🚀 Tech Innovation": "Futuristic technology, holographic interfaces, blue and purple colors, modern and clean",
        "🎭 Storytelling": "Character journey through magical forest, fantasy style, vibrant colors, emotional"
    }
    
    for col, (title, prompt) in zip(examples, example_prompts.items()):
        with col:
            if st.button(title, use_container_width=True):
                st.session_state.video_prompt = prompt
                st.rerun()

if __name__ == "__main__":
    main()
    add_examples()
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center'>
            <p>Powered by Google Gemini AI • Generates detailed video concepts and storyboards</p>
        </div>
        """,
        unsafe_allow_html=True
    )
