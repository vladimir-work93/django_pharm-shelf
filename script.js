// Состояние приложения
let currentState = 'login';
let verificationType = ''; // 'register' или 'forgot'
let countdown = 60;
let countdownInterval = null;
let generatedCode = ''; // Для демо - в реальном приложении код генерируется на сервере

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function () {
    // Инициализация полей для кода
    initCodeInputs();

    // Назначение обработчиков навигации
    document.getElementById('registerLink').addEventListener('click', () => showForm('register'));
    document.getElementById('forgotPasswordLink').addEventListener('click', () => showForm('forgot'));

    // Назначение обработчиков кнопок "Назад"
    document.getElementById('backToLoginFromRegister').addEventListener('click', () => showForm('login'));
    document.getElementById('backToLoginFromForgot').addEventListener('click', () => showForm('login'));
    document.getElementById('backToPreviousForm').addEventListener('click', handleBackFromCode);

    // Обработчики отправки форм
    document.getElementById('loginForm').addEventListener('submit', handleLogin);
    document.getElementById('registerForm').addEventListener('submit', handleRegister);
    document.getElementById('forgotPasswordForm').addEventListener('submit', handleForgotPassword);
    document.getElementById('verifyCodeForm').addEventListener('submit', handleVerifyCode);

    // Обработчик повторной отправки кода
    document.getElementById('resendCodeBtn').addEventListener('click', resendCode);

    // Вызов функции adjustFormHeight после всех инициализаций
    adjustFormHeight();

});

// Функция показа нужной формы с анимацией
function showForm(formName) {
    const wrapper = document.getElementById('formsWrapper');
    wrapper.className = 'forms-wrapper';
    
    // Даём время на сброс предыдущей анимации
    setTimeout(() => {
        wrapper.classList.add(`${formName}-active`);
        currentState = formName;
        
        // Очистка сообщений
        clearMessages();
        
        // Остановка таймера
        if (countdownInterval) {
            clearInterval(countdownInterval);
            countdownInterval = null;
        }
        
        // ← ВАЖНО: Ждём завершения CSS-перехода перед измерением
        // Даём время на применение CSS-класса
        setTimeout(() => {
            adjustFormHeight();
        }, 50); // Небольшая задержка для применения CSS
    }, 10);
}

// Инициализация полей для ввода кода
function initCodeInputs() {
    const container = document.getElementById('codeInputsContainer');
    container.innerHTML = '';

    // Создаем 6 полей для цифр кода
    for (let i = 0; i < 6; i++) {
        const input = document.createElement('input');
        input.type = 'text';
        input.maxLength = 1;
        input.className = 'code-input';
        input.dataset.index = i;

        // Обработка ввода - автоматическое перемещение к следующему полю
        input.addEventListener('input', function (e) {
            const value = e.target.value;
            const index = parseInt(e.target.dataset.index);

            // Если введена цифра и это не последнее поле
            if (value && /^\d$/.test(value) && index < 5) {
                const nextInput = container.querySelector(`.code-input[data-index="${index + 1}"]`);
                nextInput.focus();
            }

            // Если стерли значение и это не первое поле
            if (!value && index > 0) {
                const prevInput = container.querySelector(`.code-input[data-index="${index - 1}"]`);
                prevInput.focus();
            }
        });

        // Обработка нажатия клавиш (для навигации стрелками и backspace)
        input.addEventListener('keydown', function (e) {
            const index = parseInt(e.target.dataset.index);

            // Обработка backspace
            if (e.key === 'Backspace' && !e.target.value && index > 0) {
                const prevInput = container.querySelector(`.code-input[data-index="${index - 1}"]`);
                prevInput.focus();
                prevInput.value = '';
            }

            // Обработка стрелок
            if (e.key === 'ArrowLeft' && index > 0) {
                const prevInput = container.querySelector(`.code-input[data-index="${index - 1}"]`);
                prevInput.focus();
            }

            if (e.key === 'ArrowRight' && index < 5) {
                const nextInput = container.querySelector(`.code-input[data-index="${index + 1}"]`);
                nextInput.focus();
            }
        });

        container.appendChild(input);
    }
}

