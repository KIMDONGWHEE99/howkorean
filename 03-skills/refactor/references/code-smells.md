# 코드 스멜 카탈로그

마틴 파울러의 *Refactoring*(2판)에 기반한 종합 코드 스멜 레퍼런스입니다. 코드 스멜은 더 깊은 문제의 증상으로, 코드 설계에 뭔가 잘못된 부분이 있을 수 있다는 신호입니다.

> "코드 스멜은 대개 시스템의 더 깊은 문제와 맞닿아 있는, 겉으로 드러난 징후다." — 마틴 파울러

---

## 비대한 코드(Bloaters)

효과적으로 다루기 어려울 만큼 커져 버린 것을 나타내는 코드 스멜입니다.

### Long Method(긴 메서드)

**징후:**
- 메서드가 30-50줄을 넘음
- 메서드 전체를 보려면 스크롤해야 함
- 중첩 단계가 여러 겹
- 각 부분이 무엇을 하는지 설명하는 주석

**왜 나쁜가:**
- 이해하기 어려움
- 따로 떼어 테스트하기 어려움
- 변경이 의도하지 않은 결과를 낳음
- 중복 로직이 안에 숨어 있음

**리팩토링:**
- Extract Method(메서드 추출)
- Replace Temp with Query(임시 변수를 질의 함수로 바꾸기)
- Introduce Parameter Object(매개변수 객체 만들기)
- Replace Method with Method Object(메서드를 메서드 객체로 바꾸기)
- Decompose Conditional(조건문 분해하기)

**예(변경 전):**
```javascript
function processOrder(order) {
  // 주문 검증(20줄)
  if (!order.items) throw new Error('No items');
  if (order.items.length === 0) throw new Error('Empty order');
  // ... 검증 계속

  // 합계 계산(30줄)
  let subtotal = 0;
  for (const item of order.items) {
    subtotal += item.price * item.quantity;
  }
  // ... 세금, 배송비, 할인

  // 알림 보내기(20줄)
  // ... 이메일 로직
}
```

**예(변경 후):**
```javascript
function processOrder(order) {
  validateOrder(order);
  const totals = calculateOrderTotals(order);
  sendOrderNotifications(order, totals);
  return { order, totals };
}
```

---

### Large Class(거대한 클래스)

**징후:**
- 인스턴스 변수가 많은 클래스(7-10개 초과)
- 메서드가 많은 클래스(15-20개 초과)
- 클래스 이름이 모호함(Manager, Handler, Processor)
- 메서드들이 인스턴스 변수를 모두 쓰지는 않음

**왜 나쁜가:**
- 단일 책임 원칙 위반
- 테스트하기 어려움
- 변경이 관련 없는 기능까지 퍼져 나감
- 일부만 재사용하기 어려움

**리팩토링:**
- Extract Class(클래스 추출)
- Extract Subclass(서브클래스 추출)
- Extract Interface(인터페이스 추출)

**감지 기준:**
```
코드 줄 수 > 300
메서드 수 > 15
필드 수 > 10
```

---

### Primitive Obsession(기본형 집착)

**징후:**
- 도메인 개념에 기본형을 씀(이메일에 string, 금액에 int)
- 객체 대신 기본형 배열
- 타입 코드에 문자열 상수 사용
- 매직 넘버/매직 문자열

**왜 나쁜가:**
- 타입 수준에서 검증이 없음
- 로직이 코드베이스 곳곳에 흩어짐
- 잘못된 값을 넘기기 쉬움
- 도메인 개념이 빠져 있음

**리팩토링:**
- Replace Primitive with Object(기본형을 객체로 바꾸기)
- Replace Type Code with Class(타입 코드를 클래스로 바꾸기)
- Replace Type Code with Subclasses(타입 코드를 서브클래스로 바꾸기)
- Replace Type Code with State/Strategy(타입 코드를 상태/전략으로 바꾸기)

**예(변경 전):**
```javascript
const user = {
  email: 'john@example.com',     // 그냥 문자열
  phone: '1234567890',           // 그냥 문자열
  status: 'active',              // 매직 문자열
  balance: 10050                 // 센트 단위 정수
};
```

