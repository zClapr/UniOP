def floatRange(start, end, step):
    result = []
    tempVar = start

    while tempVar <= end:
        result.append(tempVar)
        tempVar += step
    
    return result