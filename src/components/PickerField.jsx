function PickerField({ label, items, selectedIds, onToggle, error, nameKey = 'name' }) {
  const fieldClass = error
    ? 'film-form-field film-form-field--picker film-form-field--error'
    : 'film-form-field film-form-field--picker';

  return (
    <div className={fieldClass}>
      <span className="film-form-label">{label}</span>
      <ul className="film-form-picker-list">
        {items.length ? (
          items.map((item) => (
            <li key={item.id}>
              <label className="film-form-picker-item">
                <input
                  type="checkbox"
                  className="film-form-picker-input"
                  checked={selectedIds.includes(item.id)}
                  onChange={() => onToggle(item.id)}
                />
                <span>{item[nameKey]}</span>
              </label>
            </li>
          ))
        ) : (
          <li className="film-form-picker-empty">Нет записей</li>
        )}
      </ul>
      {error && (
        <ul className="film-form-errors">
          <li>{error}</li>
        </ul>
      )}
    </div>
  );
}

export default PickerField;
