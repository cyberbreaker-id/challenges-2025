import puppeteer from 'puppeteer'
import express from 'express'
import rateLimit from 'express-rate-limit'

const app = express()
app.use(express.json())
app.set('trust proxy', 1);

app.use(
    '/visit', rateLimit({
        windowMs: 3 * 60 * 1000, // 5 Minutes
        max: 5,
        message: { error: 'Too many requests, try again later' }
    })
)

const port = process.env.PORT || 3001
const APP_URL = process.env.APP_URL || 'http://localhost/'
const FLAG = process.env.FLAG || "fakeflag"
const ADMIN_USERNAME = process.env.ADMIN_USERNAME || "admin"
const ADMIN_PASSWORD = process.env.ADMIN_PASSWORD || "admin"
const sleep = ms => new Promise(r => setTimeout(r, ms));

console.log(`FLAG: ${FLAG}`)
console.log(`URL: ${APP_URL}`)

async function visit(url) {
    let browser = await puppeteer.launch({
        headless: "headless",
        args: [
            '--no-sandbox',
            '--disable-background-networking',
            '--disable-default-apps',
            '--disable-extensions',
            '--disable-gpu',
            '--disable-sync',
            '--disable-translate',
            '--hide-scrollbars',
            '--metrics-recording-only',
            '--mute-audio',
            '--no-first-run',
            '--safebrowsing-disable-auto-update',
            '--disable-dev-shm-usage',
            '--incognito',
        ]
    })
    const ctx = await browser.createBrowserContext()
    const page = await ctx.newPage()
    try {
        await page.goto(`${APP_URL}`);
        
        await page.type('#username', ADMIN_USERNAME);
        await page.type('#password', ADMIN_PASSWORD);
        await page.click('button[type="submit"]');
        
        await page.waitForNavigation();
        await page.close();
        
        const newPage = await ctx.newPage();
        await newPage.goto('about:blank');
        
        await newPage.goto(url);

        await sleep(20 * 1000);
        
    } catch (err){
        console.log(err);
    } finally {
        await page.close()
        await ctx.close()
        console.log(`[*] Done visiting -> ${url}`)
    }
}

app.get('/visit', async (req, res) => {
    let {url} = req.query
    if(
        (typeof url !== 'string') || (url === undefined) ||
        (url === '') || (!url.startsWith('http'))
    ){
        return res.status(400).send({error: "Invalid url"})
    }

    try {
        console.log(`[*] Visiting -> ${url}`)
        await visit(url)
        return res.sendStatus(200)
    } catch (e) {
        console.error(`[-] Error visiting -> ${url}: ${e.message}`)
        return res.status(400).send({ error: e.message })
    }
})

app.listen(port, async () => {
    console.log(`[*] Listening on port ${port}`)
})