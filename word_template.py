from docx import Document
from docx.shared import Inches
from docx.shared import Pt
from docx.shared import RGBColor
from docx.enum.table import WD_ROW_HEIGHT_RULE
from docx.enum.text import WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

from docx.oxml import OxmlElement
from docx.oxml.ns import qn


# =====================================================
# CELL BACKGROUND COLOR
# =====================================================

def set_cell_background(cell, color):

    tc = cell._tc

    tcPr = tc.get_or_add_tcPr()

    shd = OxmlElement('w:shd')

    shd.set(qn('w:fill'), color)

    tcPr.append(shd)


# =====================================================
# REMOVE TABLE BORDERS
# =====================================================

def remove_table_borders(table):

    tbl = table._tbl

    tblPr = tbl.tblPr

    borders = OxmlElement('w:tblBorders')

    for border_name in [
        'top',
        'left',
        'bottom',
        'right',
        'insideH',
        'insideV'
    ]:

        border = OxmlElement(f'w:{border_name}')

        border.set(qn('w:val'), 'nil')

        borders.append(border)

    tblPr.append(borders)

# =====================================================
# CELL PADDING
# =====================================================

def set_cell_padding(cell, top, left, bottom, right):

    tc = cell._tc

    tcPr = tc.get_or_add_tcPr()

    tcMar = tcPr.first_child_found_in(
        "w:tcMar"
    )

    if tcMar is None:

        tcMar = OxmlElement('w:tcMar')

        tcPr.append(tcMar)

    for margin_name, margin_value in [
        ("top", top),
        ("left", left),
        ("bottom", bottom),
        ("right", right)
    ]:

        node = OxmlElement(f'w:{margin_name}')

        node.set(
            qn('w:w'),
            str(margin_value)
        )

        node.set(
            qn('w:type'),
            'dxa'
        )

        tcMar.append(node)
# =====================================================
# FONT STYLE
# =====================================================

def apply_font(run, font_name, size, bold=False, color=None):

    run.font.name = font_name

    run._element.rPr.rFonts.set(
        qn('w:eastAsia'),
        font_name
    )

    run.font.size = Pt(size)

    run.bold = bold

    if color:

        run.font.color.rgb = RGBColor.from_string(color)
# # =====================================================
# # SIDEBAR TITLE
# # =====================================================

# def add_sidebar_title(cell, text):

#     para = cell.add_paragraph()

#     para.paragraph_format.space_before = Pt(0)

#     para.paragraph_format.space_after = Pt(0)

#     run = para.add_run(text.upper())

#     apply_font(
#         run,
#         "Aptos",
#         10,
#         bold=True,
#         color="FFFFFF"
#     )

#     underline = cell.add_paragraph()

#     underline.paragraph_format.space_before = Pt(0)

#     underline.paragraph_format.space_after = Pt(0)

#     pPr = underline._element.get_or_add_pPr()

#     pBdr = OxmlElement('w:pBdr')

#     bottom = OxmlElement('w:bottom')

#     bottom.set(qn('w:val'), 'single')

#     bottom.set(qn('w:sz'), '12')

#     bottom.set(qn('w:space'), '1')

#     bottom.set(qn('w:color'), 'FFFFFF')

#     pBdr.append(bottom)

#     pPr.append(pBdr)
# =====================================================
# SIDEBAR TEXT
# =====================================================

def add_sidebar_title(cell, text):

    para = cell.add_paragraph()

    para.paragraph_format.line_spacing = 1

    para.paragraph_format.space_before = Pt(0)

    para.paragraph_format.space_after = Pt(0)


    run = para.add_run(text.upper())

    apply_font(
        run,
        "Aptos",
        10,
        bold=True,
        color="FFFFFF"
    )

    underline = cell.add_paragraph()

    underline.paragraph_format.space_before = Pt(0)

    underline.paragraph_format.space_after = Pt(0)

    underline.paragraph_format.line_spacing = 1

    pPr = underline._element.get_or_add_pPr()

    pBdr = OxmlElement('w:pBdr')

    bottom = OxmlElement('w:bottom')

    bottom.set(qn('w:val'), 'single')

    bottom.set(qn('w:sz'), '12')

    bottom.set(qn('w:space'), '0')

    bottom.set(qn('w:color'), 'FFFFFF')

    pBdr.append(bottom)

    pPr.append(pBdr)
# =====================================================
# MAIN SECTION TITLE
# =====================================================

def add_main_heading(cell, text):

    para = cell.add_paragraph()

    para.paragraph_format.space_before = Pt(0)
    para.paragraph_format.space_after = Pt(2)

    run = para.add_run(text.upper())

    apply_font(
        run,
        "Aptos",
        10,
        bold=True,
        color="007C80"
    )

    para.paragraph_format.space_after = Pt(0)

    line_para = cell.add_paragraph()

    line_para.paragraph_format.space_before = Pt(0)

    line_para.paragraph_format.space_after = Pt(6)

    pPr = line_para._element.get_or_add_pPr()

    pBdr = OxmlElement('w:pBdr')

    bottom = OxmlElement('w:bottom')

    bottom.set(qn('w:val'), 'single')

    bottom.set(qn('w:sz'), '8')   # thickness

    bottom.set(qn('w:space'), '0')

    bottom.set(qn('w:color'), '007C80')

    pBdr.append(bottom)

    pPr.append(pBdr)
