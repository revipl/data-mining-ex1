import json
import time
from selenium.webdriver import Edge
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options

# General Settings
URL = ('https://www.indiegogo.com/explore/home?project_timing=all'
       '&product_stagall&sort=trending')
PAUSE_TIME = 3  # in seconds
MAX_PAGES = 300

# Indiegogo scraping XPATHs (crawler)
XPATH_INDIEGOGO_FOOTER = '//div[@class="brandRefreshFooterDesktop"]'
XPATH_INDIEGOGO_PROJECT_URL = ('//div[@class="projectDiscoverableCard '
                               'discoverableCard"]/a')

# Indiegogo scraping XPATHs (extract project data)
XPATH_PROJECT_TITLE = ('//div[@class="basicsSection-title fullhd '
                       't-h3--sansSerif"]')
XPATH_PROJECT_CREATORS = ('//div['
                          '@class="basicsCampaignOwner-details-name"]')

# Driver Settings
edge_options = Options()
edge_options.add_argument("--headless")  # GUI is off
edge_options.add_argument("--no-sandbox")
edge_options.add_argument("--start-maximized")
edge_options.add_argument("--disable-dev-shm-usage")
driver = Edge(options=edge_options)


def indiegogo_crawler(URL: str) -> None:
    """
    Scraping Indiegogo website for project URLs.
    It uses Selenium WebDriver to load the webpage, extract project URLs,
    and scroll down to load more projects until the maximum number of
    pages is reached.
    :param URL: the projects' URL in Indiegogo
    """
    driver.get(URL)
    time.sleep(PAUSE_TIME)  # Wait for the page to load

    project_urls = []
    indiegogo_footer = driver.find_element(By.XPATH,
                                           XPATH_INDIEGOGO_FOOTER)

    while len(project_urls) < MAX_PAGES:
        # get all the project links on the page
        project_links = driver.find_elements(By.XPATH,
                                             XPATH_INDIEGOGO_PROJECT_URL)
        project_urls += [link.get_attribute('href') for link in project_links]
        print(f"total project_urls (so far): {len(project_urls)}")

        # scroll down to the bottom of the page
        driver.execute_script("arguments[0].scrollIntoView(true);",
                              indiegogo_footer)

        time.sleep(2)  # wait for the page to load with new content

    driver.quit()


def extract_project_data(index_id: int, URL: str, records: list) -> None:
    """
    Extracts project data from a given Indiegogo project URL.
    :param index_id: The index of the project in the list of URLs.
    :param URL: The URL of the Indiegogo project.
    :param records: A list to store the extracted project data.
    """
    driver.get(URL)
    time.sleep(PAUSE_TIME)

    try:
        title = driver.find_element(By.XPATH, XPATH_PROJECT_TITLE).text
    except:
        title = 'Unknown'

    print(title)

    try:
        creators = driver.find_element(By.XPATH, XPATH_PROJECT_CREATORS).text
    except:
        creators = 'Unknown'

    print(creators)

    # record = {
    #         "id": str(index_id + 1),
    #         "url": URL,
    #         "Creators": creators,
    #         "Title": project_title,
    #         "Text": project_description,
    #         "DollarsPledged": dollars_pledged,
    #         "DollarsGoal": dollars_goal,
    #         "NumBackers": num_backers,
    #         "DaysToGo": days_to_go,
    #         "FlexibleGoal": flexible_goal
    #     }
    # records.append(record)

    driver.quit()


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
    with open('indiegogo_projects.json', 'w') as json_file:
        json.dump(output, json_file, indent=2)

    print("Scraping complete. Data saved to indiegogo_projects.json")


def main():
    # project_urls = indiegogo_crawler(URL)
    records = []

    extract_project_data(1,
                         "https://www.indiegogo.com/projects/neo-ps1-ultra"
                         "-short-throw-smart"
                         "-projector", [])
    # for id, url in project_urls:
    #     extract_project_data(id, url, records)

    # extract_projects_data_to_json(records)


if __name__ == "__main__":
    main()
