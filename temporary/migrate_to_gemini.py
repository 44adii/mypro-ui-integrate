#!/usr/bin/env python3
"""
Migration script to convert all agents from Groq to Gemini API.
Run this script to automatically update all agent files.
"""

import os
import sys

def migrate_agent_file(file_path, dry_run=False):
    """Migrate a single agent file from Groq to Gemini."""
    if not os.path.exists(file_path):
        print(f"[WARNING] File not found: {file_path}")
        return False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    
    replacements = {
        'groq/llama-3.3-70b-versatile': 'gemini/gemini-1.5-flash',
        'google/gemini-1.5-flash': 'gemini/gemini-1.5-flash',
        'gemini/gemini-1.5-flash': 'gemini/gemini-1.5-flash',
        'gemini/gemini-2.0-flash': 'gemini/gemini-1.5-flash',
        'gemini/gemini-3-flash-preview': 'gemini/gemini-1.5-flash',
        'gemini/gemini-2.5-flash': 'gemini/gemini-1.5-flash',
        'gemini/gemini-pro': 'gemini/gemini-1.5-flash',
        'gemini/gemini-3-pro-preview': 'gemini/gemini-1.5-flash',
        'groq/llama': 'gemini/gemini-1.5-flash',
    }
    
    for old, new in replacements.items():
        if old in content:
            content = content.replace(old, new)
            print(f"  - Replacing: {old} -> {new}")
    
    # Only write if content changed
    if content != original_content:
        if not dry_run:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"[OK] Updated: {file_path}")
        else:
            print(f"[DRY RUN] Would update: {file_path}")
        return True
    else:
        print(f"[INFO] No changes needed: {file_path}")
        return False

def main():
    """Main migration function."""
    print("Migrating from Groq to Gemini API...")
    print("=" * 60)
    
    # Check for dry run flag
    dry_run = '--dry-run' in sys.argv or '-d' in sys.argv
    
    if dry_run:
        print("DRY RUN MODE - No files will be modified\n")
    
    # List of agent files to migrate
    agent_files = [
        "agents/case_intake_agent.py",
        "agents/ipc_section_agent.py",
        "agents/legal_precedent_agent.py",
        "agents/legal_drafter_agent.py",
        "agents/lawyer_notifier_agent.py",
        "agents/advisory_agent.py",
    ]
    
    updated_count = 0
    
    # Migrate each file
    for file_path in agent_files:
        print(f"\n[PROCESSING] {file_path}")
        if migrate_agent_file(file_path, dry_run=dry_run):
            updated_count += 1
    
    # Summary
    print("\n" + "=" * 60)
    if updated_count > 0:
        if dry_run:
            print(f"[OK] Would update {updated_count} file(s)")
        else:
            print(f"[OK] Successfully updated {updated_count} file(s)")
    else:
        print("[INFO] No files were updated")
    
    if not dry_run:
        print("\n[NEXT STEPS]")
        print("1. Add GOOGLE_API_KEY to your .env file")
        print("2. Run: pip install langchain-google-genai")
        print("3. Test the application: streamlit run app.py")
    else:
        print("\n[TIP] To actually make these changes, run without --dry-run flag")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()

