from pathlib import Path
import fitz, re
SITE=Path('/workspace/hsmu-reappointment-guide')
PDF=SITE/'assets/docs/C020_faculty_personnel_rules_2026-05-22.pdf'
SNIP=SITE/'assets/snippets'
# Create a tight screenshot just for Article 15 reappointment role research reduction table.
doc=fitz.open(PDF)
page=doc[3]  # PDF page 4, article 15
for term in ['제15조','재임용시 보직교원에 대한 경감기준','보직임용기간에 비례','최소 월 단위','학과장','30%','부총장','80%']:
    for r in page.search_for(term):
        if 285 <= r.y0 <= 410:
            a=page.add_highlight_annot(r); a.set_colors(stroke=(1,.86,0)); a.update()
pix=page.get_pixmap(matrix=fitz.Matrix(3,3), clip=fitz.Rect(45,285,page.rect.width-45,415), alpha=False)
out=SNIP/'c020_article15_reappointment_role_research_reduction.png'
pix.save(out)
print(out, out.stat().st_size)

DOC='assets/docs/C020_faculty_personnel_rules_2026-05-22.pdf'
def actions(img):
    return f'<div class="actions"><a class="btn secondary" href="{DOC}" target="_blank">원문 문서</a><a class="btn warn" href="assets/snippets/{img}" target="_blank">구문 캡쳐</a></div>'
explicit = f'''
<div class="evidence" id="chair-research-reduction" style="margin-top:16px"><b>학과장 재임용 연구실적 경감 근거 — 교원인사규정 제15조</b>
<p>재임용 평가대상기간 중 보직을 수행한 교원은 연구실적 기준을 경감할 수 있으며, 표에서 <b>“산학협력단장, 도서관장, 국제교류원장, 평생교육원장, 학과장”은 30%</b>로 명시되어 있습니다. 또한 <b>보직임용기간에 비례하여 환산</b>하고, 보직기간 산정은 <b>최소 월 단위</b>, 최소 연구실적 점수 환산 시 <b>소수점 이하는 계산하지 않는다</b>고 되어 있습니다.</p>
<div class="formula">예: 조교수 4년 기준 기본 연구실적 400%\n학과장 경감률 30% × 보직기간/전체 재임용기간\n2025.09~2029.02 = 42개월, 전체 48개월이면\n400% - (400% × 30% × 42/48) = 약 295%</div>
{actions('c020_article15_reappointment_role_research_reduction.png')}
</div>
'''
card = f'''<div class="card"><h3>제15조: 재임용시 학과장 연구실적 30% 경감</h3><p class="muted">학과장은 제15조 경감표에 직접 열거되어 있으며, 보직임용기간에 비례하여 환산합니다.</p><img class="snip" src="assets/snippets/c020_article15_reappointment_role_research_reduction.png">{actions('c020_article15_reappointment_role_research_reduction.png')}</div>'''

for fn in ['index.html','calculator.html']:
    p=SITE/fn
    s=p.read_text()
    if 'chair-research-reduction' not in s:
        # put immediately after role add/delete warning so users see it while editing role
        marker='</div></div><div class="resultbox"><h3>계산 결과</h3>'
        s=s.replace(marker, explicit + '</div></div><div class="resultbox"><h3>계산 결과</h3>', 1)
    if '제15조: 재임용시 학과장 연구실적 30% 경감' not in s:
        marker='<div class="grid two"><div class="card"><h3>제13조: 직급별 임용기간·학기말 만료</h3>'
        s=s.replace(marker, '<div class="grid two">'+card+'<div class="card"><h3>제13조: 직급별 임용기간·학기말 만료</h3>', 1)
    # Add a direct anchor in hero TOC if missing
    s=s.replace('<a href="#scores">기타 점수표</a>', '<a href="#chair-research-reduction">학과장 연구경감 근거</a><a href="#scores">기타 점수표</a>') if '학과장 연구경감 근거' not in s else s
    p.write_text(s)

# Update department-chair example page with prominent evidence
p=SITE/'department-chair.html'
s=p.read_text()
if '학과장 연구실적 30% 경감의 직접 근거' not in s:
    insert=f'''<section class="section"><div class="wrap"><h2>학과장 연구실적 30% 경감의 직접 근거</h2>{explicit}<div class="card" style="margin-top:16px"><img class="snip" src="assets/snippets/c020_article15_reappointment_role_research_reduction.png"></div></div></section>'''
    s=s.replace('<section class="section"><div class="wrap"><h2>주의점</h2>', insert+'<section class="section"><div class="wrap"><h2>주의점</h2>',1)
p.write_text(s)

# Update sources page snippet list
p=SITE/'sources.html'
s=p.read_text()
if '재임용시 학과장 연구실적 경감' not in s:
    new=f'''<div class="card"><h3>재임용시 학과장 연구실적 경감 30%</h3><a href="assets/snippets/c020_article15_reappointment_role_research_reduction.png"><img class="snip" src="assets/snippets/c020_article15_reappointment_role_research_reduction.png"></a>{actions('c020_article15_reappointment_role_research_reduction.png')}</div>'''
    s=s.replace('<div class="card"><h3>임용기간·재임용 절차</h3>', new+'\n<div class="card"><h3>임용기간·재임용 절차</h3>',1)
p.write_text(s)
print('added chair reduction evidence')
