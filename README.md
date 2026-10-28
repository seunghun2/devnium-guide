# 데브늄 통합 운영가이드 (부카결 & 이음부고 4종) 인수인계 및 작업 매뉴얼 (`HANDOVER.md`)

> **최종 업데이트**: 2026-10-29  
> **용도**: 다른 PC(컴퓨터)에서 작업을 이어서 진행하거나, AI 코딩 에이전트(Antigravity / Cursor / Claude 등)에 컨텍스트를 즉시 주입하기 위한 통합 인수인계 문서입니다.

---

## 1. 라이브 프로덕션 URL 4종 (`devnium-guide.vercel.app`)

모든 운영가이드는 본 서비스(`iumbugo.com`)와 완전히 분리된 **전용 독립 도메인(`https://devnium-guide.vercel.app`)**에서 호스팅됩니다. (PC · 태블릿 · 스마트폰 모바일 최적화 100% 완료)

| 구분 | 서비스명 | 대상 | 공식 접속 URL | 비밀번호 |
| :--- | :--- | :--- | :--- | :---: |
| **1** | **부카결** (`buipay`) | **내부용** (데브늄 팀원 전용) | [https://devnium-guide.vercel.app/buipay.html](https://devnium-guide.vercel.app/buipay.html) | `112233` |
| **2** | **부카결** (`buipay-partner`) | **고객사용** (외부 부고장 제휴사 전달용) | [https://devnium-guide.vercel.app/buipay-partner.html](https://devnium-guide.vercel.app/buipay-partner.html) | 없음 (즉시 열람) |
| **3** | **이음부고** (`eiumbugo`) | **내부용** (데브늄 팀원 전용) | [https://devnium-guide.vercel.app/eiumbugo.html](https://devnium-guide.vercel.app/eiumbugo.html) | `112233` |
| **4** | **이음부고** (`eiumbugo-partner`) | **고객사용** (제휴 장례식장·상조사 전달용) | [https://devnium-guide.vercel.app/eiumbugo-partner.html](https://devnium-guide.vercel.app/eiumbugo-partner.html) | 없음 (즉시 열람) |

> **주의 (도메인 분리 원칙)**  
> - `iumbugo.com` (EC2 본서버), `daedaesonson.vercel.app`, `deartribute-us.vercel.app`에 있던 가이드 HTML 파일들은 **모두 영구 삭제 완료**되었습니다.  
> - 앞으로도 가이드 4종은 오직 **`https://devnium-guide.vercel.app`** 에서만 운영합니다.

---

## 2. 다른 컴퓨터에서 작업 환경 세팅하는 법 (1분 컷)

### A. 가이드 페이지 4종(`devnium-guide.vercel.app`) 수정 작업 시
가이드 4종은 GitHub 저장소(`seunghun2/devnium-guide`)의 `main` 브랜치에 Push하면 **Vercel이 감지하여 약 5초 만에 `https://devnium-guide.vercel.app`에 자동 배포**됩니다.

```bash
# 1. 다른 컴퓨터에서 가이드 저장소 클론
git clone https://github.com/seunghun2/devnium-guide.git
cd devnium-guide

# 2. 파일 수정 후 GitHub에 Push (Vercel 자동 배포 트리거)
git add -A
git commit -m "chore: 가이드 내용 수정"
git push origin main
```

#### 저장소 주요 파일 구조 (`seunghun2/devnium-guide`)
```text
devnium-guide/
├── buipay.html                              # 1) 부카결 내부운영가이드 (PW: 112233)
├── buipay-partner.html                      # 2) 부카결 고객사용 운영가이드
├── eiumbugo.html                            # 3) 이음부고 내부운영가이드 (PW: 112233)
├── eiumbugo-partner.html                    # 4) 이음부고 고객사용 운영가이드
├── eiumbugo_partner_guide_v5.pdf            # 이음부고 장례식장 파트너 가이드 v.5 (PDF)
├── 부의금_서비스_운영가이드_v.4.pdf         # 부카결 운영 가이드 v.4 (PDF)
├── 부고장_푸터_제3자제공동의_약관가이드_v1.pdf # 부고장 푸터 필수 약관 가이드 v.1 (PDF)
├── devnium-bankbook-kb.jpg                  # 데브늄(주) KB국민은행 통장사본 이미지
├── guide-assets/                            # 이음부고 로고, 파비콘, 모바일 UI/UX, 어드민 STEP 1~6 스크린샷
│   ├── eiumbugo-logo.png                    # 이음부고 상단 헤더 로고
│   ├── eiumbugo-icon.png                    # 이음부고 브라우저 탭 파비콘
│   ├── admin_step1.png ~ admin_step7.png    # 마스터 어드민 & 파트너센터 실화면 캡처
│   ├── m_skin_basic.png, m_gift_step2~4.png # 모바일 답례품 4단계 화면
│   ├── m_bui_step1~4.png                    # 모바일 부의금 카드결제 4단계 화면
│   ├── p_dashboard_opt.png, p_sendlink_crop.png, p_poster_crop.png # 파트너 관리자 3대 화면
│   └── desk_qr_stand.jpg, desk_xbanner.jpg  # 장례식장 로비 QR 스탠드 & 배너 실물 사진
└── README.md / HANDOVER.md                  # 본 인수인계 문서
```

---

### B. 이음부고 본 서비스(`iumbugo.com`) 수정 작업 시
- **GitHub 저장소**: `https://github.com/seunghun991/iumbugo.git` (앱 경로: `maeumbugo-real/`)
- **실서버 (AWS EC2)**: `52.78.219.181` (`ec2-user`, PM2 프로세스명 `maeumbugo-real`, 포트 `3000`)

---

## 3. 서비스별 핵심 비즈니스 규칙 & 확정 사양 (필독)

### ① 부카결 (`buipay.html` / `buipay-partner.html`)
외부 모바일 부고장 플랫폼(국민부고, 삼가, 의전나라, 첫장, 부고알림, 효성프라콘 등)에 **부의금 신용카드 결제(선송금) 모듈만 연동**해 주는 B2B 서비스입니다.
1. **브랜드 완전 분리**: `buipay.html` 및 `buipay-partner.html` 내부에는 **`이음부고`(`iumbugo`)라는 단어나 링크가 절대 노출되면 안 됩니다.**
2. **상단 헤더 / 타이틀**:
   - 내부용: 브라우저 탭 `부카결 | 내부운영가이드`, 상단 로고 `부카결 | 내부운영가이드`, 우측 `[고객사용 가이드 열기]` 버튼 (인쇄 버튼 제거 완료)
   - 고객사용: 브라우저 탭 `부카결 | 운영가이드`, 상단 로고 `부카결 | 운영가이드`
3. **15일분 안전 예치금 자동 계산기**:
   - 제휴사의 **월 평균 부고장 발행 건수** 입력 시 즉시 산출
   - 부고 1건당 평균 부의금 카드결제액 옵션: **`60,000원 (표준)`** / **`55,000원 (보수적)`**
   - 산출 공식:
     - `예상 월 부의금 총 거래액 (30일)` = 월 부고 건수 × 건당 평균 금액(6만 원 또는 5.5만 원)
     - `일평균 부의금 송금액 (1일분)` = 월 총 거래액 ÷ 30일
     - `권장 안전 예치금 (15일분 기준)` = 월 총 거래액 ÷ 2 (15일분)
4. **예치금 입금 및 정산 원칙**:
   - 데브늄 예치금 입금 계좌: **KB국민은행 `868201-00-059645` (예금주: 데브늄(주))**
   - 상주 계좌로 `송금완료` 시 부의금 원금만큼 예치금에서 실시간 차감 (잔액 부족 시 결제 일시 차단 및 잔디 `H_한도알림` 웹훅 발송)
   - 주간 차감액 복구: **매주 금요일 복구 입금 원칙** (추후 변동 가능)
   - 업체 수수료 정산 지급일: **답례품 정산 지급일과 동일**
   - 계약 시 구비서류: 거래처로부터 **① 사업자등록증 사본 1부 + ② 거래처 통장사본(정산용) 1부** 수취 (※ 데브늄 통장사본은 업체에 별도 전달 불필요)
5. **표준계약서 버튼 상태**: `PDF 다운로드 (추가 법률자문 진행 중)`으로 표기

---

### ② 이음부고 (`eiumbugo.html` / `eiumbugo-partner.html`)
장례식장·상조사에 **이음부고 모바일 부고장 + 모바일 답례품 + 부의금 카드결제**를 올인원으로 무상 공급하고 수익을 쉐어하는 서비스입니다.
1. **상단 헤더 / 파비콘 / 타이틀**:
   - 파비콘: `guide-assets/eiumbugo-icon.png`
   - 상단 로고 이미지: `guide-assets/eiumbugo-logo.png`
   - 내부용 타이틀: `이음부고 | 내부운영가이드` / 고객사용 타이틀: `이음부고 | 운영가이드` (인쇄 버튼 제거 완료)
2. **핵심 수익 배분 및 운영 조건**:
   - **도입비 · 월 관리비 · 모바일 부고장 이용료 · 로비 QR 스탠드/포스터**: **전액 무료 (0원)**
   - **장례식장 예치금 부담**: **없음 (0원)** (데브늄 본사 송금 풀 `MID 2` 사용)
   - **장례식장 제휴 수익 요율**:
     - **모바일 답례품**: 결제 금액의 **`8%`** 지급
     - **부의금 카드결제**: 부의금 원금의 **`3%`** 지급 (결제 수수료 8.8%는 조문객 부담, 상주 계좌로 원금 100% 즉시 입금)
   - **정산 주기**: 매월 1일~말일 마감 → **익월 15일** 지정 계좌 자동 입금
3. **장례식장 예상 제휴 수익 자동 계산기**:
   - 월 평균 장례(부고 발행) 건수 × 건당 평균(`60,000원 표준` / `55,000원 보수적`) 기준
   - 답례품 수익(`8%`) + 부의금 카드결제 수익(`3%`) = **월 예상 제휴 수익 합계 및 연 환산 수익** 실시간 계산
4. **어드민 UI/UX 매뉴얼 (STEP 1 ~ STEP 6)**:
   - 기존 어드민 화면에서 **[예치금 잔액 (송금mid잔액 실시간 조회)]** 카드와 좌측 사이드바 **[조의금 서비스 설정]** 메뉴는 **실제 어드민(`iumbugo.com/admin`) 및 가이드 스크린샷·번호 콜아웃에서 모두 제거 완료**되었습니다.
   - STEP 1(부의금 결제 내역) ~ STEP 4(마스터 어드민), STEP 5 ~ STEP 6(장례식장 파트너 센터) 총 6단계로 구성되어 있습니다.
5. **표준계약서 버튼 상태**: `PDF 다운로드 (추가 법률자문 진행 중)`으로 표기

---

## 4. 제휴 장례식장 세팅 현황 & 전달용 템플릿

### 사하구민장례식장 (세팅 완료)
- **파트너 코드**: `sahaguminfh`
- **담당자**: 김준수 팀장님 (`010-2854-3081`)
- **장례식장 정보**: 사하구민장례식장 / 부산 사하구 장림번영로 26 (장림동) / `051-265-4444`
- **전용 모바일 부고장 개설 URL**: `https://sahaguminfh.iumbugo.com/create/basic`
- **파트너 관리자 URL**: `https://iumbugo.com/partner/login`
- **정산 조건**: 답례품 `8%` · 부의금 `3%` (매월 말일 마감, 익월 15일 정산)

#### 김준수 팀장님 전달용 카톡/문자 원문
```text
안녕하세요, 사하구민장례식장 김준수 팀장님!
이음부고(데브늄) 백승훈 차장입니다.

사하구민장례식장 전용 모바일 부고장 개설 링크 및 운영 가이드 안내드립니다.

■ 1. 사하구민장례식장 전용 모바일 부고장 개설 URL
▶ https://sahaguminfh.iumbugo.com/create/basic
※ 위 링크(또는 로비 QR)로 상주님이 접속하시면 '사하구민장례식장' 명칭·도로명주소·대표번호(051-265-4444)가 자동으로 입력되어 바로 부고장을 개설하실 수 있습니다.

■ 2. 장례식장 전용 파트너 관리자 센터
▶ 접속 주소 : https://iumbugo.com/partner/login
▶ 주요 기능 : 상주 부고장 작성 링크 문자 발송 / 부고·결제·정산금 실시간 조회 / 전용 QR 포스터 인쇄

■ 3. 이음부고 운영 가이드 및 예상 수익 계산기
▶ https://devnium-guide.vercel.app/eiumbugo-partner.html

■ 4. 정산 계좌 등록을 위한 구비서류 안내
편하신 때에 아래 2가지 서류를 카톡이나 메일로 전달 부탁드립니다.
 - 사업자등록증 사본 1부
 - 정산금 입금받으실 통장사본 1부

확인해보시고 궁금하신 점 있으시면 언제든 편하게 말씀해 주세요. 감사합니다!
```

---

## 5. 다른 컴퓨터에서 AI 에이전트에 첫 마디로 붙여넣을 프롬프트

새 컴퓨터에서 Antigravity / Cursor / Claude Code를 열고 아래 블록을 복사해 붙여넣으시면 바로 이어서 작업할 수 있습니다.

```text
현재 데브늄(Devnium)의 '부카결' 및 '이음부고' 운영가이드 4종 프로젝트를 이어서 작업하려고 해.
프로젝트의 모든 배경과 규칙은 저장소 내 `HANDOVER.md` (또는 `README.md`) 파일에 정리되어 있으니 먼저 그 파일을 읽고 컨텍스트를 파악해줘.

핵심 요약:
1. 라이브 배포 도메인: https://devnium-guide.vercel.app (Vercel 프로젝트명: devnium-guide, GitHub: seunghun2/devnium-guide)
   - 부카결 내부용(PW 112233): /buipay.html
   - 부카결 고객사용: /buipay-partner.html
   - 이음부고 내부용(PW 112233): /eiumbugo.html
   - 이음부고 고객사용: /eiumbugo-partner.html
2. 부카결 파일(buipay.html, buipay-partner.html)에는 '이음부고(iumbugo)' 관련 단어가 절대 들어가면 안 됨.
3. 이음부고 정산 요율은 답례품 8% / 부의금 3%이며, 계산기 단가는 부고 1건당 평균 60,000원(표준) / 55,000원(보수적) 기준임.
4. 수정 사항이 생기면 HTML 파일을 수정한 뒤 `seunghun2/devnium-guide` 저장소의 `main` 브랜치에 push하면 Vercel에 자동 배포됨.
```
