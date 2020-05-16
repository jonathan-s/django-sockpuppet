---
description: "Reflex classes are full of Reflex actions. Reflex actions? Full of love. \U0001F3E9"
---

# Reflexes

Server side reflexes inherit from `sockpuppet.Reflex`. They hold logic responsible for performing operations like writing to your backend data stores. Reflexes are not concerned with rendering because rendering is delegated to the Rails controller or Django view and action that originally rendered the page.

## Glossary

* Sockpuppet: the name of this project, which has a JS websocket client and a django based server component, which is based on django-channels.
* Stimulus: an incredibly simple yet powerful JS framework by the creators of Rails
* "a Reflex": used to describe the full, round-trip life-cycle of a Sockpuppet operation, from client to server and back again
* Reflex class: a python class that inherits from `sockpuppet.Reflex` and lives in your `reflexes` folder or `reflex.py`, this is where your Reflex actions are implemented.
* Reflex action: a method in a Reflex class, called in response to activity in the browser. It has access to several special accessors containing all of the Reflex controller element's attributes
* Reflex controller: a Stimulus controller that imports the StimulusReflex client library. It has a `stimulate` method for triggering Reflexes and like all Stimulus controllers, it's aware of the element it is attached to - as well as any Stimulus [targets](https://stimulusjs.org/reference/targets) in its DOM hierarchy
* Reflex controller element: the DOM element upon which the `data-reflex` attribute is placed, which often has data attributes intended to be delivered to the server during a Reflex action

## Calling a Reflex

Regardless of whether you use declarative Reflex calls via `data-reflex` attributes in your HTML or if you are using JavaScript, ultimately the `stimulate` method on your Stimulus controller is being called. We touched on this briefly in the **Quick Start** chapter; now we are going to document the function signature so that you fully understand what's happening behind the scenes.

All Stimulus controllers that have had `StimulusReflex.register(this)` called in their `connect` method gain a `stimulate` method.

```javascript
this.stimulate(string target, [DOMElement element], ...[JSONObject argument])
```

**target**, required \(exception: see "Requesting a Refresh" below\): a string containing the server Reflex class and method, in the form "ExampleReflex\#increment".

**element**, optional: a reference to a DOM element which will provide both attributes and scoping selectors. Frequently pointed to `event.target` in Javascript. **Defaults to the DOM element of the controller in scope**.

**argument**, optional: a **splat** of JSON-compliant Javascript datatypes - array, object, string, numeric or boolean - can be received by the server Reflex action as one or many ordered arguments. Defaults to no argument\(s\). **Note: the method signature has to match.** If the Reflex action is expecting two arguments and doesn't receive two arguments, it will raise an exception.

### Requesting a "refresh"

If you are building advanced workflows, there are edge cases where you may want to initiate a Reflex action that does nothing but re-render the view template and morph any new changes into the DOM. While this shouldn't be your primary tool, it's possible for your data to be mutated by destructive external side effects. 🧟

```javascript
this.stimulate()
```

Calling `stimulate` with no parameters invokes a special global Reflex that allows you to force a re-render of the current state of your application UI. This is the same thing that the user would see if they hit their browser's Refresh button, except without the painfully slow round-trip cycle.

It's also possible to trigger this global Reflex by passing nothing but a browser event to the `data-reflex` attribute. For example, the following button element will refresh the page content every time the user presses it:

```markup
<button data-reflex="click">Refresh</button>
```

### Scanning for new data-reflex attributes

The javascript library [StimulusReflex](https://www.npmjs.com/package/stimulus_reflex) scans the DOM looking for instances of the `data-reflex` attribute. When it finds one, it attaches a `stimulus-reflex` Stimulus controller to that element.

By default, scans happen in response to four events:

| Object | Event |
| :--- | :--- |
| window | load |
| document | turbolinks:load |
| document | cable-ready:after-morph |
| document | ajax:complete |

While those should cover the vast majority of cases, there are scenarios such as client JSX or Handlebars template rendering which require a re-scan of the DOM to pick up new `data-reflex` instances. You can manually request a re-scan in any Stimulus controller that has **already called** `StimulusReflex.register(this)`.

```javascript
StimulusReflex.setupDeclarativeReflexes()
```

## Reflex Classes

StimulusReflex makes the following properties available to the developer inside Reflex actions:

{% tabs %}
{% tab title="Python" %}
* `consumer` - the websocket connection from django channels.
* `request` - a django request object
* `session` - the django session store for the current visitor
* `url` - the URL of the page that triggered the reflex
* `element` - a dictionary like object that represents the HTML element that triggered the reflex
{% endtab %}
{% endtabs %}

{% hint style="danger" %}
`reflex` and `process` are reserved words inside Reflex classes. You cannot create Reflex actions with these names.
{% endhint %}

### `element`

The `element` property contains all of the Stimulus controller's [DOM element attributes](https://developer.mozilla.org/en-US/docs/Web/API/Element/attributes) as well as other properties like, `tagName`, `checked` and `value`.

{% hint style="info" %}
**Most values are strings.** The only exceptions are `checked` and `selected` which are booleans.

Elements that support **multiple values** (like `<select multiple>`, or a collection of checkboxes with equal `name`), will emit an additional **`values` property.** The `value` property will contain a comma-separated string of the checked options.
{% endhint %}

Here's an example that outlines how you can interact with the `element` property in your reflexes.

{% code title="app/templates/show.html" %}
```html
<checkbox id="example" label="Example" checked
  data-reflex="ExampleReflex#work" data-value="123" />
```
{% endcode %}

{% tabs %}
{% tab %}
```python
from sockpuppet.reflex import Reflex

class ExampleReflex(Reflex):
    def work(self):
        self.element['id']               # the HTML element's id attribute value
        self.element.dataset             # a dictionary that represents the HTML element's dataset

        self.element['id']               # => 'example'
        self.element['tag_name']         # => 'CHECKBOX'
        self.element['checked']          # => 'true'
        self.element['label']            # => 'Example'
        self.element['data-reflex']      # => 'ExampleReflex#work'
        self.element.dataset['reflex']   # => 'ExampleReflex#work'
        self.element['data-value']       # => '123'
        self.element.dataset['value']    # => '123'
```
{% endtab %}
{% endtabs %}

{% hint style="success" %}
When Sockpuppet is rendering your template, a context variable named **stimulus\_reflex** is available to your django view and set to true.

You can use this flag to create branching logic to control how the template might look different if it's a Reflex vs normal page refresh.
{% endhint %}
