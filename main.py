"""Orchestration entrypoint for IntelTrace CLI usage."""
import os
import argparse
import json
from datetime import datetime
from dotenv import load_dotenv
from banner import print_banner
from database import IntelDB
from ip_intel import IPIntel
from email_intel import EmailIntel
from phone_intel import PhoneIntel
from username_intel import UsernameIntel
from photo_intel import PhotoIntel
from ddos_intel import DDOSIntel
from reputation_engine import ReputationEngine
from timeline_builder import TimelineBuilder
from report_generator import ReportGenerator

load_dotenv()


def print_results(report):
    """Print investigation results to console in a formatted way."""
    print("\n" + "="*80)
    print("\033[92m" + "INVESTIGATION RESULTS".center(80) + "\033[0m")
    print("="*80)
    
    print(f"\n\033[93m[+] Case ID:\033[0m {report['case_id']}")
    print(f"\033[93m[+] Investigator:\033[0m {report['investigator']}")
    print(f"\033[93m[+] Target Type:\033[0m {report['target_type'].upper()}")
    print(f"\033[93m[+] Target:\033[0m {report['target']}")
    
    # Reputation Score
    print(f"\n\033[92m[REPUTATION SCORE]\033[0m")
    score = report['reputation']['score']
    score_color = "\033[91m" if score > 50 else "\033[93m" if score > 20 else "\033[92m"
    print(f"  Score: {score_color}{score}\033[0m")
    print(f"  Factors: {', '.join(report['reputation']['factors'])}")
    
    # Results
    print(f"\n\033[92m[INVESTIGATION RESULTS] ({len(report['results'])} items found)\033[0m")
    for idx, result in enumerate(report['results'], 1):
        print(f"\n  [{idx}] " + "-"*70)
        
        if isinstance(result, dict):
            if 'platform' in result:
                # Social media result
                status = "\033[92m✓ FOUND\033[0m" if result.get('exists') else "\033[91m✗ NOT FOUND\033[0m"
                print(f"      Platform: {result['platform'].upper()}")
                print(f"      Status: {status}")
                if result.get('exists'):
                    print(f"      URL: {result.get('url', 'N/A')}")
                    print(f"      Status Code: {result.get('status_code', 'N/A')}")
            
            elif 'type' in result:
                # Photo intel or other structured results
                print(f"      Type: {result['type'].upper()}")
                for key, value in result.items():
                    if key != 'type':
                        if isinstance(value, dict):
                            print(f"      {key.replace('_', ' ').title()}:")
                            for k, v in value.items():
                                print(f"        - {k}: {v}")
                        elif isinstance(value, list):
                            print(f"      {key.replace('_', ' ').title()}: {len(value)} items")
                        else:
                            print(f"      {key.replace('_', ' ').title()}: {value}")
            else:
                # Generic result
                for key, value in result.items():
                    print(f"      {key}: {value}")
    
    # Timeline
    print(f"\n\033[92m[TIMELINE] ({len(report['timeline'])} events)\033[0m")
    for event in report['timeline']:
        print(f"  ⏱  {event['time']} - {event['desc']}")
    
    # Save location
    print(f"\n\033[92m[+] Full report saved to:\033[0m reports/{report['case_id']}.json")
    print("="*80 + "\n")


def run_investigation(target_type, target_value, investigator_name=None):
    db = IntelDB()
    collector = {
        'ip': IPIntel(),
        'email': EmailIntel(),
        'phone': PhoneIntel(),
        'username': UsernameIntel(),
        'photo': PhotoIntel(),
        'ddos': DDOSIntel()
    }[target_type]

    print(f"[main] Starting collection for {target_type}: {target_value}")
    results = collector.collect(target_value)
    print("[main] Running reputation engine and timeline builder")
    rep = ReputationEngine().score(results)
    timeline = TimelineBuilder().build(results)

    report = {
        'case_id': f"IT-{os.urandom(4).hex()}",
        'investigator': investigator_name or os.getenv('INVESTIGATOR_NAME', 'Analyst'),
        'target_type': target_type,
        'target': target_value,
        'results': results,
        'reputation': rep,
        'timeline': timeline
    }

    db.save_case(report)
    ReportGenerator().generate(report)
    print(f"[main] Investigation saved and report generated for {target_value}")
    
    # Display results on console
    print_results(report)


def cli():
    print_banner()
    
    # Display menu
    print("\n\033[92m[+] Select Investigation Type:\033[0m")
    print("\033[92m    1. IP Address Intelligence\033[0m")
    print("\033[92m    2. Email Intelligence\033[0m")
    print("\033[92m    3. Phone Intelligence\033[0m")
    print("\033[92m    4. Username Intelligence\033[0m")
    print("\033[92m    5. Photo Intelligence\033[0m")
    print("\033[92m    6. DDOS Analysis (simulated)\033[0m")
    print("\033[92m    0. Exit\033[0m")
    print()
    
    try:
        choice = input("\033[93m[>] Enter your choice (0-6): \033[0m").strip()
        
        if choice == '0':
            print("\033[92m[+] Exiting IntelTrace. Stay safe!\033[0m")
            return
        
        type_map = {
            '1': 'ip',
            '2': 'email',
            '3': 'phone',
            '4': 'username',
            '5': 'photo',
            '6': 'ddos'
        }
        
        if choice not in type_map:
            print("\033[91m[!] Invalid choice. Please select 0-6.\033[0m")
            return
        
        target_type = type_map[choice]
        target_value = input(f"\033[93m[>] Enter target {target_type}: \033[0m").strip()
        
        if not target_value:
            print("\033[91m[!] Target value cannot be empty.\033[0m")
            return
        
        investigator_name = input("\033[93m[>] Enter investigator name (optional): \033[0m").strip()
        
        print(f"\n\033[92m[+] Starting {target_type} investigation for: {target_value}\033[0m\n")
        run_investigation(target_type, target_value, investigator_name or None)
        
    except KeyboardInterrupt:
        print("\n\033[93m[!] Investigation cancelled by user.\033[0m")
    except Exception as e:
        print(f"\033[91m[!] Error: {e}\033[0m")


if __name__ == '__main__':
    cli()
