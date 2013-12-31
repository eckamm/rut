import math


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


def classic_fmt(n):
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


_map2 = {
    5:"million",        # 7-9           1,000,000 -         999,999,999     0-2 0      (digits-7)//3 + 5
    6:"billion",        # 10-12     1,000,000,000 -     999,999,999,999     3-5 1
    7:"trillion",       # 13-15 1,000,000,000,000 - 999,999,999,999,999     6-8 
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


"""
                   0.01 ->                      0.01
                   0.12 ->                      0.12
                   1.05 ->                      1.05
                  99.23 ->                     99.2
                 198.60 ->                    199
                1234.11 ->                  1,234
               12345.11 ->                 12,345
              123456.11 ->                123,456
             1234567.11 ->              1,234,567     1.234456 million
            12345678.11 ->             12,345,678    12.345678 million
           123456789.11 ->            123,456,789   123.456789 million
          1234567890.11 ->          1,234,567,890     1.234567 billion
         12345678901.11 ->         12,345,678,901    12.345678 billion
        123456789012.11 ->        123,456,789,012   123.456789 billion    len(num) < len(word)
       1234567890123.11 ->      1,234,567,890,123     1.234567 trillion   len(num) == len(word)
      12345678901234.11 ->     12,345,678,901,234    12.345678 trillion   len(num) > len(word)
     123456789012345.11 ->    123,456,789,012,345   123.456789 trillion
    1234567890123456.11 ->  1,234,567,890,123,456     1.234567 quadrillion

import math
millnames=['','Thousand','Million','Billion','Trillion']
def millify(n):
    n = float(n)
    millidx=max(0,min(len(millnames)-1,
                      int(math.floor(math.log10(abs(n))/3))))
    return '%.0f %s'%(n/10**(3*millidx),millnames[millidx])
"""

def wordish_fmt(n):
    if n < 10:
        return "%.2f" % n
    elif n < 100:
        return "%.1f" % n
    elif n < 1000000000000l:
         return "{:,.0f}".format(n)
    else:
        t = int(math.floor(math.log10(abs(n))/3))
        mapkey = t + 3
        digits = int(math.log10(n))
        word = _map.get(mapkey)
        if word:
            return "%.6f %s" % (float(n)/pow(10, t*3), word)
        else:
            return "%.6g" % (n,)


def sn_fmt(n):
    return "{:,.6g}".format(n)


def comma_fmt(n):
    return "{:,.0f}".format(n)
    


def test():
    tests = (
                          (0.01,              "0.01"),
                          (0.12,              "0.12"),
                          (1.05,              "1.05"),
                         (99.23,              "99.2"),
                            (99,              "99.0"),
                           (99l,              "99.0"),
                        (198.60,             "199"),
                       (1234.11,           "1,234"),
                      (12345.11,          "12,345"),
                     (123456.11,         "123,456"),
                        (123456,         "123,456"),
                       (123456l,         "123,456"),
                    (1234567.11,       "1,234,567"),
                   (12345678.11,      "12,345,678"),
                  (123456789.11,     "123,456,789"),
                 (1234567890.11,   "1,234,567,890"),
                (12345678901.11,  "12,345,678,901"),
               (123456789012.11, "123,456,789,012"),
              (1234567890123.11,   "1.234568 trillion"),
             (12345678901234.11,  "12.345679 trillion"),
            (123456789012345.11, "123.456789 trillion"),
           (1234567890123456.11,   "1.234568 quadrillion"),
#           QTTTBBBMMMTTTOOO     

      (117431345070027931648.00, "117.431345 quintillion"),
        (117431345070027931648L, "117.431345 quintillion"),
#      QUIQUATTTBBBMMMTTTOOO
#     117,431,345,070,027,931,648
#     qi  qa  t   b   m
    )
    for n, s in tests:
        if wordish_fmt(n) != s:
            print "n=%r fmt(n)=%r s=%r" % (n, wordish_fmt(n), s)



class Formatter:
    _formatters = [
        classic_fmt,
        wordish_fmt,
        sn_fmt,
        comma_fmt,
    ]

    def __init__(self):
        self._idx = -1
        self.next()

    def next(self):
        self._idx = (self._idx+1) % len(self._formatters)
        self._fmt = self._formatters[self._idx]
        
    def __call__(self, n):
        return self._fmt(n)

fmt = Formatter()


if __name__=="__main__":
    test()
