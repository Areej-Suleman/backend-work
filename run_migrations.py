#!/usr/bin/env python3
"""
Script to check and apply database migrations for Glow Genius
"""
import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd="backend")
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"❌ {description} failed:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error running {description}: {e}")
        return False
    return True

def main():
    print("🚀 Glow Genius Database Migration Tool")
    print("=" * 50)
    
    # Check current migration status
    if not run_command("alembic current", "Checking current migration status"):
        return
    
    # Show migration history
    if not run_command("alembic history --verbose", "Showing migration history"):
        return
    
    # Check if we need to upgrade
    print("\n📋 Available migrations:")
    run_command("alembic heads", "Checking latest migration")
    
    # Apply latest migrations
    user_input = input("\n🤔 Do you want to upgrade to the latest migration? (y/n): ")
    if user_input.lower() in ['y', 'yes']:
        if run_command("alembic upgrade head", "Upgrading to latest migration"):
            print("\n🎉 Database successfully updated!")
            print("\n📊 Final migration status:")
            run_command("alembic current", "Checking final status")
        else:
            print("\n❌ Migration failed. Please check the errors above.")
    else:
        print("\n⏭️  Skipping migration upgrade.")
    
    print("\n✨ Migration check complete!")

if __name__ == "__main__":
    main()
