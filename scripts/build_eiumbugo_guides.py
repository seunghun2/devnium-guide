import os, re, subprocess, shutil

WORKDIR = "/Users/el/Desktop/데브늄/이음기프트/11.모바일 부고장"
SCRATCH = "/Users/el/.gemini/antigravity/brain/1b9a3745-0ae9-4184-a201-d3783030e02c/scratch"

# Copy updated Playwright MCP STEP 1 screenshot (without 예치금 잔액 card and without 조의금 서비스 설정 sidebar item)
step1_src = f"{SCRATCH}/admin_step1_final-2026-10-28T07-08-14-824Z.png"
if os.path.exists(step1_src):
    shutil.copyfile(step1_src, f"{WORKDIR}/guide-assets/admin_step1.png")
    shutil.copyfile(step1_src, f"{WORKDIR}/maeumbugo-real/public/guide-assets/admin_step1.png")

with open(f"{WORKDIR}/buipay.html", "r", encoding="utf-8") as f:
    buipay_html = f.read()

# Extract head/style from buipay.html (up to </style>)
style_end_idx = buipay_html.find("</style>")
base_head_css = buipay_html[:style_end_idx]

# Extract the STEP 1~7 screen-guide-card HTML from 74e1207:maeumbugo-real/public/buipay.html
old_html = subprocess.check_output(
    ["git", "show", "74e1207:maeumbugo-real/public/buipay.html"],
    cwd=WORKDIR
).decode("utf-8")

old_lines = old_html.splitlines()
step_cards_raw = "\n".join(old_lines[2416:3692])

# Replace each base64 image in step_cards_raw with /guide-assets/admin_step{1..7}.png
counter = [0]
def repl_b64(match):
    counter[0] += 1
    return f"guide-assets/admin_step{counter[0]}.png"

step_cards_clean = re.sub(r"data:image/png;base64,[A-Za-z0-9+/=]+", repl_b64, step_cards_raw)

# Split the 7 cards so we can:
# 1) Update STEP 1 (remove callout 3 송금mid잔액 실시간 조회, expand box 2 across all 4 cards, renumber 4->3 and 5->4)
# 2) Remove STEP 2 (조의금 서비스 설정) completely
# 3) Renumber STEP 3~7 -> STEP 2~6 and update all 3.5%/10% references to 3%/8%
parts = step_cards_clean.split('<div class="screen-guide-card">')
cards = ['    <div class="screen-guide-card">' + p.rstrip().removesuffix("<!-- 3. 일일 대사 · 주간 복구 · 월간 정산 · CS 대응 수칙 -->").rstrip() for p in parts[1:]]
assert len(cards) == 7, f"Expected 7 cards, got {len(cards)}"

# Build clean STEP 1 card (updated for 4 stat cards without 예치금 잔액 / 송금mid잔액 실시간 조회)
step1_card = """    <div class="screen-guide-card">
      <div class="screen-guide-header">
        <div>
          <div class="screen-guide-eyebrow">ADMIN &amp; PARTNER OPERATION WALKTHROUGH</div>
          <h3 class="screen-guide-title">STEP 1. 이음부고 어드민 — 부의금 결제 내역 실시간 모니터링 및 대사 원본 추출</h3>
          <p class="screen-guide-sub">조문객이 부고장에서 신용카드·간편결제로 결제한 모든 부의금 주문의 승인 상태, 원금, 수수료 마진을 실시간 확인하고 일일 3자 대사용 CSV를 추출합니다.</p>
        </div>
        <div class="screen-url-pill">https://iumbugo.com/admin/condolence-orders</div>
      </div>
      <div class="screen-canvas-wrap">
        <img src="guide-assets/admin_step1.png" alt="STEP 1. 이음부고 어드민 — 부의금 결제 내역 실시간 모니터링 및 대사 원본 추출" class="screen-img" />
        <svg class="screen-svg-overlay" viewBox="0 0 1440 920" preserveAspectRatio="xMidYMid meet">
          <!-- 1. 부의금 결제 내역 메뉴 -->
          <rect x="8" y="340" width="238" height="46" rx="6"
                fill="rgba(15, 23, 42, 0.035)" stroke="#ffffff" stroke-width="5" />
          <rect x="8" y="340" width="238" height="46" rx="6"
                fill="none" stroke="#0f172a" stroke-width="2.5" stroke-dasharray="7,4" />
          <polyline points="340,242 262,242 262,363 246,363" fill="none"
                stroke="#ffffff" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" />
          <polyline points="340,242 262,242 262,363 246,363" fill="none"
                stroke="#0f172a" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"
                marker-end="url(#mono-arrow)" />
          <g transform="translate(340, 242)">
            <rect x="0" y="-15" width="198" height="30" rx="15"
                  fill="#0f172a" stroke="#ffffff" stroke-width="2.5"
                  filter="url(#drop-shadow)" />
            <circle cx="15" cy="0" r="11" fill="#ffffff" />
            <text x="15" y="4.2" text-anchor="middle"
                  font-family="Pretendard, sans-serif" font-size="12" font-weight="900"
                  fill="#0f172a">1</text>
            <text x="32" y="4.2"
                  font-family="Pretendard, sans-serif" font-size="12" font-weight="700"
                  fill="#ffffff">부의금 결제 내역 메뉴</text>
          </g>

          <!-- 2. 실결제 4대 요약 지표 (전체 4개 카드 영역) -->
          <rect x="286" y="109" width="1108" height="116" rx="6"
                fill="rgba(15, 23, 42, 0.035)" stroke="#ffffff" stroke-width="5" />
          <rect x="286" y="109" width="1108" height="116" rx="6"
                fill="none" stroke="#0f172a" stroke-width="2.5" stroke-dasharray="7,4" />
          <line x1="840" y1="71" x2="840" y2="109"
                stroke="#ffffff" stroke-width="6" stroke-linecap="round" />
          <line x1="840" y1="71" x2="840" y2="109"
                stroke="#0f172a" stroke-width="2.8" stroke-linecap="round"
                marker-end="url(#mono-arrow)" />
          <g transform="translate(732, 56)">
            <rect x="0" y="-15" width="215" height="30" rx="15"
                  fill="#0f172a" stroke="#ffffff" stroke-width="2.5"
                  filter="url(#drop-shadow)" />
            <circle cx="15" cy="0" r="11" fill="#ffffff" />
            <text x="15" y="4.2" text-anchor="middle"
                  font-family="Pretendard, sans-serif" font-size="12" font-weight="900"
                  fill="#0f172a">2</text>
            <text x="32" y="4.2"
                  font-family="Pretendard, sans-serif" font-size="12" font-weight="700"
                  fill="#ffffff">실결제 4대 요약 지표</text>
          </g>

          <!-- 3. 업체 필터 및 대사용 CSV 추출 -->
          <rect x="442" y="260" width="934" height="92" rx="6"
                fill="rgba(15, 23, 42, 0.035)" stroke="#ffffff" stroke-width="5" />
          <rect x="442" y="260" width="934" height="92" rx="6"
                fill="none" stroke="#0f172a" stroke-width="2.5" stroke-dasharray="7,4" />
          <line x1="1290" y1="242" x2="1320" y2="260"
                stroke="#ffffff" stroke-width="6" stroke-linecap="round" />
          <line x1="1290" y1="242" x2="1320" y2="260"
                stroke="#0f172a" stroke-width="2.8" stroke-linecap="round"
                marker-end="url(#mono-arrow)" />
          <g transform="translate(1005, 242)">
            <rect x="0" y="-15" width="285" height="30" rx="15"
                  fill="#0f172a" stroke="#ffffff" stroke-width="2.5"
                  filter="url(#drop-shadow)" />
            <circle cx="15" cy="0" r="11" fill="#ffffff" />
            <text x="15" y="4.2" text-anchor="middle"
                  font-family="Pretendard, sans-serif" font-size="12" font-weight="900"
                  fill="#0f172a">3</text>
            <text x="32" y="4.2"
                  font-family="Pretendard, sans-serif" font-size="12" font-weight="700"
                  fill="#ffffff">업체 필터 및 대사용 CSV 추출</text>
          </g>

          <!-- 4. 건별 원금·결제총액·마진 원장 -->
          <rect x="286" y="365" width="1108" height="495" rx="6"
                fill="rgba(15, 23, 42, 0.035)" stroke="#ffffff" stroke-width="5" />
          <rect x="286" y="365" width="1108" height="495" rx="6"
                fill="none" stroke="#0f172a" stroke-width="2.5" stroke-dasharray="7,4" />
          <line x1="248" y1="765" x2="286" y2="765"
                stroke="#ffffff" stroke-width="6" stroke-linecap="round" />
          <line x1="248" y1="765" x2="286" y2="765"
                stroke="#0f172a" stroke-width="2.8" stroke-linecap="round"
                marker-end="url(#mono-arrow)" />
          <g transform="translate(10, 765)">
            <rect x="0" y="-15" width="238" height="30" rx="15"
                  fill="#0f172a" stroke="#ffffff" stroke-width="2.5"
                  filter="url(#drop-shadow)" />
            <circle cx="15" cy="0" r="11" fill="#ffffff" />
            <text x="15" y="4.2" text-anchor="middle"
                  font-family="Pretendard, sans-serif" font-size="12" font-weight="900"
                  fill="#0f172a">4</text>
            <text x="32" y="4.2"
                  font-family="Pretendard, sans-serif" font-size="12" font-weight="700"
                  fill="#ffffff">건별 원금·결제총액·마진 원장</text>
          </g>
        </svg>
      </div>
      <div class="screen-legend-wrap">
        <table class="mono-table">
          <thead>
            <tr>
              <th style="width:64px;text-align:center;">번호</th>
              <th style="width:210px;">화면 조작 항목</th>
              <th>운영팀 실무 처리 방법 및 정산 프로세스 상세</th>
              <th style="width:220px;">검증 기준 / 시스템 규칙</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="td-center"><span class="step-num-badge">1</span></td>
              <td class="td-bold">어드민 [부의금 결제 내역] 진입</td>
              <td>이음부고 관리자 좌측 사이드바 <strong>[결제 및 정산 &gt; 부의금 결제 내역]</strong> 메뉴를 클릭하여 전체 부의금 카드결제 승인·취소 원장 화면으로 진입합니다.</td>
              <td class="td-mono">권한: 마스터/운영·정산 관리자</td>
            </tr>
            <tr>
              <td class="td-center"><span class="step-num-badge">2</span></td>
              <td class="td-bold">총 주문·총 부의금·총 수수료·마진 확인</td>
              <td>상단 4개 요약 카드에서 <strong>① 총 주문 건수, ② 총 부의금(상주 송금 원금 합계), ③ 총 수수료(조문객 결제 수수료), ④ 데브늄 실질 마진</strong>을 즉시 파악합니다.</td>
              <td class="td-mono">실시간 승인·원금·마진 집계</td>
            </tr>
            <tr>
              <td class="td-center"><span class="step-num-badge">3</span></td>
              <td class="td-bold">제휴장례식장별 필터링 및 대사용 [내보내기] 다운로드</td>
              <td>검색창(구매자·연락처·입금자·부고번호)과 <strong>[전체 업체] / [전체 상태]</strong> 드롭다운으로 특정 장례식장이나 결제완료 건만 필터링한 뒤, 우측 <strong>[내보내기]</strong> 버튼을 눌러 일일 3자 대사(Reconciliation)용 엑셀/CSV 원본을 다운로드합니다.</td>
              <td class="td-mono">매일 오전 10:00 전일자 추출</td>
            </tr>
            <tr>
              <td class="td-center"><span class="step-num-badge">4</span></td>
              <td class="td-bold">개별 거래 원장 및 귀속 제휴처 확인</td>
              <td>테이블 각 행에서 <strong>부고/고인명, 귀속 제휴장례식장(시연 장례식장/자체몰 등), 입금자명(상주 통장 인자명), 부의금액(원금), 결제총액, 플랫폼 마진, 상태(결제완료/취소)</strong>를 건별로 대조합니다.</td>
              <td class="td-mono">상주 계좌 100% 원금 즉시 송금</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>"""

# Process cards[2]..cards[6] (formerly STEP 3..7 -> now STEP 2..6)
remaining_cards = []
for idx, c in enumerate(cards[2:], start=2):
    old_step = idx + 1
    c_new = c.replace(f"STEP {old_step}.", f"STEP {idx}.")
    # Standardize all 3.5% / 10% references to 3% / 8%
    c_new = c_new.replace("부의금(3.5%)·답례품(10%)", "부의금(3%)·답례품(8%)")
    c_new = c_new.replace("부의금 페이백 요율(기본 3.5%) 및 답례품 페이백 요율(기본 10.0%) 입력", "부의금 페이백 요율(기본 3.0%) 및 답례품 페이백 요율(기본 8.0%) 입력")
    c_new = c_new.replace("부의금 페이백 요율(표준 3.0% ~ 3.5%, VAT 포함)</strong>과 <strong>답례품 페이백 요율(표준 8.0% ~ 10.0%, VAT 포함)", "부의금 페이백 요율(표준 3.0%, VAT 포함)</strong>과 <strong>답례품 페이백 요율(표준 8.0%, VAT 포함)")
    c_new = c_new.replace("표준안 A(3.5%/10%) · B(3.0%/8%)", "표준 요율: 부의금 3% / 답례품 8%")
    c_new = c_new.replace("3.5% / 10%", "3% / 8%")
    c_new = c_new.replace("창(STEP 6)", "창(STEP 5)")
    c_new = c_new.replace("수수료율(10%)", "수수료율(8%)")
    c_new = c_new.replace("수수료율(3.5%)", "수수료율(3%)")
    c_new = c_new.replace("예상 정산금(3.5%)", "예상 정산금(3%)")
    c_new = c_new.replace("3.5% 정산금 `15,750원`", "3% 정산금")
    c_new = c_new.replace("부의금 결제액 × 3.5% 실시간 산출", "부의금 결제액 × 3% 실시간 산출")
    remaining_cards.append(c_new)

step_cards_final = (
    '      <h2 id="sec-ig-screens">3. 이음부고 어드민 &amp; 파트너센터 실화면 매뉴얼 (STEP 1 ~ STEP 6)</h2>\n'
    '      <p>우리 팀원이 사용하는 이음부고 마스터 어드민(STEP 1~4)과 장례식장·제휴 파트너가 사용하는 파트너센터(STEP 5~6)의 화면 번호별 기능 설명입니다.</p>\n\n'
    + step1_card
    + "\n\n"
    + "\n\n".join(remaining_cards)
)

