# postuploadbot



## Overview

The **Video Upload Bot** automates the process of scraping, downloading, and uploading video content from social media platforms. Initially designed for Instagram, this bot is modular and can be extended to support additional platforms like TikTok and Reddit in the future.

### Objective

- Scrape video content from Instagram.
- Filter videos based on specific criteria.
- Upload filtered videos to the **SocialVerse** platform via API.

### Key Features

- Instagram video scraping and downloading.
- Asynchronous video processing for efficient performance.
- Automated video upload to **SocialVerse**.
- Configurable parameters for video selection (duration, format, etc.).
- Logging and error handling.

---

## Technical Architecture

### Components

#### 1. Instagram Scraper (`instascrap.js`)
- Built using **Puppeteer** for web scraping.
- Cookie-based authentication.
- Extracts video post URLs from Instagram hashtag pages.

#### 2. Video Downloader and Uploader (`mainfinal.py`)
- Utilizes **instaloader** for downloading Instagram videos.
- Implements asynchronous download and upload using **aiohttp**.
- Integrates with the **SocialVerse API** for video uploads.

---

### Technology Stack

- **Languages**: Python 3.8+, Node.js.
- **Libraries**:
  - Python: `instaloader`, `aiohttp`, `aiofiles`, `tqdm`, `watchdog`.
  - Node.js: `puppeteer-extra`, `puppeteer-extra-plugin-stealth`.
  - Other: `yt_dlp`.

---

## Installation and Setup

### Prerequisites

- Python 3.8 or higher.
- Node.js and npm.

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-repository/video-upload-bot.git
   cd video-upload-bot
Install Python dependencies:

