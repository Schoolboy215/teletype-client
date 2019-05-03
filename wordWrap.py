def correctWidth (inputString, width):
    stringLength = len(inputString)
    finalString = ""
    currentIndex = 0
    lineStart = 0
    lastSpaceIndex = 0

    breakList = ["."]

    while (inputString[stringLength - 1] == " "):
        stringLength -= 1
    
    while (currentIndex < stringLength):
        if (inputString[currentIndex] == "\n" and currentIndex != stringLength-1):
            finalString += "\n"
            currentIndex += 1
            lineStart = currentIndex
            
        if (currentIndex - lineStart >= width):
            if (inputString[currentIndex] == " "):
                finalString += "\n"
                while (inputString[currentIndex] == " "):
                    currentIndex += 1
                lineStart = currentIndex
            elif (lastSpaceIndex > lineStart):
                for i in range (lastSpaceIndex, currentIndex):
                    finalString = finalString[:-1]
                if (inputString[lastSpaceIndex] in breakList):
                    finalString += inputString[lastSpaceIndex]
                finalString += "\n"
                currentIndex = lastSpaceIndex + 1
                lineStart = currentIndex
            else:
                finalString += "\n"
                lineStart = currentIndex       
        if (inputString[currentIndex] == " " and currentIndex != lineStart):
            lastSpaceIndex = currentIndex
            finalString += " "
            currentIndex += 1
        elif (inputString[currentIndex] == " " and currentIndex == lineStart):
            currentIndex += 1
            lineStart += 1
        elif (inputString[currentIndex] in breakList):
            lastSpaceIndex = currentIndex
            finalString += inputString[currentIndex]
            currentIndex += 1
        else:
            finalString += inputString[currentIndex]
            currentIndex += 1

    return finalString


