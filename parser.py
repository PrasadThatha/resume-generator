import re
from datetime import datetime
# =========================================================
# MAIN PARSER
# =========================================================

def parse_resume(raw_text):

    lines = preprocess_lines(raw_text.splitlines())

    sections = detect_sections(lines)

    resume = {

        "name": extract_name(lines),

        "role": extract_role(lines),

        "mobile": extract_mobile(raw_text),

        "email": extract_email(raw_text),

        "sidebar_sections": [

            {
                "title": "Education",
                "items": extract_education(
                    sections.get("education", [])
                )
            },

            {
                "title": "Technical Expertise",
                "items": extract_skills(
                    sections.get("skills", [])
                )
            },

            {
                "title": "Certifications",
                "items": extract_certifications(
                    sections.get("certifications", [])
                )
            }

        ],

        "summary": extract_summary(
            sections.get("summary", [])
        ),

        "experience": extract_experience(
            sections.get("experience", [])
        )

    }

    validate_resume(resume)

    return resume


# =========================================================
# PREPROCESSING
# =========================================================

def preprocess_lines(lines):

    cleaned = []

    unwanted_patterns = [

        "logos of",
        "curriculum vitae",
        "resume",
        "page ",
        "u s t",
        "ust global"

    ]

    for line in lines:

        line = normalize_text(line)

        if not line:
            continue

        lower = line.lower()

        if any(pattern in lower for pattern in unwanted_patterns):
            continue

        if len(line) <= 1:
            continue

        cleaned.append(line)

    return cleaned


def normalize_text(text):

    text = re.sub(r'\s+', ' ', text)

    text = text.replace("•", "")

    text = text.replace("|", " | ")

    text = text.strip()

    return text


# =========================================================
# SECTION DETECTION
# =========================================================

def detect_sections(lines):

    headers = {

        "summary": [
            "summary",
            "professional summary",
            "profile summary",
            "career summary"
        ],

        "skills": [
            "skills",
            "technical skills",
            "technical expertise",
            "core skills"
        ],

        "experience": [
            "experience",
            "professional experience",
            "work experience"
        ],

        "education": [
            "education",
            "academic details",
            "academic qualification"
        ],

        "certifications": [
            "certifications",
            "certification",
            "licenses"
        ]

    }

    sections = {}

    current_section = "other"

    sections[current_section] = []

    for line in lines:

        lower = line.lower().strip()

        found = False

        for section, keywords in headers.items():

            if lower in keywords:

                current_section = section

                sections[current_section] = []

                found = True

                break

        if not found:

            sections.setdefault(current_section, [])

            sections[current_section].append(line)

    return sections


# =========================================================
# BASIC DETAILS
# =========================================================

def extract_name(lines):

    blacklist = [

        "resume",
        "cv",
        "email",
        "phone",
        "mobile",
        "@"

    ]

    for line in lines[:10]:

        clean = line.strip()

        if len(clean.split()) in [2, 3]:

            if not any(word in clean.lower() for word in blacklist):

                if clean.replace(" ", "").replace(".", "").isalpha():

                    return clean

    return "Candidate"


