import re
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import (
    Table,
    TableStyle
)
from reportlab.lib.pagesizes import A4

from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)
pdfmetrics.registerFont(

    TTFont(

        'Aptos',

        'fonts/Aptos.ttf'

    )

)

pdfmetrics.registerFont(

    TTFont(

        'Aptos-Bold',

        'fonts/Aptos-Bold.ttf'

    )

)
from reportlab.lib import colors


# =========================================================
# PAGE CONFIG
# =========================================================

PAGE_WIDTH, PAGE_HEIGHT = A4

HEADER_HEIGHT = 82

styles = getSampleStyleSheet()


# =========================================================
# STYLES
# =========================================================

section_heading = ParagraphStyle(

    'section_heading',

    fontName='Aptos-Bold',

    fontSize=12,

    leading=15,

    textColor=colors.HexColor("#007C80"),

     leftIndent=10,

    spaceBefore=0,

    spaceAfter=4

)
summary_style = ParagraphStyle(

    'summary_style',

    fontName='Aptos',

    fontSize=10,

    leading=15,

    textColor=colors.black,

    leftIndent=8,

    firstLineIndent=0,

    spaceAfter=6

)

company_style = ParagraphStyle(

    'company_style',

    fontName='Aptos-Bold',

    fontSize=10,

    leading=13,

    textColor=colors.black,

    leftIndent=14,

    firstLineIndent=0,

    spaceBefore=0,

    spaceAfter=4

)

bullet_style = ParagraphStyle(

    'bullet_style',

    fontName='Aptos',

    fontSize=10,

    leading=15,

    textColor=colors.black,

    leftIndent=34,

    firstLineIndent=-10,

    spaceAfter=0

)


# =========================================================
# CREATE PDF
# =========================================================

def create_resume_pdf(
    resume,
    output_path
):

    doc = BaseDocTemplate(

        output_path,

        pagesize=A4,

        leftMargin=0,

        rightMargin=0,

        topMargin=0,

        bottomMargin=0

    )

    # =====================================================
    # STORE RESUME DATA
    # =====================================================

    doc.resume_data = resume

    # =====================================================
    # FIRST PAGE FRAME
    # =====================================================

    first_page_frame = Frame(

        185,

        60,

        PAGE_WIDTH - 200,

        PAGE_HEIGHT - HEADER_HEIGHT - 75,

        showBoundary=0,

        leftPadding=0,

        rightPadding=0,

        topPadding=0,

        bottomPadding=0

    )

    # =====================================================
    # LATER PAGE FRAME
    # =====================================================

    later_page_frame = Frame(

        185,

        60,

        PAGE_WIDTH - 200,

        PAGE_HEIGHT - 75,

        showBoundary=0,

        leftPadding=0,

        rightPadding=0,

        topPadding=0,

        bottomPadding=0

    )

    # =====================================================
    # PAGE TEMPLATES
    # =====================================================

    first_template = PageTemplate(

        id='First',

        frames=[first_page_frame],

        onPage=lambda canvas, doc:

        draw_first_page(

            canvas,

            doc,

            resume

        )

    )

    later_template = PageTemplate(

        id='Later',

        frames=[later_page_frame],

        onPage=draw_later_pages

    )

    doc.addPageTemplates([

        first_template,

        later_template

    ])

    # =====================================================
    # STORY
    # =====================================================

    from reportlab.platypus import NextPageTemplate

    story = [

        NextPageTemplate(
            'Later'
        )

    ]

    story.extend(

        build_main_content(
            resume
        )

    )

    # =====================================================
    # BUILD PDF
    # =====================================================

    doc.build(story)
# =========================================================
# FIRST PAGE
# =========================================================

