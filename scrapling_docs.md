# Scrapling Documentation



---
## Source: https://scrapling.readthedocs.io/en/latest/
---

# Index

[![Scrapling](assets/cover_light.svg)![Scrapling](assets/cover_dark.svg)](https://scrapling.readthedocs.io/en/latest/)

## *Effortless Web Scraping for the Modern Web*

Scrapling is an adaptive Web Scraping framework that handles everything from a single request to a full-scale crawl.

Its parser learns from website changes and automatically relocates your elements when pages update. Its fetchers bypass anti-bot systems like Cloudflare Turnstile out of the box. And its spider framework lets you scale up to concurrent, multi-session crawls with pause/resume and automatic proxy rotation - all in a few lines of Python. One library, zero compromises.

Blazing fast crawls with real-time stats and streaming. Built by Web Scrapers for Web Scrapers and regular users, there's something for everyone.

```
from scrapling.fetchers import Fetcher, StealthyFetcher, DynamicFetcher
StealthyFetcher.adaptive = True
page = StealthyFetcher.fetch('https://example.com', headless=True, network_idle=True)  # Fetch website under the radar!
products = page.css('.product', auto_save=True)                                        # Scrape data that survives website design changes!
products = page.css('.product', adaptive=True)                                         # Later, if the website structure changes, pass `adaptive=True` to find them!
```

Or scale up to full crawls

```
from scrapling.spiders import Spider, Response

class MySpider(Spider):
  name = "demo"
  start_urls = ["https://example.com/"]

  async def parse(self, response: Response):
      for item in response.css('.product'):
          yield {"title": item.css('h2::text').get()}

MySpider().start()
```

## Top Sponsors[¶](#top-sponsors "Permanent link")

[![](https://raw.githubusercontent.com/D4Vinci/Scrapling/main/images/HyperSolutions.png)](https://hypersolutions.co/?utm_source=github&utm_medium=readme&utm_campaign=scrapling "Bot Protection Bypass API for Akamai, DataDome, Incapsula & Kasada")
[![](https://raw.githubusercontent.com/D4Vinci/Scrapling/main/images/BirdProxies.jpg)](https://birdproxies.com/t/scrapling "At Bird Proxies, we eliminate your pains such as banned IPs, geo restriction, and high costs so you can focus on your work.")
[![](https://raw.githubusercontent.com/D4Vinci/Scrapling/main/images/evomi.png)](https://evomi.com?utm_source=github&utm_medium=banner&utm_campaign=d4vinci-scrapling "Evomi is your Swiss Quality Proxy Provider, starting at $0.49/GB")
[![](https://raw.githubusercontent.com/D4Vinci/Scrapling/main/images/TikHub.jpg)](https://tikhub.io/?utm_source=github.com/D4Vinci/Scrapling&utm_medium=marketing_social&utm_campaign=retargeting&utm_content=carousel_ad "Unlock the Power of Social Media Data & AI")
[![](https://raw.githubusercontent.com/D4Vinci/Scrapling/main/images/nsocks.png)](https://www.nsocks.com/?keyword=2p67aivg "Scalable Web Data Access for AI Applications")
[![](https://raw.githubusercontent.com/D4Vinci/Scrapling/main/images/petrosky.png)](https://petrosky.io/d4vinci "PetroSky delivers cutting-edge VPS hosting.")
[![](https://raw.githubusercontent.com/D4Vinci/Scrapling/main/images/TWSC.png)](https://substack.thewebscraping.club/p/scrapling-hands-on-guide?utm_source=github&utm_medium=repo&utm_campaign=scrapling "The #1 newsletter dedicated to Web Scraping")
[![](https://raw.githubusercontent.com/D4Vinci/Scrapling/main/images/ProxySeller.png)](https://proxy-seller.com/?partner=CU9CAA5TBYFFT2 "Proxy-Seller provides reliable proxy infrastructure for Web Scraping")
[![](https://raw.githubusercontent.com/D4Vinci/Scrapling/main/images/MangoProxy.png)](http://mangoproxy.com/?utm_source=D4Vinci&utm_medium=GitHub&utm_campaign=D4Vinci "Proxies You Can Rely On: Residential, Server, and Mobile")

*Do you want to show your ad here? Click [here](https://github.com/sponsors/D4Vinci), choose a plan, and enjoy the rest of the perks!*

## Key Features[¶](#key-features "Permanent link")

### Spiders - A Full Crawling Framework[¶](#spiders-a-full-crawling-framework "Permanent link")

* 🕷️ **Scrapy-like Spider API**: Define spiders with `start_urls`, async `parse` callbacks, and `Request`/`Response` objects.
* ⚡ **Concurrent Crawling**: Configurable concurrency limits, per-domain throttling, and download delays.
* 🔄 **Multi-Session Support**: Unified interface for HTTP requests, and stealthy headless browsers in a single spider - route requests to different sessions by ID.
* 💾 **Pause & Resume**: Checkpoint-based crawl persistence. Press Ctrl+C for a graceful shutdown; restart to resume from where you left off.
* 📡 **Streaming Mode**: Stream scraped items as they arrive via `async for item in spider.stream()` with real-time stats - ideal for UI, pipelines, and long-running crawls.
* 🛡️ **Blocked Request Detection**: Automatic detection and retry of blocked requests with customizable logic.
* 📦 **Built-in Export**: Export results through hooks and your own pipeline or the built-in JSON/JSONL with `result.items.to_json()` / `result.items.to_jsonl()` respectively.

### Advanced Websites Fetching with Session Support[¶](#advanced-websites-fetching-with-session-support "Permanent link")

* **HTTP Requests**: Fast and stealthy HTTP requests with the `Fetcher` class. Can impersonate browsers' TLS fingerprint, headers, and use HTTP/3.
* **Dynamic Loading**: Fetch dynamic websites with full browser automation through the `DynamicFetcher` class supporting Playwright's Chromium and Google's Chrome.
* **Anti-bot Bypass**: Advanced stealth capabilities with `StealthyFetcher` and fingerprint spoofing. Can easily bypass all types of Cloudflare's Turnstile/Interstitial with automation.
* **Session Management**: Persistent session support with `FetcherSession`, `StealthySession`, and `DynamicSession` classes for cookie and state management across requests.
* **Proxy Rotation**: Built-in `ProxyRotator` with cyclic or custom rotation strategies across all session types, plus per-request proxy overrides.
* **Domain Blocking**: Block requests to specific domains (and their subdomains) in browser-based fetchers.
* **Async Support**: Complete async support across all fetchers and dedicated async session classes.

### Adaptive Scraping & AI Integration[¶](#adaptive-scraping-ai-integration "Permanent link")

* 🔄 **Smart Element Tracking**: Relocate elements after website changes using intelligent similarity algorithms.
* 🎯 **Smart Flexible Selection**: CSS selectors, XPath selectors, filter-based search, text search, regex search, and more.
* 🔍 **Find Similar Elements**: Automatically locate elements similar to found elements.
* 🤖 **MCP Server to be used with AI**: Built-in MCP server for AI-assisted Web Scraping and data extraction. The MCP server features powerful, custom capabilities that leverage Scrapling to extract targeted content before passing it to the AI (Claude/Cursor/etc), thereby speeding up operations and reducing costs by minimizing token usage. ([demo video](https://www.youtube.com/watch?v=qyFk3ZNwOxE))

### High-Performance & battle-tested Architecture[¶](#high-performance-battle-tested-architecture "Permanent link")

* 🚀 **Lightning Fast**: Optimized performance outperforming most Python scraping libraries.
* 🔋 **Memory Efficient**: Optimized data structures and lazy loading for a minimal memory footprint.
* ⚡ **Fast JSON Serialization**: 10x faster than the standard library.
* 🏗️ **Battle tested**: Not only does Scrapling have 92% test coverage and full type hints coverage, but it has been used daily by hundreds of Web Scrapers over the past year.

### Developer/Web Scraper Friendly Experience[¶](#developerweb-scraper-friendly-experience "Permanent link")

* 🎯 **Interactive Web Scraping Shell**: Optional built-in IPython shell with Scrapling integration, shortcuts, and new tools to speed up Web Scraping scripts development, like converting curl requests to Scrapling requests and viewing requests results in your browser.
* 🚀 **Use it directly from the Terminal**: Optionally, you can use Scrapling to scrape a URL without writing a single line of code!
* 🛠️ **Rich Navigation API**: Advanced DOM traversal with parent, sibling, and child navigation methods.
* 🧬 **Enhanced Text Processing**: Built-in regex, cleaning methods, and optimized string operations.
* 📝 **Auto Selector Generation**: Generate robust CSS/XPath selectors for any element.
* 🔌 **Familiar API**: Similar to Scrapy/BeautifulSoup with the same pseudo-elements used in Scrapy/Parsel.
* 📘 **Complete Type Coverage**: Full type hints for excellent IDE support and code completion. The entire codebase is automatically scanned with **PyRight** and **MyPy** with each change.
* 🔋 **Ready Docker image**: With each release, a Docker image containing all browsers is automatically built and pushed.

## Star History[¶](#star-history "Permanent link")

Scrapling’s GitHub stars have grown steadily since its release (see chart below).

[![Star History Chart](https://api.star-history.com/svg?repos=D4Vinci/Scrapling&type=Date)](https://github.com/D4Vinci/Scrapling)

## Installation[¶](#installation "Permanent link")

Scrapling requires Python 3.10 or higher:

```
pip install scrapling
```

This installation only includes the parser engine and its dependencies, without any fetchers or commandline dependencies.

### Optional Dependencies[¶](#optional-dependencies "Permanent link")

1. If you are going to use any of the extra features below, the fetchers, or their classes, you will need to install fetchers' dependencies and their browser dependencies as follows:

   ```
   pip install "scrapling[fetchers]"

   scrapling install           # normal install
   scrapling install  --force  # force reinstall
   ```

   This downloads all browsers, along with their system dependencies and fingerprint manipulation dependencies.

   Or you can install them from the code instead of running a command like this:

   ```
   from scrapling.cli import install

   install([], standalone_mode=False)          # normal install
   install(["--force"], standalone_mode=False) # force reinstall
   ```
2. Extra features:

   * Install the MCP server feature:

     ```
     pip install "scrapling[ai]"
     ```
   * Install shell features (Web Scraping shell and the `extract` command):

     ```
     pip install "scrapling[shell]"
     ```
   * Install everything:

     ```
     pip install "scrapling[all]"
     ```

     Don't forget that you need to install the browser dependencies with `scrapling install` after any of these extras (if you didn't already)

### Docker[¶](#docker "Permanent link")

You can also install a Docker image with all extras and browsers with the following command from DockerHub:

```
docker pull pyd4vinci/scrapling
```

Or download it from the GitHub registry:

```
docker pull ghcr.io/d4vinci/scrapling:latest
```

This image is automatically built and pushed using GitHub Actions and the repository's main branch.

## How the documentation is organized[¶](#how-the-documentation-is-organized "Permanent link")

Scrapling has extensive documentation, so we try to follow the [Diátaxis documentation framework](https://diataxis.fr/).

## Support[¶](#support "Permanent link")

If you like Scrapling and want to support its development:

* ⭐ Star the [GitHub repository](https://github.com/D4Vinci/Scrapling)
* 🚀 Follow us on [Twitter](https://x.com/Scrapling_dev) and join the [discord server](https://discord.gg/EMgGbDceNQ)
* 💝 Consider [sponsoring the project or buying me a coffee](donate.html) ![😉](https://cdn.jsdelivr.net/gh/jdecked/twemoji@16.0.1/assets/svg/1f609.svg ":wink:")
* 🐛 Report bugs and suggest features through [GitHub Issues](https://github.com/D4Vinci/Scrapling/issues)

## License[¶](#license "Permanent link")

This project is licensed under the BSD-3 License. See the [LICENSE](https://github.com/D4Vinci/Scrapling/blob/main/LICENSE) file for details.

Was this page helpful?

Thanks for your feedback!

Thanks for your feedback! Help us improve this page by
[opening a documentation issue](https://github.com/D4Vinci/Scrapling/issues/new?template=04-docs_issue.yml).


---
## Source: https://scrapling.readthedocs.io/en/latest/index.html
---

# Index

[![Scrapling](assets/cover_light.svg)![Scrapling](assets/cover_dark.svg)](https://scrapling.readthedocs.io/en/latest/)

## *Effortless Web Scraping for the Modern Web*

Scrapling is an adaptive Web Scraping framework that handles everything from a single request to a full-scale crawl.

Its parser learns from website changes and automatically relocates your elements when pages update. Its fetchers bypass anti-bot systems like Cloudflare Turnstile out of the box. And its spider framework lets you scale up to concurrent, multi-session crawls with pause/resume and automatic proxy rotation - all in a few lines of Python. One library, zero compromises.

Blazing fast crawls with real-time stats and streaming. Built by Web Scrapers for Web Scrapers and regular users, there's something for everyone.

```
from scrapling.fetchers import Fetcher, StealthyFetcher, DynamicFetcher
StealthyFetcher.adaptive = True
page = StealthyFetcher.fetch('https://example.com', headless=True, network_idle=True)  # Fetch website under the radar!
products = page.css('.product', auto_save=True)                                        # Scrape data that survives website design changes!
products = page.css('.product', adaptive=True)                                         # Later, if the website structure changes, pass `adaptive=True` to find them!
```

Or scale up to full crawls

```
from scrapling.spiders import Spider, Response

class MySpider(Spider):
  name = "demo"
  start_urls = ["https://example.com/"]

  async def parse(self, response: Response):
      for item in response.css('.product'):
          yield {"title": item.css('h2::text').get()}

MySpider().start()
```

## Top Sponsors[¶](#top-sponsors "Permanent link")

[![](https://raw.githubusercontent.com/D4Vinci/Scrapling/main/images/HyperSolutions.png)](https://hypersolutions.co/?utm_source=github&utm_medium=readme&utm_campaign=scrapling "Bot Protection Bypass API for Akamai, DataDome, Incapsula & Kasada")
[![](https://raw.githubusercontent.com/D4Vinci/Scrapling/main/images/BirdProxies.jpg)](https://birdproxies.com/t/scrapling "At Bird Proxies, we eliminate your pains such as banned IPs, geo restriction, and high costs so you can focus on your work.")
[![](https://raw.githubusercontent.com/D4Vinci/Scrapling/main/images/evomi.png)](https://evomi.com?utm_source=github&utm_medium=banner&utm_campaign=d4vinci-scrapling "Evomi is your Swiss Quality Proxy Provider, starting at $0.49/GB")
[![](https://raw.githubusercontent.com/D4Vinci/Scrapling/main/images/TikHub.jpg)](https://tikhub.io/?utm_source=github.com/D4Vinci/Scrapling&utm_medium=marketing_social&utm_campaign=retargeting&utm_content=carousel_ad "Unlock the Power of Social Media Data & AI")
[![](https://raw.githubusercontent.com/D4Vinci/Scrapling/main/images/nsocks.png)](https://www.nsocks.com/?keyword=2p67aivg "Scalable Web Data Access for AI Applications")
[![](https://raw.githubusercontent.com/D4Vinci/Scrapling/main/images/petrosky.png)](https://petrosky.io/d4vinci "PetroSky delivers cutting-edge VPS hosting.")
[![](https://raw.githubusercontent.com/D4Vinci/Scrapling/main/images/TWSC.png)](https://substack.thewebscraping.club/p/scrapling-hands-on-guide?utm_source=github&utm_medium=repo&utm_campaign=scrapling "The #1 newsletter dedicated to Web Scraping")
[![](https://raw.githubusercontent.com/D4Vinci/Scrapling/main/images/ProxySeller.png)](https://proxy-seller.com/?partner=CU9CAA5TBYFFT2 "Proxy-Seller provides reliable proxy infrastructure for Web Scraping")
[![](https://raw.githubusercontent.com/D4Vinci/Scrapling/main/images/MangoProxy.png)](http://mangoproxy.com/?utm_source=D4Vinci&utm_medium=GitHub&utm_campaign=D4Vinci "Proxies You Can Rely On: Residential, Server, and Mobile")

*Do you want to show your ad here? Click [here](https://github.com/sponsors/D4Vinci), choose a plan, and enjoy the rest of the perks!*

## Key Features[¶](#key-features "Permanent link")

### Spiders - A Full Crawling Framework[¶](#spiders-a-full-crawling-framework "Permanent link")

* 🕷️ **Scrapy-like Spider API**: Define spiders with `start_urls`, async `parse` callbacks, and `Request`/`Response` objects.
* ⚡ **Concurrent Crawling**: Configurable concurrency limits, per-domain throttling, and download delays.
* 🔄 **Multi-Session Support**: Unified interface for HTTP requests, and stealthy headless browsers in a single spider - route requests to different sessions by ID.
* 💾 **Pause & Resume**: Checkpoint-based crawl persistence. Press Ctrl+C for a graceful shutdown; restart to resume from where you left off.
* 📡 **Streaming Mode**: Stream scraped items as they arrive via `async for item in spider.stream()` with real-time stats - ideal for UI, pipelines, and long-running crawls.
* 🛡️ **Blocked Request Detection**: Automatic detection and retry of blocked requests with customizable logic.
* 📦 **Built-in Export**: Export results through hooks and your own pipeline or the built-in JSON/JSONL with `result.items.to_json()` / `result.items.to_jsonl()` respectively.

### Advanced Websites Fetching with Session Support[¶](#advanced-websites-fetching-with-session-support "Permanent link")

* **HTTP Requests**: Fast and stealthy HTTP requests with the `Fetcher` class. Can impersonate browsers' TLS fingerprint, headers, and use HTTP/3.
* **Dynamic Loading**: Fetch dynamic websites with full browser automation through the `DynamicFetcher` class supporting Playwright's Chromium and Google's Chrome.
* **Anti-bot Bypass**: Advanced stealth capabilities with `StealthyFetcher` and fingerprint spoofing. Can easily bypass all types of Cloudflare's Turnstile/Interstitial with automation.
* **Session Management**: Persistent session support with `FetcherSession`, `StealthySession`, and `DynamicSession` classes for cookie and state management across requests.
* **Proxy Rotation**: Built-in `ProxyRotator` with cyclic or custom rotation strategies across all session types, plus per-request proxy overrides.
* **Domain Blocking**: Block requests to specific domains (and their subdomains) in browser-based fetchers.
* **Async Support**: Complete async support across all fetchers and dedicated async session classes.

### Adaptive Scraping & AI Integration[¶](#adaptive-scraping-ai-integration "Permanent link")

* 🔄 **Smart Element Tracking**: Relocate elements after website changes using intelligent similarity algorithms.
* 🎯 **Smart Flexible Selection**: CSS selectors, XPath selectors, filter-based search, text search, regex search, and more.
* 🔍 **Find Similar Elements**: Automatically locate elements similar to found elements.
* 🤖 **MCP Server to be used with AI**: Built-in MCP server for AI-assisted Web Scraping and data extraction. The MCP server features powerful, custom capabilities that leverage Scrapling to extract targeted content before passing it to the AI (Claude/Cursor/etc), thereby speeding up operations and reducing costs by minimizing token usage. ([demo video](https://www.youtube.com/watch?v=qyFk3ZNwOxE))

### High-Performance & battle-tested Architecture[¶](#high-performance-battle-tested-architecture "Permanent link")

* 🚀 **Lightning Fast**: Optimized performance outperforming most Python scraping libraries.
* 🔋 **Memory Efficient**: Optimized data structures and lazy loading for a minimal memory footprint.
* ⚡ **Fast JSON Serialization**: 10x faster than the standard library.
* 🏗️ **Battle tested**: Not only does Scrapling have 92% test coverage and full type hints coverage, but it has been used daily by hundreds of Web Scrapers over the past year.

### Developer/Web Scraper Friendly Experience[¶](#developerweb-scraper-friendly-experience "Permanent link")

* 🎯 **Interactive Web Scraping Shell**: Optional built-in IPython shell with Scrapling integration, shortcuts, and new tools to speed up Web Scraping scripts development, like converting curl requests to Scrapling requests and viewing requests results in your browser.
* 🚀 **Use it directly from the Terminal**: Optionally, you can use Scrapling to scrape a URL without writing a single line of code!
* 🛠️ **Rich Navigation API**: Advanced DOM traversal with parent, sibling, and child navigation methods.
* 🧬 **Enhanced Text Processing**: Built-in regex, cleaning methods, and optimized string operations.
* 📝 **Auto Selector Generation**: Generate robust CSS/XPath selectors for any element.
* 🔌 **Familiar API**: Similar to Scrapy/BeautifulSoup with the same pseudo-elements used in Scrapy/Parsel.
* 📘 **Complete Type Coverage**: Full type hints for excellent IDE support and code completion. The entire codebase is automatically scanned with **PyRight** and **MyPy** with each change.
* 🔋 **Ready Docker image**: With each release, a Docker image containing all browsers is automatically built and pushed.

## Star History[¶](#star-history "Permanent link")

Scrapling’s GitHub stars have grown steadily since its release (see chart below).

[![Star History Chart](https://api.star-history.com/svg?repos=D4Vinci/Scrapling&type=Date)](https://github.com/D4Vinci/Scrapling)

## Installation[¶](#installation "Permanent link")

Scrapling requires Python 3.10 or higher:

```
pip install scrapling
```

This installation only includes the parser engine and its dependencies, without any fetchers or commandline dependencies.

### Optional Dependencies[¶](#optional-dependencies "Permanent link")

1. If you are going to use any of the extra features below, the fetchers, or their classes, you will need to install fetchers' dependencies and their browser dependencies as follows:

   ```
   pip install "scrapling[fetchers]"

   scrapling install           # normal install
   scrapling install  --force  # force reinstall
   ```

   This downloads all browsers, along with their system dependencies and fingerprint manipulation dependencies.

   Or you can install them from the code instead of running a command like this:

   ```
   from scrapling.cli import install

   install([], standalone_mode=False)          # normal install
   install(["--force"], standalone_mode=False) # force reinstall
   ```
2. Extra features:

   * Install the MCP server feature:

     ```
     pip install "scrapling[ai]"
     ```
   * Install shell features (Web Scraping shell and the `extract` command):

     ```
     pip install "scrapling[shell]"
     ```
   * Install everything:

     ```
     pip install "scrapling[all]"
     ```

     Don't forget that you need to install the browser dependencies with `scrapling install` after any of these extras (if you didn't already)

### Docker[¶](#docker "Permanent link")

You can also install a Docker image with all extras and browsers with the following command from DockerHub:

```
docker pull pyd4vinci/scrapling
```

Or download it from the GitHub registry:

```
docker pull ghcr.io/d4vinci/scrapling:latest
```

This image is automatically built and pushed using GitHub Actions and the repository's main branch.

## How the documentation is organized[¶](#how-the-documentation-is-organized "Permanent link")

Scrapling has extensive documentation, so we try to follow the [Diátaxis documentation framework](https://diataxis.fr/).

## Support[¶](#support "Permanent link")

If you like Scrapling and want to support its development:

* ⭐ Star the [GitHub repository](https://github.com/D4Vinci/Scrapling)
* 🚀 Follow us on [Twitter](https://x.com/Scrapling_dev) and join the [discord server](https://discord.gg/EMgGbDceNQ)
* 💝 Consider [sponsoring the project or buying me a coffee](donate.html) ![😉](https://cdn.jsdelivr.net/gh/jdecked/twemoji@16.0.1/assets/svg/1f609.svg ":wink:")
* 🐛 Report bugs and suggest features through [GitHub Issues](https://github.com/D4Vinci/Scrapling/issues)

## License[¶](#license "Permanent link")

This project is licensed under the BSD-3 License. See the [LICENSE](https://github.com/D4Vinci/Scrapling/blob/main/LICENSE) file for details.

Was this page helpful?

Thanks for your feedback!

Thanks for your feedback! Help us improve this page by
[opening a documentation issue](https://github.com/D4Vinci/Scrapling/issues/new?template=04-docs_issue.yml).


---
## Source: https://scrapling.readthedocs.io/en/latest/overview.html
---

# Overview

## Pick Your Path[¶](#pick-your-path "Permanent link")

Not sure where to start? Pick the path that matches what you're trying to do:

| I want to... | Start here |
| --- | --- |
| **Parse HTML** I already have | [Querying elements](parsing/selection.html): CSS, XPath, and text-based selection |
| **Quickly scrape a page** and prototype | Pick a [fetcher](fetching/choosing.html) and test right away, or launch the [interactive shell](cli/interactive-shell.html) |
| **Build a crawler** that scales | [Spiders](spiders/getting-started.html): concurrent, multi-session crawls with pause/resume |
| **Scrape without writing code** | [CLI extract commands](cli/extract-commands.html) or hook up the [MCP server](ai/mcp-server.html) to your favourite AI tool |
| **Migrate** from another library | [From BeautifulSoup](tutorials/migrating_from_beautifulsoup.html) or [Scrapy comparison](spiders/architecture.html#comparison-with-scrapy) |

---

We will start by quickly reviewing the parsing capabilities. Then we will fetch websites using custom browsers, make requests, and parse the responses.

Here's an HTML document generated by ChatGPT that we will be using as an example throughout this page:

```
<html>
  <head>
    <title>Complex Web Page</title>
    <style>
      .hidden { display: none; }
    </style>
  </head>
  <body>
    <header>
      <nav>
        <ul>
          <li> <a href="#home">Home</a> </li>
          <li> <a href="#about">About</a> </li>
          <li> <a href="#contact">Contact</a> </li>
        </ul>
      </nav>
    </header>
    <main>
      <section id="products" schema='{"jsonable": "data"}'>
        <h2>Products</h2>
        <div class="product-list">
          <article class="product" data-id="1">
            <h3>Product 1</h3>
            <p class="description">This is product 1</p>
            <span class="price">$10.99</span>
            <div class="hidden stock">In stock: 5</div>
          </article>

          <article class="product" data-id="2">
            <h3>Product 2</h3>
            <p class="description">This is product 2</p>
            <span class="price">$20.99</span>
            <div class="hidden stock">In stock: 3</div>
          </article>

          <article class="product" data-id="3">
            <h3>Product 3</h3>
            <p class="description">This is product 3</p>
            <span class="price">$15.99</span>
            <div class="hidden stock">Out of stock</div>
          </article>
        </div>
      </section>

      <section id="reviews">
        <h2>Customer Reviews</h2>
        <div class="review-list">
          <div class="review" data-rating="5">
            <p class="review-text">Great product!</p>
            <span class="reviewer">John Doe</span>
          </div>
          <div class="review" data-rating="4">
            <p class="review-text">Good value for money.</p>
            <span class="reviewer">Jane Smith</span>
          </div>
        </div>
      </section>
    </main>
    <script id="page-data" type="application/json">
      {
        "lastUpdated": "2024-09-22T10:30:00Z",
        "totalProducts": 3
      }
    </script>
  </body>
</html>
```

Starting with loading raw HTML above like this

```
from scrapling.parser import Selector
page = Selector(html_doc)
page  # <data='<html><head><title>Complex Web Page</tit...'>
```

Get all text content on the page recursively

```
page.get_all_text(ignore_tags=('script', 'style'))
# 'Complex Web Page\nHome\nAbout\nContact\nProducts\nProduct 1\nThis is product 1\n$10.99\nIn stock: 5\nProduct 2\nThis is product 2\n$20.99\nIn stock: 3\nProduct 3\nThis is product 3\n$15.99\nOut of stock\nCustomer Reviews\nGreat product!\nJohn Doe\nGood value for money.\nJane Smith'
```

## Finding elements[¶](#finding-elements "Permanent link")

If there's an element you want to find on the page, you will find it! Your creativity level is the only limitation!

Finding the first HTML `section` element

```
section_element = page.find('section')
# <data='<section id="products" schema='{"jsonabl...' parent='<main><section id="products" schema='{"j...'>
```

Find all `section` elements

```
section_elements = page.find_all('section')
# [<data='<section id="products" schema='{"jsonabl...' parent='<main><section id="products" schema='{"j...'>, <data='<section id="reviews"><h2>Customer Revie...' parent='<main><section id="products" schema='{"j...'>]
```

Find all `section` elements whose `id` attribute value is `products`.

```
section_elements = page.find_all('section', {'id':"products"})
# Same as
section_elements = page.find_all('section', id="products")
# [<data='<section id="products" schema='{"jsonabl...' parent='<main><section id="products" schema='{"j...'>]
```

Find all `section` elements whose `id` attribute value contains `product`.

```
section_elements = page.find_all('section', {'id*':"product"})
```

Find all `h3` elements whose text content matches this regex `Product \d`

```
page.find_all('h3', re.compile(r'Product \d'))
# [<data='<h3>Product 1</h3>' parent='<article class="product" data-id="1"><h3...'>, <data='<h3>Product 2</h3>' parent='<article class="product" data-id="2"><h3...'>, <data='<h3>Product 3</h3>' parent='<article class="product" data-id="3"><h3...'>]
```

Find all `h3` and `h2` elements whose text content matches the regex `Product` only

```
page.find_all(['h3', 'h2'], re.compile(r'Product'))
# [<data='<h3>Product 1</h3>' parent='<article class="product" data-id="1"><h3...'>, <data='<h3>Product 2</h3>' parent='<article class="product" data-id="2"><h3...'>, <data='<h3>Product 3</h3>' parent='<article class="product" data-id="3"><h3...'>, <data='<h2>Products</h2>' parent='<section id="products" schema='{"jsonabl...'>]
```

Find all elements whose text content matches exactly `Products` (Whitespaces are not taken into consideration)

```
page.find_by_text('Products', first_match=False)
# [<data='<h2>Products</h2>' parent='<section id="products" schema='{"jsonabl...'>]
```

Or find all elements whose text content matches regex `Product \d`

```
page.find_by_regex(r'Product \d', first_match=False)
# [<data='<h3>Product 1</h3>' parent='<article class="product" data-id="1"><h3...'>, <data='<h3>Product 2</h3>' parent='<article class="product" data-id="2"><h3...'>, <data='<h3>Product 3</h3>' parent='<article class="product" data-id="3"><h3...'>]
```

Find all elements that are similar to the element you want

```
target_element = page.find_by_regex(r'Product \d', first_match=True)
# <data='<h3>Product 1</h3>' parent='<article class="product" data-id="1"><h3...'>
target_element.find_similar()
# [<data='<h3>Product 2</h3>' parent='<article class="product" data-id="2"><h3...'>, <data='<h3>Product 3</h3>' parent='<article class="product" data-id="3"><h3...'>]
```

Find the first element that matches a CSS selector

```
page.css('.product-list [data-id="1"]')[0]
# <data='<article class="product" data-id="1"><h3...' parent='<div class="product-list"> <article clas...'>
```

Find all elements that match a CSS selector

```
page.css('.product-list article')
# [<data='<article class="product" data-id="1"><h3...' parent='<div class="product-list"> <article clas...'>, <data='<article class="product" data-id="2"><h3...' parent='<div class="product-list"> <article clas...'>, <data='<article class="product" data-id="3"><h3...' parent='<div class="product-list"> <article clas...'>]
```

Find the first element that matches an XPath selector

```
page.xpath("//*[@id='products']/div/article")[0]
# <data='<article class="product" data-id="1"><h3...' parent='<div class="product-list"> <article clas...'>
```

Find all elements that match an XPath selector

```
page.xpath("//*[@id='products']/div/article")
# [<data='<article class="product" data-id="1"><h3...' parent='<div class="product-list"> <article clas...'>, <data='<article class="product" data-id="2"><h3...' parent='<div class="product-list"> <article clas...'>, <data='<article class="product" data-id="3"><h3...' parent='<div class="product-list"> <article clas...'>]
```

With this, we just scratched the surface of these functions; more advanced options with these selection methods are shown later.

## Accessing elements' data[¶](#accessing-elements-data "Permanent link")

It's as simple as

```
>>> section_element.tag
'section'
>>> print(section_element.attrib)
{'id': 'products', 'schema': '{"jsonable": "data"}'}
>>> section_element.attrib['schema'].json()  # If an attribute value can be converted to json, then use `.json()` to convert it
{'jsonable': 'data'}
>>> section_element.text  # Direct text content
''
>>> section_element.get_all_text()  # All text content recursively
'Products\nProduct 1\nThis is product 1\n$10.99\nIn stock: 5\nProduct 2\nThis is product 2\n$20.99\nIn stock: 3\nProduct 3\nThis is product 3\n$15.99\nOut of stock'
>>> section_element.html_content  # The HTML content of the element
'<section id="products" schema=\'{"jsonable": "data"}\'><h2>Products</h2>\n        <div class="product-list">\n          <article class="product" data-id="1"><h3>Product 1</h3>\n            <p class="description">This is product 1</p>\n            <span class="price">$10.99</span>\n            <div class="hidden stock">In stock: 5</div>\n          </article><article class="product" data-id="2"><h3>Product 2</h3>\n            <p class="description">This is product 2</p>\n            <span class="price">$20.99</span>\n            <div class="hidden stock">In stock: 3</div>\n          </article><article class="product" data-id="3"><h3>Product 3</h3>\n            <p class="description">This is product 3</p>\n            <span class="price">$15.99</span>\n            <div class="hidden stock">Out of stock</div>\n          </article></div>\n      </section>'
>>> print(section_element.prettify())  # The prettified version
'''
<section id="products" schema='{"jsonable": "data"}'><h2>Products</h2>
    <div class="product-list">
      <article class="product" data-id="1"><h3>Product 1</h3>
        <p class="description">This is product 1</p>
        <span class="price">$10.99</span>
        <div class="hidden stock">In stock: 5</div>
      </article><article class="product" data-id="2"><h3>Product 2</h3>
        <p class="description">This is product 2</p>
        <span class="price">$20.99</span>
        <div class="hidden stock">In stock: 3</div>
      </article><article class="product" data-id="3"><h3>Product 3</h3>
        <p class="description">This is product 3</p>
        <span class="price">$15.99</span>
        <div class="hidden stock">Out of stock</div>
      </article>
    </div>
</section>
'''
>>> section_element.path  # All the ancestors in the DOM tree of this element
[<data='<main><section id="products" schema='{"j...' parent='<body> <header><nav><ul><li> <a href="#h...'>,
 <data='<body> <header><nav><ul><li> <a href="#h...' parent='<html><head><title>Complex Web Page</tit...'>,
 <data='<html><head><title>Complex Web Page</tit...'>]
>>> section_element.generate_css_selector
'#products'
>>> section_element.generate_full_css_selector
'body > main > #products > #products'
>>> section_element.generate_xpath_selector
"//*[@id='products']"
>>> section_element.generate_full_xpath_selector
"//body/main/*[@id='products']"
```

## Navigation[¶](#navigation "Permanent link")

Using the elements we found above

```
>>> section_element.parent
<data='<main><section id="products" schema='{"j...' parent='<body> <header><nav><ul><li> <a href="#h...'>
>>> section_element.parent.tag
'main'
>>> section_element.parent.parent.tag
'body'
>>> section_element.children
[<data='<h2>Products</h2>' parent='<section id="products" schema='{"jsonabl...'>,
 <data='<div class="product-list"> <article clas...' parent='<section id="products" schema='{"jsonabl...'>]
>>> section_element.siblings
[<data='<section id="reviews"><h2>Customer Revie...' parent='<main><section id="products" schema='{"j...'>]
>>> section_element.next  # gets the next element, the same logic applies to `quote.previous`.
<data='<section id="reviews"><h2>Customer Revie...' parent='<main><section id="products" schema='{"j...'>
>>> section_element.children.css('h2::text').getall()
['Products']
>>> page.css('[data-id="1"]')[0].has_class('product')
True
```

If your case needs more than the element's parent, you can iterate over the whole ancestors' tree of any element, like the one below

```
for ancestor in section_element.iterancestors():
    # do something with it...
```

You can search for a specific ancestor of an element that satisfies a function; all you need to do is pass a function that takes a `Selector` object as an argument and returns `True` if the condition is satisfied or `False` otherwise, like below:

```
>>> section_element.find_ancestor(lambda ancestor: ancestor.css('nav'))
<data='<body> <header><nav><ul><li> <a href="#h...' parent='<html><head><title>Complex Web Page</tit...'>
```

## Fetching websites[¶](#fetching-websites "Permanent link")

Instead of passing the raw HTML to Scrapling, you can retrieve a website's response directly via HTTP requests or by fetching it in a browser.

A fetcher is made for every use case.

### HTTP Requests[¶](#http-requests "Permanent link")

For simple HTTP requests, there's a `Fetcher` class that can be imported and used as below:

```
from scrapling.fetchers import Fetcher
page = Fetcher.get('https://scrapling.requestcatcher.com/get', impersonate="chrome")
```

With that out of the way, here's how to do all HTTP methods:

```
>>> from scrapling.fetchers import Fetcher
>>> page = Fetcher.get('https://scrapling.requestcatcher.com/get', stealthy_headers=True, follow_redirects=True)
>>> page = Fetcher.post('https://scrapling.requestcatcher.com/post', data={'key': 'value'}, proxy='http://username:password@localhost:8030')
>>> page = Fetcher.put('https://scrapling.requestcatcher.com/put', data={'key': 'value'})
>>> page = Fetcher.delete('https://scrapling.requestcatcher.com/delete')
```

For Async requests, you will replace the import like below:

```
>>> from scrapling.fetchers import AsyncFetcher
>>> page = await AsyncFetcher.get('https://scrapling.requestcatcher.com/get', stealthy_headers=True, follow_redirects=True)
>>> page = await AsyncFetcher.post('https://scrapling.requestcatcher.com/post', data={'key': 'value'}, proxy='http://username:password@localhost:8030')
>>> page = await AsyncFetcher.put('https://scrapling.requestcatcher.com/put', data={'key': 'value'})
>>> page = await AsyncFetcher.delete('https://scrapling.requestcatcher.com/delete')
```

Notes:

1. You have the `stealthy_headers` argument, which, when enabled, makes requests to generate real browser headers and use them, including a Google referer header. It's enabled by default.
2. The `impersonate` argument lets you fake the TLS fingerprint for a specific browser version.
3. There's also the `http3` argument, which, when enabled, makes the fetcher use HTTP/3 for requests, which makes your requests more authentic

This is just the tip of the iceberg with this fetcher; check out the rest from [here](fetching/static.html)

### Dynamic loading[¶](#dynamic-loading "Permanent link")

We have you covered if you deal with dynamic websites like most today!

The `DynamicFetcher` class (formerly `PlayWrightFetcher`) offers many options for fetching and loading web pages using Chromium-based browsers.

```
>>> from scrapling.fetchers import DynamicFetcher
>>> page = DynamicFetcher.fetch('https://www.google.com/search?q=%22Scrapling%22', disable_resources=True)  # Vanilla Playwright option
>>> page.css("#search a::attr(href)").get()
'https://github.com/D4Vinci/Scrapling'
>>> # The async version of fetch
>>> page = await DynamicFetcher.async_fetch('https://www.google.com/search?q=%22Scrapling%22', disable_resources=True)
>>> page.css("#search a::attr(href)").get()
'https://github.com/D4Vinci/Scrapling'
```

It's built on top of [Playwright](https://playwright.dev/python/), and it's currently providing two main run options that can be mixed as you want:

* Vanilla Playwright without any modifications other than the ones you chose. It uses the Chromium browser.
* Real browsers like your Chrome browser by passing the `real_chrome` argument or the CDP URL of your browser to be controlled by the Fetcher, and most of the options can be enabled on it.

Again, this is just the tip of the iceberg with this fetcher. Check out the rest from [here](fetching/dynamic.html) for all details and the complete list of arguments.

### Dynamic anti-protection loading[¶](#dynamic-anti-protection-loading "Permanent link")

We also have you covered if you deal with dynamic websites with annoying anti-protections!

The `StealthyFetcher` class uses a stealthy version of the `DynamicFetcher` explained above.

Some of the things it does:

1. It easily bypasses all types of Cloudflare's Turnstile/Interstitial automatically.
2. It bypasses CDP runtime leaks and WebRTC leaks.
3. It isolates JS execution, removes many Playwright fingerprints, and stops detection through some of the known behaviors that bots do.
4. It generates canvas noise to prevent fingerprinting through canvas.
5. It automatically patches known methods to detect running in headless mode and provides an option to defeat timezone mismatch attacks.
6. and other anti-protection options...

```
>>> from scrapling.fetchers import StealthyFetcher
>>> page = StealthyFetcher.fetch('https://www.browserscan.net/bot-detection')  # Running headless by default
>>> page.status == 200
True
>>> page = StealthyFetcher.fetch('https://nopecha.com/demo/cloudflare', solve_cloudflare=True)  # Solve Cloudflare captcha automatically if presented
>>> page.status == 200
True
>>> page = StealthyFetcher.fetch('https://www.browserscan.net/bot-detection', humanize=True, os_randomize=True) # and the rest of arguments...
>>> # The async version of fetch
>>> page = await StealthyFetcher.async_fetch('https://www.browserscan.net/bot-detection')
>>> page.status == 200
True
```

Again, this is just the tip of the iceberg with this fetcher. Check out the rest from [here](fetching/stealthy.html) for all details and the complete list of arguments.

---

That's Scrapling at a glance. If you want to learn more, continue to the next section.

Was this page helpful?

Thanks for your feedback!

Thanks for your feedback! Help us improve this page by
[opening a documentation issue](https://github.com/D4Vinci/Scrapling/issues/new?template=04-docs_issue.yml).


---
## Source: https://scrapling.readthedocs.io/en/latest/benchmarks.html
---

# Performance Benchmarks[¶](#performance-benchmarks "Permanent link")

Scrapling isn't just powerful - it's also blazing fast. The following benchmarks compare Scrapling's parser with the latest versions of other popular libraries.

### Text Extraction Speed Test (5000 nested elements)[¶](#text-extraction-speed-test-5000-nested-elements "Permanent link")

| # | Library | Time (ms) | vs Scrapling |
| --- | --- | --- | --- |
| 1 | Scrapling | 2.02 | 1.0x |
| 2 | Parsel/Scrapy | 2.04 | 1.01 |
| 3 | Raw Lxml | 2.54 | 1.257 |
| 4 | PyQuery | 24.17 | ~12x |
| 5 | Selectolax | 82.63 | ~41x |
| 6 | MechanicalSoup | 1549.71 | ~767.1x |
| 7 | BS4 with Lxml | 1584.31 | ~784.3x |
| 8 | BS4 with html5lib | 3391.91 | ~1679.1x |

### Element Similarity & Text Search Performance[¶](#element-similarity-text-search-performance "Permanent link")

Scrapling's adaptive element finding capabilities significantly outperform alternatives:

| Library | Time (ms) | vs Scrapling |
| --- | --- | --- |
| Scrapling | 2.39 | 1.0x |
| AutoScraper | 12.45 | 5.209x |

> All benchmarks represent averages of 100+ runs. See [benchmarks.py](https://github.com/D4Vinci/Scrapling/blob/main/benchmarks.py) for methodology.

Was this page helpful?

Thanks for your feedback!

Thanks for your feedback! Help us improve this page by
[opening a documentation issue](https://github.com/D4Vinci/Scrapling/issues/new?template=04-docs_issue.yml).


---
## Source: https://scrapling.readthedocs.io/en/latest/parsing/selection.html
---

# Querying elements[¶](#querying-elements "Permanent link")

Scrapling currently supports parsing HTML pages exclusively, so it doesn't support XML feeds. This decision was made because the adaptive feature won't work with XML, but that might change soon, so stay tuned :)

In Scrapling, there are five main ways to find elements:

1. CSS3 Selectors
2. XPath Selectors
3. Finding elements based on filters/conditions.
4. Finding elements whose content contains a specific text
5. Finding elements whose content matches a specific regex

Of course, there are other indirect ways to find elements with Scrapling, but here we will discuss the main ways in detail. We will also bring up one of the most remarkable features of Scrapling: the ability to find elements that are similar to the element you have; you can jump to that section directly from [here](#finding-similar-elements).

If you are new to Web Scraping, have little to no experience writing selectors, and want to start quickly, I recommend you jump directly to learning the `find`/`find_all` methods from [here](#filters-based-searching).

## CSS/XPath selectors[¶](#cssxpath-selectors "Permanent link")

### What are CSS selectors?[¶](#what-are-css-selectors "Permanent link")

[CSS](https://en.wikipedia.org/wiki/CSS) is a language for applying styles to HTML documents. It defines selectors to associate those styles with specific HTML elements.

Scrapling implements CSS3 selectors as described in the [W3C specification](http://www.w3.org/TR/2011/REC-css3-selectors-20110929/). CSS selectors support comes from `cssselect`, so it's better to read about which [selectors are supported from cssselect](https://cssselect.readthedocs.io/en/latest/#supported-selectors) and pseudo-functions/elements.

Also, Scrapling implements some non-standard pseudo-elements like:

* To select text nodes, use `::text`.
* To select attribute values, use `::attr(name)` where name is the name of the attribute that you want the value of

In short, if you come from Scrapy/Parsel, you will find the same logic for selectors here to make it easier. No need to implement a stranger logic to the one that most of us are used to :)

To select elements with CSS selectors, use the `css` method, which returns `Selectors`. Use `[0]` to get the first element, or `.get()` / `.getall()` to extract text values from text/attribute pseudo-selectors.

### What are XPath selectors?[¶](#what-are-xpath-selectors "Permanent link")

[XPath](https://en.wikipedia.org/wiki/XPath) is a language for selecting nodes in XML documents, which can also be used with HTML. This [cheatsheet](https://devhints.io/xpath) is a good resource for learning about [XPath](https://en.wikipedia.org/wiki/XPath). Scrapling adds XPath selectors directly through [lxml](https://lxml.de/).

In short, it is the same situation as CSS Selectors; if you come from Scrapy/Parsel, you will find the same logic for selectors here. However, Scrapling doesn't implement the XPath extension function `has-class` as Scrapy/Parsel does. Instead, it provides the `has_class` method, which can be used on elements returned for the same purpose.

To select elements with XPath selectors, you have the `xpath` method. Again, this method follows the same logic as the CSS selectors method above.

> Note that each method of `css` and `xpath` has additional arguments, but we didn't explain them here, as they are all about the adaptive feature. The adaptive feature will have its own page later to be described in detail.

### Selectors examples[¶](#selectors-examples "Permanent link")

Let's see some shared examples of using CSS and XPath Selectors.

Select all elements with the class `product`.

```
products = page.css('.product')
products = page.xpath('//*[@class="product"]')
```

Note:

The XPath one won't be accurate if there's another class; **it's always better to rely on CSS for selecting by class**

Select the first element with the class `product`.

```
product = page.css('.product')[0]
product = page.xpath('//*[@class="product"]')[0]
```

Get the text of the first element with the `h1` tag name

```
title = page.css('h1::text').get()
title = page.xpath('//h1//text()').get()
```

Which is the same as doing

```
title = page.css('h1')[0].text
title = page.xpath('//h1')[0].text
```

Get the `href` attribute of the first element with the `a` tag name

```
link = page.css('a::attr(href)').get()
link = page.xpath('//a/@href').get()
```

Select the text of the first element with the `h1` tag name, which contains `Phone`, and under an element with class `product`.

```
title = page.css('.product h1:contains("Phone")::text').get()
title = page.xpath('//*[@class="product"]//h1[contains(text(),"Phone")]/text()').get()
```

You can nest and chain selectors as you want, given that they return results

```
page.css('.product')[0].css('h1:contains("Phone")::text').get()
page.xpath('//*[@class="product"]')[0].xpath('//h1[contains(text(),"Phone")]/text()').get()
page.xpath('//*[@class="product"]')[0].css('h1:contains("Phone")::text').get()
```

Another example

All links that have 'image' in their 'href' attribute

```
links = page.css('a[href*="image"]')
links = page.xpath('//a[contains(@href, "image")]')
for index, link in enumerate(links):
    link_value = link.attrib['href']  # Cleaner than link.css('::attr(href)').get()
    link_text = link.text
    print(f'Link number {index} points to this url {link_value} with text content as "{link_text}"')
```

## Text-content selection[¶](#text-content-selection "Permanent link")

Scrapling provides the ability to select elements based on their direct text content, and you have two ways to do this:

1. Elements whose direct text content contains the given text with many options through the `find_by_text` method.
2. Elements whose direct text content matches the given regex pattern with many options through the `find_by_regex` method.

What you can do with `find_by_text` can be done with `find_by_regex` if you are good enough with regular expressions (regex), but we are providing more options to make them easier for all users to access.

With `find_by_text`, you pass the text as the first argument; with `find_by_regex`, the regex pattern is the first argument. Both methods share the following arguments:

* **first_match**: If `True` (the default), the method used will return the first result it finds.
* **case_sensitive**: If `True`, the case of the letters will be considered.
* **clean_match**: If `True`, all whitespaces and consecutive spaces will be replaced with a single space before matching.

By default, Scrapling searches for the exact matching of the text/pattern you pass to `find_by_text`, so the text content of the wanted element has to be ONLY the text you input, but that's why it also has one extra argument, which is:

* **partial**: If enabled, `find_by_text` will return elements that contain the input text. So it's not an exact match anymore

Note:

The method `find_by_regex` can accept both regular strings and a compiled regex pattern as its first argument, as you will see in the upcoming examples.

### Finding Similar Elements[¶](#finding-similar-elements "Permanent link")

One of the most remarkable new features Scrapling puts on the table is the ability to tell Scrapling to find elements similar to the element at hand. This feature's inspiration came from the AutoScraper library, but in Scrapling, it can be used on elements found by any method. Most of its usage would likely occur after finding elements through text content, similar to how AutoScraper works, making it convenient to explain here.

So, how does it work?

Imagine a scenario where you found a product by its title, for example, and you want to extract other products listed in the same table/container. With the element you have, you can call the method `.find_similar()` on it, and Scrapling will:

1. Find all page elements with the same DOM tree depth as this element.
2. All found elements will be checked, and those without the same tag name, parent tag name, and grandparent tag name will be dropped.
3. Now we are sure (like 99% sure) that these elements are the ones we want, but as a last check, Scrapling will use fuzzy matching to drop the elements whose attributes don't look like the attributes of our element. There's a percentage to control this step, and I recommend you not play with it unless the default settings don't get the elements you want.

That's a lot of talking, I know, but I had to go deep. I will give examples of using this method in the next section, but first, these are the arguments that can be passed to this method:

* **similarity_threshold**: This is the percentage we discussed in step 3 for comparing elements' attributes. The default value is 0.2. In Simpler words, the tag attributes of both elements should be at least 20% similar. If you want to turn off this check (basically Step 3), you can set this attribute to 0, but I recommend you read what the other arguments do first.
* **ignore_attributes**: The attribute names passed will be ignored while matching the attributes in the last step. The default value is `('href', 'src',)` because URLs can change significantly across elements, making them unreliable.
* **match_text**: If `True`, the element's text content will be considered when matching (Step 3). Using this argument in typical cases is not recommended, but it depends.

Now, let's check out the examples below.

### Examples[¶](#examples "Permanent link")

Let's see some shared examples of finding elements with raw text and regex.

I will use the `Fetcher` class with these examples, but it will be explained in detail later.

```
from scrapling.fetchers import Fetcher
page = Fetcher.get('https://books.toscrape.com/index.html')
```

Find the first element whose text fully matches this text

```
>>> page.find_by_text('Tipping the Velvet')
<data='<a href="catalogue/tipping-the-velvet_99...' parent='<h3><a href="catalogue/tipping-the-velve...'>
```

Combining it with `page.urljoin` to return the full URL from the relative `href`.

```
>>> page.find_by_text('Tipping the Velvet').attrib['href']
'catalogue/tipping-the-velvet_999/index.html'
>>> page.urljoin(page.find_by_text('Tipping the Velvet').attrib['href'])
'https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html'
```

Get all matches if there are more (notice it returns a list)

```
>>> page.find_by_text('Tipping the Velvet', first_match=False)
[<data='<a href="catalogue/tipping-the-velvet_99...' parent='<h3><a href="catalogue/tipping-the-velve...'>]
```

Get all elements that contain the word `the` (Partial matching)

```
>>> results = page.find_by_text('the', partial=True, first_match=False)
>>> [i.text for i in results]
['A Light in the ...',
 'Tipping the Velvet',
 'The Requiem Red',
 'The Dirty Little Secrets ...',
 'The Coming Woman: A ...',
 'The Boys in the ...',
 'The Black Maria',
 'Mesaerion: The Best Science ...',
 "It's Only the Himalayas"]
```

The search is case-insensitive, so those results include `The`, not just the lowercase `the`; let's limit the search to elements with `the` only.

```
>>> results = page.find_by_text('the', partial=True, first_match=False, case_sensitive=True)
>>> [i.text for i in results]
['A Light in the ...',
 'Tipping the Velvet',
 'The Boys in the ...',
 "It's Only the Himalayas"]
```

Get the first element whose text content matches my price regex

```
>>> page.find_by_regex(r'£[\d\.]+')
<data='<p class="price_color">£51.77</p>' parent='<div class="product_price"> <p class="pr...'>
>>> page.find_by_regex(r'£[\d\.]+').text
'£51.77'
```

It's the same if you pass the compiled regex as well; Scrapling will detect the input type and act upon that:

```
>>> import re
>>> regex = re.compile(r'£[\d\.]+')
>>> page.find_by_regex(regex)
<data='<p class="price_color">£51.77</p>' parent='<div class="product_price"> <p class="pr...'>
>>> page.find_by_regex(regex).text
'£51.77'
```

Get all elements that match the regex

```
>>> page.find_by_regex(r'£[\d\.]+', first_match=False)
[<data='<p class="price_color">£51.77</p>' parent='<div class="product_price"> <p class="pr...'>,
 <data='<p class="price_color">£53.74</p>' parent='<div class="product_price"> <p class="pr...'>,
 <data='<p class="price_color">£50.10</p>' parent='<div class="product_price"> <p class="pr...'>,
 <data='<p class="price_color">£47.82</p>' parent='<div class="product_price"> <p class="pr...'>,
 ...]
```

And so on...

Find all elements similar to the current element in location and attributes. For our case, ignore the 'title' attribute while matching

```
>>> element = page.find_by_text('Tipping the Velvet')
>>> element.find_similar(ignore_attributes=['title'])
[<data='<a href="catalogue/a-light-in-the-attic_...' parent='<h3><a href="catalogue/a-light-in-the-at...'>,
 <data='<a href="catalogue/soumission_998/index....' parent='<h3><a href="catalogue/soumission_998/in...'>,
 <data='<a href="catalogue/sharp-objects_997/ind...' parent='<h3><a href="catalogue/sharp-objects_997...'>,
...]
```

Notice that the number of elements is 19, not 20, because the current element is not included in the results.

```
>>> len(element.find_similar(ignore_attributes=['title']))
19
```

Get the `href` attribute from all similar elements

```
>>> [
    element.attrib['href']
    for element in element.find_similar(ignore_attributes=['title'])
]
['catalogue/a-light-in-the-attic_1000/index.html',
 'catalogue/soumission_998/index.html',
 'catalogue/sharp-objects_997/index.html',
 ...]
```

To increase the complexity a little bit, let's say we want to get all the books' data using that element as a starting point for some reason

```
>>> for product in element.parent.parent.find_similar():
        print({
            "name": product.css('h3 a::text').get(),
            "price": product.css('.price_color')[0].re_first(r'[\d\.]+'),
            "stock": product.css('.availability::text').getall()[-1].clean()
        })
{'name': 'A Light in the ...', 'price': '51.77', 'stock': 'In stock'}
{'name': 'Soumission', 'price': '50.10', 'stock': 'In stock'}
{'name': 'Sharp Objects', 'price': '47.82', 'stock': 'In stock'}
...
```

### Advanced examples[¶](#advanced-examples "Permanent link")

See more advanced or real-world examples using the `find_similar` method.

E-commerce Product Extraction

```
def extract_product_grid(page):
    # Find the first product card
    first_product = page.find_by_text('Add to Cart').find_ancestor(
        lambda e: e.has_class('product-card')
    )

    # Find similar product cards
    products = first_product.find_similar()

    return [
        {
            'name': p.css('h3::text').get(),
            'price': p.css('.price::text').re_first(r'\d+\.\d{2}'),
            'stock': 'In stock' in p.text,
            'rating': p.css('.rating')[0].attrib.get('data-rating')
        }
        for p in products
    ]
```

Table Row Extraction

```
def extract_table_data(page):
    # Find the first data row
    first_row = page.css('table tbody tr')[0]

    # Find similar rows
    rows = first_row.find_similar()

    return [
        {
            'column1': row.css('td:nth-child(1)::text').get(),
            'column2': row.css('td:nth-child(2)::text').get(),
            'column3': row.css('td:nth-child(3)::text').get()
        }
        for row in rows
    ]
```

Form Field Extraction

```
def extract_form_fields(page):
    # Find first form field container
    first_field = page.css('input')[0].find_ancestor(
        lambda e: e.has_class('form-field')
    )

    # Find similar field containers
    fields = first_field.find_similar()

    return [
        {
            'label': f.css('label::text').get(),
            'type': f.css('input')[0].attrib.get('type'),
            'required': 'required' in f.css('input')[0].attrib
        }
        for f in fields
    ]
```

Extracting reviews from a website

```
def extract_reviews(page):
    # Find first review
    first_review = page.find_by_text('Great product!')
    review_container = first_review.find_ancestor(
        lambda e: e.has_class('review')
    )

    # Find similar reviews
    all_reviews = review_container.find_similar()

    return [
        {
            'text': r.css('.review-text::text').get(),
            'rating': r.attrib.get('data-rating'),
            'author': r.css('.reviewer::text').get()
        }
        for r in all_reviews
    ]
```

## Filters-based searching[¶](#filters-based-searching "Permanent link")

This search method is arguably the best way to find elements in Scrapling, as it is powerful and easier for newcomers to Web Scraping to learn than writing selectors.

Inspired by BeautifulSoup's `find_all` function, you can find elements using the `find_all` and `find` methods. Both methods can accept multiple filters and return all elements on the pages where all these filters apply.

To be more specific:

* Any string passed is considered a tag name.
* Any iterable passed, like List/Tuple/Set, will be considered as an iterable of tag names.
* Any dictionary is considered a mapping of HTML element(s), attribute names, and attribute values.
* Any regex patterns passed are used to filter elements by content, like the `find_by_regex` method
* Any functions passed are used to filter elements
* Any keyword argument passed is considered as an HTML element attribute with its value.

It collects all passed arguments and keywords, and each filter passes its results to the following filter in a waterfall-like filtering system.

It filters all elements in the current page/element in the following order:

1. All elements with the passed tag name(s) get collected.
2. All elements that match all passed attribute(s) are collected; if a previous filter is used, then previously collected elements are filtered.
3. All elements that match all passed regex patterns are collected, or if previous filter(s) are used, then previously collected elements are filtered.
4. All elements that fulfill all passed function(s) are collected; if a previous filter(s) is used, then previously collected elements are filtered.

Notes:

1. As you probably understood, the filtering process always starts from the first filter it finds in the filtering order above. So, if no tag name(s) are passed but attributes are passed, the process starts from that step (number 2), and so on.
2. The order in which you pass the arguments doesn't matter. The only order considered is the one explained above.

Check examples to clear any confusion :)

### Examples[¶](#examples_1 "Permanent link")

```
>>> from scrapling.fetchers import Fetcher
>>> page = Fetcher.get('https://quotes.toscrape.com/')
```

Find all elements with the tag name `div`.

```
>>> page.find_all('div')
[<data='<div class="container"> <div class="row...' parent='<body> <div class="container"> <div clas...'>,
 <data='<div class="row header-box"> <div class=...' parent='<div class="container"> <div class="row...'>,
...]
```

Find all div elements with a class that equals `quote`.

```
>>> page.find_all('div', class_='quote')
[<data='<div class="quote" itemscope itemtype="h...' parent='<div class="col-md-8"> <div class="quote...'>,
 <data='<div class="quote" itemscope itemtype="h...' parent='<div class="col-md-8"> <div class="quote...'>,
...]
```

Same as above.

```
>>> page.find_all('div', {'class': 'quote'})
[<data='<div class="quote" itemscope itemtype="h...' parent='<div class="col-md-8"> <div class="quote...'>,
 <data='<div class="quote" itemscope itemtype="h...' parent='<div class="col-md-8"> <div class="quote...'>,
...]
```

Find all elements with a class that equals `quote`.

```
>>> page.find_all({'class': 'quote'})
[<data='<div class="quote" itemscope itemtype="h...' parent='<div class="col-md-8"> <div class="quote...'>,
 <data='<div class="quote" itemscope itemtype="h...' parent='<div class="col-md-8"> <div class="quote...'>,
...]
```

Find all div elements with a class that equals `quote` and contains the element `.text`, which contains the word 'world' in its content.

```
>>> page.find_all('div', {'class': 'quote'}, lambda e: "world" in e.css('.text::text').get())
[<data='<div class="quote" itemscope itemtype="h...' parent='<div class="col-md-8"> <div class="quote...'>]
```

Find all elements that have children.

```
>>> page.find_all(lambda element: len(element.children) > 0)
[<data='<html lang="en"><head><meta charset="UTF...'>,
 <data='<head><meta charset="UTF-8"><title>Quote...' parent='<html lang="en"><head><meta charset="UTF...'>,
 <data='<body> <div class="container"> <div clas...' parent='<html lang="en"><head><meta charset="UTF...'>,
...]
```

Find all elements that contain the word 'world' in their content.

```
>>> page.find_all(lambda element: "world" in element.text)
[<data='<span class="text" itemprop="text">“The...' parent='<div class="quote" itemscope itemtype="h...'>,
 <data='<a class="tag" href="/tag/world/page/1/"...' parent='<div class="tags"> Tags: <meta class="ke...'>]
```

Find all span elements that match the given regex

```
>>> page.find_all('span', re.compile(r'world'))
[<data='<span class="text" itemprop="text">“The...' parent='<div class="quote" itemscope itemtype="h...'>]
```

Find all div and span elements with class 'quote' (No span elements like that, so only div returned)

```
>>> page.find_all(['div', 'span'], {'class': 'quote'})
[<data='<div class="quote" itemscope itemtype="h...' parent='<div class="col-md-8"> <div class="quote...'>,
 <data='<div class="quote" itemscope itemtype="h...' parent='<div class="col-md-8"> <div class="quote...'>,
...]
```

Mix things up

```
>>> page.find_all({'itemtype':"http://schema.org/CreativeWork"}, 'div').css('.author::text').getall()
['Albert Einstein',
 'J.K. Rowling',
...]
```

A bonus pro tip: Find all elements whose `href` attribute's value ends with the word 'Einstein'.

```
>>> page.find_all({'href$': 'Einstein'})
[<data='<a href="/author/Albert-Einstein">(about...' parent='<span>by <small class="author" itemprop=...'>,
 <data='<a href="/author/Albert-Einstein">(about...' parent='<span>by <small class="author" itemprop=...'>,
 <data='<a href="/author/Albert-Einstein">(about...' parent='<span>by <small class="author" itemprop=...'>]
```

Another pro tip: Find all elements whose `href` attribute's value has '/author/' in it

```
>>> page.find_all({'href*': '/author/'})
[<data='<a href="/author/Albert-Einstein">(about...' parent='<span>by <small class="author" itemprop=...'>,
 <data='<a href="/author/J-K-Rowling">(about)</a...' parent='<span>by <small class="author" itemprop=...'>,
 <data='<a href="/author/Albert-Einstein">(about...' parent='<span>by <small class="author" itemprop=...'>,
...]
```

And so on...

## Generating selectors[¶](#generating-selectors "Permanent link")

You can always generate CSS/XPath selectors for any element that can be reused here or anywhere else, and the most remarkable thing is that it doesn't matter what method you used to find that element!

Generate a short CSS selector for the `url_element` element (if possible, create a short one; otherwise, it's a full selector)

```
>>> url_element = page.find({'href*': '/author/'})
>>> url_element.generate_css_selector
'body > div > div:nth-of-type(2) > div > div > span:nth-of-type(2) > a'
```

Generate a full CSS selector for the `url_element` element from the start of the page

```
>>> url_element.generate_full_css_selector
'body > div > div:nth-of-type(2) > div > div > span:nth-of-type(2) > a'
```

Generate a short XPath selector for the `url_element` element (if possible, create a short one; otherwise, it's a full selector)

```
>>> url_element.generate_xpath_selector
'//body/div/div[2]/div/div/span[2]/a'
```

Generate a full XPath selector for the `url_element` element from the start of the page

```
>>> url_element.generate_full_xpath_selector
'//body/div/div[2]/div/div/span[2]/a'
```

Note:

When you tell Scrapling to create a short selector, it tries to find a unique element to use in generation as a stop point, like an element with an `id` attribute, but in our case, there wasn't any, so that's why the short and the full selector will be the same.

## Using selectors with regular expressions[¶](#using-selectors-with-regular-expressions "Permanent link")

Similar to `parsel`/`scrapy`, `re` and `re_first` methods are available for extracting data using regular expressions. However, unlike the former libraries, these methods are in nearly all classes like `Selector`/`Selectors`/`TextHandler` and `TextHandlers`, which means you can use them directly on the element even if you didn't select a text node.

We will have a deep look at it while explaining the [TextHandler](main_classes.html#texthandler) class, but in general, it works like the examples below:

```
>>> page.css('.price_color')[0].re_first(r'[\d\.]+')
'51.77'

>>> page.css('.price_color').re_first(r'[\d\.]+')
'51.77'

>>> page.css('.price_color').re(r'[\d\.]+')
['51.77',
 '53.74',
 '50.10',
 '47.82',
 '54.23',
...]

>>> page.css('.product_pod h3 a::attr(href)').re(r'catalogue/(.*)/index.html')
['a-light-in-the-attic_1000',
 'tipping-the-velvet_999',
 'soumission_998',
 'sharp-objects_997',
...]

>>> filtering_function = lambda e: e.parent.tag == 'h3' and e.parent.parent.has_class('product_pod')  # As above selector
>>> page.find('a', filtering_function).attrib['href'].re(r'catalogue/(.*)/index.html')
['a-light-in-the-attic_1000']

>>> page.find_by_text('Tipping the Velvet').attrib['href'].re(r'catalogue/(.*)/index.html')
['tipping-the-velvet_999']
```

And so on. You get the idea. We will explain this in more detail on the next page, along with the [TextHandler](main_classes.html#texthandler) class.

Was this page helpful?

Thanks for your feedback!

Thanks for your feedback! Help us improve this page by
[opening a documentation issue](https://github.com/D4Vinci/Scrapling/issues/new?template=04-docs_issue.yml).


---
## Source: https://scrapling.readthedocs.io/en/latest/parsing/main_classes.html
---

# Parsing main classes[¶](#parsing-main-classes "Permanent link")

Prerequisites

* You’ve completed or read the [Querying elements](../parsing/selection.html) page to understand how to find/extract elements from the [Selector](../parsing/main_classes.html#selector) object.

After exploring the various ways to select elements with Scrapling and its related features, let's take a step back and examine the [Selector](#selector) class in general, as well as other objects, to gain a better understanding of the parsing engine.

The [Selector](#selector) class is the core parsing engine in Scrapling, providing HTML parsing and element selection capabilities. You can always import it with any of the following imports

```
from scrapling import Selector
from scrapling.parser import Selector
```

Then use it directly as you already learned in the [overview](../overview.html) page

```
page = Selector(
    '<html>...</html>',
    url='https://example.com'
)

# Then select elements as you like
elements = page.css('.product')
```

In Scrapling, the main object you deal with after passing an HTML source or fetching a website is, of course, a [Selector](#selector) object. Any operation you do, like selection, navigation, etc., will return either a [Selector](#selector) object or a [Selectors](#selectors) object, given that the result is element/elements from the page, not text or similar.

In other words, the main page is a [Selector](#selector) object, and the elements within are [Selector](#selector) objects, and so on. Any text, such as the text content inside elements or the text inside element attributes, is a [TextHandler](#texthandler) object, and the attributes of each element are stored as [AttributesHandler](#attributeshandler). We will return to both objects later, so let's focus on the [Selector](#selector) object.

## Selector[¶](#selector "Permanent link")

### Arguments explained[¶](#arguments-explained "Permanent link")

The most important one is `content`, it's used to pass the HTML code you want to parse, and it accepts the HTML content as `str` or `bytes`.

Otherwise, you have the arguments `url`, `adaptive`, `storage`, and `storage_args`. All these arguments are settings used with the `adaptive` feature, and they don't make a difference if you are not going to use that feature, so just ignore them for now, and we will explain them in the [adaptive](adaptive.html) feature page.

Then you have the arguments for parsing adjustments or adjusting/manipulating the HTML content while the library is parsing it:

* **encoding**: This is the encoding that will be used while parsing the HTML. The default is `UTF-8`.
* **keep_comments**: This tells the library whether to keep HTML comments while parsing the page. It's disabled by default because it can cause issues with your scraping in various ways.
* **keep_cdata**: Same logic as the HTML comments. [cdata](https://stackoverflow.com/questions/7092236/what-is-cdata-in-html) is removed by default for cleaner HTML.

I have intended to ignore the arguments `huge_tree` and `root` to avoid making this page more complicated than needed.
You may notice that I'm doing that a lot because it involves advanced features that you don't need to know to use the library. The development section will cover these missing parts if you are very invested.

After that, most properties on the main page and its elements are lazily loaded. This means they don't get initialized until you use them like the text content of a page/element, and this is one of the reasons for Scrapling speed :)

### Properties[¶](#properties "Permanent link")

You have already seen much of this on the [overview](../overview.html) page, but don't worry if you didn't. We will review it more thoroughly using more advanced methods/usages. For clarity, the properties for traversal are separated below in the [traversal](#traversal) section.

Let's say we are parsing this HTML page for simplicity:

```
<html>
  <head>
    <title>Some page</title>
  </head>
  <body>
    <div class="product-list">
      <article class="product" data-id="1">
        <h3>Product 1</h3>
        <p class="description">This is product 1</p>
        <span class="price">$10.99</span>
        <div class="hidden stock">In stock: 5</div>
      </article>

      <article class="product" data-id="2">
        <h3>Product 2</h3>
        <p class="description">This is product 2</p>
        <span class="price">$20.99</span>
        <div class="hidden stock">In stock: 3</div>
      </article>

      <article class="product" data-id="3">
        <h3>Product 3</h3>
        <p class="description">This is product 3</p>
        <span class="price">$15.99</span>
        <div class="hidden stock">Out of stock</div>
      </article>
    </div>

    <script id="page-data" type="application/json">
      {
        "lastUpdated": "2024-09-22T10:30:00Z",
        "totalProducts": 3
      }
    </script>
  </body>
</html>
```

Load the page directly as shown before:

```
from scrapling import Selector
page = Selector(html_doc)
```

Get all text content on the page recursively

```
>>> page.get_all_text()
'Some page\n\n    \n\n      \nProduct 1\nThis is product 1\n$10.99\nIn stock: 5\nProduct 2\nThis is product 2\n$20.99\nIn stock: 3\nProduct 3\nThis is product 3\n$15.99\nOut of stock'
```

Get the first article, as explained before; we will use it as an example

```
article = page.find('article')
```

With the same logic, get all text content on the element recursively

```
>>> article.get_all_text()
'Product 1\nThis is product 1\n$10.99\nIn stock: 5'
```

But if you try to get the direct text content, it will be empty because it doesn't have direct text in the HTML code above

```
>>> article.text
''
```

The `get_all_text` method has the following optional arguments:

1. **separator**: All strings collected will be concatenated using this separator. The default is '\n'.
2. **strip**: If enabled, strings will be stripped before concatenation. Disabled by default.
3. **ignore_tags**: A tuple of all tag names you want to ignore in the final results and ignore any elements nested within them. The default is `('script', 'style',)`.
4. **valid_values**: If enabled, the method will only collect elements with real values, so all elements with empty text content or only whitespaces will be ignored. It's enabled by default

By the way, the text returned here is not a standard string but a [TextHandler](#texthandler); we will get to this in detail later, so if the text content can be serialized to JSON, use `.json()` on it

```
>>> script = page.find('script')
>>> script.json()
{'lastUpdated': '2024-09-22T10:30:00Z', 'totalProducts': 3}
```

Let's continue to get the element tag

```
>>> article.tag
'article'
```

If you use it on the page directly, you will find that you are operating on the root `html` element

```
>>> page.tag
'html'
```

Now, I think I've hammered the (`page`/`element`) idea, so I won't return to it.

Getting the attributes of the element

```
>>> print(article.attrib)
{'class': 'product', 'data-id': '1'}
```

Access a specific attribute with any of the following

```
>>> article.attrib['class']
>>> article.attrib.get('class')
>>> article['class']  # new in v0.3
```

Check if the attributes contain a specific attribute with any of the methods below

```
>>> 'class' in article.attrib
>>> 'class' in article  # new in v0.3
```

Get the HTML content of the element

```
>>> article.html_content
'<article class="product" data-id="1"><h3>Product 1</h3>\n        <p class="description">This is product 1</p>\n        <span class="price">$10.99</span>\n        <div class="hidden stock">In stock: 5</div>\n      </article>'
```

Get the prettified version of the element's HTML content

```
print(article.prettify())
```

```
<article class="product" data-id="1"><h3>Product 1</h3>
    <p class="description">This is product 1</p>
    <span class="price">$10.99</span>
    <div class="hidden stock">In stock: 5</div>
</article>
```

Use the `.body` property to get the raw content of the page. Starting from v0.4, when used on a `Response` object from fetchers, `.body` always returns `bytes`.

```
>>> page.body
'<html>\n  <head>\n    <title>Some page</title>\n  </head>\n  ...'
```

To get all the ancestors in the DOM tree of this element

```
>>> article.path
[<data='<div class="product-list"> <article clas...' parent='<body> <div class="product-list"> <artic...'>,
 <data='<body> <div class="product-list"> <artic...' parent='<html><head><title>Some page</title></he...'>,
 <data='<html><head><title>Some page</title></he...'>]
```

Generate a CSS shortened selector if possible, or generate the full selector

```
>>> article.generate_css_selector
'body > div > article'
>>> article.generate_full_css_selector
'body > div > article'
```

Same case with XPath

```
>>> article.generate_xpath_selector
"//body/div/article"
>>> article.generate_full_xpath_selector
"//body/div/article"
```

### Traversal[¶](#traversal "Permanent link")

Using the elements we found above, we will go over the properties/methods for moving on the page in detail.

If you are unfamiliar with the DOM tree or the tree data structure in general, the following traversal part can be confusing. I recommend you look up these concepts online to better understand them.

If you are too lazy to search about it, here's a quick explanation to give you a good idea.  
In simple words, the `html` element is the root of the website's tree, as every page starts with an `html` element.  
This element will be positioned directly above elements such as `head` and `body`. These are considered "children" of the `html` element, and the `html` element is considered their "parent". The element `body` is a "sibling" of the element `head` and vice versa.

Accessing the parent of an element

```
>>> article.parent
<data='<div class="product-list"> <article clas...' parent='<body> <div class="product-list"> <artic...'>
>>> article.parent.tag
'div'
```

You can chain it as you want, which applies to all similar properties/methods we will review.

```
>>> article.parent.parent.tag
'body'
```

Get the children of an element

```
>>> article.children
[<data='<h3>Product 1</h3>' parent='<article class="product" data-id="1"><h3...'>,
 <data='<p class="description">This is product 1...' parent='<article class="product" data-id="1"><h3...'>,
 <data='<span class="price">$10.99</span>' parent='<article class="product" data-id="1"><h3...'>,
 <data='<div class="hidden stock">In stock: 5</d...' parent='<article class="product" data-id="1"><h3...'>]
```

Get all elements underneath an element. It acts as a nested version of the `children` property

```
>>> article.below_elements
[<data='<h3>Product 1</h3>' parent='<article class="product" data-id="1"><h3...'>,
 <data='<p class="description">This is product 1...' parent='<article class="product" data-id="1"><h3...'>,
 <data='<span class="price">$10.99</span>' parent='<article class="product" data-id="1"><h3...'>,
 <data='<div class="hidden stock">In stock: 5</d...' parent='<article class="product" data-id="1"><h3...'>]
```

This element returns the same result as the `children` property because its children don't have children.

Another example of using the element with the `product-list` class will clear the difference between the `children` property and the `below_elements` property

```
>>> products_list = page.css('.product-list')[0]
>>> products_list.children
[<data='<article class="product" data-id="1"><h3...' parent='<div class="product-list"> <article clas...'>,
 <data='<article class="product" data-id="2"><h3...' parent='<div class="product-list"> <article clas...'>,
 <data='<article class="product" data-id="3"><h3...' parent='<div class="product-list"> <article clas...'>]

>>> products_list.below_elements
[<data='<article class="product" data-id="1"><h3...' parent='<div class="product-list"> <article clas...'>,
 <data='<h3>Product 1</h3>' parent='<article class="product" data-id="1"><h3...'>,
 <data='<p class="description">This is product 1...' parent='<article class="product" data-id="1"><h3...'>,
 <data='<span class="price">$10.99</span>' parent='<article class="product" data-id="1"><h3...'>,
 <data='<div class="hidden stock">In stock: 5</d...' parent='<article class="product" data-id="1"><h3...'>,
 <data='<article class="product" data-id="2"><h3...' parent='<div class="product-list"> <article clas...'>,
...]
```

Get the siblings of an element

```
>>> article.siblings
[<data='<article class="product" data-id="2"><h3...' parent='<div class="product-list"> <article clas...'>,
 <data='<article class="product" data-id="3"><h3...' parent='<div class="product-list"> <article clas...'>]
```

Get the next element of the current element

```
>>> article.next
<data='<article class="product" data-id="2"><h3...' parent='<div class="product-list"> <article clas...'>
```

The same logic applies to the `previous` property

```
>>> article.previous  # It's the first child, so it doesn't have a previous element
>>> second_article = page.css('.product[data-id="2"]')[0]
>>> second_article.previous
<data='<article class="product" data-id="1"><h3...' parent='<div class="product-list"> <article clas...'>
```

You can check easily and pretty fast if an element has a specific class name or not

```
>>> article.has_class('product')
True
```

If your case needs more than the element's parent, you can iterate over the whole ancestors' tree of any element, like the example below

```
for ancestor in article.iterancestors():
    # do something with it...
```

You can search for a specific ancestor of an element that satisfies a search function; all you need to do is pass a function that takes a [Selector](#selector) object as an argument and return `True` if the condition satisfies or `False` otherwise, like below:

```
>>> article.find_ancestor(lambda ancestor: ancestor.has_class('product-list'))
<data='<div class="product-list"> <article clas...' parent='<body> <div class="product-list"> <artic...'>

>>> article.find_ancestor(lambda ancestor: ancestor.css('.product-list'))  # Same result, different approach
<data='<div class="product-list"> <article clas...' parent='<body> <div class="product-list"> <artic...'>
```

## Selectors[¶](#selectors "Permanent link")

The class `Selectors` is the "List" version of the [Selector](#selector) class. It inherits from the Python standard `List` type, so it shares all `List` properties and methods while adding more methods to make the operations you want to execute on the [Selector](#selector) instances within more straightforward.

In the [Selector](#selector) class, all methods/properties that should return a group of elements return them as a [Selectors](#selectors) class instance.

Starting with v0.4, all selection methods consistently return [Selector](#selector)/[Selectors](#selectors) objects, even for text nodes and attribute values. Text nodes (selected via `::text`, `/text()`, `::attr()`, `/@attr`) are wrapped in [Selector](#selector) objects. These text node selectors have `tag` set to `"#text"`, and their `text` property returns the text value. You can still access the text value directly, and all other properties return empty/default values gracefully.

```
>>> page.css('a::text')              # -> Selectors (of text node Selectors)
>>> page.xpath('//a/text()')         # -> Selectors
>>> page.css('a::text').get()        # -> TextHandler (the first text value)
>>> page.css('a::text').getall()     # -> TextHandlers (all text values)
>>> page.css('a::attr(href)')        # -> Selectors
>>> page.xpath('//a/@href')          # -> Selectors
>>> page.css('.price_color')         # -> Selectors
```

### Data extraction methods[¶](#data-extraction-methods "Permanent link")

Starting with v0.4, [Selector](#selector) and [Selectors](#selectors) both provide `get()`, `getall()`, and their aliases `extract_first` and `extract` (following Scrapy conventions). The old `get_all()` method has been removed.

**On a [Selector](#selector) object:**

* `get()` returns a `TextHandler`: for text node selectors, it returns the text value; for HTML element selectors, it returns the serialized outer HTML.
* `getall()` returns a `TextHandlers` list containing the single serialized string.
* `extract_first` is an alias for `get()`, and `extract` is an alias for `getall()`.

```
>>> page.css('h3')[0].get()        # Outer HTML of the element
'<h3>Product 1</h3>'

>>> page.css('h3::text')[0].get()  # Text value of the text node
'Product 1'
```

**On a [Selectors](#selectors) object:**

* `get(default=None)` returns the serialized string of the **first** element, or `default` if the list is empty.
* `getall()` serializes **all** elements and returns a `TextHandlers` list.
* `extract_first` is an alias for `get()`, and `extract` is an alias for `getall()`.

```
>>> page.css('.price::text').get()      # First price text
'$10.99'

>>> page.css('.price::text').getall()   # All price texts
['$10.99', '$20.99', '$15.99']

>>> page.css('.price::text').get('')    # With default value
'$10.99'
```

These methods work seamlessly with all selection types (CSS, XPath, `find`, etc.) and are the recommended way to extract text and attribute values in a Scrapy-compatible style.

Now, let's see what [Selectors](#selectors) class adds to the table with that out of the way.

### Properties[¶](#properties_1 "Permanent link")

Apart from the standard operations on Python lists, such as iteration and slicing.

You can do the following:

Execute CSS and XPath selectors directly on the [Selector](#selector) instances it has, while the return types are the same as [Selector](#selector)'s `css` and `xpath` methods. The arguments are similar, except the `adaptive` argument is not available here. This, of course, makes chaining methods very straightforward.

```
>>> page.css('.product_pod a')
[<data='<a href="catalogue/a-light-in-the-attic_...' parent='<div class="image_container"> <a href="c...'>,
 <data='<a href="catalogue/a-light-in-the-attic_...' parent='<h3><a href="catalogue/a-light-in-the-at...'>,
 <data='<a href="catalogue/tipping-the-velvet_99...' parent='<div class="image_container"> <a href="c...'>,
 <data='<a href="catalogue/tipping-the-velvet_99...' parent='<h3><a href="catalogue/tipping-the-velve...'>,
 <data='<a href="catalogue/soumission_998/index....' parent='<div class="image_container"> <a href="c...'>,
 <data='<a href="catalogue/soumission_998/index....' parent='<h3><a href="catalogue/soumission_998/in...'>,
...]

>>> page.css('.product_pod').css('a')  # Returns the same result
[<data='<a href="catalogue/a-light-in-the-attic_...' parent='<div class="image_container"> <a href="c...'>,
 <data='<a href="catalogue/a-light-in-the-attic_...' parent='<h3><a href="catalogue/a-light-in-the-at...'>,
 <data='<a href="catalogue/tipping-the-velvet_99...' parent='<div class="image_container"> <a href="c...'>,
 <data='<a href="catalogue/tipping-the-velvet_99...' parent='<h3><a href="catalogue/tipping-the-velve...'>,
 <data='<a href="catalogue/soumission_998/index....' parent='<div class="image_container"> <a href="c...'>,
 <data='<a href="catalogue/soumission_998/index....' parent='<h3><a href="catalogue/soumission_998/in...'>,
...]
```

Run the `re` and `re_first` methods directly. They take the same arguments passed to the [Selector](#selector) class. I will leave the explanation of these methods to the [TextHandler](#texthandler) section below.

However, in this class, the `re_first` behaves differently as it runs `re` on each [Selector](#selector) within and returns the first one with a result. The `re` method will return a [TextHandlers](#texthandlers) object as normal, which combines all the [TextHandler](#texthandler) instances into one [TextHandlers](#texthandlers) instance.

```
>>> page.css('.price_color').re(r'[\d\.]+')
['51.77',
 '53.74',
 '50.10',
 '47.82',
 '54.23',
...]

>>> page.css('.product_pod h3 a::attr(href)').re(r'catalogue/(.*)/index.html')
['a-light-in-the-attic_1000',
 'tipping-the-velvet_999',
 'soumission_998',
 'sharp-objects_997',
...]
```

With the `search` method, you can search quickly in the available [Selector](#selector) instances. The function you pass must accept a [Selector](#selector) instance as the first argument and return True/False. The method will return the first [Selector](#selector) instance that satisfies the function; otherwise, it will return `None`.

```
# Find all the products with price '53.23'.
>>> search_function = lambda p: float(p.css('.price_color').re_first(r'[\d\.]+')) == 54.23
>>> page.css('.product_pod').search(search_function)
<data='<article class="product_pod"><div class=...' parent='<li class="col-xs-6 col-sm-4 col-md-3 co...'>
```

You can use the `filter` method, too, which takes a function like the `search` method but returns an `Selectors` instance of all the [Selector](#selector) instances that satisfy the function

```
# Find all products with prices over $50
>>> filtering_function = lambda p: float(p.css('.price_color').re_first(r'[\d\.]+')) > 50
>>> page.css('.product_pod').filter(filtering_function)
[<data='<article class="product_pod"><div class=...' parent='<li class="col-xs-6 col-sm-4 col-md-3 co...'>,
 <data='<article class="product_pod"><div class=...' parent='<li class="col-xs-6 col-sm-4 col-md-3 co...'>,
 <data='<article class="product_pod"><div class=...' parent='<li class="col-xs-6 col-sm-4 col-md-3 co...'>,
...]
```

You can safely access the first or last element without worrying about index errors:

```
>>> page.css('.product').first   # First Selector or None
<data='<article class="product" data-id="1"><h3...'>
>>> page.css('.product').last    # Last Selector or None
<data='<article class="product" data-id="3"><h3...'>
>>> page.css('.nonexistent').first  # Returns None instead of raising IndexError
```

If you are too lazy like me and want to know the number of [Selector](#selector) instances in a [Selectors](#selectors) instance. You can do this:

```
page.css('.product_pod').length
```

which is equivalent to

```
len(page.css('.product_pod'))
```

Yup, like JavaScript :)

## TextHandler[¶](#texthandler "Permanent link")

This class is mandatory to understand, as all methods/properties that should return a string for you will return `TextHandler`, and the ones that should return a list of strings will return [TextHandlers](#texthandlers) instead.

TextHandler is a subclass of the standard Python string, so you can do anything with it that you can do with a Python string. So, what is the difference that requires a different naming?

Of course, TextHandler provides extra methods and properties that standard Python strings can't do. We will review them now, but remember that all methods and properties in all classes that return string(s) return TextHandler, which opens the door for creativity and makes the code shorter and cleaner, as you will see. Also, you can import it directly and use it on any string, which we will explain [later](../development/scrapling_custom_types.html).

### Usage[¶](#usage "Permanent link")

First, before discussing the added methods, you need to know that all operations on it, like slicing, accessing by index, etc., and methods like `split`, `replace`, `strip`, etc., all return a `TextHandler` again, so you can chain them as you want. If you find a method or property that returns a standard string instead of `TextHandler`, please open an issue, and we will override it as well.

First, we start with the `re` and `re_first` methods. These are the same methods that exist in the other classes ([Selector](#selector), [Selectors](#selectors), and [TextHandlers](#texthandlers)), so they accept the same arguments.

* The `re` method takes a string/compiled regex pattern as the first argument. It searches the data for all strings matching the regex and returns them as a [TextHandlers](#texthandlers) instance. The `re_first` method takes the same arguments and behaves similarly, but, as you probably figured out from the name, it returns only the first result as a `TextHandler` instance.

  Also, it takes other helpful arguments, which are:

  + **replace_entities**: This is enabled by default. It replaces character entity references with their corresponding characters.
  + **clean_match**: It's disabled by default. This causes the method to ignore all whitespace, including consecutive spaces, while matching.
  + **case_sensitive**: It's enabled by default. As the name implies, disabling it causes the regex to ignore letter case during compilation.

  You have seen these examples before; the return result is [TextHandlers](#texthandlers) because we used the `re` method.

  ```
  >>> page.css('.price_color').re(r'[\d\.]+')
  ['51.77',
   '53.74',
   '50.10',
   '47.82',
   '54.23',
  ...]

  >>> page.css('.product_pod h3 a::attr(href)').re(r'catalogue/(.*)/index.html')
  ['a-light-in-the-attic_1000',
   'tipping-the-velvet_999',
   'soumission_998',
   'sharp-objects_997',
  ...]
  ```

  To explain the other arguments better, we will use a custom string for each example below

  ```
  >>> from scrapling import TextHandler
  >>> test_string = TextHandler('hi  there')  # Hence the two spaces
  >>> test_string.re('hi there')
  >>> test_string.re('hi there', clean_match=True)  # Using `clean_match` will clean the string before matching the regex
  ['hi there']

  >>> test_string2 = TextHandler('Oh, Hi Mark')
  >>> test_string2.re_first('oh, hi Mark')
  >>> test_string2.re_first('oh, hi Mark', case_sensitive=False)  # Hence disabling `case_sensitive`
  'Oh, Hi Mark'

  # Mixing arguments
  >>> test_string.re('hi there', clean_match=True, case_sensitive=False)
  ['hi There']
  ```

  Another use of the idea of replacing strings with `TextHandler` everywhere is that a property like `html_content` returns `TextHandler`, so you can do regex on the HTML content if you want:

  ```
  >>> page.html_content.re('div class=".*">(.*)</div')
  ['In stock: 5', 'In stock: 3', 'Out of stock']
  ```
* You also have the `.json()` method, which tries to convert the content to a JSON object quickly if possible; otherwise, it throws an error

  ```
  >>> page.css('#page-data::text').get()
    '\n      {\n        "lastUpdated": "2024-09-22T10:30:00Z",\n        "totalProducts": 3\n      }\n    '
  >>> page.css('#page-data::text').get().json()
    {'lastUpdated': '2024-09-22T10:30:00Z', 'totalProducts': 3}
  ```

  Hence, if you didn't specify a text node while selecting an element (like the text content or an attribute text content), the text content will be selected automatically, like this

  ```
  >>> page.css('#page-data')[0].json()
  {'lastUpdated': '2024-09-22T10:30:00Z', 'totalProducts': 3}
  ```

  The [Selector](#selector) class adds one thing here, too; let's say this is the page we are working with:

  ```
  <html>
      <body>
          <div>
            <script id="page-data" type="application/json">
              {
                "lastUpdated": "2024-09-22T10:30:00Z",
                "totalProducts": 3
              }
            </script>
          </div>
      </body>
  </html>
  ```

  The [Selector](#selector) class has the `get_all_text` method, which you should be aware of by now. This method returns a `TextHandler`, of course.  
    
  So, as you know here, if you did something like this

  ```
  >>> page.css('div::text').get().json()
  ```

  You will get an error because the `div` tag doesn't have any direct text content that can be serialized to JSON; it doesn't have any direct text content at all.  
    
  In this case, the `get_all_text` method comes to the rescue, so you can do something like that

  ```
  >>> page.css('div')[0].get_all_text(ignore_tags=[]).json()
    {'lastUpdated': '2024-09-22T10:30:00Z', 'totalProducts': 3}
  ```

  I used the `ignore_tags` argument here because the default value of it is `('script', 'style',)`, as you are aware.  
    
  Another related behavior to be aware of occurs when using any fetcher, which we will explain later. If you have a JSON response like this example:

  ```
  >>> page = Selector("""{"some_key": "some_value"}""")
  ```

  Because the [Selector](#selector) class is optimized to deal with HTML pages, it will deal with it as a broken HTML response and fix it, so if you used the `html_content` property, you get this

  ```
  >>> page.html_content
  '<html><body><p>{"some_key": "some_value"}</p></body></html>'
  ```

  Here, you can use the `json` method directly, and it will work

  ```
  >>> page.json()
  {'some_key': 'some_value'}
  ```

  You might wonder how this happened, given that the `html` tag doesn't contain direct text.  
  Well, for cases like JSON responses, I made the [Selector](#selector) class keep a raw copy of the content it receives. This way, when you use the `.json()` method, it checks for that raw copy and then converts it to JSON. If the raw copy is unavailable, as with the elements, it checks the current element's text content; otherwise, it uses the `get_all_text` method directly.
* Another handy method is `.clean()`, which will remove all white spaces and consecutive spaces for you and return a new `TextHandler` instance

  ```
  >>> TextHandler('\n wonderful  idea, \reh?').clean()
  'wonderful idea, eh?'
  ```

  Also, you can pass the `remove_entities` argument to make `clean` replace HTML entities with their corresponding characters.
* Another method that might be helpful in some cases is the `.sort()` method to sort the string for you, as you do with lists

  ```
  >>> TextHandler('acb').sort()
  'abc'
  ```

  Or do it in reverse:

  ```
  >>> TextHandler('acb').sort(reverse=True)
  'cba'
  ```

Other methods and properties will be added over time, but remember that this class is returned in place of strings nearly everywhere in the library.

## TextHandlers[¶](#texthandlers "Permanent link")

You probably guessed it: This class is similar to [Selectors](#selectors) and [Selector](#selector), but here it inherits the same logic and method as standard lists, with only `re` and `re_first` as new methods.

The only difference is that the `re_first` method logic here runs `re` on each [TextHandler](#texthandler) and returns the first result, or `None`. Nothing new needs to be explained here, but new methods will be added over time.

## AttributesHandler[¶](#attributeshandler "Permanent link")

This is a read-only version of Python's standard dictionary, or `dict`, used solely to store the attributes of each element/[Selector](#selector) instance.

```
>>> print(page.find('script').attrib)
{'id': 'page-data', 'type': 'application/json'}
>>> type(page.find('script').attrib).__name__
'AttributesHandler'
```

Because it's read-only, it will use fewer resources than the standard dictionary. Still, it has the same dictionary method and properties, except those that allow you to modify/override the data.

It currently adds two extra simple methods:

* The `search_values` method

  In standard dictionaries, you can do `dict.get("key_name")` to check if a key exists. However, if you want to search by values rather than keys, you will need some additional code lines. This method does that for you. It allows you to search the current attributes by values and returns a dictionary of each matching item.

  A simple example would be

  ```
  >>> for i in page.find('script').attrib.search_values('page-data'):
          print(i)
  {'id': 'page-data'}
  ```

  But this method provides the `partial` argument as well, which allows you to search by part of the value:

  ```
  >>> for i in page.find('script').attrib.search_values('page', partial=True):
          print(i)
  {'id': 'page-data'}
  ```

  These examples won't happen in the real world; most likely, a more real-world example would be using it with the `find_all` method to find all elements that have a specific value in their arguments:

  ```
  >>> page.find_all(lambda element: list(element.attrib.search_values('product')))
  [<data='<article class="product" data-id="1"><h3...' parent='<div class="product-list"> <article clas...'>,
   <data='<article class="product" data-id="2"><h3...' parent='<div class="product-list"> <article clas...'>,
   <data='<article class="product" data-id="3"><h3...' parent='<div class="product-list"> <article clas...'>]
  ```

  All these elements have 'product' as the value for the `class` attribute.

  Hence, I used the `list` function here because `search_values` returns a generator, so it would be `True` for all elements.
* The `json_string` property

  This property converts current attributes to a JSON string if the attributes are JSON serializable; otherwise, it throws an error.

  ```
  >>>page.find('script').attrib.json_string
  b'{"id":"page-data","type":"application/json"}'
  ```

Was this page helpful?

Thanks for your feedback!

Thanks for your feedback! Help us improve this page by
[opening a documentation issue](https://github.com/D4Vinci/Scrapling/issues/new?template=04-docs_issue.yml).


---
## Source: https://scrapling.readthedocs.io/en/latest/parsing/adaptive.html
---

# Adaptive scraping[¶](#adaptive-scraping "Permanent link")

Prerequisites

1. You've completed or read the [Querying elements](../parsing/selection.html) page to understand how to find/extract elements from the [Selector](../parsing/main_classes.html#selector) object.
2. You've completed or read the [Main classes](../parsing/main_classes.html) page to understand the [Selector](../parsing/main_classes.html#selector) class.

Adaptive scraping (previously known as automatch) is one of Scrapling's most powerful features. It allows your scraper to survive website changes by intelligently tracking and relocating elements.

Let's say you are scraping a page with a structure like this:

```
<div class="container">
    <section class="products">
        <article class="product" id="p1">
            <h3>Product 1</h3>
            <p class="description">Description 1</p>
        </article>
        <article class="product" id="p2">
            <h3>Product 2</h3>
            <p class="description">Description 2</p>
        </article>
    </section>
</div>
```

And you want to scrape the first product, the one with the `p1` ID. You will probably write a selector like this

```
page.css('#p1')
```

When website owners implement structural changes like

```
<div class="new-container">
    <div class="product-wrapper">
        <section class="products">
            <article class="product new-class" data-id="p1">
                <div class="product-info">
                    <h3>Product 1</h3>
                    <p class="new-description">Description 1</p>
                </div>
            </article>
            <article class="product new-class" data-id="p2">
                <div class="product-info">
                    <h3>Product 2</h3>
                    <p class="new-description">Description 2</p>
                </div>
            </article>
        </section>
    </div>
</div>
```

The selector will no longer function, and your code needs maintenance. That's where Scrapling's `adaptive` feature comes into play.

With Scrapling, you can enable the `adaptive` feature the first time you select an element, and the next time you select that element and it doesn't exist, Scrapling will remember its properties and search on the website for the element with the highest percentage of similarity to that element, and without AI :)

```
from scrapling import Selector, Fetcher
# Before the change
page = Selector(page_source, adaptive=True, url='example.com')
# or
Fetcher.adaptive = True
page = Fetcher.get('https://example.com')
# then
element = page.css('#p1', auto_save=True)
if not element:  # One day website changes?
    element = page.css('#p1', adaptive=True)  # Scrapling still finds it!
# the rest of your code...
```

Below, I will show you an example of how to use this feature. Then, we will dive deep into how to use it and provide details about this feature. Note that it works with all selection methods, not just CSS/XPATH selection.

## Real-World Scenario[¶](#real-world-scenario "Permanent link")

Let's use a real website as an example and use one of the fetchers to fetch its source. To achieve this, we need to identify a website that is about to update its design/structure, copy its source, and then wait for the website to change. Of course, that's nearly impossible to know unless I know the website's owner, but that will make it a staged test, haha.

To solve this issue, I will use [The Web Archive](https://archive.org/)'s [Wayback Machine](https://web.archive.org/). Here is a copy of [StackOverFlow's website in 2010](https://web.archive.org/web/20100102003420/http://stackoverflow.com/); pretty old, eh?Let's see if the adaptive feature can extract the same button in the old design from 2010 and the current design using the same selector :)

If I want to extract the Questions button from the old design, I can use a selector like this: `#hmenus > div:nth-child(1) > ul > li:nth-child(1) > a`. This selector is too specific because it was generated by Google Chrome.

Now, let's test the same selector in both versions

```
>> from scrapling import Fetcher
>> selector = '#hmenus > div:nth-child(1) > ul > li:nth-child(1) > a'
>> old_url = "https://web.archive.org/web/20100102003420/http://stackoverflow.com/"
>> new_url = "https://stackoverflow.com/"
>> Fetcher.configure(adaptive = True, adaptive_domain='stackoverflow.com')
>> 
>> page = Fetcher.get(old_url, timeout=30)
>> element1 = page.css(selector, auto_save=True)[0]
>> 
>> # Same selector but used in the updated website
>> page = Fetcher.get(new_url)
>> element2 = page.css(selector, adaptive=True)[0]
>> 
>> if element1.text == element2.text:
...    print('Scrapling found the same element in the old and new designs!')
'Scrapling found the same element in the old and new designs!'
```

Note that I introduced a new argument called `adaptive_domain`. This is because, for Scrapling, these are two different domains (`archive.org` and `stackoverflow.com`), so Scrapling will isolate their `adaptive` data. To inform Scrapling that they are the same website, we must pass the custom domain we wish to use while saving `adaptive` data for both, ensuring Scrapling doesn't isolate them.

The code will be the same in a real-world scenario, except it will use the same URL for both requests, so you won't need to use the `adaptive_domain` argument. This is the closest example I can give to real-world cases, so I hope it didn't confuse you :)

Hence, in the two examples above, I used both the `Selector` and `Fetcher` classes to show that the adaptive logic is the same.

Info

The main reason for creating the `adaptive_domain` argument was to handle if the website changed its URL while changing the design/structure. In that case, you can use it to continue using the previously stored adaptive data for the new URL. Otherwise, scrapling will consider it a new website and discard the old data.

## How the adaptive scraping feature works[¶](#how-the-adaptive-scraping-feature-works "Permanent link")

Adaptive scraping works in two phases:

1. **Save Phase**: Store unique properties of elements
2. **Match Phase**: Find elements with similar properties later

Let's say you've selected an element through any method and want the library to find it the next time you scrape this website, even if it undergoes structural/design changes.

With as few technical details as possible, the general logic goes as follows:

1. You tell Scrapling to save that element's unique properties in one of the ways we will show below.
2. Scrapling uses its configured database (SQLite by default) and saves each element's unique properties.
3. Now, because everything about the element can be changed or removed by the website's owner(s), nothing from the element can be used as a unique identifier for the database. To solve this issue, I made the storage system rely on two things:

   1. The domain of the current website. If you are using the `Selector` class, pass it when initializing; if you are using a fetcher, the domain will be automatically taken from the URL.
   2. An `identifier` to query that element's properties from the database. You don't always have to set the identifier yourself; we'll discuss this later.

   Together, they will later be used to retrieve the element's unique properties from the database.
4. Later, when the website's structure changes, you tell Scrapling to find the element by enabling `adaptive`. Scrapling retrieves the element's unique properties and matches all elements on the page against the unique properties we already have for this element. A score is calculated based on their similarity to the desired element. In that comparison, everything is taken into consideration, as you will see later
5. The element(s) with the highest similarity score to the wanted element are returned.

### The unique properties[¶](#the-unique-properties "Permanent link")

You might wonder what unique properties we are referring to when discussing the removal or alteration of all element properties.

For Scrapling, the unique elements we are relying on are:

* Element tag name, text, attributes (names and values), siblings (tag names only), and path (tag names only).
* Element's parent tag name, attributes (names and values), and text.

But you need to understand that the comparison between elements isn't exact; it's more about how similar these values are. So everything is considered, even the values' order, like the order in which the element class names were written before and the order in which the same element class names are written now.

## How to use adaptive feature[¶](#how-to-use-adaptive-feature "Permanent link")

The adaptive feature can be applied to any found element, and it's added as arguments to CSS/XPath Selection methods, as you saw above, but we will get back to that later.

First, you must enable the `adaptive` feature by passing `adaptive=True` to the [Selector](main_classes.html#selector) class when you initialize it or enable it in the fetcher you are using of the available fetchers, as we will show.

Examples:

```
>>> from scrapling import Selector, Fetcher
>>> page = Selector(html_doc, adaptive=True)
# OR
>>> Fetcher.adaptive = True
>>> page = Fetcher.get('https://example.com')
```

If you are using the [Selector](main_classes.html#selector) class, you need to pass the url of the website you are using with the argument `url` so Scrapling can separate the properties saved for each element by domain.

If you didn't pass a URL, the word `default` will be used in place of the URL field while saving the element's unique properties. So, this will only be an issue if you use the same identifier later for a different website and don't pass the URL parameter when initializing it. The save process overwrites previous data, and the `adaptive` feature uses only the latest saved properties.

Besides those arguments, we have `storage` and `storage_args`. Both are for the class to connect to the database; by default, it uses the SQLite class provided by the library. Those arguments shouldn't matter unless you want to write your own storage system, which we will cover on a [separate page in the development section](../development/adaptive_storage_system.html).

Now that you've enabled the `adaptive` feature globally, you have two main ways to use it.

### The CSS/XPath Selection way[¶](#the-cssxpath-selection-way "Permanent link")

As you have seen in the example above, first, you have to use the `auto_save` argument while selecting an element that exists on the page, like below

```
element = page.css('#p1', auto_save=True)
```

And when the element doesn't exist, you can use the same selector and the `adaptive` argument, and the library will find it for you

```
element = page.css('#p1', adaptive=True)
```

Pretty simple, eh?

Well, a lot happened under the hood here. Remember the identifier we mentioned before that you need to set to retrieve the element you want? Here, with the `css`/`xpath` methods, the identifier is set automatically as the selector you passed here to make things easier :)

Additionally, for all these methods, you can pass the `identifier` argument to set it yourself. This is useful in some instances, or you can use it to save properties with the `auto_save` argument.

### The manual way[¶](#the-manual-way "Permanent link")

You manually save and retrieve an element, then relocate it, which all happens within the `adaptive` feature, as shown below. This allows you to relocate any element using any method or selection!

First, let's say you got an element like this by text:

```
>>> element = page.find_by_text('Tipping the Velvet', first_match=True)
```

You can save its unique properties using the `save` method, as shown below, but you must set the identifier yourself. For this example, I chose `my_special_element` as an identifier, but it's best to use a meaningful identifier in your code for the same reason you use meaningful variable names :)

```
>>> page.save(element, 'my_special_element')
```

Now, later, when you want to retrieve it and relocate it inside the page with `adaptive`, it would be like this

```
>>> element_dict = page.retrieve('my_special_element')
>>> page.relocate(element_dict, selector_type=True)
[<data='<a href="catalogue/tipping-the-velvet_99...' parent='<h3><a href="catalogue/tipping-the-velve...'>]
>>> page.relocate(element_dict, selector_type=True).css('::text').getall()
['Tipping the Velvet']
```

Hence, the `retrieve` and `relocate` methods are used.

If you want to keep it as a `lxml.etree` object, leave the `selector_type` argument

```
>>> page.relocate(element_dict)
[<Element a at 0x105a2a7b0>]
```

## Troubleshooting[¶](#troubleshooting "Permanent link")

### No Matches Found[¶](#no-matches-found "Permanent link")

```
# 1. Check if data was saved
element_data = page.retrieve('identifier')
if not element_data:
    print("No data saved for this identifier")

# 2. Try with different identifier
products = page.css('.product', adaptive=True, identifier='old_selector')

# 3. Save again with new identifier
products = page.css('.new-product', auto_save=True, identifier='new_identifier')
```

### Wrong Elements Matched[¶](#wrong-elements-matched "Permanent link")

```
# Use more specific selectors
products = page.css('.product-list .product', auto_save=True)

# Or save with more context
product = page.find_by_text('Product Name').parent
page.save(product, 'specific_product')
```

## Known Issues[¶](#known-issues "Permanent link")

In the `adaptive` save process, only the unique properties of the first element in the selection results are saved. So if the selector you are using selects different elements on the page in other locations, `adaptive` will return the first element to you only when you relocate it later. This doesn't include combined CSS selectors (Using commas to combine more than one selector, for example), as these selectors are separated and each is executed alone.

## Final thoughts[¶](#final-thoughts "Permanent link")

Explaining this feature in detail without complications turned out to be challenging. However, still, if there's something left unclear, you can head out to the [discussions section](https://github.com/D4Vinci/Scrapling/discussions), and I will reply to you ASAP, or the Discord server, or reach out to me privately and have a chat :)

Was this page helpful?

Thanks for your feedback!

Thanks for your feedback! Help us improve this page by
[opening a documentation issue](https://github.com/D4Vinci/Scrapling/issues/new?template=04-docs_issue.yml).


---
## Source: https://scrapling.readthedocs.io/en/latest/fetching/choosing.html
---

# Fetchers basics[¶](#fetchers-basics "Permanent link")

## Introduction[¶](#introduction "Permanent link")

Fetchers are classes that can do requests or fetch pages for you easily in a single-line fashion with many features and then return a [Response](#response-object) object. Starting with v0.3, all fetchers have separate classes to keep the session running, so for example, a fetcher that uses a browser will keep the browser open till you finish all your requests through it instead of opening multiple browsers. So it depends on your use case.

This feature was introduced because, before v0.2, Scrapling was only a parsing engine. The target here is to gradually become the one-stop shop for all Web Scraping needs.

> Fetchers are not wrappers built on top of other libraries. However, they only use these libraries as an engine to request/fetch pages. To further clarify this, all fetchers have features that the underlying engines don't, while still fully leveraging those engines and optimizing them for Web Scraping.

## Fetchers Overview[¶](#fetchers-overview "Permanent link")

Scrapling provides three different fetcher classes with their session classes; each fetcher is designed for a specific use case.

The following table compares them and can be quickly used for guidance.

| Feature | Fetcher | DynamicFetcher | StealthyFetcher |
| --- | --- | --- | --- |
| Relative speed | 🐇🐇🐇🐇🐇 | 🐇🐇🐇 | 🐇🐇🐇 |
| Stealth | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Anti-Bot options | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| JavaScript loading | ❌ | ✅ | ✅ |
| Memory Usage | ⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| Best used for | Basic scraping when HTTP requests alone can do it | - Dynamically loaded websites  - Small automation - Small-Mid protections | - Dynamically loaded websites  - Small automation  - Small-Complicated protections |
| Browser(s) | ❌ | Chromium and Google Chrome | Chromium and Google Chrome |
| Browser API used | ❌ | PlayWright | PlayWright |
| Setup Complexity | Simple | Simple | Simple |

In the following pages, we will talk about each one in detail.

## Parser configuration in all fetchers[¶](#parser-configuration-in-all-fetchers "Permanent link")

All fetchers share the same import method, as you will see in the upcoming pages

```
>>> from scrapling.fetchers import Fetcher, AsyncFetcher, StealthyFetcher, DynamicFetcher
```

Then you use it right away without initializing like this, and it will use the default parser settings:

```
>>> page = StealthyFetcher.fetch('https://example.com')
```

If you want to configure the parser ([Selector class](../parsing/main_classes.html#selector)) that will be used on the response before returning it for you, then do this first:

```
>>> from scrapling.fetchers import Fetcher
>>> Fetcher.configure(adaptive=True, keep_comments=False, keep_cdata=False)  # and the rest
```

or

```
>>> from scrapling.fetchers import Fetcher
>>> Fetcher.adaptive=True
>>> Fetcher.keep_comments=False
>>> Fetcher.keep_cdata=False  # and the rest
```

Then, continue your code as usual.

The available configuration arguments are: `adaptive`, `adaptive_domain`, `huge_tree`, `keep_comments`, `keep_cdata`, `storage`, and `storage_args`, which are the same ones you give to the [Selector](../parsing/main_classes.html#selector) class. You can display the current configuration anytime by running `<fetcher_class>.display_config()`.

Info

The `adaptive` argument is disabled by default; you must enable it to use that feature.

### Set parser config per request[¶](#set-parser-config-per-request "Permanent link")

As you probably understand, the logic above for setting the parser config will apply globally to all requests/fetches made through that class, and it's intended for simplicity.

If your use case requires a different configuration for each request/fetch, you can pass a dictionary to the request method (`fetch`/`get`/`post`/...) to an argument named `selector_config`.

## Response Object[¶](#response-object "Permanent link")

The `Response` object is the same as the [Selector](../parsing/main_classes.html#selector) class, but it has additional details about the response, like response headers, status, cookies, etc., as shown below:

```
>>> from scrapling.fetchers import Fetcher
>>> page = Fetcher.get('https://example.com')

>>> page.status          # HTTP status code
>>> page.reason          # Status message
>>> page.cookies         # Response cookies as a dictionary
>>> page.headers         # Response headers
>>> page.request_headers # Request headers
>>> page.history         # Response history of redirections, if any
>>> page.body            # Raw response body as bytes
>>> page.encoding        # Response encoding
>>> page.meta            # Response metadata dictionary (e.g., proxy used). Mainly helpful with the spiders system.
>>> page.captured_xhr    # List of captured XHR/fetch responses (when capture_xhr is enabled on a browser session)
```

All fetchers return the `Response` object.

Note

Unlike the [Selector](../parsing/main_classes.html#selector) class, the `Response` class's body is always bytes since v0.4.

Was this page helpful?

Thanks for your feedback!

Thanks for your feedback! Help us improve this page by
[opening a documentation issue](https://github.com/D4Vinci/Scrapling/issues/new?template=04-docs_issue.yml).


---
## Source: https://scrapling.readthedocs.io/en/latest/fetching/static.html
---

# HTTP requests[¶](#http-requests "Permanent link")

The `Fetcher` class provides rapid and lightweight HTTP requests using the high-performance `curl_cffi` library with a lot of stealth capabilities.

Prerequisites

1. You've completed or read the [Fetchers basics](../fetching/choosing.html) page to understand what the [Response object](../fetching/choosing.html#response-object) is and which fetcher to use.
2. You've completed or read the [Querying elements](../parsing/selection.html) page to understand how to find/extract elements from the [Selector](../parsing/main_classes.html#selector)/[Response](../fetching/choosing.html#response-object) object.
3. You've completed or read the [Main classes](../parsing/main_classes.html) page to know what properties/methods the [Response](../fetching/choosing.html#response-object) class is inheriting from the [Selector](../parsing/main_classes.html#selector) class.

## Basic Usage[¶](#basic-usage "Permanent link")

You have one primary way to import this Fetcher, which is the same for all fetchers.

```
>>> from scrapling.fetchers import Fetcher
```

Check out how to configure the parsing options [here](choosing.html#parser-configuration-in-all-fetchers)

### Shared arguments[¶](#shared-arguments "Permanent link")

All methods for making requests here share some arguments, so let's discuss them first.

* **url**: The targeted URL
* **stealthy_headers**: If enabled (default), it creates and adds real browser headers. It also sets a Google referer header.
* **follow_redirects**: As the name implies, tell the fetcher to follow redirections. **Enabled by default**
* **timeout**: The number of seconds to wait for each request to be finished. **Defaults to 30 seconds**.
* **retries**: The number of retries that the fetcher will do for failed requests. **Defaults to three retries**.
* **retry_delay**: Number of seconds to wait between retry attempts. **Defaults to 1 second**.
* **impersonate**: Impersonate specific browsers' TLS fingerprints. Accepts browser strings or a list of them like `"chrome110"`, `"firefox102"`, `"safari15_5"` to use specific versions or `"chrome"`, `"firefox"`, `"safari"`, `"edge"` to automatically use the latest version available. This makes your requests appear to come from real browsers at the TLS level. If you pass it a list of strings, it will choose a random one with each request. **Defaults to the latest available Chrome version.**
* **http3**: Use HTTP/3 protocol for requests. **Defaults to False**. It might be problematic if used with `impersonate`.
* **cookies**: Cookies to use in the request. Can be a dictionary of `name→value` or a list of dictionaries.
* **proxy**: As the name implies, the proxy for this request is used to route all traffic (HTTP and HTTPS). The format accepted here is `http://username:password@localhost:8030`.
* **proxy_auth**: HTTP basic auth for proxy, tuple of (username, password).
* **proxies**: Dict of proxies to use. Format: `{"http": proxy_url, "https": proxy_url}`.
* **proxy_rotator**: A `ProxyRotator` instance for automatic proxy rotation. Cannot be combined with `proxy` or `proxies`.
* **headers**: Headers to include in the request. Can override any header generated by the `stealthy_headers` argument
* **max_redirects**: Maximum number of redirects. **Defaults to 30**, use -1 for unlimited.
* **verify**: Whether to verify HTTPS certificates. **Defaults to True**.
* **cert**: Tuple of (cert, key) filenames for the client certificate.
* **selector_config**: A dictionary of custom parsing arguments to be used when creating the final `Selector`/`Response` class.

Notes:

1. The currently available browsers to impersonate are (`"edge"`, `"chrome"`, `"chrome_android"`, `"safari"`, `"safari_beta"`, `"safari_ios"`, `"safari_ios_beta"`, `"firefox"`, `"tor"`)
2. The available browsers to impersonate, along with their corresponding versions, are automatically displayed in the argument autocompletion and updated with each `curl_cffi` update.
3. If any of the arguments `impersonate` or `stealthy_headers` are enabled, the fetchers will automatically generate real browser headers that match the browser version used.

Other than this, for further customization, you can pass any arguments that `curl_cffi` supports for any method if that method doesn't already support them.

### HTTP Methods[¶](#http-methods "Permanent link")

There are additional arguments for each method, depending on the method, such as `params` for GET requests and `data`/`json` for POST/PUT/DELETE requests.

Examples are the best way to explain this:

> Hence: `OPTIONS` and `HEAD` methods are not supported.

#### GET[¶](#get "Permanent link")

```
>>> from scrapling.fetchers import Fetcher
>>> # Basic GET
>>> page = Fetcher.get('https://example.com')
>>> page = Fetcher.get('https://scrapling.requestcatcher.com/get', stealthy_headers=True, follow_redirects=True)
>>> page = Fetcher.get('https://scrapling.requestcatcher.com/get', proxy='http://username:password@localhost:8030')
>>> # With parameters
>>> page = Fetcher.get('https://example.com/search', params={'q': 'query'})
>>>
>>> # With headers
>>> page = Fetcher.get('https://example.com', headers={'User-Agent': 'Custom/1.0'})
>>> # Basic HTTP authentication
>>> page = Fetcher.get("https://example.com", auth=("my_user", "password123"))
>>> # Browser impersonation
>>> page = Fetcher.get('https://example.com', impersonate='chrome')
>>> # HTTP/3 support
>>> page = Fetcher.get('https://example.com', http3=True)
```

And for asynchronous requests, it's a small adjustment

```
>>> from scrapling.fetchers import AsyncFetcher
>>> # Basic GET
>>> page = await AsyncFetcher.get('https://example.com')
>>> page = await AsyncFetcher.get('https://scrapling.requestcatcher.com/get', stealthy_headers=True, follow_redirects=True)
>>> page = await AsyncFetcher.get('https://scrapling.requestcatcher.com/get', proxy='http://username:password@localhost:8030')
>>> # With parameters
>>> page = await AsyncFetcher.get('https://example.com/search', params={'q': 'query'})
>>>
>>> # With headers
>>> page = await AsyncFetcher.get('https://example.com', headers={'User-Agent': 'Custom/1.0'})
>>> # Basic HTTP authentication
>>> page = await AsyncFetcher.get("https://example.com", auth=("my_user", "password123"))
>>> # Browser impersonation
>>> page = await AsyncFetcher.get('https://example.com', impersonate='chrome110')
>>> # HTTP/3 support
>>> page = await AsyncFetcher.get('https://example.com', http3=True)
```

Needless to say, the `page` object in all cases is [Response](choosing.html#response-object) object, which is a [Selector](../parsing/main_classes.html#selector) as we said, so you can use it directly

```
>>> page.css('.something.something')

>>> page = Fetcher.get('https://api.github.com/events')
>>> page.json()
[{'id': '<redacted>',
  'type': 'PushEvent',
  'actor': {'id': '<redacted>',
   'login': '<redacted>',
   'display_login': '<redacted>',
   'gravatar_id': '',
   'url': 'https://api.github.com/users/<redacted>',
   'avatar_url': 'https://avatars.githubusercontent.com/u/<redacted>'},
  'repo': {'id': '<redacted>',
...
```

#### POST[¶](#post "Permanent link")

```
>>> from scrapling.fetchers import Fetcher
>>> # Basic POST
>>> page = Fetcher.post('https://scrapling.requestcatcher.com/post', data={'key': 'value'}, params={'q': 'query'})
>>> page = Fetcher.post('https://scrapling.requestcatcher.com/post', data={'key': 'value'}, stealthy_headers=True, follow_redirects=True)
>>> page = Fetcher.post('https://scrapling.requestcatcher.com/post', data={'key': 'value'}, proxy='http://username:password@localhost:8030', impersonate="chrome")
>>> # Another example of form-encoded data
>>> page = Fetcher.post('https://example.com/submit', data={'username': 'user', 'password': 'pass'}, http3=True)
>>> # JSON data
>>> page = Fetcher.post('https://example.com/api', json={'key': 'value'})
```

And for asynchronous requests, it's a small adjustment

```
>>> from scrapling.fetchers import AsyncFetcher
>>> # Basic POST
>>> page = await AsyncFetcher.post('https://scrapling.requestcatcher.com/post', data={'key': 'value'})
>>> page = await AsyncFetcher.post('https://scrapling.requestcatcher.com/post', data={'key': 'value'}, stealthy_headers=True, follow_redirects=True)
>>> page = await AsyncFetcher.post('https://scrapling.requestcatcher.com/post', data={'key': 'value'}, proxy='http://username:password@localhost:8030', impersonate="chrome")
>>> # Another example of form-encoded data
>>> page = await AsyncFetcher.post('https://example.com/submit', data={'username': 'user', 'password': 'pass'}, http3=True)
>>> # JSON data
>>> page = await AsyncFetcher.post('https://example.com/api', json={'key': 'value'})
```

#### PUT[¶](#put "Permanent link")

```
>>> from scrapling.fetchers import Fetcher
>>> # Basic PUT
>>> page = Fetcher.put('https://example.com/update', data={'status': 'updated'})
>>> page = Fetcher.put('https://example.com/update', data={'status': 'updated'}, stealthy_headers=True, follow_redirects=True, impersonate="chrome")
>>> page = Fetcher.put('https://example.com/update', data={'status': 'updated'}, proxy='http://username:password@localhost:8030')
>>> # Another example of form-encoded data
>>> page = Fetcher.put("https://scrapling.requestcatcher.com/put", data={'key': ['value1', 'value2']})
```

And for asynchronous requests, it's a small adjustment

```
>>> from scrapling.fetchers import AsyncFetcher
>>> # Basic PUT
>>> page = await AsyncFetcher.put('https://example.com/update', data={'status': 'updated'})
>>> page = await AsyncFetcher.put('https://example.com/update', data={'status': 'updated'}, stealthy_headers=True, follow_redirects=True, impersonate="chrome")
>>> page = await AsyncFetcher.put('https://example.com/update', data={'status': 'updated'}, proxy='http://username:password@localhost:8030')
>>> # Another example of form-encoded data
>>> page = await AsyncFetcher.put("https://scrapling.requestcatcher.com/put", data={'key': ['value1', 'value2']})
```

#### DELETE[¶](#delete "Permanent link")

```
>>> from scrapling.fetchers import Fetcher
>>> page = Fetcher.delete('https://example.com/resource/123')
>>> page = Fetcher.delete('https://example.com/resource/123', stealthy_headers=True, follow_redirects=True, impersonate="chrome")
>>> page = Fetcher.delete('https://example.com/resource/123', proxy='http://username:password@localhost:8030')
```

And for asynchronous requests, it's a small adjustment

```
>>> from scrapling.fetchers import AsyncFetcher
>>> page = await AsyncFetcher.delete('https://example.com/resource/123')
>>> page = await AsyncFetcher.delete('https://example.com/resource/123', stealthy_headers=True, follow_redirects=True, impersonate="chrome")
>>> page = await AsyncFetcher.delete('https://example.com/resource/123', proxy='http://username:password@localhost:8030')
```

## Session Management[¶](#session-management "Permanent link")

For making multiple requests with the same configuration, use the `FetcherSession` class. It can be used in both synchronous and asynchronous code without issue; the class automatically detects and changes the session type, without requiring a different import.

The `FetcherSession` class can accept nearly all the arguments that the methods can take, which enables you to specify a config for the entire session and later choose a different config for one of the requests effortlessly, as you will see in the following examples.

```
from scrapling.fetchers import FetcherSession

# Create a session with default configuration
with FetcherSession(
    impersonate='chrome',
    http3=True,
    stealthy_headers=True,
    timeout=30,
    retries=3
) as session:
    # Make multiple requests with the same settings and the same cookies
    page1 = session.get('https://scrapling.requestcatcher.com/get')
    page2 = session.post('https://scrapling.requestcatcher.com/post', data={'key': 'value'})
    page3 = session.get('https://api.github.com/events')

    # All requests share the same session and connection pool
```

You can also use a `ProxyRotator` with `FetcherSession` for automatic proxy rotation across requests:

```
from scrapling.fetchers import FetcherSession, ProxyRotator

rotator = ProxyRotator([
    'http://proxy1:8080',
    'http://proxy2:8080',
    'http://proxy3:8080',
])

with FetcherSession(proxy_rotator=rotator, impersonate='chrome') as session:
    # Each request automatically uses the next proxy in rotation
    page1 = session.get('https://example.com/page1')
    page2 = session.get('https://example.com/page2')

    # You can check which proxy was used via the response metadata
    print(page1.meta['proxy'])
```

You can also override the session proxy (or rotator) for a specific request by passing `proxy=` directly to the request method:

```
with FetcherSession(proxy='http://default-proxy:8080') as session:
    # Uses the session proxy
    page1 = session.get('https://example.com/page1')

    # Override the proxy for this specific request
    page2 = session.get('https://example.com/page2', proxy='http://special-proxy:9090')
```

And here's an async example

```
async with FetcherSession(impersonate='firefox', http3=True) as session:
    # All standard HTTP methods available
    response = await session.get('https://example.com')
    response = await session.post('https://scrapling.requestcatcher.com/post', json={'data': 'value'})
    response = await session.put('https://scrapling.requestcatcher.com/put', data={'update': 'info'})
    response = await session.delete('https://scrapling.requestcatcher.com/delete')
```

or better

```
import asyncio
from scrapling.fetchers import FetcherSession

# Async session usage
async with FetcherSession(impersonate="safari") as session:
    urls = ['https://example.com/page1', 'https://example.com/page2']

    tasks = [
        session.get(url) for url in urls
    ]

    pages = await asyncio.gather(*tasks)
```

The `Fetcher` class uses `FetcherSession` to create a temporary session with each request you make.

### Session Benefits[¶](#session-benefits "Permanent link")

* **A lot faster**: 10 times faster than creating a single session for each request
* **Cookie persistence**: Automatic cookie handling across requests
* **Resource efficiency**: Better memory and CPU usage for multiple requests
* **Centralized configuration**: Single place to manage request settings

## Examples[¶](#examples "Permanent link")

Some well-rounded examples to aid newcomers to Web Scraping

### Basic HTTP Request[¶](#basic-http-request "Permanent link")

```
from scrapling.fetchers import Fetcher

# Make a request
page = Fetcher.get('https://example.com')

# Check the status
if page.status == 200:
    # Extract title
    title = page.css('title::text').get()
    print(f"Page title: {title}")

    # Extract all links
    links = page.css('a::attr(href)').getall()
    print(f"Found {len(links)} links")
```

### Product Scraping[¶](#product-scraping "Permanent link")

```
from scrapling.fetchers import Fetcher

def scrape_products():
    page = Fetcher.get('https://example.com/products')

    # Find all product elements
    products = page.css('.product')

    results = []
    for product in products:
        results.append({
            'title': product.css('.title::text').get(),
            'price': product.css('.price::text').re_first(r'\d+\.\d{2}'),
            'description': product.css('.description::text').get(),
            'in_stock': product.has_class('in-stock')
        })

    return results
```

### Downloading Files[¶](#downloading-files "Permanent link")

```
from scrapling.fetchers import Fetcher

page = Fetcher.get('https://raw.githubusercontent.com/D4Vinci/Scrapling/main/images/main_cover.png')
with open(file='main_cover.png', mode='wb') as f:
   f.write(page.body)
```

### Pagination Handling[¶](#pagination-handling "Permanent link")

```
from scrapling.fetchers import Fetcher

def scrape_all_pages():
    base_url = 'https://example.com/products?page={}'
    page_num = 1
    all_products = []

    while True:
        # Get current page
        page = Fetcher.get(base_url.format(page_num))

        # Find products
        products = page.css('.product')
        if not products:
            break

        # Process products
        for product in products:
            all_products.append({
                'name': product.css('.name::text').get(),
                'price': product.css('.price::text').get()
            })

        # Next page
        page_num += 1

    return all_products
```

### Form Submission[¶](#form-submission "Permanent link")

```
from scrapling.fetchers import Fetcher

# Submit login form
response = Fetcher.post(
    'https://example.com/login',
    data={
        'username': 'user@example.com',
        'password': 'password123'
    }
)

# Check login success
if response.status == 200:
    # Extract user info
    user_name = response.css('.user-name::text').get()
    print(f"Logged in as: {user_name}")
```

### Table Extraction[¶](#table-extraction "Permanent link")

```
from scrapling.fetchers import Fetcher

def extract_table():
    page = Fetcher.get('https://example.com/data')

    # Find table
    table = page.css('table')[0]

    # Extract headers
    headers = [
        th.text for th in table.css('thead th')
    ]

    # Extract rows
    rows = []
    for row in table.css('tbody tr'):
        cells = [td.text for td in row.css('td')]
        rows.append(dict(zip(headers, cells)))

    return rows
```

### Navigation Menu[¶](#navigation-menu "Permanent link")

```
from scrapling.fetchers import Fetcher

def extract_menu():
    page = Fetcher.get('https://example.com')

    # Find navigation
    nav = page.css('nav')[0]

    menu = {}
    for item in nav.css('li'):
        links = item.css('a')
        if links:
            link = links[0]
            menu[link.text] = {
                'url': link['href'],
                'has_submenu': bool(item.css('.submenu'))
            }

    return menu
```

## When to Use[¶](#when-to-use "Permanent link")

Use `Fetcher` when:

* Need rapid HTTP requests.
* Want minimal overhead.
* Don't need JavaScript execution (the website can be scraped through requests).
* Need some stealth features (ex, the targeted website is using protection but doesn't use JavaScript challenges).

Use `FetcherSession` when:

* Making multiple requests to the same or different sites.
* Need to maintain cookies/authentication between requests.
* Want connection pooling for better performance.
* Require consistent configuration across requests.
* Working with APIs that require a session state.

Use other fetchers when:

* Need browser automation.
* Need advanced anti-bot/stealth capabilities.
* Need JavaScript support or interacting with dynamic content

Was this page helpful?

Thanks for your feedback!

Thanks for your feedback! Help us improve this page by
[opening a documentation issue](https://github.com/D4Vinci/Scrapling/issues/new?template=04-docs_issue.yml).


---
## Source: https://scrapling.readthedocs.io/en/latest/fetching/dynamic.html
---

# Fetching dynamic websites[¶](#fetching-dynamic-websites "Permanent link")

Here, we will discuss the `DynamicFetcher` class (formerly `PlayWrightFetcher`). This class provides flexible browser automation with multiple configuration options and little under-the-hood stealth improvements.

As we will explain later, to automate the page, you need some knowledge of [Playwright's Page API](https://playwright.dev/python/docs/api/class-page).

Prerequisites

1. You've completed or read the [Fetchers basics](../fetching/choosing.html) page to understand what the [Response object](../fetching/choosing.html#response-object) is and which fetcher to use.
2. You've completed or read the [Querying elements](../parsing/selection.html) page to understand how to find/extract elements from the [Selector](../parsing/main_classes.html#selector)/[Response](../fetching/choosing.html#response-object) object.
3. You've completed or read the [Main classes](../parsing/main_classes.html) page to know what properties/methods the [Response](../fetching/choosing.html#response-object) class is inheriting from the [Selector](../parsing/main_classes.html#selector) class.

## Basic Usage[¶](#basic-usage "Permanent link")

You have one primary way to import this Fetcher, which is the same for all fetchers.

```
>>> from scrapling.fetchers import DynamicFetcher
```

Check out how to configure the parsing options [here](choosing.html#parser-configuration-in-all-fetchers)

Now, we will review most of the arguments one by one, using examples. If you want to jump to a table of all arguments for quick reference, [click here](#full-list-of-arguments)

Abstract

The async version of the `fetch` method is `async_fetch`, of course.

This fetcher currently provides three main run options that can be combined as desired.

Which are:

### 1. Vanilla Playwright[¶](#1-vanilla-playwright "Permanent link")

```
DynamicFetcher.fetch('https://example.com')
```

Using it in that manner will open a Chromium browser and load the page. There are optimizations for speed, and some stealth goes automatically under the hood, but other than that, there are no tricks or extra features unless you enable some; it's just a plain PlayWright API.

### 2. Real Chrome[¶](#2-real-chrome "Permanent link")

```
DynamicFetcher.fetch('https://example.com', real_chrome=True)
```

If you have a Google Chrome browser installed, use this option. It's the same as the first option, but it will use the Google Chrome browser you installed on your device instead of Chromium. This will make your requests look more authentic, so they're less detectable for better results.

If you don't have Google Chrome installed and want to use this option, you can use the command below in the terminal to install it for the library instead of installing it manually:

```
playwright install chrome
```

### 3. CDP Connection[¶](#3-cdp-connection "Permanent link")

```
DynamicFetcher.fetch('https://example.com', cdp_url='ws://localhost:9222')
```

Instead of launching a browser locally (Chromium/Google Chrome), you can connect to a remote browser through the [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/).

Notes:

* There was a `stealth` option here, but it was moved to the `StealthyFetcher` class, as explained on the next page, with additional features since version 0.3.13.
* This makes it less confusing for new users, easier to maintain, and provides other benefits, as explained on the [StealthyFetcher page](../fetching/stealthy.html).

## Full list of arguments[¶](#full-list-of-arguments "Permanent link")

Scrapling provides many options with this fetcher and its session classes. To make it as simple as possible, we will list the options here and give examples of how to use most of them.

| Argument | Description | Optional |
| --- | --- | --- |
| url | Target url | ❌ |
| headless | Pass `True` to run the browser in headless/hidden (**default**) or `False` for headful/visible mode. | ✔️ |
| disable_resources | Drop requests for unnecessary resources for a speed boost. Requests dropped are of type `font`, `image`, `media`, `beacon`, `object`, `imageset`, `texttrack`, `websocket`, `csp_report`, and `stylesheet`. | ✔️ |
| cookies | Set cookies for the next request. | ✔️ |
| useragent | Pass a useragent string to be used. **Otherwise, the fetcher will generate and use a real Useragent of the same browser and version.** | ✔️ |
| network_idle | Wait for the page until there are no network connections for at least 500 ms. | ✔️ |
| load_dom | Enabled by default, wait for all JavaScript on page(s) to fully load and execute (wait for the `domcontentloaded` state). | ✔️ |
| timeout | The timeout (milliseconds) used in all operations and waits through the page. The default is 30,000 ms (30 seconds). | ✔️ |
| wait | The time (milliseconds) the fetcher will wait after everything finishes before closing the page and returning the `Response` object. | ✔️ |
| page_action | Added for automation. Pass a function that takes the `page` object and does the necessary automation. | ✔️ |
| wait_selector | Wait for a specific css selector to be in a specific state. | ✔️ |
| init_script | An absolute path to a JavaScript file to be executed on page creation for all pages in this session. | ✔️ |
| wait_selector_state | Scrapling will wait for the given state to be fulfilled for the selector given with `wait_selector`. *Default state is `attached`.* | ✔️ |
| google_search | Enabled by default, Scrapling will set a Google referer header. | ✔️ |
| extra_headers | A dictionary of extra headers to add to the request. *The referer set by `google_search` takes priority over the referer set here if used together.* | ✔️ |
| proxy | The proxy to be used with requests. It can be a string or a dictionary with only the keys 'server', 'username', and 'password'. | ✔️ |
| real_chrome | If you have a Chrome browser installed on your device, enable this, and the Fetcher will launch and use an instance of your browser. | ✔️ |
| locale | Specify user locale, for example, `en-GB`, `de-DE`, etc. Locale will affect `navigator.language` value, `Accept-Language` request header value, as well as number and date formatting rules. Defaults to the system default locale. | ✔️ |
| timezone_id | Changes the timezone of the browser. Defaults to the system timezone. | ✔️ |
| cdp_url | Instead of launching a new browser instance, connect to this CDP URL to control real browsers through CDP. | ✔️ |
| user_data_dir | Path to a User Data Directory, which stores browser session data like cookies and local storage. The default is to create a temporary directory. **Only Works with sessions** | ✔️ |
| extra_flags | A list of additional browser flags to pass to the browser on launch. | ✔️ |
| additional_args | Additional arguments to be passed to Playwright's context as additional settings, and they take higher priority than Scrapling's settings. | ✔️ |
| selector_config | A dictionary of custom parsing arguments to be used when creating the final `Selector`/`Response` class. | ✔️ |
| blocked_domains | A set of domain names to block requests to. Subdomains are also matched (e.g., `"example.com"` blocks `"sub.example.com"` too). | ✔️ |
| proxy_rotator | A `ProxyRotator` instance for automatic proxy rotation. Cannot be combined with `proxy`. | ✔️ |
| retries | Number of retry attempts for failed requests. Defaults to 3. | ✔️ |
| retry_delay | Seconds to wait between retry attempts. Defaults to 1. | ✔️ |
| capture_xhr | Pass a regex URL pattern string to capture XHR/fetch requests matching it during page load. Captured responses are available via `response.captured_xhr`. Defaults to `None` (disabled). | ✔️ |
| executable_path | Absolute path to a custom browser executable to use instead of the bundled Chromium. Useful for non-standard installations or custom browser builds. | ✔️ |

In session classes, all these arguments can be set globally for the session. Still, you can configure each request individually by passing some of the arguments here that can be configured on the browser tab level like: `google_search`, `timeout`, `wait`, `page_action`, `extra_headers`, `disable_resources`, `wait_selector`, `wait_selector_state`, `network_idle`, `load_dom`, `blocked_domains`, `proxy`, and `selector_config`.

Notes:

1. The `disable_resources` option made requests ~25% faster in my tests for some websites and can help save your proxy usage, but be careful with it, as it can cause some websites to never finish loading.
2. The `google_search` argument is enabled by default for all requests, setting the referer to `https://www.google.com/`. If used together with `extra_headers`, it takes priority over the referer set there.
3. Since version 0.3.13, the `stealth` option has been removed here in favor of the `StealthyFetcher` class, and the `hide_canvas` option has been moved to it. The `disable_webgl` argument has been moved to the `StealthyFetcher` class and renamed as `allow_webgl`.
4. If you didn't set a user agent and enabled headless mode, the fetcher will generate a real user agent for the same browser version and use it. If you didn't set a user agent and didn't enable headless mode, the fetcher will use the browser's default user agent, which is the same as in standard browsers in the latest versions.

## Examples[¶](#examples "Permanent link")

It's easier to understand with examples, so let's take a look.

### Resource Control[¶](#resource-control "Permanent link")

```
# Disable unnecessary resources
page = DynamicFetcher.fetch('https://example.com', disable_resources=True)  # Blocks fonts, images, media, etc.
```

### Domain Blocking[¶](#domain-blocking "Permanent link")

```
# Block requests to specific domains (and their subdomains)
page = DynamicFetcher.fetch('https://example.com', blocked_domains={"ads.example.com", "tracker.net"})
```

### Network Control[¶](#network-control "Permanent link")

```
# Wait for network idle (Consider fetch to be finished when there are no network connections for at least 500 ms)
page = DynamicFetcher.fetch('https://example.com', network_idle=True)

# Custom timeout (in milliseconds)
page = DynamicFetcher.fetch('https://example.com', timeout=30000)  # 30 seconds

# Proxy support (It can also be a dictionary with only the keys 'server', 'username', and 'password'.)
page = DynamicFetcher.fetch('https://example.com', proxy='http://username:password@host:port')
```

### Proxy Rotation[¶](#proxy-rotation "Permanent link")

```
from scrapling.fetchers import DynamicSession, ProxyRotator

# Set up proxy rotation
rotator = ProxyRotator([
    "http://proxy1:8080",
    "http://proxy2:8080",
    "http://proxy3:8080",
])

# Use with session - rotates proxy automatically with each request
with DynamicSession(proxy_rotator=rotator, headless=True) as session:
    page1 = session.fetch('https://example1.com')
    page2 = session.fetch('https://example2.com')

    # Override rotator for a specific request
    page3 = session.fetch('https://example3.com', proxy='http://specific-proxy:8080')
```

Warning

Remember that by default, all browser-based fetchers and sessions use a persistent browser context with a pool of tabs. However, since browsers can't set a proxy per tab, when you use a `ProxyRotator`, the fetcher will automatically open a separate context for each proxy, with one tab per context. Once the tab's job is done, both the tab and its context are closed.

### Downloading Files[¶](#downloading-files "Permanent link")

```
page = DynamicFetcher.fetch('https://raw.githubusercontent.com/D4Vinci/Scrapling/main/images/main_cover.png')

with open(file='main_cover.png', mode='wb') as f:
    f.write(page.body)
```

The `body` attribute of the `Response` object always returns `bytes`.

### Browser Automation[¶](#browser-automation "Permanent link")

This is where your knowledge about [Playwright's Page API](https://playwright.dev/python/docs/api/class-page) comes into play. The function you pass here takes the page object from Playwright's API, performs the desired action, and then the fetcher continues.

This function is executed immediately after waiting for `network_idle` (if enabled) and before waiting for the `wait_selector` argument, allowing it to be used for purposes beyond automation. You can alter the page as you want.

In the example below, I used the pages' [mouse events](https://playwright.dev/python/docs/api/class-mouse) to scroll the page with the mouse wheel, then move the mouse.

```
from playwright.sync_api import Page

def scroll_page(page: Page):
    page.mouse.wheel(10, 0)
    page.mouse.move(100, 400)
    page.mouse.up()

page = DynamicFetcher.fetch('https://example.com', page_action=scroll_page)
```

Of course, if you use the async fetch version, the function must also be async.

```
from playwright.async_api import Page

async def scroll_page(page: Page):
   await page.mouse.wheel(10, 0)
   await page.mouse.move(100, 400)
   await page.mouse.up()

page = await DynamicFetcher.async_fetch('https://example.com', page_action=scroll_page)
```

### Wait Conditions[¶](#wait-conditions "Permanent link")

```
# Wait for the selector
page = DynamicFetcher.fetch(
    'https://example.com',
    wait_selector='h1',
    wait_selector_state='visible'
)
```

This is the last wait the fetcher will do before returning the response (if enabled). You pass a CSS selector to the `wait_selector` argument, and the fetcher will wait for the state you passed in the `wait_selector_state` argument to be fulfilled. If you didn't pass a state, the default would be `attached`, which means it will wait for the element to be present in the DOM.

After that, if `load_dom` is enabled (the default), the fetcher will check again to see if all JavaScript files are loaded and executed (in the `domcontentloaded` state) or continue waiting. If you have enabled `network_idle`, the fetcher will wait for `network_idle` to be fulfilled again, as explained above.

The states the fetcher can wait for can be any of the following ([source](https://playwright.dev/python/docs/api/class-page#page-wait-for-selector)):

* `attached`: Wait for an element to be present in the DOM.
* `detached`: Wait for an element to not be present in the DOM.
* `visible`: wait for an element to have a non-empty bounding box and no `visibility:hidden`. Note that an element without any content or with `display:none` has an empty bounding box and is not considered visible.
* `hidden`: wait for an element to be either detached from the DOM, or have an empty bounding box, or `visibility:hidden`. This is opposite to the `'visible'` option.

### Capturing XHR/Fetch Requests[¶](#capturing-xhrfetch-requests "Permanent link")

Many SPAs load data through background API calls (XHR/fetch). You can capture these requests by passing a regex URL pattern to `capture_xhr` at the session level:

```
from scrapling.fetchers import DynamicSession

with DynamicSession(capture_xhr=r"https://api\.example\.com/.*", headless=True) as session:
    page = session.fetch('https://example.com')

    # Access captured XHR responses
    for xhr in page.captured_xhr:
        print(xhr.url, xhr.status)
        print(xhr.body)  # Raw response body as bytes
```

Each item in `captured_xhr` is a full `Response` object with the same properties (`.url`, `.status`, `.headers`, `.body`, etc.). When `capture_xhr` is not set or is `None`, `captured_xhr` is an empty list.

### Some Stealth Features[¶](#some-stealth-features "Permanent link")

```
page = DynamicFetcher.fetch(
    'https://example.com',
    google_search=True,
    useragent='Mozilla/5.0...',  # Custom user agent
    locale='en-US',  # Set browser locale
)
```

### General example[¶](#general-example "Permanent link")

```
from scrapling.fetchers import DynamicFetcher

def scrape_dynamic_content():
    # Use Playwright for JavaScript content
    page = DynamicFetcher.fetch(
        'https://example.com/dynamic',
        network_idle=True,
        wait_selector='.content'
    )

    # Extract dynamic content
    content = page.css('.content')

    return {
        'title': content.css('h1::text').get(),
        'items': [
            item.text for item in content.css('.item')
        ]
    }
```

## Session Management[¶](#session-management "Permanent link")

To keep the browser open until you make multiple requests with the same configuration, use `DynamicSession`/`AsyncDynamicSession` classes. Those classes can accept all the arguments that the `fetch` function can take, which enables you to specify a config for the entire session.

```
from scrapling.fetchers import DynamicSession

# Create a session with default configuration
with DynamicSession(
    headless=True,
    disable_resources=True,
    real_chrome=True
) as session:
    # Make multiple requests with the same browser instance
    page1 = session.fetch('https://example1.com')
    page2 = session.fetch('https://example2.com')
    page3 = session.fetch('https://dynamic-site.com')

    # All requests reuse the same tab on the same browser instance
```

### Async Session Usage[¶](#async-session-usage "Permanent link")

```
import asyncio
from scrapling.fetchers import AsyncDynamicSession

async def scrape_multiple_sites():
    async with AsyncDynamicSession(
        network_idle=True,
        timeout=30000,
        max_pages=3
    ) as session:
        # Make async requests with shared browser configuration
        pages = await asyncio.gather(
            session.fetch('https://spa-app1.com'),
            session.fetch('https://spa-app2.com'),
            session.fetch('https://dynamic-content.com')
        )
        return pages
```

You may have noticed the `max_pages` argument. This is a new argument that enables the fetcher to create a **rotating pool of Browser tabs**. Instead of using a single tab for all your requests, you set a limit on the maximum number of pages that can be displayed at once. With each request, the library will close all tabs that have finished their task and check if the number of the current tabs is lower than the maximum allowed number of pages/tabs, then:

1. If you are within the allowed range, the fetcher will create a new tab for you, and then all is as normal.
2. Otherwise, it will keep checking every subsecond if creating a new tab is allowed or not for 60 seconds, then raise `TimeoutError`. This can happen when the website you are fetching becomes unresponsive.

This logic allows for multiple URLs to be fetched at the same time in the same browser, which saves a lot of resources, but most importantly, is so fast :)

In versions 0.3 and 0.3.1, the pool was reusing finished tabs to save more resources/time. That logic proved flawed, as it's nearly impossible to protect pages/tabs from contamination by the previous configuration used in the request before this one.

### Session Benefits[¶](#session-benefits "Permanent link")

* **Browser reuse**: Much faster subsequent requests by reusing the same browser instance.
* **Cookie persistence**: Automatic cookie and session state handling as any browser does automatically.
* **Consistent fingerprint**: Same browser fingerprint across all requests.
* **Memory efficiency**: Better resource usage compared to launching new browsers with each fetch.

## When to Use[¶](#when-to-use "Permanent link")

Use DynamicFetcher when:

* Need browser automation
* Want multiple browser options
* Using a real Chrome browser
* Need custom browser config
* Want a few stealth options

If you want more stealth and control without much config, check out the [StealthyFetcher](stealthy.html).

Was this page helpful?

Thanks for your feedback!

Thanks for your feedback! Help us improve this page by
[opening a documentation issue](https://github.com/D4Vinci/Scrapling/issues/new?template=04-docs_issue.yml).


---
## Source: https://scrapling.readthedocs.io/en/latest/fetching/stealthy.html
---

# Fetching dynamic websites with hard protections[¶](#fetching-dynamic-websites-with-hard-protections "Permanent link")

Here, we will discuss the `StealthyFetcher` class. This class is very similar to the [DynamicFetcher](dynamic.html#introduction) class, including the browsers, the automation, and the use of [Playwright's API](https://playwright.dev/python/docs/intro). The main difference is that this class provides advanced anti-bot protection bypass capabilities; most of them are handled automatically under the hood, and the rest is up to you to enable.

As with [DynamicFetcher](dynamic.html#introduction), you will need some knowledge about [Playwright's Page API](https://playwright.dev/python/docs/api/class-page) to automate the page, as we will explain later.

Prerequisites

1. You've completed or read the [DynamicFetcher](dynamic.html#introduction) page since this class builds upon it, and we won't repeat the same information here for that reason.
2. You've completed or read the [Fetchers basics](../fetching/choosing.html) page to understand what the [Response object](../fetching/choosing.html#response-object) is and which fetcher to use.
3. You've completed or read the [Querying elements](../parsing/selection.html) page to understand how to find/extract elements from the [Selector](../parsing/main_classes.html#selector)/[Response](../fetching/choosing.html#response-object) object.
4. You've completed or read the [Main classes](../parsing/main_classes.html) page to know what properties/methods the [Response](../fetching/choosing.html#response-object) class is inheriting from the [Selector](../parsing/main_classes.html#selector) class.

## Basic Usage[¶](#basic-usage "Permanent link")

You have one primary way to import this Fetcher, which is the same for all fetchers.

```
>>> from scrapling.fetchers import StealthyFetcher
```

Check out how to configure the parsing options [here](choosing.html#parser-configuration-in-all-fetchers)

Abstract

The async version of the `fetch` method is `async_fetch`, of course.

## What does it do?[¶](#what-does-it-do "Permanent link")

The `StealthyFetcher` class is a stealthy version of the [DynamicFetcher](dynamic.html#introduction) class, and here are some of the things it does:

1. It easily bypasses all types of Cloudflare's Turnstile/Interstitial automatically.
2. It bypasses CDP runtime leaks and WebRTC leaks.
3. It isolates JS execution, removes many Playwright fingerprints, and stops detection through some of the known behaviors that bots do.
4. It generates canvas noise to prevent fingerprinting through canvas.
5. It automatically patches known methods to detect running in headless mode and provides an option to defeat timezone mismatch attacks.
6. and other anti-protection options...

## Full list of arguments[¶](#full-list-of-arguments "Permanent link")

Scrapling provides many options with this fetcher and its session classes. Before jumping to the [examples](#examples), here's the full list of arguments

| Argument | Description | Optional |
| --- | --- | --- |
| url | Target url | ❌ |
| headless | Pass `True` to run the browser in headless/hidden (**default**) or `False` for headful/visible mode. | ✔️ |
| disable_resources | Drop requests for unnecessary resources for a speed boost. Requests dropped are of type `font`, `image`, `media`, `beacon`, `object`, `imageset`, `texttrack`, `websocket`, `csp_report`, and `stylesheet`. | ✔️ |
| cookies | Set cookies for the next request. | ✔️ |
| useragent | Pass a useragent string to be used. **Otherwise, the fetcher will generate and use a real Useragent of the same browser and version.** | ✔️ |
| network_idle | Wait for the page until there are no network connections for at least 500 ms. | ✔️ |
| load_dom | Enabled by default, wait for all JavaScript on page(s) to fully load and execute (wait for the `domcontentloaded` state). | ✔️ |
| timeout | The timeout (milliseconds) used in all operations and waits through the page. The default is 30,000 ms (30 seconds). | ✔️ |
| wait | The time (milliseconds) the fetcher will wait after everything finishes before closing the page and returning the `Response` object. | ✔️ |
| page_action | Added for automation. Pass a function that takes the `page` object and does the necessary automation. | ✔️ |
| wait_selector | Wait for a specific css selector to be in a specific state. | ✔️ |
| init_script | An absolute path to a JavaScript file to be executed on page creation for all pages in this session. | ✔️ |
| wait_selector_state | Scrapling will wait for the given state to be fulfilled for the selector given with `wait_selector`. *Default state is `attached`.* | ✔️ |
| google_search | Enabled by default, Scrapling will set a Google referer header. | ✔️ |
| extra_headers | A dictionary of extra headers to add to the request. *The referer set by `google_search` takes priority over the referer set here if used together.* | ✔️ |
| proxy | The proxy to be used with requests. It can be a string or a dictionary with only the keys 'server', 'username', and 'password'. | ✔️ |
| real_chrome | If you have a Chrome browser installed on your device, enable this, and the Fetcher will launch and use an instance of your browser. | ✔️ |
| locale | Specify user locale, for example, `en-GB`, `de-DE`, etc. Locale will affect `navigator.language` value, `Accept-Language` request header value, as well as number and date formatting rules. Defaults to the system default locale. | ✔️ |
| timezone_id | Changes the timezone of the browser. Defaults to the system timezone. | ✔️ |
| cdp_url | Instead of launching a new browser instance, connect to this CDP URL to control real browsers through CDP. | ✔️ |
| user_data_dir | Path to a User Data Directory, which stores browser session data like cookies and local storage. The default is to create a temporary directory. **Only Works with sessions** | ✔️ |
| extra_flags | A list of additional browser flags to pass to the browser on launch. | ✔️ |
| solve_cloudflare | When enabled, fetcher solves all types of Cloudflare's Turnstile/Interstitial challenges before returning the response to you. | ✔️ |
| block_webrtc | Forces WebRTC to respect proxy settings to prevent local IP address leak. | ✔️ |
| hide_canvas | Add random noise to canvas operations to prevent fingerprinting. | ✔️ |
| allow_webgl | Enabled by default. Disabling it disables WebGL and WebGL 2.0 support entirely. Disabling WebGL is not recommended, as many WAFs now check if WebGL is enabled. | ✔️ |
| additional_args | Additional arguments to be passed to Playwright's context as additional settings, and they take higher priority than Scrapling's settings. | ✔️ |
| selector_config | A dictionary of custom parsing arguments to be used when creating the final `Selector`/`Response` class. | ✔️ |
| blocked_domains | A set of domain names to block requests to. Subdomains are also matched (e.g., `"example.com"` blocks `"sub.example.com"` too). | ✔️ |
| proxy_rotator | A `ProxyRotator` instance for automatic proxy rotation. Cannot be combined with `proxy`. | ✔️ |
| retries | Number of retry attempts for failed requests. Defaults to 3. | ✔️ |
| retry_delay | Seconds to wait between retry attempts. Defaults to 1. | ✔️ |
| capture_xhr | Pass a regex URL pattern string to capture XHR/fetch requests matching it during page load. Captured responses are available via `response.captured_xhr`. Defaults to `None` (disabled). | ✔️ |
| executable_path | Absolute path to a custom browser executable to use instead of the bundled Chromium. Useful for non-standard installations or custom browser builds. | ✔️ |

In session classes, all these arguments can be set globally for the session. Still, you can configure each request individually by passing some of the arguments here that can be configured on the browser tab level like: `google_search`, `timeout`, `wait`, `page_action`, `extra_headers`, `disable_resources`, `wait_selector`, `wait_selector_state`, `network_idle`, `load_dom`, `solve_cloudflare`, `blocked_domains`, `proxy`, and `selector_config`.

Notes:

1. It's basically the same arguments as [DynamicFetcher](dynamic.html#introduction) class, but with these additional arguments: `solve_cloudflare`, `block_webrtc`, `hide_canvas`, and `allow_webgl`. The `capture_xhr` argument is shared with `DynamicFetcher`.
2. The `disable_resources` option made requests ~25% faster in my tests for some websites and can help save your proxy usage, but be careful with it, as it can cause some websites to never finish loading.
3. The `google_search` argument is enabled by default for all requests, setting the referer to `https://www.google.com/`. If used together with `extra_headers`, it takes priority over the referer set there.
4. If you didn't set a user agent and enabled headless mode, the fetcher will generate a real user agent for the same browser version and use it. If you didn't set a user agent and didn't enable headless mode, the fetcher will use the browser's default user agent, which is the same as in standard browsers in the latest versions.

## Examples[¶](#examples "Permanent link")

It's easier to understand with examples, so we will now review most of the arguments individually. Since it's the same class as the [DynamicFetcher](dynamic.html#introduction), you can refer to that page for more examples, as we won't repeat all the examples from there.

### Cloudflare and stealth options[¶](#cloudflare-and-stealth-options "Permanent link")

```
# Automatic Cloudflare solver
page = StealthyFetcher.fetch('https://nopecha.com/demo/cloudflare', solve_cloudflare=True)

# Works with other stealth options
page = StealthyFetcher.fetch(
    'https://protected-site.com',
    solve_cloudflare=True,
    block_webrtc=True,
    real_chrome=True,
    hide_canvas=True,
    google_search=True,
    proxy='http://username:password@host:port',  # It can also be a dictionary with only the keys 'server', 'username', and 'password'.
)
```

The `solve_cloudflare` parameter enables automatic detection and solving all types of Cloudflare's Turnstile/Interstitial challenges:

* JavaScript challenges (managed)
* Interactive challenges (clicking verification boxes)
* Invisible challenges (automatic background verification)

And even solves the custom pages with embedded captcha.

**Important notes:**

1. Sometimes, with websites that use custom implementations, you will need to use `wait_selector` to make sure Scrapling waits for the real website content to be loaded after solving the captcha. Some websites can be the real definition of an edge case while we are trying to make the solver as generic as possible.
2. The timeout should be at least 60 seconds when using the Cloudflare solver for sufficient challenge-solving time.
3. This feature works seamlessly with proxies and other stealth options.

### Browser Automation[¶](#browser-automation "Permanent link")

This is where your knowledge about [Playwright's Page API](https://playwright.dev/python/docs/api/class-page) comes into play. The function you pass here takes the page object from Playwright's API, performs the desired action, and then the fetcher continues.

This function is executed immediately after waiting for `network_idle` (if enabled) and before waiting for the `wait_selector` argument, allowing it to be used for purposes beyond automation. You can alter the page as you want.

In the example below, I used the pages' [mouse events](https://playwright.dev/python/docs/api/class-mouse) to scroll the page with the mouse wheel, then move the mouse.

```
from playwright.sync_api import Page

def scroll_page(page: Page):
    page.mouse.wheel(10, 0)
    page.mouse.move(100, 400)
    page.mouse.up()

page = StealthyFetcher.fetch('https://example.com', page_action=scroll_page)
```

Of course, if you use the async fetch version, the function must also be async.

```
from playwright.async_api import Page

async def scroll_page(page: Page):
   await page.mouse.wheel(10, 0)
   await page.mouse.move(100, 400)
   await page.mouse.up()

page = await StealthyFetcher.async_fetch('https://example.com', page_action=scroll_page)
```

### Wait Conditions[¶](#wait-conditions "Permanent link")

```
# Wait for the selector
page = StealthyFetcher.fetch(
    'https://example.com',
    wait_selector='h1',
    wait_selector_state='visible'
)
```

This is the last wait the fetcher will do before returning the response (if enabled). You pass a CSS selector to the `wait_selector` argument, and the fetcher will wait for the state you passed in the `wait_selector_state` argument to be fulfilled. If you didn't pass a state, the default would be `attached`, which means it will wait for the element to be present in the DOM.

After that, if `load_dom` is enabled (the default), the fetcher will check again to see if all JavaScript files are loaded and executed (in the `domcontentloaded` state) or continue waiting. If you have enabled `network_idle`, the fetcher will wait for `network_idle` to be fulfilled again, as explained above.

The states the fetcher can wait for can be any of the following ([source](https://playwright.dev/python/docs/api/class-page#page-wait-for-selector)):

* `attached`: Wait for an element to be present in the DOM.
* `detached`: Wait for an element to not be present in the DOM.
* `visible`: wait for an element to have a non-empty bounding box and no `visibility:hidden`. Note that an element without any content or with `display:none` has an empty bounding box and is not considered visible.
* `hidden`: wait for an element to be either detached from the DOM, or have an empty bounding box, or `visibility:hidden`. This is opposite to the `'visible'` option.

### Real-world example (Amazon)[¶](#real-world-example-amazon "Permanent link")

This is for educational purposes only; this example was generated by AI, which also shows how easy it is to work with Scrapling through AI

```
def scrape_amazon_product(url):
    # Use StealthyFetcher to bypass protection
    page = StealthyFetcher.fetch(url)

    # Extract product details
    return {
        'title': page.css('#productTitle::text').get().clean(),
        'price': page.css('.a-price .a-offscreen::text').get(),
        'rating': page.css('[data-feature-name="averageCustomerReviews"] .a-popover-trigger .a-color-base::text').get(),
        'reviews_count': page.css('#acrCustomerReviewText::text').re_first(r'[\d,]+'),
        'features': [
            li.get().clean() for li in page.css('#feature-bullets li span::text')
        ],
        'availability': page.css('#availability')[0].get_all_text(strip=True),
        'images': [
            img.attrib['src'] for img in page.css('#altImages img')
        ]
    }
```

## Session Management[¶](#session-management "Permanent link")

To keep the browser open until you make multiple requests with the same configuration, use `StealthySession`/`AsyncStealthySession` classes. Those classes can accept all the arguments that the `fetch` function can take, which enables you to specify a config for the entire session.

```
from scrapling.fetchers import StealthySession

# Create a session with default configuration
with StealthySession(
    headless=True,
    real_chrome=True,
    block_webrtc=True,
    solve_cloudflare=True
) as session:
    # Make multiple requests with the same browser instance
    page1 = session.fetch('https://example1.com')
    page2 = session.fetch('https://example2.com') 
    page3 = session.fetch('https://nopecha.com/demo/cloudflare')

    # All requests reuse the same tab on the same browser instance
```

### Async Session Usage[¶](#async-session-usage "Permanent link")

```
import asyncio
from scrapling.fetchers import AsyncStealthySession

async def scrape_multiple_sites():
    async with AsyncStealthySession(
        real_chrome=True,
        block_webrtc=True,
        solve_cloudflare=True,
        timeout=60000,  # 60 seconds for Cloudflare challenges
        max_pages=3
    ) as session:
        # Make async requests with shared browser configuration
        pages = await asyncio.gather(
            session.fetch('https://site1.com'),
            session.fetch('https://site2.com'), 
            session.fetch('https://protected-site.com')
        )
        return pages
```

You may have noticed the `max_pages` argument. This is a new argument that enables the fetcher to create a **rotating pool of Browser tabs**. Instead of using a single tab for all your requests, you set a limit on the maximum number of pages that can be displayed at once. With each request, the library will close all tabs that have finished their task and check if the number of the current tabs is lower than the maximum allowed number of pages/tabs, then:

1. If you are within the allowed range, the fetcher will create a new tab for you, and then all is as normal.
2. Otherwise, it will keep checking every subsecond if creating a new tab is allowed or not for 60 seconds, then raise `TimeoutError`. This can happen when the website you are fetching becomes unresponsive.

This logic allows for multiple URLs to be fetched at the same time in the same browser, which saves a lot of resources, but most importantly, is so fast :)

In versions 0.3 and 0.3.1, the pool was reusing finished tabs to save more resources/time. That logic proved flawed, as it's nearly impossible to protect pages/tabs from contamination by the previous configuration used in the request before this one.

### Session Benefits[¶](#session-benefits "Permanent link")

* **Browser reuse**: Much faster subsequent requests by reusing the same browser instance.
* **Cookie persistence**: Automatic cookie and session state handling as any browser does automatically.
* **Consistent fingerprint**: Same browser fingerprint across all requests.
* **Memory efficiency**: Better resource usage compared to launching new browsers with each fetch.

## Using Camoufox as an engine[¶](#using-camoufox-as-an-engine "Permanent link")

This fetcher used a custom version of [Camoufox](https://github.com/daijro/camoufox) as an engine before version 0.3.13, which was replaced by [patchright](https://github.com/Kaliiiiiiiiii-Vinyzu/patchright) for many reasons. If you see that Camoufox is stable on your device, has no high memory issues, and you want to continue using it, then you can.

First, you will need to install the Camoufox library, browser, and Firefox system dependencies if you didn't already:

```
pip install camoufox
playwright install-deps firefox
camoufox fetch
```

Then you will inherit from `StealthySession` and set it as below:

```
from scrapling.fetchers import StealthySession
from playwright.sync_api import sync_playwright
from camoufox.utils import launch_options as generate_launch_options

class StealthySession(StealthySession):
    def start(self):
        """Create a browser for this instance and context."""
        if not self.playwright:
            self.playwright = sync_playwright().start()
            # Configure camoufox run options here
            launch_options = generate_launch_options(**{"headless": True, "user_data_dir": ''})
            # Here's an example, part of what we have been doing before v0.3.13
            launch_options = generate_launch_options(**{
                "geoip": False,
                "proxy": self._config.proxy,
                "headless": self._config.headless,
                "humanize": True if self._config.solve_cloudflare else False,  # Better enable humanize for Cloudflare, otherwise it's up to you
                "i_know_what_im_doing": True,  # To turn warnings off with the user configurations
                "allow_webgl": self._config.allow_webgl,
                "block_webrtc": self._config.block_webrtc,
                "os": None,
                "user_data_dir": self._config.user_data_dir,
                "firefox_user_prefs": {
                    # This is what enabling `enable_cache` does internally, so we do it from here instead
                    "browser.sessionhistory.max_entries": 10,
                    "browser.sessionhistory.max_total_viewers": -1,
                    "browser.cache.memory.enable": True,
                    "browser.cache.disk_cache_ssl": True,
                    "browser.cache.disk.smart_size.enabled": True,
                },
                # etc...
            })
            self.context = self.playwright.firefox.launch_persistent_context(**launch_options)
        else:
            raise RuntimeError("Session has been already started")
```

After that, you can use it normally as before, even for solving Cloudflare challenges:

```
with StealthySession(solve_cloudflare=True, headless=True) as session:
    page = session.fetch('https://sergiodemo.com/security/challenge/legacy-challenge')
    if page.css('#page-not-found-404'):
        print('Cloudflare challenge solved successfully!')
```

The same logic applies to the `AsyncStealthySession` class with a few differences:

```
from scrapling.fetchers import AsyncStealthySession
from playwright.async_api import async_playwright
from camoufox.utils import launch_options as generate_launch_options

class AsyncStealthySession(AsyncStealthySession):
    async def start(self):
        """Create a browser for this instance and context."""
        if not self.playwright:
            self.playwright = await async_playwright().start()
            # Configure camoufox run options here
            launch_options = generate_launch_options(**{"headless": True, "user_data_dir": ''})
            # or set the launch options as in the above example
            self.context = await self.playwright.firefox.launch_persistent_context(**launch_options)
        else:
            raise RuntimeError("Session has been already started")

async with AsyncStealthySession(solve_cloudflare=True, headless=True) as session:
    page = await session.fetch('https://sergiodemo.com/security/challenge/legacy-challenge')
    if page.css('#page-not-found-404'):
        print('Cloudflare challenge solved successfully!')
```

Enjoy! :)

## When to Use[¶](#when-to-use "Permanent link")

Use StealthyFetcher when:

* Bypassing anti-bot protection
* Need a reliable browser fingerprint
* Full JavaScript support needed
* Want automatic stealth features
* Need browser automation
* Dealing with Cloudflare protection

Was this page helpful?

Thanks for your feedback!

Thanks for your feedback! Help us improve this page by
[opening a documentation issue](https://github.com/D4Vinci/Scrapling/issues/new?template=04-docs_issue.yml).


---
## Source: https://scrapling.readthedocs.io/en/latest/spiders/architecture.html
---

# Spiders architecture[¶](#spiders-architecture "Permanent link")

Prerequisites

1. You've completed or read the [Fetchers basics](../fetching/choosing.html) page to understand the different fetcher types and when to use each one.
2. You've completed or read the [Main classes](../parsing/main_classes.html) page to understand the [Selector](../parsing/main_classes.html#selector) and [Response](../fetching/choosing.html#response-object) classes.

Scrapling's spider system is a Scrapy-inspired async crawling framework designed for concurrent, multi-session crawls with built-in pause/resume support. It brings together Scrapling's parsing engine and fetchers into a unified crawling API while adding scheduling, concurrency control, and checkpointing.

If you're familiar with Scrapy, you'll feel right at home. If not, don't worry - the system is designed to be straightforward.

## Data Flow[¶](#data-flow "Permanent link")

The diagram below shows how data flows through the spider system when a crawl is running:

![Spider architecture diagram by @TrueSkills](../assets/spider_architecture.png "Spider architecture diagram by @TrueSkills")

Here's what happens step by step when you run a spider without many details:

1. The **Spider** produces the first batch of `Request` objects. By default, it creates one request for each URL in `start_urls`, but you can override `start_requests()` for custom logic.
2. The **Scheduler** receives requests and places them in a priority queue, and creates fingerprints for them. Higher-priority requests are dequeued first.
3. The **Crawler Engine** asks the **Scheduler** to dequeue the next request, respecting concurrency limits (global and per-domain) and download delays. Once the **Crawler Engine** receives the request, it passes it to the **Session Manager**, which routes it to the correct session based on the request's `sid` (session ID).
4. The **session** fetches the page and returns a [Response](../fetching/choosing.html#response-object) object to the **Crawler Engine**. The engine records statistics and checks for blocked responses. If the response is blocked, the engine retries the request up to `max_blocked_retries` times. Of course, the blocking detection and the retry logic for blocked requests can be customized.
5. The **Crawler Engine** passes the [Response](../fetching/choosing.html#response-object) to the request's callback. The callback either yields a dictionary, which gets treated as a scraped item, or a follow-up request, which gets sent to the scheduler for queuing.
6. The cycle repeats from step 2 until the scheduler is empty and no tasks are active, or the spider is paused.
7. If `crawldir` is set while starting the spider, the **Crawler Engine** periodically saves a checkpoint (pending requests + seen URLs set) to disk. On graceful shutdown (Ctrl+C), a final checkpoint is saved. The next time the spider runs with the same `crawldir`, it resumes from where it left off, skipping `start_requests()` and restoring the scheduler state.

## Components[¶](#components "Permanent link")

### Spider[¶](#spider "Permanent link")

The central class you interact with. You subclass `Spider`, define your `start_urls` and `parse()` method, and optionally configure sessions and override lifecycle hooks.

```
from scrapling.spiders import Spider, Response, Request

class MySpider(Spider):
    name = "my_spider"
    start_urls = ["https://example.com"]

    async def parse(self, response: Response):
        for link in response.css("a::attr(href)").getall():
            yield response.follow(link, callback=self.parse_page)

    async def parse_page(self, response: Response):
        yield {"title": response.css("h1::text").get("")}
```

### Crawler Engine[¶](#crawler-engine "Permanent link")

The engine orchestrates the entire crawl. It manages the main loop, enforces concurrency limits, dispatches requests through the Session Manager, and processes results from callbacks. You don't interact with it directly - the `Spider.start()` and `Spider.stream()` methods handle it for you.

### Scheduler[¶](#scheduler "Permanent link")

A priority queue with built-in URL deduplication. Requests are fingerprinted based on their URL, HTTP method, body, and session ID. The scheduler supports `snapshot()` and `restore()` for the checkpoint system, allowing the crawl state to be saved and resumed.

### Session Manager[¶](#session-manager "Permanent link")

Manages one or more named session instances. Each session is one of:

* [FetcherSession](../fetching/static.html)
* [AsyncDynamicSession](../fetching/dynamic.html)
* [AsyncStealthySession](../fetching/stealthy.html)

When a request comes in, the Session Manager routes it to the correct session based on the request's `sid` field. Sessions can be started with the spider start (default) or lazily (started on the first use).

### Checkpoint System[¶](#checkpoint-system "Permanent link")

An optional system that, if enabled, saves the crawler's state (pending requests + seen URL fingerprints) to a pickle file on disk. Writes are atomic (temp file + rename) to prevent corruption. Checkpoints are saved periodically at a configurable interval and on graceful shutdown. Upon successful completion (not paused), checkpoint files are automatically cleaned up.

### Output[¶](#output "Permanent link")

Scraped items are collected in an `ItemList` (a list subclass with `to_json()` and `to_jsonl()` export methods). Crawl statistics are tracked in a `CrawlStats` dataclass which contains a lot of useful info.

## Comparison with Scrapy[¶](#comparison-with-scrapy "Permanent link")

If you're coming from Scrapy, here's how Scrapling's spider system maps:

| Concept | Scrapy | Scrapling |
| --- | --- | --- |
| Spider definition | `scrapy.Spider` subclass | `scrapling.spiders.Spider` subclass |
| Initial requests | `start_requests()` | `async start_requests()` |
| Callbacks | `def parse(self, response)` | `async def parse(self, response)` |
| Following links | `response.follow(url)` | `response.follow(url)` |
| Item output | `yield dict` or `yield Item` | `yield dict` |
| Request scheduling | Scheduler + Dupefilter | Scheduler with built-in deduplication |
| Downloading | Downloader + Middlewares | Session Manager with multi-session support |
| Item processing | Item Pipelines | `on_scraped_item()` hook |
| Blocked detection | Through custom middlewares | Built-in `is_blocked()` + `retry_blocked_request()` hooks |
| Concurrency | `CONCURRENT_REQUESTS` setting | `concurrent_requests` class attribute |
| Domain filtering | `allowed_domains` | `allowed_domains` |
| Pause/Resume | `JOBDIR` setting | `crawldir` constructor argument |
| Export | Feed exports | `result.items.to_json()` / `to_jsonl()` or custom through hooks |
| Running | `scrapy crawl spider_name` | `MySpider().start()` |
| Streaming | N/A | `async for item in spider.stream()` |
| Multi-session | N/A | Multiple sessions with different types per spider |

Was this page helpful?

Thanks for your feedback!

Thanks for your feedback! Help us improve this page by
[opening a documentation issue](https://github.com/D4Vinci/Scrapling/issues/new?template=04-docs_issue.yml).


---
## Source: https://scrapling.readthedocs.io/en/latest/spiders/getting-started.html
---

# Getting started[¶](#getting-started "Permanent link")

## Introduction[¶](#introduction "Permanent link")

Prerequisites

1. You've completed or read the [Fetchers basics](../fetching/choosing.html) page to understand the different fetcher types and when to use each one.
2. You've completed or read the [Main classes](../parsing/main_classes.html) page to understand the [Selector](../parsing/main_classes.html#selector) and [Response](../fetching/choosing.html#response-object) classes.
3. You've read the [Architecture](architecture.html) page for a high-level overview of how the spider system works.

The spider system lets you build concurrent, multi-page crawlers in just a few lines of code. If you've used Scrapy before, the patterns will feel familiar. If not, this guide will walk you through everything you need to get started.

## Your First Spider[¶](#your-first-spider "Permanent link")

A spider is a class that defines how to crawl and extract data from websites. Here's the simplest possible spider:

```
from scrapling.spiders import Spider, Response

class QuotesSpider(Spider):
    name = "quotes"
    start_urls = ["https://quotes.toscrape.com"]

    async def parse(self, response: Response):
        for quote in response.css("div.quote"):
            yield {
                "text": quote.css("span.text::text").get(""),
                "author": quote.css("small.author::text").get(""),
            }
```

Every spider needs three things:

1. **`name`** - A unique identifier for the spider.
2. **`start_urls`** - A list of URLs to start crawling from.
3. **`parse()`** - An async generator method that processes each response and yields results.

The `parse()` method is where the magic happens. You use the same selection methods you'd use with Scrapling's [Selector](../parsing/main_classes.html#selector)/[Response](../fetching/choosing.html#response-object), and `yield` dictionaries to output scraped items.

## Running the Spider[¶](#running-the-spider "Permanent link")

To run your spider, create an instance and call `start()`:

```
result = QuotesSpider().start()
```

The `start()` method handles all the async machinery internally, so no need to worry about event loops. While the spider is running, everything that happens is logged to the terminal, and at the end of the crawl, you get very detailed stats.

Those stats are in the returned `CrawlResult` object, which gives you everything you need:

```
result = QuotesSpider().start()

# Access scraped items
for item in result.items:
    print(item["text"], "-", item["author"])

# Check statistics
print(f"Scraped {result.stats.items_scraped} items")
print(f"Made {result.stats.requests_count} requests")
print(f"Took {result.stats.elapsed_seconds:.1f} seconds")

# Did the crawl finish or was it paused?
print(f"Completed: {result.completed}")
```

## Following Links[¶](#following-links "Permanent link")

Most crawls need to follow links across multiple pages. Use `response.follow()` to create follow-up requests:

```
from scrapling.spiders import Spider, Response

class QuotesSpider(Spider):
    name = "quotes"
    start_urls = ["https://quotes.toscrape.com"]

    async def parse(self, response: Response):
        # Extract items from the current page
        for quote in response.css("div.quote"):
            yield {
                "text": quote.css("span.text::text").get(""),
                "author": quote.css("small.author::text").get(""),
            }

        # Follow the "next page" link
        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
```

`response.follow()` handles relative URLs automatically by joining them with the current page's URL. It also sets the current page as the `Referer` header by default.

You can point follow-up requests at different callback methods for different page types:

```
async def parse(self, response: Response):
    for link in response.css("a.product-link::attr(href)").getall():
        yield response.follow(link, callback=self.parse_product)

async def parse_product(self, response: Response):
    yield {
        "name": response.css("h1::text").get(""),
        "price": response.css(".price::text").get(""),
    }
```

Note

All callback methods must be async generators (using `async def` and `yield`).

## Exporting Data[¶](#exporting-data "Permanent link")

The `ItemList` returned in `result.items` has built-in export methods:

```
result = QuotesSpider().start()

# Export as JSON
result.items.to_json("quotes.json")

# Export as JSON with pretty-printing
result.items.to_json("quotes.json", indent=True)

# Export as JSON Lines (one JSON object per line)
result.items.to_jsonl("quotes.jsonl")
```

Both methods create parent directories automatically if they don't exist.

## Filtering Domains[¶](#filtering-domains "Permanent link")

Use `allowed_domains` to restrict the spider to specific domains. This prevents it from accidentally following links to external websites:

```
class MySpider(Spider):
    name = "my_spider"
    start_urls = ["https://example.com"]
    allowed_domains = {"example.com"}

    async def parse(self, response: Response):
        for link in response.css("a::attr(href)").getall():
            # Links to other domains are silently dropped
            yield response.follow(link, callback=self.parse)
```

Subdomains are matched automatically, so setting `allowed_domains = {"example.com"}` also allows `sub.example.com`, `blog.example.com`, etc.

When a request is filtered out, it's counted in `stats.offsite_requests_count` so you can see how many were dropped.

## What's Next[¶](#whats-next "Permanent link")

Now that you have the basics, you can explore:

* [Requests & Responses](requests-responses.html) - learn about request priority, deduplication, metadata, and more.
* [Sessions](sessions.html) - use multiple fetcher types (HTTP, browser, stealth) in a single spider.
* [Proxy management & blocking](proxy-blocking.html) - rotate proxies across requests and how to handle blocking in the spider.
* [Advanced features](advanced.html) - concurrency control, pause/resume, streaming, lifecycle hooks, and logging.

Was this page helpful?

Thanks for your feedback!

Thanks for your feedback! Help us improve this page by
[opening a documentation issue](https://github.com/D4Vinci/Scrapling/issues/new?template=04-docs_issue.yml).


---
## Source: https://scrapling.readthedocs.io/en/latest/spiders/requests-responses.html
---

# Requests & Responses[¶](#requests-responses "Permanent link")

Prerequisites

1. You've read the [Getting started](getting-started.html) page and know how to create and run a basic spider.

This page covers the `Request` object in detail: how to construct requests, pass data between callbacks, control priority and deduplication, and use `response.follow()` for link-following.

## The Request Object[¶](#the-request-object "Permanent link")

A `Request` represents a URL to be fetched. You create requests either directly or via `response.follow()`:

```
from scrapling.spiders import Request

# Direct construction
request = Request(
    "https://example.com/page",
    callback=self.parse_page,
    priority=5,
)

# Via response.follow (preferred in callbacks)
request = response.follow("/page", callback=self.parse_page)
```

Here are all the arguments you can pass to `Request`:

| Argument | Type | Default | Description |
| --- | --- | --- | --- |
| `url` | `str` | *required* | The URL to fetch |
| `sid` | `str` | `""` | Session ID - routes the request to a specific session (see [Sessions](sessions.html)) |
| `callback` | `callable` | `None` | Async generator method to process the response. Defaults to `parse()` |
| `priority` | `int` | `0` | Higher values are processed first |
| `dont_filter` | `bool` | `False` | If `True`, skip deduplication (allow duplicate requests) |
| `meta` | `dict` | `{}` | Arbitrary metadata passed through to the response |
| `**kwargs` |  |  | Additional keyword arguments passed to the session's fetch method (e.g., `headers`, `method`, `data`) |

Any extra keyword arguments are forwarded directly to the underlying session. For example, to make a POST request:

```
yield Request(
    "https://example.com/api",
    method="POST",
    data={"key": "value"},
    callback=self.parse_result,
)
```

## Response.follow()[¶](#responsefollow "Permanent link")

`response.follow()` is the recommended way to create follow-up requests inside callbacks. It offers several advantages over constructing `Request` objects directly:

* **Relative URLs** are resolved automatically against the current page URL
* **Referer header** is set to the current page URL by default
* **Session kwargs** from the original request are inherited (headers, proxy settings, etc.)
* **Callback, session ID, and priority** are inherited from the original request if not specified

```
async def parse(self, response: Response):
    # Minimal - inherits callback, sid, priority from current request
    yield response.follow("/next-page")

    # Override specific fields
    yield response.follow(
        "/product/123",
        callback=self.parse_product,
        priority=10,
    )

    # Pass additional metadata to
    yield response.follow(
        "/details",
        callback=self.parse_details,
        meta={"category": "electronics"},
    )
```

| Argument | Type | Default | Description |
| --- | --- | --- | --- |
| `url` | `str` | *required* | URL to follow (absolute or relative) |
| `sid` | `str` | `""` | Session ID (inherits from original request if empty) |
| `callback` | `callable` | `None` | Callback method (inherits from original request if `None`) |
| `priority` | `int` | `None` | Priority (inherits from original request if `None`) |
| `dont_filter` | `bool` | `False` | Skip deduplication |
| `meta` | `dict` | `None` | Metadata (merged with existing response meta) |
| **`referer_flow`** | `bool` | `True` | Set current URL as Referer header |
| `**kwargs` |  |  | Merged with original request's session kwargs |

### Disabling Referer Flow[¶](#disabling-referer-flow "Permanent link")

By default, `response.follow()` sets the `Referer` header to the current page URL. To disable this:

```
yield response.follow("/page", referer_flow=False)
```

## Callbacks[¶](#callbacks "Permanent link")

Callbacks are async generator methods on your spider that process responses. They must `yield` one of three types:

* **`dict`** - A scraped item, added to the results
* **`Request`** - A follow-up request, added to the queue
* **`None`** - Silently ignored

```
class MySpider(Spider):
    name = "my_spider"
    start_urls = ["https://example.com"]

    async def parse(self, response: Response):
        # Yield items (dicts)
        yield {"url": response.url, "title": response.css("title::text").get("")}

        # Yield follow-up requests
        for link in response.css("a::attr(href)").getall():
            yield response.follow(link, callback=self.parse_page)

    async def parse_page(self, response: Response):
        yield {"content": response.css("article::text").get("")}
```

Note:

All callback methods must be `async def` and use `yield` (not `return`). Even if a callback only yields items with no follow-up requests, it must still be an async generator.

## Request Priority[¶](#request-priority "Permanent link")

Requests with higher priority values are processed first. This is useful when some pages are more important to be processed first before others:

```
async def parse(self, response: Response):
    # High priority - process product pages first
    for link in response.css("a.product::attr(href)").getall():
        yield response.follow(link, callback=self.parse_product, priority=10)

    # Low priority - pagination links processed after products
    next_page = response.css("a.next::attr(href)").get()
    if next_page:
        yield response.follow(next_page, callback=self.parse, priority=0)
```

When using `response.follow()`, the priority is inherited from the original request unless you specify a new one.

## Deduplication[¶](#deduplication "Permanent link")

The spider automatically deduplicates requests based on a fingerprint computed from the URL, HTTP method, request body, and session ID. If two requests produce the same fingerprint, the second one is silently dropped.

To allow duplicate requests (e.g., re-visiting a page after login), set `dont_filter=True`:

```
yield Request("https://example.com/dashboard", dont_filter=True, callback=self.parse_dashboard)

# Or with response.follow
yield response.follow("/dashboard", dont_filter=True, callback=self.parse_dashboard)
```

You can fine-tune what goes into the fingerprint using class attributes on your spider:

| Attribute | Default | Effect |
| --- | --- | --- |
| `fp_include_kwargs` | `False` | Include extra request kwargs (arguments you passed to the session fetch, like headers, etc.) in the fingerprint |
| `fp_keep_fragments` | `False` | Keep URL fragments (`#section`) when computing fingerprints |
| `fp_include_headers` | `False` | Include request headers in the fingerprint |

For example, if you need to treat `https://example.com/page#section1` and `https://example.com/page#section2` as different URLs:

```
class MySpider(Spider):
    name = "my_spider"
    fp_keep_fragments = True
    # ...
```

## Request Meta[¶](#request-meta "Permanent link")

The `meta` dictionary lets you pass arbitrary data between callbacks. This is useful when you need context from one page to process another:

```
async def parse(self, response: Response):
    for product in response.css("div.product"):
        category = product.css("span.category::text").get("")
        link = product.css("a::attr(href)").get()
        if link:
            yield response.follow(
                link,
                callback=self.parse_product,
                meta={"category": category},
            )

async def parse_product(self, response: Response):
    yield {
        "name": response.css("h1::text").get(""),
        "price": response.css(".price::text").get(""),
        # Access meta from the request
        "category": response.meta.get("category", ""),
    }
```

When using `response.follow()`, the meta from the current response is merged with the new meta you provide (new values take precedence).

The spider system also automatically stores some metadata. For example, the proxy used for a request is available as `response.meta["proxy"]` when proxy rotation is enabled.

Was this page helpful?

Thanks for your feedback!

Thanks for your feedback! Help us improve this page by
[opening a documentation issue](https://github.com/D4Vinci/Scrapling/issues/new?template=04-docs_issue.yml).


---
## Source: https://scrapling.readthedocs.io/en/latest/spiders/sessions.html
---

# Spiders sessions[¶](#spiders-sessions "Permanent link")

Prerequisites

1. You've read the [Getting started](getting-started.html) page and know how to create and run a basic spider.
2. You're familiar with [Fetchers basics](../fetching/choosing.html) and the differences between HTTP, Dynamic, and Stealthy sessions.

A spider can use multiple fetcher sessions simultaneously. For example, a fast HTTP session for simple pages and a stealth browser session for protected pages. This page shows you how to configure and use sessions.

## What are Sessions?[¶](#what-are-sessions "Permanent link")

As you should already know, a session is a pre-configured fetcher instance that stays alive for the duration of the crawl. Instead of creating a new connection or browser for every request, the spider reuses sessions, which is faster and more resource-efficient.

By default, every spider creates a single [FetcherSession](../fetching/static.html). You can add more sessions or swap the default by overriding the `configure_sessions()` method, but you have to use the async version of each session only, as the table shows below:

| Session Type | Use Case |
| --- | --- |
| [FetcherSession](../fetching/static.html) | Fast HTTP requests, no JavaScript |
| [AsyncDynamicSession](../fetching/dynamic.html) | Browser automation, JavaScript rendering |
| [AsyncStealthySession](../fetching/stealthy.html) | Anti-bot bypass, Cloudflare, etc. |

## Configuring Sessions[¶](#configuring-sessions "Permanent link")

Override `configure_sessions()` on your spider to set up sessions. The `manager` parameter is a `SessionManager` instance. Use `manager.add()` to register sessions:

```
from scrapling.spiders import Spider, Response
from scrapling.fetchers import FetcherSession

class MySpider(Spider):
    name = "my_spider"
    start_urls = ["https://example.com"]

    def configure_sessions(self, manager):
        manager.add("default", FetcherSession())

    async def parse(self, response: Response):
        yield {"title": response.css("title::text").get("")}
```

The `manager.add()` method takes:

| Argument | Type | Default | Description |
| --- | --- | --- | --- |
| `session_id` | `str` | *required* | A name to reference this session in requests |
| `session` | `Session` | *required* | The session instance |
| `default` | `bool` | `False` | Make this the default session |
| `lazy` | `bool` | `False` | Start the session only when first used |

Notes:

1. In all requests, if you don't specify which session to use, the default session is used. The default session is determined in one of two ways:
   1. The first session you add to the managed becomes the default automatically.
   2. The session that gets `default=True` while added to the manager.
2. The instances you pass of each session don't have to be already started by you; the spider checks on all sessions if they are not already started and starts them.
3. If you want a specific session to start when used only, then use the `lazy` argument while adding that session to the manager. Example: start the browser only when you need it, not with the spider start.

## Multi-Session Spider[¶](#multi-session-spider "Permanent link")

Here's a practical example: use a fast HTTP session for listing pages and a stealth browser for detail pages that have bot protection:

```
from scrapling.spiders import Spider, Response
from scrapling.fetchers import FetcherSession, AsyncStealthySession

class ProductSpider(Spider):
    name = "products"
    start_urls = ["https://shop.example.com/products"]

    def configure_sessions(self, manager):
        # Fast HTTP for listing pages (default)
        manager.add("http", FetcherSession())

        # Stealth browser for protected product pages
        # capture_xhr captures background API calls matching the regex
        manager.add("stealth", AsyncStealthySession(
            headless=True,
            network_idle=True,
            capture_xhr=r"https://api\.shop\.example\.com/.*",
        ))

    async def parse(self, response: Response):
        for link in response.css("a.product::attr(href)").getall():
            # Route product pages through the stealth session
            yield response.follow(link, sid="stealth", callback=self.parse_product)

        next_page = response.css("a.next::attr(href)").get()
        if next_page:
            yield response.follow(next_page)

    async def parse_product(self, response: Response):
        # Access captured XHR/fetch API calls (if capture_xhr was set on the session)
        for xhr in response.captured_xhr:
            self.logger.info(f"Captured API call: {xhr.url} ({xhr.status})")

        yield {
            "name": response.css("h1::text").get(""),
            "price": response.css(".price::text").get(""),
        }
```

The key is the `sid` parameter - it tells the spider which session to use for each request. When you call `response.follow()` without `sid`, the session ID from the original request is inherited.

Note that the sessions don't have to be from different classes only, but can be the same session, but different instances with different configurations, for example, like below:

```
from scrapling.spiders import Spider, Response
from scrapling.fetchers import FetcherSession

class ProductSpider(Spider):
    name = "products"
    start_urls = ["https://shop.example.com/products"]

    def configure_sessions(self, manager):
        chrome_requests = FetcherSession(impersonate="chrome")
        firefox_requests = FetcherSession(impersonate="firefox")

        manager.add("chrome", chrome_requests)
        manager.add("firefox", firefox_requests)

    async def parse(self, response: Response):
        for link in response.css("a.product::attr(href)").getall():
            yield response.follow(link, callback=self.parse_product)

        next_page = response.css("a.next::attr(href)").get()
        if next_page:
            yield response.follow(next_page, sid="firefox")

    async def parse_product(self, response: Response):
        yield {
            "name": response.css("h1::text").get(""),
            "price": response.css(".price::text").get(""),
        }
```

Or you can separate concerns and keep a session with its cookies/state for specific requests, etc...

## Session Arguments[¶](#session-arguments "Permanent link")

Extra keyword arguments passed to a `Request` (or through `response.follow(**kwargs)`) are forwarded to the session's fetch method. This lets you customize individual requests without changing the session configuration:

```
async def parse(self, response: Response):
    # Pass extra headers for this specific request
    yield Request(
        "https://api.example.com/data",
        headers={"Authorization": "Bearer token123"},
        callback=self.parse_api,
    )

    # Use a different HTTP method
    yield Request(
        "https://example.com/submit",
        method="POST",
        data={"field": "value"},
        sid="firefox",
        callback=self.parse_result,
    )
```

Warning

Normally, when you use `FetcherSession`, `Fetcher`, or `AsyncFetcher`, you specify the HTTP method to use with the corresponding method like `.get()` and `.post()`. But while using `FetcherSession` in spiders, you can't do this. By default, the request is an *HTTP GET* request; if you want to use another HTTP method, you have to pass it to the `method` argument, as in the above example. The reason for this is to unify the `Request` interface across all session types.

For browser sessions (`AsyncDynamicSession`, `AsyncStealthySession`), you can pass browser-specific arguments like `wait_selector`, `page_action`, or `extra_headers`:

```
async def parse(self, response: Response):
    # Use Cloudflare solver with the `AsyncStealthySession` we configured above
    yield Request(
        "https://nopecha.com/demo/cloudflare",
        sid="stealth",
        callback=self.parse_result,
        solve_cloudflare=True,
        block_webrtc=True,
        hide_canvas=True,
        google_search=True,
    )

    yield response.follow(
        "/dynamic-page",
        sid="browser",
        callback=self.parse_dynamic,
        wait_selector="div.loaded",
        network_idle=True,
    )
```

Warning

Session arguments (**kwargs) passed from the original request are inherited by `response.follow()`. New kwargs take precedence over inherited ones.

```
from scrapling.spiders import Spider, Response
from scrapling.fetchers import FetcherSession

class ProductSpider(Spider):
    name = "products"
    start_urls = ["https://shop.example.com/products"]

    def configure_sessions(self, manager):
        manager.add("http", FetcherSession(impersonate='chrome'))

    async def parse(self, response: Response):
        # I don't want the follow request to impersonate a desktop Chrome like the previous request, but a mobile one
        # so I override it like this
        for link in response.css("a.product::attr(href)").getall():
            yield response.follow(link, impersonate="chrome131_android", callback=self.parse_product)

        next_page = response.css("a.next::attr(href)").get()
        if next_page:
            yield Request(next_page)

    async def parse_product(self, response: Response):
        yield {
            "name": response.css("h1::text").get(""),
            "price": response.css(".price::text").get(""),
        }
```

Info

No need to mention that, upon spider closure, the manager automatically checks whether any sessions are still running and closes them before closing the spider.

Was this page helpful?

Thanks for your feedback!

Thanks for your feedback! Help us improve this page by
[opening a documentation issue](https://github.com/D4Vinci/Scrapling/issues/new?template=04-docs_issue.yml).


---
## Source: https://scrapling.readthedocs.io/en/latest/spiders/proxy-blocking.html
---

# Proxy management and handling Blocks[¶](#proxy-management-and-handling-blocks "Permanent link")

## Introduction[¶](#introduction "Permanent link")

Prerequisites

1. You've read the [Getting started](getting-started.html) page and know how to create and run a basic spider.
2. You've read the [Sessions](sessions.html) page and understand how to configure sessions.

When scraping at scale, you'll often need to rotate through multiple proxies to avoid rate limits and blocks. Scrapling's `ProxyRotator` makes this straightforward. It works with all session types and integrates with the spider's blocked request retry system.

If you don't know what a proxy is or how to choose a good one, [this guide can help](https://substack.thewebscraping.club/p/everything-about-proxies).

## ProxyRotator[¶](#proxyrotator "Permanent link")

The `ProxyRotator` class manages a list of proxies and rotates through them automatically. Pass it to any session type via the `proxy_rotator` parameter:

```
from scrapling.spiders import Spider, Response
from scrapling.fetchers import FetcherSession, ProxyRotator

class MySpider(Spider):
    name = "my_spider"
    start_urls = ["https://example.com"]

    def configure_sessions(self, manager):
        rotator = ProxyRotator([
            "http://proxy1:8080",
            "http://proxy2:8080",
            "http://user:pass@proxy3:8080",
        ])
        manager.add("default", FetcherSession(proxy_rotator=rotator))

    async def parse(self, response: Response):
        # Check which proxy was used
        print(f"Proxy used: {response.meta.get('proxy')}")
        yield {"title": response.css("title::text").get("")}
```

Each request automatically gets the next proxy in the rotation. The proxy used is stored in `response.meta["proxy"]` so you can track which proxy fetched which page.

When you use it with browser sessions, you will need some adjustments, like below:

```
from scrapling.fetchers import AsyncDynamicSession, AsyncStealthySession, ProxyRotator

# String proxies work for all session types
rotator = ProxyRotator([
    "http://proxy1:8080",
    "http://proxy2:8080",
])

# Dict proxies (Playwright format) work for browser sessions
rotator = ProxyRotator([
    {"server": "http://proxy1:8080", "username": "user", "password": "pass"},
    {"server": "http://proxy2:8080"},
])

# Then inside the spider
def configure_sessions(self, manager):
    rotator = ProxyRotator(["http://proxy1:8080", "http://proxy2:8080"])
    manager.add("browser", AsyncStealthySession(proxy_rotator=rotator))
```

Info

1. You cannot use the `proxy_rotator` argument together with the static `proxy` or `proxies` parameters on the same session. Pick one approach when configuring the session, and override it per request later if you want, as we will show later.
2. Remember that by default, all browser-based sessions use a persistent browser context with a pool of tabs. However, since browsers can't set a proxy per tab, when you use a `ProxyRotator`, the fetcher will automatically open a separate context for each proxy, with one tab per context. Once the tab's job is done, both the tab and its context are closed.

## Custom Rotation Strategies[¶](#custom-rotation-strategies "Permanent link")

By default, `ProxyRotator` uses cyclic rotation, iterating through proxies sequentially and wrapping around at the end.

You can provide a custom strategy function to change this behavior, but it has to match the below signature:

```
from scrapling.core._types import ProxyType

def my_strategy(proxies: list, current_index: int) -> tuple[ProxyType, int]:
    ...
```

It receives the list of proxies and the current index, and must return the chosen proxy and the next index.

Below are some examples of custom rotation strategies you can use.

### Random Rotation[¶](#random-rotation "Permanent link")

```
import random
from scrapling.fetchers import ProxyRotator

def random_strategy(proxies, current_index):
    idx = random.randint(0, len(proxies) - 1)
    return proxies[idx], idx

rotator = ProxyRotator(
    ["http://proxy1:8080", "http://proxy2:8080", "http://proxy3:8080"],
    strategy=random_strategy,
)
```

### Weighted Rotation[¶](#weighted-rotation "Permanent link")

```
import random

def weighted_strategy(proxies, current_index):
    # First proxy gets 60% of traffic, others split the rest
    weights = [60] + [40 // (len(proxies) - 1)] * (len(proxies) - 1)
    proxy = random.choices(proxies, weights=weights, k=1)[0]
    return proxy, current_index  # Index doesn't matter for weighted

rotator = ProxyRotator(proxies, strategy=weighted_strategy)
```

## Per-Request Proxy Override[¶](#per-request-proxy-override "Permanent link")

You can override the rotator for individual requests by passing `proxy=` as a keyword argument:

```
async def parse(self, response: Response):
    # This request uses the rotator's next proxy
    yield response.follow("/page1", callback=self.parse_page)

    # This request uses a specific proxy, bypassing the rotator
    yield response.follow(
        "/special-page",
        callback=self.parse_page,
        proxy="http://special-proxy:8080",
    )
```

This is useful when certain pages require a specific proxy (e.g., a geo-located proxy for region-specific content).

## Blocked Request Handling[¶](#blocked-request-handling "Permanent link")

The spider has built-in blocked request detection and retry. By default, it considers the following HTTP status codes blocked: `401`, `403`, `407`, `429`, `444`, `500`, `502`, `503`, `504`.

The retry system works like this:

1. After a response comes back, the spider calls the `is_blocked(response)` method.
2. If blocked, it copies the request and calls the `retry_blocked_request()` method so you can modify it before retrying.
3. The retried request is re-queued with `dont_filter=True` (bypassing deduplication) and lower priority, so it's not retried right away.
4. This repeats up to `max_blocked_retries` times (default: 3).

Tip

1. On retry, the previous `proxy`/`proxies` kwargs are cleared from the request automatically, so the rotator assigns a fresh proxy.
2. The `max_blocked_retries` attribute is different than the session retries and doesn't share the counter.

### Custom Block Detection[¶](#custom-block-detection "Permanent link")

Override `is_blocked()` to add your own detection logic:

```
class MySpider(Spider):
    name = "my_spider"
    start_urls = ["https://example.com"]

    async def is_blocked(self, response: Response) -> bool:
        # Check status codes (default behavior)
        if response.status in {403, 429, 503}:
            return True

        # Check response content
        body = response.body.decode("utf-8", errors="ignore")
        if "access denied" in body.lower() or "rate limit" in body.lower():
            return True

        return False

    async def parse(self, response: Response):
        yield {"title": response.css("title::text").get("")}
```

### Customizing Retries[¶](#customizing-retries "Permanent link")

Override `retry_blocked_request()` to modify the request before retrying. The `max_blocked_retries` attribute controls how many times a blocked request is retried (default: 3):

```
from scrapling.spiders import Spider, SessionManager, Request, Response
from scrapling.fetchers import FetcherSession, AsyncStealthySession


class MySpider(Spider):
    name = "my_spider"
    start_urls = ["https://example.com"]
    max_blocked_retries = 5

    def configure_sessions(self, manager: SessionManager) -> None:
        manager.add('requests', FetcherSession(impersonate=['chrome', 'firefox', 'safari']))
        manager.add('stealth', AsyncStealthySession(block_webrtc=True), lazy=True)

    async def retry_blocked_request(self, request: Request, response: Response) -> Request:
        request.sid = "stealth"
        self.logger.info(f"Retrying blocked request: {request.url}")
        return request

    async def parse(self, response: Response):
        yield {"title": response.css("title::text").get("")}
```

What happened above is that I left the blocking detection logic unchanged and had the spider mainly use requests until it got blocked, then switch to the stealthy browser.

Putting it all together:

```
from scrapling.spiders import Spider, SessionManager, Request, Response
from scrapling.fetchers import FetcherSession, AsyncStealthySession, ProxyRotator


cheap_proxies = ProxyRotator([ "http://proxy1:8080", "http://proxy2:8080"])

# A format acceptable by the browser
expensive_proxies = ProxyRotator([
    {"server": "http://residential_proxy1:8080", "username": "user", "password": "pass"},
    {"server": "http://residential_proxy2:8080", "username": "user", "password": "pass"},
    {"server": "http://mobile_proxy1:8080", "username": "user", "password": "pass"},
    {"server": "http://mobile_proxy2:8080", "username": "user", "password": "pass"},
])


class MySpider(Spider):
    name = "my_spider"
    start_urls = ["https://example.com"]
    max_blocked_retries = 5

    def configure_sessions(self, manager: SessionManager) -> None:
        manager.add('requests', FetcherSession(impersonate=['chrome', 'firefox', 'safari'], proxy_rotator=cheap_proxies))
        manager.add('stealth', AsyncStealthySession(block_webrtc=True, proxy_rotator=expensive_proxies), lazy=True)

    async def retry_blocked_request(self, request: Request, response: Response) -> Request:
        request.sid = "stealth"
        self.logger.info(f"Retrying blocked request: {request.url}")
        return request

    async def parse(self, response: Response):
        yield {"title": response.css("title::text").get("")}
```

The above logic is: requests are made with cheap proxies, such as datacenter proxies, until they are blocked, then retried with higher-quality proxies, such as residential or mobile proxies.

Was this page helpful?

Thanks for your feedback!

Thanks for your feedback! Help us improve this page by
[opening a documentation issue](https://github.com/D4Vinci/Scrapling/issues/new?template=04-docs_issue.yml).


---
## Source: https://scrapling.readthedocs.io/en/latest/spiders/advanced.html
---

# Advanced usages[¶](#advanced-usages "Permanent link")

## Introduction[¶](#introduction "Permanent link")

Prerequisites

1. You've read the [Getting started](getting-started.html) page and know how to create and run a basic spider.

This page covers the spider system's advanced features: concurrency control, pause/resume, streaming, lifecycle hooks, statistics, and logging.

## Concurrency Control[¶](#concurrency-control "Permanent link")

The spider system uses three class attributes to control how aggressively it crawls:

| Attribute | Default | Description |
| --- | --- | --- |
| `concurrent_requests` | `4` | Maximum number of requests being processed at the same time |
| `concurrent_requests_per_domain` | `0` | Maximum concurrent requests per domain (0 = no per-domain limit) |
| `download_delay` | `0.0` | Seconds to wait before each request |

```
class PoliteSpider(Spider):
    name = "polite"
    start_urls = ["https://example.com"]

    # Be gentle with the server
    concurrent_requests = 4
    concurrent_requests_per_domain = 2
    download_delay = 1.0  # Wait 1 second between requests

    async def parse(self, response: Response):
        yield {"title": response.css("title::text").get("")}
```

When `concurrent_requests_per_domain` is set, each domain gets its own concurrency limiter in addition to the global limit. This is useful when crawling multiple domains simultaneously, as you can allow high global concurrency while being polite to each individual domain.

Tip

The `download_delay` parameter adds a fixed wait before every request, regardless of the domain. Use it for simple rate limiting.

### Using uvloop[¶](#using-uvloop "Permanent link")

The `start()` method accepts a `use_uvloop` parameter to use the faster [uvloop](https://github.com/MagicStack/uvloop)/[winloop](https://github.com/nicktimko/winloop) event loop implementation, if available:

```
result = MySpider().start(use_uvloop=True)
```

This can improve throughput for I/O-heavy crawls. You'll need to install `uvloop` (Linux/macOS) or `winloop` (Windows) separately.

## Pause & Resume[¶](#pause-resume "Permanent link")

The spider supports graceful pause-and-resume via checkpointing. To enable it, pass a `crawldir` directory to the spider constructor:

```
spider = MySpider(crawldir="crawl_data/my_spider")
result = spider.start()

if result.paused:
    print("Crawl was paused. Run again to resume.")
else:
    print("Crawl completed!")
```

### How It Works[¶](#how-it-works "Permanent link")

1. **Pausing**: Press `Ctrl+C` during a crawl. The spider waits for all in-flight requests to finish, saves a checkpoint (pending requests + a set of seen request fingerprints), and then exits.
2. **Force stopping**: Press `Ctrl+C` a second time to stop immediately without waiting for active tasks.
3. **Resuming**: Run the spider again with the same `crawldir`. It detects the checkpoint, restores the queue and seen set, and continues from where it left off, skipping `start_requests()`.
4. **Cleanup**: When a crawl completes normally (not paused), the checkpoint files are deleted automatically.

**Checkpoints are also saved periodically during the crawl (every 5 minutes by default).**

You can change the interval as follows:

```
# Save checkpoint every 2 minutes
spider = MySpider(crawldir="crawl_data/my_spider", interval=120.0)
```

The writing to the disk is atomic, so it's totally safe.

Tip

Pressing `Ctrl+C` during a crawl always causes the spider to close gracefully, even if the checkpoint system is not enabled. Doing it again without waiting forces the spider to close immediately.

### Knowing If You're Resuming[¶](#knowing-if-youre-resuming "Permanent link")

The `on_start()` hook receives a `resuming` flag:

```
async def on_start(self, resuming: bool = False):
    if resuming:
        self.logger.info("Resuming from checkpoint!")
    else:
        self.logger.info("Starting fresh crawl")
```

## Streaming[¶](#streaming "Permanent link")

For long-running spiders or applications that need real-time access to scraped items, use the `stream()` method instead of `start()`:

```
import anyio

async def main():
    spider = MySpider()
    async for item in spider.stream():
        print(f"Got item: {item}")
        # Access real-time stats
        print(f"Items so far: {spider.stats.items_scraped}")
        print(f"Requests made: {spider.stats.requests_count}")

anyio.run(main)
```

Key differences from `start()`:

* `stream()` must be called from an async context
* Items are yielded one by one as they're scraped, not collected into a list
* You can access `spider.stats` during iteration for real-time statistics

Abstract

The full list of all stats that can be accessed by `spider.stats` is explained below [here](#results--statistics)

You can use it with the checkpoint system too, so it's easy to build UI on top of spiders. UIs that have real-time data and can be paused/resumed.

```
import anyio

async def main():
    spider = MySpider(crawldir="crawl_data/my_spider")
    async for item in spider.stream():
        print(f"Got item: {item}")
        # Access real-time stats
        print(f"Items so far: {spider.stats.items_scraped}")
        print(f"Requests made: {spider.stats.requests_count}")

anyio.run(main)
```

You can also use `spider.pause()` to shut down the spider in the code above. If you used it without enabling the checkpoint system, it will just close the crawl.

## Lifecycle Hooks[¶](#lifecycle-hooks "Permanent link")

The spider provides several hooks you can override to add custom behavior at different stages of the crawl:

### on_start[¶](#on_start "Permanent link")

Called before crawling begins. Use it for setup tasks like loading data or initializing resources:

```
async def on_start(self, resuming: bool = False):
    self.logger.info("Spider starting up")
    # Load seed URLs from a database, initialize counters, etc.
```

### on_close[¶](#on_close "Permanent link")

Called after crawling finishes (whether completed or paused). Use it for cleanup:

```
async def on_close(self):
    self.logger.info("Spider shutting down")
    # Close database connections, flush buffers, etc.
```

### on_error[¶](#on_error "Permanent link")

Called when a request fails with an exception. Use it for error tracking or custom recovery logic:

```
async def on_error(self, request: Request, error: Exception):
    self.logger.error(f"Failed: {request.url} - {error}")
    # Log to error tracker, save failed URL for later, etc.
```

### on_scraped_item[¶](#on_scraped_item "Permanent link")

Called for every scraped item before it's added to the results. Return the item (modified or not) to keep it, or return `None` to drop it:

```
async def on_scraped_item(self, item: dict) -> dict | None:
    # Drop items without a title
    if not item.get("title"):
        return None

    # Modify items (e.g., add timestamps)
    item["scraped_at"] = "2026-01-01"
    return item
```

Tip

This hook can also be used to direct items through your own pipelines and drop them from the spider.

### start_requests[¶](#start_requests "Permanent link")

Override `start_requests()` for custom initial request generation instead of using `start_urls`:

```
async def start_requests(self):
    # POST request to log in first
    yield Request(
        "https://example.com/login",
        method="POST",
        data={"user": "admin", "pass": "secret"},
        callback=self.after_login,
    )

async def after_login(self, response: Response):
    # Now crawl the authenticated pages
    yield response.follow("/dashboard", callback=self.parse)
```

## Results & Statistics[¶](#results-statistics "Permanent link")

The `CrawlResult` returned by `start()` contains both the scraped items and detailed statistics:

```
result = MySpider().start()

# Items
print(f"Total items: {len(result.items)}")
result.items.to_json("output.json", indent=True)

# Did the crawl complete?
print(f"Completed: {result.completed}")
print(f"Paused: {result.paused}")

# Statistics
stats = result.stats
print(f"Requests: {stats.requests_count}")
print(f"Failed: {stats.failed_requests_count}")
print(f"Blocked: {stats.blocked_requests_count}")
print(f"Offsite filtered: {stats.offsite_requests_count}")
print(f"Items scraped: {stats.items_scraped}")
print(f"Items dropped: {stats.items_dropped}")
print(f"Response bytes: {stats.response_bytes}")
print(f"Duration: {stats.elapsed_seconds:.1f}s")
print(f"Speed: {stats.requests_per_second:.1f} req/s")
```

### Detailed Stats[¶](#detailed-stats "Permanent link")

The `CrawlStats` object tracks granular information:

```
stats = result.stats

# Status code distribution
print(stats.response_status_count)
# {'status_200': 150, 'status_404': 3, 'status_403': 1}

# Bytes downloaded per domain
print(stats.domains_response_bytes)
# {'example.com': 1234567, 'api.example.com': 45678}

# Requests per session
print(stats.sessions_requests_count)
# {'http': 120, 'stealth': 34}

# Proxies used during the crawl
print(stats.proxies)
# ['http://proxy1:8080', 'http://proxy2:8080']

# Log level counts
print(stats.log_levels_counter)
# {'debug': 200, 'info': 50, 'warning': 3, 'error': 1, 'critical': 0}

# Timing information
print(stats.start_time)       # Unix timestamp when crawl started
print(stats.end_time)         # Unix timestamp when crawl finished
print(stats.download_delay)   # The download delay used (seconds)

# Concurrency settings used
print(stats.concurrent_requests)             # Global concurrency limit
print(stats.concurrent_requests_per_domain)  # Per-domain concurrency limit

# Custom stats (set by your spider code)
print(stats.custom_stats)
# {'login_attempts': 3, 'pages_with_errors': 5}

# Export everything as a dict
print(stats.to_dict())
```

## Logging[¶](#logging "Permanent link")

The spider has a built-in logger accessible via `self.logger`. It's pre-configured with the spider's name and supports several customization options:

| Attribute | Default | Description |
| --- | --- | --- |
| `logging_level` | `logging.DEBUG` | Minimum log level |
| `logging_format` | `"[%(asctime)s]:({spider_name}) %(levelname)s: %(message)s"` | Log message format |
| `logging_date_format` | `"%Y-%m-%d %H:%M:%S"` | Date format in log messages |
| `log_file` | `None` | Path to a log file (in addition to console output) |

```
import logging

class MySpider(Spider):
    name = "my_spider"
    start_urls = ["https://example.com"]
    logging_level = logging.INFO
    log_file = "logs/my_spider.log"

    async def parse(self, response: Response):
        self.logger.info(f"Processing {response.url}")
        yield {"title": response.css("title::text").get("")}
```

The log file directory is created automatically if it doesn't exist. Both console and file output use the same format.

Was this page helpful?

Thanks for your feedback!

Thanks for your feedback! Help us improve this page by
[opening a documentation issue](https://github.com/D4Vinci/Scrapling/issues/new?template=04-docs_issue.yml).


---
## Source: https://scrapling.readthedocs.io/en/latest/cli/overview.html
---

# Command Line Interface[¶](#command-line-interface "Permanent link")

Since v0.3, Scrapling includes a powerful command-line interface that provides three main capabilities:

1. **Interactive Shell**: An interactive Web Scraping shell based on IPython that provides many shortcuts and useful tools
2. **Extract Commands**: Scrape websites from the terminal without any programming
3. **Utility Commands**: Installation and management tools

```
# Launch interactive shell
scrapling shell

# Convert the content of a page to markdown and save it to a file
scrapling extract get "https://example.com" content.md

# Get help for any command
scrapling --help
scrapling extract --help
```

## Requirements[¶](#requirements "Permanent link")

This section requires you to install the extra `shell` dependency group, like the following:

```
pip install "scrapling[shell]"
```

and the installation of the fetchers' dependencies with the following command

```
scrapling install
```

This downloads all browsers, along with their system dependencies and fingerprint manipulation dependencies.

Was this page helpful?

Thanks for your feedback!

Thanks for your feedback! Help us improve this page by
[opening a documentation issue](https://github.com/D4Vinci/Scrapling/issues/new?template=04-docs_issue.yml).


---
## Source: https://scrapling.readthedocs.io/en/latest/cli/interactive-shell.html
---

# Scrapling Interactive Shell Guide[¶](#scrapling-interactive-shell-guide "Permanent link")

**Powerful Web Scraping REPL for Developers and Data Scientists**

The Scrapling Interactive Shell is an enhanced IPython-based environment designed specifically for Web Scraping tasks. It provides instant access to all Scrapling features, clever shortcuts, automatic page management, and advanced tools, such as conversion of the curl command.

Prerequisites

1. You've completed or read the [Fetchers basics](../fetching/choosing.html) page to understand what the [Response object](../fetching/choosing.html#response-object) is and which fetcher to use.
2. You've completed or read the [Querying elements](../parsing/selection.html) page to understand how to find/extract elements from the [Selector](../parsing/main_classes.html#selector)/[Response](../fetching/choosing.html#response-object) object.
3. You've completed or read the [Main classes](../parsing/main_classes.html) page to know what properties/methods the [Response](../fetching/choosing.html#response-object) class is inheriting from the [Selector](../parsing/main_classes.html#selector) class.
4. You've completed or read at least one page from the fetchers section to use here for requests: [HTTP requests](../fetching/static.html), [Dynamic websites](../fetching/dynamic.html), or [Dynamic websites with hard protections](../fetching/stealthy.html).

## Why use the Interactive Shell?[¶](#why-use-the-interactive-shell "Permanent link")

The interactive shell transforms web scraping from a slow script-and-run cycle into a fast, exploratory experience. It's perfect for:

* **Rapid prototyping**: Test scraping strategies instantly
* **Data exploration**: Interactively navigate and extract from websites
* **Learning Scrapling**: Experiment with features in real-time
* **Debugging scrapers**: Step through requests and inspect results
* **Converting workflows**: Transform curl commands from browser DevTools to a Fetcher request in a one-liner

## Getting Started[¶](#getting-started "Permanent link")

### Launch the Shell[¶](#launch-the-shell "Permanent link")

```
# Start the interactive shell
scrapling shell

# Execute code and exit (useful for scripting)
scrapling shell -c "get('https://quotes.toscrape.com'); print(len(page.css('.quote')))"

# Set logging level
scrapling shell --loglevel info
```

Once launched, you'll see the Scrapling banner and can immediately start scraping as the video above shows:

```
# No imports needed - everything is ready!
>>> get('https://news.ycombinator.com')

>>> # Explore the page structure
>>> page.css('a')[:5]  # Look at first 5 links

>>> # Refine your selectors
>>> stories = page.css('.titleline>a')
>>> len(stories)
30

>>> # Extract specific data
>>> for story in stories[:3]:
...     title = story.text
...     url = story['href']
...     print(f"{title}: {url}")

>>> # Try different approaches
>>> titles = page.css('.titleline>a::text')  # Direct text extraction
>>> urls = page.css('.titleline>a::attr(href)')  # Direct attribute extraction
```

## Built-in Shortcuts[¶](#built-in-shortcuts "Permanent link")

The shell provides convenient shortcuts that eliminate boilerplate code:

* **`get(url, **kwargs)`** - HTTP GET request (instead of `Fetcher.get`)
* **`post(url, **kwargs)`** - HTTP POST request (instead of `Fetcher.post`)
* **`put(url, **kwargs)`** - HTTP PUT request (instead of `Fetcher.put`)
* **`delete(url, **kwargs)`** - HTTP DELETE request (instead of `Fetcher.delete`)
* **`fetch(url, **kwargs)`** - Browser-based fetch (instead of `DynamicFetcher.fetch`)
* **`stealthy_fetch(url, **kwargs)`** - Stealthy browser fetch (instead of `StealthyFetcher.fetch`)

The most commonly used classes are automatically available without any import, including `Fetcher`, `AsyncFetcher`, `DynamicFetcher`, `StealthyFetcher`, and `Selector`.

### Smart Page Management[¶](#smart-page-management "Permanent link")

The shell automatically tracks your requests and pages:

* **Current Page Access**

  The `page` and `response` commands are automatically updated with the last fetched page:

  ```
  >>> get('https://quotes.toscrape.com')
  >>> # 'page' and 'response' both refer to the last fetched page
  >>> page.url
  'https://quotes.toscrape.com'
  >>> response.status  # Same as page.status
  200
  ```
* **Page History**

  The `pages` command keeps track of the last five pages (it's a `Selectors` object):

  ```
  >>> get('https://site1.com')
  >>> get('https://site2.com') 
  >>> get('https://site3.com')

  >>> # Access last 5 pages
  >>> len(pages)  # `Selectors` object with `page` history
  3
  >>> pages[0].url  # First page in history
  'https://site1.com'
  >>> pages[-1].url  # Most recent page
  'https://site3.com'

  >>> # Work with historical pages
  >>> for i, old_page in enumerate(pages):
  ...     print(f"Page {i}: {old_page.url} - {old_page.status}")
  ```

## Additional helpful commands[¶](#additional-helpful-commands "Permanent link")

### Page Visualization[¶](#page-visualization "Permanent link")

View scraped pages in your browser:

```
>>> get('https://quotes.toscrape.com')
>>> view(page)  # Opens the page HTML in your default browser
```

### Curl Command Integration[¶](#curl-command-integration "Permanent link")

The shell provides a few functions to help you convert curl commands from the browser DevTools to `Fetcher` requests: `uncurl` and `curl2fetcher`.

First, you need to copy a request as a curl command like the following:

![Copying a request as a curl command from Chrome](../assets/scrapling_shell_curl.png "Copying a request as a curl command from Chrome")

* **Convert Curl command to Request Object**

  ```
  >>> curl_cmd = '''curl 'https://scrapling.requestcatcher.com/post' \
  ...   -X POST \
  ...   -H 'Content-Type: application/json' \
  ...   -d '{"name": "test", "value": 123}' '''

  >>> request = uncurl(curl_cmd)
  >>> request.method
  'post'
  >>> request.url
  'https://scrapling.requestcatcher.com/post'
  >>> request.headers
  {'Content-Type': 'application/json'}
  ```
* **Execute Curl Command Directly**

  ```
  >>> # Convert and execute in one step
  >>> curl2fetcher(curl_cmd)
  >>> page.status
  200
  >>> page.json()['json']
  {'name': 'test', 'value': 123}
  ```

### IPython Features[¶](#ipython-features "Permanent link")

The shell inherits all IPython capabilities:

```
>>> # Magic commands
>>> %time page = get('https://example.com')  # Time execution
>>> %history  # Show command history
>>> %save filename.py 1-10  # Save commands 1-10 to file

>>> # Tab completion works everywhere
>>> page.c<TAB>  # Shows: css, cookies, headers, etc.
>>> Fetcher.<TAB>  # Shows all Fetcher methods

>>> # Object inspection
>>> get? # Show get documentation
```

## Examples[¶](#examples "Permanent link")

Here are a few examples generated via AI:

#### E-commerce Data Collection[¶](#e-commerce-data-collection "Permanent link")

```
>>> # Start with product listing page
>>> catalog = get('https://shop.example.com/products')

>>> # Find product links
>>> product_links = catalog.css('.product-link::attr(href)')
>>> print(f"Found {len(product_links)} products")

>>> # Sample a few products first
>>> for link in product_links[:3]:
...     product = get(f"https://shop.example.com{link}")
...     name = product.css('.product-name::text').get('')
...     price = product.css('.price::text').get('')
...     print(f"{name}: {price}")

>>> # Scale up with sessions for efficiency
>>> from scrapling.fetchers import FetcherSession
>>> with FetcherSession() as session:
...     products = []
...     for link in product_links:
...         product = session.get(f"https://shop.example.com{link}")
...         products.append({
...             'name': product.css('.product-name::text').get(''),
...             'price': product.css('.price::text').get(''),
...             'url': link
...         })
```

#### API Integration and Testing[¶](#api-integration-and-testing "Permanent link")

```
>>> # Test API endpoints interactively
>>> response = get('https://jsonplaceholder.typicode.com/posts/1')
>>> response.json()
{'userId': 1, 'id': 1, 'title': 'sunt aut...', 'body': 'quia et...'}

>>> # Test POST requests
>>> new_post = post('https://jsonplaceholder.typicode.com/posts', 
...                 json={'title': 'Test Post', 'body': 'Test content', 'userId': 1})
>>> new_post.json()['id']
101

>>> # Test with different data
>>> updated = put(f'https://jsonplaceholder.typicode.com/posts/{new_post.json()["id"]}',
...               json={'title': 'Updated Title'})
```

## Getting Help[¶](#getting-help "Permanent link")

If you need help other than what is available in-terminal, you can:

* [Scrapling Documentation](https://scrapling.readthedocs.io/)
* [Discord Community](https://discord.gg/EMgGbDceNQ)
* [GitHub Issues](https://github.com/D4Vinci/Scrapling/issues)

And that's it! Happy scraping! The shell makes web scraping as easy as a conversation.

Was this page helpful?

Thanks for your feedback!

Thanks for your feedback! Help us improve this page by
[opening a documentation issue](https://github.com/D4Vinci/Scrapling/issues/new?template=04-docs_issue.yml).


---
## Source: https://scrapling.readthedocs.io/en/latest/cli/extract-commands.html
---

# Scrapling Extract Command Guide[¶](#scrapling-extract-command-guide "Permanent link")

**Web Scraping through the terminal without requiring any programming!**

The `scrapling extract` command lets you download and extract content from websites directly from your terminal without writing any code. Ideal for beginners, researchers, and anyone requiring rapid web data extraction.

Prerequisites

1. You've completed or read the [Fetchers basics](../fetching/choosing.html) page to understand what the [Response object](../fetching/choosing.html#response-object) is and which fetcher to use.
2. You've completed or read the [Querying elements](../parsing/selection.html) page to understand how to find/extract elements from the [Selector](../parsing/main_classes.html#selector)/[Response](../fetching/choosing.html#response-object) object.
3. You've completed or read the [Main classes](../parsing/main_classes.html) page to know what properties/methods the [Response](../fetching/choosing.html#response-object) class is inheriting from the [Selector](../parsing/main_classes.html#selector) class.
4. You've completed or read at least one page from the fetchers section to use here for requests: [HTTP requests](../fetching/static.html), [Dynamic websites](../fetching/dynamic.html), or [Dynamic websites with hard protections](../fetching/stealthy.html).

## What is the Extract Command group?[¶](#what-is-the-extract-command-group "Permanent link")

The extract command is a set of simple terminal tools that:

* **Downloads web pages** and saves their content to files.
* **Converts HTML to readable formats** like Markdown, keeps it as HTML, or just extracts the text content of the page.
* **Supports custom CSS selectors** to extract specific parts of the page.
* **Handles HTTP requests and fetching through browsers**
* **Highly customizable** with custom headers, cookies, proxies, and the rest of the options. Almost all the options available through the code are also accessible through the command line.

AI-Targeted Mode

All extract commands support an `--ai-targeted` flag. When enabled, it extracts only the main body content, strips noise tags (script, style, noscript, svg), removes hidden elements that could be used for prompt injection (CSS-hidden, aria-hidden, template tags), strips zero-width unicode characters, and removes HTML comments. This is ideal when the output is destined for an AI model.

## Quick Start[¶](#quick-start "Permanent link")

* **Basic Website Download**

  Download a website's text content as clean, readable text:

  ```
  scrapling extract get "https://example.com" page_content.txt
  ```

  This makes an HTTP GET request and saves the webpage's text content to `page_content.txt`.
* **Save as Different Formats**

  Choose your output format by changing the file extension:

  ```
  # Convert the HTML content to Markdown, then save it to the file (great for documentation)
  scrapling extract get "https://blog.example.com" article.md

  # Save the HTML content as it is to the file
  scrapling extract get "https://example.com" page.html

  # Save a clean version of the text content of the webpage to the file
  scrapling extract get "https://example.com" content.txt

  # Or use the Docker image with something like this:
  docker run -v $(pwd)/output:/output scrapling extract get "https://blog.example.com" /output/article.md
  ```
* **Extract Specific Content**

  All commands can use CSS selectors to extract specific parts of the page through `--css-selector` or `-s` as you will see in the examples below.

## Available Commands[¶](#available-commands "Permanent link")

You can display the available commands through `scrapling extract --help` to get the following list:

```
Usage: scrapling extract [OPTIONS] COMMAND [ARGS]...

  Fetch web pages using various fetchers and extract full/selected HTML content as HTML, Markdown, or extract text content.

Options:
  --help  Show this message and exit.

Commands:
  get             Perform a GET request and save the content to a file.
  post            Perform a POST request and save the content to a file.
  put             Perform a PUT request and save the content to a file.
  delete          Perform a DELETE request and save the content to a file.
  fetch           Use DynamicFetcher to fetch content with browser...
  stealthy-fetch  Use StealthyFetcher to fetch content with advanced...
```

We will go through each command in detail below.

### HTTP Requests[¶](#http-requests "Permanent link")

1. **GET Request**

   The most common command for downloading website content:

   ```
   scrapling extract get [URL] [OUTPUT_FILE] [OPTIONS]
   ```

   **Examples:**

   ```
   # Basic download
   scrapling extract get "https://news.site.com" news.md

   # Download with custom timeout
   scrapling extract get "https://example.com" content.txt --timeout 60

   # Extract only specific content using CSS selectors
   scrapling extract get "https://blog.example.com" articles.md --css-selector "article"

   # Send a request with cookies
   scrapling extract get "https://scrapling.requestcatcher.com" content.md --cookies "session=abc123; user=john"

   # Add user agent
   scrapling extract get "https://api.site.com" data.json -H "User-Agent: MyBot 1.0"

   # Add multiple headers
   scrapling extract get "https://site.com" page.html -H "Accept: text/html" -H "Accept-Language: en-US"
   ```

   Get the available options for the command with `scrapling extract get --help` as follows:

   ```
   Usage: scrapling extract get [OPTIONS] URL OUTPUT_FILE

     Perform a GET request and save the content to a file.

     The output file path can be an HTML file, a Markdown file of the HTML content, or the text content itself. Use file extensions (`.html`/`.md`/`.txt`) respectively.

   Options:
     -H, --headers TEXT                             HTTP headers in format "Key: Value" (can be used multiple times)
     --cookies TEXT                                 Cookies string in format "name1=value1;name2=value2"
     --timeout INTEGER                              Request timeout in seconds (default: 30)
     --proxy TEXT                                   Proxy URL in format "http://username:password@host:port"
     -s, --css-selector TEXT                        CSS selector to extract specific content from the page. It returns all matches.
     -p, --params TEXT                              Query parameters in format "key=value" (can be used multiple times)
     --follow-redirects / --no-follow-redirects     Whether to follow redirects (default: True)
     --verify / --no-verify                         Whether to verify SSL certificates (default: True)
     --impersonate TEXT                             Browser to impersonate (e.g., chrome, firefox).
     --stealthy-headers / --no-stealthy-headers     Use stealthy browser headers (default: True)
     --ai-targeted                                  Extract only main content and sanitize hidden elements for AI consumption (default: False)
     --help                                         Show this message and exit.
   ```

   Note that the options will work in the same way for all other request commands, so no need to repeat them.
2. **Post Request**

   ```
   scrapling extract post [URL] [OUTPUT_FILE] [OPTIONS]
   ```

   **Examples:**

   ```
   # Submit form data
   scrapling extract post "https://api.site.com/search" results.html --data "query=python&type=tutorial"

   # Send JSON data
   scrapling extract post "https://api.site.com" response.json --json '{"username": "test", "action": "search"}'
   ```

   Get the available options for the command with `scrapling extract post --help` as follows:

   ```
   Usage: scrapling extract post [OPTIONS] URL OUTPUT_FILE

     Perform a POST request and save the content to a file.

     The output file path can be an HTML file, a Markdown file of the HTML content, or the text content itself. Use file extensions (`.html`/`.md`/`.txt`) respectively.

   Options:
     -d, --data TEXT                                Form data to include in the request body (as string, ex: "param1=value1&param2=value2")
     -j, --json TEXT                                JSON data to include in the request body (as string)
     -H, --headers TEXT                             HTTP headers in format "Key: Value" (can be used multiple times)
     --cookies TEXT                                 Cookies string in format "name1=value1;name2=value2"
     --timeout INTEGER                              Request timeout in seconds (default: 30)
     --proxy TEXT                                   Proxy URL in format "http://username:password@host:port"
     -s, --css-selector TEXT                        CSS selector to extract specific content from the page. It returns all matches.
     -p, --params TEXT                              Query parameters in format "key=value" (can be used multiple times)
     --follow-redirects / --no-follow-redirects     Whether to follow redirects (default: True)
     --verify / --no-verify                         Whether to verify SSL certificates (default: True)
     --impersonate TEXT                             Browser to impersonate (e.g., chrome, firefox).
     --stealthy-headers / --no-stealthy-headers     Use stealthy browser headers (default: True)
     --ai-targeted                                  Extract only main content and sanitize hidden elements for AI consumption (default: False)
     --help                                         Show this message and exit.
   ```
3. **Put Request**

   ```
   scrapling extract put [URL] [OUTPUT_FILE] [OPTIONS]
   ```

   **Examples:**

   ```
   # Send data
   scrapling extract put "https://scrapling.requestcatcher.com/put" results.html --data "update=info" --impersonate "firefox"

   # Send JSON data
   scrapling extract put "https://scrapling.requestcatcher.com/put" response.json --json '{"username": "test", "action": "search"}'
   ```

   Get the available options for the command with `scrapling extract put --help` as follows:

   ```
   Usage: scrapling extract put [OPTIONS] URL OUTPUT_FILE

     Perform a PUT request and save the content to a file.

     The output file path can be an HTML file, a Markdown file of the HTML content, or the text content itself. Use file extensions (`.html`/`.md`/`.txt`) respectively.

   Options:
     -d, --data TEXT                                Form data to include in the request body
     -j, --json TEXT                                JSON data to include in the request body (as string)
     -H, --headers TEXT                             HTTP headers in format "Key: Value" (can be used multiple times)
     --cookies TEXT                                 Cookies string in format "name1=value1;name2=value2"
     --timeout INTEGER                              Request timeout in seconds (default: 30)
     --proxy TEXT                                   Proxy URL in format "http://username:password@host:port"
     -s, --css-selector TEXT                        CSS selector to extract specific content from the page. It returns all matches.
     -p, --params TEXT                              Query parameters in format "key=value" (can be used multiple times)
     --follow-redirects / --no-follow-redirects     Whether to follow redirects (default: True)
     --verify / --no-verify                         Whether to verify SSL certificates (default: True)
     --impersonate TEXT                             Browser to impersonate (e.g., chrome, firefox).
     --stealthy-headers / --no-stealthy-headers     Use stealthy browser headers (default: True)
     --ai-targeted                                  Extract only main content and sanitize hidden elements for AI consumption (default: False)
     --help                                         Show this message and exit.
   ```
4. **Delete Request**

   ```
   scrapling extract delete [URL] [OUTPUT_FILE] [OPTIONS]
   ```

   **Examples:**

   ```
   # Send data
   scrapling extract delete "https://scrapling.requestcatcher.com/delete" results.html

   # Send JSON data
   scrapling extract delete "https://scrapling.requestcatcher.com/" response.txt --impersonate "chrome"
   ```

   Get the available options for the command with `scrapling extract delete --help` as follows:

   ```
   Usage: scrapling extract delete [OPTIONS] URL OUTPUT_FILE

     Perform a DELETE request and save the content to a file.

     The output file path can be an HTML file, a Markdown file of the HTML content, or the text content itself. Use file extensions (`.html`/`.md`/`.txt`) respectively.

   Options:
     -H, --headers TEXT                             HTTP headers in format "Key: Value" (can be used multiple times)
     --cookies TEXT                                 Cookies string in format "name1=value1;name2=value2"
     --timeout INTEGER                              Request timeout in seconds (default: 30)
     --proxy TEXT                                   Proxy URL in format "http://username:password@host:port"
     -s, --css-selector TEXT                        CSS selector to extract specific content from the page. It returns all matches.
     -p, --params TEXT                              Query parameters in format "key=value" (can be used multiple times)
     --follow-redirects / --no-follow-redirects     Whether to follow redirects (default: True)
     --verify / --no-verify                         Whether to verify SSL certificates (default: True)
     --impersonate TEXT                             Browser to impersonate (e.g., chrome, firefox).
     --stealthy-headers / --no-stealthy-headers     Use stealthy browser headers (default: True)
     --ai-targeted                                  Extract only main content and sanitize hidden elements for AI consumption (default: False)
     --help                                         Show this message and exit.
   ```

### Browsers fetching[¶](#browsers-fetching "Permanent link")

1. **fetch - Handle Dynamic Content**

   For websites that load content with dynamic content or have slight protection

   ```
   scrapling extract fetch [URL] [OUTPUT_FILE] [OPTIONS]
   ```

   **Examples:**

   ```
   # Wait for JavaScript to load content and finish network activity
   scrapling extract fetch "https://scrapling.requestcatcher.com/" content.md --network-idle

   # Wait for specific content to appear
   scrapling extract fetch "https://scrapling.requestcatcher.com/" data.txt --wait-selector ".content-loaded"

   # Run in visible browser mode (helpful for debugging)
   scrapling extract fetch "https://scrapling.requestcatcher.com/" page.html --no-headless --disable-resources
   ```

   Get the available options for the command with `scrapling extract fetch --help` as follows:

   ```
   Usage: scrapling extract fetch [OPTIONS] URL OUTPUT_FILE

     Use DynamicFetcher to fetch content with browser automation.

     The output file path can be an HTML file, a Markdown file of the HTML content, or the text content itself. Use file extensions (`.html`/`.md`/`.txt`) respectively.

   Options:
     --headless / --no-headless                  Run browser in headless mode (default: True)
     --disable-resources / --enable-resources    Drop unnecessary resources for speed boost (default: False)
     --network-idle / --no-network-idle          Wait for network idle (default: False)
     --timeout INTEGER                           Timeout in milliseconds (default: 30000)
     --wait INTEGER                              Additional wait time in milliseconds after page load (default: 0)
     -s, --css-selector TEXT                     CSS selector to extract specific content from the page. It returns all matches.
     --wait-selector TEXT                        CSS selector to wait for before proceeding
     --locale TEXT                               Specify user locale. Defaults to the system default locale.
     --real-chrome/--no-real-chrome              If you have a Chrome browser installed on your device, enable this, and the Fetcher will launch an instance of your browser and use it. (default: False)
     --proxy TEXT                                Proxy URL in format "http://username:password@host:port"
     -H, --extra-headers TEXT                    Extra headers in format "Key: Value" (can be used multiple times)
     --ai-targeted                              Extract only main content and sanitize hidden elements for AI consumption (default: False)
     --help                                      Show this message and exit.
   ```
2. **stealthy-fetch - Bypass Protection**

   For websites with anti-bot protection or Cloudflare protection

   ```
   scrapling extract stealthy-fetch [URL] [OUTPUT_FILE] [OPTIONS]
   ```

   **Examples:**

   ```
   # Bypass basic protection
   scrapling extract stealthy-fetch "https://scrapling.requestcatcher.com" content.md

   # Solve Cloudflare challenges
   scrapling extract stealthy-fetch "https://nopecha.com/demo/cloudflare" data.txt --solve-cloudflare --css-selector "#padded_content a"

   # Use a proxy for anonymity.
   scrapling extract stealthy-fetch "https://site.com" content.md --proxy "http://proxy-server:8080"
   ```

   Get the available options for the command with `scrapling extract stealthy-fetch --help` as follows:

   ```
   Usage: scrapling extract stealthy-fetch [OPTIONS] URL OUTPUT_FILE

     Use StealthyFetcher to fetch content with advanced stealth features.

     The output file path can be an HTML file, a Markdown file of the HTML content, or the text content itself. Use file extensions (`.html`/`.md`/`.txt`) respectively.

   Options:
     --headless / --no-headless                  Run browser in headless mode (default: True)
     --disable-resources / --enable-resources    Drop unnecessary resources for speed boost (default: False)
     --block-webrtc / --allow-webrtc             Block WebRTC entirely (default: False)
     --solve-cloudflare / --no-solve-cloudflare  Solve Cloudflare challenges (default: False)
     --allow-webgl / --block-webgl               Allow WebGL (default: True)
     --network-idle / --no-network-idle          Wait for network idle (default: False)
     --real-chrome/--no-real-chrome              If you have a Chrome browser installed on your device, enable this, and the Fetcher will launch an instance of your browser and use it. (default: False)
     --timeout INTEGER                           Timeout in milliseconds (default: 30000)
     --wait INTEGER                              Additional wait time in milliseconds after page load (default: 0)
     -s, --css-selector TEXT                     CSS selector to extract specific content from the page. It returns all matches.
     --wait-selector TEXT                        CSS selector to wait for before proceeding
     --hide-canvas / --show-canvas               Add noise to canvas operations (default: False)
     --proxy TEXT                                Proxy URL in format "http://username:password@host:port"
     -H, --extra-headers TEXT                    Extra headers in format "Key: Value" (can be used multiple times)
     --ai-targeted                              Extract only main content and sanitize hidden elements for AI consumption (default: False)
     --help                                      Show this message and exit.
   ```

## When to use each command[¶](#when-to-use-each-command "Permanent link")

If you are not a Web Scraping expert and can't decide what to choose, you can use the following formula to help you decide:

* Use **`get`** with simple websites, blogs, or news articles
* Use **`fetch`** with modern web apps, or sites with dynamic content
* Use **`stealthy-fetch`** with protected sites, Cloudflare, or anti-bot systems

## Legal and Ethical Considerations[¶](#legal-and-ethical-considerations "Permanent link")

⚠️ **Important Guidelines:**

* **Check robots.txt**: Visit `https://website.com/robots.txt` to see scraping rules
* **Respect rate limits**: Don't overwhelm servers with requests
* **Terms of Service**: Read and comply with website terms
* **Copyright**: Respect intellectual property rights
* **Privacy**: Be mindful of personal data protection laws
* **Commercial use**: Ensure you have permission for business purposes

---

*Happy scraping! Remember to always respect website policies and comply with all applicable laws and regulations.*

Was this page helpful?

Thanks for your feedback!

Thanks for your feedback! Help us improve this page by
[opening a documentation issue](https://github.com/D4Vinci/Scrapling/issues/new?template=04-docs_issue.yml).


---
## Source: https://scrapling.readthedocs.io/en/latest/ai/mcp-server.html
---

# Scrapling MCP Server Guide[¶](#scrapling-mcp-server-guide "Permanent link")

The **Scrapling MCP Server** is a new feature that brings Scrapling's powerful Web Scraping capabilities directly to your favorite AI chatbot or AI agent. This integration allows you to scrape websites, extract data, and bypass anti-bot protections conversationally through Claude's AI interface or any interface that supports MCP.

## Features[¶](#features "Permanent link")

The Scrapling MCP Server provides nine powerful tools for web scraping:

### 🚀 Basic HTTP Scraping[¶](#basic-http-scraping "Permanent link")

* **`get`**: Fast HTTP requests with browser fingerprint impersonation, generating real browser headers matching the TLS version, HTTP/3, and more!
* **`bulk_get`**: An async version of the above tool that allows scraping of multiple URLs at the same time!

### 🌐 Dynamic Content Scraping[¶](#dynamic-content-scraping "Permanent link")

* **`fetch`**: Rapidly fetch dynamic content with Chromium/Chrome browser with complete control over the request/browser, and more!
* **`bulk_fetch`**: An async version of the above tool that allows scraping of multiple URLs in different browser tabs at the same time!

### 🔒 Stealth Scraping[¶](#stealth-scraping "Permanent link")

* **`stealthy_fetch`**: Uses our Stealthy browser to bypass Cloudflare Turnstile/Interstitial and other anti-bot systems with complete control over the request/browser!
* **`bulk_stealthy_fetch`**: An async version of the above tool that allows stealth scraping of multiple URLs in different browser tabs at the same time!

### 🔌 Session Management[¶](#session-management "Permanent link")

* **`open_session`**: Create a persistent browser session (dynamic or stealthy) that stays open across multiple fetch calls, avoiding the overhead of launching a new browser each time.
* **`close_session`**: Close a persistent browser session and free its resources.
* **`list_sessions`**: List all active browser sessions with their details.

### Key Capabilities[¶](#key-capabilities "Permanent link")

* **Smart Content Extraction**: Convert web pages/elements to Markdown, HTML, or extract a clean version of the text content
* **CSS Selector Support**: Use the Scrapling engine to target specific elements with precision before handing the content to the AI
* **Anti-Bot Bypass**: Handle Cloudflare Turnstile, Interstitial, and other protections
* **Proxy Support**: Use proxies for anonymity and geo-targeting
* **Browser Impersonation**: Mimic real browsers with TLS fingerprinting, real browser headers matching that version, and more
* **Parallel Processing**: Scrape multiple URLs concurrently for efficiency
* **Session Persistence**: Reuse browser sessions across multiple requests for better performance
* **Prompt Injection Protection**: Automatic sanitization of hidden content (CSS-hidden elements, aria-hidden, zero-width characters, HTML comments, template tags) that could be used for prompt injection attacks

#### But why use Scrapling MCP Server instead of other available tools?[¶](#but-why-use-scrapling-mcp-server-instead-of-other-available-tools "Permanent link")

Aside from its stealth capabilities and ability to bypass Cloudflare Turnstile/Interstitial, Scrapling's server is the only one that lets you select specific elements to pass to the AI, saving a lot of time and tokens!

The way other servers work is that they extract the content, then pass it all to the AI to extract the fields you want. This causes the AI to consume far more tokens than needed (from irrelevant content). Scrapling solves this problem by allowing you to pass a CSS selector to narrow down the content you want before passing it to the AI, which makes the whole process much faster and more efficient.

If you don't know how to write/use CSS selectors, don't worry. You can tell the AI in the prompt to write selectors to match possible fields for you and watch it try different combinations until it finds the right one, as we will show in the examples section.

## Installation[¶](#installation "Permanent link")

Install Scrapling with MCP Support, then double-check that the browser dependencies are installed.

```
# Install Scrapling with MCP server dependencies
pip install "scrapling[ai]"

# Install browser dependencies
scrapling install
```

Or use the Docker image directly from the Docker registry:

```
docker pull pyd4vinci/scrapling
```

Or download it from the GitHub registry:

```
docker pull ghcr.io/d4vinci/scrapling:latest
```

## Setting up the MCP Server[¶](#setting-up-the-mcp-server "Permanent link")

Here we will explain how to add Scrapling MCP Server to [Claude Desktop](https://claude.ai/download) and [Claude Code](https://www.anthropic.com/claude-code), but the same logic applies to any other chatbot that supports MCP:

### Claude Desktop[¶](#claude-desktop "Permanent link")

1. Open Claude Desktop
2. Click the hamburger menu (☰) at the top left → Settings → Developer → Edit Config
3. Add the Scrapling MCP server configuration:

   ```
   "ScraplingServer": {
     "command": "scrapling",
     "args": [
       "mcp"
     ]
   }
   ```

   If that's the first MCP server you're adding, set the content of the file to this:

   ```
   {
     "mcpServers": {
       "ScraplingServer": {
         "command": "scrapling",
         "args": [
           "mcp"
         ]
       }
     }
   }
   ```

   As per the [official article](https://modelcontextprotocol.io/quickstart/user), this action either creates a new configuration file if none exists or opens your existing configuration. The file is located at
4. **MacOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
5. **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

To ensure it's working, use the full path to the `scrapling` executable. Open the terminal and execute the following command:

1. **MacOS**: `which scrapling`
2. **Windows**: `where scrapling`

For me, on my Mac, it returned `/Users/<MyUsername>/.venv/bin/scrapling`, so the config I used in the end is:

```
{
  "mcpServers": {
    "ScraplingServer": {
      "command": "/Users/<MyUsername>/.venv/bin/scrapling",
      "args": [
        "mcp"
      ]
    }
  }
}
```

#### Docker[¶](#docker "Permanent link")

If you are using the Docker image, then it would be something like

```
{
  "mcpServers": {
    "ScraplingServer": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm", "scrapling", "mcp"
      ]
    }
  }
}
```

The same logic applies to [Cursor](https://cursor.com/docs/context/mcp), [WindSurf](https://windsurf.com/university/tutorials/configuring-first-mcp-server), and others.

### Claude Code[¶](#claude-code "Permanent link")

Here it's much simpler to do. If you have [Claude Code](https://www.anthropic.com/claude-code) installed, open the terminal and execute the following command:

```
claude mcp add ScraplingServer "/Users/<MyUsername>/.venv/bin/scrapling" mcp
```

Same as above, to get Scrapling's executable path, open the terminal and execute the following command:

1. **MacOS**: `which scrapling`
2. **Windows**: `where scrapling`

Here's the main article from Anthropic on [how to add MCP servers to Claude code](https://docs.anthropic.com/en/docs/claude-code/mcp#option-1%3A-add-a-local-stdio-server) for further details.

Then, after you've added the server, you need to completely quit and restart the app you used above. In Claude Desktop, you should see an MCP server indicator (🔧) in the bottom-right corner of the chat input or see `ScraplingServer` in the `Search and tools` dropdown in the chat input box.

### Streamable HTTP[¶](#streamable-http "Permanent link")

As per version 0.3.6, we have added the ability to make the MCP server use the 'Streamable HTTP' transport mode instead of the traditional 'stdio' transport.

So instead of using the following command (the 'stdio' one):

```
scrapling mcp
```

Use the following to enable 'Streamable HTTP' transport mode:

```
scrapling mcp --http
```

Hence, the default value for the host the server is listening to is '0.0.0.0' and the port is 8000, which both can be configured as below:

```
scrapling mcp --http --host '127.0.0.1' --port 8000
```

## Examples[¶](#examples "Permanent link")

Now we will show you some examples of prompts we used while testing the MCP server, but you are probably more creative than we are and better at prompt engineering than we are :)

We will gradually go from simple prompts to more complex ones. We will use Claude Desktop for the examples, but the same logic applies to the rest, of course.

1. **Basic Web Scraping**

   Extract the main content from a webpage as Markdown:

   ```
   Scrape the main content from https://example.com and convert it to markdown format.
   ```

   Claude will use the `get` tool to fetch the page and return clean, readable content. If it fails, it will continue retrying every second for 3 attempts, unless you instruct it otherwise. If it fails to retrieve content for any reason, such as protection or if it's a dynamic website, it will automatically try the other tools. If Claude didn't do that automatically for some reason, you can add that to the prompt.

   A more optimized version of the same prompt would be:

   ```
   Use regular requests to scrape the main content from https://example.com and convert it to markdown format.
   ```

   This tells Claude which tool to use here, so it doesn't have to guess. Sometimes it will start using normal requests on its own, and at other times, it will assume browsers are better suited for this website without any apparent reason. As a rule of thumb, you should always tell Claude which tool to use to save time and money and get consistent results.
2. **Targeted Data Extraction**

   Extract specific elements using CSS selectors:

   ```
   Get all product titles from https://shop.example.com using the CSS selector '.product-title'. If the request fails, retry up to 5 times every 10 seconds.
   ```

   The server will extract only the elements matching your selector and return them as a structured list. Notice I told it to set the tool to try up to 5 times in case the website has connection issues, but the default setting should be fine for most cases.
3. **E-commerce Data Collection**

   Another example of a bit more complex prompt:

   ```
   Extract product information from these e-commerce URLs using bulk browser fetches:
   - https://shop1.com/product-a
   - https://shop2.com/product-b  
   - https://shop3.com/product-c

   Get the product names, prices, and descriptions from each page.
   ```

   Claude will use `bulk_fetch` to concurrently scrape all URLs, then analyze the extracted data.
4. **More advanced workflow**

   Let's say I want to get all the action games available on PlayStation's store first page right now. I can use the following prompt to do that:

   ```
   Extract the URLs of all games in this page, then do a bulk request to them and return a list of all action games: https://store.playstation.com/en-us/pages/browse
   ```

   Note that I instructed it to use a bulk request for all the URLs collected. If I hadn't mentioned it, sometimes it works as intended, and other times it makes a separate request to each URL, which takes significantly longer. This prompt takes approximately one minute to complete.

   However, because I wasn't specific enough, it actually used the `stealthy_fetch` here and the `bulk_stealthy_fetch` in the second step, which unnecessarily consumed a large number of tokens. A better prompt would be:

   ```
   Use normal requests to extract the URLs of all games in this page, then do a bulk request to them and return a list of all action games: https://store.playstation.com/en-us/pages/browse
   ```

   And if you know how to write CSS selectors, you can instruct Claude to apply the selectors to the elements you want, and it will nearly complete the task immediately.

   ```
   Use normal requests to extract the URLs of all games on the page below, then perform a bulk request to them and return a list of all action games.
   The selector for games in the first page is `[href*="/concept/"]` and the selector for the genre in the second request is `[data-qa="gameInfo#releaseInformation#genre-value"]`.

   URL: https://store.playstation.com/en-us/pages/browse
   ```
5. **Get data from a website with Cloudflare protection**

   If you think the website you are targeting has Cloudflare protection, tell Claude instead of letting it discover it on its own.

   ```
   What's the price of this product? Be cautious, as it utilizes Cloudflare's Turnstile protection. Make the browser visible while you work.

   https://ao.com/product/oo101uk-ninja-woodfire-outdoor-pizza-oven-brown-99357-685.aspx
   ```
6. **Long workflow**

   You can, for example, use a prompt like this:

   ```
   Extract all product URLs for the following category, then return the prices and details for the first 3 products.

   https://www.arnotts.ie/furniture/bedroom/bed-frames/
   ```

   But a better prompt would be:

   ```
   Go to the following category URL and extract all product URLs using the CSS selector "a". Then, fetch the first 3 product pages in parallel and extract each product’s price and details.

   Keep the output in markdown format to reduce irrelevant content.

   Category URL:
   https://www.arnotts.ie/furniture/bedroom/bed-frames/
   ```
7. **Using Persistent Sessions**

   When scraping multiple pages from the same site, use a persistent browser session to avoid the overhead of launching a new browser for each request:

   ```
   Open a stealthy browser session with 5 pages maximum pool, then use it to scrape the main details in bulk from the first 5 product pages on https://shop.example.com. Close the session when you're done.
   ```

   Claude will use `open_session` to create a persistent browser, pass the `session_id` to `bulk_stealthy_fetch` call while opening all pages at the same time, and then call `close_session` at the end. This is significantly faster than launching a new browser for each page.

   Danger

   When using persistent sessions, always remember to close the session after you finish or it will stay open!
8. **Using Persistent Session on a long flow**

   Another long test example that makes Clause think:

   ```
   Use Scrapling MCP to do the following in this order:

   1. Open a stealthy browser session with headless mode off.
   2. Go to this page and collect the number of stars: https://github.com/D4Vinci/Scrapling
   3. From the README, get the URL that shows the number of downloads and go to it.
   4. Get the number of downloads and the top 3 countries from the graph.
   5. Prepare a report with the results.
   6. Close the browser.
   ```

And so on, you get the idea. Your creativity is the key here.

## Best Practices[¶](#best-practices "Permanent link")

Here is some technical advice for you.

### 1. Choose the Right Tool[¶](#1-choose-the-right-tool "Permanent link")

* **`get`**: Fast, simple websites
* **`fetch`**: Sites with JavaScript/dynamic content
* **`stealthy_fetch`**: Protected sites, Cloudflare, anti-bot systems

### 2. Optimize Performance[¶](#2-optimize-performance "Permanent link")

* Use bulk tools for multiple URLs
* Disable unnecessary resources
* Set appropriate timeouts
* Use CSS selectors for targeted extraction

### 3. Handle Dynamic Content[¶](#3-handle-dynamic-content "Permanent link")

* Use `network_idle` for SPAs
* Set `wait_selector` for specific elements
* Increase timeout for slow-loading sites

### 4. Data Quality[¶](#4-data-quality "Permanent link")

* Use `main_content_only=true` to avoid navigation/ads
* Choose an appropriate `extraction_type` for your use case

### 5. Prompt Injection Protection[¶](#5-prompt-injection-protection "Permanent link")

The MCP server automatically sanitizes scraped content when `main_content_only` is enabled (the default). This strips hidden content that malicious websites could use to inject instructions into the AI's context:

* **CSS-hidden elements**: `display:none`, `visibility:hidden`, `opacity:0`, `font-size:0`, `height:0`, `width:0`
* **Accessibility-hidden elements**: `aria-hidden="true"`
* **Template tags**: `<template>` elements
* **HTML comments**: `<!-- ... -->`
* **Zero-width characters**: Invisible unicode characters like zero-width spaces

This protection runs automatically on all MCP tool responses. Keep `main_content_only=true` (the default) for maximum protection.

### 6. Use Sessions for Multiple Requests[¶](#6-use-sessions-for-multiple-requests "Permanent link")

* Use `open_session` to create a persistent browser session when scraping multiple pages
* Pass the `session_id` to `fetch` or `stealthy_fetch` calls to reuse the same browser
* Always close sessions with `close_session` when done to free resources
* Use `list_sessions` to check which sessions are still active
* A `session_id` from a dynamic session can only be used with `fetch`/`bulk_fetch`, and a stealthy session can only be used with `stealthy_fetch`/`bulk_stealthy_fetch`

## Legal and Ethical Considerations[¶](#legal-and-ethical-considerations "Permanent link")

⚠️ **Important Guidelines:**

* **Check robots.txt**: Visit `https://website.com/robots.txt` to see scraping rules
* **Respect rate limits**: Don't overwhelm servers with requests
* **Terms of Service**: Read and comply with website terms
* **Copyright**: Respect intellectual property rights
* **Privacy**: Be mindful of personal data protection laws
* **Commercial use**: Ensure you have permission for business purposes

---

*Built with ❤️ by the Scrapling team. Happy scraping!*

Was this page helpful?

Thanks for your feedback!

Thanks for your feedback! Help us improve this page by
[opening a documentation issue](https://github.com/D4Vinci/Scrapling/issues/new?template=04-docs_issue.yml).


---
## Source: https://scrapling.readthedocs.io/en/latest/tutorials/replacing_ai.html
---

# Scrapling: A Free Alternative to AI for Robust Web Scraping[¶](#scrapling-a-free-alternative-to-ai-for-robust-web-scraping "Permanent link")

Web scraping has long been a vital tool for data extraction, indexing, and preparing datasets, among other purposes. But experienced users often encounter persistent issues that can hinder effectiveness. Recently, there's been a noticeable shift toward AI-based web scraping, driven by its potential to address these challenges.

In this article, we will discuss these common issues, why companies are shifting toward that approach, the problems with that approach, and how scrapling solves them for you without the cost of using AI.

## Common issues and challenging goals[¶](#common-issues-and-challenging-goals "Permanent link")

If you have been doing Web Scraping for a long time, you probably noticed that there are repeating problems with Web Scraping, like:

1. **Rapidly changing website structures** - Sites frequently update their DOM structures, breaking static XPath/CSS selectors.
2. **Unstable selectors** - Class names and IDs often change or use randomly generated values that break scrapers or make scraping these websites difficult.
3. **Increasingly complex anti-bot measures** - CAPTCHA systems, browser fingerprinting, and behavior analysis make traditional scraping difficult
   and others

But that's only if you are doing targeted Web Scraping for known websites, in which case you can write specific code for every website.

If you start thinking about bigger goals like Broad Scraping or Generic Web Scraping, or what you like to call it, then the above issues intensify, and you will face new issues like:

1. **Extreme Website Diversity** - Generic scraping must handle countless variations in HTML structures, CSS usage, JavaScript frameworks, and backend technologies.
2. **Identifying Relevant Data** - How does the scraper know what data is important on a page it has never seen before?
3. **Pagination variations** - Infinite scroll, traditional pagination, "load more" buttons, all requiring different approaches
   and more

How will you solve that manually? I'm referring to generic web scraping of various websites that don't share any common technologies.

## AI to the rescue, but at a high cost[¶](#ai-to-the-rescue-but-at-a-high-cost "Permanent link")

Of course, AI can easily solve most of these issues because it can understand the page source and identify the fields you want or create selectors for them. That's, of course, if you already solved the anti-bot measures through other tools :)

This approach is, of course, beautiful. I love AI and find it very fascinating, especially Generative AI. You will probably spend a lot of time on prompt engineering and tweaking the prompts, but if that's cool with you, you will soon hit the real issue with using AI here.

Most websites have vast amounts of content per page, which you will need to pass to the AI somehow so it can do its magic. This will burn through tokens like fire in a haystack, quickly accumulating high costs.

Unless money is irrelevant to you, you will try to find less expensive approaches, and that's where Scrapling comes into play ![😄](https://cdn.jsdelivr.net/gh/jdecked/twemoji@16.0.1/assets/svg/1f604.svg ":smile:")

## Scrapling got you covered[¶](#scrapling-got-you-covered "Permanent link")

Scrapling can handle almost all issues you will face during Web Scraping, and the following updates will cover the rest carefully.

### Solving issue T1: Rapidly changing website structures[¶](#solving-issue-t1-rapidly-changing-website-structures "Permanent link")

That's why the [adaptive](https://scrapling.readthedocs.io/en/latest/parsing/adaptive.html) feature was made. You knew I would talk about it, and here we are :)

While Web Scraping, if you have the `adaptive` feature enabled, you can save any element's unique properties so you can find it again later when the website's structure changes. The most frustrating thing about changes is that anything about an element can change, so there's nothing to rely on.

That's how the adaptive feature works: it stores everything unique about an element. When the website structure changes, it returns the element with the highest similarity score of the previous element.

I have already explained this in more detail, with many examples. Read more from [here](https://scrapling.readthedocs.io/en/latest/parsing/adaptive.html#how-the-adaptive-feature-works).

### Solving issue T2: Unstable selectors[¶](#solving-issue-t2-unstable-selectors "Permanent link")

If you have been doing Web scraping for a long enough time, you have likely experienced this once. I'm referring to a website that employs poor design patterns, built on raw HTML without any IDs/classes, or uses random class names with nothing else to rely on, etc...

In these cases, standard selection methods with CSS/XPath selectors won't be optimal, and that's why Scrapling provides three more methods for Selection:

1. [Selection by element content](https://scrapling.readthedocs.io/en/latest/parsing/selection.html#text-content-selection): Through text content (`find_by_text`) or regex that matches text content (`find_by_regex`)
2. [Selecting elements similar to another element](https://scrapling.readthedocs.io/en/latest/parsing/selection.html#finding-similar-elements): You find an element, and we will do the rest!
3. [Selecting elements by filters](https://scrapling.readthedocs.io/en/latest/parsing/selection.html#filters-based-searching): You specify conditions/filters that this element must fulfill, we find it!

There is no need to explain any of these; click on the links, and it will be clear how Scrapling solves this.

### Solving issue T3: Increasingly complex anti-bot measures[¶](#solving-issue-t3-increasingly-complex-anti-bot-measures "Permanent link")

It's well known that creating an undetectable spider requires more than residential/mobile proxies and human-like behavior. It also needs a hard-to-detect browser, which Scrapling provides two main options to solve:

1. [DynamicFetcher](https://scrapling.readthedocs.io/en/latest/fetching/dynamic.html) - This fetcher provides flexible browser automation with multiple configuration options and little under-the-hood stealth improvements.
2. [StealthyFetcher](https://scrapling.readthedocs.io/en/latest/fetching/stealthy.html) - Because we live in a harsh world and you need to take [full measure instead of half-measures](https://www.youtube.com/watch?v=7BE4QcwX4dU), `StealthyFetcher` was born. This fetcher uses our stealthy browser -- a version of [DynamicFetcher](https://scrapling.readthedocs.io/en/latest/fetching/dynamic.html) that nearly bypasses all annoying anti-protections, provides tools to handle the rest, and automatically bypasses all types of Cloudflare's Turnstile/Interstitial!

We keep improving these two with each update, so stay tuned :)

### Solving issues B1 & B2: Extreme Website Diversity / Identifying Relevant Data[¶](#solving-issues-b1-b2-extreme-website-diversity-identifying-relevant-data "Permanent link")

This one is tough to handle, but Scrapling's flexibility makes it possible.

I talked with someone who uses AI to extract prices from different websites. He is only interested in prices and titles, so he uses AI to find the price for him.

I told him you don't need to use AI here and gave this code as an example

```
price_element = page.find_by_regex(r'£[\d\.,]+', first_match=True)  # Get the first element that contains a text that matches price regex eg. £10.50
# If you want the container/element that contains the price element
price_element_container = price_element.parent or price_element.find_ancestor(lambda ancestor: ancestor.has_class('product'))  # or other methods...
target_element_selector = price_element_container.generate_css_selector or price_element_container.generate_full_css_selector # or xpath
```

Then he said What about cases like this:

```
<span class='currency'> $ </span> <span class='a-price'> 45,000 </span>
```

So, I updated the code like this

```
price_element_container = page.find_by_regex(r'[\d,]+', first_match=True).parent # Adjusted the regex for this example
full_price_data = price_element_container.get_all_text(strip=True)  # Returns '$45,000' in this case
```

This was enough for his use case. You can use the first regex, and if it doesn't find anything, use the following regex, and so on. Try to cover the most common patterns first, then the less common ones, and so on.
It will be a bit boring, but it's definitely less expensive than AI.

This example illustrates the point I aim to convey here. Not every challenge will need AI to be solved, but sometimes you need to be creative, and that might save you a lot of money.

### Solving issue B3: Pagination variations[¶](#solving-issue-b3-pagination-variations "Permanent link")

This issue, Scrapling currently doesn't have a direct method to automatically extract pagination's URLs for you, but it will be added with the upcoming updates :)

But you can handle most websites if you search for the most common patterns with `page.find_by_text('Next')['href']` or `page.find_by_text('load more')['href']` or selectors like `'a[href*="?page="]'` or `'a[href*="/page/"]'` - you get the idea.

## Cost Comparison and Savings[¶](#cost-comparison-and-savings "Permanent link")

For a quick comparison.

| Aspect | Scrapling | AI-Based Tools (e.g., Browse AI, Oxylabs) |
| --- | --- | --- |
| Cost Structure | Likely free or low-cost, no per-use fees | Starts at $19/month (Browse AI) to $49/month (Oxylabs), scales with usage |
| Setup Effort | Requires little technical expertise, manual setup | Often no-code, easier for non-technical users |
| Usage options | Through code, terminal, or MCP server. | Often through GUI or API, depending on the option the company is providing |
| Scalability | Depends on user implementation | Built-in support for large-scale, managed services |
| Adaptability | High with features like `adaptive` and the non-selectors selection methods | High, automatic with AI, but costly for frequent changes |

This table is based on pricing from [Browse AI Pricing](https://www.browse.ai/pricing) and [Oxylabs Web Scraper API Pricing](https://oxylabs.io/products/scraper-api/web/pricing)

## Conclusion[¶](#conclusion "Permanent link")

While AI offers powerful capabilities, its cost can be prohibitive for many Web scraping tasks. Scrapling provides a robust, flexible, and cost-effective toolkit for tackling the real-world challenges of both targeted and broad scraping, often eliminating the need for expensive AI solutions. You can build resilient scrapers more efficiently by leveraging features like `adaptive`, diverse selection methods, and advanced fetchers.

Explore the documentation further and see how Scrapling can simplify your future Web Scraping projects!

Was this page helpful?

Thanks for your feedback!

Thanks for your feedback! Help us improve this page by
[opening a documentation issue](https://github.com/D4Vinci/Scrapling/issues/new?template=04-docs_issue.yml).


---
## Source: https://scrapling.readthedocs.io/en/latest/tutorials/migrating_from_beautifulsoup.html
---

# Migrating from BeautifulSoup to Scrapling[¶](#migrating-from-beautifulsoup-to-scrapling "Permanent link")

If you're already familiar with BeautifulSoup, you're in for a treat. Scrapling is much faster, provides the same parsing capabilities as BS, adds additional parsing capabilities not found in BS, and introduces powerful new features for fetching and handling modern web pages. This guide will help you quickly adapt your existing BeautifulSoup code to leverage Scrapling's capabilities.

Below is a table that covers the most common operations you'll perform when scraping web pages. Each row illustrates how to achieve a specific task using BeautifulSoup and the corresponding method in Scrapling.

You will notice that some shortcuts in BeautifulSoup are missing in Scrapling, which is one of the reasons BeautifulSoup is slower than Scrapling. The point is: If the same feature can be used in a short one-liner, there is no need to sacrifice performance to shorten that short line :)

| Task | BeautifulSoup Code | Scrapling Code |
| --- | --- | --- |
| Parser import | `from bs4 import BeautifulSoup` | `from scrapling.parser import Selector` |
| Parsing HTML from string | `soup = BeautifulSoup(html, 'html.parser')` | `page = Selector(html)` |
| Finding a single element | `element = soup.find('div', class_='example')` | `element = page.find('div', class_='example')` |
| Finding multiple elements | `elements = soup.find_all('div', class_='example')` | `elements = page.find_all('div', class_='example')` |
| Finding a single element (Example 2) | `element = soup.find('div', attrs={"class": "example"})` | `element = page.find('div', {"class": "example"})` |
| Finding a single element (Example 3) | `element = soup.find(re.compile("^b"))` | `element = page.find(re.compile("^b"))` `element = page.find_by_regex(r"^b")` |
| Finding a single element (Example 4) | `element = soup.find(lambda e: len(list(e.children)) > 0)` | `element = page.find(lambda e: len(e.children) > 0)` |
| Finding a single element (Example 5) | `element = soup.find(["a", "b"])` | `element = page.find(["a", "b"])` |
| Find element by its text content | `element = soup.find(text="some text")` | `element = page.find_by_text("some text", partial=False)` |
| Using CSS selectors to find the first matching element | `elements = soup.select_one('div.example')` | `elements = page.css('div.example').first` |
| Using CSS selectors to find all matching element | `elements = soup.select('div.example')` | `elements = page.css('div.example')` |
| Get a prettified version of the page/element source | `prettified = soup.prettify()` | `prettified = page.prettify()` |
| Get a Non-pretty version of the page/element source | `source = str(soup)` | `source = page.html_content` |
| Get tag name of an element | `name = element.name` | `name = element.tag` |
| Extracting text content of an element | `string = element.string` | `string = element.text` |
| Extracting all the text in a document or beneath a tag | `text = soup.get_text(strip=True)` | `text = page.get_all_text(strip=True)` |
| Access the dictionary of attributes | `attrs = element.attrs` | `attrs = element.attrib` |
| Extracting attributes | `attr = element['href']` | `attr = element['href']` |
| Navigating to parent | `parent = element.parent` | `parent = element.parent` |
| Get all parents of an element | `parents = list(element.parents)` | `parents = list(element.iterancestors())` |
| Searching for an element in the parents of an element | `target_parent = element.find_parent("a")` | `target_parent = element.find_ancestor(lambda p: p.tag == 'a')` |
| Get all siblings of an element | N/A | `siblings = element.siblings` |
| Get next sibling of an element | `next_element = element.next_sibling` | `next_element = element.next` |
| Searching for an element in the siblings of an element | `target_sibling = element.find_next_sibling("a")` `target_sibling = element.find_previous_sibling("a")` | `target_sibling = element.siblings.search(lambda s: s.tag == 'a')` |
| Searching for elements in the siblings of an element | `target_sibling = element.find_next_siblings("a")` `target_sibling = element.find_previous_siblings("a")` | `target_sibling = element.siblings.filter(lambda s: s.tag == 'a')` |
| Searching for an element in the next elements of an element | `target_parent = element.find_next("a")` | `target_parent = element.below_elements.search(lambda p: p.tag == 'a')` |
| Searching for elements in the next elements of an element | `target_parent = element.find_all_next("a")` | `target_parent = element.below_elements.filter(lambda p: p.tag == 'a')` |
| Searching for an element in the ancestors of an element | `target_parent = element.find_previous("a")` ¹ | `target_parent = element.path.search(lambda p: p.tag == 'a')` |
| Searching for elements in the ancestors of an element | `target_parent = element.find_all_previous("a")` ¹ | `target_parent = element.path.filter(lambda p: p.tag == 'a')` |
| Get previous sibling of an element | `prev_element = element.previous_sibling` | `prev_element = element.previous` |
| Navigating to children | `children = list(element.children)` | `children = element.children` |
| Get all descendants of an element | `children = list(element.descendants)` | `children = element.below_elements` |
| Filtering a group of elements that satisfies a condition | `group = soup.find('p', 'story').css.filter('a')` | `group = page.find_all('p', 'story').filter(lambda p: p.tag == 'a')` |

¹ **Note:** BS4's `find_previous`/`find_all_previous` searches all preceding elements in document order, while Scrapling's `path` only returns ancestors (the parent chain). These are not exact equivalents, but ancestor search covers the most common use case.

**One key point to remember**: BeautifulSoup offers features for modifying and manipulating the page after it has been parsed. Scrapling focuses more on scraping the page faster for you, and then you can do what you want with the extracted information. So, two different tools can be used in Web Scraping, but one of them specializes in Web Scraping :)

### Putting It All Together[¶](#putting-it-all-together "Permanent link")

Here's a simple example of scraping a web page to extract all the links using BeautifulSoup and Scrapling.

**With BeautifulSoup:**

```
import requests
from bs4 import BeautifulSoup

url = 'https://example.com'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

links = soup.find_all('a')
for link in links:
    print(link['href'])
```

**With Scrapling:**

```
from scrapling import Fetcher

url = 'https://example.com'
page = Fetcher.get(url)

links = page.css('a::attr(href)')
for link in links:
    print(link)
```

As you can see, Scrapling simplifies the process by combining fetching and parsing into a single step, making your code cleaner and more efficient.

**Additional Notes:**

* **Different parsers**: BeautifulSoup allows you to set the parser engine to use, and one of them is `lxml`. Scrapling doesn't do that and uses the `lxml` library by default for performance reasons.
* **Element Types**: In BeautifulSoup, elements are `Tag` objects; in Scrapling, they are `Selector` objects. However, they provide similar methods and properties for navigation and data extraction.
* **Error Handling**: Both libraries return `None` when an element is not found (e.g., `soup.find()` or `page.find()`). In Scrapling, `page.css()` returns an empty `Selectors` list when no elements match, and you can use `page.css('.foo').first` to safely get the first match or `None`. To avoid errors, check for `None` or empty results before accessing properties.
* **Text Extraction**: Scrapling provides additional methods for handling text through `TextHandler`, such as `clean()`, which can help remove extra whitespace, consecutive spaces, or unwanted characters. Please check out the documentation for the complete list.

The documentation provides more details on Scrapling's features and the complete list of arguments that can be passed to all methods.

This guide should make your transition from BeautifulSoup to Scrapling smooth and straightforward. Happy scraping!

Was this page helpful?

Thanks for your feedback!

Thanks for your feedback! Help us improve this page by
[opening a documentation issue](https://github.com/D4Vinci/Scrapling/issues/new?template=04-docs_issue.yml).


---
## Source: https://scrapling.readthedocs.io/en/latest/api-reference/selector.html
---

# Selector Class[¶](#selector-class "Permanent link")

The `Selector` class is the core parsing engine in Scrapling that provides HTML parsing and element selection capabilities.

Here's the reference information for the `Selector` class, with all its parameters, attributes, and methods.

You can import the `Selector` class directly from `scrapling`:

```
from scrapling.parser import Selector
```

## scrapling.parser.Selector [¶](#scrapling.parser.Selector "Permanent link")

```
Selector(
    content=None,
    url="",
    encoding="utf-8",
    huge_tree=True,
    root=None,
    keep_comments=False,
    keep_cdata=False,
    adaptive=False,
    _storage=None,
    storage=SQLiteStorageSystem,
    storage_args=None,
    **_
)
```

Bases: `SelectorsGeneration`

```
              flowchart TD
              scrapling.parser.Selector[Selector]
              scrapling.core.mixins.SelectorsGeneration[SelectorsGeneration]

                              scrapling.core.mixins.SelectorsGeneration --> scrapling.parser.Selector
                


              click scrapling.parser.Selector href "" "scrapling.parser.Selector"
              click scrapling.core.mixins.SelectorsGeneration href "" "scrapling.core.mixins.SelectorsGeneration"
```

The main class that works as a wrapper for the HTML input data. Using this class, you can search for elements
with expressions in CSS, XPath, or with simply text. Check the docs for more info.

Here we try to extend module `lxml.html.HtmlElement` while maintaining a simpler interface, We are not
inheriting from the `lxml.html.HtmlElement` because it's not pickleable, which makes a lot of reference jobs
not possible. You can test it here and see code explodes with `AssertionError: invalid Element proxy at...`.
It's an old issue with lxml, see `this entry <https://bugs.launchpad.net/lxml/+bug/736708>`

| PARAMETER | DESCRIPTION |
| --- | --- |
| `content` | HTML content as either string or bytes.  **TYPE:** `Optional[str | bytes]`  **DEFAULT:** `None` |
| `url` | It allows storing a URL with the HTML data for retrieving later.  **TYPE:** `str`  **DEFAULT:** `''` |
| `encoding` | The encoding type that will be used in HTML parsing, default is `UTF-8`  **TYPE:** `str`  **DEFAULT:** `'utf-8'` |
| `huge_tree` | Enabled by default, should always be enabled when parsing large HTML documents. This controls the libxml2 feature that forbids parsing certain large documents to protect from possible memory exhaustion.  **TYPE:** `bool`  **DEFAULT:** `True` |
| `root` | Used internally to pass etree objects instead of text/body arguments, it takes the highest priority. Don't use it unless you know what you are doing!  **TYPE:** `Optional[HtmlElement]`  **DEFAULT:** `None` |
| `keep_comments` | While parsing the HTML body, drop comments or not. Disabled by default for obvious reasons  **TYPE:** `Optional[bool]`  **DEFAULT:** `False` |
| `keep_cdata` | While parsing the HTML body, drop cdata or not. Disabled by default for cleaner HTML.  **TYPE:** `Optional[bool]`  **DEFAULT:** `False` |
| `adaptive` | Globally turn off the adaptive feature in all functions, this argument takes higher priority over all adaptive related arguments/functions in the class.  **TYPE:** `Optional[bool]`  **DEFAULT:** `False` |
| `storage` | The storage class to be passed for adaptive functionalities, see `Docs` for more info.  **TYPE:** `Any`  **DEFAULT:** `SQLiteStorageSystem` |
| `storage_args` | A dictionary of `argument->value` pairs to be passed for the storage class. If empty, default values will be used.  **TYPE:** `Optional[Dict]`  **DEFAULT:** `None` |

Source code in `scrapling/parser.py`

|  |  |
| --- | --- |
| ```  80  81  82  83  84  85  86  87  88  89  90  91  92  93  94  95  96  97  98  99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 ``` | ``` def __init__(     self,     content: Optional[str | bytes] = None,     url: str = "",     encoding: str = "utf-8",     huge_tree: bool = True,     root: Optional[HtmlElement] = None,     keep_comments: Optional[bool] = False,     keep_cdata: Optional[bool] = False,     adaptive: Optional[bool] = False,     _storage: Optional[StorageSystemMixin] = None,     storage: Any = SQLiteStorageSystem,     storage_args: Optional[Dict] = None,     **_, ):     """The main class that works as a wrapper for the HTML input data. Using this class, you can search for elements     with expressions in CSS, XPath, or with simply text. Check the docs for more info.      Here we try to extend module ``lxml.html.HtmlElement`` while maintaining a simpler interface, We are not     inheriting from the ``lxml.html.HtmlElement`` because it's not pickleable, which makes a lot of reference jobs     not possible. You can test it here and see code explodes with `AssertionError: invalid Element proxy at...`.     It's an old issue with lxml, see `this entry <https://bugs.launchpad.net/lxml/+bug/736708>`      :param content: HTML content as either string or bytes.     :param url: It allows storing a URL with the HTML data for retrieving later.     :param encoding: The encoding type that will be used in HTML parsing, default is `UTF-8`     :param huge_tree: Enabled by default, should always be enabled when parsing large HTML documents. This controls          the libxml2 feature that forbids parsing certain large documents to protect from possible memory exhaustion.     :param root: Used internally to pass etree objects instead of text/body arguments, it takes the highest priority.         Don't use it unless you know what you are doing!     :param keep_comments: While parsing the HTML body, drop comments or not. Disabled by default for obvious reasons     :param keep_cdata: While parsing the HTML body, drop cdata or not. Disabled by default for cleaner HTML.     :param adaptive: Globally turn off the adaptive feature in all functions, this argument takes higher         priority over all adaptive related arguments/functions in the class.     :param storage: The storage class to be passed for adaptive functionalities, see ``Docs`` for more info.     :param storage_args: A dictionary of ``argument->value`` pairs to be passed for the storage class.         If empty, default values will be used.     """     if root is None and content is None:         raise ValueError("Selector class needs HTML content, or root arguments to work")      self.url = url     self._raw_body: str | bytes = ""     self.encoding = encoding     self.__keep_cdata = keep_cdata     self.__huge_tree_enabled = huge_tree     self.__keep_comments = keep_comments     # For selector stuff     self.__text: Optional[TextHandler] = None     self.__attributes: Optional[AttributesHandler] = None     self.__tag: Optional[str] = None     self._storage: Optional[StorageSystemMixin] = None     if root is None:         body: str | bytes         if isinstance(content, str):             body = content.strip().replace("\x00", "") or "<html/>"         elif isinstance(content, bytes):             body = content.replace(b"\x00", b"")         else:             raise TypeError(f"content argument must be str or bytes, got {type(content)}")          # https://lxml.de/api/lxml.etree.HTMLParser-class.html         _parser_kwargs: Dict[str, Any] = dict(             recover=True,             remove_blank_text=True,             remove_comments=(not keep_comments),             encoding=encoding,             compact=True,             huge_tree=huge_tree,             default_doctype=True,  # Supported by lxml but missing from stubs             strip_cdata=(not keep_cdata),         )         parser = HTMLParser(**_parser_kwargs)         self._root = cast(HtmlElement, fromstring(body or "<html/>", parser=parser, base_url=url or ""))         self._raw_body = content      else:         self._root = cast(HtmlElement, root)          if self._is_text_node(root):             self.__adaptive_enabled = False             return      self.__adaptive_enabled = bool(adaptive)      if self.__adaptive_enabled:         if _storage is not None:             self._storage = _storage         else:             if not storage_args:                 storage_args = {                     "storage_file": __DEFAULT_DB_FILE__,                     "url": url,                 }              if not hasattr(storage, "__wrapped__"):                 raise ValueError("Storage class must be wrapped with lru_cache decorator, see docs for info")              if not issubclass(storage.__wrapped__, StorageSystemMixin):  # pragma: no cover                 raise ValueError("Storage system must be inherited from class `StorageSystemMixin`")              self._storage = storage(**storage_args) ``` |

### __slots__ `class-attribute` `instance-attribute` [¶](#scrapling.parser.Selector.__slots__ "Permanent link")

```
__slots__ = (
    "url",
    "encoding",
    "__adaptive_enabled",
    "_root",
    "_storage",
    "__keep_comments",
    "__huge_tree_enabled",
    "__attributes",
    "__text",
    "__tag",
    "__keep_cdata",
    "_raw_body",
)
```

### url `instance-attribute` [¶](#scrapling.parser.Selector.url "Permanent link")

```
url = url
```

### encoding `instance-attribute` [¶](#scrapling.parser.Selector.encoding "Permanent link")

```
encoding = encoding
```

### tag `property` [¶](#scrapling.parser.Selector.tag "Permanent link")

```
tag
```

Get the tag name of the element

### text `property` [¶](#scrapling.parser.Selector.text "Permanent link")

```
text
```

Get text content of the element

### attrib `property` [¶](#scrapling.parser.Selector.attrib "Permanent link")

```
attrib
```

Get attributes of the element

### html_content `property` [¶](#scrapling.parser.Selector.html_content "Permanent link")

```
html_content
```

Return the inner HTML code of the element

### body `property` [¶](#scrapling.parser.Selector.body "Permanent link")

```
body
```

Return the raw body of the current `Selector` without any processing. Useful for binary and non-HTML requests.

### parent `property` [¶](#scrapling.parser.Selector.parent "Permanent link")

```
parent
```

Return the direct parent of the element or `None` otherwise

### below_elements `property` [¶](#scrapling.parser.Selector.below_elements "Permanent link")

```
below_elements
```

Return all elements under the current element in the DOM tree

### children `property` [¶](#scrapling.parser.Selector.children "Permanent link")

```
children
```

Return the children elements of the current element or empty list otherwise

### siblings `property` [¶](#scrapling.parser.Selector.siblings "Permanent link")

```
siblings
```

Return other children of the current element's parent or empty list otherwise

### path `property` [¶](#scrapling.parser.Selector.path "Permanent link")

```
path
```

Returns a list of type `Selectors` that contains the path leading to the current element from the root.

### next `property` [¶](#scrapling.parser.Selector.next "Permanent link")

```
next
```

Returns the next element of the current element in the children of the parent or `None` otherwise.

### previous `property` [¶](#scrapling.parser.Selector.previous "Permanent link")

```
previous
```

Returns the previous element of the current element in the children of the parent or `None` otherwise.

### extract `class-attribute` `instance-attribute` [¶](#scrapling.parser.Selector.extract "Permanent link")

```
extract = getall
```

### extract_first `class-attribute` `instance-attribute` [¶](#scrapling.parser.Selector.extract_first "Permanent link")

```
extract_first = get
```

### generate_css_selector `property` [¶](#scrapling.parser.Selector.generate_css_selector "Permanent link")

```
generate_css_selector
```

Generate a CSS selector for the current element

| RETURNS | DESCRIPTION |
| --- | --- |
| `str` | A string of the generated selector. |

### generate_full_css_selector `property` [¶](#scrapling.parser.Selector.generate_full_css_selector "Permanent link")

```
generate_full_css_selector
```

Generate a complete CSS selector for the current element

| RETURNS | DESCRIPTION |
| --- | --- |
| `str` | A string of the generated selector. |

### generate_xpath_selector `property` [¶](#scrapling.parser.Selector.generate_xpath_selector "Permanent link")

```
generate_xpath_selector
```

Generate an XPath selector for the current element

| RETURNS | DESCRIPTION |
| --- | --- |
| `str` | A string of the generated selector. |

### generate_full_xpath_selector `property` [¶](#scrapling.parser.Selector.generate_full_xpath_selector "Permanent link")

```
generate_full_xpath_selector
```

Generate a complete XPath selector for the current element

| RETURNS | DESCRIPTION |
| --- | --- |
| `str` | A string of the generated selector. |

### __getitem__ [¶](#scrapling.parser.Selector.__getitem__ "Permanent link")

```
__getitem__(key)
```

Source code in `scrapling/parser.py`

|  |  |
| --- | --- |
| ``` 183 184 185 186 ``` | ``` def __getitem__(self, key: str) -> TextHandler:     if self._is_text_node(self._root):         raise TypeError("Text nodes do not have attributes")     return self.attrib[key] ``` |

### __contains__ [¶](#scrapling.parser.Selector.__contains__ "Permanent link")

```
__contains__(key)
```

Source code in `scrapling/parser.py`

|  |  |
| --- | --- |
| ``` 188 189 190 191 ``` | ``` def __contains__(self, key: str) -> bool:     if self._is_text_node(self._root):         return False     return key in self.attrib ``` |

### __getstate__ [¶](#scrapling.parser.Selector.__getstate__ "Permanent link")

```
__getstate__()
```

Source code in `scrapling/parser.py`

|  |  |
| --- | --- |
| ``` 250 251 252 ``` | ``` def __getstate__(self) -> Any:     # lxml don't like it :)     raise TypeError("Can't pickle Selector objects") ``` |

### get_all_text [¶](#scrapling.parser.Selector.get_all_text "Permanent link")

```
get_all_text(
    separator="\n",
    strip=False,
    ignore_tags=("script", "style"),
    valid_values=True,
)
```

Get all child strings of this element, concatenated using the given separator.

| PARAMETER | DESCRIPTION |
| --- | --- |
| `separator` | Strings will be concatenated using this separator.  **TYPE:** `str`  **DEFAULT:** `'\n'` |
| `strip` | If True, strings will be stripped before being concatenated.  **TYPE:** `bool`  **DEFAULT:** `False` |
| `ignore_tags` | A tuple of all tag names you want to ignore  **TYPE:** `Tuple`  **DEFAULT:** `('script', 'style')` |
| `valid_values` | If enabled, elements with text-content that is empty or only whitespaces will be ignored  **TYPE:** `bool`  **DEFAULT:** `True` |

| RETURNS | DESCRIPTION |
| --- | --- |
| `TextHandler` | A TextHandler |

Source code in `scrapling/parser.py`

|  |  |
| --- | --- |
| ``` 279 280 281 282 283 284 285 286 287 288 289 290 291 292 293 294 295 296 297 298 299 300 301 302 303 304 305 306 307 308 309 310 311 312 313 314 315 316 317 318 319 320 321 322 323 324 325 326 327 328 329 ``` | ``` def get_all_text(     self,     separator: str = "\n",     strip: bool = False,     ignore_tags: Tuple = (         "script",         "style",     ),     valid_values: bool = True, ) -> TextHandler:     """Get all child strings of this element, concatenated using the given separator.      :param separator: Strings will be concatenated using this separator.     :param strip: If True, strings will be stripped before being concatenated.     :param ignore_tags: A tuple of all tag names you want to ignore     :param valid_values: If enabled, elements with text-content that is empty or only whitespaces will be ignored      :return: A TextHandler     """     if self._is_text_node(self._root):         return TextHandler(str(self._root))      ignored_elements: set[Any] = set()     if ignore_tags:         ignored_elements.update(self._root.iter(*ignore_tags))      _all_strings = []      def append_text(text: str) -> None:         processed_text = text.strip() if strip else text         if not valid_values or processed_text.strip():             _all_strings.append(processed_text)      def is_visible_text_node(text_node: _ElementUnicodeResult) -> bool:         parent = text_node.getparent()         if parent is None:             return False          owner = parent.getparent() if text_node.is_tail else parent         while owner is not None:             if owner in ignored_elements:                 return False             owner = owner.getparent()         return True      for text_node in cast(list[_ElementUnicodeResult], _find_all_text_nodes(self._root)):         text = str(text_node)         if text and is_visible_text_node(text_node):             append_text(text)      return cast(TextHandler, TextHandler(separator).join(_all_strings)) ``` |

### urljoin [¶](#scrapling.parser.Selector.urljoin "Permanent link")

```
urljoin(relative_url)
```

Join this Selector's url with a relative url to form an absolute full URL.

Source code in `scrapling/parser.py`

|  |  |
| --- | --- |
| ``` 331 332 333 ``` | ``` def urljoin(self, relative_url: str) -> str:     """Join this Selector's url with a relative url to form an absolute full URL."""     return urljoin(self.url, relative_url) ``` |

### prettify [¶](#scrapling.parser.Selector.prettify "Permanent link")

```
prettify()
```

Return a prettified version of the element's inner html-code

Source code in `scrapling/parser.py`

|  |  |
| --- | --- |
| ``` 361 362 363 364 365 366 367 368 369 370 371 372 373 374 ``` | ``` def prettify(self) -> TextHandler:     """Return a prettified version of the element's inner html-code"""     if self._is_text_node(self._root):         return TextHandler(str(self._root))     content = tostring(         self._root,         encoding=self.encoding,         pretty_print=True,         method="html",         with_tail=False,     )     if isinstance(content, bytes):         content = content.strip().decode(self.encoding)     return TextHandler(content) ``` |

### has_class [¶](#scrapling.parser.Selector.has_class "Permanent link")

```
has_class(class_name)
```

Check if the element has a specific class

| PARAMETER | DESCRIPTION |
| --- | --- |
| `class_name` | The class name to check for  **TYPE:** `str` |

| RETURNS | DESCRIPTION |
| --- | --- |
| `bool` | True if element has class with that name otherwise False |

Source code in `scrapling/parser.py`

|  |  |
| --- | --- |
| ``` 376 377 378 379 380 381 382 383 ``` | ``` def has_class(self, class_name: str) -> bool:     """Check if the element has a specific class     :param class_name: The class name to check for     :return: True if element has class with that name otherwise False     """     if self._is_text_node(self._root):         return False     return class_name in self._root.classes ``` |

### iterancestors [¶](#scrapling.parser.Selector.iterancestors "Permanent link")

```
iterancestors()
```

Return a generator that loops over all ancestors of the element, starting with the element's parent.

Source code in `scrapling/parser.py`

|  |  |
| --- | --- |
| ``` 417 418 419 420 421 422 ``` | ``` def iterancestors(self) -> Generator["Selector", None, None]:     """Return a generator that loops over all ancestors of the element, starting with the element's parent."""     if self._is_text_node(self._root):         return     for ancestor in self._root.iterancestors():         yield self.__element_convertor(ancestor) ``` |

### find_ancestor [¶](#scrapling.parser.Selector.find_ancestor "Permanent link")

```
find_ancestor(func)
```

Loop over all ancestors of the element till one match the passed function

| PARAMETER | DESCRIPTION |
| --- | --- |
| `func` | A function that takes each ancestor as an argument and returns True/False  **TYPE:** `Callable[[Selector], bool]` |

| RETURNS | DESCRIPTION |
| --- | --- |
| `Optional[Selector]` | The first ancestor that match the function or `None` otherwise. |

Source code in `scrapling/parser.py`

|  |  |
| --- | --- |
| ``` 424 425 426 427 428 429 430 431 432 ``` | ``` def find_ancestor(self, func: Callable[["Selector"], bool]) -> Optional["Selector"]:     """Loop over all ancestors of the element till one match the passed function     :param func: A function that takes each ancestor as an argument and returns True/False     :return: The first ancestor that match the function or ``None`` otherwise.     """     for ancestor in self.iterancestors():         if func(ancestor):             return ancestor     return None ``` |

### get [¶](#scrapling.parser.Selector.get "Permanent link")

```
get()
```

Serialize this element to a string.
For text nodes, returns the text value. For HTML elements, returns the outer HTML.

Source code in `scrapling/parser.py`

|  |  |
| --- | --- |
| ``` 464 465 466 467 468 469 470 471 ``` | ``` def get(self) -> TextHandler:     """     Serialize this element to a string.     For text nodes, returns the text value. For HTML elements, returns the outer HTML.     """     if self._is_text_node(self._root):         return TextHandler(str(self._root))     return self.html_content ``` |

### getall [¶](#scrapling.parser.Selector.getall "Permanent link")

```
getall()
```

Return a single-element list containing this element's serialized string.

Source code in `scrapling/parser.py`

|  |  |
| --- | --- |
| ``` 473 474 475 ``` | ``` def getall(self) -> TextHandlers:     """Return a single-element list containing this element's serialized string."""     return TextHandlers([self.get()]) ``` |

### __str__ [¶](#scrapling.parser.Selector.__str__ "Permanent link")

```
__str__()
```

Source code in `scrapling/parser.py`

|  |  |
| --- | --- |
| ``` 480 481 482 483 ``` | ``` def __str__(self) -> str:     if self._is_text_node(self._root):         return str(self._root)     return self.html_content ``` |

### __repr__ [¶](#scrapling.parser.Selector.__repr__ "Permanent link")

```
__repr__()
```

Source code in `scrapling/parser.py`

|  |  |
| --- | --- |
| ``` 485 486 487 488 489 490 491 492 493 494 495 496 497 498 499 500 501 502 503 504 505 506 ``` | ``` def __repr__(self) -> str:     length_limit = 40      if self._is_text_node(self._root):         text = str(self._root)         if len(text) > length_limit:             text = text[:length_limit].strip() + "..."         return f"<text='{text}'>"      content = clean_spaces(self.html_content)     if len(content) > length_limit:         content = content[:length_limit].strip() + "..."     data = f"<data='{content}'"      if self.parent:         parent_content = clean_spaces(self.parent.html_content)         if len(parent_content) > length_limit:             parent_content = parent_content[:length_limit].strip() + "..."          data += f" parent='{parent_content}'"      return data + ">" ``` |

### relocate [¶](#scrapling.parser.Selector.relocate "Permanent link")

```
relocate(element, percentage=0, selector_type=False)
```

This function will search again for the element in the page tree, used automatically on page structure change

| PARAMETER | DESCRIPTION |
| --- | --- |
| `element` | The element we want to relocate in the tree  **TYPE:** `Union[Dict, HtmlElement, Selector]` |
| `percentage` | The minimum percentage to accept and not going lower than that. Be aware that the percentage calculation depends solely on the page structure, so don't play with this number unless you must know what you are doing!  **TYPE:** `int`  **DEFAULT:** `0` |
| `selector_type` | If True, the return result will be converted to `Selectors` object  **TYPE:** `bool`  **DEFAULT:** `False` |

| RETURNS | DESCRIPTION |
| --- | --- |
| `Union[List[HtmlElement], Selectors]` | List of pure HTML elements that got the highest matching score or 'Selectors' object |

Source code in `scrapling/parser.py`

|  |  |
| --- | --- |
| ``` 519 520 521 522 523 524 525 526 527 528 529 530 531 532 533 534 535 536 537 538 539 540 541 542 543 544 545 546 547 548 549 550 551 552 553 554 555 556 557 558 559 560 561 562 ``` | ``` def relocate(     self,     element: Union[Dict, HtmlElement, "Selector"],     percentage: int = 0,     selector_type: bool = False, ) -> Union[List[HtmlElement], "Selectors"]:     """This function will search again for the element in the page tree, used automatically on page structure change      :param element: The element we want to relocate in the tree     :param percentage: The minimum percentage to accept and not going lower than that. Be aware that the percentage      calculation depends solely on the page structure, so don't play with this number unless you must know      what you are doing!     :param selector_type: If True, the return result will be converted to `Selectors` object     :return: List of pure HTML elements that got the highest matching score or 'Selectors' object     """     score_table: Dict[float, List[Any]] = {}     # Note: `element` will most likely always be a dictionary at this point.     if isinstance(element, self.__class__):         element = element._root      if issubclass(type(element), HtmlElement):         element = _StorageTools.element_to_dict(element)      for node in cast(List, _find_all_elements(self._root)):         # Collect all elements in the page, then for each element get the matching score of it against the node.         # Hence: the code doesn't stop even if the score was 100%         # because there might be another element(s) left in page with the same score         score = self.__calculate_similarity_score(cast(Dict, element), node)         score_table.setdefault(score, []).append(node)      if score_table:         highest_probability = max(score_table.keys())         if score_table[highest_probability] and highest_probability >= percentage:             if log.getEffectiveLevel() < 20:                 # No need to execute this part if the logging level is not debugging                 log.debug(f"Highest probability was {highest_probability}%")                 log.debug("Top 5 best matching elements are: ")                 for percent in tuple(sorted(score_table.keys(), reverse=True))[:5]:                     log.debug(f"{percent} -> {self.__elements_convertor(score_table[percent])}")              if not selector_type:                 return score_table[highest_probability]             return self.__elements_convertor(score_table[highest_probability])     return [] ``` |

### css [¶](#scrapling.parser.Selector.css "Permanent link")

```
css(
    selector,
    identifier="",
    adaptive=False,
    auto_save=False,
    percentage=0,
)
```

Search the current tree with CSS3 selectors

**Important:
It's recommended to use the identifier argument if you plan to use a different selector later
and want to relocate the same element(s)**

| PARAMETER | DESCRIPTION |
| --- | --- |
| `selector` | The CSS3 selector to be used.  **TYPE:** `str` |
| `adaptive` | Enabled will make the function try to relocate the element if it was 'saved' before  **TYPE:** `bool`  **DEFAULT:** `False` |
| `identifier` | A string that will be used to save/retrieve element's data in adaptive, otherwise the selector will be used.  **TYPE:** `str`  **DEFAULT:** `''` |
| `auto_save` | Automatically save new elements for `adaptive` later  **TYPE:** `bool`  **DEFAULT:** `False` |
| `percentage` | The minimum percentage to accept while `adaptive` is working and not going lower than that. Be aware that the percentage calculation depends solely on the page structure, so don't play with this number unless you must know what you are doing!  **TYPE:** `int`  **DEFAULT:** `0` |

| RETURNS | DESCRIPTION |
| --- | --- |
| `Selectors` | `Selectors` class. |

Source code in `scrapling/parser.py`

|  |  |
| --- | --- |
| ``` 564 565 566 567 568 569 570 571 572 573 574 575 576 577 578 579 580 581 582 583 584 585 586 587 588 589 590 591 592 593 594 595 596 597 598 599 600 601 602 603 604 605 606 607 608 609 610 611 612 613 614 615 616 617 618 619 620 621 622 ``` | ``` def css(     self,     selector: str,     identifier: str = "",     adaptive: bool = False,     auto_save: bool = False,     percentage: int = 0, ) -> "Selectors":     """Search the current tree with CSS3 selectors      **Important:     It's recommended to use the identifier argument if you plan to use a different selector later     and want to relocate the same element(s)**      :param selector: The CSS3 selector to be used.     :param adaptive: Enabled will make the function try to relocate the element if it was 'saved' before     :param identifier: A string that will be used to save/retrieve element's data in adaptive,      otherwise the selector will be used.     :param auto_save: Automatically save new elements for `adaptive` later     :param percentage: The minimum percentage to accept while `adaptive` is working and not going lower than that.      Be aware that the percentage calculation depends solely on the page structure, so don't play with this      number unless you must know what you are doing!      :return: `Selectors` class.     """     if self._is_text_node(self._root):         return Selectors()      try:         if not self.__adaptive_enabled or "," not in selector:             # No need to split selectors in this case, let's save some CPU cycles :)             xpath_selector = _css_to_xpath(selector)             return self.xpath(                 xpath_selector,                 identifier or selector,                 adaptive,                 auto_save,                 percentage,             )          results = Selectors()         for single_selector in split_selectors(selector):             # I'm doing this only so the `save` function saves data correctly for combined selectors             # Like using the ',' to combine two different selectors that point to different elements.             xpath_selector = _css_to_xpath(single_selector.canonical())             results += self.xpath(                 xpath_selector,                 identifier or single_selector.canonical(),                 adaptive,                 auto_save,                 percentage,             )          return Selectors(results)     except (         SelectorError,         SelectorSyntaxError,     ) as e:         raise SelectorSyntaxError(f"Invalid CSS selector '{selector}': {str(e)}") from e ``` |

### xpath [¶](#scrapling.parser.Selector.xpath "Permanent link")

```
xpath(
    selector,
    identifier="",
    adaptive=False,
    auto_save=False,
    percentage=0,
    **kwargs
)
```

Search the current tree with XPath selectors

**Important:
It's recommended to use the identifier argument if you plan to use a different selector later
and want to relocate the same element(s)**

Note: **Additional keyword arguments will be passed as XPath variables in the XPath expression!**

| PARAMETER | DESCRIPTION |
| --- | --- |
| `selector` | The XPath selector to be used.  **TYPE:** `str` |
| `adaptive` | Enabled will make the function try to relocate the element if it was 'saved' before  **TYPE:** `bool`  **DEFAULT:** `False` |
| `identifier` | A string that will be used to save/retrieve element's data in adaptive, otherwise the selector will be used.  **TYPE:** `str`  **DEFAULT:** `''` |
| `auto_save` | Automatically save new elements for `adaptive` later  **TYPE:** `bool`  **DEFAULT:** `False` |
| `percentage` | The minimum percentage to accept while `adaptive` is working and not going lower than that. Be aware that the percentage calculation depends solely on the page structure, so don't play with this number unless you must know what you are doing!  **TYPE:** `int`  **DEFAULT:** `0` |

| RETURNS | DESCRIPTION |
| --- | --- |
| `Selectors` | `Selectors` class. |

Source code in `scrapling/parser.py`

|  |  |
| --- | --- |
| ``` 624 625 626 627 628 629 630 631 632 633 634 635 636 637 638 639 640 641 642 643 644 645 646 647 648 649 650 651 652 653 654 655 656 657 658 659 660 661 662 663 664 665 666 667 668 669 670 671 672 673 674 675 676 677 678 679 680 681 682 683 684 685 686 687 688 689 690 691 692 ``` | ``` def xpath(     self,     selector: str,     identifier: str = "",     adaptive: bool = False,     auto_save: bool = False,     percentage: int = 0,     **kwargs: Any, ) -> "Selectors":     """Search the current tree with XPath selectors      **Important:     It's recommended to use the identifier argument if you plan to use a different selector later     and want to relocate the same element(s)**       Note: **Additional keyword arguments will be passed as XPath variables in the XPath expression!**      :param selector: The XPath selector to be used.     :param adaptive: Enabled will make the function try to relocate the element if it was 'saved' before     :param identifier: A string that will be used to save/retrieve element's data in adaptive,      otherwise the selector will be used.     :param auto_save: Automatically save new elements for `adaptive` later     :param percentage: The minimum percentage to accept while `adaptive` is working and not going lower than that.      Be aware that the percentage calculation depends solely on the page structure, so don't play with this      number unless you must know what you are doing!      :return: `Selectors` class.     """     if self._is_text_node(self._root):         return Selectors()      try:         if elements := self._root.xpath(selector, **kwargs):             if not self.__adaptive_enabled and auto_save:                 log.warning(                     "Argument `auto_save` will be ignored because `adaptive` wasn't enabled on initialization. Check docs for more info."                 )             elif self.__adaptive_enabled and auto_save:                 self.save(elements[0], identifier or selector)              return self.__handle_elements(elements)         elif self.__adaptive_enabled:             if adaptive:                 element_data = self.retrieve(identifier or selector)                 if element_data:                     elements = self.relocate(element_data, percentage)                     if elements is not None and auto_save:                         self.save(elements[0], identifier or selector)              return self.__handle_elements(elements)         else:             if adaptive:                 log.warning(                     "Argument `adaptive` will be ignored because `adaptive` wasn't enabled on initialization. Check docs for more info."                 )             elif auto_save:                 log.warning(                     "Argument `auto_save` will be ignored because `adaptive` wasn't enabled on initialization. Check docs for more info."                 )              return self.__handle_elements(elements)      except (         SelectorError,         SelectorSyntaxError,         XPathError,         XPathEvalError,     ) as e:         raise SelectorSyntaxError(f"Invalid XPath selector: {selector}") from e ``` |

### find_all [¶](#scrapling.parser.Selector.find_all "Permanent link")

```
find_all(*args, **kwargs)
```

Find elements by filters of your creations for ease.

| PARAMETER | DESCRIPTION |
| --- | --- |
| `args` | Tag name(s), iterable of tag names, regex patterns, function, or a dictionary of elements' attributes. Leave empty for selecting all.  **TYPE:** `str | Iterable[str] | Pattern | Callable | Dict[str, str]`  **DEFAULT:** `()` |
| `kwargs` | The attributes you want to filter elements based on it.  **TYPE:** `str`  **DEFAULT:** `{}` |

| RETURNS | DESCRIPTION |
| --- | --- |
| `Selectors` | The `Selectors` object of the elements or empty list |

Source code in `scrapling/parser.py`

|  |  |
| --- | --- |
| ``` 694 695 696 697 698 699 700 701 702 703 704 705 706 707 708 709 710 711 712 713 714 715 716 717 718 719 720 721 722 723 724 725 726 727 728 729 730 731 732 733 734 735 736 737 738 739 740 741 742 743 744 745 746 747 748 749 750 751 752 753 754 755 756 757 758 759 760 761 762 763 764 765 766 767 768 769 770 771 772 773 774 775 776 777 778 779 780 781 782 783 784 785 786 ``` | ``` def find_all(     self,     *args: str | Iterable[str] | Pattern | Callable | Dict[str, str],     **kwargs: str, ) -> "Selectors":     """Find elements by filters of your creations for ease.      :param args: Tag name(s), iterable of tag names, regex patterns, function, or a dictionary of elements' attributes. Leave empty for selecting all.     :param kwargs: The attributes you want to filter elements based on it.     :return: The `Selectors` object of the elements or empty list     """     if self._is_text_node(self._root):         return Selectors()      if not args and not kwargs:         raise TypeError("You have to pass something to search with, like tag name(s), tag attributes, or both.")      attributes: Dict[str, Any] = dict()     tags: Set[str] = set()     patterns: Set[Pattern] = set()     results, functions, selectors = Selectors(), [], []      # Brace yourself for a wonderful journey!     for arg in args:         if isinstance(arg, str):             tags.add(arg)          elif type(arg) in (list, tuple, set):             arg = cast(Iterable, arg)  # Type narrowing for type checkers like pyright             if not all(map(lambda x: isinstance(x, str), arg)):                 raise TypeError("Nested Iterables are not accepted, only iterables of tag names are accepted")             tags.update(set(arg))          elif isinstance(arg, dict):             if not all([(isinstance(k, str) and isinstance(v, str)) for k, v in arg.items()]):                 raise TypeError(                     "Nested dictionaries are not accepted, only string keys and string values are accepted"                 )             attributes.update(arg)          elif isinstance(arg, re_Pattern):             patterns.add(arg)          elif callable(arg):             if len(signature(arg).parameters) > 0:                 functions.append(arg)             else:                 raise TypeError(                     "Callable filter function must have at least one argument to take `Selector` objects."                 )          else:             raise TypeError(f'Argument with type "{type(arg)}" is not accepted, please read the docs.')      if not all([(isinstance(k, str) and isinstance(v, str)) for k, v in kwargs.items()]):         raise TypeError("Only string values are accepted for arguments")      for attribute_name, value in kwargs.items():         # Only replace names for kwargs, replacing them in dictionaries doesn't make sense         attribute_name = _whitelisted.get(attribute_name, attribute_name)         attributes[attribute_name] = value      # It's easier and faster to build a selector than traversing the tree     tags = tags or set("*")     for tag in tags:         selector = tag         for key, value in attributes.items():             value = value.replace('"', r"\"")  # Escape double quotes in user input             # Not escaping anything with the key so the user can pass patterns like {'href*': '/p/'} or get errors :)             selector += '[{}="{}"]'.format(key, value)         if selector != "*":             selectors.append(selector)      if selectors:         results = cast(Selectors, self.css(", ".join(selectors)))         if results:             # From the results, get the ones that fulfill passed regex patterns             for pattern in patterns:                 results = results.filter(lambda e: e.text.re(pattern, check_match=True))              # From the results, get the ones that fulfill passed functions             for function in functions:                 results = results.filter(function)     else:         results = results or self.below_elements         for pattern in patterns:             results = results.filter(lambda e: e.text.re(pattern, check_match=True))          # Collect an element if it fulfills the passed function otherwise         for function in functions:             results = results.filter(function)      return results ``` |

### find [¶](#scrapling.parser.Selector.find "Permanent link")

```
find(*args, **kwargs)
```

Find elements by filters of your creations for ease, then return the first result. Otherwise return `None`.

| PARAMETER | DESCRIPTION |
| --- | --- |
| `args` | Tag name(s), iterable of tag names, regex patterns, function, or a dictionary of elements' attributes. Leave empty for selecting all.  **TYPE:** `str | Iterable[str] | Pattern | Callable | Dict[str, str]`  **DEFAULT:** `()` |
| `kwargs` | The attributes you want to filter elements based on it.  **TYPE:** `str`  **DEFAULT:** `{}` |

| RETURNS | DESCRIPTION |
| --- | --- |
| `Optional[Selector]` | The `Selector` object of the element or `None` if the result didn't match |

Source code in `scrapling/parser.py`

|  |  |
| --- | --- |
| ``` 788 789 790 791 792 793 794 795 796 797 798 799 800 801 ``` | ``` def find(     self,     *args: str | Iterable[str] | Pattern | Callable | Dict[str, str],     **kwargs: str, ) -> Optional["Selector"]:     """Find elements by filters of your creations for ease, then return the first result. Otherwise return `None`.      :param args: Tag name(s), iterable of tag names, regex patterns, function, or a dictionary of elements' attributes. Leave empty for selecting all.     :param kwargs: The attributes you want to filter elements based on it.     :return: The `Selector` object of the element or `None` if the result didn't match     """     for element in self.find_all(*args, **kwargs):         return element     return None ``` |

### save [¶](#scrapling.parser.Selector.save "Permanent link")

```
save(element, identifier)
```

Saves the element's unique properties to the storage for retrieval and relocation later

| PARAMETER | DESCRIPTION |
| --- | --- |
| `element` | The element itself that we want to save to storage, it can be a `Selector` or pure `HtmlElement`  **TYPE:** `HtmlElement` |
| `identifier` | This is the identifier that will be used to retrieve the element later from the storage. See the docs for more info.  **TYPE:** `str` |

Source code in `scrapling/parser.py`

|  |  |
| --- | --- |
| ``` 877 878 879 880 881 882 883 884 885 886 887 888 889 890 891 892 893 894 895 896 ``` | ``` def save(self, element: HtmlElement, identifier: str) -> None:     """Saves the element's unique properties to the storage for retrieval and relocation later      :param element: The element itself that we want to save to storage, it can be a ` Selector ` or pure ` HtmlElement `     :param identifier: This is the identifier that will be used to retrieve the element later from the storage. See         the docs for more info.     """     if self.__adaptive_enabled and self._storage:         target_element: Any = element         if isinstance(target_element, self.__class__):             target_element = target_element._root          if self._is_text_node(target_element):             target_element = target_element.getparent()          self._storage.save(target_element, identifier)     else:         raise RuntimeError(             "Can't use `adaptive` features while it's disabled globally, you have to start a new class instance."         ) ``` |

### retrieve [¶](#scrapling.parser.Selector.retrieve "Permanent link")

```
retrieve(identifier)
```

Using the identifier, we search the storage and return the unique properties of the element

| PARAMETER | DESCRIPTION |
| --- | --- |
| `identifier` | This is the identifier that will be used to retrieve the element from the storage. See the docs for more info.  **TYPE:** `str` |

| RETURNS | DESCRIPTION |
| --- | --- |
| `Optional[Dict[str, Any]]` | A dictionary of the unique properties |

Source code in `scrapling/parser.py`

|  |  |
| --- | --- |
| ``` 898 899 900 901 902 903 904 905 906 907 908 909 910 ``` | ``` def retrieve(self, identifier: str) -> Optional[Dict[str, Any]]:     """Using the identifier, we search the storage and return the unique properties of the element      :param identifier: This is the identifier that will be used to retrieve the element from the storage. See         the docs for more info.     :return: A dictionary of the unique properties     """     if self.__adaptive_enabled and self._storage:         return self._storage.retrieve(identifier)      raise RuntimeError(         "Can't use `adaptive` features while it's disabled globally, you have to start a new class instance."     ) ``` |

### json [¶](#scrapling.parser.Selector.json "Permanent link")

```
json()
```

Return JSON response if the response is jsonable otherwise throws error

Source code in `scrapling/parser.py`

|  |  |
| --- | --- |
| ``` 913 914 915 916 917 918 919 920 921 922 923 924 925 926 927 ``` | ``` def json(self) -> Dict:     """Return JSON response if the response is jsonable otherwise throws error"""     if self._is_text_node(self._root):         return TextHandler(str(self._root)).json()     if self._raw_body and isinstance(self._raw_body, (str, bytes)):         if isinstance(self._raw_body, str):             return TextHandler(self._raw_body).json()         else:             if TYPE_CHECKING:                 assert isinstance(self._raw_body, bytes)             return TextHandler(self._raw_body.decode()).json()     elif self.text:         return self.text.json()     else:         return self.get_all_text(strip=True).json() ``` |

### re [¶](#scrapling.parser.Selector.re "Permanent link")

```
re(
    regex,
    replace_entities=True,
    clean_match=False,
    case_sensitive=True,
)
```

Apply the given regex to the current text and return a list of strings with the matches.

| PARAMETER | DESCRIPTION |
| --- | --- |
| `regex` | Can be either a compiled regular expression or a string.  **TYPE:** `str | Pattern[str]` |
| `replace_entities` | If enabled character entity references are replaced by their corresponding character  **TYPE:** `bool`  **DEFAULT:** `True` |
| `clean_match` | if enabled, this will ignore all whitespaces and consecutive spaces while matching  **TYPE:** `bool`  **DEFAULT:** `False` |
| `case_sensitive` | if disabled, the function will set the regex to ignore the letters case while compiling it  **TYPE:** `bool`  **DEFAULT:** `True` |

Source code in `scrapling/parser.py`

|  |  |
| --- | --- |
| ``` 929 930 931 932 933 934 935 936 937 938 939 940 941 942 943 ``` | ``` def re(     self,     regex: str | Pattern[str],     replace_entities: bool = True,     clean_match: bool = False,     case_sensitive: bool = True, ) -> TextHandlers:     """Apply the given regex to the current text and return a list of strings with the matches.      :param regex: Can be either a compiled regular expression or a string.     :param replace_entities: If enabled character entity references are replaced by their corresponding character     :param clean_match: if enabled, this will ignore all whitespaces and consecutive spaces while matching     :param case_sensitive: if disabled, the function will set the regex to ignore the letters case while compiling it     """     return self.text.re(regex, replace_entities, clean_match, case_sensitive) ``` |

### re_first [¶](#scrapling.parser.Selector.re_first "Permanent link")

```
re_first(
    regex,
    default=None,
    replace_entities=True,
    clean_match=False,
    case_sensitive=True,
)
```

Apply the given regex to text and return the first match if found, otherwise return the default value.

| PARAMETER | DESCRIPTION |
| --- | --- |
| `regex` | Can be either a compiled regular expression or a string.  **TYPE:** `str | Pattern[str]` |
| `default` | The default value to be returned if there is no match  **DEFAULT:** `None` |
| `replace_entities` | if enabled character entity references are replaced by their corresponding character  **TYPE:** `bool`  **DEFAULT:** `True` |
| `clean_match` | if enabled, this will ignore all whitespaces and consecutive spaces while matching  **TYPE:** `bool`  **DEFAULT:** `False` |
| `case_sensitive` | if disabled, the function will set the regex to ignore the letters case while compiling it  **TYPE:** `bool`  **DEFAULT:** `True` |

Source code in `scrapling/parser.py`

|  |  |
| --- | --- |
| ``` 945 946 947 948 949 950 951 952 953 954 955 956 957 958 959 960 961 ``` | ``` def re_first(     self,     regex: str | Pattern[str],     default=None,     replace_entities: bool = True,     clean_match: bool = False,     case_sensitive: bool = True, ) -> TextHandler:     """Apply the given regex to text and return the first match if found, otherwise return the default value.      :param regex: Can be either a compiled regular expression or a string.     :param default: The default value to be returned if there is no match     :param replace_entities: if enabled character entity references are replaced by their corresponding character     :param clean_match: if enabled, this will ignore all whitespaces and consecutive spaces while matching     :param case_sensitive: if disabled, the function will set the regex to ignore the letters case while compiling it     """     return self.text.re_first(regex, default, replace_entities, clean_match, case_sensitive) ``` |

### find_similar [¶](#scrapling.parser.Selector.find_similar "Permanent link")

```
find_similar(
    similarity_threshold=0.2,
    ignore_attributes=("href", "src"),
    match_text=False,
)
```

Find elements that are in the same tree depth in the page with the same tag name and same parent tag etc...
then return the ones that match the current element attributes with a percentage higher than the input threshold.

This function is inspired by AutoScraper and made for cases where you, for example, found a product div inside
a products-list container and want to find other products using that element as a starting point EXCEPT
this function works in any case without depending on the element type.

| PARAMETER | DESCRIPTION |
| --- | --- |
| `similarity_threshold` | The percentage to use while comparing element attributes. Note: Elements found before attributes matching/comparison will be sharing the same depth, same tag name, same parent tag name, and same grand parent tag name. So they are 99% likely to be correct unless you are extremely unlucky, then attributes matching comes into play, so don't play with this number unless you are getting the results you don't want. Also, if the current element doesn't have attributes and the similar element as well, then it's a 100% match.  **TYPE:** `float`  **DEFAULT:** `0.2` |
| `ignore_attributes` | Attribute names passed will be ignored while matching the attributes in the last step. The default value is to ignore `href` and `src` as URLs can change a lot between elements, so it's unreliable  **TYPE:** `List | Tuple`  **DEFAULT:** `('href', 'src')` |
| `match_text` | If True, element text content will be taken into calculation while matching. Not recommended to use in normal cases, but it depends.  **TYPE:** `bool`  **DEFAULT:** `False` |

| RETURNS | DESCRIPTION |
| --- | --- |
| `Selectors` | A `Selectors` container of `Selector` objects or empty list |

Source code in `scrapling/parser.py`

|  |  |
| --- | --- |
| ``` 1009 1010 1011 1012 1013 1014 1015 1016 1017 1018 1019 1020 1021 1022 1023 1024 1025 1026 1027 1028 1029 1030 1031 1032 1033 1034 1035 1036 1037 1038 1039 1040 1041 1042 1043 1044 1045 1046 1047 1048 1049 1050 1051 1052 1053 1054 1055 1056 1057 1058 1059 1060 1061 1062 1063 1064 1065 1066 1067 1068 ``` | ``` def find_similar(     self,     similarity_threshold: float = 0.2,     ignore_attributes: List | Tuple = (         "href",         "src",     ),     match_text: bool = False, ) -> "Selectors":     """Find elements that are in the same tree depth in the page with the same tag name and same parent tag etc...     then return the ones that match the current element attributes with a percentage higher than the input threshold.      This function is inspired by AutoScraper and made for cases where you, for example, found a product div inside     a products-list container and want to find other products using that element as a starting point EXCEPT     this function works in any case without depending on the element type.      :param similarity_threshold: The percentage to use while comparing element attributes.         Note: Elements found before attributes matching/comparison will be sharing the same depth, same tag name,         same parent tag name, and same grand parent tag name. So they are 99% likely to be correct unless you are         extremely unlucky, then attributes matching comes into play, so don't play with this number unless         you are getting the results you don't want.         Also, if the current element doesn't have attributes and the similar element as well, then it's a 100% match.     :param ignore_attributes: Attribute names passed will be ignored while matching the attributes in the last step.         The default value is to ignore `href` and `src` as URLs can change a lot between elements, so it's unreliable     :param match_text: If True, element text content will be taken into calculation while matching.         Not recommended to use in normal cases, but it depends.      :return: A ``Selectors`` container of ``Selector`` objects or empty list     """     if self._is_text_node(self._root):         return Selectors()      # We will use the elements' root from now on to get the speed boost of using Lxml directly     root = self._root     similar_elements = list()      current_depth = len(list(root.iterancestors()))     target_attrs = self.__get_attributes(root, ignore_attributes) if ignore_attributes else root.attrib      path_parts = [self.tag]     if (parent := root.getparent()) is not None:         path_parts.insert(0, parent.tag)         if (grandparent := parent.getparent()) is not None:             path_parts.insert(0, grandparent.tag)      xpath_path = "//{}".format("/".join(path_parts))     potential_matches = root.xpath(f"{xpath_path}[count(ancestor::*) = {current_depth}]")      for potential_match in potential_matches:         if potential_match != root and self.__are_alike(             root,             target_attrs,             potential_match,             ignore_attributes,             similarity_threshold,             match_text,         ):             similar_elements.append(potential_match)      return Selectors(map(self.__element_convertor, similar_elements)) ``` |

### find_by_text [¶](#scrapling.parser.Selector.find_by_text "Permanent link")

```
find_by_text(
    text,
    first_match=True,
    partial=False,
    case_sensitive=False,
    clean_match=True,
)
```

Find elements that its text content fully/partially matches input.

| PARAMETER | DESCRIPTION |
| --- | --- |
| `text` | Text query to match  **TYPE:** `str` |
| `first_match` | Returns the first element that matches conditions, enabled by default  **TYPE:** `bool`  **DEFAULT:** `True` |
| `partial` | If enabled, the function returns elements that contain the input text  **TYPE:** `bool`  **DEFAULT:** `False` |
| `case_sensitive` | if enabled, the letters case will be taken into consideration  **TYPE:** `bool`  **DEFAULT:** `False` |
| `clean_match` | if enabled, this will ignore all whitespaces and consecutive spaces while matching  **TYPE:** `bool`  **DEFAULT:** `True` |

Source code in `scrapling/parser.py`

|  |  |
| --- | --- |
| ``` 1090 1091 1092 1093 1094 1095 1096 1097 1098 1099 1100 1101 1102 1103 1104 1105 1106 1107 1108 1109 1110 1111 1112 1113 1114 1115 1116 1117 1118 1119 1120 1121 1122 1123 1124 1125 1126 1127 1128 1129 1130 1131 1132 1133 1134 1135 1136 ``` | ``` def find_by_text(     self,     text: str,     first_match: bool = True,     partial: bool = False,     case_sensitive: bool = False,     clean_match: bool = True, ) -> Union["Selectors", "Selector"]:     """Find elements that its text content fully/partially matches input.     :param text: Text query to match     :param first_match: Returns the first element that matches conditions, enabled by default     :param partial: If enabled, the function returns elements that contain the input text     :param case_sensitive: if enabled, the letters case will be taken into consideration     :param clean_match: if enabled, this will ignore all whitespaces and consecutive spaces while matching     """     if self._is_text_node(self._root):         return Selectors()      results = Selectors()     if not case_sensitive:         text = text.lower()      possible_targets = cast(List, _find_all_elements_with_spaces(self._root))     if possible_targets:         for node in self.__elements_convertor(possible_targets):             """Check if element matches given text otherwise, traverse the children tree and iterate"""             node_text: TextHandler = node.text             if clean_match:                 node_text = TextHandler(node_text.clean())              if not case_sensitive:                 node_text = TextHandler(node_text.lower())              if partial:                 if text in node_text:                     results.append(node)             elif text == node_text:                 results.append(node)              if first_match and results:                 # we got an element so we should stop                 break          if first_match:             if results:                 return results[0]     return results ``` |

### find_by_regex [¶](#scrapling.parser.Selector.find_by_regex "Permanent link")

```
find_by_regex(
    query,
    first_match=True,
    case_sensitive=False,
    clean_match=True,
)
```

Find elements that its text content matches the input regex pattern.

| PARAMETER | DESCRIPTION |
| --- | --- |
| `query` | Regex query/pattern to match  **TYPE:** `str | Pattern[str]` |
| `first_match` | Return the first element that matches conditions; enabled by default.  **TYPE:** `bool`  **DEFAULT:** `True` |
| `case_sensitive` | If enabled, the letters case will be taken into consideration in the regex.  **TYPE:** `bool`  **DEFAULT:** `False` |
| `clean_match` | If enabled, this will ignore all whitespaces and consecutive spaces while matching.  **TYPE:** `bool`  **DEFAULT:** `True` |

Source code in `scrapling/parser.py`

|  |  |
| --- | --- |
| ``` 1156 1157 1158 1159 1160 1161 1162 1163 1164 1165 1166 1167 1168 1169 1170 1171 1172 1173 1174 1175 1176 1177 1178 1179 1180 1181 1182 1183 1184 1185 1186 1187 1188 1189 1190 1191 1192 1193 ``` | ``` def find_by_regex(     self,     query: str | Pattern[str],     first_match: bool = True,     case_sensitive: bool = False,     clean_match: bool = True, ) -> Union["Selectors", "Selector"]:     """Find elements that its text content matches the input regex pattern.     :param query: Regex query/pattern to match     :param first_match: Return the first element that matches conditions; enabled by default.     :param case_sensitive: If enabled, the letters case will be taken into consideration in the regex.     :param clean_match: If enabled, this will ignore all whitespaces and consecutive spaces while matching.     """     if self._is_text_node(self._root):         return Selectors()      results = Selectors()      possible_targets = cast(List, _find_all_elements_with_spaces(self._root))     if possible_targets:         for node in self.__elements_convertor(possible_targets):             """Check if element matches given regex otherwise, traverse the children tree and iterate"""             node_text = node.text             if node_text.re(                 query,                 check_match=True,                 clean_match=clean_match,                 case_sensitive=case_sensitive,             ):                 results.append(node)              if first_match and results:                 # we got an element so we should stop                 break          if results and first_match:             return results[0]     return results ``` |

## scrapling.parser.Selectors [¶](#scrapling.parser.Selectors "Permanent link")

Bases: `List[Selector]`

```
              flowchart TD
              scrapling.parser.Selectors[Selectors]

              

              click scrapling.parser.Selectors href "" "scrapling.parser.Selectors"
```

The `Selectors` class is a subclass of the builtin `List` class, which provides a few additional methods.

### __slots__ `class-attribute` `instance-attribute` [¶](#scrapling.parser.Selectors.__slots__ "Permanent link")

```
__slots__ = ()
```

### extract `class-attribute` `instance-attribute` [¶](#scrapling.parser.Selectors.extract "Permanent link")

```
extract = getall
```

### extract_first `class-attribute` `instance-attribute` [¶](#scrapling.parser.Selectors.extract_first "Permanent link")

```
extract_first = get
```

### first `property` [¶](#scrapling.parser.Selectors.first "Permanent link")

```
first
```

Returns the first Selector item of the current list or `None` if the list is empty

### last `property` [¶](#scrapling.parser.Selectors.last "Permanent link")

```
last
```

Returns the last Selector item of the current list or `None` if the list is empty

### length `property` [¶](#scrapling.parser.Selectors.length "Permanent link")

```
length
```

Returns the length of the current list

### __getitem__ [¶](#scrapling.parser.Selectors.__getitem__ "Permanent link")

```
__getitem__(pos)
```

Source code in `scrapling/parser.py`

|  |  |
| --- | --- |
| ``` 1211 1212 1213 1214 1215 1216 ``` | ``` def __getitem__(self, pos: SupportsIndex | slice) -> Union[Selector, "Selectors"]:     lst = super().__getitem__(pos)     if isinstance(pos, slice):         return self.__class__(cast(List[Selector], lst))     else:         return cast(Selector, lst) ``` |

### xpath [¶](#scrapling.parser.Selectors.xpath "Permanent link")

```
xpath(
    selector,
    identifier="",
    auto_save=False,
    percentage=0,
    **kwargs
)
```

Call the `.xpath()` method for each element in this list and return
their results as another `Selectors` class.

**Important:
It's recommended to use the identifier argument if you plan to use a different selector later
and want to relocate the same element(s)**

Note: **Additional keyword arguments will be passed as XPath variables in the XPath expression!**

| PARAMETER | DESCRIPTION |
| --- | --- |
| `selector` | The XPath selector to be used.  **TYPE:** `str` |
| `identifier` | A string that will be used to retrieve element's data in adaptive, otherwise the selector will be used.  **TYPE:** `str`  **DEFAULT:** `''` |
| `auto_save` | Automatically save new elements for `adaptive` later  **TYPE:** `bool`  **DEFAULT:** `False` |
| `percentage` | The minimum percentage to accept while `adaptive` is working and not going lower than that. Be aware that the percentage calculation depends solely on the page structure, so don't play with this number unless you must know what you are doing!  **TYPE:** `int`  **DEFAULT:** `0` |

| RETURNS | DESCRIPTION |
| --- | --- |
| `Selectors` | `Selectors` class. |

Source code in `scrapling/parser.py`

|  |  |
| --- | --- |
| ``` 1218 1219 1220 1221 1222 1223 1224 1225 1226 1227 1228 1229 1230 1231 1232 1233 1234 1235 1236 1237 1238 1239 1240 1241 1242 1243 1244 1245 1246 1247 ``` | ``` def xpath(     self,     selector: str,     identifier: str = "",     auto_save: bool = False,     percentage: int = 0,     **kwargs: Any, ) -> "Selectors":     """     Call the ``.xpath()`` method for each element in this list and return     their results as another `Selectors` class.      **Important:     It's recommended to use the identifier argument if you plan to use a different selector later     and want to relocate the same element(s)**       Note: **Additional keyword arguments will be passed as XPath variables in the XPath expression!**      :param selector: The XPath selector to be used.     :param identifier: A string that will be used to retrieve element's data in adaptive,      otherwise the selector will be used.     :param auto_save: Automatically save new elements for `adaptive` later     :param percentage: The minimum percentage to accept while `adaptive` is working and not going lower than that.      Be aware that the percentage calculation depends solely on the page structure, so don't play with this      number unless you must know what you are doing!      :return: `Selectors` class.     """     results = [n.xpath(selector, identifier or selector, False, auto_save, percentage, **kwargs) for n in self]     return self.__class__(flatten(results)) ``` |

### css [¶](#scrapling.parser.Selectors.css "Permanent link")

```
css(selector, identifier='', auto_save=False, percentage=0)
```

Call the `.css()` method for each element in this list and return
their results flattened as another `Selectors` class.

**Important:
It's recommended to use the identifier argument if you plan to use a different selector later
and want to relocate the same element(s)**

| PARAMETER | DESCRIPTION |
| --- | --- |
| `selector` | The CSS3 selector to be used.  **TYPE:** `str` |
| `identifier` | A string that will be used to retrieve element's data in adaptive, otherwise the selector will be used.  **TYPE:** `str`  **DEFAULT:** `''` |
| `auto_save` | Automatically save new elements for `adaptive` later  **TYPE:** `bool`  **DEFAULT:** `False` |
| `percentage` | The minimum percentage to accept while `adaptive` is working and not going lower than that. Be aware that the percentage calculation depends solely on the page structure, so don't play with this number unless you must know what you are doing!  **TYPE:** `int`  **DEFAULT:** `0` |

| RETURNS | DESCRIPTION |
| --- | --- |
| `Selectors` | `Selectors` class. |

Source code in `scrapling/parser.py`

|  |  |
| --- | --- |
| ``` 1249 1250 1251 1252 1253 1254 1255 1256 1257 1258 1259 1260 1261 1262 1263 1264 1265 1266 1267 1268 1269 1270 1271 1272 1273 1274 1275 ``` | ``` def css(     self,     selector: str,     identifier: str = "",     auto_save: bool = False,     percentage: int = 0, ) -> "Selectors":     """     Call the ``.css()`` method for each element in this list and return     their results flattened as another `Selectors` class.      **Important:     It's recommended to use the identifier argument if you plan to use a different selector later     and want to relocate the same element(s)**      :param selector: The CSS3 selector to be used.     :param identifier: A string that will be used to retrieve element's data in adaptive,      otherwise the selector will be used.     :param auto_save: Automatically save new elements for `adaptive` later     :param percentage: The minimum percentage to accept while `adaptive` is working and not going lower than that.      Be aware that the percentage calculation depends solely on the page structure, so don't play with this      number unless you must know what you are doing!      :return: `Selectors` class.     """     results = [n.css(selector, identifier or selector, False, auto_save, percentage) for n in self]     return self.__class__(flatten(results)) ``` |

### re [¶](#scrapling.parser.Selectors.re "Permanent link")

```
re(
    regex,
    replace_entities=True,
    clean_match=False,
    case_sensitive=True,
)
```

Call the `.re()` method for each element in this list and return
their results flattened as List of TextHandler.

| PARAMETER | DESCRIPTION |
| --- | --- |
| `regex` | Can be either a compiled regular expression or a string.  **TYPE:** `str | Pattern` |
| `replace_entities` | If enabled character entity references are replaced by their corresponding character  **TYPE:** `bool`  **DEFAULT:** `True` |
| `clean_match` | if enabled, this will ignore all whitespaces and consecutive spaces while matching  **TYPE:** `bool`  **DEFAULT:** `False` |
| `case_sensitive` | if disabled, the function will set the regex to ignore the letters case while compiling it  **TYPE:** `bool`  **DEFAULT:** `True` |

Source code in `scrapling/parser.py`

|  |  |
| --- | --- |
| ``` 1277 1278 1279 1280 1281 1282 1283 1284 1285 1286 1287 1288 1289 1290 1291 1292 1293 ``` | ``` def re(     self,     regex: str | Pattern,     replace_entities: bool = True,     clean_match: bool = False,     case_sensitive: bool = True, ) -> TextHandlers:     """Call the ``.re()`` method for each element in this list and return     their results flattened as List of TextHandler.      :param regex: Can be either a compiled regular expression or a string.     :param replace_entities: If enabled character entity references are replaced by their corresponding character     :param clean_match: if enabled, this will ignore all whitespaces and consecutive spaces while matching     :param case_sensitive: if disabled, the function will set the regex to ignore the letters case while compiling it     """     results = [n.re(regex, replace_entities, clean_match, case_sensitive) for n in self]     return TextHandlers(flatten(results)) ``` |

### re_first [¶](#scrapling.parser.Selectors.re_first "Permanent link")

```
re_first(
    regex,
    default=None,
    replace_entities=True,
    clean_match=False,
    case_sensitive=True,
)
```

Call the `.re_first()` method for each element in this list and return
the first result or the default value otherwise.

| PARAMETER | DESCRIPTION |
| --- | --- |
| `regex` | Can be either a compiled regular expression or a string.  **TYPE:** `str | Pattern` |
| `default` | The default value to be returned if there is no match  **TYPE:** `Any`  **DEFAULT:** `None` |
| `replace_entities` | if enabled character entity references are replaced by their corresponding character  **TYPE:** `bool`  **DEFAULT:** `True` |
| `clean_match` | if enabled, this will ignore all whitespaces and consecutive spaces while matching  **TYPE:** `bool`  **DEFAULT:** `False` |
| `case_sensitive` | if disabled, function will set the regex to ignore the letters case while compiling it  **TYPE:** `bool`  **DEFAULT:** `True` |

Source code in `scrapling/parser.py`

|  |  |
| --- | --- |
| ``` 1295 1296 1297 1298 1299 1300 1301 1302 1303 1304 1305 1306 1307 1308 1309 1310 1311 1312 1313 1314 1315 ``` | ``` def re_first(     self,     regex: str | Pattern,     default: Any = None,     replace_entities: bool = True,     clean_match: bool = False,     case_sensitive: bool = True, ) -> TextHandler:     """Call the ``.re_first()`` method for each element in this list and return     the first result or the default value otherwise.      :param regex: Can be either a compiled regular expression or a string.     :param default: The default value to be returned if there is no match     :param replace_entities: if enabled character entity references are replaced by their corresponding character     :param clean_match: if enabled, this will ignore all whitespaces and consecutive spaces while matching     :param case_sensitive: if disabled, function will set the regex to ignore the letters case while compiling it     """     for n in self:         for result in n.re(regex, replace_entities, clean_match, case_sensitive):             return result     return default ``` |

### search [¶](#scrapling.parser.Selectors.search "Permanent link")

```
search(func)
```

Loop over all current elements and return the first element that matches the passed function

| PARAMETER | DESCRIPTION |
| --- | --- |
| `func` | A function that takes each element as an argument and returns True/False  **TYPE:** `Callable[[Selector], bool]` |

| RETURNS | DESCRIPTION |
| --- | --- |
| `Optional[Selector]` | The first element that match the function or `None` otherwise. |

Source code in `scrapling/parser.py`

|  |  |
| --- | --- |
| ``` 1317 1318 1319 1320 1321 1322 1323 1324 1325 ``` | ``` def search(self, func: Callable[["Selector"], bool]) -> Optional["Selector"]:     """Loop over all current elements and return the first element that matches the passed function     :param func: A function that takes each element as an argument and returns True/False     :return: The first element that match the function or ``None`` otherwise.     """     for element in self:         if func(element):             return element     return None ``` |

### filter [¶](#scrapling.parser.Selectors.filter "Permanent link")

```
filter(func)
```

Filter current elements based on the passed function

| PARAMETER | DESCRIPTION |
| --- | --- |
| `func` | A function that takes each element as an argument and returns True/False  **TYPE:** `Callable[[Selector], bool]` |

| RETURNS | DESCRIPTION |
| --- | --- |
| `Selectors` | The new `Selectors` object or empty list otherwise. |

Source code in `scrapling/parser.py`

|  |  |
| --- | --- |
| ``` 1327 1328 1329 1330 1331 1332 ``` | ``` def filter(self, func: Callable[["Selector"], bool]) -> "Selectors":     """Filter current elements based on the passed function     :param func: A function that takes each element as an argument and returns True/False     :return: The new `Selectors` object or empty list otherwise.     """     return self.__class__([element for element in self if func(element)]) ``` |

### get [¶](#scrapling.parser.Selectors.get "Permanent link")

```
get(default=None)
```

Returns the serialized string of the first element, or `default` if empty.

| PARAMETER | DESCRIPTION |
| --- | --- |
| `default` | the default value to return if the current list is empty  **DEFAULT:** `None` |

Source code in `scrapling/parser.py`

|  |  |
| --- | --- |
| ``` 1340 1341 1342 1343 1344 1345 1346 ``` | ``` def get(self, default=None):     """Returns the serialized string of the first element, or ``default`` if empty.     :param default: the default value to return if the current list is empty     """     for x in self:         return x.get()     return default ``` |

### getall [¶](#scrapling.parser.Selectors.getall "Permanent link")

```
getall()
```

Serialize all elements and return as a TextHandlers list.

Source code in `scrapling/parser.py`

|  |  |
| --- | --- |
| ``` 1348 1349 1350 ``` | ``` def getall(self) -> TextHandlers:     """Serialize all elements and return as a TextHandlers list."""     return TextHandlers([x.get() for x in self]) ``` |

### __getstate__ [¶](#scrapling.parser.Selectors.__getstate__ "Permanent link")

```
__getstate__()
```

Source code in `scrapling/parser.py`

|  |  |
| --- | --- |
| ``` 1370 1371 1372 ``` | ``` def __getstate__(self) -> Any:  # pragma: no cover     # lxml don't like it :)     raise TypeError("Can't pickle Selectors object") ``` |

Was this page helpful?

Thanks for your feedback!

Thanks for your feedback! Help us improve this page by
[opening a documentation issue](https://github.com/D4Vinci/Scrapling/issues/new?template=04-docs_issue.yml).


---
## Source: https://scrapling.readthedocs.io/en/latest/api-reference/fetchers.html
---

# Fetchers Classes[¶](#fetchers-classes "Permanent link")

Here's the reference information for all fetcher-type classes' parameters, attributes, and methods.

You can import all of them directly like below:

```
from scrapling.fetchers import (
    Fetcher, AsyncFetcher, StealthyFetcher, DynamicFetcher,
    FetcherSession, AsyncStealthySession, StealthySession, DynamicSession, AsyncDynamicSession
)
```

## scrapling.fetchers.Fetcher [¶](#scrapling.fetchers.Fetcher "Permanent link")

```
Fetcher(*args, **kwargs)
```

Bases: `BaseFetcher`

```
              flowchart TD
              scrapling.fetchers.Fetcher[Fetcher]
              scrapling.engines.toolbelt.custom.BaseFetcher[BaseFetcher]

                              scrapling.engines.toolbelt.custom.BaseFetcher --> scrapling.fetchers.Fetcher
                


              click scrapling.fetchers.Fetcher href "" "scrapling.fetchers.Fetcher"
              click scrapling.engines.toolbelt.custom.BaseFetcher href "" "scrapling.engines.toolbelt.custom.BaseFetcher"
```

A basic `Fetcher` class type that can only do basic GET, POST, PUT, and DELETE HTTP requests based on `curl_cffi`.

Source code in `scrapling/engines/toolbelt/custom.py`

|  |  |
| --- | --- |
| ``` 169 170 171 172 173 174 175 176 177 178 179 ``` | ``` def __init__(self, *args, **kwargs):     # For backward-compatibility before 0.2.99     args_str = ", ".join(args) or ""     kwargs_str = ", ".join(f"{k}={v}" for k, v in kwargs.items()) or ""     if args_str:         args_str += ", "      log.warning(         f"This logic is deprecated now, and have no effect; It will be removed with v0.3. Use `{self.__class__.__name__}.configure({args_str}{kwargs_str})` instead before fetching"     )     pass ``` |

### __slots__ `class-attribute` `instance-attribute` [¶](#scrapling.fetchers.Fetcher.__slots__ "Permanent link")

```
__slots__ = ()
```

### huge_tree `class-attribute` `instance-attribute` [¶](#scrapling.fetchers.Fetcher.huge_tree "Permanent link")

```
huge_tree = True
```

### adaptive `class-attribute` `instance-attribute` [¶](#scrapling.fetchers.Fetcher.adaptive "Permanent link")

```
adaptive = False
```

### storage `class-attribute` `instance-attribute` [¶](#scrapling.fetchers.Fetcher.storage "Permanent link")

```
storage = SQLiteStorageSystem
```

### keep_cdata `class-attribute` `instance-attribute` [¶](#scrapling.fetchers.Fetcher.keep_cdata "Permanent link")

```
keep_cdata = False
```

### storage_args `class-attribute` `instance-attribute` [¶](#scrapling.fetchers.Fetcher.storage_args "Permanent link")

```
storage_args = None
```

### keep_comments `class-attribute` `instance-attribute` [¶](#scrapling.fetchers.Fetcher.keep_comments "Permanent link")

```
keep_comments = False
```

### adaptive_domain `class-attribute` `instance-attribute` [¶](#scrapling.fetchers.Fetcher.adaptive_domain "Permanent link")

```
adaptive_domain = ''
```

### parser_keywords `class-attribute` `instance-attribute` [¶](#scrapling.fetchers.Fetcher.parser_keywords "Permanent link")

```
parser_keywords = (
    "huge_tree",
    "adaptive",
    "storage",
    "keep_cdata",
    "storage_args",
    "keep_comments",
    "adaptive_domain",
)
```

### get `class-attribute` `instance-attribute` [¶](#scrapling.fetchers.Fetcher.get "Permanent link")

```
get = get
```

### post `class-attribute` `instance-attribute` [¶](#scrapling.fetchers.Fetcher.post "Permanent link")

```
post = post
```

### put `class-attribute` `instance-attribute` [¶](#scrapling.fetchers.Fetcher.put "Permanent link")

```
put = put
```

### delete `class-attribute` `instance-attribute` [¶](#scrapling.fetchers.Fetcher.delete "Permanent link")

```
delete = delete
```

### display_config `classmethod` [¶](#scrapling.fetchers.Fetcher.display_config "Permanent link")

```
display_config()
```

Source code in `scrapling/engines/toolbelt/custom.py`

|  |  |
| --- | --- |
| ``` 181 182 183 184 185 186 187 188 189 190 191 ``` | ``` @classmethod def display_config(cls):     return dict(         huge_tree=cls.huge_tree,         keep_comments=cls.keep_comments,         keep_cdata=cls.keep_cdata,         adaptive=cls.adaptive,         storage=cls.storage,         storage_args=cls.storage_args,         adaptive_domain=cls.adaptive_domain,     ) ``` |

### configure `classmethod` [¶](#scrapling.fetchers.Fetcher.configure "Permanent link")

```
configure(**kwargs)
```

Set multiple arguments for the parser at once globally

| PARAMETER | DESCRIPTION |
| --- | --- |
| `kwargs` | The keywords can be any arguments of the following: huge_tree, keep_comments, keep_cdata, adaptive, storage, storage_args, adaptive_domain  **DEFAULT:** `{}` |

Source code in `scrapling/engines/toolbelt/custom.py`

|  |  |
| --- | --- |
| ``` 193 194 195 196 197 198 199 200 201 202 203 204 205 206 207 208 209 210 211 ``` | ``` @classmethod def configure(cls, **kwargs):     """Set multiple arguments for the parser at once globally      :param kwargs: The keywords can be any arguments of the following: huge_tree, keep_comments, keep_cdata, adaptive, storage, storage_args, adaptive_domain     """     for key, value in kwargs.items():         key = key.strip().lower()         if hasattr(cls, key):             if key in cls.parser_keywords:                 setattr(cls, key, value)             else:                 # Yup, no fun allowed LOL                 raise AttributeError(f'Unknown parser argument: "{key}"; maybe you meant {cls.parser_keywords}?')         else:             raise ValueError(f'Unknown parser argument: "{key}"; maybe you meant {cls.parser_keywords}?')      if not kwargs:         raise AttributeError(f"You must pass a keyword to configure, current keywords: {cls.parser_keywords}?") ``` |

## scrapling.fetchers.AsyncFetcher [¶](#scrapling.fetchers.AsyncFetcher "Permanent link")

```
AsyncFetcher(*args, **kwargs)
```

Bases: `BaseFetcher`

```
              flowchart TD
              scrapling.fetchers.AsyncFetcher[AsyncFetcher]
              scrapling.engines.toolbelt.custom.BaseFetcher[BaseFetcher]

                              scrapling.engines.toolbelt.custom.BaseFetcher --> scrapling.fetchers.AsyncFetcher
                


              click scrapling.fetchers.AsyncFetcher href "" "scrapling.fetchers.AsyncFetcher"
              click scrapling.engines.toolbelt.custom.BaseFetcher href "" "scrapling.engines.toolbelt.custom.BaseFetcher"
```

A basic `Fetcher` class type that can only do basic GET, POST, PUT, and DELETE HTTP requests based on `curl_cffi`.

Source code in `scrapling/engines/toolbelt/custom.py`

|  |  |
| --- | --- |
| ``` 169 170 171 172 173 174 175 176 177 178 179 ``` | ``` def __init__(self, *args, **kwargs):     # For backward-compatibility before 0.2.99     args_str = ", ".join(args) or ""     kwargs_str = ", ".join(f"{k}={v}" for k, v in kwargs.items()) or ""     if args_str:         args_str += ", "      log.warning(         f"This logic is deprecated now, and have no effect; It will be removed with v0.3. Use `{self.__class__.__name__}.configure({args_str}{kwargs_str})` instead before fetching"     )     pass ``` |

### __slots__ `class-attribute` `instance-attribute` [¶](#scrapling.fetchers.AsyncFetcher.__slots__ "Permanent link")

```
__slots__ = ()
```

### huge_tree `class-attribute` `instance-attribute` [¶](#scrapling.fetchers.AsyncFetcher.huge_tree "Permanent link")

```
huge_tree = True
```

### adaptive `class-attribute` `instance-attribute` [¶](#scrapling.fetchers.AsyncFetcher.adaptive "Permanent link")

```
adaptive = False
```

### storage `class-attribute` `instance-attribute` [¶](#scrapling.fetchers.AsyncFetcher.storage "Permanent link")

```
storage = SQLiteStorageSystem
```

### keep_cdata `class-attribute` `instance-attribute` [¶](#scrapling.fetchers.AsyncFetcher.keep_cdata "Permanent link")

```
keep_cdata = False
```

### storage_args `class-attribute` `instance-attribute` [¶](#scrapling.fetchers.AsyncFetcher.storage_args "Permanent link")

```
storage_args = None
```

### keep_comments `class-attribute` `instance-attribute` [¶](#scrapling.fetchers.AsyncFetcher.keep_comments "Permanent link")

```
keep_comments = False
```

### adaptive_domain `class-attribute` `instance-attribute` [¶](#scrapling.fetchers.AsyncFetcher.adaptive_domain "Permanent link")

```
adaptive_domain = ''
```

### parser_keywords `class-attribute` `instance-attribute` [¶](#scrapling.fetchers.AsyncFetcher.parser_keywords "Permanent link")

```
parser_keywords = (
    "huge_tree",
    "adaptive",
    "storage",
    "keep_cdata",
    "storage_args",
    "keep_comments",
    "adaptive_domain",
)
```

### get `class-attribute` `instance-attribute` [¶](#scrapling.fetchers.AsyncFetcher.get "Permanent link")

```
get = get
```

### post `class-attribute` `instance-attribute` [¶](#scrapling.fetchers.AsyncFetcher.post "Permanent link")

```
post = post
```

### put `class-attribute` `instance-attribute` [¶](#scrapling.fetchers.AsyncFetcher.put "Permanent link")

```
put = put
```

### delete `class-attribute` `instance-attribute` [¶](#scrapling.fetchers.AsyncFetcher.delete "Permanent link")

```
delete = delete
```

### display_config `classmethod` [¶](#scrapling.fetchers.AsyncFetcher.display_config "Permanent link")

```
display_config()
```

Source code in `scrapling/engines/toolbelt/custom.py`

|  |  |
| --- | --- |
| ``` 181 182 183 184 185 186 187 188 189 190 191 ``` | ``` @classmethod def display_config(cls):     return dict(         huge_tree=cls.huge_tree,         keep_comments=cls.keep_comments,         keep_cdata=cls.keep_cdata,         adaptive=cls.adaptive,         storage=cls.storage,         storage_args=cls.storage_args,         adaptive_domain=cls.adaptive_domain,     ) ``` |

### configure `classmethod` [¶](#scrapling.fetchers.AsyncFetcher.configure "Permanent link")

```
configure(**kwargs)
```

Set multiple arguments for the parser at once globally

| PARAMETER | DESCRIPTION |
| --- | --- |
| `kwargs` | The keywords can be any arguments of the following: huge_tree, keep_comments, keep_cdata, adaptive, storage, storage_args, adaptive_domain  **DEFAULT:** `{}` |

Source code in `scrapling/engines/toolbelt/custom.py`

|  |  |
| --- | --- |
| ``` 193 194 195 196 197 198 199 200 201 202 203 204 205 206 207 208 209 210 211 ``` | ``` @classmethod def configure(cls, **kwargs):     """Set multiple arguments for the parser at once globally      :param kwargs: The keywords can be any arguments of the following: huge_tree, keep_comments, keep_cdata, adaptive, storage, storage_args, adaptive_domain     """     for key, value in kwargs.items():         key = key.strip().lower()         if hasattr(cls, key):             if key in cls.parser_keywords:                 setattr(cls, key, value)             else:                 # Yup, no fun allowed LOL                 raise AttributeError(f'Unknown parser argument: "{key}"; maybe you meant {cls.parser_keywords}?')         else:             raise ValueError(f'Unknown parser argument: "{key}"; maybe you meant {cls.parser_keywords}?')      if not kwargs:         raise AttributeError(f"You must pass a keyword to configure, current keywords: {cls.parser_keywords}?") ``` |

## scrapling.fetchers.DynamicFetcher [¶](#scrapling.fetchers.DynamicFetcher "Permanent link")

```
DynamicFetcher(*args, **kwargs)
```

Bases: `BaseFetcher`

```
              flowchart TD
              scrapling.fetchers.DynamicFetcher[DynamicFetcher]
              scrapling.engines.toolbelt.custom.BaseFetcher[BaseFetcher]

                              scrapling.engines.toolbelt.custom.BaseFetcher --> scrapling.fetchers.DynamicFetcher
                


              click scrapling.fetchers.DynamicFetcher href "" "scrapling.fetchers.DynamicFetcher"
              click scrapling.engines.toolbelt.custom.BaseFetcher href "" "scrapling.engines.toolbelt.custom.BaseFetcher"
```

A `Fetcher` that provide many options to fetch/load websites' pages through chromium-based browsers.

Source code in `scrapling/engines/toolbelt/custom.py`

|  |  |
| --- | --- |
| ``` 169 170 171 172 173 174 175 176 177 178 179 ``` | ``` def __init__(self, *args, **kwargs):     # For backward-compatibility before 0.2.99     args_str = ", ".join(args) or ""     kwargs_str = ", ".join(f"{k}={v}" for k, v in kwargs.items()) or ""     if args_str:         args_str += ", "      log.warning(         f"This logic is deprecated now, and have no effect; It will be removed with v0.3. Use `{self.__class__.__name__}.configure({args_str}{kwargs_str})` instead before fetching"     )     pass ``` |

### __slots__ `class-attribute` `instance-attribute` [¶](#scrapling.fetchers.DynamicFetcher.__slots__ "Permanent link")

```
__slots__ = ()
```

### huge_tree `class-attribute` `instance-attribute` [¶](#scrapling.fetchers.DynamicFetcher.huge_tree "Permanent link")

```
huge_tree = True
```

### adaptive `class-attribute` `instance-attribute` [¶](#scrapling.fetchers.DynamicFetcher.adaptive "Permanent link")

```
adaptive = False
```

### storage `class-attribute` `instance-attribute` [¶](#scrapling.fetchers.DynamicFetcher.storage "Permanent link")

```
storage = SQLiteStorageSystem
```

### keep_cdata `class-attribute` `instance-attribute` [¶](#scrapling.fetchers.DynamicFetcher.keep_cdata "Permanent link")

```
keep_cdata = False
```

### storage_args `class-attribute` `instance-attribute` [¶](#scrapling.fetchers.DynamicFetcher.storage_args "Permanent link")

```
storage_args = None
```

### keep_comments `class-attribute` `instance-attribute` [¶](#scrapling.fetchers.DynamicFetcher.keep_comments "Permanent link")

```
keep_comments = False
```

### adaptive_domain `class-attribute` `instance-attribute` [¶](#scrapling.fetchers.DynamicFetcher.adaptive_domain "Permanent link")

```
adaptive_domain = ''
```

### parser_keywords `class-attribute` `instance-attribute` [¶](#scrapling.fetchers.DynamicFetcher.parser_keywords "Permanent link")

```
parser_keywords = (
    "huge_tree",
    "adaptive",
    "storage",
    "keep_cdata",
    "storage_args",
    "keep_comments",
    "adaptive_domain",
)
```

### display_config `classmethod` [¶](#scrapling.fetchers.DynamicFetcher.display_config "Permanent link")

```
display_config()
```

Source code in `scrapling/engines/toolbelt/custom.py`

|  |  |
| --- | --- |
| ``` 181 182 183 184 185 186 187 188 189 190 191 ``` | ``` @classmethod def display_config(cls):     return dict(         huge_tree=cls.huge_tree,         keep_comments=cls.keep_comments,         keep_cdata=cls.keep_cdata,         adaptive=cls.adaptive,         storage=cls.storage,         storage_args=cls.storage_args,         adaptive_domain=cls.adaptive_domain,     ) ``` |

### configure `classmethod` [¶](#scrapling.fetchers.DynamicFetcher.configure "Permanent link")

```
configure(**kwargs)
```

Set multiple arguments for the parser at once globally

| PARAMETER | DESCRIPTION |
| --- | --- |
| `kwargs` | The keywords can be any arguments of the following: huge_tree, keep_comments, keep_cdata, adaptive, storage, storage_args, adaptive_domain  **DEFAULT:** `{}` |

Source code in `scrapling/engines/toolbelt/custom.py`

|  |  |
| --- | --- |
| ``` 193 194 195 196 197 198 199 200 201 202 203 204 205 206 207 208 209 210 211 ``` | ``` @classmethod def configure(cls, **kwargs):     """Set multiple arguments for the parser at once globally      :param kwargs: The keywords can be any arguments of the following: huge_tree, keep_comments, keep_cdata, adaptive, storage, storage_args, adaptive_domain     """     for key, value in kwargs.items():         key = key.strip().lower()         if hasattr(cls, key):             if key in cls.parser_keywords:                 setattr(cls, key, value)             else:                 # Yup, no fun allowed LOL                 raise AttributeError(f'Unknown parser argument: "{key}"; maybe you meant {cls.parser_keywords}?')         else:             raise ValueError(f'Unknown parser argument: "{key}"; maybe you meant {cls.parser_keywords}?')      if not kwargs:         raise AttributeError(f"You must pass a keyword to configure, current keywords: {cls.parser_keywords}?") ``` |

### fetch `classmethod` [¶](#scrapling.fetchers.DynamicFetcher.fetch "Permanent link")

```
fetch(url, **kwargs)
```

Opens up a browser and do your request based on your chosen options below.

| PARAMETER | DESCRIPTION |
| --- | --- |
| `url` | Target url.  **TYPE:** `str` |
| `headless` | Run the browser in headless/hidden (default), or headful/visible mode. |
| `disable_resources` | Drop requests for unnecessary resources for a speed boost. |
| `blocked_domains` | A set of domain names to block requests to. Subdomains are also matched (e.g., `"example.com"` blocks `"sub.example.com"` too). |
| `useragent` | Pass a useragent string to be used. Otherwise the fetcher will generate a real Useragent of the same browser and use it. |
| `cookies` | Set cookies for the next request. |
| `network_idle` | Wait for the page until there are no network connections for at least 500 ms. |
| `load_dom` | Enabled by default, wait for all JavaScript on page(s) to fully load and execute. |
| `timeout` | The timeout in milliseconds that is used in all operations and waits through the page. The default is 30,000 |
| `wait` | The time (milliseconds) the fetcher will wait after everything finishes before closing the page and returning the Response object. |
| `page_action` | Added for automation. A function that takes the `page` object and does the automation you need. |
| `wait_selector` | Wait for a specific CSS selector to be in a specific state. |
| `init_script` | An absolute path to a JavaScript file to be executed on page creation with this request. |
| `locale` | Set the locale for the browser if wanted. Defaults to the system default locale. |
| `wait_selector_state` | The state to wait for the selector given with `wait_selector`. The default state is `attached`. |
| `real_chrome` | If you have a Chrome browser installed on your device, enable this, and the Fetcher will launch an instance of your browser and use it. |
| `cdp_url` | Instead of launching a new browser instance, connect to this CDP URL to control real browsers through CDP. |
| `google_search` | Enabled by default, Scrapling will set a Google referer header. |
| `extra_headers` | A dictionary of extra headers to add to the request. |
| `proxy` | The proxy to be used with requests, it can be a string or a dictionary with the keys 'server', 'username', and 'password' only. |
| `extra_flags` | A list of additional browser flags to pass to the browser on launch. |
| `selector_config` | The arguments that will be passed in the end while creating the final Selector's class. |
| `additional_args` | Additional arguments to be passed to Playwright's context as additional settings. |

| RETURNS | DESCRIPTION |
| --- | --- |
| `Response` | A `Response` object. |

Source code in `scrapling/fetchers/chrome.py`

|  |  |
| --- | --- |
| ``` 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 ``` | ``` @classmethod def fetch(cls, url: str, **kwargs: Unpack[PlaywrightSession]) -> Response:     """Opens up a browser and do your request based on your chosen options below.      :param url: Target url.     :param headless: Run the browser in headless/hidden (default), or headful/visible mode.     :param disable_resources: Drop requests for unnecessary resources for a speed boost.     :param blocked_domains: A set of domain names to block requests to. Subdomains are also matched (e.g., ``"example.com"`` blocks ``"sub.example.com"`` too).     :param useragent: Pass a useragent string to be used. Otherwise the fetcher will generate a real Useragent of the same browser and use it.     :param cookies: Set cookies for the next request.     :param network_idle: Wait for the page until there are no network connections for at least 500 ms.     :param load_dom: Enabled by default, wait for all JavaScript on page(s) to fully load and execute.     :param timeout: The timeout in milliseconds that is used in all operations and waits through the page. The default is 30,000     :param wait: The time (milliseconds) the fetcher will wait after everything finishes before closing the page and returning the Response object.     :param page_action: Added for automation. A function that takes the `page` object and does the automation you need.     :param wait_selector: Wait for a specific CSS selector to be in a specific state.     :param init_script: An absolute path to a JavaScript file to be executed on page creation with this request.     :param locale: Set the locale for the browser if wanted. Defaults to the system default locale.     :param wait_selector_state: The state to wait for the selector given with `wait_selector`. The default state is `attached`.     :param real_chrome: If you have a Chrome browser installed on your device, enable this, and the Fetcher will launch an instance of your browser and use it.     :param cdp_url: Instead of launching a new browser instance, connect to this CDP URL to control real browsers through CDP.     :param google_search: Enabled by default, Scrapling will set a Google referer header.     :param extra_headers: A dictionary of extra headers to add to the request.     :param proxy: The proxy to be used with requests, it can be a string or a dictionary with the keys 'server', 'username', and 'password' only.     :param extra_flags: A list of additional browser flags to pass to the browser on launch.     :param selector_config: The arguments that will be passed in the end while creating the final Selector's class.     :param additional_args: Additional arguments to be passed to Playwright's context as additional settings.     :return: A `Response` object.     """     selector_config = kwargs.get("selector_config", {}) or kwargs.get(         "custom_config", {}     )  # Checking `custom_config` for backward compatibility     if not isinstance(selector_config, dict):         raise TypeError("Argument `selector_config` must be a dictionary.")      kwargs["selector_config"] = {**cls._generate_parser_arguments(), **selector_config}      with DynamicSession(**kwargs) as session:         return session.fetch(url) ``` |

### async_fetch `async` `classmethod` [¶](#scrapling.fetchers.DynamicFetcher.async_fetch "Permanent link")

```
async_fetch(url, **kwargs)
```

Opens up a browser and do your request based on your chosen options below.

| PARAMETER | DESCRIPTION |
| --- | --- |
| `url` | Target url.  **TYPE:** `str` |
| `headless` | Run the browser in headless/hidden (default), or headful/visible mode. |
| `disable_resources` | Drop requests for unnecessary resources for a speed boost. |
| `blocked_domains` | A set of domain names to block requests to. Subdomains are also matched (e.g., `"example.com"` blocks `"sub.example.com"` too). |
| `useragent` | Pass a useragent string to be used. Otherwise the fetcher will generate a real Useragent of the same browser and use it. |
| `cookies` | Set cookies for the next request. |
| `network_idle` | Wait for the page until there are no network connections for at least 500 ms. |
| `load_dom` | Enabled by default, wait for all JavaScript on page(s) to fully load and execute. |
| `timeout` | The timeout in milliseconds that is used in all operations and waits through the page. The default is 30,000 |
| `wait` | The time (milliseconds) the fetcher will wait after everything finishes before closing the page and returning the Response object. |
| `page_action` | Added for automation. A function that takes the `page` object and does the automation you need. |
| `wait_selector` | Wait for a specific CSS selector to be in a specific state. |
| `init_script` | An absolute path to a JavaScript file to be executed on page creation with this request. |
| `locale` | Set the locale for the browser if wanted. Defaults to the system default locale. |
| `wait_selector_state` | The state to wait for the selector given with `wait_selector`. The default state is `attached`. |
| `real_chrome` | If you have a Chrome browser installed on your device, enable this, and the Fetcher will launch an instance of your browser and use it. |
| `cdp_url` | Instead of launching a new browser instance, connect to this CDP URL to control real browsers through CDP. |
| `google_search` | Enabled by default, Scrapling will set a Google referer header. |
| `extra_headers` | A dictionary of extra headers to add to the request. |
| `proxy` | The proxy to be used with requests, it can be a string or a dictionary with the keys 'server', 'username', and 'password' only. |
| `extra_flags` | A list of additional browser flags to pass to the browser on launch. |
| `selector_config` | The arguments that will be passed in the end while creating the final Selector's class. |
| `additional_args` | Additional arguments to be passed to Playwright's context as additional settings. |

| RETURNS | DESCRIPTION |
| --- | --- |
| `Response` | A `Response` object. |

Source code in `scrapling/fetchers/chrome.py`

|  |  |
| --- | --- |
| ``` 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 ``` | ``` @classmethod async def async_fetch(cls, url: str, **kwargs: Unpack[PlaywrightSession]) -> Response:     """Opens up a browser and do your request based on your chosen options below.      :param url: Target url.     :param headless: Run the browser in headless/hidden (default), or headful/visible mode.     :param disable_resources: Drop requests for unnecessary resources for a speed boost.     :param blocked_domains: A set of domain names to block requests to. Subdomains are also matched (e.g., ``"example.com"`` blocks ``"sub.example.com"`` too).     :param useragent: Pass a useragent string to be used. Otherwise the fetcher will generate a real Useragent of the same browser and use it.     :param cookies: Set cookies for the next request.     :param network_idle: Wait for the page until there are no network connections for at least 500 ms.     :param load_dom: Enabled by default, wait for all JavaScript on page(s) to fully load and execute.     :param timeout: The timeout in milliseconds that is used in all operations and waits through the page. The default is 30,000     :param wait: The time (milliseconds) the fetcher will wait after everything finishes before closing the page and returning the Response object.     :param page_action: Added for automation. A function that takes the `page` object and does the automation you need.     :param wait_selector: Wait for a specific CSS selector to be in a specific state.     :param init_script: An absolute path to a JavaScript file to be executed on page creation with this request.     :param locale: Set the locale for the browser if wanted. Defaults to the system default locale.     :param wait_selector_state: The state to wait for the selector given with `wait_selector`. The default state is `attached`.     :param real_chrome: If you have a Chrome browser installed on your device, enable this, and the Fetcher will launch an instance of your browser and use it.     :param cdp_url: Instead of launching a new browser instance, connect to this CDP URL to control real browsers through CDP.     :param google_search: Enabled by default, Scrapling will set a Google referer header.     :param extra_headers: A dictionary of extra headers to add to the request.     :param proxy: The proxy to be used with requests, it can be a string or a dictionary with the keys 'server', 'username', and 'password' only.     :param extra_flags: A list of additional browser flags to pass to the browser on launch.     :param selector_config: The arguments that will be passed in the end while creating the final Selector's class.     :param additional_args: Additional arguments to be passed to Playwright's context as additional settings.     :return: A `Response` object.     """     selector_config = kwargs.get("selector_config", {}) or kwargs.get(         "custom_config", {}     )  # Checking `custom_config` for backward compatibility     if not isinstance(selector_config, dict):         raise TypeError("Argument `selector_config` must be a dictionary.")      kwargs["selector_config"] = {**cls._generate_parser_arguments(), **selector_config}      async with AsyncDynamicSession(**kwargs) as session:         return await session.fetch(url) ``` |

## scrapling.fetchers.StealthyFetcher [¶](#scrapling.fetchers.StealthyFetcher "Permanent link")

```
StealthyFetcher(*args, **kwargs)
```

Bases: `BaseFetcher`

```
              flowchart TD
              scrapling.fetchers.StealthyFetcher[StealthyFetcher]
              scrapling.engines.toolbelt.custom.BaseFetcher[BaseFetcher]

                              scrapling.engines.toolbelt.custom.BaseFetcher --> scrapling.fetchers.StealthyFetcher
                


              click scrapling.fetchers.StealthyFetcher href "" "scrapling.fetchers.StealthyFetcher"
              click scrapling.engines.toolbelt.custom.BaseFetcher href "" "scrapling.engines.toolbelt.custom.BaseFetcher"
```

A `Fetcher` class type which is a completely stealthy built on top of Chromium.

It works as real browsers passing almost all online tests/protections with many customization options.

Source code in `scrapling/engines/toolbelt/custom.py`

|  |  |
| --- | --- |
| ``` 169 170 171 172 173 174 175 176 177 178 179 ``` | ``` def __init__(self, *args, **kwargs):     # For backward-compatibility before 0.2.99     args_str = ", ".join(args) or ""     kwargs_str = ", ".join(f"{k}={v}" for k, v in kwargs.items()) or ""     if args_str:         args_str += ", "      log.warning(         f"This logic is deprecated now, and have no effect; It will be removed with v0.3. Use `{self.__class__.__name__}.configure({args_str}{kwargs_str})` instead before fetching"     )     pass ``` |

### __slots__ `class-attribute` `instance-attribute` [¶](#scrapling.fetchers.StealthyFetcher.__slots__ "Permanent link")

```
__slots__ = ()
```

### huge_tree `class-attribute` `instance-attribute` [¶](#scrapling.fetchers.StealthyFetcher.huge_tree "Permanent link")

```
huge_tree = True
```

### adaptive `class-attribute` `instance-attribute` [¶](#scrapling.fetchers.StealthyFetcher.adaptive "Permanent link")

```
adaptive = False
```

### storage `class-attribute` `instance-attribute` [¶](#scrapling.fetchers.StealthyFetcher.storage "Permanent link")

```
storage = SQLiteStorageSystem
```

### keep_cdata `class-attribute` `instance-attribute` [¶](#scrapling.fetchers.StealthyFetcher.keep_cdata "Permanent link")

```
keep_cdata = False
```

### storage_args `class-attribute` `instance-attribute` [¶](#scrapling.fetchers.StealthyFetcher.storage_args "Permanent link")

```
storage_args = None
```

### keep_comments `class-attribute` `instance-attribute` [¶](#scrapling.fetchers.StealthyFetcher.keep_comments "Permanent link")

```
keep_comments = False
```

### adaptive_domain `class-attribute` `instance-attribute` [¶](#scrapling.fetchers.StealthyFetcher.adaptive_domain "Permanent link")

```
adaptive_domain = ''
```

### parser_keywords `class-attribute` `instance-attribute` [¶](#scrapling.fetchers.StealthyFetcher.parser_keywords "Permanent link")

```
parser_keywords = (
    "huge_tree",
    "adaptive",
    "storage",
    "keep_cdata",
    "storage_args",
    "keep_comments",
    "adaptive_domain",
)
```

### display_config `classmethod` [¶](#scrapling.fetchers.StealthyFetcher.display_config "Permanent link")

```
display_config()
```

Source code in `scrapling/engines/toolbelt/custom.py`

|  |  |
| --- | --- |
| ``` 181 182 183 184 185 186 187 188 189 190 191 ``` | ``` @classmethod def display_config(cls):     return dict(         huge_tree=cls.huge_tree,         keep_comments=cls.keep_comments,         keep_cdata=cls.keep_cdata,         adaptive=cls.adaptive,         storage=cls.storage,         storage_args=cls.storage_args,         adaptive_domain=cls.adaptive_domain,     ) ``` |

### configure `classmethod` [¶](#scrapling.fetchers.StealthyFetcher.configure "Permanent link")

```
configure(**kwargs)
```

Set multiple arguments for the parser at once globally

| PARAMETER | DESCRIPTION |
| --- | --- |
| `kwargs` | The keywords can be any arguments of the following: huge_tree, keep_comments, keep_cdata, adaptive, storage, storage_args, adaptive_domain  **DEFAULT:** `{}` |

Source code in `scrapling/engines/toolbelt/custom.py`

|  |  |
| --- | --- |
| ``` 193 194 195 196 197 198 199 200 201 202 203 204 205 206 207 208 209 210 211 ``` | ``` @classmethod def configure(cls, **kwargs):     """Set multiple arguments for the parser at once globally      :param kwargs: The keywords can be any arguments of the following: huge_tree, keep_comments, keep_cdata, adaptive, storage, storage_args, adaptive_domain     """     for key, value in kwargs.items():         key = key.strip().lower()         if hasattr(cls, key):             if key in cls.parser_keywords:                 setattr(cls, key, value)             else:                 # Yup, no fun allowed LOL                 raise AttributeError(f'Unknown parser argument: "{key}"; maybe you meant {cls.parser_keywords}?')         else:             raise ValueError(f'Unknown parser argument: "{key}"; maybe you meant {cls.parser_keywords}?')      if not kwargs:         raise AttributeError(f"You must pass a keyword to configure, current keywords: {cls.parser_keywords}?") ``` |

### fetch `classmethod` [¶](#scrapling.fetchers.StealthyFetcher.fetch "Permanent link")

```
fetch(url, **kwargs)
```

Opens up a browser and do your request based on your chosen options below.

| PARAMETER | DESCRIPTION |
| --- | --- |
| `url` | Target url.  **TYPE:** `str` |
| `headless` | Run the browser in headless/hidden (default), or headful/visible mode. |
| `disable_resources` | Drop requests for unnecessary resources for a speed boost. Requests dropped are of type `font`, `image`, `media`, `beacon`, `object`, `imageset`, `texttrack`, `websocket`, `csp_report`, and `stylesheet`. |
| `blocked_domains` | A set of domain names to block requests to. Subdomains are also matched (e.g., `"example.com"` blocks `"sub.example.com"` too). |
| `useragent` | Pass a useragent string to be used. Otherwise the fetcher will generate a real Useragent of the same browser and use it. |
| `cookies` | Set cookies for the next request. |
| `network_idle` | Wait for the page until there are no network connections for at least 500 ms. |
| `timeout` | The timeout in milliseconds that is used in all operations and waits through the page. The default is 30,000 |
| `wait` | The time (milliseconds) the fetcher will wait after everything finishes before closing the page and returning the `Response` object. |
| `page_action` | Added for automation. A function that takes the `page` object and does the automation you need. |
| `wait_selector` | Wait for a specific CSS selector to be in a specific state. |
| `init_script` | An absolute path to a JavaScript file to be executed on page creation for all pages in this session. |
| `locale` | Specify user locale, for example, `en-GB`, `de-DE`, etc. Locale will affect navigator.language value, Accept-Language request header value as well as number and date formatting rules. Defaults to the system default locale. |
| `timezone_id` | Changes the timezone of the browser. Defaults to the system timezone. |
| `wait_selector_state` | The state to wait for the selector given with `wait_selector`. The default state is `attached`. |
| `solve_cloudflare` | Solves all types of the Cloudflare's Turnstile/Interstitial challenges before returning the response to you. |
| `real_chrome` | If you have a Chrome browser installed on your device, enable this, and the Fetcher will launch an instance of your browser and use it. |
| `hide_canvas` | Add random noise to canvas operations to prevent fingerprinting. |
| `block_webrtc` | Forces WebRTC to respect proxy settings to prevent local IP address leak. |
| `allow_webgl` | Enabled by default. Disabling it disables WebGL and WebGL 2.0 support entirely. Disabling WebGL is not recommended as many WAFs now check if WebGL is enabled. |
| `load_dom` | Enabled by default, wait for all JavaScript on page(s) to fully load and execute. |
| `cdp_url` | Instead of launching a new browser instance, connect to this CDP URL to control real browsers through CDP. |
| `google_search` | Enabled by default, Scrapling will set a Google referer header. |
| `extra_headers` | A dictionary of extra headers to add to the request. *The referer set by `google_search` takes priority over the referer set here if used together.* |
| `proxy` | The proxy to be used with requests, it can be a string or a dictionary with the keys 'server', 'username', and 'password' only. |
| `user_data_dir` | Path to a User Data Directory, which stores browser session data like cookies and local storage. The default is to create a temporary directory. |
| `extra_flags` | A list of additional browser flags to pass to the browser on launch. |
| `selector_config` | The arguments that will be passed in the end while creating the final Selector's class. |
| `additional_args` | Additional arguments to be passed to Playwright's context as additional settings, and it takes higher priority than Scrapling's settings. |

| RETURNS | DESCRIPTION |
| --- | --- |
| `Response` | A `Response` object. |

Source code in `scrapling/fetchers/stealth_chrome.py`

|  |  |
| --- | --- |
| ``` 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 ``` | ``` @classmethod def fetch(cls, url: str, **kwargs: Unpack[StealthSession]) -> Response:     """     Opens up a browser and do your request based on your chosen options below.      :param url: Target url.     :param headless: Run the browser in headless/hidden (default), or headful/visible mode.     :param disable_resources: Drop requests for unnecessary resources for a speed boost.         Requests dropped are of type `font`, `image`, `media`, `beacon`, `object`, `imageset`, `texttrack`, `websocket`, `csp_report`, and `stylesheet`.     :param blocked_domains: A set of domain names to block requests to. Subdomains are also matched (e.g., ``"example.com"`` blocks ``"sub.example.com"`` too).     :param useragent: Pass a useragent string to be used. Otherwise the fetcher will generate a real Useragent of the same browser and use it.     :param cookies: Set cookies for the next request.     :param network_idle: Wait for the page until there are no network connections for at least 500 ms.     :param timeout: The timeout in milliseconds that is used in all operations and waits through the page. The default is 30,000     :param wait: The time (milliseconds) the fetcher will wait after everything finishes before closing the page and returning the ` Response ` object.     :param page_action: Added for automation. A function that takes the `page` object and does the automation you need.     :param wait_selector: Wait for a specific CSS selector to be in a specific state.     :param init_script: An absolute path to a JavaScript file to be executed on page creation for all pages in this session.     :param locale: Specify user locale, for example, `en-GB`, `de-DE`, etc. Locale will affect navigator.language value, Accept-Language request header value as well as number and date formatting         rules. Defaults to the system default locale.     :param timezone_id: Changes the timezone of the browser. Defaults to the system timezone.     :param wait_selector_state: The state to wait for the selector given with `wait_selector`. The default state is `attached`.     :param solve_cloudflare: Solves all types of the Cloudflare's Turnstile/Interstitial challenges before returning the response to you.     :param real_chrome: If you have a Chrome browser installed on your device, enable this, and the Fetcher will launch an instance of your browser and use it.     :param hide_canvas: Add random noise to canvas operations to prevent fingerprinting.     :param block_webrtc: Forces WebRTC to respect proxy settings to prevent local IP address leak.     :param allow_webgl: Enabled by default. Disabling it disables WebGL and WebGL 2.0 support entirely. Disabling WebGL is not recommended as many WAFs now check if WebGL is enabled.     :param load_dom: Enabled by default, wait for all JavaScript on page(s) to fully load and execute.     :param cdp_url: Instead of launching a new browser instance, connect to this CDP URL to control real browsers through CDP.     :param google_search: Enabled by default, Scrapling will set a Google referer header.     :param extra_headers: A dictionary of extra headers to add to the request. _The referer set by `google_search` takes priority over the referer set here if used together._     :param proxy: The proxy to be used with requests, it can be a string or a dictionary with the keys 'server', 'username', and 'password' only.     :param user_data_dir: Path to a User Data Directory, which stores browser session data like cookies and local storage. The default is to create a temporary directory.     :param extra_flags: A list of additional browser flags to pass to the browser on launch.     :param selector_config: The arguments that will be passed in the end while creating the final Selector's class.     :param additional_args: Additional arguments to be passed to Playwright's context as additional settings, and it takes higher priority than Scrapling's settings.     :return: A `Response` object.     """     selector_config = kwargs.get("selector_config", {}) or kwargs.get(         "custom_config", {}     )  # Checking `custom_config` for backward compatibility     if not isinstance(selector_config, dict):         raise TypeError("Argument `selector_config` must be a dictionary.")      kwargs["selector_config"] = {**cls._generate_parser_arguments(), **selector_config}      with StealthySession(**kwargs) as engine:         return engine.fetch(url) ``` |

### async_fetch `async` `classmethod` [¶](#scrapling.fetchers.StealthyFetcher.async_fetch "Permanent link")

```
async_fetch(url, **kwargs)
```

Opens up a browser and do your request based on your chosen options below.

| PARAMETER | DESCRIPTION |
| --- | --- |
| `url` | Target url.  **TYPE:** `str` |
| `headless` | Run the browser in headless/hidden (default), or headful/visible mode. |
| `disable_resources` | Drop requests for unnecessary resources for a speed boost. Requests dropped are of type `font`, `image`, `media`, `beacon`, `object`, `imageset`, `texttrack`, `websocket`, `csp_report`, and `stylesheet`. |
| `blocked_domains` | A set of domain names to block requests to. Subdomains are also matched (e.g., `"example.com"` blocks `"sub.example.com"` too). |
| `useragent` | Pass a useragent string to be used. Otherwise the fetcher will generate a real Useragent of the same browser and use it. |
| `cookies` | Set cookies for the next request. |
| `network_idle` | Wait for the page until there are no network connections for at least 500 ms. |
| `timeout` | The timeout in milliseconds that is used in all operations and waits through the page. The default is 30,000 |
| `wait` | The time (milliseconds) the fetcher will wait after everything finishes before closing the page and returning the `Response` object. |
| `page_action` | Added for automation. A function that takes the `page` object and does the automation you need. |
| `wait_selector` | Wait for a specific CSS selector to be in a specific state. |
| `init_script` | An absolute path to a JavaScript file to be executed on page creation for all pages in this session. |
| `locale` | Specify user locale, for example, `en-GB`, `de-DE`, etc. Locale will affect navigator.language value, Accept-Language request header value as well as number and date formatting rules. Defaults to the system default locale. |
| `timezone_id` | Changes the timezone of the browser. Defaults to the system timezone. |
| `wait_selector_state` | The state to wait for the selector given with `wait_selector`. The default state is `attached`. |
| `solve_cloudflare` | Solves all types of the Cloudflare's Turnstile/Interstitial challenges before returning the response to you. |
| `real_chrome` | If you have a Chrome browser installed on your device, enable this, and the Fetcher will launch an instance of your browser and use it. |
| `hide_canvas` | Add random noise to canvas operations to prevent fingerprinting. |
| `block_webrtc` | Forces WebRTC to respect proxy settings to prevent local IP address leak. |
| `allow_webgl` | Enabled by default. Disabling it disables WebGL and WebGL 2.0 support entirely. Disabling WebGL is not recommended as many WAFs now check if WebGL is enabled. |
| `load_dom` | Enabled by default, wait for all JavaScript on page(s) to fully load and execute. |
| `cdp_url` | Instead of launching a new browser instance, connect to this CDP URL to control real browsers through CDP. |
| `google_search` | Enabled by default, Scrapling will set a Google referer header. |
| `extra_headers` | A dictionary of extra headers to add to the request. *The referer set by `google_search` takes priority over the referer set here if used together.* |
| `proxy` | The proxy to be used with requests, it can be a string or a dictionary with the keys 'server', 'username', and 'password' only. |
| `user_data_dir` | Path to a User Data Directory, which stores browser session data like cookies and local storage. The default is to create a temporary directory. |
| `extra_flags` | A list of additional browser flags to pass to the browser on launch. |
| `selector_config` | The arguments that will be passed in the end while creating the final Selector's class. |
| `additional_args` | Additional arguments to be passed to Playwright's context as additional settings, and it takes higher priority than Scrapling's settings. |

| RETURNS | DESCRIPTION |
| --- | --- |
| `Response` | A `Response` object. |

Source code in `scrapling/fetchers/stealth_chrome.py`

|  |  |
| --- | --- |
| ```  62  63  64  65  66  67  68  69  70  71  72  73  74  75  76  77  78  79  80  81  82  83  84  85  86  87  88  89  90  91  92  93  94  95  96  97  98  99 100 101 102 103 104 105 106 107 108 109 ``` | ``` @classmethod async def async_fetch(cls, url: str, **kwargs: Unpack[StealthSession]) -> Response:     """     Opens up a browser and do your request based on your chosen options below.      :param url: Target url.     :param headless: Run the browser in headless/hidden (default), or headful/visible mode.     :param disable_resources: Drop requests for unnecessary resources for a speed boost.         Requests dropped are of type `font`, `image`, `media`, `beacon`, `object`, `imageset`, `texttrack`, `websocket`, `csp_report`, and `stylesheet`.     :param blocked_domains: A set of domain names to block requests to. Subdomains are also matched (e.g., ``"example.com"`` blocks ``"sub.example.com"`` too).     :param useragent: Pass a useragent string to be used. Otherwise the fetcher will generate a real Useragent of the same browser and use it.     :param cookies: Set cookies for the next request.     :param network_idle: Wait for the page until there are no network connections for at least 500 ms.     :param timeout: The timeout in milliseconds that is used in all operations and waits through the page. The default is 30,000     :param wait: The time (milliseconds) the fetcher will wait after everything finishes before closing the page and returning the ` Response ` object.     :param page_action: Added for automation. A function that takes the `page` object and does the automation you need.     :param wait_selector: Wait for a specific CSS selector to be in a specific state.     :param init_script: An absolute path to a JavaScript file to be executed on page creation for all pages in this session.     :param locale: Specify user locale, for example, `en-GB`, `de-DE`, etc. Locale will affect navigator.language value, Accept-Language request header value as well as number and date formatting         rules. Defaults to the system default locale.     :param timezone_id: Changes the timezone of the browser. Defaults to the system timezone.     :param wait_selector_state: The state to wait for the selector given with `wait_selector`. The default state is `attached`.     :param solve_cloudflare: Solves all types of the Cloudflare's Turnstile/Interstitial challenges before returning the response to you.     :param real_chrome: If you have a Chrome browser installed on your device, enable this, and the Fetcher will launch an instance of your browser and use it.     :param hide_canvas: Add random noise to canvas operations to prevent fingerprinting.     :param block_webrtc: Forces WebRTC to respect proxy settings to prevent local IP address leak.     :param allow_webgl: Enabled by default. Disabling it disables WebGL and WebGL 2.0 support entirely. Disabling WebGL is not recommended as many WAFs now check if WebGL is enabled.     :param load_dom: Enabled by default, wait for all JavaScript on page(s) to fully load and execute.     :param cdp_url: Instead of launching a new browser instance, connect to this CDP URL to control real browsers through CDP.     :param google_search: Enabled by default, Scrapling will set a Google referer header.     :param extra_headers: A dictionary of extra headers to add to the request. _The referer set by `google_search` takes priority over the referer set here if used together._     :param proxy: The proxy to be used with requests, it can be a string or a dictionary with the keys 'server', 'username', and 'password' only.     :param user_data_dir: Path to a User Data Directory, which stores browser session data like cookies and local storage. The default is to create a temporary directory.     :param extra_flags: A list of additional browser flags to pass to the browser on launch.     :param selector_config: The arguments that will be passed in the end while creating the final Selector's class.     :param additional_args: Additional arguments to be passed to Playwright's context as additional settings, and it takes higher priority than Scrapling's settings.     :return: A `Response` object.     """     selector_config = kwargs.get("selector_config", {}) or kwargs.get(         "custom_config", {}     )  # Checking `custom_config` for backward compatibility     if not isinstance(selector_config, dict):         raise TypeError("Argument `selector_config` must be a dictionary.")      kwargs["selector_config"] = {**cls._generate_parser_arguments(), **selector_config}      async with AsyncStealthySession(**kwargs) as engine:         return await engine.fetch(url) ``` |

## Session Classes[¶](#session-classes "Permanent link")

### HTTP Sessions[¶](#http-sessions "Permanent link")

## scrapling.fetchers.FetcherSession [¶](#scrapling.fetchers.FetcherSession "Permanent link")

```
FetcherSession(
    impersonate="chrome",
    http3=False,
    stealthy_headers=True,
    proxies=None,
    proxy=None,
    proxy_auth=None,
    timeout=30,
    headers=None,
    retries=3,
    retry_delay=1,
    follow_redirects=True,
    max_redirects=30,
    verify=True,
    cert=None,
    selector_config=None,
    proxy_rotator=None,
)
```

A factory context manager that provides configured Fetcher sessions.

When this manager is used in a 'with' or 'async with' block,
it yields a new session configured with the manager's defaults.
A single instance of this manager should ideally be used for one active
session at a time (or sequentially). Re-entering a context with the
same manager instance while a session is already active is disallowed.

| PARAMETER | DESCRIPTION |
| --- | --- |
| `impersonate` | Browser version to impersonate. Can be a single browser string or a list of browser strings for random selection. (Default: latest available Chrome version)  **TYPE:** `ImpersonateType`  **DEFAULT:** `'chrome'` |
| `http3` | Whether to use HTTP3. Defaults to False. It might be problematic if used it with `impersonate`.  **TYPE:** `Optional[bool]`  **DEFAULT:** `False` |
| `stealthy_headers` | If enabled (default), it creates and adds real browser headers. It also sets a Google referer header.  **TYPE:** `Optional[bool]`  **DEFAULT:** `True` |
| `proxies` | Dict of proxies to use. Format: {"http": proxy_url, "https": proxy_url}.  **TYPE:** `Optional[Dict[str, str]]`  **DEFAULT:** `None` |
| `proxy` | Proxy URL to use. Format: "http://username:password@localhost:8030". Cannot be used together with the `proxies` parameter.  **TYPE:** `Optional[str]`  **DEFAULT:** `None` |
| `proxy_auth` | HTTP basic auth for proxy, tuple of (username, password).  **TYPE:** `Optional[Tuple[str, str]]`  **DEFAULT:** `None` |
| `timeout` | Number of seconds to wait before timing out.  **TYPE:** `Optional[int | float]`  **DEFAULT:** `30` |
| `headers` | Headers to include in the session with every request.  **TYPE:** `Optional[Dict[str, str]]`  **DEFAULT:** `None` |
| `retries` | Number of retry attempts. Defaults to 3.  **TYPE:** `Optional[int]`  **DEFAULT:** `3` |
| `retry_delay` | Number of seconds to wait between retry attempts. Defaults to 1 second.  **TYPE:** `Optional[int]`  **DEFAULT:** `1` |
| `follow_redirects` | Whether to follow redirects. Defaults to True.  **TYPE:** `bool`  **DEFAULT:** `True` |
| `max_redirects` | Maximum number of redirects. Default 30, use -1 for unlimited.  **TYPE:** `int`  **DEFAULT:** `30` |
| `verify` | Whether to verify HTTPS certificates. Defaults to True.  **TYPE:** `bool`  **DEFAULT:** `True` |
| `cert` | Tuple of (cert, key) filenames for the client certificate.  **TYPE:** `Optional[str | Tuple[str, str]]`  **DEFAULT:** `None` |
| `selector_config` | Arguments passed when creating the final Selector class.  **TYPE:** `Optional[Dict]`  **DEFAULT:** `None` |
| `proxy_rotator` | A ProxyRotator instance for automatic proxy rotation.  **TYPE:** `Optional[ProxyRotator]`  **DEFAULT:** `None` |

Source code in `scrapling/engines/static.py`

|  |  |
| --- | --- |
| ``` 653 654 655 656 657 658 659 660 661 662 663 664 665 666 667 668 669 670 671 672 673 674 675 676 677 678 679 680 681 682 683 684 685 686 687 688 689 690 691 692 693 694 695 696 697 698 699 700 701 702 703 704 705 706 707 708 ``` | ``` def __init__(     self,     impersonate: ImpersonateType = "chrome",     http3: Optional[bool] = False,     stealthy_headers: Optional[bool] = True,     proxies: Optional[Dict[str, str]] = None,     proxy: Optional[str] = None,     proxy_auth: Optional[Tuple[str, str]] = None,     timeout: Optional[int | float] = 30,     headers: Optional[Dict[str, str]] = None,     retries: Optional[int] = 3,     retry_delay: Optional[int] = 1,     follow_redirects: bool = True,     max_redirects: int = 30,     verify: bool = True,     cert: Optional[str | Tuple[str, str]] = None,     selector_config: Optional[Dict] = None,     proxy_rotator: Optional[ProxyRotator] = None, ):     """     :param impersonate: Browser version to impersonate. Can be a single browser string or a list of browser strings for random selection. (Default: latest available Chrome version)     :param http3: Whether to use HTTP3. Defaults to False. It might be problematic if used it with `impersonate`.     :param stealthy_headers: If enabled (default), it creates and adds real browser headers. It also sets a Google referer header.     :param proxies: Dict of proxies to use. Format: {"http": proxy_url, "https": proxy_url}.     :param proxy: Proxy URL to use. Format: "http://username:password@localhost:8030".                  Cannot be used together with the `proxies` parameter.     :param proxy_auth: HTTP basic auth for proxy, tuple of (username, password).     :param timeout: Number of seconds to wait before timing out.     :param headers: Headers to include in the session with every request.     :param retries: Number of retry attempts. Defaults to 3.     :param retry_delay: Number of seconds to wait between retry attempts. Defaults to 1 second.     :param follow_redirects: Whether to follow redirects. Defaults to True.     :param max_redirects: Maximum number of redirects. Default 30, use -1 for unlimited.     :param verify: Whether to verify HTTPS certificates. Defaults to True.     :param cert: Tuple of (cert, key) filenames for the client certificate.     :param selector_config: Arguments passed when creating the final Selector class.     :param proxy_rotator: A ProxyRotator instance for automatic proxy rotation.     """     self._default_impersonate: ImpersonateType = impersonate     self._stealth = stealthy_headers     self._default_proxies = proxies or {}     self._default_proxy = proxy or None     self._default_proxy_auth = proxy_auth or None     self._default_timeout = timeout     self._default_headers = headers or {}     self._default_retries = retries     self._default_retry_delay = retry_delay     self._default_follow_redirects = follow_redirects     self._default_max_redirects = max_redirects     self._default_verify = verify     self._default_cert = cert     self._default_http3 = http3     self.selector_config = selector_config or {}     self._is_alive = False     self._client: _SyncSessionLogic | _ASyncSessionLogic | None = None     self._proxy_rotator = proxy_rotator ``` |

### __slots__ `class-attribute` `instance-attribute` [¶](#scrapling.fetchers.FetcherSession.__slots__ "Permanent link")

```
__slots__ = (
    "_default_impersonate",
    "_stealth",
    "_default_proxies",
    "_default_proxy",
    "_default_proxy_auth",
    "_default_timeout",
    "_default_headers",
    "_default_retries",
    "_default_retry_delay",
    "_default_follow_redirects",
    "_default_max_redirects",
    "_default_verify",
    "_default_cert",
    "_default_http3",
    "selector_config",
    "_client",
    "_is_alive",
    "_proxy_rotator",
)
```

### selector_config `instance-attribute` [¶](#scrapling.fetchers.FetcherSession.selector_config "Permanent link")

```
selector_config = selector_config or {}
```

### __enter__ [¶](#scrapling.fetchers.FetcherSession.__enter__ "Permanent link")

```
__enter__()
```

Creates and returns a new synchronous Fetcher Session

Source code in `scrapling/engines/static.py`

|  |  |
| --- | --- |
| ``` 710 711 712 713 714 715 716 717 718 719 720 721 ``` | ``` def __enter__(self) -> _SyncSessionLogic:     """Creates and returns a new synchronous Fetcher Session"""     if self._client is None:         # Use **vars(self) to avoid repeating all parameters         config = {k.replace("_default_", ""): getattr(self, k) for k in self.__slots__ if k.startswith("_default")}         config["stealthy_headers"] = self._stealth         config["selector_config"] = self.selector_config         config["proxy_rotator"] = self._proxy_rotator         self._client = _SyncSessionLogic(**config)         self._is_alive = True         return self._client.__enter__()     raise RuntimeError("This FetcherSession instance already has an active synchronous session.") ``` |

### __exit__ [¶](#scrapling.fetchers.FetcherSession.__exit__ "Permanent link")

```
__exit__(exc_type, exc_val, exc_tb)
```

Source code in `scrapling/engines/static.py`

|  |  |
| --- | --- |
| ``` 723 724 725 726 727 728 729 ``` | ``` def __exit__(self, exc_type, exc_val, exc_tb):     if self._client is not None and isinstance(self._client, _SyncSessionLogic):         self._client.__exit__(exc_type, exc_val, exc_tb)         self._client = None         self._is_alive = False         return     raise RuntimeError("Cannot exit invalid session") ``` |

### __aenter__ `async` [¶](#scrapling.fetchers.FetcherSession.__aenter__ "Permanent link")

```
__aenter__()
```

Creates and returns a new asynchronous Session.

Source code in `scrapling/engines/static.py`

|  |  |
| --- | --- |
| ``` 731 732 733 734 735 736 737 738 739 740 741 742 ``` | ``` async def __aenter__(self) -> _ASyncSessionLogic:     """Creates and returns a new asynchronous Session."""     if self._client is None:         # Use **vars(self) to avoid repeating all parameters         config = {k.replace("_default_", ""): getattr(self, k) for k in self.__slots__ if k.startswith("_default")}         config["stealthy_headers"] = self._stealth         config["selector_config"] = self.selector_config         config["proxy_rotator"] = self._proxy_rotator         self._client = _ASyncSessionLogic(**config)         self._is_alive = True         return await self._client.__aenter__()     raise RuntimeError("This FetcherSession instance already has an active asynchronous session.") ``` |

### __aexit__ `async` [¶](#scrapling.fetchers.FetcherSession.__aexit__ "Permanent link")

```
__aexit__(exc_type, exc_val, exc_tb)
```

Source code in `scrapling/engines/static.py`

|  |  |
| --- | --- |
| ``` 744 745 746 747 748 749 750 ``` | ``` async def __aexit__(self, exc_type, exc_val, exc_tb):     if self._client is not None and isinstance(self._client, _ASyncSessionLogic):         await self._client.__aexit__(exc_type, exc_val, exc_tb)         self._client = None         self._is_alive = False         return     raise RuntimeError("Cannot exit invalid session") ``` |

### Stealth Sessions[¶](#stealth-sessions "Permanent link")

## scrapling.fetchers.StealthySession [¶](#scrapling.fetchers.StealthySession "Permanent link")

```
StealthySession(**kwargs)
```

Bases: `SyncSession`, `StealthySessionMixin`

```
              flowchart TD
              scrapling.fetchers.StealthySession[StealthySession]
              scrapling.engines._browsers._base.SyncSession[SyncSession]
              scrapling.engines._browsers._base.StealthySessionMixin[StealthySessionMixin]
              scrapling.engines._browsers._base.BaseSessionMixin[BaseSessionMixin]

                              scrapling.engines._browsers._base.SyncSession --> scrapling.fetchers.StealthySession
                
                scrapling.engines._browsers._base.StealthySessionMixin --> scrapling.fetchers.StealthySession
                                scrapling.engines._browsers._base.BaseSessionMixin --> scrapling.engines._browsers._base.StealthySessionMixin
                



              click scrapling.fetchers.StealthySession href "" "scrapling.fetchers.StealthySession"
              click scrapling.engines._browsers._base.SyncSession href "" "scrapling.engines._browsers._base.SyncSession"
              click scrapling.engines._browsers._base.StealthySessionMixin href "" "scrapling.engines._browsers._base.StealthySessionMixin"
              click scrapling.engines._browsers._base.BaseSessionMixin href "" "scrapling.engines._browsers._base.BaseSessionMixin"
```

A Stealthy Browser session manager with page pooling.

A Browser session manager with page pooling, it's using a persistent browser Context by default with a temporary user profile directory.

| PARAMETER | DESCRIPTION |
| --- | --- |
| `headless` | Run the browser in headless/hidden (default), or headful/visible mode. |
| `disable_resources` | Drop requests for unnecessary resources for a speed boost. Requests dropped are of type `font`, `image`, `media`, `beacon`, `object`, `imageset`, `texttrack`, `websocket`, `csp_report`, and `stylesheet`. |
| `blocked_domains` | A set of domain names to block requests to. Subdomains are also matched (e.g., `"example.com"` blocks `"sub.example.com"` too). |
| `useragent` | Pass a useragent string to be used. Otherwise the fetcher will generate a real Useragent of the same browser and use it. |
| `cookies` | Set cookies for the next request. |
| `network_idle` | Wait for the page until there are no network connections for at least 500 ms. |
| `timeout` | The timeout in milliseconds that is used in all operations and waits through the page. The default is 30,000 |
| `wait` | The time (milliseconds) the fetcher will wait after everything finishes before closing the page and returning the `Response` object. |
| `page_action` | Added for automation. A function that takes the `page` object and does the automation you need. |
| `wait_selector` | Wait for a specific CSS selector to be in a specific state. |
| `init_script` | An absolute path to a JavaScript file to be executed on page creation for all pages in this session. |
| `locale` | Specify user locale, for example, `en-GB`, `de-DE`, etc. Locale will affect navigator.language value, Accept-Language request header value as well as number and date formatting rules. Defaults to the system default locale. |
| `timezone_id` | Changes the timezone of the browser. Defaults to the system timezone. |
| `wait_selector_state` | The state to wait for the selector given with `wait_selector`. The default state is `attached`. |
| `solve_cloudflare` | Solves all types of the Cloudflare's Turnstile/Interstitial challenges before returning the response to you. |
| `real_chrome` | If you have a Chrome browser installed on your device, enable this, and the Fetcher will launch an instance of your browser and use it. |
| `hide_canvas` | Add random noise to canvas operations to prevent fingerprinting. |
| `block_webrtc` | Forces WebRTC to respect proxy settings to prevent local IP address leak. |
| `allow_webgl` | Enabled by default. Disabling it disables WebGL and WebGL 2.0 support entirely. Disabling WebGL is not recommended as many WAFs now check if WebGL is enabled. |
| `load_dom` | Enabled by default, wait for all JavaScript on page(s) to fully load and execute. |
| `cdp_url` | Instead of launching a new browser instance, connect to this CDP URL to control real browsers through CDP. |
| `google_search` | Enabled by default, Scrapling will set a Google referer header. |
| `extra_headers` | A dictionary of extra headers to add to the request. *The referer set by `google_search` takes priority over the referer set here if used together.* |
| `proxy` | The proxy to be used with requests, it can be a string or a dictionary with the keys 'server', 'username', and 'password' only. |
| `user_data_dir` | Path to a User Data Directory, which stores browser session data like cookies and local storage. The default is to create a temporary directory. |
| `extra_flags` | A list of additional browser flags to pass to the browser on launch. |
| `selector_config` | The arguments that will be passed in the end while creating the final Selector's class. |
| `additional_args` | Additional arguments to be passed to Playwright's context as additional settings, and it takes higher priority than Scrapling's settings. |

Source code in `scrapling/engines/_browsers/_stealth.py`

|  |  |
| --- | --- |
| ``` 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 ``` | ``` def __init__(self, **kwargs: Unpack[StealthSession]):     """A Browser session manager with page pooling, it's using a persistent browser Context by default with a temporary user profile directory.      :param headless: Run the browser in headless/hidden (default), or headful/visible mode.     :param disable_resources: Drop requests for unnecessary resources for a speed boost.         Requests dropped are of type `font`, `image`, `media`, `beacon`, `object`, `imageset`, `texttrack`, `websocket`, `csp_report`, and `stylesheet`.     :param blocked_domains: A set of domain names to block requests to. Subdomains are also matched (e.g., ``"example.com"`` blocks ``"sub.example.com"`` too).     :param useragent: Pass a useragent string to be used. Otherwise the fetcher will generate a real Useragent of the same browser and use it.     :param cookies: Set cookies for the next request.     :param network_idle: Wait for the page until there are no network connections for at least 500 ms.     :param timeout: The timeout in milliseconds that is used in all operations and waits through the page. The default is 30,000     :param wait: The time (milliseconds) the fetcher will wait after everything finishes before closing the page and returning the ` Response ` object.     :param page_action: Added for automation. A function that takes the `page` object and does the automation you need.     :param wait_selector: Wait for a specific CSS selector to be in a specific state.     :param init_script: An absolute path to a JavaScript file to be executed on page creation for all pages in this session.     :param locale: Specify user locale, for example, `en-GB`, `de-DE`, etc. Locale will affect navigator.language value, Accept-Language request header value as well as number and date formatting         rules. Defaults to the system default locale.     :param timezone_id: Changes the timezone of the browser. Defaults to the system timezone.     :param wait_selector_state: The state to wait for the selector given with `wait_selector`. The default state is `attached`.     :param solve_cloudflare: Solves all types of the Cloudflare's Turnstile/Interstitial challenges before returning the response to you.     :param real_chrome: If you have a Chrome browser installed on your device, enable this, and the Fetcher will launch an instance of your browser and use it.     :param hide_canvas: Add random noise to canvas operations to prevent fingerprinting.     :param block_webrtc: Forces WebRTC to respect proxy settings to prevent local IP address leak.     :param allow_webgl: Enabled by default. Disabling it disables WebGL and WebGL 2.0 support entirely. Disabling WebGL is not recommended as many WAFs now check if WebGL is enabled.     :param load_dom: Enabled by default, wait for all JavaScript on page(s) to fully load and execute.     :param cdp_url: Instead of launching a new browser instance, connect to this CDP URL to control real browsers through CDP.     :param google_search: Enabled by default, Scrapling will set a Google referer header.     :param extra_headers: A dictionary of extra headers to add to the request. _The referer set by `google_search` takes priority over the referer set here if used together._     :param proxy: The proxy to be used with requests, it can be a string or a dictionary with the keys 'server', 'username', and 'password' only.     :param user_data_dir: Path to a User Data Directory, which stores browser session data like cookies and local storage. The default is to create a temporary directory.     :param extra_flags: A list of additional browser flags to pass to the browser on launch.     :param selector_config: The arguments that will be passed in the end while creating the final Selector's class.     :param additional_args: Additional arguments to be passed to Playwright's context as additional settings, and it takes higher priority than Scrapling's settings.     """     self.__validate__(**kwargs)     super().__init__() ``` |

### max_pages `instance-attribute` [¶](#scrapling.fetchers.StealthySession.max_pages "Permanent link")

```
max_pages = max_pages
```

### page_pool `instance-attribute` [¶](#scrapling.fetchers.StealthySession.page_pool "Permanent link")

```
page_pool = PagePool(max_pages)
```

### playwright `instance-attribute` [¶](#scrapling.fetchers.StealthySession.playwright "Permanent link")

```
playwright = None
```

### context `instance-attribute` [¶](#scrapling.fetchers.StealthySession.context "Permanent link")

```
context = None
```

### browser `instance-attribute` [¶](#scrapling.fetchers.StealthySession.browser "Permanent link")

```
browser = None
```

### __slots__ `class-attribute` `instance-attribute` [¶](#scrapling.fetchers.StealthySession.__slots__ "Permanent link")

```
__slots__ = (
    "_config",
    "_context_options",
    "_browser_options",
    "_user_data_dir",
    "_headers_keys",
    "max_pages",
    "page_pool",
    "_max_wait_for_page",
    "playwright",
    "context",
)
```

### __validate_routine__ [¶](#scrapling.fetchers.StealthySession.__validate_routine__ "Permanent link")

```
__validate_routine__(params, model)
```

Source code in `scrapling/engines/_browsers/_base.py`

|  |  |
| --- | --- |
| ``` 412 413 414 415 416 417 418 419 420 421 422 423 424 425 426 427 428 429 ``` | ``` def __validate_routine__(     self, params: Dict, model: type[PlaywrightConfig] | type[StealthConfig] ) -> PlaywrightConfig | StealthConfig:     # Dark color scheme bypasses the 'prefersLightColor' check in creepjs     self._context_options: Dict[str, Any] = {"color_scheme": "dark", "device_scale_factor": 2}     self._browser_options: Dict[str, Any] = {         "args": DEFAULT_ARGS,         "ignore_default_args": HARMFUL_ARGS,     }     if "__max_pages" in params:         params["max_pages"] = params.pop("__max_pages")      config = validate(params, model=model)     self._headers_keys = (         {header.lower() for header in config.extra_headers.keys()} if config.extra_headers else set()     )      return config ``` |

### __generate_options__ [¶](#scrapling.fetchers.StealthySession.__generate_options__ "Permanent link")

```
__generate_options__(extra_flags=None)
```

Source code in `scrapling/engines/_browsers/_base.py`

|  |  |
| --- | --- |
| ``` 431 432 433 434 435 436 437 438 439 440 441 442 443 444 445 446 447 448 449 450 451 452 453 454 455 456 457 458 459 460 461 462 463 464 465 466 467 468 469 ``` | ``` def __generate_options__(self, extra_flags: Tuple | None = None) -> None:     config: PlaywrightConfig | StealthConfig = self._config     self._context_options.update(         {             "proxy": config.proxy,             "locale": config.locale,             "timezone_id": config.timezone_id,             "extra_http_headers": config.extra_headers,         }     )     # The default useragent in the headful is always correct now in the current versions of Playwright     if config.useragent:         self._context_options["user_agent"] = config.useragent     elif not config.useragent and config.headless:         self._context_options["user_agent"] = (             __default_chrome_useragent__ if config.real_chrome else __default_useragent__         )      if not config.cdp_url:         flags = self._browser_options["args"]         if config.extra_flags or extra_flags:             flags = list(set(tuple(flags) + tuple(config.extra_flags or extra_flags or ())))          self._browser_options.update(             {                 "args": flags,                 "headless": config.headless,                 "channel": "chrome" if config.real_chrome else "chromium",             }         )         if config.executable_path:             self._browser_options["executable_path"] = config.executable_path          self._user_data_dir = config.user_data_dir     else:         self._browser_options = {}      if config.additional_args:         self._context_options.update(config.additional_args) ``` |

### __validate__ [¶](#scrapling.fetchers.StealthySession.__validate__ "Permanent link")

```
__validate__(**params)
```

Source code in `scrapling/engines/_browsers/_base.py`

|  |  |
| --- | --- |
| ``` 495 496 497 498 499 500 501 502 503 504 505 506 507 508 509 ``` | ``` def __validate__(self, **params):     self._config = self.__validate_routine__(params, model=StealthConfig)     self._context_options.update(         {             "is_mobile": False,             "has_touch": False,             # I'm thinking about disabling it to rest from all Service Workers' headache, but let's keep it as it is for now             "service_workers": "allow",             "ignore_https_errors": True,             "screen": {"width": 1920, "height": 1080},             "viewport": {"width": 1920, "height": 1080},             "permissions": ["geolocation", "notifications"],         }     )     self.__generate_stealth_options() ``` |

### close [¶](#scrapling.fetchers.StealthySession.close "Permanent link")

```
close()
```

Close all resources

Source code in `scrapling/engines/_browsers/_base.py`

|  |  |
| --- | --- |
| ``` 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 ``` | ``` def close(self):  # pragma: no cover     """Close all resources"""     if not self._is_alive:         return      if self.context:         self.context.close()         self.context = None      if self.browser:         self.browser.close()         self.browser = None      if self.playwright:         self.playwright.stop()         self.playwright = None  # pyright: ignore      self._is_alive = False ``` |

### __enter__ [¶](#scrapling.fetchers.StealthySession.__enter__ "Permanent link")

```
__enter__()
```

Source code in `scrapling/engines/_browsers/_base.py`

|  |  |
| --- | --- |
| ``` 86 87 88 ``` | ``` def __enter__(self):     self.start()     return self ``` |

### __exit__ [¶](#scrapling.fetchers.StealthySession.__exit__ "Permanent link")

```
__exit__(exc_type, exc_val, exc_tb)
```

Source code in `scrapling/engines/_browsers/_base.py`

|  |  |
| --- | --- |
| ``` 90 91 ``` | ``` def __exit__(self, exc_type, exc_val, exc_tb):     self.close() ``` |

### get_pool_stats [¶](#scrapling.fetchers.StealthySession.get_pool_stats "Permanent link")

```
get_pool_stats()
```

Get statistics about the current page pool

Source code in `scrapling/engines/_browsers/_base.py`

|  |  |
| --- | --- |
| ``` 127 128 129 130 131 132 133 ``` | ``` def get_pool_stats(self) -> Dict[str, int]:     """Get statistics about the current page pool"""     return {         "total_pages": self.page_pool.pages_count,         "busy_pages": self.page_pool.busy_count,         "max_pages": self.max_pages,     } ``` |

### start [¶](#scrapling.fetchers.StealthySession.start "Permanent link")

```
start()
```

Create a browser for this instance and context.

Source code in `scrapling/engines/_browsers/_stealth.py`

|  |  |
| --- | --- |
| ```  75  76  77  78  79  80  81  82  83  84  85  86  87  88  89  90  91  92  93  94  95  96  97  98  99 100 101 102 103 104 ``` | ``` def start(self) -> None:     """Create a browser for this instance and context."""     if not self.playwright:         self.playwright = sync_playwright().start()          try:             if self._config.cdp_url:  # pragma: no cover                 self.browser = self.playwright.chromium.connect_over_cdp(endpoint_url=self._config.cdp_url)                 if not self._config.proxy_rotator:                     assert self.browser is not None                     self.context = self.browser.new_context(**self._context_options)             elif self._config.proxy_rotator:                 self.browser = self.playwright.chromium.launch(**self._browser_options)             else:                 persistent_options = (                     self._browser_options | self._context_options | {"user_data_dir": self._user_data_dir}                 )                 self.context = self.playwright.chromium.launch_persistent_context(**persistent_options)              if self.context:                 self.context = self._initialize_context(self._config, self.context)              self._is_alive = True         except Exception:             # Clean up playwright if browser setup fails             self.playwright.stop()             self.playwright = None             raise     else:         raise RuntimeError("Session has been already started") ``` |

### fetch [¶](#scrapling.fetchers.StealthySession.fetch "Permanent link")

```
fetch(url, **kwargs)
```

Opens up the browser and do your request based on your chosen options.

| PARAMETER | DESCRIPTION |
| --- | --- |
| `url` | The Target url.  **TYPE:** `str` |
| `google_search` | Enabled by default, Scrapling will set a Google referer header. |
| `timeout` | The timeout in milliseconds that is used in all operations and waits through the page. The default is 30,000 |
| `wait` | The time (milliseconds) the fetcher will wait after everything finishes before closing the page and returning the `Response` object. |
| `page_action` | Added for automation. A function that takes the `page` object and does the automation you need. |
| `extra_headers` | A dictionary of extra headers to add to the request. *The referer set by `google_search` takes priority over the referer set here if used together.* |
| `disable_resources` | Drop requests for unnecessary resources for a speed boost. Requests dropped are of type `font`, `image`, `media`, `beacon`, `object`, `imageset`, `texttrack`, `websocket`, `csp_report`, and `stylesheet`. |
| `blocked_domains` | A set of domain names to block requests to. Subdomains are also matched (e.g., `"example.com"` blocks `"sub.example.com"` too). |
| `wait_selector` | Wait for a specific CSS selector to be in a specific state. |
| `wait_selector_state` | The state to wait for the selector given with `wait_selector`. The default state is `attached`. |
| `network_idle` | Wait for the page until there are no network connections for at least 500 ms. |
| `load_dom` | Enabled by default, wait for all JavaScript on page(s) to fully load and execute. |
| `solve_cloudflare` | Solves all types of the Cloudflare's Turnstile/Interstitial challenges before returning the response to you. |
| `selector_config` | The arguments that will be passed in the end while creating the final Selector's class. |
| `proxy` | Static proxy to override rotator and session proxy. A new browser context will be created and used with it. |

| RETURNS | DESCRIPTION |
| --- | --- |
| `Response` | A `Response` object. |

Source code in `scrapling/engines/_browsers/_stealth.py`

|  |  |
| --- | --- |
| ``` 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200 201 202 203 204 205 206 207 208 209 210 211 212 213 214 215 216 217 218 219 220 221 222 223 224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239 240 241 242 243 244 245 246 247 248 249 250 251 252 253 254 255 256 257 258 259 260 261 262 263 264 265 266 267 268 269 270 271 272 273 274 275 276 277 278 279 280 281 282 283 284 285 286 287 288 289 290 291 292 ``` | ``` def fetch(self, url: str, **kwargs: Unpack[StealthFetchParams]) -> Response:     """Opens up the browser and do your request based on your chosen options.      :param url: The Target url.     :param google_search: Enabled by default, Scrapling will set a Google referer header.     :param timeout: The timeout in milliseconds that is used in all operations and waits through the page. The default is 30,000     :param wait: The time (milliseconds) the fetcher will wait after everything finishes before closing the page and returning the ` Response ` object.     :param page_action: Added for automation. A function that takes the `page` object and does the automation you need.     :param extra_headers: A dictionary of extra headers to add to the request. _The referer set by `google_search` takes priority over the referer set here if used together._     :param disable_resources: Drop requests for unnecessary resources for a speed boost.         Requests dropped are of type `font`, `image`, `media`, `beacon`, `object`, `imageset`, `texttrack`, `websocket`, `csp_report`, and `stylesheet`.     :param blocked_domains: A set of domain names to block requests to. Subdomains are also matched (e.g., ``"example.com"`` blocks ``"sub.example.com"`` too).     :param wait_selector: Wait for a specific CSS selector to be in a specific state.     :param wait_selector_state: The state to wait for the selector given with `wait_selector`. The default state is `attached`.     :param network_idle: Wait for the page until there are no network connections for at least 500 ms.     :param load_dom: Enabled by default, wait for all JavaScript on page(s) to fully load and execute.     :param solve_cloudflare: Solves all types of the Cloudflare's Turnstile/Interstitial challenges before returning the response to you.     :param selector_config: The arguments that will be passed in the end while creating the final Selector's class.     :param proxy: Static proxy to override rotator and session proxy. A new browser context will be created and used with it.     :return: A `Response` object.     """     static_proxy = kwargs.pop("proxy", None)      params = _validate(kwargs, self, StealthConfig)     if not self._is_alive:  # pragma: no cover         raise RuntimeError("Context manager has been closed")      request_headers_keys = {h.lower() for h in params.extra_headers.keys()} if params.extra_headers else set()     referer = (         "https://www.google.com/" if (params.google_search and "referer" not in request_headers_keys) else None     )      for attempt in range(self._config.retries):         proxy: Optional[ProxyType] = None         if self._config.proxy_rotator and static_proxy is None:             proxy = self._config.proxy_rotator.get_proxy()         else:             proxy = static_proxy          with self._page_generator(             params.timeout, params.extra_headers, params.disable_resources, proxy, params.blocked_domains         ) as page_info:             final_response: List = [None]             xhr_captured: List = []             page = page_info.page             page.on(                 "response",                 self._create_response_handler(                     page_info,                     final_response,                     xhr_pattern=self._config.capture_xhr,                     xhr_container=xhr_captured,                 ),             )              try:                 first_response = page.goto(url, referer=referer)                 self._wait_for_page_stability(page, params.load_dom, params.network_idle)                  if not first_response:                     raise RuntimeError(f"Failed to get response for {url}")                  if params.solve_cloudflare:                     self._cloudflare_solver(page)                     # Make sure the page is fully loaded after the captcha                     self._wait_for_page_stability(page, params.load_dom, params.network_idle)                  if params.page_action:                     try:                         _ = params.page_action(page)                     except Exception as e:  # pragma: no cover                         log.error(f"Error executing page_action: {e}")                  if params.wait_selector:                     try:                         waiter: Locator = page.locator(params.wait_selector)                         waiter.first.wait_for(state=params.wait_selector_state)                         self._wait_for_page_stability(page, params.load_dom, params.network_idle)                     except Exception as e:  # pragma: no cover                         log.error(f"Error waiting for selector {params.wait_selector}: {e}")                  page.wait_for_timeout(params.wait)                  response = ResponseFactory.from_playwright_response(                     page,                     first_response,                     final_response[0],                     params.selector_config,                     meta={"proxy": proxy},                     xhr_captured=xhr_captured,                 )                 return response              except Exception as e:                 page_info.mark_error()                 if attempt < self._config.retries - 1:                     if is_proxy_error(e):                         log.warning(                             f"Proxy '{proxy}' failed (attempt {attempt + 1}) | Retrying in {self._config.retry_delay}s..."                         )                     else:                         log.warning(                             f"Attempt {attempt + 1} failed: {e}. Retrying in {self._config.retry_delay}s..."                         )                     time_sleep(self._config.retry_delay)                 else:                     log.error(f"Failed after {self._config.retries} attempts: {e}")                     raise      raise RuntimeError("Request failed")  # pragma: no cover ``` |

## scrapling.fetchers.AsyncStealthySession [¶](#scrapling.fetchers.AsyncStealthySession "Permanent link")

```
AsyncStealthySession(**kwargs)
```

Bases: `AsyncSession`, `StealthySessionMixin`

```
              flowchart TD
              scrapling.fetchers.AsyncStealthySession[AsyncStealthySession]
              scrapling.engines._browsers._base.AsyncSession[AsyncSession]
              scrapling.engines._browsers._base.StealthySessionMixin[StealthySessionMixin]
              scrapling.engines._browsers._base.BaseSessionMixin[BaseSessionMixin]

                              scrapling.engines._browsers._base.AsyncSession --> scrapling.fetchers.AsyncStealthySession
                
                scrapling.engines._browsers._base.StealthySessionMixin --> scrapling.fetchers.AsyncStealthySession
                                scrapling.engines._browsers._base.BaseSessionMixin --> scrapling.engines._browsers._base.StealthySessionMixin
                



              click scrapling.fetchers.AsyncStealthySession href "" "scrapling.fetchers.AsyncStealthySession"
              click scrapling.engines._browsers._base.AsyncSession href "" "scrapling.engines._browsers._base.AsyncSession"
              click scrapling.engines._browsers._base.StealthySessionMixin href "" "scrapling.engines._browsers._base.StealthySessionMixin"
              click scrapling.engines._browsers._base.BaseSessionMixin href "" "scrapling.engines._browsers._base.BaseSessionMixin"
```

An async Stealthy Browser session manager with page pooling.

A Browser session manager with page pooling, it's using a persistent browser Context by default with a temporary user profile directory.

| PARAMETER | DESCRIPTION |
| --- | --- |
| `headless` | Run the browser in headless/hidden (default), or headful/visible mode. |
| `disable_resources` | Drop requests for unnecessary resources for a speed boost. Requests dropped are of type `font`, `image`, `media`, `beacon`, `object`, `imageset`, `texttrack`, `websocket`, `csp_report`, and `stylesheet`. |
| `blocked_domains` | A set of domain names to block requests to. Subdomains are also matched (e.g., `"example.com"` blocks `"sub.example.com"` too). |
| `useragent` | Pass a useragent string to be used. Otherwise the fetcher will generate a real Useragent of the same browser and use it. |
| `cookies` | Set cookies for the next request. |
| `network_idle` | Wait for the page until there are no network connections for at least 500 ms. |
| `timeout` | The timeout in milliseconds that is used in all operations and waits through the page. The default is 30,000 |
| `wait` | The time (milliseconds) the fetcher will wait after everything finishes before closing the page and returning the `Response` object. |
| `page_action` | Added for automation. A function that takes the `page` object and does the automation you need. |
| `wait_selector` | Wait for a specific CSS selector to be in a specific state. |
| `init_script` | An absolute path to a JavaScript file to be executed on page creation for all pages in this session. |
| `locale` | Specify user locale, for example, `en-GB`, `de-DE`, etc. Locale will affect navigator.language value, Accept-Language request header value as well as number and date formatting rules. Defaults to the system default locale. |
| `timezone_id` | Changes the timezone of the browser. Defaults to the system timezone. |
| `wait_selector_state` | The state to wait for the selector given with `wait_selector`. The default state is `attached`. |
| `solve_cloudflare` | Solves all types of the Cloudflare's Turnstile/Interstitial challenges before returning the response to you. |
| `real_chrome` | If you have a Chrome browser installed on your device, enable this, and the Fetcher will launch an instance of your browser and use it. |
| `hide_canvas` | Add random noise to canvas operations to prevent fingerprinting. |
| `block_webrtc` | Forces WebRTC to respect proxy settings to prevent local IP address leak. |
| `allow_webgl` | Enabled by default. Disabling it disables WebGL and WebGL 2.0 support entirely. Disabling WebGL is not recommended as many WAFs now check if WebGL is enabled. |
| `load_dom` | Enabled by default, wait for all JavaScript on page(s) to fully load and execute. |
| `cdp_url` | Instead of launching a new browser instance, connect to this CDP URL to control real browsers through CDP. |
| `google_search` | Enabled by default, Scrapling will set a Google referer header. |
| `extra_headers` | A dictionary of extra headers to add to the request. *The referer set by `google_search` takes priority over the referer set here if used together.* |
| `proxy` | The proxy to be used with requests, it can be a string or a dictionary with the keys 'server', 'username', and 'password' only. |
| `user_data_dir` | Path to a User Data Directory, which stores browser session data like cookies and local storage. The default is to create a temporary directory. |
| `extra_flags` | A list of additional browser flags to pass to the browser on launch. |
| `selector_config` | The arguments that will be passed in the end while creating the final Selector's class. |
| `additional_args` | Additional arguments to be passed to Playwright's context as additional settings, and it takes higher priority than Scrapling's settings. |

Source code in `scrapling/engines/_browsers/_stealth.py`

|  |  |
| --- | --- |
| ``` 306 307 308 309 310 311 312 313 314 315 316 317 318 319 320 321 322 323 324 325 326 327 328 329 330 331 332 333 334 335 336 337 338 339 340 341 ``` | ``` def __init__(self, **kwargs: Unpack[StealthSession]):     """A Browser session manager with page pooling, it's using a persistent browser Context by default with a temporary user profile directory.      :param headless: Run the browser in headless/hidden (default), or headful/visible mode.     :param disable_resources: Drop requests for unnecessary resources for a speed boost.         Requests dropped are of type `font`, `image`, `media`, `beacon`, `object`, `imageset`, `texttrack`, `websocket`, `csp_report`, and `stylesheet`.     :param blocked_domains: A set of domain names to block requests to. Subdomains are also matched (e.g., ``"example.com"`` blocks ``"sub.example.com"`` too).     :param useragent: Pass a useragent string to be used. Otherwise the fetcher will generate a real Useragent of the same browser and use it.     :param cookies: Set cookies for the next request.     :param network_idle: Wait for the page until there are no network connections for at least 500 ms.     :param timeout: The timeout in milliseconds that is used in all operations and waits through the page. The default is 30,000     :param wait: The time (milliseconds) the fetcher will wait after everything finishes before closing the page and returning the ` Response ` object.     :param page_action: Added for automation. A function that takes the `page` object and does the automation you need.     :param wait_selector: Wait for a specific CSS selector to be in a specific state.     :param init_script: An absolute path to a JavaScript file to be executed on page creation for all pages in this session.     :param locale: Specify user locale, for example, `en-GB`, `de-DE`, etc. Locale will affect navigator.language value, Accept-Language request header value as well as number and date formatting         rules. Defaults to the system default locale.     :param timezone_id: Changes the timezone of the browser. Defaults to the system timezone.     :param wait_selector_state: The state to wait for the selector given with `wait_selector`. The default state is `attached`.     :param solve_cloudflare: Solves all types of the Cloudflare's Turnstile/Interstitial challenges before returning the response to you.     :param real_chrome: If you have a Chrome browser installed on your device, enable this, and the Fetcher will launch an instance of your browser and use it.     :param hide_canvas: Add random noise to canvas operations to prevent fingerprinting.     :param block_webrtc: Forces WebRTC to respect proxy settings to prevent local IP address leak.     :param allow_webgl: Enabled by default. Disabling it disables WebGL and WebGL 2.0 support entirely. Disabling WebGL is not recommended as many WAFs now check if WebGL is enabled.     :param load_dom: Enabled by default, wait for all JavaScript on page(s) to fully load and execute.     :param cdp_url: Instead of launching a new browser instance, connect to this CDP URL to control real browsers through CDP.     :param google_search: Enabled by default, Scrapling will set a Google referer header.     :param extra_headers: A dictionary of extra headers to add to the request. _The referer set by `google_search` takes priority over the referer set here if used together._     :param proxy: The proxy to be used with requests, it can be a string or a dictionary with the keys 'server', 'username', and 'password' only.     :param user_data_dir: Path to a User Data Directory, which stores browser session data like cookies and local storage. The default is to create a temporary directory.     :param extra_flags: A list of additional browser flags to pass to the browser on launch.     :param selector_config: The arguments that will be passed in the end while creating the final Selector's class.     :param additional_args: Additional arguments to be passed to Playwright's context as additional settings, and it takes higher priority than Scrapling's settings.     """     self.__validate__(**kwargs)     super().__init__(max_pages=self._config.max_pages) ``` |

### max_pages `instance-attribute` [¶](#scrapling.fetchers.AsyncStealthySession.max_pages "Permanent link")

```
max_pages = max_pages
```

### page_pool `instance-attribute` [¶](#scrapling.fetchers.AsyncStealthySession.page_pool "Permanent link")

```
page_pool = PagePool(max_pages)
```

### playwright `instance-attribute` [¶](#scrapling.fetchers.AsyncStealthySession.playwright "Permanent link")

```
playwright = None
```

### context `instance-attribute` [¶](#scrapling.fetchers.AsyncStealthySession.context "Permanent link")

```
context = None
```

### browser `instance-attribute` [¶](#scrapling.fetchers.AsyncStealthySession.browser "Permanent link")

```
browser = None
```

### __slots__ `class-attribute` `instance-attribute` [¶](#scrapling.fetchers.AsyncStealthySession.__slots__ "Permanent link")

```
__slots__ = (
    "_config",
    "_context_options",
    "_browser_options",
    "_user_data_dir",
    "_headers_keys",
)
```

### __validate_routine__ [¶](#scrapling.fetchers.AsyncStealthySession.__validate_routine__ "Permanent link")

```
__validate_routine__(params, model)
```

Source code in `scrapling/engines/_browsers/_base.py`

|  |  |
| --- | --- |
| ``` 412 413 414 415 416 417 418 419 420 421 422 423 424 425 426 427 428 429 ``` | ``` def __validate_routine__(     self, params: Dict, model: type[PlaywrightConfig] | type[StealthConfig] ) -> PlaywrightConfig | StealthConfig:     # Dark color scheme bypasses the 'prefersLightColor' check in creepjs     self._context_options: Dict[str, Any] = {"color_scheme": "dark", "device_scale_factor": 2}     self._browser_options: Dict[str, Any] = {         "args": DEFAULT_ARGS,         "ignore_default_args": HARMFUL_ARGS,     }     if "__max_pages" in params:         params["max_pages"] = params.pop("__max_pages")      config = validate(params, model=model)     self._headers_keys = (         {header.lower() for header in config.extra_headers.keys()} if config.extra_headers else set()     )      return config ``` |

### __generate_options__ [¶](#scrapling.fetchers.AsyncStealthySession.__generate_options__ "Permanent link")

```
__generate_options__(extra_flags=None)
```

Source code in `scrapling/engines/_browsers/_base.py`

|  |  |
| --- | --- |
| ``` 431 432 433 434 435 436 437 438 439 440 441 442 443 444 445 446 447 448 449 450 451 452 453 454 455 456 457 458 459 460 461 462 463 464 465 466 467 468 469 ``` | ``` def __generate_options__(self, extra_flags: Tuple | None = None) -> None:     config: PlaywrightConfig | StealthConfig = self._config     self._context_options.update(         {             "proxy": config.proxy,             "locale": config.locale,             "timezone_id": config.timezone_id,             "extra_http_headers": config.extra_headers,         }     )     # The default useragent in the headful is always correct now in the current versions of Playwright     if config.useragent:         self._context_options["user_agent"] = config.useragent     elif not config.useragent and config.headless:         self._context_options["user_agent"] = (             __default_chrome_useragent__ if config.real_chrome else __default_useragent__         )      if not config.cdp_url:         flags = self._browser_options["args"]         if config.extra_flags or extra_flags:             flags = list(set(tuple(flags) + tuple(config.extra_flags or extra_flags or ())))          self._browser_options.update(             {                 "args": flags,                 "headless": config.headless,                 "channel": "chrome" if config.real_chrome else "chromium",             }         )         if config.executable_path:             self._browser_options["executable_path"] = config.executable_path          self._user_data_dir = config.user_data_dir     else:         self._browser_options = {}      if config.additional_args:         self._context_options.update(config.additional_args) ``` |

### __validate__ [¶](#scrapling.fetchers.AsyncStealthySession.__validate__ "Permanent link")

```
__validate__(**params)
```

Source code in `scrapling/engines/_browsers/_base.py`

|  |  |
| --- | --- |
| ``` 495 496 497 498 499 500 501 502 503 504 505 506 507 508 509 ``` | ``` def __validate__(self, **params):     self._config = self.__validate_routine__(params, model=StealthConfig)     self._context_options.update(         {             "is_mobile": False,             "has_touch": False,             # I'm thinking about disabling it to rest from all Service Workers' headache, but let's keep it as it is for now             "service_workers": "allow",             "ignore_https_errors": True,             "screen": {"width": 1920, "height": 1080},             "viewport": {"width": 1920, "height": 1080},             "permissions": ["geolocation", "notifications"],         }     )     self.__generate_stealth_options() ``` |

### close `async` [¶](#scrapling.fetchers.AsyncStealthySession.close "Permanent link")

```
close()
```

Close all resources

Source code in `scrapling/engines/_browsers/_base.py`

|  |  |
| --- | --- |
| ``` 236 237 238 239 240 241 242 243 244 245 246 247 248 249 250 251 252 253 ``` | ``` async def close(self):     """Close all resources"""     if not self._is_alive:  # pragma: no cover         return      if self.context:         await self.context.close()         self.context = None  # pyright: ignore      if self.browser:         await self.browser.close()         self.browser = None      if self.playwright:         await self.playwright.stop()         self.playwright = None  # pyright: ignore      self._is_alive = False ``` |

### __aenter__ `async` [¶](#scrapling.fetchers.AsyncStealthySession.__aenter__ "Permanent link")

```
__aenter__()
```

Source code in `scrapling/engines/_browsers/_base.py`

|  |  |
| --- | --- |
| ``` 255 256 257 ``` | ``` async def __aenter__(self):     await self.start()     return self ``` |

### __aexit__ `async` [¶](#scrapling.fetchers.AsyncStealthySession.__aexit__ "Permanent link")

```
__aexit__(exc_type, exc_val, exc_tb)
```

Source code in `scrapling/engines/_browsers/_base.py`

|  |  |
| --- | --- |
| ``` 259 260 ``` | ``` async def __aexit__(self, exc_type, exc_val, exc_tb):     await self.close() ``` |

### get_pool_stats [¶](#scrapling.fetchers.AsyncStealthySession.get_pool_stats "Permanent link")

```
get_pool_stats()
```

Get statistics about the current page pool

Source code in `scrapling/engines/_browsers/_base.py`

|  |  |
| --- | --- |
| ``` 312 313 314 315 316 317 318 ``` | ``` def get_pool_stats(self) -> Dict[str, int]:     """Get statistics about the current page pool"""     return {         "total_pages": self.page_pool.pages_count,         "busy_pages": self.page_pool.busy_count,         "max_pages": self.max_pages,     } ``` |

### start `async` [¶](#scrapling.fetchers.AsyncStealthySession.start "Permanent link")

```
start()
```

Create a browser for this instance and context.

Source code in `scrapling/engines/_browsers/_stealth.py`

|  |  |
| --- | --- |
| ``` 343 344 345 346 347 348 349 350 351 352 353 354 355 356 357 358 359 360 361 362 363 364 365 366 367 368 369 370 371 ``` | ``` async def start(self) -> None:     """Create a browser for this instance and context."""     if not self.playwright:         self.playwright = await async_playwright().start()         try:             if self._config.cdp_url:                 self.browser = await self.playwright.chromium.connect_over_cdp(endpoint_url=self._config.cdp_url)                 if not self._config.proxy_rotator:                     assert self.browser is not None                     self.context = await self.browser.new_context(**self._context_options)             elif self._config.proxy_rotator:                 self.browser = await self.playwright.chromium.launch(**self._browser_options)             else:                 persistent_options = (                     self._browser_options | self._context_options | {"user_data_dir": self._user_data_dir}                 )                 self.context = await self.playwright.chromium.launch_persistent_context(**persistent_options)              if self.context:                 self.context = await self._initialize_context(self._config, self.context)              self._is_alive = True         except Exception:             # Clean up playwright if browser setup fails             await self.playwright.stop()             self.playwright = None             raise     else:         raise RuntimeError("Session has been already started") ``` |

### fetch `async` [¶](#scrapling.fetchers.AsyncStealthySession.fetch "Permanent link")

```
fetch(url, **kwargs)
```

Opens up the browser and do your request based on your chosen options.

| PARAMETER | DESCRIPTION |
| --- | --- |
| `url` | The Target url.  **TYPE:** `str` |
| `google_search` | Enabled by default, Scrapling will set a Google referer header. |
| `timeout` | The timeout in milliseconds that is used in all operations and waits through the page. The default is 30,000 |
| `wait` | The time (milliseconds) the fetcher will wait after everything finishes before closing the page and returning the `Response` object. |
| `page_action` | Added for automation. A function that takes the `page` object and does the automation you need. |
| `extra_headers` | A dictionary of extra headers to add to the request. *The referer set by `google_search` takes priority over the referer set here if used together.* |
| `disable_resources` | Drop requests for unnecessary resources for a speed boost. Requests dropped are of type `font`, `image`, `media`, `beacon`, `object`, `imageset`, `texttrack`, `websocket`, `csp_report`, and `stylesheet`. |
| `blocked_domains` | A set of domain names to block requests to. Subdomains are also matched (e.g., `"example.com"` blocks `"sub.example.com"` too). |
| `wait_selector` | Wait for a specific CSS selector to be in a specific state. |
| `wait_selector_state` | The state to wait for the selector given with `wait_selector`. The default state is `attached`. |
| `network_idle` | Wait for the page until there are no network connections for at least 500 ms. |
| `load_dom` | Enabled by default, wait for all JavaScript on page(s) to fully load and execute. |
| `solve_cloudflare` | Solves all types of the Cloudflare's Turnstile/Interstitial challenges before returning the response to you. |
| `selector_config` | The arguments that will be passed in the end while creating the final Selector's class. |
| `proxy` | Static proxy to override rotator and session proxy. A new browser context will be created and used with it. |

| RETURNS | DESCRIPTION |
| --- | --- |
| `Response` | A `Response` object. |

Source code in `scrapling/engines/_browsers/_stealth.py`

|  |  |
| --- | --- |
| ``` 450 451 452 453 454 455 456 457 458 459 460 461 462 463 464 465 466 467 468 469 470 471 472 473 474 475 476 477 478 479 480 481 482 483 484 485 486 487 488 489 490 491 492 493 494 495 496 497 498 499 500 501 502 503 504 505 506 507 508 509 510 511 512 513 514 515 516 517 518 519 520 521 522 523 524 525 526 527 528 529 530 531 532 533 534 535 536 537 538 539 540 541 542 543 544 545 546 547 548 549 550 551 552 553 554 555 556 557 558 559 560 ``` | ``` async def fetch(self, url: str, **kwargs: Unpack[StealthFetchParams]) -> Response:     """Opens up the browser and do your request based on your chosen options.      :param url: The Target url.     :param google_search: Enabled by default, Scrapling will set a Google referer header.     :param timeout: The timeout in milliseconds that is used in all operations and waits through the page. The default is 30,000     :param wait: The time (milliseconds) the fetcher will wait after everything finishes before closing the page and returning the ` Response ` object.     :param page_action: Added for automation. A function that takes the `page` object and does the automation you need.     :param extra_headers: A dictionary of extra headers to add to the request. _The referer set by `google_search` takes priority over the referer set here if used together._     :param disable_resources: Drop requests for unnecessary resources for a speed boost.         Requests dropped are of type `font`, `image`, `media`, `beacon`, `object`, `imageset`, `texttrack`, `websocket`, `csp_report`, and `stylesheet`.     :param blocked_domains: A set of domain names to block requests to. Subdomains are also matched (e.g., ``"example.com"`` blocks ``"sub.example.com"`` too).     :param wait_selector: Wait for a specific CSS selector to be in a specific state.     :param wait_selector_state: The state to wait for the selector given with `wait_selector`. The default state is `attached`.     :param network_idle: Wait for the page until there are no network connections for at least 500 ms.     :param load_dom: Enabled by default, wait for all JavaScript on page(s) to fully load and execute.     :param solve_cloudflare: Solves all types of the Cloudflare's Turnstile/Interstitial challenges before returning the response to you.     :param selector_config: The arguments that will be passed in the end while creating the final Selector's class.     :param proxy: Static proxy to override rotator and session proxy. A new browser context will be created and used with it.     :return: A `Response` object.     """     static_proxy = kwargs.pop("proxy", None)      params = _validate(kwargs, self, StealthConfig)      if not self._is_alive:  # pragma: no cover         raise RuntimeError("Context manager has been closed")      request_headers_keys = {h.lower() for h in params.extra_headers.keys()} if params.extra_headers else set()     referer = (         "https://www.google.com/" if (params.google_search and "referer" not in request_headers_keys) else None     )      for attempt in range(self._config.retries):         proxy: Optional[ProxyType] = None         if self._config.proxy_rotator and static_proxy is None:             proxy = self._config.proxy_rotator.get_proxy()         else:             proxy = static_proxy          async with self._page_generator(             params.timeout, params.extra_headers, params.disable_resources, proxy, params.blocked_domains         ) as page_info:             final_response: List = [None]             xhr_captured: List = []             page = page_info.page             page.on(                 "response",                 self._create_response_handler(                     page_info,                     final_response,                     xhr_pattern=self._config.capture_xhr,                     xhr_container=xhr_captured,                 ),             )              try:                 first_response = await page.goto(url, referer=referer)                 await self._wait_for_page_stability(page, params.load_dom, params.network_idle)                  if not first_response:                     raise RuntimeError(f"Failed to get response for {url}")                  if params.solve_cloudflare:                     await self._cloudflare_solver(page)                     # Make sure the page is fully loaded after the captcha                     await self._wait_for_page_stability(page, params.load_dom, params.network_idle)                  if params.page_action:                     try:                         _ = await params.page_action(page)                     except Exception as e:  # pragma: no cover                         log.error(f"Error executing page_action: {e}")                  if params.wait_selector:                     try:                         waiter: AsyncLocator = page.locator(params.wait_selector)                         await waiter.first.wait_for(state=params.wait_selector_state)                         await self._wait_for_page_stability(page, params.load_dom, params.network_idle)                     except Exception as e:  # pragma: no cover                         log.error(f"Error waiting for selector {params.wait_selector}: {e}")                  await page.wait_for_timeout(params.wait)                  response = await ResponseFactory.from_async_playwright_response(                     page,                     first_response,                     final_response[0],                     params.selector_config,                     meta={"proxy": proxy},                     xhr_captured=xhr_captured,                 )                 return response              except Exception as e:                 page_info.mark_error()                 if attempt < self._config.retries - 1:                     if is_proxy_error(e):                         log.warning(                             f"Proxy '{proxy}' failed (attempt {attempt + 1}) | Retrying in {self._config.retry_delay}s..."                         )                     else:                         log.warning(                             f"Attempt {attempt + 1} failed: {e}. Retrying in {self._config.retry_delay}s..."                         )                     await asyncio_sleep(self._config.retry_delay)                 else:                     log.error(f"Failed after {self._config.retries} attempts: {e}")                     raise      raise RuntimeError("Request failed")  # pragma: no cover ``` |

### Dynamic Sessions[¶](#dynamic-sessions "Permanent link")

## scrapling.fetchers.DynamicSession [¶](#scrapling.fetchers.DynamicSession "Permanent link")

```
DynamicSession(**kwargs)
```

Bases: `SyncSession`, `DynamicSessionMixin`

```
              flowchart TD
              scrapling.fetchers.DynamicSession[DynamicSession]
              scrapling.engines._browsers._base.SyncSession[SyncSession]
              scrapling.engines._browsers._base.DynamicSessionMixin[DynamicSessionMixin]
              scrapling.engines._browsers._base.BaseSessionMixin[BaseSessionMixin]

                              scrapling.engines._browsers._base.SyncSession --> scrapling.fetchers.DynamicSession
                
                scrapling.engines._browsers._base.DynamicSessionMixin --> scrapling.fetchers.DynamicSession
                                scrapling.engines._browsers._base.BaseSessionMixin --> scrapling.engines._browsers._base.DynamicSessionMixin
                



              click scrapling.fetchers.DynamicSession href "" "scrapling.fetchers.DynamicSession"
              click scrapling.engines._browsers._base.SyncSession href "" "scrapling.engines._browsers._base.SyncSession"
              click scrapling.engines._browsers._base.DynamicSessionMixin href "" "scrapling.engines._browsers._base.DynamicSessionMixin"
              click scrapling.engines._browsers._base.BaseSessionMixin href "" "scrapling.engines._browsers._base.BaseSessionMixin"
```

A Browser session manager with page pooling.

A Browser session manager with page pooling, it's using a persistent browser Context by default with a temporary user profile directory.

| PARAMETER | DESCRIPTION |
| --- | --- |
| `headless` | Run the browser in headless/hidden (default), or headful/visible mode. |
| `disable_resources` | Drop requests for unnecessary resources for a speed boost. Requests dropped are of type `font`, `image`, `media`, `beacon`, `object`, `imageset`, `texttrack`, `websocket`, `csp_report`, and `stylesheet`. |
| `blocked_domains` | A set of domain names to block requests to. Subdomains are also matched (e.g., `"example.com"` blocks `"sub.example.com"` too). |
| `useragent` | Pass a useragent string to be used. Otherwise the fetcher will generate a real Useragent of the same browser and use it. |
| `cookies` | Set cookies for the next request. |
| `network_idle` | Wait for the page until there are no network connections for at least 500 ms. |
| `timeout` | The timeout in milliseconds that is used in all operations and waits through the page. The default is 30,000 |
| `wait` | The time (milliseconds) the fetcher will wait after everything finishes before closing the page and returning the `Response` object. |
| `page_action` | Added for automation. A function that takes the `page` object and does the automation you need. |
| `wait_selector` | Wait for a specific CSS selector to be in a specific state. |
| `init_script` | An absolute path to a JavaScript file to be executed on page creation for all pages in this session. |
| `locale` | Specify user locale, for example, `en-GB`, `de-DE`, etc. Locale will affect navigator.language value, Accept-Language request header value as well as number and date formatting rules. Defaults to the system default locale. |
| `timezone_id` | Changes the timezone of the browser. Defaults to the system timezone. |
| `wait_selector_state` | The state to wait for the selector given with `wait_selector`. The default state is `attached`. |
| `real_chrome` | If you have a Chrome browser installed on your device, enable this, and the Fetcher will launch an instance of your browser and use it. |
| `load_dom` | Enabled by default, wait for all JavaScript on page(s) to fully load and execute. |
| `cdp_url` | Instead of launching a new browser instance, connect to this CDP URL to control real browsers through CDP. |
| `google_search` | Enabled by default, Scrapling will set a Google referer header. |
| `extra_headers` | A dictionary of extra headers to add to the request. *The referer set by `google_search` takes priority over the referer set here if used together.* |
| `proxy` | The proxy to be used with requests, it can be a string or a dictionary with the keys 'server', 'username', and 'password' only. |
| `user_data_dir` | Path to a User Data Directory, which stores browser session data like cookies and local storage. The default is to create a temporary directory. |
| `extra_flags` | A list of additional browser flags to pass to the browser on launch. |
| `selector_config` | The arguments that will be passed in the end while creating the final Selector's class. |
| `additional_args` | Additional arguments to be passed to Playwright's context as additional settings, and it takes higher priority than Scrapling's settings. |

Source code in `scrapling/engines/_browsers/_controllers.py`

|  |  |
| --- | --- |
| ``` 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 ``` | ``` def __init__(self, **kwargs: Unpack[PlaywrightSession]):     """A Browser session manager with page pooling, it's using a persistent browser Context by default with a temporary user profile directory.      :param headless: Run the browser in headless/hidden (default), or headful/visible mode.     :param disable_resources: Drop requests for unnecessary resources for a speed boost.         Requests dropped are of type `font`, `image`, `media`, `beacon`, `object`, `imageset`, `texttrack`, `websocket`, `csp_report`, and `stylesheet`.     :param blocked_domains: A set of domain names to block requests to. Subdomains are also matched (e.g., ``"example.com"`` blocks ``"sub.example.com"`` too).     :param useragent: Pass a useragent string to be used. Otherwise the fetcher will generate a real Useragent of the same browser and use it.     :param cookies: Set cookies for the next request.     :param network_idle: Wait for the page until there are no network connections for at least 500 ms.     :param timeout: The timeout in milliseconds that is used in all operations and waits through the page. The default is 30,000     :param wait: The time (milliseconds) the fetcher will wait after everything finishes before closing the page and returning the ` Response ` object.     :param page_action: Added for automation. A function that takes the `page` object and does the automation you need.     :param wait_selector: Wait for a specific CSS selector to be in a specific state.     :param init_script: An absolute path to a JavaScript file to be executed on page creation for all pages in this session.     :param locale: Specify user locale, for example, `en-GB`, `de-DE`, etc. Locale will affect navigator.language value, Accept-Language request header value as well as number and date formatting         rules. Defaults to the system default locale.     :param timezone_id: Changes the timezone of the browser. Defaults to the system timezone.     :param wait_selector_state: The state to wait for the selector given with `wait_selector`. The default state is `attached`.     :param real_chrome: If you have a Chrome browser installed on your device, enable this, and the Fetcher will launch an instance of your browser and use it.     :param load_dom: Enabled by default, wait for all JavaScript on page(s) to fully load and execute.     :param cdp_url: Instead of launching a new browser instance, connect to this CDP URL to control real browsers through CDP.     :param google_search: Enabled by default, Scrapling will set a Google referer header.     :param extra_headers: A dictionary of extra headers to add to the request. _The referer set by `google_search` takes priority over the referer set here if used together._     :param proxy: The proxy to be used with requests, it can be a string or a dictionary with the keys 'server', 'username', and 'password' only.     :param user_data_dir: Path to a User Data Directory, which stores browser session data like cookies and local storage. The default is to create a temporary directory.     :param extra_flags: A list of additional browser flags to pass to the browser on launch.     :param selector_config: The arguments that will be passed in the end while creating the final Selector's class.     :param additional_args: Additional arguments to be passed to Playwright's context as additional settings, and it takes higher priority than Scrapling's settings.     """     self.__validate__(**kwargs)     super().__init__() ``` |

### max_pages `instance-attribute` [¶](#scrapling.fetchers.DynamicSession.max_pages "Permanent link")

```
max_pages = max_pages
```

### page_pool `instance-attribute` [¶](#scrapling.fetchers.DynamicSession.page_pool "Permanent link")

```
page_pool = PagePool(max_pages)
```

### playwright `instance-attribute` [¶](#scrapling.fetchers.DynamicSession.playwright "Permanent link")

```
playwright = None
```

### context `instance-attribute` [¶](#scrapling.fetchers.DynamicSession.context "Permanent link")

```
context = None
```

### browser `instance-attribute` [¶](#scrapling.fetchers.DynamicSession.browser "Permanent link")

```
browser = None
```

### __slots__ `class-attribute` `instance-attribute` [¶](#scrapling.fetchers.DynamicSession.__slots__ "Permanent link")

```
__slots__ = (
    "_config",
    "_context_options",
    "_browser_options",
    "_user_data_dir",
    "_headers_keys",
    "max_pages",
    "page_pool",
    "_max_wait_for_page",
    "playwright",
    "context",
)
```

### __validate_routine__ [¶](#scrapling.fetchers.DynamicSession.__validate_routine__ "Permanent link")

```
__validate_routine__(params, model)
```

Source code in `scrapling/engines/_browsers/_base.py`

|  |  |
| --- | --- |
| ``` 412 413 414 415 416 417 418 419 420 421 422 423 424 425 426 427 428 429 ``` | ``` def __validate_routine__(     self, params: Dict, model: type[PlaywrightConfig] | type[StealthConfig] ) -> PlaywrightConfig | StealthConfig:     # Dark color scheme bypasses the 'prefersLightColor' check in creepjs     self._context_options: Dict[str, Any] = {"color_scheme": "dark", "device_scale_factor": 2}     self._browser_options: Dict[str, Any] = {         "args": DEFAULT_ARGS,         "ignore_default_args": HARMFUL_ARGS,     }     if "__max_pages" in params:         params["max_pages"] = params.pop("__max_pages")      config = validate(params, model=model)     self._headers_keys = (         {header.lower() for header in config.extra_headers.keys()} if config.extra_headers else set()     )      return config ``` |

### __generate_options__ [¶](#scrapling.fetchers.DynamicSession.__generate_options__ "Permanent link")

```
__generate_options__(extra_flags=None)
```

Source code in `scrapling/engines/_browsers/_base.py`

|  |  |
| --- | --- |
| ``` 431 432 433 434 435 436 437 438 439 440 441 442 443 444 445 446 447 448 449 450 451 452 453 454 455 456 457 458 459 460 461 462 463 464 465 466 467 468 469 ``` | ``` def __generate_options__(self, extra_flags: Tuple | None = None) -> None:     config: PlaywrightConfig | StealthConfig = self._config     self._context_options.update(         {             "proxy": config.proxy,             "locale": config.locale,             "timezone_id": config.timezone_id,             "extra_http_headers": config.extra_headers,         }     )     # The default useragent in the headful is always correct now in the current versions of Playwright     if config.useragent:         self._context_options["user_agent"] = config.useragent     elif not config.useragent and config.headless:         self._context_options["user_agent"] = (             __default_chrome_useragent__ if config.real_chrome else __default_useragent__         )      if not config.cdp_url:         flags = self._browser_options["args"]         if config.extra_flags or extra_flags:             flags = list(set(tuple(flags) + tuple(config.extra_flags or extra_flags or ())))          self._browser_options.update(             {                 "args": flags,                 "headless": config.headless,                 "channel": "chrome" if config.real_chrome else "chromium",             }         )         if config.executable_path:             self._browser_options["executable_path"] = config.executable_path          self._user_data_dir = config.user_data_dir     else:         self._browser_options = {}      if config.additional_args:         self._context_options.update(config.additional_args) ``` |

### __validate__ [¶](#scrapling.fetchers.DynamicSession.__validate__ "Permanent link")

```
__validate__(**params)
```

Source code in `scrapling/engines/_browsers/_base.py`

|  |  |
| --- | --- |
| ``` 489 490 491 ``` | ``` def __validate__(self, **params):     self._config = self.__validate_routine__(params, model=PlaywrightConfig)     self.__generate_options__() ``` |

### close [¶](#scrapling.fetchers.DynamicSession.close "Permanent link")

```
close()
```

Close all resources

Source code in `scrapling/engines/_browsers/_base.py`

|  |  |
| --- | --- |
| ``` 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 ``` | ``` def close(self):  # pragma: no cover     """Close all resources"""     if not self._is_alive:         return      if self.context:         self.context.close()         self.context = None      if self.browser:         self.browser.close()         self.browser = None      if self.playwright:         self.playwright.stop()         self.playwright = None  # pyright: ignore      self._is_alive = False ``` |

### __enter__ [¶](#scrapling.fetchers.DynamicSession.__enter__ "Permanent link")

```
__enter__()
```

Source code in `scrapling/engines/_browsers/_base.py`

|  |  |
| --- | --- |
| ``` 86 87 88 ``` | ``` def __enter__(self):     self.start()     return self ``` |

### __exit__ [¶](#scrapling.fetchers.DynamicSession.__exit__ "Permanent link")

```
__exit__(exc_type, exc_val, exc_tb)
```

Source code in `scrapling/engines/_browsers/_base.py`

|  |  |
| --- | --- |
| ``` 90 91 ``` | ``` def __exit__(self, exc_type, exc_val, exc_tb):     self.close() ``` |

### get_pool_stats [¶](#scrapling.fetchers.DynamicSession.get_pool_stats "Permanent link")

```
get_pool_stats()
```

Get statistics about the current page pool

Source code in `scrapling/engines/_browsers/_base.py`

|  |  |
| --- | --- |
| ``` 127 128 129 130 131 132 133 ``` | ``` def get_pool_stats(self) -> Dict[str, int]:     """Get statistics about the current page pool"""     return {         "total_pages": self.page_pool.pages_count,         "busy_pages": self.page_pool.busy_count,         "max_pages": self.max_pages,     } ``` |

### start [¶](#scrapling.fetchers.DynamicSession.start "Permanent link")

```
start()
```

Create a browser for this instance and context.

Source code in `scrapling/engines/_browsers/_controllers.py`

|  |  |
| --- | --- |
| ``` 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 ``` | ``` def start(self):     """Create a browser for this instance and context."""     if not self.playwright:         self.playwright = sync_playwright().start()          try:             if self._config.cdp_url:  # pragma: no cover                 self.browser = self.playwright.chromium.connect_over_cdp(endpoint_url=self._config.cdp_url)                 if not self._config.proxy_rotator and self.browser:                     self.context = self.browser.new_context(**self._context_options)             elif self._config.proxy_rotator:                 self.browser = self.playwright.chromium.launch(**self._browser_options)             else:                 persistent_options = (                     self._browser_options | self._context_options | {"user_data_dir": self._user_data_dir}                 )                 self.context = self.playwright.chromium.launch_persistent_context(**persistent_options)              if self.context:                 self.context = self._initialize_context(self._config, self.context)              self._is_alive = True         except Exception:             # Clean up playwright if browser setup fails             self.playwright.stop()             self.playwright = None             raise     else:         raise RuntimeError("Session has been already started") ``` |

### fetch [¶](#scrapling.fetchers.DynamicSession.fetch "Permanent link")

```
fetch(url, **kwargs)
```

Opens up the browser and do your request based on your chosen options.

| PARAMETER | DESCRIPTION |
| --- | --- |
| `url` | The Target url.  **TYPE:** `str` |
| `google_search` | Enabled by default, Scrapling will set a Google referer header. |
| `timeout` | The timeout in milliseconds that is used in all operations and waits through the page. The default is 30,000 |
| `wait` | The time (milliseconds) the fetcher will wait after everything finishes before closing the page and returning the `Response` object. |
| `page_action` | Added for automation. A function that takes the `page` object and does the automation you need. |
| `extra_headers` | A dictionary of extra headers to add to the request. *The referer set by `google_search` takes priority over the referer set here if used together.* |
| `disable_resources` | Drop requests for unnecessary resources for a speed boost. Requests dropped are of type `font`, `image`, `media`, `beacon`, `object`, `imageset`, `texttrack`, `websocket`, `csp_report`, and `stylesheet`. |
| `blocked_domains` | A set of domain names to block requests to. Subdomains are also matched (e.g., `"example.com"` blocks `"sub.example.com"` too). |
| `wait_selector` | Wait for a specific CSS selector to be in a specific state. |
| `wait_selector_state` | The state to wait for the selector given with `wait_selector`. The default state is `attached`. |
| `network_idle` | Wait for the page until there are no network connections for at least 500 ms. |
| `load_dom` | Enabled by default, wait for all JavaScript on page(s) to fully load and execute. |
| `selector_config` | The arguments that will be passed in the end while creating the final Selector's class. |
| `proxy` | Static proxy to override rotator and session proxy. A new browser context will be created and used with it. |

| RETURNS | DESCRIPTION |
| --- | --- |
| `Response` | A `Response` object. |

Source code in `scrapling/engines/_browsers/_controllers.py`

|  |  |
| --- | --- |
| ``` 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200 201 202 203 204 ``` | ``` def fetch(self, url: str, **kwargs: Unpack[PlaywrightFetchParams]) -> Response:     """Opens up the browser and do your request based on your chosen options.      :param url: The Target url.     :param google_search: Enabled by default, Scrapling will set a Google referer header.     :param timeout: The timeout in milliseconds that is used in all operations and waits through the page. The default is 30,000     :param wait: The time (milliseconds) the fetcher will wait after everything finishes before closing the page and returning the ` Response ` object.     :param page_action: Added for automation. A function that takes the `page` object and does the automation you need.     :param extra_headers: A dictionary of extra headers to add to the request. _The referer set by `google_search` takes priority over the referer set here if used together._     :param disable_resources: Drop requests for unnecessary resources for a speed boost.         Requests dropped are of type `font`, `image`, `media`, `beacon`, `object`, `imageset`, `texttrack`, `websocket`, `csp_report`, and `stylesheet`.     :param blocked_domains: A set of domain names to block requests to. Subdomains are also matched (e.g., ``"example.com"`` blocks ``"sub.example.com"`` too).     :param wait_selector: Wait for a specific CSS selector to be in a specific state.     :param wait_selector_state: The state to wait for the selector given with `wait_selector`. The default state is `attached`.     :param network_idle: Wait for the page until there are no network connections for at least 500 ms.     :param load_dom: Enabled by default, wait for all JavaScript on page(s) to fully load and execute.     :param selector_config: The arguments that will be passed in the end while creating the final Selector's class.     :param proxy: Static proxy to override rotator and session proxy. A new browser context will be created and used with it.     :return: A `Response` object.     """     static_proxy = kwargs.pop("proxy", None)      params = _validate(kwargs, self, PlaywrightConfig)     if not self._is_alive:  # pragma: no cover         raise RuntimeError("Context manager has been closed")      request_headers_keys = {h.lower() for h in params.extra_headers.keys()} if params.extra_headers else set()     referer = (         "https://www.google.com/" if (params.google_search and "referer" not in request_headers_keys) else None     )      for attempt in range(self._config.retries):         proxy: Optional[ProxyType] = None         if self._config.proxy_rotator and static_proxy is None:             proxy = self._config.proxy_rotator.get_proxy()         else:             proxy = static_proxy          with self._page_generator(             params.timeout, params.extra_headers, params.disable_resources, proxy, params.blocked_domains         ) as page_info:             final_response: List = [None]             xhr_captured: List = []             page = page_info.page             page.on(                 "response",                 self._create_response_handler(                     page_info,                     final_response,                     xhr_pattern=self._config.capture_xhr,                     xhr_container=xhr_captured,                 ),             )              try:                 first_response = page.goto(url, referer=referer)                 self._wait_for_page_stability(page, params.load_dom, params.network_idle)                  if not first_response:                     raise RuntimeError(f"Failed to get response for {url}")                  if params.page_action:                     try:                         _ = params.page_action(page)                     except Exception as e:  # pragma: no cover                         log.error(f"Error executing page_action: {e}")                  if params.wait_selector:                     try:                         waiter: Locator = page.locator(params.wait_selector)                         waiter.first.wait_for(state=params.wait_selector_state)                         self._wait_for_page_stability(page, params.load_dom, params.network_idle)                     except Exception as e:  # pragma: no cover                         log.error(f"Error waiting for selector {params.wait_selector}: {e}")                  page.wait_for_timeout(params.wait)                  response = ResponseFactory.from_playwright_response(                     page,                     first_response,                     final_response[0],                     params.selector_config,                     meta={"proxy": proxy},                     xhr_captured=xhr_captured,                 )                 return response              except Exception as e:                 page_info.mark_error()                 if attempt < self._config.retries - 1:                     if is_proxy_error(e):                         log.warning(                             f"Proxy '{proxy}' failed (attempt {attempt + 1}) | Retrying in {self._config.retry_delay}s..."                         )                     else:                         log.warning(                             f"Attempt {attempt + 1} failed: {e}. Retrying in {self._config.retry_delay}s..."                         )                     time_sleep(self._config.retry_delay)                 else:                     log.error(f"Failed after {self._config.retries} attempts: {e}")                     raise      raise RuntimeError("Request failed")  # pragma: no cover ``` |

## scrapling.fetchers.AsyncDynamicSession [¶](#scrapling.fetchers.AsyncDynamicSession "Permanent link")

```
AsyncDynamicSession(**kwargs)
```

Bases: `AsyncSession`, `DynamicSessionMixin`

```
              flowchart TD
              scrapling.fetchers.AsyncDynamicSession[AsyncDynamicSession]
              scrapling.engines._browsers._base.AsyncSession[AsyncSession]
              scrapling.engines._browsers._base.DynamicSessionMixin[DynamicSessionMixin]
              scrapling.engines._browsers._base.BaseSessionMixin[BaseSessionMixin]

                              scrapling.engines._browsers._base.AsyncSession --> scrapling.fetchers.AsyncDynamicSession
                
                scrapling.engines._browsers._base.DynamicSessionMixin --> scrapling.fetchers.AsyncDynamicSession
                                scrapling.engines._browsers._base.BaseSessionMixin --> scrapling.engines._browsers._base.DynamicSessionMixin
                



              click scrapling.fetchers.AsyncDynamicSession href "" "scrapling.fetchers.AsyncDynamicSession"
              click scrapling.engines._browsers._base.AsyncSession href "" "scrapling.engines._browsers._base.AsyncSession"
              click scrapling.engines._browsers._base.DynamicSessionMixin href "" "scrapling.engines._browsers._base.DynamicSessionMixin"
              click scrapling.engines._browsers._base.BaseSessionMixin href "" "scrapling.engines._browsers._base.BaseSessionMixin"
```

An async Browser session manager with page pooling, it's using a persistent browser Context by default with a temporary user profile directory.

A Browser session manager with page pooling

| PARAMETER | DESCRIPTION |
| --- | --- |
| `headless` | Run the browser in headless/hidden (default), or headful/visible mode. |
| `disable_resources` | Drop requests for unnecessary resources for a speed boost. Requests dropped are of type `font`, `image`, `media`, `beacon`, `object`, `imageset`, `texttrack`, `websocket`, `csp_report`, and `stylesheet`. |
| `blocked_domains` | A set of domain names to block requests to. Subdomains are also matched (e.g., `"example.com"` blocks `"sub.example.com"` too). |
| `useragent` | Pass a useragent string to be used. Otherwise the fetcher will generate a real Useragent of the same browser and use it. |
| `cookies` | Set cookies for the next request. |
| `network_idle` | Wait for the page until there are no network connections for at least 500 ms. |
| `load_dom` | Enabled by default, wait for all JavaScript on page(s) to fully load and execute. |
| `timeout` | The timeout in milliseconds that is used in all operations and waits through the page. The default is 30,000 |
| `wait` | The time (milliseconds) the fetcher will wait after everything finishes before closing the page and returning the `Response` object. |
| `page_action` | Added for automation. A function that takes the `page` object and does the automation you need. |
| `wait_selector` | Wait for a specific CSS selector to be in a specific state. |
| `init_script` | An absolute path to a JavaScript file to be executed on page creation for all pages in this session. |
| `locale` | Specify user locale, for example, `en-GB`, `de-DE`, etc. Locale will affect navigator.language value, Accept-Language request header value as well as number and date formatting rules. Defaults to the system default locale. |
| `timezone_id` | Changes the timezone of the browser. Defaults to the system timezone. |
| `wait_selector_state` | The state to wait for the selector given with `wait_selector`. The default state is `attached`. |
| `real_chrome` | If you have a Chrome browser installed on your device, enable this, and the Fetcher will launch an instance of your browser and use it. |
| `cdp_url` | Instead of launching a new browser instance, connect to this CDP URL to control real browsers through CDP. |
| `google_search` | Enabled by default, Scrapling will set a Google referer header. |
| `extra_headers` | A dictionary of extra headers to add to the request. *The referer set by `google_search` takes priority over the referer set here if used together.* |
| `proxy` | The proxy to be used with requests, it can be a string or a dictionary with the keys 'server', 'username', and 'password' only. |
| `max_pages` | The maximum number of tabs to be opened at the same time. It will be used in rotation through a PagePool. |
| `user_data_dir` | Path to a User Data Directory, which stores browser session data like cookies and local storage. The default is to create a temporary directory. |
| `extra_flags` | A list of additional browser flags to pass to the browser on launch. |
| `selector_config` | The arguments that will be passed in the end while creating the final Selector's class. |
| `additional_args` | Additional arguments to be passed to Playwright's context as additional settings, and it takes higher priority than Scrapling's settings. |

Source code in `scrapling/engines/_browsers/_controllers.py`

|  |  |
| --- | --- |
| ``` 218 219 220 221 222 223 224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239 240 241 242 243 244 245 246 247 248 249 250 ``` | ``` def __init__(self, **kwargs: Unpack[PlaywrightSession]):     """A Browser session manager with page pooling      :param headless: Run the browser in headless/hidden (default), or headful/visible mode.     :param disable_resources: Drop requests for unnecessary resources for a speed boost.         Requests dropped are of type `font`, `image`, `media`, `beacon`, `object`, `imageset`, `texttrack`, `websocket`, `csp_report`, and `stylesheet`.     :param blocked_domains: A set of domain names to block requests to. Subdomains are also matched (e.g., ``"example.com"`` blocks ``"sub.example.com"`` too).     :param useragent: Pass a useragent string to be used. Otherwise the fetcher will generate a real Useragent of the same browser and use it.     :param cookies: Set cookies for the next request.     :param network_idle: Wait for the page until there are no network connections for at least 500 ms.     :param load_dom: Enabled by default, wait for all JavaScript on page(s) to fully load and execute.     :param timeout: The timeout in milliseconds that is used in all operations and waits through the page. The default is 30,000     :param wait: The time (milliseconds) the fetcher will wait after everything finishes before closing the page and returning the ` Response ` object.     :param page_action: Added for automation. A function that takes the `page` object and does the automation you need.     :param wait_selector: Wait for a specific CSS selector to be in a specific state.     :param init_script: An absolute path to a JavaScript file to be executed on page creation for all pages in this session.     :param locale: Specify user locale, for example, `en-GB`, `de-DE`, etc. Locale will affect navigator.language value, Accept-Language request header value as well as number and date formatting         rules. Defaults to the system default locale.     :param timezone_id: Changes the timezone of the browser. Defaults to the system timezone.     :param wait_selector_state: The state to wait for the selector given with `wait_selector`. The default state is `attached`.     :param real_chrome: If you have a Chrome browser installed on your device, enable this, and the Fetcher will launch an instance of your browser and use it.     :param cdp_url: Instead of launching a new browser instance, connect to this CDP URL to control real browsers through CDP.     :param google_search: Enabled by default, Scrapling will set a Google referer header.     :param extra_headers: A dictionary of extra headers to add to the request. _The referer set by `google_search` takes priority over the referer set here if used together._     :param proxy: The proxy to be used with requests, it can be a string or a dictionary with the keys 'server', 'username', and 'password' only.     :param max_pages: The maximum number of tabs to be opened at the same time. It will be used in rotation through a PagePool.     :param user_data_dir: Path to a User Data Directory, which stores browser session data like cookies and local storage. The default is to create a temporary directory.     :param extra_flags: A list of additional browser flags to pass to the browser on launch.     :param selector_config: The arguments that will be passed in the end while creating the final Selector's class.     :param additional_args: Additional arguments to be passed to Playwright's context as additional settings, and it takes higher priority than Scrapling's settings.     """     self.__validate__(**kwargs)     super().__init__(max_pages=self._config.max_pages) ``` |

### max_pages `instance-attribute` [¶](#scrapling.fetchers.AsyncDynamicSession.max_pages "Permanent link")

```
max_pages = max_pages
```

### page_pool `instance-attribute` [¶](#scrapling.fetchers.AsyncDynamicSession.page_pool "Permanent link")

```
page_pool = PagePool(max_pages)
```

### playwright `instance-attribute` [¶](#scrapling.fetchers.AsyncDynamicSession.playwright "Permanent link")

```
playwright = None
```

### context `instance-attribute` [¶](#scrapling.fetchers.AsyncDynamicSession.context "Permanent link")

```
context = None
```

### browser `instance-attribute` [¶](#scrapling.fetchers.AsyncDynamicSession.browser "Permanent link")

```
browser = None
```

### __slots__ `class-attribute` `instance-attribute` [¶](#scrapling.fetchers.AsyncDynamicSession.__slots__ "Permanent link")

```
__slots__ = (
    "_config",
    "_context_options",
    "_browser_options",
    "_user_data_dir",
    "_headers_keys",
)
```

### __validate_routine__ [¶](#scrapling.fetchers.AsyncDynamicSession.__validate_routine__ "Permanent link")

```
__validate_routine__(params, model)
```

Source code in `scrapling/engines/_browsers/_base.py`

|  |  |
| --- | --- |
| ``` 412 413 414 415 416 417 418 419 420 421 422 423 424 425 426 427 428 429 ``` | ``` def __validate_routine__(     self, params: Dict, model: type[PlaywrightConfig] | type[StealthConfig] ) -> PlaywrightConfig | StealthConfig:     # Dark color scheme bypasses the 'prefersLightColor' check in creepjs     self._context_options: Dict[str, Any] = {"color_scheme": "dark", "device_scale_factor": 2}     self._browser_options: Dict[str, Any] = {         "args": DEFAULT_ARGS,         "ignore_default_args": HARMFUL_ARGS,     }     if "__max_pages" in params:         params["max_pages"] = params.pop("__max_pages")      config = validate(params, model=model)     self._headers_keys = (         {header.lower() for header in config.extra_headers.keys()} if config.extra_headers else set()     )      return config ``` |

### __generate_options__ [¶](#scrapling.fetchers.AsyncDynamicSession.__generate_options__ "Permanent link")

```
__generate_options__(extra_flags=None)
```

Source code in `scrapling/engines/_browsers/_base.py`

|  |  |
| --- | --- |
| ``` 431 432 433 434 435 436 437 438 439 440 441 442 443 444 445 446 447 448 449 450 451 452 453 454 455 456 457 458 459 460 461 462 463 464 465 466 467 468 469 ``` | ``` def __generate_options__(self, extra_flags: Tuple | None = None) -> None:     config: PlaywrightConfig | StealthConfig = self._config     self._context_options.update(         {             "proxy": config.proxy,             "locale": config.locale,             "timezone_id": config.timezone_id,             "extra_http_headers": config.extra_headers,         }     )     # The default useragent in the headful is always correct now in the current versions of Playwright     if config.useragent:         self._context_options["user_agent"] = config.useragent     elif not config.useragent and config.headless:         self._context_options["user_agent"] = (             __default_chrome_useragent__ if config.real_chrome else __default_useragent__         )      if not config.cdp_url:         flags = self._browser_options["args"]         if config.extra_flags or extra_flags:             flags = list(set(tuple(flags) + tuple(config.extra_flags or extra_flags or ())))          self._browser_options.update(             {                 "args": flags,                 "headless": config.headless,                 "channel": "chrome" if config.real_chrome else "chromium",             }         )         if config.executable_path:             self._browser_options["executable_path"] = config.executable_path          self._user_data_dir = config.user_data_dir     else:         self._browser_options = {}      if config.additional_args:         self._context_options.update(config.additional_args) ``` |

### __validate__ [¶](#scrapling.fetchers.AsyncDynamicSession.__validate__ "Permanent link")

```
__validate__(**params)
```

Source code in `scrapling/engines/_browsers/_base.py`

|  |  |
| --- | --- |
| ``` 489 490 491 ``` | ``` def __validate__(self, **params):     self._config = self.__validate_routine__(params, model=PlaywrightConfig)     self.__generate_options__() ``` |

### close `async` [¶](#scrapling.fetchers.AsyncDynamicSession.close "Permanent link")

```
close()
```

Close all resources

Source code in `scrapling/engines/_browsers/_base.py`

|  |  |
| --- | --- |
| ``` 236 237 238 239 240 241 242 243 244 245 246 247 248 249 250 251 252 253 ``` | ``` async def close(self):     """Close all resources"""     if not self._is_alive:  # pragma: no cover         return      if self.context:         await self.context.close()         self.context = None  # pyright: ignore      if self.browser:         await self.browser.close()         self.browser = None      if self.playwright:         await self.playwright.stop()         self.playwright = None  # pyright: ignore      self._is_alive = False ``` |

### __aenter__ `async` [¶](#scrapling.fetchers.AsyncDynamicSession.__aenter__ "Permanent link")

```
__aenter__()
```

Source code in `scrapling/engines/_browsers/_base.py`

|  |  |
| --- | --- |
| ``` 255 256 257 ``` | ``` async def __aenter__(self):     await self.start()     return self ``` |

### __aexit__ `async` [¶](#scrapling.fetchers.AsyncDynamicSession.__aexit__ "Permanent link")

```
__aexit__(exc_type, exc_val, exc_tb)
```

Source code in `scrapling/engines/_browsers/_base.py`

|  |  |
| --- | --- |
| ``` 259 260 ``` | ``` async def __aexit__(self, exc_type, exc_val, exc_tb):     await self.close() ``` |

### get_pool_stats [¶](#scrapling.fetchers.AsyncDynamicSession.get_pool_stats "Permanent link")

```
get_pool_stats()
```

Get statistics about the current page pool

Source code in `scrapling/engines/_browsers/_base.py`

|  |  |
| --- | --- |
| ``` 312 313 314 315 316 317 318 ``` | ``` def get_pool_stats(self) -> Dict[str, int]:     """Get statistics about the current page pool"""     return {         "total_pages": self.page_pool.pages_count,         "busy_pages": self.page_pool.busy_count,         "max_pages": self.max_pages,     } ``` |

### start `async` [¶](#scrapling.fetchers.AsyncDynamicSession.start "Permanent link")

```
start()
```

Create a browser for this instance and context.

Source code in `scrapling/engines/_browsers/_controllers.py`

|  |  |
| --- | --- |
| ``` 252 253 254 255 256 257 258 259 260 261 262 263 264 265 266 267 268 269 270 271 272 273 274 275 276 277 278 279 ``` | ``` async def start(self) -> None:     """Create a browser for this instance and context."""     if not self.playwright:         self.playwright = await async_playwright().start()         try:             if self._config.cdp_url:                 self.browser = await self.playwright.chromium.connect_over_cdp(endpoint_url=self._config.cdp_url)                 if not self._config.proxy_rotator and self.browser:                     self.context = await self.browser.new_context(**self._context_options)             elif self._config.proxy_rotator:                 self.browser = await self.playwright.chromium.launch(**self._browser_options)             else:                 persistent_options = (                     self._browser_options | self._context_options | {"user_data_dir": self._user_data_dir}                 )                 self.context = await self.playwright.chromium.launch_persistent_context(**persistent_options)              if self.context:                 self.context = await self._initialize_context(self._config, self.context)              self._is_alive = True         except Exception:             # Clean up playwright if browser setup fails             await self.playwright.stop()             self.playwright = None             raise     else:         raise RuntimeError("Session has been already started") ``` |

### fetch `async` [¶](#scrapling.fetchers.AsyncDynamicSession.fetch "Permanent link")

```
fetch(url, **kwargs)
```

Opens up the browser and do your request based on your chosen options.

| PARAMETER | DESCRIPTION |
| --- | --- |
| `url` | The Target url.  **TYPE:** `str` |
| `google_search` | Enabled by default, Scrapling will set a Google referer header. |
| `timeout` | The timeout in milliseconds that is used in all operations and waits through the page. The default is 30,000 |
| `wait` | The time (milliseconds) the fetcher will wait after everything finishes before closing the page and returning the `Response` object. |
| `page_action` | Added for automation. A function that takes the `page` object and does the automation you need. |
| `extra_headers` | A dictionary of extra headers to add to the request. *The referer set by `google_search` takes priority over the referer set here if used together.* |
| `disable_resources` | Drop requests for unnecessary resources for a speed boost. Requests dropped are of type `font`, `image`, `media`, `beacon`, `object`, `imageset`, `texttrack`, `websocket`, `csp_report`, and `stylesheet`. |
| `blocked_domains` | A set of domain names to block requests to. Subdomains are also matched (e.g., `"example.com"` blocks `"sub.example.com"` too). |
| `wait_selector` | Wait for a specific CSS selector to be in a specific state. |
| `wait_selector_state` | The state to wait for the selector given with `wait_selector`. The default state is `attached`. |
| `network_idle` | Wait for the page until there are no network connections for at least 500 ms. |
| `load_dom` | Enabled by default, wait for all JavaScript on page(s) to fully load and execute. |
| `selector_config` | The arguments that will be passed in the end while creating the final Selector's class. |
| `proxy` | Static proxy to override rotator and session proxy. A new browser context will be created and used with it. |

| RETURNS | DESCRIPTION |
| --- | --- |
| `Response` | A `Response` object. |

Source code in `scrapling/engines/_browsers/_controllers.py`

|  |  |
| --- | --- |
| ``` 281 282 283 284 285 286 287 288 289 290 291 292 293 294 295 296 297 298 299 300 301 302 303 304 305 306 307 308 309 310 311 312 313 314 315 316 317 318 319 320 321 322 323 324 325 326 327 328 329 330 331 332 333 334 335 336 337 338 339 340 341 342 343 344 345 346 347 348 349 350 351 352 353 354 355 356 357 358 359 360 361 362 363 364 365 366 367 368 369 370 371 372 373 374 375 376 377 378 379 380 381 382 383 384 385 ``` | ``` async def fetch(self, url: str, **kwargs: Unpack[PlaywrightFetchParams]) -> Response:     """Opens up the browser and do your request based on your chosen options.      :param url: The Target url.     :param google_search: Enabled by default, Scrapling will set a Google referer header.     :param timeout: The timeout in milliseconds that is used in all operations and waits through the page. The default is 30,000     :param wait: The time (milliseconds) the fetcher will wait after everything finishes before closing the page and returning the ` Response ` object.     :param page_action: Added for automation. A function that takes the `page` object and does the automation you need.     :param extra_headers: A dictionary of extra headers to add to the request. _The referer set by `google_search` takes priority over the referer set here if used together._     :param disable_resources: Drop requests for unnecessary resources for a speed boost.         Requests dropped are of type `font`, `image`, `media`, `beacon`, `object`, `imageset`, `texttrack`, `websocket`, `csp_report`, and `stylesheet`.     :param blocked_domains: A set of domain names to block requests to. Subdomains are also matched (e.g., ``"example.com"`` blocks ``"sub.example.com"`` too).     :param wait_selector: Wait for a specific CSS selector to be in a specific state.     :param wait_selector_state: The state to wait for the selector given with `wait_selector`. The default state is `attached`.     :param network_idle: Wait for the page until there are no network connections for at least 500 ms.     :param load_dom: Enabled by default, wait for all JavaScript on page(s) to fully load and execute.     :param selector_config: The arguments that will be passed in the end while creating the final Selector's class.     :param proxy: Static proxy to override rotator and session proxy. A new browser context will be created and used with it.     :return: A `Response` object.     """     static_proxy = kwargs.pop("proxy", None)      params = _validate(kwargs, self, PlaywrightConfig)      if not self._is_alive:  # pragma: no cover         raise RuntimeError("Context manager has been closed")      request_headers_keys = {h.lower() for h in params.extra_headers.keys()} if params.extra_headers else set()     referer = (         "https://www.google.com/" if (params.google_search and "referer" not in request_headers_keys) else None     )      for attempt in range(self._config.retries):         proxy: Optional[ProxyType] = None         if self._config.proxy_rotator and static_proxy is None:             proxy = self._config.proxy_rotator.get_proxy()         else:             proxy = static_proxy          async with self._page_generator(             params.timeout, params.extra_headers, params.disable_resources, proxy, params.blocked_domains         ) as page_info:             final_response: List = [None]             xhr_captured: List = []             page = page_info.page             page.on(                 "response",                 self._create_response_handler(                     page_info,                     final_response,                     xhr_pattern=self._config.capture_xhr,                     xhr_container=xhr_captured,                 ),             )              try:                 first_response = await page.goto(url, referer=referer)                 await self._wait_for_page_stability(page, params.load_dom, params.network_idle)                  if not first_response:                     raise RuntimeError(f"Failed to get response for {url}")                  if params.page_action:                     try:                         _ = await params.page_action(page)                     except Exception as e:  # pragma: no cover                         log.error(f"Error executing page_action: {e}")                  if params.wait_selector:                     try:                         waiter: AsyncLocator = page.locator(params.wait_selector)                         await waiter.first.wait_for(state=params.wait_selector_state)                         await self._wait_for_page_stability(page, params.load_dom, params.network_idle)                     except Exception as e:  # pragma: no cover                         log.error(f"Error waiting for selector {params.wait_selector}: {e}")                  await page.wait_for_timeout(params.wait)                  response = await ResponseFactory.from_async_playwright_response(                     page,                     first_response,                     final_response[0],                     params.selector_config,                     meta={"proxy": proxy},                     xhr_captured=xhr_captured,                 )                 return response              except Exception as e:                 page_info.mark_error()                 if attempt < self._config.retries - 1:                     if is_proxy_error(e):                         log.warning(                             f"Proxy '{proxy}' failed (attempt {attempt + 1}) | Retrying in {self._config.retry_delay}s..."                         )                     else:                         log.warning(                             f"Attempt {attempt + 1} failed: {e}. Retrying in {self._config.retry_delay}s..."                         )                     await asyncio_sleep(self._config.retry_delay)                 else:                     log.error(f"Failed after {self._config.retries} attempts: {e}")                     raise      raise RuntimeError("Request failed")  # pragma: no cover ``` |

Was this page helpful?

Thanks for your feedback!

Thanks for your feedback! Help us improve this page by
[opening a documentation issue](https://github.com/D4Vinci/Scrapling/issues/new?template=04-docs_issue.yml).


---
## Source: https://scrapling.readthedocs.io/en/latest/api-reference/mcp-server.html
---

# MCP Server API Reference[¶](#mcp-server-api-reference "Permanent link")

The **Scrapling MCP Server** provides nine powerful tools for web scraping through the Model Context Protocol (MCP). This server integrates Scrapling's capabilities directly into AI chatbots and agents, allowing conversational web scraping with advanced anti-bot bypass features.

You can start the MCP server by running:

```
scrapling mcp
```

Or import the server class directly:

```
from scrapling.core.ai import ScraplingMCPServer

server = ScraplingMCPServer()
server.serve(http=False, host="0.0.0.0", port=8000)
```

## Response Model[¶](#response-model "Permanent link")

The standardized response structure that's returned by all MCP server tools:

## scrapling.core.ai.ResponseModel [¶](#scrapling.core.ai.ResponseModel "Permanent link")

Bases: `BaseModel`

```
              flowchart TD
              scrapling.core.ai.ResponseModel[ResponseModel]

              

              click scrapling.core.ai.ResponseModel href "" "scrapling.core.ai.ResponseModel"
```

Request's response information structure.

### status `class-attribute` `instance-attribute` [¶](#scrapling.core.ai.ResponseModel.status "Permanent link")

```
status = Field(
    description="The status code returned by the website."
)
```

### content `class-attribute` `instance-attribute` [¶](#scrapling.core.ai.ResponseModel.content "Permanent link")

```
content = Field(
    description="The content as Markdown/HTML or the text content of the page."
)
```

### url `class-attribute` `instance-attribute` [¶](#scrapling.core.ai.ResponseModel.url "Permanent link")

```
url = Field(
    description="The URL given by the user that resulted in this response."
)
```

## Session Models[¶](#session-models "Permanent link")

Model classes for session management:

## scrapling.core.ai.SessionInfo [¶](#scrapling.core.ai.SessionInfo "Permanent link")

Bases: `BaseModel`

```
              flowchart TD
              scrapling.core.ai.SessionInfo[SessionInfo]

              

              click scrapling.core.ai.SessionInfo href "" "scrapling.core.ai.SessionInfo"
```

Information about an open browser session.

### session_id `class-attribute` `instance-attribute` [¶](#scrapling.core.ai.SessionInfo.session_id "Permanent link")

```
session_id = Field(
    description="The unique identifier of the session."
)
```

### session_type `class-attribute` `instance-attribute` [¶](#scrapling.core.ai.SessionInfo.session_type "Permanent link")

```
session_type = Field(
    description="The type of the session: 'dynamic' or 'stealthy'."
)
```

### created_at `class-attribute` `instance-attribute` [¶](#scrapling.core.ai.SessionInfo.created_at "Permanent link")

```
created_at = Field(
    description="ISO timestamp of when the session was created."
)
```

### is_alive `class-attribute` `instance-attribute` [¶](#scrapling.core.ai.SessionInfo.is_alive "Permanent link")

```
is_alive = Field(
    description="Whether the session is still alive and usable."
)
```

## scrapling.core.ai.SessionCreatedModel [¶](#scrapling.core.ai.SessionCreatedModel "Permanent link")

Bases: `SessionInfo`

```
              flowchart TD
              scrapling.core.ai.SessionCreatedModel[SessionCreatedModel]
              scrapling.core.ai.SessionInfo[SessionInfo]

                              scrapling.core.ai.SessionInfo --> scrapling.core.ai.SessionCreatedModel
                


              click scrapling.core.ai.SessionCreatedModel href "" "scrapling.core.ai.SessionCreatedModel"
              click scrapling.core.ai.SessionInfo href "" "scrapling.core.ai.SessionInfo"
```

Response returned when a new session is created.

### message `class-attribute` `instance-attribute` [¶](#scrapling.core.ai.SessionCreatedModel.message "Permanent link")

```
message = Field(description='A confirmation message.')
```

### session_id `class-attribute` `instance-attribute` [¶](#scrapling.core.ai.SessionCreatedModel.session_id "Permanent link")

```
session_id = Field(
    description="The unique identifier of the session."
)
```

### session_type `class-attribute` `instance-attribute` [¶](#scrapling.core.ai.SessionCreatedModel.session_type "Permanent link")

```
session_type = Field(
    description="The type of the session: 'dynamic' or 'stealthy'."
)
```

### created_at `class-attribute` `instance-attribute` [¶](#scrapling.core.ai.SessionCreatedModel.created_at "Permanent link")

```
created_at = Field(
    description="ISO timestamp of when the session was created."
)
```

### is_alive `class-attribute` `instance-attribute` [¶](#scrapling.core.ai.SessionCreatedModel.is_alive "Permanent link")

```
is_alive = Field(
    description="Whether the session is still alive and usable."
)
```

## scrapling.core.ai.SessionClosedModel [¶](#scrapling.core.ai.SessionClosedModel "Permanent link")

Bases: `BaseModel`

```
              flowchart TD
              scrapling.core.ai.SessionClosedModel[SessionClosedModel]

              

              click scrapling.core.ai.SessionClosedModel href "" "scrapling.core.ai.SessionClosedModel"
```

Response returned when a session is closed.

### session_id `class-attribute` `instance-attribute` [¶](#scrapling.core.ai.SessionClosedModel.session_id "Permanent link")

```
session_id = Field(
    description="The unique identifier of the closed session."
)
```

### message `class-attribute` `instance-attribute` [¶](#scrapling.core.ai.SessionClosedModel.message "Permanent link")

```
message = Field(description='A confirmation message.')
```

## MCP Server Class[¶](#mcp-server-class "Permanent link")

The main MCP server class that provides all web scraping tools:

## scrapling.core.ai.ScraplingMCPServer [¶](#scrapling.core.ai.ScraplingMCPServer "Permanent link")

```
ScraplingMCPServer()
```

Source code in `scrapling/core/ai.py`

|  |  |
| --- | --- |
| ``` 105 106 ``` | ``` def __init__(self):     self._sessions: Dict[str, _SessionEntry] = {} ``` |

### open_session `async` [¶](#scrapling.core.ai.ScraplingMCPServer.open_session "Permanent link")

```
open_session(
    session_type,
    headless=True,
    google_search=True,
    real_chrome=False,
    wait=0,
    proxy=None,
    timezone_id=None,
    locale=None,
    extra_headers=None,
    useragent=None,
    cdp_url=None,
    timeout=30000,
    disable_resources=False,
    wait_selector=None,
    cookies=None,
    network_idle=False,
    wait_selector_state="attached",
    max_pages=5,
    hide_canvas=False,
    block_webrtc=False,
    allow_webgl=True,
    solve_cloudflare=False,
    additional_args=None,
)
```

Open a persistent browser session that can be reused across multiple fetch calls.
This avoids the overhead of launching a new browser for each request.
Use close_session to close the session when done, and list_sessions to see all active sessions.

| PARAMETER | DESCRIPTION |
| --- | --- |
| `session_type` | The type of session to open. Use "dynamic" for standard Playwright browser, or "stealthy" for anti-bot bypass with fingerprint spoofing.  **TYPE:** `SessionType` |
| `headless` | Run the browser in headless/hidden (default), or headful/visible mode.  **TYPE:** `bool`  **DEFAULT:** `True` |
| `google_search` | Enabled by default, Scrapling will set a Google referer header.  **TYPE:** `bool`  **DEFAULT:** `True` |
| `real_chrome` | If you have a Chrome browser installed on your device, enable this, and the Fetcher will launch an instance of your browser and use it.  **TYPE:** `bool`  **DEFAULT:** `False` |
| `wait` | The time (milliseconds) the fetcher will wait after everything finishes before closing the page and returning the Response object.  **TYPE:** `int | float`  **DEFAULT:** `0` |
| `proxy` | The proxy to be used with requests, it can be a string or a dictionary with the keys 'server', 'username', and 'password' only.  **TYPE:** `Optional[str | Dict[str, str]]`  **DEFAULT:** `None` |
| `timezone_id` | Changes the timezone of the browser. Defaults to the system timezone.  **TYPE:** `str | None`  **DEFAULT:** `None` |
| `locale` | Specify user locale, for example, `en-GB`, `de-DE`, etc.  **TYPE:** `str | None`  **DEFAULT:** `None` |
| `extra_headers` | A dictionary of extra headers to add to the request.  **TYPE:** `Optional[Dict[str, str]]`  **DEFAULT:** `None` |
| `useragent` | Pass a useragent string to be used. Otherwise the fetcher will generate a real Useragent of the same browser and use it.  **TYPE:** `Optional[str]`  **DEFAULT:** `None` |
| `cdp_url` | Instead of launching a new browser instance, connect to this CDP URL to control real browsers through CDP.  **TYPE:** `Optional[str]`  **DEFAULT:** `None` |
| `timeout` | The timeout in milliseconds that is used in all operations and waits through the page. The default is 30,000.  **TYPE:** `int | float`  **DEFAULT:** `30000` |
| `disable_resources` | Drop requests for unnecessary resources for a speed boost.  **TYPE:** `bool`  **DEFAULT:** `False` |
| `wait_selector` | Wait for a specific CSS selector to be in a specific state.  **TYPE:** `Optional[str]`  **DEFAULT:** `None` |
| `cookies` | Set cookies for the session. It should be in a dictionary format that Playwright accepts.  **TYPE:** `Sequence[SetCookieParam] | None`  **DEFAULT:** `None` |
| `network_idle` | Wait for the page until there are no network connections for at least 500 ms.  **TYPE:** `bool`  **DEFAULT:** `False` |
| `wait_selector_state` | The state to wait for the selector given with `wait_selector`. The default state is `attached`.  **TYPE:** `SelectorWaitStates`  **DEFAULT:** `'attached'` |
| `max_pages` | Maximum number of concurrent pages/tabs in the browser. Defaults to 5. Higher values allow more parallel fetches.  **TYPE:** `int`  **DEFAULT:** `5` |
| `hide_canvas` | (Stealthy only) Add random noise to canvas operations to prevent fingerprinting.  **TYPE:** `bool`  **DEFAULT:** `False` |
| `block_webrtc` | (Stealthy only) Forces WebRTC to respect proxy settings to prevent local IP address leak.  **TYPE:** `bool`  **DEFAULT:** `False` |
| `allow_webgl` | (Stealthy only) Enabled by default. Disabling WebGL is not recommended as many WAFs now check if WebGL is enabled.  **TYPE:** `bool`  **DEFAULT:** `True` |
| `solve_cloudflare` | (Stealthy only) Solves all types of the Cloudflare's Turnstile/Interstitial challenges.  **TYPE:** `bool`  **DEFAULT:** `False` |
| `additional_args` | (Stealthy only) Additional arguments to be passed to Playwright's context as additional settings.  **TYPE:** `Optional[Dict]`  **DEFAULT:** `None` |

Source code in `scrapling/core/ai.py`

|  |  |
| --- | --- |
| ``` 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200 201 202 203 204 205 206 207 208 209 210 211 212 213 214 215 216 217 218 219 220 221 222 ``` | ``` async def open_session(     self,     session_type: SessionType,     headless: bool = True,     google_search: bool = True,     real_chrome: bool = False,     wait: int | float = 0,     proxy: Optional[str | Dict[str, str]] = None,     timezone_id: str | None = None,     locale: str | None = None,     extra_headers: Optional[Dict[str, str]] = None,     useragent: Optional[str] = None,     cdp_url: Optional[str] = None,     timeout: int | float = 30000,     disable_resources: bool = False,     wait_selector: Optional[str] = None,     cookies: Sequence[SetCookieParam] | None = None,     network_idle: bool = False,     wait_selector_state: SelectorWaitStates = "attached",     max_pages: int = 5,     # Stealthy-only params (ignored for dynamic sessions)     hide_canvas: bool = False,     block_webrtc: bool = False,     allow_webgl: bool = True,     solve_cloudflare: bool = False,     additional_args: Optional[Dict] = None, ) -> SessionCreatedModel:     """Open a persistent browser session that can be reused across multiple fetch calls.     This avoids the overhead of launching a new browser for each request.     Use close_session to close the session when done, and list_sessions to see all active sessions.      :param session_type: The type of session to open. Use "dynamic" for standard Playwright browser, or "stealthy" for anti-bot bypass with fingerprint spoofing.     :param headless: Run the browser in headless/hidden (default), or headful/visible mode.     :param google_search: Enabled by default, Scrapling will set a Google referer header.     :param real_chrome: If you have a Chrome browser installed on your device, enable this, and the Fetcher will launch an instance of your browser and use it.     :param wait: The time (milliseconds) the fetcher will wait after everything finishes before closing the page and returning the Response object.     :param proxy: The proxy to be used with requests, it can be a string or a dictionary with the keys 'server', 'username', and 'password' only.     :param timezone_id: Changes the timezone of the browser. Defaults to the system timezone.     :param locale: Specify user locale, for example, `en-GB`, `de-DE`, etc.     :param extra_headers: A dictionary of extra headers to add to the request.     :param useragent: Pass a useragent string to be used. Otherwise the fetcher will generate a real Useragent of the same browser and use it.     :param cdp_url: Instead of launching a new browser instance, connect to this CDP URL to control real browsers through CDP.     :param timeout: The timeout in milliseconds that is used in all operations and waits through the page. The default is 30,000.     :param disable_resources: Drop requests for unnecessary resources for a speed boost.     :param wait_selector: Wait for a specific CSS selector to be in a specific state.     :param cookies: Set cookies for the session. It should be in a dictionary format that Playwright accepts.     :param network_idle: Wait for the page until there are no network connections for at least 500 ms.     :param wait_selector_state: The state to wait for the selector given with `wait_selector`. The default state is `attached`.     :param max_pages: Maximum number of concurrent pages/tabs in the browser. Defaults to 5. Higher values allow more parallel fetches.     :param hide_canvas: (Stealthy only) Add random noise to canvas operations to prevent fingerprinting.     :param block_webrtc: (Stealthy only) Forces WebRTC to respect proxy settings to prevent local IP address leak.     :param allow_webgl: (Stealthy only) Enabled by default. Disabling WebGL is not recommended as many WAFs now check if WebGL is enabled.     :param solve_cloudflare: (Stealthy only) Solves all types of the Cloudflare's Turnstile/Interstitial challenges.     :param additional_args: (Stealthy only) Additional arguments to be passed to Playwright's context as additional settings.     """     common_kwargs: Dict[str, Any] = dict(         wait=wait,         proxy=proxy,         locale=locale,         timeout=timeout,         cookies=cookies,         cdp_url=cdp_url,         headless=headless,         max_pages=max_pages,         useragent=useragent,         timezone_id=timezone_id,         real_chrome=real_chrome,         network_idle=network_idle,         wait_selector=wait_selector,         google_search=google_search,         extra_headers=extra_headers,         disable_resources=disable_resources,         wait_selector_state=wait_selector_state,     )      session: Union[AsyncDynamicSession, AsyncStealthySession]     if session_type == "stealthy":         session = AsyncStealthySession(             **common_kwargs,             hide_canvas=hide_canvas,             block_webrtc=block_webrtc,             allow_webgl=allow_webgl,             solve_cloudflare=solve_cloudflare,             additional_args=additional_args,         )     else:         session = AsyncDynamicSession(**common_kwargs)      await session.start()      session_id = uuid4().hex[:12]     entry = _SessionEntry(session=session, session_type=session_type)     self._sessions[session_id] = entry      return SessionCreatedModel(         session_id=session_id,         session_type=session_type,         created_at=entry.created_at,         is_alive=True,         message=f"Session '{session_id}' ({session_type}) created successfully.",     ) ``` |

### close_session `async` [¶](#scrapling.core.ai.ScraplingMCPServer.close_session "Permanent link")

```
close_session(session_id)
```

Close a persistent browser session and free its resources.

| PARAMETER | DESCRIPTION |
| --- | --- |
| `session_id` | The unique identifier of the session to close. Use list_sessions to see active sessions.  **TYPE:** `str` |

Source code in `scrapling/core/ai.py`

|  |  |
| --- | --- |
| ``` 224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239 240 ``` | ``` async def close_session(     self,     session_id: str, ) -> SessionClosedModel:     """Close a persistent browser session and free its resources.      :param session_id: The unique identifier of the session to close. Use list_sessions to see active sessions.     """     entry = self._sessions.pop(session_id, None)     if entry is None:         raise ValueError(f"Session '{session_id}' not found. Use list_sessions to see active sessions.")      await entry.session.close()     return SessionClosedModel(         session_id=session_id,         message=f"Session '{session_id}' closed successfully.",     ) ``` |

### list_sessions `async` [¶](#scrapling.core.ai.ScraplingMCPServer.list_sessions "Permanent link")

```
list_sessions()
```

List all active browser sessions with their details.

Source code in `scrapling/core/ai.py`

|  |  |
| --- | --- |
| ``` 242 243 244 245 246 247 248 249 250 251 252 ``` | ``` async def list_sessions(self) -> List[SessionInfo]:     """List all active browser sessions with their details."""     return [         SessionInfo(             session_id=sid,             session_type=entry.session_type,             created_at=entry.created_at,             is_alive=entry.session._is_alive,         )         for sid, entry in self._sessions.items()     ] ``` |

### get `async` `staticmethod` [¶](#scrapling.core.ai.ScraplingMCPServer.get "Permanent link")

```
get(
    url,
    impersonate="chrome",
    extraction_type="markdown",
    css_selector=None,
    main_content_only=True,
    params=None,
    headers=None,
    cookies=None,
    timeout=30,
    follow_redirects=True,
    max_redirects=30,
    retries=3,
    retry_delay=1,
    proxy=None,
    proxy_auth=None,
    auth=None,
    verify=True,
    http3=False,
    stealthy_headers=True,
)
```

Make GET HTTP request to a URL and return a structured output of the result.
Note: This is only suitable for low-mid protection levels. For high-protection levels or websites that require JS loading, use the other tools directly.
Note: If the `css_selector` resolves to more than one element, all the elements will be returned.

| PARAMETER | DESCRIPTION |
| --- | --- |
| `url` | The URL to request.  **TYPE:** `str` |
| `impersonate` | Browser version to impersonate its fingerprint. It's using the latest chrome version by default.  **TYPE:** `ImpersonateType`  **DEFAULT:** `'chrome'` |
| `extraction_type` | The type of content to extract from the page. Defaults to "markdown". Options are: - Markdown will convert the page content to Markdown format. - HTML will return the raw HTML content of the page. - Text will return the text content of the page.  **TYPE:** `extraction_types`  **DEFAULT:** `'markdown'` |
| `css_selector` | CSS selector to extract the content from the page. If main_content_only is True, then it will be executed on the main content of the page. Defaults to None.  **TYPE:** `Optional[str]`  **DEFAULT:** `None` |
| `main_content_only` | Whether to extract only the main content of the page. Defaults to True. The main content here is the data inside the `<body>` tag.  **TYPE:** `bool`  **DEFAULT:** `True` |
| `params` | Query string parameters for the request.  **TYPE:** `Optional[Dict]`  **DEFAULT:** `None` |
| `headers` | Headers to include in the request.  **TYPE:** `Optional[Mapping[str, Optional[str]]]`  **DEFAULT:** `None` |
| `cookies` | Cookies to use in the request.  **TYPE:** `Optional[Dict[str, str]]`  **DEFAULT:** `None` |
| `timeout` | Number of seconds to wait before timing out.  **TYPE:** `Optional[int | float]`  **DEFAULT:** `30` |
| `follow_redirects` | Whether to follow redirects. Defaults to True.  **TYPE:** `bool`  **DEFAULT:** `True` |
| `max_redirects` | Maximum number of redirects. Default 30, use -1 for unlimited.  **TYPE:** `int`  **DEFAULT:** `30` |
| `retries` | Number of retry attempts. Defaults to 3.  **TYPE:** `Optional[int]`  **DEFAULT:** `3` |
| `retry_delay` | Number of seconds to wait between retry attempts. Defaults to 1 second.  **TYPE:** `Optional[int]`  **DEFAULT:** `1` |
| `proxy` | Proxy URL to use. Format: "http://username:password@localhost:8030". Cannot be used together with the `proxies` parameter.  **TYPE:** `Optional[str]`  **DEFAULT:** `None` |
| `proxy_auth` | HTTP basic auth for proxy in dictionary format with `username` and `password` keys.  **TYPE:** `Optional[Dict[str, str]]`  **DEFAULT:** `None` |
| `auth` | HTTP basic auth in dictionary format with `username` and `password` keys.  **TYPE:** `Optional[Dict[str, str]]`  **DEFAULT:** `None` |
| `verify` | Whether to verify HTTPS certificates.  **TYPE:** `Optional[bool]`  **DEFAULT:** `True` |
| `http3` | Whether to use HTTP3. Defaults to False. It might be problematic if used it with `impersonate`.  **TYPE:** `Optional[bool]`  **DEFAULT:** `False` |
| `stealthy_headers` | If enabled (default), it creates and adds real browser headers. It also sets a Google referer header.  **TYPE:** `Optional[bool]`  **DEFAULT:** `True` |

Source code in `scrapling/core/ai.py`

|  |  |
| --- | --- |
| ``` 254 255 256 257 258 259 260 261 262 263 264 265 266 267 268 269 270 271 272 273 274 275 276 277 278 279 280 281 282 283 284 285 286 287 288 289 290 291 292 293 294 295 296 297 298 299 300 301 302 303 304 305 306 307 308 309 310 311 312 313 314 315 316 317 318 319 320 321 322 323 324 325 ``` | ``` @staticmethod async def get(     url: str,     impersonate: ImpersonateType = "chrome",     extraction_type: extraction_types = "markdown",     css_selector: Optional[str] = None,     main_content_only: bool = True,     params: Optional[Dict] = None,     headers: Optional[Mapping[str, Optional[str]]] = None,     cookies: Optional[Dict[str, str]] = None,     timeout: Optional[int | float] = 30,     follow_redirects: bool = True,     max_redirects: int = 30,     retries: Optional[int] = 3,     retry_delay: Optional[int] = 1,     proxy: Optional[str] = None,     proxy_auth: Optional[Dict[str, str]] = None,     auth: Optional[Dict[str, str]] = None,     verify: Optional[bool] = True,     http3: Optional[bool] = False,     stealthy_headers: Optional[bool] = True, ) -> ResponseModel:     """Make GET HTTP request to a URL and return a structured output of the result.     Note: This is only suitable for low-mid protection levels. For high-protection levels or websites that require JS loading, use the other tools directly.     Note: If the `css_selector` resolves to more than one element, all the elements will be returned.      :param url: The URL to request.     :param impersonate: Browser version to impersonate its fingerprint. It's using the latest chrome version by default.     :param extraction_type: The type of content to extract from the page. Defaults to "markdown". Options are:         - Markdown will convert the page content to Markdown format.         - HTML will return the raw HTML content of the page.         - Text will return the text content of the page.     :param css_selector: CSS selector to extract the content from the page. If main_content_only is True, then it will be executed on the main content of the page. Defaults to None.     :param main_content_only: Whether to extract only the main content of the page. Defaults to True. The main content here is the data inside the `<body>` tag.     :param params: Query string parameters for the request.     :param headers: Headers to include in the request.     :param cookies: Cookies to use in the request.     :param timeout: Number of seconds to wait before timing out.     :param follow_redirects: Whether to follow redirects. Defaults to True.     :param max_redirects: Maximum number of redirects. Default 30, use -1 for unlimited.     :param retries: Number of retry attempts. Defaults to 3.     :param retry_delay: Number of seconds to wait between retry attempts. Defaults to 1 second.     :param proxy: Proxy URL to use. Format: "http://username:password@localhost:8030".                  Cannot be used together with the `proxies` parameter.     :param proxy_auth: HTTP basic auth for proxy in dictionary format with `username` and `password` keys.     :param auth: HTTP basic auth in dictionary format with `username` and `password` keys.     :param verify: Whether to verify HTTPS certificates.     :param http3: Whether to use HTTP3. Defaults to False. It might be problematic if used it with `impersonate`.     :param stealthy_headers: If enabled (default), it creates and adds real browser headers. It also sets a Google referer header.     """     results = await ScraplingMCPServer.bulk_get(         urls=[url],         impersonate=impersonate,         extraction_type=extraction_type,         css_selector=css_selector,         main_content_only=main_content_only,         params=params,         headers=headers,         cookies=cookies,         timeout=timeout,         follow_redirects=follow_redirects,         max_redirects=max_redirects,         retries=retries,         retry_delay=retry_delay,         proxy=proxy,         proxy_auth=proxy_auth,         auth=auth,         verify=verify,         http3=http3,         stealthy_headers=stealthy_headers,     )     return results[0] ``` |

### bulk_get `async` `staticmethod` [¶](#scrapling.core.ai.ScraplingMCPServer.bulk_get "Permanent link")

```
bulk_get(
    urls,
    impersonate="chrome",
    extraction_type="markdown",
    css_selector=None,
    main_content_only=True,
    params=None,
    headers=None,
    cookies=None,
    timeout=30,
    follow_redirects=True,
    max_redirects=30,
    retries=3,
    retry_delay=1,
    proxy=None,
    proxy_auth=None,
    auth=None,
    verify=True,
    http3=False,
    stealthy_headers=True,
)
```

Make GET HTTP request to a group of URLs and for each URL, return a structured output of the result.
Note: This is only suitable for low-mid protection levels. For high-protection levels or websites that require JS loading, use the other tools directly.
Note: If the `css_selector` resolves to more than one element, all the elements will be returned.

| PARAMETER | DESCRIPTION |
| --- | --- |
| `urls` | A list of the URLs to request.  **TYPE:** `List[str]` |
| `impersonate` | Browser version to impersonate its fingerprint. It's using the latest chrome version by default.  **TYPE:** `ImpersonateType`  **DEFAULT:** `'chrome'` |
| `extraction_type` | The type of content to extract from the page. Defaults to "markdown". Options are: - Markdown will convert the page content to Markdown format. - HTML will return the raw HTML content of the page. - Text will return the text content of the page.  **TYPE:** `extraction_types`  **DEFAULT:** `'markdown'` |
| `css_selector` | CSS selector to extract the content from the page. If main_content_only is True, then it will be executed on the main content of the page. Defaults to None.  **TYPE:** `Optional[str]`  **DEFAULT:** `None` |
| `main_content_only` | Whether to extract only the main content of the page. Defaults to True. The main content here is the data inside the `<body>` tag.  **TYPE:** `bool`  **DEFAULT:** `True` |
| `params` | Query string parameters for the request.  **TYPE:** `Optional[Dict]`  **DEFAULT:** `None` |
| `headers` | Headers to include in the request.  **TYPE:** `Optional[Mapping[str, Optional[str]]]`  **DEFAULT:** `None` |
| `cookies` | Cookies to use in the request.  **TYPE:** `Optional[Dict[str, str]]`  **DEFAULT:** `None` |
| `timeout` | Number of seconds to wait before timing out.  **TYPE:** `Optional[int | float]`  **DEFAULT:** `30` |
| `follow_redirects` | Whether to follow redirects. Defaults to True.  **TYPE:** `bool`  **DEFAULT:** `True` |
| `max_redirects` | Maximum number of redirects. Default 30, use -1 for unlimited.  **TYPE:** `int`  **DEFAULT:** `30` |
| `retries` | Number of retry attempts. Defaults to 3.  **TYPE:** `Optional[int]`  **DEFAULT:** `3` |
| `retry_delay` | Number of seconds to wait between retry attempts. Defaults to 1 second.  **TYPE:** `Optional[int]`  **DEFAULT:** `1` |
| `proxy` | Proxy URL to use. Format: "http://username:password@localhost:8030". Cannot be used together with the `proxies` parameter.  **TYPE:** `Optional[str]`  **DEFAULT:** `None` |
| `proxy_auth` | HTTP basic auth for proxy in dictionary format with `username` and `password` keys.  **TYPE:** `Optional[Dict[str, str]]`  **DEFAULT:** `None` |
| `auth` | HTTP basic auth in dictionary format with `username` and `password` keys.  **TYPE:** `Optional[Dict[str, str]]`  **DEFAULT:** `None` |
| `verify` | Whether to verify HTTPS certificates.  **TYPE:** `Optional[bool]`  **DEFAULT:** `True` |
| `http3` | Whether to use HTTP3. Defaults to False. It might be problematic if used it with `impersonate`.  **TYPE:** `Optional[bool]`  **DEFAULT:** `False` |
| `stealthy_headers` | If enabled (default), it creates and adds real browser headers. It also sets a Google referer header.  **TYPE:** `Optional[bool]`  **DEFAULT:** `True` |

Source code in `scrapling/core/ai.py`

|  |  |
| --- | --- |
| ``` 327 328 329 330 331 332 333 334 335 336 337 338 339 340 341 342 343 344 345 346 347 348 349 350 351 352 353 354 355 356 357 358 359 360 361 362 363 364 365 366 367 368 369 370 371 372 373 374 375 376 377 378 379 380 381 382 383 384 385 386 387 388 389 390 391 392 393 394 395 396 397 398 399 400 401 402 403 ``` | ``` @staticmethod async def bulk_get(     urls: List[str],     impersonate: ImpersonateType = "chrome",     extraction_type: extraction_types = "markdown",     css_selector: Optional[str] = None,     main_content_only: bool = True,     params: Optional[Dict] = None,     headers: Optional[Mapping[str, Optional[str]]] = None,     cookies: Optional[Dict[str, str]] = None,     timeout: Optional[int | float] = 30,     follow_redirects: bool = True,     max_redirects: int = 30,     retries: Optional[int] = 3,     retry_delay: Optional[int] = 1,     proxy: Optional[str] = None,     proxy_auth: Optional[Dict[str, str]] = None,     auth: Optional[Dict[str, str]] = None,     verify: Optional[bool] = True,     http3: Optional[bool] = False,     stealthy_headers: Optional[bool] = True, ) -> List[ResponseModel]:     """Make GET HTTP request to a group of URLs and for each URL, return a structured output of the result.     Note: This is only suitable for low-mid protection levels. For high-protection levels or websites that require JS loading, use the other tools directly.     Note: If the `css_selector` resolves to more than one element, all the elements will be returned.      :param urls: A list of the URLs to request.     :param impersonate: Browser version to impersonate its fingerprint. It's using the latest chrome version by default.     :param extraction_type: The type of content to extract from the page. Defaults to "markdown". Options are:         - Markdown will convert the page content to Markdown format.         - HTML will return the raw HTML content of the page.         - Text will return the text content of the page.     :param css_selector: CSS selector to extract the content from the page. If main_content_only is True, then it will be executed on the main content of the page. Defaults to None.     :param main_content_only: Whether to extract only the main content of the page. Defaults to True. The main content here is the data inside the `<body>` tag.     :param params: Query string parameters for the request.     :param headers: Headers to include in the request.     :param cookies: Cookies to use in the request.     :param timeout: Number of seconds to wait before timing out.     :param follow_redirects: Whether to follow redirects. Defaults to True.     :param max_redirects: Maximum number of redirects. Default 30, use -1 for unlimited.     :param retries: Number of retry attempts. Defaults to 3.     :param retry_delay: Number of seconds to wait between retry attempts. Defaults to 1 second.     :param proxy: Proxy URL to use. Format: "http://username:password@localhost:8030".                  Cannot be used together with the `proxies` parameter.     :param proxy_auth: HTTP basic auth for proxy in dictionary format with `username` and `password` keys.     :param auth: HTTP basic auth in dictionary format with `username` and `password` keys.     :param verify: Whether to verify HTTPS certificates.     :param http3: Whether to use HTTP3. Defaults to False. It might be problematic if used it with `impersonate`.     :param stealthy_headers: If enabled (default), it creates and adds real browser headers. It also sets a Google referer header.     """     normalized_proxy_auth = _normalize_credentials(proxy_auth)     normalized_auth = _normalize_credentials(auth)      async with FetcherSession() as session:         tasks: List[Any] = [             session.get(                 url,                 auth=normalized_auth,                 proxy=proxy,                 http3=http3,                 verify=verify,                 params=params,                 headers=headers,                 cookies=cookies,                 timeout=timeout,                 retries=retries,                 proxy_auth=normalized_proxy_auth,                 retry_delay=retry_delay,                 impersonate=impersonate,                 max_redirects=max_redirects,                 follow_redirects=follow_redirects,                 stealthy_headers=stealthy_headers,             )             for url in urls         ]         responses = await gather(*tasks)         return [_translate_response(page, extraction_type, css_selector, main_content_only) for page in responses] ``` |

### fetch `async` [¶](#scrapling.core.ai.ScraplingMCPServer.fetch "Permanent link")

```
fetch(
    url,
    extraction_type="markdown",
    css_selector=None,
    main_content_only=True,
    headless=True,
    google_search=True,
    real_chrome=False,
    wait=0,
    proxy=None,
    timezone_id=None,
    locale=None,
    extra_headers=None,
    useragent=None,
    cdp_url=None,
    timeout=30000,
    disable_resources=False,
    wait_selector=None,
    cookies=None,
    network_idle=False,
    wait_selector_state="attached",
    session_id=None,
)
```

Use playwright to open a browser to fetch a URL and return a structured output of the result.
Note: This is only suitable for low-mid protection levels.
Note: If the `css_selector` resolves to more than one element, all the elements will be returned.
Note: If a `session_id` is provided (from open_session), the browser session will be reused instead of creating a new one.
When using a session, browser-level params (headless, proxy, locale, etc.) are ignored since they were set at session creation time.

| PARAMETER | DESCRIPTION |
| --- | --- |
| `url` | The URL to request.  **TYPE:** `str` |
| `extraction_type` | The type of content to extract from the page. Defaults to "markdown". Options are: - Markdown will convert the page content to Markdown format. - HTML will return the raw HTML content of the page. - Text will return the text content of the page.  **TYPE:** `extraction_types`  **DEFAULT:** `'markdown'` |
| `css_selector` | CSS selector to extract the content from the page. If main_content_only is True, then it will be executed on the main content of the page. Defaults to None.  **TYPE:** `Optional[str]`  **DEFAULT:** `None` |
| `main_content_only` | Whether to extract only the main content of the page. Defaults to True. The main content here is the data inside the `<body>` tag.  **TYPE:** `bool`  **DEFAULT:** `True` |
| `headless` | Run the browser in headless/hidden (default), or headful/visible mode.  **TYPE:** `bool`  **DEFAULT:** `True` |
| `disable_resources` | Drop requests for unnecessary resources for a speed boost. Requests dropped are of type `font`, `image`, `media`, `beacon`, `object`, `imageset`, `texttrack`, `websocket`, `csp_report`, and `stylesheet`.  **TYPE:** `bool`  **DEFAULT:** `False` |
| `useragent` | Pass a useragent string to be used. Otherwise the fetcher will generate a real Useragent of the same browser and use it.  **TYPE:** `Optional[str]`  **DEFAULT:** `None` |
| `cookies` | Set cookies for the next request. It should be in a dictionary format that Playwright accepts.  **TYPE:** `Sequence[SetCookieParam] | None`  **DEFAULT:** `None` |
| `network_idle` | Wait for the page until there are no network connections for at least 500 ms.  **TYPE:** `bool`  **DEFAULT:** `False` |
| `timeout` | The timeout in milliseconds that is used in all operations and waits through the page. The default is 30,000  **TYPE:** `int | float`  **DEFAULT:** `30000` |
| `wait` | The time (milliseconds) the fetcher will wait after everything finishes before closing the page and returning the `Response` object.  **TYPE:** `int | float`  **DEFAULT:** `0` |
| `wait_selector` | Wait for a specific CSS selector to be in a specific state.  **TYPE:** `Optional[str]`  **DEFAULT:** `None` |
| `timezone_id` | Changes the timezone of the browser. Defaults to the system timezone.  **TYPE:** `str | None`  **DEFAULT:** `None` |
| `locale` | Specify user locale, for example, `en-GB`, `de-DE`, etc. Locale will affect navigator.language value, Accept-Language request header value as well as number and date formatting rules. Defaults to the system default locale.  **TYPE:** `str | None`  **DEFAULT:** `None` |
| `wait_selector_state` | The state to wait for the selector given with `wait_selector`. The default state is `attached`.  **TYPE:** `SelectorWaitStates`  **DEFAULT:** `'attached'` |
| `real_chrome` | If you have a Chrome browser installed on your device, enable this, and the Fetcher will launch an instance of your browser and use it.  **TYPE:** `bool`  **DEFAULT:** `False` |
| `cdp_url` | Instead of launching a new browser instance, connect to this CDP URL to control real browsers through CDP.  **TYPE:** `Optional[str]`  **DEFAULT:** `None` |
| `google_search` | Enabled by default, Scrapling will set a Google referer header.  **TYPE:** `bool`  **DEFAULT:** `True` |
| `extra_headers` | A dictionary of extra headers to add to the request. *The referer set by `google_search` takes priority over the referer set here if used together.*  **TYPE:** `Optional[Dict[str, str]]`  **DEFAULT:** `None` |
| `proxy` | The proxy to be used with requests, it can be a string or a dictionary with the keys 'server', 'username', and 'password' only.  **TYPE:** `Optional[str | Dict[str, str]]`  **DEFAULT:** `None` |
| `session_id` | Optional session ID from open_session. If provided, reuses the existing browser session instead of creating a new one.  **TYPE:** `Optional[str]`  **DEFAULT:** `None` |

Source code in `scrapling/core/ai.py`

|  |  |
| --- | --- |
| ``` 405 406 407 408 409 410 411 412 413 414 415 416 417 418 419 420 421 422 423 424 425 426 427 428 429 430 431 432 433 434 435 436 437 438 439 440 441 442 443 444 445 446 447 448 449 450 451 452 453 454 455 456 457 458 459 460 461 462 463 464 465 466 467 468 469 470 471 472 473 474 475 476 477 478 479 480 481 482 483 484 485 ``` | ``` async def fetch(     self,     url: str,     extraction_type: extraction_types = "markdown",     css_selector: Optional[str] = None,     main_content_only: bool = True,     headless: bool = True,  # noqa: F821     google_search: bool = True,     real_chrome: bool = False,     wait: int | float = 0,     proxy: Optional[str | Dict[str, str]] = None,     timezone_id: str | None = None,     locale: str | None = None,     extra_headers: Optional[Dict[str, str]] = None,     useragent: Optional[str] = None,     cdp_url: Optional[str] = None,     timeout: int | float = 30000,     disable_resources: bool = False,     wait_selector: Optional[str] = None,     cookies: Sequence[SetCookieParam] | None = None,     network_idle: bool = False,     wait_selector_state: SelectorWaitStates = "attached",     session_id: Optional[str] = None, ) -> ResponseModel:     """Use playwright to open a browser to fetch a URL and return a structured output of the result.     Note: This is only suitable for low-mid protection levels.     Note: If the `css_selector` resolves to more than one element, all the elements will be returned.     Note: If a `session_id` is provided (from open_session), the browser session will be reused instead of creating a new one.         When using a session, browser-level params (headless, proxy, locale, etc.) are ignored since they were set at session creation time.      :param url: The URL to request.     :param extraction_type: The type of content to extract from the page. Defaults to "markdown". Options are:         - Markdown will convert the page content to Markdown format.         - HTML will return the raw HTML content of the page.         - Text will return the text content of the page.     :param css_selector: CSS selector to extract the content from the page. If main_content_only is True, then it will be executed on the main content of the page. Defaults to None.     :param main_content_only: Whether to extract only the main content of the page. Defaults to True. The main content here is the data inside the `<body>` tag.     :param headless: Run the browser in headless/hidden (default), or headful/visible mode.     :param disable_resources: Drop requests for unnecessary resources for a speed boost.         Requests dropped are of type `font`, `image`, `media`, `beacon`, `object`, `imageset`, `texttrack`, `websocket`, `csp_report`, and `stylesheet`.     :param useragent: Pass a useragent string to be used. Otherwise the fetcher will generate a real Useragent of the same browser and use it.     :param cookies: Set cookies for the next request. It should be in a dictionary format that Playwright accepts.     :param network_idle: Wait for the page until there are no network connections for at least 500 ms.     :param timeout: The timeout in milliseconds that is used in all operations and waits through the page. The default is 30,000     :param wait: The time (milliseconds) the fetcher will wait after everything finishes before closing the page and returning the ` Response ` object.     :param wait_selector: Wait for a specific CSS selector to be in a specific state.     :param timezone_id: Changes the timezone of the browser. Defaults to the system timezone.     :param locale: Specify user locale, for example, `en-GB`, `de-DE`, etc. Locale will affect navigator.language value, Accept-Language request header value as well as number and date formatting         rules. Defaults to the system default locale.     :param wait_selector_state: The state to wait for the selector given with `wait_selector`. The default state is `attached`.     :param real_chrome: If you have a Chrome browser installed on your device, enable this, and the Fetcher will launch an instance of your browser and use it.     :param cdp_url: Instead of launching a new browser instance, connect to this CDP URL to control real browsers through CDP.     :param google_search: Enabled by default, Scrapling will set a Google referer header.     :param extra_headers: A dictionary of extra headers to add to the request. _The referer set by `google_search` takes priority over the referer set here if used together._     :param proxy: The proxy to be used with requests, it can be a string or a dictionary with the keys 'server', 'username', and 'password' only.     :param session_id: Optional session ID from open_session. If provided, reuses the existing browser session instead of creating a new one.     """     results = await self.bulk_fetch(         urls=[url],         extraction_type=extraction_type,         css_selector=css_selector,         main_content_only=main_content_only,         headless=headless,         google_search=google_search,         real_chrome=real_chrome,         wait=wait,         proxy=proxy,         timezone_id=timezone_id,         locale=locale,         extra_headers=extra_headers,         useragent=useragent,         cdp_url=cdp_url,         timeout=timeout,         disable_resources=disable_resources,         wait_selector=wait_selector,         cookies=cookies,         network_idle=network_idle,         wait_selector_state=wait_selector_state,         session_id=session_id,     )     return results[0] ``` |

### bulk_fetch `async` [¶](#scrapling.core.ai.ScraplingMCPServer.bulk_fetch "Permanent link")

```
bulk_fetch(
    urls,
    extraction_type="markdown",
    css_selector=None,
    main_content_only=True,
    headless=True,
    google_search=True,
    real_chrome=False,
    wait=0,
    proxy=None,
    timezone_id=None,
    locale=None,
    extra_headers=None,
    useragent=None,
    cdp_url=None,
    timeout=30000,
    disable_resources=False,
    wait_selector=None,
    cookies=None,
    network_idle=False,
    wait_selector_state="attached",
    session_id=None,
)
```

Use playwright to open a browser, then fetch a group of URLs at the same time, and for each page return a structured output of the result.
Note: This is only suitable for low-mid protection levels.
Note: If the `css_selector` resolves to more than one element, all the elements will be returned.
Note: If a `session_id` is provided (from open_session), the browser session will be reused instead of creating a new one.
When using a session, browser-level params (headless, proxy, locale, etc.) are ignored since they were set at session creation time.

| PARAMETER | DESCRIPTION |
| --- | --- |
| `urls` | A list of the URLs to request.  **TYPE:** `List[str]` |
| `extraction_type` | The type of content to extract from the page. Defaults to "markdown". Options are: - Markdown will convert the page content to Markdown format. - HTML will return the raw HTML content of the page. - Text will return the text content of the page.  **TYPE:** `extraction_types`  **DEFAULT:** `'markdown'` |
| `css_selector` | CSS selector to extract the content from the page. If main_content_only is True, then it will be executed on the main content of the page. Defaults to None.  **TYPE:** `Optional[str]`  **DEFAULT:** `None` |
| `main_content_only` | Whether to extract only the main content of the page. Defaults to True. The main content here is the data inside the `<body>` tag.  **TYPE:** `bool`  **DEFAULT:** `True` |
| `headless` | Run the browser in headless/hidden (default), or headful/visible mode.  **TYPE:** `bool`  **DEFAULT:** `True` |
| `disable_resources` | Drop requests for unnecessary resources for a speed boost. Requests dropped are of type `font`, `image`, `media`, `beacon`, `object`, `imageset`, `texttrack`, `websocket`, `csp_report`, and `stylesheet`.  **TYPE:** `bool`  **DEFAULT:** `False` |
| `useragent` | Pass a useragent string to be used. Otherwise the fetcher will generate a real Useragent of the same browser and use it.  **TYPE:** `Optional[str]`  **DEFAULT:** `None` |
| `cookies` | Set cookies for the next request. It should be in a dictionary format that Playwright accepts.  **TYPE:** `Sequence[SetCookieParam] | None`  **DEFAULT:** `None` |
| `network_idle` | Wait for the page until there are no network connections for at least 500 ms.  **TYPE:** `bool`  **DEFAULT:** `False` |
| `timeout` | The timeout in milliseconds that is used in all operations and waits through the page. The default is 30,000  **TYPE:** `int | float`  **DEFAULT:** `30000` |
| `wait` | The time (milliseconds) the fetcher will wait after everything finishes before closing the page and returning the `Response` object.  **TYPE:** `int | float`  **DEFAULT:** `0` |
| `wait_selector` | Wait for a specific CSS selector to be in a specific state.  **TYPE:** `Optional[str]`  **DEFAULT:** `None` |
| `timezone_id` | Changes the timezone of the browser. Defaults to the system timezone.  **TYPE:** `str | None`  **DEFAULT:** `None` |
| `locale` | Specify user locale, for example, `en-GB`, `de-DE`, etc. Locale will affect navigator.language value, Accept-Language request header value as well as number and date formatting rules. Defaults to the system default locale.  **TYPE:** `str | None`  **DEFAULT:** `None` |
| `wait_selector_state` | The state to wait for the selector given with `wait_selector`. The default state is `attached`.  **TYPE:** `SelectorWaitStates`  **DEFAULT:** `'attached'` |
| `real_chrome` | If you have a Chrome browser installed on your device, enable this, and the Fetcher will launch an instance of your browser and use it.  **TYPE:** `bool`  **DEFAULT:** `False` |
| `cdp_url` | Instead of launching a new browser instance, connect to this CDP URL to control real browsers through CDP.  **TYPE:** `Optional[str]`  **DEFAULT:** `None` |
| `google_search` | Enabled by default, Scrapling will set a Google referer header.  **TYPE:** `bool`  **DEFAULT:** `True` |
| `extra_headers` | A dictionary of extra headers to add to the request. *The referer set by `google_search` takes priority over the referer set here if used together.*  **TYPE:** `Optional[Dict[str, str]]`  **DEFAULT:** `None` |
| `proxy` | The proxy to be used with requests, it can be a string or a dictionary with the keys 'server', 'username', and 'password' only.  **TYPE:** `Optional[str | Dict[str, str]]`  **DEFAULT:** `None` |
| `session_id` | Optional session ID from open_session. If provided, reuses the existing browser session instead of creating a new one.  **TYPE:** `Optional[str]`  **DEFAULT:** `None` |

Source code in `scrapling/core/ai.py`

|  |  |
| --- | --- |
| ``` 487 488 489 490 491 492 493 494 495 496 497 498 499 500 501 502 503 504 505 506 507 508 509 510 511 512 513 514 515 516 517 518 519 520 521 522 523 524 525 526 527 528 529 530 531 532 533 534 535 536 537 538 539 540 541 542 543 544 545 546 547 548 549 550 551 552 553 554 555 556 557 558 559 560 561 562 563 564 565 566 567 568 569 570 571 572 573 574 575 576 577 578 579 580 581 582 583 584 585 ``` | ``` async def bulk_fetch(     self,     urls: List[str],     extraction_type: extraction_types = "markdown",     css_selector: Optional[str] = None,     main_content_only: bool = True,     headless: bool = True,  # noqa: F821     google_search: bool = True,     real_chrome: bool = False,     wait: int | float = 0,     proxy: Optional[str | Dict[str, str]] = None,     timezone_id: str | None = None,     locale: str | None = None,     extra_headers: Optional[Dict[str, str]] = None,     useragent: Optional[str] = None,     cdp_url: Optional[str] = None,     timeout: int | float = 30000,     disable_resources: bool = False,     wait_selector: Optional[str] = None,     cookies: Sequence[SetCookieParam] | None = None,     network_idle: bool = False,     wait_selector_state: SelectorWaitStates = "attached",     session_id: Optional[str] = None, ) -> List[ResponseModel]:     """Use playwright to open a browser, then fetch a group of URLs at the same time, and for each page return a structured output of the result.     Note: This is only suitable for low-mid protection levels.     Note: If the `css_selector` resolves to more than one element, all the elements will be returned.     Note: If a `session_id` is provided (from open_session), the browser session will be reused instead of creating a new one.         When using a session, browser-level params (headless, proxy, locale, etc.) are ignored since they were set at session creation time.      :param urls: A list of the URLs to request.     :param extraction_type: The type of content to extract from the page. Defaults to "markdown". Options are:         - Markdown will convert the page content to Markdown format.         - HTML will return the raw HTML content of the page.         - Text will return the text content of the page.     :param css_selector: CSS selector to extract the content from the page. If main_content_only is True, then it will be executed on the main content of the page. Defaults to None.     :param main_content_only: Whether to extract only the main content of the page. Defaults to True. The main content here is the data inside the `<body>` tag.     :param headless: Run the browser in headless/hidden (default), or headful/visible mode.     :param disable_resources: Drop requests for unnecessary resources for a speed boost.         Requests dropped are of type `font`, `image`, `media`, `beacon`, `object`, `imageset`, `texttrack`, `websocket`, `csp_report`, and `stylesheet`.     :param useragent: Pass a useragent string to be used. Otherwise the fetcher will generate a real Useragent of the same browser and use it.     :param cookies: Set cookies for the next request. It should be in a dictionary format that Playwright accepts.     :param network_idle: Wait for the page until there are no network connections for at least 500 ms.     :param timeout: The timeout in milliseconds that is used in all operations and waits through the page. The default is 30,000     :param wait: The time (milliseconds) the fetcher will wait after everything finishes before closing the page and returning the ` Response ` object.     :param wait_selector: Wait for a specific CSS selector to be in a specific state.     :param timezone_id: Changes the timezone of the browser. Defaults to the system timezone.     :param locale: Specify user locale, for example, `en-GB`, `de-DE`, etc. Locale will affect navigator.language value, Accept-Language request header value as well as number and date formatting         rules. Defaults to the system default locale.     :param wait_selector_state: The state to wait for the selector given with `wait_selector`. The default state is `attached`.     :param real_chrome: If you have a Chrome browser installed on your device, enable this, and the Fetcher will launch an instance of your browser and use it.     :param cdp_url: Instead of launching a new browser instance, connect to this CDP URL to control real browsers through CDP.     :param google_search: Enabled by default, Scrapling will set a Google referer header.     :param extra_headers: A dictionary of extra headers to add to the request. _The referer set by `google_search` takes priority over the referer set here if used together._     :param proxy: The proxy to be used with requests, it can be a string or a dictionary with the keys 'server', 'username', and 'password' only.     :param session_id: Optional session ID from open_session. If provided, reuses the existing browser session instead of creating a new one.     """     if session_id:         entry = self._get_session(session_id, "dynamic")         tasks = [             entry.session.fetch(                 url,                 wait=wait,                 timeout=timeout,                 google_search=google_search,                 extra_headers=extra_headers,                 disable_resources=disable_resources,                 wait_selector=wait_selector,                 wait_selector_state=wait_selector_state,                 network_idle=network_idle,                 proxy=proxy,             )             for url in urls         ]         responses = await gather(*tasks)     else:         async with AsyncDynamicSession(             wait=wait,             proxy=proxy,             locale=locale,             timeout=timeout,             cookies=cookies,             cdp_url=cdp_url,             headless=headless,             max_pages=len(urls),             useragent=useragent,             timezone_id=timezone_id,             real_chrome=real_chrome,             network_idle=network_idle,             wait_selector=wait_selector,             google_search=google_search,             extra_headers=extra_headers,             disable_resources=disable_resources,             wait_selector_state=wait_selector_state,         ) as session:             tasks = [session.fetch(url) for url in urls]             responses = await gather(*tasks)      return [_translate_response(page, extraction_type, css_selector, main_content_only) for page in responses] ``` |

### stealthy_fetch `async` [¶](#scrapling.core.ai.ScraplingMCPServer.stealthy_fetch "Permanent link")

```
stealthy_fetch(
    url,
    extraction_type="markdown",
    css_selector=None,
    main_content_only=True,
    headless=True,
    google_search=True,
    real_chrome=False,
    wait=0,
    proxy=None,
    timezone_id=None,
    locale=None,
    extra_headers=None,
    useragent=None,
    hide_canvas=False,
    cdp_url=None,
    timeout=30000,
    disable_resources=False,
    wait_selector=None,
    cookies=None,
    network_idle=False,
    wait_selector_state="attached",
    block_webrtc=False,
    allow_webgl=True,
    solve_cloudflare=False,
    additional_args=None,
    session_id=None,
)
```

Use the stealthy fetcher to fetch a URL and return a structured output of the result.
Note: This is the only suitable fetcher for high protection levels.
Note: If the `css_selector` resolves to more than one element, all the elements will be returned.
Note: If a `session_id` is provided (from open_session), the browser session will be reused instead of creating a new one.
When using a session, browser-level params (headless, proxy, locale, etc.) are ignored since they were set at session creation time.

| PARAMETER | DESCRIPTION |
| --- | --- |
| `url` | The URL to request.  **TYPE:** `str` |
| `extraction_type` | The type of content to extract from the page. Defaults to "markdown". Options are: - Markdown will convert the page content to Markdown format. - HTML will return the raw HTML content of the page. - Text will return the text content of the page.  **TYPE:** `extraction_types`  **DEFAULT:** `'markdown'` |
| `css_selector` | CSS selector to extract the content from the page. If main_content_only is True, then it will be executed on the main content of the page. Defaults to None.  **TYPE:** `Optional[str]`  **DEFAULT:** `None` |
| `main_content_only` | Whether to extract only the main content of the page. Defaults to True. The main content here is the data inside the `<body>` tag.  **TYPE:** `bool`  **DEFAULT:** `True` |
| `headless` | Run the browser in headless/hidden (default), or headful/visible mode.  **TYPE:** `bool`  **DEFAULT:** `True` |
| `disable_resources` | Drop requests for unnecessary resources for a speed boost. Requests dropped are of type `font`, `image`, `media`, `beacon`, `object`, `imageset`, `texttrack`, `websocket`, `csp_report`, and `stylesheet`.  **TYPE:** `bool`  **DEFAULT:** `False` |
| `useragent` | Pass a useragent string to be used. Otherwise the fetcher will generate a real Useragent of the same browser and use it.  **TYPE:** `Optional[str]`  **DEFAULT:** `None` |
| `cookies` | Set cookies for the next request.  **TYPE:** `Sequence[SetCookieParam] | None`  **DEFAULT:** `None` |
| `solve_cloudflare` | Solves all types of the Cloudflare's Turnstile/Interstitial challenges before returning the response to you.  **TYPE:** `bool`  **DEFAULT:** `False` |
| `allow_webgl` | Enabled by default. Disabling WebGL is not recommended as many WAFs now check if WebGL is enabled.  **TYPE:** `bool`  **DEFAULT:** `True` |
| `network_idle` | Wait for the page until there are no network connections for at least 500 ms.  **TYPE:** `bool`  **DEFAULT:** `False` |
| `wait` | The time (milliseconds) the fetcher will wait after everything finishes before closing the page and returning the `Response` object.  **TYPE:** `int | float`  **DEFAULT:** `0` |
| `timeout` | The timeout in milliseconds that is used in all operations and waits through the page. The default is 30,000  **TYPE:** `int | float`  **DEFAULT:** `30000` |
| `wait_selector` | Wait for a specific CSS selector to be in a specific state.  **TYPE:** `Optional[str]`  **DEFAULT:** `None` |
| `timezone_id` | Changes the timezone of the browser. Defaults to the system timezone.  **TYPE:** `str | None`  **DEFAULT:** `None` |
| `locale` | Specify user locale, for example, `en-GB`, `de-DE`, etc. Locale will affect navigator.language value, Accept-Language request header value as well as number and date formatting rules. Defaults to the system default locale.  **TYPE:** `str | None`  **DEFAULT:** `None` |
| `wait_selector_state` | The state to wait for the selector given with `wait_selector`. The default state is `attached`.  **TYPE:** `SelectorWaitStates`  **DEFAULT:** `'attached'` |
| `real_chrome` | If you have a Chrome browser installed on your device, enable this, and the Fetcher will launch an instance of your browser and use it.  **TYPE:** `bool`  **DEFAULT:** `False` |
| `hide_canvas` | Add random noise to canvas operations to prevent fingerprinting.  **TYPE:** `bool`  **DEFAULT:** `False` |
| `block_webrtc` | Forces WebRTC to respect proxy settings to prevent local IP address leak.  **TYPE:** `bool`  **DEFAULT:** `False` |
| `cdp_url` | Instead of launching a new browser instance, connect to this CDP URL to control real browsers through CDP.  **TYPE:** `Optional[str]`  **DEFAULT:** `None` |
| `google_search` | Enabled by default, Scrapling will set a Google referer header.  **TYPE:** `bool`  **DEFAULT:** `True` |
| `extra_headers` | A dictionary of extra headers to add to the request. *The referer set by `google_search` takes priority over the referer set here if used together.*  **TYPE:** `Optional[Dict[str, str]]`  **DEFAULT:** `None` |
| `proxy` | The proxy to be used with requests, it can be a string or a dictionary with the keys 'server', 'username', and 'password' only.  **TYPE:** `Optional[str | Dict[str, str]]`  **DEFAULT:** `None` |
| `additional_args` | Additional arguments to be passed to Playwright's context as additional settings, and it takes higher priority than Scrapling's settings.  **TYPE:** `Optional[Dict]`  **DEFAULT:** `None` |
| `session_id` | Optional session ID from open_session. If provided, reuses the existing browser session instead of creating a new one.  **TYPE:** `Optional[str]`  **DEFAULT:** `None` |

Source code in `scrapling/core/ai.py`

|  |  |
| --- | --- |
| ``` 587 588 589 590 591 592 593 594 595 596 597 598 599 600 601 602 603 604 605 606 607 608 609 610 611 612 613 614 615 616 617 618 619 620 621 622 623 624 625 626 627 628 629 630 631 632 633 634 635 636 637 638 639 640 641 642 643 644 645 646 647 648 649 650 651 652 653 654 655 656 657 658 659 660 661 662 663 664 665 666 667 668 669 670 671 672 673 674 675 676 677 678 679 680 681 682 ``` | ``` async def stealthy_fetch(     self,     url: str,     extraction_type: extraction_types = "markdown",     css_selector: Optional[str] = None,     main_content_only: bool = True,     headless: bool = True,  # noqa: F821     google_search: bool = True,     real_chrome: bool = False,     wait: int | float = 0,     proxy: Optional[str | Dict[str, str]] = None,     timezone_id: str | None = None,     locale: str | None = None,     extra_headers: Optional[Dict[str, str]] = None,     useragent: Optional[str] = None,     hide_canvas: bool = False,     cdp_url: Optional[str] = None,     timeout: int | float = 30000,     disable_resources: bool = False,     wait_selector: Optional[str] = None,     cookies: Sequence[SetCookieParam] | None = None,     network_idle: bool = False,     wait_selector_state: SelectorWaitStates = "attached",     block_webrtc: bool = False,     allow_webgl: bool = True,     solve_cloudflare: bool = False,     additional_args: Optional[Dict] = None,     session_id: Optional[str] = None, ) -> ResponseModel:     """Use the stealthy fetcher to fetch a URL and return a structured output of the result.     Note: This is the only suitable fetcher for high protection levels.     Note: If the `css_selector` resolves to more than one element, all the elements will be returned.     Note: If a `session_id` is provided (from open_session), the browser session will be reused instead of creating a new one.         When using a session, browser-level params (headless, proxy, locale, etc.) are ignored since they were set at session creation time.      :param url: The URL to request.     :param extraction_type: The type of content to extract from the page. Defaults to "markdown". Options are:         - Markdown will convert the page content to Markdown format.         - HTML will return the raw HTML content of the page.         - Text will return the text content of the page.     :param css_selector: CSS selector to extract the content from the page. If main_content_only is True, then it will be executed on the main content of the page. Defaults to None.     :param main_content_only: Whether to extract only the main content of the page. Defaults to True. The main content here is the data inside the `<body>` tag.     :param headless: Run the browser in headless/hidden (default), or headful/visible mode.     :param disable_resources: Drop requests for unnecessary resources for a speed boost.         Requests dropped are of type `font`, `image`, `media`, `beacon`, `object`, `imageset`, `texttrack`, `websocket`, `csp_report`, and `stylesheet`.     :param useragent: Pass a useragent string to be used. Otherwise the fetcher will generate a real Useragent of the same browser and use it.     :param cookies: Set cookies for the next request.     :param solve_cloudflare: Solves all types of the Cloudflare's Turnstile/Interstitial challenges before returning the response to you.     :param allow_webgl: Enabled by default. Disabling WebGL is not recommended as many WAFs now check if WebGL is enabled.     :param network_idle: Wait for the page until there are no network connections for at least 500 ms.     :param wait: The time (milliseconds) the fetcher will wait after everything finishes before closing the page and returning the ` Response ` object.     :param timeout: The timeout in milliseconds that is used in all operations and waits through the page. The default is 30,000     :param wait_selector: Wait for a specific CSS selector to be in a specific state.     :param timezone_id: Changes the timezone of the browser. Defaults to the system timezone.     :param locale: Specify user locale, for example, `en-GB`, `de-DE`, etc. Locale will affect navigator.language value, Accept-Language request header value as well as number and date formatting         rules. Defaults to the system default locale.     :param wait_selector_state: The state to wait for the selector given with `wait_selector`. The default state is `attached`.     :param real_chrome: If you have a Chrome browser installed on your device, enable this, and the Fetcher will launch an instance of your browser and use it.     :param hide_canvas: Add random noise to canvas operations to prevent fingerprinting.     :param block_webrtc: Forces WebRTC to respect proxy settings to prevent local IP address leak.     :param cdp_url: Instead of launching a new browser instance, connect to this CDP URL to control real browsers through CDP.     :param google_search: Enabled by default, Scrapling will set a Google referer header.     :param extra_headers: A dictionary of extra headers to add to the request. _The referer set by `google_search` takes priority over the referer set here if used together._     :param proxy: The proxy to be used with requests, it can be a string or a dictionary with the keys 'server', 'username', and 'password' only.     :param additional_args: Additional arguments to be passed to Playwright's context as additional settings, and it takes higher priority than Scrapling's settings.     :param session_id: Optional session ID from open_session. If provided, reuses the existing browser session instead of creating a new one.     """     results = await self.bulk_stealthy_fetch(         urls=[url],         extraction_type=extraction_type,         css_selector=css_selector,         main_content_only=main_content_only,         headless=headless,         google_search=google_search,         real_chrome=real_chrome,         wait=wait,         proxy=proxy,         timezone_id=timezone_id,         locale=locale,         extra_headers=extra_headers,         useragent=useragent,         hide_canvas=hide_canvas,         cdp_url=cdp_url,         timeout=timeout,         disable_resources=disable_resources,         wait_selector=wait_selector,         cookies=cookies,         network_idle=network_idle,         wait_selector_state=wait_selector_state,         block_webrtc=block_webrtc,         allow_webgl=allow_webgl,         solve_cloudflare=solve_cloudflare,         additional_args=additional_args,         session_id=session_id,     )     return results[0] ``` |

### bulk_stealthy_fetch `async` [¶](#scrapling.core.ai.ScraplingMCPServer.bulk_stealthy_fetch "Permanent link")

```
bulk_stealthy_fetch(
    urls,
    extraction_type="markdown",
    css_selector=None,
    main_content_only=True,
    headless=True,
    google_search=True,
    real_chrome=False,
    wait=0,
    proxy=None,
    timezone_id=None,
    locale=None,
    extra_headers=None,
    useragent=None,
    hide_canvas=False,
    cdp_url=None,
    timeout=30000,
    disable_resources=False,
    wait_selector=None,
    cookies=None,
    network_idle=False,
    wait_selector_state="attached",
    block_webrtc=False,
    allow_webgl=True,
    solve_cloudflare=False,
    additional_args=None,
    session_id=None,
)
```

Use the stealthy fetcher to fetch a group of URLs at the same time, and for each page return a structured output of the result.
Note: This is the only suitable fetcher for high protection levels.
Note: If the `css_selector` resolves to more than one element, all the elements will be returned.
Note: If a `session_id` is provided (from open_session), the browser session will be reused instead of creating a new one.
When using a session, browser-level params (headless, proxy, locale, etc.) are ignored since they were set at session creation time.

| PARAMETER | DESCRIPTION |
| --- | --- |
| `urls` | A list of the URLs to request.  **TYPE:** `List[str]` |
| `extraction_type` | The type of content to extract from the page. Defaults to "markdown". Options are: - Markdown will convert the page content to Markdown format. - HTML will return the raw HTML content of the page. - Text will return the text content of the page.  **TYPE:** `extraction_types`  **DEFAULT:** `'markdown'` |
| `css_selector` | CSS selector to extract the content from the page. If main_content_only is True, then it will be executed on the main content of the page. Defaults to None.  **TYPE:** `Optional[str]`  **DEFAULT:** `None` |
| `main_content_only` | Whether to extract only the main content of the page. Defaults to True. The main content here is the data inside the `<body>` tag.  **TYPE:** `bool`  **DEFAULT:** `True` |
| `headless` | Run the browser in headless/hidden (default), or headful/visible mode.  **TYPE:** `bool`  **DEFAULT:** `True` |
| `disable_resources` | Drop requests for unnecessary resources for a speed boost. Requests dropped are of type `font`, `image`, `media`, `beacon`, `object`, `imageset`, `texttrack`, `websocket`, `csp_report`, and `stylesheet`.  **TYPE:** `bool`  **DEFAULT:** `False` |
| `useragent` | Pass a useragent string to be used. Otherwise the fetcher will generate a real Useragent of the same browser and use it.  **TYPE:** `Optional[str]`  **DEFAULT:** `None` |
| `cookies` | Set cookies for the next request.  **TYPE:** `Sequence[SetCookieParam] | None`  **DEFAULT:** `None` |
| `solve_cloudflare` | Solves all types of the Cloudflare's Turnstile/Interstitial challenges before returning the response to you.  **TYPE:** `bool`  **DEFAULT:** `False` |
| `allow_webgl` | Enabled by default. Disabling WebGL is not recommended as many WAFs now check if WebGL is enabled.  **TYPE:** `bool`  **DEFAULT:** `True` |
| `network_idle` | Wait for the page until there are no network connections for at least 500 ms.  **TYPE:** `bool`  **DEFAULT:** `False` |
| `wait` | The time (milliseconds) the fetcher will wait after everything finishes before closing the page and returning the `Response` object.  **TYPE:** `int | float`  **DEFAULT:** `0` |
| `timeout` | The timeout in milliseconds that is used in all operations and waits through the page. The default is 30,000  **TYPE:** `int | float`  **DEFAULT:** `30000` |
| `wait_selector` | Wait for a specific CSS selector to be in a specific state.  **TYPE:** `Optional[str]`  **DEFAULT:** `None` |
| `timezone_id` | Changes the timezone of the browser. Defaults to the system timezone.  **TYPE:** `str | None`  **DEFAULT:** `None` |
| `locale` | Specify user locale, for example, `en-GB`, `de-DE`, etc. Locale will affect navigator.language value, Accept-Language request header value as well as number and date formatting rules. Defaults to the system default locale.  **TYPE:** `str | None`  **DEFAULT:** `None` |
| `wait_selector_state` | The state to wait for the selector given with `wait_selector`. The default state is `attached`.  **TYPE:** `SelectorWaitStates`  **DEFAULT:** `'attached'` |
| `real_chrome` | If you have a Chrome browser installed on your device, enable this, and the Fetcher will launch an instance of your browser and use it.  **TYPE:** `bool`  **DEFAULT:** `False` |
| `hide_canvas` | Add random noise to canvas operations to prevent fingerprinting.  **TYPE:** `bool`  **DEFAULT:** `False` |
| `block_webrtc` | Forces WebRTC to respect proxy settings to prevent local IP address leak.  **TYPE:** `bool`  **DEFAULT:** `False` |
| `cdp_url` | Instead of launching a new browser instance, connect to this CDP URL to control real browsers through CDP.  **TYPE:** `Optional[str]`  **DEFAULT:** `None` |
| `google_search` | Enabled by default, Scrapling will set a Google referer header.  **TYPE:** `bool`  **DEFAULT:** `True` |
| `extra_headers` | A dictionary of extra headers to add to the request. *The referer set by `google_search` takes priority over the referer set here if used together.*  **TYPE:** `Optional[Dict[str, str]]`  **DEFAULT:** `None` |
| `proxy` | The proxy to be used with requests, it can be a string or a dictionary with the keys 'server', 'username', and 'password' only.  **TYPE:** `Optional[str | Dict[str, str]]`  **DEFAULT:** `None` |
| `additional_args` | Additional arguments to be passed to Playwright's context as additional settings, and it takes higher priority than Scrapling's settings.  **TYPE:** `Optional[Dict]`  **DEFAULT:** `None` |
| `session_id` | Optional session ID from open_session. If provided, reuses the existing browser session instead of creating a new one.  **TYPE:** `Optional[str]`  **DEFAULT:** `None` |

Source code in `scrapling/core/ai.py`

|  |  |
| --- | --- |
| ``` 684 685 686 687 688 689 690 691 692 693 694 695 696 697 698 699 700 701 702 703 704 705 706 707 708 709 710 711 712 713 714 715 716 717 718 719 720 721 722 723 724 725 726 727 728 729 730 731 732 733 734 735 736 737 738 739 740 741 742 743 744 745 746 747 748 749 750 751 752 753 754 755 756 757 758 759 760 761 762 763 764 765 766 767 768 769 770 771 772 773 774 775 776 777 778 779 780 781 782 783 784 785 786 787 788 789 790 791 792 793 794 795 796 797 ``` | ``` async def bulk_stealthy_fetch(     self,     urls: List[str],     extraction_type: extraction_types = "markdown",     css_selector: Optional[str] = None,     main_content_only: bool = True,     headless: bool = True,  # noqa: F821     google_search: bool = True,     real_chrome: bool = False,     wait: int | float = 0,     proxy: Optional[str | Dict[str, str]] = None,     timezone_id: str | None = None,     locale: str | None = None,     extra_headers: Optional[Dict[str, str]] = None,     useragent: Optional[str] = None,     hide_canvas: bool = False,     cdp_url: Optional[str] = None,     timeout: int | float = 30000,     disable_resources: bool = False,     wait_selector: Optional[str] = None,     cookies: Sequence[SetCookieParam] | None = None,     network_idle: bool = False,     wait_selector_state: SelectorWaitStates = "attached",     block_webrtc: bool = False,     allow_webgl: bool = True,     solve_cloudflare: bool = False,     additional_args: Optional[Dict] = None,     session_id: Optional[str] = None, ) -> List[ResponseModel]:     """Use the stealthy fetcher to fetch a group of URLs at the same time, and for each page return a structured output of the result.     Note: This is the only suitable fetcher for high protection levels.     Note: If the `css_selector` resolves to more than one element, all the elements will be returned.     Note: If a `session_id` is provided (from open_session), the browser session will be reused instead of creating a new one.         When using a session, browser-level params (headless, proxy, locale, etc.) are ignored since they were set at session creation time.      :param urls: A list of the URLs to request.     :param extraction_type: The type of content to extract from the page. Defaults to "markdown". Options are:         - Markdown will convert the page content to Markdown format.         - HTML will return the raw HTML content of the page.         - Text will return the text content of the page.     :param css_selector: CSS selector to extract the content from the page. If main_content_only is True, then it will be executed on the main content of the page. Defaults to None.     :param main_content_only: Whether to extract only the main content of the page. Defaults to True. The main content here is the data inside the `<body>` tag.     :param headless: Run the browser in headless/hidden (default), or headful/visible mode.     :param disable_resources: Drop requests for unnecessary resources for a speed boost.         Requests dropped are of type `font`, `image`, `media`, `beacon`, `object`, `imageset`, `texttrack`, `websocket`, `csp_report`, and `stylesheet`.     :param useragent: Pass a useragent string to be used. Otherwise the fetcher will generate a real Useragent of the same browser and use it.     :param cookies: Set cookies for the next request.     :param solve_cloudflare: Solves all types of the Cloudflare's Turnstile/Interstitial challenges before returning the response to you.     :param allow_webgl: Enabled by default. Disabling WebGL is not recommended as many WAFs now check if WebGL is enabled.     :param network_idle: Wait for the page until there are no network connections for at least 500 ms.     :param wait: The time (milliseconds) the fetcher will wait after everything finishes before closing the page and returning the ` Response ` object.     :param timeout: The timeout in milliseconds that is used in all operations and waits through the page. The default is 30,000     :param wait_selector: Wait for a specific CSS selector to be in a specific state.     :param timezone_id: Changes the timezone of the browser. Defaults to the system timezone.     :param locale: Specify user locale, for example, `en-GB`, `de-DE`, etc. Locale will affect navigator.language value, Accept-Language request header value as well as number and date formatting         rules. Defaults to the system default locale.     :param wait_selector_state: The state to wait for the selector given with `wait_selector`. The default state is `attached`.     :param real_chrome: If you have a Chrome browser installed on your device, enable this, and the Fetcher will launch an instance of your browser and use it.     :param hide_canvas: Add random noise to canvas operations to prevent fingerprinting.     :param block_webrtc: Forces WebRTC to respect proxy settings to prevent local IP address leak.     :param cdp_url: Instead of launching a new browser instance, connect to this CDP URL to control real browsers through CDP.     :param google_search: Enabled by default, Scrapling will set a Google referer header.     :param extra_headers: A dictionary of extra headers to add to the request. _The referer set by `google_search` takes priority over the referer set here if used together._     :param proxy: The proxy to be used with requests, it can be a string or a dictionary with the keys 'server', 'username', and 'password' only.     :param additional_args: Additional arguments to be passed to Playwright's context as additional settings, and it takes higher priority than Scrapling's settings.     :param session_id: Optional session ID from open_session. If provided, reuses the existing browser session instead of creating a new one.     """     if session_id:         entry = self._get_session(session_id, "stealthy")         tasks = [             entry.session.fetch(                 url,                 wait=wait,                 timeout=timeout,                 google_search=google_search,                 extra_headers=extra_headers,                 disable_resources=disable_resources,                 wait_selector=wait_selector,                 wait_selector_state=wait_selector_state,                 network_idle=network_idle,                 proxy=proxy,                 solve_cloudflare=solve_cloudflare,             )             for url in urls         ]         responses = await gather(*tasks)     else:         async with AsyncStealthySession(             wait=wait,             proxy=proxy,             locale=locale,             cdp_url=cdp_url,             timeout=timeout,             cookies=cookies,             headless=headless,             useragent=useragent,             timezone_id=timezone_id,             real_chrome=real_chrome,             hide_canvas=hide_canvas,             allow_webgl=allow_webgl,             network_idle=network_idle,             block_webrtc=block_webrtc,             wait_selector=wait_selector,             google_search=google_search,             extra_headers=extra_headers,             additional_args=additional_args,             solve_cloudflare=solve_cloudflare,             disable_resources=disable_resources,             wait_selector_state=wait_selector_state,         ) as session:             tasks = [session.fetch(url) for url in urls]             responses = await gather(*tasks)      return [_translate_response(page, extraction_type, css_selector, main_content_only) for page in responses] ``` |

### serve [¶](#scrapling.core.ai.ScraplingMCPServer.serve "Permanent link")

```
serve(http, host, port)
```

Serve the MCP server.

Source code in `scrapling/core/ai.py`

|  |  |
| --- | --- |
| ``` 799 800 801 802 803 804 805 806 807 808 809 810 811 812 813 814 815 816 817 818 819 820 821 822 823 824 825 826 827 ``` | ``` def serve(self, http: bool, host: str, port: int):     """Serve the MCP server."""     server = FastMCP(name="Scrapling", host=host, port=port)     # Session management tools     server.add_tool(self.open_session, title="open_session", structured_output=True)     server.add_tool(self.close_session, title="close_session", structured_output=True)     server.add_tool(self.list_sessions, title="list_sessions", structured_output=True)     # HTTP tools     server.add_tool(self.get, title="get", description=self.get.__doc__, structured_output=True)     server.add_tool(self.bulk_get, title="bulk_get", description=self.bulk_get.__doc__, structured_output=True)     # Dynamic browser tools     server.add_tool(self.fetch, title="fetch", description=self.fetch.__doc__, structured_output=True)     server.add_tool(         self.bulk_fetch, title="bulk_fetch", description=self.bulk_fetch.__doc__, structured_output=True     )     # Stealthy browser tools     server.add_tool(         self.stealthy_fetch,         title="stealthy_fetch",         description=self.stealthy_fetch.__doc__,         structured_output=True,     )     server.add_tool(         self.bulk_stealthy_fetch,         title="bulk_stealthy_fetch",         description=self.bulk_stealthy_fetch.__doc__,         structured_output=True,     )     server.run(transport="stdio" if not http else "streamable-http") ``` |

Was this page helpful?

Thanks for your feedback!

Thanks for your feedback! Help us improve this page by
[opening a documentation issue](https://github.com/D4Vinci/Scrapling/issues/new?template=04-docs_issue.yml).


---
## Source: https://scrapling.readthedocs.io/en/latest/api-reference/custom-types.html
---

# Custom Types API Reference[¶](#custom-types-api-reference "Permanent link")

Here's the reference information for all custom types of classes Scrapling implemented, with all their parameters, attributes, and methods.

You can import all of them directly like below:

```
from scrapling.core.custom_types import TextHandler, TextHandlers, AttributesHandler
```

## scrapling.core.custom_types.TextHandler [¶](#scrapling.core.custom_types.TextHandler "Permanent link")

Bases: `str`

```
              flowchart TD
              scrapling.core.custom_types.TextHandler[TextHandler]

              

              click scrapling.core.custom_types.TextHandler href "" "scrapling.core.custom_types.TextHandler"
```

Extends standard Python string by adding more functionality

### __slots__ `class-attribute` `instance-attribute` [¶](#scrapling.core.custom_types.TextHandler.__slots__ "Permanent link")

```
__slots__ = ()
```

### extract `class-attribute` `instance-attribute` [¶](#scrapling.core.custom_types.TextHandler.extract "Permanent link")

```
extract = getall
```

### extract_first `class-attribute` `instance-attribute` [¶](#scrapling.core.custom_types.TextHandler.extract_first "Permanent link")

```
extract_first = get
```

### __getitem__ [¶](#scrapling.core.custom_types.TextHandler.__getitem__ "Permanent link")

```
__getitem__(key)
```

Source code in `scrapling/core/custom_types.py`

|  |  |
| --- | --- |
| ``` 34 35 36 ``` | ``` def __getitem__(self, key: SupportsIndex | slice) -> "TextHandler":  # pragma: no cover     lst = super().__getitem__(key)     return TextHandler(lst) ``` |

### split [¶](#scrapling.core.custom_types.TextHandler.split "Permanent link")

```
split(sep=None, maxsplit=-1)
```

Source code in `scrapling/core/custom_types.py`

|  |  |
| --- | --- |
| ``` 38 39 ``` | ``` def split(self, sep: str | None = None, maxsplit: SupportsIndex = -1) -> list[Any]:  # pragma: no cover     return TextHandlers([TextHandler(s) for s in super().split(sep, maxsplit)]) ``` |

### strip [¶](#scrapling.core.custom_types.TextHandler.strip "Permanent link")

```
strip(chars=None)
```

Source code in `scrapling/core/custom_types.py`

|  |  |
| --- | --- |
| ``` 41 42 ``` | ``` def strip(self, chars: str | None = None) -> Union[str, "TextHandler"]:  # pragma: no cover     return TextHandler(super().strip(chars)) ``` |

### lstrip [¶](#scrapling.core.custom_types.TextHandler.lstrip "Permanent link")

```
lstrip(chars=None)
```

Source code in `scrapling/core/custom_types.py`

|  |  |
| --- | --- |
| ``` 44 45 ``` | ``` def lstrip(self, chars: str | None = None) -> Union[str, "TextHandler"]:  # pragma: no cover     return TextHandler(super().lstrip(chars)) ``` |

### rstrip [¶](#scrapling.core.custom_types.TextHandler.rstrip "Permanent link")

```
rstrip(chars=None)
```

Source code in `scrapling/core/custom_types.py`

|  |  |
| --- | --- |
| ``` 47 48 ``` | ``` def rstrip(self, chars: str | None = None) -> Union[str, "TextHandler"]:  # pragma: no cover     return TextHandler(super().rstrip(chars)) ``` |

### capitalize [¶](#scrapling.core.custom_types.TextHandler.capitalize "Permanent link")

```
capitalize()
```

Source code in `scrapling/core/custom_types.py`

|  |  |
| --- | --- |
| ``` 50 51 ``` | ``` def capitalize(self) -> Union[str, "TextHandler"]:  # pragma: no cover     return TextHandler(super().capitalize()) ``` |

### casefold [¶](#scrapling.core.custom_types.TextHandler.casefold "Permanent link")

```
casefold()
```

Source code in `scrapling/core/custom_types.py`

|  |  |
| --- | --- |
| ``` 53 54 ``` | ``` def casefold(self) -> Union[str, "TextHandler"]:  # pragma: no cover     return TextHandler(super().casefold()) ``` |

### center [¶](#scrapling.core.custom_types.TextHandler.center "Permanent link")

```
center(width, fillchar=' ')
```

Source code in `scrapling/core/custom_types.py`

|  |  |
| --- | --- |
| ``` 56 57 ``` | ``` def center(self, width: SupportsIndex, fillchar: str = " ") -> Union[str, "TextHandler"]:  # pragma: no cover     return TextHandler(super().center(width, fillchar)) ``` |

### expandtabs [¶](#scrapling.core.custom_types.TextHandler.expandtabs "Permanent link")

```
expandtabs(tabsize=8)
```

Source code in `scrapling/core/custom_types.py`

|  |  |
| --- | --- |
| ``` 59 60 ``` | ``` def expandtabs(self, tabsize: SupportsIndex = 8) -> Union[str, "TextHandler"]:  # pragma: no cover     return TextHandler(super().expandtabs(tabsize)) ``` |

### format [¶](#scrapling.core.custom_types.TextHandler.format "Permanent link")

```
format(*args, **kwargs)
```

Source code in `scrapling/core/custom_types.py`

|  |  |
| --- | --- |
| ``` 62 63 ``` | ``` def format(self, *args: object, **kwargs: object) -> Union[str, "TextHandler"]:  # pragma: no cover     return TextHandler(super().format(*args, **kwargs)) ``` |

### format_map [¶](#scrapling.core.custom_types.TextHandler.format_map "Permanent link")

```
format_map(mapping)
```

Source code in `scrapling/core/custom_types.py`

|  |  |
| --- | --- |
| ``` 65 66 ``` | ``` def format_map(self, mapping) -> Union[str, "TextHandler"]:  # pragma: no cover     return TextHandler(super().format_map(mapping)) ``` |

### join [¶](#scrapling.core.custom_types.TextHandler.join "Permanent link")

```
join(iterable)
```

Source code in `scrapling/core/custom_types.py`

|  |  |
| --- | --- |
| ``` 68 69 ``` | ``` def join(self, iterable: Iterable[str]) -> Union[str, "TextHandler"]:  # pragma: no cover     return TextHandler(super().join(iterable)) ``` |

### ljust [¶](#scrapling.core.custom_types.TextHandler.ljust "Permanent link")

```
ljust(width, fillchar=' ')
```

Source code in `scrapling/core/custom_types.py`

|  |  |
| --- | --- |
| ``` 71 72 ``` | ``` def ljust(self, width: SupportsIndex, fillchar: str = " ") -> Union[str, "TextHandler"]:  # pragma: no cover     return TextHandler(super().ljust(width, fillchar)) ``` |

### rjust [¶](#scrapling.core.custom_types.TextHandler.rjust "Permanent link")

```
rjust(width, fillchar=' ')
```

Source code in `scrapling/core/custom_types.py`

|  |  |
| --- | --- |
| ``` 74 75 ``` | ``` def rjust(self, width: SupportsIndex, fillchar: str = " ") -> Union[str, "TextHandler"]:  # pragma: no cover     return TextHandler(super().rjust(width, fillchar)) ``` |

### swapcase [¶](#scrapling.core.custom_types.TextHandler.swapcase "Permanent link")

```
swapcase()
```

Source code in `scrapling/core/custom_types.py`

|  |  |
| --- | --- |
| ``` 77 78 ``` | ``` def swapcase(self) -> Union[str, "TextHandler"]:  # pragma: no cover     return TextHandler(super().swapcase()) ``` |

### title [¶](#scrapling.core.custom_types.TextHandler.title "Permanent link")

```
title()
```

Source code in `scrapling/core/custom_types.py`

|  |  |
| --- | --- |
| ``` 80 81 ``` | ``` def title(self) -> Union[str, "TextHandler"]:  # pragma: no cover     return TextHandler(super().title()) ``` |

### translate [¶](#scrapling.core.custom_types.TextHandler.translate "Permanent link")

```
translate(table)
```

Source code in `scrapling/core/custom_types.py`

|  |  |
| --- | --- |
| ``` 83 84 ``` | ``` def translate(self, table) -> Union[str, "TextHandler"]:  # pragma: no cover     return TextHandler(super().translate(table)) ``` |

### zfill [¶](#scrapling.core.custom_types.TextHandler.zfill "Permanent link")

```
zfill(width)
```

Source code in `scrapling/core/custom_types.py`

|  |  |
| --- | --- |
| ``` 86 87 ``` | ``` def zfill(self, width: SupportsIndex) -> Union[str, "TextHandler"]:  # pragma: no cover     return TextHandler(super().zfill(width)) ``` |

### replace [¶](#scrapling.core.custom_types.TextHandler.replace "Permanent link")

```
replace(old, new, count=-1)
```

Source code in `scrapling/core/custom_types.py`

|  |  |
| --- | --- |
| ``` 89 90 ``` | ``` def replace(self, old: str, new: str, count: SupportsIndex = -1) -> Union[str, "TextHandler"]:     return TextHandler(super().replace(old, new, count)) ``` |

### upper [¶](#scrapling.core.custom_types.TextHandler.upper "Permanent link")

```
upper()
```

Source code in `scrapling/core/custom_types.py`

|  |  |
| --- | --- |
| ``` 92 93 ``` | ``` def upper(self) -> Union[str, "TextHandler"]:     return TextHandler(super().upper()) ``` |

### lower [¶](#scrapling.core.custom_types.TextHandler.lower "Permanent link")

```
lower()
```

Source code in `scrapling/core/custom_types.py`

|  |  |
| --- | --- |
| ``` 95 96 ``` | ``` def lower(self) -> Union[str, "TextHandler"]:     return TextHandler(super().lower()) ``` |

### sort [¶](#scrapling.core.custom_types.TextHandler.sort "Permanent link")

```
sort(reverse=False)
```

Return a sorted version of the string

Source code in `scrapling/core/custom_types.py`

|  |  |
| --- | --- |
| ``` 100 101 102 ``` | ``` def sort(self, reverse: bool = False) -> Union[str, "TextHandler"]:     """Return a sorted version of the string"""     return self.__class__("".join(sorted(self, reverse=reverse))) ``` |

### clean [¶](#scrapling.core.custom_types.TextHandler.clean "Permanent link")

```
clean(remove_entities=False)
```

Return a new version of the string after removing all white spaces and consecutive spaces

Source code in `scrapling/core/custom_types.py`

|  |  |
| --- | --- |
| ``` 104 105 106 107 108 109 ``` | ``` def clean(self, remove_entities=False) -> Union[str, "TextHandler"]:     """Return a new version of the string after removing all white spaces and consecutive spaces"""     data = self.translate(__CLEANING_TABLE__)     if remove_entities:         data = _replace_entities(data)     return self.__class__(__CONSECUTIVE_SPACES_REGEX__.sub(" ", data).strip()) ``` |

### get [¶](#scrapling.core.custom_types.TextHandler.get "Permanent link")

```
get(default=None)
```

Source code in `scrapling/core/custom_types.py`

|  |  |
| --- | --- |
| ``` 112 113 ``` | ``` def get(self, default=None):  # pragma: no cover     return self ``` |

### getall [¶](#scrapling.core.custom_types.TextHandler.getall "Permanent link")

```
getall()
```

Source code in `scrapling/core/custom_types.py`

|  |  |
| --- | --- |
| ``` 115 116 ``` | ``` def getall(self):  # pragma: no cover     return self ``` |

### json [¶](#scrapling.core.custom_types.TextHandler.json "Permanent link")

```
json()
```

Return JSON response if the response is jsonable otherwise throw error

Source code in `scrapling/core/custom_types.py`

|  |  |
| --- | --- |
| ``` 121 122 123 124 125 ``` | ``` def json(self) -> Dict:     """Return JSON response if the response is jsonable otherwise throw error"""     # Using str function as a workaround for orjson issue with subclasses of str.     # Check this out: https://github.com/ijl/orjson/issues/445     return loads(str(self)) ``` |

### re [¶](#scrapling.core.custom_types.TextHandler.re "Permanent link")

```
re(
    regex,
    replace_entities=True,
    clean_match=False,
    case_sensitive=True,
    check_match=False,
)
```

Apply the given regex to the current text and return a list of strings with the matches.

| PARAMETER | DESCRIPTION |
| --- | --- |
| `regex` | Can be either a compiled regular expression or a string.  **TYPE:** `str | Pattern` |
| `replace_entities` | If enabled character entity references are replaced by their corresponding character  **TYPE:** `bool`  **DEFAULT:** `True` |
| `clean_match` | If enabled, this will ignore all whitespaces and consecutive spaces while matching  **TYPE:** `bool`  **DEFAULT:** `False` |
| `case_sensitive` | If disabled, function will set the regex to ignore the letters-case while compiling it  **TYPE:** `bool`  **DEFAULT:** `True` |
| `check_match` | Used to quickly check if this regex matches or not without any operations on the results  **TYPE:** `bool`  **DEFAULT:** `False` |

Source code in `scrapling/core/custom_types.py`

|  |  |
| --- | --- |
| ``` 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 ``` | ``` def re(     self,     regex: str | Pattern,     replace_entities: bool = True,     clean_match: bool = False,     case_sensitive: bool = True,     check_match: bool = False, ) -> Union["TextHandlers", bool]:     """Apply the given regex to the current text and return a list of strings with the matches.      :param regex: Can be either a compiled regular expression or a string.     :param replace_entities: If enabled character entity references are replaced by their corresponding character     :param clean_match: If enabled, this will ignore all whitespaces and consecutive spaces while matching     :param case_sensitive: If disabled, function will set the regex to ignore the letters-case while compiling it     :param check_match: Used to quickly check if this regex matches or not without any operations on the results      """     if isinstance(regex, str):         if case_sensitive:             regex = re_compile(regex, UNICODE)         else:             regex = re_compile(regex, flags=UNICODE | IGNORECASE)      input_text = self.clean() if clean_match else self     results = regex.findall(input_text)     if check_match:         return bool(results)      if all(_is_iterable(res) for res in results):         results = flatten(results)      if not replace_entities:         return TextHandlers([TextHandler(string) for string in results])      return TextHandlers([TextHandler(_replace_entities(s)) for s in results]) ``` |

### re_first [¶](#scrapling.core.custom_types.TextHandler.re_first "Permanent link")

```
re_first(
    regex,
    default=None,
    replace_entities=True,
    clean_match=False,
    case_sensitive=True,
)
```

Apply the given regex to text and return the first match if found, otherwise return the default value.

| PARAMETER | DESCRIPTION |
| --- | --- |
| `regex` | Can be either a compiled regular expression or a string.  **TYPE:** `str | Pattern` |
| `default` | The default value to be returned if there is no match  **TYPE:** `Any`  **DEFAULT:** `None` |
| `replace_entities` | If enabled character entity references are replaced by their corresponding character  **TYPE:** `bool`  **DEFAULT:** `True` |
| `clean_match` | If enabled, this will ignore all whitespaces and consecutive spaces while matching  **TYPE:** `bool`  **DEFAULT:** `False` |
| `case_sensitive` | If disabled, function will set the regex to ignore the letters-case while compiling it  **TYPE:** `bool`  **DEFAULT:** `True` |

Source code in `scrapling/core/custom_types.py`

|  |  |
| --- | --- |
| ``` 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200 201 202 203 204 205 206 207 ``` | ``` def re_first(     self,     regex: str | Pattern,     default: Any = None,     replace_entities: bool = True,     clean_match: bool = False,     case_sensitive: bool = True, ) -> "TextHandler":     """Apply the given regex to text and return the first match if found, otherwise return the default value.      :param regex: Can be either a compiled regular expression or a string.     :param default: The default value to be returned if there is no match     :param replace_entities: If enabled character entity references are replaced by their corresponding character     :param clean_match: If enabled, this will ignore all whitespaces and consecutive spaces while matching     :param case_sensitive: If disabled, function will set the regex to ignore the letters-case while compiling it      """     result = self.re(         regex,         replace_entities,         clean_match=clean_match,         case_sensitive=case_sensitive,     )     return result[0] if result else default ``` |

## scrapling.core.custom_types.TextHandlers [¶](#scrapling.core.custom_types.TextHandlers "Permanent link")

Bases: `List[TextHandler]`

```
              flowchart TD
              scrapling.core.custom_types.TextHandlers[TextHandlers]

              

              click scrapling.core.custom_types.TextHandlers href "" "scrapling.core.custom_types.TextHandlers"
```

The :class:`TextHandlers` class is a subclass of the builtin `List` class, which provides a few additional methods.

### __slots__ `class-attribute` `instance-attribute` [¶](#scrapling.core.custom_types.TextHandlers.__slots__ "Permanent link")

```
__slots__ = ()
```

### extract_first `class-attribute` `instance-attribute` [¶](#scrapling.core.custom_types.TextHandlers.extract_first "Permanent link")

```
extract_first = get
```

### getall `class-attribute` `instance-attribute` [¶](#scrapling.core.custom_types.TextHandlers.getall "Permanent link")

```
getall = extract
```

### __getitem__ [¶](#scrapling.core.custom_types.TextHandlers.__getitem__ "Permanent link")

```
__getitem__(pos)
```

Source code in `scrapling/core/custom_types.py`

|  |  |
| --- | --- |
| ``` 225 226 227 228 229 ``` | ``` def __getitem__(self, pos: SupportsIndex | slice) -> Union[TextHandler, "TextHandlers"]:     lst = super().__getitem__(pos)     if isinstance(pos, slice):         return TextHandlers(cast(List[TextHandler], lst))     return TextHandler(cast(TextHandler, lst)) ``` |

### re [¶](#scrapling.core.custom_types.TextHandlers.re "Permanent link")

```
re(
    regex,
    replace_entities=True,
    clean_match=False,
    case_sensitive=True,
)
```

Call the `.re()` method for each element in this list and return
their results flattened as TextHandlers.

| PARAMETER | DESCRIPTION |
| --- | --- |
| `regex` | Can be either a compiled regular expression or a string.  **TYPE:** `str | Pattern` |
| `replace_entities` | If enabled character entity references are replaced by their corresponding character  **TYPE:** `bool`  **DEFAULT:** `True` |
| `clean_match` | if enabled, this will ignore all whitespaces and consecutive spaces while matching  **TYPE:** `bool`  **DEFAULT:** `False` |
| `case_sensitive` | if disabled, the function will set the regex to ignore the letters-case while compiling it  **TYPE:** `bool`  **DEFAULT:** `True` |

Source code in `scrapling/core/custom_types.py`

|  |  |
| --- | --- |
| ``` 231 232 233 234 235 236 237 238 239 240 241 242 243 244 245 246 247 ``` | ``` def re(     self,     regex: str | Pattern,     replace_entities: bool = True,     clean_match: bool = False,     case_sensitive: bool = True, ) -> "TextHandlers":     """Call the ``.re()`` method for each element in this list and return     their results flattened as TextHandlers.      :param regex: Can be either a compiled regular expression or a string.     :param replace_entities: If enabled character entity references are replaced by their corresponding character     :param clean_match: if enabled, this will ignore all whitespaces and consecutive spaces while matching     :param case_sensitive: if disabled, the function will set the regex to ignore the letters-case while compiling it     """     results = [n.re(regex, replace_entities, clean_match, case_sensitive) for n in self]     return TextHandlers(flatten(results)) ``` |

### re_first [¶](#scrapling.core.custom_types.TextHandlers.re_first "Permanent link")

```
re_first(
    regex,
    default=None,
    replace_entities=True,
    clean_match=False,
    case_sensitive=True,
)
```

Call the `.re_first()` method for each element in this list and return
the first result or the default value otherwise.

| PARAMETER | DESCRIPTION |
| --- | --- |
| `regex` | Can be either a compiled regular expression or a string.  **TYPE:** `str | Pattern` |
| `default` | The default value to be returned if there is no match  **TYPE:** `Any`  **DEFAULT:** `None` |
| `replace_entities` | If enabled character entity references are replaced by their corresponding character  **TYPE:** `bool`  **DEFAULT:** `True` |
| `clean_match` | If enabled, this will ignore all whitespaces and consecutive spaces while matching  **TYPE:** `bool`  **DEFAULT:** `False` |
| `case_sensitive` | If disabled, function will set the regex to ignore the letters-case while compiling it  **TYPE:** `bool`  **DEFAULT:** `True` |

Source code in `scrapling/core/custom_types.py`

|  |  |
| --- | --- |
| ``` 249 250 251 252 253 254 255 256 257 258 259 260 261 262 263 264 265 266 267 268 269 ``` | ``` def re_first(     self,     regex: str | Pattern,     default: Any = None,     replace_entities: bool = True,     clean_match: bool = False,     case_sensitive: bool = True, ) -> TextHandler:  # pragma: no cover     """Call the ``.re_first()`` method for each element in this list and return     the first result or the default value otherwise.      :param regex: Can be either a compiled regular expression or a string.     :param default: The default value to be returned if there is no match     :param replace_entities: If enabled character entity references are replaced by their corresponding character     :param clean_match: If enabled, this will ignore all whitespaces and consecutive spaces while matching     :param case_sensitive: If disabled, function will set the regex to ignore the letters-case while compiling it     """     for n in self:         for result in n.re(regex, replace_entities, clean_match, case_sensitive):             return result     return default ``` |

### get [¶](#scrapling.core.custom_types.TextHandlers.get "Permanent link")

```
get(default=None)
```

Returns the first item of the current list

| PARAMETER | DESCRIPTION |
| --- | --- |
| `default` | the default value to return if the current list is empty  **DEFAULT:** `None` |

Source code in `scrapling/core/custom_types.py`

|  |  |
| --- | --- |
| ``` 272 273 274 275 276 ``` | ``` def get(self, default=None):     """Returns the first item of the current list     :param default: the default value to return if the current list is empty     """     return self[0] if len(self) > 0 else default ``` |

### extract [¶](#scrapling.core.custom_types.TextHandlers.extract "Permanent link")

```
extract()
```

Source code in `scrapling/core/custom_types.py`

|  |  |
| --- | --- |
| ``` 278 279 ``` | ``` def extract(self):     return self ``` |

## scrapling.core.custom_types.AttributesHandler [¶](#scrapling.core.custom_types.AttributesHandler "Permanent link")

```
AttributesHandler(mapping=None, **kwargs)
```

Bases: `Mapping[str, _TextHandlerType]`

```
              flowchart TD
              scrapling.core.custom_types.AttributesHandler[AttributesHandler]

              

              click scrapling.core.custom_types.AttributesHandler href "" "scrapling.core.custom_types.AttributesHandler"
```

A read-only mapping to use instead of the standard dictionary for the speed boost, but at the same time I use it to add more functionalities.
If the standard dictionary is needed, convert this class to a dictionary with the `dict` function

Source code in `scrapling/core/custom_types.py`

|  |  |
| --- | --- |
| ``` 292 293 294 295 296 297 298 299 300 301 302 303 304 305 ``` | ``` def __init__(self, mapping: Any = None, **kwargs: Any) -> None:     mapping = (         {key: TextHandler(value) if isinstance(value, str) else value for key, value in mapping.items()}         if mapping is not None         else {}     )      if kwargs:         mapping.update(             {key: TextHandler(value) if isinstance(value, str) else value for key, value in kwargs.items()}         )      # Fastest read-only mapping type     self._data: Mapping[str, Any] = MappingProxyType(mapping) ``` |

### __slots__ `class-attribute` `instance-attribute` [¶](#scrapling.core.custom_types.AttributesHandler.__slots__ "Permanent link")

```
__slots__ = ('_data',)
```

### json_string `property` [¶](#scrapling.core.custom_types.AttributesHandler.json_string "Permanent link")

```
json_string
```

Convert current attributes to JSON bytes if the attributes are JSON serializable otherwise throws error

### get [¶](#scrapling.core.custom_types.AttributesHandler.get "Permanent link")

```
get(key, default=None)
```

Acts like the standard dictionary `.get()` method

Source code in `scrapling/core/custom_types.py`

|  |  |
| --- | --- |
| ``` 307 308 309 ``` | ``` def get(self, key: str, default: Any = None) -> _TextHandlerType:     """Acts like the standard dictionary `.get()` method"""     return self._data.get(key, default) ``` |

### search_values [¶](#scrapling.core.custom_types.AttributesHandler.search_values "Permanent link")

```
search_values(keyword, partial=False)
```

Search current attributes by values and return a dictionary of each matching item

| PARAMETER | DESCRIPTION |
| --- | --- |
| `keyword` | The keyword to search for in the attribute values  **TYPE:** `str` |
| `partial` | If True, the function will search if keyword in each value instead of perfect match  **TYPE:** `bool`  **DEFAULT:** `False` |

Source code in `scrapling/core/custom_types.py`

|  |  |
| --- | --- |
| ``` 311 312 313 314 315 316 317 318 319 320 321 322 ``` | ``` def search_values(self, keyword: str, partial: bool = False) -> Generator["AttributesHandler", None, None]:     """Search current attributes by values and return a dictionary of each matching item     :param keyword: The keyword to search for in the attribute values     :param partial: If True, the function will search if keyword in each value instead of perfect match     """     for key, value in self._data.items():         if partial:             if keyword in value:                 yield AttributesHandler({key: value})         else:             if keyword == value:                 yield AttributesHandler({key: value}) ``` |

### __getitem__ [¶](#scrapling.core.custom_types.AttributesHandler.__getitem__ "Permanent link")

```
__getitem__(key)
```

Source code in `scrapling/core/custom_types.py`

|  |  |
| --- | --- |
| ``` 329 330 ``` | ``` def __getitem__(self, key: str) -> _TextHandlerType:     return self._data[key] ``` |

### __iter__ [¶](#scrapling.core.custom_types.AttributesHandler.__iter__ "Permanent link")

```
__iter__()
```

Source code in `scrapling/core/custom_types.py`

|  |  |
| --- | --- |
| ``` 332 333 ``` | ``` def __iter__(self):     return iter(self._data) ``` |

### __len__ [¶](#scrapling.core.custom_types.AttributesHandler.__len__ "Permanent link")

```
__len__()
```

Source code in `scrapling/core/custom_types.py`

|  |  |
| --- | --- |
| ``` 335 336 ``` | ``` def __len__(self):     return len(self._data) ``` |

### __repr__ [¶](#scrapling.core.custom_types.AttributesHandler.__repr__ "Permanent link")

```
__repr__()
```

Source code in `scrapling/core/custom_types.py`

|  |  |
| --- | --- |
| ``` 338 339 ``` | ``` def __repr__(self):     return f"{self.__class__.__name__}({self._data})" ``` |

### __str__ [¶](#scrapling.core.custom_types.AttributesHandler.__str__ "Permanent link")

```
__str__()
```

Source code in `scrapling/core/custom_types.py`

|  |  |
| --- | --- |
| ``` 341 342 ``` | ``` def __str__(self):     return str(self._data) ``` |

### __contains__ [¶](#scrapling.core.custom_types.AttributesHandler.__contains__ "Permanent link")

```
__contains__(key)
```

Source code in `scrapling/core/custom_types.py`

|  |  |
| --- | --- |
| ``` 344 345 ``` | ``` def __contains__(self, key):     return key in self._data ``` |

Was this page helpful?

Thanks for your feedback!

Thanks for your feedback! Help us improve this page by
[opening a documentation issue](https://github.com/D4Vinci/Scrapling/issues/new?template=04-docs_issue.yml).


---
## Source: https://scrapling.readthedocs.io/en/latest/api-reference/response.html
---

# Response Class[¶](#response-class "Permanent link")

The `Response` class wraps HTTP responses returned by all fetchers, providing access to status, headers, body, cookies, and a `Selector` for parsing.

You can import the `Response` class like below:

```
from scrapling.engines.toolbelt.custom import Response
```

## scrapling.engines.toolbelt.custom.Response [¶](#scrapling.engines.toolbelt.custom.Response "Permanent link")

```
Response(
    url,
    content,
    status,
    reason,
    cookies,
    headers,
    request_headers,
    encoding="utf-8",
    method="GET",
    history=None,
    meta=None,
    **selector_config
)
```

Bases: `Selector`

```
              flowchart TD
              scrapling.engines.toolbelt.custom.Response[Response]
              scrapling.parser.Selector[Selector]
              scrapling.core.mixins.SelectorsGeneration[SelectorsGeneration]

                              scrapling.parser.Selector --> scrapling.engines.toolbelt.custom.Response
                                scrapling.core.mixins.SelectorsGeneration --> scrapling.parser.Selector
                



              click scrapling.engines.toolbelt.custom.Response href "" "scrapling.engines.toolbelt.custom.Response"
              click scrapling.parser.Selector href "" "scrapling.parser.Selector"
              click scrapling.core.mixins.SelectorsGeneration href "" "scrapling.core.mixins.SelectorsGeneration"
```

This class is returned by all engines as a way to unify the response type between different libraries.

| PARAMETER | DESCRIPTION |
| --- | --- |
| `status` | HTTP status code.  **TYPE:** `int` |
| `reason` | HTTP status message.  **TYPE:** `str` |
| `cookies` | Response cookies.  **TYPE:** `Tuple[Dict[str, str], ...] | Dict[str, str]` |
| `headers` | Response headers.  **TYPE:** `Dict` |
| `request_headers` | Request headers sent with the request.  **TYPE:** `Dict` |
| `history` | List of redirect responses, if any.  **TYPE:** `List | None`  **DEFAULT:** `None` |
| `meta` | Metadata dictionary (e.g., proxy used).  **TYPE:** `Dict[str, Any] | None`  **DEFAULT:** `None` |
| `request` | Associated spider Request object (set by crawler, in the spiders framework). |
| `captured_xhr` | List of captured XHR/fetch `Response` objects. Populated when `capture_xhr` is set on a browser session. |

The main class that works as a wrapper for the HTML input data. Using this class, you can search for elements
with expressions in CSS, XPath, or with simply text. Check the docs for more info.

Here we try to extend module `lxml.html.HtmlElement` while maintaining a simpler interface, We are not
inheriting from the `lxml.html.HtmlElement` because it's not pickleable, which makes a lot of reference jobs
not possible. You can test it here and see code explodes with `AssertionError: invalid Element proxy at...`.
It's an old issue with lxml, see `this entry <https://bugs.launchpad.net/lxml/+bug/736708>`

| PARAMETER | DESCRIPTION |
| --- | --- |
| `content` | HTML content as either string or bytes.  **TYPE:** `str | bytes` |
| `url` | It allows storing a URL with the HTML data for retrieving later.  **TYPE:** `str` |
| `encoding` | The encoding type that will be used in HTML parsing, default is `UTF-8`  **TYPE:** `str`  **DEFAULT:** `'utf-8'` |
| `huge_tree` | Enabled by default, should always be enabled when parsing large HTML documents. This controls the libxml2 feature that forbids parsing certain large documents to protect from possible memory exhaustion. |
| `root` | Used internally to pass etree objects instead of text/body arguments, it takes the highest priority. Don't use it unless you know what you are doing! |
| `keep_comments` | While parsing the HTML body, drop comments or not. Disabled by default for obvious reasons |
| `keep_cdata` | While parsing the HTML body, drop cdata or not. Disabled by default for cleaner HTML. |
| `adaptive` | Globally turn off the adaptive feature in all functions, this argument takes higher priority over all adaptive related arguments/functions in the class. |
| `storage` | The storage class to be passed for adaptive functionalities, see `Docs` for more info. |
| `storage_args` | A dictionary of `argument->value` pairs to be passed for the storage class. If empty, default values will be used. |

Source code in `scrapling/engines/toolbelt/custom.py`

|  |  |
| --- | --- |
| ``` 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 ``` | ``` def __init__(     self,     url: str,     content: str | bytes,     status: int,     reason: str,     cookies: Tuple[Dict[str, str], ...] | Dict[str, str],     headers: Dict,     request_headers: Dict,     encoding: str = "utf-8",     method: str = "GET",     history: List | None = None,     meta: Dict[str, Any] | None = None,     **selector_config: Any, ):     if isinstance(content, str):         content = content.encode("utf-8")      adaptive_domain: str = cast(str, selector_config.pop("adaptive_domain", ""))     self.status = status     self.reason = reason     self.cookies = cookies     self.headers = headers     self.request_headers = request_headers     self.history = history or []     super().__init__(         content=content,         url=adaptive_domain or url,         encoding=encoding,         **selector_config,     )     # For easier debugging while working from a Python shell     log.info(f"Fetched ({status}) <{method} {url}> (referer: {request_headers.get('referer')})")      if meta and not isinstance(meta, dict):         raise TypeError(f"Response meta should be dictionary but got {type(meta).__name__} instead!")      self.meta: Dict[str, Any] = meta or {}     self.request: Optional["Request"] = None  # Will be set by crawler     self.captured_xhr: List["Response"] = [] ``` |

### status `instance-attribute` [¶](#scrapling.engines.toolbelt.custom.Response.status "Permanent link")

```
status = status
```

### reason `instance-attribute` [¶](#scrapling.engines.toolbelt.custom.Response.reason "Permanent link")

```
reason = reason
```

### cookies `instance-attribute` [¶](#scrapling.engines.toolbelt.custom.Response.cookies "Permanent link")

```
cookies = cookies
```

### headers `instance-attribute` [¶](#scrapling.engines.toolbelt.custom.Response.headers "Permanent link")

```
headers = headers
```

### request_headers `instance-attribute` [¶](#scrapling.engines.toolbelt.custom.Response.request_headers "Permanent link")

```
request_headers = request_headers
```

### history `instance-attribute` [¶](#scrapling.engines.toolbelt.custom.Response.history "Permanent link")

```
history = history or []
```

### meta `instance-attribute` [¶](#scrapling.engines.toolbelt.custom.Response.meta "Permanent link")

```
meta = meta or {}
```

### request `instance-attribute` [¶](#scrapling.engines.toolbelt.custom.Response.request "Permanent link")

```
request = None
```

### captured_xhr `instance-attribute` [¶](#scrapling.engines.toolbelt.custom.Response.captured_xhr "Permanent link")

```
captured_xhr = []
```

### body `property` [¶](#scrapling.engines.toolbelt.custom.Response.body "Permanent link")

```
body
```

Return the raw body of the current `Selector` without any processing. Useful for binary and non-HTML requests.

Return the raw body of the response as bytes.

### generate_css_selector `property` [¶](#scrapling.engines.toolbelt.custom.Response.generate_css_selector "Permanent link")

```
generate_css_selector
```

Generate a CSS selector for the current element

| RETURNS | DESCRIPTION |
| --- | --- |
| `str` | A string of the generated selector. |

### generate_full_css_selector `property` [¶](#scrapling.engines.toolbelt.custom.Response.generate_full_css_selector "Permanent link")

```
generate_full_css_selector
```

Generate a complete CSS selector for the current element

| RETURNS | DESCRIPTION |
| --- | --- |
| `str` | A string of the generated selector. |

### generate_xpath_selector `property` [¶](#scrapling.engines.toolbelt.custom.Response.generate_xpath_selector "Permanent link")

```
generate_xpath_selector
```

Generate an XPath selector for the current element

| RETURNS | DESCRIPTION |
| --- | --- |
| `str` | A string of the generated selector. |

### generate_full_xpath_selector `property` [¶](#scrapling.engines.toolbelt.custom.Response.generate_full_xpath_selector "Permanent link")

```
generate_full_xpath_selector
```

Generate a complete XPath selector for the current element

| RETURNS | DESCRIPTION |
| --- | --- |
| `str` | A string of the generated selector. |

### __slots__ `class-attribute` `instance-attribute` [¶](#scrapling.engines.toolbelt.custom.Response.__slots__ "Permanent link")

```
__slots__ = (
    "url",
    "encoding",
    "__adaptive_enabled",
    "_root",
    "_storage",
    "__keep_comments",
    "__huge_tree_enabled",
    "__attributes",
    "__text",
    "__tag",
    "__keep_cdata",
    "_raw_body",
)
```

### url `instance-attribute` [¶](#scrapling.engines.toolbelt.custom.Response.url "Permanent link")

```
url = url
```

### encoding `instance-attribute` [¶](#scrapling.engines.toolbelt.custom.Response.encoding "Permanent link")

```
encoding = encoding
```

### tag `property` [¶](#scrapling.engines.toolbelt.custom.Response.tag "Permanent link")

```
tag
```

Get the tag name of the element

### text `property` [¶](#scrapling.engines.toolbelt.custom.Response.text "Permanent link")

```
text
```

Get text content of the element

### attrib `property` [¶](#scrapling.engines.toolbelt.custom.Response.attrib "Permanent link")

```
attrib
```

Get attributes of the element

### html_content `property` [¶](#scrapling.engines.toolbelt.custom.Response.html_content "Permanent link")

```
html_content
```

Return the inner HTML code of the element

### parent `property` [¶](#scrapling.engines.toolbelt.custom.Response.parent "Permanent link")

```
parent
```

Return the direct parent of the element or `None` otherwise

### below_elements `property` [¶](#scrapling.engines.toolbelt.custom.Response.below_elements "Permanent link")

```
below_elements
```

Return all elements under the current element in the DOM tree

### children `property` [¶](#scrapling.engines.toolbelt.custom.Response.children "Permanent link")

```
children
```

Return the children elements of the current element or empty list otherwise

### siblings `property` [¶](#scrapling.engines.toolbelt.custom.Response.siblings "Permanent link")

```
siblings
```

Return other children of the current element's parent or empty list otherwise

### path `property` [¶](#scrapling.engines.toolbelt.custom.Response.path "Permanent link")

```
path
```

Returns a list of type `Selectors` that contains the path leading to the current element from the root.

### next `property` [¶](#scrapling.engines.toolbelt.custom.Response.next "Permanent link")

```
next
```

Returns the next element of the current element in the children of the parent or `None` otherwise.

### previous `property` [¶](#scrapling.engines.toolbelt.custom.Response.previous "Permanent link")

```
previous
```

Returns the previous element of the current element in the children of the parent or `None` otherwise.

### extract `class-attribute` `instance-attribute` [¶](#scrapling.engines.toolbelt.custom.Response.extract "Permanent link")

```
extract = getall
```

### extract_first `class-attribute` `instance-attribute` [¶](#scrapling.engines.toolbelt.custom.Response.extract_first "Permanent link")

```
extract_first = get
```

### follow [¶](#scrapling.engines.toolbelt.custom.Response.follow "Permanent link")

```
follow(
    url,
    sid="",
    callback=None,
    priority=None,
    dont_filter=False,
    meta=None,
    referer_flow=True,
    **kwargs
)
```

Create a Request to follow a URL.

This is a helper method for spiders to easily follow links found in pages.

**IMPORTANT**: The below arguments if left empty, the corresponding value from the previous request will be used. The only exception is `dont_filter`.

| PARAMETER | DESCRIPTION |
| --- | --- |
| `url` | The URL to follow (can be relative, will be joined with current URL)  **TYPE:** `str` |
| `sid` | The session id to use  **TYPE:** `str`  **DEFAULT:** `''` |
| `callback` | Spider callback method to use  **TYPE:** `Callable[[Response], AsyncGenerator[Union[Dict[str, Any], Request, None], None]] | None`  **DEFAULT:** `None` |
| `priority` | The priority number to use, the higher the number, the higher priority to be processed first.  **TYPE:** `int | None`  **DEFAULT:** `None` |
| `dont_filter` | If this request has been done before, disable the filter to allow it again.  **TYPE:** `bool`  **DEFAULT:** `False` |
| `meta` | Additional meta data to included in the request  **TYPE:** `dict[str, Any] | None`  **DEFAULT:** `None` |
| `referer_flow` | Enabled by default, set the current response url as referer for the new request url.  **TYPE:** `bool`  **DEFAULT:** `True` |
| `kwargs` | Additional Request arguments  **TYPE:** `Any`  **DEFAULT:** `{}` |

| RETURNS | DESCRIPTION |
| --- | --- |
| `Any` | Request object ready to be yielded |

Source code in `scrapling/engines/toolbelt/custom.py`

|  |  |
| --- | --- |
| ```  88  89  90  91  92  93  94  95  96  97  98  99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 ``` | ``` def follow(     self,     url: str,     sid: str = "",     callback: Callable[["Response"], AsyncGenerator[Union[Dict[str, Any], "Request", None], None]] | None = None,     priority: int | None = None,     dont_filter: bool = False,     meta: dict[str, Any] | None = None,     referer_flow: bool = True,     **kwargs: Any, ) -> Any:     """Create a Request to follow a URL.      This is a helper method for spiders to easily follow links found in pages.      **IMPORTANT**: The below arguments if left empty, the corresponding value from the previous request will be used. The only exception is `dont_filter`.      :param url: The URL to follow (can be relative, will be joined with current URL)     :param sid: The session id to use     :param callback: Spider callback method to use     :param priority: The priority number to use, the higher the number, the higher priority to be processed first.     :param dont_filter: If this request has been done before, disable the filter to allow it again.     :param meta: Additional meta data to included in the request     :param referer_flow: Enabled by default, set the current response url as referer for the new request url.     :param kwargs: Additional Request arguments     :return: Request object ready to be yielded     """     from scrapling.spiders import Request      if not self.request or not isinstance(self.request, Request):         raise TypeError("This response has no request set yet.")      # Merge original session kwargs with new kwargs (new takes precedence)     session_kwargs = {**self.request._session_kwargs, **kwargs}      if referer_flow:         # For requests         headers = session_kwargs.get("headers", {})         headers["referer"] = self.url         session_kwargs["headers"] = headers          # For browsers         extra_headers = session_kwargs.get("extra_headers", {})         extra_headers["referer"] = self.url         session_kwargs["extra_headers"] = extra_headers          session_kwargs["google_search"] = False      return Request(         url=self.urljoin(url),         sid=sid or self.request.sid,         callback=callback or self.request.callback,         priority=priority if priority is not None else self.request.priority,         dont_filter=dont_filter,         meta={**(self.meta or {}), **(meta or {})},         **session_kwargs,     ) ``` |

### __str__ [¶](#scrapling.engines.toolbelt.custom.Response.__str__ "Permanent link")

```
__str__()
```

Source code in `scrapling/engines/toolbelt/custom.py`

|  |  |
| --- | --- |
| ``` 146 147 ``` | ``` def __str__(self) -> str:     return f"<{self.status} {self.url}>" ``` |

### __getitem__ [¶](#scrapling.engines.toolbelt.custom.Response.__getitem__ "Permanent link")

```
__getitem__(key)
```

Source code in `scrapling/parser.py`

|  |  |
| --- | --- |
| ``` 183 184 185 186 ``` | ``` def __getitem__(self, key: str) -> TextHandler:     if self._is_text_node(self._root):         raise TypeError("Text nodes do not have attributes")     return self.attrib[key] ``` |

### __contains__ [¶](#scrapling.engines.toolbelt.custom.Response.__contains__ "Permanent link")

```
__contains__(key)
```

Source code in `scrapling/parser.py`

|  |  |
| --- | --- |
| ``` 188 189 190 191 ``` | ``` def __contains__(self, key: str) -> bool:     if self._is_text_node(self._root):         return False     return key in self.attrib ``` |

### __getstate__ [¶](#scrapling.engines.toolbelt.custom.Response.__getstate__ "Permanent link")

```
__getstate__()
```

Source code in `scrapling/parser.py`

|  |  |
| --- | --- |
| ``` 250 251 252 ``` | ``` def __getstate__(self) -> Any:     # lxml don't like it :)     raise TypeError("Can't pickle Selector objects") ``` |

### get_all_text [¶](#scrapling.engines.toolbelt.custom.Response.get_all_text "Permanent link")

```
get_all_text(
    separator="\n",
    strip=False,
    ignore_tags=("script", "style"),
    valid_values=True,
)
```

Get all child strings of this element, concatenated using the given separator.

| PARAMETER | DESCRIPTION |
| --- | --- |
| `separator` | Strings will be concatenated using this separator.  **TYPE:** `str`  **DEFAULT:** `'\n'` |
| `strip` | If True, strings will be stripped before being concatenated.  **TYPE:** `bool`  **DEFAULT:** `False` |
| `ignore_tags` | A tuple of all tag names you want to ignore  **TYPE:** `Tuple`  **DEFAULT:** `('script', 'style')` |
| `valid_values` | If enabled, elements with text-content that is empty or only whitespaces will be ignored  **TYPE:** `bool`  **DEFAULT:** `True` |

| RETURNS | DESCRIPTION |
| --- | --- |
| `TextHandler` | A TextHandler |

Source code in `scrapling/parser.py`

|  |  |
| --- | --- |
| ``` 279 280 281 282 283 284 285 286 287 288 289 290 291 292 293 294 295 296 297 298 299 300 301 302 303 304 305 306 307 308 309 310 311 312 313 314 315 316 317 318 319 320 321 322 323 324 325 326 327 328 329 ``` | ``` def get_all_text(     self,     separator: str = "\n",     strip: bool = False,     ignore_tags: Tuple = (         "script",         "style",     ),     valid_values: bool = True, ) -> TextHandler:     """Get all child strings of this element, concatenated using the given separator.      :param separator: Strings will be concatenated using this separator.     :param strip: If True, strings will be stripped before being concatenated.     :param ignore_tags: A tuple of all tag names you want to ignore     :param valid_values: If enabled, elements with text-content that is empty or only whitespaces will be ignored      :return: A TextHandler     """     if self._is_text_node(self._root):         return TextHandler(str(self._root))      ignored_elements: set[Any] = set()     if ignore_tags:         ignored_elements.update(self._root.iter(*ignore_tags))      _all_strings = []      def append_text(text: str) -> None:         processed_text = text.strip() if strip else text         if not valid_values or processed_text.strip():             _all_strings.append(processed_text)      def is_visible_text_node(text_node: _ElementUnicodeResult) -> bool:         parent = text_node.getparent()         if parent is None:             return False          owner = parent.getparent() if text_node.is_tail else parent         while owner is not None:             if owner in ignored_elements:                 return False             owner = owner.getparent()         return True      for text_node in cast(list[_ElementUnicodeResult], _find_all_text_nodes(self._root)):         text = str(text_node)         if text and is_visible_text_node(text_node):             append_text(text)      return cast(TextHandler, TextHandler(separator).join(_all_strings)) ``` |

### urljoin [¶](#scrapling.engines.toolbelt.custom.Response.urljoin "Permanent link")

```
urljoin(relative_url)
```

Join this Selector's url with a relative url to form an absolute full URL.

Source code in `scrapling/parser.py`

|  |  |
| --- | --- |
| ``` 331 332 333 ``` | ``` def urljoin(self, relative_url: str) -> str:     """Join this Selector's url with a relative url to form an absolute full URL."""     return urljoin(self.url, relative_url) ``` |

### prettify [¶](#scrapling.engines.toolbelt.custom.Response.prettify "Permanent link")

```
prettify()
```

Return a prettified version of the element's inner html-code

Source code in `scrapling/parser.py`

|  |  |
| --- | --- |
| ``` 361 362 363 364 365 366 367 368 369 370 371 372 373 374 ``` | ``` def prettify(self) -> TextHandler:     """Return a prettified version of the element's inner html-code"""     if self._is_text_node(self._root):         return TextHandler(str(self._root))     content = tostring(         self._root,         encoding=self.encoding,         pretty_print=True,         method="html",         with_tail=False,     )     if isinstance(content, bytes):         content = content.strip().decode(self.encoding)     return TextHandler(content) ``` |

### has_class [¶](#scrapling.engines.toolbelt.custom.Response.has_class "Permanent link")

```
has_class(class_name)
```

Check if the element has a specific class

| PARAMETER | DESCRIPTION |
| --- | --- |
| `class_name` | The class name to check for  **TYPE:** `str` |

| RETURNS | DESCRIPTION |
| --- | --- |
| `bool` | True if element has class with that name otherwise False |

Source code in `scrapling/parser.py`

|  |  |
| --- | --- |
| ``` 376 377 378 379 380 381 382 383 ``` | ``` def has_class(self, class_name: str) -> bool:     """Check if the element has a specific class     :param class_name: The class name to check for     :return: True if element has class with that name otherwise False     """     if self._is_text_node(self._root):         return False     return class_name in self._root.classes ``` |

### iterancestors [¶](#scrapling.engines.toolbelt.custom.Response.iterancestors "Permanent link")

```
iterancestors()
```

Return a generator that loops over all ancestors of the element, starting with the element's parent.

Source code in `scrapling/parser.py`

|  |  |
| --- | --- |
| ``` 417 418 419 420 421 422 ``` | ``` def iterancestors(self) -> Generator["Selector", None, None]:     """Return a generator that loops over all ancestors of the element, starting with the element's parent."""     if self._is_text_node(self._root):         return     for ancestor in self._root.iterancestors():         yield self.__element_convertor(ancestor) ``` |

### find_ancestor [¶](#scrapling.engines.toolbelt.custom.Response.find_ancestor "Permanent link")

```
find_ancestor(func)
```

Loop over all ancestors of the element till one match the passed function

| PARAMETER | DESCRIPTION |
| --- | --- |
| `func` | A function that takes each ancestor as an argument and returns True/False  **TYPE:** `Callable[[Selector], bool]` |

| RETURNS | DESCRIPTION |
| --- | --- |
| `Optional[Selector]` | The first ancestor that match the function or `None` otherwise. |

Source code in `scrapling/parser.py`

|  |  |
| --- | --- |
| ``` 424 425 426 427 428 429 430 431 432 ``` | ``` def find_ancestor(self, func: Callable[["Selector"], bool]) -> Optional["Selector"]:     """Loop over all ancestors of the element till one match the passed function     :param func: A function that takes each ancestor as an argument and returns True/False     :return: The first ancestor that match the function or ``None`` otherwise.     """     for ancestor in self.iterancestors():         if func(ancestor):             return ancestor     return None ``` |

### get [¶](#scrapling.engines.toolbelt.custom.Response.get "Permanent link")

```
get()
```

Serialize this element to a string.
For text nodes, returns the text value. For HTML elements, returns the outer HTML.

Source code in `scrapling/parser.py`

|  |  |
| --- | --- |
| ``` 464 465 466 467 468 469 470 471 ``` | ``` def get(self) -> TextHandler:     """     Serialize this element to a string.     For text nodes, returns the text value. For HTML elements, returns the outer HTML.     """     if self._is_text_node(self._root):         return TextHandler(str(self._root))     return self.html_content ``` |

### getall [¶](#scrapling.engines.toolbelt.custom.Response.getall "Permanent link")

```
getall()
```

Return a single-element list containing this element's serialized string.

Source code in `scrapling/parser.py`

|  |  |
| --- | --- |
| ``` 473 474 475 ``` | ``` def getall(self) -> TextHandlers:     """Return a single-element list containing this element's serialized string."""     return TextHandlers([self.get()]) ``` |

### __repr__ [¶](#scrapling.engines.toolbelt.custom.Response.__repr__ "Permanent link")

```
__repr__()
```

Source code in `scrapling/parser.py`

|  |  |
| --- | --- |
| ``` 485 486 487 488 489 490 491 492 493 494 495 496 497 498 499 500 501 502 503 504 505 506 ``` | ``` def __repr__(self) -> str:     length_limit = 40      if self._is_text_node(self._root):         text = str(self._root)         if len(text) > length_limit:             text = text[:length_limit].strip() + "..."         return f"<text='{text}'>"      content = clean_spaces(self.html_content)     if len(content) > length_limit:         content = content[:length_limit].strip() + "..."     data = f"<data='{content}'"      if self.parent:         parent_content = clean_spaces(self.parent.html_content)         if len(parent_content) > length_limit:             parent_content = parent_content[:length_limit].strip() + "..."          data += f" parent='{parent_content}'"      return data + ">" ``` |

### relocate [¶](#scrapling.engines.toolbelt.custom.Response.relocate "Permanent link")

```
relocate(element, percentage=0, selector_type=False)
```

This function will search again for the element in the page tree, used automatically on page structure change

| PARAMETER | DESCRIPTION |
| --- | --- |
| `element` | The element we want to relocate in the tree  **TYPE:** `Union[Dict, HtmlElement, Selector]` |
| `percentage` | The minimum percentage to accept and not going lower than that. Be aware that the percentage calculation depends solely on the page structure, so don't play with this number unless you must know what you are doing!  **TYPE:** `int`  **DEFAULT:** `0` |
| `selector_type` | If True, the return result will be converted to `Selectors` object  **TYPE:** `bool`  **DEFAULT:** `False` |

| RETURNS | DESCRIPTION |
| --- | --- |
| `Union[List[HtmlElement], Selectors]` | List of pure HTML elements that got the highest matching score or 'Selectors' object |

Source code in `scrapling/parser.py`

|  |  |
| --- | --- |
| ``` 519 520 521 522 523 524 525 526 527 528 529 530 531 532 533 534 535 536 537 538 539 540 541 542 543 544 545 546 547 548 549 550 551 552 553 554 555 556 557 558 559 560 561 562 ``` | ``` def relocate(     self,     element: Union[Dict, HtmlElement, "Selector"],     percentage: int = 0,     selector_type: bool = False, ) -> Union[List[HtmlElement], "Selectors"]:     """This function will search again for the element in the page tree, used automatically on page structure change      :param element: The element we want to relocate in the tree     :param percentage: The minimum percentage to accept and not going lower than that. Be aware that the percentage      calculation depends solely on the page structure, so don't play with this number unless you must know      what you are doing!     :param selector_type: If True, the return result will be converted to `Selectors` object     :return: List of pure HTML elements that got the highest matching score or 'Selectors' object     """     score_table: Dict[float, List[Any]] = {}     # Note: `element` will most likely always be a dictionary at this point.     if isinstance(element, self.__class__):         element = element._root      if issubclass(type(element), HtmlElement):         element = _StorageTools.element_to_dict(element)      for node in cast(List, _find_all_elements(self._root)):         # Collect all elements in the page, then for each element get the matching score of it against the node.         # Hence: the code doesn't stop even if the score was 100%         # because there might be another element(s) left in page with the same score         score = self.__calculate_similarity_score(cast(Dict, element), node)         score_table.setdefault(score, []).append(node)      if score_table:         highest_probability = max(score_table.keys())         if score_table[highest_probability] and highest_probability >= percentage:             if log.getEffectiveLevel() < 20:                 # No need to execute this part if the logging level is not debugging                 log.debug(f"Highest probability was {highest_probability}%")                 log.debug("Top 5 best matching elements are: ")                 for percent in tuple(sorted(score_table.keys(), reverse=True))[:5]:                     log.debug(f"{percent} -> {self.__elements_convertor(score_table[percent])}")              if not selector_type:                 return score_table[highest_probability]             return self.__elements_convertor(score_table[highest_probability])     return [] ``` |

### css [¶](#scrapling.engines.toolbelt.custom.Response.css "Permanent link")

```
css(
    selector,
    identifier="",
    adaptive=False,
    auto_save=False,
    percentage=0,
)
```

Search the current tree with CSS3 selectors

**Important:
It's recommended to use the identifier argument if you plan to use a different selector later
and want to relocate the same element(s)**

| PARAMETER | DESCRIPTION |
| --- | --- |
| `selector` | The CSS3 selector to be used.  **TYPE:** `str` |
| `adaptive` | Enabled will make the function try to relocate the element if it was 'saved' before  **TYPE:** `bool`  **DEFAULT:** `False` |
| `identifier` | A string that will be used to save/retrieve element's data in adaptive, otherwise the selector will be used.  **TYPE:** `str`  **DEFAULT:** `''` |
| `auto_save` | Automatically save new elements for `adaptive` later  **TYPE:** `bool`  **DEFAULT:** `False` |
| `percentage` | The minimum percentage to accept while `adaptive` is working and not going lower than that. Be aware that the percentage calculation depends solely on the page structure, so don't play with this number unless you must know what you are doing!  **TYPE:** `int`  **DEFAULT:** `0` |

| RETURNS | DESCRIPTION |
| --- | --- |
| `Selectors` | `Selectors` class. |

Source code in `scrapling/parser.py`

|  |  |
| --- | --- |
| ``` 564 565 566 567 568 569 570 571 572 573 574 575 576 577 578 579 580 581 582 583 584 585 586 587 588 589 590 591 592 593 594 595 596 597 598 599 600 601 602 603 604 605 606 607 608 609 610 611 612 613 614 615 616 617 618 619 620 621 622 ``` | ``` def css(     self,     selector: str,     identifier: str = "",     adaptive: bool = False,     auto_save: bool = False,     percentage: int = 0, ) -> "Selectors":     """Search the current tree with CSS3 selectors      **Important:     It's recommended to use the identifier argument if you plan to use a different selector later     and want to relocate the same element(s)**      :param selector: The CSS3 selector to be used.     :param adaptive: Enabled will make the function try to relocate the element if it was 'saved' before     :param identifier: A string that will be used to save/retrieve element's data in adaptive,      otherwise the selector will be used.     :param auto_save: Automatically save new elements for `adaptive` later     :param percentage: The minimum percentage to accept while `adaptive` is working and not going lower than that.      Be aware that the percentage calculation depends solely on the page structure, so don't play with this      number unless you must know what you are doing!      :return: `Selectors` class.     """     if self._is_text_node(self._root):         return Selectors()      try:         if not self.__adaptive_enabled or "," not in selector:             # No need to split selectors in this case, let's save some CPU cycles :)             xpath_selector = _css_to_xpath(selector)             return self.xpath(                 xpath_selector,                 identifier or selector,                 adaptive,                 auto_save,                 percentage,             )          results = Selectors()         for single_selector in split_selectors(selector):             # I'm doing this only so the `save` function saves data correctly for combined selectors             # Like using the ',' to combine two different selectors that point to different elements.             xpath_selector = _css_to_xpath(single_selector.canonical())             results += self.xpath(                 xpath_selector,                 identifier or single_selector.canonical(),                 adaptive,                 auto_save,                 percentage,             )          return Selectors(results)     except (         SelectorError,         SelectorSyntaxError,     ) as e:         raise SelectorSyntaxError(f"Invalid CSS selector '{selector}': {str(e)}") from e ``` |

### xpath [¶](#scrapling.engines.toolbelt.custom.Response.xpath "Permanent link")

```
xpath(
    selector,
    identifier="",
    adaptive=False,
    auto_save=False,
    percentage=0,
    **kwargs
)
```

Search the current tree with XPath selectors

**Important:
It's recommended to use the identifier argument if you plan to use a different selector later
and want to relocate the same element(s)**

Note: **Additional keyword arguments will be passed as XPath variables in the XPath expression!**

| PARAMETER | DESCRIPTION |
| --- | --- |
| `selector` | The XPath selector to be used.  **TYPE:** `str` |
| `adaptive` | Enabled will make the function try to relocate the element if it was 'saved' before  **TYPE:** `bool`  **DEFAULT:** `False` |
| `identifier` | A string that will be used to save/retrieve element's data in adaptive, otherwise the selector will be used.  **TYPE:** `str`  **DEFAULT:** `''` |
| `auto_save` | Automatically save new elements for `adaptive` later  **TYPE:** `bool`  **DEFAULT:** `False` |
| `percentage` | The minimum percentage to accept while `adaptive` is working and not going lower than that. Be aware that the percentage calculation depends solely on the page structure, so don't play with this number unless you must know what you are doing!  **TYPE:** `int`  **DEFAULT:** `0` |

| RETURNS | DESCRIPTION |
| --- | --- |
| `Selectors` | `Selectors` class. |

Source code in `scrapling/parser.py`

|  |  |
| --- | --- |
| ``` 624 625 626 627 628 629 630 631 632 633 634 635 636 637 638 639 640 641 642 643 644 645 646 647 648 649 650 651 652 653 654 655 656 657 658 659 660 661 662 663 664 665 666 667 668 669 670 671 672 673 674 675 676 677 678 679 680 681 682 683 684 685 686 687 688 689 690 691 692 ``` | ``` def xpath(     self,     selector: str,     identifier: str = "",     adaptive: bool = False,     auto_save: bool = False,     percentage: int = 0,     **kwargs: Any, ) -> "Selectors":     """Search the current tree with XPath selectors      **Important:     It's recommended to use the identifier argument if you plan to use a different selector later     and want to relocate the same element(s)**       Note: **Additional keyword arguments will be passed as XPath variables in the XPath expression!**      :param selector: The XPath selector to be used.     :param adaptive: Enabled will make the function try to relocate the element if it was 'saved' before     :param identifier: A string that will be used to save/retrieve element's data in adaptive,      otherwise the selector will be used.     :param auto_save: Automatically save new elements for `adaptive` later     :param percentage: The minimum percentage to accept while `adaptive` is working and not going lower than that.      Be aware that the percentage calculation depends solely on the page structure, so don't play with this      number unless you must know what you are doing!      :return: `Selectors` class.     """     if self._is_text_node(self._root):         return Selectors()      try:         if elements := self._root.xpath(selector, **kwargs):             if not self.__adaptive_enabled and auto_save:                 log.warning(                     "Argument `auto_save` will be ignored because `adaptive` wasn't enabled on initialization. Check docs for more info."                 )             elif self.__adaptive_enabled and auto_save:                 self.save(elements[0], identifier or selector)              return self.__handle_elements(elements)         elif self.__adaptive_enabled:             if adaptive:                 element_data = self.retrieve(identifier or selector)                 if element_data:                     elements = self.relocate(element_data, percentage)                     if elements is not None and auto_save:                         self.save(elements[0], identifier or selector)              return self.__handle_elements(elements)         else:             if adaptive:                 log.warning(                     "Argument `adaptive` will be ignored because `adaptive` wasn't enabled on initialization. Check docs for more info."                 )             elif auto_save:                 log.warning(                     "Argument `auto_save` will be ignored because `adaptive` wasn't enabled on initialization. Check docs for more info."                 )              return self.__handle_elements(elements)      except (         SelectorError,         SelectorSyntaxError,         XPathError,         XPathEvalError,     ) as e:         raise SelectorSyntaxError(f"Invalid XPath selector: {selector}") from e ``` |

### find_all [¶](#scrapling.engines.toolbelt.custom.Response.find_all "Permanent link")

```
find_all(*args, **kwargs)
```

Find elements by filters of your creations for ease.

| PARAMETER | DESCRIPTION |
| --- | --- |
| `args` | Tag name(s), iterable of tag names, regex patterns, function, or a dictionary of elements' attributes. Leave empty for selecting all.  **TYPE:** `str | Iterable[str] | Pattern | Callable | Dict[str, str]`  **DEFAULT:** `()` |
| `kwargs` | The attributes you want to filter elements based on it.  **TYPE:** `str`  **DEFAULT:** `{}` |

| RETURNS | DESCRIPTION |
| --- | --- |
| `Selectors` | The `Selectors` object of the elements or empty list |

Source code in `scrapling/parser.py`

|  |  |
| --- | --- |
| ``` 694 695 696 697 698 699 700 701 702 703 704 705 706 707 708 709 710 711 712 713 714 715 716 717 718 719 720 721 722 723 724 725 726 727 728 729 730 731 732 733 734 735 736 737 738 739 740 741 742 743 744 745 746 747 748 749 750 751 752 753 754 755 756 757 758 759 760 761 762 763 764 765 766 767 768 769 770 771 772 773 774 775 776 777 778 779 780 781 782 783 784 785 786 ``` | ``` def find_all(     self,     *args: str | Iterable[str] | Pattern | Callable | Dict[str, str],     **kwargs: str, ) -> "Selectors":     """Find elements by filters of your creations for ease.      :param args: Tag name(s), iterable of tag names, regex patterns, function, or a dictionary of elements' attributes. Leave empty for selecting all.     :param kwargs: The attributes you want to filter elements based on it.     :return: The `Selectors` object of the elements or empty list     """     if self._is_text_node(self._root):         return Selectors()      if not args and not kwargs:         raise TypeError("You have to pass something to search with, like tag name(s), tag attributes, or both.")      attributes: Dict[str, Any] = dict()     tags: Set[str] = set()     patterns: Set[Pattern] = set()     results, functions, selectors = Selectors(), [], []      # Brace yourself for a wonderful journey!     for arg in args:         if isinstance(arg, str):             tags.add(arg)          elif type(arg) in (list, tuple, set):             arg = cast(Iterable, arg)  # Type narrowing for type checkers like pyright             if not all(map(lambda x: isinstance(x, str), arg)):                 raise TypeError("Nested Iterables are not accepted, only iterables of tag names are accepted")             tags.update(set(arg))          elif isinstance(arg, dict):             if not all([(isinstance(k, str) and isinstance(v, str)) for k, v in arg.items()]):                 raise TypeError(                     "Nested dictionaries are not accepted, only string keys and string values are accepted"                 )             attributes.update(arg)          elif isinstance(arg, re_Pattern):             patterns.add(arg)          elif callable(arg):             if len(signature(arg).parameters) > 0:                 functions.append(arg)             else:                 raise TypeError(                     "Callable filter function must have at least one argument to take `Selector` objects."                 )          else:             raise TypeError(f'Argument with type "{type(arg)}" is not accepted, please read the docs.')      if not all([(isinstance(k, str) and isinstance(v, str)) for k, v in kwargs.items()]):         raise TypeError("Only string values are accepted for arguments")      for attribute_name, value in kwargs.items():         # Only replace names for kwargs, replacing them in dictionaries doesn't make sense         attribute_name = _whitelisted.get(attribute_name, attribute_name)         attributes[attribute_name] = value      # It's easier and faster to build a selector than traversing the tree     tags = tags or set("*")     for tag in tags:         selector = tag         for key, value in attributes.items():             value = value.replace('"', r"\"")  # Escape double quotes in user input             # Not escaping anything with the key so the user can pass patterns like {'href*': '/p/'} or get errors :)             selector += '[{}="{}"]'.format(key, value)         if selector != "*":             selectors.append(selector)      if selectors:         results = cast(Selectors, self.css(", ".join(selectors)))         if results:             # From the results, get the ones that fulfill passed regex patterns             for pattern in patterns:                 results = results.filter(lambda e: e.text.re(pattern, check_match=True))              # From the results, get the ones that fulfill passed functions             for function in functions:                 results = results.filter(function)     else:         results = results or self.below_elements         for pattern in patterns:             results = results.filter(lambda e: e.text.re(pattern, check_match=True))          # Collect an element if it fulfills the passed function otherwise         for function in functions:             results = results.filter(function)      return results ``` |

### find [¶](#scrapling.engines.toolbelt.custom.Response.find "Permanent link")

```
find(*args, **kwargs)
```

Find elements by filters of your creations for ease, then return the first result. Otherwise return `None`.

| PARAMETER | DESCRIPTION |
| --- | --- |
| `args` | Tag name(s), iterable of tag names, regex patterns, function, or a dictionary of elements' attributes. Leave empty for selecting all.  **TYPE:** `str | Iterable[str] | Pattern | Callable | Dict[str, str]`  **DEFAULT:** `()` |
| `kwargs` | The attributes you want to filter elements based on it.  **TYPE:** `str`  **DEFAULT:** `{}` |

| RETURNS | DESCRIPTION |
| --- | --- |
| `Optional[Selector]` | The `Selector` object of the element or `None` if the result didn't match |

Source code in `scrapling/parser.py`

|  |  |
| --- | --- |
| ``` 788 789 790 791 792 793 794 795 796 797 798 799 800 801 ``` | ``` def find(     self,     *args: str | Iterable[str] | Pattern | Callable | Dict[str, str],     **kwargs: str, ) -> Optional["Selector"]:     """Find elements by filters of your creations for ease, then return the first result. Otherwise return `None`.      :param args: Tag name(s), iterable of tag names, regex patterns, function, or a dictionary of elements' attributes. Leave empty for selecting all.     :param kwargs: The attributes you want to filter elements based on it.     :return: The `Selector` object of the element or `None` if the result didn't match     """     for element in self.find_all(*args, **kwargs):         return element     return None ``` |

### save [¶](#scrapling.engines.toolbelt.custom.Response.save "Permanent link")

```
save(element, identifier)
```

Saves the element's unique properties to the storage for retrieval and relocation later

| PARAMETER | DESCRIPTION |
| --- | --- |
| `element` | The element itself that we want to save to storage, it can be a `Selector` or pure `HtmlElement`  **TYPE:** `HtmlElement` |
| `identifier` | This is the identifier that will be used to retrieve the element later from the storage. See the docs for more info.  **TYPE:** `str` |

Source code in `scrapling/parser.py`

|  |  |
| --- | --- |
| ``` 877 878 879 880 881 882 883 884 885 886 887 888 889 890 891 892 893 894 895 896 ``` | ``` def save(self, element: HtmlElement, identifier: str) -> None:     """Saves the element's unique properties to the storage for retrieval and relocation later      :param element: The element itself that we want to save to storage, it can be a ` Selector ` or pure ` HtmlElement `     :param identifier: This is the identifier that will be used to retrieve the element later from the storage. See         the docs for more info.     """     if self.__adaptive_enabled and self._storage:         target_element: Any = element         if isinstance(target_element, self.__class__):             target_element = target_element._root          if self._is_text_node(target_element):             target_element = target_element.getparent()          self._storage.save(target_element, identifier)     else:         raise RuntimeError(             "Can't use `adaptive` features while it's disabled globally, you have to start a new class instance."         ) ``` |

### retrieve [¶](#scrapling.engines.toolbelt.custom.Response.retrieve "Permanent link")

```
retrieve(identifier)
```

Using the identifier, we search the storage and return the unique properties of the element

| PARAMETER | DESCRIPTION |
| --- | --- |
| `identifier` | This is the identifier that will be used to retrieve the element from the storage. See the docs for more info.  **TYPE:** `str` |

| RETURNS | DESCRIPTION |
| --- | --- |
| `Optional[Dict[str, Any]]` | A dictionary of the unique properties |

Source code in `scrapling/parser.py`

|  |  |
| --- | --- |
| ``` 898 899 900 901 902 903 904 905 906 907 908 909 910 ``` | ``` def retrieve(self, identifier: str) -> Optional[Dict[str, Any]]:     """Using the identifier, we search the storage and return the unique properties of the element      :param identifier: This is the identifier that will be used to retrieve the element from the storage. See         the docs for more info.     :return: A dictionary of the unique properties     """     if self.__adaptive_enabled and self._storage:         return self._storage.retrieve(identifier)      raise RuntimeError(         "Can't use `adaptive` features while it's disabled globally, you have to start a new class instance."     ) ``` |

### json [¶](#scrapling.engines.toolbelt.custom.Response.json "Permanent link")

```
json()
```

Return JSON response if the response is jsonable otherwise throws error

Source code in `scrapling/parser.py`

|  |  |
| --- | --- |
| ``` 913 914 915 916 917 918 919 920 921 922 923 924 925 926 927 ``` | ``` def json(self) -> Dict:     """Return JSON response if the response is jsonable otherwise throws error"""     if self._is_text_node(self._root):         return TextHandler(str(self._root)).json()     if self._raw_body and isinstance(self._raw_body, (str, bytes)):         if isinstance(self._raw_body, str):             return TextHandler(self._raw_body).json()         else:             if TYPE_CHECKING:                 assert isinstance(self._raw_body, bytes)             return TextHandler(self._raw_body.decode()).json()     elif self.text:         return self.text.json()     else:         return self.get_all_text(strip=True).json() ``` |

### re [¶](#scrapling.engines.toolbelt.custom.Response.re "Permanent link")

```
re(
    regex,
    replace_entities=True,
    clean_match=False,
    case_sensitive=True,
)
```

Apply the given regex to the current text and return a list of strings with the matches.

| PARAMETER | DESCRIPTION |
| --- | --- |
| `regex` | Can be either a compiled regular expression or a string.  **TYPE:** `str | Pattern[str]` |
| `replace_entities` | If enabled character entity references are replaced by their corresponding character  **TYPE:** `bool`  **DEFAULT:** `True` |
| `clean_match` | if enabled, this will ignore all whitespaces and consecutive spaces while matching  **TYPE:** `bool`  **DEFAULT:** `False` |
| `case_sensitive` | if disabled, the function will set the regex to ignore the letters case while compiling it  **TYPE:** `bool`  **DEFAULT:** `True` |

Source code in `scrapling/parser.py`

|  |  |
| --- | --- |
| ``` 929 930 931 932 933 934 935 936 937 938 939 940 941 942 943 ``` | ``` def re(     self,     regex: str | Pattern[str],     replace_entities: bool = True,     clean_match: bool = False,     case_sensitive: bool = True, ) -> TextHandlers:     """Apply the given regex to the current text and return a list of strings with the matches.      :param regex: Can be either a compiled regular expression or a string.     :param replace_entities: If enabled character entity references are replaced by their corresponding character     :param clean_match: if enabled, this will ignore all whitespaces and consecutive spaces while matching     :param case_sensitive: if disabled, the function will set the regex to ignore the letters case while compiling it     """     return self.text.re(regex, replace_entities, clean_match, case_sensitive) ``` |

### re_first [¶](#scrapling.engines.toolbelt.custom.Response.re_first "Permanent link")

```
re_first(
    regex,
    default=None,
    replace_entities=True,
    clean_match=False,
    case_sensitive=True,
)
```

Apply the given regex to text and return the first match if found, otherwise return the default value.

| PARAMETER | DESCRIPTION |
| --- | --- |
| `regex` | Can be either a compiled regular expression or a string.  **TYPE:** `str | Pattern[str]` |
| `default` | The default value to be returned if there is no match  **DEFAULT:** `None` |
| `replace_entities` | if enabled character entity references are replaced by their corresponding character  **TYPE:** `bool`  **DEFAULT:** `True` |
| `clean_match` | if enabled, this will ignore all whitespaces and consecutive spaces while matching  **TYPE:** `bool`  **DEFAULT:** `False` |
| `case_sensitive` | if disabled, the function will set the regex to ignore the letters case while compiling it  **TYPE:** `bool`  **DEFAULT:** `True` |

Source code in `scrapling/parser.py`

|  |  |
| --- | --- |
| ``` 945 946 947 948 949 950 951 952 953 954 955 956 957 958 959 960 961 ``` | ``` def re_first(     self,     regex: str | Pattern[str],     default=None,     replace_entities: bool = True,     clean_match: bool = False,     case_sensitive: bool = True, ) -> TextHandler:     """Apply the given regex to text and return the first match if found, otherwise return the default value.      :param regex: Can be either a compiled regular expression or a string.     :param default: The default value to be returned if there is no match     :param replace_entities: if enabled character entity references are replaced by their corresponding character     :param clean_match: if enabled, this will ignore all whitespaces and consecutive spaces while matching     :param case_sensitive: if disabled, the function will set the regex to ignore the letters case while compiling it     """     return self.text.re_first(regex, default, replace_entities, clean_match, case_sensitive) ``` |

### find_similar [¶](#scrapling.engines.toolbelt.custom.Response.find_similar "Permanent link")

```
find_similar(
    similarity_threshold=0.2,
    ignore_attributes=("href", "src"),
    match_text=False,
)
```

Find elements that are in the same tree depth in the page with the same tag name and same parent tag etc...
then return the ones that match the current element attributes with a percentage higher than the input threshold.

This function is inspired by AutoScraper and made for cases where you, for example, found a product div inside
a products-list container and want to find other products using that element as a starting point EXCEPT
this function works in any case without depending on the element type.

| PARAMETER | DESCRIPTION |
| --- | --- |
| `similarity_threshold` | The percentage to use while comparing element attributes. Note: Elements found before attributes matching/comparison will be sharing the same depth, same tag name, same parent tag name, and same grand parent tag name. So they are 99% likely to be correct unless you are extremely unlucky, then attributes matching comes into play, so don't play with this number unless you are getting the results you don't want. Also, if the current element doesn't have attributes and the similar element as well, then it's a 100% match.  **TYPE:** `float`  **DEFAULT:** `0.2` |
| `ignore_attributes` | Attribute names passed will be ignored while matching the attributes in the last step. The default value is to ignore `href` and `src` as URLs can change a lot between elements, so it's unreliable  **TYPE:** `List | Tuple`  **DEFAULT:** `('href', 'src')` |
| `match_text` | If True, element text content will be taken into calculation while matching. Not recommended to use in normal cases, but it depends.  **TYPE:** `bool`  **DEFAULT:** `False` |

| RETURNS | DESCRIPTION |
| --- | --- |
| `Selectors` | A `Selectors` container of `Selector` objects or empty list |

Source code in `scrapling/parser.py`

|  |  |
| --- | --- |
| ``` 1009 1010 1011 1012 1013 1014 1015 1016 1017 1018 1019 1020 1021 1022 1023 1024 1025 1026 1027 1028 1029 1030 1031 1032 1033 1034 1035 1036 1037 1038 1039 1040 1041 1042 1043 1044 1045 1046 1047 1048 1049 1050 1051 1052 1053 1054 1055 1056 1057 1058 1059 1060 1061 1062 1063 1064 1065 1066 1067 1068 ``` | ``` def find_similar(     self,     similarity_threshold: float = 0.2,     ignore_attributes: List | Tuple = (         "href",         "src",     ),     match_text: bool = False, ) -> "Selectors":     """Find elements that are in the same tree depth in the page with the same tag name and same parent tag etc...     then return the ones that match the current element attributes with a percentage higher than the input threshold.      This function is inspired by AutoScraper and made for cases where you, for example, found a product div inside     a products-list container and want to find other products using that element as a starting point EXCEPT     this function works in any case without depending on the element type.      :param similarity_threshold: The percentage to use while comparing element attributes.         Note: Elements found before attributes matching/comparison will be sharing the same depth, same tag name,         same parent tag name, and same grand parent tag name. So they are 99% likely to be correct unless you are         extremely unlucky, then attributes matching comes into play, so don't play with this number unless         you are getting the results you don't want.         Also, if the current element doesn't have attributes and the similar element as well, then it's a 100% match.     :param ignore_attributes: Attribute names passed will be ignored while matching the attributes in the last step.         The default value is to ignore `href` and `src` as URLs can change a lot between elements, so it's unreliable     :param match_text: If True, element text content will be taken into calculation while matching.         Not recommended to use in normal cases, but it depends.      :return: A ``Selectors`` container of ``Selector`` objects or empty list     """     if self._is_text_node(self._root):         return Selectors()      # We will use the elements' root from now on to get the speed boost of using Lxml directly     root = self._root     similar_elements = list()      current_depth = len(list(root.iterancestors()))     target_attrs = self.__get_attributes(root, ignore_attributes) if ignore_attributes else root.attrib      path_parts = [self.tag]     if (parent := root.getparent()) is not None:         path_parts.insert(0, parent.tag)         if (grandparent := parent.getparent()) is not None:             path_parts.insert(0, grandparent.tag)      xpath_path = "//{}".format("/".join(path_parts))     potential_matches = root.xpath(f"{xpath_path}[count(ancestor::*) = {current_depth}]")      for potential_match in potential_matches:         if potential_match != root and self.__are_alike(             root,             target_attrs,             potential_match,             ignore_attributes,             similarity_threshold,             match_text,         ):             similar_elements.append(potential_match)      return Selectors(map(self.__element_convertor, similar_elements)) ``` |

### find_by_text [¶](#scrapling.engines.toolbelt.custom.Response.find_by_text "Permanent link")

```
find_by_text(
    text,
    first_match=True,
    partial=False,
    case_sensitive=False,
    clean_match=True,
)
```

Find elements that its text content fully/partially matches input.

| PARAMETER | DESCRIPTION |
| --- | --- |
| `text` | Text query to match  **TYPE:** `str` |
| `first_match` | Returns the first element that matches conditions, enabled by default  **TYPE:** `bool`  **DEFAULT:** `True` |
| `partial` | If enabled, the function returns elements that contain the input text  **TYPE:** `bool`  **DEFAULT:** `False` |
| `case_sensitive` | if enabled, the letters case will be taken into consideration  **TYPE:** `bool`  **DEFAULT:** `False` |
| `clean_match` | if enabled, this will ignore all whitespaces and consecutive spaces while matching  **TYPE:** `bool`  **DEFAULT:** `True` |

Source code in `scrapling/parser.py`

|  |  |
| --- | --- |
| ``` 1090 1091 1092 1093 1094 1095 1096 1097 1098 1099 1100 1101 1102 1103 1104 1105 1106 1107 1108 1109 1110 1111 1112 1113 1114 1115 1116 1117 1118 1119 1120 1121 1122 1123 1124 1125 1126 1127 1128 1129 1130 1131 1132 1133 1134 1135 1136 ``` | ``` def find_by_text(     self,     text: str,     first_match: bool = True,     partial: bool = False,     case_sensitive: bool = False,     clean_match: bool = True, ) -> Union["Selectors", "Selector"]:     """Find elements that its text content fully/partially matches input.     :param text: Text query to match     :param first_match: Returns the first element that matches conditions, enabled by default     :param partial: If enabled, the function returns elements that contain the input text     :param case_sensitive: if enabled, the letters case will be taken into consideration     :param clean_match: if enabled, this will ignore all whitespaces and consecutive spaces while matching     """     if self._is_text_node(self._root):         return Selectors()      results = Selectors()     if not case_sensitive:         text = text.lower()      possible_targets = cast(List, _find_all_elements_with_spaces(self._root))     if possible_targets:         for node in self.__elements_convertor(possible_targets):             """Check if element matches given text otherwise, traverse the children tree and iterate"""             node_text: TextHandler = node.text             if clean_match:                 node_text = TextHandler(node_text.clean())              if not case_sensitive:                 node_text = TextHandler(node_text.lower())              if partial:                 if text in node_text:                     results.append(node)             elif text == node_text:                 results.append(node)              if first_match and results:                 # we got an element so we should stop                 break          if first_match:             if results:                 return results[0]     return results ``` |

### find_by_regex [¶](#scrapling.engines.toolbelt.custom.Response.find_by_regex "Permanent link")

```
find_by_regex(
    query,
    first_match=True,
    case_sensitive=False,
    clean_match=True,
)
```

Find elements that its text content matches the input regex pattern.

| PARAMETER | DESCRIPTION |
| --- | --- |
| `query` | Regex query/pattern to match  **TYPE:** `str | Pattern[str]` |
| `first_match` | Return the first element that matches conditions; enabled by default.  **TYPE:** `bool`  **DEFAULT:** `True` |
| `case_sensitive` | If enabled, the letters case will be taken into consideration in the regex.  **TYPE:** `bool`  **DEFAULT:** `False` |
| `clean_match` | If enabled, this will ignore all whitespaces and consecutive spaces while matching.  **TYPE:** `bool`  **DEFAULT:** `True` |

Source code in `scrapling/parser.py`

|  |  |
| --- | --- |
| ``` 1156 1157 1158 1159 1160 1161 1162 1163 1164 1165 1166 1167 1168 1169 1170 1171 1172 1173 1174 1175 1176 1177 1178 1179 1180 1181 1182 1183 1184 1185 1186 1187 1188 1189 1190 1191 1192 1193 ``` | ``` def find_by_regex(     self,     query: str | Pattern[str],     first_match: bool = True,     case_sensitive: bool = False,     clean_match: bool = True, ) -> Union["Selectors", "Selector"]:     """Find elements that its text content matches the input regex pattern.     :param query: Regex query/pattern to match     :param first_match: Return the first element that matches conditions; enabled by default.     :param case_sensitive: If enabled, the letters case will be taken into consideration in the regex.     :param clean_match: If enabled, this will ignore all whitespaces and consecutive spaces while matching.     """     if self._is_text_node(self._root):         return Selectors()      results = Selectors()      possible_targets = cast(List, _find_all_elements_with_spaces(self._root))     if possible_targets:         for node in self.__elements_convertor(possible_targets):             """Check if element matches given regex otherwise, traverse the children tree and iterate"""             node_text = node.text             if node_text.re(                 query,                 check_match=True,                 clean_match=clean_match,                 case_sensitive=case_sensitive,             ):                 results.append(node)              if first_match and results:                 # we got an element so we should stop                 break          if results and first_match:             return results[0]     return results ``` |

Was this page helpful?

Thanks for your feedback!

Thanks for your feedback! Help us improve this page by
[opening a documentation issue](https://github.com/D4Vinci/Scrapling/issues/new?template=04-docs_issue.yml).


---
## Source: https://scrapling.readthedocs.io/en/latest/api-reference/spiders.html
---

# Spider Classes[¶](#spider-classes "Permanent link")

Here's the reference information for the spider framework classes' parameters, attributes, and methods.

You can import them directly like below:

```
from scrapling.spiders import Spider, Request, CrawlResult, SessionManager, Response
```

## scrapling.spiders.Spider [¶](#scrapling.spiders.Spider "Permanent link")

```
Spider(crawldir=None, interval=300.0)
```

Bases: `ABC`

```
              flowchart TD
              scrapling.spiders.Spider[Spider]

              

              click scrapling.spiders.Spider href "" "scrapling.spiders.Spider"
```

An abstract base class for creating web spiders.

Check the documentation website for more information.

Initialize the spider.

| PARAMETER | DESCRIPTION |
| --- | --- |
| `crawldir` | Directory for checkpoint files. If provided, enables pause/resume.  **TYPE:** `Optional[Union[str, Path, Path]]`  **DEFAULT:** `None` |
| `interval` | Seconds between periodic checkpoint saves (default 5 minutes).  **TYPE:** `float`  **DEFAULT:** `300.0` |

Source code in `scrapling/spiders/spider.py`

|  |  |
| --- | --- |
| ```  92  93  94  95  96  97  98  99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 ``` | ``` def __init__(self, crawldir: Optional[Union[str, Path, AsyncPath]] = None, interval: float = 300.0):     """Initialize the spider.      :param crawldir: Directory for checkpoint files. If provided, enables pause/resume.     :param interval: Seconds between periodic checkpoint saves (default 5 minutes).     """     if self.name is None:         raise ValueError(f"{self.__class__.__name__} must have a name.")      self.logger = logging.getLogger(f"scrapling.spiders.{self.name}")     self.logger.setLevel(self.logging_level)     self.logger.handlers.clear()     self.logger.propagate = False  # Don't propagate to parent 'scrapling' logger      formatter = logging.Formatter(         fmt=self.logging_format.format(spider_name=self.name), datefmt=self.logging_date_format     )      # Add a log counter handler to track log counts by level     self._log_counter = LogCounterHandler()     self.logger.addHandler(self._log_counter)      console_handler = logging.StreamHandler()     console_handler.setFormatter(formatter)     self.logger.addHandler(console_handler)      if self.log_file:         Path(self.log_file).parent.mkdir(parents=True, exist_ok=True)         file_handler = logging.FileHandler(self.log_file)         file_handler.setFormatter(formatter)         self.logger.addHandler(file_handler)      self.crawldir: Optional[Path] = Path(crawldir) if crawldir else None     self._interval = interval     self._engine: Optional[CrawlerEngine] = None     self._original_sigint_handler: Any = None      self._session_manager = SessionManager()      try:         self.configure_sessions(self._session_manager)     except Exception as e:         raise SessionConfigurationError(f"Error in {self.__class__.__name__}.configure_sessions(): {e}") from e      if len(self._session_manager) == 0:         raise SessionConfigurationError(f"{self.__class__.__name__}.configure_sessions() did not add any sessions")      self.logger.info("Spider initialized") ``` |

### name `class-attribute` `instance-attribute` [¶](#scrapling.spiders.Spider.name "Permanent link")

```
name = None
```

### start_urls `class-attribute` `instance-attribute` [¶](#scrapling.spiders.Spider.start_urls "Permanent link")

```
start_urls = []
```

### allowed_domains `class-attribute` `instance-attribute` [¶](#scrapling.spiders.Spider.allowed_domains "Permanent link")

```
allowed_domains = set()
```

### concurrent_requests `class-attribute` `instance-attribute` [¶](#scrapling.spiders.Spider.concurrent_requests "Permanent link")

```
concurrent_requests = 4
```

### concurrent_requests_per_domain `class-attribute` `instance-attribute` [¶](#scrapling.spiders.Spider.concurrent_requests_per_domain "Permanent link")

```
concurrent_requests_per_domain = 0
```

### download_delay `class-attribute` `instance-attribute` [¶](#scrapling.spiders.Spider.download_delay "Permanent link")

```
download_delay = 0.0
```

### max_blocked_retries `class-attribute` `instance-attribute` [¶](#scrapling.spiders.Spider.max_blocked_retries "Permanent link")

```
max_blocked_retries = 3
```

### fp_include_kwargs `class-attribute` `instance-attribute` [¶](#scrapling.spiders.Spider.fp_include_kwargs "Permanent link")

```
fp_include_kwargs = False
```

### fp_keep_fragments `class-attribute` `instance-attribute` [¶](#scrapling.spiders.Spider.fp_keep_fragments "Permanent link")

```
fp_keep_fragments = False
```

### fp_include_headers `class-attribute` `instance-attribute` [¶](#scrapling.spiders.Spider.fp_include_headers "Permanent link")

```
fp_include_headers = False
```

### logging_level `class-attribute` `instance-attribute` [¶](#scrapling.spiders.Spider.logging_level "Permanent link")

```
logging_level = DEBUG
```

### logging_format `class-attribute` `instance-attribute` [¶](#scrapling.spiders.Spider.logging_format "Permanent link")

```
logging_format = "[%(asctime)s]:({spider_name}) %(levelname)s: %(message)s"
```

### logging_date_format `class-attribute` `instance-attribute` [¶](#scrapling.spiders.Spider.logging_date_format "Permanent link")

```
logging_date_format = '%Y-%m-%d %H:%M:%S'
```

### log_file `class-attribute` `instance-attribute` [¶](#scrapling.spiders.Spider.log_file "Permanent link")

```
log_file = None
```

### logger `instance-attribute` [¶](#scrapling.spiders.Spider.logger "Permanent link")

```
logger = getLogger(f'scrapling.spiders.{name}')
```

### crawldir `instance-attribute` [¶](#scrapling.spiders.Spider.crawldir "Permanent link")

```
crawldir = Path(crawldir) if crawldir else None
```

### stats `property` [¶](#scrapling.spiders.Spider.stats "Permanent link")

```
stats
```

Access current crawl stats (works during streaming).

### start_requests `async` [¶](#scrapling.spiders.Spider.start_requests "Permanent link")

```
start_requests()
```

Generate initial requests to start the crawl.

By default, this generates Request objects for each URL in `start_urls`
using the session manager's default session and `parse()` as callback.

Override this method for more control over initial requests
(e.g., to add custom headers, use different callbacks, etc.)

Source code in `scrapling/spiders/spider.py`

|  |  |
| --- | --- |
| ``` 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 ``` | ``` async def start_requests(self) -> AsyncGenerator[Request, None]:     """Generate initial requests to start the crawl.      By default, this generates Request objects for each URL in `start_urls`     using the session manager's default session and `parse()` as callback.      Override this method for more control over initial requests     (e.g., to add custom headers, use different callbacks, etc.)     """     if not self.start_urls:         raise RuntimeError(             "Spider has no starting point, either set `start_urls` or override `start_requests` function."         )      for url in self.start_urls:         yield Request(url, sid=self._session_manager.default_session_id) ``` |

### parse `abstractmethod` `async` [¶](#scrapling.spiders.Spider.parse "Permanent link")

```
parse(response)
```

Default callback for processing responses

Source code in `scrapling/spiders/spider.py`

|  |  |
| --- | --- |
| ``` 158 159 160 161 162 ``` | ``` @abstractmethod async def parse(self, response: "Response") -> AsyncGenerator[Dict[str, Any] | Request | None, None]:     """Default callback for processing responses"""     raise NotImplementedError(f"{self.__class__.__name__} must implement parse() method")     yield  # Make this a generator for type checkers ``` |

### on_start `async` [¶](#scrapling.spiders.Spider.on_start "Permanent link")

```
on_start(resuming=False)
```

Called before crawling starts. Override for setup logic.

| PARAMETER | DESCRIPTION |
| --- | --- |
| `resuming` | It's enabled if the spider is resuming from a checkpoint, left for the user to use.  **TYPE:** `bool`  **DEFAULT:** `False` |

Source code in `scrapling/spiders/spider.py`

|  |  |
| --- | --- |
| ``` 164 165 166 167 168 169 170 171 172 ``` | ``` async def on_start(self, resuming: bool = False) -> None:     """Called before crawling starts. Override for setup logic.      :param resuming: It's enabled if the spider is resuming from a checkpoint, left for the user to use.     """     if resuming:         self.logger.debug("Resuming spider from checkpoint")     else:         self.logger.debug("Starting spider") ``` |

### on_close `async` [¶](#scrapling.spiders.Spider.on_close "Permanent link")

```
on_close()
```

Called after crawling finishes. Override for cleanup logic.

Source code in `scrapling/spiders/spider.py`

|  |  |
| --- | --- |
| ``` 174 175 176 ``` | ``` async def on_close(self) -> None:     """Called after crawling finishes. Override for cleanup logic."""     self.logger.debug("Spider closed") ``` |

### on_error `async` [¶](#scrapling.spiders.Spider.on_error "Permanent link")

```
on_error(request, error)
```

Handle request errors for all spider requests.

Override for custom error handling.

Source code in `scrapling/spiders/spider.py`

|  |  |
| --- | --- |
| ``` 178 179 180 181 182 183 184 ``` | ``` async def on_error(self, request: Request, error: Exception) -> None:     """     Handle request errors for all spider requests.      Override for custom error handling.     """     pass ``` |

### on_scraped_item `async` [¶](#scrapling.spiders.Spider.on_scraped_item "Permanent link")

```
on_scraped_item(item)
```

A hook to be overridden by users to do some processing on scraped items, return `None` to drop the item silently.

Source code in `scrapling/spiders/spider.py`

|  |  |
| --- | --- |
| ``` 186 187 188 ``` | ``` async def on_scraped_item(self, item: Dict[str, Any]) -> Dict[str, Any] | None:     """A hook to be overridden by users to do some processing on scraped items, return `None` to drop the item silently."""     return item ``` |

### is_blocked `async` [¶](#scrapling.spiders.Spider.is_blocked "Permanent link")

```
is_blocked(response)
```

Check if the response is blocked. Users should override this for custom detection logic.

Source code in `scrapling/spiders/spider.py`

|  |  |
| --- | --- |
| ``` 190 191 192 193 194 ``` | ``` async def is_blocked(self, response: "Response") -> bool:     """Check if the response is blocked. Users should override this for custom detection logic."""     if response.status in BLOCKED_CODES:         return True     return False ``` |

### retry_blocked_request `async` [¶](#scrapling.spiders.Spider.retry_blocked_request "Permanent link")

```
retry_blocked_request(request, response)
```

Users should override this to prepare the blocked request before retrying, if needed.

Source code in `scrapling/spiders/spider.py`

|  |  |
| --- | --- |
| ``` 196 197 198 ``` | ``` async def retry_blocked_request(self, request: Request, response: "Response") -> Request:     """Users should override this to prepare the blocked request before retrying, if needed."""     return request ``` |

### __repr__ [¶](#scrapling.spiders.Spider.__repr__ "Permanent link")

```
__repr__()
```

String representation of the spider.

Source code in `scrapling/spiders/spider.py`

|  |  |
| --- | --- |
| ``` 200 201 202 ``` | ``` def __repr__(self) -> str:     """String representation of the spider."""     return f"<{self.__class__.__name__} '{self.name}'>" ``` |

### configure_sessions [¶](#scrapling.spiders.Spider.configure_sessions "Permanent link")

```
configure_sessions(manager)
```

Configure sessions for this spider.

Override this method to add custom sessions.
The default implementation creates a FetcherSession session.

The first session added becomes the default for `start_requests()` unless specified otherwise.

| PARAMETER | DESCRIPTION |
| --- | --- |
| `manager` | SessionManager to configure  **TYPE:** `SessionManager` |

Source code in `scrapling/spiders/spider.py`

|  |  |
| --- | --- |
| ``` 204 205 206 207 208 209 210 211 212 213 214 215 216 ``` | ``` def configure_sessions(self, manager: SessionManager) -> None:     """Configure sessions for this spider.      Override this method to add custom sessions.     The default implementation creates a FetcherSession session.      The first session added becomes the default for `start_requests()` unless specified otherwise.      :param manager: SessionManager to configure     """     from scrapling.fetchers import FetcherSession      manager.add("default", FetcherSession()) ``` |

### pause [¶](#scrapling.spiders.Spider.pause "Permanent link")

```
pause()
```

Request graceful shutdown of the crawling process.

Source code in `scrapling/spiders/spider.py`

|  |  |
| --- | --- |
| ``` 218 219 220 221 222 223 ``` | ``` def pause(self):     """Request graceful shutdown of the crawling process."""     if self._engine:         self._engine.request_pause()     else:         raise RuntimeError("No active crawl to stop") ``` |

### start [¶](#scrapling.spiders.Spider.start "Permanent link")

```
start(use_uvloop=False, **backend_options)
```

Run the spider and return results.

This is the main entry point for running a spider.
Handles async execution internally via anyio.

Pressing Ctrl+C will initiate graceful shutdown (waits for active tasks to complete).
Pressing Ctrl+C a second time will force immediate stop.

If crawldir is set, a checkpoint will also be saved on graceful shutdown,
allowing you to resume the crawl later by running the spider again.

| PARAMETER | DESCRIPTION |
| --- | --- |
| `use_uvloop` | Whether to use the faster uvloop/winloop event loop implementation, if available.  **TYPE:** `bool`  **DEFAULT:** `False` |
| `backend_options` | Asyncio backend options to be used with `anyio.run`  **TYPE:** `Any`  **DEFAULT:** `{}` |

Source code in `scrapling/spiders/spider.py`

|  |  |
| --- | --- |
| ``` 264 265 266 267 268 269 270 271 272 273 274 275 276 277 278 279 280 281 282 283 284 285 286 287 288 ``` | ``` def start(self, use_uvloop: bool = False, **backend_options: Any) -> CrawlResult:     """Run the spider and return results.      This is the main entry point for running a spider.     Handles async execution internally via anyio.      Pressing Ctrl+C will initiate graceful shutdown (waits for active tasks to complete).     Pressing Ctrl+C a second time will force immediate stop.      If crawldir is set, a checkpoint will also be saved on graceful shutdown,     allowing you to resume the crawl later by running the spider again.      :param use_uvloop: Whether to use the faster uvloop/winloop event loop implementation, if available.     :param backend_options: Asyncio backend options to be used with `anyio.run`     """     backend_options = backend_options or {}     if use_uvloop:         backend_options.update({"use_uvloop": True})      # Set up SIGINT handler for graceful shutdown     self._setup_signal_handler()     try:         return anyio.run(self.__run, backend="asyncio", backend_options=backend_options)     finally:         self._restore_signal_handler() ``` |

### stream `async` [¶](#scrapling.spiders.Spider.stream "Permanent link")

```
stream()
```

Stream items as they're scraped. Ideal for long-running spiders or building applications on top of the spiders.

Must be called from an async context. Yields items one by one as they are scraped.
Access `spider.stats` during iteration for real-time statistics.

Note: SIGINT handling for pause/resume is not available in stream mode.

Source code in `scrapling/spiders/spider.py`

|  |  |
| --- | --- |
| ``` 290 291 292 293 294 295 296 297 298 299 300 301 302 303 304 305 306 307 308 309 ``` | ``` async def stream(self) -> AsyncGenerator[Dict[str, Any], None]:     """Stream items as they're scraped. Ideal for long-running spiders or building applications on top of the spiders.      Must be called from an async context. Yields items one by one as they are scraped.     Access `spider.stats` during iteration for real-time statistics.      Note: SIGINT handling for pause/resume is not available in stream mode.     """     token = set_logger(self.logger)     try:         self._engine = CrawlerEngine(self, self._session_manager, self.crawldir, self._interval)         async for item in self._engine:             yield item     finally:         self._engine = None         reset_logger(token)         if self.log_file:             for handler in self.logger.handlers:                 if isinstance(handler, logging.FileHandler):                     handler.close() ``` |

## scrapling.spiders.Request [¶](#scrapling.spiders.Request "Permanent link")

```
Request(
    url,
    sid="",
    callback=None,
    priority=0,
    dont_filter=False,
    meta=None,
    _retry_count=0,
    **kwargs
)
```

Source code in `scrapling/spiders/request.py`

|  |  |
| --- | --- |
| ``` 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 ``` | ``` def __init__(     self,     url: str,     sid: str = "",     callback: Callable[[Response], AsyncGenerator[Union[Dict[str, Any], "Request", None], None]] | None = None,     priority: int = 0,     dont_filter: bool = False,     meta: dict[str, Any] | None = None,     _retry_count: int = 0,     **kwargs: Any, ) -> None:     self.url: str = url     self.sid: str = sid     self.callback = callback     self.priority: int = priority     self.dont_filter: bool = dont_filter     self.meta: dict[str, Any] = meta if meta else {}     self._retry_count: int = _retry_count     self._session_kwargs = kwargs if kwargs else {}     self._fp: Optional[bytes] = None ``` |

### url `instance-attribute` [¶](#scrapling.spiders.Request.url "Permanent link")

```
url = url
```

### sid `instance-attribute` [¶](#scrapling.spiders.Request.sid "Permanent link")

```
sid = sid
```

### callback `instance-attribute` [¶](#scrapling.spiders.Request.callback "Permanent link")

```
callback = callback
```

### priority `instance-attribute` [¶](#scrapling.spiders.Request.priority "Permanent link")

```
priority = priority
```

### dont_filter `instance-attribute` [¶](#scrapling.spiders.Request.dont_filter "Permanent link")

```
dont_filter = dont_filter
```

### meta `instance-attribute` [¶](#scrapling.spiders.Request.meta "Permanent link")

```
meta = meta if meta else {}
```

### domain `cached` `property` [¶](#scrapling.spiders.Request.domain "Permanent link")

```
domain
```

### copy [¶](#scrapling.spiders.Request.copy "Permanent link")

```
copy()
```

Create a copy of this request.

Source code in `scrapling/spiders/request.py`

|  |  |
| --- | --- |
| ``` 47 48 49 50 51 52 53 54 55 56 57 58 ``` | ``` def copy(self) -> "Request":     """Create a copy of this request."""     return Request(         url=self.url,         sid=self.sid,         callback=self.callback,         priority=self.priority,         dont_filter=self.dont_filter,         meta=self.meta.copy(),         _retry_count=self._retry_count,         **self._session_kwargs,     ) ``` |

### update_fingerprint [¶](#scrapling.spiders.Request.update_fingerprint "Permanent link")

```
update_fingerprint(
    include_kwargs=False,
    include_headers=False,
    keep_fragments=False,
)
```

Generate a unique fingerprint for deduplication.

Caches the result in self._fp after first computation.

Source code in `scrapling/spiders/request.py`

|  |  |
| --- | --- |
| ```  64  65  66  67  68  69  70  71  72  73  74  75  76  77  78  79  80  81  82  83  84  85  86  87  88  89  90  91  92  93  94  95  96  97  98  99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 ``` | ``` def update_fingerprint(     self,     include_kwargs: bool = False,     include_headers: bool = False,     keep_fragments: bool = False, ) -> bytes:     """Generate a unique fingerprint for deduplication.      Caches the result in self._fp after first computation.     """     if self._fp is not None:         return self._fp      post_data = self._session_kwargs.get("data", {})     body = b""     if post_data:         if isinstance(post_data, dict | list | tuple):             body = urlencode(post_data).encode()         elif isinstance(post_data, str):             body = post_data.encode()         elif isinstance(post_data, BytesIO):             body = post_data.getvalue()         elif isinstance(post_data, bytes):             body = post_data     else:         post_data = self._session_kwargs.get("json", {})         body = orjson.dumps(post_data) if post_data else b""      data: Dict[str, str | Tuple] = {         "sid": self.sid,         "body": body.hex(),         "method": self._session_kwargs.get("method", "GET"),         "url": canonicalize_url(self.url, keep_fragments=keep_fragments),     }      if include_kwargs:         kwargs = (key.lower() for key in self._session_kwargs.keys() if key.lower() not in ("data", "json"))         data["kwargs"] = "".join(set(_convert_to_bytes(key).hex() for key in kwargs))      if include_headers:         headers = self._session_kwargs.get("headers") or self._session_kwargs.get("extra_headers") or {}         processed_headers = {}         # Some header normalization         for key, value in headers.items():             processed_headers[_convert_to_bytes(key.lower()).hex()] = _convert_to_bytes(value.lower()).hex()         data["headers"] = tuple(processed_headers.items())      fp = hashlib.sha1(orjson.dumps(data, option=orjson.OPT_SORT_KEYS), usedforsecurity=False).digest()     self._fp = fp     return fp ``` |

### __repr__ [¶](#scrapling.spiders.Request.__repr__ "Permanent link")

```
__repr__()
```

Source code in `scrapling/spiders/request.py`

|  |  |
| --- | --- |
| ``` 115 116 117 ``` | ``` def __repr__(self) -> str:     callback_name = getattr(self.callback, "__name__", None) or "None"     return f"<Request({self.url}) priority={self.priority} callback={callback_name}>" ``` |

### __str__ [¶](#scrapling.spiders.Request.__str__ "Permanent link")

```
__str__()
```

Source code in `scrapling/spiders/request.py`

|  |  |
| --- | --- |
| ``` 119 120 ``` | ``` def __str__(self) -> str:     return self.url ``` |

### __lt__ [¶](#scrapling.spiders.Request.__lt__ "Permanent link")

```
__lt__(other)
```

Compare requests by priority

Source code in `scrapling/spiders/request.py`

|  |  |
| --- | --- |
| ``` 122 123 124 125 126 ``` | ``` def __lt__(self, other: object) -> bool:     """Compare requests by priority"""     if not isinstance(other, Request):         return NotImplemented     return self.priority < other.priority ``` |

### __gt__ [¶](#scrapling.spiders.Request.__gt__ "Permanent link")

```
__gt__(other)
```

Compare requests by priority

Source code in `scrapling/spiders/request.py`

|  |  |
| --- | --- |
| ``` 128 129 130 131 132 ``` | ``` def __gt__(self, other: object) -> bool:     """Compare requests by priority"""     if not isinstance(other, Request):         return NotImplemented     return self.priority > other.priority ``` |

### __eq__ [¶](#scrapling.spiders.Request.__eq__ "Permanent link")

```
__eq__(other)
```

Requests are equal if they have the same fingerprint.

Source code in `scrapling/spiders/request.py`

|  |  |
| --- | --- |
| ``` 134 135 136 137 138 139 140 ``` | ``` def __eq__(self, other: object) -> bool:     """Requests are equal if they have the same fingerprint."""     if not isinstance(other, Request):         return NotImplemented     if self._fp is None or other._fp is None:         raise RuntimeError("Cannot compare requests before generating their fingerprints!")     return self._fp == other._fp ``` |

### __getstate__ [¶](#scrapling.spiders.Request.__getstate__ "Permanent link")

```
__getstate__()
```

Prepare state for pickling - store callback as name string for pickle compatibility.

Source code in `scrapling/spiders/request.py`

|  |  |
| --- | --- |
| ``` 142 143 144 145 146 147 ``` | ``` def __getstate__(self) -> dict[str, Any]:     """Prepare state for pickling - store callback as name string for pickle compatibility."""     state = self.__dict__.copy()     state["_callback_name"] = getattr(self.callback, "__name__", None) if self.callback is not None else None     state["callback"] = None  # Don't pickle the actual callable     return state ``` |

### __setstate__ [¶](#scrapling.spiders.Request.__setstate__ "Permanent link")

```
__setstate__(state)
```

Restore state from pickle - callback restored later via _restore_callback().

Source code in `scrapling/spiders/request.py`

|  |  |
| --- | --- |
| ``` 149 150 151 152 ``` | ``` def __setstate__(self, state: dict[str, Any]) -> None:     """Restore state from pickle - callback restored later via _restore_callback()."""     self._callback_name: str | None = state.pop("_callback_name", None)     self.__dict__.update(state) ``` |

## Result Classes[¶](#result-classes "Permanent link")

## scrapling.spiders.result.CrawlResult `dataclass` [¶](#scrapling.spiders.result.CrawlResult "Permanent link")

```
CrawlResult(stats, items, paused=False)
```

Complete result from a spider run.

### stats `instance-attribute` [¶](#scrapling.spiders.result.CrawlResult.stats "Permanent link")

```
stats
```

### items `instance-attribute` [¶](#scrapling.spiders.result.CrawlResult.items "Permanent link")

```
items
```

### paused `class-attribute` `instance-attribute` [¶](#scrapling.spiders.result.CrawlResult.paused "Permanent link")

```
paused = False
```

### completed `property` [¶](#scrapling.spiders.result.CrawlResult.completed "Permanent link")

```
completed
```

True if the crawl completed normally (not paused).

### __len__ [¶](#scrapling.spiders.result.CrawlResult.__len__ "Permanent link")

```
__len__()
```

Source code in `scrapling/spiders/result.py`

|  |  |
| --- | --- |
| ``` 121 122 ``` | ``` def __len__(self) -> int:     return len(self.items) ``` |

### __iter__ [¶](#scrapling.spiders.result.CrawlResult.__iter__ "Permanent link")

```
__iter__()
```

Source code in `scrapling/spiders/result.py`

|  |  |
| --- | --- |
| ``` 124 125 ``` | ``` def __iter__(self) -> Iterator[dict[str, Any]]:     return iter(self.items) ``` |

## scrapling.spiders.result.CrawlStats `dataclass` [¶](#scrapling.spiders.result.CrawlStats "Permanent link")

```
CrawlStats(
    requests_count=0,
    concurrent_requests=0,
    concurrent_requests_per_domain=0,
    failed_requests_count=0,
    offsite_requests_count=0,
    response_bytes=0,
    items_scraped=0,
    items_dropped=0,
    start_time=0.0,
    end_time=0.0,
    download_delay=0.0,
    blocked_requests_count=0,
    custom_stats=dict(),
    response_status_count=dict(),
    domains_response_bytes=dict(),
    sessions_requests_count=dict(),
    proxies=list(),
    log_levels_counter=dict(),
)
```

Statistics for a crawl run.

### requests_count `class-attribute` `instance-attribute` [¶](#scrapling.spiders.result.CrawlStats.requests_count "Permanent link")

```
requests_count = 0
```

### concurrent_requests `class-attribute` `instance-attribute` [¶](#scrapling.spiders.result.CrawlStats.concurrent_requests "Permanent link")

```
concurrent_requests = 0
```

### concurrent_requests_per_domain `class-attribute` `instance-attribute` [¶](#scrapling.spiders.result.CrawlStats.concurrent_requests_per_domain "Permanent link")

```
concurrent_requests_per_domain = 0
```

### failed_requests_count `class-attribute` `instance-attribute` [¶](#scrapling.spiders.result.CrawlStats.failed_requests_count "Permanent link")

```
failed_requests_count = 0
```

### offsite_requests_count `class-attribute` `instance-attribute` [¶](#scrapling.spiders.result.CrawlStats.offsite_requests_count "Permanent link")

```
offsite_requests_count = 0
```

### response_bytes `class-attribute` `instance-attribute` [¶](#scrapling.spiders.result.CrawlStats.response_bytes "Permanent link")

```
response_bytes = 0
```

### items_scraped `class-attribute` `instance-attribute` [¶](#scrapling.spiders.result.CrawlStats.items_scraped "Permanent link")

```
items_scraped = 0
```

### items_dropped `class-attribute` `instance-attribute` [¶](#scrapling.spiders.result.CrawlStats.items_dropped "Permanent link")

```
items_dropped = 0
```

### start_time `class-attribute` `instance-attribute` [¶](#scrapling.spiders.result.CrawlStats.start_time "Permanent link")

```
start_time = 0.0
```

### end_time `class-attribute` `instance-attribute` [¶](#scrapling.spiders.result.CrawlStats.end_time "Permanent link")

```
end_time = 0.0
```

### download_delay `class-attribute` `instance-attribute` [¶](#scrapling.spiders.result.CrawlStats.download_delay "Permanent link")

```
download_delay = 0.0
```

### blocked_requests_count `class-attribute` `instance-attribute` [¶](#scrapling.spiders.result.CrawlStats.blocked_requests_count "Permanent link")

```
blocked_requests_count = 0
```

### custom_stats `class-attribute` `instance-attribute` [¶](#scrapling.spiders.result.CrawlStats.custom_stats "Permanent link")

```
custom_stats = field(default_factory=dict)
```

### response_status_count `class-attribute` `instance-attribute` [¶](#scrapling.spiders.result.CrawlStats.response_status_count "Permanent link")

```
response_status_count = field(default_factory=dict)
```

### domains_response_bytes `class-attribute` `instance-attribute` [¶](#scrapling.spiders.result.CrawlStats.domains_response_bytes "Permanent link")

```
domains_response_bytes = field(default_factory=dict)
```

### sessions_requests_count `class-attribute` `instance-attribute` [¶](#scrapling.spiders.result.CrawlStats.sessions_requests_count "Permanent link")

```
sessions_requests_count = field(default_factory=dict)
```

### proxies `class-attribute` `instance-attribute` [¶](#scrapling.spiders.result.CrawlStats.proxies "Permanent link")

```
proxies = field(default_factory=list)
```

### log_levels_counter `class-attribute` `instance-attribute` [¶](#scrapling.spiders.result.CrawlStats.log_levels_counter "Permanent link")

```
log_levels_counter = field(default_factory=dict)
```

### elapsed_seconds `property` [¶](#scrapling.spiders.result.CrawlStats.elapsed_seconds "Permanent link")

```
elapsed_seconds
```

### requests_per_second `property` [¶](#scrapling.spiders.result.CrawlStats.requests_per_second "Permanent link")

```
requests_per_second
```

### increment_status [¶](#scrapling.spiders.result.CrawlStats.increment_status "Permanent link")

```
increment_status(status)
```

Source code in `scrapling/spiders/result.py`

|  |  |
| --- | --- |
| ``` 74 75 ``` | ``` def increment_status(self, status: int) -> None:     self.response_status_count[f"status_{status}"] = self.response_status_count.get(f"status_{status}", 0) + 1 ``` |

### increment_response_bytes [¶](#scrapling.spiders.result.CrawlStats.increment_response_bytes "Permanent link")

```
increment_response_bytes(domain, count)
```

Source code in `scrapling/spiders/result.py`

|  |  |
| --- | --- |
| ``` 77 78 79 ``` | ``` def increment_response_bytes(self, domain: str, count: int) -> None:     self.response_bytes += count     self.domains_response_bytes[domain] = self.domains_response_bytes.get(domain, 0) + count ``` |

### increment_requests_count [¶](#scrapling.spiders.result.CrawlStats.increment_requests_count "Permanent link")

```
increment_requests_count(sid)
```

Source code in `scrapling/spiders/result.py`

|  |  |
| --- | --- |
| ``` 81 82 83 ``` | ``` def increment_requests_count(self, sid: str) -> None:     self.requests_count += 1     self.sessions_requests_count[sid] = self.sessions_requests_count.get(sid, 0) + 1 ``` |

### to_dict [¶](#scrapling.spiders.result.CrawlStats.to_dict "Permanent link")

```
to_dict()
```

Source code in `scrapling/spiders/result.py`

|  |  |
| --- | --- |
| ```  85  86  87  88  89  90  91  92  93  94  95  96  97  98  99 100 101 102 103 104 105 ``` | ``` def to_dict(self) -> dict[str, Any]:     return {         "items_scraped": self.items_scraped,         "items_dropped": self.items_dropped,         "elapsed_seconds": round(self.elapsed_seconds, 2),         "download_delay": round(self.download_delay, 2),         "concurrent_requests": self.concurrent_requests,         "concurrent_requests_per_domain": self.concurrent_requests_per_domain,         "requests_count": self.requests_count,         "requests_per_second": round(self.requests_per_second, 2),         "sessions_requests_count": self.sessions_requests_count,         "failed_requests_count": self.failed_requests_count,         "offsite_requests_count": self.offsite_requests_count,         "blocked_requests_count": self.blocked_requests_count,         "response_status_count": self.response_status_count,         "response_bytes": self.response_bytes,         "domains_response_bytes": self.domains_response_bytes,         "proxies": self.proxies,         "custom_stats": self.custom_stats,         "log_count": self.log_levels_counter,     } ``` |

## scrapling.spiders.result.ItemList [¶](#scrapling.spiders.result.ItemList "Permanent link")

Bases: `list`

```
              flowchart TD
              scrapling.spiders.result.ItemList[ItemList]

              

              click scrapling.spiders.result.ItemList href "" "scrapling.spiders.result.ItemList"
```

A list of scraped items with export capabilities.

### to_json [¶](#scrapling.spiders.result.ItemList.to_json "Permanent link")

```
to_json(path, *, indent=False)
```

Export items to a JSON file.

| PARAMETER | DESCRIPTION |
| --- | --- |
| `path` | Path to the output file  **TYPE:** `Union[str, Path]` |
| `indent` | Pretty-print with 2-space indentation (slightly slower)  **TYPE:** `bool`  **DEFAULT:** `False` |

Source code in `scrapling/spiders/result.py`

|  |  |
| --- | --- |
| ``` 13 14 15 16 17 18 19 20 21 22 23 24 25 26 ``` | ``` def to_json(self, path: Union[str, Path], *, indent: bool = False):     """Export items to a JSON file.      :param path: Path to the output file     :param indent: Pretty-print with 2-space indentation (slightly slower)     """     options = orjson.OPT_SERIALIZE_NUMPY     if indent:         options |= orjson.OPT_INDENT_2      file = Path(path)     file.parent.mkdir(parents=True, exist_ok=True)     file.write_bytes(orjson.dumps(list(self), option=options))     log.info("Saved %d items to %s", len(self), path) ``` |

### to_jsonl [¶](#scrapling.spiders.result.ItemList.to_jsonl "Permanent link")

```
to_jsonl(path)
```

Export items as JSON Lines (one JSON object per line).

| PARAMETER | DESCRIPTION |
| --- | --- |
| `path` | Path to the output file  **TYPE:** `Union[str, Path]` |

Source code in `scrapling/spiders/result.py`

|  |  |
| --- | --- |
| ``` 28 29 30 31 32 33 34 35 36 37 38 ``` | ``` def to_jsonl(self, path: Union[str, Path]):     """Export items as JSON Lines (one JSON object per line).      :param path: Path to the output file     """     Path(path).parent.mkdir(parents=True, exist_ok=True)     with open(path, "wb") as f:         for item in self:             f.write(orjson.dumps(item, option=orjson.OPT_SERIALIZE_NUMPY))             f.write(b"\n")     log.info("Saved %d items to %s", len(self), path) ``` |

## Session Management[¶](#session-management "Permanent link")

## scrapling.spiders.session.SessionManager [¶](#scrapling.spiders.session.SessionManager "Permanent link")

```
SessionManager()
```

Manages pre-configured session instances.

Source code in `scrapling/spiders/session.py`

|  |  |
| --- | --- |
| ``` 15 16 17 18 19 20 ``` | ``` def __init__(self) -> None:     self._sessions: dict[str, Session] = {}     self._default_session_id: str | None = None     self._started: bool = False     self._lazy_sessions: Set[str] = set()     self._lazy_lock = Lock() ``` |

### default_session_id `property` [¶](#scrapling.spiders.session.SessionManager.default_session_id "Permanent link")

```
default_session_id
```

### session_ids `property` [¶](#scrapling.spiders.session.SessionManager.session_ids "Permanent link")

```
session_ids
```

### add [¶](#scrapling.spiders.session.SessionManager.add "Permanent link")

```
add(session_id, session, *, default=False, lazy=False)
```

Register a session instance.

| PARAMETER | DESCRIPTION |
| --- | --- |
| `session_id` | Name to reference this session in requests  **TYPE:** `str` |
| `session` | Your pre-configured session instance  **TYPE:** `Session` |
| `default` | If True, this becomes the default session  **TYPE:** `bool`  **DEFAULT:** `False` |
| `lazy` | If True, the session will be started only when a request uses its ID.  **TYPE:** `bool`  **DEFAULT:** `False` |

Source code in `scrapling/spiders/session.py`

|  |  |
| --- | --- |
| ``` 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 ``` | ``` def add(self, session_id: str, session: Session, *, default: bool = False, lazy: bool = False) -> "SessionManager":     """Register a session instance.      :param session_id: Name to reference this session in requests     :param session: Your pre-configured session instance     :param default: If True, this becomes the default session     :param lazy: If True, the session will be started only when a request uses its ID.     """     if session_id in self._sessions:         raise ValueError(f"Session '{session_id}' already registered")      self._sessions[session_id] = session      if default or self._default_session_id is None:         self._default_session_id = session_id      if lazy:         self._lazy_sessions.add(session_id)      return self ``` |

### remove [¶](#scrapling.spiders.session.SessionManager.remove "Permanent link")

```
remove(session_id)
```

Removes a session.

| PARAMETER | DESCRIPTION |
| --- | --- |
| `session_id` | ID of session to remove  **TYPE:** `str` |

Source code in `scrapling/spiders/session.py`

|  |  |
| --- | --- |
| ``` 43 44 45 46 47 48 ``` | ``` def remove(self, session_id: str) -> None:     """Removes a session.      :param session_id: ID of session to remove     """     _ = self.pop(session_id) ``` |

### pop [¶](#scrapling.spiders.session.SessionManager.pop "Permanent link")

```
pop(session_id)
```

Remove and returns a session.

| PARAMETER | DESCRIPTION |
| --- | --- |
| `session_id` | ID of session to remove  **TYPE:** `str` |

Source code in `scrapling/spiders/session.py`

|  |  |
| --- | --- |
| ``` 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 ``` | ``` def pop(self, session_id: str) -> Session:     """Remove and returns a session.      :param session_id: ID of session to remove     """     if session_id not in self._sessions:         raise KeyError(f"Session '{session_id}' not found")      session = self._sessions.pop(session_id)     if session_id in self._lazy_sessions:         self._lazy_sessions.remove(session_id)      if session and self._default_session_id == session_id:         self._default_session_id = next(iter(self._sessions), None)      return session ``` |

### get [¶](#scrapling.spiders.session.SessionManager.get "Permanent link")

```
get(session_id)
```

Source code in `scrapling/spiders/session.py`

|  |  |
| --- | --- |
| ``` 77 78 79 80 81 ``` | ``` def get(self, session_id: str) -> Session:     if session_id not in self._sessions:         available = ", ".join(self._sessions.keys())         raise KeyError(f"Session '{session_id}' not found. Available: {available}")     return self._sessions[session_id] ``` |

### start `async` [¶](#scrapling.spiders.session.SessionManager.start "Permanent link")

```
start()
```

Start all sessions that aren't already alive.

Source code in `scrapling/spiders/session.py`

|  |  |
| --- | --- |
| ``` 83 84 85 86 87 88 89 90 91 92 ``` | ``` async def start(self) -> None:     """Start all sessions that aren't already alive."""     if self._started:         return      for sid, session in self._sessions.items():         if sid not in self._lazy_sessions and not session._is_alive:             await session.__aenter__()      self._started = True ``` |

### close `async` [¶](#scrapling.spiders.session.SessionManager.close "Permanent link")

```
close()
```

Close all registered sessions.

Source code in `scrapling/spiders/session.py`

|  |  |
| --- | --- |
| ``` 94 95 96 97 98 99 ``` | ``` async def close(self) -> None:     """Close all registered sessions."""     for session in self._sessions.values():         _ = await session.__aexit__(None, None, None)      self._started = False ``` |

### fetch `async` [¶](#scrapling.spiders.session.SessionManager.fetch "Permanent link")

```
fetch(request)
```

Source code in `scrapling/spiders/session.py`

|  |  |
| --- | --- |
| ``` 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 ``` | ``` async def fetch(self, request: Request) -> Response:     sid = request.sid if request.sid else self.default_session_id     session = self.get(sid)      if session:         if sid in self._lazy_sessions and not session._is_alive:             async with self._lazy_lock:                 if not session._is_alive:                     await session.__aenter__()          if isinstance(session, FetcherSession):             client = session._client              if isinstance(client, _ASyncSessionLogic):                 kwargs = request._session_kwargs.copy()                 method = cast(SUPPORTED_HTTP_METHODS, kwargs.pop("method", "GET"))                 response = await client._make_request(                     method=method,                     url=request.url,                     **kwargs,                 )             else:                 # Sync session or other types - shouldn't happen in async context                 raise TypeError(f"Session type {type(client)} not supported for async fetch")         else:             response = await session.fetch(url=request.url, **request._session_kwargs)          response.request = request         # Merge request meta into response meta (response meta takes priority)         response.meta = {**request.meta, **response.meta}         return response     raise RuntimeError("No session found with the request session id") ``` |

### __aenter__ `async` [¶](#scrapling.spiders.session.SessionManager.__aenter__ "Permanent link")

```
__aenter__()
```

Source code in `scrapling/spiders/session.py`

|  |  |
| --- | --- |
| ``` 134 135 136 ``` | ``` async def __aenter__(self) -> "SessionManager":     await self.start()     return self ``` |

### __aexit__ `async` [¶](#scrapling.spiders.session.SessionManager.__aexit__ "Permanent link")

```
__aexit__(*exc)
```

Source code in `scrapling/spiders/session.py`

|  |  |
| --- | --- |
| ``` 138 139 ``` | ``` async def __aexit__(self, *exc) -> None:     await self.close() ``` |

### __contains__ [¶](#scrapling.spiders.session.SessionManager.__contains__ "Permanent link")

```
__contains__(session_id)
```

Check if a session ID is registered.

Source code in `scrapling/spiders/session.py`

|  |  |
| --- | --- |
| ``` 141 142 143 ``` | ``` def __contains__(self, session_id: str) -> bool:     """Check if a session ID is registered."""     return session_id in self._sessions ``` |

### __len__ [¶](#scrapling.spiders.session.SessionManager.__len__ "Permanent link")

```
__len__()
```

Number of registered sessions.

Source code in `scrapling/spiders/session.py`

|  |  |
| --- | --- |
| ``` 145 146 147 ``` | ``` def __len__(self) -> int:     """Number of registered sessions."""     return len(self._sessions) ``` |

Was this page helpful?

Thanks for your feedback!

Thanks for your feedback! Help us improve this page by
[opening a documentation issue](https://github.com/D4Vinci/Scrapling/issues/new?template=04-docs_issue.yml).


---
## Source: https://scrapling.readthedocs.io/en/latest/api-reference/proxy-rotation.html
---

# Proxy Rotation[¶](#proxy-rotation "Permanent link")

The `ProxyRotator` class provides thread-safe proxy rotation for any fetcher or session.

You can import it directly like below:

```
from scrapling.fetchers import ProxyRotator
```

## scrapling.engines.toolbelt.proxy_rotation.ProxyRotator [¶](#scrapling.engines.toolbelt.proxy_rotation.ProxyRotator "Permanent link")

```
ProxyRotator(proxies, strategy=cyclic_rotation)
```

A thread-safe proxy rotator with pluggable rotation strategies.

Supports:
- Cyclic rotation (default)
- Custom rotation strategies via callable
- Both string URLs and Playwright-style dict proxies

Initialize the proxy rotator.

| PARAMETER | DESCRIPTION |
| --- | --- |
| `proxies` | List of proxy URLs or Playwright-style proxy dicts. - String format: "http://proxy1:8080" or "http://user:pass@proxy:8080" - Dict format: {"server": "http://proxy:8080", "username": "user", "password": "pass"}  **TYPE:** `List[ProxyType]` |
| `strategy` | Rotation strategy function. Takes (proxies, current_index) and returns (proxy, next_index). Defaults to cyclic_rotation.  **TYPE:** `RotationStrategy`  **DEFAULT:** `cyclic_rotation` |

Source code in `scrapling/engines/toolbelt/proxy_rotation.py`

|  |  |
| --- | --- |
| ``` 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 ``` | ``` def __init__(     self,     proxies: List[ProxyType],     strategy: RotationStrategy = cyclic_rotation, ):     """     Initialize the proxy rotator.      :param proxies: List of proxy URLs or Playwright-style proxy dicts.         - String format: "http://proxy1:8080" or "http://user:pass@proxy:8080"         - Dict format: {"server": "http://proxy:8080", "username": "user", "password": "pass"}     :param strategy: Rotation strategy function. Takes (proxies, current_index) and returns (proxy, next_index). Defaults to cyclic_rotation.     """     if not proxies:         raise ValueError("At least one proxy must be provided")      if not callable(strategy):         raise TypeError(f"strategy must be callable, got {type(strategy).__name__}")      self._strategy = strategy     self._lock = Lock()      # Validate and store proxies     self._proxies: List[ProxyType] = []     self._proxy_to_index: Dict[str, int] = {}  # O(1) lookup by unique key (server + username)     for i, proxy in enumerate(proxies):         if isinstance(proxy, (str, dict)):             if isinstance(proxy, dict) and "server" not in proxy:                 raise ValueError("Proxy dict must have a 'server' key")              self._proxy_to_index[_get_proxy_key(proxy)] = i             self._proxies.append(proxy)         else:             raise TypeError(f"Invalid proxy type: {type(proxy)}. Expected str or dict.")      self._current_index = 0 ``` |

### __slots__ `class-attribute` `instance-attribute` [¶](#scrapling.engines.toolbelt.proxy_rotation.ProxyRotator.__slots__ "Permanent link")

```
__slots__ = (
    "_proxies",
    "_proxy_to_index",
    "_strategy",
    "_current_index",
    "_lock",
)
```

### proxies `property` [¶](#scrapling.engines.toolbelt.proxy_rotation.ProxyRotator.proxies "Permanent link")

```
proxies
```

Get a copy of all configured proxies.

### get_proxy [¶](#scrapling.engines.toolbelt.proxy_rotation.ProxyRotator.get_proxy "Permanent link")

```
get_proxy()
```

Get the next proxy according to the rotation strategy.

Source code in `scrapling/engines/toolbelt/proxy_rotation.py`

|  |  |
| --- | --- |
| ``` 88 89 90 91 92 ``` | ``` def get_proxy(self) -> ProxyType:     """Get the next proxy according to the rotation strategy."""     with self._lock:         proxy, self._current_index = self._strategy(self._proxies, self._current_index)         return proxy ``` |

### __len__ [¶](#scrapling.engines.toolbelt.proxy_rotation.ProxyRotator.__len__ "Permanent link")

```
__len__()
```

Return the total number of configured proxies.

Source code in `scrapling/engines/toolbelt/proxy_rotation.py`

|  |  |
| --- | --- |
| ```  99 100 101 ``` | ``` def __len__(self) -> int:     """Return the total number of configured proxies."""     return len(self._proxies) ``` |

### __repr__ [¶](#scrapling.engines.toolbelt.proxy_rotation.ProxyRotator.__repr__ "Permanent link")

```
__repr__()
```

Source code in `scrapling/engines/toolbelt/proxy_rotation.py`

|  |  |
| --- | --- |
| ``` 103 104 ``` | ``` def __repr__(self) -> str:     return f"ProxyRotator(proxies={len(self._proxies)})" ``` |

Was this page helpful?

Thanks for your feedback!

Thanks for your feedback! Help us improve this page by
[opening a documentation issue](https://github.com/D4Vinci/Scrapling/issues/new?template=04-docs_issue.yml).


---
## Source: https://scrapling.readthedocs.io/en/latest/development/adaptive_storage_system.html
---

# Writing your retrieval system[¶](#writing-your-retrieval-system "Permanent link")

Scrapling uses SQLite by default, but this tutorial shows how to write your own storage system to store element properties for the `adaptive` feature.

You might want to use Firebase, for example, and share the database between multiple spiders on different machines. It's a great idea to use an online database like that because spiders can share adaptive data with each other.

So first, to make your storage class work, it must do the big 3:

1. Inherit from the abstract class `scrapling.core.storage.StorageSystemMixin` and accept a string argument, which will be the `url` argument to maintain the library logic.
2. Use the decorator `functools.lru_cache` on top of the class to follow the Singleton design pattern as other classes.
3. Implement methods `save` and `retrieve`, as you see from the type hints:
   * The method `save` returns nothing and will get two arguments from the library
     + The first one is of type `lxml.html.HtmlElement`, which is the element itself. It must be converted to a dictionary using the `element_to_dict` function in the submodule `scrapling.core.utils._StorageTools` to maintain the same format, and then saved to your database as you wish.
     + The second one is a string, the identifier used for retrieval. The combination result of this identifier and the `url` argument from initialization must be unique for each row, or the `adaptive` data will be messed up.
   * The method `retrieve` takes a string, which is the identifier; using it with the `url` passed on initialization, the element's dictionary is retrieved from the database and returned if it exists; otherwise, it returns `None`.

> If the instructions weren't clear enough for you, you can check my implementation using SQLite3 in [storage_adaptors](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/core/storage.py) file

If your class meets these criteria, the rest is straightforward. If you plan to use the library in a threaded application, ensure your class supports it. The default used class is thread-safe.

Some helper functions are added to the abstract class if you want to use them. It's easier to see it for yourself in the [code](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/core/storage.py); it's heavily commented :)

## Real-World Example: Redis Storage[¶](#real-world-example-redis-storage "Permanent link")

Here's a more practical example generated by AI using Redis:

```
import redis
import orjson
from functools import lru_cache
from scrapling.core.storage import StorageSystemMixin
from scrapling.core.utils import _StorageTools

@lru_cache(None)
class RedisStorage(StorageSystemMixin):
    def __init__(self, host='localhost', port=6379, db=0, url=None):
        super().__init__(url)
        self.redis = redis.Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=False
        )

    def save(self, element, identifier: str) -> None:
        # Convert element to dictionary
        element_dict = _StorageTools.element_to_dict(element)

        # Create key
        key = f"scrapling:{self._get_base_url()}:{identifier}"

        # Store as JSON
        self.redis.set(
            key,
            orjson.dumps(element_dict)
        )

    def retrieve(self, identifier: str) -> dict | None:
        # Get data
        key = f"scrapling:{self._get_base_url()}:{identifier}"
        data = self.redis.get(key)

        # Parse JSON if exists
        if data:
            return orjson.loads(data)
        return None
```

Was this page helpful?

Thanks for your feedback!

Thanks for your feedback! Help us improve this page by
[opening a documentation issue](https://github.com/D4Vinci/Scrapling/issues/new?template=04-docs_issue.yml).


---
## Source: https://scrapling.readthedocs.io/en/latest/development/scrapling_custom_types.html
---

# Using Scrapling's custom types[¶](#using-scraplings-custom-types "Permanent link")

> You can take advantage of the custom-made types for Scrapling and use them outside the library if you want. It's better than copying their code, after all :)

### All current types can be imported alone, like below[¶](#all-current-types-can-be-imported-alone-like-below "Permanent link")

```
>>> from scrapling.core.custom_types import TextHandler, AttributesHandler

>>> somestring = TextHandler('{}')
>>> somestring.json()
'{}'
>>> somedict_1 = AttributesHandler({'a': 1})
>>> somedict_2 = AttributesHandler(a=1)
```

Note that `TextHandler` is a subclass of Python's `str`, so all standard operations/methods that work with Python strings will work.
If you want to check the type in your code, it's better to use Python's built-in `issubclass` function.

The class `AttributesHandler` is a subclass of `collections.abc.Mapping`, so it's immutable (read-only), and all operations are inherited from it. The data passed can be accessed later through the `_data` property, but be careful; it's of type `types.MappingProxyType`, so it's immutable (read-only) as well (faster than `collections.abc.Mapping` by fractions of seconds).

So, to make it simple for you, if you are new to Python, the same operations and methods from the Python standard `dict` type will all work with the class `AttributesHandler` except for the ones that try to modify the actual data.

If you want to modify the data inside `AttributesHandler`, you have to convert it to a dictionary first, e.g., using the `dict` function, and then change it outside.

Was this page helpful?

Thanks for your feedback!

Thanks for your feedback! Help us improve this page by
[opening a documentation issue](https://github.com/D4Vinci/Scrapling/issues/new?template=04-docs_issue.yml).


---
## Source: https://scrapling.readthedocs.io/en/latest/donate.html
---

# Donate

I've been creating all of these projects in my spare time and have invested considerable resources & effort in providing them to the community for free. By becoming a sponsor, you'd be directly funding my coffee reserves, helping me fulfill my responsibilities, and enabling me to continuously update existing projects and potentially create new ones.

You can sponsor me directly through the [GitHub Sponsors program](https://github.com/sponsors/D4Vinci) or [Buy Me a Coffee](https://buymeacoffee.com/d4vinci).

Thank you, stay curious, and hack the planet! ❤️

## Advertisement[¶](#advertisement "Permanent link")

If you are looking to **advertise** your business to our target audience, check out the [available tiers](https://github.com/sponsors/D4Vinci):

### 1. [The Silver tier](https://github.com/sponsors/D4Vinci/sponsorships?tier_id=435495) ($100/month)[¶](#1-the-silver-tier-100month "Permanent link")

Perks:

1. Your logo will be featured at [the top of Scrapling's project page](https://github.com/D4Vinci/Scrapling?tab=readme-ov-file#sponsors).
2. The same logo will be featured at [the top of Scrapling's PyPI page](https://pypi.org/project/scrapling/) and [the top of Docker's image page](https://hub.docker.com/r/pyd4vinci/scrapling), the same way it was placed on the project's page.

### 2. [The Gold tier](https://github.com/sponsors/D4Vinci/sponsorships?tier_id=591422) ($200/month)[¶](#2-the-gold-tier-200month "Permanent link")

Perks:

1. Your logo will be featured at [the top of Scrapling's project page](https://github.com/D4Vinci/Scrapling?tab=readme-ov-file#sponsors).
2. The same logo will be featured at [the top of Scrapling's PyPI page](https://pypi.org/project/scrapling/) and [the top of Docker's image page](https://hub.docker.com/r/pyd4vinci/scrapling), the same way it was placed on the project's page.
3. Your logo will be featured as a top sponsor on [Scrapling's website](https://scrapling.readthedocs.io/en/latest/) main page.

### 3. [The Platinum tier](https://github.com/sponsors/D4Vinci/sponsorships?tier_id=586646) ($300/month)[¶](#3-the-platinum-tier-300month "Permanent link")

Perks:

1. Your logo will have a special placement at [the very top of Scrapling's project page](https://github.com/D4Vinci/Scrapling?tab=readme-ov-file#platinum-sponsors) with a 25-word paragraph or less.
2. The same logo will be featured at [the PyPI page](https://pypi.org/project/scrapling/)/[the Docker page](https://hub.docker.com/r/pyd4vinci/scrapling), the same way it was placed on the project's page.
3. A special placement for your logo as a top sponsor on [Scrapling's website](https://scrapling.readthedocs.io/en/latest/) main page.
4. A partner role at our Discord server and an announcement on the Twitter page and the Discord server.
5. A Shoutout at the end of each Release notes.

Was this page helpful?

Thanks for your feedback!

Thanks for your feedback! Help us improve this page by
[opening a documentation issue](https://github.com/D4Vinci/Scrapling/issues/new?template=04-docs_issue.yml).