**예(변경 후):**
```javascript
const user = {
  email: new Email('john@example.com'),
  phone: new PhoneNumber('1234567890'),
  status: UserStatus.ACTIVE,
  balance: Money.cents(10050)
};
```

---

### Long Parameter List(긴 매개변수 목록)

**징후:**
- 매개변수가 4개 이상인 메서드
- 늘 함께 나타나는 매개변수
- 메서드 동작을 바꾸는 불리언 플래그
- null/undefined를 자주 넘김

**왜 나쁜가:**
- 올바르게 호출하기 어려움
- 매개변수 순서를 헷갈림
- 메서드가 너무 많은 일을 한다는 신호
- 새 매개변수를 추가하기 어려움

**리팩토링:**
- Introduce Parameter Object(매개변수 객체 만들기)
- Preserve Whole Object(객체 통째로 넘기기)
- Replace Parameter with Method Call(매개변수를 메서드 호출로 바꾸기)
- Remove Flag Argument(플래그 인수 제거하기)

**예(변경 전):**
```javascript
function createUser(firstName, lastName, email, phone,
                    street, city, state, zip,
                    isAdmin, isActive, createdBy) {
  // ...
}
```

**예(변경 후):**
```javascript
function createUser(personalInfo, address, options) {
  // personalInfo: { firstName, lastName, email, phone }
  // address: { street, city, state, zip }
  // options: { isAdmin, isActive, createdBy }
}
```

---

### Data Clumps(데이터 뭉치)

**징후:**
- 같은 필드 3개 이상이 반복해서 함께 나타남
- 늘 함께 다니는 매개변수
- 필드 일부가 따로 묶여야 할 것 같은 클래스

**왜 나쁜가:**
- 처리 로직이 중복됨
- 추상화가 빠져 있음
- 확장하기 어려움
- 숨은 클래스가 있다는 신호

**리팩토링:**
- Extract Class(클래스 추출)
- Introduce Parameter Object(매개변수 객체 만들기)
- Preserve Whole Object(객체 통째로 넘기기)

**예:**
```javascript
// 데이터 뭉치: (x, y, z) 좌표
function movePoint(x, y, z, dx, dy, dz) { }
function scalePoint(x, y, z, factor) { }
function distanceBetween(x1, y1, z1, x2, y2, z2) { }

// Point3D 클래스 추출
class Point3D {
  constructor(x, y, z) { }
  move(delta) { }
  scale(factor) { }
  distanceTo(other) { }
}
```

---

## 객체 지향 남용(Object-Orientation Abusers)

객체 지향 원칙을 불완전하거나 잘못 쓰고 있음을 나타내는 스멜입니다.

### Switch Statements(switch 문)

**징후:**
- 긴 switch/case나 if/else 연쇄
- 같은 switch가 여러 곳에 있음
- 타입 코드로 분기하는 switch
- 새 case를 추가하려면 모든 곳을 바꿔야 함

**왜 나쁜가:**
- 개방/폐쇄 원칙 위반
- 변경이 모든 switch 위치로 퍼져 나감
- 확장하기 어려움
- 다형성이 빠져 있다는 신호인 경우가 많음

**리팩토링:**
- Replace Conditional with Polymorphism(조건부 로직을 다형성으로 바꾸기)
- Replace Type Code with Subclasses(타입 코드를 서브클래스로 바꾸기)
- Replace Type Code with State/Strategy(타입 코드를 상태/전략으로 바꾸기)

**예(변경 전):**
```javascript
function calculatePay(employee) {
  switch (employee.type) {
    case 'hourly':
      return employee.hours * employee.rate;
    case 'salaried':
      return employee.salary / 12;
    case 'commissioned':
      return employee.sales * employee.commission;
  }
}
```

**예(변경 후):**
```javascript
class HourlyEmployee {
  calculatePay() {
    return this.hours * this.rate;
  }
}

class SalariedEmployee {
  calculatePay() {
    return this.salary / 12;
  }
}
```

---

### Temporary Field(임시 필드)

**징후:**
- 일부 메서드에서만 쓰는 인스턴스 변수
- 조건에 따라 설정되는 필드
- 특정 경우에만 필요한 복잡한 초기화

