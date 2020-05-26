def short_type(obj):
    s = str(type(obj))
    s = s.split('.')
    s = s[len(s)-1]
    s = s.replace('<class', '')
    s = s.replace('\'', '')
    s = s.replace('>', '')
    s = s.strip()
    return s

    
if __name__ == '__main__':
    from pyprone.core import PrObj

    print(short_type(1))
    print(short_type(PrObj('abc')))
