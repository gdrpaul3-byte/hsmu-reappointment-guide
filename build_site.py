from pathlib import Path
import shutil, html, re
import fitz

SITE=Path('/workspace/hsmu-reappointment-guide')
AS=SITE/'assets'; DOCS=AS/'docs'; SNIP=AS/'snippets'
DOCS.mkdir(parents=True, exist_ok=True); SNIP.mkdir(parents=True, exist_ok=True)
SRC=Path('/workspace/hsmu_professor_rules')

sources = {
  'faculty_rules_pdf': SRC/'downloads/1316_교원인사규정(2026.05.22.시행_25차개정)/C020_교원인사규정(20260522시행_25차개정).pdf',
  'faculty_rules_hwp': SRC/'downloads/1316_교원인사규정(2026.05.22.시행_25차개정)/C020_교원인사규정(20260522시행_25차개정).hwp',
  'performance_detail_pdf': SRC/'downloads/1079_교원인사규정_업적실적평가_시행세칙(2024.12.06.시행_제정)/C023_교원인사규정 업적실적평가 시행세칙(20241206시행_제정).pdf',
  'appointment_committee_pdf': SRC/'downloads/1187_교원인사위원회_규정(2023.01.19.시행_4차개정)/F020_교원인사위원회 규정(20230119시행_4차개정).pdf',
  'tenure_committee_pdf': SRC/'downloads/1114_승진·정년임용심사위원회_규정(2025.08.25.시행_제정)/F040_승진·정년임용심사위원회 규정(20250825시행_제정).pdf',
  'counseling_center_pdf': SRC/'downloads_extra_counseling/1284_학생상담센터_운영에_관한_규정(2026.02.12.시행_3차개정)/G040_학생상담센터 운영에 관한 규정(20260212시행_3차개정).pdf',
}
name_map = {
 'faculty_rules_pdf':'C020_faculty_personnel_rules_2026-05-22.pdf',
 'faculty_rules_hwp':'C020_faculty_personnel_rules_2026-05-22.hwp',
 'performance_detail_pdf':'C023_performance_evaluation_detailed_rules_2024-12-06.pdf',
 'appointment_committee_pdf':'F020_faculty_personnel_committee_2023-01-19.pdf',
 'tenure_committee_pdf':'F040_promotion_tenure_committee_2025-08-25.pdf',
 'counseling_center_pdf':'G040_student_counseling_center_2026-02-12.pdf',
}
for k,p in sources.items():
    if p.exists(): shutil.copy2(p, DOCS/name_map[k])

# Render clipped snippets with highlighted searched terms.
def snippet(src_key, out_name, page_no, y0, y1, highlights=()):
    src = DOCS/name_map[src_key]
    doc = fitz.open(src)
    page = doc[page_no-1]
    for term in highlights:
        for r in page.search_for(term):
            if y0-40 <= r.y0 <= y1+40:
                annot = page.add_highlight_annot(r)
                annot.set_colors(stroke=(1, .86, 0))
                annot.update()
    rect=fitz.Rect(36,y0,page.rect.width-36,y1)
    pix=page.get_pixmap(matrix=fitz.Matrix(2.5,2.5), clip=rect, alpha=False)
    pix.save(SNIP/out_name)

snippet('faculty_rules_pdf','c020_article13_14_period_reappointment.png',3,520,780,['제13조','제14조','조교수 : 4년','교원인사위원회의 의결'])
snippet('faculty_rules_pdf','c020_article14_15_criteria_reduction.png',4,40,380,['연평균 100%','연평균 70점','제15조','학과장','30%'])
snippet('faculty_rules_pdf','c020_article16_documents.png',4,330,470,['제16조','재임용(재계약) 신청서','연구실적조서','교육업적조서','봉사업적조서'])
snippet('faculty_rules_pdf','c020_appendix3_education_counseling.png',16,40,785,['【별표 3】','학생 상담','학생상담결과보고서'])
snippet('faculty_rules_pdf','c020_appendix4_service_chair.png',17,235,430,['【별표 4】','교내 보직 활동','학과장','15점/학기'])
snippet('counseling_center_pdf','g040_counseling_center_professor_counseling.png',2,50,230,['교수의 학생지도 및 상담','개인 및 집단 상담'])

