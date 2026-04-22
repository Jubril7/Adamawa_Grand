"""
Converts EPROJECT_REPORT.md to a professionally styled PDF.
Run: python3 make_pdf.py
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, black, white, grey
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import Flowable
import re

# ── Colours ────────────────────────────────────────────────
GOLD   = HexColor('#B8860B')
GOLD_L = HexColor('#D4A017')
NAVY   = HexColor('#1C2B3A')
CREAM  = HexColor('#F7F3EC')
LIGHT  = HexColor('#F0EAD6')
MID    = HexColor('#888888')
BORDER = HexColor('#D4C4A0')

W, H = A4

# ── Styles ──────────────────────────────────────────────────
base = getSampleStyleSheet()

def S(name, **kw):
    return ParagraphStyle(name, **kw)

styles = {
    'cover_hotel': S('cover_hotel',
        fontName='Helvetica-Bold', fontSize=28, textColor=GOLD,
        spaceAfter=6, leading=34, alignment=TA_CENTER),
    'cover_title': S('cover_title',
        fontName='Helvetica', fontSize=18, textColor=white,
        spaceAfter=4, leading=24, alignment=TA_CENTER),
    'cover_sub': S('cover_sub',
        fontName='Helvetica', fontSize=12, textColor=HexColor('#CCBBAA'),
        spaceAfter=4, alignment=TA_CENTER),
    'h1': S('h1',
        fontName='Helvetica-Bold', fontSize=18, textColor=NAVY,
        spaceBefore=18, spaceAfter=6, leading=22),
    'h2': S('h2',
        fontName='Helvetica-Bold', fontSize=13, textColor=NAVY,
        spaceBefore=14, spaceAfter=4, leading=17),
    'h3': S('h3',
        fontName='Helvetica-BoldOblique', fontSize=11, textColor=GOLD,
        spaceBefore=10, spaceAfter=3, leading=14),
    'body': S('body',
        fontName='Helvetica', fontSize=10, textColor=HexColor('#333333'),
        spaceAfter=5, leading=15),
    'code': S('code',
        fontName='Courier', fontSize=8.5, textColor=HexColor('#1C2B3A'),
        backColor=HexColor('#F5F0E8'), spaceAfter=4, leading=13,
        leftIndent=10, rightIndent=10, spaceBefore=4,
        borderPad=6),
    'li': S('li',
        fontName='Helvetica', fontSize=10, textColor=HexColor('#333333'),
        spaceAfter=3, leading=14, leftIndent=18,
        bulletIndent=8),
    'eyebrow': S('eyebrow',
        fontName='Helvetica-Bold', fontSize=8, textColor=GOLD,
        spaceBefore=8, spaceAfter=2, leading=10,
        charSpace=1.5),
    'toc': S('toc',
        fontName='Helvetica', fontSize=10.5, textColor=NAVY,
        spaceAfter=5, leading=16, leftIndent=0),
    'toc_sub': S('toc_sub',
        fontName='Helvetica', fontSize=10, textColor=HexColor('#555555'),
        spaceAfter=3, leading=14, leftIndent=16),
    'table_header': S('th',
        fontName='Helvetica-Bold', fontSize=9, textColor=white, leading=12),
    'table_cell': S('td',
        fontName='Helvetica', fontSize=9, textColor=HexColor('#333333'), leading=12),
}


class GoldRule(Flowable):
    """A full-width gold horizontal rule."""
    def __init__(self, height=2, color=GOLD):
        super().__init__()
        self.height = height
        self.color = color
        self.width = 0

    def wrap(self, availWidth, availHeight):
        self.width = availWidth
        return availWidth, self.height + 4

    def draw(self):
        self.canv.setFillColor(self.color)
        self.canv.rect(0, 2, self.width, self.height, stroke=0, fill=1)


class NavyCoverBlock(Flowable):
    """Dark cover header block."""
    def __init__(self, w, h=200):
        super().__init__()
        self._w, self._h = w, h

    def wrap(self, *args):
        return self._w, self._h

    def draw(self):
        c = self.canv
        # Background
        c.setFillColor(NAVY)
        c.rect(0, 0, self._w, self._h, stroke=0, fill=1)
        # Gold bottom stripe
        c.setFillColor(GOLD)
        c.rect(0, 0, self._w, 5, stroke=0, fill=1)
        # Gold top stripe
        c.setFillColor(GOLD_L)
        c.rect(0, self._h - 4, self._w, 4, stroke=0, fill=1)
        # Diagonal pattern lines
        c.setStrokeColor(HexColor('#FFFFFF'))
        c.setLineWidth(0.3)
        for x in range(int(-self._h), int(self._w + self._h), 40):
            c.setStrokeAlpha(0.04)
            c.line(x, 0, x + self._h, self._h)
        c.setStrokeAlpha(1.0)


def on_page(canvas, doc):
    """Header/footer on every page except first."""
    if doc.page <= 1:
        return
    w, h = A4
    canvas.saveState()
    # Top rule
    canvas.setFillColor(NAVY)
    canvas.rect(doc.leftMargin, h - 1.2*cm, w - doc.leftMargin - doc.rightMargin, 0.4, stroke=0, fill=1)
    # Header text
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(MID)
    canvas.drawString(doc.leftMargin, h - 1.05*cm, 'Adamawa Grand Hotel & Suites — Hotel Room Booking System')
    canvas.drawRightString(w - doc.rightMargin, h - 1.05*cm, 'eProject Report')
    # Footer rule
    canvas.setFillColor(GOLD)
    canvas.rect(doc.leftMargin, 1.5*cm, w - doc.leftMargin - doc.rightMargin, 1.5, stroke=0, fill=1)
    # Page number
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(MID)
    canvas.drawCentredString(w / 2, 1.0*cm, f'Page {doc.page}')
    canvas.restoreState()


def read_md(path):
    with open(path, encoding='utf-8') as f:
        return f.read()


def table_from_rows(rows, col_widths=None):
    data = []
    for row in rows:
        data.append([Paragraph(c, styles['table_cell']) for c in row])

    ts = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('TEXTCOLOR',  (0, 0), (-1, 0), white),
        ('FONTNAME',   (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE',   (0, 0), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [CREAM, white]),
        ('GRID',       (0, 0), (-1, -1), 0.4, BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN',     (0, 0), (-1, -1), 'TOP'),
    ])
    avail = W - 4*cm
    if not col_widths:
        n = len(rows[0]) if rows else 1
        col_widths = [avail / n] * n
    return Table(data, colWidths=col_widths, style=ts, repeatRows=1)


def md_to_rl(txt):
    """Convert inline markdown to ReportLab-safe XML."""
    # Escape special XML chars first (before adding tags)
    txt = txt.replace('&', '&amp;')
    # Bold: **text**
    txt = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', txt)
    # Inline code: `text`
    txt = re.sub(r'`(.+?)`', lambda m: '<font face="Courier" size="9" color="#1C2B3A">' + m.group(1).replace('&amp;', '&amp;') + '</font>', txt)
    # Strip any leftover bare * that would break XML
    txt = re.sub(r'(?<!\*)\*(?!\*)', '', txt)
    return txt


# ── Parse and build story ────────────────────────────────────
def build_story(md_text):
    story = []
    lines = md_text.split('\n')

    # ── Cover Page ────────────────────────────────────────────
    avail_w = W - 4*cm
    story.append(NavyCoverBlock(avail_w, h=220))
    story.append(Spacer(1, 0.4*cm))
    story.append(Paragraph('ADAMAWA GRAND HOTEL &amp; SUITES', styles['cover_hotel']))
    story.append(Spacer(1, 0.1*cm))
    story.append(Paragraph('Hotel Room Booking System', styles['cover_title']))
    story.append(Spacer(1, 0.3*cm))
    story.append(GoldRule())
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph('eProject Report', ParagraphStyle('ep',
        fontName='Helvetica-Bold', fontSize=22, textColor=NAVY,
        alignment=TA_CENTER, spaceAfter=6)))
    story.append(Paragraph('Yola, Adamawa State, Nigeria  ·  Developed with Django (Python)', styles['cover_sub']))
    story.append(Spacer(1, 2*cm))

    # Metadata block
    meta = [
        ['Technology',  'Django 4.2, Bootstrap 5, SQLite, Python 3.x'],
        ['Hotel',       'Adamawa Grand Hotel & Suites, Yola, Adamawa State'],
        ['Date',        'April 2026'],
        ['Framework',   'Aptech eProject Learning Environment'],
    ]
    meta_table = Table(
        [[Paragraph(f'<b>{k}</b>', styles['table_cell']),
          Paragraph(v, styles['table_cell'])] for k, v in meta],
        colWidths=[3.5*cm, avail_w - 3.5*cm],
        style=TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), LIGHT),
            ('GRID', (0, 0), (-1, -1), 0.4, BORDER),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ])
    )
    story.append(meta_table)
    story.append(PageBreak())

    # ── Parse MD ─────────────────────────────────────────────
    in_table  = False
    in_code   = False
    code_buf  = []
    table_buf = []

    def flush_code():
        if code_buf:
            txt = '\n'.join(code_buf)
            # Wrap in a light box
            story.append(Paragraph(
                txt.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('\n', '<br/>').replace(' ', '&nbsp;'),
                styles['code']
            ))
            code_buf.clear()

    def flush_table():
        if not table_buf:
            return
        rows = []
        for row_line in table_buf:
            if re.match(r'^\s*\|?\s*[-:]+', row_line):
                continue
            cells = [c.strip() for c in row_line.strip().strip('|').split('|')]
            rows.append(cells)
        if len(rows) >= 2:
            max_cols = max(len(r) for r in rows)
            for r in rows:
                while len(r) < max_cols:
                    r.append('')
            avail = W - 4*cm
            col_w = [avail / max_cols] * max_cols
            # Give first col more weight in 2-col tables
            if max_cols == 2:
                col_w = [avail * 0.3, avail * 0.7]
            elif max_cols == 3:
                col_w = [avail * 0.22, avail * 0.28, avail * 0.5]
            story.append(table_from_rows(rows, col_w))
            story.append(Spacer(1, 0.2*cm))
        table_buf.clear()

    for line in lines:
        stripped = line.strip()

        # Code fence
        if stripped.startswith('```'):
            if in_code:
                flush_code()
                in_code = False
            else:
                flush_table()
                in_code = True
            continue

        if in_code:
            code_buf.append(line)
            continue

        # Table row
        if stripped.startswith('|'):
            in_table = True
            table_buf.append(stripped)
            continue
        else:
            if in_table:
                flush_table()
                in_table = False

        # Empty line
        if not stripped:
            story.append(Spacer(1, 0.15*cm))
            continue

        # Headings
        if stripped.startswith('#### '):
            story.append(Paragraph(stripped[5:], styles['h3']))
        elif stripped.startswith('### '):
            flush_table()
            text = stripped[4:]
            story.append(Spacer(1, 0.1*cm))
            story.append(Paragraph(text, styles['h2']))
            story.append(HRFlowable(width='100%', thickness=0.5, color=BORDER, spaceAfter=4))
        elif stripped.startswith('## '):
            flush_table()
            text = stripped[3:]
            # New section — add gold rule + heading
            story.append(Spacer(1, 0.3*cm))
            story.append(GoldRule(height=3))
            story.append(Spacer(1, 0.1*cm))
            story.append(Paragraph(text, styles['h1']))
        elif stripped.startswith('# '):
            # Document title — skip (already on cover)
            pass
        elif stripped.startswith('- '):
            txt = md_to_rl(stripped[2:])
            story.append(Paragraph(f'• &nbsp;{txt}', styles['li']))
        elif re.match(r'^\d+\.', stripped):
            txt = md_to_rl(re.sub(r'^(\d+)\.\s+', r'\1.  ', stripped))
            story.append(Paragraph(txt, styles['li']))
        else:
            story.append(Paragraph(md_to_rl(stripped), styles['body']))

    flush_code()
    flush_table()
    return story


# ── Build PDF ─────────────────────────────────────────────────
md = read_md('/Users/jubrilafc/Documents/HotelRoomBooking/EPROJECT_REPORT.md')
output = '/Users/jubrilafc/Documents/HotelRoomBooking/EPROJECT_REPORT.pdf'

doc = SimpleDocTemplate(
    output,
    pagesize=A4,
    leftMargin=2*cm,
    rightMargin=2*cm,
    topMargin=1.8*cm,
    bottomMargin=2*cm,
    title='eProject Report — Hotel Room Booking System',
    author='Adamawa Grand Hotel & Suites',
)

story = build_story(md)
doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print(f'PDF created: {output}')
