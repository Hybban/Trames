import os
import re

def fix_file(filepath):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern 0: Convert "**Encadré** **Title :** Content" to "> **Title :** Content"
    content = re.sub(r'^\*\*Encadré\*\*\s+', r'> ', content, flags=re.MULTILINE)
    
    # Pattern 1: Encadré headers that are already converted to separate lines
    # > **Title :** \n*Content*
    # We want: > **Title :** *Content*
    # new_content = re.sub(r'>( \*\*.* : \*\*) \n\*(.*)\*', r'>\1 *\2*', content)
    
    # Pattern 2: Multi-line blocks (like in 05)
    # > **Title :** \n**Header**\n* Bullet
    # We want: > **Title :** **Header**\n> * Bullet
    
    # Actually, let's do a more generic fix for all > **Title :** headers
    lines = content.splitlines()
    fixed_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("> **") and line.endswith(" :** "):
            title = line
            i += 1
            if i < len(lines):
                next_line = lines[i]
                # Join with a space and keep the > prefix
                joined = title + next_line
                fixed_lines.append(joined)
            else:
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)
        i += 1
        
    final_content = "\n".join(fixed_lines)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(final_content)
    print(f"Fixed {filepath}")

from pathlib import Path

# Locate the Sources directory relative to the script's location
script_dir = Path(__file__).parent
sources_dir = script_dir.parent / "Sources"

if not sources_dir.exists():
    print(f"Sources directory not found at: {sources_dir}")
else:
    # Find all markdown files recursively in the Sources directory
    for filepath in sources_dir.rglob("*.md"):
        fix_file(str(filepath))
