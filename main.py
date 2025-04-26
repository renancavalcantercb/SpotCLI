import os
import sys
import time
from typing import Optional

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Spotify API Configuration
SPOTIFY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI', 'http://127.0.0.1:8888/callback')
SPOTIFY_SCOPE = "user-read-playback-state,user-modify-playback-state,user-read-currently-playing,playlist-read-private"

# Initialize Rich console
console = Console()

def setup_spotify() -> Optional[spotipy.Spotify]:
    """Configure Spotify authentication."""
    if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
        console.print("[bold red]Error: Spotify credentials not configured![/bold red]")
        console.print("Please set the following environment variables:")
        console.print("  - SPOTIPY_CLIENT_ID")
        console.print("  - SPOTIPY_CLIENT_SECRET")
        console.print("  - SPOTIPY_REDIRECT_URI (optional, default: http://127.0.0.1:8888/callback)")
        sys.exit(1)
    
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
            redirect_uri=SPOTIFY_REDIRECT_URI,
            scope=SPOTIFY_SCOPE
        ))
        return sp
    except Exception as e:
        console.print(f"[bold red]Error authenticating with Spotify: {e}[/bold red]")
        sys.exit(1)

def display_menu() -> str:
    """Display the main menu and get user input."""
    console.clear()
    console.print("[bold green]===== Spotify CLI Player =====[/bold green]")
    console.print("1. Play/Pause")
    console.print("2. Next Track")
    console.print("3. Previous Track")
    console.print("4. Search Track")
    console.print("5. My Playlists")
    console.print("6. Current Track Info")
    console.print("7. Adjust Volume")
    console.print("0. Exit")
    return console.input("[bold cyan]Choose an option: [/bold cyan]")

def toggle_playback(sp: spotipy.Spotify) -> None:
    """Toggle between play and pause."""
    try:
        status = sp.current_playback()
        if status and status['is_playing']:
            sp.pause_playback()
            console.print("[yellow]Playback paused[/yellow]")
        else:
            sp.start_playback()
            console.print("[green]Playback started[/green]")
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
    
    time.sleep(1)

def next_track(sp: spotipy.Spotify) -> None:
    """Skip to the next track."""
    try:
        sp.next_track()
        console.print("[green]Skipped to next track[/green]")
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
    
    time.sleep(1)

def previous_track(sp: spotipy.Spotify) -> None:
    """Go back to the previous track."""
    try:
        sp.previous_track()
        console.print("[green]Returned to previous track[/green]")
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
    
    time.sleep(1)

def search_track(sp: spotipy.Spotify) -> None:
    """Search and play a track."""
    query = console.input("[bold cyan]Enter track name or artist: [/bold cyan]")
    
    if not query:
        return
    
    try:
        with Progress() as progress:
            task = progress.add_task("[cyan]Searching...", total=1)
            results = sp.search(q=query, limit=10)
            progress.update(task, completed=1)
        
        tracks = results['tracks']['items']
        
        if not tracks:
            console.print("[yellow]No tracks found.[/yellow]")
            time.sleep(2)
            return
        
        table = Table(title=f"Results for '{query}'")
        table.add_column("#", style="dim")
        table.add_column("Name", style="cyan")
        table.add_column("Artist", style="green")
        table.add_column("Album", style="yellow")
        
        for i, track in enumerate(tracks, 1):
            artists = ", ".join([artist['name'] for artist in track['artists']])
            table.add_row(
                str(i),
                track['name'],
                artists,
                track['album']['name']
            )
        
        console.print(table)
        
        choice = console.input("[bold cyan]Choose a track to play (1-10) or 0 to go back: [/bold cyan]")
        
        if choice.isdigit() and 1 <= int(choice) <= len(tracks):
            track_uri = tracks[int(choice) - 1]['uri']
            sp.start_playback(uris=[track_uri])
            console.print(f"[green]Now playing: {tracks[int(choice) - 1]['name']}[/green]")
            time.sleep(2)
    
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        time.sleep(2)

def list_playlists(sp: spotipy.Spotify) -> None:
    """List and play user's playlists."""
    try:
        with Progress() as progress:
            task = progress.add_task("[cyan]Loading playlists...", total=1)
            playlists = sp.current_user_playlists()
            progress.update(task, completed=1)
        
        if not playlists['items']:
            console.print("[yellow]No playlists found.[/yellow]")
            time.sleep(2)
            return
        
        table = Table(title="Your Playlists")
        table.add_column("#", style="dim")
        table.add_column("Name", style="cyan")
        table.add_column("Tracks", style="green")
        
        for i, playlist in enumerate(playlists['items'], 1):
            table.add_row(
                str(i),
                playlist['name'],
                str(playlist['tracks']['total'])
            )
        
        console.print(table)
        
        choice = console.input("[bold cyan]Choose a playlist to play (1-10) or 0 to go back: [/bold cyan]")
        
        if choice.isdigit() and 1 <= int(choice) <= len(playlists['items']):
            playlist_uri = playlists['items'][int(choice) - 1]['uri']
            sp.start_playback(context_uri=playlist_uri)
            console.print(f"[green]Now playing playlist: {playlists['items'][int(choice) - 1]['name']}[/green]")
            time.sleep(2)
    
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        time.sleep(2)

def show_current_track(sp: spotipy.Spotify) -> None:
    """Display information about the currently playing track."""
    try:
        current = sp.current_playback()
        
        if not current or not current.get('item'):
            console.print("[yellow]No track currently playing.[/yellow]")
            time.sleep(2)
            return
        
        track = current['item']
        artists = ", ".join([artist['name'] for artist in track['artists']])
        
        console.print("[bold green]Now Playing:[/bold green]")
        console.print(f"[cyan]Track:[/cyan] {track['name']}")
        console.print(f"[cyan]Artist:[/cyan] {artists}")
        console.print(f"[cyan]Album:[/cyan] {track['album']['name']}")
        
        # Calculate track progress
        progress_ms = current['progress_ms']
        duration_ms = track['duration_ms']
        progress_percent = (progress_ms / duration_ms) * 100
        
        # Format time in minutes:seconds
        progress_sec = progress_ms // 1000
        duration_sec = duration_ms // 1000
        progress_str = f"{progress_sec // 60}:{progress_sec % 60:02d}"
        duration_str = f"{duration_sec // 60}:{duration_sec % 60:02d}"
        
        console.print(f"[cyan]Progress:[/cyan] {progress_str}/{duration_str} ({progress_percent:.1f}%)")
        
        # Show shuffle and repeat states
        if current.get('shuffle_state'):
            console.print("[cyan]Shuffle:[/cyan] [green]On[/green]")
        else:
            console.print("[cyan]Shuffle:[/cyan] [red]Off[/red]")
        
        repeat_state = current.get('repeat_state', 'off')
        if repeat_state == 'off':
            console.print("[cyan]Repeat:[/cyan] [red]Off[/red]")
        elif repeat_state == 'track':
            console.print("[cyan]Repeat:[/cyan] [green]Track[/green]")
        elif repeat_state == 'context':
            console.print("[cyan]Repeat:[/cyan] [green]Playlist/Album[/green]")
        
        console.input("\n[bold cyan]Press Enter to return to menu...[/bold cyan]")
    
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        time.sleep(2)

def adjust_volume(sp: spotipy.Spotify) -> None:
    """Adjust the playback volume."""
    try:
        current = sp.current_playback()
        if not current:
            console.print("[yellow]No active device found.[/yellow]")
            time.sleep(2)
            return
        
        current_volume = current['device']['volume_percent']
        console.print(f"[cyan]Current volume:[/cyan] {current_volume}%")
        
        new_volume = console.input("[bold cyan]Enter new volume (0-100): [/bold cyan]")
        
        if new_volume.isdigit() and 0 <= int(new_volume) <= 100:
            sp.volume(int(new_volume))
            console.print(f"[green]Volume adjusted to {new_volume}%[/green]")
        else:
            console.print("[yellow]Invalid value. Volume must be between 0 and 100.[/yellow]")
        
        time.sleep(1)
    
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        time.sleep(2)

def main() -> None:
    """Main function of the player."""
    console.print("[bold green]Starting Spotify CLI Player...[/bold green]")
    
    try:
        sp = setup_spotify()
        
        while True:
            option = display_menu()
            
            if option == '1':
                toggle_playback(sp)
            elif option == '2':
                next_track(sp)
            elif option == '3':
                previous_track(sp)
            elif option == '4':
                search_track(sp)
            elif option == '5':
                list_playlists(sp)
            elif option == '6':
                show_current_track(sp)
            elif option == '7':
                adjust_volume(sp)
            elif option == '0':
                console.print("[bold green]Exiting Spotify CLI Player. Goodbye![/bold green]")
                break
            else:
                console.print("[bold red]Invalid option. Please try again.[/bold red]")
                time.sleep(1)
    
    except KeyboardInterrupt:
        console.print("\n[bold green]Program interrupted. Goodbye![/bold green]")
    except Exception as e:
        console.print(f"[bold red]Unexpected error: {e}[/bold red]")

if __name__ == "__main__":
    main()
