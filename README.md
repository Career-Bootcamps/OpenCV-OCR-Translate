# OpenCV-OCR-Translate

OpenCV라는 기술은 마치 사람이 눈으로 보는 영상(또는 이미지)에 존재하는 사물을 인식하는 것과 같은 역할을 소프트웨어적으로 처리해주는 기술을 말합니다. 예를 들어, 자동차의 자율 주행에서 카메라로 들어오는 영상 속 모든 사물을 파악하고 그 결과로 운전의 방향과 속도 등을 결정하는 동작에서 OpenCV는 핵심 기술로 사용됩니다. 

본 프로젝트에서는 OpenCV 기술을 활용하여 중국의 쇼핑몰에 있는 상품을 국내 쇼핑몰에 올려서 팔고 싶은 구매 대행 사업자들이 편하게 중국어가 포함된 상세 페이지의 상품 이미지(그림 파일)를 한국어로 쉽게 번역할 수 있도록 도와주는 소프트웨어를 개발하는 것을 목표로 합니다.

## 개발환경 설정

```
pip install opencv-python
pip install opencv-python-headless
pip install easyocr
pip install pillow==9.5.0
pip install ninja
pip install googletrans==4.0.0-rc1
```

<details>
  <summary>버전 상세</summary>
  
  - opencv: 4.6.0
  - easyocr: 1.7.0
  - pillow: 9.5.0
  - ninja: 1.10.2
  - googletrans: 4.0.0-rc1
</details>


## 업데이트 내역
* v10

