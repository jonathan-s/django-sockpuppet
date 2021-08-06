---
description: "How to update everything, nothing or something in-between \U0001F9D8"
---

# Morphs

By default, django-sockpuppet updates your entire page. After re-processing your view, rendering your template, and sending the raw HTML to your browser, django-sockpuppet uses [morphdom](https://github.com/patrick-steele-idem/morphdom) library to do the smallest number of DOM modifications necessary to refresh your UI in just a few milliseconds. For many developers, this will be a perfect solution forever. They can stop reading here.

Most real-world applications are more sophisticated, though. You think of your site in terms of sections, components and content areas. We reason about our functionality with abstractions like _"sidebar"_ but when it's time to work, we shift back to contemplating a giant tree of nested containers. Sometimes we need to surgically swap out one of those containers with something new. Sending the entire page to the client seems like massive overkill. We need to update just part of the DOM without disturbing the rest of the tree... _and we need it to happen in ~10ms_.

Other times... we just need to hit a button which feeds a cat which may or may not still be alive in a steel box. 🐈

It's _almost_ as if complex, real-world scenarios don't always fit the one-size-fits-all default full page Reflex.

## Introducing Morphs

Behind the scenes, there are actually three different _modes_ in which StimulusReflex can process your requests. We refer to them by _what they will replace_ on your page: **Page**, **Selector** and **Nothing**. All three benefit from the same logging, callbacks, events and promises.

Changing the Morph mode happens in your server-side Reflex class in one of your action methods. Both markup e.g. `data-reflex` and programmatic e.g. `stimulate()` mechanisms for initiating a Reflex on the client work without modification.

`morph` is only available in Reflex classes. Once you change modes, you cannot change between them. Meaning that if you call morph in the reflex class it will only execute that morph and no other change to the page will be made.

![Each Morph is useful in different scenarios.](.gitbook/assets/power-rangers%20%281%29.jpg)

| What are you replacing? | Typical Round-Trip Speed |
| :--- | :--- | :--- |
| The full **page** \(default\) | ~50ms-100ms |
| All children of a CSS DOM **selector** | ~15ms |
| **Nothing** at all | No | ~6ms |

## Page Morphs

Full-page Reflexes are described in great detail on the Reflexes page. Page morphs are the default behavior of StimulusReflex and they are what will occur if you don't call `morph` in your Reflex.

All Reflexes are, in fact, Page morphs - until they are not. 👴⚗️

If you've already been using Page morphs, nothing below changes what you know about them.

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

{% tab title="example\_reflex.py" %}
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
A selector morph is the act of executing `morph` function in the reflex class. This is the perfect option if you want to re-render a template partial, update a counter or just set a container to empty. Since it accepts a string or a template, you can pass a value to it directly.

### Tutorial

Let's first establish a baseline HTML sample to modify. Our attention will focus primarily on the `div` known colloquially as **\#foo**.

{% code title="show.html" %}
```html
<header data-reflex="click->Example#change">
  {% include "path/to/foo.html" message="Am I the medium or the massage?" %}
</header>
```
{% endcode %}

Behold! For this is the `foo` partial. It is an example of perfection:

{% code title="\_foo.html" %}
```html
<div id="foo">
  <span class="spa">{{ message }}</span>
</div>
```
{% endcode %}

You create a Selector morph by calling the `morph` method. In its simplest form, it takes two parameters: **selector** and **html**. We pass any valid CSS DOM selector that returns a reference to the first matching element, as well as the value we're updating it with.

You can also provide the keyword argument `template` and `context` to morph, in that case it will either treat the template argument as a string or look for the template partial and render the template with the provided context.

{% code title="my_app/reflexes/example\_reflex.py" %}
```python
from sockpuppet import reflex

class ExampleReflex(reflex.Reflex):
  def change(self):
    self.morph("#foo", html="Your muscles... they are so tight.")
```
{% endcode %}

If you consult your Elements Inspector, you'll now see that "\#foo" now contains a text node and your `header` has gained some attributes.

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

```python
yelling = "hello world".upper()
self.morph("#foo", template="path/to/foo.html", context={"message": yelling})
```

The `foo` partial (listed in the [Tutorial](morph-mode.md#tutorial) section above) is an example of a best practice for several subtle but important reasons which you should use to model your own updates:

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

```python
self.morph("#foo", html="<div id=\"foo\">Let's do something about those muscles.</div>")
```

This update will use morphdom to update the existing \#foo div. However, because \#foo contains a [text node](https://developer.mozilla.org/en-US/docs/Web/API/Node/nodeType), `data-reflex-permanent` is ignored.

```python
self.morph("#foo", html="<div id=\"baz\"><span>Just breathe in... and out.</span></div>")
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

1. Updating a partial to reflect a state change.
2. Updating a container element with a new simple value or HTML fragment.

### Things go wrong...

We've worked really hard to make morphs easy to work with, but there are some rules and edge cases that you have to follow. If something strange seems to be happening, please consult the [Morphing Sanity Checklist](https://sockpuppet.argpar.se/troubleshooting#morphing-sanity-checklist) to make sure you're on the right side of history.

## Nothing Morphs

Your user clicks a button. Something happens on the server. The browser is notified that this task was completed via the usual callbacks and events.

Nothing morphs are [Remote Procedure Calls](https://en.wikipedia.org/wiki/Remote_procedure_call), implemented on top of ActionCable.

Sometimes you want to take advantage of the chassis and infrastructure of sockpuppet, without any assumptions or expectations about changing your DOM afterwards. The bare metal nature of Nothing morphs means that the time between initiating a Reflex and receiving a confirmation can be low single-digit milliseconds, if you don't do anything to slow it down.

Nothing morphs usually initiate a long-running process, such as making calls to APIs or supervising I/O operations like file uploads or video transcoding. However, they are equally useful for emitting signals; you could send messages into a queue, tell your media player to play, or tell your Arduino to launch the rocket.

The key strategy when working with Nothing morphs is to **avoid blocking calls at all costs**.

#### I can't take the suspense. How can I capture this raw power for myself?

It's wickedly hard... but with practice, you'll be able to do it, too:

```python
self.morph()
```

That's it. That's the entire API surface. 🙇
