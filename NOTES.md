# NOTES.md

## Project Overview

This project scrapes book data from https://books.toscrape.com/.

The scraper visits all catalogue pages, collects book URLs, opens each individual book page, and extracts the required fields for the assessment.

The final dataset is saved as `books.csv`.

---

## Decisions and Trade-offs

- Used Python with requests and BeautifulSoup because they are straightforward and well suited for this type of website.
- Chose a sequential scraping approach to keep the code simple and easy to understand.
- Visited each book's detail page because important fields such as category, UPC, stock count, and review count are not fully available on the catalogue pages.
- Focused on building a scraper specifically for the assessment website instead of creating a generic scraping framework.

---

## Data Volume and Runtime

- The website contains 1,000 books across 50 catalogue pages.
- The scraper first collects all book URLs and then visits each book page individually.
- A requests Session is used to reuse connections and improve efficiency.
- The volume of data is small enough that sequential processing is practical without introducing additional complexity.

---

## What I Would Do Differently With More Time

- Add more detailed validation checks.
- Add logging to a dedicated log file.
- Implement retry handling for temporary request failures.
- Add automated tests for key scraping functions.
- Improve reporting for failed pages and extraction issues.

---

## Areas of Uncertainty

- I reviewed the output structure, row count, required columns, and sample records.
- I did not manually compare every record against the website.
- If the website structure changes, some extraction logic may need to be updated.

---

## Commercial Website Considerations

This assessment website is specifically designed for scraping practice, so permission was not required.

Before scraping a commercial website, I would:

- Review the website's terms of service.
- Check robots.txt guidance.
- Confirm that collecting and storing the data is permitted.
- Ensure requests would not place excessive load on the website.
- Stop and seek clarification if the site's policies are unclear or restrictive.

---

## AI Tool Usage

The following AI tools were used during this assessment:

### ChatGPT

- Helped refine project requirements and prompts.
- Reviewed the scraper structure and overall approach.
- Suggested improvements for readability, reliability, and interview preparation.
- Provided feedback on reports and documentation.

### Claude Code

- Assisted with implementing the Python scraper.
- Helped generate portions of the code and project files.
- Assisted with refining functions, data extraction logic, and report generation.

### Microsoft Copilot

- Used as an additional review tool.
- Checked for potential issues, bugs, simplifications, and improvements.
- Provided feedback on code clarity and assessment compliance.

All code, outputs, reports, and documentation were reviewed and understood before submission. The final submission reflects my understanding of how the scraper works, how the data was collected, and the trade-offs made during implementation.