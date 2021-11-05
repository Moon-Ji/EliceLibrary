# 엘리스AI트랙 2기 개인프로젝트
### 프로젝트 주제
- 도서관 대출 서비스
### 기간
- 2021.08.16 ~ 2021.08.27 (2주)
### 기술 스택
<img src="https://img.shields.io/badge/-Flask-black?style=for-the-badge&logo=flask&logoColor=white"/> <img src="https://img.shields.io/badge/-mysql-4479A1?style=for-the-badge&logo=mysql&logoColor=white"/> <img src="https://img.shields.io/badge/-jinja-B41717?style=for-the-badge&logo=jinja&logoColor=white"/> <img src="https://img.shields.io/badge/html-E34F26?style=for-the-badge&logo=html5&logoColor=white"> <img src="https://img.shields.io/badge/css-1572B6?style=for-the-badge&logo=css3&logoColor=white">


------------------------------------------------------------
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

------------------------------------------------------------
### 둘러보기
<details>
<summary>로그인</summary>
<div markdown="1"> 
      
![login](https://user-images.githubusercontent.com/83294396/140542444-4721a11d-47b2-4f79-8fcc-e1f0a1f26444.PNG)

</div>
</details>

<details>
<summary>회원가입</summary>
<div markdown="1">       
![register](https://user-images.githubusercontent.com/83294396/140542597-1e6de72b-9b32-401d-990d-99a3bb5383d2.PNG)
</div>
</details>

<details>
<summary>메인 페이지</summary>
<div markdown="1">       

![main2](https://user-images.githubusercontent.com/83294396/140542718-803e5db6-d491-4005-bfa7-8439b6ac3684.PNG)

</div>
</details>

<details>
<summary>반납하기</summary>
<div markdown="1">       

![return_book](https://user-images.githubusercontent.com/83294396/140542792-1b0761aa-b37e-4000-8c3a-93142d0ad88c.PNG)

</div>
</details>

<details>
<summary>대여기록</summary>
<div markdown="1">       

![log](https://user-images.githubusercontent.com/83294396/140542887-e47ce8d6-142d-4b4c-b1c4-3664e23bf700.PNG)

</div>
</details>

<details>
<summary>책 상세 페이지</summary>
<div markdown="1">       

![detail](https://user-images.githubusercontent.com/83294396/140542967-ef54f9b1-197f-4323-8eac-8f17842c5930.PNG)

</div>
</details>

------------------------------------------------------------
