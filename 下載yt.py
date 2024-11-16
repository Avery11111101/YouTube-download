import os
import re
from yt_dlp import YoutubeDL

def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', "", filename)

def download_content(url):
    try:
        # 首先取得影片或播放清單資訊
        with YoutubeDL({'quiet': True, 'extract_flat': True}) as ydl:
            info = ydl.extract_info(url, download=False)
        
        # 檢查是否為播放清單
        if 'entries' in info:
            print(f"偵測到播放清單：{info['title']}")
            print(f"播放清單中共有 {len(info['entries'])} 個影片")
            playlist = True
        else:
            print(f"偵測到單一影片：{info['title']}")
            playlist = False
        
        download_type = input("選擇下載類型（影片/音訊）：").strip()
        while download_type not in ['影片', '音訊']:
            download_type = input("無效選擇。請輸入「影片」或「音訊」：").strip()
        
        ydl_opts = {
            'outtmpl': '%(title)s.%(ext)s' if not playlist else '%(playlist_title)s/%(title)s.%(ext)s',
            'ignoreerrors': False,
            'no_color': False,
            'live_from_start': True,
        }
        
        if download_type == '音訊':
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            })
        else:
            ydl_opts.update({
                'format': 'bestvideo+bestaudio/best',
                'merge_output_format': 'mp4',
            })
        
        with YoutubeDL(ydl_opts) as ydl:
            if playlist:
                for index, entry in enumerate(info['entries'], 1):
                    video_url = entry['url']
                    print(f"\n正在下載播放清單中的第 {index} 個影片")
                    ydl.download([video_url])
                    print(f"第 {index} 個影片下載完成")
                print("\n播放清單全部下載完成")
            else:
                print(f"正在下載：{info['title']}")
                ydl.download([url])
                print("下載完成")

    except Exception as e:
        print(f"下載失敗：{str(e)}")

def main():
    while True:
        url = input("\n請輸入 YouTube 網址（或輸入「q」退出）：").strip()
        if url.lower() == 'q':
            break

        # 處理手機版網址和播放清單網址
        if 'youtu.be' in url or 'youtube.com' in url:
            if 'list=' in url:
                # 這是一個播放清單網址
                playlist_id = re.search(r'list=(.*?)(&|$)', url).group(1)
                url = f"https://www.youtube.com/playlist?list={playlist_id}"
            elif 'youtu.be' in url:
                # 這是一個短網址
                video_id = url.split('/')[-1].split('?')[0]
                url = f"https://www.youtube.com/watch?v={video_id}"

        download_content(url)


main()
