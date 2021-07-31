---
description: "Reflex classes are full of Reflex actions. Reflex actions? Full of love. \U0001F3E9"
---

# Reflexes

Server-side Reflexes inherit from `sockpuppet.Reflex`. They hold logic responsible for performing operations like writing to your backend data stores. Reflexes are not concerned with rendering because rendering is delegated to the Django view.

## Glossary

* Sockpuppet: The name of this project, which has a JS websocket client and a Django-based server component, which is based on `django-channels`.
* Stimulus: An incredibly simple yet powerful JS framework by the creators of Rails.
* "a Reflex": Used to describe the full, round-trip life-cycle of a Sockpuppet operation, from client to server and back again
* Reflex class: A Python class that inherits from `sockpuppet.Reflex` and lives in your `reflexes` folder or `reflex.py`, this is where your Reflex actions are implemented.
* Reflex action: A method in a Reflex class, called in response to activity in the browser. It has access to several special accessors containing all of the Reflex controller element's attributes
* Reflex controller: A Stimulus controller that imports the StimulusReflex client library. It has a `stimulate` method for triggering Reflexes and like all Stimulus controllers, it's aware of the element it is attached to - as well as any Stimulus [targets](https://stimulusjs.org/reference/targets) in its DOM hierarchy
* Reflex controller element: The DOM element upon which the `data-reflex` attribute is placed, which often has data attributes intended to be delivered to the server during a Reflex action

## Calling a Reflex

Regardless of whether you use declarative Reflex calls via `data-reflex` attributes in your HTML or if you are using JavaScript, ultimately the `stimulate` method on your Stimulus controller is being called. We touched on this briefly in the **Quick Start** chapter; now we are going to document the function signature so that you fully understand what's happening behind the scenes.

All Stimulus controllers that have had `StimulusReflex.register(this)` called in their `connect` method gain a `stimulate` method.

```javascript
this.stimulate(string target, [DOMElement element], ...[JSONObject argument])
```

- **target**, required \(exception: see "Requesting a Refresh" below\): A string containing the server Reflex class and method, in the form "ExampleReflex\#increment".

- **element**, optional: A reference to a DOM element which will provide both attributes and scoping selectors. Frequently pointed to `event.target` in JavaScript. **Defaults to the DOM element of the controller in scope**.

- **argument**, optional: A **splat** of JSON-compliant JavaScript datatypes - array, object, string, numeric or boolean - can be received by the server Reflex action as one or many ordered arguments. Defaults to no argument\(s\). **Note: the method signature has to match.** If the Reflex action is expecting two arguments and doesn't receive two arguments, it will raise an exception.

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

## The Reflex Class

StimulusReflex makes the following properties available to the developer inside Reflex actions:

## Properties
- `consumer` - the Websocket connection from django channels.
- `request` - a django request object
- `request.post` - If the page contains a form, it will find the closest form which and the parameters will be contained here.
- `session` - the Django session store for the current visitor
- `url` - the URL of the page that triggered the reflex
- `element` - an object that represents the HTML element that triggered the reflex
- `params` - Contains the form parameters for the closest form

## Methods
- `get_context_data` - Accesses the context data from the view associated with the reflex. You will know that the method is triggered from the reflex because the context now contains `stimulus_reflex` which is equal to `True`. This will be available from `kwargs` so you can modify the context based on whether it is a reflex or not.

- `get_channel_id` - By default this returns the session key which is used to deliver the websocket update to the client. This function can be overridden if you need a different key for transferring the update.

{% hint style="danger" %}
`reflex` and `process` are reserved words inside Reflex classes. You cannot create Reflex actions with these names.
{% endhint %}

### Modify or add to the view context

When a reflex is triggered you can modify the current context of the view or add more context which previously didn't exist when the view rendered in the normal request-response cycle.

{% tabs %}
{% tab %}
```python
from sockpuppet.reflex import Reflex

class ExampleReflex(Reflex):
    def work(self):
        # All new instance variables in the reflex will be accessible
        # in the context during rendering.
        self.instance_variable = 'hello world'

        context = self.get_context_data()
        context['a_key'] = 'a pink elephant'
        # If "a_key" existed in the context before the reflex was triggered
        # the context variable will now be modified to "a pink elephant"

        # if it didn't exist, the context variable is then created with the
        # data "a pink elephant" 🐘

```
{% endtab %}

{% tab %}
```html
<div>
    <!-- When the work reflex is triggered "new_variable" will be
    available in the context -->
    <span>{{ instance_variable }}</span>

    <!-- This will show up as "a pink elephant" when triggering the reflex -->
    <span>{{ a_key }}</span>
</div>

```
{% endtab %}
{% endtabs %}

### The `element` property

The `element` property contains all of the Reflex controller's [DOM element attributes](https://developer.mozilla.org/en-US/docs/Web/API/Element/attributes) as well as other properties like, `tag_name`, `checked` and `value`.

{% hint style="info" %}
**Most values are strings.** The only exceptions are `checked` and `selected` which are booleans.

Elements that support **multiple values** \(like `<select multiple>`, or a collection of checkboxes with equal `name`\), will emit an additional **`values` property.** The `value` property will contain a comma-separated string of the checked options.
{% endhint %}

Here's an example that outlines how you can interact with the `element` property in your Reflexes.

{% code title="app/templates/show.html" %}
```markup
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
        self.element.attributes          # a dictionary that represents all attributes of the HTML element
        self.element.dataset             # a dictionary that represents the HTML element's dataset

        self.element.attributes['id']           # => 'example'
        self.element.attributes['tag_name']     # => 'CHECKBOX'
        self.element.attributes['checked']      # => 'true'
        self.element.attributes['label']        # => 'Example'
        self.element.attributes['data-reflex']  # => 'ExampleReflex#work'
        self.element.dataset['reflex']          # => 'ExampleReflex#work'
        self.element.attributes['data-value']   # => '123'
        self.element.dataset['value']           # => '123'

```
{% endtab %}
{% endtabs %}

{% hint style="success" %}
When Sockpuppet is rendering your template, a context variable named **stimulus\_reflex** is available to your Django view and set to true.

You can use this flag to create branching logic to control how the template might look different if it's a Reflex versus a normal page refresh.
{% endhint %}


### Inheriting data-attributes from parent elements

You might design your interface such that you have a deeply nested structure of data attributes on parent elements. Instead of writing code to travel your DOM and access those values, you can use the `data-reflex-dataset="combined"` directive to scoop all data attributes up the hierarchy and pass them as part of the Reflex payload.

```html
<div data-post-id="{{ @post.id }}">
  <div data-category-id="{{ @category.id }}">
    <button data-reflex="click->Comment#create" data-reflex-dataset="combined">Create</button>
  </div>
</div>
```

This Reflex action will have `post-id` and `category-id` accessible:

```python
from sockpuppet import reflex

class CommentReflex(reflex.Reflex):
  def create(self)
    print(element.dataset["post-id"])
    print(element.dataset["category-id"])
```

If a data attribute appears several times, the deepest one in the DOM tree is taken. In the following example, `data-id` would be **2**.

```html
<div data-id="1">
  <button data-id="2" data-reflex="Example#whatever" data-reflex-dataset="combined">Click me</button>
</div>
```
