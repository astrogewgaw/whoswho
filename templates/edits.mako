<%inherit file="page.mako"/>

<%!
    id_ = "edits"
    title = "Submit edits to Who's Who"
%>

<%block name="requests">
requests:
  - id: save_data
    type: GoogleSheetAppendOne
    connectionId: edit_sheet
    properties:
      row:
      % for field in fields:
      person_${field.lower()}:
        _state: person_${field.lower()}
      % endfor
</%block>

<%block name="contents">
      - id: title
        type: Title
        properties:
          content: Submit edits to the Who's Who list.
          level: 1
          style:
            text-align: center
            font-family: Fredoka One
          underline: true
  
      % for field in fields:
      - id: person_${field.lower()}
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
          style:
            font-family: Fredoka One
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
          style:
            font-family: Fredoka One
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