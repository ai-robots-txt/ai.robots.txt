# Frequently asked questions

## Why should we block these crawlers?

They're extractive, confer no benefit to the creators of data they're ingesting and also have wide-ranging negative externalities: particularly copyright abuse and environmental impact.

**[How Tech Giants Cut Corners to Harvest Data for A.I.](https://www.nytimes.com/2024/04/06/technology/tech-giants-harvest-data-artificial-intelligence.html?unlocked_article_code=1.ik0.Ofja.L21c1wyW-0xj&ugrp=m)**
> OpenAI, Google and Meta ignored corporate policies, altered their own rules and discussed skirting copyright law as they sought online information to train their newest artificial intelligence systems.

**[How AI copyright lawsuits could make the whole industry go extinct](https://www.theverge.com/24062159/ai-copyright-fair-use-lawsuits-new-york-times-openai-chatgpt-decoder-podcast)**
> The New York Times' lawsuit against OpenAI is part of a broader, industry-shaking copyright challenge that could define the future of AI.

**[Reconciling the contrasting narratives on the environmental impact of large language models](https://www.nature.com/articles/s41598-024-76682-6)**
> Studies have shown that the training of just one LLM can consume as much energy as five cars do across their lifetimes. The water footprint of AI is also substantial; for example, recent work has highlighted that water consumption associated with AI models involves data centers using millions of gallons of water per day for cooling. Additionally, the energy consumption and carbon emissions of AI are projected to grow quickly in the coming years [...].

**[Scientists Predict AI to Generate Millions of Tons of E-Waste](https://www.sciencealert.com/scientists-predict-ai-to-generate-millions-of-tons-of-e-waste)**
> we could end up with between 1.2 million and 5 million metric tons of additional electronic waste by the end of this decade [the 2020's].

## How do we know AI companies/bots respect `robots.txt`?

The short answer is that we don't. `robots.txt` is a well-established standard, but compliance is voluntary. There is no enforcement mechanism.

## Why might AI web crawlers respect `robots.txt`?

Larger and/or reputable companies developing AI models probably wouldn't want to damage their reputation by ignoring `robots.txt`.

Also, given the contentious nature of AI and the possibility of legislation limiting its development, companies developing AI models will probably want to be seen to be behaving ethically, and so should (eventually) respect `robots.txt`.

## Can we block crawlers based on user agent strings?

Yes, provided the crawlers identify themselves and your application/hosting supports doing so.

Some crawlers — [such as Perplexity](https://rknight.me/blog/perplexity-ai-is-lying-about-its-user-agent/) — do not identify themselves via their user agent strings and, as such, are difficult to block.

## What can we do if a bot doesn't respect `robots.txt`?

That depends on your stack.

- Nginx
  - [Blocking Bots with Nginx](https://rknight.me/blog/blocking-bots-with-nginx/) by Robb Knight
  - [Blocking AI web crawlers](https://underlap.org/blocking-ai-web-crawlers) by Glyn Normington
- Apache httpd
  - [Blockin' bots.](https://ethanmarcotte.com/wrote/blockin-bots/) by Ethan Marcotte
  - [Blocking Bots With 11ty And Apache](https://flamedfury.com/posts/blocking-bots-with-11ty-and-apache/) by fLaMEd fury
  > [!TIP]
  > The snippets in these articles all use `mod_rewrite`, which [should be considered a last resort](https://httpd.apache.org/docs/trunk/rewrite/avoid.html). A good alternative that's less resource-intensive is `mod_setenvif`; see [httpd docs](https://httpd.apache.org/docs/trunk/rewrite/access.html#blocking-of-robots) for an example. You should also consider [setting this up in `httpd.conf` instead of `.htaccess`](https://httpd.apache.org/docs/trunk/howto/htaccess.html#when) if it's available to you.
- Netlify
  - [Blockin' bots on Netlify](https://www.jeremiak.com/blog/block-bots-netlify-edge-functions/) by Jeremia Kimelman
- Cloudflare
  - [Block AI bots, scrapers and crawlers with a single click](https://blog.cloudflare.com/declaring-your-aindependence-block-ai-bots-scrapers-and-crawlers-with-a-single-click) by Cloudflare
  - [I’m blocking AI crawlers](https://roelant.net/en/2024/im-blocking-ai-crawlers-part-2/) by Roelant
- Vercel
  - [Block AI Bots Firewall Rule](https://vercel.com/templates/firewall/block-ai-bots-firewall-rule) by Vercel

## How can I contribute?

Open a pull request. It will be reviewed and acted upon appropriately. **We really appreciate contributions** — this is a community effort.

## I'd like to donate money

That's kind of you, but we don't need your money. If you insist, we'd love you to make a donation to the [American Civil Liberties Union](https://www.aclu.org/), the [Disasters Emergency Committee](https://www.dec.org.uk/), or a similar organisation.

## Can my company sponsor ai.robots.txt?

No, thank you. We do not accept sponsorship of any kind. We prefer to maintain our independence. Our costs are negligible as we are entirely volunteer-based and community-driven.
