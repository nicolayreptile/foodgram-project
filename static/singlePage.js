const container = document.querySelector('.single-card');
const counterId = document.querySelector('#counter');
const api = new Api(apiUrl);
const header = new Header(counterId);

const configButton = {
    purchpurachases: {
        attr: 'data-out',
        default: {
            class: 'button_style_blue',
            text: '<span class="icon-plus button__icon"></span>Добавить в покупки'
        },
        active: {
            class: 'button_style_light-blue-outline',
            text: `<span class="icon-check button__icon"></span> Рецепт добавлен`
        }
    },
    favorites: {
        attr: 'data-out',
        default: {
            text: '<span class="icon-favorite icon-favorite_big"></span>'
        },
        active: {
            text: `<span class="icon-favorite icon-favorite_big icon-favorite_active"></span>`
        }
    },
    subscribe: {
        attr: 'data-out',
        default: {
            class: 'button_style_light-blue',
            text: 'Подписаться на автора'
        },
        active: {
            class: 'button_style_light-blue-outline',
            text: `<span class="icon-check button__icon"></span> Отписаться от автора`
        }
    }
}
const purchpurachases = new Purchases(configButton.purchpurachases, api);
const favorites = new Favorites(configButton.favorites, api);
const subscribe = new Subscribe(configButton.subscribe, api);


const singleCard = new SingleCard(container, '.single-card', header, api, true,{
    purchpurachases,
    favorites,
    subscribe
});
singleCard.addEvent();


