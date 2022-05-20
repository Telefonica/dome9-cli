# Dome9 

[![Build Status][build_status_badge]][build_status_link]

Dome9 is a Cloud Security Posture Management platform that allows to define and visualize the security posture,
detecting misconfigurations and protecting against identity theft and data loss in cloud environments. 
Dome9 delivers security capabilities across Amazon Web Services, Microsoft Azure, Google Cloud Platform (GCP) and Kubernetes.

In the CDO area, we have decided to approach cloud protection from an "agile" point of view, defining a methodology
that allows teams to work comfortably with Dome9, isolating themselves from the logic and complexity of the interface.

These are the 3 components developed by us:

* **Dome9 SDK**
* **Dome9 CLI**
* **Dome9 Agile**


## Dome9 SDK

[Repository](https://github.com/davidmoremad/dome9/) | [Documentation](http://dome9.readthedocs.io/) | [Pypi](https://pypi.org/project/dome9/)

This package is a temporary development waiting for [official Dome9 SDK for Python](https://github.com/dome9/python-api-sdk) to incorporate new functionalities.
This package has been registered on Pypi repository so you just have to install it running `pip install dome9` on your preferred console.

Usage:
```python
    import dome9
    d9 = dome9.Dome9(key='xxxxxx', secret='yyyyyyy')
    rulesets = d9.list_rulesets()
```


## Dome9 CLI

![](https://github.com/Telefonica/dome9/workflows/CLI%20Workflow/badge.svg)

[Repository & Documentation](https://github.com/Telefonica/Dome9/tree/master/cli)

This Command Line Interface (CLI) is a simple tool that facilitates the daily use and helps enormously to work in agile methodologies.
This package consumes calls through the Dome9 Python SDK mentioned above so it contains the same methods.

This CLI helps to work on Dome9 from our different agile services like Jenkins, Github or Travis, creating new rulesets, running
assessments or getting protected assets. You only need to download the script stored on `./cli/` folder and launch it with `./dome9cli.py --help`
If you want to use it in any path or just typing `dome9`, you have to add the absolute path to your `PATH` environment variable. It will be
automated soon. 

Usage:
```bash
    dome9 generate_ruleset --name=ISO27001-Telefonica --cloud=aws --rulesFile=./rules-iso27001-telefonica.json >> ruleset.json
    dome9 create_ruleset ./ruleset.json >> rulesetid.txt
    dome9 run_assessment --rulesetId=`cat rulesetid.txt` --cloudAccountId="0000-0000-0000-0000"
```

## Dome9 Agile

![](https://github.com/Telefonica/dome9/workflows/Agile%20Workflow/badge.svg)

[Repository & Documentation](https://github.com/Telefonica/Dome9/tree/master/agile)

Through this simple script and the CLI we are able to create rulesets dinamically using templates.
The purpose of this tool is to have just a unique file of rules for each cloud environment (AWS, Azure, GCP & Kubernetes)
and create different kind of rulesets based on those rule files.
In this way, every team are able to use its own rulesets with specific tests on their environment.

Usage:
```bash
    dome9agile --templateName="default" --rulesetKey="costsaving"
    dome9agile --templateName="aura" --rulesetKey="networking"
```

---

_CDO Telefonica_
_Copyright (c) Telefonica Digital España, 2019_