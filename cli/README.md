# Dome9 CLI

This Command Line Interface (CLI) is a simple tool that facilitates the daily use and helps enormously to work in agile methodologies.
This package consumes calls through the Dome9 Python SDK mentioned above so it contains the same methods.

This CLI helps to work on Dome9 from our different agile services like Jenkins, Github or Travis, creating new rulesets, running
assessments or getting protected assets. You only need to download the script stored on `./cli/` folder and launch it with `./dome9cli.py --help`
If you want to use it in any path or just typing `dome9`, you have to add the absolute path to your `PATH` environment variable. It will be
automated soon. 

For detailed information on this command, run:
`dome9cli.py --help`


## Installation

1. Open the file `dome9cli.py` and copy its content
1. Create the file `/usr/local/bin/dome9` and paste the code
1. Give it execution permission: `chmod u+x /usr/local/bin/dome9`

Now, run `dome9 --help` and you should see the expected output.

## Commands


```
Usage: .\dome9cli.py <command> <arguments>

```

#### create_ruleset  
Description: Create a compliance ruleset  
Command: `.\dome9cli.py create_ruleset jsonFile`  


#### delete_exclusion  
Description: Delete a specific exclusion  
Command: `.\dome9cli.py delete_exclusion id=0`  


#### delete_remediation  
Description: Delete a specific remediation  
Command: `.\dome9cli.py delete_remediation id=0`  


#### delete_ruleset  
Description: Delete a specific ruleset  
Command: `.\dome9cli.py delete_ruleset id=0`  


#### generate_ruleset  
Description: Generate a ruleset template  
Command: `.\dome9cli.py generate_ruleset name=minimum, cloud=aws, rulesFile='./rules.json', desc='My description'`  


#### get_cloud_account  
Description: Get a specific cloud account  
Command: `.\dome9cli.py get_cloud_account id=0`  


#### get_ruleset  
Description: Get a specific compliance ruleset  
Command: `.\dome9cli.py get_ruleset id=0`  


#### list_aws_accounts  
Description: List AWS Cloud accounts  
Command: `.\dome9cli.py list_aws_accounts`  


#### list_azure_accounts  
Description: List Azure Cloud accounts  
Command: `.\dome9cli.py list_azure_accounts`  


#### list_cloud_accounts  
Description: List all cloud accounts (AWS, Azure, GCP and Kubernetes)  
Command: `.\dome9cli.py list_cloud_accounts`  


#### list_exclusions  
Description: List all exclusions  
Command: `.\dome9cli.py list_exclusions`  


#### list_google_accounts  
Description: List Google Cloud accounts  
Command: `.\dome9cli.py list_google_accounts`  


#### list_kubernetes_accounts  
Description: List Kubernetes accounts  
Command: `.\dome9cli.py list_kubernetes_accounts`  


#### list_remediations  
Description: List all remediations  
Command: `.\dome9cli.py list_remediations`  


#### list_rulesets  
Description: List compliance rulesets  
Command: `.\dome9cli.py list_rulesets`  


####  run_assessment  
Description: Run assessment and get report URL  
Command: `.\dome9cli.py run_assessment rulesetId=0, cloudAccountId=0000-0000-0000-0000`  

---

_CDO Telefonica_
_Copyright (c) Telefonica Digital España, 2019_