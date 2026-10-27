# 리팩토링 카탈로그

마틴 파울러의 *Refactoring*(2판)에서 골라 정리한 리팩토링 기법 카탈로그입니다. 리팩토링마다 동기, 단계별 절차, 예시를 담았습니다.

> "리팩토링은 그 절차, 즉 변경을 수행하기 위해 따르는 정확한 단계의 순서로 정의된다." — 마틴 파울러

---

## 이 카탈로그를 쓰는 방법

1. 코드 스멜 레퍼런스로 **스멜을 찾기**
2. 이 카탈로그에서 **맞는 리팩토링을 찾기**
3. **절차를** 한 단계씩 따르기
4. 동작이 보존되는지 확인하도록 **단계마다 테스트하기**

**황금률**: 어떤 단계든 10분 넘게 걸린다면 더 작은 단계로 나누세요.

---

## 가장 많이 쓰는 리팩토링

### Extract Method(메서드 추출)

**언제 쓰나**: 긴 메서드, 중복 코드, 개념에 이름을 붙여야 할 때

**동기**: 코드 조각을, 목적을 설명하는 이름의 메서드로 바꿉니다.

**절차**:
1. (어떻게 하는지가 아니라) 무엇을 하는지를 이름으로 삼아 새 메서드 만들기
2. 코드 조각을 새 메서드로 복사
3. 조각에서 쓰는 지역 변수 찾기
4. 지역 변수를 매개변수로 넘기기(또는 메서드 안에서 선언)
5. 반환값을 알맞게 처리
6. 원래 코드 조각을 새 메서드 호출로 바꾸기
7. 테스트

**변경 전**:
```javascript
function printOwing(invoice) {
  let outstanding = 0;

  console.log("***********************");
  console.log("**** Customer Owes ****");
  console.log("***********************");

  // 미지급액 계산
  for (const order of invoice.orders) {
    outstanding += order.amount;
  }

  // 세부 정보 출력
  console.log(`name: ${invoice.customer}`);
  console.log(`amount: ${outstanding}`);
}
```

**변경 후**:
```javascript
function printOwing(invoice) {
  printBanner();
  const outstanding = calculateOutstanding(invoice);
  printDetails(invoice, outstanding);
}

function printBanner() {
  console.log("***********************");
  console.log("**** Customer Owes ****");
  console.log("***********************");
}

function calculateOutstanding(invoice) {
  return invoice.orders.reduce((sum, order) => sum + order.amount, 0);
}

function printDetails(invoice, outstanding) {
  console.log(`name: ${invoice.customer}`);
  console.log(`amount: ${outstanding}`);
}
```

---

### Inline Method(메서드 인라인)

**언제 쓰나**: 메서드 본문이 이름만큼 명확할 때, 위임이 지나칠 때

**동기**: 메서드가 가치를 더하지 않으면 불필요한 간접 참조를 없앱니다.

**절차**:
1. 메서드가 다형적이지 않은지 확인
2. 메서드를 호출하는 곳을 모두 찾기
3. 각 호출을 메서드 본문으로 바꾸기
4. 바꿀 때마다 테스트
5. 메서드 정의 제거

**변경 전**:
```javascript
function getRating(driver) {
  return moreThanFiveLateDeliveries(driver) ? 2 : 1;
}

function moreThanFiveLateDeliveries(driver) {
  return driver.numberOfLateDeliveries > 5;
}
```

**변경 후**:
```javascript
function getRating(driver) {
  return driver.numberOfLateDeliveries > 5 ? 2 : 1;
}
```

---

### Extract Variable(변수 추출)

**언제 쓰나**: 이해하기 어려운 복잡한 표현식

**동기**: 복잡한 표현식의 일부에 이름을 붙입니다.

**절차**:
1. 표현식에 부수 효과가 없는지 확인
2. 불변 변수 선언
3. 변수에 표현식(또는 그 일부)의 결과를 대입
4. 원래 표현식을 변수로 바꾸기
5. 테스트

**변경 전**:
```javascript
return order.quantity * order.itemPrice -
  Math.max(0, order.quantity - 500) * order.itemPrice * 0.05 +
  Math.min(order.quantity * order.itemPrice * 0.1, 100);
```

