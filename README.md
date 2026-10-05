# DECAMERON

**[English](#english) · [Español](#español)**

---

## English

### Audio Transcription & Formatting Tool

This script automates the process of transcribing audio files using OpenAI's **Whisper** and formats the resulting raw text into well-structured, highly readable documents (DOCX and PDF).

Instead of a single block of continuous text, the tool intelligently parses punctuation and randomly groups sentences into natural-looking paragraphs.

### Features

- Transcribes multiple audio files in a single run using Whisper.
- Cleans and formats raw text into human-readable paragraphs.
- Generates Microsoft Word (`.docx`) and PDF (`.pdf`) files, both by default.
- Each document starts with the file name as a title and the date and time of the conversion.
- Saves each conversion in its own folder, with a `README.txt` recording when it was made.
- Includes pre-execution dependency checks to prevent failures after long transcriptions.

### Requirements

Ensure you have Python installed, along with the command-line version of `whisper` and the required Python libraries.

The repository includes a `requirements.txt` file:

```text
openai-whisper
python-docx
fpdf2
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

_Note: You also need `ffmpeg` installed on your system for Whisper to process audio files._

### Usage

Run the script from your terminal, passing the audio file(s) and any desired flags.

**Basic Usage (defaults to Medium model, Spanish, DOCX and PDF output):**

```bash
python3 decameron.py "audio_file.m4a"
```

**Specify Model and Language:**

```bash
python3 decameron.py "interview.mp3" --model large --language en
```

**Generate Only One Format:**

```bash
python3 decameron.py "recording.wav" --docx
python3 decameron.py "recording.wav" --pdf
```

**Process Multiple Files at Once:**

```bash
python3 decameron.py "audio1.m4a" "audio2.m4a" --model medium
```

_Tip: always quote file names that contain spaces or brackets, e.g. `"[Info] [Título] - random quote.m4a"`._

### Where files go

The audio files can be anywhere: pass a file name if it is in the current folder, or a full path otherwise (e.g. `~/Downloads/interview.m4a`).

The results are saved in a `converted` folder inside the folder where you run the command. Each audio file gets its own subfolder, named after the file without its extension:

```text
converted/
└── interview/
    ├── README.txt       ← date and time of the conversion, source file, model, language
    ├── interview.docx
    ├── interview.pdf
    └── interview.txt    ← raw Whisper transcript (plus .srt, .vtt, .tsv, .json)
```

Each DOCX and PDF document contains:

- The file name as a level-1 heading.
- A blank line.
- The date and time of the conversion as a level-3 heading.
- A blank line, and the formatted transcript.

Use `-o` / `--output-dir` to use another base folder instead of `converted`; it is created if it doesn't exist:

```bash
python3 decameron.py ~/Downloads/interview.m4a -o ~/Documents/transcripts
```

Converting the same file again overwrites the contents of its subfolder.

The script exits with code `0` when every file was processed and `1` if any file failed or a dependency is missing.

---

## Español

### Herramienta de transcripción y formato de audio

Este script automatiza la transcripción de archivos de audio con **Whisper** de OpenAI y convierte el texto en bruto resultante en documentos bien estructurados y fáciles de leer (DOCX y PDF).

En lugar de un único bloque de texto continuo, la herramienta analiza la puntuación y agrupa las oraciones de forma aleatoria en párrafos de aspecto natural.

### Características

- Transcribe varios archivos de audio en una sola ejecución con Whisper.
- Limpia el texto en bruto y lo organiza en párrafos legibles.
- Genera archivos de Microsoft Word (`.docx`) y PDF (`.pdf`), ambos por defecto.
- Cada documento empieza con el nombre del archivo como título y la fecha y hora de la conversión.
- Guarda cada conversión en su propia carpeta, con un `README.txt` que indica cuándo se hizo.
- Comprueba las dependencias antes de empezar, para evitar fallos después de una transcripción larga.

### Requisitos

Asegúrate de tener Python instalado, junto con la versión de línea de comandos de `whisper` y las bibliotecas de Python necesarias.

El repositorio incluye un archivo `requirements.txt`:

```text
openai-whisper
python-docx
fpdf2
```

Instala las dependencias:

```bash
pip install -r requirements.txt
```

_Nota: también necesitas tener `ffmpeg` instalado en tu sistema para que Whisper pueda procesar los archivos de audio._

### Uso

Ejecuta el script desde la terminal, indicando el o los archivos de audio y las opciones que quieras.

**Uso básico (por defecto: modelo medium, español, salida DOCX y PDF):**

```bash
python3 decameron.py "archivo_de_audio.m4a"
```

**Indicar modelo e idioma:**

```bash
python3 decameron.py "entrevista.mp3" --model large --language en
```

**Generar un solo formato:**

```bash
python3 decameron.py "grabacion.wav" --docx
python3 decameron.py "grabacion.wav" --pdf
```

**Procesar varios archivos a la vez:**

```bash
python3 decameron.py "audio1.m4a" "audio2.m4a" --model medium
```

_Consejo: pon siempre entre comillas los nombres de archivo con espacios o corchetes, por ejemplo `"[Info] [Título] - random quote.m4a"`._

### Dónde se guardan los archivos

Los audios pueden estar en cualquier carpeta: indica solo el nombre si están en la carpeta actual, o la ruta completa en caso contrario (por ejemplo, `~/Downloads/entrevista.m4a`).

Los resultados se guardan en una carpeta `converted` dentro de la carpeta desde donde ejecutas el comando. Cada audio tiene su propia subcarpeta, con el nombre del archivo sin extensión:

```text
converted/
└── entrevista/
    ├── README.txt        ← fecha y hora de la conversión, archivo de origen, modelo, idioma
    ├── entrevista.docx
    ├── entrevista.pdf
    └── entrevista.txt    ← transcripción en bruto de Whisper (más .srt, .vtt, .tsv, .json)
```

Cada documento DOCX y PDF contiene:

- Nombre del archivo como encabezado de nivel 1.
- Línea en blanco.
- Fecha y hora de la conversión como encabezado de nivel 3.
- Otra línea en blanco y la transcripción con formato.

Usa `-o` / `--output-dir` para usar otra carpeta base en lugar de `converted`; se crea si no existe:

```bash
python3 decameron.py ~/Downloads/entrevista.m4a -o ~/Documents/transcripciones
```

Si conviertes el mismo archivo otra vez, se sobrescribe el contenido de su subcarpeta.

El script termina con código `0` si todos los archivos se procesaron correctamente y con `1` si alguno falló o falta alguna dependencia.