def extract_role(lines):

    if not lines:

        return "Professional"

    role_keywords = [

        # ============================================
        # SOFTWARE / DEVELOPMENT
        # ============================================

        "developer",
        "software developer",
        "software engineer",
        "backend developer",
        "frontend developer",
        "full stack developer",
        "python developer",
        "java developer",
        "dot net developer",
        ".net developer",
        "web developer",
        "application developer",

        # ============================================
        # ENGINEERING
        # ============================================

        "engineer",
        "system engineer",
        "platform engineer",
        "site reliability engineer",
        "sre engineer",
        "cloud engineer",
        "devops engineer",
        "data engineer",
        "network engineer",
        "support engineer",
        "security engineer",
        "qa engineer",
        "test engineer",

        # ============================================
        # SAP
        # ============================================

        "sap consultant",
        "sap developer",
        "sap analyst",
        "sap architect",
        "abap developer",
        "abap consultant",
        "functional consultant",
        "technical consultant",

        # ============================================
        # ARCHITECTURE
        # ============================================

        "architect",
        "solution architect",
        "technical architect",
        "enterprise architect",
        "cloud architect",

        # ============================================
        # ANALYSIS
        # ============================================

        "analyst",
        "business analyst",
        "system analyst",
        "data analyst",
        "security analyst",
        "functional analyst",

        # ============================================
        # ADMINISTRATION
        # ============================================

        "administrator",
        "system administrator",
        "database administrator",
        "cloud administrator",

        # ============================================
        # MANAGEMENT
        # ============================================

        "manager",
        "project manager",
        "program manager",
        "delivery manager",
        "product manager",
        "team lead",
        "technical lead",
        "lead developer",
        "lead engineer",

        # ============================================
        # SPECIALIST
        # ============================================

        "specialist",
        "technical specialist",
        "application specialist",
        "product specialist",

        # ============================================
        # DATA / AI
        # ============================================

        "data scientist",
        "machine learning engineer",
        "ai engineer",
        "ml engineer",
        "ai specialist",

        # ============================================
        # TESTING / QA
        # ============================================

        "tester",
        "qa tester",
        "automation tester",
        "manual tester",
        "quality analyst",

        # ============================================
        # INFRASTRUCTURE
        # ============================================

        "devops",
        "cloud consultant",
        "infra engineer",
        "infrastructure engineer",

        # ============================================
        # SUPPORT
        # ============================================

        "support analyst",
        "application support",
        "technical support",

        # ============================================
        # UI / UX
        # ============================================

        "designer",
        "ui designer",
        "ux designer",
        "ui ux designer",

        # ============================================
        # CYBER SECURITY
        # ============================================

        "cyber security analyst",
        "security consultant",
        "information security analyst"

    ]

    # =================================================
    # CHECK FIRST 20 LINES
    # =================================================

    for line in lines[:20]:

        clean = cleanup_bullet(
            line
        ).strip()

        if not clean:

            continue

        lower = clean.lower()

        # =============================================
        # IGNORE LONG SENTENCES
        # =============================================

        if len(clean.split()) > 10:

            continue

        # =============================================
        # MATCH ROLE
        # =============================================

        if any(

            keyword in lower

            for keyword in role_keywords

        ):

            return clean.title()

    # =================================================
    # FALLBACK
    # =================================================

    return "Professional"


def extract_email(text):

    match = re.search(
        r'[\w\.-]+@[\w\.-]+\.\w+',
        text
    )

    return match.group(0) if match else "Not Available"


def extract_mobile(text):

    match = re.search(
        r'(\+?\d[\d\s\-]{8,15}\d)',
        text
    )

    return match.group(0) if match else "Not Available"


# =========================================================
# EDUCATION
# =========================================================

def extract_education(lines):

    education = []

    for line in lines:

        clean = cleanup_bullet(line)

        if len(clean.split()) >= 3:

            education.append(clean)

    education = remove_duplicates(education)

    if not education:

        education.append("Education Not Found")

    return education


# =========================================================
# SKILLS
# =========================================================

def extract_skills(lines):

    structured_skills = []

    fallback_skills = []

    for line in lines:

        clean = cleanup_bullet(line)

        if not clean:
            continue

        # =====================================================
        # CATEGORY : VALUES FORMAT
        # Example:
        # Salesforce: Apex, LWC, Trigger
        # =====================================================

        if ":" in clean:

            category, values = clean.split(
                ":",
                1
            )

            category = normalize_text(
                category
            )

            values = normalize_text(
                values
            )

            # Split skill values properly
            raw_skills = re.split(

                r',|•|\|',

                values

            )

            skills = []

            for skill in raw_skills:

                skill = normalize_text(skill)

                if not skill:
                    continue

                if len(skill) <= 1:
                    continue

                skills.append(skill)

            skills = remove_duplicates(
                skills
            )

            if skills:

                structured_skills.append({

                    "category": category,

                    "skills": skills

                })

        # =====================================================
        # NORMAL SKILL LINES
        # Example:
        # Python, SQL, Git
        # =====================================================

        else:

            parts = re.split(

                r',|•|\|',

                clean

            )

            for part in parts:

                skill = normalize_text(
                    part
                )

                if not skill:
                    continue

                if len(skill) <= 1:
                    continue

                fallback_skills.append(
                    skill
                )

    # =========================================================
    # REMOVE DUPLICATES
    # =========================================================

    fallback_skills = remove_duplicates(
        fallback_skills
    )

    # =========================================================
    # ADD FALLBACK SKILLS
    # =========================================================

    if fallback_skills:

        structured_skills.append({

            "category": "",

            "skills": fallback_skills

        })

    # =========================================================
    # DEFAULT FALLBACK
    # =========================================================

    if not structured_skills:

        structured_skills.append({

            "category": "Skills",

            "skills": [

                "Skills Not Found"

            ]

        })

    return structured_skills


