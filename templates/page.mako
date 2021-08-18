<%!
    id_ = "default"
    type_ = "PageHCF"
    title = "Default"

    gutter = 15
    align = "center"
    bgcolor = "black"
    body_font = "Cantarell"
    head_font = "Fredoka One"
    title_font = "Bungee Shade"
%>

id: ${self.attr.id_}
type: ${self.attr.type_}
layout:
  contentJustify: ${self.attr.align}
properties:
  title: ${self.attr.title}
  style:
    background-color: ${self.attr.bgcolor}

<%block name="requests"/>

blocks:

  - id: main_menu
    type: Menu
    style:
      text-align: ${self.attr.align}
      font-family: ${self.attr.head_font}
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

  - id: cover
    type: Card
    layout:
      contentGutter: ${self.attr.gutter}
    blocks:
      <%block name="contents"/>
      <%block name="footer">
      - id: footer
        type: Markdown
        properties:
          style:
            text-align: center
            font-family: ${self.attr.head_font}
          skipHtml: true
          content: |
            Copyright &#xa9; 2021 Ujjwal Panda
      </%block>