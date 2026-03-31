# tests/test_header_footer_simple.py
import datetime
import re
import pytest
from playwright.sync_api import Page

# URL we are testing
BASE = "http://localhost:5500/web/index.html"

# -------------------------
# Helper functions
# -------------------------

def formatted_today_string():
    """
    Build today's date string in the exact format required by the acceptance criteria:
      Weekday, Month Day, Year
    Example: "Monday, March 2, 2026"

    We use the system date (the machine running the test) so the test verifies
    the page shows today's date dynamically.
    """
    today = datetime.date.today()
    weekday = today.strftime("%A")   # full weekday (e.g., Monday)
    month = today.strftime("%B")     # full month name (e.g., March)
    day = today.day                  # integer (no leading zero)
    year = today.year
    return f"{weekday}, {month} {day}, {year}"


def find_visible_link_by_text(page: Page, text: str) -> bool:
    """
    Look for a link (<a>) that contains `text` in its accessible name or visible text.
    - `page.get_by_role("link", name=...)` is accessibility-aware (preferred).
    - returning True/False keeps tests simple and readable for students.
    """
    # get_by_role finds links by role=name; regex ignore-case helps match many variants
    locator = page.get_by_role("link", name=re.compile(text, re.IGNORECASE))
    # locator.count() > 0 ensures the element exists; .first.is_visible() verifies it's visible on page
    return locator.count() > 0 and locator.first.is_visible()


# -------------------------
# Fixtures
# -------------------------

@pytest.fixture(autouse=True)
def open_base(page: Page):
    """
    Automatically open the base URL before each test runs.
    - `page` is a pytest-playwright fixture that gives us a browser page.
    - page.goto(...) navigates the browser to the URL.
    - yield allows the test to run, then cleanup (if any) happens after yield.
    """
    page.goto(BASE)
    yield


# -------------------------
# Tests (each maps to an acceptance criterion)
# -------------------------

def test_header_logo_and_title(page: Page):
    """
    Verify header logo visible and site name / title present.
    - set_viewport_size: ensures we run in desktop viewport so responsive layout is the expected desktop version.
    - page.locator(...) finds elements using CSS selectors.
    - page.title() reads the browser tab title.
    """
    page.set_viewport_size({"width": 1280, "height": 800})

    # Look for image elements whose alt contains 'Teton' or 'Chamber'
    logo = page.locator('img[alt*="Teton"], img[alt*="Chamber"]')
    assert logo.count() > 0 and logo.first.is_visible(), "Logo not visible."

    # Read the whole page body text and ensure site name appears
    body = page.locator("body").inner_text()
    assert (
        "Teton Idaho Chamber of Commerce" in body
        or "Teton Idaho CoC" in body
    ), "Site name not found."

    # Make sure the browser tab title contains something that looks like the site
    assert "teton" in page.title().lower()


def test_header_links_in_screen_view(page: Page):
    """
    Verify Home and Join links are visible on a standard desktop/screen viewport.
    - Changing viewport helps us test responsive differences (desktop vs mobile).
    """
    page.set_viewport_size({"width": 1130, "height": 768})

    assert find_visible_link_by_text(page, "Home"), "Home link not visible."
    assert find_visible_link_by_text(page, "Join"), "Join link not visible."


def test_header_hamburger_on_phone_shows_links(page: Page):
    """
    Verify the mobile hamburger menu works:
    - Resize to phone viewport, click the known hamburger button (#hamburger-menu),
      then ensure Home, Join and Directory links are visible.
    - We use the button's ID for reliable selection.
    """
    page.set_viewport_size({"width": 375, "height": 812})

    # Find the hamburger button by its ID and click it to open mobile nav
    hamburger = page.locator("#hamburger-menu")
    assert hamburger.count() > 0, "Hamburger menu button not found."
    hamburger.click()

    # After opening the menu, check the links are visible
    assert find_visible_link_by_text(page, "home"), "Home link not visible in phone menu."
    assert find_visible_link_by_text(page, "join"), "Join link not visible in phone menu."
    assert find_visible_link_by_text(page, "directory"), "Directory link not visible in phone menu."


def test_social_icons_visible(page: Page):
    """
    Check that Pinterest and Instagram icons/links are present and visible.
    - Using `a[href*="pinterest"]` is a robust way to find social links.
    """
    pinterest = page.locator('a[href*="pinterest"]')
    instagram = page.locator('a[href*="instagram"]')

    assert pinterest.count() > 0 and pinterest.first.is_visible(), "Pinterest link not visible."
    assert instagram.count() > 0 and instagram.first.is_visible(), "Instagram link not visible."


def test_todays_date_is_displayed(page: Page):
    """
    Ensure the page displays today's date exactly as:
      Monday, March 2, 2026
    - We compute the expected string on the test machine
      and assert the page contains that exact text.
    """
    expected = formatted_today_string()
    body = page.locator("body").inner_text()
    assert expected in body, f"Expected date '{expected}' not found on page."


def test_footer_map_icon_exists(page: Page):
    """
    Verify a map link exists in the footer and that its href points to Google Maps (goo.gl link).
    """
    map_link = page.locator('footer a[href*="https://maps.app.goo.gl/"]')
    assert map_link.count() > 0, "Google Maps link not found in footer."
    href = map_link.first.get_attribute("href")
    assert href and "goo.gl" in href.lower(), "Map link does not point to Google Maps."


def test_footer_contact_info(page: Page):
    """
    Check the expected email and phone number appear on the page.
    - We lower-case the body text to make the check robust to capitalization.
    - The phone regex allows flexible punctuation/spacing.
    """
    body = page.locator("body").inner_text().lower()
    assert "info@tetonchamber.org" in body, "Email not found."
    phone_ok = re.search(r"208[^\d]*458[^\d]*4444", body) is not None
    assert phone_ok, "Phone number not found."

# random comment to test deployment