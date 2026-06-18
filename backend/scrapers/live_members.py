from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import re
import logging

logger = logging.getLogger(__name__)


def slugify(name):
    """
    Converts a name to a clean lowercase underscore slug.
    """
    slug = name.lower()
    slug = re.sub(r'[^a-z0-9\s_]', '', slug)
    slug = re.sub(r'\s+', '_', slug)
    slug = re.sub(r'_+', '_', slug)
    return slug.strip('_')


def get_official_cdn_url(name):
    """
    Generates the official government CDN photo URL path for the MP.
    """
    slug = slugify(name)
    if not slug:
        return "https://hr.parliament.gov.np/uploads/member/member_placeholder.jpg"
    return f"https://hr.parliament.gov.np/uploads/member/{slug}.jpg"


def load_snapshot_lookup():
    """
    Loads local snapshot members to verify details and constituencies.
    """
    import os
    snapshot_path = os.path.join(os.path.dirname(__file__), "mp_snapshot.txt")
    lookup = {}
    try:
        with open(snapshot_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split("|")
                if len(parts) < 4:
                    continue
                name, party, constituency, gender = parts[0], parts[1], parts[2], parts[3]
                slug = slugify(name)
                lookup[slug] = {
                    "name": name.strip(),
                    "party": party.strip(),
                    "constituency": constituency.strip(),
                    "gender": gender.strip()
                }
    except Exception as e:
        logger.error(f"Failed to load snapshot lookup: {e}")
    return lookup


async def scrape_live_members():
    """
    Scrapes the list of live MPs from the official HoR website.
    Uses headless Playwright (async) to handle Javascript rendering natively.
    Returns a list of MP dicts on success, or None if the portal is unreachable / returns bad data.
    """
    url = "https://hr.parliament.gov.np/np/member"
    logger.info(f"Initiating headless Playwright scraper targeting {url}...")

    try:
        return await _do_scrape(url)
    except Exception as e:
        logger.warning(f"Live scraper failed — portal may be down: {e}")
        return None


async def _do_scrape(url: str):

    async with async_playwright() as p:
        # Launch browser with no-sandbox for docker container compatibility
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"]
        )
        context = await browser.new_context(ignore_https_errors=True)
        page = await context.new_page()

        try:
            await page.goto(url, timeout=30000)

            # Wait for content to render — networkidle ensures full JS rendering
            await page.wait_for_load_state("networkidle", timeout=15000)

            html_content = await page.content()
            soup = BeautifulSoup(html_content, "html.parser")

            members = []
            member_blocks = []

            # Find cards or containers representing members
            for div in soup.find_all("div", class_=True):
                classes = " ".join(div.get("class", []))
                if "member" in classes or "profile" in classes or "card" in classes:
                    img = div.find("img")
                    a = div.find("a", href=True)
                    if img and a and ("/member/" in a["href"] or "/detail/" in a["href"]):
                        member_blocks.append(div)

            if not member_blocks:
                for a in soup.find_all("a", href=True):
                    if "/member/" in a["href"] or "/detail/" in a["href"]:
                        parent = a.find_parent("div")
                        if parent and parent not in member_blocks:
                            img = parent.find("img")
                            if img:
                                member_blocks.append(parent)

            snapshot_lookup = load_snapshot_lookup()
            for block in member_blocks:
                try:
                    name_a = block.find("a")
                    name = name_a.text.strip() if name_a else ""
                    if not name:
                        name_h = block.find(["h3", "h4", "h5", "h6", "p"])
                        if name_h:
                            name = name_h.text.strip()

                    if not name:
                        continue

                    name = name.strip()
                    slug = slugify(name)
                    img_url = get_official_cdn_url(name)

                    if slug in snapshot_lookup:
                        snap_item = snapshot_lookup[slug]
                        name = snap_item["name"]
                        party = snap_item["party"]
                        constituency = snap_item["constituency"]
                        gender = snap_item["gender"]
                    else:
                        text_content = block.text.strip()

                        party = "Independent"
                        parties_list = [
                            "नेपाली कांग्रेस", "नेकपा (एमाले)", "नेकपा (माओवादी केन्द्र)",
                            "राष्ट्रिय स्वतन्त्र पार्टी", "राष्ट्रिय प्रजातन्त्र पार्टी",
                            "जनता समाजवादी पार्टी", "नेकपा (एकीकृत समाजवादी)"
                        ]
                        for p_name in parties_list:
                            if p_name in text_content:
                                if "कांग्रेस" in p_name:           party = "Nepali Congress"
                                elif "एमाले" in p_name:            party = "CPN-UML"
                                elif "माओवादी" in p_name:          party = "CPN-Maoist Center"
                                elif "स्वतन्त्र पार्टी" in p_name: party = "Rastriya Swatantra Party"
                                elif "प्रजातन्त्र" in p_name:      party = "Rastriya Prajatantra Party"
                                elif "समाजवादी पार्टी" in p_name:  party = "Janata Samajbadi Party"
                                elif "एकीकृत समाजवादी" in p_name: party = "CPN-Unified Socialist"
                                break

                        constituency = "Kathmandu-1"
                        districts_list = ["काठमाडौं", "ललितपुर", "भक्तपुर", "कास्की", "झापा", "मोरङ", "चितवन", "बाँके", "कैलाली", "धनुषा", "बारा", "पर्सा"]
                        eng_map = {
                            "काठमाडौं": "Kathmandu", "ललितपुर": "Lalitpur", "भक्तपुर": "Bhaktapur",
                            "कास्की": "Kaski", "झापा": "Jhapa", "मोरङ": "Morang",
                            "चितवन": "Chitwan", "बाँके": "Banke", "कैलाली": "Kailali",
                            "धनुषा": "Dhanusha", "बारा": "Bara", "पर्सा": "Parsa"
                        }
                        for d in districts_list:
                            if d in text_content:
                                num_match = re.search(rf"{d}\s*(?:निर्वाचन\s*क्षेत्र\s*(?:नं\.?\s*)?)?(\d+)", text_content)
                                if not num_match:
                                    num_match = re.search(r'(\d+)', text_content)
                                num = num_match.group(1) if num_match else "1"
                                constituency = f"{eng_map[d]}-{num}"
                                break

                        gender = "Female" if "महिला" in text_content else "Male"

                    if len(members) < 275:
                        members.append({
                            "name": name,
                            "party": party,
                            "constituency": constituency,
                            "gender": gender,
                            "profile_pic_url": img_url
                        })
                except Exception as ex:
                    logger.debug(f"Error parsing single block: {ex}")

            if len(members) == 0:
                logger.warning("Headless live scraper returned 0 members — portal may be serving an error page.")
                return None

            logger.info(f"Successfully scraped {len(members)} real members from live network.")
            return members

        except Exception as e:
            logger.warning(f"Unrecoverable exception during page scrape: {e}")
            return None
        finally:
            await browser.close()