# =====================================================
# EXPERIENCE BLOCK
# =====================================================

def add_experience_entry(cell, project):

    # ================================================
    # COMPANY
    # ================================================

    company = project.get(
        "company",
        ""
    )

    if company:

        para = cell.add_paragraph()

        para.paragraph_format.keep_with_next = True

        para.paragraph_format.space_before = Pt(0)

        para.paragraph_format.space_after = Pt(0)

        para.paragraph_format.line_spacing = 1

        run = para.add_run(company)

        apply_font(
            run,
            "Aptos",
            10,
            bold=True,
            color="000000"
        )

    # ================================================
    # TENURE
    # ================================================

    tenure = project.get(
        "tenure",
        ""
    )

    if tenure:

        para = cell.add_paragraph()

        para.paragraph_format.keep_with_next = True

        para.paragraph_format.space_before = Pt(0)

        para.paragraph_format.space_after = Pt(0)

        para.paragraph_format.line_spacing = 1

        label = para.add_run("Tenure: ")

        apply_font(
            label,
            "Aptos",
            9,
            bold=True,
            color="007C80"
        )

        value = para.add_run(tenure)

        apply_font(
            value,
            "Aptos",
            9,
            color="000000"
        )

    # ================================================
    # ROLE
    # ================================================

    role = project.get(
        "role",
        ""
    )

    if role:

        para = cell.add_paragraph()

        para.paragraph_format.keep_with_next = True

        para.paragraph_format.space_before = Pt(0)

        para.paragraph_format.space_after = Pt(0)

        para.paragraph_format.line_spacing = 1

        label = para.add_run("Role: ")

        apply_font(
            label,
            "Aptos",
            9,
            bold=True,
            color="007C80"
        )

        value = para.add_run(role)

        apply_font(
            value,
            "Aptos",
            9,
            bold=True,
            color="000000"
        )

    # ================================================
    # RESPONSIBILITIES
    # ================================================

    points = project.get(
        "points",
        []
    )

    if points:

        para = cell.add_paragraph()

        para.paragraph_format.keep_with_next = True

        para.paragraph_format.space_before = Pt(1)

        para.paragraph_format.space_after = Pt(1)

        para.paragraph_format.line_spacing = 1

        run = para.add_run(
            "Responsibilities:"
        )

        apply_font(
            run,
            "Aptos",
            10,
            bold=True,
            color="000000"
        )

    for point in points:

        bullet_para = cell.add_paragraph()

        bullet_para.paragraph_format.keep_together = True

        bullet_para.paragraph_format.space_after = Pt(0)

        bullet_para.paragraph_format.line_spacing = 1

        bullet_para.style = 'List Bullet'

        run = bullet_para.add_run(point)

        apply_font(
            run,
            "Aptos",
            9,
            color="000000"
        )
    space_para = cell.add_paragraph()

    space_para.paragraph_format.space_before = Pt(0)

    space_para.paragraph_format.space_after = Pt(2)
def add_sidebar_text(
    cell,
    text,
    bullet=False,
    last_item=False
):

    para = cell.add_paragraph()

    para.paragraph_format.space_before = Pt(0)

    if last_item:

        para.paragraph_format.space_after = Pt(10)

    else:

        para.paragraph_format.space_after = Pt(4)

    if bullet:

        para.paragraph_format.left_indent = Pt(12)

        para.paragraph_format.first_line_indent = Pt(-5)

        bullet_run = para.add_run("• ")

        apply_font(
            bullet_run,
            "Aptos",
            10,
            color="000000"
        )

    run = para.add_run(text)

    apply_font(
        run,
        "Aptos",
        9,
        color="FFFFFF"
    )

# =====================================================
# CREATE DOCX
# =====================================================