## 목차
* [팀원 소개](#팀원-소개)
* [프로젝트 소개](#프로젝트-소개)
  * [기획 배경](#기획-배경)
  * [프로젝트 목표](#프로젝트-목표)
  * [개발 핵심 개념](#개발-핵심-개념)
  * [개발일정 및 개발환경](#개발일정-및-개발환경)
* [기능 소개](#기능-소개)
  * [Data Manager](#Data-Manager)
  * [Top Frame](#Top-Frame)
  * [지우기](#지우기)
  * [쓰기](#쓰기)
  * [이미지 편집](#이미지-편집)
  * [모자이크](#모자이크)
* [결과](#결과)
  * [결과 시연](#결과-시연)
  * [기대 효과](#기대-효과)
  * [시행착오](#시행착오)
  * [소감](#소감)

## 팀원 소개
<a id="팀원-소개"></a>
<details>
  <summary>
   팀원 소개
  </summary>
 
![슬라이드2](https://github.com/user-attachments/assets/7e85fb30-7328-4b71-8088-80f157ece6c1)

| 이름    | 역할                                                  |
| ------- | ------------------------------------------------------------------ |
| 정윤정   | 지우기 기능 담당. 이미지에서 텍스트 인식, 인식된 텍스트 출력, 텍스트 선택 후 지우기 기능.       |
| 김주영   | 이미지 편집 기능 담당. 수치 조정 바를 통해 이미지 밝기 및 대비 조절 기능.                     |
| 황지원   | 쓰기 기능 담당. 인식된 텍스트 한국어로 번역, 번역된 텍스트 수정, 글씨체와 글씨 크기 및 색상 변경 기능.            |
| 정은서   | 모자이크 기능 담당. 이미지에서 얼굴 인식, 인식된 얼굴 목록 출력, 선택적 모자이크 및 모자이크 정도 조절 기능.           |

</details>

## 프로젝트 소개
<a id="기획-배경"></a>
<details>
  <summary>
   기획 배경
  </summary>
  
  ![슬라이드5](https://github.com/user-attachments/assets/850fa2aa-abe6-4bf0-bda9-db652813ad89)
  ![슬라이드6](https://github.com/user-attachments/assets/e058c501-d96a-4657-8a95-747484455fb4)
  
</details>

<a id="프로젝트-목표"></a>
<details>
  <summary>
    프로젝트 목표  
  </summary>
  
  ![슬라이드7](https://github.com/user-attachments/assets/62864c1f-3120-4e9b-8734-297f5caaa1a1)
  ![슬라이드8](https://github.com/user-attachments/assets/4bef4e95-b442-45b4-9fda-a13c5a9ed78a)
  
</details>

<a id="개발-핵심-개념"></a>
<details>
  <summary>
    개발 핵심 개념
  </summary>
  
  ![슬라이드9](https://github.com/user-attachments/assets/79a54c8f-71fa-4937-b927-a6e7513d4b19)
  ![슬라이드10](https://github.com/user-attachments/assets/3b5e5409-09c3-43ed-a842-e1830256e341)
  ![슬라이드11](https://github.com/user-attachments/assets/2ddd06f8-cc4a-4fd1-809c-669b953d6bfa)
  ![슬라이드12](https://github.com/user-attachments/assets/4dca718e-4c21-47b2-9448-5a1af5754b3c)
  ![슬라이드13](https://github.com/user-attachments/assets/cadb7cd7-ca29-4a99-9dc0-915e44a0f90b)
  ![슬라이드14](https://github.com/user-attachments/assets/b170fb5c-2911-4671-bc10-4e105ba7c718)
  ![슬라이드15](https://github.com/user-attachments/assets/89fdd612-22b5-4239-a1e5-0091dac3eae3)
  ![슬라이드16](https://github.com/user-attachments/assets/7ed5eb88-92fb-41e4-8fe6-d6692a2aa8e4)
  ![슬라이드17](https://github.com/user-attachments/assets/46d80694-0b97-4351-94d0-e6c81ac9c518)
  ![슬라이드18](https://github.com/user-attachments/assets/f86364d8-8e36-484c-a779-ca83ec563f22)
  
</details>

<a id="개발일정-및-개발환경"></a>
<details>
  <summary>
    개발일정 및 개발환경
  </summary>
  
  ![슬라이드19](https://github.com/user-attachments/assets/72c86466-17e5-4591-93a9-64a028818b65)
  ![슬라이드20](https://github.com/user-attachments/assets/2b534570-9a2b-4a0c-a79a-5b4f7b8a599b)
  ![슬라이드21](https://github.com/user-attachments/assets/8dfb36ad-a460-455d-bd3b-2fd214e960c1)
  
</details>

## 기능 소개
<a id="Data-Manager"></a>
<details>
  <summary>
   Data Manager
  </summary>
  
  ![슬라이드23](https://github.com/user-attachments/assets/2a4b269a-e9e2-411a-bd9f-3b2915e202e9)
  ![슬라이드24](https://github.com/user-attachments/assets/0df869fb-7187-4779-ab0b-f6d046047217)
  
</details>

<a id="Top-Frame"></a>
<details>
  <summary>
   Top Frame
  </summary>
  
  ![슬라이드25](https://github.com/user-attachments/assets/81c46ed4-904f-46a3-9489-bea90e8d07dc)
  ![슬라이드26](https://github.com/user-attachments/assets/e3d9562c-381d-4e01-bb15-4548fed44ee6)
  ![슬라이드27](https://github.com/user-attachments/assets/86735cc7-e52b-4528-b0ad-23a9d5a81fd2)
  ![슬라이드28](https://github.com/user-attachments/assets/5d954d38-5267-48c5-a2b5-24e07570f2ad)
  ![슬라이드29](https://github.com/user-attachments/assets/296b1115-ecc0-4d94-891f-f95add0c6669)
  
</details>

<a id="지우기"></a>
<details>
  <summary>
   지우기
  </summary>
  
  ![슬라이드30](https://github.com/user-attachments/assets/3a2e5438-8839-496c-98a7-1d6fcf058a8f)
  ![슬라이드31](https://github.com/user-attachments/assets/3eb7788e-b2d0-415b-ae78-e85cf457dec2)
  ![슬라이드32](https://github.com/user-attachments/assets/110d8ce9-529e-45c2-83e2-61443e026129)
  
</details>

<a id="쓰기"></a>
<details>
  <summary>
   쓰기
  </summary>
  
  ![슬라이드33](https://github.com/user-attachments/assets/40b17ced-e2fe-4202-b461-89ccaba069af)
  ![슬라이드34](https://github.com/user-attachments/assets/adffc7b7-6a72-40d7-a2ed-0976b06aa8b4)
  ![슬라이드35](https://github.com/user-attachments/assets/a9a38b3b-1fd7-4a7f-a242-7444794ffd80)
  
</details>

<a id="이미지-편집"></a>
<details>
  <summary>
   이미지 편집
  </summary>
  
  ![슬라이드36](https://github.com/user-attachments/assets/984790da-ae16-4861-8f78-d7a3711f13d8)
  ![슬라이드37](https://github.com/user-attachments/assets/55bcad68-558f-491d-9e39-284dbeb24e5a)
  ![슬라이드38](https://github.com/user-attachments/assets/93e08644-fa64-47d5-9c59-339da6df5e77)
  
</details>

<a id="모자이크"></a>
<details>
  <summary>
   모자이크
  </summary>
  
  ![슬라이드39](https://github.com/user-attachments/assets/5b737c92-dfcc-4941-bca6-11a0c325ef9b)
  ![슬라이드40](https://github.com/user-attachments/assets/127fbe4d-c75f-49b7-a6b0-8dcce668ebd9)
  ![슬라이드41](https://github.com/user-attachments/assets/15ed7646-8a73-4803-9329-0d509b1487af)
  ![슬라이드42](https://github.com/user-attachments/assets/46aeca9a-4553-4f75-9097-c49becc13fd7)
  ![슬라이드43](https://github.com/user-attachments/assets/5be7278e-2d49-4d1d-8ecc-49bc0f523cc3)
  
</details>

## 결과

<a id="결과-시연"></a>
<details>
  <summary>
   결과 시연
  </summary>
  ![시연 영상 썸네일](https://youtu.be/zIppXkwfIOs)
  
</details>

<a id="기대-효과"></a>
<details>
  <summary>
   기대 효과
  </summary>
  
  ![슬라이드47](https://github.com/user-attachments/assets/de210e83-9f9f-4764-9947-abce5599fd10)
  ![슬라이드48](https://github.com/user-attachments/assets/832d6010-57e5-477b-83c6-c5202294e424)
  
</details>

<a id="시행착오"></a>
<details>
  <summary>
   시행착오
  </summary>
  
  ![슬라이드49](https://github.com/user-attachments/assets/ccddc713-a09e-4859-8e9a-379efad6c25e)
  ![슬라이드50](https://github.com/user-attachments/assets/55eb15a7-ec68-4c52-bd55-9ce484f8a511)
  ![슬라이드51](https://github.com/user-attachments/assets/94f18e09-8db8-4dc3-bb0e-2a64347b55b5)
  ![슬라이드52](https://github.com/user-attachments/assets/90ac6fc6-a454-4fc7-a61c-5041cd6a6b5b)
  ![슬라이드53](https://github.com/user-attachments/assets/cf83fa79-1ecb-4143-9e6a-71f6c10344f5)
  ![슬라이드54](https://github.com/user-attachments/assets/6ecf354e-343b-4b43-a957-07e773c1afd3)
  
</details>

<a id="소감"></a>
<details>
  <summary>
   소감
  </summary>
  
  ![슬라이드55](https://github.com/user-attachments/assets/c81a2472-5797-4554-a6cb-1b43b7419b9a)
  ![슬라이드56](https://github.com/user-attachments/assets/3613e973-814d-46e4-964c-a2de2c493da3)
  ![슬라이드57](https://github.com/user-attachments/assets/0c562f4a-d6d0-4e0e-8a89-f2ee071f101b)
  
</details>