CSS = r'''
:root{--bg:#fff;--alt:#f6f7fb;--ink:#101318;--muted:#5f6673;--line:#dfe4ec;--blue:#075fe4;--blue2:#eef5ff;--green:#008a42;--orange:#c45100;--shadow:0 8px 30px rgba(18,38,63,.08)}*{box-sizing:border-box}body{margin:0;font-family:Inter,system-ui,-apple-system,"Segoe UI",Roboto,"Noto Sans KR",sans-serif;color:var(--ink);line-height:1.62;background:var(--bg)}a{color:var(--blue);text-decoration:none}a:hover{text-decoration:underline}.wrap{max-width:1180px;margin:auto;padding:0 24px}.nav{position:sticky;top:0;z-index:10;background:rgba(255,255,255,.9);backdrop-filter:blur(14px);border-bottom:1px solid var(--line)}.navin{height:64px;display:flex;align-items:center;justify-content:space-between}.brand{font-weight:900;letter-spacing:-.03em}.navlinks{display:flex;gap:16px;align-items:center;font-size:14px;font-weight:750}.hero{padding:76px 0 48px}.badge{display:inline-flex;align-items:center;border-radius:999px;padding:5px 10px;background:var(--blue2);color:#084fbf;font-size:12px;font-weight:800}.hero h1{font-size:clamp(38px,6.4vw,72px);line-height:1;letter-spacing:-.055em;margin:18px 0}.lead{font-size:19px;color:var(--muted);max-width:900px;font-weight:550}.section{padding:54px 0}.alt{background:var(--alt)}h2{font-size:clamp(30px,4vw,48px);letter-spacing:-.04em;line-height:1.05;margin:0 0 20px}.grid{display:grid;gap:18px}.two{grid-template-columns:repeat(2,minmax(0,1fr))}.three{grid-template-columns:repeat(3,minmax(0,1fr))}.card{background:#fff;border:1px solid var(--line);border-radius:18px;padding:22px;box-shadow:var(--shadow)}.card h3{font-size:22px;letter-spacing:-.025em;margin:0 0 8px}.metric{font-size:42px;font-weight:900;letter-spacing:-.05em;line-height:1}.muted{color:var(--muted)}.btn{display:inline-flex;align-items:center;gap:7px;border-radius:9px;background:var(--blue);color:#fff!important;padding:8px 12px;font-weight:850;font-size:14px}.btn.secondary{background:#eef1f6;color:#17202b!important}.btn.warn{background:#fff4e8;color:#a24400!important}.actions{display:flex;gap:8px;flex-wrap:wrap;margin-top:14px}.toc{display:flex;gap:9px;flex-wrap:wrap;margin-top:22px}.toc a{border:1px solid var(--line);border-radius:999px;padding:7px 11px;background:#fff;font-weight:800;font-size:13px}.table{overflow:auto;border:1px solid var(--line);border-radius:16px;background:#fff;box-shadow:var(--shadow)}table{border-collapse:collapse;width:100%;min-width:760px}th,td{border-bottom:1px solid var(--line);padding:14px 15px;text-align:left;vertical-align:top}th{background:#f8fafc;font-size:13px;color:#475569}.evidence{border-left:4px solid var(--blue);background:#f8fbff;border-radius:14px;padding:16px;margin-top:14px}.callout{border-radius:16px;padding:18px 20px;background:#eefdf4;border:1px solid #c9f1d9}.source-list li{margin:10px 0}.footer{padding:36px 0;color:var(--muted);border-top:1px solid var(--line)}img.snip{width:100%;border:1px solid var(--line);border-radius:14px;background:#fff;box-shadow:var(--shadow)}.small{font-size:13px}.pill{display:inline-block;border:1px solid var(--line);border-radius:999px;padding:2px 8px;margin:2px;background:#fff;font-size:12px;font-weight:800}.formula{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;background:#111827;color:#fff;border-radius:12px;padding:14px;overflow:auto}@media(max-width:860px){.two,.three{grid-template-columns:1fr}.navlinks{gap:8px;font-size:12px}.navin{height:auto;padding:12px 0;align-items:flex-start}.navlinks{flex-wrap:wrap;justify-content:flex-end}}
'''

def ev(doc='assets/docs/C020_faculty_personnel_rules_2026-05-22.pdf', img='', label='근거 보기'):
    imgbtn=f'<a class="btn warn" href="assets/snippets/{img}" target="_blank">구문 캡쳐</a>' if img else ''
    return f'<div class="actions"><a class="btn secondary" href="{doc}" target="_blank">원문 문서</a>{imgbtn}</div>'

def head(title):
    return f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet"><title>{html.escape(title)}</title><style>{CSS}</style></head><body><div class="nav"><div class="wrap navin"><div class="brand">HSMU 교수 재임용 근거 가이드</div><div class="navlinks"><a href="index.html">요약</a><a href="department-chair.html">학과장</a><a href="regular-faculty.html">일반교원</a><a href="sources.html">원자료</a></div></div></div>'''

