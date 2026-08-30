#!/usr/bin/env python3
import json

# Build the complete lesson data structure
lesson = {
    "slug": "fourth-wave",
    "date": "2026-08-31",
    "subject": "feminism",
    "related": ["first-wave", "second-wave", "third-wave"],
    "title": "Fourth Wave (c. 2010s–): when the machine was the hashtag",
    "dek": "A Toronto police officer's comment, a British website for everyday stories, Tarana Burke's phrase from 2006, and two 2017 investigations made hashtag feminism look global and instant. The wave number came after. The activism was not one platform.",
    "era": "c. early 2010s–",
    "reading_minutes": 19,
    "thumb": {
        "src": "lessons/fourth-wave/womens-march-2017.jpg",
        "alt": "Aerial view of massive crowd at Women's March on Washington, January 21, 2017."
    },
    "hero": {
        "src": "lessons/fourth-wave/womens-march-2017.jpg",
        "alt": "Wide photograph of the Women's March on Washington filling streets near the Capitol, January 21, 2017. Massive crowds stretch into the distance, many wearing pink hats, holding signs.",
        "caption": "The Women's March on Washington, 21 January 2017, the day after Donald Trump's inauguration. An estimated 500,000 people gathered in Washington, with millions more in sister marches worldwide. This is a demonstration of scale, not a picture of the hashtag that would follow in October. The march is its own fact: women and allies in the streets, visible and counted.",
        "credit": "Rosa Pineda / Wikimedia Commons / CC BY-SA 4.0",
        "credit_url": "https://commons.wikimedia.org/wiki/File:Women%27s_March_Washington,_DC_USA_41.jpg"
    },
    "honesty": '"Fourth wave" is a later Anglo-American journalistic and classroom name, not what most participants called themselves in 2012 or 2017. The machine that changed was digital: smartphones, Twitter, Facebook, Instagram, later TikTok. Dates are conveniences: Toronto SlutWalk in 2011, the Everyday Sexism Project in 2012, Burke Me Too from 2006, the 2017 Weinstein reporting, Women March in January 2017. Many contemporary photographs are still in copyright or require model releases. The images here are free-licensed or public-domain: a 2017 march, a 2011 SlutWalk. Where a usable photograph could not be found, the lesson names the event without a picture. This lesson cannot show you a viral tweet or a hashtag cascade, only that they happened and what came before and after.',
    "timeline": [],
    "watch": [],
    "listen": [],
    "read": [],
    "fun_fact": {
        "title": "Test",
        "text": "Test"
    },
    "glossary": [],
    "sections": []
}

# Write to file
with open('content/lessons/2026-08-31-fourth-wave.json', 'w', encoding='utf-8') as f:
    json.dump(lesson, f, indent=2, ensure_ascii=False)

print("Basic structure written")
