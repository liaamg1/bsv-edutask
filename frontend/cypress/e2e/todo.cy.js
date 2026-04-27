let uid
let name
let email
function login(){
    
    before(function () {
    cy.fixture('user.json')
    .then((user) => {
            cy.request({
            method: 'POST',
            url: 'http://localhost:5000/users/create',
            form: true,
            body: user
        }).then((response) => {
            uid = response.body._id.$oid
            name = user.firstName + ' ' + user.lastName
            email = user.email
        })
    })
    })
    beforeEach(function(){
        cy.visit('http://localhost:3000')
        cy.contains('div', 'Email Address')
        .find('input[type=text]')
        .type(email)
    cy.get('form')
        .submit()
    })
    
    
}

describe('R8UC1', () => {
    login()

    after(() => {
        cy.request('DELETE', `http://localhost:5000/users/${uid}`)
    })
})

describe('R8UC2 - Toggle todo-item as done or active', () => {
    login()

    it("Toggle todo-item as done", ()=> {
        // Write Task Title
        cy.get("#title").type("Go to the movies")
        // Create Task
        cy.get('input[value="Create new Task"]').click()
        // Enter Task
        cy.get(".title-overlay").contains("Go to the movies").click()
        // Write Todo-Item
        cy.get('input[placeholder="Add a new todo item"]').should('be.visible').type("Buy popcorn")
        // Add Todo-Item
        cy.get('input[value="Add"]').click()
        // Click check box
        cy.get(".checker.unchecked").first().click()
    })

    it("Toggle todo-item as active", () => {
        // Write Task Title
        cy.get("#title").type("Go to the films")
        // Create Task
        cy.get('input[value="Create new Task"]').click()
        // Enter Task
        cy.get(".title-overlay").contains("Go to the films").click()
        // Write Todo-Item
        cy.get('input[placeholder="Add a new todo item"]').should('be.visible').type("Buy popcorn")
        // Add Todo-Item
        cy.get('input[value="Add"]').click()
        // Click check box
        cy.get(".checker.unchecked").first().click()
        // Click check box
        cy.get(".checker.checked").first().click()
    })

    after(() => {
        cy.request('DELETE', `http://localhost:5000/users/${uid}`)
    })
})

describe('R8UC3 - Delete todo-item', () => {
    login()

    after(() => {
        cy.request('DELETE', `http://localhost:5000/users/${uid}`)
    })
})