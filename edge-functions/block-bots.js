/**
* block-bots.js
* View the original post by Jeremia Kimelman at:
* https://www.jeremiak.com/blog/block-bots-netlify-edge-functions/
*
* modify `netlify.toml`
* [[edge_functions]]
* function = "block-bots"
* path = "/*"
*
* Place at `netlify/edge-functions/block-bots.js`
*
* (Or adapt for your edge function-supporting platform of choice.)
*/

// inspired (and taken) from ethan marcotte's blog post
// https://ethanmarcotte.com/wrote/blockin-bots/
const botUas = [
  'AdsBot-Google',
  'Amazonbot',
  'anthropic-ai',
  'Applebot-Extended',
  'AwarioRssBot',
  'AwarioSmartBot',
  'Bytespider',
  'CCBot',
  'ChatGPT-User',
  'ClaudeBot',
  'Claude-Web',
  'cohere-ai',
  'DataForSeoBot',
  'Diffbot',
  'FacebookBot',
  'FriendlyCrawler',
  'Google-Extended',
  'GoogleOther',
  'GPTBot',
  'img2dataset',
  'ImagesiftBot',
  'magpie-crawler',
  'Meltwater',
  'omgili',
  'omgilibot',
  'peer39_crawler',
  'peer39_crawler/1.0',
  'PerplexityBot',
  'PiplBot',
  'scoop.it',
  'Seekr',
  'YouBot',
]

export default async (request, context) => {
  const ua = request.headers.get('user-agent');

  let isBot = false

  botUas.forEach(u => {
    if (ua.toLowerCase().includes(u.toLowerCase())) {
      isBot = true
    }
  })

  const response = isBot ? new Response(null, { status: 401 }) : await context.next();
  return response
};
