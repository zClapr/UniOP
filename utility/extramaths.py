def floatRange(start, end, step):
    result = []
    tempVar = start

    while tempVar <= end:
        result.append(tempVar)
        tempVar += step
    
    return result

def closest(from_list:list, number:float):
    return float(from_list[
        min(
            range(len(from_list)), 
            key = lambda i: abs(float(list(from_list)[i])-number)
        )
    ])

def byteSimplify(bytes):
    b = float(bytes)
    KB = float(1024)
    MB = float(KB ** 2)
    GB = float(KB ** 3)
    TB = float(KB ** 4)

    if b < KB: return '{0} {1}'.format(b,'Bytes' if 0 == b > 1 else 'Byte')
    elif KB <= b < MB: return '{0:.2f} KB'.format(b/KB)
    elif MB <= b < GB: return '{0:.2f} MB'.format(b/MB)
    elif GB <= b < TB: return '{0:.2f} GB'.format(b/GB)
    elif TB <= b: return '{0:.2f} TB'.format(b/TB)