**왜 나쁜가:**
- 헷갈림 — 필드는 있지만 null일 수도 있음
- 객체 상태를 이해하기 어려움
- 조건부 로직이 숨어 있다는 신호

**리팩토링:**
- Extract Class(클래스 추출)
- Introduce Null Object(널 객체 도입하기)
- Replace Temp Field with Local(임시 필드를 지역 변수로 바꾸기)

---

### Refused Bequest(상속 포기)

**징후:**
- 서브클래스가 상속받은 메서드/데이터를 쓰지 않음
- 서브클래스가 아무것도 하지 않도록 재정의함
- IS-A 관계가 아니라 코드 재사용을 위해 상속을 씀

**왜 나쁜가:**
- 잘못된 추상화
- 리스코프 치환 원칙 위반
- 오해를 부르는 계층 구조

**리팩토링:**
- Push Down Method/Field(메서드/필드 내리기)
- Replace Subclass with Delegate(서브클래스를 위임으로 바꾸기)
- Replace Inheritance with Delegation(상속을 위임으로 바꾸기)

---

### Alternative Classes with Different Interfaces(서로 다른 인터페이스의 대안 클래스들)

**징후:**
- 비슷한 일을 하는 클래스 두 개
- 같은 개념에 다른 메서드 이름
- 서로 바꿔 쓸 수 있음

**왜 나쁜가:**
- 구현이 중복됨
- 공통 인터페이스가 없음
- 서로 바꿔 쓰기 어려움

**리팩토링:**
- Rename Method(메서드 이름 바꾸기)
- Move Method(메서드 옮기기)
- Extract Superclass(슈퍼클래스 추출)
- Extract Interface(인터페이스 추출)

---

## 변경 방해꾼(Change Preventers)

변경을 어렵게 만드는 스멜입니다 — 하나를 바꾸려면 다른 많은 것을 함께 바꿔야 합니다.

### Divergent Change(뒤엉킨 변경)

**징후:**
- 한 클래스가 여러 가지 다른 이유로 바뀜
- 서로 다른 영역의 변경이 같은 클래스 수정으로 이어짐
- 클래스가 "갓 클래스"임

**왜 나쁜가:**
- 단일 책임 원칙 위반
- 변경 빈도가 높음
- 병합 충돌

**리팩토링:**
- Extract Class(클래스 추출)
- Extract Superclass(슈퍼클래스 추출)
- Extract Subclass(서브클래스 추출)

**예:**
`User` 클래스가 다음 때문에 바뀝니다:
- 인증 변경
- 프로필 변경
- 결제 변경
- 알림 변경

→ 추출: `AuthService`, `ProfileService`, `BillingService`, `NotificationService`

---

### Shotgun Surgery(산탄총 수술)

**징후:**
- 변경 하나에 여러 클래스를 고쳐야 함
- 작은 기능 하나에 파일 10개 이상을 건드려야 함
- 변경할 곳이 흩어져 있어 모두 찾기 어려움

**왜 나쁜가:**
- 한 곳을 빠뜨리기 쉬움
- 결합도가 높음
- 변경할 때 실수하기 쉬움

**리팩토링:**
- Move Method(메서드 옮기기)
- Move Field(필드 옮기기)
- Inline Class(클래스 인라인)

**감지 기준:**
필드 하나를 추가하는데 파일 5개 넘게 바꿔야 하는지 확인하세요.

---

### Parallel Inheritance Hierarchies(평행 상속 계층)

**징후:**
- 한 계층에 서브클래스를 만들면 다른 계층에도 서브클래스를 만들어야 함
- 클래스 접두사가 짝을 이룸(예: `DatabaseOrder`, `DatabaseProduct`)

**왜 나쁜가:**
- 유지 보수가 두 배
- 계층 사이의 결합
- 한쪽을 잊기 쉬움

**리팩토링:**
- Move Method(메서드 옮기기)
- Move Field(필드 옮기기)
- 계층 하나를 없애기

---

## 없어도 되는 것(Dispensables)

없애야 할 불필요한 것들입니다.

### Comments (Excessive)(과도한 주석)

