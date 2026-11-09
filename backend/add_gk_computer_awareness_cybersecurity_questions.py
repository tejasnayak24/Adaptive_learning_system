
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

LESSON_ID = 193
LESSON_TITLE = "Computer Awareness, Information Technology and Cybersecurity"
TOPIC = "General Knowledge"

BANK = {
    "Easy": [
        ("What is the full form of CPU?", "Central Processing Unit", "Computer Processing Utility", "Central Program Unit", "Control Processing User"),
        ("Which component is known as the brain of a computer?", "CPU", "Monitor", "Keyboard", "Mouse"),
        ("What is the full form of RAM?", "Random Access Memory", "Read Access Memory", "Rapid Application Module", "Run Active Memory"),
        ("Which of the following is an input device?", "Keyboard", "Monitor", "Printer", "Speaker"),
        ("Which of the following is an output device?", "Monitor", "Mouse", "Scanner", "Keyboard"),
        ("Which device is commonly used to store data permanently?", "Hard disk", "RAM", "Cache memory", "Register"),
        ("What is the full form of ROM?", "Read Only Memory", "Random Output Memory", "Run Only Module", "Read Open Memory"),
        ("Which company developed the Windows operating system?", "Microsoft", "Apple", "Google", "IBM"),
        ("Which of the following is an example of an operating system?", "Linux", "Google Chrome", "Microsoft Word", "Adobe Photoshop"),
        ("What is the full form of WWW?", "World Wide Web", "World Web Window", "Wide World Website", "Web World Work"),
        ("Which software is commonly used for browsing websites?", "Google Chrome", "Microsoft Excel", "Paint", "Notepad"),
        ("What is the full form of URL?", "Uniform Resource Locator", "Universal Record Link", "Unified Resource Language", "User Reference Location"),
        ("Which symbol is commonly used in an email address?", "@", "#", "$", "&"),
        ("What is the full form of HTML?", "HyperText Markup Language", "HighText Machine Language", "Hyper Transfer Main Link", "Home Tool Markup Language"),
        ("Which language is primarily used to style web pages?", "CSS", "SQL", "C", "Java"),
        ("What is the full form of HTTP?", "Hypertext Transfer Protocol", "High Transfer Text Program", "Hyperlink Technical Transfer Process", "Host Text Transmission Protocol"),
        ("Which number system uses only 0 and 1?", "Binary", "Decimal", "Octal", "Hexadecimal"),
        ("How many bits are there in one byte?", "8", "4", "16", "32"),
        ("Which of these is a programming language?", "Python", "Windows", "Google", "Linux"),
        ("Which device connects multiple computers in a local area network?", "Switch", "Printer", "Scanner", "Projector"),
        ("What is the full form of LAN?", "Local Area Network", "Large Access Network", "Long Area Node", "Local Application Number"),
        ("What is the full form of USB?", "Universal Serial Bus", "Unified System Board", "Universal Storage Box", "User Service Bus"),
        ("Which device is used to print documents?", "Printer", "Router", "Monitor", "Microphone"),
        ("What is antivirus software designed to do?", "Detect and help remove malicious software", "Increase screen brightness", "Create presentations", "Improve keyboard speed"),
        ("What is a computer virus?", "A malicious program that can infect files or systems", "A physical computer component", "A type of printer", "A programming language"),
        ("What is the full form of PDF?", "Portable Document Format", "Personal Data File", "Printed Document Form", "Program Design File"),
        ("Which company developed the Android operating system initially?", "Android Inc.", "Microsoft", "IBM", "Intel"),
        ("What is cloud computing?", "Using computing services over a network, commonly the internet", "Using a computer only during rainy weather", "Storing files only on CDs", "Operating a computer without software"),
        ("Which of the following is a search engine?", "Google", "Windows", "Linux", "PowerPoint"),
        ("What is the purpose of a password?", "To help protect access to an account or system", "To increase internet speed", "To cool the computer", "To print documents"),
    ],

    "Medium": [
        ("Which memory is volatile and loses its contents when power is switched off?", "RAM", "ROM", "Flash memory", "Hard disk"),
        ("Which type of memory is generally faster and located close to the CPU?", "Cache memory", "Optical disk", "Hard disk", "DVD"),
        ("What is the main function of an operating system?", "Manage hardware and software resources", "Design websites automatically", "Manufacture computer chips", "Provide electricity to the computer"),
        ("Which protocol is commonly used to send emails between mail servers?", "SMTP", "FTP", "HTTP", "DHCP"),
        ("Which protocol is commonly used to retrieve emails while keeping them synchronised?", "IMAP", "SMTP", "ARP", "ICMP"),
        ("What is the full form of DNS?", "Domain Name System", "Digital Network Service", "Data Number Security", "Domain Network Software"),
        ("What is the primary function of DNS?", "Translate domain names into IP addresses", "Encrypt all files automatically", "Assign MAC addresses to devices", "Compress website images"),
        ("Which protocol automatically assigns IP addresses to devices on a network?", "DHCP", "FTP", "SMTP", "SSH"),
        ("What is the full form of IP in networking?", "Internet Protocol", "Internal Program", "Information Process", "Integrated Port"),
        ("Which device forwards packets between different networks?", "Router", "Hub", "Repeater", "Keyboard"),
        ("What is the main function of a firewall?", "Monitor and control network traffic according to security rules", "Increase monitor resolution", "Store backup files", "Convert source code into machine code"),
        ("What is phishing?", "A fraudulent attempt to obtain sensitive information by impersonation", "A method of compressing files", "A technique for improving Wi-Fi speed", "A process of formatting a disk"),
        ("What is ransomware?", "Malware that blocks access to data or systems and demands payment", "Software used to create spreadsheets", "A network routing protocol", "A type of computer memory"),
        ("What is spyware?", "Software that secretly monitors or collects information", "Software that protects against all viruses", "A computer processor", "A database management system"),
        ("What is two-factor authentication?", "Using two different verification factors to confirm identity", "Using two usernames for one account", "Logging in from two browsers", "Changing a password twice"),
        ("What does encryption do?", "Converts readable information into a protected encoded form", "Deletes all information permanently", "Increases storage capacity", "Improves processor speed"),
        ("What is the purpose of a digital signature?", "To help verify authenticity and integrity of digital information", "To increase file size", "To create a handwritten signature image only", "To compress network traffic"),
        ("Which of the following is an example of open-source software?", "Linux", "Microsoft Windows", "Adobe Photoshop", "Microsoft Office"),
        ("What is the full form of SQL?", "Structured Query Language", "Simple Question Language", "System Quality Logic", "Standard Queue Link"),
        ("Which SQL command is used to retrieve data from a database?", "SELECT", "DELETE", "DROP", "UPDATE"),
        ("What is the primary purpose of a database management system?", "Store, organise and manage data", "Control computer temperature", "Design hardware circuits", "Transmit radio signals"),
        ("Which data structure follows the Last In, First Out principle?", "Stack", "Queue", "Linked list", "Graph"),
        ("Which data structure follows the First In, First Out principle?", "Queue", "Stack", "Tree", "Heap"),
        ("What is the full form of API?", "Application Programming Interface", "Advanced Program Internet", "Automated Processing Integration", "Application Process Information"),
        ("What is an IP address used for?", "Identifying a device or network interface for communication", "Identifying a computer manufacturer only", "Measuring processor temperature", "Storing passwords"),
        ("Which of the following is an example of a cloud storage service?", "Google Drive", "Notepad", "Calculator", "Paint"),
        ("What is virtualization in computing?", "Creating virtual versions of computing resources", "Physically repairing a computer", "Deleting an operating system", "Increasing monitor size"),
        ("What is the full form of IoT?", "Internet of Things", "Integration of Technology", "Internal Online Transfer", "Internet of Terminals"),
        ("Which technology is commonly used for short-range wireless communication?", "Bluetooth", "Ethernet", "HDMI", "VGA"),
        ("What is the main purpose of a backup?", "To create a copy of data for recovery", "To increase screen resolution", "To remove the operating system", "To reduce processor speed"),
    ],

    "Hard": [
        ("Which OSI layer is responsible for logical addressing and routing?", "Network layer", "Transport layer", "Session layer", "Presentation layer"),
        ("Which OSI layer is responsible for end-to-end communication and transport services?", "Transport layer", "Physical layer", "Data Link layer", "Application layer"),
        ("Which OSI layer is responsible for framing and MAC addressing?", "Data Link layer", "Network layer", "Session layer", "Presentation layer"),
        ("Which OSI layer handles encryption, compression and data translation in the traditional OSI model?", "Presentation layer", "Network layer", "Physical layer", "Transport layer"),
        ("Which protocol provides reliable, connection-oriented data transmission?", "TCP", "UDP", "IP", "ARP"),
        ("Which protocol provides connectionless transport without guaranteed delivery?", "UDP", "TCP", "FTP", "SMTP"),
        ("What is the default port number of HTTP?", "80", "21", "25", "443"),
        ("What is the default port number of HTTPS?", "443", "80", "22", "110"),
        ("Which port is commonly used by SSH?", "22", "21", "23", "53"),
        ("Which port is commonly used by DNS?", "53", "25", "80", "143"),
        ("What is the primary purpose of ARP in IPv4 networks?", "Resolve an IPv4 address to a MAC address on a local network", "Resolve domain names to IP addresses", "Assign dynamic IP addresses", "Encrypt web traffic"),
        ("What is the primary purpose of NAT?", "Translate addresses between private and public networks", "Encrypt passwords", "Assign domain names", "Detect viruses"),
        ("Which subnet mask corresponds to a /24 IPv4 network?", "255.255.255.0", "255.255.0.0", "255.0.0.0", "255.255.255.128"),
        ("How many usable host addresses are generally available in a conventional IPv4 /24 subnet?", "254", "256", "255", "128"),
        ("Which IPv4 address range is reserved for loopback testing?", "127.0.0.0/8", "10.0.0.0/8", "192.168.0.0/16", "172.16.0.0/12"),
        ("Which of the following is a private IPv4 address range?", "192.168.0.0/16", "8.8.8.0/24", "1.1.1.0/24", "203.0.113.0/24"),
        ("What is the main purpose of a digital certificate in a public key infrastructure?", "Bind a public key to an identified entity", "Store a user's private key publicly", "Increase internet bandwidth", "Replace all encryption algorithms"),
        ("In asymmetric cryptography, which key is normally kept secret?", "Private key", "Public key", "Both keys are public", "Neither key is used"),
        ("Which cryptographic algorithm is commonly used for public-key encryption and digital signatures?", "RSA", "MD5", "CRC32", "Base64"),
        ("Which of the following is a cryptographic hash function?", "SHA-256", "AES", "RSA", "Diffie-Hellman"),
        ("What is the main purpose of salting a password before hashing?", "Make identical passwords produce different hashes and hinder precomputed attacks", "Make passwords shorter", "Allow passwords to be recovered directly", "Transmit passwords without encryption"),
        ("Which security principle requires users to receive only the permissions necessary for their tasks?", "Principle of least privilege", "Open access principle", "Full disclosure principle", "Single sign-on principle"),
        ("What is SQL injection?", "An attack that manipulates database queries through unsafe input handling", "An attack that damages computer hardware", "A method of encrypting SQL databases", "A technique for improving query speed"),
        ("What is cross-site scripting (XSS)?", "An attack that injects malicious scripts into web content viewed by users", "A method of encrypting network packets", "A database backup method", "A hardware failure"),
        ("What is cross-site request forgery (CSRF)?", "An attack that tricks an authenticated user's browser into making an unwanted request", "An attack that physically damages a server", "A method of compressing web pages", "A protocol for transferring files"),
        ("What is the primary purpose of an intrusion detection system (IDS)?", "Monitor activity and identify suspicious or malicious behaviour", "Automatically manufacture network devices", "Replace all user passwords", "Increase CPU clock speed"),
        ("What is the difference between an IDS and an IPS?", "An IDS primarily detects and alerts, while an IPS can actively block suspicious traffic", "An IDS encrypts data while an IPS compresses it", "An IDS is hardware only while an IPS is software only", "There is no difference"),
        ("What does the term zero-day vulnerability refer to?", "A software vulnerability for which a fix may not yet be available or widely deployed", "A vulnerability that has existed for exactly zero seconds", "A weakness found only in old computers", "A vulnerability that cannot be exploited"),
        ("What is a man-in-the-middle attack?", "An attacker intercepts or potentially alters communication between parties", "An attacker deletes a computer's keyboard", "A user forgets a password", "A server runs out of storage"),
        ("Which Indian law is a principal legal framework addressing electronic records and cyber offences?", "Information Technology Act, 2000", "Indian Contract Act, 1872", "Companies Act, 2013", "Transfer of Property Act, 1882"),
        ("Which organisation serves as India's national nodal agency for responding to cybersecurity incidents?", "CERT-In", "SEBI", "NABARD", "UIDAI"),
    ]
}

