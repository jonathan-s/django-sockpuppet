---
description: How to restrict DOM updates
---

# Scoping

By default, the JavaScript library StimulusReflex updates your entire page. It uses the amazing [`morphdom`](https://github.com/patrick-steele-idem/morphdom) library to do the smallest number of DOM modifications necessary to refresh your UI in just a few milliseconds. For many developers, this will be a perfect solution and they can stop reading here.

Some applications are more sophisticated. You might want to think of your site in terms of components, or you might need to interact with legacy JavaScript plugins on your page that don't play nicely with modern techniques. Heck, you might just need to make sure we don't reload the same third-party ad tracker every time someone clicks a button.

Great news: we have you covered.

## Partial DOM updates

Instead of updating your entire page, you can specify exactly which parts of the DOM will be updated using the `data-reflex-root` attribute.

`data-reflex-root=".class, #id, [attribute]"`

Simply pass a comma-delimited list of CSS selectors. Each selector will retrieve one DOM element; if there are no elements that match, the selector will be ignored.

StimulusReflex will decide which element's children to replace by evaluating three criteria in order:

1. Is there a `data-reflex-root` on the element with the `data-reflex`?
2. Is there a `data-reflex-root` on an ancestor element with a `data-controller` above the element in the DOM? It could be the element's immediate parent, but it doesn't have to be.
3. Just use the `body` element.

Here is a simple example: the user is presented with a text box. Anything they type into the text box will be echoed back in two div elements, forward and backward.

{% tabs %}
{% tab title="index.html" %}
```text
<div data-controller="example" data-reflex-root="[forward],[backward]">
  <input type="text" value="{{ words }}" data-reflex="keyup->ExampleReflex#words">
  <div forward>{{ words }}</div>
  <!-- provided there you have created a template tag that handles the reverse scenario -->
  <div backward>{{ words|reverse }}</div>
</div>
```
{% endtab %}
{% endtabs %}

{% tabs %}
{% tab title="example\_reflex.py" %}
```python
class ExampleReflex(Reflex):
  def words():
    self.words = element['value']
    self.reversed = element['value'][::-1]
```
{% endtab %}
{% endtabs %}

{% hint style="info" %}
One interesting detail of this example is that by assigning the root to `[forward],[backward]` we are implicitly telling StimulusReflex to **not** update the text input itself. This prevents resetting the input value while the user is typing.
{% endhint %}

{% hint style="warning" %}
In StimulusReflex, `morphdom` is called with the **childrenOnly** flag set to _true_.

This means that `<body>` or the custom parent selector\(s\) you specify are not updated. For this reason, it's necessary to wrap anything you need to be updated in a `<div>`, `<span>`, or other bounding tag so that it can be swapped out without confusion.

If you're stuck with an element that just won't update, make sure that you're not attempting to update the attributes on an `<a>`.
{% endhint %}

{% hint style="info" %}
It's completely valid for an element with a `data-reflex-root` attribute to reference itself via a CSS class or other mechanism. Just always remember that the parent itself will not be replaced! Only the children of the parent are modified.
{% endhint %}

## Persisting Elements

Perhaps you just don't want a section of your DOM to be updated by StimulusReflex, even if you're using the full document body default.

Just add `data-reflex-permanent` to any element in your DOM, and it will be left unchanged.

{% code title="index.html" %}
```markup
<div data-reflex-permanent>
  <iframe src="https://ghbtns.com/github-btn.html?user=hopsoft&repo=stimulus_reflex&type=star&count=true" frameborder="0" scrolling="0" class="ghbtn"></iframe>
  <iframe src="https://ghbtns.com/github-btn.html?user=hopsoft&repo=stimulus_reflex&type=fork&count=true" frameborder="0" scrolling="0" class="ghbtn"></iframe>
</div>
```
{% endcode %}

{% hint style="warning" %}
This is especially important for third-party elements such as ad tracking scripts, Google Analytics, and any other widget that renders itself such as a React component or legacy jQuery plugin.
{% endhint %}

## Single Source of Truth

While stateless form submissions have technically always suffered from the "last update wins" problem, it's only in recent years that developers have created interfaces that need to respond to changing application state in real-time.

There are a few guiding principles that we adhere to when building a technology that can change the page you're on, even while you busy working on something important. The most important consideration is that even though Sockpuppet applications persist state on the server, the client should be the single source of truth for the text input element that has active focus.

Put differently: **the server should never update the value of a text box while you're typing into it**.

We've worked really hard to make sure that developers can update other aspects of the active text input element. For example, it's possible to change the background color or even mark the element as disables while you're typing into it. However, all attempts to overwrite the input element's value will be silently suppressed.

If you need to filter or constrain the contents of a text input, consider using a client-side library such as [Cleave.js](https://nosir.github.io/cleave.js/) instead of trying to circumvent the Single Source of Truth mechanisms, which are there to protect your users from their fellow collaborators.

Note that this concept only applies to the active text input element. Any elements which are marked with `data-reflex-permanent` will not be morphed in any way.
