import React from 'react';

const LoginForm = () => {
  const csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0]?.value;

  const handleLogin = async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);
    formData.append('csrfmiddlewaretoken', csrfToken);

    try {
      const response = await fetch('/token/', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        // Обработка успешного входа
        const data = await response.json();
        console.log('Успешный вход', data);
      } else {
        // Обработка ошибок
        const errorData = await response.json();
        console.error('Ошибка входа', errorData);
      }
    } catch (error) {
      // Обработка ошибок сети
      console.error('Ошибка входа', error);
    }
  };

  return (
    <form onSubmit={handleLogin}>
      <input type="hidden" name="csrfmiddlewaretoken" value={csrfToken} />
      <label>
        Логин:
        <input type="text" name="username" />
      </label>
      <br />
      <label>
        Пароль:
        <input type="password" name="password" />
      </label>
      <br />
      <button type="submit">Войти</button>
    </form>
  );
};

export default LoginForm;
