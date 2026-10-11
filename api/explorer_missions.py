"""Eight fictional, defensive Cyber Explorers scenarios (three stages each)."""
from mission_data import step

EXPLORER_MISSIONS = {
    "privacy-patrol": {
        "title": "Privacy Patrol", "track": "Digital safety", "difficulty": "Beginner",
        "summary": "Protect personal information across a school portal.", "steps": [
            step("Profile check", "A school club asks you to publish your home address on a public profile.",
                 ["Public profile is searchable","Home address is sensitive","Club membership is optional"], "What should you do?", [
                     ("Keep your address private and ask why it is needed", 10, "Correct. This is the safest defensive choice."),
                     ("Publish the address to join faster", 0, "This choice creates avoidable risk; review the evidence and use trusted channels."),
                     ("Post a friend's address instead", 0, "This choice creates avoidable risk; review the evidence and use trusted channels.")
                 ]),
            step("Sharing settings", "A photo album is visible to everyone, including strangers.",
                 ["Album visibility is public","Friends-only access is available","Location tags reveal where photos were taken"], "How should you protect the album?", [
                     ("Keep all location tags enabled", 0, "This choice creates avoidable risk; review the evidence and use trusted channels."),
                     ("Restrict visibility and remove unnecessary location tags", 10, "Correct. This is the safest defensive choice."),
                     ("Share the public link widely", 0, "This choice creates avoidable risk; review the evidence and use trusted channels.")
                 ]),
            step("Data request", "An unfamiliar quiz app asks for your contacts and exact location.",
                 ["Quiz only needs answers","Contacts permission is unrelated","Location permission is optional"], "What is the safest action?", [
                     ("Grant every permission", 0, "This choice creates avoidable risk; review the evidence and use trusted channels."),
                     ("Ask classmates to grant access", 0, "This choice creates avoidable risk; review the evidence and use trusted channels."),
                     ("Decline unnecessary permissions or use another app", 10, "Correct. This is the safest defensive choice.")
                 ]),
        ],
        "finding_key": [1,2,1],
    },
    "scam-spotter": {
        "title": "Scam Spotter", "track": "Digital safety", "difficulty": "Beginner",
        "summary": "Spot payment and prize scams without risking real money.", "steps": [
            step("Prize message", "A stranger says you won a phone but must pay a delivery fee immediately.",
                 ["Prize was not entered","Upfront payment demanded","Sender uses urgent language"], "What is the safest response?", [
                     ("Do not pay; verify through an independent official channel", 10, "Correct. This is the safest defensive choice."),
                     ("Send a small fee to test it", 0, "This choice creates avoidable risk; review the evidence and use trusted channels."),
                     ("Share your card details", 0, "This choice creates avoidable risk; review the evidence and use trusted channels.")
                 ]),
            step("Impersonation call", "A caller claims to be a bank agent and asks for a one-time code.",
                 ["Caller identity is unverified","One-time code protects sign-in","Official bank number is available separately"], "What should you do?", [
                     ("Read the code aloud", 0, "This choice creates avoidable risk; review the evidence and use trusted channels."),
                     ("End the call and contact the bank through its official number", 10, "Correct. This is the safest defensive choice."),
                     ("Send a screenshot of the code", 0, "This choice creates avoidable risk; review the evidence and use trusted channels.")
                 ]),
            step("Marketplace listing", "A seller insists on payment outside the marketplace before showing the item.",
                 ["Seller avoids platform protections","No verified delivery method","Unusually low price"], "Which action reduces risk?", [
                     ("Transfer money immediately", 0, "This choice creates avoidable risk; review the evidence and use trusted channels."),
                     ("Share your account password", 0, "This choice creates avoidable risk; review the evidence and use trusted channels."),
                     ("Use verified marketplace protections or decline the deal", 10, "Correct. This is the safest defensive choice.")
                 ]),
        ],
        "finding_key": [1,1,0],
    },
    "safe-social": {
        "title": "Safe Social", "track": "Digital safety", "difficulty": "Beginner",
        "summary": "Practice safer responses to harmful social-media situations.", "steps": [
            step("Unknown follower", "An unknown account asks where you go to school and when you travel home.",
                 ["Identity is not verified","Routine details can reveal location","Privacy controls are available"], "What is safest?", [
                     ("Do not share your routine and restrict the account", 10, "Correct. This is the safest defensive choice."),
                     ("Share your daily route", 0, "This choice creates avoidable risk; review the evidence and use trusted channels."),
                     ("Post your live location", 0, "This choice creates avoidable risk; review the evidence and use trusted channels.")
                 ]),
            step("Hurtful group chat", "A classmate is targeted by repeated cruel messages.",
                 ["Messages are persistent","Screenshots can preserve evidence","Trusted adults can help"], "What should you do?", [
                     ("Join the teasing", 0, "This choice creates avoidable risk; review the evidence and use trusted channels."),
                     ("Support the classmate, preserve evidence and report", 10, "Correct. This is the safest defensive choice."),
                     ("Publish the victim's personal details", 0, "This choice creates avoidable risk; review the evidence and use trusted channels.")
                 ]),
            step("Account impersonation", "A fake account copies your friend's profile and asks for money.",
                 ["Profile picture is copied","Money request is unusual","You can contact your friend independently"], "What should you do?", [
                     ("Send money to help immediately", 0, "This choice creates avoidable risk; review the evidence and use trusted channels."),
                     ("Share the fake account's request", 0, "This choice creates avoidable risk; review the evidence and use trusted channels."),
                     ("Verify with your friend through another channel and report the account", 10, "Correct. This is the safest defensive choice.")
                 ]),
        ],
        "finding_key": [1,2,1],
    },
    "device-defender": {
        "title": "Device Defender", "track": "Digital safety", "difficulty": "Beginner",
        "summary": "Secure a shared laptop and respond to suspicious downloads.", "steps": [
            step("Update prompt", "Your laptop shows an official security update notification.",
                 ["Operating system reports an update","Updates can fix vulnerabilities","Device restart may be required"], "What should you do?", [
                     ("Install through the official update settings", 10, "Correct. This is the safest defensive choice."),
                     ("Download a random updater from a chat", 0, "This choice creates avoidable risk; review the evidence and use trusted channels."),
                     ("Disable updates permanently", 0, "This choice creates avoidable risk; review the evidence and use trusted channels.")
                 ]),
            step("Shared computer", "You finish using a school computer with your account signed in.",
                 ["Session remains active","Next student will use the computer","Sign-out is available"], "What should you do?", [
                     ("Leave the browser open", 0, "This choice creates avoidable risk; review the evidence and use trusted channels."),
                     ("Sign out and close your session", 10, "Correct. This is the safest defensive choice."),
                     ("Share your password with the next student", 0, "This choice creates avoidable risk; review the evidence and use trusted channels.")
                 ]),
            step("Unexpected attachment", "A download from an unknown sender requests administrator permissions.",
                 ["Sender is unknown","Admin access is requested","School IT support is available"], "What is safest?", [
                     ("Approve immediately", 0, "This choice creates avoidable risk; review the evidence and use trusted channels."),
                     ("Turn off protection", 0, "This choice creates avoidable risk; review the evidence and use trusted channels."),
                     ("Stop and ask trusted IT support to assess it", 10, "Correct. This is the safest defensive choice.")
                 ]),
        ],
        "finding_key": [1,0,1],
    },
    "wifi-wise": {
        "title": "Wi-Fi Wise", "track": "Digital safety", "difficulty": "Beginner",
        "summary": "Choose safer connections and protect online sessions.", "steps": [
            step("Cafe network", "Two similarly named free Wi-Fi networks appear in a cafe.",
                 ["One network name is unverified","Cafe staff can confirm official Wi-Fi","Lookalike hotspots exist"], "What should you do?", [
                     ("Confirm the legitimate network with staff", 10, "Correct. This is the safest defensive choice."),
                     ("Connect to the strongest unknown signal", 0, "This choice creates avoidable risk; review the evidence and use trusted channels."),
                     ("Enter banking credentials to test it", 0, "This choice creates avoidable risk; review the evidence and use trusted channels.")
                 ]),
            step("Public connection", "You need to check a school account on public Wi-Fi.",
                 ["HTTPS helps protect traffic","Shared devices retain sessions","Sensitive transactions need care"], "What is safest?", [
                     ("Ignore website warnings", 0, "This choice creates avoidable risk; review the evidence and use trusted channels."),
                     ("Use the verified HTTPS site and avoid unnecessary sensitive actions", 10, "Correct. This is the safest defensive choice."),
                     ("Disable browser security checks", 0, "This choice creates avoidable risk; review the evidence and use trusted channels.")
                 ]),
            step("Certificate warning", "Your browser warns that a site's certificate cannot be verified.",
                 ["Browser shows a certificate error","Connection identity is uncertain","A trusted alternative connection exists"], "What should you do?", [
                     ("Click through every warning", 0, "This choice creates avoidable risk; review the evidence and use trusted channels."),
                     ("Enter your password anyway", 0, "This choice creates avoidable risk; review the evidence and use trusted channels."),
                     ("Stop and verify the site or connection before proceeding", 10, "Correct. This is the safest defensive choice.")
                 ]),
        ],
        "finding_key": [0,0,1],
    },
    "digital-footprints": {
        "title": "Digital Footprints", "track": "Digital safety", "difficulty": "Beginner",
        "summary": "Learn how online posts persist and shape reputation.", "steps": [
            step("Public post", "You are about to share a classmate's embarrassing photo publicly.",
                 ["Photo identifies a classmate","Consent was not obtained","Public copies may persist"], "What is the right action?", [
                     ("Ask permission and respect a refusal", 10, "Correct. This is the safest defensive choice."),
                     ("Publish it before asking", 0, "This choice creates avoidable risk; review the evidence and use trusted channels."),
                     ("Tag everyone for attention", 0, "This choice creates avoidable risk; review the evidence and use trusted channels.")
                 ]),
            step("Old account", "An old public profile contains your phone number and school schedule.",
                 ["Phone number is visible","Schedule reveals routines","Profile settings can be changed"], "What should you do?", [
                     ("Leave it public", 0, "This choice creates avoidable risk; review the evidence and use trusted channels."),
                     ("Remove unnecessary details and tighten privacy settings", 10, "Correct. This is the safest defensive choice."),
                     ("Add your home address", 0, "This choice creates avoidable risk; review the evidence and use trusted channels.")
                 ]),
            step("Search results", "A friend finds a misleading post about you.",
                 ["Post may be inaccurate","Reporting tools exist","Escalation support is available"], "What is a sensible response?", [
                     ("Threaten the poster", 0, "This choice creates avoidable risk; review the evidence and use trusted channels."),
                     ("Share more private information", 0, "This choice creates avoidable risk; review the evidence and use trusted channels."),
                     ("Save evidence and request correction or report it", 10, "Correct. This is the safest defensive choice.")
                 ]),
        ],
        "finding_key": [1,1,0],
    },
    "mfa-guardian": {
        "title": "MFA Guardian", "track": "Digital safety", "difficulty": "Beginner",
        "summary": "Defend accounts against unexpected verification prompts.", "steps": [
            step("Unexpected approval", "Your phone receives an MFA approval request while you are not signing in.",
                 ["No sign-in was initiated","Approval prompt is unexpected","Account security page is available"], "What should you do?", [
                     ("Deny the request and review account security", 10, "Correct. This is the safest defensive choice."),
                     ("Approve to stop notifications", 0, "This choice creates avoidable risk; review the evidence and use trusted channels."),
                     ("Share the prompt with a stranger", 0, "This choice creates avoidable risk; review the evidence and use trusted channels.")
                 ]),
            step("Recovery codes", "A service provides one-time recovery codes after MFA setup.",
                 ["Codes can restore access","Codes should be kept confidential","Codes can be stored securely"], "How should you handle them?", [
                     ("Post codes in a group chat", 0, "This choice creates avoidable risk; review the evidence and use trusted channels."),
                     ("Store them securely and privately", 10, "Correct. This is the safest defensive choice."),
                     ("Give all codes to a friend", 0, "This choice creates avoidable risk; review the evidence and use trusted channels.")
                 ]),
            step("New phone", "You are replacing a phone used for MFA.",
                 ["Old device may be lost soon","Official recovery steps exist","Account has trusted settings"], "What should you do?", [
                     ("Wait until locked out", 0, "This choice creates avoidable risk; review the evidence and use trusted channels."),
                     ("Disable MFA permanently", 0, "This choice creates avoidable risk; review the evidence and use trusted channels."),
                     ("Transfer or re-enrol MFA through official account settings", 10, "Correct. This is the safest defensive choice.")
                 ]),
        ],
        "finding_key": [1,0,1],
    },
    "backup-buddy": {
        "title": "Backup Buddy", "track": "Digital safety", "difficulty": "Beginner",
        "summary": "Protect schoolwork with reliable backups and recovery checks.", "steps": [
            step("Project deadline", "Your laptop contains the only copy of a school project.",
                 ["Single copy can be lost","External or cloud backup is available","Project is due tomorrow"], "What is the best next step?", [
                     ("Create a separate backup now", 10, "Correct. This is the safest defensive choice."),
                     ("Assume the laptop cannot fail", 0, "This choice creates avoidable risk; review the evidence and use trusted channels."),
                     ("Email your password to yourself", 0, "This choice creates avoidable risk; review the evidence and use trusted channels.")
                 ]),
            step("Backup check", "A cloud service says the project was synced last week.",
                 ["Last sync is old","Recent edits exist","File restore can be tested"], "What should you do?", [
                     ("Trust the old sync", 0, "This choice creates avoidable risk; review the evidence and use trusted channels."),
                     ("Confirm a current backup and test file access", 10, "Correct. This is the safest defensive choice."),
                     ("Delete the local copy first", 0, "This choice creates avoidable risk; review the evidence and use trusted channels.")
                 ]),
            step("Lost laptop", "Your laptop is missing, but you have a verified backup.",
                 ["Laptop may contain account sessions","Backup was tested","Device management is available"], "What should you do?", [
                     ("Publish passwords to find it", 0, "This choice creates avoidable risk; review the evidence and use trusted channels."),
                     ("Ignore account security", 0, "This choice creates avoidable risk; review the evidence and use trusted channels."),
                     ("Report the loss, secure accounts and restore from trusted backup", 10, "Correct. This is the safest defensive choice.")
                 ]),
        ],
        "finding_key": [0,0,1],
    },
}
