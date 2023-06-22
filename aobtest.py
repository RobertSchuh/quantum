import zipfile
import re
from tqdm import tqdm

def count_words_in_epub(epub_file):
    word_count = 0

    with zipfile.ZipFile(epub_file, 'r') as zip_ref:
        xhtml_files = [f for f in zip_ref.namelist() if f.endswith('.xhtml')]

        # Add tqdm progress bar
        with tqdm(total=len(xhtml_files), desc="Counting words") as pbar:
            for file_name in xhtml_files:
                with zip_ref.open(file_name) as xhtml_file:
                    content = xhtml_file.read().decode('utf-8')

                    # Remove HTML tags and non-alphanumeric characters
                    content = re.sub('<[^<]+?>', '', content)
                    content = re.sub('[^\w\s]', '', content)

                    # Split into words and count
                    words = content.split()
                    word_count += len(words)

                pbar.update(1)

    return word_count

# Usage example
epub_file_path = r'C:\Users\rober\Downloads\AOAB\Ascendance of a Bookworm Anthology.epub'
total_words = count_words_in_epub(epub_file_path)
print("Total words in the EPUB file:", total_words)
