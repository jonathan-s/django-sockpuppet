---
description: Build reactive applications with the Rails tooling you already know and love
---

# Welcome

## What is StimulusReflex?

**StimulusReflex is a new way to craft modern, reactive web interfaces with Ruby on Rails.**

We extend the capabilities of both [Rails](https://rubyonrails.org) and [Stimulus](https://stimulusjs.org) by intercepting user interactions and passing them to Rails over real-time websockets. These interactions are processed by _Reflex actions_ that change application state. The current page is quickly re-rendered and the changes are sent to the client using [CableReady](https://cableready.stimulusreflex.com). The page is then [morphed](https://github.com/patrick-steele-idem/morphdom) to reflect the new application state. This entire round-trip allows us to update the UI in 20-30ms without flicker or expensive page loads.

This architecture eliminates the complexity imposed by full-stack frontend frameworks without abandoning [high-performance reactive user experiences](https://www.youtube.com/watch?v=SWEts0rlezA&t=214s). With StimulusReflex, small teams can do big things faster than ever before. We invite you to explore **a fresh alternative to the Single Page App** \(SPA\).

{% hint style="success" %}
**Get Involved.** We are stronger together! Please join us on [Discord.![](https://img.shields.io/discord/629472241427415060)](https://discord.gg/XveN625)

 [![GitHub stars](https://img.shields.io/github/stars/hopsoft/stimulus_reflex?style=social)](https://github.com/hopsoft/stimulus_reflex) [![GitHub forks](https://img.shields.io/github/forks/hopsoft/stimulus_reflex?style=social)](https://github.com/hopsoft/stimulus_reflex) [![Twitter follow](https://img.shields.io/twitter/follow/hopsoft?style=social)](https://twitter.com/hopsoft)
{% endhint %}

## Why should I use StimulusReflex?

Wouldn't it be great if you could **focus on your product** instead of the technical noise introduced by modern JavaScript. With StimulusReflex, you'll **ship projects faster, with smaller teams** and re-discover the joy of programming.

### Goals

* [x] Enable small teams to do big things, faster 🏃🏽‍♀️
* [x] Increase developer happiness ❤️❤️❤️
* [x] Facilitate simple, concise, and clear code 🤸
* [x] Integrate seamlessly with Ruby on Rails 🚝

## Live demo

[StimulusReflex Expo](http://expo.stimulusreflex.com/) is a growing collection of like examples showing different use-cases alongside the [source code](https://github.com/hopsoft/stimulus_reflex_expo) behind them.

Some of our favorite demos include:

* [Tabular](https://expo.stimulusreflex.com/demos/tabular): filtering, sorting and pagination without any client JavaScript
* [Todo](https://expo.stimulusreflex.com/demos/todo): our take on the [classic](http://todomvc.com/), with a wire size 2-15x smaller than every other solution

## Build the next Twitter in just 9 minutes \(or less\) 😉

{% embed url="https://www.youtube.com/watch?v=F5hA79vKE\_E" %}

## How we got here

**We love Rails.** Veterans of the framework remember the feeling of awe and disbelief after seeing David Heinemeier-Hansson's [Build a Blog in 15 minutes](https://www.youtube.com/watch?v=Gzj723LkRJY) video. It didn't seem possible that web development could be so easy, productive, and fun. We're talking [exponential gains in developer efficiency](https://www.youtube.com/watch?v=SWEts0rlezA&t=3m23s) and happiness. Rails has become so successful that nearly every framework since has borrowed ideas, patterns, and features from it.

The landscape has changed a lot since those early days. Applications are more ambitious now. The pursuit of native UI speeds spawned a new breed of increasingly complex technologies. Modern **Single Page Apps** have pushed much of the server's responsibilities to the client. Unfortunately this new approach trades _a developer experience_ that was once **fun and productive** for an alternative of high complexity and only marginal gains.

**There must be a better way.**

## The revolution begins

In his 2018 ElixirConf keynote, [Chris McCord](https://twitter.com/chris_mccord) _\(creator of the_ [_Phoenix_](http://www.phoenixframework.org/) _framework for_ [_Elixir_](https://elixir-lang.org/)_\)_ introduced [LiveView](https://github.com/phoenixframework/phoenix_live_view), an alternative to the SPA. His [presentation](https://www.youtube.com/watch?v=8xJzHq8ru0M) captures the same promise and excitement that Rails had in the early days.

We love Elixir and Phoenix. Elixir hits a sweet spot for people who want Rails-like conventions in a functional language. The community is terrific, but it's still small and comparatively niche.

Also, we just really enjoy using **Ruby and Rails**.

StimulusReflex was originally inspired by LiveView, but we are charting our own course. Our goal has always been to make building modern apps with Rails the most productive and enjoyable option available. We want to inspire our friends working with other tools and technologies to evaluate how concepts like StimulusReflex could work in their ecosystems and communities.

So far, it's working! Not only do we now have 20+ developers actively contributing to StimulusReflex, but we've inspired projects like [SockPuppet](https://github.com/jonathan-s/django-sockpuppet) for **Django**.

We are truly stronger together.

