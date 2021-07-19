describe("Integration tests", () => {
  // TODO, use something like this https://github.com/cypress-io/cypress/issues/1922
  // Then we can replace the cy.wait(200)
  it("has session persistance for anonymous user!", () => {
    cy.visit('/test/')
    cy.get('#counter').should('have.text', '0')
    cy.wait(200)

    cy.get('#link').click()
    cy.get('#counter').should('have.text', '1')

    cy.reload(true)

    cy.get('#counter').should('have.text', '1')
  }),

  it("are able to use reflex which isn't registered", () => {
    cy.visit('/test/')
    cy.get('#counter-2').should('have.text', '0')
    cy.wait(200)

    cy.get('#decrementor').click()
    cy.get('#counter-2').should('have.text', '-1')
  }),

  it('is able to submit and get form parameters', () => {
    cy.visit('/test/')
    cy.get('#text-input').type('Hello world')
    cy.get('#submit').click()
    cy.wait(200)

    cy.get('#text-output').should('have.text', 'Hello world')
  })

  it("get parameters won't throw exceptions when triggering reflex", () => {
    cy.visit('/param/?word=world')
    cy.get('#word').should('have.text', 'world')
    cy.wait(200)

    cy.get('#button').click()
    cy.get('#word').should('have.text', 'space')
  })

  it("is able to use the generated static thing without issues", () => {
    cy.visit('/test-static/')
    cy.get('#decrementor-counter').should('have.text', '0')
    cy.wait(200)

    cy.get('#decrementor').click()
    cy.get('#decrementor-counter').should('have.text', '-1')
  })

  it("throws an error in frontend when using error reflex", () => {
    cy.visit('/error/')
    cy.wait(200)

    cy.get("#increment").click()
    cy.wait(200)
    cy.window().then((win) => {
      expect(win.console.log).to.have.callCount(2);
      let secondCall = win.console.log.args[1][0]
      expect(secondCall).to.contain('failed')
    });
  })

  it("able to use a list view without errors", () => {
    cy.visit('/users/')
    cy.wait(200)
    cy.get('#button').click()

    cy.get('#success').should('have.text', 'True')
  })

  it("able to use a detail view without errors", () => {
    cy.visit('/users/1/')
    cy.wait(200)
    cy.get('#user-button').click()
    cy.wait(200)

    cy.get('#user-reflex').should('have.text', 'test_user')
  })
})
