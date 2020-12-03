#!/usr/bin/env python3

import sys
import traceback
import time

import distlib.locators  # type: ignore


NEWLINE = "\n"
NOT_NEWLINE = "\u2424"


# generate this with something like:
# curl https://pypi.org/simple/ | rg -or '$1' '">([-._a-zA-Z0-9]+)<' > package-list-2020-08-27
packages = []
with open(sys.argv[1], "r") as f:
    for line in f:
        packages.append(line.strip())


for package in packages:
    time.sleep(0.1)
    try:
        distribution = distlib.locators.locate(package)
        if distribution is None:
            print(f"# {package}: no distribution available")
            continue
        package = distribution.metadata.name  # normalise capitalisation
        deps = distribution.metadata.dependencies
        if not deps:
            print(f"# {package}: no dependencies")
            continue
        for dep in {
            dep.split()[0]
            for extra in deps["run_requires"]
            for dep in extra["requires"]
        }:
            print(f"{package}: {dep}")
    except Exception as e:
        print(f"# {package}: {type(e)}: {str(e).replace(NEWLINE, NOT_NEWLINE)}")
        print(f"error processing {package}:", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
