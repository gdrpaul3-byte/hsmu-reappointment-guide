# 힐리 pixel asset kit

화성의과학대학교 워크샵 마스코트 `힐리`의 도트 그래픽 재사용 패키지입니다. 다른 프로젝트로 폴더째 복사해서 쓸 수 있도록 이미지, CSS, React 컴포넌트 예제를 함께 묶었습니다.

## 폴더 구성

```text
asset-kits/healy-pixel/
  assets/
    sheet-transparent.png   # 3x3, 9프레임 투명 스프라이트 시트
    animation.gif           # 움직임 미리보기
    healy-frame-1..9.png    # 개별 프레임
  css/
    healy-sprite.css        # CSS 전용 사용 예제
  react/
    HealySprite.tsx         # React/Next.js 컴포넌트 예제
  source/
    raw-sheet.png
    raw-sheet-clean.png
    prompt-used.txt
    pipeline-meta.json
```

## 빠른 사용법: React/Next.js

1. `assets/sheet-transparent.png`를 대상 프로젝트의 `public/assets/healy-pixel/sheet-transparent.png`로 복사합니다.
2. `css/healy-sprite.css` 내용을 전역 CSS에 추가합니다.
3. `react/HealySprite.tsx`를 컴포넌트 폴더로 복사합니다.
4. 컴포넌트의 `spriteUrl` 기본값이 `/assets/healy-pixel/sheet-transparent.png`인지 확인합니다.

```tsx
import { HealySprite } from '@/components/HealySprite';

export function HeaderMascot() {
  return <HealySprite size={88} label="힐리, 화성의과학대학교 마스코트" />;
}
```

## 빠른 사용법: CSS만 사용

```html
<span class="healy-sprite healy-sprite--animated" role="img" aria-label="힐리"></span>
```

```css
@import './healy-sprite.css';
```

이미지 경로가 다르면 CSS 변수로 바꿀 수 있습니다.

```html
<span
  class="healy-sprite healy-sprite--animated"
  style="--healy-sprite-url: url('/my/path/sheet-transparent.png'); --healy-size: 96px"
  role="img"
  aria-label="힐리"
></span>
```

## 애니메이션 정보

- 프레임 수: 9
- 배열: 3 columns x 3 rows
- 기본 재생 시간: 1.35초
- CSS 방식: `background-position` + `steps(1, end)`
- 픽셀 선명도: `image-rendering: pixelated`
- 접근성: `prefers-reduced-motion: reduce`에서는 애니메이션을 끕니다.

## 언제 폴더째 복사하는 게 좋은가

이 asset kit처럼 폴더째 복사하는 방식은 작은 마스코트/브랜딩 asset에는 효율적입니다. 별도 npm 패키지로 만들 정도의 버전 관리나 여러 앱 동시 업데이트가 필요한 상황은 아직 아니기 때문입니다.

나중에 여러 프로젝트에서 동시에 관리해야 하면 그때 `@hsmu/healy-assets` 같은 private package로 승격하면 됩니다.
