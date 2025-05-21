#!/usr/bin/env python3

import asyncio
import pandas as pd
import random
import os
from datetime import datetime
from playwright.async_api import async_playwright

# Supprime les popups et paywalls
async def handle_obstacles(page):
    await page.wait_for_timeout(2000)
    await page.evaluate("""
        const selectors = [
            '.ew-paywall-outer', '.modal-backdrop', '.popup-backdrop',
            '.overlay', '.cookie-notice', '.general-popup-outer'
        ];
        selectors.forEach(sel => {
            document.querySelectorAll(sel).forEach(el => el.remove());
        });
        document.body.style.overflow = 'auto';
    """)

# Lance le scraping
async def scrape_breguet_cards():
    print(f"[DÉMARRAGE] Scraping des montres Breguet en cours...")
    data = []
    os.makedirs("debug", exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )

        page = await context.new_page()
        await page.goto("https://everywatch.com/watch-listing", timeout=90000)
        print("[INFO] Page de listing chargée.")
        await handle_obstacles(page)

        # Scroll jusqu'à charger toutes les cartes
        last_height = 0
        max_tries = 30
        tries = 0
        while tries < max_tries:
            cards = await page.query_selector_all(".ew-watch-card")
            print(f"[INFO] {len(cards)} montres détectées...")
            await page.mouse.wheel(0, 1500)
            await page.wait_for_timeout(random.uniform(800, 1300))

            height = await page.evaluate("document.body.scrollHeight")
            if height == last_height:
                tries += 1
            else:
                last_height = height
                tries = 0

        await page.screenshot(path="debug/final_scroll.png")

        # Récupère toutes les cartes chargées
        cards = await page.query_selector_all(".ew-watch-card")
        print(f"[INFO] {len(cards)} cartes au total.")

        for i, card in enumerate(cards):
            try:
                text = (await card.inner_text()).lower()
                if "breguet" not in text:
                    continue

                brand = "Breguet"
                name = ref = est = img_url = link = "N/A"

                # Nom
                name_elem = await card.query_selector("div.lot-detail > div:nth-child(2) span")
                if name_elem:
                    name = await name_elem.inner_text()

                # Référence
                ref_elem = await card.query_selector("div.lot-detail > div:nth-child(3) span")
                if ref_elem:
                    ref = await ref_elem.inner_text()

                # Estimation
                est_elem = await card.query_selector(".price span")
                if est_elem:
                    est = await est_elem.inner_text()

                # Image
                img_elem = await card.query_selector("img")
                if img_elem:
                    img_url = await img_elem.get_attribute("src") or "N/A"

                # Lien
                link_elem = await card.query_selector("a")
                if link_elem:
                    href = await link_elem.get_attribute("href")
                    if href:
                        link = f"https://everywatch.com{href}"

                data.append({
                    "Marque": brand,
                    "Modèle": name.strip(),
                    "Référence": ref.strip(),
                    "Estimation": est.strip(),
                    "Image": img_url.strip(),
                    "Lien": link.strip()
                })
                print(f"[✓] {brand} : {name} ({ref})")

            except Exception as e:
                print(f"[ERREUR] Carte {i+1} : {e}")
                continue

        await browser.close()

    if not data:
        print("[⚠️] Aucune montre Breguet trouvée.")
        return

    # Export Excel
    df = pd.DataFrame(data)
    filename = f"breguet_watches_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    df.to_excel(filename, index=False)
    print(f"[✅] {len(df)} montres Breguet exportées dans '{filename}'.")

if __name__ == "__main__":
    try:
        asyncio.run(scrape_breguet_cards())
    except KeyboardInterrupt:
        print("\n[INFO] Interruption par l'utilisateur.")
    except Exception as e:
        print(f"\n[ERREUR CRITIQUE] {e}")
        import traceback
        traceback.print_exc()
