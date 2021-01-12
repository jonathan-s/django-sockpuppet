---
description: "How to update everything, nothing or something in-between \U0001F9D8"
---

# Morphs

By default, django-sockpuppet updates your entire page. After re-processing your view, rendering your template, and sending the raw HTML to your browser, django-sockpuppet uses the amazing [morphdom](https://github.com/patrick-steele-idem/morphdom) library to do the smallest number of DOM modifications necessary to refresh your UI in just a few milliseconds. For many developers, this will be a perfect solution forever. They can stop reading here.

Most real-world applications are more sophisticated, though. You think of your site in terms of sections, components and content areas. We reason about our functionality with abstractions like _"sidebar"_ but when it's time to work, we shift back to contemplating a giant tree of nested containers. Sometimes we need to surgically swap out one of those containers with something new. Sending the entire page to the client seems like massive overkill. We need to update just part of the DOM without disturbing the rest of the tree... _and we need it to happen in ~10ms_.

Other times... we just need to hit a button which feeds a cat which may or may not still be alive in a steel box. 🐈

It's _almost_ as if complex, real-world scenarios don't always fit the one-size-fits-all default full page Reflex.

## Introducing Morphs

Behind the scenes, there are actually three different _modes_ in which StimulusReflex can process your requests. We refer to them by _what they will replace_ on your page: **Page**, **Selector** and **Nothing**. All three benefit from the same logging, callbacks, events and promises.

Changing the Morph mode happens in your server-side Reflex class, either in the action method or the callbacks. Both markup e.g. `data-reflex` and programmatic e.g. `stimulate()` mechanisms for initiating a Reflex on the client work without modification.

`morph` is only available in Reflex classes, not controller actions. Once you change modes, you cannot change between them.

![Each Morph is useful in different scenarios.](.gitbook/assets/power-rangers%20%281%29.jpg)

| What are you replacing? | Process Controller Action? | Typical Round-Trip Speed |
| :--- | :--- | :--- |
| The full **page** \(default\) | Yes | ~50ms |
| All children of a CSS DOM **selector** | No | ~15ms |
| **Nothing** at all | No | ~6ms |

## Page Morphs

Full-page Reflexes are described in great detail on the Reflexes page. Page morphs are the default behavior of StimulusReflex and they are what will occur if you don't call `morph` in your Reflex.

All Reflexes are, in fact, Page morphs - until they are not. 👴⚗️

{% hint style="info" %}
StimulusReflex does not support using redirect\_to in a Page Morph. If you try to return an HTTP 302 in your controller during a Reflex action, your page content will become "You are being redirected."
{% endhint %}

If you've already been using Page morphs, nothing below changes what you know about them, with the possible exception that the `data-reflex-permanent` attribute is not all-powerful and can be defeated if you aren't careful with your Selector morphs.

{% page-ref page="reflexes.md" %}

### Scoping Page Morphs

Instead of updating your entire page, you can specify exactly which parts of the DOM will be updated using the `data-reflex-root` attribute.

`data-reflex-root=".class, #id, [attribute]"`

Simply pass a comma-delimited list of CSS selectors. Each selector will retrieve one DOM element; if there are no elements that match, the selector will be ignored.

StimulusReflex will decide which element's children to replace by evaluating three criteria in order:

1. Is there a `data-reflex-root` on the element with the `data-reflex`?
2. Is there a `data-reflex-root` on an ancestor element above the element in the DOM? It could be the element's immediate parent, but it doesn't have to be.
3. Just use the `body` element.

Here is a simple example: the user is presented with a text box. Anything they type into the text box will be echoed back in two div elements, forwards and backwards.

{% tabs %}
{% tab title="index.html" %}
```html
<div data-reflex-root="[forward],[backward]">
  <input type="text" value="{{ words }}" data-reflex="keyup->Example#words">
  <div forward>{{ words }}</div>
  <div backward>{{ words_reverse }}</div>
</div>
```
{% endtab %}

{% tab title="example\_reflex.rb" %}
```python
  def words(self):
    self.words = self.element['value']
    self.words_reverse = self.element['value'][::-1]
```
{% endtab %}
{% endtabs %}

{% hint style="info" %}
One interesting detail of this example is that by assigning the root to `[forward],[backward]` we are implicitly telling StimulusReflex to **not** update the text input itself. This prevents resetting the input value while the user is typing.
{% endhint %}

{% hint style="warning" %}
In StimulusReflex, morphdom is called with the **childrenOnly** flag set to _true_.

This means that &lt;body&gt; or the custom parent selector\(s\) you specify are not updated. For this reason, it's necessary to wrap anything you need to be updated in a div, span or other bounding tag so that it can be swapped out without confusion.

If you're stuck with an element that just won't update, make sure that you're not attempting to update the attributes on an &lt;a&gt;.
{% endhint %}

{% hint style="info" %}
It's completely valid to for an element with a data-reflex-root attribute to reference itself via a CSS class or other mechanism. Just always remember that the parent itself will not be replaced! Only the children of the parent are modified.
{% endhint %}

### Permanent Elements

Perhaps you just don't want a section of your DOM to be updated by StimulusReflex. Perhaps you need to integrate 3rd-party elements such as ad tracking scripts, Google Analytics, and any other widget that renders itself such as a React component or legacy jQuery plugin.

Just add `data-reflex-permanent` to any element in your DOM, and it will be left unchanged by full-page Reflex updates and `morph` calls that re-render partials. Note that `morph` calls which insert simple strings or empty values do not respect the `data-reflex-permanent` attribute.

{% code title="index.html" %}
```html
<div data-reflex-permanent>
  <iframe src="https://ghbtns.com/github-btn.html?user=hopsoft&repo=stimulus_reflex&type=star&count=true" frameborder="0" scrolling="0" class="ghbtn"></iframe>
</div>
```
{% endcode %}

{% hint style="warning" %}
We have encountered scenarios where the `data-reflex-permanent` attribute is ignored unless there is a unique `id` attribute on the element as well. Please let us know if you can identify this happening in the wild, as technically it shouldn't be necessary... and yet, it works.

¯\\__\(ツ\)\__/¯
{% endhint %}

{% hint style="danger" %}
Beware of Python packages that implicitly inject HTML into the body as it might be removed from the DOM when a Reflex is invoked. Packages like this often provide instructions for explicitly including their markup. We recommend using the explicit option whenever possible, so that you can wrap the content with `data-reflex-permanent`.
{% endhint %}

## Selector Morphs

This is the perfect option if you want to re-render a partial, update a counter or just set a container to empty. Since it accepts a string, you can pass a value to it directly, use `render` to regenerate a partial or even connect it to a ViewComponent.

Updating a target element with a Selector morph does _not_ invoke ActionDispatch. There is no routing, your controller is not run, and the view template is not re-rendered. This means that if your content is properly fragment cached, you should see round-trip updates in **10-15ms**... which is a nice change from the before times. 🐇

### Tutorial

Let's first establish a baseline HTML sample to modify. Our attention will focus primarily on the `div` known colloquially as **\#foo**.

{% code title="show.html" %}
```html
<header data-reflex="click->Example#change">
  {% include "path/to/foo.html" message=""Am I the medium or the massage?" %}
</header>
```
{% endcode %}

Behold! For this is the `foo` partial. It is an example of perfection:

{% code title="\_foo.html.erb" %}
```html
<div id="foo">
  <span class="spa">{{ message }}</span>
</div>
```
{% endcode %}

You create a Selector morph by calling the `morph` method. In its simplest form, it takes two parameters: **selector** and **html**. We pass any valid CSS DOM selector that returns a reference to the first matching element, as well as the value we're updating it with.

{% code title="my_app/reflexes/example\_reflex.rb" %}
```python
from sockpuppet import reflex

class ExampleReflex(reflex.Reflex):
  def change(self):
    self.morph("#foo", "Your muscles... they are so tight.")
```
{% endcode %}

If you consult your Elements Inspector, you'll now see that \#foo now contains a text node and your `header` has gained some attributes. This is just how StimulusReflex makes the magic happen.

```html
<header data-reflex="click->Example#change" data-controller="stimulus-reflex" data-action="click->stimulus-reflex#__perform">
  <div id="foo">Your muscles... they are so tight.</div>
</header>
```

**Morphs only replace the children of the element that you are targeting.** If you need to update the target element \(as you would with `outerHTML`\) consider targeting the parent of the element you need to change. You could, for example, call `morph "header", "No more #foo."` and start fresh.

{% hint style="info" %}
Cool, but _where did the span go_? We're glad you asked!

The truth is that a lot of complexity and nasty edge cases are being hidden away, while presenting you intelligent defaults and generally trying to follow the _principle of least surprise_.

There's no sugar coating the fact that there's a happy path for all of the typical use cases, and lots of gotchas to be mindful of otherwise. We're going to tackle this by showing you best practices first. Start by \#winning now and later there will be a section with all of the logic behind the decisions so you can troubleshoot if things go awry / [Charlie Sheen](https://www.youtube.com/watch?v=pipTwjwrQYQ).
{% endhint %}

### Intelligent defaults

Morphs work differently depending on whether you are replacing existing content with a new version or something entirely new. This allows us to intelligently re-render partials and ViewComponents based on data that has been changed in the Reflex action.

```ruby
yelling = element.value.upcase
morph "#foo", ApplicationController.render(partial: "path/to/foo", locals: {message: yelling})
```

{% hint style="success" %}
When you're using `morph` in a production application, it's a good habit to use the controller that is associated with the thing you're rendering, just as way to remind your future self which resource you're operating on.

If you're rendering the `users/profile` partial, you might consider using `UsersController.render` instead of `ApplicationController.render` so that in six months, you really can feel smarter.
{% endhint %}

The `foo` partial is an example of a best practice for several subtle but important reasons which you should use to model your own updates:

* it has a **single** top-level container element with the same CSS selector as the target
* inside that container element is another [element node](https://developer.mozilla.org/en-US/docs/Web/API/Node/nodeType), **not a text node**

If you can follow those two guidelines, you will see several important benefits regardless of how the HTML stream is generated:

* DOM changes will be performed by the morphdom library, which is highly efficient
* morph will respect elements with the `data-reflex-permanent` attribute
* any event handlers set on contents should remain intact \(unless they no longer exist\)

As you have already seen, it's **okay** to morph a container with a string, or a container element that has a different CSS selector. However, `morph` will treat these updates _slightly_ differently:

* DOM elements are replaced by updating innerHTML
* elements with the `data-reflex-permanent` attribute will be over-written
* any event handlers on replaced elements are immediately de-referenced
* you could end up with a nested container that might be jarring if you're not expecting it

Let's say that you update \#foo with the following morph:

```ruby
morph "#foo", "<div id=\"foo\">Let's do something about those muscles.</div>"
```

This update will use morphdom to update the existing \#foo div. However, because \#foo contains a [text node](https://developer.mozilla.org/en-US/docs/Web/API/Node/nodeType), `data-reflex-permanent` is ignored. \(Sorry! We just work here.\)

```ruby
morph "#foo", "<div id=\"baz\"><span>Just breathe in... and out.</span></div>"
```

Now your content is contained in a `span` element node. All set... except that you changed \#foo to \#baz.

```html
<header data-reflex="click->Example#change">
  <div id="foo">
    <div id="baz">
      <span>Just breathe in... and out.</span>
    </div>
  </div>
</header>
```

That's great - if that's what you want. 🤨

Ultimately, we've optimized for two primary use cases for morph functionality:

1. Updating a partial or ViewComponent to reflect a state change.
2. Updating a container element with a new simple value or HTML fragment.

If you're trying to do something not covered by the above: tell us about it on Discord, consult the list of gotchas and exceptions below, and consider calling CableReady\#outer\_html directly in your Reflex.

### Morphing Multiplicity

What fun is morphing if you can't [stretch out a little](https://www.youtube.com/watch?v=J5G_rdNQLFU)?

```ruby
morph "#username": "hopsoft", "#notification_count": 5
morph "#regrets"
```

You can call `morph` multiple times in your Reflex action method.

You can use Ruby's implicit Hash syntax to update multiple selectors with one morph. These updates will all be sent as part of the same broadcast, and executed in the order they are defined. Any non-String values will be coerced into Strings. Passing no html argument is equivalent to `""`.

### dom\_id

One of the best perks of Rails naming conventions is that you can usually calculate what the name of an element or resource will be programmatically, so long as you know the class name and id.

Inside a Reflex class, you might find yourself typing code like:

```ruby
morph "#user_#{user.id}", user.name
```

The [dom\_id](https://apidock.com/rails/v6.0.0/ActionView/RecordIdentifier/dom_id) helper is available inside Reflex classes and supports the optional prefix argument:

```ruby
morph dom_id(user), user.name
```

### View Helpers

If you render a partial that makes use of controller-specific helpers, use that controller to render the partial:

```ruby
morph "#stan", StanController.render(stan)
```

If you are planning to render a partial that uses Rails routing view helpers to create URLs, you will need to [set up your environment configuration files](https://docs.stimulusreflex.com/deployment#set-your-default_url_options-for-each-environment) to make the live site metadata available inside your Reflexes.

### Things go wrong...

We've worked really hard to make morphs easy to work with, but there are some rules and edge cases that you have to follow. If something strange seems to be happening, please consult the [Morphing Sanity Checklist](https://docs.stimulusreflex.com/troubleshooting#morphing-sanity-checklist) to make sure you're on the right side of history.

## Nothing Morphs

Your user clicks a button. Something happens on the server. The browser is notified that this task was completed via the usual callbacks and events.

Nothing morphs are [Remote Procedure Calls](https://en.wikipedia.org/wiki/Remote_procedure_call), implemented on top of ActionCable.

Sometimes you want to take advantage of the chasis and infrastructure of StimulusReflex, without any assumptions or expectations about changing your DOM afterwards. The bare metal nature of Nothing morphs means that the time between initiating a Reflex and receiving a confirmation can be low single-digit milliseconds, if you don't do anything to slow it down.

Nothing morphs usually initiate a long-running process, such as making calls to APIs or supervising I/O operations like file uploads or video transcoding. However, they are equally useful for emitting signals; you could send messages into a queue, tell your media player to play, or tell your Arduino to launch the rocket.

The key strategy when working with Nothing morphs is to **avoid blocking calls at all costs**. While we might still be years away from a viable asynchronous Ruby ecosystem, using Reflexes to initiate Rails ActiveJob instances - ideally processed by Sidekiq and powered by Redis - provides a reliable platform that financial institutions still pay millions of dollars to achieve.

In a sense, Nothing morphs are _yin_ to CableReady's _yang_. A Reflex conveys user intent to the server, and a broadcast is the vehicle for server intent to be realized on the client, completing the circle. ☯️

#### I can't take the suspense. How can I capture this raw power for myself?

It's wickedly hard... but with practice, you'll be able to do it, too:

```ruby
morph :nothing
```

That's it. That's the entire API surface. 🙇

### Multi-Stage Morphs

You can morph the same target element multiple times in one Reflex by calling CableReady directly. One clever use of this technique is to morph a container to display a spinner, call an API or access computationally intense results - which you cache for next time - and then replace the spinner with the new update... all in the same Reflex action.

```ruby
morph :nothing
cable_ready[stream_name].morph { spinner... }
cable_ready.broadcast
# long running work
cable_ready[stream_name].morph { progress update... }
cable_ready.broadcast
# long running work
cable_ready[stream_name].morph { final update... }
cable_ready.broadcast
```
