# Frequently asked questions

## How do we know AI companies/bots respect `robots.txt`?

The short answer is that we don't. `robots.txt` is a well-established standard but compliance is voluntary. There is no enforcement mechanism.

## Can we block crawlers based on user agent strings?

Yes, provided the crawlers identify themselves and your application/hosting supports doing so.

## What can we do if a bot doesn't respect `robots.txt`?

That depends on your stack.

- Nginx
  - [Blocking Bots with Nginx](https://rknight.me/blog/blocking-bots-with-nginx/) by Robb Knight
  - [Blocking AI web crawlers](https://underlap.org/blocking-ai-web-crawlers) by Glyn Normington
- Apache httpd
  - [Blockin' bots.](https://ethanmarcotte.com/wrote/blockin-bots/) by Ethan Marcotte
  - [Blocking Bots With 11ty And Apache](https://flamedfury.com/posts/blocking-bots-with-11ty-and-apache/) by fLaMEd fury
> [!TIP]
> The snippets in these articles all use `mod_rewrite`, which [should be considered a last resort](https://httpd.apache.org/docs/trunk/rewrite/avoid.html). A good alternative that's less resource-intensive is `mod_setenvif`; see [httpd docs](https://httpd.apache.org/docs/trunk/rewrite/access.html#blocking-of-robots) for an example.
- Netlify
  - [Blockin' bots on Netlify](https://www.jeremiak.com/blog/block-bots-netlify-edge-functions/) by Jeremia Kimelman
- Cloudflare
  - [I’m blocking AI crawlers](https://roelant.net/en/2024/im-blocking-ai-crawlers-part-2/) by Roelant

## Why should we block these crawlers?

They're extractive, confer no benefit to the creators of data they're ingesting and also have wide-ranging negative externalities.

**[How Tech Giants Cut Corners to Harvest Data for A.I.](https://www.nytimes.com/2024/04/06/technology/tech-giants-harvest-data-artificial-intelligence.html?unlocked_article_code=1.ik0.Ofja.L21c1wyW-0xj&ugrp=m)**
> OpenAI, Google and Meta ignored corporate policies, altered their own rules and discussed skirting copyright law as they sought online information to train their newest artificial intelligence systems.

**[How AI copyright lawsuits could make the whole industry go extinct](https://www.theverge.com/24062159/ai-copyright-fair-use-lawsuits-new-york-times-openai-chatgpt-decoder-podcast)**
> The New York Times' lawsuit against OpenAI is part of a broader, industry-shaking copyright challenge that could define the future of AI.

## How can I contribute?

Open a pull request. It will be reviewed and acted upon appropriately. **We really appreciate contributions** — this is a community effort.
