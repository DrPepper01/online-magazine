document.addEventListener('DOMContentLoaded', () => {
  const { useState, useEffect } = React;
  const { render } = ReactDOM;

  const SearchComponent = () => {
    const [searchQuery, setSearchQuery] = useState('');
    const [searchResults, setSearchResults] = useState([]);

    const handleSearch = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/product/search/?q=${encodeURIComponent(searchQuery)}');
        const data = await response.json();
        setSearchResults(data);
      } catch (error) {
        console.error('Ошибка при выполнении запроса:', error);
      }
    };

    useEffect(() => {
      handleSearch();
    }, []); // Вызывается при загрузке компонента

    window.submitSearch = () => {
      handleSearch();
    };

    return (
      <div>
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Введите запрос"
          onInput={submitSearch} />
        <button onClick={submitSearch}>Искать</button>

        <ul>
          {searchResults.map((result) => (
            <li key={result.id}>{result.title}</li>
          ))}
        </ul>
      </div>
    );
  };

  const searchContainer = document.getElementById('search-container');
  if (searchContainer) {
    render(<SearchComponent />, searchContainer);
  }
});