# =========================================================
# CERTIFICATIONS
# =========================================================

def extract_certifications(lines):

    certifications = []

    for line in lines:

        clean = cleanup_bullet(line)

        if len(clean.split()) >= 2:

            certifications.append(clean)

    certifications = remove_duplicates(certifications)

    if not certifications:

        certifications.append("Certification Not Found")

    return certifications


# =========================================================
# SUMMARY
# =========================================================

def extract_summary(lines):

    if not lines:

        return [

            "Summary Not Found"

        ]

    cleaned_lines = []

    ignore_patterns = [

        "@",
        "linkedin",
        "github",
        "mobile",
        "phone",
        "email"

    ]

    for line in lines:

        clean = normalize_text(line)

        lower = clean.lower()

        # ==========================================
        # IGNORE JUNK
        # ==========================================

        if any(

            pattern in lower

            for pattern in ignore_patterns

        ):

            continue

        # Ignore very small lines
        if len(clean.split()) < 4:

            continue

        cleaned_lines.append(
            clean
        )

    # ==============================================
    # REMOVE DUPLICATES
    # ==============================================

    cleaned_lines = remove_duplicates(
        cleaned_lines
    )

    if not cleaned_lines:

        return [

            "Summary Not Found"

        ]

    # ==============================================
    # JOIN SUMMARY
    # ==============================================

    summary = " ".join(
        cleaned_lines
    )

    # ==============================================
    # LIMIT WORDS
    # ==============================================

    MAX_WORDS = 140

    words = summary.split()

    if len(words) > MAX_WORDS:

        summary = " ".join(

            words[:MAX_WORDS]

        ) + "..."

    # ==============================================
    # SPLIT INTO SMALLER SENTENCES
    # ==============================================

    sentences = summary.split(".")

    formatted_summary = []

    for sentence in sentences:

        sentence = sentence.strip()

        if sentence:

            formatted_summary.append(
                sentence + "."
            )

    return formatted_summary[:6]


# =========================================================
# EXPERIENCE
# =========================================================

# =========================================================
# EXPERIENCE
# =========================================================
def calculate_tenure(text):

    pattern = r'([A-Za-z]{3,9}\s\d{4})\s*[-–to]+\s*([A-Za-z]{3,9}\s\d{4}|Present|Till Date|Current)'

    match = re.search(
        pattern,
        text,
        re.IGNORECASE
    )

    if not match:

        return ""

    start_raw = match.group(1)

    end_raw = match.group(2)

    try:

        start_date = datetime.strptime(
            start_raw,
            "%b %Y"
        )

    except:

        try:

            start_date = datetime.strptime(
                start_raw,
                "%B %Y"
            )

        except:

            return ""

    if end_raw.lower() in [

        "present",
        "till date",
        "current"

    ]:

        end_date = datetime.now()

    else:

        try:

            end_date = datetime.strptime(
                end_raw,
                "%b %Y"
            )

        except:

            try:

                end_date = datetime.strptime(
                    end_raw,
                    "%B %Y"
                )

            except:

                return ""

    months = (

        (end_date.year - start_date.year) * 12

        + (end_date.month - start_date.month)

    )

    years = months // 12

    remaining_months = months % 12

    tenure = []

    if years > 0:

        tenure.append(
            f"{years} Years"
        )

    if remaining_months > 0:

        tenure.append(
            f"{remaining_months} Months"
        )

    return " ".join(tenure)
def extract_role(lines):

    if not lines:

        return ""

    role_keywords = [

        "developer",
        "engineer",
        "lead",
        "architect",
        "consultant",
        "manager",
        "analyst",
        "tester",
        "administrator"

    ]

    # =================================================
    # CHECK FIRST 20 LINES
    # =================================================

    for line in lines[:20]:

        clean = cleanup_bullet(
            line
        ).strip()

        if not clean:

            continue

        lower = clean.lower()

        # Ignore long paragraphs
        if len(clean.split()) > 10:

            continue

        # Match role keywords
        if any(

            keyword in lower

            for keyword in role_keywords

        ):

            return clean.title()

    return ""
