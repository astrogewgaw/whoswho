<%inherit file="page.mako"/>

<%block name="title">Submit edits to Who's Who</%block>

<%block name="requests">
requests:
  - id: save_data
    type: GoogleSheetAppendOne
    connectionId: edit_sheet
    properties:
      row:
      % for field in stats.columns:
      person_${field.lower()}:
        _state: person_${field.lower()}
      % endfor
</%block>
  
<%block name="pgbody">
      % for field in stats.columns:
      - id: person_${field.lower()}settings.
        type: TextInput
        required: true
        properties:
          title: ${field}
      % endfor
  
      - id: reset_button
        type: Button
        layout:
          span: 12
        properties:
          block: true
          title: Reset
          type: default
          icon: ClearOutlined
        events:
          onClick:
            - id: reset
              type: Reset
  
      - id: submit_button
        type: Button
        layout:
          span: 12
        properties:
          block: true
          title: Submit
          type: primary
          icon: SaveOutlined
        events:
          onClick:
            - id: validate
              type: Validate
            - id: save_data
              type: Request
              params: save_data
            - id: reset
              type: Reset
</%block>