# PageFetcher

A Python script that fetches web pages from a list of URLs and searches for "Impressum" links in all capitalization variations.

## Description

This script reads URLs from a text file (one URL per line), fetches each webpage, and searches for links containing the word "Impressum" in any capitalization style (impressum, Impressum, IMPRESSUM, ImPrEsSum, etc.). When found, it displays the link text and URL in the console.

## Features

- Reads URLs from a text file with comment support
- Fetches web pages with proper User-Agent headers
- Searches for "Impressum" in all capitalization variations (case-insensitive)
- Converts relative URLs to absolute URLs
- Handles errors gracefully
- Includes rate limiting to be respectful to servers
- Ignores comment lines and shows accurate URL counts
- Fixed BeautifulSoup deprecation warnings

## Installation

1. Make sure you have Python 3.6+ installed
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

```bash
python page_fetcher.py <path_to_pages.txt>
```

### Example

```bash
python page_fetcher.py pages.txt
```

## File Format

The `pages.txt` file should contain one URL per line. Comments are supported:

```
# Main German news sites
https://www.spiegel.de
https://www.zeit.de
    # Technology sites
https://www.heise.de
# https://www.focus.de  (commented out)
```

**Comment Support:**

- Lines starting with `#` are ignored
- Lines with indented `#` (spaces/tabs + #) are also ignored
- Empty lines are skipped

## Impressum Detection

The script searches for "Impressum" in **any capitalization**:

- `impressum` (lowercase)
- `Impressum` (title case)
- `IMPRESSUM` (uppercase)
- `ImPressum` (camel case)
- `ImPrEsSum` (mixed case)
- Any other combination

## Output

The script will display:

- Accurate count of URLs to be processed (excludes comments)
- Progress information for each URL
- Success/failure status for each page fetched
- Impressum links found (if any) with their text and URLs

### Sample Output

```
PageFetcher - Impressum Link Finder
========================================
Processing 4 URLs from pages.txt
------------------------------------------------------------

Line 2: Checking https://www.spiegel.de
✓ Found 1 Impressum link(s):
  1. Text: 'Impressum'
     URL:  https://www.spiegel.de/impressum

Line 3: Checking https://www.zeit.de
✓ Found 1 Impressum link(s):
  1. Text: 'IMPRESSUM'
     URL:  https://www.zeit.de/impressum

Line 5: Checking https://www.heise.de
✗ No Impressum links found

========================================
Processing complete!
```

## Requirements

- Python 3.6+
- requests library
- beautifulsoup4 library

## Error Handling

The script handles various error conditions:

- Invalid URLs
- Network errors
- Timeout errors
- File not found errors

## Note

"Impressum" is a German legal requirement for websites, so this tool is particularly useful for checking German websites for their legal disclosure pages.