def draw_first_page(
    canvas,
    doc,
    resume
):

    canvas.saveState()

    # Background
    canvas.setFillColor(
        colors.HexColor("#ECECEC")
    )

    canvas.rect(

        0,
        0,
        PAGE_WIDTH,
        PAGE_HEIGHT,
        fill=1,
        stroke=0

    )

    # Header
    canvas.setFillColor(
        colors.HexColor("#1C181B")
    )

    canvas.rect(

        0,
        PAGE_HEIGHT - HEADER_HEIGHT,
        PAGE_WIDTH,
        HEADER_HEIGHT,
        fill=1,
        stroke=0

    )

    # Sidebar Background
    canvas.setFillColor(
        colors.HexColor("#006D73")
    )

    canvas.rect(

        0,

        0,

        180,

        PAGE_HEIGHT - HEADER_HEIGHT ,

        fill=1,

        stroke=0

    )

    # =====================================================
    # UST LOGO
    # =====================================================

    canvas.setFillColor(
        colors.white
    )

    canvas.setFont(
        "Aptos-Bold",
        22
    )

    canvas.drawString(

        40,

        PAGE_HEIGHT - 46,

        "UST" 

    )

    # =====================================================
    # NAME
    # =====================================================

    canvas.setFillColor(
        colors.white
    )

    canvas.setFont(
        "Aptos-Bold",
        22
    )

    canvas.drawString(

        145,

        PAGE_HEIGHT - 46,

        resume.get(
            "name",
            ""
        ).title()

    )

    # =====================================================
    # ROLE
    # =====================================================

    canvas.setFillColor(
        colors.HexColor("#D9D9D9")
    )

    canvas.setFont(
        "Aptos-Bold",
        9
    )

    canvas.drawString(

        145,

        PAGE_HEIGHT - 64,

        resume.get(
            "role",
            ""
        )

    )

    # =====================================================
    # CONTACT
    # =====================================================
    canvas.setFillColor(
        colors.HexColor("#CFCFCF")
    )
    canvas.setFont(
        "Aptos",
        9
    )

    canvas.drawString(

        145,

        PAGE_HEIGHT - 78,

        f"Mob: {resume.get('mobile', '')} | "
        f"Email: {resume.get('email', '')}"

    )

    # =====================================================
    # SIDEBAR
    # =====================================================

    draw_sidebar(
        canvas,
        resume
    )

    canvas.restoreState()


# =========================================================
# LATER PAGES
# =========================================================

# =========================================================
# SIDEBAR DRAWING
# =========================================================

def draw_sidebar(
    canvas,
    resume
):

    x = 16

    y = PAGE_HEIGHT - 112

    section_gap = 14

    line_gap = 10

    for section in resume.get(
        "sidebar_sections",
        []
    ):

        # =================================================
        # SECTION TITLE
        # =================================================

        canvas.setFillColor(
            colors.white
        )

        canvas.setStrokeColor(
            colors.white
        )

        canvas.setFont(
            "Aptos-Bold",
            11
        )

        title = section.get(
            "title",
            ""
        ).upper()

        canvas.drawString(

            x,

            y,

            title

        )

        # UNDERLINE
        canvas.setLineWidth(0.7)

        canvas.line(

            x,

            y - 6,

            x + 135,

            y - 6

        )

        y -= 22

        # =================================================
        # SECTION ITEMS
        # =================================================

        canvas.setFillColor(
            colors.white
        )

        canvas.setFont(
            "Aptos",
            9
        )

        section_title = title.lower()

        for item in section.get(
            "items",
            []
        ):

            # =============================================
            # STRUCTURED SKILLS
            # =============================================

            if isinstance(item, dict):

                category = item.get(
                    "category",
                    ""
                )

                skills = item.get(
                    "skills",
                    []
                )

                skills_text = ", ".join(
                    skills
                )

                if category:

                    text = (

                        f"{category}: "

                        f"{skills_text}"

                    )

                else:

                    text = skills_text

            # =============================================
            # NORMAL ITEMS
            # =============================================

            else:

                text = item

            wrapped_lines = split_text(
                text,
                32
            )

            # =============================================
            # BULLET ENABLED SECTIONS
            # =============================================

            is_bullet_section = (

                "technical" in section_title

                or "certification" in section_title
                or "ai tools" in section_title

            )

            for index, line in enumerate(
                wrapped_lines
            ):

                # =========================================
                # BULLET POINTS
                # =========================================

                if is_bullet_section:

                    # Draw bullet ONLY once
                    if index == 0:

                        canvas.setStrokeColor(
                            colors.black
                        )
                        canvas.setFillColor(
                            colors.black
                        )

                        canvas.circle(

                            x + 4,

                            y + 2,

                            2,

                            fill=1

                        )

                    # Draw text
                    canvas.setFillColor(
                        colors.white
                    )

                    canvas.drawString(

                        x + 12,

                        y,

                        line

                    )

                # =========================================
                # NORMAL TEXT
                # =========================================

                else:

                    canvas.setFillColor(
                        colors.white
                    )

                    canvas.drawString(

                        x,

                        y,

                        line

                    )

                y -= line_gap

            y -= 4

        y -= section_gap
