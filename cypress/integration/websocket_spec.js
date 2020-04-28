describe("Integration tests", () => {

    it("has session persistance for anonymous user!", () => {
        cy.visit('/test/')
        cy.get('#counter').should('have.text', '0')
        cy.wait(100)

        cy.get('#link').click()
        cy.get('#counter').should('have.text', '1')

        cy.reload(true)

        cy.get('#counter').should('have.text', '1')
    })
})
