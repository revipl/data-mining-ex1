import os
import json
import time
import multiprocessing as mp
from selenium.webdriver import Edge
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options

# General Settings
OUTPUT_DIR = "../../output/problem1"
PROJECT_URLS_FILE_NAME = "project_urls.txt"
URL = ('https://www.indiegogo.com/explore/home?project_timing=all'
       '&product_stagall&sort=trending')
PAUSE_TIME = 2  # in seconds
NUM_OF_PROJECTS = 300
DEBUG = False
DIVIDER = '*' * 100

# Indiegogo scraping XPATHs (crawler)
XPATH_INDIEGOGO_FOOTER = '//div[@class="brandRefreshFooterDesktop"]'
XPATH_INDIEGOGO_PROJECT_URL = ('//div[@class="projectDiscoverableCard '
                               'discoverableCard"]/a')

# Driver Settings
edge_options = Options()
edge_options.add_argument("--headless")  # GUI is off
edge_options.add_argument("--no-sandbox")
edge_options.add_argument("--start-maximized")
edge_options.add_argument("--disable-dev-shm-usage")


def indiegogo_crawler(URL: str) -> None:
    """
    Scraping Indiegogo website for project URLs.
    It uses Selenium WebDriver to load the webpage, extract project URLs,
    and scroll down to load more projects until the maximum number of
    pages is reached.
    :param URL: the projects' URL in Indiegogo
    """
    print(f"Gathering projects URLs:")
    driver = Edge(options=edge_options)
    driver.get(URL)
    # time.sleep(PAUSE_TIME)  # Wait for the page to load

    project_urls = []
    indiegogo_footer = driver.find_element(By.XPATH,
                                           XPATH_INDIEGOGO_FOOTER)

    while len(project_urls) < NUM_OF_PROJECTS:
        # get all the project links on the page
        project_links = driver.find_elements(By.XPATH,
                                             XPATH_INDIEGOGO_PROJECT_URL)
        project_urls += [link.get_attribute('href') for link in project_links]
        print(f"→ total project_urls (so far): {len(project_urls)}")

        # scroll down to the bottom of the page
        driver.execute_script("arguments[0].scrollIntoView(true);",
                              indiegogo_footer)

        time.sleep(PAUSE_TIME)  # wait for the page to load with new content

    driver.quit()

    with open(PROJECT_URLS_FILE_NAME, 'w+') as f:
        for url in project_urls:
            f.write('%s\n' % url)


def extract_project_data(index_id: int, URL: str) -> dict:
    """
    Extracts project data from a given Indiegogo project URL.
    :param index_id: The index of the project in the list of URLs.
    :param URL: The URL of the Indiegogo project.
    :param records: A list to store the extracted project data.
    """

    print(f"Project: {index_id}/{NUM_OF_PROJECTS}")

    driver = Edge(options=edge_options)
    driver.get(URL)
    # time.sleep(PAUSE_TIME)  # Wait for the page to load

    try:
        creators = driver.find_element(By.CLASS_NAME,
                                       'basicsCampaignOwner-details-name')
        creators = creators.get_attribute('innerText')
        creators = ' '.join(creators.split())
    except:
        creators = 'Unknown'
    if DEBUG:
        print(f"creators: {creators}")

    try:
        title = driver.find_element(By.CLASS_NAME, 'basicsSection-title')
        title = title.get_attribute('innerText')
        title = ' '.join(title.split())

    except:
        title = 'Unknown'
    if DEBUG:
        print(f"title: {title}")

    try:
        description = driver.find_element(By.CLASS_NAME,
                                          'basicsSection-tagline')
        description = description.get_attribute('innerText')
        description = ' '.join(description.split())
    except:
        description = 'Unknown'
    if DEBUG:
        print(f"description: {description}")

    try:
        dollars_pledged = driver.find_element(By.CLASS_NAME,
                                              'basicsGoalProgress-amountSold')
        dollars_pledged = dollars_pledged.get_attribute('innerText')
        dollars_pledged = ' '.join(dollars_pledged.split())
        dollars_pledged = int(''.join(c for c in dollars_pledged if
                                      c.isdigit()))
    except:
        dollars_pledged = 'Unknown'
    if DEBUG:
        print(f"dollars_pledged: {dollars_pledged}")

    try:
        dollars_goal = driver.find_element(By.CLASS_NAME,
                                           'basicsGoalProgress-progressDetails-detailsGoal-goalPercentageOrInitiallyRaised')
        dollars_goal = dollars_goal.get_attribute('textContent')
        dollars_goal = ' '.join(dollars_goal.split())
        dollars_goal = dollars_goal[dollars_goal.find("of "):]
        dollars_goal = int(''.join(c for c in dollars_goal if c.isdigit()))
    except:
        dollars_goal = 'Unknown'
    if DEBUG:
        print(f"dollars_goal: {dollars_goal}")

    try:
        num_backers = driver.find_element(By.CLASS_NAME,
                                          'basicsGoalProgress-claimedOrBackers')
        num_backers = num_backers.get_attribute('textContent')
        num_backers = ' '.join(num_backers.split())
        num_backers = int(''.join(c for c in num_backers if c.isdigit()))
    except:
        num_backers = 'Unknown'
    if DEBUG:
        print(f"dollars_goal: {num_backers}")

    try:
        days_to_go = driver.find_element(By.CLASS_NAME,
                                         'basicsGoalProgress-progressDetails-detailsTimeLeft')
        days_to_go = days_to_go.get_attribute('textContent')
        days_to_go = ' '.join(days_to_go.split())
        days_to_go = int(''.join(c for c in days_to_go if c.isdigit()))
    except:
        days_to_go = 'Unknown'
    if DEBUG:
        print(f"dollars_goal: {days_to_go}")

    try:
        flexible_goal = driver.find_element(By.CLASS_NAME,
                                            'basicsGoalProgress-progressDetails-detailsGoal-goalWording')
        flexible_goal = flexible_goal.get_attribute('textContent')
        flexible_goal = ' '.join(flexible_goal.split())
        flexible_goal = \
            True if flexible_goal.lower().find('flexible') != -1 else False
    except:
        flexible_goal = False
    if DEBUG:
        print(f"flexible_goal: {flexible_goal}")

    record = {
        "id": str(index_id + 1),
        "url": URL,
        "Creators": creators,
        "Title": title,
        "Text": description,
        "DollarsPledged": dollars_pledged,
        "DollarsGoal": dollars_goal,
        "NumBackers": num_backers,
        "DaysToGo": days_to_go,
        "FlexibleGoal": flexible_goal
    }
    driver.quit()
    print(DIVIDER)
    return record