# Additional CSS for Screen Guide Cards & Mobile/Partner UI/UX Showcase
extra_uiux_css = """
    /* Screen Guide Cards (Admin & Partner Center STEP 1~6) */
    .screen-guide-card {
      border: 1px solid #d8e2f0;
      border-radius: 12px;
      background: #ffffff;
      margin-bottom: 32px;
      overflow: hidden;
      box-shadow: 0 2px 10px rgba(15, 23, 42, 0.04);
    }
    .screen-guide-header {
      background: #f8fafc;
      padding: 18px 24px;
      border-bottom: 1px solid #e2e8f0;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
    }
    .screen-guide-eyebrow {
      font-size: 11.5px;
      font-weight: 800;
      color: #3566e0;
      letter-spacing: 0.05em;
      margin-bottom: 4px;
    }
    .screen-guide-title {
      font-size: 19px;
      font-weight: 800;
      color: #0f172a;
      margin: 2px 0 6px;
    }
    .screen-guide-sub {
      font-size: 14px;
      color: #475569;
      padding-bottom: 0;
      margin: 0;
      line-height: 1.5;
    }
    .screen-url-pill {
      background: #eff6ff;
      border: 1px solid #bfdbfe;
      color: #1d4ed8;
      padding: 6px 12px;
      border-radius: 6px;
      font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
      font-size: 12.5px;
      font-weight: 700;
      white-space: nowrap;
    }
    .screen-canvas-wrap {
      position: relative;
      width: 100%;
      background: #f1f5f9;
      border-bottom: 1px solid #e2e8f0;
      line-height: 0;
    }
    .screen-img {
      width: 100%;
      height: auto;
      display: block;
    }
    .screen-svg-overlay {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
    }
    .screen-legend-wrap table {
      width: 100%;
      border-collapse: collapse;
    }
    .screen-legend-wrap th {
      background: #f1f5f9;
      color: #334155;
      font-weight: 700;
      text-align: center;
      padding: 11px 12px;
      border-right: 1px solid #e2e8f0;
      border-bottom: 1px solid #e2e8f0;
      font-size: 13.5px;
    }
    .screen-legend-wrap td {
      padding: 11px 14px;
      border-right: 1px solid #e2e8f0;
      border-bottom: 1px solid #e2e8f0;
      font-size: 14px;
      color: #334155;
      line-height: 1.55;
    }
    .step-num-badge {
      display: inline-flex;
      width: 24px;
      height: 24px;
      border-radius: 50%;
      background: #0f172a;
      color: #ffffff;
      font-size: 12px;
      font-weight: 800;
      align-items: center;
      justify-content: center;
    }
    .td-center { text-align: center !important; }
    .td-bold { font-weight: 700 !important; color: #0f172a !important; }
    .td-mono { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 13px !important; color: #1d4ed8 !important; font-weight: 600; background: #f8fafc; }

    /* Mobile 4-Step Phone UI/UX Flow Grid */
    .uiux-flow-box {
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 12px;
      padding: 22px 24px;
      margin-bottom: 24px;
    }
    .uiux-flow-title {
      font-size: 17px;
      font-weight: 800;
      color: #0f172a;
      margin-bottom: 4px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .uiux-flow-sub {
      font-size: 13.5px;
      color: #64748b;
      margin-bottom: 16px;
    }
    .phone-flow-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
    }
    .phone-flow-item {
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 10px;
      padding: 12px;
      text-align: center;
    }
    .phone-frame-box {
      border: 3px solid #1e293b;
      border-radius: 14px;
      overflow: hidden;
      background: #ffffff;
      margin-bottom: 10px;
      aspect-ratio: 9 / 17.5;
      display: flex;
      align-items: flex-start;
      justify-content: center;
    }
    .phone-frame-box img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      object-position: top center;
      display: block;
    }
    .phone-step-title {
      font-size: 14px;
      font-weight: 800;
      color: #0f172a;
      margin-bottom: 3px;
    }
    .phone-step-desc {
      font-size: 12.5px;
      color: #64748b;
      line-height: 1.4;
    }
    .partner-screen-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 16px;
      margin-top: 12px;
      margin-bottom: 24px;
    }
    .partner-screen-card {
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 10px;
      overflow: hidden;
    }
    .partner-screen-img-wrap {
      background: #f1f5f9;
      border-bottom: 1px solid #e2e8f0;
      height: 210px;
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
    }
    .partner-screen-img-wrap img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      object-position: top center;
    }
    .partner-screen-body {
      padding: 14px 16px;
    }
    .partner-screen-body h4 {
      font-size: 15px;
      font-weight: 800;
      color: #0f172a;
      margin: 0 0 4px;
    }
    .partner-screen-body p {
      font-size: 13px;
      color: #475569;
      margin: 0;
      line-height: 1.5;
    }
    .stand-photo-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 16px;
      margin-top: 12px;
      margin-bottom: 24px;
    }
    .stand-photo-card {
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 10px;
      overflow: hidden;
    }
    .stand-photo-card img {
      width: 100%;
      height: 240px;
      object-fit: cover;
      display: block;
      border-bottom: 1px solid #e2e8f0;
    }
    .stand-photo-card .stand-cap {
      padding: 12px 16px;
      font-size: 14px;
      font-weight: 700;
      color: #1e293b;
    }
    .stand-photo-card .stand-cap span {
      display: block;
      font-size: 12.5px;
      font-weight: 500;
      color: #64748b;
      margin-top: 2px;
    }
    @media (max-width: 900px) {
      .phone-flow-grid { grid-template-columns: repeat(2, 1fr); }
      .partner-screen-grid { grid-template-columns: 1fr; }
      .stand-photo-grid { grid-template-columns: 1fr; }
    }
    @media (max-width: 640px) {
      .uiux-flow-box {
        padding: 16px 14px;
        margin-bottom: 18px;
      }
      .uiux-flow-title {
        font-size: 15px;
        line-height: 1.4;
      }
      .uiux-flow-sub {
        font-size: 12.5px;
        line-height: 1.45;
        margin-bottom: 12px;
      }
      .phone-flow-grid {
        grid-template-columns: repeat(2, 1fr);
        gap: 10px;
      }
      .phone-flow-item {
        padding: 8px;
      }
      .phone-frame-box {
        border-width: 2px;
        border-radius: 10px;
        margin-bottom: 8px;
      }
      .phone-step-title {
        font-size: 13px;
      }
      .phone-step-desc {
        font-size: 11.5px;
        line-height: 1.35;
      }
      .stand-photo-card img {
        height: 190px;
      }
      .stand-photo-card .stand-cap {
        padding: 10px 12px;
        font-size: 13px;
      }
      .partner-screen-img-wrap {
        height: 185px;
      }
      .partner-screen-body {
        padding: 12px 14px;
      }
      .partner-screen-body h4 {
        font-size: 14.5px;
      }
      .partner-screen-body p {
        font-size: 12.5px;
      }
      .screen-guide-card {
        margin-bottom: 22px;
      }
      .screen-guide-header {
        padding: 14px 16px;
        flex-direction: column;
        align-items: flex-start;
        gap: 8px;
      }
      .screen-guide-title {
        font-size: 16px;
        line-height: 1.35;
      }
      .screen-guide-sub {
        font-size: 13px;
        line-height: 1.45;
      }
      .screen-url-pill {
        font-size: 11px;
        padding: 5px 10px;
        max-width: 100%;
        box-sizing: border-box;
        white-space: normal;
        word-break: break-all;
      }
      .screen-legend-wrap {
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
      }
      .screen-legend-wrap table {
        min-width: 520px;
      }
      .screen-legend-wrap th,
      .screen-legend-wrap td {
        padding: 9px 10px;
        font-size: 12.5px;
      }
    }
"""

svg_defs_block = """
  <svg width="0" height="0" style="position:absolute;">
    <defs>
      <marker id="mono-arrow" viewBox="0 0 10 10" refX="8" refY="5"
              markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse">
        <path d="M 0 1 L 10 5 L 0 9 z" fill="#0f172a" stroke="#ffffff" stroke-width="0.8" />
      </marker>
      <filter id="drop-shadow" x="-10%" y="-10%" width="130%" height="130%">
        <feDropShadow dx="0" dy="2" stdDeviation="2.5" flood-color="#0f172a" flood-opacity="0.35" />
      </filter>
    </defs>
  </svg>
"""

uiux_mobile_flow_section = """
      <h2>3. 모바일 답례품 &amp; 부의금 카드결제 화면 흐름 (UI/UX)</h2>
      <p>상주와 조문객이 스마트폰에서 실제로 이용하는 <strong>모바일 답례품(4단계)</strong>과 <strong>부의금 카드결제(4단계)</strong> 화면 흐름 및 <strong>장례식장 로비 QR 비치물</strong> 예시입니다.</p>

      <div class="uiux-flow-box">
        <div class="uiux-flow-title">1) 모바일 답례품 서비스 흐름 (상주 대상 · 결제 금액의 8% 장례식장 정산)</div>
        <div class="uiux-flow-sub">발인 후 상주에게 감사 알림톡이 자동 발송되며, 상주가 답례품을 선택·결제하면 조문객에게 모바일 쿠폰으로 즉시 전송됩니다.</div>
        <div class="phone-flow-grid">
          <div class="phone-flow-item">
            <div class="phone-frame-box"><img src="guide-assets/m_skin_basic.png" alt="1. 모바일 부고장" /></div>
            <div class="phone-step-title">1. 모바일 부고장</div>
            <div class="phone-step-desc">고인 정보 및 장례 일정 안내</div>
          </div>
          <div class="phone-flow-item">
            <div class="phone-frame-box"><img src="guide-assets/m_gift_step2.png" alt="2. 감사 안내 알림톡" /></div>
            <div class="phone-step-title">2. 감사 안내 알림톡</div>
            <div class="phone-step-desc">발인 후 상주에게 자동 발송</div>
          </div>
          <div class="phone-flow-item">
            <div class="phone-frame-box"><img src="guide-assets/m_gift_step3.png" alt="3. 답례품 선택·결제" /></div>
            <div class="phone-step-title">3. 답례품 선택·결제</div>
            <div class="phone-step-desc">전용 답례품몰에서 간편 결제</div>
          </div>
          <div class="phone-flow-item">
            <div class="phone-frame-box"><img src="guide-assets/m_gift_step4.png" alt="4. 모바일 쿠폰 전달" /></div>
            <div class="phone-step-title">4. 모바일 쿠폰 전달</div>
            <div class="phone-step-desc">조문객에게 실시간 선물 전송</div>
          </div>
        </div>
      </div>

      <div class="uiux-flow-box">
        <div class="uiux-flow-title">2) 부의금 카드결제 서비스 흐름 (조문객 대상 · 결제 금액의 3% 장례식장 정산)</div>
        <div class="uiux-flow-sub">조문객이 부고장에서 신용카드·간편결제로 부의금을 결제하면 상주 계좌로 원금 100%가 실시간 입금됩니다.</div>
        <div class="phone-flow-grid">
          <div class="phone-flow-item">
            <div class="phone-frame-box"><img src="guide-assets/m_bui_step1.png" alt="1. 부고장 카드결제" /></div>
            <div class="phone-step-title">1. 부고장 카드결제</div>
            <div class="phone-step-desc">부고장 내 카드결제 버튼 터치</div>
          </div>
          <div class="phone-flow-item">
            <div class="phone-frame-box"><img src="guide-assets/m_bui_step2.png" alt="2. 정보 기입" /></div>
            <div class="phone-step-title">2. 정보 기입</div>
            <div class="phone-step-desc">조문객 성함·연락처 및 금액 선택</div>
          </div>
          <div class="phone-flow-item">
            <div class="phone-frame-box"><img src="guide-assets/m_bui_step3.png" alt="3. 결제하기" /></div>
            <div class="phone-step-title">3. 결제하기</div>
            <div class="phone-step-desc">상주 계좌 확인 후 카드 승인</div>
          </div>
          <div class="phone-flow-item">
            <div class="phone-frame-box"><img src="guide-assets/m_bui_step4.png" alt="4. 결제완료" /></div>
            <div class="phone-step-title">4. 결제완료</div>
            <div class="phone-step-desc">상주 계좌로 원금 100% 즉시 입금</div>
          </div>
        </div>
      </div>

      <div class="stand-photo-grid">
        <div class="stand-photo-card">
          <img src="guide-assets/desk_qr_stand.jpg" alt="데스크 QR 아크릴 스탠드" />
          <div class="stand-cap">
            현장 비치물 ① — 데스크 QR 스탠드 (무상 제공)
            <span>상담 데스크·접수처에 비치하여 상주가 스캔 즉시 장례식장 전용 부고장을 개설합니다.</span>
          </div>
        </div>
        <div class="stand-photo-card">
          <img src="guide-assets/desk_xbanner.jpg" alt="데스크 옆 X배너" />
          <div class="stand-cap">
            현장 비치물 ② — 로비 안내 배너 &amp; A4 포스터 (무상 제공)
            <span>무빈소·가족장 및 일반 빈소 상주에게 모바일 부고장 무료 개설을 안내합니다.</span>
          </div>
        </div>
      </div>
"""

partner_admin_3screens_html = """
      <h2>2. 장례식장 전용 파트너 관리자 3대 핵심 화면 (UI/UX)</h2>
      <p>제휴 장례식장에 발급해 드리는 <strong>파트너 관리자(<code>https://iumbugo.com/partner/login</code>)</strong>의 주요 화면입니다.</p>

      <div class="partner-screen-grid">
        <div class="partner-screen-card">
          <div class="partner-screen-img-wrap">
            <img src="guide-assets/p_dashboard_opt.png" alt="파트너 관리자 대시보드" />
          </div>
          <div class="partner-screen-body">
            <h4>① 실시간 정산 대시보드</h4>
            <p>QR 스캔 수, 부고장 등록 건수, 부의금 카드결제(3%) 및 모바일 답례품(8%) 실시간 예상 정산금을 한눈에 확인합니다.</p>
          </div>
        </div>
        <div class="partner-screen-card">
          <div class="partner-screen-img-wrap">
            <img src="guide-assets/p_sendlink_crop.png" alt="상주 부고장 링크 문자 발송" />
          </div>
          <div class="partner-screen-body">
            <h4>② 상주 부고장 작성 링크 문자 발송</h4>
            <p>전화·방문 상담 시 상주님 성함과 연락처만 입력하면 장례식장 정보가 자동 세팅된 부고장 작성 링크가 즉시 문자로 발송됩니다.</p>
          </div>
        </div>
        <div class="partner-screen-card">
          <div class="partner-screen-img-wrap">
            <img src="guide-assets/p_poster_crop.png" style="object-fit:contain; padding:8px;" alt="전용 QR 포스터 인쇄" />
          </div>
          <div class="partner-screen-body">
            <h4>③ 장례식장 전용 QR 포스터 인쇄</h4>
            <p>장례식장 고유 QR 코드가 삽입된 A4 안내 포스터를 언제든 바로 인쇄하거나 이미지로 다운로드하여 비치할 수 있습니다.</p>
          </div>
        </div>
      </div>
"""

