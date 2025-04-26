# SpotCLI

A command-line interface (CLI) player for Spotify that allows you to control your Spotify playback directly from the terminal.

## Features

- 🎵 Play/Pause tracks
- ⏭️ Skip to next track
- ⏮️ Go to previous track
- 🔍 Search and play tracks
- 📋 List and play your playlists
- ℹ️ Display current track information
- 🔊 Adjust playback volume
- 🎨 Beautiful terminal interface with Rich

## Prerequisites

- Python 3.8 or higher
- A Spotify account
- Spotify Premium subscription (required for playback control)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/renancavalcantercb/SpotCLI.git
cd SpotCLI
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with your Spotify credentials:
```env
SPOTIPY_CLIENT_ID=your_client_id_here
SPOTIPY_CLIENT_SECRET=your_client_secret_here
SPOTIPY_REDIRECT_URI=http://127.0.0.1:8888/callback
```

## Getting Spotify Credentials

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Log in with your Spotify account
3. Create a new application
4. Copy the Client ID and Client Secret
5. Add `http://127.0.0.1:8888/callback` to the Redirect URIs in your app settings

## Usage

1. Make sure you have an active Spotify device (desktop app, web player, or mobile app)
2. Run the player:
```bash
python main.py
```

3. Use the menu options to control your Spotify playback:
   - 1: Play/Pause
   - 2: Next Track
   - 3: Previous Track
   - 4: Search Track
   - 5: My Playlists
   - 6: Current Track Info
   - 7: Adjust Volume
   - 0: Exit

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- [Spotipy](https://github.com/plamere/spotipy) - Python library for the Spotify Web API
- [Rich](https://github.com/Textualize/rich) - Python library for rich text and beautiful formatting in the terminal 