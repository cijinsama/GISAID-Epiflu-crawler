"""
Possible reconstructure:
abstract method to deal with 
<tr>
    <td> src1
    <td> src2
<tr>
    <td> dst1
    <td> dst2
, which is used in `select_type`...
and

<tr>
    <td> src1
    <td> dst1
    <td> src2
    <td> dst2
, which is used in `select_Submission_Date`...
"""
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException 
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
import time
import re

def print_retry():
    print("Element reference is stale, retrying...")

def setup_driver():
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument('--disable-dev-shm-usage')
    prefs = {
        "download.prompt_for_download": False,  # Disable the download prompt
        "directory_upgrade": True,  # Allow changing the download directory
        "profile.managed_default_content_settings.images": 2
    }
    chrome_options.add_experimental_option("prefs", prefs)

    # Initialize WebDriver with the ChromeOptions
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def login(driver, Username, Password, timeout):
    # Open the target webpage
    driver.get("https://platform.epicov.org/epi3/frontend#79487")
    
    # Explicitly wait to ensure the page loads completely
    WebDriverWait(driver, timeout).until(
        expected_conditions.presence_of_element_located((By.ID, "elogin"))
    )

    # Locate the username input field and enter the username
    username_field = driver.find_element(By.ID, "elogin")
    username_field.clear()
    username_field.send_keys(Username)  # Replace with the actual username

    # Locate the password input field and enter the password
    password_field = driver.find_element(By.ID, "epassword")
    password_field.clear()
    password_field.send_keys(Password)  # Replace with the actual password

    # Locate and click the login button
    login_button = driver.find_element(By.CSS_SELECTOR, "input.form_button_submit")
    login_button.click()

def goto_SearchPage(driver, timeout):
    # Wait for the EpiFlu™ element to become visible
    epi_flu_button = WebDriverWait(driver, timeout).until(
        expected_conditions.element_to_be_clickable((By.LINK_TEXT, "EpiFlu™"))
    )
    epi_flu_button.click()
    
    # Navigate to the "Search" option on the EpiFlu page
    wait = WebDriverWait(driver, timeout)
    while True:
        try:
            search_button = wait.until(
                expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, "div.sys-actionbar-action-ni[onclick*='Browse']"))
            )
            search_button.click()
            break
        except StaleElementReferenceException:
            print_retry()

def input_SearchPatterns(driver, SearchPatterns, timeout):
    search_pattern_label = WebDriverWait(driver, timeout).until(
                expected_conditions.presence_of_element_located((By.XPATH, "//div[text()='Search patterns']"))
            )
    search_pattern_input = search_pattern_label.find_element(By.XPATH, "./ancestor::tr//input")
    search_pattern_input.clear()
    search_pattern_input.send_keys(SearchPatterns)

def get_select_by_header(driver, timeout, header_text):
    # locate td where header exist
    header_div = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, f"//tr/td/div[text()='{header_text}']"))
    )
    header_td = header_div.find_element(By.XPATH, "./parent::td")
    
    # calc index of td in tr
    all_tds = header_td.find_elements(By.XPATH, "../td")
    index = all_tds.index(header_td) + 1  # XPath索引从1开始
    
    # select corresponding one
    select_element = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((
            By.XPATH, 
            f"//tr[td/div[text()='{header_text}']]/following-sibling::tr[1]/td[{index}]//select"
        ))
    )
    return select_element

def select_type(driver, typ, timeout):
    h_select = get_select_by_header(driver, timeout, "Type")
    Select(h_select).deselect_all()
    if typ is not None and len(typ) > 0:
        Select(h_select).select_by_visible_text(typ)
    wait_spinning_loader(driver, timeout)

def select_H(driver, H, timeout):
    h_select = get_select_by_header(driver, timeout, "H")
    Select(h_select).deselect_all()
    if H is not None and len(H) > 0:
        Select(h_select).select_by_visible_text(H)
    wait_spinning_loader(driver, timeout)

def select_N(driver, N, timeout):
    n_select = get_select_by_header(driver, timeout, "N")
    Select(n_select).deselect_all()
    if N is not None and len(N) > 0:
        Select(n_select).select_by_visible_text(N)
    wait_spinning_loader(driver, timeout)

def select_Host(driver, Host, timeout):
    host_select = get_select_by_header(driver, timeout, "Host")
    Select(host_select).deselect_all()
    if Host is not None and len(Host) > 0:
        Select(host_select).select_by_visible_text(Host)
    wait_spinning_loader(driver, timeout)

def input_Submission_Date(driver, start_date, end_date, timeout):
    type_div = driver.find_element(By.XPATH, "//div[text()='Submission date from']")
    parent_td = type_div.find_element(By.XPATH, "./ancestor::td[1]")
    next_td = parent_td.find_element(By.XPATH, f"./following-sibling::td")
    input_place = next_td.find_element(By.CSS_SELECTOR, "input.sys-event-hook.sys-fi-mark.hasDatepicker")
    input_place.clear()
    if start_date is not None:
        input_place.send_keys(start_date.strftime("%Y-%m-%d"))
    next_td = next_td.find_element(By.XPATH, f"./following-sibling::td")
    next_td = next_td.find_element(By.XPATH, f"./following-sibling::td")
    input_place = next_td.find_element(By.CSS_SELECTOR, "input.sys-event-hook.sys-fi-mark.hasDatepicker")
    input_place.clear()
    if end_date is not None:
        input_place.send_keys(end_date.strftime("%Y-%m-%d"))

