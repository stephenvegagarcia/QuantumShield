#!/usr/bin/env python3
"""
QuantumShield - Cybersecurity Training Module
Interactive training with 5 realistic attack scenarios
"""

import random
import time
from datetime import datetime
from typing import Dict, List
from database import get_db, SecurityEvent

class CybersecurityTraining:
    """Interactive cybersecurity training with real attack scenarios"""
    
    def __init__(self):
        self.scenarios = self._load_scenarios()
        self.score = 0
        self.completed_scenarios = []
        
    def _load_scenarios(self) -> List[Dict]:
        """Load all 5 training scenarios"""
        return [
            {
                "id": 1,
                "title": "🦠 Malware Detection Challenge",
                "description": "A suspicious executable appeared on your system. You must identify if it's malware.",
                "difficulty": "Medium",
                "scenario": """
You receive an email with an attachment named "invoice_final_URGENT.exe"
The file claims to be an invoice but has these characteristics:
- File size: 2.3 MB
- Extension: .exe (executable)
- Source: Unknown sender <noreply@inv0ice-system.com>
- File hash: 89a3f21d4c5e6b7890abcdef1234567890abcdef1234567890abcdef12345678
                """,
                "options": {
                    "A": "Open the file immediately to check the invoice",
                    "B": "Scan with antivirus and check file hash against threat databases",
                    "C": "Delete the email without investigation",
                    "D": "Forward to colleagues to see if they recognize it"
                },
                "correct_answer": "B",
                "explanation": """
CORRECT! You should:
1. **Never execute** suspicious .exe files directly
2. **Scan with antivirus** first
3. **Check file hash** against VirusTotal or threat databases
4. **Verify sender** - 'inv0ice' with zero instead of 'o' is suspicious
5. **Report** to security team

Invoices should be PDF, not executables. The misspelled domain is a huge red flag!
                """,
                "points": 20
            },
            {
                "id": 2,
                "title": "🎣 Phishing Attack Recognition",
                "description": "Identify the phishing attempt from real communications",
                "difficulty": "Easy",
                "scenario": """
You receive this email:

From: security@paypa1-verification.com
Subject: URGENT: Your Account Will Be Suspended

Dear Valued Customer,

We have detected unusual activity on your account. To prevent suspension,
please verify your identity immediately by clicking the link below:

http://paypa1-verify.tk/login

You have 24 hours to respond or your account will be permanently locked.

Best regards,
PayPal Security Team
                """,
                "options": {
                    "A": "Click the link immediately to save your account",
                    "B": "Reply with your password to verify identity",
                    "C": "Recognize phishing: Check sender, URL, urgency tactics",
                    "D": "Forward to friends to warn them"
                },
                "correct_answer": "C",
                "explanation": """
CORRECT! This is a classic phishing attack. Red flags:
1. **Fake domain**: 'paypa1' uses number '1' instead of letter 'l'
2. **Suspicious TLD**: '.tk' is common for phishing
3. **Urgency tactics**: "24 hours" creates panic
4. **Generic greeting**: "Valued Customer" instead of your name
5. **Requests action**: Never click links in suspicious emails

Always go directly to the official website (paypal.com) if concerned!
                """,
                "points": 15
            },
            {
                "id": 3,
                "title": "🔐 Ransomware Response Protocol",
                "description": "Your files are being encrypted! Take the right action.",
                "difficulty": "Hard",
                "scenario": """
ALERT! Your system shows:
- Files changing to .encrypted extension
- Wallpaper changed to ransom note
- Message: "Pay 0.5 BTC in 48 hours or lose all files"
- Network activity spiking
- Multiple processes creating/modifying files rapidly

Current status:
- 45% of files encrypted
- Process 'svchost32.exe' using 90% CPU
- Outbound connections to unknown IPs

What do you do FIRST?
                """,
                "options": {
                    "A": "Pay the ransom immediately to save files",
                    "B": "Disconnect from network, kill malicious process, restore from backup",
                    "C": "Restart computer to stop the encryption",
                    "D": "Delete all encrypted files to save space"
                },
                "correct_answer": "B",
                "explanation": """
CORRECT! Ransomware response priority:
1. **IMMEDIATELY disconnect** from network (prevent spread & command-and-control)
2. **Kill malicious process** (stop encryption)
3. **Isolate infected system** (protect other devices)
4. **Document everything** (for forensics)
5. **Restore from backup** (if available)
6. **Report to security team/authorities**

NEVER pay ransom - no guarantee you'll get files back & funds criminals!
Use offline backups and proper incident response procedures.
                """,
                "points": 30
            },
            {
                "id": 4,
                "title": "🌐 SQL Injection Attack Prevention",
                "description": "Secure your web application against SQL injection",
                "difficulty": "Hard",
                "scenario": """
You're reviewing code for a login system:

```python
username = request.form['username']
password = request.form['password']

query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
cursor.execute(query)
user = cursor.fetchone()
```

A security researcher shows you can bypass login with:
Username: admin' OR '1'='1' --
Password: (anything)

How do you fix this?
                """,
                "options": {
                    "A": "Add more password validation rules",
                    "B": "Use prepared statements/parameterized queries",
                    "C": "Encrypt the username before the query",
                    "D": "Block the word 'OR' in all inputs"
                },
                "correct_answer": "B",
                "explanation": """
CORRECT! SQL Injection prevention:
1. **Use prepared statements**: Separates data from commands
2. **Parameterized queries**: Database handles escaping
3. **Input validation**: Whitelist allowed characters
4. **Principle of least privilege**: Limit database permissions
5. **Use ORMs**: Modern frameworks handle this automatically

Correct code:
```python
query = "SELECT * FROM users WHERE username=? AND password=?"
cursor.execute(query, (username, password))
```

NEVER build SQL queries with string concatenation of user input!
                """,
                "points": 30
            },
            {
                "id": 5,
                "title": "🔑 Password Security & MFA",
                "description": "Implement secure authentication practices",
                "difficulty": "Medium",
                "scenario": """
Your company needs a new password policy. You're choosing between:

Option A:
- Minimum 8 characters
- Must change every 30 days
- No special character requirements

Option B:
- Minimum 12 characters
- Mix of uppercase, lowercase, numbers, symbols
- MFA (Multi-Factor Authentication) required
- Password manager encouraged
- No forced expiration unless compromised

Option C:
- Minimum 6 characters
- Simple words allowed
- Change every 90 days

Which is most secure?
                """,
                "options": {
                    "A": "Option A - Simple and users won't forget",
                    "B": "Option B - Long passwords + MFA + password manager",
                    "C": "Option C - Balance between security and usability",
                    "D": "No password policy needed, just biometrics"
                },
                "correct_answer": "B",
                "explanation": """
CORRECT! Modern password security best practices:
1. **Length > Complexity**: 12+ characters better than complex 8
2. **MFA is crucial**: Second factor stops 99.9% of account takeovers
3. **No forced rotation**: Leads to weak passwords (Password1, Password2...)
4. **Password managers**: Enable unique, strong passwords everywhere
5. **Biometrics as 2nd factor**: Not standalone (can't change if compromised)

NIST guidelines (2024):
✅ Long passphrases (e.g., "CorrectHorseBatteryStaple!")
✅ Multi-factor authentication
✅ Check against breach databases
❌ Frequent forced password changes
❌ Complex requirements that reduce entropy
                """,
                "points": 25
            }
        ]
    
    def start_training(self):
        """Start the interactive training session"""
        print("\n" + "="*70)
        print("   🎓 QUANTUMSHIELD CYBERSECURITY TRAINING")
        print("="*70)
        print("\nWelcome to hands-on cybersecurity training!")
        print("You'll face 5 realistic security scenarios.")
        print("Make the right decisions to protect your systems.\n")
        
        for scenario in self.scenarios:
            self._run_scenario(scenario)
            time.sleep(1)
        
        self._show_results()
    
    def _run_scenario(self, scenario: Dict):
        """Run a single training scenario"""
        print("\n" + "─"*70)
        print(f"📚 Scenario {scenario['id']}/5: {scenario['title']}")
        print(f"Difficulty: {scenario['difficulty']}")
        print("─"*70)
        
        print(f"\n{scenario['description']}\n")
        print(scenario['scenario'])
        
        print("\n🎯 What do you do?")
        for option_key, option_text in scenario['options'].items():
            print(f"  {option_key}. {option_text}")
        
        # Get user answer
        answer = ""
        while answer.upper() not in scenario['options'].keys():
            answer = input("\nYour answer (A/B/C/D): ").strip().upper()
            if answer not in scenario['options'].keys():
                print("❌ Invalid choice. Please enter A, B, C, or D.")
        
        # Check answer
        if answer == scenario['correct_answer']:
            print("\n✅ CORRECT!")
            self.score += scenario['points']
            self.completed_scenarios.append({
                'id': scenario['id'],
                'correct': True,
                'points': scenario['points']
            })
        else:
            print(f"\n❌ INCORRECT. The correct answer was {scenario['correct_answer']}.")
            self.completed_scenarios.append({
                'id': scenario['id'],
                'correct': False,
                'points': 0
            })
        
        print(scenario['explanation'])
        
        # Log to database
        try:
            db = get_db()
            event = SecurityEvent(
                event_type="Training Completed",
                reason=f"Scenario {scenario['id']}: {scenario['title']} - {'Correct' if answer == scenario['correct_answer'] else 'Incorrect'}",
                entropy=0.5,
                correlation=0.8
            )
            db.add(event)
            db.commit()
            db.close()
        except:
            pass
        
        input("\nPress Enter to continue...")
    
    def _show_results(self):
        """Show final training results"""
        total_possible = sum(s['points'] for s in self.scenarios)
        percentage = (self.score / total_possible) * 100
        
        print("\n" + "="*70)
        print("   📊 TRAINING RESULTS")
        print("="*70)
        
        print(f"\nFinal Score: {self.score}/{total_possible} ({percentage:.1f}%)")
        print(f"Scenarios Completed: {len(self.completed_scenarios)}/5")
        print(f"Correct Answers: {sum(1 for s in self.completed_scenarios if s['correct'])}/5")
        
        # Performance rating
        if percentage >= 90:
            rating = "🏆 EXCELLENT - Cybersecurity Expert!"
            message = "Outstanding! You have strong security awareness."
        elif percentage >= 70:
            rating = "⭐ GOOD - Security Conscious"
            message = "Well done! You understand key security principles."
        elif percentage >= 50:
            rating = "📚 AVERAGE - Keep Learning"
            message = "You're on the right track. Review the explanations."
        else:
            rating = "⚠️ NEEDS IMPROVEMENT"
            message = "Please review security fundamentals and retake training."
        
        print(f"\nPerformance Rating: {rating}")
        print(f"{message}")
        
        # Breakdown
        print("\n📋 Scenario Breakdown:")
        for i, scenario in enumerate(self.scenarios, 1):
            completed = next((s for s in self.completed_scenarios if s['id'] == i), None)
            if completed:
                status = "✅" if completed['correct'] else "❌"
                points = f"{completed['points']}/{scenario['points']}"
                print(f"  {status} {scenario['title']}: {points} points")
        
        print("\n" + "="*70)
        print("Training session completed!")
        print("Review the explanations above to strengthen your security knowledge.")
        print("="*70 + "\n")


def run_interactive_training():
    """Run the full interactive training program"""
    trainer = CybersecurityTraining()
    trainer.start_training()


if __name__ == "__main__":
    run_interactive_training()
