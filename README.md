# DECAMERON (Audio Transcription & Formatting Tool)

This script automates the process of transcribing audio files using OpenAI's **Whisper** and formats the resulting raw text into well-structured, highly readable documents (DOCX and PDF).

Instead of a single block of continuous text, the tool intelligently parses punctuation and randomly groups sentences into natural-looking paragraphs.

## Features
- Transcribes multiple audio files in a single run using Whisper.
- Cleans and formats raw text into human-readable paragraphs.
- Automatically generates Microsoft Word (`.docx`) and PDF (`.pdf`) files.
- Includes pre-execution dependency checks to prevent failures after long transcriptions.

## Requirements
Ensure you have Python installed, along with the command-line version of `whisper` and the required Python libraries.

Create a `requirements.txt` file in your directory:

```text
openai-whisper
python-docx
fpdf2
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

*Note: You also need `ffmpeg` installed on your system for Whisper to process audio files.*

## Usage
Run the script from your terminal, passing the audio file(s) and any desired flags.

**Basic Usage (defaults to Medium model, Spanish, DOCX output):**
```bash
python formatter.py "audio_file.m4a"
```

**Specify Model and Language:**
```bash
python formatter.py "interview.mp3" --model large --language en
```

**Choose Output Formats (DOCX, PDF, or both):**
```bash
python formatter.py "recording.wav" --docx
python formatter.py "recording.wav" --pdf
python formatter.py "recording.wav" --docx --pdf
```

**Process Multiple Files at Once:**
```bash
python formatter.py "audio1.m4a" "audio2.m4a" --model medium --docx --pdf
```