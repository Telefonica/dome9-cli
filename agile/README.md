# Dome9 Agile

Through this script, and the CLI, we are able to create dinamically diferent Dome9 objects and upload them vía API.
The purpose of this tool is to facilitate the use of Dome9 in projects using agile methodologies, unifying sets of
rules, instead of duplicated files, and automate hundreds of actions in just one command.

Actions:
 - **Compliance Rulesets**: Create rulesets for different teams and purposes using just one master rules file.
 - **Remediations**: Each remediation apply to specific ruleset and rule or resource. This script create remediations
 that apply to all rules and accounts.




## Compliance


Usage:

```bash
./dome9agile.py generateComplianceRulesets
./dome9agile.py generateComplianceRulesets --templateName="octopus"
./dome9agile.py generateComplianceRulesets --templateName="aura" --rulesetKey="networking"
```

### Compliance Rules

Rules are the different security compliance policies (also called Dome rules) that make up a ruleset.
In order to avoid redundancy, we have a unique set of rules used by differents rulesets or templates.

These files are written in `YAML` format file ([see reference](https://docs.ansible.com/ansible/latest/reference_appendices/YAMLSyntax.html)) 
because of easy understanding and design. You can find the rules stored into `rules` subfolder for
every type of ruleset (Compliance, Logic, Remediation...)

```
./Compliance/rules/aws.yml
./Compliance/rules/kubernetes.yml

./Logic/rules/access-management.yml
./Logic/rules/key-management.yml

```

These rules are composed of the same fields of a Dome9 Rule and 2 added fields (`templates` and `level`) in order to generate different rulesets.
All these fields are mandatory.

- **name** (str): Name of the ruleset
- **description** (str): Description of the security case
- **severity** (str): Risk of the rule. Allowed values: [low, medium, high]
- **logic** (str): Rule syntax in GSL Language ([see reference](https://sc1.checkpoint.com/documents/CloudGuard_Dome9/Documentation/Compliance-and-Governance/GSL.html))
- **remediation** (str): Solution to fix the case
- **complianceTag** (str): Section to identify groups of different rules
- **templates** (\[str\]): List of keys of different templates
- **level** (str): Risk acceptance. Allowed values: [minimum, medium, advance]

Example:

```yml
-
    name: 'EBS Volumes not used'
    description: "Checks for EBS volumes that are unattached to instances, for example, if they persist after an EC2 instance has been terminated. It is recommended to review of these volumes regularly, since they may contain sensitive company data, application, infrastructure or users.\nIn addition, removing unattached instances will lower your AWS bill"
    severity: Medium
    logic: 'Volume should have attachments contain [ state=''attached'' ]'
    remediation: "Periodically review EBS volumes. Archive them to Glacier, remove the volume entirely, or reattach them if they were inadvertently orphaned. \n\n1. Navigate to the the AWS console EC2 dashboard \n2. In the navigation pane, select Volumes \n3. Sort using the State column and locate the volumes marked 'available' \n4. Review the volume information (create date, size, status, etc) \n5. Determine if you wish to retain or remove each volume"
    complianceTag: 'Cost Saving'
    templates: [governance, costsaving]
    level: advanced
```


## Compliance Templates

Templates are configurations that allow us to generate different rulesets using the unique rules file.
Are also written in YAML format and are stored into `templates` subfolder.

These templates are composed of the following fields, all of them required:

- **type** (str): Ruleset type. Allower values: [type, level]
- **name** (str): Name of the Dome9 Ruleset
- **desc** (str): Description of the Dome9 Ruleset
- **key** (str): Identifiers of the set of rules
- **env** (\[str\]): List of cloud vendors. Allowed values: [aws, azure, gcp, kubernetes]

Example:

```yml
- template:
  type: type
  name: Cost Savings
  desc: Type-based template of security controls related to cost control
  key : costsaving
  env :
    - aws
    - azure
```

## Remediations

If you want to apply one remediation to all rules of a ruleset (i.e: 40 rules), you will have to create as many
remediations as rules have in the ruleset, so 40 rules. With this module you can create complex and multiple 
remediations with a simple template and just one command.

Usage:

```bash
./dome9agile.py generateRemediations
./dome9agile.py generateRemediations --templateName="default"
```

### Remediation Templates

These templates are composed of the following fields:

- **name** (str): Simple tag to identify the purpose of the remediation (will be shown in Dome9 remediation as comment)
- **ruleset** (str): Ruleset where the rules included below are.
- **rules** (\[str\]): Group of rules to remediate. Each remediation is associated to a specific rule so there will be as many remediations as rules.
- **cloudbot** (\[str\]): List of action to take in case of incident. ([see reference](https://github.com/dome9/cloud-bots))
- **accounts** (\[str\]): **Optional**. List of accounts where the remediation will run.
Each remediation is associated to all or one account, not a bunch of them, so there will be as many remediations as accounts.

```yml
-
  name: Minimal template remediations
  ruleset: AWS CDO - LT. Minimum v1.0
  rules:
    - IAM Root account with MFA enabled
    - IAM Root account without API access keys
  accounts:
    - 1234567890
    - 9876543210
  cloudbots:
    - name: tag_ec2_resource
      args:
        key: dome9
        value: unaccomplished

```

---

_CDO Telefonica_  
_Copyright (c) Telefonica Digital España, 2019_