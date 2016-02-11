import string
from publicsuffix import PublicSuffixList
psl = PublicSuffixList()

def cutOutPorts(dm):
    colIdx = string.find(dm, ':')
    if colIdx>-1:
        dm = dm[:colIdx]
    return dm

def isIP(domain):
    parts = domain.split('.')
    try:
        return len(parts) == 4 and all(0 <= int(part) < 256 for part in parts)
    except Exception as e:
        return False

def getDomain(fqdn, freereg=False):
    fqdn=cutOutPorts(fqdn)
    parts = fqdn.split('.')
    if isIP('.'.join(parts[-4:])):
        return '.'.join(parts[-4:])
    dom = psl.get_public_suffix(fqdn)
    if not freereg:
        return dom
    else:
        if dom in freewr:
            dotIdx = string.rfind(fqdn[:string.index(fqdn,dom)-1],'.')
            if dotIdx==-1:
                return fqdn
            else:
                return fqdn[dotIdx+1:]
        else:
            return dom

def gettld(url):
    if '://' in url:
        url = url[string.index(url,'://')+3:]
    slashIdx = string.find(url,'/')
    if slashIdx > -1:
        return getDomain(url[:slashIdx])
    else:
        return getDomain(url)