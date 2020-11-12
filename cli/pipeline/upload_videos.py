__all__ = ['upload_videos']

from simple_youtube_api.Channel import Channel
from simple_youtube_api.LocalVideo import LocalVideo

from cli import settings
from cli.structures import Job


def upload_videos(job: Job):
    video = job['video']
    metadata = job['metadata']

    channel = Channel()
    channel.login(
        settings.youtube()['client_secret'],
        settings.youtube()['credentials']
    )

    playlist_id = get_or_create_playlist(metadata['course'], channel)

    video = LocalVideo(file_path=video)
    video.set_title(f"[{metadata['course']}] {metadata['title']} - {metadata['subject']}")
    video.set_description(f"Recorded on {metadata['date']}")
    video.set_default_language("en-US")
    video.set_privacy_status("private")

    video = channel.upload_video(video)
    channel.add_video_to_playlist(playlist_id, video)

    return {
        'playlist_id': playlist_id,
        'video_id': video.id
    }


def get_or_create_playlist(name: str, channel: Channel) -> str:
    # Loop through playlists to find the desired one
    print(f'Searching for playlist {name}')
    request = channel.channel.playlists().list(
        part="snippet",
        mine=True,
        maxResults=50
    )
    while request:
        response = request.execute()
        for item in response.get("items", []):
            id = item['id']
            title = item['snippet']['title']
            if title == name:
                print(f'Found playlist {name} with id: {id}')
                return id

            request = channel.channel.playlists().list_next(request, response)

    print(f'Playlist is not found. Creating new playlist {name}')
    response = channel.channel.playlists().insert(
        part='snippet,status',
        body=dict(
            snippet=dict(
                title=name,
                description=name
            ),
            status=dict(
                privacyStatus='private'
            )
        )
    ).execute()

    id = response['id']
    print(f'Created playlist {name} with id: {id}')
    return id
