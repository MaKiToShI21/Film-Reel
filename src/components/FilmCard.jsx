import { memo } from 'react';
import { getNamesByIds, truncateText } from '../utils/catalogUtils';

function FilmCard({ film, genres, directors, tags }) {
  const genreNames = getNamesByIds(genres, film.genreIds);
  const directorNames = getNamesByIds(directors, film.directorIds);
  const filmTags = tags.filter((tag) => film.tagIds.includes(tag.id));

  return (
    <article className="film-catalog-card">
      <div className="film-catalog-poster">
        {film.poster ? (
          <img src={film.poster} alt={`Постер: ${film.title}`} />
        ) : (
          <div className="film-catalog-poster-fallback">Нет фото</div>
        )}
      </div>

      <div className="film-catalog-body">
        <header className="film-catalog-header">
          <div className="film-catalog-title-wrap">
            <h2 className="film-catalog-title">
              <span>{film.title}</span>
            </h2>
          </div>
          <div className="film-catalog-rating" title="Оценка">
            <span className="film-field-label">Оценка</span>
            <span className="film-catalog-rating-value">&#9733; {film.rating.toFixed(1)}</span>
          </div>
        </header>

        <dl className="film-catalog-fields">
          <div className="film-catalog-field">
            <dt>Жанр</dt>
            <dd>{genreNames.length ? genreNames.join(', ') : '—'}</dd>
          </div>
          <div className="film-catalog-field">
            <dt>Режиссёр</dt>
            <dd>{directorNames.length ? directorNames.join(', ') : '—'}</dd>
          </div>
          <div className="film-catalog-field film-catalog-field--tags">
            <dt>Теги</dt>
            <dd>
              {filmTags.length ? (
                <ul className="film-catalog-tags">
                  {filmTags.map((tag) => (
                    <li key={tag.id}>
                      <span>{tag.tag}</span>
                    </li>
                  ))}
                </ul>
              ) : (
                '—'
              )}
            </dd>
          </div>
          <div className="film-catalog-field film-catalog-field--description">
            <dt>Описание</dt>
            <dd>{truncateText(film.description || 'Описание пока не добавлено.')}</dd>
          </div>
        </dl>
      </div>
    </article>
  );
}

export default memo(FilmCard);
