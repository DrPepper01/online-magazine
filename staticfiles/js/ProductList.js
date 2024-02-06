// ProductList.js
const { useState, useEffect } = React;

function ProductList() {
  const [products, setProducts] = useState([]);

  const fetchProducts = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/product/');
      const data = await response.json();
      setProducts(data);
    } catch (error) {
      console.error('Ошибка при получении данных:', error);
    }
  };

  useEffect(() => {
    fetchProducts();
  }, []);

  const navigateToDetail = (productId) => {
    // Перенаправляем пользователя на страницу с деталями продукта
    window.location.href = `http://127.0.0.1:8000/products_list/${productId}`;
  };

  return (
    <div className="product-list-container">
      {products.map((product) => (
        <div key={product.id} className="product-item">
          {product.images && product.images.length > 0 && (
            <img
              src={product.images[0].image}
              alt={`${product.title} - изображение`}
              className="product-image"
            />
          )}
          <h3>{product.title}</h3>
          <p>Цена: {product.price}</p>
          {/* Добавляем обработчик события для перенаправления */}
          <button onClick={() => navigateToDetail(product.id)}>Подробнее</button>
        </div>
      ))}
    </div>
  );
}

const container = document.getElementById('product-list-container');
if (container) {
  ReactDOM.render(<ProductList />, container);
}
