import { Link } from 'react-router-dom';

function FilterSection({ title, items, selectedIds, onToggle }) {
  return (
    <div className="sidebar-section">
      <h3 className="sidebar-title">{title}</h3>
      <ul className="sidebar-filter-list">
        {items.length ? (
          items.map((item) => (
            <li key={item.id}>
              <label className="sidebar-checkbox">
                <input
                  type="checkbox"
                  value={item.id}
                  checked={selectedIds.includes(item.id)}
                  onChange={() => onToggle(item.id)}
                />
                <span>{item.name ?? item.tag}</span>
              </label>
            </li>
          ))
        ) : (
          <li className="sidebar-empty">Нет записей</li>
        )}
      </ul>
    </div>
  );
}

export default function CatalogSidebar({
  genres,
  directors,
  tags,
  selectedGenres,
  selectedDirectors,
  selectedTags,
  onToggleGenre,
  onToggleDirector,
  onToggleTag,
  onApplyFilters,
  onResetFilters,
  hasActiveFilters,
  searchQuery,
}) {
  return (
    <>
      <Link to="/add" className="sidebar-add-film">
        <img src="/img/add.png" alt="" className="sidebar-add-film-icon" width="22" height="22" />
        <span>Добавить фильм</span>
      </Link>

      <form
        className="catalog-filter-form"
        onSubmit={(event) => {
          event.preventDefault();
          onApplyFilters();
        }}
      >
        <FilterSection
          title="Жанры"
          items={genres}
          selectedIds={selectedGenres}
          onToggle={onToggleGenre}
        />
        <FilterSection
          title="Режиссёры"
          items={directors}
          selectedIds={selectedDirectors}
          onToggle={onToggleDirector}
        />
        <FilterSection
          title="Теги"
          items={tags}
          selectedIds={selectedTags}
          onToggle={onToggleTag}
        />

        <div className="sidebar-actions">
          <button type="submit" className="btn sidebar-apply-btn">
            Применить
          </button>
          {(hasActiveFilters || searchQuery) && (
            <button type="button" className="sidebar-reset-link" onClick={onResetFilters}>
              Сбросить
            </button>
          )}
        </div>
      </form>
    </>
  );
}
