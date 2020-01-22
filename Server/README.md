# API 가이드
`"필드명": 자료형 설명`
## 수신 이벤트 (서버 -> 클라이언트)
### `getq`
```
[
    {
        "x": Number 쿼터니언X,
        "y": Number 쿼터니언Y,
        "z": Number 쿼터니언Z,
        "w": Number 쿼터니언W
    }, {
        "x": Number 가속도X,
        "y": Number 가속도Y,
        "z": Number 가속도Z
    }
]
```

### `geto`
```
[{
    "type": String 감지된 물체의 타입
    "v": [Number, Number] 물체의 위치를 표현하는 벡터
}]
```

## 송신 이벤트 (클라이언트 -> 서버)
### `putq`
서버가 클라이언트로부터 쿼터니언 및 가속도를 받는 이벤트
```
[
    {
        "x": Number 쿼터니언X,
        "y": Number 쿼터니언Y,
        "z": Number 쿼터니언Z,
        "w": Number 쿼터니언W
    }, {
        "x": Number 가속도X,
        "y": Number 가속도Y,
        "z": Number 가속도Z
    }
]
```

### `puto`
서버가 클라이언트로부터 사물 정보를 받는 이벤트
```
[
    {
        "dist": Number 카메라가 사물로부터 떨어진 거리,
        "px": Number 감지된 오브젝트가 화면 중심점에서로부터 떨어진 거리
        "type": String 물체의 종류
    }
]
```
