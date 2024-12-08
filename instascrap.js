const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
const fs = require('fs');
const path = require('path');
const readline = require('readline');

// Use stealth plugin to bypass bot detection
puppeteer.use(StealthPlugin());

// Function to parse cookies from a cookies.txt file
function parseCookiesFromFile(filePath) {
    const cookies = [];
    const rl = readline.createInterface({
        input: fs.createReadStream(filePath),
        crlfDelay: Infinity,
    });

    return new Promise((resolve, reject) => {
        rl.on('line', line => {
            if (!line || line.startsWith('#')) return;
            const parts = line.split('\t');
            if (parts.length >= 7) {
                cookies.push({
                    domain: parts[0],
                    httpOnly: parts[1].toLowerCase() === 'true',
                    path: parts[2],
                    secure: parts[3].toLowerCase() === 'true',
                    expires: Number(parts[4]),
                    name: parts[5],
                    value: parts[6],
                });
            }
        });
        rl.on('close', () => resolve(cookies));
        rl.on('error', reject);
    });
}

async function scrapeInstagramHashtag() {
    let browser;
    try {
        // Launch Puppeteer
        browser = await puppeteer.launch({
            headless: false,
            defaultViewport: null,
            args: [
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-accelerated-2d-canvas',
                '--start-maximized',
                '--disable-gpu',
            ],
        });

        const page = await browser.newPage();
        await page.setDefaultNavigationTimeout(120000);

        // Load cookies from cookies.txt
        const cookiesPath = path.join(__dirname, 'instagram.com_cookies.txt');
        if (fs.existsSync(cookiesPath)) {
            console.log('Loading cookies from cookies.txt...');
            const cookies = await parseCookiesFromFile(cookiesPath);
            for (const cookie of cookies) {
                // Puppeteer requires cookies to have a valid `url`
                const url = `https://${cookie.domain.replace(/^\./, '')}`;
                await page.setCookie({ ...cookie, url });
            }
        } else {
            console.error('cookies.txt not found. Please provide the file.');
            process.exit(1);
        }

        // Navigate to the hashtag page
        const url = 'https://www.instagram.com/explore/tags/motivationalspeechoftheday/';
        await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });

        // Wait for the page to load post links
        console.log('Waiting for posts to appear...');
        await page.waitForSelector('a[href^="/p/"]', { timeout: 60000 });

        // Scroll the page to load more posts
        console.log('Scrolling to load more posts...');
        await page.evaluate(() => {
            window.scrollBy(0, window.innerHeight * 2);
        });

        // Wait for additional posts to load
        await new Promise(resolve => setTimeout(resolve, 5000)); // Replaces waitForTimeout

        // Extract post URLs
        console.log('Extracting post URLs...');
        const postUrls = await page.evaluate(() => {
            const links = document.querySelectorAll('a[href^="/p/"]');
            return Array.from(new Set(Array.from(links).map(link => `https://www.instagram.com${link.getAttribute('href')}`))).slice(0, 50);
        });

        // Save the scraped URLs to a JSON file
        const outputFilePath = path.join(__dirname, 'instagram_posts.json');
        fs.writeFileSync(outputFilePath, JSON.stringify(postUrls, null, 2));
        console.log(`Scraped ${postUrls.length} posts. Results saved to ${outputFilePath}.`);

        return postUrls;

    } catch (error) {
        console.error('Error during scraping:', error);
        throw error;
    } finally {
        if (browser) {
            console.log('Closing browser...');
            await browser.close();
        }
    }
}

// Run the scraper
scrapeInstagramHashtag()
    .then(posts => {
        console.log(`Successfully scraped ${posts.length} posts.`);
        process.exit(0);
    })
    .catch(error => {
        console.error('Scraping failed:', error);
        process.exit(1);
    });
