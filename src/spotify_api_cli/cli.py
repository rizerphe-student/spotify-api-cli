"""A very simple CLI for getting some data from spotify"""
import os

import click
import dotenv
from spotify_minimal_client import Spotify

dotenv.load_dotenv()


@click.group()
@click.option(
    "--client-id",
    prompt="Client ID",
    help="The client ID for your app",
    hide_input=True,
    default=os.getenv("CLIENT_ID", ""),
)
@click.option(
    "--client-secret",
    prompt="Client Secret",
    help="The client secret for your app",
    hide_input=True,
    default=os.getenv("CLIENT_SECRET", ""),
)
@click.pass_context
def cli(ctx, client_id: str, client_secret: str) -> None:
    """A very simple CLI for getting some data from spotify"""
    ctx.obj = Spotify(client_id, client_secret)


@cli.group()
def albums() -> None:
    """Get spotify album data"""


@albums.command()
@click.argument("album_id")
@click.pass_obj
def get(spotify: Spotify, album_id: str) -> None:
    """Get an album by id"""
    album = spotify.albums[album_id]
    print(album.name)
    for track in album.tracks:
        print(f"  ({track.id}) {track.name}")


@cli.group()
def artists() -> None:
    """Get spotify artist data"""


@artists.command()
@click.argument("artist_id")
@click.option(
    "--country", type=str, default="US", help="The country to get the data for"
)
@click.pass_obj
def get(spotify: Spotify, artist_id: str, country: str) -> None:
    """Get an artist by id"""
    artist = spotify.artists[artist_id]
    print(artist.name)
    for track in artist.top_tracks(country):
        print(f"  ({track.id}) {track.name}")


@artists.command()
@click.argument("query")
@click.pass_obj
def search(spotify: Spotify, query: str) -> None:
    """Search for an artist"""
    results = spotify.artists.search(query)
    for artist in results:
        print(f"({artist.id}) {artist.name}")


if __name__ == "__main__":
    cli()
