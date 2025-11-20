#!/usr/bin/env python3
# python3 -m venv venv 
# source venv/bin/activate
# /home/mato/Desktop/bash/test/venv/bin/python /home/mato/Desktop/bash/test/h.py > /home/mato/Desktop/bash/test/tempmail.log 2>&1
from patchright.sync_api import sync_playwright
import time
import easyocr  # pip install easyocr
import cv2
import numpy as np
import re
import random
from pathlib import Path 
needle   = 'https://temp-mail.org/en/view/'
link_re  = re.compile(r'https://temp-mail\.org/en/view/[a-zA-Z0-9]+')

def fix_email(text: str) -> str:
    t = re.sub(r'\s+', '', text)     # 1. remove every space
    if len(t) >= 4 and t[-4] != '.': # 2. missing dot?
        t = t[:-3] + '.' + t[-3:]
    return t

def extract_email_from_screenshot(screenshot_path):
    """Extract email from screenshot using OCR"""
    reader = easyocr.Reader(['en'])
    results = reader.readtext(screenshot_path)
    for (coordinates, text, confidence) in results:
        if '@' in text:  # Basic email validation
            return  fix_email(re.sub(r' (\w+)$', r'.\1', text.strip()))

            
    return results
    return "there is no mail"


def random_user_agent():
    """Return a random Windows / Chrome UA string (major version 110–130)."""
    major = random.randint(110, 130)
    minor = random.randint(0, 555)
    webkit = random.randint(530, 540)
    return (
        f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        f"AppleWebKit/{webkit}.36 (KHTML, like Gecko) "
        f"Chrome/{major}.0.{minor}.0 Safari/{webkit}.36"
    )

def main():
    a=0
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        ra=random_user_agent()
        page = browser.new_page()
                #       user_agent=ra#"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
        #Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/5364.36 (KHTML, like Gecko) Chrome/120.0.657.0 Safari/5364.36

        # print(random_user_agent())
        
        page.goto("https://temp-mail.org/en/")
        time.sleep(7)  # Wait for email to appear
        # Take screenshot of just the email input area
        email_element = page.locator('input#mail')
        email_element.screenshot(path='email_screenshot.png')
        
        # Extract email with OCR
        email = extract_email_from_screenshot('email_screenshot.png')
        
        if email:
            with open("mail.txt", "a") as f:
                f.write(f"{email}\n")
            print(email)
            while True:
                with open('page.html', 'w', encoding='utf-8') as f:
                    f.write(page.content())
                seen = set()
                for line in Path('page.html').read_text(encoding='utf-8').splitlines():
                    if needle in line:
                        print("found_part of the link")# cheap pre-filter
                        for url in link_re.findall(line):
                            seen.add(url)                            # discard duplicates
#print(list(seen)) #print the array ['a','b','c']
                for url in seen:
                    # new_page = browser.new_page(
                    #         user_agent=ra
                    # )
                    # new_page.bring_to_front()
                    # new_page.goto(url)
                    time.sleep(random.uniform(1, 2))
                    page.goto(url)
                    time.sleep(100)
                    a=1
                    break
                if a>0:
                    break;
                print("checking for the mail")
                time.sleep(random.uniform(1, 2))

        browser.close()

if __name__ == "__main__":
    main()