**변경 후**:
```javascript
const basePrice = order.quantity * order.itemPrice;
const quantityDiscount = Math.max(0, order.quantity - 500) * order.itemPrice * 0.05;
const shipping = Math.min(basePrice * 0.1, 100);
return basePrice - quantityDiscount + shipping;
```

---

### Inline Variable(변수 인라인)

**언제 쓰나**: 변수 이름이 표현식 자체보다 더 많은 것을 전달하지 못할 때

**동기**: 불필요한 간접 참조를 없앱니다.

**절차**:
1. 대입문 오른쪽에 부수 효과가 없는지 확인
2. 변수가 불변이 아니면 불변으로 만들고 테스트
3. 첫 번째 참조를 찾아 표현식으로 바꾸기
4. 테스트
5. 모든 참조에 반복
6. 선언과 대입 제거
7. 테스트

---

### Rename Variable(변수 이름 바꾸기)

**언제 쓰나**: 이름이 목적을 분명하게 전달하지 못할 때

**동기**: 좋은 이름은 깔끔한 코드에 꼭 필요합니다.

**절차**:
1. 변수가 널리 쓰인다면 캡슐화를 고려
2. 모든 참조 찾기
3. 참조를 하나씩 바꾸기
4. 테스트

**팁**:
- 의도가 드러나는 이름 쓰기
- 약어 피하기
- 도메인 용어 쓰기

```javascript
// 나쁨
const d = 30;
const x = users.filter(u => u.a);

// 좋음
const daysSinceLastLogin = 30;
const activeUsers = users.filter(user => user.isActive);
```

---

### Change Function Declaration(함수 선언 바꾸기)

**언제 쓰나**: 함수 이름이 목적을 설명하지 못할 때, 매개변수를 바꿔야 할 때

**동기**: 좋은 함수 이름은 코드를 그 자체로 설명이 되게 만듭니다.

**절차(간단한 방법)**:
1. 필요 없는 매개변수 제거
2. 이름 바꾸기
3. 필요한 매개변수 추가
4. 테스트

**절차(마이그레이션 방법 - 복잡한 변경용)**:
1. 매개변수를 제거한다면 쓰이지 않는지 확인
2. 원하는 선언으로 새 함수 만들기
3. 옛 함수가 새 함수를 호출하게 하기
4. 테스트
5. 호출하는 쪽이 새 함수를 쓰도록 바꾸기
6. 하나 바꿀 때마다 테스트
7. 옛 함수 제거

**변경 전**:
```javascript
function circum(radius) {
  return 2 * Math.PI * radius;
}
```

**변경 후**:
```javascript
function circumference(radius) {
  return 2 * Math.PI * radius;
}
```

---

### Encapsulate Variable(변수 캡슐화)

**언제 쓰나**: 여러 곳에서 데이터에 직접 접근할 때

**동기**: 데이터 조작을 위한 명확한 접근 지점을 제공합니다.

**절차**:
1. getter와 setter 함수 만들기
2. 모든 참조 찾기
3. 읽기를 getter로 바꾸기
4. 쓰기를 setter로 바꾸기
5. 바꿀 때마다 테스트
6. 변수의 가시성 제한

**변경 전**:
```javascript
let defaultOwner = { firstName: "Martin", lastName: "Fowler" };

// 여러 곳에서 사용
spaceship.owner = defaultOwner;
```

**변경 후**:
```javascript
let defaultOwnerData = { firstName: "Martin", lastName: "Fowler" };

function defaultOwner() { return defaultOwnerData; }
function setDefaultOwner(arg) { defaultOwnerData = arg; }

spaceship.owner = defaultOwner();
```

---

### Introduce Parameter Object(매개변수 객체 만들기)

**언제 쓰나**: 자주 함께 다니는 매개변수가 여러 개일 때

**동기**: 본래 함께 속하는 데이터를 묶습니다.

**절차**:
1. 묶을 매개변수를 위한 새 클래스/구조체 만들기
2. 테스트
3. Change Function Declaration으로 새 객체를 추가
4. 테스트
5. 묶음에 속한 매개변수를 하나씩 함수에서 제거하고 새 객체를 쓰게 하기
6. 하나 바꿀 때마다 테스트

**변경 전**:
```javascript
function amountInvoiced(startDate, endDate) { ... }
function amountReceived(startDate, endDate) { ... }
function amountOverdue(startDate, endDate) { ... }
```

