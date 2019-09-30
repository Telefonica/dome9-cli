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
		self._dome9 = dome9.Dome9()


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
		'''List AWS Cloud accounts
		'''
		data = self._dome9.list_aws_accounts()
		self._pprint(data, ['id', 'name'])

	def list_azure_accounts(self):
		'''List Azure Cloud accounts
		'''
		data = self._dome9.list_azure_accounts()
		self._pprint(data, ['id', 'name'])

	def list_google_accounts(self):
		'''List Google Cloud accounts
		'''
		data = self._dome9.list_google_accounts()
		self._pprint(data, ['id', 'name'])

	def list_kubernetes_accounts(self):
		'''List Kubernetes accounts
		'''
		data = self._dome9.list_kubernetes_accounts()
		self._pprint(data, ['id', 'name'])

	def list_cloud_accounts(self):
		'''List all cloud accounts (AWS, Azure, GCP and Kubernetes)
		'''
		data = self._dome9.list_cloud_accounts()
		self._pprint(data, ['id', 'name'])

	def get_cloud_account(self, id):
		'''Get a specific cloud account
		Args:
			id (str): Id of the cloud account
		'''
		data = self._dome9.get_cloud_account(id)
		self._pprint([data], ['id', 'name'])


	# 		RULESETS
	# ---------------------

	def list_rulesets(self):
		'''List compliance rulesets
		'''
		data = self._dome9.list_rulesets()
		self._pprint(data, ['id', 'cloudVendor', 'name'])
		
	def get_ruleset(self, id):
		'''Get a specific compliance ruleset
		Args:
			id (int): Id of the ruleset
		'''
		data = self._dome9.get_ruleset(id)
		self._pprint([data], ['id', 'cloudVendor', 'name', 'createdTime', 'updatedTime'])

	def create_ruleset(self, jsonFile):
		'''Create a compliance ruleset
		Args:
			jsonFile (str): Absolute or relative path to a JSON file with the ruleset
		'''
		ruleset = self._read_file(jsonFile)
		data = self._dome9.create_ruleset(ruleset)
		print('Ruleset create with ID: {}'.format(data['id']))

	def delete_ruleset(self, id):
		'''Delete a specific ruleset
		Args:
			id (int): Id of the ruleset
		'''
		data = self._dome9.delete_ruleset(id)
		print('Ruleset deleted') if data else ('Resource not deleted')

	def generate_ruleset(self, name, cloud, rulesFile=None, desc=''):
		'''Generate a ruleset template
		
		Args:
			cloud (str): Name of the cloud vendor. Accepted values: [aws, azure, google, kubernetes]
			name (str): Name of the ruleset
			desc (str, optional): Description of the ruleset. Defaults to ''.
			rulesFile (str, optional): Absolute or relative path to a JSON file with Dome9 rules. Defaults to None.
		'''
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
		'''List all remediations
		'''
		data = self._dome9.list_remediations()
		self._pprint(data, ['id', 'ruleName', 'cloudBots'])

	def delete_remediation(self, id):
		'''Delete a specific remediation
		Args:
			id (id): Id of the remediation
		'''
		data = self._dome9.delete_remediation(id)
		print('Remediation deleted') if data else ('Resource not deleted')


	# 	EXCLUSIONS
	# ---------------------

	def list_exclusions(self):
		'''List all exclusions
		'''
		data = self._dome9.list_exclusions()
		self._pprint(data, ['id', 'cloudAccountId', 'logic', 'comment'])

	def delete_exclusion(self, id):
		'''Delete a specific exclusion
		Args:
			id (id): Id of the exclusion
		'''
		data = self._dome9.delete_exclusion(id)
		print('Exclusion deleted') if data else ('Resource not deleted')


	# 	ASSESSMENTS
	# ---------------------

	def run_assessment(self, rulesetId, cloudAccountId):
		"""Run assessment and get report URL
		
		Args:
			rulesetId (int): ID of the ruleset
			cloudAccountId (str): ID of the cloud account which will be scanned
		"""
		data = self._dome9.run_assessment(rulesetId, cloudAccountId)
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