**징후:**
- 코드가 무엇을 하는지 설명하는 주석
- 주석 처리된 코드
- 영원히 남아 있는 TODO/FIXME
- 주석으로 사과하기

**왜 나쁜가:**
- 주석은 거짓말을 함(코드와 어긋남)
- 코드는 그 자체로 설명이 되어야 함
- 죽은 코드는 혼란을 일으킴

**리팩토링:**
- Extract Method(메서드 추출, 이름이 무엇을 하는지 설명)
- Rename(이름 바꾸기, 주석 없이도 명확하게)
- 주석 처리된 코드 제거
- Introduce Assertion(어서션 추가하기)

**좋은 주석과 나쁜 주석:**
```javascript
// 나쁨: 무엇을 하는지 설명
// 사용자를 순회하며 활성 상태인지 확인
for (const user of users) {
  if (user.status === 'active') { }
}

// 좋음: 왜 하는지 설명
// 활성 사용자만 - 비활성 사용자는 정리 작업이 처리함
const activeUsers = users.filter(u => u.isActive);
```

---

### Duplicate Code(중복 코드)

**징후:**
- 같은 코드가 여러 곳에 있음
- 조금씩만 다른 비슷한 코드
- 복사해 붙여 넣은 패턴

**왜 나쁜가:**
- 버그를 고칠 때 여러 곳을 고쳐야 함
- 일관성이 깨질 위험
- 코드베이스가 비대해짐

**리팩토링:**
- Extract Method(메서드 추출)
- Extract Class(클래스 추출)
- Pull Up Method(메서드 올리기, 계층 구조에서)
- Form Template Method(템플릿 메서드 만들기)

**감지 규칙:**
3번 이상 중복된 코드는 추출해야 합니다.

---

### Lazy Class(성의 없는 클래스)

**징후:**
- 존재 이유를 정당화할 만큼 일을 하지 않는 클래스
- 덧붙이는 가치가 없는 래퍼
- 과도한 설계의 결과

**왜 나쁜가:**
- 유지 보수 부담
- 불필요한 간접 참조
- 이득 없는 복잡도

**리팩토링:**
- Inline Class(클래스 인라인)
- Collapse Hierarchy(계층 합치기)

---

### Dead Code(죽은 코드)

**징후:**
- 도달할 수 없는 코드
- 쓰이지 않는 변수/메서드/클래스
- 주석 처리된 코드
- 결코 참이 될 수 없는 조건 뒤의 코드

**왜 나쁜가:**
- 혼란
- 유지 보수 부담
- 이해하는 속도를 늦춤

**리팩토링:**
- Remove Dead Code(죽은 코드 제거)
- Safe Delete(안전한 삭제)

**감지:**
```bash
# 쓰이지 않는 export 찾기
# 참조되지 않는 함수 찾기
# IDE의 "unused" 경고
```

---

### Speculative Generality(추측성 일반화)

**징후:**
- 서브클래스가 하나뿐인 추상 클래스
- "나중을 위해" 둔 쓰이지 않는 매개변수
- 위임만 하는 메서드
- 사용 사례가 하나뿐인 "프레임워크"

