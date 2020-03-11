import Image_Downloader
import time

FILENAME = "List.txt"
VERBOS = True

if __name__ == "__main__":
    queueFile = open(FILENAME, "r")
    download_Queue = queueFile.readlines()
    queueFile.close()

    totalNumber = 0
    doneList = []

    #첫번째 주소 불러오기
    current = download_Queue.pop(0)
    Image_Downloader.driver.get(current)
    time.sleep(10)

    while True:
        totalNumber += 1

        #이미지 다운로드
        if not (current in doneList):
            Image_Downloader.download_manga(current, VERBOS)
            doneList.append(current)

        #큐 업데이트
        queueFile = open(FILENAME, "r")
        Updated_Queue = queueFile.readlines()
        queueFile.close()

        if Updated_Queue[0] == current:
            Updated_Queue.pop(0)
            
            queueFile = open(FILENAME, "w")
            for s in Updated_Queue:
                queueFile.write(s)
            
            queueFile.close()

        if len(Updated_Queue) == 0:
            break

        print("Remaining " + len(Updated_Queue) + " item(s).")
        current = Updated_Queue.pop(0)

    print("Done! Total: " + totalNumber + " Manga.")