# =========================================================
# LATER PAGES
# =========================================================
# =========================================================
# LATER PAGES
# =========================================================

# =========================================================
# LATER PAGES
# =========================================================

def draw_later_pages(
    canvas,
    doc
):

    canvas.saveState()

    # =====================================================
    # PAGE BACKGROUND
    # =====================================================

    canvas.setFillColor(
        colors.HexColor("#ECECEC")
    )

    canvas.rect(

        0,

        0,
        

        PAGE_WIDTH,

        PAGE_HEIGHT,

        fill=1,

        stroke=0

    )

    # =====================================================
    # SIDEBAR BACKGROUND ONLY
    # =====================================================

    canvas.setFillColor(
        colors.HexColor("#006D73")
    )

    canvas.rect(

        0,

        0,

        180,

        PAGE_HEIGHT,

        fill=1,

        stroke=0

    )

    canvas.restoreState()

# =========================================================
# TEXT WRAPPING
# =========================================================

def split_text(
    text,
    max_chars
):

    words = text.split()

    lines = []

    current_line = ""

    for word in words:

        test_line = (
            current_line
            + " "
            + word
        ).strip()

        if len(test_line) <= max_chars:

            current_line = test_line

        else:

            lines.append(
                current_line
            )

            current_line = word

    if current_line:

        lines.append(
            current_line
        )

    return lines


# =========================================================
# MAIN CONTENT
# =========================================================

