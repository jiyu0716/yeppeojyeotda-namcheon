# 예뻐졌다 남천점

부산 남천동 두피 · 페이스 · 바디 에스테틱 소개 사이트.

정적 HTML 사이트이며 별도 빌드나 서버 설치 없이 GitHub Pages에서 실행됩니다.

- 진입 파일: `index.html`
- GitHub Pages: `main` 브랜치, `/(root)`에서 배포
- 첫 화면: 핑크 배경 + 세로 영상 `serum-drop.mp4` (Pexels, Ron Lach). 화면에 보일 때만 재생, 정지 버튼 있음
- 디자인 기준: `DESIGN.md` (색·글꼴·섹션 구성). 글꼴은 Gmarket Sans(제목)와 Pretendard(본문)를 CDN으로 불러옴
- 관리 이미지: HTML 안에 포함
- 텍스트 수정 모드는 제거했습니다. 문구와 디자인 변경은 소스 파일 수정 후 반영합니다.
- 예약 문의는 안내 창과 문의 문구 복사 기능입니다. 실제 예약 채널은 아직 연결되지 않았습니다.
- 확인되지 않은 세부 프로그램, 가격, 시간은 확인 필요로 표시합니다.
- AI 및 스톡 이미지는 실제 샵·고객·관리 결과를 나타내지 않습니다. 이미지 출처는 `PHOTO-CREDITS.md`를 확인하세요.

## 블로그 후기 자동 불러오기

- 매일 오전 9시(한국 시간) GitHub Actions(`.github/workflows/blog-reviews.yml`)가 네이버 검색 API로 "예뻐졌다 남천점" 블로그 글을 찾아 `blog-reviews.json`에 저장합니다.
- 제목·요약에 "예뻐졌다"와 "남천"이 모두 들어간 글만 최대 9개 보여 줍니다. 글이 없으면 블로그 후기 영역은 숨겨집니다.
- 키는 저장소 Settings → Secrets and variables → Actions의 `NAVER_CLIENT_ID`, `NAVER_CLIENT_SECRET`에 넣습니다. 코드에 키를 적지 않습니다.
- 바로 갱신하려면 저장소 Actions 탭 → "네이버 블로그 후기 불러오기" → Run workflow.
