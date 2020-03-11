import Image_Downloader
import time

FILENAME = "List.txt"

queueFile = open(FILENAME, "r")
download_Queue = queueFile.readlines()
queueFile.close()
totalNumber = len(download_Queue)
doneList = []

#첫번째 주소 불러오기
current = download_Queue.pop(0)

while True:

    #이미지 다운로드
    if not (current in doneList):
        print(current)
        time.sleep(5)
        doneList.append(current)

    #큐 업데이트
    queueFile = open(FILENAME, "r")
    Updated_Queue = queueFile.readlines()
    print(Updated_Queue)
    queueFile.close()

    if Updated_Queue[0] == current:
        Updated_Queue.pop(0)
        
        queueFile = open(FILENAME, "w")
        for s in Updated_Queue:
            queueFile.write(s)
        
        queueFile.close()

    if len(Updated_Queue) == 0:
        break

    current = Updated_Queue.pop(0)

print("Done!")