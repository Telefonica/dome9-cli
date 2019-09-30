# Dome9 Agile

Through this simple script and the CLI we are able to create rulesets dinamically using templates.
The purpose of this tool is to have just one master file of rules for each cloud environment (AWS, Azure, GCP & Kubernetes)
and create different kind of rulesets based on those rule files.

Usage:
```bash
    dome9agile --templateName="default" --rulesetKey="costsaving"
    dome9agile --templateName="aura" --rulesetKey="networking"
```

## Rules

Rules are the different security policies (also called Dome rules) that make up a ruleset.
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

These rules are composed of the same fields of a Dome9 Rule and 2 added fields (`templates` and `level`) in order to generate different rulesets:

- Name: Name of the ruleset
- Description: Description of the security case
- Severity: Risk of the rule. Allowed values: [low, medium, high]
- Logic: Rule syntax in GSL Language ([see reference](https://sc1.checkpoint.com/documents/CloudGuard_Dome9/Documentation/Compliance-and-Governance/GSL.html))
- Remediation: Solution to fix the case
- ComplianceTag: Section to identify groups of different rules
- Templates: List of keys of different templates
- Level: Risk acceptance. Allowed values: [minimum, medium, advance]

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


## Templates

Templates are configurations that allow us to generate different rulesets using the unique rules file.
Are written in YAML format and are stored into `templates` subfolder.

These templates are composed of the following fields:

- Name: Name of the ruleset
- Description: Description of the security case
- Severity: Risk of the rule. Allowed values: [low, medium, high]
- Logic: Rule syntax in GSL Language ([see reference](https://sc1.checkpoint.com/documents/CloudGuard_Dome9/Documentation/Compliance-and-Governance/GSL.html))
- Remediation: Solution to fix the case
- ComplianceTag: Section to identify groups of different rules
- Templates: List of keys of different templates
- Level: Risk acceptance. Allowed values: [minimum, medium, advance]

Example

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

## 