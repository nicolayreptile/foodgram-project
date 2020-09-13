const container = document.getElementById('subscribe_btn');
const counterId = document.querySelector('#counter');
const api = new Api(apiUrl);
const header = new Header(counterId);
const configButton = {
    subscribe: {
        attr: 'data-out',
        default: {
            class: 'button_style_blue',
            text: 'Подписаться на автора'
        },
        active: {
            class: 'button_style_light-blue-outline',
            text: `Отписаться`
        }
    }
}
const subscribe = new Subscribe(configButton.subscribe, api);
const myFollow = new AuthorFollow(container, '.card-user', header, api, true,{
    subscribe
})
myFollow.addEvent();