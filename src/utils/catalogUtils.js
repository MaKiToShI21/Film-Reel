export function getNamesByIds(items, ids) {
  return items.filter((item) => ids.includes(item.id)).map((item) => item.name ?? item.tag);
}

export function filterFilms(films, { searchQuery, genreIds, directorIds, tagIds }, lookup) {
  const query = searchQuery.trim().toLowerCase();

  return films.filter((film) => {
    if (genreIds.length && !genreIds.some((id) => film.genreIds.includes(id))) {
      return false;
    }
    if (directorIds.length && !directorIds.some((id) => film.directorIds.includes(id))) {
      return false;
    }
    if (tagIds.length && !tagIds.some((id) => film.tagIds.includes(id))) {
      return false;
    }

    if (!query) {
      return true;
    }

    const genreNames = getNamesByIds(lookup.genres, film.genreIds).join(' ');
    const haystack = `${film.title} ${film.description} ${genreNames}`.toLowerCase();
    return haystack.includes(query);
  });
}

export function sortFilms(films, sortBy) {
  const sorted = [...films];

  if (sortBy === 'rating') {
    sorted.sort((a, b) => b.rating - a.rating || b.addedAt.localeCompare(a.addedAt));
  } else {
    sorted.sort((a, b) => b.addedAt.localeCompare(a.addedAt));
  }

  return sorted;
}

export function truncateText(text, maxLength = 280) {
  if (text.length <= maxLength) {
    return text;
  }
  return `${text.slice(0, maxLength).trimEnd()}…`;
}
