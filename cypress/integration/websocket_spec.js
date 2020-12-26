describe("Integration tests", () => {
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
})
