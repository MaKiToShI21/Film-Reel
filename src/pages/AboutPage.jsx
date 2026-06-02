import { Link } from 'react-router-dom';

export default function AboutPage() {
  return (
    <section className="about-page">
      <article className="about-card">
        <header className="about-header">
          <h1>О проекте FilmReel</h1>
          <p className="about-lead">
            FilmReel — это домашний каталог фильмов, где можно искать картины,
            читать описания и просматривать рейтинги. Версия на React работает
            без серверной части: данные хранятся в памяти браузера.
          </p>
        </header>

        <div className="about-section">
          <h2 className="about-section-title">Что можно делать на сайте</h2>
          <ul className="about-features">
            <li className="about-feature">
              <h3 className="about-feature-title">Смотреть каталог</h3>
              <p>
                На главной собраны фильмы с постерами, жанрами, режиссёрами
                и кратким описанием. Удобно листать и быстро находить нужное.
              </p>
            </li>
            <li className="about-feature">
              <h3 className="about-feature-title">Искать и фильтровать</h3>
              <p>
                Поиск работает по названию, описанию и жанру. В боковой панели
                можно отфильтровать фильмы по жанру, режиссёру и тегам,
                а также отсортировать их по дате добавления или рейтингу.
              </p>
            </li>
            <li className="about-feature">
              <h3 className="about-feature-title">Добавлять фильмы</h3>
              <p>
                Через форму можно пополнить каталог: указать название, год,
                описание, жанры, режиссёров, теги и технические детали.
                Новые записи сразу появляются в списке.
              </p>
            </li>
            <li className="about-feature">
              <h3 className="about-feature-title">React без бэкенда</h3>
              <p>
                Приложение построено на компонентах React. Авторизация, база
                данных и серверные запросы не используются — это учебная
                клиентская версия проекта.
              </p>
            </li>
          </ul>
        </div>

        <footer className="about-footer">
          <Link className="btn about-link" to="/">
            Перейти в каталог
          </Link>
        </footer>
      </article>
    </section>
  );
}
