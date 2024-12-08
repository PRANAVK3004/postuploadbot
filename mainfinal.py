import os
import json
import asyncio
import logging
import hashlib
import aiohttp
import aiofiles
import instaloader
import yt_dlp
from tqdm import tqdm
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class InstagramDownloader:
    def __init__(self, username=None, password=None, cookie_file='instagram_cookies.txt'):
        self.L = instaloader.Instaloader()
        self.username = username
        self.password = password
        self.cookie_file = cookie_file

        # Load session from cookies or login
        try:
            if username and password:
                self.L.login(username, password)
                self.L.save_session_to_file(cookie_file)
                logger.info("Instagram login successful and session saved.")
            else:
                self.L.load_session_from_file(username, cookie_file)
                logger.info("Loaded Instagram session from cookies.")
        except Exception as e:
            logger.warning(f"Failed to load or create session: {e}. Limited functionality may apply.")

    async def download_post(self, post_url, output_dir='videos'):
        """
        Download Instagram post (video or image) using Instaloader asynchronously.
        """
        try:
            os.makedirs(output_dir, exist_ok=True)
            shortcode = post_url.split('/')[-2] if '/p/' in post_url else post_url.split('/')[-1].split('?')[0]
            post = instaloader.Post.from_shortcode(self.L.context, shortcode)

            if post.is_video:
                if 10 <= post.video_duration <= 250:
                    # Perform asynchronous download of video
                    video_url = post.video_url
                    filename = os.path.join(output_dir, f"{shortcode}.mp4")
                    
                    async with aiohttp.ClientSession() as session:
                        async with session.get(video_url) as response:
                            if response.status == 200:
                                async with aiofiles.open(filename, 'wb') as f:
                                    await f.write(await response.read())
                                logger.info(f"Video downloaded: {filename}")
                                return filename
                            else:
                                logger.error(f"Failed to download video: {response.status}")
                else:
                    logger.info(f"Video duration {post.video_duration} seconds is out of range.")
            else:
                logger.info("Post is not a video.")
            return None
        except Exception as e:
            logger.error(f"Instagram download error: {e}")
            return None

class VideoDownloader:
    def __init__(self, api_token, base_url, videos_dir='videos', instagram_username=None, instagram_password=None):
        self.api_token = api_token
        self.base_url = base_url
        self.videos_dir = videos_dir
        os.makedirs(videos_dir, exist_ok=True)
        self.instagram_downloader = InstagramDownloader(instagram_username, instagram_password)

    async def generate_upload_url(self, filename):
        """
        Generate an upload URL for a video.
        """
        try:
            async with aiohttp.ClientSession() as session:
                headers = {"Flic-Token": self.api_token, "Content-Type": "application/json"}
                async with aiofiles.open(filename, 'rb') as f:
                    file_hash = hashlib.md5(await f.read()).hexdigest()
                payload = {"hash": file_hash}
                async with session.get(f"{self.base_url}/posts/generate-upload-url", headers=headers, json=payload) as response:
                    response_data = await response.json()
                    return response_data.get('url'), response_data.get('hash')
        except Exception as e:
            logger.error(f"URL generation error: {e}")
            return None, None

    async def upload_video(self, video_path, title, category_id=1):
        """
        Upload the video to the server.
        """
        upload_url, file_hash = await self.generate_upload_url(video_path)
        if not upload_url:
            logger.error("Failed to generate upload URL")
            return False

        try:
            async with aiohttp.ClientSession() as session:
                async with aiofiles.open(video_path, 'rb') as f:
                    file_content = await f.read()

                # Upload the video
                upload_headers = {"Content-Type": "video/mp4"}
                async with session.put(upload_url, data=file_content, headers=upload_headers) as upload_response:
                    if upload_response.status not in [200, 204]:
                        logger.error(f"Upload failed: {upload_response.status} - {await upload_response.text()}")
                        return False

                # Send metadata to create a post
                post_headers = {
                    "Flic-Token": self.api_token,
                    "Content-Type": "application/json"
                }
                post_payload = {
                    "title": title,
                    "hash": file_hash,
                    "is_available_in_public_feed": True,
                    "category_id": category_id
                }
                async with session.post(f"{self.base_url}/posts", headers=post_headers, json=post_payload) as post_response:
                    if post_response.status not in [200, 201]:
                        logger.error(f"Post creation failed: {await post_response.text()}")
                        return False

                os.remove(video_path)
                logger.info(f"Video uploaded and post created successfully: {title}")
                return True
        except Exception as e:
            logger.error(f"Upload error: {e}")
            return False

async def main():
    API_TOKEN = os.getenv('FLIC_API_TOKEN', 'flic_a3588b33316009369ef74879f796c0cbbfa4b75eb715f67c1d81c204d92bddd8')
    BASE_URL = 'https://api.socialverseapp.com'
    VIDEOS_DIR = 'videos'
    INSTAGRAM_USERNAME = 'pktry2'
    INSTAGRAM_PASSWORD = 'Peo248363'

    downloader = VideoDownloader(API_TOKEN, BASE_URL, VIDEOS_DIR, INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
    
    # Load JSON file with URLs
    with open(r"C:\instagram scraper\instagram_posts.json", 'r') as f:
        urls = json.load(f)

    for url in urls:
        video_path = await downloader.instagram_downloader.download_post(url, VIDEOS_DIR)
        if video_path:
            success = await downloader.upload_video(video_path, "Instagram Video", category_id=25)
            if success:
                logger.info(f"Successfully uploaded video from {url}")
            else:
                logger.error(f"Failed to upload video from {url}")
        else:
            logger.info(f"Skipping URL {url}")

if __name__ == '__main__':
    asyncio.run(main())
