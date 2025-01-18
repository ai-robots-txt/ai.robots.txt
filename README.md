# ai.robots.txt

<img src="/assets/images/noai-logo.png" width="100" />

This is an open list of web crawlers associated with AI companies and the training of LLMs to block. We encourage you to contribute to and implement this list on your own site. See [information about the listed crawlers](./table-of-bot-metrics.md) and the [FAQ](https://github.com/ai-robots-txt/ai.robots.txt/blob/main/FAQ.md).

A number of these crawlers have been sourced from [Dark Visitors](https://darkvisitors.com) and we appreciate the ongoing effort they put in to track these crawlers. 

If you'd like to add information about a crawler to the list, please make a pull request with the bot name added to `robots.txt`, `ai.txt`, and any relevant details in `table-of-bot-metrics.md` to help people understand what's crawling.

## Usage

Many visitors will find these files from this repository most useful:
- `robots.txt`
- `.htaccess`

`robots.txt` implements the Robots Exclusion Protocol ([RFC 9309](https://www.rfc-editor.org/rfc/rfc9309.html)).

The second one tells your own webserver to return an error page when one of the listed AI crawlers tries to request a page from your website. A `.htaccess` file does not work on every webserver, but works correctly on most common and cheap shared hosting providers. The majority of AI crawlers set a "User Agent" string in every request they send, by which they are identifiable: this string is used to filter the request. Instead of simply hoping the crawler pledges to respect our intention, this solution actively sends back a bad webpage (an error or an empty page). Note that this solution isn't bulletproof either, as anyone can fake the sent User Agent.

Note that, as stated in the [httpd documentation](https://httpd.apache.org/docs/current/howto/htaccess.html), more performant methods than an `.htaccess` file exist. Nevertheless, most shared hosting providers only allow `.htaccess` configuration.


## Contributing

A note about contributing: updates should be added/made to `robots.json`. A GitHub action, courtesy of [Adam](https://github.com/newbold), will then generate the updated `robots.txt` and `table-of-bot-metrics.md`.

## Subscribe to updates

You can subscribe to list updates via RSS/Atom with the releases feed:

```
https://github.com/ai-robots-txt/ai.robots.txt/releases.atom
```

You can subscribe with [Feedly](https://feedly.com/i/subscription/feed/https://github.com/ai-robots-txt/ai.robots.txt/releases.atom), [Inoreader](https://www.inoreader.com/?add_feed=https://github.com/ai-robots-txt/ai.robots.txt/releases.atom), [The Old Reader](https://theoldreader.com/feeds/subscribe?url=https://github.com/ai-robots-txt/ai.robots.txt/releases.atom), [Feedbin](https://feedbin.me/?subscribe=https://github.com/ai-robots-txt/ai.robots.txt/releases.atom), or any other reader app.

Alternatively, you can also subscribe to new releases with your GitHub account by clicking the ⬇️ on "Watch" button at the top of this page, clicking "Custom" and selecting "Releases".

## Report abusive crawlers

If you use [Cloudflare's hard block](https://blog.cloudflare.com/declaring-your-aindependence-block-ai-bots-scrapers-and-crawlers-with-a-single-click) alongside this list, you can report abusive crawlers that don't respect `robots.txt` [here](https://docs.google.com/forms/d/e/1FAIpQLScbUZ2vlNSdcsb8LyTeSF7uLzQI96s0BKGoJ6wQ6ocUFNOKEg/viewform).

## Additional resources

- [Blocking Bots with Nginx](https://rknight.me/blog/blocking-bots-with-nginx/) by Robb Knight
- [Blockin' bots.](https://ethanmarcotte.com/wrote/blockin-bots/) by Ethan Marcotte
- [Blocking Bots With 11ty And Apache](https://flamedfury.com/posts/blocking-bots-with-11ty-and-apache/) by fLaMEd fury
- [Blockin' bots on Netlify](https://www.jeremiak.com/blog/block-bots-netlify-edge-functions/) by Jeremia Kimelman
- [Blocking AI web crawlers](https://underlap.org/blocking-ai-web-crawlers) by Glyn Normington
- [Block AI Bots from Crawling Websites Using Robots.txt](https://originality.ai/ai-bot-blocking) by Jonathan Gillham, Originality.AI