**변경 후**:
```javascript
class DateRange {
  constructor(start, end) {
    this.start = start;
    this.end = end;
  }
}

function amountInvoiced(dateRange) { ... }
function amountReceived(dateRange) { ... }
function amountOverdue(dateRange) { ... }
```

---

### Combine Functions into Class(여러 함수를 클래스로 묶기)

**언제 쓰나**: 여러 함수가 같은 데이터를 다룰 때

**동기**: 함수를 그 함수가 다루는 데이터와 함께 묶습니다.

**절차**:
1. 공통 데이터에 Encapsulate Record 적용
2. 함수를 하나씩 클래스로 옮기기
3. 옮길 때마다 테스트
4. 데이터 인수를 클래스 필드 사용으로 바꾸기

**변경 전**:
```javascript
function base(reading) { ... }
function taxableCharge(reading) { ... }
function calculateBaseCharge(reading) { ... }
```

**변경 후**:
```javascript
class Reading {
  constructor(data) { this._data = data; }

  get base() { ... }
  get taxableCharge() { ... }
  get calculateBaseCharge() { ... }
}
```

---

### Split Phase(단계 쪼개기)

**언제 쓰나**: 코드가 서로 다른 두 가지 일을 다룰 때

**동기**: 경계가 분명한 별개의 단계로 코드를 나눕니다.

**절차**:
1. 두 번째 단계를 위한 두 번째 함수 만들기
2. 테스트
3. 단계 사이에 중간 데이터 구조 도입
4. 테스트
5. 첫 번째 단계를 별도 함수로 추출
6. 테스트

**변경 전**:
```javascript
function priceOrder(product, quantity, shippingMethod) {
  const basePrice = product.basePrice * quantity;
  const discount = Math.max(quantity - product.discountThreshold, 0)
    * product.basePrice * product.discountRate;
  const shippingPerCase = (basePrice > shippingMethod.discountThreshold)
    ? shippingMethod.discountedFee : shippingMethod.feePerCase;
  const shippingCost = quantity * shippingPerCase;
  return basePrice - discount + shippingCost;
}
```

**변경 후**:
```javascript
function priceOrder(product, quantity, shippingMethod) {
  const priceData = calculatePricingData(product, quantity);
  return applyShipping(priceData, shippingMethod);
}

function calculatePricingData(product, quantity) {
  const basePrice = product.basePrice * quantity;
  const discount = Math.max(quantity - product.discountThreshold, 0)
    * product.basePrice * product.discountRate;
  return { basePrice, quantity, discount };
}

function applyShipping(priceData, shippingMethod) {
  const shippingPerCase = (priceData.basePrice > shippingMethod.discountThreshold)
    ? shippingMethod.discountedFee : shippingMethod.feePerCase;
  const shippingCost = priceData.quantity * shippingPerCase;
  return priceData.basePrice - priceData.discount + shippingCost;
}
```

---

## 기능 옮기기

### Move Method(메서드 옮기기)

**언제 쓰나**: 메서드가 자기 클래스보다 다른 클래스의 기능을 더 많이 쓸 때

**동기**: 함수를 가장 많이 쓰는 데이터와 함께 둡니다.

**절차**:
1. 메서드가 자기 클래스에서 쓰는 모든 요소 살펴보기
2. 메서드가 다형적인지 확인
3. 메서드를 대상 클래스로 복사
4. 새 맥락에 맞게 조정
5. 원래 메서드가 대상에 위임하게 하기
6. 테스트
7. 원래 메서드 제거를 고려

---

### Move Field(필드 옮기기)

**언제 쓰나**: 다른 클래스가 필드를 더 많이 쓸 때

**동기**: 데이터를 그 데이터를 쓰는 함수와 함께 둡니다.

**절차**:
1. 아직 캡슐화하지 않았다면 필드 캡슐화
2. 테스트
3. 대상 클래스에 필드 만들기
4. 참조가 대상 필드를 쓰도록 갱신
5. 테스트
6. 원래 필드 제거

---

### Move Statements into Function(문장을 함수로 옮기기)

**언제 쓰나**: 같은 코드가 항상 함수 호출과 함께 나타날 때

**동기**: 반복되는 코드를 함수 안으로 옮겨 중복을 없앱니다.

