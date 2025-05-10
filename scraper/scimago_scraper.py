import json
import os
import time
import requests
from bs4 import BeautifulSoup
from pathlib import Path

class ScimagoScraper:
    def __init__(self):
        self.base_url = "https://www.scimagojr.com/journalsearch.php"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.existing_data = self._load_existing_data()

    def _normalize_title(self, title):
        """Normalize journal title to match Scimago's format"""
        # Convert to lowercase and trim spaces
        normalized = title.lower().strip()
        # Replace multiple spaces with single space
        normalized = ' '.join(normalized.split())
        # Keep special characters that are significant for journal titles
        # but remove unwanted punctuation
        normalized = normalized.replace('&', 'and')
        # Remove specific unwanted characters but keep numbers and letters
        return normalized

    def _load_existing_data(self):
        json_path = Path(__file__).parent.parent / 'datos' / 'json' / 'revistas.json'
        if json_path.exists():
            with open(json_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _save_data(self, data):
        json_path = Path(__file__).parent.parent / 'datos' / 'json' / 'scimago_journals.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _get_issn_from_title(self, title):
        # Extract ISSN from the existing data if available
        for journal in self.existing_data.get('journals', []):
            if journal.get('title') == title:
                return journal.get('issn', '')
        return ''

    def scrape_journal(self, title, issn=''):
        # Check if we already have the data for this journal
        for journal in self.existing_data.get('journals', []):
            if journal.get('title') == title:
                print(f"Journal '{title}' already exists in database.")
                return journal

        # Search for the journal
        params = {'q': title}
        response = requests.get(self.base_url, params=params, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the correct journal link with more flexible matching
        journal_links = soup.select('a.jrnlname')
        journal_url = None
        
        normalized_search_title = self._normalize_title(title)
        
        # Try exact match first
        for link in journal_links:
            normalized_link_title = self._normalize_title(link.text)
            if normalized_search_title == normalized_link_title:
                journal_url = 'https://www.scimagojr.com/' + link['href']
                break
        
        # If no exact match, try partial match
        if not journal_url:
            for link in journal_links:
                normalized_link_title = self._normalize_title(link.text)
                # Check if all words from search title appear in the link title
                search_words = set(normalized_search_title.split())
                link_words = set(normalized_link_title.split())
                if search_words.issubset(link_words) or link_words.issubset(search_words):
                    journal_url = 'https://www.scimagojr.com/' + link['href']
                    print(f"Found similar match: {link.text}")
                    break
        
        if not journal_url:
            print(f"Could not find journal: {title}")
            return None

        # Get journal details
        response = requests.get(journal_url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        journal_data = {
            'title': title,
            'website': '',
            'h_index': '',
            'subject_areas': [],
            'publisher': '',
            'issn': issn or self._get_issn_from_title(title),
            'publication_type': '',
            'widget_url': ''
        }

        # Extract data
        cell_data = soup.select('div.cell_data')
        for cell in cell_data:
            label = cell.select_one('.label')
            if not label:
                continue
            
            label_text = label.text.strip().lower()
            if 'publisher:' in label_text:
                journal_data['publisher'] = cell.select_one('.data').text.strip()
            elif 'type:' in label_text:
                journal_data['publication_type'] = cell.select_one('.data').text.strip()
            elif 'issn:' in label_text and not journal_data['issn']:
                journal_data['issn'] = cell.select_one('.data').text.strip()
            elif 'h index:' in label_text:
                journal_data['h_index'] = cell.select_one('.data').text.strip()

        # Get subject areas
        subjects = soup.select('div.subject_area span.subject_area_item')
        journal_data['subject_areas'] = [subject.text.strip() for subject in subjects]

        # Get website if available
        website_link = soup.select_one('a[title="Go to website"]')
        if website_link:
            journal_data['website'] = website_link['href']

        # Get widget URL
        widget_div = soup.select_one('#widget')
        if widget_div:
            iframe = widget_div.select_one('iframe')
            if iframe:
                journal_data['widget_url'] = iframe['src']

        # Add delay to be respectful to the server
        time.sleep(2)
        
        return journal_data

    def scrape_journals(self):
        all_journals = []
        existing_journals = set()

        # Add existing journals to avoid duplicates
        if self.existing_data and 'journals' in self.existing_data:
            for journal in self.existing_data['journals']:
                if journal not in all_journals:
                    all_journals.append(journal)
                    existing_journals.add(journal['title'])

        # Read the current journals.json
        with open(Path(__file__).parent.parent / 'datos' / 'json' / 'revistas.json', 'r', encoding='utf-8') as f:
            current_data = json.load(f)

        # Process each journal
        for title in current_data.keys():
            if title and title not in existing_journals:
                normalized_title = self._normalize_title(title)
                print(f"Scraping data for: {normalized_title}")
                journal_data = self.scrape_journal(normalized_title)
                if journal_data and journal_data not in all_journals:
                    all_journals.append(journal_data)
                    existing_journals.add(title)

        # Save the combined data
        output_data = {'journals': all_journals}
        self._save_data(output_data)
        print(f"Scraping completed. Saved {len(all_journals)} journals to scimago_journals.json")

if __name__ == '__main__':
    scraper = ScimagoScraper()
    scraper.scrape_journals()
