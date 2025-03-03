import NETWORK_SCAN_CONFIGURATION_SCHEMA from './networkScan.js';
import CREDENTIALS from './credentials';
import EXPLOITATION_CONFIGURATION_SCHEMA from './exploitation';

const PROPAGATION_CONFIGURATION_SCHEMA = {
  'title': 'Propagation',
  'type': 'object',
  'properties': {
    'exploitation': EXPLOITATION_CONFIGURATION_SCHEMA,
    'credentials': CREDENTIALS,
    'maximum_depth': {
      'title': 'Maximum scan depth',
      'type': 'integer',
      'minimum': 1,
      'default': 2,
      'description': 'Amount of hops allowed for the monkey to spread from the ' +
      'Island server. \n' +
      ' \u26A0' +
      ' Note that setting this value too high may result in the ' +
      'Monkey propagating too far, '+
      'if the "Local network scan" is enabled'
    },
    'network_scan': NETWORK_SCAN_CONFIGURATION_SCHEMA
  }
}
export default PROPAGATION_CONFIGURATION_SCHEMA;