def extract_experience(lines):

    if not lines:

        return [

            {
                "projects": [

                    {
                        "role": "",

                        "company": "",

                        "duration": "",

                        "tenure": "",

                        "points": [

                            "Experience Not Found"

                        ]
                    }

                ]
            }

        ]

    experience_entries = []

    current_entry = {

        "role": "",

        "company": "",

        "duration": "",

        "tenure": "",

        "points": []

    }

    role_keywords = [

        "developer",
        "engineer",
        "consultant",
        "lead",
        "architect",
        "analyst",
        "manager",
        "tester",
        "support",
        "administrator"

    ]

    # =====================================================
    # TENURE CALCULATOR
    # =====================================================

    def calculate_tenure(text):

        pattern = (

            r'([A-Za-z]{3,9}\s\d{4})'

            r'\s*[-–to]+\s*'

            r'([A-Za-z]{3,9}\s\d{4}|Present|Till Date|Current)'
        )

        match = re.search(

            pattern,

            text,

            re.IGNORECASE

        )

        if not match:

            return ""

        start_raw = match.group(1)

        end_raw = match.group(2)

        date_formats = [

            "%b %Y",
            "%B %Y"

        ]

        start_date = None

        for fmt in date_formats:

            try:

                start_date = datetime.strptime(

                    start_raw,

                    fmt

                )

                break

            except:

                pass

        if not start_date:

            return ""

        # =============================================
        # END DATE
        # =============================================

        if end_raw.lower() in [

            "present",
            "current",
            "till date"

        ]:

            end_date = datetime.now()

        else:

            end_date = None

            for fmt in date_formats:

                try:

                    end_date = datetime.strptime(

                        end_raw,

                        fmt

                    )

                    break

                except:

                    pass

            if not end_date:

                return ""

        # =============================================
        # CALCULATE MONTHS
        # =============================================

        months = (

            (end_date.year - start_date.year) * 12

            + (end_date.month - start_date.month)

        )

        years = months // 12

        remaining_months = months % 12

        tenure_parts = []

        if years > 0:

            if years == 1:

                tenure_parts.append(
                    "1 Year"
                )

            else:

                tenure_parts.append(
                    f"{years} Years"
                )

        if remaining_months > 0:

            if remaining_months == 1:

                tenure_parts.append(
                    "1 Month"
                )

            else:

                tenure_parts.append(
                    f"{remaining_months} Months"
                )

        return " ".join(
            tenure_parts
        )

    # =====================================================
    # MAIN LOOP
    # =====================================================

    for line in lines:

        clean = cleanup_bullet(line)

        lower = clean.lower()

        if not clean:

            continue

        # =================================================
        # ROLE DETECTION
        # =================================================

        is_role = (

            len(clean.split()) <= 8

            and any(

                keyword in lower

                for keyword in role_keywords

            )

        )

        if is_role:

            # SAVE PREVIOUS ENTRY
            if (

                current_entry["role"]

                or current_entry["company"]

                or current_entry["points"]

            ):

                experience_entries.append(
                    current_entry
                )

            # START NEW ENTRY
            current_entry = {

                "role": clean,

                "company": "",

                "duration": "",

                "tenure": "",

                "points": []

            }

            continue

        # =================================================
        # COMPANY + DURATION
        # =================================================

        if "|" in clean:

            current_entry["company"] = clean

            current_entry["tenure"] = calculate_tenure(
                clean
            )

            continue

        # =================================================
        # RESPONSIBILITIES
        # =================================================

        current_entry["points"].append(
            clean
        )

    # =====================================================
    # FINAL ENTRY
    # =====================================================

    if (

        current_entry["role"]

        or current_entry["company"]

        or current_entry["points"]

    ):

        experience_entries.append(
            current_entry
        )

    # =====================================================
    # REMOVE DUPLICATES
    # =====================================================

    for entry in experience_entries:

        entry["points"] = remove_duplicates(

            entry["points"]

        )

    return [

        {

            "projects": experience_entries

        }

    ]

# =========================================================
# HELPERS
# =========================================================

def cleanup_bullet(text):

    text = text.strip()

    text = re.sub(
        r'^[\-\*\•\d\.\)]+',
        '',
        text
    )

    return normalize_text(text)


def remove_duplicates(items):

    seen = set()

    result = []

    for item in items:

        clean = item.lower().strip()

        if clean not in seen:

            seen.add(clean)

            result.append(item)

    return result


# =========================================================
# VALIDATION
# =========================================================

def validate_resume(data):

    required_fields = [

        "name",
        "email",
        "mobile"

    ]

    for field in required_fields:

        if not data.get(field):

            print(f"Missing field: {field}")