**절차**:
1. 반복되는 코드가 아직 함수가 아니라면 함수로 추출
2. 문장을 그 함수 안으로 옮기기
3. 테스트
4. 호출하는 쪽에 더는 따로 둔 문장이 필요 없으면 제거

---

### Move Statements to Callers(문장을 호출한 곳으로 옮기기)

**언제 쓰나**: 공통 동작이 호출하는 쪽마다 달라질 때

**동기**: 동작이 달라져야 한다면 함수 밖으로 옮깁니다.

**절차**:
1. 옮길 코드에 Extract Method 적용
2. 원래 함수에 Inline Method 적용
3. 이제 인라인된 호출 제거
4. 추출한 코드를 각 호출 위치로 옮기기
5. 테스트

---

## 데이터 구성하기

### Replace Primitive with Object(기본형을 객체로 바꾸기)

**언제 쓰나**: 데이터 항목에 단순한 값 이상의 동작이 필요할 때

**동기**: 데이터를 그 동작과 함께 캡슐화합니다.

**절차**:
1. Encapsulate Variable 적용
2. 간단한 값 클래스 만들기
3. setter가 새 인스턴스를 만들도록 바꾸기
4. getter가 값을 반환하도록 바꾸기
5. 테스트
6. 새 클래스에 더 풍부한 동작 추가

**변경 전**:
```javascript
class Order {
  constructor(data) {
    this.priority = data.priority; // 문자열: "high", "rush" 등
  }
}

// 사용 예
if (order.priority === "high" || order.priority === "rush") { ... }
```

**변경 후**:
```javascript
class Priority {
  constructor(value) {
    if (!Priority.legalValues().includes(value))
      throw new Error(`Invalid priority: ${value}`);
    this._value = value;
  }

  static legalValues() { return ['low', 'normal', 'high', 'rush']; }
  get value() { return this._value; }

  higherThan(other) {
    return Priority.legalValues().indexOf(this._value) >
           Priority.legalValues().indexOf(other._value);
  }
}

// 사용 예
if (order.priority.higherThan(new Priority("normal"))) { ... }
```

---

### Replace Temp with Query(임시 변수를 질의 함수로 바꾸기)

**언제 쓰나**: 임시 변수가 표현식의 결과를 담고 있을 때

**동기**: 표현식을 함수로 추출해 코드를 더 명확하게 만듭니다.

**절차**:
1. 변수에 값이 한 번만 대입되는지 확인
2. 대입문의 오른쪽을 메서드로 추출
3. 임시 변수 참조를 메서드 호출로 바꾸기
4. 테스트
5. 임시 변수 선언과 대입 제거

**변경 전**:
```javascript
const basePrice = this._quantity * this._itemPrice;
if (basePrice > 1000) {
  return basePrice * 0.95;
} else {
  return basePrice * 0.98;
}
```

**변경 후**:
```javascript
get basePrice() {
  return this._quantity * this._itemPrice;
}

// 메서드 안에서
if (this.basePrice > 1000) {
  return this.basePrice * 0.95;
} else {
  return this.basePrice * 0.98;
}
```

---

## 조건부 로직 간소화

### Decompose Conditional(조건문 분해하기)

**언제 쓰나**: 복잡한 조건문(if-then-else)

**동기**: 조건과 동작을 추출해 의도를 분명하게 만듭니다.

**절차**:
1. 조건에 Extract Method 적용
2. then 분기에 Extract Method 적용
3. else 분기에 Extract Method 적용(있는 경우)

**변경 전**:
```javascript
if (!aDate.isBefore(plan.summerStart) && !aDate.isAfter(plan.summerEnd)) {
  charge = quantity * plan.summerRate;
} else {
  charge = quantity * plan.regularRate + plan.regularServiceCharge;
}
```

**변경 후**:
```javascript
if (isSummer(aDate, plan)) {
  charge = summerCharge(quantity, plan);
} else {
  charge = regularCharge(quantity, plan);
}

function isSummer(date, plan) {
  return !date.isBefore(plan.summerStart) && !date.isAfter(plan.summerEnd);
}

function summerCharge(quantity, plan) {
  return quantity * plan.summerRate;
}

function regularCharge(quantity, plan) {
  return quantity * plan.regularRate + plan.regularServiceCharge;
}
```

---

### Consolidate Conditional Expression(조건식 통합하기)