# ==============================================================================
# 1. BUILD INTERNAL GUIDE: eiumbugo.html
# ==============================================================================
eiumbugo_internal_html = (
    base_head_css.replace(
        "<title>부카결 | 내부운영가이드</title>",
        '<title>이음부고 | 내부운영가이드</title>\n  <link rel="icon" type="image/png" href="guide-assets/eiumbugo-icon.png" />'
    )
    + extra_uiux_css
    + """
  </style>
<meta name="robots" content="noindex,nofollow"></head>
<body>
"""
    + svg_defs_block
    + """
  <div id="pw-gate" style="position:fixed;inset:0;z-index:99999;background:#f8fafc;display:flex;align-items:center;justify-content:center;">
    <form onsubmit="return checkPw(event)" style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:32px 28px;text-align:center;width:300px;">
      <img src="guide-assets/eiumbugo-logo.png" alt="이음부고" style="height:30px;width:auto;margin:0 auto 12px;display:block;" />
      <div style="font-size:18px;font-weight:700;margin-bottom:6px;">이음부고 | 내부운영가이드</div>
      <div style="font-size:13px;color:#64748b;margin-bottom:16px;">비밀번호를 입력하세요</div>
      <input id="pw-input" type="password" inputmode="numeric" autocomplete="off" style="width:100%;padding:10px;border:1px solid #cbd5e1;border-radius:8px;font-size:16px;text-align:center;box-sizing:border-box;" autofocus/>
      <div id="pw-err" style="color:#dc2626;font-size:12px;height:16px;margin:6px 0;"></div>
      <button type="submit" style="width:100%;padding:10px;background:#3566e0;color:#fff;border:0;border-radius:8px;font-weight:700;cursor:pointer;">확인</button>
    </form>
  </div>
  <script>
    (function(){ if (sessionStorage.getItem('buipay_ok')==='1') { var g=document.getElementById('pw-gate'); if(g) g.style.display='none'; } })();
    function checkPw(e){ e.preventDefault(); if(document.getElementById('pw-input').value==='112233'){ sessionStorage.setItem('buipay_ok','1'); document.getElementById('pw-gate').style.display='none'; } else { document.getElementById('pw-err').textContent='비밀번호가 올바르지 않습니다.'; } return false; }
  </script>

  <!-- ========================================================================
        TOP GNB HEADER (#header-outer)
        ======================================================================== -->
  <div id="header-outer">
    <header id="top">
      <a class="logo-wrap" onclick="showPage('pdfs')">
        <img src="guide-assets/eiumbugo-logo.png" alt="이음부고" style="height:28px; width:auto; display:block;" />
        <div class="logo-sub">내부운영가이드</div>
      </a>

      <nav>
        <ul class="sf-menu">
          <li id="nav-pdfs" class="current-menu-ancestor">
            <a onclick="showPage('pdfs')"><span class="menu-title-text">1. 표준계약서</span></a>
          </li>
          <li id="nav-client">
            <a onclick="showPage('client-guide')"><span class="menu-title-text">2. 고객사 가이드</span></a>
          </li>
          <li id="nav-internal">
            <a onclick="showPage('internal-guide')"><span class="menu-title-text">3. 내부 운영 가이드 (UI/UX)</span></a>
          </li>
          <li id="nav-step">
            <a onclick="showPage('step-guide')"><span class="menu-title-text">4. 업체별 지침 (Step 1~6)</span></a>
          </li>
          <li id="nav-checklist">
            <a onclick="showPage('checklist')"><span class="menu-title-text">5. 업체별 체크리스트</span></a>
          </li>
          <li id="nav-cs">
            <a onclick="showPage('cs-guide')"><span class="menu-title-text">6. 운영 가이드</span></a>
          </li>
        </ul>
      </nav>

      <div class="header-right-tools">
        <a class="btn-header-outline" href="eiumbugo-partner.html" target="_blank" style="background:#3566e0; color:#ffffff; border-color:#3566e0; font-weight:700; text-decoration:none;">고객사용 가이드 열기</a>
      </div>
    </header>
  </div>

  <!-- ========================================================================
        PAGE HEADER BANNER (#page-header-bg)
        ======================================================================== -->
  <div id="page-header-bg">
    <div class="container">
      <h1 id="banner-title">① 표준계약서</h1>
      <span class="subheader" id="banner-sub">장례식장·제휴사에 전달하는 필수 자료 4종(표준계약서 · 파트너 리플렛 v.5 · 상주 부고장 시연 · 파트너 관리자 시연) 및 고객사 전달용 공식 URL입니다.</span>
    </div>
  </div>

  <!-- Quick 1-Click Navigation Bar -->
  <div class="quick-subnav-bar">
    <div class="quick-subnav-inner">
      <button class="quick-pill active" data-pill="pdfs" onclick="showPage('pdfs')">① 표준계약서</button>
      <button class="quick-pill" data-pill="client-guide" onclick="showPage('client-guide')">② 고객사 운영 가이드</button>
      <button class="quick-pill" data-pill="internal-guide" onclick="showPage('internal-guide')">③ 내부 운영 가이드 (UI/UX)</button>
      <button class="quick-pill" data-pill="step-guide" onclick="showPage('step-guide')">④ 업체별 지침 (Step 1~6)</button>
      <button class="quick-pill" data-pill="checklist" onclick="showPage('checklist')">⑤ 업체별 체크리스트</button>
      <button class="quick-pill" data-pill="cs-guide" onclick="showPage('cs-guide')">⑥ 운영 가이드</button>
    </div>
  </div>

  <main class="main-content">

    <!-- ====================================================================
          ① 표준계약서 (#pdfs)
          ==================================================================== -->
    <section id="page-pdfs" class="guide-page active">

      <!-- 고객사 전달용 외부 URL 분리 안내 배너 -->
      <div class="ext-url-banner">
        <div class="ext-url-banner-left">
          <span class="ext-url-badge">공식 분리 운영 · 외부 전달 전용</span>
          <div class="ext-url-title">장례식장(제휴사) 원장님·팀장님 전달용 공식 웹 가이드 URL</div>
          <p class="ext-url-desc">
            내부 전용 탭(마스터 어드민 UI/UX 매뉴얼 · 업체별 지침 · 업체별 체크리스트 메모장)을 모두 제외하고,
            <strong>① 도입 절차 &amp; 수익 자동 계산기 + ② 표준계약서 &amp; 리플렛 + ③ 운영 가이드</strong>만 담은 장례식장 전달용 전용 페이지입니다.
          </p>
        </div>
        <div class="ext-url-actions">
          <a class="btn-pdf-download" href="eiumbugo-partner.html" target="_blank">고객사용 페이지 새창 열기</a>
        </div>
      </div>

      <h2 style="margin-top:0;">표준계약서 및 필수 자료 4종 (표준계약서 · 파트너 리플렛 · 부고장 시연 · 파트너 관리자 시연)</h2>
      <p>장례식장 제휴 진행 시 전달해야 하는 자료는 아래 <strong>4가지</strong>이며, 계약 체결 시 장례식장으로부터 <strong>사업자등록증 사본 + 장례식장 통장사본(정산용)</strong>을 수취합니다.</p>

      <div class="pdf-grid" style="margin-bottom:28px;">
        <!-- 1. 표준계약서 -->
        <div class="pdf-card">
          <div class="pdf-card-info">
            <span class="pdf-tag" style="background:#e8effe; color:#2451c8; font-weight:700;">1. 표준계약서</span>
            <div class="pdf-title">1) 이음부고 장례식장 제휴 표준계약서</div>
            <div class="pdf-desc">
              제휴 장례식장 날인용 표준계약서(답례품 8% · 부의금 3% 정산 기준)입니다. 계약 시 <strong>장례식장 사업자등록증 사본 1부 + 통장사본(정산용) 1부</strong>를 전달받습니다.
            </div>
          </div>
          <div class="pdf-card-actions">
            <span class="btn-pdf-download" style="opacity:0.65; cursor:default;">PDF 다운로드 (추가 법률자문 진행 중)</span>
          </div>
        </div>

        <!-- 2. 이음부고 장례식장 파트너 가이드 v.5 -->
        <div class="pdf-card">
          <div class="pdf-card-info">
            <span class="pdf-tag" style="background:#e8effe; color:#2451c8; font-weight:700;">2. 파트너 가이드 (v.5)</span>
            <div class="pdf-title">2) 이음부고 장례식장 파트너 가이드 v.5</div>
            <div class="pdf-desc">무빈소·가족장 및 일반 장례 부가수익 모델(모바일 답례품·부의금 카드결제), 현장 QR 비치, 파트너 관리자 기능을 정리한 공식 브로슈어(v.5) 원본 PDF입니다.</div>
          </div>
          <div class="pdf-card-actions">
            <a class="btn-pdf-download" href="eiumbugo_partner_guide_v5.pdf" download="이음부고 장례식장 파트너 가이드 v.5.pdf">PDF 다운로드</a>
            <a class="btn-pdf-view" href="eiumbugo_partner_guide_v5.pdf" target="_blank">새창 열람</a>
          </div>
        </div>

        <!-- 3. 상주용 모바일 부고장 작성 체험 -->
        <div class="pdf-card">
          <div class="pdf-card-info">
            <span class="pdf-tag" style="background:#e8effe; color:#2451c8; font-weight:700;">3. 모바일 부고장 시연</span>
            <div class="pdf-title">3) 상주용 모바일 부고장 개설 실시간 시연</div>
            <div class="pdf-desc">상주가 로비 QR 스캔 또는 문자 링크를 통해 접속했을 때 장례식장 정보가 자동 입력되는 <strong>모바일 부고장 개설 시연 페이지</strong>입니다.</div>
          </div>
          <div class="pdf-card-actions">
            <a class="btn-pdf-view" href="https://demo.iumbugo.com/create/basic" target="_blank">새창 열람</a>
          </div>
        </div>

        <!-- 4. 장례식장 파트너 관리자 실시간 체험 -->
        <div class="pdf-card">
          <div class="pdf-card-info">
            <span class="pdf-tag" style="background:#e8effe; color:#2451c8; font-weight:700;">4. 파트너 관리자 시연</span>
            <div class="pdf-title">4) 장례식장 전용 파트너 관리자 센터</div>
            <div class="pdf-desc">장례식장 담당자가 실시간 부고 현황, 답례품·부의금 예상 정산금, 상주 링크 문자 발송, QR 포스터 인쇄를 이용하는 <strong>파트너 관리자 로그인 페이지</strong>입니다.</div>
          </div>
          <div class="pdf-card-actions">
            <a class="btn-pdf-view" href="https://iumbugo.com/partner/login" target="_blank">새창 열람</a>
          </div>
        </div>
      </div>

      <div class="page-Turn-nav">
        <span></span>
        <button class="page-turn-btn" onclick="showPage('client-guide')">다음: ② 고객사 운영 가이드 →</button>
      </div>
    </section>

    <!-- ====================================================================
          ② 고객사 운영 가이드 (#client-guide)
          ==================================================================== -->
    <section id="page-client-guide" class="guide-page">
      <h2 style="margin-top:0;">1. 고객사(장례식장)가 알아야 할 핵심 운영 기준</h2>
      <p>장례식장은 <strong>초기 비용이나 예치금 부담 없이 데스크에 QR만 비치</strong>하면 모든 부고·답례품·부의금 정산이 자동으로 이루어집니다.</p>

      <div class="table_wrap">
        <table class="my_table">
          <thead>
            <tr>
              <th style="width:24%;">항목</th>
              <th style="width:30%;" class="bg_y">핵심 기준</th>
              <th>고객사(장례식장) 안내 내용</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="ta_c"><strong>도입비 · 월 관리비 ·<br/>모바일 부고장 이용료</strong></td>
              <td class="ta_c bg_y"><strong>전액 무료 (0원)</strong><br/>(QR 스탠드·포스터 무상 제공)</td>
              <td>모바일 부고장 개설·알림톡 발송·파트너 관리자 이용료는 <strong>전액 무료</strong>이며, 로비 비치용 아크릴 QR 스탠드와 안내 포스터를 무상 지원합니다.</td>
            </tr>
            <tr>
              <td class="ta_c"><strong>모바일 답례품<br/>장례식장 제휴 수익</strong></td>
              <td class="ta_c bg_y"><strong>결제 금액의 8% 지급</strong></td>
              <td>발인 후 상주에게 감사 알림톡이 자동 발송되며, 상주가 조문객에게 모바일 답례품을 결제·발송할 때마다 <strong>결제 금액의 8%가 장례식장 제휴 수익</strong>으로 적립됩니다.</td>
            </tr>
            <tr>
              <td class="ta_c"><strong>부의금 카드결제<br/>장례식장 제휴 수익</strong></td>
              <td class="ta_c bg_y"><strong>결제 금액의 3% 지급</strong><br/>(상주에게 원금 100% 실시간 입금)</td>
              <td>조문객이 부고장에서 신용카드·간편결제로 부의금을 결제하면 <strong>상주 계좌로 원금 100%가 즉시 입금</strong>되고, <strong>부의금 원금의 3%가 장례식장 제휴 수익</strong>으로 적립됩니다. (결제 수수료 8.8%는 조문객 부담)</td>
            </tr>
            <tr>
              <td class="ta_c"><strong>예치금 부담 여부</strong></td>
              <td class="ta_c bg_y"><strong>예치금 없음 (0원)</strong></td>
              <td>이음부고 모바일 부고장을 직접 도입하는 장례식장은 데브늄 본사 송금 풀(Pool)을 사용하므로 <strong>장례식장이 별도 예치금을 납부할 필요가 전혀 없습니다.</strong></td>
            </tr>
            <tr>
              <td class="ta_c"><strong>제휴 수익 정산 지급일</strong></td>
              <td class="ta_c bg_y"><strong>매월 말일 마감 → 익월 15일 지급</strong></td>
              <td>매월 1일~말일까지 발생한 답례품(8%) 및 부의금 카드결제(3%) 제휴 수익을 합산하여 <strong>익월 15일(주말·공휴일 시 익영업일)</strong>에 장례식장 지정 계좌로 입금합니다.</td>
            </tr>
            <tr>
              <td class="ta_c"><strong>계약 시 구비서류</strong></td>
              <td class="ta_c bg_y"><strong>제휴 계약서 +<br/>사업자등록증 · 통장사본 수취</strong></td>
              <td>제휴 계약 체결 시 장례식장으로부터 <strong>① 사업자등록증 사본 1부 + ② 정산 입금용 통장사본 1부</strong>를 전달받습니다.</td>
            </tr>
          </tbody>
        </table>
      </div>

      <h2>2. 장례식장 월 장례 건수 기반 — 예상 제휴 수익 자동 계산기</h2>
      <p>장례식장의 <strong>월 평균 장례(부고장 발행) 건수</strong>를 입력하면 <strong>모바일 답례품(8%)</strong>과 <strong>부의금 카드결제(3%)</strong>로 발생하는 월 예상 정산 수익과 연간 추가 수익이 즉시 산출됩니다.</p>

      <div class="calc-box">
        <div class="calc-top-row">
          <div class="calc-input-group">
            <label class="calc-label" for="calc-bugo-count">월 평균 장례(부고장 발행) 건수 입력 (건/월)</label>
            <div class="calc-input-wrap">
              <input type="number" id="calc-bugo-count" class="calc-num-input" value="100" min="10" step="10" oninput="updateRevenueCalc()" />
              <span style="font-size:16px; font-weight:700; color:#334155;">건 / 월</span>
              <select id="calc-per-bugo" class="partner-input" style="max-width:270px; font-weight:700;" onchange="updateRevenueCalc()">
                <option value="60000" selected>부고 1건당 평균 60,000원 (표준)</option>
                <option value="55000">부고 1건당 평균 55,000원 (보수적)</option>
              </select>
            </div>
            <div class="calc-preset-bar">
              <button type="button" class="calc-preset-btn" onclick="setBugoPreset(30)">월 30건</button>
              <button type="button" class="calc-preset-btn" onclick="setBugoPreset(50)">월 50건</button>
              <button type="button" class="calc-preset-btn active" onclick="setBugoPreset(100)">월 100건</button>
              <button type="button" class="calc-preset-btn" onclick="setBugoPreset(200)">월 200건</button>
              <button type="button" class="calc-preset-btn" onclick="setBugoPreset(300)">월 300건</button>
              <button type="button" class="calc-preset-btn" onclick="setBugoPreset(500)">월 500건</button>
            </div>
          </div>
          <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:10px; padding:12px 16px; font-size:13px; color:#475569; max-width:360px;">
            <strong style="color:#1e293b; display:block; margin-bottom:4px;">수익 산출 기준 (답례품 8% + 부의금 3%)</strong>
            · <strong>모바일 답례품</strong>: 부고 1건당 평균 5.5만~6만 원 × <strong>장례식장 수수료 8%</strong><br/>
            · <strong>부의금 카드결제</strong>: 부고 1건당 평균 5.5만~6만 원 × <strong>장례식장 수수료 3%</strong>
          </div>
        </div>

        <div class="calc-result-grid">
          <div class="calc-stat-card highlight">
            <div class="calc-stat-title">예상 월 제휴 정산 수익 (합계)</div>
            <div class="calc-stat-val" id="calc-res-total">66만 원 / 월</div>
            <div class="calc-stat-sub" id="calc-res-yearly">연 환산 약 792만 원 추가 수익</div>
          </div>
          <div class="calc-stat-card">
            <div class="calc-stat-title">모바일 답례품 수익 (8% 기준)</div>
            <div class="calc-stat-val" id="calc-res-gift">48만 원</div>
            <div class="calc-stat-sub" id="calc-res-gift-sub">월 100건 × 평균 6만 원 × 8%</div>
          </div>
          <div class="calc-stat-card">
            <div class="calc-stat-title">부의금 카드결제 수익 (3% 기준)</div>
            <div class="calc-stat-val" id="calc-res-condol">18만 원</div>
            <div class="calc-stat-sub" id="calc-res-condol-sub">월 100건 × 평균 6만 원 × 3%</div>
          </div>
        </div>
      </div>
"""
    + uiux_mobile_flow_section
    + """
      <div class="page-Turn-nav">
        <button class="page-turn-btn" onclick="showPage('pdfs')">← 이전: ① 표준계약서</button>
        <button class="page-turn-btn" onclick="showPage('internal-guide')">다음: ③ 내부 운영 가이드 (UI/UX) →</button>
      </div>
    </section>

    <!-- ====================================================================
          ③ 내부 운영 가이드 (UI/UX 매뉴얼) (#internal-guide)
          ==================================================================== -->
    <section id="page-internal-guide" class="guide-page">
      <h2 style="margin-top:0;">1. 우리 팀 내부 운영 기준</h2>
      <p>이음부고 제휴 장례식장·상조사를 세팅하고 운영할 때 우리 팀 내부에서 적용하는 기준입니다.</p>

      <div class="table_wrap">
        <table class="my_table">
          <thead>
            <tr>
              <th style="width:24%;">내부 관리 항목</th>
              <th style="width:30%;" class="bg_y">운영 기준</th>
              <th>실무 처리 방식</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="ta_c"><strong>장례식장 전용 URL<br/>(서브도메인 자동 귀속)</strong></td>
              <td class="ta_c bg_y"><strong><code>https://{파트너코드}.iumbugo.com/create/basic</code></strong></td>
              <td>어드민에서 파트너 코드(예: <code>sahaguminfh</code>)를 등록하면 전용 부고 개설 URL이 즉시 활성화되며, 해당 URL로 개설된 모든 부고의 <strong>답례품·부의금 실적이 해당 장례식장으로 자동 귀속</strong>됩니다.</td>
            </tr>
            <tr>
              <td class="ta_c"><strong>장례식장 기본 정보 고정</strong></td>
              <td class="ta_c bg_y"><strong>장례식장명 · 주소 · 대표번호<br/>오타 없이 정확히 등록</strong></td>
              <td>전용 URL 접속 시 상주 화면에 장례식장명·주소·대표번호가 자동 입력되므로, 어드민 파트너 등록 시 <strong>도로명 주소와 지역번호 포함 대표번호</strong>를 반드시 검수합니다.</td>
            </tr>
            <tr>
              <td class="ta_c"><strong>기본 정산 요율 세팅</strong></td>
              <td class="ta_c bg_y"><strong>답례품 <code>8.0%</code><br/>부의금 카드결제 <code>3.0%</code></strong></td>
              <td>별도 특약이 없는 한 장례식장 표준 요율은 <strong>답례품 8.0% / 부의금 3%</strong>로 어드민에 세팅합니다. (개인 장례지도사 등 별도 협의 시 어드민에서 개별 요율 조정 가능)</td>
            </tr>
            <tr>
              <td class="ta_c"><strong>부의금 송금 재원 구분<br/>(자체 부고장 vs 외부 앱 연동)</strong></td>
              <td class="ta_c bg_y"><strong>이음부고 직접 사용 : 본사 풀(Pool)<br/>외부 부고장 앱 연동 : 업체 예치금</strong></td>
              <td>
                · <strong>이음부고 부고장을 그대로 쓰는 장례식장</strong>: 데브늄 본사(<code>MD2</code>) 예치금 풀에서 송금되므로 장례식장에 예치금을 요구하지 않습니다.<br/>
                · <strong>자체 부고장 앱에 부카결만 연동하는 업체</strong>: <a href="buipay.html" style="color:#2451c8; font-weight:700;">부카결 내부운영가이드</a> 기준에 따라 15일분 예치금을 수취합니다.
              </td>
            </tr>
            <tr>
              <td class="ta_c"><strong>파트너 관리자 계정 발급</strong></td>
              <td class="ta_c bg_y"><strong><code>https://iumbugo.com/partner/login</code></strong></td>
              <td>장례식장 담당자(원장/팀장)가 직접 <strong>상주 부고장 링크 문자 발송, QR 포스터 인쇄, 실시간 부고·결제·정산금 조회</strong>를 할 수 있도록 파트너 계정을 발급해 전달합니다.</td>
            </tr>
            <tr>
              <td class="ta_c"><strong>월간 정산 및 명세서 발행</strong></td>
              <td class="ta_c bg_y"><strong>매월 말일 마감 → 익월 15일 지급</strong><br/>(법인 세금계산서 / 개인 3.3% 원천징수)</td>
              <td>어드민 <code>[통합 정산 관리]</code>에서 파트너별 답례품·부의금 정산액을 확정하고 공식 정산 명세서(PDF)를 발행한 뒤 <strong>익월 15일</strong>에 지급합니다.</td>
            </tr>
          </tbody>
        </table>
      </div>
"""
    + partner_admin_3screens_html
    + "\n"
    + step_cards_final
    + """
      <div class="page-Turn-nav">
        <button class="page-turn-btn" onclick="showPage('client-guide')">← 이전: ② 고객사 운영 가이드</button>
        <button class="page-turn-btn" onclick="showPage('step-guide')">다음: ④ 업체별 지침 (Step 1~6) →</button>
      </div>
    </section>

    <!-- ====================================================================
          ④ 업체별 지침 가이드 (Step 1~6) (#step-guide)
          ==================================================================== -->
    <section id="page-step-guide" class="guide-page">
      <h2 style="margin-top:0;">1. 신규 장례식장 유입 시 Step 1 ~ Step 6 진행 지침</h2>
      <p>새로운 제휴 장례식장(또는 상조사)이 유입되었을 때 우리 팀이 <strong>Step 1부터 Step 6까지 순서대로 해야 할 일</strong>입니다.</p>

      <div class="table_wrap">
        <table class="my_table">
          <thead>
            <tr>
              <th style="width:12%;">단계</th>
              <th style="width:22%;">단계명</th>
              <th style="width:42%;" class="bg_y">우리가 해야 할 일</th>
              <th style="width:24%;">전달 자료 / 구비서류</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="ta_c"><strong>STEP 1</strong></td>
              <td><strong>제휴 계약 체결 &amp;<br/>구비서류 2종 · 기본정보 수취</strong></td>
              <td class="bg_y">제휴 계약서를 작성·날인하고, 장례식장으로부터 <strong>① 사업자등록증 사본 + ② 정산용 통장사본 + ③ 장례식장 기본정보(정식 명칭, 도로명 주소, 대표번호, 담당자 연락처)</strong>를 수취합니다.</td>
              <td>계약서 날인<br/><strong>사업자등록증 + 통장사본 수취</strong></td>
            </tr>
            <tr>
              <td class="ta_c"><strong>STEP 2</strong></td>
              <td><strong>어드민 파트너 등록 &amp;<br/>수수료 요율(8% / 3%) 세팅</strong></td>
              <td class="bg_y">마스터 어드민(<code>/admin/partners</code>)에서 <strong>파트너 코드(영문 소문자, 예: <code>sahaguminfh</code>)</strong>를 부여하고, 장례식장 주소·대표번호 및 <strong>답례품 8.0% / 부의금 3%</strong> 요율을 세팅합니다.</td>
              <td>어드민 파트너 생성</td>
            </tr>
            <tr>
              <td class="ta_c"><strong>STEP 3</strong></td>
              <td><strong>전용 부고 개설 URL 검수 &amp;<br/>QR 스탠드 · 포스터 제작</strong></td>
              <td class="bg_y">생성된 전용 URL(<code>https://{코드}.iumbugo.com/create/basic</code>)에 접속하여 <strong>장례식장명·주소·대표번호가 오타 없이 자동 채워지는지 확인</strong>하고, 전용 QR 포스터·아크릴 스탠드를 준비합니다.</td>
              <td>전용 URL 검수 · QR 제작</td>
            </tr>
            <tr>
              <td class="ta_c"><strong>STEP 4</strong></td>
              <td><strong>파트너 관리자 계정 발급 &amp;<br/>문자 발송 테스트</strong></td>
              <td class="bg_y">장례식장 전용 파트너 센터(<code>/partner/login</code>) 로그인 계정을 발급하고, 대시보드 조회 및 상주 부고장 링크 문자 발송 기능이 정상 작동하는지 확인합니다.</td>
              <td>파트너 센터 계정 발급</td>
            </tr>
            <tr>
              <td class="ta_c"><strong>STEP 5</strong></td>
              <td><strong>담당자 온보딩 안내 발송 &amp;<br/>로비 QR 비치 오픈</strong></td>
              <td class="bg_y">장례식장 담당자(팀장/원장님)에게 <strong>전용 부고장 개설 URL + 파트너 관리자 계정 + 고객사용 가이드 URL(<code>/eiumbugo-partner.html</code>)</strong>을 카톡/문자로 전달하고 현장 운영을 시작합니다.</td>
              <td>온보딩 완료 카톡 발송<br/>정식 오픈</td>
            </tr>
            <tr>
              <td class="ta_c"><strong>STEP 6</strong></td>
              <td><strong>월간 정산 확정 &amp;<br/>익월 15일 정산금 지급</strong></td>
              <td class="bg_y">매월 말일 마감 후 어드민(<code>/admin/settlements</code>)에서 답례품(8%) + 부의금(3%) 정산 내역을 확정하고 정산 명세서를 발행하여 <strong>익월 15일</strong>에 지급합니다.</td>
              <td>매월 15일 정기 정산</td>
            </tr>
          </tbody>
        </table>
      </div>

      <h2>2. 장례식장 담당자 전달용 온보딩 카톡/문자 템플릿 (복사용)</h2>
      <div class="grid-2-tables">
        <div class="code-block-pro" style="margin:0;">
          <div class="code-block-header">
            <span>① [세팅 전] 구비서류 및 기본 정보 요청 문구</span>
            <button class="code-copy-btn" onclick="copyCode(this)">복사</button>
          </div>
          <pre style="white-space:pre-wrap; word-break:keep-all;">안녕하세요, [장례식장명] [담당자 성함/직함]님.
이음부고(데브늄) 백승훈 차장입니다.

모바일 부고장 및 부의금 카드결제·답례품 제휴 세팅을 위해 아래 서류와 기본 정보를 전달 부탁드립니다.

1. 구비서류 (정산 계좌 등록용)
 - 사업자등록증 사본 1부
 - 정산금 입금용 통장사본 1부
 - 세금계산서 수신 이메일 주소

2. 장례식장 기본 정보 확인
 - 장례식장 표기명 : [장례식장명]
 - 도로명 주소 : [주소]
 - 대표 전화번호 : [대표번호]

전달해 주시는 대로 장례식장 전용 부고장 개설 링크(QR)와 파트너 관리자 계정을 바로 발급해 안내드리겠습니다. 감사합니다.</pre>
        </div>

        <div class="code-block-pro" style="margin:0;">
          <div class="code-block-header">
            <span>② [세팅 완료 후] 전용 URL · 파트너 관리자 전달 문구</span>
            <button class="code-copy-btn" onclick="copyCode(this)">복사</button>
          </div>
          <pre style="white-space:pre-wrap; word-break:keep-all;">안녕하세요, [장례식장명] [담당자 성함/직함]님.
이음부고(데브늄) 백승훈 차장입니다.

[장례식장명] 전용 모바일 부고장 개설 링크 및 파트너 관리자 세팅이 완료되어 안내드립니다.

■ 1. [장례식장명] 전용 모바일 부고장 개설 URL
▶ https://[파트너코드].iumbugo.com/create/basic
※ 위 링크(또는 전용 QR)로 상주님이 접속하시면 장례식장명·주소·대표번호가 자동으로 입력되어 바로 부고장을 만드실 수 있습니다.

■ 2. 장례식장 전용 파트너 관리자
▶ 접속 주소 : https://iumbugo.com/partner/login
▶ 주요 기능 : 상주 부고장 링크 문자 발송 / 부고·결제·정산 실시간 조회 / 전용 QR 포스터 인쇄

■ 3. 이음부고 운영 가이드 및 브로슈어
▶ https://devnium-guide.vercel.app/eiumbugo-partner.html

궁금하신 점은 언제든 편하게 연락 부탁드립니다. 감사합니다!</pre>
        </div>
      </div>

      <div class="page-Turn-nav">
        <button class="page-turn-btn" onclick="showPage('internal-guide')">← 이전: ③ 내부 운영 가이드 (UI/UX)</button>
        <button class="page-turn-btn" onclick="showPage('checklist')">다음: ⑤ 업체별 체크리스트 →</button>
      </div>
    </section>

    <!-- ====================================================================
          ⑤ 업체별 & 내부 체크리스트 (#checklist)
          ==================================================================== -->
    <section id="page-checklist" class="guide-page">
      <h2 style="margin-top:0;">1. 제휴 장례식장별 온보딩 체크리스트 (업체 클릭)</h2>
      <p>아래 <strong>장례식장(업체)을 클릭</strong>하면 전용 부고장 URL, 정산 요율 조건, 그리고 <strong>Step 1~6 온보딩 체크리스트(6개 항목)</strong>가 바로 나옵니다.</p>

      <!-- 업체 선택 버튼 바 -->
      <div class="partner-pill-bar">
        <div id="partner-pills-chk" style="display:flex; flex-wrap:wrap; gap:8px; flex:1;"></div>
        <div style="display:flex; gap:8px; flex-shrink:0;">
          <button class="btn-header-outline" style="background:#3566e0; color:#ffffff; border-color:#3566e0; font-weight:700;" onclick="toggleAddPartnerForm()">+ 장례식장 추가</button>
          <button class="btn-header-outline" onclick="resetPartnerDataToDefault()">기본값 복원</button>
        </div>
      </div>

      <!-- 간단한 업체 추가 폼 (평소 숨김) -->
      <div id="add-partner-form-box" style="display:none; background:#f8fafc; border:2px solid #3566e0; border-radius:10px; padding:18px 20px; margin-bottom:20px;">
        <div style="display:flex; gap:10px; flex-wrap:wrap; align-items:center;">
          <input type="text" id="new-p-name" class="partner-input" placeholder="장례식장명 (예: 사하구민장례식장)" style="max-width:200px;"/>
          <input type="text" id="new-p-fee" class="partner-input" value="답례품 8% · 부의금 3% (익월 15일)" style="max-width:260px;"/>
          <input type="text" id="new-p-reqdep" class="partner-input" placeholder="전용 URL (예: sahaguminfh.iumbugo.com)" style="max-width:280px;"/>
          <input type="text" id="new-p-memo" class="partner-input" placeholder="담당자 / 메모 입력" style="flex:1; min-width:180px;"/>
          <button class="btn-header-outline" style="background:#3566e0; color:#fff; border-color:#3566e0; font-weight:700;" onclick="addNewPartnerCompany()">등록</button>
          <button class="btn-header-outline" onclick="toggleAddPartnerForm(false)">닫기</button>
        </div>
      </div>

      <!-- 선택된 업체 요약 + 체크리스트 -->
      <div class="partner-detail-box" style="margin-bottom:32px;">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; padding-bottom:14px; border-bottom:1px solid #e2e8f0; margin-bottom:16px;">
          <div>
            <strong id="chk-tab-partner-title" style="font-size:21px; color:#111111;">[사하구민장례식장] Step 1 ~ Step 6 체크리스트</strong>
            <div id="chk-tab-partner-meta" style="font-size:14px; color:#555555; margin-top:4px;"></div>
          </div>
          <div style="display:flex; align-items:center; gap:8px;">
            <strong id="chk-tab-partner-prog" style="font-size:16px; color:#3566e0; margin-right:6px;">0 / 6 완료</strong>
            <button class="btn-header-outline" onclick="checkAllForCurrentPartner(true)">전체 체크</button>
            <button class="btn-header-outline" onclick="checkAllForCurrentPartner(false)">초기화</button>
            <button class="btn-header-outline" style="color:#dc2626; border-color:#fca5a5;" onclick="deleteCurrentPartner()">삭제</button>
          </div>
        </div>

        <!-- 한 줄 조건 수정 바 -->
        <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap:8px; margin-bottom:16px; background:#f8fafc; padding:12px; border-radius:8px; border:1px solid #e2e8f0;">
          <div>
            <div style="font-size:12px; color:#64748b; font-weight:600; margin-bottom:3px;">제휴 수수료율 · 정산일</div>
            <input type="text" id="edit-p-fee" class="partner-input" onchange="saveCurrentPartnerSettings()" />
          </div>
          <div>
            <div style="font-size:12px; color:#64748b; font-weight:600; margin-bottom:3px;">전용 부고장 URL (파트너 코드)</div>
            <input type="text" id="edit-p-reqdep" class="partner-input" onchange="saveCurrentPartnerSettings()" />
          </div>
          <div>
            <div style="font-size:12px; color:#64748b; font-weight:600; margin-bottom:3px;">담당자 / 진행 메모</div>
            <input type="text" id="edit-p-memo" class="partner-input" onchange="saveCurrentPartnerSettings()" />
          </div>
        </div>

        <div class="table_wrap" style="margin-bottom:0;">
          <table class="my_table" style="margin-bottom:0;">
            <thead>
              <tr>
                <th style="width:8%;">체크</th>
                <th style="width:14%;">단계</th>
                <th style="width:42%;">진행 항목</th>
                <th style="width:36%;" class="bg_y">확인 기준</th>
              </tr>
            </thead>
            <tbody id="partner-checklist-tbody"></tbody>
          </table>
        </div>
      </div>

      <!-- 전체 업체 진행 현황 요약표 -->
      <h2>2. 전체 제휴 장례식장 진행 현황 한눈에 보기</h2>
      <div class="table_wrap">
        <table class="my_table">
          <thead>
            <tr>
              <th style="width:18%;">장례식장명</th>
              <th style="width:24%;">수수료율 · 정산일</th>
              <th style="width:26%;">전용 부고장 URL</th>
              <th style="width:18%;">담당자 / 메모</th>
              <th style="width:14%;" class="bg_y">진행률</th>
            </tr>
          </thead>
          <tbody id="partner-summary-tbody"></tbody>
        </table>
      </div>

      <div class="page-Turn-nav">
        <button class="page-turn-btn" onclick="showPage('step-guide')">← 이전: ④ 업체별 지침 (Step 1~6)</button>
        <button class="page-turn-btn" onclick="showPage('cs-guide')">다음: ⑥ 운영 가이드 →</button>
      </div>
    </section>

    <!-- ====================================================================
          ⑥ 운영 가이드 (#cs-guide)
          ==================================================================== -->
    <section id="page-cs-guide" class="guide-page">
      <h2 style="margin-top:0;">1. 이음부고(모바일 부고장 · 답례품 · 부의금) CS 처리 기준</h2>
      <p>장례식장 담당자, 상주, 조문객 문의 발생 시 아래 기준으로 신속하게 응대합니다.</p>

      <div class="table_wrap">
        <table class="my_table">
          <thead>
            <tr>
              <th style="width:24%;">문의 유형</th>
              <th style="width:28%;" class="bg_y">처리 원칙</th>
              <th>상세 응대 기준</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="ta_c"><strong>1) 부고장 정보 수정 요청<br/>(상주명·계좌·빈소·발인일시)</strong></td>
              <td class="ta_c bg_y"><strong>상주 비밀번호 수정 또는<br/>마스터 어드민 즉시 수정</strong></td>
              <td>상주가 부고장 하단 <code>[부고 수정]</code>에서 개설 시 설정한 비밀번호로 직접 수정할 수 있으며, 긴급 시 우리 팀이 <strong>마스터 어드민(<code>/admin/obituaries</code>)에서 즉시 대행 수정</strong>합니다.</td>
            </tr>
            <tr>
              <td class="ta_c"><strong>2) 상주에게 부고장 작성 링크<br/>문자 발송 요청</strong></td>
              <td class="ta_c bg_y"><strong>파트너 관리자 문자 발송 또는<br/>전용 URL 즉시 전달</strong></td>
              <td>장례식장 파트너 관리자(<code>/partner/dashboard</code>)의 <strong>[문자 발송]</strong> 기능으로 상주 연락처에 즉시 발송하거나, <code>https://{파트너코드}.iumbugo.com/create/basic</code> 링크를 전달합니다.</td>
            </tr>
            <tr>
              <td class="ta_c"><strong>3) 모바일 답례품 배송 ·<br/>교환 · 주문 취소 문의</strong></td>
              <td class="ta_c bg_y"><strong>데브늄 전담 CS 처리<br/>(장례식장 업무 부담 0%)</strong></td>
              <td>답례품 모바일 쿠폰 재발송, 배송지 변경, 상품 불량 교환 및 환불 문의는 <strong>데브늄 고객센터에서 100% 전담 처리</strong>합니다.</td>
            </tr>
            <tr>
              <td class="ta_c"><strong>4) 부의금 카드결제 단순 변심 ·<br/>금액 오입력 취소 요청</strong></td>
              <td class="ta_c bg_y"><strong style="color:#dc2626;">원금 반환 입금 확인 후 취소</strong><br/>(송금완료 후 임의 취소 불가)</td>
              <td>
                결제 즉시 상주 계좌로 현금이 입금되므로 당사에서 임의로 회수·취소할 수 없습니다.<br/>
                - 결제자에게 <strong>부의금 원금을 데브늄 계좌(KB국민은행 <code>868201-00-059645</code> / 예금주 데브늄(주))로 입금</strong>하도록 안내하고, <strong>입금 확인 즉시 카드 승인 취소</strong>를 진행합니다.
              </td>
            </tr>
            <tr>
              <td class="ta_c"><strong>5) 상주 측 부의금 미입금 문의</strong></td>
              <td class="ta_c bg_y"><strong>어드민 송금 상태 및<br/>입금자명(조문객 성명) 안내</strong></td>
              <td>어드민(<code>/admin/condolence-orders</code>)에서 <code>송금완료</code> 여부를 확인하고 상주 통장에 찍힌 <strong>입금자명(조문객 성명)</strong>을 안내합니다. (은행 점검 시간 <strong>23:50~00:30</strong> 결제 건은 점검 종료 후 순차 입금)</td>
            </tr>
          </tbody>
        </table>
      </div>

      <h2>2. 상황별 표준 응대 멘트 (복사용)</h2>
      <div class="grid-2-tables">
        <div class="code-block-pro" style="margin:0;">
          <div class="code-block-header">
            <span>① 부의금 금액 오입력 · 단순 변심 취소 요청 시 (입금 안내)</span>
            <button class="code-copy-btn" onclick="copyCode(this)">복사</button>
          </div>
          <pre style="white-space:pre-wrap; word-break:keep-all;">안녕하세요, 고객님.
부의금은 결제와 동시에 상주님 계좌로 바로 전달되는 서비스라, 저희가 임의로 취소하기가 어렵습니다.

아래 계좌로 부의금 원금을 입금해 주시면, 확인 후 카드 결제를 바로 취소해 드리겠습니다.

▶ KB국민은행 868201-00-059645
▶ 예금주 : 데브늄(주)
▶ 입금액 : 결제하신 부의금 원금 (수수료 제외)

※ 카드 취소 후 환급 시점은 카드사에 따라 다를 수 있습니다.</pre>
        </div>

        <div class="code-block-pro" style="margin:0;">
          <div class="code-block-header">
            <span>② 상주 측 "부의금 입금이 안 들어왔다" 문의 시</span>
            <button class="code-copy-btn" onclick="copyCode(this)">복사</button>
          </div>
          <pre style="white-space:pre-wrap; word-break:keep-all;">상주님, 삼가 고인의 명복을 빕니다.
확인 결과 [조문객 성명]님께서 [결제 시각]에 결제하신 [금액]원이 상주님의 계좌로 정상 입금 완료되었습니다.
통장 거래내역에서 입금자명 '[조문객 성명]'으로 입금된 내역을 한 번 더 확인 부탁드립니다.

※ 은행 점검 시간(23:50~00:30)에 결제된 건은 점검 종료 이후 순차적으로 입금될 예정입니다.</pre>
        </div>
      </div>

      <div class="page-Turn-nav">
        <button class="page-turn-btn" onclick="showPage('checklist')">← 이전: ⑤ 업체별 체크리스트</button>
        <button class="page-turn-btn" onclick="showPage('pdfs')">처음으로: ① 표준계약서 →</button>
      </div>
    </section>

  </main>

  <!-- ========================================================================
        FOOTER (.before-footer)
        ======================================================================== -->
  <footer class="before-footer">
    <div class="container">
      <div class="footer-links" style="margin-bottom:0;">
        <a onclick="showPage('pdfs')">1. 표준계약서</a>
        <a onclick="showPage('client-guide')">2. 고객사 가이드</a>
        <a onclick="showPage('internal-guide')">3. 내부 운영 가이드 (UI/UX)</a>
        <a onclick="showPage('step-guide')">4. 업체별 지침 (Step 1~6)</a>
        <a onclick="showPage('checklist')">5. 업체별 체크리스트</a>
        <a onclick="showPage('cs-guide')">6. 운영 가이드</a>
      </div>
    </div>
  </footer>

  <!-- ========================================================================
        JAVASCRIPT
        ======================================================================== -->
  <script>
    const PAGE_META = {
      'pdfs': {
        title: '① 표준계약서',
        sub: '장례식장·제휴사에 전달하는 필수 자료 4종(표준계약서 · 파트너 리플렛 v.5 · 상주 부고장 시연 · 파트너 관리자 시연) 및 고객사 전달용 공식 URL입니다.',
        nav: 'nav-pdfs'
      },
      'client-guide': {
        title: '② 고객사 운영 가이드 & 수익 계산기',
        sub: '장례식장이 알아야 할 무료 도입 기준, 답례품(8%)·부의금(3%) 수익 정산, 예상 제휴 수익 자동 계산기 및 모바일 UI/UX 흐름입니다.',
        nav: 'nav-client'
      },
      'internal-guide': {
        title: '③ 내부 운영 가이드 (어드민 · 파트너센터 UI/UX 매뉴얼)',
        sub: '우리 팀이 사용하는 이음부고 마스터 어드민과 장례식장 파트너센터의 실화면(STEP 1~6) UI/UX 매뉴얼 및 내부 운영 기준입니다.',
        nav: 'nav-internal'
      },
      'step-guide': {
        title: '④ 업체별 지침 가이드 (Step 1~6)',
        sub: '신규 장례식장이 유입되었을 때 Step 1(계약 및 서류 수취)부터 Step 6(익월 15일 정산)까지 우리가 해야 할 일과 복사용 안내 템플릿입니다.',
        nav: 'nav-step'
      },
      'checklist': {
        title: '⑤ 업체별 체크리스트',
        sub: '사하구민장례식장 등 제휴 장례식장을 클릭하면 전용 URL, 요율 조건, Step 1~6 온보딩 체크리스트가 바로 나옵니다.',
        nav: 'nav-checklist'
      },
      'cs-guide': {
        title: '⑥ 운영 가이드',
        sub: '부고장 정보 수정, 링크 문자 발송, 답례품 배송·교환, 부의금 결제 취소·미입금 문의 등 상황별 CS 처리 기준과 표준 응대 멘트입니다.',
        nav: 'nav-cs'
      }
    };

    const PARTNER_CHECKLIST_ITEMS = [
      { step: 'STEP 1', title: '표준계약서 작성·날인 및 장례식장 구비서류(사업자등록증 사본 + 정산용 통장사본) 수취', guide: () => '사업자등록증 사본 + 통장사본 + 도로명주소·대표번호 확인' },
      { step: 'STEP 2', title: '마스터 어드민(/admin/partners) 신규 파트너 등록 및 요율(답례품 8% · 부의금 3%) 세팅', guide: (p) => p.feeRate + ' · ' + p.reqDeposit },
      { step: 'STEP 3', title: '장례식장 전용 부고장 URL 개설 확인 (장례식장명·주소·대표번호 자동 입력 검수)', guide: (p) => p.reqDeposit },
      { step: 'STEP 4', title: '파트너 관리자(/partner/login) 계정 발급 및 QR 스탠드·포스터 준비', guide: () => '상주 문자 발송 · 대시보드 · QR 포스터 인쇄 확인' },
      { step: 'STEP 5', title: '담당자 온보딩 안내 카톡 발송 (전용 URL + 파트너 관리자 계정 + 고객사용 가이드)', guide: (p) => p.memo },
      { step: 'STEP 6', title: '로비 QR 비치 오픈 확인 및 매월 말일 마감 → 익월 15일 정기 정산', guide: () => '매월 15일 답례품(8%) + 부의금(3%) 합산 지급' }
    ];

    const DEFAULT_PARTNERS = [
      { id: 'sahaguminfh', name: '사하구민장례식장', feeRate: '답례품 8% · 부의금 3% (익월 15일)', reqDeposit: 'https://sahaguminfh.iumbugo.com/create/basic', memo: '김준수 팀장(010-4694-1315) · 어드민 URL 세팅 완료', checks: [0,1,1,0,0,0] },
      { id: 'boram', name: '보람장례식장', feeRate: '답례품 8% · 부의금 3% (익월 15일)', reqDeposit: 'https://boram.iumbugo.com/create/basic', memo: '도입 협의 중', checks: [0,0,0,0,0,0] },
      { id: 'kyowon', name: '교원예움 장례식장', feeRate: '답례품 8% · 부의금 3% (익월 15일)', reqDeposit: 'https://kyowon.iumbugo.com/create/basic', memo: '도입 제안 진행', checks: [0,0,0,0,0,0] },
      { id: 'shilnakwon', name: '쉴낙원 장례식장', feeRate: '답례품 8% · 부의금 3% (익월 15일)', reqDeposit: 'https://shilnakwon.iumbugo.com/create/basic', memo: '도입 제안 진행', checks: [0,0,0,0,0,0] }
    ];

    let partnerList = [];
    let currentPartnerId = 'sahaguminfh';

    function loadPartnerData() {
      try {
        const raw = localStorage.getItem('devnium_eiumbugo_partner_v2');
        if (raw) {
          const parsed = JSON.parse(raw);
          if (Array.isArray(parsed) && parsed.length > 0) {
            partnerList = parsed;
            return;
          }
        }
      } catch (e) {}
      partnerList = JSON.parse(JSON.stringify(DEFAULT_PARTNERS));
    }

    function savePartnerData() {
      try {
        localStorage.setItem('devnium_eiumbugo_partner_v2', JSON.stringify(partnerList));
      } catch (e) {}
    }

    function getPartnerProgress(p) {
      const checks = Array.isArray(p.checks) ? p.checks : [];
      const total = PARTNER_CHECKLIST_ITEMS.length;
      let done = 0;
      for (let i = 0; i < total; i++) {
        if (checks[i]) done++;
      }
      const pct = Math.round((done / total) * 100);
      return { done, total, pct };
    }

    function renderPartnerManager() {
      const curr = partnerList.find(p => p.id === currentPartnerId) || partnerList[0];
      if (!curr) return;
      currentPartnerId = curr.id;

      const pillBox = document.getElementById('partner-pills-chk');
      if (pillBox) {
        pillBox.innerHTML = partnerList.map(p => {
          const prog = getPartnerProgress(p);
          const activeCls = p.id === currentPartnerId ? ' active' : '';
          return `<button type="button" class="partner-pill-btn${activeCls}" onclick="selectPartnerCompany('${p.id}')">
            <span>${p.name}</span>
            <span class="partner-pill-pct">${prog.done}/${prog.total}</span>
          </button>`;
        }).join('');
      }

      const currProg = getPartnerProgress(curr);
      const titleEl = document.getElementById('chk-tab-partner-title');
      const metaEl = document.getElementById('chk-tab-partner-meta');
      const progEl = document.getElementById('chk-tab-partner-prog');
      if (titleEl) titleEl.textContent = `[${curr.name}] Step 1 ~ Step 6 체크리스트`;
      if (metaEl) metaEl.innerHTML = `${curr.feeRate} &nbsp;|&nbsp; <code>${curr.reqDeposit}</code> &nbsp;|&nbsp; ${curr.memo}`;
      if (progEl) progEl.textContent = `${currProg.done} / ${currProg.total} 완료 (${currProg.pct}%)`;

      const setVal = (id, val) => { const el = document.getElementById(id); if (el) el.value = val || ''; };
      setVal('edit-p-fee', curr.feeRate);
      setVal('edit-p-reqdep', curr.reqDeposit);
      setVal('edit-p-memo', curr.memo);

      const chkBody = document.getElementById('partner-checklist-tbody');
      if (chkBody) {
        chkBody.innerHTML = PARTNER_CHECKLIST_ITEMS.map((item, idx) => {
          const isChecked = Boolean(curr.checks && curr.checks[idx]);
          const rowCls = isChecked ? 'chk-row checked' : 'chk-row';
          return `<tr class="${rowCls}" onclick="togglePartnerCheckItem('${curr.id}', ${idx})">
            <td class="ta_c"><input type="checkbox" class="chk-box" ${isChecked ? 'checked' : ''} onclick="event.stopPropagation(); togglePartnerCheckItem('${curr.id}', ${idx});"/></td>
            <td class="ta_c"><strong>${item.step}</strong></td>
            <td><strong>${item.title}</strong></td>
            <td class="bg_y">${item.guide(curr)}</td>
          </tr>`;
        }).join('');
      }

      const sumBody = document.getElementById('partner-summary-tbody');
      if (sumBody) {
        sumBody.innerHTML = partnerList.map(p => {
          const prog = getPartnerProgress(p);
          const isSel = p.id === currentPartnerId;
          const rowStyle = isSel ? 'background:#f0f6ff; cursor:pointer;' : 'cursor:pointer;';
          return `<tr style="${rowStyle}" onclick="selectPartnerCompany('${p.id}')">
            <td class="ta_c"><strong>${p.name}</strong></td>
            <td>${p.feeRate}</td>
            <td><code>${p.reqDeposit}</code></td>
            <td>${p.memo}</td>
            <td class="ta_c bg_y"><strong style="color:#3566e0;">${prog.done} / ${prog.total} (${prog.pct}%)</strong></td>
          </tr>`;
        }).join('');
      }
    }

    function selectPartnerCompany(partnerId) {
      currentPartnerId = partnerId;
      renderPartnerManager();
    }

    function togglePartnerCheckItem(partnerId, idx) {
      const p = partnerList.find(x => x.id === partnerId);
      if (!p) return;
      if (!Array.isArray(p.checks) || p.checks.length < PARTNER_CHECKLIST_ITEMS.length) {
        p.checks = new Array(PARTNER_CHECKLIST_ITEMS.length).fill(0);
      }
      p.checks[idx] = p.checks[idx] ? 0 : 1;
      savePartnerData();
      renderPartnerManager();
    }

    function checkAllForCurrentPartner(state) {
      const p = partnerList.find(x => x.id === currentPartnerId);
      if (!p) return;
      p.checks = new Array(PARTNER_CHECKLIST_ITEMS.length).fill(state ? 1 : 0);
      savePartnerData();
      renderPartnerManager();
    }

    function saveCurrentPartnerSettings() {
      const p = partnerList.find(x => x.id === currentPartnerId);
      if (!p) return;
      const getVal = (id) => { const el = document.getElementById(id); return el ? el.value.trim() : ''; };
      p.feeRate = getVal('edit-p-fee') || p.feeRate;
      p.reqDeposit = getVal('edit-p-reqdep') || p.reqDeposit;
      p.memo = getVal('edit-p-memo') || p.memo;
      savePartnerData();
      renderPartnerManager();
    }

    function toggleAddPartnerForm(forceOpen = null) {
      const box = document.getElementById('add-partner-form-box');
      if (!box) return;
      const show = forceOpen !== null ? forceOpen : (box.style.display === 'none');
      box.style.display = show ? 'block' : 'none';
    }

    function addNewPartnerCompany() {
      const getVal = (id) => { const el = document.getElementById(id); return el ? el.value.trim() : ''; };
      const name = getVal('new-p-name');
      if (!name) { alert('장례식장명을 입력해 주세요.'); return; }
      const newId = 'partner_' + Date.now();
      partnerList.push({
        id: newId,
        name: name,
        feeRate: getVal('new-p-fee') || '답례품 8% · 부의금 3% (익월 15일)',
        reqDeposit: getVal('new-p-reqdep') || 'https://{코드}.iumbugo.com/create/basic',
        memo: getVal('new-p-memo') || '신규 추가 장례식장',
        checks: [0,0,0,0,0,0]
      });
      currentPartnerId = newId;
      savePartnerData();
      renderPartnerManager();
      toggleAddPartnerForm(false);
      document.getElementById('new-p-name').value = '';
    }

    function deleteCurrentPartner() {
      if (partnerList.length <= 1) return;
      const p = partnerList.find(x => x.id === currentPartnerId);
      if (!p || !confirm(`[${p.name}] 항목을 삭제하시겠습니까?`)) return;
      partnerList = partnerList.filter(x => x.id !== currentPartnerId);
      currentPartnerId = partnerList[0].id;
      savePartnerData();
      renderPartnerManager();
    }

    function resetPartnerDataToDefault() {
      if (!confirm('장례식장 목록을 기본값으로 복원하시겠습니까?')) return;
      partnerList = JSON.parse(JSON.stringify(DEFAULT_PARTNERS));
      currentPartnerId = 'sahaguminfh';
      savePartnerData();
      renderPartnerManager();
    }

    function showPage(pageId, pushHash = true) {
      if (!PAGE_META[pageId]) pageId = 'pdfs';
      document.querySelectorAll('.guide-page').forEach(sec => {
        sec.classList.toggle('active', sec.id === 'page-' + pageId);
      });
      const meta = PAGE_META[pageId];
      document.getElementById('banner-title').textContent = meta.title;
      document.getElementById('banner-sub').textContent = meta.sub;
      document.querySelectorAll('.sf-menu > li').forEach(li => {
        li.classList.toggle('current-menu-ancestor', li.id === meta.nav);
      });
      document.querySelectorAll('.quick-pill').forEach(btn => {
        btn.classList.toggle('active', btn.getAttribute('data-pill') === pageId);
      });
      if (pushHash) {
        try { history.replaceState(null, '', '#' + pageId); } catch (e) {}
      }
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    function copyCode(btn) {
      const pre = btn.closest('.code-block-pro').querySelector('pre');
      if (!pre) return;
      navigator.clipboard.writeText(pre.innerText).then(() => {
        const orig = btn.textContent;
        btn.textContent = '복사완료!';
        setTimeout(() => { btn.textContent = orig; }, 1400);
      });
    }

    function formatKoreanMoney(won) {
      if (!won || won <= 0) return '0원';
      const eok = Math.floor(won / 100000000);
      const remAfterEok = won % 100000000;
      const man = Math.floor(remAfterEok / 10000);
      const remWon = remAfterEok % 10000;
      let parts = [];
      if (eok > 0) parts.push(`${eok.toLocaleString('ko-KR')}억`);
      if (man > 0) parts.push(`${man.toLocaleString('ko-KR')}만`);
      if (remWon > 0) {
        parts.push(`${remWon.toLocaleString('ko-KR')}원`);
        return parts.join(' ');
      }
      return parts.join(' ') + ' 원';
    }

    function setBugoPreset(cnt) {
      const inp = document.getElementById('calc-bugo-count');
      if (inp) inp.value = cnt;
      document.querySelectorAll('.calc-preset-btn').forEach(btn => {
        btn.classList.toggle('active', btn.textContent.replace(/[^0-9]/g, '') === String(cnt));
      });
      updateRevenueCalc();
    }

    function updateRevenueCalc() {
      const cntEl = document.getElementById('calc-bugo-count');
      const modeEl = document.getElementById('calc-per-bugo');
      if (!cntEl || !modeEl) return;
      const cnt = Math.max(0, parseInt(cntEl.value, 10) || 0);
      const perBugo = parseInt(modeEl.value, 10) || 60000;
      const perBugoStr = perBugo === 55000 ? '5.5만 원' : '6만 원';

      const giftFee = Math.round(cnt * perBugo * 0.08);
      const condolFee = Math.round(cnt * perBugo * 0.03);
      const totalMonthly = giftFee + condolFee;
      const totalYearly = totalMonthly * 12;

      const totEl = document.getElementById('calc-res-total');
      const yrEl = document.getElementById('calc-res-yearly');
      const gEl = document.getElementById('calc-res-gift');
      const gSubEl = document.getElementById('calc-res-gift-sub');
      const cEl = document.getElementById('calc-res-condol');
      const cSubEl = document.getElementById('calc-res-condol-sub');

      if (totEl) totEl.textContent = `${formatKoreanMoney(totalMonthly)} / 월`;
      if (yrEl) yrEl.textContent = `연 환산 약 ${formatKoreanMoney(totalYearly)} 추가 수익`;
      if (gEl) gEl.textContent = formatKoreanMoney(giftFee);
      if (gSubEl) gSubEl.textContent = `월 ${cnt.toLocaleString('ko-KR')}건 × 평균 ${perBugoStr} × 8%`;
      if (cEl) cEl.textContent = formatKoreanMoney(condolFee);
      if (cSubEl) cSubEl.textContent = `월 ${cnt.toLocaleString('ko-KR')}건 × 평균 ${perBugoStr} × 3%`;
    }

    window.addEventListener('DOMContentLoaded', () => {
      loadPartnerData();
      renderPartnerManager();
      updateRevenueCalc();
      const hash = (window.location.hash || '').replace('#', '').trim();
      if (hash && PAGE_META[hash]) {
        showPage(hash, false);
      } else {
        showPage('pdfs', false);
      }
    });
  </script>
</body>
</html>
"""
)

