import dome9

d9 = dome9.Dome9()

ruleset = {
    "description": "vamooooos",
    "cloudVendor": "Aws",
    "minFeatureTier": "Advanced",
    "rules": [],
    "hideInCompliance": True,
    "id": 91301,
    "name": "chusta"
}

d9.delete_ruleset('91301')