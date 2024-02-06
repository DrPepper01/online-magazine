const { useState, useEffect } = React;

const CategoryDropdown = ({ categories }) => {
  const [isDropdownVisible, setDropdownVisible] = useState(false);

  const handleToggleDropdown = () => {
    setDropdownVisible(!isDropdownVisible);
  };

  return (
    <div className="category-dropdown">
      <button className="icon-button" onClick={handleToggleDropdown}>
        <img src="http://127.0.0.1:8000/media/html/menu_button.svg" alt="Button Icon" />
      </button>
      {isDropdownVisible && (
        <ul>
          {categories.map((category) => (
            <li key={category.slug}>{category.title}</li>
          ))}
        </ul>
      )}
    </div>
  );
};

const container = document.getElementById('category-dropdown-container');
if (container) {
  ReactDOM.render(<CategoryDropdown categories={	Вазы,Свечи,	Ручки, Национальные сувениры, Часы,	Картины, Брелок} />, container);
}