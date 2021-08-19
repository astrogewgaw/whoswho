<%inherit file="page.mako"/>

<%!
    id_ = "about"
    title = "About Who's Who"
%>

<%block name="contents">
      - id: title
        type: Title
        properties:
          level: 1
          content: Who's Who?
          style:
            text-align: center
            font-family: ${self.attr.title_font}
      - id: netlify_status
        type: Markdown
        properties:
          style:
            text-align: center
          content: |
            [![Netlify Status][deploy-status]][deploys]
            
            [deploys]: https://app.netlify.com/sites/whoswho/deploys
            [deploy-status]: https://api.netlify.com/api/v1/badges/ebd6006f-31b2-4fb4-bde0-b358aee83986/deploy-status
      - id: badges
        type: Markdown
        properties:
          style:
            text-align: center
          content: |
            ![License][license]
            [![Gitmoji][gitmoji-badge]][gitmoji]

            ![Last Updated][updated]

            ![Count][count]
            ![Contactable][contactable]
            ![Tweeters][tweeters]

            [gitmoji]: https://gitmoji.dev
            [license]: https://img.shields.io/github/license/astrogewgaw/whoswho?style=for-the-badge
            [gitmoji-badge]: https://img.shields.io/badge/gitmoji-%20😜%20😍-FFDD67.svg?style=for-the-badge
            [count]: https://img.shields.io/badge/Astrochemists-${count | u}-blueviolet?style=for-the-badge
            [tweeters]: https://img.shields.io/badge/Tweeters-${tweeters | u}-blue?style=for-the-badge&logo=twitter            
            [contactable]: https://img.shields.io/badge/Contactable-${contactable | u}-darkgreen?style=for-the-badge
            [updated]: https://img.shields.io/badge/Last%20Updated-${updated.replace(" ", "%20")}-purple?style=for-the-badge
      
      - id: subtitle
        type: Title
        properties:
          level: 2
          content: A list 📝 of astrochemists 🧪 from across the globe 🌏 !
          style:
            text-align: center
            font-family: ${self.attr.head_font}
      - id: intro
        type: Markdown
        properties:
          style:
            text-align: justify
            font-family: ${self.attr.body_font}
          content:
</%block>
