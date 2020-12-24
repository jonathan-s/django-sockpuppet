---
description: Forms fly business class on StimulusReflex Airways ✈️
---

# Working with HTML Forms

## Single source of truth

While stateless form submissions have technically always suffered from the "last update wins" problem, it's only in recent years that developers have created interfaces that need to respond to changing application state in real-time.

There are a few guiding principles that we adhere to when building a technology that can change the page you're on, even while you're busy working on something important. One of the biggest wins associated with keeping the web server as the single source of truth about the state of your application and its data is that you don't have to worry about the synchronization of state with the client. Whatever you see on your screen is the same thing that you would see if you hit refresh. This makes developing applications with django-sockpuppet faster and significantly less complicated than equivalent solutions which make use of SPAs like React.

However, **django-sockpuppet will never overwrite the value of a text input or textarea element if it has active focus in your browser**. This exception is important because there's no compelling UI experience where you want to change the contents of an input element _while the user is typing into it_.

We've worked really hard to make sure that developers can update other aspects of the active text input element. For example, it's possible to change the background color or even mark the element as disabled while you're typing into it. However, all attempts to overwrite the input element's value will be silently suppressed.

If you need to filter or constrain the contents of a text input, consider using a client-side library such as [Cleave.js](https://nosir.github.io/cleave.js/) instead of trying to circumvent the Single Source of Truth mechanisms, which are there to protect your users from their fellow collaborators.

Note that this concept only applies to the active text input element. Any elements which are marked with `data-reflex-permanent` will not be morphed in any way.

## Form submission

Django-sockpuppet gathers all of the attributes on the element that initiates a Reflex. All of this data gets packed into an object that is made available to your Reflex action method through the `element` accessor. You can even [scoop up the attributes of parent elements](https://sockpuppet.argpar.se/reflexes#inheriting-data-attributes-from-parent-elements). This leaves form submission in the cold, though... doesn't it? 🥶

### The `params` accessor

_Heck no!_ If a Reflex is called on a `form` element - or a **child** of that `form` element - then the data for the whole form will be properly serialized and made available to the Reflex action method as the `params` accessor. `params` is a dictionary that you can input into a django form as data, and then validate that data as you normally would.

One of the most exciting benefits of this design is that autosaving the data in your form becomes as simple as adding `data-reflex="change->Post#update"` to each field. Since the field is inside the parent `form` element, all inputs are automatically serialized and sent to your Reflex class.

You are free to add additional business logic on the client using the Reflex [lifecycle callbacks](https://sockpuppet.argpar.se/lifecycle) in your Stimulus controllers.

Reflex actions called outside of a form will still have a `params` instance variable; it will be an empty dictionary.

{% hint style="danger" %}
If you call a full-page update Reflex outside of a form that has unsaved data, you will lose the data in the form. You will also lose the data if you throw your laptop into a volcano. 🌋
{% endhint %}

#### Modifying form data before sending to the server

Should you need to modify the contents of your params before the Reflex sends the data to the server, you can use the `before` callbacks to do so:

```javascript
document.addEventListener('stimulus-reflex:before', event => {
  const { params } = event.target.reflexData
  event.target.reflexData.params = { ...params, foo: true, bar: false }
})
```

#### A note about &lt;input type="file"&gt; fields

At the time of this writing, **forms that upload files are unsupported by django-sockpuppet**. We suggest that you design your UI in such a way that files can be uploaded directly, making use of the standard django-form upload techniques. You might need to use `data-reflex-permanent` so that you don't lose UI state when a Reflex is triggered.

As websockets is a text-based protocol that doesn't guarantee packet delivery or the order of packet arrival, it is not well-suited to uploading binary files. This is an example of a problem best solved with vanilla Django.

#### Resetting a Submitted Form

If you submit a form via django-sockpuppet, and the resulting DOM diff doesn't touch the form, you will end up with stale data in your form `<input>` fields. You're going to need to clear your form so the user can add more data.

One simple technique is to use a Stimulus controller to reset the form after the Reflex completes successfully. We'll call this controller `reflex-form` and we'll use it to set a target on the first text field, as well as an action on the submit button:

```html
<form data-controller="form">
    <input type="text" data-form-target="focus">
    <button data-action="click->form#submit"></button>
</form>
```

This controller will make use of the [Promise](https://sockpuppet.argpar.se/lifecycle#promises) returned by the `stimulate` method:

```javascript
// my_app/javascript/form_controller.js
import { Controller } from 'stimulus';

export default class extends Controller {
  static targets = ['focus']
  submit (e) {
    e.preventDefault()
    this.stimulate(this.data.get('reflex')).then(() => {
      this.element.reset()
      // optional: set focus on the freshly cleared input
      this.focusTarget.focus()
    })
  }
}
```
