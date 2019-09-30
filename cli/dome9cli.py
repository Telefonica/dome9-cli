#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import fire
import json
import dome9
from tabulate import tabulate

class Dome9CLI():

	_tablefmt = 'github'

	def __init__(self):
		self.dome9 = dome9.Dome9SDK()


	# 	SYSTEM METHODS
	# ---------------------

	def _read_file(self, file):
		with open(file, 'r') as f:
			return f.read()

	def _pprint(self, dataset, headers):
		output = list()
		for item in dataset:
			rows = list()
			for key in headers:
				rows.append(item[key])
			output.append(rows)
		print(tabulate(output, headers=headers, tablefmt=self._tablefmt))


	# 	CLOUD ACCOUNTS
	# ---------------------

	def list_aws_accounts(self):
		data = self.dome9.list_aws_accounts()
		self._pprint(data, ['id', 'name'])

	def list_azure_accounts(self):
		data = self.dome9.list_azure_accounts()
		self._pprint(data, ['id', 'name'])

	def list_cloud_accounts(self):
		data = self.dome9.list_cloud_accounts()
		self._pprint(data, ['id', 'name'])

	def get_cloud_account(self, id):
		data = self.dome9.get_cloud_account(id)
		self._pprint([data], ['id', 'name'])


	# 		RULESETS
	# ---------------------

	def list_rulesets(self):
		data = self.dome9.list_rulesets()
		self._pprint(data, ['id', 'cloudVendor', 'name'])
		
	def get_ruleset(self, id):
		data = self.dome9.get_ruleset(id)
		self._pprint([data], ['id', 'cloudVendor', 'name', 'createdTime', 'updatedTime'])

	def create_ruleset(self, jsonFile):
		ruleset = self._read_file(jsonFile)
		data = self.dome9.create_ruleset(ruleset)
		print('Ruleset create with ID: {}'.format(data['id']))

	def delete_ruleset(self, id):
		data = self.dome9.delete_ruleset(id)
		print('Ruleset deleted') if data else ('Resource not deleted')

	def generate_ruleset(self, name, cloud, rulesFile=None, desc=''):
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
		


	# 	REMEDIATIONS
	# ---------------------

	def list_remediations(self):
		data = self.dome9.list_remediations()
		self._pprint(data, ['id', 'ruleName', 'cloudBots'])

	def delete_remediation(self, id):
		data = self.dome9.delete_remediation(id)
		print('Remediation deleted') if data else ('Resource not deleted')


	# 	EXCLUSIONS
	# ---------------------

	def list_exclusions(self):
		data = self.dome9.list_exclusions()
		self._pprint(data, ['id', 'cloudAccountId', 'logic', 'comment'])

	def delete_exclusion(self, id):
		data = self.dome9.delete_exclusion(id)
		print('Exclusion deleted') if data else ('Resource not deleted')


	# 	ASSESSMENTS
	# ---------------------

	# def generate_template(self, rulesetId, cloudAccountId):
	# 	data = self.dome9.generate_assessment_template(rulesetId, cloudAccountId)
	# 	print(data)
	# 	self._pprint([data], ['id', 'name'])

	def run_assessment(self, rulesetId, cloudAccountId):
		data = self.dome9.run_assessment(rulesetId, cloudAccountId)
		if data:
			print('See report on: https://secure.dome9.com/v2/compliance-engine/result/%s' % data['id'])


if __name__ == '__main__':
	try:
		fire.Fire(Dome9CLI())
		sys.exit(0)
	except KeyboardInterrupt as e: # Ctrl-C
		raise e
	except SystemExit as e: # sys.exit()
		raise e
