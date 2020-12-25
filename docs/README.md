---
description: Build reactive applications with the Django tooling you already know and love
---

# Welcome

## What is Sockpuppet?

**Sockpuppet is a new way to craft modern, reactive web interfaces with Django.**

We extend the capabilities of both [Django](https://www.djangoproject.com/) and [Stimulus](https://stimulusjs.org) by intercepting user interactions and passing them to Django over real-time websockets. These interactions are processed by _Reflex actions_ that change application state. The current page is quickly re-rendered and the changes are sent to the client. The page is then [morphed](https://github.com/patrick-steele-idem/morphdom) to reflect the new application state. This entire round-trip allows us to update the UI in 20-30ms without flicker or expensive page loads.

This architecture eliminates the complexity imposed by full-stack frontend frameworks without abandoning [high-performance reactive user experiences](https://www.youtube.com/watch?v=SWEts0rlezA&t=214s). With Sockpuppet, small teams can do big things faster than ever before. We invite you to explore **a fresh alternative to the Single Page App** \(SPA\).

We are indebted to the the work done in [StimulusReflex](https://docs.stimulusreflex.com). Without them Sockpuppet wouldn't exist, it's our bigger sibling who prefers to play in the rails world.

{% hint style="success" %}
**Get Involved.** We are stronger together! Please join us on [Discord.![](https://img.shields.io/discord/629472241427415060)](https://discord.gg/XveN625)

[![GitHub stars](https://img.shields.io/github/stars/jonathan-s/sockpuppet?style=social)](https://github.com/jonathan-s/sockpuppet) [![GitHub forks](https://img.shields.io/github/forks/jonathan-s/sockpuppet?style=social)](https://github.com/jonathan-s/sockpuppet) [![Twitter follow](https://img.shields.io/twitter/follow/argparse?style=social)](https://twitter.com/argparse)
{% endhint %}

## Why should I use Sockpuppet?

Wouldn't it be great if you could **focus on your product** instead of the technical noise introduced by modern JavaScript. With Sockpuppet, you'll **ship projects faster, with smaller teams** and re-discover the joy of programming.

### Goals

* [x] Enable small teams to do big things, faster 🏃🏽‍♀️
* [x] Increase developer happiness ❤️❤️❤️
* [x] Facilitate simple, concise, and clear code 🤸
* [x] Integrate seamlessly with Django 🚝

## Build the next Twitter in just 9 minutes \(or less\) 😉

Our friends at StimulusReflex proves that you can build things fast.

{% embed url="https://www.youtube.com/watch?v=F5hA79vKE\_E" caption="" %}

## How we got here

Applications nowadays pursue native UI speeds which spawned a new breed of increasingly complex technologies. Modern **Single Page Apps** have pushed much of the server's responsibilities to the client. Unfortunately this new approach trades _a developer experience_ that was once **fun and productive** for an alternative of high complexity and only marginal gains.

**There must be a better way.**

## The revolution begins

In his 2018 ElixirConf keynote, [Chris McCord](https://twitter.com/chris_mccord) _\(creator of the_ [_Phoenix_](http://www.phoenixframework.org/) _framework for_ [_Elixir_](https://elixir-lang.org/)_\)_ introduced [LiveView](https://github.com/phoenixframework/phoenix_live_view), an alternative to the SPA. His [presentation](https://www.youtube.com/watch?v=8xJzHq8ru0M) captures the same promise and excitement that Rails had in the early days.

We love Elixir and Phoenix. Elixir hits a sweet spot for people who want Rails-like conventions in a functional language. The community is terrific, but it's still small and comparatively niche.

Also, we just really enjoy using **Django**.

Sockpuppet was originally inspired by StimulusReflex which was inspired by LiveView, but we are charting our own course together with StimulusReflex. Our goal has always been to make building modern apps with Django the most productive and enjoyable option available. We want to inspire our friends working with other tools and technologies to evaluate how concepts like Sockpuppet could work in their ecosystems and communities.

## Architecture

So what is happening behind the scenes here? Sockpuppet works in three layers.

It uses javascript; The javascript is re-used from StimulusReflex, which in itself is built upon stimulusjs. The javascript in StimulusReflex also uses something called cable_ready which has the responsibility of modifying the DOM. The javascript layer ensures that the data is being sent to the server layer through websockets. When a message is received from the server layer it will re-render the dom according to the server side instructions.

The HTML layer has the responsibility of defining where and how a "reflex" is going to be triggered. Ie, a reflex could be triggered by an browser event or the click of a button. When building more complex applications the HTML layer may also be used to store state so that this state is accessible when doing some interactivity in a stimulus controller.

The last layer is server layer. This is where a "Reflex" class is defined. The reflex knows what path and template was received and will re-render that template to contain any new information defined in the reflex. The reflex could also make database queries and such as well. Once the template is re-rendered it will send it back to frontend where javascript will modify the DOM to update everything.
