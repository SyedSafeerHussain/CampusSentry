from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

def run_bot():
    print("✅ Bot has started running...")
    driver = webdriver.Chrome()
    url = "https://erp.superior.edu.pk/web/login?redirect=https%3A%2F%2Ferp.superior.edu.pk%2Fstudents%2Fdashboard"
    driver.get(url)
    time.sleep(2)

    # Login
    user_id = driver.find_element(By.XPATH, "//*[@id='login']")
    user_id.send_keys("SU73-BSAIM-F24-002")
    password = driver.find_element(By.XPATH, "//*[@id='password']")
    password.send_keys("00@Ali514")
    button = driver.find_element(By.XPATH, "//*[@id='wrapwrap']/main/div/div/div/form/button")
    button.click()
    time.sleep(5)

    # Collect main links
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='hierarchical-show']"))
    )

    subjects = []
    links = []
    divs = driver.find_elements(By.XPATH, "//*[@id='hierarchical-show']/div")

    for div in divs:
        if len(links) >= 8:
            break
        try:
            link = div.find_element(By.XPATH, "./a").get_attribute('href')
            if link and link != 'javascript:void(0);':
                links.append(link)
                sub = div.find_element(By.XPATH, "./a/span").text
                subjects.append(sub if sub else "N/A")
        except:
            continue

    print(f"\nTotal links found: {len(links)}")

    # Final output
    with open("std.csv", 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Subject", "Assessment", "Obtained Marks"])

        for i, subject_url in enumerate(links):
            print(f"\nProcessing Subject {i+1}: {subjects[i]}")
            driver.get(subject_url)
            time.sleep(1)

            seen = set()  # to avoid duplicates

            try:
                parent_rows = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tr.table-parent-row"))
                )

                for row in parent_rows:
                    try:
                        expand_link = row.find_element(By.CSS_SELECTOR, "td a")
                        driver.execute_script("arguments[0].click();", expand_link)
                        time.sleep(0.5)
                    except Exception as e:
                        print(f"  Expand error: {e}")
                        continue

                # Now all child rows should be visible
                child_rows = driver.find_elements(By.CSS_SELECTOR, "tr.table-child-row")
                print(f"  Found {len(child_rows)} child rows.")

                for child in child_rows:
                    columns = child.find_elements(By.TAG_NAME, "td")
                    if len(columns) >= 4:
                        assessment_name = columns[0].text.strip()
                        obtained_marks = columns[3].text.strip()
                        if obtained_marks and "Obtained Marks" not in assessment_name:
                            key = (assessment_name, obtained_marks)
                            if key not in seen:
                                seen.add(key)
                                writer.writerow([subjects[i], assessment_name, obtained_marks])
                                print(f"{assessment_name} → {obtained_marks}")

            except Exception as e:
                print(f"Error finding rows: {e}")

    driver.quit()
