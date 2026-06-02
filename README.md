# FilmReel — React

Клиентский каталог фильмов на React (лабораторная работа №13).

## Требования

- Node.js 20+
- npm

## Запуск

```bash
npm install
npm run dev
```

Приложение откроется по адресу http://localhost:5173

## Сборка

```bash
npm run build
npm run preview
```

## Возможности

- Каталог фильмов с поиском и фильтрами
- Сортировка по дате добавления и рейтингу
- Форма добавления фильма с валидацией
- Страница «О нас»

Данные хранятся в памяти браузера, бэкенд не используется.

## Структура

```
public/          # CSS, постеры, иконки
src/
  components/    # Header, Footer, FilmCard, форма
  context/       # FilmsContext — состояние каталога
  data/          # начальные mock-данные
  pages/         # CatalogPage, AddFilmPage, AboutPage
  utils/         # фильтрация, сортировка, валидация
```
