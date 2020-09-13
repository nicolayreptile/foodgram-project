
class Api {
    constructor(apiUrl) {
        this.apiUrl =  apiUrl;
        this.csrftoken = csrftoken;
    }
  getPurchases () {
    return fetch(this.apiUrl+`/shoplist`, {
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': this.csrftoken        
      }
    })
      .then( e => {
          if(e.ok) {
              return e.json()
          }
          return Promise.reject(e.statusText)
      })
  }
  addPurchases (id) {
    return fetch(this.apiUrl+`/shoplist/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': this.csrftoken
      },
      body: JSON.stringify({
        recipe: id
      })
    })
      .then( e => {
          if(e.ok) {
              return e.json()
          }
          return Promise.reject(e.statusText)
      })
  }
  removePurchases (id){
    return fetch(this.apiUrl+`/shoplist/${id}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': this.csrftoken
      }
    })
      .then( e => {
          if(e.ok) {
              return e.data
          }
          return Promise.reject(e.statusText)
      })
  }
  addSubscriptions(id) {
    return fetch(this.apiUrl + `/follow/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': this.csrftoken
      },
      body: JSON.stringify({
        author: id
      })
    })
      .then( e => {
          if(e.ok) {
              return e.data
          }
          return Promise.reject(e.statusText)
      })
  }
  removeSubscriptions (id) {
    return fetch(this.apiUrl + `/follow/${id}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': this.csrftoken
      }
    })
      .then( e => {
          if(e.ok) {
              return e.data
          }
          return Promise.reject(e.statusText)
      })
  }
  addFavorites (id)  {
    return fetch(this.apiUrl+`/favorites/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': this.csrftoken
      },
      body: JSON.stringify({
        recipe: id,
      })
    })
        .then( e => {
            if(e.ok) {
                return e.json()
            }
            return Promise.reject(e.statusText)
        })
  }
  removeFavorites (id) {
    return fetch(apiUrl+`/favorites/${id}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': this.csrftoken
      },
    })
        .then( e => {          
            if(e.status == 204) {
                return e.data
            }
            return Promise.reject(e.statusText)
        })
  }
    getIngredients  (text)  {
        return fetch(apiUrl+`/ingredient/list/${text}`, {
            headers: {
                'Content-Type': 'application/json'
            }
        })
            .then( e => {
                if(e.ok) {
                    return e.json()
                }
                return Promise.reject(e.statusText)
            })
    }

}