def foot():
    return '''<div class="footer"><div class="wrap small">출처: 화성의과학대학교 그룹웨어 대학규정 게시판에서 내려받은 최신 자료 기준. 이 페이지는 규정 검토 보조자료이며, 최종 적용·인정 여부는 교무/인사 담당 부서 확인이 필요합니다.</div></div></body></html>'''

index = head('HSMU 교수 재임용 기준·근거 자료') + f'''
<section class="hero"><div class="wrap"><span class="badge">원문 PDF/HWP + 구문 캡쳐 포함</span><h1>교수 재임용 기준을 근거 문서와 함께 확인하는 페이지</h1><p class="lead">각 기준 항목에 <b>원문 문서</b>와 <b>해당 구문 캡쳐</b> 링크를 붙였습니다. 사용자는 요약표에서 바로 원 규정 PDF/HWP와 캡쳐 이미지로 이동할 수 있습니다.</p><div class="toc"><a href="#compare">핵심 비교</a><a href="#criteria">재임용 기준</a><a href="#evidence">근거 캡쳐</a><a href="sources.html">원자료 전체</a></div></div></section>
<section id="compare" class="section alt"><div class="wrap"><h2>핵심 비교</h2><div class="grid two"><div class="card"><span class="badge">학과장 보직 있음</span><h3>2025.09~2029.02 학과장 계속 가정</h3><div class="metric">약 295%</div><p class="muted">조교수 4년 기본 400%에서 학과장 연구실적 30% 경감을 보직기간 비례로 적용한 추정치입니다.</p>{ev(img='c020_article14_15_criteria_reduction.png')}<a class="btn" href="department-chair.html" style="margin-top:14px">상세 계산 보기</a></div><div class="card"><span class="badge">일반 전임교원</span><h3>학과장 보직 없음</h3><div class="metric">400%</div><p class="muted">조교수 임용기간 4년 × 재임용 연구실적 연평균 100% = 400%입니다.</p>{ev(img='c020_article13_14_period_reappointment.png')}<a class="btn secondary" href="regular-faculty.html" style="margin-top:14px">상세 기준 보기</a></div></div></div></section>
<section id="criteria" class="section"><div class="wrap"><h2>항목별 기준과 근거</h2><div class="table"><table><thead><tr><th>항목</th><th>요약</th><th>근거 이동</th></tr></thead><tbody>
<tr><td>임용기간</td><td>교수 6년, 부교수 6년, 조교수 4년. 교수는 승진·정년임용심사위원회 심사 통과 후 정년까지 임용.</td><td>{ev(img='c020_article13_14_period_reappointment.png')}</td></tr>
<tr><td>재임용 절차</td><td>교원인사위원회 의결 → 총장 제청 → 이사회 의결.</td><td>{ev(img='c020_article13_14_period_reappointment.png')}</td></tr>
<tr><td>연구실적</td><td>현직급 재임용기간 내 연평균 100% 이상. 등재/등재후보지급 이상 논문실적 1편 이상 필요.</td><td>{ev(img='c020_article14_15_criteria_reduction.png')}</td></tr>
<tr><td>교육업적</td><td>현직급 재임용기간 내 연평균 70점 이상.</td><td>{ev(img='c020_article14_15_criteria_reduction.png')}</td></tr>
<tr><td>봉사업적</td><td>현직급 재임용기간 내 연평균 70점 이상.</td><td>{ev(img='c020_article14_15_criteria_reduction.png')}</td></tr>
<tr><td>학과장 연구실적 경감</td><td>학과장은 연구실적 기준 30% 경감 가능. 보직임용기간에 비례하여 환산.</td><td>{ev(img='c020_article14_15_criteria_reduction.png')}</td></tr>
<tr><td>학과장 봉사업적</td><td>봉사 업적 평가 기준상 학과장 등 센터장/부서장급 보직은 15점/학기.</td><td>{ev(img='c020_appendix4_service_chair.png')}</td></tr>
<tr><td>학생상담/면담</td><td>교육업적 별표 3상 학생 상담 결과보고서 제출 시 10점/학기, 미제출 시 -5점/학기. 교양과목은 15명 이상 제출 기준 별도.</td><td>{ev(img='c020_appendix3_education_counseling.png')}</td></tr>
<tr><td>제출서류</td><td>재임용 신청서, 연구실적조서, 교육업적조서, 봉사업적조서 및 증빙자료.</td><td>{ev(img='c020_article16_documents.png')}</td></tr>
</tbody></table></div></div></section>
<section id="evidence" class="section alt"><div class="wrap"><h2>주요 구문 캡쳐</h2><div class="grid two"><div class="card"><h3>제13조~제14조: 임용기간·재임용 절차</h3><a href="assets/snippets/c020_article13_14_period_reappointment.png" target="_blank"><img class="snip" src="assets/snippets/c020_article13_14_period_reappointment.png"></a></div><div class="card"><h3>제14조~제15조: 기준·보직 경감</h3><a href="assets/snippets/c020_article14_15_criteria_reduction.png" target="_blank"><img class="snip" src="assets/snippets/c020_article14_15_criteria_reduction.png"></a></div><div class="card"><h3>별표 3: 학생 상담/결과보고서</h3><a href="assets/snippets/c020_appendix3_education_counseling.png" target="_blank"><img class="snip" src="assets/snippets/c020_appendix3_education_counseling.png"></a></div><div class="card"><h3>별표 4: 학과장 봉사업적 15점/학기</h3><a href="assets/snippets/c020_appendix4_service_chair.png" target="_blank"><img class="snip" src="assets/snippets/c020_appendix4_service_chair.png"></a></div></div></div></section>
''' + foot()

