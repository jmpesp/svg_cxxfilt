#!/usr/bin/env python3
import sys

import cxxfilt
from bs4 import BeautifulSoup

with open(sys.argv[1]) as fp:
    doc = fp.read()

soup = BeautifulSoup(doc, 'xml')

def demangle(s):
    r = cxxfilt.demangle(s)

    # Harness$LT$T$C$S$GT$ -> Harness<T,S>
    r = r.replace("$LT$", "<")
    r = r.replace("$C$", ",")
    r = r.replace("$GT$", ">")

    return r

assert(demangle("Harness$LT$T$C$S$GT$") == "Harness<T,S>")

def t(s):
    try:
        if '`' in s:
            parts = s.split('`')
            if len(parts) == 2:
                if '(' in parts[1]:
                    subparts = parts[1].split('(')
                    if len(subparts) == 2:
                        return "".join([
                            parts[0],
                            '`',
                            demangle(subparts[0].strip()),
                            ' (',
                            subparts[1],
                        ])
                    else:
                        raise RuntimeError()
                else:
                    return "".join([
                        parts[0],
                        '`',
                        demangle(parts[1]),
                    ])
            else:
                raise RuntimeError()
    except cxxfilt.InvalidName:
        return s
    except RuntimeError:
        raise

    return s

tests = [
    [
        "crucible-downstairs-main`_ZN5tokio7runtime4task7harness20Harness$LT$T$C$S$GT$4poll17h17c50d9b6cd7d9bfE (42 samples, 0.03%)",
        "crucible-downstairs-main`tokio::runtime::task::harness::Harness<T,S>::poll::h17c50d9b6cd7d9bf (42 samples, 0.03%)",
    ]
]
for test in tests:
    actual = t(test[0])
    expected = test[1]
    if actual != expected:
        print("{} != {}".format(actual, expected))
        exit(1)

for tag in ['title', 'text']:
    for x in soup.find_all(tag):
        if x.string is not None:
            if t(x.string) is None:
                print(x.string)
                exit(1)
            x.string = t(x.string)

print(soup.prettify())
