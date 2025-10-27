# The Definitive download_data.py

import nltk
import ssl

# This is a common fix for network issues on some systems (e.g., SSL certificate errors).
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

print("--- NLTK Data Downloader ---")
print("This script will check for and download all necessary packages.")
print("Please copy the ENTIRE output of this script if you still have issues.")
print("-" * 50)

# A complete list of all required packages.
packages = ['punkt', 'punkt_tab', 'stopwords', 'wordnet', 'omw-1.4']
all_successful = True

for package_id in packages:
    try:
        print(f"Checking for '{package_id}'...")
        # A more reliable way to check is to try loading it.
        # This will raise a LookupError if not found.
        nltk.data.find(f'tokenizers/{package_id}' if 'punkt' in package_id else f'corpora/{package_id}')
        print(f"-> '{package_id}' is already installed.")
    except LookupError:
        print(f"-> '{package_id}' not found. Attempting to download...")
        if nltk.download(package_id):
            print(f"-> Successfully downloaded '{package_id}'.")
        else:
            print(f"-> !!! FAILED to download '{package_id}'. !!!")
            all_successful = False
    except Exception as e:
        print(f"An unexpected error occurred for '{package_id}': {e}")
        all_successful = False

print("-" * 50)
if all_successful:
    print("✅ All necessary packages appear to be ready!")
    print("You can now run 'python chatbot.py' again.")
else:
    print("❌ One or more packages failed to download.")
    print("Please check your internet connection and firewall settings.")
