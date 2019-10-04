#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This script is used to split a master ruleset file
in different files based on audit type or use case.

Copyright (c) Telefonica Digital España, 2019
"""

import os
import fire
import json
import yaml
from dome9 import Dome9

class Agile(object):

    def __init__(self, *args, **kwargs):
        self._dome9 = Dome9()


    @classmethod
    def _read_yml_file(cls, obj, dir, file):
        path = './{obj}/{dir}/{file}.yml'.format(obj=obj, dir=dir, file=file)
        with open(path) as x:
            return yaml.load(x.read())

    @classmethod
    def _export_result(cls, obj, file, content):
        filename = file.lower().replace(' ', '_')
        directory = './_output/{obj}/'.format(obj=obj)
        filepath = '{dir}{file}.json'.format(dir=directory, file=filename)

        if not os.path.exists(directory):
            os.makedirs(directory)
        
        with open(filepath, 'w') as f:
            f.write(content)

        print('[+] {file}'.format(file=filepath))

    @classmethod
    def _load_compliance_ruleset_template(cls, name, desc, vend, type, rules):
        template = {
            "id": 0,
            "name": "{vendor} CDO - {type}T. {name}".format(vendor=vend.upper(), type=type[0].upper(), name=name),
            "description": desc,
            "hideInCompliance": True,
            "cloudVendor": vend,
            "minFeatureTier": "Advanced",
            "rules": rules,
        }
        return template

    @classmethod
    def _load_remediation_template(cls, rulesetId, ruleName, comment, cloudbots, ruleLogicHash, accountId=None):
        template = {
            "ruleLogicHash": ruleLogicHash,
            "ruleName": ruleName,
            "rulesetId": rulesetId,
            "platform": "aws",
            "comment": comment,
            "cloudBots": cloudbots,
        }
        if accountId:
            template["cloudAccountId"]= accountId
        return template

    
    def generateComplianceRulesets(self, templateName='default', rulesetKey=None):
        templates = self._read_yml_file('Compliance', 'templates', templateName)
        for template in templates:

            if rulesetKey and rulesetKey.lower() != template['key'].lower():
                continue

            for env in template['env']:

                env_rules = self._read_yml_file('Compliance', 'rules', env)
                if template['type'].lower() == 'level':
                    rules = filter(lambda x: template['key'] == x['level'], env_rules)
                else:
                    rules = filter(lambda x: template['key'] in x['templates'], env_rules)
                
                map(lambda x: x.pop('templates') ,rules)
                map(lambda x: x.pop('level') ,rules)

                ruleset = self._load_compliance_ruleset_template(
                    name = template['name'],
                    desc = template['desc'],
                    type = template['type'],
                    rules = rules,
                    vend = env)

                self._export_result('Compliance', file=ruleset['name'], content=json.dumps(ruleset))


    def generateRemediations(self, templateName='default'):
        d9accounts = self._dome9.list_aws_accounts()

        templates = self._read_yml_file('Remediation', 'templates', templateName)
        for template in templates:

            if rulesetKey and rulesetKey.lower() != template['key'].lower():
                continue

            rules = template['rules']
            d9ruleset = self._dome9.get_ruleset(name=template['ruleset'])
            cloudbots = ['{} {}'.format(x['name'], ' '.join(x['args'].values())) for x in template['cloudbots']]

            for rule in rules:
                d9rule = filter(lambda x: x['name'] == rule, d9ruleset['rules'])[0]

                if template.get('accounts', None):
                    for account in template['accounts']:
                        d9account = filter(lambda x: x['externalAccountNumber'] == account, d9accounts)[0]

                        remediation = self._load_remediation_template(
                            rulesetId=d9ruleset['id'],
                            ruleName=rule,
                            comment=template['name'],
                            cloudbots=cloudbots,
                            ruleLogicHash=d9rule['logicHash'],
                            accountId=d9account['id'])

                        filename = '{}_{}_{}'.format(template['name'].replace(' ', '_'), rule.replace(' ', '_'), account)
                        self._export_result('Remediation', filename , json.dumps(remediation, indent=4))

                else:
                    remediation = self._load_remediation_template(
                        rulesetId=d9ruleset['id'],
                        ruleName=rule,
                        comment=template['name'],
                        cloudbots=cloudbots,
                        ruleLogicHash=d9rule['logicHash'])
                    filename = '{}_{}'.format(template['name'].replace(' ', '_'), rule.replace(' ', '_'))
                    self._export_result('Remediation', filename , json.dumps(remediation, indent=4))


if __name__ == '__main__':
    fire.Fire(Agile())