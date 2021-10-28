# 엘리스AI트랙 2기 개인프로젝트
### 프로젝트 주제
- 도서관 대출 서비스
### 기간
- 2021.08.16 ~ 2021.08.27 (2주)
### 기술 스택
- Flask, SQLAlchemy, MySQL, Jinja2

### 프로젝트 실행
/library Flask run

### [구현 기능](https://github.com/Moon-Ji/LibraryLoan/wiki/%EA%B5%AC%ED%98%84-%EA%B8%B0%EB%8A%A5)

### 디렉토리 구조
```
library
    ├───model
    │   └───model.py        # 유저, 책, 리뷰, 대여기록 테이블
    ├───static
    │   ├───css
    |   |   └───style.css
    │   └───image
    │       ├───book_img
    │       └───icon
    ├───templates
    |   |   _navbar.html    # 네비게이션 바 
    |   |   base.html       # 페이지 기본 특
    |   |   info.html       # 책 상세 페이지
    |   |   log.html        # 대여 기록 페이지
    |   |   login.html      # 로그인 페이지
    |   |   main.html       # 메인 페이지
    |   |   return.html     # 책 반납 페이지
    |   └───signup.html     # 회원가입 페이지
    ├───view
    |   |   api.py          # 책 대여, 반납, 리뷰작성 API
    │   └───user_api.py     # 로그인 API
    |   app.py              # 실행 파일
    └───load_data.py        # 책 데이터 load 파일
```