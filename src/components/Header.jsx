import { Link } from 'react-router-dom';

export default function Header({ searchQuery, onSearchChange, onSearchSubmit }) {
  return (
    <header>
      <div className="header header-shell">
        <Link className="header-brand" to="/">
          FilmReel
        </Link>
        <nav>
          <ul className="mainmenu">
            <li>
              <Link to="/">Главная</Link>
            </li>
            <li>
              <Link to="/about">О нас</Link>
            </li>
          </ul>
        </nav>
        <form
          className="header-search"
          onSubmit={(event) => {
            event.preventDefault();
            onSearchSubmit();
          }}
        >
          <input
            type="search"
            value={searchQuery}
            onChange={(event) => onSearchChange(event.target.value)}
            placeholder="Поиск по названию, описанию, жанру"
            aria-label="Поиск фильмов"
          />
          <button type="submit">Найти</button>
        </form>
      </div>
    </header>
  );
}