common_evidence = f'''<div class="evidence"><b>근거 구조</b><p class="muted">각 판단 항목은 원문 PDF와 캡쳐 이미지를 함께 제공합니다. PDF는 원자료 전체 확인용, PNG는 해당 구문 빠른 확인용입니다.</p>{ev(img='c020_article14_15_criteria_reduction.png')}</div>'''

department = head('학과장 교수 재임용 기준') + f'''
<section class="hero"><div class="wrap"><span class="badge">학과장 보직자용</span><h1>학과장인 경우: 연구실적 경감과 봉사업적 보직점수</h1><p class="lead">2025.03 조교수 임용, 2025.09부터 2029.02까지 학과장 보직을 계속 수행한다는 가정의 계산입니다.</p></div></section>
<section class="section alt"><div class="wrap"><h2>계산</h2><div class="grid two"><div class="card"><h3>연구실적 필요치</h3><div class="formula">기본: 4년 × 100% = 400%\n학과장 보직기간: 2025.09~2029.02 = 42개월\n전체 재임용기간: 2025.03~2029.02 = 48개월\n경감: 400% × 30% × 42/48 = 105%\n예상 필요치: 400% - 105% = 295%</div>{ev(img='c020_article14_15_criteria_reduction.png')}</div><div class="card"><h3>봉사업적</h3><p>별표 4상 학과장은 교내 보직 활동으로 <b>15점/학기</b>를 받을 수 있습니다. 2025.09~2029.02는 약 7학기이므로 약 105점으로 계산할 수 있습니다.</p>{ev(img='c020_appendix4_service_chair.png')}</div></div>{common_evidence}</div></section>
<section class="section"><div class="wrap"><h2>주의점</h2><ul><li>경감은 “할 수 있으며” 문구이므로 자동 적용 여부는 인사 담당 부서 확인이 필요합니다.</li><li>보직기간 산정은 최소 월 단위이며, 소수점 이하는 계산하지 않는다고 규정되어 있습니다.</li><li>교육업적·봉사업적 연평균 70점 이상 요건은 학과장 여부와 무관하게 유지됩니다.</li></ul></div></section>
''' + foot()

regular = head('일반 전임교원 재임용 기준') + f'''
<section class="hero"><div class="wrap"><span class="badge">일반 전임교원용</span><h1>학과장 보직이 없는 경우: 조교수 4년 400% 기준</h1><p class="lead">조교수 임용기간 4년을 기준으로 연구실적은 연평균 100%, 교육·봉사업적은 각각 연평균 70점 이상을 충족해야 합니다.</p></div></section>
<section class="section alt"><div class="wrap"><h2>기준</h2><div class="grid three"><div class="card"><h3>연구</h3><div class="metric">400%</div><p>4년 × 100%. 등재/등재후보지급 이상 논문 1편 이상 필요.</p>{ev(img='c020_article14_15_criteria_reduction.png')}</div><div class="card"><h3>교육</h3><div class="metric">70점</div><p>현직급 재임용기간 내 연평균 70점 이상.</p>{ev(img='c020_article14_15_criteria_reduction.png')}</div><div class="card"><h3>봉사</h3><div class="metric">70점</div><p>현직급 재임용기간 내 연평균 70점 이상.</p>{ev(img='c020_article14_15_criteria_reduction.png')}</div></div>{common_evidence}</div></section>
<section class="section"><div class="wrap"><h2>학생 상담 관련</h2><p class="lead">교육업적 별표 3에 학생 상담 결과보고서 제출 항목이 포함되어 있습니다. 규정 자체는 별도 서식인지 인트라넷 상담카드인지 명시하지 않습니다.</p><div class="grid two"><div class="card"><h3>교원인사규정 별표 3</h3><img class="snip" src="assets/snippets/c020_appendix3_education_counseling.png">{ev(img='c020_appendix3_education_counseling.png')}</div><div class="card"><h3>학생상담센터 운영 규정</h3><img class="snip" src="assets/snippets/g040_counseling_center_professor_counseling.png"><div class="actions"><a class="btn secondary" href="assets/docs/G040_student_counseling_center_2026-02-12.pdf" target="_blank">원문 문서</a><a class="btn warn" href="assets/snippets/g040_counseling_center_professor_counseling.png" target="_blank">구문 캡쳐</a></div></div></div></div></section>
''' + foot()

