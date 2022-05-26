#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This script is a simple tool that facilitates the daily
use and helps enormously to work in agile methodologies.
This package consumes calls through the Dome9 Python SDK
mentioned above so it contains the same methods.

Copyright (c) Telefonica Digital España, 2019
"""
import sys
import json
import fire
import dome9
from tabulate import tabulate


class Dome9CLI():

    _tablefmt = 'github'

    def __init__(self):
        self._dome9 = dome9.Dome9()

    # ------------------------------------------
    # 			  SYSTEM METHODS
    # ------------------------------------------

    def _read_file(self, file):
        with open(file, 'r') as f:
            return f.read()

    def _find(self, element, json):
        keys = element.split('.')
        rv = json
        for key in keys:
            rv = rv[key]
        return rv

    def _pprint(self, dataset, headers):
        output = list()
        for item in dataset:
            rows = list()
            for key in headers:
                rows.append(self._find(key, item))
            output.append(rows)
        print(tabulate(output, headers=headers, tablefmt=self._tablefmt))

    # ------------------------------------------
    # 			  CLOUD ACCOUNTS
    # ------------------------------------------

    def list_aws_accounts(self):
        """List AWS (Amazon Web Services) accounts
        """
        data = self._dome9.list_aws_accounts()
        self._pprint(data, ['id', 'name', 'externalAccountNumber'])

    def list_azure_accounts(self):
        """List AZURE accounts
        """
        data = self._dome9.list_azure_accounts()
        self._pprint(data, ['id', 'name'])

    def list_google_accounts(self):
        """List GCP (Google Cloud Platform) accounts
        """
        data = self._dome9.list_google_accounts()
        self._pprint(data, ['id', 'name'])

    def list_kubernetes_accounts(self):
        """List Kubernetes accounts
        """
        data = self._dome9.list_kubernetes_accounts()
        self._pprint(data, ['id', 'name'])

    def list_cloud_accounts(self):
        """List all types of cloud accounts
        """
        data = self._dome9.list_cloud_accounts()
        self._pprint(data, ['id', 'name'])

    def get_cloud_account(self, accountId):
        """Get a cloud account by ID

        Args:
            accountId (int): Cloud account ID
        """
        data = self._dome9.get_cloud_account(accountId)
        self._pprint([data], ['id', 'name'])

    # ------------------------------------------
    # 				  RULESETS
    # ------------------------------------------

    def list_rulesets(self):
        """List all Compliance Rulesets
        """
        data = self._dome9.list_rulesets()
        self._pprint(data, ['id', 'cloudVendor', 'name'])

    def get_ruleset(self, rulesetId):
        """Get a ruleset by ID

        Args:
            rulesetId (int): Id of the ruleset
        """
        data = self._dome9.get_ruleset(rulesetId)
        self._pprint([data], ['id', 'cloudVendor', 'name', 'createdTime', 'updatedTime'])

    def create_ruleset(self, jsonFile):
        """Create a compliance ruleset

        Args:
            jsonFile (str): Absolute or relative path to a JSON file with the ruleset
        """
        ruleset = self._read_file(jsonFile)
        data = self._dome9.create_ruleset(ruleset)
        print('Ruleset created with ID: {}'.format(data['id']))

    def update_ruleset(self, jsonFile):
        """Update ruleset data

        Args:
            jsonFile (str): Absolute or relative path to a JSON file with the ruleset
        """
        ruleset = json.loads(self._read_file(jsonFile))
        remote_ruleset = filter(lambda x: ruleset['name'] in x['name'], self._dome9.list_rulesets())
        if remote_ruleset:
            ruleset['id'] = remote_ruleset[0]['id']
            self._dome9.update_ruleset(ruleset)
            print('Ruleset updated with ID: {}'.format(ruleset['id']))
        else:
            print('Ruleset "{}" not found'.format(ruleset['name']))

    def delete_ruleset(self, rulesetId):
        """Delete a compliance

        Args:
            rulesetId (int): Id of the ruleset
        """
        data = self._dome9.delete_ruleset(rulesetId)
        print('Ruleset deleted') if data else ('Resource not deleted')

    def generate_ruleset(self, name, cloud, rulesFile=None, desc=''):
        """Generate a ruleset template

        Args:
            cloud (str): Name of the cloud vendor. Accepted values: [aws, azure, google, kubernetes]
            name (str): Name of the ruleset
            rulesFile (str, optional): Absolute or relative path to a JSON file with Dome9 rules. Defaults to None.
            desc (str, optional): Description of the ruleset. Defaults to ''.
        """
        rules = []
        if rulesFile:
            rules.extend(json.loads(self._read_file(rulesFile)))
        ruleset = {
            "id": 0,
            "name": name,
            "description": desc,
            "hideInCompliance": True,
            "cloudVendor": cloud,
            "minFeatureTier": "Advanced",
            "rules": rules,
        }
        print(json.dumps(ruleset))

    # ------------------------------------------
    # 			  COMPLIANCE RULES
    # ------------------------------------------

    def list_rules(self, rulesetId):
        """List compliance rulesets
        """
        data = self._dome9.get_ruleset(id=rulesetId)['rules']
        self._pprint(data, ['name', 'severity', 'complianceTag'])

    # ------------------------------------------
    # 			  REMEDIATIONS
    # ------------------------------------------

    def list_remediations(self):
        """List all remediations
        """
        data = self._dome9.list_remediations()
        self._pprint(data, ['id', 'ruleName', 'cloudBots', 'comment'])

    def get_remediation(self, remediationId):
        """Get a remediation by ID

        Args:
            remediationId (int): Id of the remediation
        """
        data = self._dome9.get_remediation(remediationId)
        self._pprint([data], ['id', 'ruleName', 'cloudBots', 'comment'])

    def create_remediation(self, remediationFile):
        """Create a new remediation

        Args:
            remediationFile (str): Absolute or relative path to a JSON file with Dome9 remediation.
        """
        remediation = json.loads(self._read_file(remediationFile))
        data = self._dome9.create_remediation(remediation)
        print('Remediation created with ID: {}'.format(data['id']))

    def delete_remediation(self, remediationId):
        """Delete a specific remediation

        Args:
            remediationId (int): Id of the remediation
        """
        data = self._dome9.delete_remediation(remediationId)
        print('Remediation deleted') if data else ('Resource not deleted')

    # ------------------------------------------
    # 			  EXCLUSIONS
    # ------------------------------------------

    def list_exclusions(self):
        """List all exclusions
        """
        data = self._dome9.list_exclusions()
        self._pprint(data, ['id', 'cloudAccountId', 'logic', 'comment'])

    def get_exclusion(self, exclusionId):
        """Get a specific exclusion

        Args:
            exclusionId (int): Id of the exclusion
        """
        data = self._dome9.get_exclusion(exclusionId)
        print(json.dumps(data, indent=4))
        self._pprint([data], ['id', 'cloudAccountType', 'cloudAccountId', 'logic', 'comment'])

    def create_exclusion(self, exclusionFile):
        """Create a new exclusion

        Args:
            exclusion (str): Absolute or relative path to a JSON file with Dome9 exclusion.
        """
        exclusion = json.loads(self._read_file(exclusionFile))
        data = self._dome9.create_exclusion(exclusion)
        print('Exclusion created with ID: {}'.format(data['id']))

    def delete_exclusion(self, exclusionId):
        """Delete a specific exclusion

        Args:
            exclusionId (id): Id of the exclusion
        """
        data = self._dome9.delete_exclusion(exclusionId)
        print('Exclusion deleted') if data else ('Resource not deleted')

    # ------------------------------------------
    # 			  ASSESSMENTS
    # ------------------------------------------

    def _print_assessment_stats(self, assessment):
        print('\nSee report on: https://secure.dome9.com/v2/compliance-engine/result/%s' % assessment['id'])
        print('\n#########################################\n')
        print('Scan ID: %s' % assessment['id'])
        print('Account: %s' % assessment['request']['cloudAccountId'])
        print('Ruleset: %s' % assessment['request']['name'])
        print()
        print('Total rules: %s' % len(assessment['tests']))
        print('Tested Entities:')
        for k, v in assessment['testEntities'].items():
            print('\t%s\t%s' % (k.title().ljust(10), len(v)))
        print()
        print('Exam Passed: %s' % assessment['assessmentPassed'])
        print('\n#########################################\n')

    def run_assessment(self, rulesetId, cloudAccountId):
        """Run assessment and get report URL

        Args:
            rulesetId (int): ID of the ruleset
            cloudAccountId (str): ID of the cloud account which will be scanned
        """
        data = self._dome9.run_assessment(rulesetId, cloudAccountId)
        if data:
            self._print_assessment_stats(data)
            self._pprint(data['tests'], ['rule.name', 'rule.severity', 'testedCount', 'nonComplyingCount'])

    def get_assessment(self, assessmentId):
        data = self._dome9.get_assessment(assessmentId)
        if data:
            self._print_assessment_stats(data)
            self._pprint(data['tests'], ['rule.name', 'rule.severity', 'testedCount', 'nonComplyingCount'])


if __name__ == '__main__':
    try:
        fire.Fire(Dome9CLI())
        sys.exit(0)
    # Ctrl-C
    except KeyboardInterrupt as e:
        raise e
    # sys.exit()
    except SystemExit as e:
        raise e
