# ai.robots.txt

<img src="/assets/images/noai-logo.png" width="100" />

This list contains AI-related crawlers of all types, regardless of purpose. We encourage you to contribute to and implement this list on your own site. See [information about the listed crawlers](./table-of-bot-metrics.md) and the [FAQ](https://github.com/ai-robots-txt/ai.robots.txt/blob/main/FAQ.md).

A number of these crawlers have been sourced from [Dark Visitors](https://darkvisitors.com) and we appreciate the ongoing effort they put in to track these crawlers. 

If you'd like to add information about a crawler to the list, please make a pull request with the bot name added to `robots.txt`, `ai.txt`, and any relevant details in `table-of-bot-metrics.md` to help people understand what's crawling.

## Usage

This repository provides the following files:
- `robots.txt`
- `.htaccess`
- `nginx-block-ai-bots.conf`
- `Caddyfile`
- `haproxy-block-ai-bots.txt`

`robots.txt` implements the Robots Exclusion Protocol ([RFC 9309](https://www.rfc-editor.org/rfc/rfc9309.html)).

`.htaccess` may be used to configure web servers such as [Apache httpd](https://httpd.apache.org/) to return an error page when one of the listed AI crawlers sends a request to the web server.
Note that, as stated in the [httpd documentation](https://httpd.apache.org/docs/current/howto/htaccess.html), more performant methods than an `.htaccess` file exist.

`nginx-block-ai-bots.conf` implements a Nginx configuration snippet that can be included in any virtual host `server {}` block via the `include` directive.

`Caddyfile` includes a Header Regex matcher group you can copy or import into your Caddyfile, the rejection can then be handled as followed `abort @aibots`

`haproxy-block-ai-bots.txt` may be used to configure HAProxy to block AI bots. To implement it;
1. Add the file to the config directory of HAProxy
2. Add the following lines in the `frontend` section;
   ```
   acl ai_robot hdr_sub(user-agent) -i -f /etc/haproxy/haproxy-block-ai-bots.txt
   http-request deny if ai_robot
   ```
   (Note that the path of the `haproxy-block-ai-bots.txt` may be different in your environment.)


[Bing uses the data it crawls for AI and training, you may opt out by adding a `meta` tag to the `head` of your site.](./docs/additional-steps/bing.md)

### Related

- [Robots.txt Traefik plugin](https://plugins.traefik.io/plugins/681b2f3fba3486128fc34fae/robots-txt-plugin):
middleware plugin for [Traefik](https://traefik.io/traefik/) to automatically add rules of [robots.txt](./robots.txt)
file on-the-fly.

- Alternatively you can [manually configure Traefik](./docs/traefik-manual-setup.md) to centrally serve a static `robots.txt`.
## Contributing

A note about contributing: updates should be added/made to `robots.json`. A GitHub action will then generate the updated `robots.txt`, `table-of-bot-metrics.md`, `.htaccess` and `nginx-block-ai-bots.conf`.

You can run the tests by [installing](https://www.python.org/about/gettingstarted/) Python 3, installing the depenendcies, and then issuing:
```console
python code/tests.py


### Installing Dependencies

Before running the tests, install all required Python packages:
pip install -r requirements.txt


```

## Releasing

Admins may ship a new release `v1.n` (where `n` increments the minor version of the current release) as follows:

* Navigate to the [new release page](https://github.com/ai-robots-txt/ai.robots.txt/releases/new) on GitHub.
* Click `Select tag`, choose `Create new tag`, enter `v1.n` in the pop-up, and click `Create`.
* Enter a suitable release title (e.g. `v1.n: adds user-agent1, user-agent2`).
* Click `Generate release notes`.
* Click `Publish release`.

A GitHub action will then add the asset `robots.txt` to the release. That's it.

## Subscribe to updates

You can subscribe to list updates via RSS/Atom with the releases feed:

```
https://github.com/ai-robots-txt/ai.robots.txt/releases.atom
```

You can subscribe with [Feedly](https://feedly.com/i/subscription/feed/https://github.com/ai-robots-txt/ai.robots.txt/releases.atom), [Inoreader](https://www.inoreader.com/?add_feed=https://github.com/ai-robots-txt/ai.robots.txt/releases.atom), [The Old Reader](https://theoldreader.com/feeds/subscribe?url=https://github.com/ai-robots-txt/ai.robots.txt/releases.atom), [Feedbin](https://feedbin.me/?subscribe=https://github.com/ai-robots-txt/ai.robots.txt/releases.atom), or any other reader app.

Alternatively, you can also subscribe to new releases with your GitHub account by clicking the ⬇️ on "Watch" button at the top of this page, clicking "Custom" and selecting "Releases".

## License content with RSL

It is also possible to license your content to AI companies in `robots.txt` using 
the [Really Simple Licensing](https://rslstandard.org) standard, with an option of 
collective bargaining. A [plugin](https://github.com/Jameswlepage/rsl-wp) currently
implements RSL as well as payment processing for WordPress sites.

## Report abusive crawlers

If you use [Cloudflare's hard block](https://blog.cloudflare.com/declaring-your-aindependence-block-ai-bots-scrapers-and-crawlers-with-a-single-click) alongside this list, you can report abusive crawlers that don't respect `robots.txt` [here](https://docs.google.com/forms/d/e/1FAIpQLScbUZ2vlNSdcsb8LyTeSF7uLzQI96s0BKGoJ6wQ6ocUFNOKEg/viewform).
But even if you don't use Cloudflare's hard block, their list of [verified bots](https://radar.cloudflare.com/traffic/verified-bots) may come in handy.
## Additional resources

- [Blocking Bots with Nginx](https://rknight.me/blog/blocking-bots-with-nginx/) by Robb Knight
- [Blockin' bots.](https://ethanmarcotte.com/wrote/blockin-bots/) by Ethan Marcotte
- [Blocking Bots With 11ty And Apache](https://flamedfury.com/posts/blocking-bots-with-11ty-and-apache/) by fLaMEd fury
- [Blockin' bots on Netlify](https://www.jeremiak.com/blog/block-bots-netlify-edge-functions/) by Jeremia Kimelman
- [Blocking AI web crawlers](https://underlap.org/blocking-ai-web-crawlers) by Glyn Normington
- [Block AI Bots from Crawling Websites Using Robots.txt](https://originality.ai/ai-bot-blocking) by Jonathan Gillham, Originality.AI


