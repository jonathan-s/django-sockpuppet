---
description: >-
  noun: firm or obstinate continuance in a course of action in spite of
  difficulty or opposition
---

# Persistence

We estimate that 80% of the pain points in web development are the direct result of maintaining state on the client. Even without considering the complexity of frameworks like React, how much time have you lost to fretting about model validation, stale data, and DOM readiness over your career?

#### Sockpuppet applications don't have a client state.\*

> \* This is _at least_ 98% true.

Imagine if you could focus almost all of your time and attention on the fun parts of web development again. Exploring the best way to implement features instead of worrying about data serialization and forgotten user flows. Smaller teams working smarter and faster, then going home on time.

Designing applications in the Sockpuppet mindset is far simpler than what we're used to, and we don't have to give up responsive client functionality to see our productivity shoot through the roof. It does, however, require some unlearning of old habits. You're about to rethink how you approach persisting the state of your application. This can be jarring at first! Even positive changes feel like work.

### The life of a Reflex

When you access a page in a Sockpuppet application, you see the current state of your user interface for that URL. There is no mounting process and no fetching of JSON from an API. Your request goes through the url router to your django view where it renders the template and sends HTML to the browser. This is Django in all it's server-rendered glory.

Only once the HTML page is displayed in your browser, the javascript library StimulusReflex wakes up. First, it opens a websocket connection and waits for messages. Then it scans your DOM for elements with `data-reflex` attributes. Those attributes become event handlers that map to methods in Stimulus controllers. The controllers connect events in your browser to methods in your Reflex classes on the server.

In a Reflex method you can call the django orm, access data from Redis or sessions, and set instance variables that get picked up in your view. After the Reflex method is complete, the django view is executed and any instance variables set on the Reflex will be passed onto the view's context.

We find that people learn how to work with Sockpuppet quickly when they are pushed in the right direction. The order of operations can seem fuzzy until the light bulb flicks on.

This document is here to get you to the light bulb moment quickly.

{% hint style="danger" %}
Sockpuppet only works with class based views and expects the method `get_context_data` to exist on the view.

As Sockpuppet re-renders the view during the reflex phase it's important to consider caching the view correctly. Otherwise queries in the view will be executed again which will decrease performance.
{% endhint %}

## Instance Variables

One of the most common patterns in Sockpuppet is to pass instance variables from the Reflex method to the view and which then gets rendered in the template. Ruby's `||=` \(pronounced "**or equals**"\) operator helps us manage this hand-off:

{% tabs %}
{% tab title="example\_reflex.py" %}
```python
def updateValue
  this.value = self.element['value']
```
{% endtab %}
{% endtabs %}

{% tabs %}
{% tab title="example\_view.py" %}
```python
def get_context_data(self, *args, **kwargs):
    context = super().get_context_data(*args, **kwargs)
    context['value'] = 0
    return context
```
{% endtab %}
{% endtabs %}

{% tabs %}
{% tab title="index.html" %}
```html
<div data-controller="example">
  <input type="text" data-reflex-permanent
    data-reflex="input->ExampleReflex#updateValue">
  <p>The value is: {{ value }}.</p>
</div>
```
{% endtab %}
{% endtabs %}

When you access the index page, the value will initially be set to 0. If the user changes the value of the text input, the value is updated to reflect whatever has been typed. This is possible because reflex data takes precedence over view data.

{% hint style="success" %}
Sockpuppet doesn't need to go through django routing. This means updates are processed much faster than requests that come from typing in a URL or refreshing the page.
{% endhint %}

Of course, instance variables are aptly named; they only exist for the duration of a single request, regardless of whether that request is initiated by accessing a URL or clicking a button managed by javascript through the library StimulusReflex.

### The stimulus\_reflex context variable

When Sockpuppet calls your django view, it passes any active instance variables along with a special context variable called `stimulus_reflex` which is set to `true`. **You can use this context variable to create an if/else block in your template or view that behaves differently depending on whether it's being called within the context of a Reflex update or not.**

{% tabs %}
{% tab title="pinball\_view.py" %}
```python
def get_context_data(self, *args, **kwargs):
    context = super().get_context_data(*args, **kwargs)
    if not context['stimulus_reflex']:
        self.request.session['balls_left'] = 3
    return context
```
{% endtab %}
{% endtabs %}

In this example, the user is given 3 new balls every time they refresh the page in their browser, effectively restarting the game. If the page state is updated via the Sockpuppet reflex, no new balls are allocated.

This also means that `self.request.session['balls_left']` will be set to 3 before the initial HTML page has been rendered and transmitted.

{% hint style="success" %}
**The first time the view action executes is your opportunity to set up the state that Sockpuppet will later modify.**
{% endhint %}

## The Rails session object

The `session` object will persist across multiple requests; indeed, you can open multiple browser tabs and they will all share the same `session.id` value on the server. See for yourself: you can create a new session using Incognito Mode or using a 2nd web browser.

We can update our earlier example to use the session object, and it will now persist across multiple browser tabs and refreshes:

{% tabs %}
{% tab title="example\_reflex.rb" %}
```ruby
def updateValue
  session[:value] = element[:value]
end
```
{% endtab %}
{% endtabs %}

{% tabs %}
{% tab title="example\_controller.rb" %}
```ruby
def index
  session[:value] ||= 0
end
```
{% endtab %}
{% endtabs %}

{% tabs %}
{% tab title="index.html.erb" %}
```html
<div data-controller="example">
  <input type="text" data-reflex-permanent
    data-reflex="input->ExampleReflex#updateValue">
  <p>The value is: <%= session[:value] %>.</p>
</div>
```
{% endtab %}
{% endtabs %}
