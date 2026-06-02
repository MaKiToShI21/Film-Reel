import { useMemo, useState } from 'react';
import CatalogSidebar from '../components/CatalogSidebar';
import FilmCard from '../components/FilmCard';
import { useFilms } from '../context/FilmsContext';
import { filterFilms, sortFilms } from '../utils/catalogUtils';

function toggleId(list, id) {
  return list.includes(id) ? list.filter((item) => item !== id) : [...list, id];
}

export default function CatalogPage({ searchQuery, onSearchQueryChange }) {
  const { films, genres, directors, tags } = useFilms();
  const [sortBy, setSortBy] = useState('date');
  const [selectedGenres, setSelectedGenres] = useState([]);
  const [selectedDirectors, setSelectedDirectors] = useState([]);
  const [selectedTags, setSelectedTags] = useState([]);
  const [appliedFilters, setAppliedFilters] = useState({
    genreIds: [],
    directorIds: [],
    tagIds: [],
  });

  const visibleFilms = useMemo(() => {
    const filtered = filterFilms(
      films,
      {
        searchQuery,
        genreIds: appliedFilters.genreIds,
        directorIds: appliedFilters.directorIds,
        tagIds: appliedFilters.tagIds,
      },
      { genres },
    );
    return sortFilms(filtered, sortBy);
  }, [films, searchQuery, appliedFilters, sortBy, genres]);

  const hasActiveFilters =
    appliedFilters.genreIds.length > 0 ||
    appliedFilters.directorIds.length > 0 ||
    appliedFilters.tagIds.length > 0;

  const handleApplyFilters = () => {
    setAppliedFilters({
      genreIds: selectedGenres,
      directorIds: selectedDirectors,
      tagIds: selectedTags,
    });
  };

  const handleResetFilters = () => {
    setSelectedGenres([]);
    setSelectedDirectors([]);
    setSelectedTags([]);
    setAppliedFilters({ genreIds: [], directorIds: [], tagIds: [] });
    onSearchQueryChange('');
  };

  return (
    <div className="catalog-layout">
      <aside className="catalog-sidebar">
        <CatalogSidebar
          genres={genres}
          directors={directors}
          tags={tags}
          selectedGenres={selectedGenres}
          selectedDirectors={selectedDirectors}
          selectedTags={selectedTags}
          onToggleGenre={(id) => setSelectedGenres((current) => toggleId(current, id))}
          onToggleDirector={(id) => setSelectedDirectors((current) => toggleId(current, id))}
          onToggleTag={(id) => setSelectedTags((current) => toggleId(current, id))}
          onApplyFilters={handleApplyFilters}
          onResetFilters={handleResetFilters}
          hasActiveFilters={hasActiveFilters}
          searchQuery={searchQuery}
        />
      </aside>

      <main className="catalog-main">
        <div className="catalog-heading">
          <h1>Каталог фильмов</h1>
          <p>Найдено фильмов: {visibleFilms.length}</p>
          <div className="catalog-sort-form">
            <label className="catalog-sort-label" htmlFor="catalog-sort">
              Сортировать по:
            </label>
            <select
              className="catalog-sort-select"
              id="catalog-sort"
              value={sortBy}
              onChange={(event) => setSortBy(event.target.value)}
            >
              <option value="date">дате добавления</option>
              <option value="rating">рейтингу</option>
            </select>
          </div>
        </div>

        <div className="film-cards">
          {visibleFilms.length ? (
            visibleFilms.map((film) => (
              <FilmCard
                key={film.id}
                film={film}
                genres={genres}
                directors={directors}
                tags={tags}
              />
            ))
          ) : (
            <p className="error-message">Фильмы не найдены.</p>
          )}
        </div>
      </main>
    </div>
  );
}
