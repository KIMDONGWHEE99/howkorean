# [METHOD] /api/v1/[endpoint]

## 설명
이 엔드포인트가 하는 일을 간단히 설명합니다.

## 인증
필요한 인증 방식(예: Bearer 토큰).

## 매개변수

### 경로 매개변수
| 이름 | 타입 | 필수 | 설명 |
|------|------|----------|-------------|
| id | string | 예 | 리소스 ID |

### 쿼리 매개변수
| 이름 | 타입 | 필수 | 설명 |
|------|------|----------|-------------|
| page | integer | 아니요 | 페이지 번호(기본값: 1) |
| limit | integer | 아니요 | 페이지당 항목 수(기본값: 20) |

### 요청 본문
```json
{
  "field": "value"
}
```

## 응답

### 200 OK
```json
{
  "success": true,
  "data": {
    "id": "123",
    "name": "Example"
  }
}
```

### 400 Bad Request
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "잘못된 입력입니다"
  }
}
```

### 404 Not Found
```json
{
  "success": false,
  "error": {
    "code": "NOT_FOUND",
    "message": "리소스를 찾을 수 없습니다"
  }
}
```

## 예제

### cURL
```bash
curl -X GET "https://api.example.com/api/v1/endpoint" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json"
```

### JavaScript
```javascript
const response = await fetch('/api/v1/endpoint', {
  headers: {
    'Authorization': 'Bearer token',
    'Content-Type': 'application/json'
  }
});
const data = await response.json();
```

### Python
```python
import requests

response = requests.get(
    'https://api.example.com/api/v1/endpoint',
    headers={'Authorization': 'Bearer token'}
)
data = response.json()
```

## 속도 제한
- 인증된 사용자는 시간당 요청 1000개
- 공개 엔드포인트는 시간당 요청 100개

## 관련 엔드포인트
- [GET /api/v1/related](#)
- [POST /api/v1/related](#)

---

**최종 업데이트**: 2026년 8월 4일
**Claude Code 버전**: 2.1.220
**출처**:
- https://code.claude.com/docs/ko/plugins
**호환 모델**: Claude Fable 5, Claude Opus 5, Claude Sonnet 5, Claude Sonnet 4.6, Claude Opus 4.8, Claude Haiku 4.5
