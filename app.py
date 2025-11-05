import streamlit as st
import requests
import tempfile
import os
import base64
import json
from datetime import datetime
import io

# Page configuration
st.set_page_config(
    page_title="AI Video Generator",
    page_icon="🎬",
    layout="wide"
)

# Title and description
st.title("🎬 AI Video Generator from Audio")
st.markdown("Upload your audio narration and generate videos using AI APIs")

# Available APIs configuration
API_OPTIONS = {
    "RunwayML": "runway",
    "Stability AI": "stability",
    "Hugging Face (Demo)": "huggingface"
}

def setup_sidebar():
    with st.sidebar:
        st.header("🔧 Configuration")
        
        # API Selection
        selected_api = st.selectbox(
            "Choose AI Video API:",
            list(API_OPTIONS.keys())
        )
        
        # API Keys based on selection
        if selected_api == "RunwayML":
            api_key = st.text_input("RunwayML API Key:", type="password")
            st.markdown("[Get RunwayML API Key](https://runwayml.com/)")
            
        elif selected_api == "Stability AI":
            api_key = st.text_input("Stability AI API Key:", type="password")
            st.markdown("[Get Stability AI API Key](https://platform.stability.ai/)")
            
        else:  # Hugging Face
            api_key = st.text_input("Hugging Face Token (optional):", type="password")
            st.markdown("[Get Hugging Face Token](https://huggingface.co/settings/tokens)")
        
        # Video settings
        st.subheader("🎥 Video Settings")
        video_style = st.selectbox(
            "Style",
            ["Realistic", "Cinematic", "Animated", "Artistic", "Documentary", "Fantasy"]
        )
        
        duration = st.slider("Duration (seconds)", 2, 10, 4)
        
        resolution = st.selectbox(
            "Resolution",
            ["512x512", "768x768", "1024x1024"]
        )
        
        st.subheader("🎨 Advanced")
        creativity = st.slider("Creativity", 0.1, 1.0, 0.7)
        
        return selected_api, api_key, {
            "style": video_style,
            "duration": duration,
            "resolution": resolution,
            "creativity": creativity
        }

def transcribe_audio(audio_file, api_key=None):
    """Transcribe audio using Whisper API"""
    try:
        # Save audio to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_audio:
            tmp_audio.write(audio_file.read())
            audio_path = tmp_audio.name
        
        # For demo purposes, we'll simulate transcription
        # In production, use OpenAI Whisper API or similar
        transcribed_text = "A person narrating a story about creating amazing videos with artificial intelligence."
        
        # Clean up
        os.unlink(audio_path)
        
        return transcribed_text
        
    except Exception as e:
        st.error(f"Transcription error: {str(e)}")
        return "A creative video showcasing technology and innovation."

def generate_video_runway(prompt, settings, api_key):
    """Generate video using RunwayML API"""
    try:
        # RunwayML API endpoint (example - check actual API docs)
        url = "https://api.runwayml.com/v1/video/generate"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "prompt": prompt,
            "duration": settings["duration"],
            "resolution": settings["resolution"],
            "style": settings["style"],
            "creativity": settings["creativity"]
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=120)
        response.raise_for_status()
        
        # Save video to temporary file
        video_content = response.content
        temp_video = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        temp_video.write(video_content)
        temp_video.close()
        
        return temp_video.name
        
    except Exception as e:
        st.error(f"RunwayML API error: {str(e)}")
        return None

def generate_video_stability(prompt, settings, api_key):
    """Generate video using Stability AI API"""
    try:
        # Stability AI API endpoint
        url = "https://api.stability.ai/v2beta/image-to-video"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
        }
        
        # For Stability AI, we might need to generate an image first, then video
        # This is a simplified example
        data = {
            "prompt": prompt,
            "cfg_scale": settings["creativity"] * 10,
            "steps": 30,
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=120)
        response.raise_for_status()
        
        # Process response and save video
        temp_video = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        temp_video.write(response.content)
        temp_video.close()
        
        return temp_video.name
        
    except Exception as e:
        st.error(f"Stability AI API error: {str(e)}")
        return None

