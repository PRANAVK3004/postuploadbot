# postuploadbot

Video Upload Bot
Overview
The Video Upload Bot automates the process of scraping, downloading, and uploading video content from social media platforms. Initially designed for Instagram, this bot is modular and can be extended to support additional platforms like TikTok and Reddit in the future.

Objective
Scrape video content from Instagram.
Filter videos based on specific criteria.
Upload filtered videos to the SocialVerse platform via API.
Key Features
Instagram video scraping and downloading.
Asynchronous video processing for efficient performance.
Automated video upload to SocialVerse.
Configurable parameters for video selection (duration, format, etc.).
Logging and error handling.
Technical Architecture
Components
1. Instagram Scraper (instascrap.js)
Built using Puppeteer for web scraping.
Cookie-based authentication.
Extracts video post URLs from Instagram hashtag pages.
2. Video Downloader and Uploader (mainfinal.py)
Utilizes instaloader for downloading Instagram videos.
Implements asynchronous download and upload using aiohttp.
Integrates with the SocialVerse API for video uploads.
Technology Stack
Languages: Python 3.8+, Node.js.
Libraries:
Python: instaloader, aiohttp, aiofiles, tqdm, watchdog.
Node.js: puppeteer-extra, puppeteer-extra-plugin-stealth.
Other: yt_dlp.
Installation and Setup
Prerequisites
Python 3.8 or higher.
Node.js and npm.
Installation Steps
Clone the repository:

bash
Copy code
git clone https://github.com/your-repository/video-upload-bot.git
cd video-upload-bot
Install Python dependencies:

bash
Copy code
pip install instaloader aiohttp aiofiles tqdm watchdog
Install Node.js dependencies:

bash
Copy code
npm install puppeteer-extra puppeteer-extra-plugin-stealth
Set environment variables:

Define FLIC_API_TOKEN for SocialVerse API.
Configure instagram.com_cookies.txt for authentication.
Modify configuration files:

Add target hashtags and URLs in instagram_posts.json.
Workflow
1. Video Scraping Process
Run the Instagram scraper script:
bash
Copy code
node instascrap.js
The script searches Instagram hashtag pages and saves video URLs in instagram_posts.json.
2. Video Download and Upload Process
Load video URLs from instagram_posts.json.
Download videos matching these criteria:
Duration: 10–250 seconds.
Format: Supported video formats.
Upload videos to SocialVerse using its API.
Remove local files after a successful upload.
Run the video processing script:

bash
Copy code
python mainfinal.py
Key Code Highlights
Instagram Video Download
python
Copy code
async def download_post(self, post_url, output_dir='videos'):
    if post.is_video and 10 <= post.video_duration <= 250:
        # Async video download logic
Video Upload
python
Copy code
async def upload_video(self, video_path, title, category_id=1):
    # Generate upload URL
    # Upload video to server
    # Create post metadata
Error Handling and Logging
Comprehensive logging using Python's logging module.
Handles:
Authentication failures.
Download errors.
Upload issues.
Provides detailed log messages with timestamps.
Security Considerations
Sensitive data (e.g., API tokens) managed via environment variables.
Uses cookie-based authentication to interact with Instagram.
Incorporates Puppeteer stealth plugins to avoid bot detection.
Limitations and Future Improvements
Current Limitations:
Supports only Instagram.
Planned Enhancements:
Integration with TikTok and Reddit.
Advanced video filtering options.
Improved parallel processing for higher efficiency.
Deployment Recommendations
Use virtual environments for Python dependencies.
Implement robust error monitoring systems.
Add unit tests to ensure code reliability.
Consider containerization using Docker for ease of deployment.
Ethical and Legal Note
Ensure compliance with platform terms of service.
Respect copyrights and the rights of content creators.
Obtain necessary permissions for video usage.
Example Usage
Scrape Instagram Videos:
bash
Copy code
node instascrap.js
Upload Scraped Videos:
bash
Copy code
python mainfinal.py
Project Status
Version: 1.0
Current Support: Instagram
Future Work: Multi-platform support (TikTok, Reddit).