**언제 쓰나**: 결과가 같은 조건이 여러 개일 때

**동기**: 여러 조건이 사실 하나의 검사임을 분명히 합니다.

**절차**:
1. 조건에 부수 효과가 없는지 확인
2. `and`나 `or`로 조건 합치기
3. 합친 조건에 Extract Method 적용을 고려

**변경 전**:
```javascript
if (employee.seniority < 2) return 0;
if (employee.monthsDisabled > 12) return 0;
if (employee.isPartTime) return 0;
```

**변경 후**:
```javascript
if (isNotEligibleForDisability(employee)) return 0;

function isNotEligibleForDisability(employee) {
  return employee.seniority < 2 ||
         employee.monthsDisabled > 12 ||
         employee.isPartTime;
}
```

---

### Replace Nested Conditional with Guard Clauses(중첩 조건문을 보호 구문으로 바꾸기)

**언제 쓰나**: 깊이 중첩된 조건문 때문에 흐름을 따라가기 어려울 때

**동기**: 특수한 경우에는 보호 구문을 써서 정상 흐름을 분명하게 유지합니다.

**절차**:
1. 특수한 경우의 조건 찾기
2. 일찍 반환하는 보호 구문으로 바꾸기
3. 바꿀 때마다 테스트

**변경 전**:
```javascript
function payAmount(employee) {
  let result;
  if (employee.isSeparated) {
    result = { amount: 0, reasonCode: "SEP" };
  } else {
    if (employee.isRetired) {
      result = { amount: 0, reasonCode: "RET" };
    } else {
      result = calculateNormalPay(employee);
    }
  }
  return result;
}
```

**변경 후**:
```javascript
function payAmount(employee) {
  if (employee.isSeparated) return { amount: 0, reasonCode: "SEP" };
  if (employee.isRetired) return { amount: 0, reasonCode: "RET" };
  return calculateNormalPay(employee);
}
```

---

### Replace Conditional with Polymorphism(조건부 로직을 다형성으로 바꾸기)

**언제 쓰나**: 타입에 따른 switch/case, 타입마다 달라지는 조건부 로직

**동기**: 객체가 자기 동작을 직접 처리하게 합니다.

**절차**:
1. 클래스 계층 만들기(없는 경우)
2. 객체 생성에 팩터리 함수 사용
3. 조건부 로직을 슈퍼클래스 메서드로 옮기기
4. 경우마다 서브클래스 메서드 만들기
5. 원래 조건문 제거

**변경 전**:
```javascript
function plumages(birds) {
  return birds.map(b => plumage(b));
}

function plumage(bird) {
  switch (bird.type) {
    case 'EuropeanSwallow':
      return "average";
    case 'AfricanSwallow':
      return (bird.numberOfCoconuts > 2) ? "tired" : "average";
    case 'NorwegianBlueParrot':
      return (bird.voltage > 100) ? "scorched" : "beautiful";
    default:
      return "unknown";
  }
}
```

**변경 후**:
```javascript
class Bird {
  get plumage() { return "unknown"; }
}

class EuropeanSwallow extends Bird {
  get plumage() { return "average"; }
}

class AfricanSwallow extends Bird {
  get plumage() {
    return (this.numberOfCoconuts > 2) ? "tired" : "average";
  }
}

class NorwegianBlueParrot extends Bird {
  get plumage() {
    return (this.voltage > 100) ? "scorched" : "beautiful";
  }
}

function createBird(data) {
  switch (data.type) {
    case 'EuropeanSwallow': return new EuropeanSwallow(data);
    case 'AfricanSwallow': return new AfricanSwallow(data);
    case 'NorwegianBlueParrot': return new NorwegianBlueParrot(data);
    default: return new Bird(data);
  }
}
```

---

### Introduce Special Case (Null Object)(특이 케이스 추가하기)

**언제 쓰나**: 특수한 경우를 위해 null 검사를 반복할 때

**동기**: 특수한 경우를 처리하는 특별한 객체를 반환합니다.

**절차**:
1. 기대하는 인터페이스를 갖춘 특이 케이스 클래스 만들기
2. isSpecialCase 검사 추가
3. 팩터리 메서드 도입
4. null 검사를 특이 케이스 객체 사용으로 바꾸기
5. 테스트

