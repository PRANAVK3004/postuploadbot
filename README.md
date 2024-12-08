# postuploadbot
Video Upload Bot Project Report
1. Project Overview
Objective
The primary goal of this project is to develop an automated bot capable of:

Scraping video content from social media platforms (currently implemented for Instagram)
Downloading and filtering videos based on specific criteria
Uploading videos to a designated server using a provided API

Key Features

Instagram video scraping and downloading
Automatic video upload to SocialVerse platform
Asynchronous processing
Logging and error handling
Configurable parameters for video selection

2. Technical Architecture
Components

Instagram Scraper (instascrap.js)

Uses Puppeteer for web scraping
Implements cookie-based authentication
Extracts video post URLs from Instagram hashtag pages


Video Downloader and Uploader (mainfinal.py)

Utilizes instaloader for Instagram video downloads
Implements asynchronous download and upload using aiohttp
Integrates with SocialVerse API for video uploads



Technology Stack

Python 3.8+
Node.js
Libraries:

Instaloader
aiohttp
aiofiles
Puppeteer
Watchdog
yt_dlp



3. Installation and Setup
Prerequisites

Python 3.8 or higher
Node.js
npm (Node Package Manager)

Installation Steps

Clone the repository
Install Python dependencies:
bashCopypip install instaloader aiohttp aiofiles tqdm watchdog

Install Node.js dependencies:
bashCopynpm install puppeteer-extra puppeteer-extra-plugin-stealth


Configuration

Set environment variables:

FLIC_API_TOKEN: API token for SocialVerse


Configure instagram.com_cookies.txt for authentication
Modify instagram_posts.json with target video URLs

4. Workflow
Video Scraping Process

Run Instagram scraper script
Script searches hashtag pages
Extracts video post URLs
Saves URLs to instagram_posts.json

Video Download and Upload Process

Load video URLs from JSON
Download videos matching criteria:

Duration between 10-250 seconds
Video format


Generate upload URL via SocialVerse API
Upload videos with metadata
Remove local video files after successful upload

5. Key Code Highlights
Instagram Video Download
pythonCopyasync def download_post(self, post_url, output_dir='videos'):
    # Download Instagram video if meets duration criteria
    if post.is_video and 10 <= post.video_duration <= 250:
        # Async video download logic
Video Upload
pythonCopyasync def upload_video(self, video_path, title, category_id=1):
    # Generate upload URL
    # Upload video to server
    # Create post metadata
6. Error Handling and Logging

Comprehensive logging using Python's logging module
Graceful error handling for:

Authentication failures
Download errors
Upload issues


Detailed log messages with timestamps

7. Security Considerations

Uses environment variables for sensitive data
Implements cookie-based authentication
Stealth plugin to avoid bot detection

8. Limitations and Future Improvements

Currently supports only Instagram
Planned expansions:

TikTok video support
Reddit video integration
Enhanced video filtering
Parallel processing



9. Deployment Recommendations

Use virtual environments
Implement robust error monitoring
Add comprehensive unit tests
Consider containerization (Docker)

10. Ethical and Legal Note

Ensure compliance with platform terms of service
Respect copyright and content creator rights
Obtain necessary permissions for video usage

Conclusion
This bot demonstrates a robust, asynchronous approach to social media content scraping and uploading, with a focus on modularity and extensibility.
Project Status

Current version: 1.0
Platforms supported: Instagram
Ongoing development: Planned multi-platform support


Appendix: Example Usage
bashCopy# Scrape Instagram videos
node instascrap.js

# Upload scraped videos
python mainfinal.py