def build_main_content(resume):

    content = []

    # =====================================================
    # =====================================================
    # SUMMARY
    # =====================================================

    content.append(

        Spacer(1, 2.5)

    )



    content.append(

        Paragraph(

            "PROFILE SUMMARY",

            section_heading

        )

    )

    # =====================================================
    # GREEN UNDERLINE
    # =====================================================

    line = Table(

        [[""]],

        colWidths=[380],

        rowHeights=[1.2]

    )

    line.setStyle(

        TableStyle([

            (

                'BACKGROUND',

                (0, 0),

                (-1, -1),

                colors.HexColor("#007C80")

            ),

            (

                'BOTTOMPADDING',

                (0, 0),

                (-1, -1),

                0

            ),

            (

                'TOPPADDING',

                (0, 0),

                (-1, -1),

                0

            )

        ])

    )

    content.append(line)

    content.append(
        Spacer(1, 8)
    )

    # =====================================================
    # SUMMARY CONTENT
    # =====================================================

    summary_text = " ".join(

        resume.get(
            "summary",
            []
        )

    )

    content.append(

        Paragraph(

            summary_text,

            summary_style

        )

    )

    content.append(
        Spacer(1, 18)
    )
        # =====================================================
    # EXPERIENCE
    # =====================================================

    content.append(

        Paragraph(

            "PROFESSIONAL EXPERIENCE",

            section_heading

        )
        

    )
    line = Table(

        [[""]],

        colWidths=[385],

        rowHeights=[1.2]

    )

    line.setStyle(

        TableStyle([

            (

                'BACKGROUND',

                (0, 0),

                (-1, -1),

                colors.HexColor("#007C80")

            )

        ])

    )

    content.append(line)

    content.append(
        Spacer(1, 6)
    )

    # project_counter = 1

    for exp in resume.get(
        "experience",
        []
    ):

        for project in exp.get(
            "projects",
            []
        ):

            # =============================================
            # PROJECT TITLE
            # =============================================

            # content.append(

            #     Paragraph(

            #         f"<b>PROJECT {project_counter}</b>",

            #         company_style

            #     )

            # )

            # project_counter += 1

            # =============================================
            # COMPANY
            # =============================================

            company = project.get(
                "company",
                ""
            )

            if company.strip():

                content.append(

                    Paragraph(

                        company,

                        company_style

                    )

                )
            tenure = project.get(
                "tenure",
                ""
            )

            details = []

            if tenure:

                content.append(

                    Paragraph(

                        f'<font color="#007C80"><b>Tenure:</b></font> {tenure}',

                        ParagraphStyle(

                            'tenure_style',

                            parent=bullet_style,

                            fontName='Aptos-Bold',

                            fontSize=9.5,

                            leading=12,

                            leftIndent=25,

                            spaceBefore=0,

                            spaceAfter=0

                        )

                    )

                )

            # =============================================
            # METADATA
            # =============================================

            technology = project.get(
                "technology",
                ""
            )

            tools = project.get(
                "tools",
                ""
            )

            duration = project.get(
                "duration",
                ""
            )

            team_size = project.get(
                "team_size",
                ""
            )

            description = project.get(
                "description",
                ""
            )

            # if duration:

            #     content.append(

            #         Paragraph(

            #             f"<b>Duration:</b> {duration}",

            #             bullet_style

            #         )

            #     )

            if technology:

                content.append(

                    Paragraph(

                        f"<b>Technology:</b> {technology}",

                        bullet_style

                    )

                )

            if tools:

                content.append(

                    Paragraph(

                        f"<b>Tools Used:</b> {tools}",

                        bullet_style

                    )

                )

            if team_size:

                content.append(

                    Paragraph(

                        f"<b>Team Size:</b> {team_size}",

                        bullet_style

                    )

                )

            if description:

                content.append(

                    Paragraph(

                        f"<b>Description:</b> {description}",

                        bullet_style

                    )

                )

            content.append(
                Spacer(1, 2)
            )
            role = project.get(
                "role",
                ""
            )

            if role:

                content.append(

                    Paragraph(

                        f'<font color="#007C80"><b>Role:</b></font> '
                        f'<b>{role}</b>',

                        ParagraphStyle(

                            'role_style',

                            parent=bullet_style,

                            fontName='Aptos-Bold',

                            fontSize=9.5,

                            leading=12,

                            leftIndent=25,

                            spaceBefore=0,

                            spaceAfter=1

                        )

                    )

                )
            if details:

                content.append(

                    Paragraph(

                        " | ".join(details),

                        bullet_style

                    )

                )
            # =============================================
            # RESPONSIBILITIES
            # =============================================
            # =============================================
            # RESPONSIBILITIES HEADING
            # =============================================

            if project.get("points"):

                content.append(

                    Paragraph(

                        "<b>Responsibilities:</b>",

                        ParagraphStyle(

                            'responsibility_heading',

                            parent=bullet_style,

                            fontName='Aptos-Bold',

                            fontSize=10,

                            leading=14,

                            leftIndent=25,

                            spaceBefore=4,

                            spaceAfter=0

                        )

                    )

                )

            for point in project.get(
                "points",
                []
            ):

                clean_point = point.strip()

                if not clean_point:
                    continue

                content.append(

                   Paragraph(

                        f'<font size="13" color="black">•</font>&nbsp;&nbsp;{clean_point}',

                        bullet_style

                    )

                )

            content.append(
                Spacer(1, 8)
            )

    return content