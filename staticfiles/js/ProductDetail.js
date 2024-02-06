// ProductDetail.js
const { useState, useEffect } = React;

function ProductDetail({ productId, onClose }) {
  const [product, setProduct] = useState(null);

  const fetchProductDetail = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/product/${productId}/`);
      const data = await response.json();
      setProduct(data);
    } catch (error) {
      console.error('Ошибка при получении данных о продукте:', error);
    }
  };

  useEffect(() => {
    fetchProductDetail();
  }, [productId]);

  return (
    <div className="product-detail-overlay">
      <div className="product-detail">
        <button onClick={onClose}>Закрыть</button>
        {product ? (
          <div>
            <h2>{product.title}</h2>
            <p>Цена: {product.price}</p>
            <p>{product.description}</p>
            {product.images && product.images.length > 0 && (
              <div className="product-images">
                {product.images.map((image, index) => (
                  <img key={index} src={image.image} alt={`${product.title} - изображение`} />
                ))}
              </div>
            )}
          </div>
        ) : (
          <p>Загрузка данных...</p>
        )}
      </div>
    </div>
  );
}

export default ProductDetail; // добавлено экспортирование компонента