**왜 나쁜가:**
- 이득 없는 복잡도
- YAGNI(You Ain't Gonna Need It, 결국 필요 없을 것이다)
- 이해하기 더 어려움

**리팩토링:**
- Collapse Hierarchy(계층 합치기)
- Inline Class(클래스 인라인)
- Remove Parameter(매개변수 제거)
- Rename Method(메서드 이름 바꾸기)

---

## 결합(Couplers)

클래스 사이의 지나친 결합을 나타내는 스멜입니다.

### Feature Envy(기능 편애)

**징후:**
- 메서드가 자기 클래스보다 다른 클래스의 데이터를 더 많이 씀
- 다른 객체의 getter를 많이 호출함
- 데이터와 동작이 분리되어 있음

**왜 나쁜가:**
- 동작이 잘못된 곳에 있음
- 캡슐화가 약함
- 유지 보수하기 어려움

**리팩토링:**
- Move Method(메서드 옮기기)
- Move Field(필드 옮기기)
- Extract Method(메서드 추출, 그다음 옮기기)

**예(변경 전):**
```javascript
class Order {
  getDiscountedPrice(customer) {
    // 고객 데이터를 많이 씀
    if (customer.loyaltyYears > 5) {
      return this.price * customer.discountRate;
    }
    return this.price;
  }
}
```

**예(변경 후):**
```javascript
class Customer {
  getDiscountedPriceFor(price) {
    if (this.loyaltyYears > 5) {
      return price * this.discountRate;
    }
    return price;
  }
}
```

---

### Inappropriate Intimacy(부적절한 친밀함)

**징후:**
- 클래스끼리 서로의 private 부분에 접근함
- 양방향 참조
- 서브클래스가 부모에 대해 너무 많이 앎

**왜 나쁜가:**
- 결합도가 높음
- 변경이 연쇄적으로 퍼짐
- 하나를 고치려면 다른 하나도 고쳐야 함

**리팩토링:**
- Move Method(메서드 옮기기)
- Move Field(필드 옮기기)
- Change Bidirectional to Unidirectional(양방향 연관을 단방향으로 바꾸기)
- Extract Class(클래스 추출)
- Hide Delegate(위임 숨기기)

---

### Message Chains(메시지 체인)

**징후:**
- 메서드 호출이 길게 이어짐: `a.getB().getC().getD().getValue()`
- 클라이언트가 탐색 구조에 의존함
- "열차 사고" 같은 코드

**왜 나쁜가:**
- 깨지기 쉬움 — 어느 하나만 바뀌어도 체인이 깨짐
- 디미터 법칙 위반
- 구조에 결합됨

**리팩토링:**
- Hide Delegate(위임 숨기기)
- Extract Method(메서드 추출)
- Move Method(메서드 옮기기)

**예:**
```javascript
// 나쁨: 메시지 체인
const managerName = employee.getDepartment().getManager().getName();

// 더 나음: 위임 숨기기
const managerName = employee.getManagerName();
```

---

### Middle Man(중개자)

**징후:**
- 다른 클래스에 위임만 하는 클래스
- 메서드의 절반이 위임
- 덧붙이는 가치가 없음

**왜 나쁜가:**
- 불필요한 간접 참조
- 유지 보수 부담
- 헷갈리는 아키텍처

**리팩토링:**
- Remove Middle Man(중개자 제거하기)
- Inline Method(메서드 인라인)

---

## 스멜 심각도 가이드

| 심각도 | 설명 | 조치 |
|----------|-------------|--------|
| **Critical** | 개발을 막고 버그를 일으킴 | 즉시 수정 |
| **High** | 유지 보수 부담이 큼 | 이번 스프린트에서 수정 |
| **Medium** | 눈에 띄지만 감당할 수 있음 | 가까운 시일 안에 계획 |
| **Low** | 사소한 불편 | 기회가 될 때 수정 |

---

## 빠른 감지 체크리스트

코드를 훑어볼 때 이 체크리스트를 쓰세요:

- [ ] 30줄이 넘는 메서드가 있는가?
- [ ] 300줄이 넘는 클래스가 있는가?
- [ ] 매개변수가 4개를 넘는 메서드가 있는가?
- [ ] 중복된 코드 블록이 있는가?
- [ ] 타입 코드로 분기하는 switch/case가 있는가?
- [ ] 쓰이지 않는 코드가 있는가?
- [ ] 다른 클래스의 데이터를 많이 쓰는 메서드가 있는가?
- [ ] 메서드 호출이 길게 이어지는 곳이 있는가?
- [ ] "왜"가 아니라 "무엇"을 설명하는 주석이 있는가?
- [ ] 객체여야 할 기본형이 있는가?

---

## 더 읽을거리

- Fowler, M. (2018). *Refactoring: Improving the Design of Existing Code* (2nd ed.)
- Kerievsky, J. (2004). *Refactoring to Patterns*
- Feathers, M. (2004). *Working Effectively with Legacy Code*

---

**최종 업데이트**: 2026년 8월 4일
**Claude Code 버전**: 2.1.220
**출처**:
- https://code.claude.com/docs/ko/skills
**호환 모델**: Claude Fable 5, Claude Opus 5, Claude Sonnet 5, Claude Sonnet 4.6, Claude Opus 4.8, Claude Haiku 4.5