def select_Required_Segments(driver, Segments, timeout):
    segment_div = driver.find_element(By.XPATH, "//div[text()='Required Segments']")
    parent_td = segment_div.find_element(By.XPATH, "./ancestor::td[1]")
    next_td = parent_td.find_element(By.XPATH, f"./following-sibling::td")
    checkbox = WebDriverWait(next_td, timeout).until(
        expected_conditions.presence_of_element_located((By.XPATH, f'//input[@type="checkbox" and @value="{Segments}"]'))
    )
    checkbox.click()
    while not checkbox.is_selected():
        print_retry()
        time.sleep(1)
        checkbox.click()
    wait_spinning_loader(driver, timeout)

def select_only_complete(driver, timeout):
    only_complete_span = driver.find_element(By.XPATH, '//span[text()="only complete"]')
    parent_div = only_complete_span.find_element(By.XPATH, "./ancestor::div[1]")
    checkbox = WebDriverWait(parent_div, timeout).until(
        expected_conditions.presence_of_element_located((By.XPATH, f'//input[@type="checkbox" and @value="y"]'))
    )
    while checkbox.get_attribute("disabled") is not None:
        print_retry()
        time.sleep(1)
        only_complete_span = driver.find_element(By.XPATH, '//span[text()="only complete"]')
        parent_div = only_complete_span.find_element(By.XPATH, "./ancestor::div[1]")
        checkbox = WebDriverWait(parent_div, timeout).until(
            expected_conditions.presence_of_element_located((By.XPATH, f'//input[@type="checkbox" and @value="y"]'))
        )
    checkbox.click()
    while not checkbox.is_selected():
        print_retry()
        time.sleep(1)
        checkbox.click()
    wait_systimer(driver, timeout)

def wait_systimer(driver, timeout):
    sys_timer = WebDriverWait(driver, timeout).until(
        expected_conditions.presence_of_element_located((By.ID, "sys_timer"))
    )
    WebDriverWait(driver, timeout).until(
        lambda driver: sys_timer.get_attribute("style") == "display: none;"
    )

def wait_spinning_loader(driver, timeout):
    WebDriverWait(driver, timeout).until(
        lambda d: d.find_element(By.ID, "sys_curtain").value_of_css_property("display") == "none"
    )

def select_all(driver, timeout):
    checkbox = WebDriverWait(driver, timeout).until(
        expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, "input[type='checkbox'][onclick^='sys.getC'][onclick*='toggleAll(this)']"))
    )
    checkbox.click()

def goto_download_frame(driver, timeout):
        # Click on the Download button
        new_download_button = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, ".//button[text()='Download']"))
        )
        new_download_button.click()

        # Enter iframe
        iframe = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.TAG_NAME, "iframe"))
        )
        driver.switch_to.frame(iframe)

def filters(driver, SearchPatterns, Type, H, N, Host, start_date, end_date, Segments, not_complete, timeout):
    input_SearchPatterns(driver, SearchPatterns, timeout)
    select_type(driver, Type, timeout)
    select_H(driver, H, timeout)
    select_N(driver, N, timeout)
    select_Host(driver, Host, timeout)
    input_Submission_Date(driver, start_date, end_date, timeout)
    select_Required_Segments(driver, Segments, timeout)
    if ~not_complete:
        select_only_complete(driver, timeout)

def search(driver, timeout):
    button_element = WebDriverWait(driver, timeout).until(
        expected_conditions.element_to_be_clickable((By.XPATH, "//button[text()='Search']"))
    )
    button_element.click()

    viruses, sequences = get_virus_and_sequence_numbers(driver, timeout)
    if sequences < 1:
        raise ValueError("Find 0 sequence. Change your filter")
    else:
        print(f"Found {viruses} viruses and {sequences} sequences")

def get_virus_and_sequence_numbers(driver, timeout):
    element = WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((
            By.XPATH,
            "//span["
            "contains(., 'Total:') "
            "and contains(., 'viruses (') "
            "and contains(., 'sequences)')"
            "]"
        ))
    )
    text = element.text.strip()
    
    pattern = r"Total: (\d{1,3}(?:,\d{3})*) viruses \((\d{1,3}(?:,\d{3})*) sequences\)"
    match = re.search(pattern, text)
    
    if not match:
        raise ValueError(f"Re Error: {text}")
    
    viruses = int(match.group(1).replace(",", ""))
    sequences = int(match.group(2).replace(",", ""))
    
    return viruses, sequences

def wait_table(driver, timeout):
    tbody = WebDriverWait(driver, timeout).until(
        expected_conditions.presence_of_element_located((By.XPATH, '//tbody[tabindex()="0"]'))
    )

def download_meta(driver, timeout):
    # Select metadata
    checkbox = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.XPATH, "//input[contains(@class, 'sys-event-hook') and @type='radio' and @value='xls']"))
    )
    checkbox.click()

    # download metadata
    time.sleep(timeout)
    second_download_button = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.XPATH, ".//button[text()='Download']"))
    )
    second_download_button.click()

def download_protein(driver, timeout, header_pattern):
    # Select "Sequences (proteins) as FASTA"
    checkbox = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.XPATH, "//input[contains(@class, 'sys-event-hook') and @type='radio' and @value='proteins']"))
    )
    checkbox.click()
    
    # Select Proteins as "all"
    checkbox = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.XPATH, "//input[contains(@class, 'sys-event-hook') and @type='checkbox' and @value='all']"))
    )
    checkbox.click()

    # Enter the FASTA Header
    fasta_header_input = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'sys-form-filabel') and text()='FASTA Header']"))
    )
    fasta_header_input = fasta_header_input.find_element(By.XPATH, "./ancestor::tr[1]//input")
    fasta_header_input.clear()
    fasta_header_input.send_keys(header_pattern)
    
    # download fasta
    time.sleep(timeout)
    second_download_button = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.XPATH, ".//button[text()='Download']"))
    )
    second_download_button.click()
