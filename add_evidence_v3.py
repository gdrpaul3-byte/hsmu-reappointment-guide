from pathlib import Path
import fitz
SITE=Path('/workspace/hsmu-reappointment-guide')
SNIP=SITE/'assets/snippets'
PDF=SITE/'assets/docs/C020_faculty_personnel_rules_2026-05-22.pdf'

def make_snip(out_name,page_no,y0,y1,terms):
    out=SNIP/out_name
    doc=fitz.open(PDF)
    page=doc[page_no-1]
    for term in terms:
        for r in page.search_for(term):
            if y0-50 <= r.y0 <= y1+50:
                a=page.add_highlight_annot(r); a.set_colors(stroke=(1,.86,0)); a.update()
    pix=page.get_pixmap(matrix=fitz.Matrix(2.5,2.5), clip=fitz.Rect(36,y0,page.rect.width-36,y1), alpha=False)
    pix.save(out)
    print(out, out.stat().st_size)

make_snip('c020_article23_evaluation_target.png',6,120,360,['제21조','제23조','재임용은','임용기간 내','교육업적과 봉사업적'])
make_snip('c020_article13_period_semester_end.png',3,535,710,['제13조','교수 : 6년','부교수 : 6년','조교수 : 4년','학기의 말일'])
make_snip('c020_article26_role_term_appointment.png',6,320,560,['제26조','보직','기타 부속기관장','보직의 임기는','3월 1일','9월 1일','학기말까지 연장'])

DOC='assets/docs/C020_faculty_personnel_rules_2026-05-22.pdf'
def ev(img):
    return f'<div class="actions"><a class="btn secondary" href="{DOC}" target="_blank">원문 문서</a><a class="btn warn" href="assets/snippets/{img}" target="_blank">구문 캡쳐</a></div>'

period_evidence = f'''
<div class="evidence" id="period-evidence"><b>연차·평가기간 산정 근거</b>
<ul>
<li><b>직급별 재임용 연차</b>: 제13조 제1항 — 교수 6년, 부교수 6년, 조교수 4년.</li>
<li><b>학기말 만료 처리</b>: 제13조 제3항 — 임용기간 만료일이 학기 도중이면 그 학기의 말일을 만료일로 봄.</li>
<li><b>평가 대상 기간</b>: 제14조 제2항 — 현직급 재임용기간 내 연평균 연구 100%, 교육/봉사 70점.</li>
<li><b>연구실적 발생 기간</b>: 제23조 제1항 — 재임용 연구실적은 임용기간 내 발표된 것이어야 함.</li>
<li><b>보직기간 환산</b>: 제15조 — 보직임용기간에 비례하여 환산, 최소 월 단위, 소수점 이하는 계산하지 않음.</li>
<li><b>보직 임명/임기</b>: 제26조 — 보직 정의, 임기, 3월 1일/9월 1일 임명 원칙, 학기 중 종료 시 학기말 연장 가능.</li>
</ul>
<div class="grid three">
<div>{ev('c020_article13_period_semester_end.png')}</div>
<div>{ev('c020_article23_evaluation_target.png')}</div>
<div>{ev('c020_article26_role_term_appointment.png')}</div>
</div></div>
'''

calc_note = f'''<div class="warnbox" style="margin-top:14px"><b>계산기 입력칸별 근거</b><br>
직급 선택은 제13조의 직급별 임용기간을 따르고, 평가 시작/종료일은 제13조의 임용기간 및 학기말 만료 문구, 연구/교육/봉사 목표는 제14조의 “현직급 재임용기간 내 연평균” 문구, 보직 기간은 제15조의 “보직임용기간에 비례·월 단위” 문구를 근거로 계산합니다.
{ev('c020_article13_period_semester_end.png')}{ev('c020_article14_15_criteria_reduction.png')}{ev('c020_article23_evaluation_target.png')}{ev('c020_article26_role_term_appointment.png')}
</div>'''

score_evidence = f'''<div class="evidence" style="margin-top:16px"><b>점수표 근거</b><br>
교육 점수는 교원인사규정 별표3, 봉사 점수는 별표4에서 가져왔습니다. 검색 결과의 항목명은 요약이므로 실제 제출 전 원문 캡쳐와 PDF를 함께 확인하세요.
{ev('c020_appendix3_education_counseling.png')}{ev('c020_appendix4_service_chair.png')}
</div>'''

for fn in ['index.html','calculator.html']:
    p=SITE/fn
    s=p.read_text()
    # Insert calculator field evidence immediately after basic information form block if not present
    if '계산기 입력칸별 근거' not in s:
        marker='<h3 style="margin-top:20px">보직 추가/삭제</h3>'
        s=s.replace(marker, calc_note + marker)
    # Insert period evidence before calculation evidence section
    if '연차·평가기간 산정 근거' not in s:
        marker='<section id="evidence" class="section alt"><div class="wrap"><h2>계산 근거</h2>'
        s=s.replace(marker, '<section class="section"><div class="wrap"><h2>연차/기간 산정 근거</h2>'+period_evidence+'</div></section>\n'+marker)
    # Insert score evidence after scoreList card
    if '점수표 근거' not in s:
        marker='<div id="scoreList" style="margin-top:12px"></div></div></div></section>'
        s=s.replace(marker, '<div id="scoreList" style="margin-top:12px"></div>'+score_evidence+'</div></div></section>')
    # Add article13 snippet to evidence grid if absent in grid
    if 'c020_article13_period_semester_end.png"' not in s.split('<section id="evidence"')[-1]:
        insert='<div class="card"><h3>제13조: 직급별 임용기간·학기말 만료</h3><img class="snip" src="assets/snippets/c020_article13_period_semester_end.png">'+ev('c020_article13_period_semester_end.png')+'</div>'
        s=s.replace('<div class="grid two"><div class="card"><h3>제14조~제15조', '<div class="grid two">'+insert+'<div class="card"><h3>제14조~제15조')
    p.write_text(s)

# Update sources page snippet list
p=SITE/'sources.html'
s=p.read_text()
if '연차/평가기간' not in s:
    cards='''
<div class="card"><h3>연차/임용기간·학기말 만료</h3><a href="assets/snippets/c020_article13_period_semester_end.png"><img class="snip" src="assets/snippets/c020_article13_period_semester_end.png"></a></div>
<div class="card"><h3>평가대상 기간: 임용기간 내 실적</h3><a href="assets/snippets/c020_article23_evaluation_target.png"><img class="snip" src="assets/snippets/c020_article23_evaluation_target.png"></a></div>
<div class="card"><h3>보직 임기/임명일/학기말 연장</h3><a href="assets/snippets/c020_article26_role_term_appointment.png"><img class="snip" src="assets/snippets/c020_article26_role_term_appointment.png"></a></div>
'''
    s=s.replace('</div></div></section>\n<div class="footer">', cards+'</div></div></section>\n<div class="footer">')
p.write_text(s)

# README
(SITE/'README.md').write_text('# HSMU 교수 재임용 선택형 계산기\n\n정적 HTML 웹페이지입니다. 보직 선택형 재임용 계산기, 교육/봉사 점수 검색, 원문 PDF/HWP와 주요 구문 캡쳐 이미지를 포함합니다. v3에서는 재임용 연차·평가기간·보직기간 산정 근거를 각 입력 항목에 연결했습니다.\n')
print('v3 evidence inserted')
