import urllib.request
import os
import sys
from PIL import Image

#실행창의 로그 클리어
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

#각종 에러 처리
def error(code):
    clear()
    try:
        sys.exit(1)  # 강제 종료
    except SystemExit:
        print(f"프로그램 실행 도중 오류가 발생했습니다. (오류코드: {code})")
        print("errors.txt에서 해당 오류코드의 내용을 확인해 주세요.")
        print("Enter 키를 눌러 창을 닫으세요...")
        input()  # 사용자 입력 대기
        sys.exit(1)

# 파일의 현재 실행 위치 반환
def get_current_path():
    if getattr(sys, 'frozen', False):  # 프로그램이 .exe로 변환되었는지 확인
        # 실행 중인 .exe 파일의 디렉토리 경로 가져오기
        exe_path = os.path.dirname(sys.executable)
    else:
        # 스크립트가 직접 실행 중일 경우 (__file__ 사용)
        exe_path = os.path.dirname(os.path.realpath(__file__))

    return exe_path

# PNG 및 PDF 파일을 저장할 경로 반환
def get_folder_path(name):
    return os.path.join(get_current_path(), name)

# PNG 및 PDF 파일을 저장할 폴더 생성
def generate_folder(name: str):
    try:
        path = get_folder_path(name)
        os.mkdir(path)
    except:
        error(3)

# 입력된 링크에서 마지막 페이지 번호 추출
def extract_last_page(link):
    try:
        number = link.split("/")[-1].split(".")[0]
        if number.isdigit(): # 추출한 페이지 번호가 숫자인지 확인
            return int(number)
        else:
            raise ValueError("에러")
    except:
        error(1)

# 입력된 링크에서 페이지 번호를 제외한 기본 링크 추출
def extract_link(link):
    try:
        base_link = link.split(str(extract_last_page(link))+".png")[0][:-1]
        return base_link
    except:
        error(2)

# PNG파일 다운로드
def download(link, name):
    # 총 페이지수 추출
    max_page = extract_last_page(link)
    # 저장 폴더 생성
    generate_folder(name)
    try:
        for i in range(1,max_page+1):
            download_path = extract_link(link) + "/" + str(i) + ".png"
            save_path = get_folder_path(name) + "/" + str(i) + ".png"
            urllib.request.urlretrieve(download_path, save_path)
            print(f"> {download_path}") #로그출력
    except:
        error(4)

# PNG파일을 PDF파일로 변환
def images_to_pdf(image_folder, output_pdf):
    # 폴더 내의 이미지 파일 가져오기
    image_files = [f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff'))]

    if not image_files:
        print("지정된 폴더에 이미지 파일이 없습니다.")
        return

    #이미지를 페이지 번호로 정렬
    image_files = sorted(image_files, key=lambda x: int(x.split('.')[0]))

    # 이미지를 열고 RGB 모드로 변환
    images = []
    for file in image_files:
        img_path = os.path.join(image_folder, file)
        img = Image.open(img_path).convert("RGB")  # PDF 호환성을 위해 RGB 모드로 변환
        images.append(img)


    # 이미지를 PDF로 저장
    images[0].save(output_pdf, save_all=True, append_images=images[1:])  # 첫 번째 이미지를 기반으로 PDF 생성
    print(f"PDF가 성공적으로 저장되었습니다: {output_pdf}")
    input("\nEnter 키를 입력하면 초기 화면으로 이동합니다...")

### 프로그램 시작점 ###
while True:
    # 안내메세지
    clear()
    print("강릉원주대 해람인의 e참뜰에서 다운로드가 불가능한 수업자료를 PDF로 저장하는 프로그램입니다.")
    print("프로그램 사용 전, 반드시 readme.txt파일을 읽고 사용법을 숙지해 주시기 바랍니다.")
    print("대부분의 오류발생은 errors.txt에서 해당 오류 코드의 내용을 확인함으로서 해결이 가능합니다.")
    input("\nEnter 키를 눌러 다음으로...")
    clear()

    # 이미지 링크 입력
    print("수업자료의 마지막 이미지 링크를 입력해 주세요.")
    link = input(">>> ")
    # 저장 폴더명 입력
    print("\n저장하실 폴더의 이름을 입력해 주세요. (해당 경로에 없는 폴더 이름이어야 합니다)")
    name = input(">>> ")
    clear()

    # 이미지 다운로드
    print("다운로드를 시작합니다...")
    download(link, name)

    # PDF변환
    clear()
    print("PDF로 변환중...")
    try:
        images_to_pdf(get_folder_path(name), get_folder_path(name) + f"/{name}.pdf")
    except:
        error(5)

