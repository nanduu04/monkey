import Form from 'react-jsonschema-form-bs4';
import React, {useState, useEffect} from 'react';
import {Nav} from 'react-bootstrap';
import _ from 'lodash';

const sectionOrder = [
  'exploitation',
  'network_scan',
  'credentials',
  'maximum_depth'
];

const initialSection = sectionOrder[0];

export default function PropagationConfig(props) {
  const {
    schema,
    uiSchema,
    onChange,
    customFormats,
    className,
    formData
  } = props;
  const [selectedSection, setSelectedSection] = useState(initialSection);
  const [displayedSchema, setDisplayedSchema] = useState(getSchemaByKey(schema, initialSection));
  const [displayedSchemaUi, setDisplayedSchemaUi] = useState(getUiSchemaByKey(uiSchema, initialSection));
  const [localFormData, setLocalFormData] = useState(formData[initialSection]);

  useEffect(() => {
    setLocalFormData(formData[selectedSection]);
    setDisplayedSchema(getSchemaByKey(schema, selectedSection));
    setDisplayedSchemaUi(getUiSchemaByKey(uiSchema, selectedSection));
    setLocalFormData(formData[selectedSection]);
  }, [selectedSection])

  useEffect(() => {
    setLocalFormData(formData[selectedSection]);
  }, [formData])

  const onInnerDataChange = (innerData) => {
    let innerDataClone = _.clone(innerData);
    let formDataClone = _.clone(formData);

    formDataClone[selectedSection] = innerDataClone.formData;
    onChange({formData: formDataClone});
  }

  const setSection = (sectionKey) => {
    setSelectedSection(sectionKey);
  }

  const renderNav = () => {
    return (<Nav variant='tabs'
                 fill
                 activeKey={selectedSection} onSelect={setSection}
                 style={{'marginBottom': '2em'}}
                 className={'config-nav'}>
      {sectionOrder.map(section => {
        return (
          <Nav.Item key={section}>
            <Nav.Link eventKey={section}>{getNavTitle(schema, section)}</Nav.Link>
          </Nav.Item>);
      })}
    </Nav>)
  }


  return (<div>
    {renderNav()}
    <Form schema={displayedSchema}
          uiSchema={displayedSchemaUi}
          formData={localFormData}
          onChange={onInnerDataChange}
          customFormats={customFormats}
          className={className}
          liveValidate>
      <button type='submit' className={'hidden'}>Submit</button>
    </Form>
  </div>)
}

function getSchemaByKey(schema, key) {
  return schema['properties'][key];
}

function getUiSchemaByKey(uiSchema, key) {
  return uiSchema[key];
}

function getNavTitle(schema, key) {
  if (key === 'maximum_depth') {
    return 'General';
  }
  if (key === 'credentials') {
    return 'Credentials';
  }
  return schema['properties'][key].title;
}
