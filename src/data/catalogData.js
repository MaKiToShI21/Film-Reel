export const genres = [
  { id: 1, name: 'Боевик' },
  { id: 2, name: 'Биография' },
  { id: 3, name: 'Драма' },
  { id: 4, name: 'Криминал' },
  { id: 5, name: 'Приключения' },
  { id: 6, name: 'Фантастика' },
];

export const directors = [
  { id: 1, name: 'Джеймс Кэмерон' },
  { id: 2, name: 'Дени Вильнёв' },
  { id: 3, name: 'Квентин Тарантино' },
  { id: 4, name: 'Кристофер Нолан' },
  { id: 5, name: 'Мартин Скорсезе' },
  { id: 6, name: 'Питер Джексон' },
];

export const tags = [
  { id: 1, tag: 'блокбастер', slug: 'blockbuster' },
  { id: 2, tag: 'классика', slug: 'classic' },
  { id: 3, tag: 'осцар', slug: 'oscar' },
  { id: 4, tag: 'фантастика', slug: 'sci-fi' },
  { id: 5, tag: 'эпик', slug: 'epic' },
];

export const initialFilms = [
  {
    id: 1,
    title: 'Начало',
    year: 2010,
    rating: 8.7,
    description:
      'Профессиональный вор Дом Кobb специализируется на краже секретов из подсознания во время сна. Ему предлагают шанс вернуться домой, если он выполнит невозможное — не украсть идею, а внедрить её.',
    poster: '/posters/Начало.webp',
    addedAt: '2026-01-10T12:00:00.000Z',
    genreIds: [6, 3],
    directorIds: [4],
    tagIds: [1, 4],
  },
  {
    id: 2,
    title: 'Дюна',
    year: 2021,
    rating: 8.2,
    description:
      'Наследник знатного дома Атрейдесов отправляется на опасную планету Арракис, чтобы обеспечить будущее своей семьи и народа.',
    poster: '/posters/Дюна.webp',
    addedAt: '2026-01-15T10:30:00.000Z',
    genreIds: [5, 6],
    directorIds: [2],
    tagIds: [1, 5],
  },
  {
    id: 3,
    title: 'Криминальное чтиво',
    year: 1994,
    rating: 8.9,
    description:
      'Двое бандитов Винcent Vega и Jules Winfield ведут философские беседы между «делами», пока судьба переплетает их истории с другими персонажами Лос-Анджелеса.',
    poster: '/posters/Криминальное_чтиво.webp',
    addedAt: '2026-02-01T09:00:00.000Z',
    genreIds: [4, 3],
    directorIds: [3],
    tagIds: [2, 3],
  },
  {
    id: 4,
    title: 'Титаник',
    year: 1997,
    rating: 7.9,
    description:
      'История любви между бедным художником и молодой аристократкой на борту легендарного лайнера, обречённого на трагическую гибель.',
    poster: '/posters/Титаник.webp',
    addedAt: '2026-02-05T14:20:00.000Z',
    genreIds: [3],
    directorIds: [1],
    tagIds: [2, 3],
  },
  {
    id: 5,
    title: 'Властелин колец: Братство кольца',
    year: 2001,
    rating: 8.8,
    description:
      'Молодой хоббит Фродо получает в наследство Кольцо Власти и отправляется в опасное путешествие, чтобы уничтожить его в огне Роковой горы.',
    poster: '/posters/Властелин_колец.webp',
    addedAt: '2026-02-12T11:45:00.000Z',
    genreIds: [5, 6],
    directorIds: [6],
    tagIds: [2, 5],
  },
  {
    id: 6,
    title: 'Волк с Уолл-стрит',
    year: 2013,
    rating: 8.1,
    description:
      'История взлёта и падения брокера Джордана Belfort, который построил империю на манипуляциях и неумолимой жажде богатства.',
    poster: '/posters/Волк_с_Уолл-стрит.jpg',
    addedAt: '2026-02-20T16:00:00.000Z',
    genreIds: [2, 3],
    directorIds: [5],
    tagIds: [1, 3],
  },
  {
    id: 7,
    title: 'Аватар',
    year: 2009,
    rating: 7.8,
    description:
      'Бывший морпех отправляется на далёкую луну Пандора, где конфликт между людьми и коренным народом набирает обороты.',
    poster: '/posters/Аватар.jpg',
    addedAt: '2026-03-01T08:15:00.000Z',
    genreIds: [1, 5, 6],
    directorIds: [1],
    tagIds: [1, 4],
  },
];
