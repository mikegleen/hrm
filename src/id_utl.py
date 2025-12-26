import re


def _splitid(idstr: str, m: re.Match) -> (str, int, int, int):
    """
    Subroutine to function expand_one_idnum.

    Handle the case of JB121-24.

    :return: prefix = "JB1"
             variablepart: int = 21
             intsecondidnum: int = 24
             len(variablepart) = 2
    """
    if m[3] and m[1] != m[3]:
        raise ValueError(f'{idstr} first "{m[1]}" and second "{m[3]}"    prefix must match')
    prefix = m[1]  # will be updated later if 2nd # is shorter than 1st #
    lenprefix = len(prefix)
    firstidnum = m[2]
    intsecondidnum = int(m[4])  # the numbers after the '-'
    # lenfirstid will change if the second # is shorter than the first
    lenfirstid = len(firstidnum)
    lenlastid = len(m[4])
    lenfixedpart = max(lenfirstid - lenlastid, 0)
    # In a case like SH21-4, the fixed part will be the leading part of the
    # number, in this case "2".
    fixedpart = idstr[lenprefix:lenprefix + lenfixedpart]
    variablepart = idstr[lenprefix + lenfixedpart:lenprefix + lenfirstid]
    prefix += fixedpart
    intvariablepart = int(variablepart)
    if intvariablepart >= intsecondidnum:
        raise ValueError(f'{idstr} first number must be less than last number')
    return prefix, intvariablepart, intsecondidnum, len(variablepart)


def _expand_one_idnum(idstr: str) -> list[str]:
    jlist = []
    idstr = ''.join(idstr.split())  # remove all whitespace
    if '-' in idstr or '/' in idstr:  # if ID is actually a range like JB021-23
        if '&' in idstr:
            raise ValueError(f'Bad accession number list: cannot contain both'
                             f' "-" and "&": "{idstr}"')
        if m := re.match(r'''(.+?)  # prefix like "JB" or "LDHRM.2024."
                             (\d+)  # number up to the separator
                             [-/]   # the separator can be "-" or "/"
                             (.*?)  # possibly a prefix on the second part
                             (\d+)$ # the trailing number
                             ''', idstr, flags=re.VERBOSE):
            prefix, num1, num2, lenvariablepart = _splitid(idstr, m)
            try:
                for suffix in range(num1, num2 + 1):
                    newidnum = f'{prefix}{suffix:0{lenvariablepart}}'
                    jlist.append(newidnum)
            except ValueError:
                raise ValueError(f'Bad accession number, contains "-" but not '
                                 f'well formed: {m.groups()}')
        else:
            raise ValueError('Bad accession number, failed pattern match:', idstr)
    elif '&' in idstr:
        parts = idstr.split('&')
        head = parts[0]
        jlist.append(head)
        m = re.match(r'(.+?)(\d+)$', head)
        # prefix will be everything up to the trailing number. So for:
        #   JB001 -> JB
        #   LDHRM.2023.1 -> LDHRM.2023.
        prefix = m[1]
        for tail in parts[1:]:
            if not tail.isnumeric():
                raise ValueError(f'Extension numbers must be numeric: "{idstr}"')
            jlist.append(prefix + tail)

    else:
        # It's just a single accession number.
        jlist.append(idstr)
    return jlist


def expand_idnum(idnumstr: str) -> list[str]:
    """
    Expand an idnumstr to a list of idnums.
    :param idnumstr: (See expand_one_idnum for the definition of idstr)
        idnumstr ::= idstr | idnumstr,idstr
    :return: list of idnums
    """
    idstrlist = idnumstr.split(',')
    rtnlist = []
    for idstr in idstrlist:
        # _expand_one_idnum returns a list. Append the members of that list.
        rtnlist += _expand_one_idnum(idstr)
    return rtnlist