**변경 전**:
```javascript
const customer = site.customer;
// ... 여러 곳에서 검사
if (customer === "unknown") {
  customerName = "occupant";
} else {
  customerName = customer.name;
}
```

**변경 후**:
```javascript
class UnknownCustomer {
  get name() { return "occupant"; }
  get billingPlan() { return registry.defaultPlan; }
}

// 팩터리 메서드
function customer(site) {
  return site.customer === "unknown"
    ? new UnknownCustomer()
    : site.customer;
}

// 사용 예 - null 검사가 필요 없음
const customerName = customer.name;
```

---

## API 리팩토링

### Separate Query from Modifier(질의 함수와 변경 함수 분리하기)

**언제 쓰나**: 함수가 값을 반환하면서 부수 효과도 일으킬 때

**동기**: 어떤 작업에 부수 효과가 있는지 분명히 합니다.

**절차**:
1. 새 질의 함수 만들기
2. 원래 함수의 반환 로직 복사
3. 원래 함수가 아무것도 반환하지 않도록(void) 수정
4. 반환값을 쓰는 호출을 바꾸기
5. 테스트

**변경 전**:
```javascript
function alertForMiscreant(people) {
  for (const p of people) {
    if (p === "Don") {
      setOffAlarms();
      return "Don";
    }
    if (p === "John") {
      setOffAlarms();
      return "John";
    }
  }
  return "";
}
```

**변경 후**:
```javascript
function findMiscreant(people) {
  for (const p of people) {
    if (p === "Don") return "Don";
    if (p === "John") return "John";
  }
  return "";
}

function alertForMiscreant(people) {
  if (findMiscreant(people) !== "") setOffAlarms();
}
```

---

### Parameterize Function(함수 매개변수화하기)

**언제 쓰나**: 여러 함수가 값만 다르게 비슷한 일을 할 때

**동기**: 매개변수를 추가해 중복을 없앱니다.

**절차**:
1. 함수 하나 고르기
2. 달라지는 리터럴을 위한 매개변수 추가
3. 본문이 매개변수를 쓰도록 바꾸기
4. 테스트
5. 호출하는 쪽이 매개변수화한 버전을 쓰도록 바꾸기
6. 이제 쓰이지 않는 함수 제거

**변경 전**:
```javascript
function tenPercentRaise(person) {
  person.salary = person.salary * 1.10;
}

function fivePercentRaise(person) {
  person.salary = person.salary * 1.05;
}
```

**변경 후**:
```javascript
function raise(person, factor) {
  person.salary = person.salary * (1 + factor);
}

// 사용 예
raise(person, 0.10);
raise(person, 0.05);
```

---

### Remove Flag Argument(플래그 인수 제거하기)

**언제 쓰나**: 불리언 매개변수가 함수 동작을 바꿀 때

**동기**: 별도의 함수로 동작을 명시적으로 드러냅니다.

**절차**:
1. 플래그 값마다 명시적인 함수 만들기
2. 각 호출을 알맞은 새 함수로 바꾸기
3. 바꿀 때마다 테스트
4. 원래 함수 제거

**변경 전**:
```javascript
function bookConcert(customer, isPremium) {
  if (isPremium) {
    // 프리미엄 예약 로직
  } else {
    // 일반 예약 로직
  }
}

bookConcert(customer, true);
bookConcert(customer, false);
```

**변경 후**:
```javascript
function bookPremiumConcert(customer) {
  // 프리미엄 예약 로직
}

function bookRegularConcert(customer) {
  // 일반 예약 로직
}

bookPremiumConcert(customer);
bookRegularConcert(customer);
```

---

## 상속 다루기

### Pull Up Method(메서드 올리기)

**언제 쓰나**: 여러 서브클래스에 같은 메서드가 있을 때

**동기**: 클래스 계층의 중복을 없앱니다.

**절차**:
1. 메서드들이 똑같은지 살펴보기
2. 시그니처가 같은지 확인
3. 슈퍼클래스에 새 메서드 만들기
4. 서브클래스 하나에서 본문 복사
5. 서브클래스 메서드 하나를 지우고 테스트
6. 나머지 서브클래스 메서드를 지우고 하나씩 테스트

---

### Push Down Method(메서드 내리기)

**언제 쓰나**: 동작이 일부 서브클래스에만 관련될 때

