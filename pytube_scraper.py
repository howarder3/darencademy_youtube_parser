import yt_dlp

def get_playlist_with_yt_dlp(playlist_url):
    """
    使用 yt-dlp 套件來獲取播放清單資訊。
    這個方法非常可靠，因為 yt-dlp 的更新速度極快。
    """
    # yt-dlp 的設定選項
    # 我們告訴它：不要下載影片，只要平鋪直敘地列出清單中的項目資訊即可。
    ydl_opts = {
        'ignoreerrors': True,  # 忽略任何可能導致錯誤的影片
        'extract_flat': True,  # 只獲取基本資訊，速度更快
        'quiet': True,         # 不要在螢幕上印出 yt-dlp 的下載訊息
    }

    hyperlink_list = []
    print("正在使用 yt-dlp 獲取播放清單資訊...")

    try:
        # 使用 with 陳述式來確保資源被正確關閉
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # 提取資訊
            playlist_info = ydl.extract_info(playlist_url, download=False)

            if 'entries' in playlist_info:
                videos = playlist_info['entries']
                print(f"成功獲取到 {len(videos)} 部影片的資訊，開始處理...")

                for video in videos:
                    video_title = video.get('title', '!! 標題無法取得 !!')
                    video_id = video.get('id')

                    if video_id:
                        video_url = f"https://www.youtube.com/watch?v={video_id}"
                        sanitized_title = video_title.replace('"', "'")
                        hyperlink = f'=HYPERLINK("{video_url}", "{sanitized_title}")'
                        hyperlink_list.append(hyperlink)

            else:
                print("錯誤：在回傳的資料中找不到 'entries' 項目。")

    except Exception as e:
        print(f"使用 yt-dlp 時發生錯誤: {e}")
        return None

    return hyperlink_list

# --- 主程式執行區 ---
if __name__ == "__main__":
    target_playlist_url = "https://www.youtube.com/playlist?list=PL45a1lc7-gwsz8_Nt7Ao9BFavZBrz2FGK"

    links = get_playlist_with_yt_dlp(target_playlist_url)

    if links:
        print("\n" + "="*50)
        print(f"yt-dlp 執行完畢！成功解析出 {len(links)} 部影片。")
        print("="*50 + "\n")

        # 將結果儲存到檔案
        file_name = "youtube_playlist_yt-dlp.txt"
        with open(file_name, "w", encoding="utf-8") as f:
            for link_string in links:
                f.write(link_string + "\n")
        print(f"所有 HYPERLINK 字串已儲存至檔案: {file_name}")