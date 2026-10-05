import os
import re
import argparse
import random
import subprocess
import sys
from pathlib import Path
from typing import List, Optional



# COLORS
class Color:
    BOLD = "\033[1m"
    RESET = "\033[0m"
    GREEN = "\033[38;2;0;255;0m"   # #00FF00
    NAVY = "\033[38;2;0;49;83m"    # #003153

# Optional libraries for DOCX and PDF generation
try:
    from docx import Document
except ImportError:
    Document = None

try:
    from fpdf import FPDF
except ImportError:
    FPDF = None


def format_text_to_paragraphs(text: str) -> str:
    """Cleans up the text and groups sentences into paragraphs of random size."""
    # Remove line breaks and normalize multiple spaces into a single space
    clean_text = text.replace('\n', ' ')
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()
    
    # Split the text by sentences (looking for ., !, or ? followed by a space)
    sentences = re.split(r'(?<=[.!?])\s+', clean_text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    paragraphs = []
    while sentences:
        # Randomly choose paragraph size between 2 and 5 sentences
        paragraph_size = random.randint(2, 5)
        group = sentences[:paragraph_size]
        paragraphs.append(' '.join(group))
        
        # Remove the used sentences from the list
        sentences = sentences[paragraph_size:]
        
    return '\n\n'.join(paragraphs)


def save_as_docx(text: str, file_path: str) -> None:
    """Saves the formatted text into a Microsoft Word (.docx) document."""
    doc = Document()
    for paragraph in text.split('\n\n'):
        doc.add_paragraph(paragraph)
    doc.save(file_path)


def save_as_pdf(text: str, file_path: str) -> None:
    """Saves the formatted text into a PDF document."""
    pdf = FPDF()
    pdf.add_page()
    # Helvetica handles basic Latin characters and accents natively
    pdf.set_font("helvetica", size=11) 
    
    for paragraph in text.split('\n\n'):
        pdf.multi_cell(0, 6, text=paragraph)
        pdf.ln(4) # Extra space between paragraphs
        
    pdf.output(file_path)


def run_whisper(audio_file: str, model: str, language: str) -> Optional[Path]:
    """Executes the native Whisper CLI command and returns the path to the text file."""
    print(f"\n🎙️ Transcribing with Whisper: {audio_file}...")
    
    # Set output directory to current working directory to easily locate the txt file
    output_dir = Path.cwd()
    
    command = [
        "whisper",
        audio_file,
        "--model", model,
        "--language", language,
        "--output_dir", str(output_dir)
    ]
    
    try:
        subprocess.run(command, check=True)
        base_name = Path(audio_file).stem
        generated_txt = output_dir / f"{base_name}.txt"
        return generated_txt
    except FileNotFoundError:
        print("❌ Error: 'whisper' command not found. Ensure it is installed and available in your PATH.")
        return None
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during the transcription of '{audio_file}': {e}")
        return None


def process_audio(audio_file: str, model: str, language: str, export_formats: List[str]) -> None:
    """Handles the complete pipeline: transcription, formatting, and file generation."""
    if not os.path.exists(audio_file):
        print(f"❌ The audio file '{audio_file}' does not exist.")
        return

    # 1. Execute Whisper
    txt_file_path = run_whisper(audio_file, model, language)
    
    if not txt_file_path or not txt_file_path.exists():
        print(f"⚠️ Could not find the .txt transcription for '{audio_file}'.")
        return

    # 2. Read the raw transcription
    with open(txt_file_path, 'r', encoding='utf-8') as f:
        raw_content = f.read()

    # 3. Format the text
    print(f"⚙️ Creating structured version for '{audio_file}'...")
    formatted_text = format_text_to_paragraphs(raw_content)

    # 4. Generate the requested documents
    base_name = Path(audio_file).stem

    for fmt in export_formats:
        output_file = f"{base_name}.{fmt}"
        
        try:
            if fmt == 'docx':
                save_as_docx(formatted_text, output_file)
            elif fmt == 'pdf':
                save_as_pdf(formatted_text, output_file)
            print(f"   ✅ Successfully exported: {output_file}")
        except Exception as e:
            print(f"   ❌ Error exporting to .{fmt}: {e}")


if __name__ == "__main__":
    print(f"\n{Color.BOLD}DECAMERON{Color.RESET}")
    print("(Audio Transcription & Formatting Tool)")
    print("==================================================")
    print("==================================================")
    print("==================================================")
    parser = argparse.ArgumentParser(description="Transcribes audio using Whisper and exports to DOCX or PDF with proper formatting.")
    
    parser.add_argument("files", nargs="+", help="Paths to the audio files to process.")
    parser.add_argument("--model", default="medium", help="Whisper model to use (e.g., small, medium, large). Default: medium")
    parser.add_argument("--language", default="es", help="Language of the audio. Default: es (Spanish)")
    
    # Direct flags for output formats
    parser.add_argument("--docx", action="store_true", help="Generate a formatted Word (.docx) file")
    parser.add_argument("--pdf", action="store_true", help="Generate a formatted PDF (.pdf) file")
    
    args = parser.parse_args()

    # Determine which formats to export
    formats = []
    if args.docx:
        formats.append("docx")
    if args.pdf:
        formats.append("pdf")
        
    # If no flag is provided, default to DOCX
    if not formats:
        formats = ["docx"]

    # =========================================================================
    # DEPENDENCY CHECK (RUNS BEFORE TRANSCRIPTION STARTS)
    # =========================================================================
    missing_libraries = []
    
    if "docx" in formats and Document is None:
        missing_libraries.append("python-docx")
    if "pdf" in formats and FPDF is None:
        missing_libraries.append("fpdf2")

    if missing_libraries:
        print("\n❌ ABORTED: Missing dependencies for the requested output formats.")
        for lib in missing_libraries:
            print(f"   - Missing module: {lib}")
        print(f"\n💡 Solution: Install them by running:\n   pip install {' '.join(missing_libraries)}")
        print("   or install everything using:\n   pip install -r requirements.txt\n")
        sys.exit(1) # Exits the script immediately
    # =========================================================================

    # Process each provided audio file
    for audio in args.files:
        process_audio(audio, args.model, args.language, formats)

    print("\n==================================================")
    print("🎉 All audio files have been processed successfully!")
    print("==================================================\n")