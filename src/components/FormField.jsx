function FormField({
  id,
  label,
  type = 'text',
  value,
  onChange,
  onBlur,
  error,
  help,
  inputProps = {},
  children,
}) {
  const fieldClass = error ? 'film-form-field film-form-field--error' : 'film-form-field';

  return (
    <div className={fieldClass}>
      <label className="film-form-label" htmlFor={id}>
        {label}
      </label>
      {children ?? (
        <input
          id={id}
          type={type}
          className="film-form-input"
          value={value}
          onChange={onChange}
          onBlur={onBlur}
          {...inputProps}
        />
      )}
      {help && <p className="film-form-help">{help}</p>}
      {error && (
        <ul className="film-form-errors">
          <li>{error}</li>
        </ul>
      )}
    </div>
  );
}

export default FormField;
