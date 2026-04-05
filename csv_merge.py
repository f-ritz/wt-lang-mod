#!/usr/bin/env python3
"""
CSV merge utility:
1. Joins incomplete lines (those not ending with ";;")
2. Compares first entries between units_old.csv and units_default.csv
3. Appends missing entries from default to old
"""

def fix_incomplete_lines(filepath):
    """
    Read a CSV file and join lines that don't end with ";;".
    Returns a list of complete lines.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    fixed_lines = []
    i = 0
    while i < len(lines):
        current_line = lines[i].rstrip('\n')
        
        # Keep joining lines until we find one ending with ";;
        while not current_line.endswith(';;') and i + 1 < len(lines):
            i += 1
            current_line += lines[i].rstrip('\n')
        
        fixed_lines.append(current_line)
        i += 1
    
    return fixed_lines


def extract_first_entry(line):
    """
    Extract the first entry from a line (first field before the first delimiter).
    Assumes fields are separated by some delimiter - adjust if needed.
    """
    # Split by common delimiters (comma, semicolon, etc.)
    # Adjust based on your actual delimiter
    if not line:
        return None
    
    # If using semicolon as delimiter
    parts = line.split(';')
    return parts[0].strip() if parts else None


def merge_csv_files(old_file, default_file, output_file=None):
    """
    Main merge logic:
    1. Fix incomplete lines in both files
    2. Compare first entries
    3. Append missing entries from default to old
    """
    
    print("Reading and fixing incomplete lines...")
    old_lines = fix_incomplete_lines(old_file)
    default_lines = fix_incomplete_lines(default_file)
    
    print(f"Old file: {len(old_lines)} complete lines")
    print(f"Default file: {len(default_lines)} complete lines")
    
    # Create a mapping of first entries in old file
    old_entries = {}
    for i, line in enumerate(old_lines):
        first_entry = extract_first_entry(line)
        if first_entry:
            old_entries[first_entry] = i
    
    print(f"Old file has {len(old_entries)} unique first entries")
    
    # Check default entries and append missing ones
    added_count = 0
    for default_line in default_lines:
        first_entry = extract_first_entry(default_line)
        
        if first_entry and first_entry not in old_entries:
            print(f"  Adding missing entry: {first_entry}")
            old_lines.append(default_line)
            added_count += 1
    
    print(f"Added {added_count} missing entries from default file")
    
    # Write output
    output_path = output_file or old_file.replace('.csv', '_merged.csv')
    with open(output_path, 'w', encoding='utf-8') as f:
        for line in old_lines:
            f.write(line + '\n')
    
    print(f"Output written to: {output_path}")
    return old_lines


if __name__ == '__main__':
    # Run the merge
    result = merge_csv_files('units_old.csv', 'units_default.csv', 'units')
    print(f"\nFinal merged file contains {len(result)} lines")