def create_resume_docx(resume, output_path):

    doc = Document()

    # =================================================
    # PAGE MARGINS
    # =================================================

    section = doc.sections[0]

    section.top_margin = Inches(0.3)

    section.bottom_margin = Inches(0.3)

    section.left_margin = Inches(0.3)

    section.right_margin = Inches(0.3)

    # =================================================
    # HEADER TABLE
    # =================================================

    header_table = doc.add_table(
        rows=1,
        cols=2
    )
    header_table.autofit = False

    header_table.allow_autofit = False

    remove_table_borders(header_table)

    header_table.alignment = WD_TABLE_ALIGNMENT.LEFT

    left_cell = header_table.cell(0, 0)

    right_cell = header_table.cell(0, 1)

    left_cell.width = Inches(1.8)

    right_cell.width = Inches(5.7)

    # =================================================
    # HEADER BACKGROUND
    # =================================================

    set_cell_background(left_cell, "1C181B")

    set_cell_background(right_cell, "1C181B")

    set_cell_padding(
        right_cell,
        120,
        80,
        80,
        120
    )

    # =================================================
    # LEFT HEADER
    # =================================================

    p = left_cell.paragraphs[0]

    run = p.add_run("UST")
    p.paragraph_format.left_indent = Pt(45)

    p.paragraph_format.space_before = Pt(10)

    apply_font(
        run,
        "Aptos",
        20,
        bold=True,
        color="FFFFFF"
    )

    # =================================================
    # RIGHT HEADER
    # =================================================

    name_para = right_cell.paragraphs[0]
    name_para.paragraph_format.space_after = Pt(0)
    name_para.paragraph_format.space_before = Pt(10)
    run = name_para.add_run(
        resume.get("name", "")
    )

    apply_font(
        run,
        "Aptos",
        20,
        bold=True,
        color="FFFFFF"
    )

    role_para = right_cell.add_paragraph()

    role_para.paragraph_format.space_before = Pt(0)

    role_para.paragraph_format.space_after = Pt(0)

    run = role_para.add_run(
        resume.get("role", "")
    )

    apply_font(
        run,
        "Aptos",
        10,
        bold=True,
        color="D9D9D9"
    )

    contact_para = right_cell.add_paragraph()

    contact_para.paragraph_format.space_before = Pt(0)

    contact_para.paragraph_format.space_after = Pt(0)

    contact_text = (
        f"Mob: {resume.get('mobile', '')} | "
        f"Email: {resume.get('email', '')}"
    )

    run = contact_para.add_run(contact_text)

    apply_font(
        run,
        "Aptos",
        9,
        color="CFCFCF"
    )

    # =================================================
    # MAIN LAYOUT TABLE
    # =================================================

    layout_table = doc.add_table(
        rows=1,
        cols=2
    )

    layout_table.alignment = WD_TABLE_ALIGNMENT.LEFT
    row = layout_table.rows[0]

    row.height_rule = WD_ROW_HEIGHT_RULE.AT_LEAST

    row.height = Inches(8.6)

    remove_table_borders(layout_table)

    layout_table.autofit = False

    layout_table.allow_autofit = False

    layout_table.left_indent = Inches(0.25)

    sidebar_cell = layout_table.cell(0, 0)


    content_cell = layout_table.cell(0, 1)

    # =================================================
    # COLUMN WIDTHS
    # =================================================

    sidebar_cell.width = Inches(2.2)

    content_cell.width = Inches(5.3)

    # =================================================
    # SIDEBAR COLOR
    # =================================================

    set_cell_background(
        sidebar_cell,
        "006D73"
    )
    set_cell_padding(
        sidebar_cell,
        10,
        120,
        120,
        80
    )

    set_cell_padding(
        content_cell,
        120,
        180,
        120,
        180
    )

    # =================================================
    # SIDEBAR DATA
    # =================================================
    sidebar_cell.paragraphs[0]._element.getparent().remove(
        sidebar_cell.paragraphs[0]._element
    )
    for section in resume.get(
        "sidebar_sections",
        []
    ):

        title = section.get(
            "title",
            ""
        )

        items = section.get(
            "items",
            []
        )

        add_sidebar_title(
            sidebar_cell,
            title
        )

        for index, item in enumerate(items):

            is_last = index == len(items) - 1

            if isinstance(item, dict):

                category = item.get(
                    "category",
                    ""
                )

                skills = item.get(
                    "skills",
                    []
                )

                if category:

                    text = (
                        f"{category} : "
                        f"{', '.join(skills)}"
                    )

                    add_sidebar_text(
                        sidebar_cell,
                        text,
                        bullet=True,
                        last_item=True
                    )

                else:

                    for skill_index, skill in enumerate(skills):

                        add_sidebar_text(
                            sidebar_cell,
                            skill,
                            bullet=True,
                            last_item=(
                                skill_index == len(skills) - 1
                            )
                        )

            else:

                add_sidebar_text(
                    sidebar_cell,
                    str(item),
                    bullet=True,
                    last_item=is_last
                )

    # =================================================
    # MAIN CONTENT
    # =================================================
    content_cell.paragraphs[-1].paragraph_format.space_after = Pt(0)
    add_main_heading(
        content_cell,
        "Profile Summary"
    )

    summary = " ".join(

        resume.get(
            "summary",
            []
        )

    )

    para = content_cell.add_paragraph()

    para.paragraph_format.line_spacing = 1.2

    para.paragraph_format.space_after = Pt(8)

    run = para.add_run(summary)

    apply_font(
        run,
        "Aptos",
        9,
        color="000000"
    )
    # =================================================
    # EXPERIENCE SECTION
    # =================================================

    add_main_heading(
        content_cell,
        "Professional Experience"
    )
    for exp in resume.get(
    "experience",
    []
    ):

        for project in exp.get(
            "projects",
            []
        ):

            add_experience_entry(
                content_cell,
                project
            )
    doc.save(output_path)