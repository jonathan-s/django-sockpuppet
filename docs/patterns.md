---
description: How to build a great StimulusReflex application
---

# Useful Patterns

In the course of creating Sockpuppet and using it to build applications, we have discovered several useful tricks. While it may be tempting to add features to the core library, every idea that we include creates bloat and comes with the risk of stepping on someone's toes because we didn't anticipate all of the ways it could be used.

## Client Side

### Application controller

You can make use of JavaScript's class inheritance to set up an Application controller that will serve as the foundation for all of your StimulusReflex controllers to build upon. This not only reduces boilerplate, but it's also a convenient way to set up lifecycle callback methods for your entire application.

{% tabs %}
{% tab title="application\_controller.js" %}
```javascript
import { Controller } from 'stimulus'
import StimulusReflex from 'stimulus_reflex'

export default class extends Controller {
  connect () {
    StimulusReflex.register(this)
  }

  sayHi () {
    console.log('Hello from the Application controller.')
  }
}
```
{% endtab %}
{% endtabs %}

Then, all that's required to create a StimulusReflex controller is inherit from ApplicationController:

{% tabs %}
{% tab title="custom\_controller.js" %}
```javascript
import ApplicationController from './application_controller'

export default class extends ApplicationController {
  sayHi () {
    super.sayHi()
    console.log('Hello from a Custom controller')
  }
}
```
{% endtab %}
{% endtabs %}

If you need to override any methods on your Application controller, you can redefine them. Optionally call `super.sayHi(...Array.from(arguments))` to invoke the method on the parent super class.

### Benchmarking your Reflex actions

You might want to see how long your Reflex actions are taking to complete a round-trip, and without Ajax calls to monitor getting reliable metrics requires new approaches.

We suggest making use of the `beforeReflex` and `afterReflex` lifecycle callback methods to sample your performance. As a rule of thumb, anything below 200-300ms will be perceived as "native" by your users.

You can add this code to your desired Reflex controller. If you're making use of the ApplicationController pattern described above, all of your Reflexes will log their round-trip execution times.

{% tabs %}
{% tab title="application\_controller.js" %}
```javascript
  beforeReflex () {
    this.benchmark = performance.now()
  }

  afterReflex (element, reflex) {
    console.log(reflex, `${(performance.now() - this.benchmark).toFixed(0)}ms`)
  }
```
{% endtab %}
{% endtabs %}

### Spinners for long-running actions

You can use `beforeReflex` and `afterReflex` to create UI spinners for anything that might take more than a heartbeat to complete. In addition to providing helpful visual feedback, research has demonstrated that acknowledging a slight delay will result in the user _perceiving_ the delay as being shorter than they would if you did not acknowledge the delay. This is likely because we've been trained by good UI design to understand that this convention means we're waiting on the system. A sluggish UI otherwise forces people to wonder if they have done something wrong, and you don't want that.

{% tabs %}
{% tab title="application\_controller.js" %}
```javascript
  beforeReflex () {
    document.body.classList.add('wait')
  }

  afterReflex () {
    document.body.classList.remove('wait')
  }
```
{% endtab %}

{% tab title="application.css" %}
```css
body.wait, body.wait * {
  cursor: wait !important;
}
```
{% endtab %}
{% endtabs %}

### Autofocus text boxes

If you are working with input elements in your application, you will quickly realize an unfortunate quirk of web browsers is that the `autofocus` attribute is only processed on the initial page load. If you want to implement a "click to edit" UI, you need to use a lifecycle callback method to make sure that the focus lands in the right place.

Handling this problem for every action would be extremely tedious. Luckily we can make use of the `afterReflex` callback to inspect the element to see if it has the `autofocus` attribute and, if so, correctly set the focus on that element.

{% tabs %}
{% tab title="application\_controller.js" %}
```javascript
  afterReflex () {
    const focusElement = this.element.querySelector('[autofocus]')
    if (focusElement) {
      focusElement.focus()

      // shenanigans to ensure that the cursor is placed at the end of the existing value
      const value = focusElement.value
      focusElement.value = ''
      focusElement.value = value
    }
  }
```
{% endtab %}
{% endtabs %}

{% hint style="success" %}
Note that to obtain our **focusElement**, we looked for a single instance of `autofocus` on an element that is a child of our controller. We used **this.element** where **this** is a reference to the Stimulus controller.

If we wanted to only check the element that triggered the Reflex action, we would modify our **afterReflex \(\)** to **afterReflex\(element\)** and then call **element.querySelector** - or just check the attributes directly.

If we wanted to check the whole page for an **autofocus** attribute, we can just use **document.querySelector\('\[autofocus\]'\)** as usual. The square-bracket notation just tells your browser to look for an attribute called **autofocus**, regardless of whether it has a value or not.
{% endhint %}

### Offering visual feedback