# ==============================================================================
# 2. BUILD EXTERNAL PARTNER GUIDE: eiumbugo-partner.html
# ==============================================================================
eiumbugo_partner_html = (
    base_head_css.replace(
        "<title>부카결 | 내부운영가이드</title>",
        '<title>이음부고 | 운영가이드</title>\n  <link rel="icon" type="image/png" href="guide-assets/eiumbugo-icon.png" />'
    )
    + extra_uiux_css
    + """
  </style>
<meta name="robots" content="noindex,nofollow"></head>
<body>

  <!-- ========================================================================
        TOP GNB HEADER (#header-outer)
        ======================================================================== -->
  <div id="header-outer">
    <header id="top">
      <a class="logo-wrap" onclick="showPage('intro-calc')">
        <img src="guide-assets/eiumbugo-logo.png" alt="이음부고" style="height:28px; width:auto; display:block;" />
        <div class="logo-sub">운영가이드</div>
      </a>

      <nav>
        <ul class="sf-menu">
          <li id="nav-intro" class="current-menu-ancestor">
            <a onclick="showPage('intro-calc')"><span class="menu-title-text">1. 도입 절차 &amp; 수익 계산기</span></a>
          </li>
          <li id="nav-deliverables">
            <a onclick="showPage('deliverables')"><span class="menu-title-text">2. 표준계약서</span></a>
          </li>
          <li id="nav-cs">
            <a onclick="showPage('cs-policy')"><span class="menu-title-text">3. 운영 가이드</span></a>
          </li>
        </ul>
      </nav>

      <div class="header-right-tools"></div>
    </header>
  </div>

  <!-- ========================================================================
        PAGE HEADER BANNER (#page-header-bg)
        ======================================================================== -->
  <div id="page-header-bg">
    <div class="container">
      <h1 id="banner-title">① 도입 절차 &amp; 예상 수익 자동 계산기</h1>
      <span class="subheader" id="banner-sub">장례식장 월 평균 장례 건수에 따른 모바일 답례품(8%)·부의금 카드결제(3%) 예상 수익 산출 및 도입 절차를 안내해 드립니다.</span>
    </div>
  </div>

  <!-- Quick 1-Click Navigation Bar -->
  <div class="quick-subnav-bar">
    <div class="quick-subnav-inner">
      <button class="quick-pill active" data-pill="intro-calc" onclick="showPage('intro-calc')">① 도입 절차 &amp; 수익 계산기</button>
      <button class="quick-pill" data-pill="deliverables" onclick="showPage('deliverables')">② 표준계약서</button>
      <button class="quick-pill" data-pill="cs-policy" onclick="showPage('cs-policy')">③ 운영 가이드</button>
    </div>
  </div>

  <main class="main-content">

    <!-- ====================================================================
          ① 도입 절차 & 수익 자동 계산기 (#intro-calc)
          ==================================================================== -->
    <section id="page-intro-calc" class="guide-page active">
      <h2 style="margin-top:0;">1. 장례식장 월 장례 건수 기반 — 예상 제휴 수익 자동 계산기</h2>
      <p>장례식장의 <strong>월 평균 장례(부고장 발행) 건수</strong>를 입력하면 별도 설비나 비용 부담 없이 <strong>모바일 답례품(8%)</strong>과 <strong>부의금 카드결제(3%)</strong>로 발생하는 월 예상 정산 수익이 즉시 산출됩니다.</p>

      <div class="calc-box">
        <div class="calc-top-row">
          <div class="calc-input-group">
            <label class="calc-label" for="partner-bugo-count">월 평균 장례(부고장 발행) 건수 입력 (건/월)</label>
            <div class="calc-input-wrap">
              <input type="number" id="partner-bugo-count" class="calc-num-input" value="100" min="10" step="10" oninput="updatePartnerCalc()" />
              <span style="font-size:16px; font-weight:700; color:#334155;">건 / 월</span>
              <select id="partner-per-bugo" class="partner-input" style="max-width:270px; font-weight:700;" onchange="updatePartnerCalc()">
                <option value="60000" selected>부고 1건당 평균 60,000원 (표준)</option>
                <option value="55000">부고 1건당 평균 55,000원 (보수적)</option>
              </select>
            </div>
            <div class="calc-preset-bar">
              <button type="button" class="calc-preset-btn" onclick="setPartnerPreset(30)">월 30건</button>
              <button type="button" class="calc-preset-btn" onclick="setPartnerPreset(50)">월 50건</button>
              <button type="button" class="calc-preset-btn active" onclick="setPartnerPreset(100)">월 100건</button>
              <button type="button" class="calc-preset-btn" onclick="setPartnerPreset(200)">월 200건</button>
              <button type="button" class="calc-preset-btn" onclick="setPartnerPreset(300)">월 300건</button>
              <button type="button" class="calc-preset-btn" onclick="setPartnerPreset(500)">월 500건</button>
            </div>
          </div>
          <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:10px; padding:12px 16px; font-size:13px; color:#475569; max-width:360px;">
            <strong style="color:#1e293b; display:block; margin-bottom:4px;">수익 산출 기준 (답례품 8% + 부의금 3%)</strong>
            · <strong>모바일 답례품</strong>: 부고 1건당 평균 5.5만~6만 원 × <strong>장례식장 수수료 8%</strong><br/>
            · <strong>부의금 카드결제</strong>: 부고 1건당 평균 5.5만~6만 원 × <strong>장례식장 수수료 3%</strong>
          </div>
        </div>

        <div class="calc-result-grid">
          <div class="calc-stat-card highlight">
            <div class="calc-stat-title">예상 월 제휴 정산 수익 (합계)</div>
            <div class="calc-stat-val" id="p-calc-total">66만 원 / 월</div>
            <div class="calc-stat-sub" id="p-calc-yearly">연 환산 약 792만 원 추가 수익</div>
          </div>
          <div class="calc-stat-card">
            <div class="calc-stat-title">모바일 답례품 수익 (8% 기준)</div>
            <div class="calc-stat-val" id="p-calc-gift">48만 원</div>
            <div class="calc-stat-sub" id="p-calc-gift-sub">월 100건 × 평균 6만 원 × 8%</div>
          </div>
          <div class="calc-stat-card">
            <div class="calc-stat-title">부의금 카드결제 수익 (3% 기준)</div>
            <div class="calc-stat-val" id="p-calc-condol">18만 원</div>
            <div class="calc-stat-sub" id="p-calc-condol-sub">월 100건 × 평균 6만 원 × 3%</div>
          </div>
        </div>
      </div>

      <h2>2. 장례식장 도입 절차 (Step 1 ~ Step 4)</h2>
      <p>계약 체결부터 현장 오픈까지 별도 개발이나 설비 공사 없이 아래 순서로 즉시 시작하실 수 있습니다.</p>

      <div class="table_wrap">
        <table class="my_table">
          <thead>
            <tr>
              <th style="width:14%;">단계</th>
              <th style="width:26%;">진행 항목</th>
              <th style="width:38%;" class="bg_y">상세 진행 내용</th>
              <th style="width:22%;">장례식장 준비 사항</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="ta_c"><strong>STEP 1</strong></td>
              <td><strong>제휴 계약 체결 및<br/>구비서류 2종 제출</strong></td>
              <td class="bg_y">표준 제휴 계약서를 작성·날인하며, 정산 계좌 등록을 위해 <strong>사업자등록증 사본과 거래처 통장사본(정산용)</strong>을 제출합니다.</td>
              <td><strong>① 사업자등록증 사본 1부<br/>② 거래처 통장사본(정산용) 1부</strong></td>
            </tr>
            <tr>
              <td class="ta_c"><strong>STEP 2</strong></td>
              <td><strong>전용 모바일 부고장 URL 및<br/>파트너 관리자 발급</strong></td>
              <td class="bg_y">데브늄이 장례식장명·주소·대표번호가 자동 입력되는 <strong>전용 부고장 개설 링크(QR)</strong>와 <strong>파트너 관리자 계정</strong>을 발급해 드립니다.</td>
              <td>기본 정보 확인</td>
            </tr>
            <tr>
              <td class="ta_c"><strong>STEP 3</strong></td>
              <td><strong>로비 QR 스탠드 비치 및<br/>상주 부고장 링크 안내</strong></td>
              <td class="bg_y">데스크·로비에 전용 QR 스탠드(무상 제공)를 비치하거나, 파트너 관리자에서 상주 연락처로 부고장 작성 링크를 문자로 발송합니다.</td>
              <td>로비 QR 비치 · 상주 안내</td>
            </tr>
            <tr>
              <td class="ta_c"><strong>STEP 4</strong></td>
              <td><strong>실시간 내역 확인 및<br/>매월 15일 수익 정산</strong></td>
              <td class="bg_y">파트너 관리자에서 실시간 부고·결제 내역을 확인하며, 매월 발생한 답례품(8%) + 부의금(3%) 수익은 <strong>익월 15일</strong> 지정 계좌로 자동 입금됩니다.</td>
              <td>정식 운영 · 수익 정산</td>
            </tr>
          </tbody>
        </table>
      </div>
"""
    + uiux_mobile_flow_section
    + """
      <h2>4. 장례식장이 알아야 할 핵심 운영 기준</h2>
      <p>초기 도입비·월 관리비·예치금 부담 없이 운영하실 수 있는 핵심 기준입니다.</p>

      <div class="table_wrap">
        <table class="my_table">
          <thead>
            <tr>
              <th style="width:24%;">항목</th>
              <th style="width:30%;" class="bg_y">핵심 기준</th>
              <th>상세 안내 내용</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="ta_c"><strong>도입비 · 월 관리비 ·<br/>모바일 부고장 이용료</strong></td>
              <td class="ta_c bg_y"><strong>전액 무료 (0원)</strong><br/>(QR 스탠드·포스터 무상 제공)</td>
              <td>모바일 부고장 개설·알림톡 발송·파트너 관리자 이용료는 <strong>전액 무료</strong>이며, 로비 비치용 아크릴 QR 스탠드와 안내 포스터를 무상 지원합니다.</td>
            </tr>
            <tr>
              <td class="ta_c"><strong>모바일 답례품<br/>장례식장 제휴 수익</strong></td>
              <td class="ta_c bg_y"><strong>결제 금액의 8% 지급</strong></td>
              <td>발인 후 상주가 조문객에게 모바일 답례품을 결제·발송할 때마다 <strong>결제 금액의 8%가 장례식장 제휴 수익</strong>으로 자동 적립됩니다.</td>
            </tr>
            <tr>
              <td class="ta_c"><strong>부의금 카드결제<br/>장례식장 제휴 수익</strong></td>
              <td class="ta_c bg_y"><strong>결제 금액의 3% 지급</strong><br/>(상주에게 원금 100% 실시간 입금)</td>
              <td>조문객이 부고장에서 카드로 부의금을 결제하면 <strong>상주 계좌로 원금 100%가 즉시 입금</strong>되고, <strong>부의금 원금의 3%가 장례식장 제휴 수익</strong>으로 적립됩니다. (결제 수수료는 조문객 부담)</td>
            </tr>
            <tr>
              <td class="ta_c"><strong>예치금 부담 여부</strong></td>
              <td class="ta_c bg_y"><strong>예치금 없음 (0원)</strong></td>
              <td>이음부고 모바일 부고장을 도입하시는 장례식장은 별도 예치금이나 초기 비용을 납부하실 필요가 전혀 없습니다.</td>
            </tr>
            <tr>
              <td class="ta_c"><strong>제휴 수익 정산 지급일</strong></td>
              <td class="ta_c bg_y"><strong>매월 말일 마감 → 익월 15일 지급</strong></td>
              <td>매월 1일~말일까지 발생한 답례품(8%) 및 부의금 카드결제(3%) 제휴 수익을 합산하여 <strong>익월 15일(주말·공휴일 시 익영업일)</strong>에 지정 계좌로 입금합니다.</td>
            </tr>
            <tr>
              <td class="ta_c"><strong>계약 시 구비서류</strong></td>
              <td class="ta_c bg_y"><strong>제휴 계약서 +<br/>사업자등록증 · 통장사본</strong></td>
              <td>제휴 계약서 체결 시 <strong>① 사업자등록증 사본 1부 + ② 거래처 통장사본(수수료 정산 입금용) 1부</strong>를 제출해 주시면 됩니다.</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="page-Turn-nav">
        <span></span>
        <button class="page-turn-btn" onclick="showPage('deliverables')">다음: ② 표준계약서 →</button>
      </div>
    </section>

    <!-- ====================================================================
          ② 표준계약서 (#deliverables)
          ==================================================================== -->
    <section id="page-deliverables" class="guide-page">
      <h2 style="margin-top:0;">1. 표준계약서 및 필수 자료 4종 (표준계약서 · 파트너 가이드 · 부고장 시연 · 관리자 시연)</h2>
      <p>제휴 진행 시 제공해 드리는 필수 자료 및 실시간 시연 페이지 <strong>4가지</strong>입니다.</p>

      <div class="pdf-grid" style="margin-bottom:28px;">
        <!-- 1. 표준계약서 -->
        <div class="pdf-card">
          <div class="pdf-card-info">
            <span class="pdf-tag" style="background:#e8effe; color:#2451c8; font-weight:700;">1. 표준계약서</span>
            <div class="pdf-title">1) 이음부고 장례식장 제휴 표준계약서</div>
            <div class="pdf-desc">
              제휴사 날인용 표준계약서입니다. 계약 시 <strong>사업자등록증 사본 1부 + 거래처 통장사본(정산용) 1부</strong>를 제출해 주시면 됩니다.
            </div>
          </div>
          <div class="pdf-card-actions">
            <span class="btn-pdf-download" style="opacity:0.65; cursor:default;">PDF 다운로드 (추가 법률자문 진행 중)</span>
          </div>
        </div>

        <!-- 2. 이음부고 장례식장 파트너 가이드 v.5 -->
        <div class="pdf-card">
          <div class="pdf-card-info">
            <span class="pdf-tag" style="background:#e8effe; color:#2451c8; font-weight:700;">2. 파트너 가이드 (v.5)</span>
            <div class="pdf-title">2) 이음부고 장례식장 파트너 가이드 v.5</div>
            <div class="pdf-desc">모바일 부고장·답례품·부의금 카드결제 수익 구조, 현장 QR 비치 예시, 파트너 관리자 기능을 정리한 공식 파트너 가이드(v.5) 원본 PDF입니다.</div>
          </div>
          <div class="pdf-card-actions">
            <a class="btn-pdf-download" href="eiumbugo_partner_guide_v5.pdf" download="이음부고 장례식장 파트너 가이드 v.5.pdf">PDF 다운로드</a>
            <a class="btn-pdf-view" href="eiumbugo_partner_guide_v5.pdf" target="_blank">새창 열람</a>
          </div>
        </div>

        <!-- 3. 상주용 모바일 부고장 작성 체험 -->
        <div class="pdf-card">
          <div class="pdf-card-info">
            <span class="pdf-tag" style="background:#e8effe; color:#2451c8; font-weight:700;">3. 모바일 부고장 시연</span>
            <div class="pdf-title">3) 상주용 모바일 부고장 개설 실시간 시연</div>
            <div class="pdf-desc">상주가 로비 QR 스캔 또는 문자 링크를 통해 접속했을 때 장례식장 정보가 자동 입력되는 <strong>모바일 부고장 개설 시연 페이지</strong>입니다.</div>
          </div>
          <div class="pdf-card-actions">
            <a class="btn-pdf-view" href="https://demo.iumbugo.com/create/basic" target="_blank">새창 열람</a>
          </div>
        </div>

        <!-- 4. 장례식장 파트너 관리자 실시간 체험 -->
        <div class="pdf-card">
          <div class="pdf-card-info">
            <span class="pdf-tag" style="background:#e8effe; color:#2451c8; font-weight:700;">4. 파트너 관리자 시연</span>
            <div class="pdf-title">4) 장례식장 전용 파트너 관리자 센터</div>
            <div class="pdf-desc">장례식장 담당자가 실시간 부고 현황, 답례품·부의금 예상 정산금, 상주 링크 문자 발송, QR 포스터 인쇄를 이용하는 <strong>파트너 관리자 페이지</strong>입니다.</div>
          </div>
          <div class="pdf-card-actions">
            <a class="btn-pdf-view" href="https://iumbugo.com/partner/login" target="_blank">새창 열람</a>
          </div>
        </div>
      </div>

      <div class="page-Turn-nav">
        <button class="page-turn-btn" onclick="showPage('intro-calc')">← 이전: ① 도입 절차 &amp; 수익 계산기</button>
        <button class="page-turn-btn" onclick="showPage('cs-policy')">다음: ③ 운영 가이드 →</button>
      </div>
    </section>

    <!-- ====================================================================
          ③ 운영 가이드 (#cs-policy)
          ==================================================================== -->
    <section id="page-cs-policy" class="guide-page">
      <h2 style="margin-top:0;">1. 장례식장 전용 파트너 관리자 화면 안내</h2>
      <p>제휴 계약과 동시에 발급해 드리는 <strong>장례식장 전용 파트너 관리자(<code>https://iumbugo.com/partner/login</code>)</strong>에서 모든 현황을 실시간으로 확인하실 수 있습니다.</p>

      <div class="partner-screen-grid">
        <div class="partner-screen-card">
          <div class="partner-screen-img-wrap">
            <img src="guide-assets/p_dashboard_opt.png" alt="파트너 관리자 대시보드" />
          </div>
          <div class="partner-screen-body">
            <h4>① 실시간 정산 대시보드</h4>
            <p>QR 스캔 수, 부고장 등록 건수, 부의금 카드결제(3%) 및 모바일 답례품(8%) 실시간 예상 정산금을 한눈에 확인합니다.</p>
          </div>
        </div>
        <div class="partner-screen-card">
          <div class="partner-screen-img-wrap">
            <img src="guide-assets/p_sendlink_crop.png" alt="상주 부고장 링크 문자 발송" />
          </div>
          <div class="partner-screen-body">
            <h4>② 상주 부고장 작성 링크 문자 발송</h4>
            <p>전화·방문 상담 시 상주님 성함과 연락처만 입력하면 장례식장 정보가 자동 세팅된 부고장 작성 링크가 즉시 문자로 발송됩니다.</p>
          </div>
        </div>
        <div class="partner-screen-card">
          <div class="partner-screen-img-wrap">
            <img src="guide-assets/p_poster_crop.png" style="object-fit:contain; padding:8px;" alt="전용 QR 포스터 인쇄" />
          </div>
          <div class="partner-screen-body">
            <h4>③ 장례식장 전용 QR 포스터 인쇄</h4>
            <p>장례식장 고유 QR 코드가 삽입된 A4 안내 포스터를 언제든 바로 인쇄하거나 이미지로 다운로드하여 비치할 수 있습니다.</p>
          </div>
        </div>
      </div>

      <h2>2. 현장 운영 및 CS 처리 기준</h2>
      <p>상품 배송, 결제 취소, 고객 문의 등 모든 CS는 <strong>데브늄 전담 고객센터에서 처리</strong>하므로 장례식장의 추가 업무 부담이 없습니다.</p>

      <div class="table_wrap">
        <table class="my_table">
          <thead>
            <tr>
              <th style="width:24%;">문의 유형</th>
              <th style="width:28%;" class="bg_y">처리 원칙</th>
              <th>상세 안내 기준</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="ta_c"><strong>1) 상주 부고장 개설 안내</strong></td>
              <td class="ta_c bg_y"><strong>로비 QR 스캔 또는<br/>관리자에서 문자 링크 발송</strong></td>
              <td>상주가 데스크 QR 코드를 스캔하거나 장례식장 관리자에서 발송한 문자 링크를 열면 <strong>장례식장명·주소·대표번호가 자동으로 채워진 상태</strong>에서 3분 만에 부고장을 완성할 수 있습니다.</td>
            </tr>
            <tr>
              <td class="ta_c"><strong>2) 모바일 답례품 주문 ·<br/>배송 · 교환 문의</strong></td>
              <td class="ta_c bg_y"><strong>데브늄 전담 처리<br/>(장례식장 재고·관리 불필요)</strong></td>
              <td>발인 후 알림톡 발송, 답례품 결제, 모바일 쿠폰 발송, 배송 및 교환/환불 문의는 <strong>데브늄에서 100% 전담</strong>합니다.</td>
            </tr>
            <tr>
              <td class="ta_c"><strong>3) 부의금 카드결제 취소 ·<br/>금액 오입력 문의</strong></td>
              <td class="ta_c bg_y"><strong>원금 반환 입금 확인 후 취소</strong><br/>(상주 계좌 즉시 입금 구조)</td>
              <td>부의금은 결제 즉시 상주 계좌로 실시간 입금되므로, 단순 변심·금액 오입력 취소 시 결제자가 부의금 원금을 데브늄 계좌(<strong>KB국민은행 868201-00-059645 / 예금주 데브늄(주)</strong>)로 반환 입금하면 확인 즉시 카드 승인 취소를 진행합니다.</td>
            </tr>
            <tr>
              <td class="ta_c"><strong>4) 상주 측 부의금 미입금 문의</strong></td>
              <td class="ta_c bg_y"><strong>통장 입금자명(조문객 성명) 확인</strong></td>
              <td>상주 통장에 찍힌 <strong>입금자명(조문객 성명)</strong>을 확인하도록 안내합니다. (은행 점검 시간 <strong>23:50~00:30</strong> 결제 건은 점검 종료 후 순차 입금됩니다.)</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="page-Turn-nav">
        <button class="page-turn-btn" onclick="showPage('deliverables')">← 이전: ② 표준계약서</button>
        <button class="page-turn-btn" onclick="showPage('intro-calc')">처음으로: ① 도입 절차 &amp; 수익 계산기 →</button>
      </div>
    </section>

  </main>

  <footer class="before-footer">
    <div class="container">
      <div class="footer-links" style="margin-bottom:0;">
        <a onclick="showPage('intro-calc')">1. 도입 절차 &amp; 수익 계산기</a>
        <a onclick="showPage('deliverables')">2. 표준계약서</a>
        <a onclick="showPage('cs-policy')">3. 운영 가이드</a>
      </div>
    </div>
  </footer>

  <script>
    const PARTNER_PAGE_META = {
      'intro-calc': {
        title: '① 도입 절차 & 예상 수익 자동 계산기',
        sub: '장례식장 월 평균 장례 건수에 따른 모바일 답례품(8%)·부의금 카드결제(3%) 예상 수익 산출 및 도입 절차를 안내해 드립니다.',
        nav: 'nav-intro'
      },
      'deliverables': {
        title: '② 표준계약서',
        sub: '제휴 진행 시 제공해 드리는 필수 자료 4종(표준계약서 · 파트너 가이드 v.5 · 상주 부고장 시연 · 파트너 관리자 시연)입니다.',
        nav: 'nav-deliverables'
      },
      'cs-policy': {
        title: '③ 운영 가이드',
        sub: '장례식장 전용 파트너 관리자 화면 안내 및 현장 운영·CS 처리 기준입니다.',
        nav: 'nav-cs'
      }
    };

    function showPage(pageId, pushHash = true) {
      if (!PARTNER_PAGE_META[pageId]) pageId = 'intro-calc';
      document.querySelectorAll('.guide-page').forEach(sec => {
        sec.classList.toggle('active', sec.id === 'page-' + pageId);
      });
      const meta = PARTNER_PAGE_META[pageId];
      document.getElementById('banner-title').textContent = meta.title;
      document.getElementById('banner-sub').textContent = meta.sub;
      document.querySelectorAll('.sf-menu > li').forEach(li => {
        li.classList.toggle('current-menu-ancestor', li.id === meta.nav);
      });
      document.querySelectorAll('.quick-pill').forEach(btn => {
        btn.classList.toggle('active', btn.getAttribute('data-pill') === pageId);
      });
      if (pushHash) {
        try { history.replaceState(null, '', '#' + pageId); } catch (e) {}
      }
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    function formatKoreanMoney(won) {
      if (!won || won <= 0) return '0원';
      const eok = Math.floor(won / 100000000);
      const remAfterEok = won % 100000000;
      const man = Math.floor(remAfterEok / 10000);
      const remWon = remAfterEok % 10000;
      let parts = [];
      if (eok > 0) parts.push(`${eok.toLocaleString('ko-KR')}억`);
      if (man > 0) parts.push(`${man.toLocaleString('ko-KR')}만`);
      if (remWon > 0) {
        parts.push(`${remWon.toLocaleString('ko-KR')}원`);
        return parts.join(' ');
      }
      return parts.join(' ') + ' 원';
    }

    function setPartnerPreset(cnt) {
      const inp = document.getElementById('partner-bugo-count');
      if (inp) inp.value = cnt;
      document.querySelectorAll('.calc-preset-btn').forEach(btn => {
        btn.classList.toggle('active', btn.textContent.replace(/[^0-9]/g, '') === String(cnt));
      });
      updatePartnerCalc();
    }

    function updatePartnerCalc() {
      const cntEl = document.getElementById('partner-bugo-count');
      const modeEl = document.getElementById('partner-per-bugo');
      if (!cntEl || !modeEl) return;
      const cnt = Math.max(0, parseInt(cntEl.value, 10) || 0);
      const perBugo = parseInt(modeEl.value, 10) || 60000;
      const perBugoStr = perBugo === 55000 ? '5.5만 원' : '6만 원';

      const giftFee = Math.round(cnt * perBugo * 0.08);
      const condolFee = Math.round(cnt * perBugo * 0.03);
      const totalMonthly = giftFee + condolFee;
      const totalYearly = totalMonthly * 12;

      document.getElementById('p-calc-total').textContent = `${formatKoreanMoney(totalMonthly)} / 월`;
      document.getElementById('p-calc-yearly').textContent = `연 환산 약 ${formatKoreanMoney(totalYearly)} 추가 수익`;
      document.getElementById('p-calc-gift').textContent = formatKoreanMoney(giftFee);
      document.getElementById('p-calc-gift-sub').textContent = `월 ${cnt.toLocaleString('ko-KR')}건 × 평균 ${perBugoStr} × 8%`;
      document.getElementById('p-calc-condol').textContent = formatKoreanMoney(condolFee);
      document.getElementById('p-calc-condol-sub').textContent = `월 ${cnt.toLocaleString('ko-KR')}건 × 평균 ${perBugoStr} × 3%`;
    }

    window.addEventListener('DOMContentLoaded', () => {
      updatePartnerCalc();
      const hash = (window.location.hash || '').replace('#', '').trim();
      if (hash && PARTNER_PAGE_META[hash]) {
        showPage(hash, false);
      } else {
        showPage('intro-calc', false);
      }
    });
  </script>
</body>
</html>
"""
)

for dst in [f"{WORKDIR}/eiumbugo.html"]:
    with open(dst, "w", encoding="utf-8") as f:
        f.write(eiumbugo_internal_html)

for dst in [f"{WORKDIR}/eiumbugo-partner.html"]:
    with open(dst, "w", encoding="utf-8") as f:
        f.write(eiumbugo_partner_html)

print("Generated eiumbugo.html and eiumbugo-partner.html successfully!")
print("eiumbugo.html size:", len(eiumbugo_internal_html))
print("eiumbugo-partner.html size:", len(eiumbugo_partner_html))
