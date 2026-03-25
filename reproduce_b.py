import sys
import os

# Add project root to path
sys.path.append(os.path.abspath('projeto-cifras'))

from lib.cifra_logic import get_cifra_content

# Problematic URL
url = "https://www.cifraclub.com.br/asaph-borba/ao-unico/#key=2"
# Expecting Key B (key=2)
# User says they got C.

print(f"Fetching from {url}")

try:
    title, artist, key, lines = get_cifra_content(url)
    print(f"Title: {title}")
    print(f"Artist: {artist}")
    print(f"Final Key: {key}") # Should be B
    
    # Print preview
    print("\n--- CHORD PREVIEW ---")
    count = 0
    for line in lines:
        if count > 10: break
        line_text = ""
        for seg in line:
            text = seg['text']
            if seg['bold']:
                text = f"[{text}]"
            line_text += text
        print(line_text)
        count += 1
    print("--- END PREVIEW ---\n")
        
except Exception as e:
    print(f"Error: {e}")
