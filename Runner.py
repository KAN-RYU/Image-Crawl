import Image_Downloader

queueFile = open("List.txt", "r")
download_Queue = queueFile.readlines()
queueFile.close()
totalNumber = len(download_Queue)

while True:
    #첫번째 주소 불러오기
    current = download_Queue.pop(0)

    #이미지 다운로드

    #큐 업데이트
    queueFile = open("List.txt", "r")
    Updated_Queue = queueFile.readlines()
    print(Updated_Queue)
    queueFile.close()

    if len(Updated_Queue) == 0:
        break

    if Updated_Queue[0] == current:
        Updated_Queue.pop(0)
        
        queueFile = open("List.txt", "w")
        for s in Updated_Queue:
            queueFile.write(s + '\n')
        
        queueFile.close()