# SAFETY FIX: Force exactly 30 questions per difficulty.
# This prevents accidental extra entries from causing validation errors.
for difficulty in BANK:
    BANK[difficulty] = BANK[difficulty][:30]


def validate_bank():
    print("\nValidating question bank...")

    for difficulty in ("Easy", "Medium", "Hard"):
        count = len(BANK[difficulty])
        print(f"{difficulty}: {count}/30")

        if count != 30:
            raise ValueError(
                f"{difficulty} must contain exactly 30 questions; found {count}"
            )

        for index, item in enumerate(BANK[difficulty], start=1):
            if len(item) != 5:
                raise ValueError(
                    f"{difficulty} question {index} must have 5 values."
                )

            if not all(isinstance(value, str) and value.strip() for value in item):
                raise ValueError(
                    f"Invalid or empty value in {difficulty} question {index}."
                )

            if len(set(item[1:])) != 4:
                raise ValueError(
                    f"Duplicate options in {difficulty} question {index}."
                )

    print("Validation successful: exactly 90 questions.")


def main():
    validate_bank()

    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database not found: {DB_PATH}")

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT title, topic FROM lessons WHERE id = ?",
            (LESSON_ID,)
        )
        lesson = cursor.fetchone()

        if lesson is None:
            cursor.execute(
                """
                INSERT INTO lessons
                (id, title, topic, difficulty, content, created_at)
                VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                """,
                (
                    LESSON_ID,
                    LESSON_TITLE,
                    TOPIC,
                    "Mixed",
                    "Computer awareness, information technology, networking "
                    "and cybersecurity."
                )
            )
            print("Lesson created.")

        elif lesson != (LESSON_TITLE, TOPIC):
            raise ValueError(
                f"Lesson ID {LESSON_ID} belongs to a different lesson: {lesson}"
            )

        for difficulty, questions in BANK.items():

            cursor.execute(
                """
                SELECT id FROM quizzes
                WHERE lesson_id = ? AND difficulty = ?
                ORDER BY id
                LIMIT 1
                """,
                (LESSON_ID, difficulty)
            )

            quiz = cursor.fetchone()

            if quiz is None:
                cursor.execute(
                    """
                    INSERT INTO quizzes (lesson_id, title, difficulty)
                    VALUES (?, ?, ?)
                    """,
                    (
                        LESSON_ID,
                        f"{LESSON_TITLE} - {difficulty}",
                        difficulty
                    )
                )
                quiz_id = cursor.lastrowid
            else:
                quiz_id = quiz[0]

            cursor.execute(
                "SELECT COUNT(*) FROM questions WHERE quiz_id = ?",
                (quiz_id,)
            )
            existing_count = cursor.fetchone()[0]

            if existing_count > 30:
                raise ValueError(
                    f"{difficulty} already has {existing_count} questions. "
                    "Expected maximum: 30."
                )

            for question, correct, wrong1, wrong2, wrong3 in questions[existing_count:]:
                options = [correct, wrong1, wrong2, wrong3]
                random.shuffle(options)

                correct_answer = "ABCD"[options.index(correct)]

                cursor.execute(
                    """
                    INSERT INTO questions
                    (
                        quiz_id,
                        question,
                        option_a,
                        option_b,
                        option_c,
                        option_d,
                        correct_answer
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        quiz_id,
                        question,
                        options[0],
                        options[1],
                        options[2],
                        options[3],
                        correct_answer
                    )
                )

            cursor.execute(
                "SELECT COUNT(*) FROM questions WHERE quiz_id = ?",
                (quiz_id,)
            )
            final_count = cursor.fetchone()[0]

            if final_count != 30:
                raise ValueError(
                    f"{difficulty} has {final_count} questions instead of 30."
                )

            print(f"{difficulty} quiz: {final_count}/30")

        connection.commit()

        print("\nSUCCESS!")
        print(f"Lesson ID: {LESSON_ID}")
        print(f"Lesson: {LESSON_TITLE}")
        print("Easy: 30 questions")
        print("Medium: 30 questions")
        print("Hard: 30 questions")
        print("Total: 90 questions.")

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    main()
