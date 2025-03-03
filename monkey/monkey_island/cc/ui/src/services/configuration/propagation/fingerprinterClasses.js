const FINGERPRINTER_CLASSES = {
  'title': 'Fingerprinters',
  'description': 'Fingerprint modules collect info about external services ' +
  'Infection Monkey scans.',
  'type': 'string',
  'pluginDefs': {
    'smb' : {'name':'smb', 'options':''},
    'ssh' : {'name':'ssh', 'options':''},
    'http' : {'name':'http', 'options':''},
    'mssql' : {'name':'mssql', 'options':''},
    'elastic' : {'name':'elastic', 'options':''}
  },
  'anyOf': [
    {
      'type': 'string',
      'enum': ['smb'],
      'title': 'SMB Fingerprinter',
      'safe': true,
      'info': 'Figures out if SMB is running and what\'s the version of it.'
    },
    {
      'type': 'string',
      'enum': ['ssh'],
      'title': 'SSH Fingerprinter',
      'safe': true,
      'info': 'Figures out if SSH is running.'
    },
    {
      'type': 'string',
      'enum': ['http'],
      'title': 'HTTP Fingerprinter',
      'safe': true,
      'info': 'Checks if host has HTTP/HTTPS ports open.'
    },
    {
      'type': 'string',
      'enum': ['mssql'],
      'title': 'MSSQL Fingerprinter',
      'safe': true,
      'info': 'Checks if Microsoft SQL service is running and tries to gather ' +
      'information about it.'
    },
    {
      'type': 'string',
      'enum': ['elastic'],
      'title': 'Elastic Fingerprinter',
      'safe': true,
      'info': 'Checks if ElasticSearch is running and attempts to find it\'s version.'
    }
  ]

}

export default FINGERPRINTER_CLASSES;
