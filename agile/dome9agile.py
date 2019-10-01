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

OUTPUT_DIR = './_output/'

def read_yml(path):
    with open(path) as x:
        return yaml.load(x.read())

def load_rules(rulesType, vendor):
    path = './{type}/rules/{vendor}.yml'.format(type=rulesType, vendor=vendor)
    return read_yml(path)

def load_template(templateType, templateName):
    path = './{type}/templates/{name}.yml'.format(type=templateType, name=templateName)
    return read_yml(path)

def export_ruleset(rulesetType, filename, content):
    filename = filename.lower().replace(' ', '_')
    directory = './_output/{type}/'.format(type=rulesetType)
    filepath = '{directory}{filename}.json'.format(directory=directory, filename=filename)

    if not os.path.exists(directory):
        os.mkdir(directory)
    
    with open(filepath, 'w') as f:
        f.write(content)
    
    return filepath

def generate_ruleset_template(name, desc, vend, type, rules):
    return {
        "id": 0,
        "name": "{} CDO - {}T. {}".format(vend.upper(), type[0].upper(), name),
        "description": desc,
        "hideInCompliance": True,
        "cloudVendor": vend,
        "minFeatureTier": "Advanced",
        "rules": rules,
    }

def generator(templateType='Compliance', templateName='default', rulesetKey=None):
    templates = load_template(templateType, templateName)
    for template in templates:

        if rulesetKey and rulesetKey.lower() != template['key'].lower():
            continue

        for env in template['env']:

            # Load environemnt rules (aws, azure)
            env_rules = load_rules(templateType, env)

            if template['type'] == 'level':
                if template['key'] == 'minimum':
                    rules = filter(lambda x: x['level'] == 'minimum', env_rules)
                elif template['key'] == 'medium':
                    rules = filter(lambda x: x['level'] in ['minimum', 'medium'], env_rules)
                elif template['key'] == 'advanced':
                    rules = filter(lambda x: x['level'] in ['minimum', 'medium', 'advanced'], env_rules)
            else:
                rules = filter(lambda x: template['key'] in x['templates'], env_rules)
            
            # Remove excess data
            map(lambda x: x.pop('templates') ,rules)
            map(lambda x: x.pop('level') ,rules)

            ruleset = generate_ruleset_template(
                name = template['name'],
                desc = template['desc'],
                type = template['type'],
                rules = rules,
                vend = env
            )

            file = export_ruleset(templateType, ruleset['name'], json.dumps(ruleset, indent=4))
            print('[+] {file}'.format(file=file))


if __name__ == '__main__':
    fire.Fire(generator)