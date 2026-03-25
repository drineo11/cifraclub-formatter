import sys
import os

# Add project root to path
sys.path.append(os.path.abspath('projeto-cifras'))

from lib.cifra_logic import get_cifra_content

# Problematic URL
url = "https://www.cifraclub.com.br/julliany-souza/quem-e-esse/#capo=0&key=3"
# Expecting Key C (key=3)
# User says they got A.

print(f"Fetching from {url}")

try:
    title, artist, key, lines = get_cifra_content(url)
    print(f"Title: {title}")
    print(f"Artist: {artist}")
    print(f"Final Key: {key}") # Should be C
    
    print("\n--- FULL CHORD PREVIEW ---")
    for line in lines:
        line_text = ""
        for seg in line:
            text = seg['text']
            if seg['bold']:
                text = f"[{text}]"
            line_text += text
        print(line_text)
    print("--- END PREVIEW ---\n")
        
except Exception as e:
    print(f"Error: {e}")
