#!/usr/bin/env python3
"""
Robust script to extract all complete resources from the original resources_fixed.json.
This version handles JSON formatting issues more gracefully.
"""

import json
import re
from pathlib import Path

def fix_json_escaping(content):
    """Fix common JSON escaping issues."""
    # Fix invalid escape sequences
    content = re.sub(r'\\(?!["\\/bfnrt]|u[0-9a-fA-F]{4})', r'\\\\', content)
    
    # Fix common problematic patterns
    content = content.replace("\\'", "'")  # Single quotes don't need escaping in JSON
    content = content.replace('\\n', '\\n')  # Keep actual newlines escaped
    content = content.replace('\\t', '\\t')  # Keep actual tabs escaped
    
    return content

def extract_resources_manually():
    """Extract resources by parsing the file line by line."""
    
    original_file = Path('resources_fixed.json')
    
    if not original_file.exists():
        print(f"❌ Error: {original_file} not found!")
        return []
    
    print("🔍 Reading and parsing file manually...")
    
    resources = []
    current_resource = {}
    in_object = False
    brace_count = 0
    current_key = None
    current_value = ""
    in_value = False
    
    required_fields = {'Title/Name', 'Type', 'Category', 'Link', 'Short Description', 'Access type'}
    
    try:
        with open(original_file, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            
            if not line or line == ',':
                continue
                
            if line == '[':  # Start of array
                continue
            elif line == ']':  # End of array
                break
            elif line == '{':  # Start of object
                current_resource = {}
                in_object = True
                brace_count = 1
            elif line == '},':  # End of object
                if in_object and current_resource:
                    # Check if resource is complete
                    if all(field in current_resource for field in required_fields):
                        # Clean up the resource
                        cleaned = {}
                        for k, v in current_resource.items():
                            if isinstance(v, str):
                                # Fix escaped quotes
                                v = v.replace('\\"', '"').replace("\\'", "'")
                                v = v.replace('\\\\', '\\')
                            cleaned[k] = v
                        
                        if cleaned.get('Title/Name', '').strip():  # Must have a title
                            resources.append(cleaned)
                
                current_resource = {}
                in_object = False
                brace_count = 0
            elif ':' in line and in_object:
                # Parse key-value pair
                try:
                    # Split on first colon
                    parts = line.split(':', 1)
                    if len(parts) == 2:
                        key = parts[0].strip().strip('"')
                        value = parts[1].strip().rstrip(',').strip('"')
                        
                        if key and value:
                            current_resource[key] = value
                except Exception as e:
                    print(f"⚠️  Line {line_num}: Could not parse line: {line[:50]}...")
                    continue
        
        return resources
        
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return []

def main():
    """Main extraction function."""
    print("=" * 60)
    print("  EduResource Hub - Robust Resource Extractor")  
    print("=" * 60)
    print()
    
    # Extract resources
    resources = extract_resources_manually()
    
    if not resources:
        print("❌ No resources extracted!")
        return
    
    print(f"✅ Successfully extracted {len(resources)} complete resources!")
    
    # Save to file
    output_file = Path('resources_complete.json')
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(resources, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Saved to {output_file}")
        
        # Show statistics
        categories = {}
        types = {}
        access_types = {}
        
        for resource in resources:
            cat = resource.get('Category', 'Unknown')
            typ = resource.get('Type', 'Unknown')  
            acc = resource.get('Access type', 'Unknown')
            
            categories[cat] = categories.get(cat, 0) + 1
            types[typ] = types.get(typ, 0) + 1
            access_types[acc] = access_types.get(acc, 0) + 1
        
        print(f"\n📈 Resource Statistics:")
        print(f"   📚 Total Resources: {len(resources)}")
        print(f"   🏷️  Unique Categories: {len(categories)}")
        print(f"   📝 Unique Types: {len(types)}")
        print(f"   🔓 Access Types: {len(access_types)}")
        
        print(f"\n🎯 Top Categories:")
        for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"   • {cat}: {count} resources")
        
        print(f"\n🔧 Resource Types:")
        for typ, count in sorted(types.items(), key=lambda x: x[1], reverse=True):
            print(f"   • {typ}: {count} resources")
        
        print(f"\n🔓 Access Types:")
        for acc, count in sorted(access_types.items(), key=lambda x: x[1], reverse=True):
            print(f"   • {acc}: {count} resources")
            
        print("\n🎉 Extraction completed successfully!")
        print("\n💡 Next steps:")
        print("   1. Update script.js to use 'resources_complete.json'")
        print("   2. Or rename this file to 'resources_clean.json'")
        print("   3. Refresh your website to see all resources!")
        
    except Exception as e:
        print(f"❌ Error saving file: {e}")

if __name__ == "__main__":
    main()
