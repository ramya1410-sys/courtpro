from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from PIL import Image
import pytesseract
import time

def fetch_captcha_code():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get("https://dhccaseinfo.nic.in/pcase/guiCaseWise.php")

    try:
        # Step 1: Wait and select dropdown
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ddlCourt")))
        court_dropdown = Select(driver.find_element(By.ID, "ddlCourt"))
        court_dropdown.select_by_visible_text("MAIN")

        # Step 2: Wait for CAPTCHA image
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "captcha_image")))

        # Step 3: Save CAPTCHA image screenshot
        captcha_element = driver.find_element(By.ID, "captcha_image")
        location = captcha_element.location
        size = captcha_element.size
        driver.save_screenshot("full_page.png")

        # Crop only CAPTCHA region
        x, y, width, height = location['x'], location['y'], size['width'], size['height']
        image = Image.open("full_page.png")
        captcha_image = image.crop((x, y, x + width, y + height))
        captcha_image.save("captcha_crop.png")

        # Step 4: Use OCR to extract text
        captcha_text = pytesseract.image_to_string(captcha_image, config='--psm 8 --oem 3')
        print("✅ CAPTCHA:", captcha_text.strip())

        return captcha_text.strip()

    except Exception as e:
        print("❌ Error reading CAPTCHA:", str(e))
        return None

    finally:
        driver.quit()
