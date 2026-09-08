from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from bs4 import BeautifulSoup
import time


def analyze_content(url):

    result = {
        "contact": False,
        "about": False,
        "refund": False,
        "score": 0,
        "reasons": []
    }

    # Add https:// automatically
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    try:

        options = Options()

        # Comment this line if browser doesn't open
        options.add_argument("--headless=new")

        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")

        driver = webdriver.Edge(
            service=Service(EdgeChromiumDriverManager().install()),
            options=options
        )

        driver.get(url)

        # Wait for page to load
        time.sleep(5)

        html = driver.page_source.lower()

        soup = BeautifulSoup(html, "html.parser")

        page = soup.get_text().lower()

        # CONTACT
        if "contact" in page or "contact us" in page:
            result["contact"] = True
            result["score"] += 10
            result["reasons"].append("Contact information found")

        # ABOUT
        if "about" in page or "about us" in page:
            result["about"] = True
            result["score"] += 5
            result["reasons"].append("About page found")

        # REFUND / RETURN
        if (
            "refund" in page
            or "return" in page
            or "replacement" in page
        ):
            result["refund"] = True
            result["score"] += 10
            result["reasons"].append("Refund/Return policy found")

        driver.quit()

    except Exception as e:

        result["reasons"].append(str(e))

    return result