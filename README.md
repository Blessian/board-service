# User boad Service



## 👋🏻 팀원 및 업무분담

</br>

## ⏳ 개발 기간
**2022.09.06 ~ 2022.09.07**

</br>
  
## 🖥️ 프로젝트

#### 프로젝트 설명

1. 사용자는 게시글을 올릴 수 있습니다.
1. 게시글은 제목과 본문으로 구성됩니다.
2. 제목은 최대 20 자, 본문은 200 자로 서버에서 제한해야 합니다.
3. 제목과 본문 모두 이모지가 포함될 수 있습니다.
2. 사용자는 게시글을 올릴 때 비밀번호를 설정할 수 있습니다. 추후 본인이 작성한 게시물에
비밀번호 입력 후 수정, 삭제할 수 있습니다.
1. 회원 가입, 로그인 없이 비밀번호만 일치하면 수정, 삭제가 가능합니다.
2. 비밀번호는 데이터베이스에 암호화 된 형태로 저장이 되어야 합니다.
3. 비밀번호는 6 자 이상이어야 하고, 숫자 1 개 이상 반드시 포함 되어야 합니다.
3. 모든 사용자는 한 페이지 내에서 모든 게시글을 최신 글 순서로 확인할 수 있습니다



<br/>

## 🧹 사용된 기술
- **Back-End** : Python, Django, Django REST framework
, Pandas
- **ETC** : Git, Github

<br>

## ⚙️ ERD
<img width="608" alt="image" src="https://user-images.githubusercontent.com/95831345/188399711-3305c014-9a1f-4485-ad1f-240c75bd0213.png">
</div>

</br>
## 🛠 Unit test

- 핵심 기능이라 판단한 **게시판**과 **통계 분석 api** 에 대해 **총 29개**의 테스트 코드를 작성 ( 게시판테스트 18개, 통계 분석 테스트 11개 )

![image](https://user-images.githubusercontent.com/83492367/188457691-4f931106-3ddb-44ee-8e55-38c96b9c061e.png)

</br>

## ✍🏻 프로젝트 구현사항

- **유저 로그인 / 회원가입 / 회원탈퇴 API**
    -  회원가입 시 생성되는  `DRF auth token`을 바탕으로 **로그인 시 유효성 검증**
    -  회원탈퇴 시 DB에서 직접 삭제되지 않고 `is_active`를 비활성화함으로써 **soft delete** 구현

- **자유게시판, 공지사항, 운영자게시판 API**
   - 각 게시판의 list view에서는 `수정시간` 필드 제외 
   - `제목`과 `본문` 내용을 토대로 **검색 기능** 구현
   - `cusor pagination`을 이용한 **pagination** 구현


- **권한 부여**
	- 회원  ( `사용자(User)`, `관리자(Staff)`, `운영자(SuperUser)` )
   		- 회원 가입은 누구나 가능하지만, 회원 목록은 관리자만 접근 가능
   		- 회원 정보 수정은 본인만 가능
   		- 관리자 임명은 관리자만 접근 가능
   		- 회원 탈퇴는 관리자와 본인 접근 가능

   - 게시판
		- 자유게시판 : 작성자와 관리자는 게시글에 대한 전체 액세스 권한, 운영자는 게시판을 삭제하되 편집 할 수 없음
		- 공지사항 : 운영자와 관리자는 게시글에 대한 전체 액세스 권한, 사용자는 읽기 권한만 가짐
		- 운영자 게시판 : 운영자와 관리자는 게시글에 대한 전체 액세스 권한, 사용자는 모든 권한을 가지지 않음 (읽기 불가)




- **사이트 이용 통계 집계 API**
	-  **Pandas**를 이용하여 남 · 여 / 나이 / 접속시간을 이용한 다양한 통계 구현
	-  DAU, WAU, MAU 서비스 측정을 위해 전체 회원 중 **집계 기간 내 로그인한 사용자 비율** 구현
    -  구현한 통계 사항들
    
  		- 전체 회원 중 집계 기간 내 로그인한 사용자 비율
  		- 집계 기간 내 로그인한 사용자의 성별 비율
  		- 집계 기간 내 로그인한 사용자의 나이대 비율
  		- 집계 기간 내 로그인한 사용자의 성별과 나이대 비율
  		- 집계 기간 내 로그인한 사용자 유저의 나이대 비율
  		- 집계 기간 내 로그인한 사용자 유저의 나이대 비율
  		- 집계 기간 내 로그인한 사용자의 매 시간 별 비율

