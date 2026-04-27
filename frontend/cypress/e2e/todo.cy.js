describe('R8UC1', () => {
    let uid
    let name
    let email
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
    
    after(() => {
        cy.request('DELETE', `http://localhost:5000/users/${uid}`)
    })
})