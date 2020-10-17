# Troubleshooting

![](https://cdn.vox-cdn.com/thumbor/2q97YCXcLOlkoR2jKKEMQ-wkG9k=/0x0:900x500/1200x800/filters:focal%28378x178:522x322%29/cdn.vox-cdn.com/uploads/chorus_image/image/49493993/this-is-fine.0.jpg)

## Logging

### Client-Side

You might want to know the order in which your Reflexes are called, how long it took to process each Reflex or what the Reflex response payload contains. Luckily you can enable Reflex logging to your browser's Console Inspector.

![](.gitbook/assets/screenshot_2020-05-05_at_01.19.44.png)

There are two ways to enable client debugging in your StimulusReflex instance.

You can provide `debug: true` to the initialize options like this:

{% code title="app/javascript/controllers/index.js" %}
```javascript
StimulusReflex.initialize(application, { consumer, debug: true })
```
{% endcode %}

You can also set debug mode after you've initialized StimulusReflex. This is especially useful if you just want to log the Reflex calls in your development environment:

{% code title="app/javascript/controllers/index.js" %}
```javascript
StimulusReflex.initialize(application, { consumer })
if (process.env.ENVIRONMENT === 'development') StimulusReflex.debug = true
```
{% endcode %}

### Server-Side

To get debug logging for Sockpuppet you need to make some modifications to `LOGGING` in `settings.py`. Below you can see an example logging configuration that enables debug-level logging Sockpuppet.

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG'
    },
    'handlers': {
        'sockpuppet': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'loggers': {
        'sockpuppet': {
            'level': 'DEBUG',
            'handlers': ['sockpuppet']
        }
    }
}
```

## Morphing Sanity Checklist

We want to stress that if you follow the happy path explained on the [Morphs](../rtfm/morph-modes.md#intelligent-defaults) page, you shouldn't need to ever worry about the edge cases that follow. However, we have worked hard to think of and collect the possible ways someone could abuse the HTML spec and potentially experience unexpected outcomes.

#### You cannot change the attributes of your morph target.

Even if you maintain the same CSS selector, you cannot modify any attributes \(including data attributes\) of the container element with the `morph` method.

```python
self.morph("#foo", html="<div id=\"foo\" data-muscles=\"sore\">data-muscles will not be set.</div>")
```

You might consider digging into the CableReady/Channel implementation and use `outer_html` or `set_attribute`, have a look in the [source code](https://github.com/jonathan-s/django-sockpuppet/blob/master/sockpuppet/channel.py#L110-L118)

#### Your top-level content needs to be an element.

It's not enough for the container selector to match. Your content needs to be wrapped in an element, or else `data-reflex-permanent` will not work.

```python
self.morph("#foo", html="<div id=\"foo\"><p>Strengthen your core.</p></div>")
```

#### No closing tag? No problem.

Inexplicably, morphdom just doesn't seem to care if your top-level element node is closed.

```python
self.morph("#foo", html="<div id=\"foo\"><span>Who needs muscl</span>")
```

#### Different element type altogether? Who cares, so long as the CSS selector matches?

Go ahead, turn your `div` into a `span`. morphdom just doesn't care.

```python
self.morph("#foo", html="<span id=\"foo\">Are these muscles or rocks? lol</span>")
```

#### A new CSS selector \(or no CSS selector\) will be processed with innerHTML

Changing the CSS selector will result in some awkward nesting issues.

```python
self.morph("#foo", html="<div id=\"baz\">Let me know if this is too strong.</div>")
```

```html
<div id="foo">
  <div id="baz">Let me know if this is too strong.</div>
</div>
```

#### If the element with the CSS selector is surrounded, external content will be discarded.

```python
self.morph("#foo", html="I am excited to see your <div id=\"foo\">muscles</div> next week.")
```

```html
<div id="foo">muscles</div>
```

#### If an element matches the target CSS selector, other elements will be ignored.

```python
self.morph("#foo", html="<div id=\"foo\">Foo!</div><div id=\"post_foo\">Avant-Foo!</div>")
```

```html
<div id="foo">Foo!</div>
```

#### This is true even if the elements are reversed.

```python
self.morph("#foo", html="<div id=\"post_foo\">Avant-Foo!</div><div id=\"foo\">Foo!</div>")
```

```html
<div id="foo">Foo!</div>
```

#### But it's all good in the hood if the selector is not present.

```python
self.morph("#foo", html="<div id=\"mike\">Mike</div> and <div id=\"ike\">Ike</div>")
```

```html
<div id="foo">
  <div id="mike">Mike</div>
  and
  <div id="ike">Ike</div>
</div>
```

{% hint style="success" %}
Do you have any more weird edge cases? Please let us know!
{% endhint %}

## Open Issues

There are some things that we'd very much like to fix, but we simply haven't been able to or the responsibility falls to an upstream dependency we don't have direct access to.

#### iFrame gets refreshed despite data-reflex-permanent

Depending on how your DOM is structured, it's possible to have an iframe element which has been marked with `data-reflex-permanent` get morphed. [We're aware of it, and we've tried to fix it.](https://github.com/hopsoft/stimulus_reflex/issues/452)
