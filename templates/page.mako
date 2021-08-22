id: ${pgid}
type: ${pgctx}
properties:
  title: ${self.title()}
  style:
    text-align: ${pgalign}
    font-family: ${hdfont}
    background-color: ${bgcolor}

<%block name="requests"/>

blocks:

  <%block name="menu">
  - id: menu
    type: Menu
    style:
      text-align: ${mnalign}
      font-family: ${hdfont}
    properties:
      mode: horizontal
      links:
      % for page in pages:
        - id: ${page}_menu
          type: MenuLink
          pageId: ${page}
          properties:
            title: ${page.title().replace("_", " ")}
      % endfor
  </%block>

  <%block name="contents">
  - id: cover
    type: Card
    layout:
      contentGutter: ${gutter}
    blocks:
      <%block name="pghead">
      - id: title
        type: Title
        properties:
          content: ${self.title()}
          level: 1
          style:
            text-align: ${ttalign}
            font-family: ${ttfont}
          underline: true
      </%block>
      <%block name="pgbody"/>
      <%block name="pgfoot">
      - id: footer
        type: Markdown
        properties:
          style:
            text-align: center
            font-family: ${hdfont}
          skipHtml: true
          content: |
            Copyright &#xa9; 2021 Ujjwal Panda
      </%block>
  </%block>
