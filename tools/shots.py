#!/usr/bin/env python3
"""
Screenshot every page at desktop and phone widths, for eyeballing changes.

    python3 -m http.server 8765 &
    python3 tools/shots.py [outdir]

Requires playwright (`pip install playwright && playwright install chromium`).
Not needed to build or deploy the site -- purely a review aid.
"""
import asyncio, sys, os
from playwright.async_api import async_playwright

OUT = sys.argv[1] if len(sys.argv) > 1 else "shots"
BASE = "http://localhost:8765"
PAGES = ["index", "theme", "program", "speakers", "venue", "register", "organizers"]
SIZES = [("desktop", 1440, 900), ("phone", 390, 844)]


async def main():
    os.makedirs(OUT, exist_ok=True)
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        problems = []
        for label, w, h in SIZES:
            page = await browser.new_page(viewport={"width": w, "height": h},
                                          device_scale_factor=1)
            page.on("response", lambda r: problems.append((r.status, r.url))
                    if r.status >= 400 else None)
            page.on("pageerror", lambda e: problems.append(("JS", str(e))))
            for name in PAGES:
                await page.goto(f"{BASE}/{name}.html", wait_until="networkidle")
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await page.wait_for_timeout(700)          # let reveals fire
                await page.evaluate("window.scrollTo(0, 0)")
                await page.wait_for_timeout(300)
                await page.screenshot(path=f"{OUT}/{label}-{name}.png", full_page=True)
                print(f"  {label:8} {name}")
            await page.close()
        await browser.close()
    if problems:
        print("\nPROBLEMS:")
        for s, u in dict.fromkeys(problems):
            print(f"  {s}  {u}")
    else:
        print("\nNo failed requests, no JS errors.")


asyncio.run(main())
