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
describe('R8UC1 - ', () => {
    login()
    it('Write description and submit todo item successfully.', () => {
        cy.get("#title").type("Go to the movies")
        cy.get('input[value="Create new Task"]').click()
        
        cy.contains("Go to the movies").should("exist")
    })
    it('Empty description and submit disabled.', () => {
        cy.get('input[value="Create new Task"]').should('be.disabled')
        
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