def generate_video_huggingface(prompt, settings, api_key=None):
    """Generate video using Hugging Face models"""
    try:
        # Using a demo Hugging Face model
        # Note: This is a placeholder - actual implementation would use specific model APIs
        
        # For demo purposes, create a simple animated video
        from moviepy.editor import ColorClip, TextClip, CompositeVideoClip
        
        # Create video with text overlay
        width, height = map(int, settings["resolution"].split('x'))
        duration = settings["duration"]
        
        # Background
        background = ColorClip(
            size=(width, height), 
            color=(45, 25, 85), 
            duration=duration
        )
        
        # Text content
        text_content = f"AI Generated Video\n\nPrompt: {prompt[:100]}..."
        
        text_clip = TextClip(
            text_content,
            fontsize=24,
            color='white',
            font='Arial-Bold',
            size=(width-100, height-100)
        ).set_duration(duration).set_position('center')
        
        # Combine
        video = CompositeVideoClip([background, text_clip])
        
        # Save
        temp_video = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        video.write_videofile(
            temp_video.name,
            fps=24,
            codec='libx264',
            audio_codec='aac'
        )
        
        return temp_video.name
        
    except ImportError:
        st.error("MoviePy required for demo videos. Install with: pip install moviepy")
        return None
    except Exception as e:
        st.error(f"Hugging Face demo error: {str(e)}")
        return None

def main():
    # Setup sidebar
    selected_api, api_key, settings = setup_sidebar()
    
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
        
        # Additional context
        with st.expander("⚙️ Advanced Options"):
            negative_prompt = st.text_input(
                "Avoid in video:",
                placeholder="Things you don't want in the video...",
                help="Describe elements to avoid"
            )
            
            num_variations = st.slider("Number of variations", 1, 3, 1)

    with col2:
        st.subheader("🎬 Generated Video")
        
        if audio_file and st.button("🚀 Generate Video", use_container_width=True):
            if not api_key and selected_api != "Hugging Face (Demo)":
                st.error("🔑 API key required for selected service")
                return
            
            with st.spinner("Processing your video... This may take 1-5 minutes."):
                try:
                    # Step 1: Transcribe audio
                    with st.status("Processing audio...", expanded=True) as status:
                        transcription = transcribe_audio(audio_file, api_key)
                        st.write(f"📝 Transcription: {transcription}")
                        status.update(label="Audio processed!", state="complete")
                    
                    # Step 2: Combine with user prompt
                    final_prompt = f"{video_prompt}. Audio context: {transcription}" if video_prompt else transcription
                    
                    with st.status("Generating video...", expanded=True) as status:
                        st.write(f"🎯 Final prompt: {final_prompt}")
                        
                        # Generate video based on selected API
                        if selected_api == "RunwayML":
                            video_path = generate_video_runway(final_prompt, settings, api_key)
                        elif selected_api == "Stability AI":
                            video_path = generate_video_stability(final_prompt, settings, api_key)
                        else:
                            video_path = generate_video_huggingface(final_prompt, settings, api_key)
                        
                        status.update(label="Video generated!", state="complete")
                    
                    # Display results
                    if video_path and os.path.exists(video_path):
                        st.success("✅ Video generated successfully!")
                        
                        # Display video
                        st.video(video_path)
                        
                        # Video info
                        file_size = os.path.getsize(video_path) / (1024 * 1024)  # MB
                        st.caption(f"Video size: {file_size:.1f} MB | Duration: {settings['duration']}s")
                        
                        # Download button
                        with open(video_path, "rb") as f:
                            st.download_button(
                                "📥 Download Video",
                                f,
                                file_name=f"ai_video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4",
                                mime="video/mp4",
                                use_container_width=True
                            )
                        
                        # Clean up
                        os.unlink(video_path)
                        
                    else:
                        st.error("❌ Failed to generate video. Please try again.")
                        
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    st.info("💡 Tip: Check your API keys and try a shorter prompt")
        
        elif not audio_file:
            # Show preview/instructions
            st.info("""
            ## 🎯 How to use:
            1. **Upload** your audio narration
            2. **Describe** the video you want
            3. **Configure** settings in sidebar
            4. **Generate** your AI video!
            
            ### Supported APIs:
            - **RunwayML**: Professional video generation
            - **Stability AI**: Image-to-video technology  
            - **Hugging Face**: Demo mode (no API key needed)
            """)

# Additional features
def add_examples():
    st.markdown("---")
    st.subheader("🎨 Example Prompts")
    
    examples = st.columns(3)
    
    with examples[0]:
        if st.button("🌅 Scenic Landscape", use_container_width=True):
            st.session_state.video_prompt = "A beautiful sunset over mountains, cinematic style, warm colors, peaceful atmosphere"
    
    with examples[1]:
        if st.button("🚀 Tech Innovation", use_container_width=True):
            st.session_state.video_prompt = "Futuristic technology, holographic interfaces, blue and purple colors, modern and clean"
    
    with examples[2]:
        if st.button("🎭 Storytelling", use_container_width=True):
            st.session_state.video_prompt = "Character journey through magical forest, fantasy style, vibrant colors, emotional"

if __name__ == "__main__":
    main()
    add_examples()
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center'>
            <p>Powered by RunwayML • Stability AI • Hugging Face</p>
        </div>
        """,
        unsafe_allow_html=True
    )
