// AnotherComponent.js
const { useState, useEffect } = React;

function AnotherComponent() {
  const openProductDetail = () => {
    const productId = 1; // Здесь вы можете установить нужный productId
    ReactDOM.createPortal(
      <ProductDetail productId={productId} onClose=() =>  />,
      document.getElementById('product-detail-container')
    );
  };

  return (
    <div>
      {/* Другой контент */}
      <button onClick={openProductDetail}>Открыть ProductDetail</button>
    </div>
  );
}

const containerAnother = document.getElementById('another-component-container');
if (containerAnother) {
  ReactDOM.render(<AnotherComponent />, containerAnother);
}
