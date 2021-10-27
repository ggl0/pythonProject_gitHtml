import os
from datetime import date

isDebug = True
allType = ['type1','type2','type3']

def getTDate():
    todayDate = date.today()
    todayDate = str(todayDate).replace("-","")
    return todayDate


def spaceStr(spNum):
    spaceS = " "
    if spNum > 1:
        for i in range(spNum):
            spaceS = spaceS + " "
    return spaceS

def htmlFormatS():
    htmlStrList = ["<html> \n",
                   spaceStr(1) + "<head> \n",
                     spaceStr(2) + "<title> \n", spaceStr(2) + "</title> \n",
                   spaceStr(1) + "</head> \n",
                   spaceStr(1) + "<body> \n", spaceStr(1) + "</body> \n",
                   "</html> \n"]
    return htmlStrList

def writeFile(dataStr,fileName):
    writeFile = open(fileName, 'a', encoding='UTF-8')
    writeFile.write(dataStr)
    writeFile.close()


def getHtmlistByType(hType,isFullath,rmPathStr):
    dirPath = "./hisBBands" + "/" + hType + "/"
    listFiles = list()
    if os.path.isdir(dirPath):
        if isDebug: print("Dir ", dirPath, " is existing!!!")
        listFiles = os.listdir(dirPath)
    if isFullath:
        listFullPath = list()
        for i in range(len(listFiles)):
            renameDirPath = dirPath.replace(rmPathStr,'')
            fullStr = renameDirPath + listFiles[i]
            listFullPath.append(fullStr)
        listFiles = listFullPath
        del listFullPath
    return listFiles

def getNumStr(fullPath):
    strL = fullPath.split("/")
    strLl = len(strL)
    num = strL[strLl-1]
    num = num.replace(".html","")
    #if isDebug: print(num)
    return num

def wLeftPage(dateStr_,typeStr='type1'):
    fileName = typeStr + '_left' + dateStr_ + '.html'
    writeTo = 'hisBBands/'
    savePath = writeTo + fileName
    for i in range(len(htmlFormatS())):
        writeFile(htmlFormatS()[i],savePath)
        if "<body>" in htmlFormatS()[i]:
            fullPathStr = getHtmlistByType(typeStr, True, writeTo)
            for k in range(len(fullPathStr)):
                bodyStr = spaceStr(2) + '<p><a href="' + fullPathStr[k] + '" target="right">' + getNumStr(fullPathStr[k]) + '</a></p>' + '\n'
                writeFile(bodyStr,savePath)

def wTopPage(dateStr_):
    fileName = './' + 'hisBBands/' + 'mainTop_' + dateStr_ + '.html'
    for i in range(len(htmlFormatS())):
        writeFile(htmlFormatS()[i], fileName)
        if "<title>" in htmlFormatS()[i]:
            titleStr = spaceStr(3) + "Type List \n"
            writeFile(titleStr, fileName)
        elif "<body>" in htmlFormatS()[i]:
            bodyStr = spaceStr(2) + '<div id="tabTitle"> \n' \
                        + spaceStr(3) + '<div id="id1"><a href="type1_left' + getTDate() + '.html" target="left">Type1</a></div> \n' \
                        + spaceStr(3) + '<div id="id2"><a href="type2_left' + getTDate() + '.html" target="left">Type2</a></div> \n' \
                        + spaceStr(3) + '<div id="id3"><a href="type3_left' + getTDate() + '.html" target="left">Type3</a></div> \n' \
                        + spaceStr(2) + '</div> \n'
            writeFile(bodyStr, fileName)
        elif "</body>" in htmlFormatS()[i]:
            styleStr = spaceStr(1) + "<style> \n" \
                        + spaceStr(2) + "#tabTitle{ \n" \
                            + spaceStr(3) + "display: flex; \n" \
                            + spaceStr(3) + "justify-content: space-around; \n" \
                        + spaceStr(2) + "} \n" \
                        + spaceStr(1) + "</style> \n"
            writeFile(styleStr, fileName)

def defaultRpage():
    dRp = 'right.html'
    for i in range(len(allType)):
        dRpL = getHtmlistByType(allType[i], True, 'hisBBands/')
        if len(dRpL) > 0:
            dRp = dRpL[0]
            break
    return dRp

def defaultLPage(dateStr_):
    dLp = 'left.html'
    for i in range(len(allType)):
        dLpL = getHtmlistByType(allType[i], True, 'hisBBands/')
        if len(dLpL) > 0:
            dLp = allType[i] + '_left' + dateStr_ + '.html'
            break
    return dLp

def wMainPage(dateStr_):
    ddRp = defaultRpage()
    ddLp = defaultLPage(dateStr_)
    fileName = './' + 'hisBBands/' + 'mainPage_' + dateStr_ + '.html'
    for i in range(len(htmlFormatS())):
        #change to frameset from body
        if "body>" in htmlFormatS()[i]:
            frameStr = spaceStr(1) + '<frameset rows="5%,*"> \n' \
                        + spaceStr(2) + '<frame src="mainTop_' + dateStr_ + '.html"></frame> \n' \
                        + spaceStr(2) + '<frameset cols="3%,*">' \
                            + spaceStr(3) + '<frame name="left" src="' + ddLp + '"></frame> \n' \
                            + spaceStr(3) + '<frame name="right" src="' + ddRp + '"></frame> \n' \
                        + spaceStr(2) + '</frameset>' \
                        + spaceStr(1) + '</frameset> \n'
            writeFile(frameStr, fileName)
        else:
            writeFile(htmlFormatS()[i], fileName)
        if "<title>" in htmlFormatS()[i]:
            titleStr = spaceStr(3) + "Full Page \n"
            writeFile(titleStr, fileName)

def clearHtmlFile(targetDir):
    listHtml = os.listdir(targetDir)
    for i in range(len(listHtml)):
        if '.html' in listHtml[i]:
            fullFName = targetDir + '/' + listHtml[i]
            if isDebug: print('sss=',fullFName)
            os.remove(fullFName)

def wAllHtmlPage():
    clearHtmlFile('./hisBBands')
    wLeftPage(getTDate(),'type1')
    wLeftPage(getTDate(),'type2')
    wLeftPage(getTDate(),'type3')
    wTopPage(getTDate())
    wMainPage(getTDate())

if __name__ == '__main__':
    wAllHtmlPage()