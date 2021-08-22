<%inherit file="page.mako"/>

<%block name="title">The Who's Who database</%block>

<%block name="pgbody">
      - id: intro
        type: Markdown
        properties:
          style:
            text-align: ${txalign}
            font-family: ${bdfont}
          content: |
            The list.

      - id: table
        type: AgGridAlpine
        properties:
          style:
            font-family: ${bdfont}
          pagination: true
          rowData:
            _ref: public/whoswho.json
          defaultColDef:
            sortable: true
            resizable: true
            filter: true
          columnDefs:
            % for field in fields:
            - headeName: ${field}
              field: ${field}
              width: 350
              % if field in ["Email", "Website", "Twitter"]:
              cellRenderer:
                _function:
                  __string.concat:
                    % if field == "Email":
                    <%text>
                    - '<a href="mailto:'
                    </%text>
                    % elif field == "Website":
                    <%text>
                    - '<a href="'
                    </%text>
                    % elif field == "Twitter":
                    <%text>
                    - '<a href="https://twitter.com/'
                    </%text>
                    % endif
                    - __args: 0.data.${field}
                    - '">'
                    - __args: 0.data.${field}
                    <%text>
                    - </a>
                    </%text>
              % endif
            % endfor
      
      - id: download_button
        type: Button
        properties:
          block: true
          title: "Download as CSV"
          type: primary
          icon: SaveOutlined
          style:
            font-family: ${hdfont}
        events:
          onClick:
            - id: download
              type: CallMethod
              params:
                blockId: table
                method: exportDataAsCsv
                args:
                  - fileName: whoswho.csv
</%block>