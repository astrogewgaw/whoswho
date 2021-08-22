<%inherit file="page.mako"/>

<%block name="title">Who's Who in Astrochemistry</%block>

<%block name="pgbody">
      - id: netlify_status
        type: Markdown
        properties:
          style:
            text-align: ${ttalign}
          content: |
            [![Netlify Status][deploy-status]][deploys]
            
            [deploys]: https://app.netlify.com/sites/whoswho/deploys
            [deploy-status]: https://api.netlify.com/api/v1/badges/ebd6006f-31b2-4fb4-bde0-b358aee83986/deploy-status

      - id: badges
        type: Markdown
        properties:
          style:
            text-align: ${ttalign}
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
            text-align: ${ttalign}
            font-family: ${hdfont}

      - id: intro
        type: Markdown
        properties:
          style:
            text-align: ${txalign}
            font-family: ${bdfont}
          content:
</%block>