from django.shortcuts import render
from pytube import YouTube
import os
import locale

def download_video(url, download_path, quality):
    try:
        yt = YouTube(url)
        if quality == 'mp3':
            audio_streams = yt.streams.filter(only_audio=True)
            if not audio_streams:
                video_path = None
            else:
                video = audio_streams.first()
                title = yt.title
                video_path = os.path.join(download_path, f"{title}.{video.subtype}")
                video.download(download_path, filename=title)
        else:
            video = yt.streams.filter(file_extension='mp4', resolution=quality).first()
            title = yt.title
            video_path = os.path.join(download_path, f"{title}.{video.subtype}")
            video.download(download_path, filename=title)

        return video_path

    except ValueError as ve:
        raise ve 

    except Exception as e:
        raise e

def get_default_download_folder():
    if os.name == 'posix':  # Linux
        return os.path.expanduser('~/Downloads')
    elif os.name == 'nt':  # Windows
        return os.path.join(os.path.expanduser('~'), 'Downloads')
    elif os.name == 'mac':  # macOS
        return os.path.join(os.path.expanduser('~'), 'Downloads')
    else:
        return None  

def get_system_language():
    system_language, _ = locale.getdefaultlocale()
    return system_language

def index(request):
    message = "" 
    video_path = ""  
    if request.method == 'POST':
        video_url = request.POST.get('link')
        quality = request.POST.get('quality')

        system_language = get_system_language()
        language_folder_mapping = {
            'fr_FR': 'Téléchargements',  
            'en_US': 'Downloads',
        }
        download_folder_name = language_folder_mapping.get(system_language, 'Downloads') 

        user_download_path = os.path.expanduser(f'~/{download_folder_name}')

        if not os.path.exists(user_download_path):
            message = "Le dossier de téléchargement n'existe pas pour cet utilisateur."
        else:
            try:
                video_path = download_video(video_url, user_download_path, quality)
                if quality == 'mp3' and video_path is not None:
                    message = f"La vidéo a été téléchargée avec succès au format MP3"
                elif quality != 'mp3' and video_path is not None:
                    message = f"La vidéo a été téléchargée avec succès au format MP4"
                else:
                    message = f"La vidéo n'existe pas sur YouTube"
            except ValueError as ve:
                message = f"La vidéo n'existe pas sur YouTube"
            except Exception as e:
                message = f"Erreur lors du téléchargement"

    return render(request, 'index.html', {'message': message, 'video_path': video_path})