// Обработка входа
function handleLogin(e) {
    e.preventDefault();
    const btn = document.getElementById('loginBtn');
    const originalText = btn.innerHTML;

    // Имитация загрузки
    btn.innerHTML = '<i class="fas fa-spinner"></i> Выполняется вход...';
    btn.disabled = true;

    // В реальном приложении здесь будет AJAX-запрос к Django
    setTimeout(() => {
        const email = document.getElementById('loginEmail').value;
        const password = document.getElementById('loginPassword').value;

        // Простая валидация для демо
        if (email && password) {
            showMessage('loginMessage', 'Вход выполнен успешно! Перенаправление...', 'success');

            // В реальном приложении здесь будет перенаправление
            setTimeout(() => {
                alert('В реальном приложении здесь происходит перенаправление в личный кабинет');
                btn.innerHTML = originalText;
                btn.disabled = false;
            }, 1500);
        } else {
            showMessage('loginMessage', 'Пожалуйста, заполните все поля', 'error');
            btn.innerHTML = originalText;
            btn.disabled = false;
        }
    }, 1200);
}

// Обработка регистрации
function handleRegister(e) {
    e.preventDefault();
    const btn = document.getElementById('registerBtn');
    const originalText = btn.innerHTML;

    // Валидация паролей
    const password = document.getElementById('registerPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;

    if (password !== confirmPassword) {
        showMessage('registerMessage', 'Пароли не совпадают', 'error');
        return;
    }

    if (password.length < 8) {
        showMessage('registerMessage', 'Пароль должен содержать не менее 8 символов', 'error');
        return;
    }

    // Имитация отправки данных на сервер
    btn.innerHTML = '<i class="fas fa-spinner"></i> Отправка данных...';
    btn.disabled = true;

    setTimeout(() => {
        // Генерация демо-кода (в реальном приложении код генерируется на сервере)
        generatedCode = Math.floor(100000 + Math.random() * 900000).toString();
        verificationType = 'register';

        // Обновление текста в форме подтверждения
        const email = document.getElementById('registerEmail').value;
        document.getElementById('codeSubtitle').textContent = `Введите 6-значный код, отправленный на ${email}`;

        // Показ формы подтверждения кода
        showForm('code');

        // Запуск таймера для повторной отправки
        startCountdown();

        // Имитация отправки письма
        console.log(`Демо: Код подтверждения для регистрации ${email}: ${generatedCode}`);
        showMessage('codeMessage', `Код отправлен на ${email}. Для демо: ${generatedCode}`, 'success');

        btn.innerHTML = originalText;
        btn.disabled = false;
    }, 1500);
}

// Обработка восстановления пароля
function handleForgotPassword(e) {
    e.preventDefault();
    const btn = document.getElementById('sendCodeBtn');
    const originalText = btn.innerHTML;

    // Имитация отправки
    btn.innerHTML = '<i class="fas fa-spinner"></i> Отправка...';
    btn.disabled = true;

    setTimeout(() => {
        const email = document.getElementById('forgotEmail').value;

        if (!email) {
            showMessage('forgotMessage', 'Введите адрес электронной почты', 'error');
            btn.innerHTML = originalText;
            btn.disabled = false;
            return;
        }

        // Генерация демо-кода
        generatedCode = Math.floor(100000 + Math.random() * 900000).toString();
        verificationType = 'forgot';

        // Обновление текста
        document.getElementById('codeSubtitle').textContent = `Введите 6-значный код, отправленный на ${email}`;

        // Показ формы подтверждения кода
        showForm('code');

        // Запуск таймера
        startCountdown();

        // Имитация отправки письма
        console.log(`Демо: Код восстановления для ${email}: ${generatedCode}`);
        showMessage('codeMessage', `Код отправлен на ${email}. Для демо: ${generatedCode}`, 'success');

        btn.innerHTML = originalText;
        btn.disabled = false;
    }, 1200);
}

// Обработка подтверждения кода
function handleVerifyCode(e) {
    e.preventDefault();
    const btn = document.getElementById('verifyCodeBtn');
    const originalText = btn.innerHTML;

    // Сбор кода из всех полей
    const codeInputs = document.querySelectorAll('.code-input');
    let enteredCode = '';
    codeInputs.forEach(input => {
        enteredCode += input.value;
    });

    // Проверка кода
    if (enteredCode.length !== 6) {
        showMessage('codeMessage', 'Введите все 6 цифр кода', 'error');
        return;
    }

    // Имитация проверки
    btn.innerHTML = '<i class="fas fa-spinner"></i> Проверка...';
    btn.disabled = true;

    setTimeout(() => {
        // В демо-режиме проверяем совпадение с сгенерированным кодом
        if (enteredCode === generatedCode) {
            showMessage('codeMessage', 'Код подтвержден успешно!', 'success');

            // В зависимости от типа верификации показываем соответствующий результат
            setTimeout(() => {
                if (verificationType === 'register') {
                    alert('Регистрация завершена успешно! Теперь вы можете войти в систему.');
                    showForm('login');
                } else {
                    alert('Пароль успешно сброшен! На вашу почту отправлено письмо с инструкциями.');
                    showForm('login');
                }

                // Очистка полей кода
                codeInputs.forEach(input => {
                    input.value = '';
                });

                // Фокусировка на первом поле
                if (codeInputs[0]) {
                    codeInputs[0].focus();
                }
            }, 1500);
        } else {
            showMessage('codeMessage', 'Неверный код. Попробуйте еще раз.', 'error');
        }

        btn.innerHTML = originalText;
        btn.disabled = false;
    }, 1200);
}

// Обработка кнопки "Назад" в форме кода
function handleBackFromCode() {
    if (verificationType === 'register') {
        showForm('register');
    } else {
        showForm('forgot');
    }
}

// Запуск таймера для повторной отправки кода
function startCountdown() {
    countdown = 60;
    const countdownElement = document.getElementById('countdown');
    const resendBtn = document.getElementById('resendCodeBtn');

    resendBtn.disabled = true;
    countdownElement.textContent = countdown;

    if (countdownInterval) {
        clearInterval(countdownInterval);
    }

    countdownInterval = setInterval(() => {
        countdown--;
        countdownElement.textContent = countdown;

        if (countdown <= 0) {
            clearInterval(countdownInterval);
            resendBtn.disabled = false;
            countdownElement.textContent = '0';
        }
    }, 1000);
}

// Повторная отправка кода
function resendCode() {
    // Генерация нового кода
    generatedCode = Math.floor(100000 + Math.random() * 900000).toString();

    // Запуск таймера заново
    startCountdown();

    // Показ сообщения
    showMessage('codeMessage', `Новый код отправлен. Для демо: ${generatedCode}`, 'success');

    // Очистка полей ввода кода
    const codeInputs = document.querySelectorAll('.code-input');
    codeInputs.forEach(input => {
        input.value = '';
    });

    // Фокусировка на первом поле
    if (codeInputs[0]) {
        codeInputs[0].focus();
    }

    console.log(`Демо: Новый код: ${generatedCode}`);
}

// Функция показа сообщений
function showMessage(elementId, text, type) {
    const element = document.getElementById(elementId);
    element.textContent = text;
    element.className = `message ${type}`;
    element.style.display = 'block';

    // Автоматическое скрытие сообщений об успехе через 5 секунд
    if (type === 'success') {
        setTimeout(() => {
            element.style.display = 'none';
        }, 5000);
    }
}

// Очистка всех сообщений
function clearMessages() {
    const messages = document.querySelectorAll('.message');
    messages.forEach(message => {
        message.style.display = 'none';
    });
}

// Функция для расчета высоты
function adjustFormHeight() {
    const wrapper = document.getElementById('formsWrapper');
    if (!wrapper) return;
    
    // 1. Определяем, какая форма сейчас активна
    let activeForm = null;
    
    if (wrapper.classList.contains('register-active')) {
        activeForm = document.getElementById('registerForm');
    } else if (wrapper.classList.contains('forgot-active')) {
        activeForm = document.getElementById('forgotPasswordForm');
    } else if (wrapper.classList.contains('code-active')) {
        activeForm = document.getElementById('verifyCodeForm');
    } else {
        activeForm = document.getElementById('loginForm'); // По умолчанию
    }
    
    if (!activeForm) return;
    
    // 2. Временно клонируем форму для измерения (без вмешательства в DOM)
    const clone = activeForm.cloneNode(true);
    clone.style.position = 'fixed'; // Выводим из потока
    clone.style.top = '-9999px';    // Скрываем
    clone.style.transform = 'none'; // Сбрасываем трансформации
    clone.style.opacity = '1';      // Делаем видимой
    clone.style.visibility = 'visible';
    clone.style.display = 'block';
    clone.style.height = 'auto';    // Автоматическая высота
    
    // 3. Добавляем клон в DOM для измерения
    document.body.appendChild(clone);
    
    // 4. Измеряем реальную высоту с учётом padding и margins
    const height = clone.offsetHeight;
    
    // 5. Удаляем клон
    document.body.removeChild(clone);
    
    // 6. Устанавливаем высоту контейнера
    // Добавляем небольшой запас для гарантии
    wrapper.style.height = (height + 10) + 'px';
    
    console.log(`Установлена высота: ${height + 30}px для формы: ${activeForm.id}`);
}