sources_html = head('원자료 목록') + '''
<section class="hero"><div class="wrap"><span class="badge">원자료 아카이브</span><h1>웹페이지에 포함된 원문 문서</h1><p class="lead">아래 문서는 사이트 안에 포함되어 있어 요약 항목에서 직접 열 수 있습니다.</p></div></section>
<section class="section alt"><div class="wrap"><h2>문서 목록</h2><ul class="source-list">
<li><b>교원인사규정</b> (2026.05.22 시행, 25차 개정) — <a href="assets/docs/C020_faculty_personnel_rules_2026-05-22.pdf">PDF</a> · <a href="assets/docs/C020_faculty_personnel_rules_2026-05-22.hwp">HWP</a> <span class="pill">핵심 기준</span></li>
<li><b>교원인사규정 업적실적평가 시행세칙</b> (2024.12.06 시행) — <a href="assets/docs/C023_performance_evaluation_detailed_rules_2024-12-06.pdf">PDF</a></li>
<li><b>교원인사위원회 규정</b> (2023.01.19 시행) — <a href="assets/docs/F020_faculty_personnel_committee_2023-01-19.pdf">PDF</a></li>
<li><b>승진·정년임용심사위원회 규정</b> (2025.08.25 시행) — <a href="assets/docs/F040_promotion_tenure_committee_2025-08-25.pdf">PDF</a></li>
<li><b>학생상담센터 운영에 관한 규정</b> (2026.02.12 시행) — <a href="assets/docs/G040_student_counseling_center_2026-02-12.pdf">PDF</a></li>
</ul></div></section>
<section class="section"><div class="wrap"><h2>구문 캡쳐 목록</h2><div class="grid two">
<div class="card"><h3>임용기간·재임용 절차</h3><a href="assets/snippets/c020_article13_14_period_reappointment.png"><img class="snip" src="assets/snippets/c020_article13_14_period_reappointment.png"></a></div>
<div class="card"><h3>평가 기준·보직 경감</h3><a href="assets/snippets/c020_article14_15_criteria_reduction.png"><img class="snip" src="assets/snippets/c020_article14_15_criteria_reduction.png"></a></div>
<div class="card"><h3>제출서류</h3><a href="assets/snippets/c020_article16_documents.png"><img class="snip" src="assets/snippets/c020_article16_documents.png"></a></div>
<div class="card"><h3>학생상담</h3><a href="assets/snippets/c020_appendix3_education_counseling.png"><img class="snip" src="assets/snippets/c020_appendix3_education_counseling.png"></a></div>
<div class="card"><h3>학과장 봉사업적</h3><a href="assets/snippets/c020_appendix4_service_chair.png"><img class="snip" src="assets/snippets/c020_appendix4_service_chair.png"></a></div>
<div class="card"><h3>상담센터 운영 규정</h3><a href="assets/snippets/g040_counseling_center_professor_counseling.png"><img class="snip" src="assets/snippets/g040_counseling_center_professor_counseling.png"></a></div>
</div></div></section>
''' + foot()

(SITE/'index.html').write_text(index)
(SITE/'department-chair.html').write_text(department)
(SITE/'regular-faculty.html').write_text(regular)
(SITE/'sources.html').write_text(sources_html)
(SITE/'.nojekyll').write_text('')
(SITE/'README.md').write_text('# HSMU 교수 재임용 근거 가이드\n\n정적 HTML 웹페이지입니다. 원문 PDF/HWP와 주요 구문 캡쳐 이미지를 포함합니다.\n')
print('built', SITE)
