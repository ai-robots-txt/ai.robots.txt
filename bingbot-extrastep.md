# Bing (bingbot)

It's not well publicised, but Bing uses the data it crawls for AI and training.

However, the current thinking is, blocking a search engine of this size using `robots.txt` seems a quite drastic approach as it is second only to Google and could significantly impact your website in search results.

Additionally, Bing powers a number of search engines such as Yahoo and AOL, and its search results are also used in Duck Duck Go, amongst others.

Fortunately, Bing supports a relatively simple opt-out method, requiring an additional step.


## How to opt-out of AI training

You must add a metatag in the `<head>` of your webpage. This also needs to be added to every page on your website.

The line you need to add is:
```
<meta name="robots" content="noarchive">
```

By adding this line, you are signifying to Bing: "Do not use the content for training Microsoft's generative AI foundation models."


## Will my site be negatively affected

Simple answer, no.
The original use of "noarchive" has been retired by all search engines. Google retired its use in 2024.

The use of this metatag will not impact your site in search engines or in any other meaningful way if you add it to your page(s).

It is now solely used by a handful of crawlers, such as Bingbot and Amazonbot, to signify to them not to use your data for AI/training.



## Resources

Bing Blog AI opt-out announcement:
https://blogs.bing.com/webmaster/september-2023/Announcing-new-options-for-webmasters-to-control-usage-of-their-content-in-Bing-Chat

Bing metatag information, including AI opt-out:
https://www.bing.com/webmasters/help/which-robots-metatags-does-bing-support-5198d240
