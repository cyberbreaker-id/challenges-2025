import puppeteer from "puppeteer";
import express from "express";
import rateLimit from "express-rate-limit";

const app = express();
app.use(express.json());
app.set('trust proxy', 1);

app.use(
    "/visit",
    rateLimit({
        windowMs: 3 * 60 * 1000, // 5 Minutes
        max: 5,
        message: { error: "Too many requests, try again later" },
    })
);

const port = process.env.PORT || 3001;
const APP_URL = process.env.APP_URL || "http://localhost/";
const FLAG = process.env.GZCTF_FLAG || "fakeflag";
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

console.log(`FLAG: ${FLAG}`);
console.log(`URL: ${APP_URL}`);

async function visit(url) {
    let browser = await puppeteer.launch({
        headless: "headless",
        args: [
            "--no-sandbox",
            "--disable-background-networking",
            "--disable-default-apps",
            "--disable-extensions",
            "--disable-gpu",
            "--disable-sync",
            "--disable-translate",
            "--hide-scrollbars",
            "--metrics-recording-only",
            "--mute-audio",
            "--no-first-run",
            "--safebrowsing-disable-auto-update",
            "--disable-dev-shm-usage",
            "--incognito",
        ],
    });
    const ctx = await browser.createBrowserContext();
    const page = await ctx.newPage();
    try {
        await page.goto(`${APP_URL}`);

        await sleep(3 * 1000);
        await page.setCookie({
            name: "flag",
            value: FLAG,
            httpOnly: true,
            sameSite: "Strict",
            domain: new URL(APP_URL).hostname,
        });

        const newPage = await ctx.newPage();
        await newPage.goto("about:blank");

        await page.close();

        await newPage.goto(url);

        await sleep(10 * 1000);
    } catch (err) {
        console.log(err);
    } finally {
        await ctx.close();
        console.log(`[*] Done visiting -> ${url}`);
    }
}

app.get("/visit", async (req, res) => {
    let { url } = req.query;
    if (typeof url !== "string" || url === undefined || url === "" || !url.startsWith("http")) {
        return res.status(400).send({ error: "Invalid url" });
    }

    try {
        console.log(`[*] Visiting -> ${url}`);
        visit(url);
        return res.sendStatus(200);
    } catch (e) {
        console.error(`[-] Error visiting -> ${url}: ${e.message}`);
        return res.status(400).send({ error: e.message });
    }
});

app.listen(port, async () => {
    console.log(`[*] Listening on port ${port}`);
});
