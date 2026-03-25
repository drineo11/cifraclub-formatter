import sys
import os

# Add project root to path
sys.path.append(os.path.abspath('projeto-cifras'))

from lib.cifra_logic import get_cifra_content

url = "https://www.cifraclub.com.br/asaph-borba/deus-esta-aqui-jesus-em-tua-presenca/"
target_key_index = 5 # From #key=5

print(f"Fetching from {url} with target_key_index={target_key_index}")

try:
    title, artist, key, lines = get_cifra_content(url, target_key_index)
    print(f"Title: {title}")
    print(f"Artist: {artist}")
    print(f"Final Key: {key}")
    
    # Print first 10 lines to see chords clearly
    print("\n--- CHORD PREVIEW ---")
    count = 0
    for line in lines:
        if count > 10: break
        
        # Check if line has details
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
