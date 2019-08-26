import pandas as pd
import requests

USERNAME = "PhiladelphiaController"

if __name__ == "__main__":

    # load the raw data
    data = pd.read_csv("data.csv", header=None, names=["name", "maintained"])

    # read the template files
    lines = [line.strip("\n") for line in open("template.md", "r").readlines()]
    lines = [line for line in lines if line]

    for i, row in data.iterrows():
        line = "| "
        slug = row["name"]

        # Github
        line += f"[{slug}](https://www.github.com/{USERNAME}/{slug})"
        line += "| "

        # PyPi
        pypi = f"https://pypi.org/project/{slug}"
        if requests.get(pypi).status_code == 200:
            line += f"[![PyPI version](https://img.shields.io/pypi/v/{slug}.svg)](https://pypi.org/project/row[name])"
        line += "| "

        # Travis CI
        travis = f"https://travis-ci.org/{USERNAME}/{slug}.png?branch=master"
        if "unknown" not in requests.get(travis).text:
            line += (
                f"[![Build Status]({travis})](https://travis-ci.org/{USERNAME}/{slug}) "
            )

        # Maintained?
        line += "| "
        if row["maintained"]:
            line += "✔"
        else:
            line += "❌"
        line += "|"

        lines.append(line)

    with open("README.md", "w") as ff:
        ff.write("\n".join(lines))

