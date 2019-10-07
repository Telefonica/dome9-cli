# -*- coding: utf-8 -*-
import os
import json
import uuid
import requests
from requests import ConnectionError, auth

class Dome9(object):

    def __init__(self, key=None, secret=None, endpoint='https://api.dome9.com', apiVersion='v2'):
        self.key = None
        self.secret = None
        self.headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        self.endpoint = endpoint + '/{}/'.format(apiVersion)
        self._load_credentials(key, secret)

    # ------ System Methods ------ 
    # ----------------------------

    def _load_credentials(self, key, secret):
        if key and secret:
            self.key = key
            self.secret = secret
        elif os.getenv('DOME9_ACCESS_KEY') and os.getenv('DOME9_SECRET_KEY'):
            self.key = os.getenv('DOME9_ACCESS_KEY')
            self.secret = os.getenv('DOME9_SECRET_KEY')
        else:
            raise ValueError('No provided credentials')

    def _request(self, method, route, payload=None):
        res = url = err = jsonObject = None
        _payload = json.dumps(payload)
        try:
            url = '{}{}'.format(self.endpoint, route)
            if method == 'get':
                res = requests.get(url=url, params=_payload, headers=self.headers, auth=(self.key, self.secret))
            elif method == 'post':
                res = requests.post(url=url, data=_payload, headers=self.headers, auth=(self.key, self.secret))
            elif method == 'patch':
                res = requests.patch(url=url, json=_payload, headers=self.headers, auth=(self.key, self.secret))
            elif method == 'put':
                res = requests.put(url=url, data=_payload, headers=self.headers, auth=(self.key, self.secret))
            elif method == 'delete':
                res = requests.delete(url=url, params=_payload, headers=self.headers, auth=(self.key, self.secret))
                return bool(res.status_code == 204)

        except requests.ConnectionError as ex:
            raise ConnectionError(url, ex.message)

        if res.status_code in range(200, 299):
            try:
                if res.content:
                    jsonObject = res.json()
            except Exception as ex:
                err = {'code': res.status_code, 'message': ex.message, 'content': res.content}
        else:
            err = {'code': res.status_code, 'message': res.reason, 'content': res.content}

        if err:
            raise Exception(err)
        return jsonObject

    def _get(self, route, payload=None):
        return self._request('get', route, payload)

    def _post(self, route, payload=None):
        return self._request('post', route, payload)

    def _patch(self, route, payload=None):
        return self._request('patch', route, payload)

    def _put(self, route, payload=None):
        return self._request('put', route, payload)

    def _delete(self, route, payload=None):
        return self._request('delete', route, payload)


    # ------------------   Accounts   ------------------
    # --------------------------------------------------

    def get_cloud_account(self, id):
        """Get a Cloud Account
        
        Args:
            id (str): ID of the Cloud Account
        
        Returns:
            dict: Cloud Account object.

        Response object:
            .. literalinclude:: schemas/AwsCloudAccount.json
        """
        return self._get(route='CloudAccounts/%s' % str(id))

    def list_aws_accounts(self):
        """List AWS accounts
        
        Returns:
            list: List of AWS Cloud Accounts.

        Response object:
            .. literalinclude:: schemas/AwsCloudAccount.json
        """
        return self._get(route='CloudAccounts')

    def list_azure_accounts(self):
        """List Azure accounts
        
        Returns:
            list: List of Azure Cloud Accounts.

        Response object:
            .. literalinclude:: schemas/AzureCloudAccount.json
        """
        return self._get(route='AzureCloudAccount')

    def list_google_accounts(self):
        """List Google Cloud Accounts
        
        Returns:
            list: List of Google accounts.

        Response object:
            .. literalinclude:: schemas/GoogleCloudAccount.json
        """
        return self._get(route='GoogleCloudAccount')

    def list_kubernetes_accounts(self):
        """List Kubernetes accounts
        
        Returns:
            list: List of Kubernetes accounts.

        Response object:
            .. literalinclude:: schemas/KubernetesCloudAccount.json
        """
        return self._get(route='KubernetesAccount')

    def list_cloud_accounts(self):
        """List all accounts (AWS, Azure, GCP & Kubernetes)
        
        Returns:
            list: List of Cloud Accounts.

        Response object:
            .. literalinclude:: schemas/AwsCloudAccount.json
        """
        accounts = self.list_azure_accounts()
        accounts.extend(self.list_aws_accounts())
        accounts.extend(self.list_google_accounts())
        accounts.extend(self.list_kubernetes_accounts())
        return accounts

    def create_aws_account(self, name, secret, roleArn):
        account = { "vendor": "aws", "name": "test", "credentials": { "type": "RoleBased", "secret": "", "arn": "" }, "fullProtection": False, "allowReadOnly": True, "lambdaScanner": False }
        account['name'] = name
        account['credentials']['secret'] = secret
        account['credentials']['arn'] = roleArn
        return self._post(route='CloudAccounts', payload=account)

    # ------------------ Rulesets ------------------
    # ----------------------------------------------

    def list_rulesets(self):
        """List Compliance Rulesets
        
        Returns:
            list: List of Compliance rulesets.

        Response object:
            .. literalinclude:: schemas/ComplianceRuleset.json
        """
        return self._get(route='CompliancePolicy')

    def get_ruleset(self, id=None, name=None):
        """Get a specific Compliance ruleset

        Args:
            id (str): Locate ruleset by id
            name (str): Locate ruleset by name
        
        Returns:
            dict: Compliance ruleset.

        Response object:
            .. literalinclude:: schemas/ComplianceRuleset.json
        """
        if id:
            return self._get(route='CompliancePolicy/%s' % str(id))
        elif name:
            return filter(lambda x: x['name'] == name, self.list_rulesets())[0]

    def create_ruleset(self, ruleset):
        """Create a Compliance ruleset

        Args:
            ruleset (dict): Ruleset object.
        
        Returns:
            dict: Compliance ruleset.

        Response object:
            .. literalinclude:: schemas/ComplianceRuleset.json
        """
        return self._post(route='CompliancePolicy', payload=ruleset)

    def update_ruleset(self, ruleset):
        """Update a Compliance ruleset

        Args:
            ruleset (dict): Ruleset object.
        
        Returns:
            dict: Compliance ruleset.

        Response object:
            .. literalinclude:: schemas/ComplianceRuleset.json
        """
        return self._put(route='CompliancePolicy', payload=ruleset)

    def delete_ruleset(self, id):
        """Delete a Compliance ruleset

        Args:
            id (str): ID of the ruleset
        
        Returns:
            bool: Deletion status
        """
        return self._delete(route='CompliancePolicy/%s' % str(id))


    # ------------------ Remediations ------------------
    # --------------------------------------------------

    def list_remediations(self):
        """List Remediations
        
        Returns:
            list: List of Remediation object.

        Response object:
            .. literalinclude:: schemas/Remediation.json
        """
        return self._get(route='ComplianceRemediation')

    def create_remediation(self, remediation):
        """Create a Remediation

        Args:
            remediation (dict): Remediation object.
        
        Returns:
            dict: Remediation object.

        Response object:
            .. literalinclude:: schemas/Remediation.json
        """
        return self._post(route='ComplianceRemediation', payload=remediation)

    def update_remediation(self, remediation):
        """Update a Remediation

        Args:
            remediation (dict): Remediation object.
        
        Returns:
            dict: Remediation object.

        Response object:
            .. literalinclude:: schemas/Remediation.json
        """
        return self._put(route='ComplianceRemediation', payload=remediation)

    def delete_remediation(self, id):
        """Delete a Remediation

        Args:
            id (str): ID of the remediation
        
        Returns:
            bool: Deletion status
        """
        return self._delete(route='ComplianceRemediation/%s' % str(id))


    # ------------------  Exclusions  ------------------
    # --------------------------------------------------

    def list_exclusions(self):
        """List all exclusions
        
        Returns:
            list: List of Exclusion object.

        Response object:
            .. literalinclude:: schemas/Exclusion.json
        """
        return self._get(route='Exclusion')

    def delete_exclusion(self, id):
        """Delete an exclusion
        
        Args:
            id (str): Id of the exclusion
        
        Returns:
            bool: Deletion status
        """
        return self._delete(route='Exclusion/%s' % str(id))


    # ------------------ Assessments  ------------------
    # --------------------------------------------------

    def run_assessment(self, rulesetId, cloudAccountId, region=None):
        """Run compliance assessments on Cloud Accounts, and get the results
        
        Args:
            rulesetId (int): Id of the Compliance Policy Ruleset to run
            cloudAccountId (str): Id of the Cloud Account
            region (str, optional): Set a specific region. Defaults to None.

        Returns:
            dict: AssessmentResult. Ref ./outputs/AssessmentResults.json

        Response object:
            .. literalinclude:: schemas/AssessmentResult.json
        """
        bundle = {
			'id': rulesetId,
			'cloudAccountId': cloudAccountId,
			'requestId': str(uuid.uuid4())
		}
        if region:
            bundle['region'] = region
        results = self._post(route='assessment/bundleV2', payload=json.dumps(bundle))
        return results