We recommend [Velocity](https://github.com/julianshapiro/velocity/wiki) for light, tweening animations that alert the user to UI state changes.

### Capture all DOM update events

Stimulus provides a really powerful event routing syntax that includes custom events, specifying multiple events and capturing events on **document** and **window**.

```markup
<div data-action="cable-ready:after-morph@document->chat#scroll">
```

By capturing the **cable-ready:after-morph** event, we can run code after every update from the server. In this example, the scroll method on our Chat controller is being called to scroll the content window to the bottom, displaying new messages.

### Capture jQuery events with DOM event listeners

Don't hate jQuery: it was a life-saver 12 years ago, and many of its best ideas are now part of the JavaScript language. However, one of the uglier realities of jQuery in a contemporary context is that it has its' own entirely proprietary system for managing events, and it's not compatible with the now-standard DOM Events API.

Sometimes you still need to be able to interface with legacy components, but you don't want to have to write two event handling systems.

[jquery-events-to-dom-events](https://www.npmjs.com/package/jquery-events-to-dom-events) is an npm package that lets you easily access and respond to jQuery events.

### Access Stimulus controller instances

Stimulus doesn't provide an easy way to access a controller instance; you have to have access to your Stimulus application object, the element, the name of the controller and be willing to call an undocumented API.

```javascript
this.application.getControllerForElementAndIdentifier(document.getElementById('users'), 'users')
```

This is ugly, verbose and potentially impossible outside of another Stimulus controller. Wouldn't it be nice to access your controller's methods and local variables from a legacy jQuery component? Just add this line to the **initialize\(\)** method of your Stimulus controllers:

```javascript
this.element[this.identifier] = this
```

This creates a document-scoped variable with the same name as your controller \(or controllers!\) on the element itself, so you can now call **element.controllerName.method\(\)** without any Pilates required. You can read more about this technique [here](https://leastbad.com/stimulus-power-move).

{% hint style="warning" %}
If your controller's identifier doesn't obey the rules of JavaScript variable naming conventions, you will need to specify a viable name for your instance.

For example, if your controller is named _list-item_ you might consider **this.element.listItem = this** for that controller**.**
{% endhint %}

## Server-Side

### Rendering views inside of an ActiveRecord model or ActiveJob class

If you plan to broadcast an update of an html template from somewhere outside a reflex you can draw from the example below.

**The following isn't a complete working example**, but it should set you on the right path.

```python
from django.template.loader import render_to_string
from sockpuppet.channel import Channel


class Notification(models.Model):
    def save(self, *args, **kwargs):
        result = super().save(*args, **kwargs)
        html = render_to_string('my_template.html', {'foo': 'bar'})

        user_session_key = ... # get the user session somehow
        channel = Channel(user_session_key)
        channel.insert_adjacent_html({
            'selector': '#notification_dropdown',
            'position': 'afterbegin',
            'html': html
        })
        channel.broadcast()
```

### Triggering custom events and forcing DOM updates

You can trigger out of band updates with the `Channel` class, it is the workhorse behind Sockpuppet. Take a look at the [source code](https://github.com/jonathan-s/django-sockpuppet/blob/master/sockpuppet/channel.py) to learn more about what kind of updates you can do.

One of the things you can do is to dispatch an event. You can do that with the method `dispatch_event`, which allows you to trigger any event in the client, including custom events and jQuery events.

{% tabs %}
{% tab title="Python" %}
```python
from sockpuppet.reflex import Reflex
from sockpuppet.channel import Channel

class NotificationReflex(Reflex):

    def force_update(id)
        channel = Channel(self.consumer.scope['session'].session_key)
        channel.dispatch_event {
        name: "force:update",
        detail: {id: id},
        }
        channel.broadcast()

    def reload(self):
        # noop: this method exists so we can refresh the DOM
        pass
```
{% endtab %}
{% endtabs %}

{% tabs %}
{% tab title="index.html" %}
```markup
<div data-action="force:update@document->notification#reload">
  <button data-action="notification#forceUpdate">
</div>
```
{% endtab %}
{% endtabs %}

We use the Stimulus event mapper to call our controller's reload method whenever a force:update event is received:

{% tabs %}
{% tab title="notification\_controller.js" %}
```javascript
let lastId

export default class extends Controller {
  forceUpdate () {
    lastId = Math.random()
    this.stimulate("NotificationReflex#force_update", lastId)
  }

  reload (event) {
    const { id } = event.detail
    if (id === lastId) return
    this.stimulate("NotificationReflex#reload")
  }
}
```
{% endtab %}
{% endtabs %}

By passing a randomized number to the Reflex as an argument, we allow ourselves to return before triggering a reload if we were the ones that initiated the operation.

#### Coming Soon: Notifications

## Anti-Patterns

#### Coming Soon: How to change the URL rendered by a reflex
