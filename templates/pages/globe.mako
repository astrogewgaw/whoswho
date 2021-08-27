<%inherit file="page.mako"/>
<%block name="title">The Astrochemists' World Map</%block>

<%block name="pgbody">
      - id: intro
        type: Markdown
        properties:
          style:
            text-align: ${settings.txalign}
            font-family: ${settings.bdfont}
          content:
            _ref: content/${pgid}.md
</%block>