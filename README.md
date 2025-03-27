# AI Video Editor

A powerful Python-based video editing tool that leverages AI to process, transcribe, and enhance video content. This tool automates the video editing process by analyzing content, generating summaries, and creating engaging video segments. It also generates social media content for LinkedIn and Threads, automatically posting them as comments on Trello cards.

## Features

- 🎥 Video Processing: Extract and process video content
- 🎵 Audio Extraction: Separate audio from video files
- 🗣️ Transcription: Convert speech to text using OpenAI's Whisper
- 📝 Text Analysis: Analyze content using AI for better understanding
- ✂️ Video Editing: Automatically edit and segment videos
- 🤖 AI Integration: Leverage OpenAI's capabilities for content enhancement
- 🔄 Content Generation: Generate summaries and highlights
- 📱 Social Media: Generate optimized content for LinkedIn and Threads
- 📋 Trello Integration: Automatically post content as Trello card comments

## Prerequisites

- Python 3.8 or higher
- FFmpeg (for video processing)
- OpenAI API key
- Trello API credentials

## Installation

### Quick Start

The easiest way to get started is using the provided Makefile:

```bash
# Clone the repository
git clone https://github.com/guilherme-toti/video-editor.git
cd video-editor

# Set up the environment and install dependencies
make setup
```

This will:

1. Create a virtual environment
2. Install all dependencies
3. Set up pre-commit hooks
4. Create a `.env` file from the example if it doesn't exist

### Manual Installation

If you prefer to set up manually:

1. Clone the repository:

```bash
git clone https://github.com/guilherme-toti/video-editor.git
cd video-editor
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up environment variables:

```bash
cp .env.example .env
# Edit .env with your OpenAI API key, Trello credentials, and other configurations
```

## Usage

### Workflow

1. Create a Trello card for your video
2. Use the "API Developer ID Helper (by Sensum365)" Trello Power Up to get the Card ID
3. Rename your video file to include the Trello card ID (e.g., "67cc79f9b57bbf8b65d9409d.mov")
4. Place the video file in the `data/raw` directory
5. Run the video processor:

```bash
# Using make
make run

# Or directly
python main.py
```

The script will:

- Process the video
- Generate social media content
- Automatically post the content as comments on the corresponding Trello card

The processed videos will be saved in the `data/output` directory.

### Available Make Commands

The project includes several useful make commands:

```bash
make setup      # Create virtual environment and install dependencies
make install    # Install dependencies only
make run        # Run the video processor
make lint       # Run linting
make format     # Auto-format code with black
make env        # Create .env file from example if it doesn't exist
make help       # Show all available commands
```

## Project Structure

```
video-editor/
├── src/
│   ├── config/         # Configuration settings
│   ├── core/           # Core processing logic
│   ├── services/       # Service implementations
│   ├── prompts/        # AI prompt templates
│   └── utils.py        # Utility functions
├── data/               # Data directories
├── main.py            # Main entry point
├── requirements.txt   # Project dependencies
└── .env              # Environment variables
```

## Configuration

The project can be configured through the following:

- `.env` file: API keys and environment-specific settings
- `src/config/settings.py`: Application-wide settings

## Development

### Running Tests

```bash
pytest
```

### Code Quality

This project uses pre-commit hooks for code quality. Install them with:

```bash
pre-commit install
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for providing the Whisper model and API
- FFmpeg for video processing capabilities
