# Dome9 

Dome9 is a Cloud Security Posture Management platform that allows to define and visualize the security posture,
detecting misconfigurations and protecting against identity theft and data loss in cloud environments. 
Dome9 delivers security capabilities across Amazon Web Services, Microsoft Azure, Google Cloud Platform (GCP) and Kubernetes.

In the CDO area, we have decided to approach cloud protection from an "agile" point of view, defining a methodology
that allows teams to work comfortably with Dome9, isolating themselves from the logic and complexity of the interface.

These are the 3 components developed by us:

* Dome9 SDK
* Dome9 CLI
* Dome9 Agile


## Dome9 SDK

This python package is a temporary development waiting for Dome9 to incorporate new functionalities in 
its official SDK for Python ([see here](https://github.com/dome9/python-api-sdk)). Through this package we can interact and
interconnect our services with Dome9.

- Repository: https://github.com/davidmoremad/dome9
- Documentation: http://dome9.readthedocs.io/?badge=latest
- Installation: `pip install dome9`

Usage:
```python
    import dome9

    d9 = dome9.Dome9(key='xxxxxx', secret='yyyyyyy')
    rulesets = d9.list_rulesets()
```


## Dome9 CLI

This Command Line Interface is a simple tool that facilitates the daily use and helps enormously to work in agile methodologies.
This package consumes calls through the SDK mentioned above so it contains the same calls.

- Repository: https://github.com/davidmoremad/dome9cli
- Documentation: https://github.com/davidmoremad/dome9cli
- Installation: `pip install --user dome9cli`

Usage:
```bash
    dome9 generate_ruleset --name=ISO27001-Telefonica --cloud=aws --rulesFile=./rules-iso27001-telefonica.json >> ruleset.json
    dome9 create_ruleset ./ruleset.json >> rulesetid.txt
    dome9 run_assessment --rulesetId=`cat rulesetid.txt` --cloudAccountId="0000-0000-0000-0000"
```

## Dome9 Agile

Through this simple script and the CLI we are able to create rulesets dinamically using templates.
The purpose of this tool is to have just one master file of rules for each cloud environment (AWS, Azure, GCP & Kubernetes)
and create different kind of rulesets based on those rule files.

Usage:
```bash
    dome9agile --templateName="default" --rulesetKey="costsaving"
    dome9agile --templateName="aura" --rulesetKey="networking"
```

