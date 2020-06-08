import Image_Downloader

FILENAME = "List.txt"
VERBOS = True
done = False
if __name__ == "__main__":
    while not done:
        queueFile = open(FILENAME, "r")
        download_Queue = queueFile.readlines()
        queueFile.close()

        totalNumber = 0
        doneList = []
        
        remain = True

        #첫번째 주소 불러오기
        if len(download_Queue) == 0:
            remain = False
        else:
            current = download_Queue.pop(0)

        while remain:
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
                remain = False
                break

            print("Remaining " + str(len(Updated_Queue)) + " item(s).")
            current = Updated_Queue.pop(0)

        print("Done! Total: " + str(totalNumber) + " Manga.")
        a = input("r to redownload: ")
        if not a.startswith("r"):
            done = True
    Image_Downloader.driver.close()