def extract_projects_data_to_json(records: list) -> None:
    """
    Takes a list of project records and saves them to a JSON file.
    :param records: A list of dictionaries, where each dictionary represents
    a project record.
    """
    # Structure data into the desired JSON format
    output = {
        "records": {
            "record": records
        }
    }

    # Output to JSON file
    output_file = os.path.join(OUTPUT_DIR, "data.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2)

    print(f"Scraping complete. Data saved to {output_file}")


def workertest(records_queue, project_urls_queue):
    while True:
        try:
            index, url = project_urls_queue.get()
            if index is None:  # Sentinel value to signal termination
                break
            record = extract_project_data(index, url)
            records_queue.put(record)
        except Exception as e:
            print(f"Error in worker process: {e}")


def main(crawler=True, browsers=5):
    records = []
    project_id = 0

    # fixed goal project:
    # https://www.indiegogo.com/projects/racebox-micro-diy-gps-data-for-the-driven--2

    # flexible goal project:
    # https://www.indiegogo.com/projects/neo-ps1-ultra-short-throw-smart-projector

    # test single project:
    # extract_project_data(0,
    #                      "https://www.indiegogo.com/projects/racebox-micro-diy-gps-data-for-the-driven--2", records)

    if crawler:
        indiegogo_crawler(URL)

    f = open(PROJECT_URLS_FILE_NAME, "r")
    project_urls = f.read().splitlines()
    f.close()

    # single thread
    # for index, url in enumerate(project_urls):
    #     records.append(extract_project_data(index+1, url))

    # multiprocessing
    records_queue = mp.Queue()  # Queue to store extracted records
    project_urls_queue = mp.Queue()  # Queue to store tasks (index, url)

    # enqueue project URLs (replace with your actual URLs)
    for index, url in enumerate(project_urls):
        project_urls_queue.put((index + 1, url))

    # create and start worker processes
    workers = [mp.Process(target=workertest, args=(records_queue,
                                               project_urls_queue)) for _ in
               range(browsers)]
    for worker in workers:
        worker.start()

    # put sentinel values to signal end of tasks (one for each worker)
    for _ in range(browsers):
        project_urls_queue.put((None, None))

    # collect extracted records from the queue
    records = []
    while not records_queue.empty():
        record = records_queue.get()
        records.append(record)

    # wait for worker processes to finish
    for worker in workers:
        worker.join()

    extract_projects_data_to_json(records)


if __name__ == "__main__":
    main(crawler=False)
