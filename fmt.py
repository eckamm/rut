
_map = {
    5:"million",
    6:"billion",
    7:"trillion",
    8:"quadrillion",
    9:"quintillion",
    10:"sextillion",
    11:"septillion",
    12:"octillion",
    13:"nonillion",
    14:"decillion",
    15:"undecillion",
    16:"duodecillion",
    17:"tredecillion",
    18:"quattuordecillion",
    19:"quinquadecillion",
    20:"sedecillion",
    21:"septendecillion",
    22:"octodecillion",
    23:"novendecillion",
    24:"vigintillion",
    25:"unvigintillion",
    26:"duovigintillion",
    27:"tresvigintillion",
    28:"quattuorvigintillion",
    29:"quinquavigintillion",
    30:"sesvigintillion",
    31:"septemvigintillion",
    32:"octovigintillion",
    33:"novemvigintillion",
    34:"trigintillion",
    35:"untrigintillion",
    36:"duotrigintillion",
    37:"trestrigintillion",
    38:"quattuortrigintillion",
    39:"quinquatrigintillion",
    40:"sestrigintillion",
    41:"septentrigintillion",
    42:"octotrigintillion",
    43:"noventrigintillion",
    44:"quadragintillion",
}


def fmt(n):
    if type(n) not in (long, int, float):
        return n
    if type(n) in (long, int):
        s = "{:1,d}".format(n)
    elif type(n) is float:
        s = "{:1,.1f}".format(n)
    parts = s.split(",")
    if len(parts) <= 3:
        return s
    
    word = _map.get(len(parts))
    if word is not None:
        return "%s %s" % (",".join(parts[:3]), word)
    return s

    """
    6 aaa,bbb,ccc,ddd,eee,fff.234
    5 aaa,bbb,ccc,ddd,eee.234
    4 aaa,bbb,ccc,ddd.234   
    3 aaa,bbb,ccc.234
    2 aaa,bbb.234
    1 aaa.234
    """


