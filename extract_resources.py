#!/usr/bin/env python3
"""
Script to extract all complete resources from the original resources_fixed.json
and create a comprehensive resources_clean.json file.
"""

import json
import re
from pathlib import Path

def is_complete_resource(resource):
    """Check if a resource object has all required fields."""
    required_fields = [
        'Title/Name',
        'Type', 
        'Category',
        'Link',
        'Short Description',
        'Access type'
    ]
    
    # Check if all required fields exist and are not empty
    for field in required_fields:
        if field not in resource or not resource[field] or resource[field].strip() == '':
            return False
    
    # Check if it has meaningful content (not just "Access type": "Free")
    if len(resource) <= 2:  # Only has Access type and maybe one other field
        return False
        
    return True

def clean_text(text):
    """Clean up escaped quotes and other formatting issues in text."""
    if not isinstance(text, str):
        return text
    
    # Fix escaped quotes
    text = text.replace('\\"', '"').replace("\\'", "'")
    # Fix any double escaping
    text = text.replace('\\\\', '\\')
    
    return text

def clean_resource(resource):
    """Clean up a single resource object."""
    cleaned = {}
    
    for key, value in resource.items():
        # Clean the key
        clean_key = clean_text(key) if isinstance(key, str) else key
        
        # Clean the value
        if isinstance(value, str):
            clean_value = clean_text(value)
        else:
            clean_value = value
            
        cleaned[clean_key] = clean_value
    
    return cleaned

def extract_complete_resources():
    """Extract all complete resources from the original file."""
    
    original_file = Path('resources_fixed.json')
    output_file = Path('resources_complete.json')
    
    if not original_file.exists():
        print(f"❌ Error: {original_file} not found!")
        return
    
    try:
        print("🔍 Reading original resources file...")
        
        # Read the file content
        with open(original_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Try to parse as JSON
        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing error: {e}")
            print("🔧 Trying to fix JSON format...")
            
            # Try to fix common JSON issues
            content = content.strip()
            if not content.startswith('['):
                content = '[' + content
            if not content.endswith(']'):
                content = content + ']'
            
            # Try parsing again
            try:
                data = json.loads(content)
            except json.JSONDecodeError as e2:
                print(f"❌ Still can't parse JSON: {e2}")
                return
        
        if not isinstance(data, list):
            print("❌ Data is not a list!")
            return
        
        print(f"📊 Found {len(data)} total entries in original file")
        
        # Filter complete resources
        complete_resources = []
        incomplete_count = 0
        
        for i, resource in enumerate(data):
            if not isinstance(resource, dict):
                incomplete_count += 1
                continue
                
            if is_complete_resource(resource):
                # Clean the resource
                cleaned_resource = clean_resource(resource)
                complete_resources.append(cleaned_resource)
            else:
                incomplete_count += 1
        
        print(f"✅ Found {len(complete_resources)} complete resources")
        print(f"⚠️  Skipped {incomplete_count} incomplete entries")
        
        # Save the complete resources
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(complete_resources, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Saved complete resources to {output_file}")
        
        # Show some statistics
        categories = set()
        types = set()
        access_types = set()
        
        for resource in complete_resources:
            if 'Category' in resource:
                categories.add(resource['Category'])
            if 'Type' in resource:
                types.add(resource['Type'])
            if 'Access type' in resource:
                access_types.add(resource['Access type'])
        
        print(f"\n📈 Resource Statistics:")
        print(f"   📚 Total Resources: {len(complete_resources)}")
        print(f"   🏷️  Categories: {len(categories)}")
        print(f"   📝 Types: {len(types)}")
        print(f"   🔓 Access Types: {len(access_types)}")
        
        print(f"\n🎯 Categories found:")
        for category in sorted(categories):
            count = sum(1 for r in complete_resources if r.get('Category') == category)
            print(f"   • {category}: {count} resources")
            
        return complete_resources
        
    except Exception as e:
        print(f"❌ Error processing file: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("=" * 60)
    print("  EduResource Hub - Resource Extraction Tool")  
    print("=" * 60)
    print()
    
    resources = extract_complete_resources()
    
    if resources:
        print("\n🎉 Extraction completed successfully!")
        print(f"📁 Check 'resources_complete.json' for the cleaned data")
        print("\n💡 Next steps:")
        print("   1. Rename 'resources_complete.json' to 'resources_clean.json'")
        print("   2. Or update script.js to use 'resources_complete.json'")
        print("   3. Start your server and enjoy all your resources!")
    else:
        print("\n❌ Extraction failed. Please check the errors above.")