**동기**: 메서드를 쓰이는 곳에 둡니다.

**절차**:
1. 메서드가 필요한 서브클래스마다 복사
2. 슈퍼클래스에서 메서드 제거
3. 테스트
4. 필요 없는 서브클래스에서 제거
5. 테스트

---

### Replace Subclass with Delegate(서브클래스를 위임으로 바꾸기)

**언제 쓰나**: 상속을 잘못 쓰고 있을 때, 더 많은 유연성이 필요할 때

**동기**: 적절한 경우 상속보다 합성을 우선합니다.

**절차**:
1. 위임용 빈 클래스 만들기
2. 호스트 클래스에 위임 객체를 담을 필드 추가
3. 호스트에서 호출하는 위임 생성자 만들기
4. 기능을 위임으로 옮기기
5. 옮길 때마다 테스트
6. 상속을 위임으로 바꾸기

---

## Extract Class(클래스 추출)

**언제 쓰나**: 책임이 여러 개인 거대한 클래스

**동기**: 단일 책임을 유지하도록 클래스를 나눕니다.

**절차**:
1. 책임을 어떻게 나눌지 정하기
2. 새 클래스 만들기
3. 원래 클래스에서 새 클래스로 필드 옮기기
4. 테스트
5. 원래 클래스에서 새 클래스로 메서드 옮기기
6. 옮길 때마다 테스트
7. 두 클래스를 검토하고 이름 다시 짓기
8. 새 클래스를 어떻게 노출할지 정하기

**변경 전**:
```javascript
class Person {
  get name() { return this._name; }
  set name(arg) { this._name = arg; }
  get officeAreaCode() { return this._officeAreaCode; }
  set officeAreaCode(arg) { this._officeAreaCode = arg; }
  get officeNumber() { return this._officeNumber; }
  set officeNumber(arg) { this._officeNumber = arg; }

  get telephoneNumber() {
    return `(${this._officeAreaCode}) ${this._officeNumber}`;
  }
}
```

**변경 후**:
```javascript
class Person {
  constructor() {
    this._telephoneNumber = new TelephoneNumber();
  }
  get name() { return this._name; }
  set name(arg) { this._name = arg; }
  get telephoneNumber() { return this._telephoneNumber.toString(); }
  get officeAreaCode() { return this._telephoneNumber.areaCode; }
  set officeAreaCode(arg) { this._telephoneNumber.areaCode = arg; }
}

class TelephoneNumber {
  get areaCode() { return this._areaCode; }
  set areaCode(arg) { this._areaCode = arg; }
  get number() { return this._number; }
  set number(arg) { this._number = arg; }
  toString() { return `(${this._areaCode}) ${this._number}`; }
}
```

---

## 빠른 참조: 스멜별 리팩토링

| 코드 스멜 | 주 리팩토링 | 대안 |
|------------|-------------------|-------------|
| Long Method | Extract Method | Replace Temp with Query |
| Duplicate Code | Extract Method | Pull Up Method |
| Large Class | Extract Class | Extract Subclass |
| Long Parameter List | Introduce Parameter Object | Preserve Whole Object |
| Feature Envy | Move Method | Extract Method + Move |
| Data Clumps | Extract Class | Introduce Parameter Object |
| Primitive Obsession | Replace Primitive with Object | Replace Type Code |
| Switch Statements | Replace Conditional with Polymorphism | Replace Type Code |
| Temporary Field | Extract Class | Introduce Null Object |
| Message Chains | Hide Delegate | Extract Method |
| Middle Man | Remove Middle Man | Inline Method |
| Divergent Change | Extract Class | Split Phase |
| Shotgun Surgery | Move Method | Inline Class |
| Dead Code | Remove Dead Code | - |
| Speculative Generality | Collapse Hierarchy | Inline Class |

---

## 더 읽을거리

- Fowler, M. (2018). *Refactoring: Improving the Design of Existing Code* (2nd ed.)
- 온라인 카탈로그: https://refactoring.com/catalog/

---

**최종 업데이트**: 2026년 8월 4일
**Claude Code 버전**: 2.1.220
**출처**:
- https://code.claude.com/docs/ko/skills
**호환 모델**: Claude Fable 5, Claude Opus 5, Claude Sonnet 5, Claude Sonnet 4.6, Claude Opus 4.8, Claude Haiku 4.5
