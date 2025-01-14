import {Button, Form, Modal} from 'react-bootstrap';
import React, {useState} from 'react';

import FileSaver from 'file-saver';
import '../../styles/components/configuration-components/ExportConfigModal.scss';
import {encryptText} from '../utils/PasswordBasedEncryptor';
import {reformatConfig} from './ReformatHook';


type Props = {
  show: boolean,
  configuration: object,
  onHide: () => void
}

const ConfigExportModal = (props: Props) => {
  const [pass, setPass] = useState('');
  const [radioValue, setRadioValue] = useState('password');

  function isExportBtnDisabled() {
    return pass === '' && radioValue === 'password';
  }

  function onSubmit() {
    let config = reformatConfig(props.configuration, true);
    let config_export = {'metadata': {}, 'contents': null};

    if (radioValue === 'password') {
      config_export.contents = encryptText(JSON.stringify(config), pass);
      config_export.metadata = {'encrypted': true};
    } else {
      config_export.contents = config;
      config_export.metadata = {'encrypted': false};
    }

    let export_json = JSON.stringify(config_export, null, 2);
    let export_blob = new Blob(
      [export_json],
      {type: 'text/plain;charset=utf-8'}
    );
    FileSaver.saveAs(export_blob, 'monkey.conf');
    props.onHide();
  }

  return (
    <Modal show={props.show}
           onHide={props.onHide}
           size={'lg'}
           className={'config-export-modal'}>
      <Modal.Header closeButton>
        <Modal.Title>Configuration export</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <div key={'config-export-option'}
             className={`mb-3 export-type-radio-buttons`}>
          <Form>
            <Form.Check
              type={'radio'}
              className={'password-radio-button'}
              label={<PasswordInput onChange={setPass}/>}
              name={'export-choice'}
              value={'password'}
              onChange={evt => {
                setRadioValue(evt.target.value)
              }}
              checked={radioValue === 'password'}
            />
            <ExportPlaintextChoiceField onChange={setRadioValue}
                                        radioValue={radioValue}/>
          </Form>

        </div>
      </Modal.Body>
      <Modal.Footer>
        <Button variant={'info'}
                onClick={onSubmit}
                disabled={isExportBtnDisabled()}>
          Export
        </Button>
      </Modal.Footer>
    </Modal>)
}

const PasswordInput = (props: {
  onChange: (passValue) => void
}) => {
  return (
    <div className={'config-export-password-input'}>
      <p>Encrypt with a password:</p>
      <Form.Control type='password'
                    placeholder='Password'
                    onChange={evt => (props.onChange(evt.target.value))}/>
    </div>
  )
}

const ExportPlaintextChoiceField = (props: {
  radioValue: string,
  onChange: (radioValue) => void
}) => {
  return (
    <div className={'config-export-plaintext'}>
      <Form.Check
        type={'radio'}
        label={'Skip encryption (export as plaintext)'}
        name={'export-choice'}
        value={'plaintext'}
        checked={props.radioValue === 'plaintext'}
        onChange={evt => {
          props.onChange(evt.target.value);
        }}
      />
      <p className={`export-warning text-secondary`}>
        Configuration may contain stolen credentials or sensitive data.<br/>
        It is recommended that you use the <b>Encrypt with a password</b> option.
      </p>
    </div>
  )
}


export default ConfigExportModal;
