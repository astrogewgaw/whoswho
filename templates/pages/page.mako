id: ${pgid}
type: ${settings.pgctx}
properties:
  title: ${self.title()}
  style:
    text-align: ${settings.pgalign}
    font-family: ${settings.hdfont}
    background-color: ${settings.bgcolor}

<%block name="requests"/>

blocks:

  <%block name="menu">
  - id: menu
    type: Menu
    style:
      text-align: ${settings.mnalign}
      font-family: ${settings.hdfont}
    properties:
      mode: horizontal
      links:
      % for page in settings.pages:
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
      contentGutter: ${settings.gutter}
    blocks:
      <%block name="pghead">
      - id: title
        type: Title
        properties:
          content: ${self.title()}
          level: 1
          style:
            text-align: ${settings.ttalign}
            font-family: ${settings.ttfont}
      </%block>
      <%block name="pgbody"/>
      <%block name="pgfoot">
      - id: footer
        type: Markdown
        properties:
          style:
            text-align: center
          skipHtml: true
          content: |
            <%
            import arrow
            current_year = arrow.now().year
            %>
            Copyright &#xa9; ${current_year} ${meta.author}
      </%block>
  </%block>
