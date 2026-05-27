// Hamburger Menu Toggle
const hamburger = document.querySelector('.hamburger');
const navLinks = document.querySelector('.nav-links');

if (hamburger) {
    hamburger.addEventListener('click', () => {
        navLinks.classList.toggle('active');
        hamburger.classList.toggle('active');
    });
}

// Smooth Scrolling for Navigation Links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href !== '#') {
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
                // Close mobile menu if open
                navLinks.classList.remove('active');
            }
        }
    });
});

// Active Navigation Link on Scroll
const sections = document.querySelectorAll('section[id]');
const navLinksArr = document.querySelectorAll('.nav-link');

function activateNavLink() {
    let current = '';
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        if (scrollY >= (sectionTop - 100)) {
            current = section.getAttribute('id');
        }
    });

    navLinksArr.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${current}`) {
            link.classList.add('active');
        }
    });
}

window.addEventListener('scroll', activateNavLink);

// Chatbot Functionality
const chatWidget = document.getElementById('chatbot-widget');
const floatingBtn = document.querySelector('.floating-chat-btn');
const chatMessages = document.getElementById('chat-messages');
const chatInput = document.getElementById('chat-input');
const notificationBadge = document.querySelector('.notification-badge');

// Bot responses database
const botResponses = {
    'hola': '¡Hola! ¿Cómo puedo ayudarte hoy?',
    'ayuda': 'Puedo ayudarte con información sobre nuestros servicios, API, soporte técnico y más. ¿Qué necesitas?',
    'api': 'Nuestra API REST te permite acceder a todos nuestros servicios. Visita la sección de Servicios para más información.',
    'servicios': 'Ofrecemos API REST, Seguridad, Soporte 24/7 y Analíticas en tiempo real. ¿Sobre cuál te gustaría saber más?',
    'contacto': 'Puedes contactarnos en info@tuempresa.com o llamarnos al +34 123 456 789',
    'precio': 'Tenemos diferentes planes adaptados a tus necesidades. ¿Te gustaría que un asesor te contacte?',
    'soporte': 'Nuestro equipo de soporte está disponible 24/7. ¿En qué podemos ayudarte?',
    'gracias': '¡De nada! ¿Hay algo más en lo que pueda ayudarte?',
    'adios': '¡Hasta pronto! Si necesitas ayuda, estaré aquí.',
    'default': 'Interesante pregunta. Para asistencia específica, te recomiendo visitar nuestra web principal o contactar con nuestro equipo.'
};

function toggleChat() {
    chatWidget.classList.toggle('active');
    if (chatWidget.classList.contains('active')) {
        chatInput.focus();
        // Hide notification badge when chat is opened
        if (notificationBadge) {
            notificationBadge.style.display = 'none';
        }
    }
}

function openChat() {
    chatWidget.classList.add('active');
    chatInput.focus();
    if (notificationBadge) {
        notificationBadge.style.display = 'none';
    }
}

function closeChat() {
    chatWidget.classList.remove('active');
}

function sendMessage() {
    const message = chatInput.value.trim();
    if (message === '') return;

    // Add user message
    addMessage(message, 'user');
    chatInput.value = '';

    // Simulate bot typing
    setTimeout(() => {
        const response = getBotResponse(message);
        addMessage(response, 'bot');
    }, 800);
}

function addMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;

    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.innerHTML = sender === 'bot' ? '<i class="fas fa-robot"></i>' : '<i class="fas fa-user"></i>';

    const content = document.createElement('div');
    content.className = 'message-content';
    content.textContent = text;

    messageDiv.appendChild(avatar);
    messageDiv.appendChild(content);
    chatMessages.appendChild(messageDiv);

    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function getBotResponse(message) {
    const lowerMessage = message.toLowerCase();
    
    // Check for keywords in the message
    for (const [key, response] of Object.entries(botResponses)) {
        if (lowerMessage.includes(key)) {
            return response;
        }
    }
    
    return botResponses['default'];
}

function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

// Animate statistics on scroll
function animateStats() {
    const statCards = document.querySelectorAll('.stat-card');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '0';
                entry.target.style.transform = 'translateY(20px)';
                
                setTimeout(() => {
                    entry.target.style.transition = 'all 0.6s ease';
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, 100);
                
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });
    
    statCards.forEach(card => observer.observe(card));
}

// Simulate real-time statistics updates
function updateStatistics() {
    const usersCount = document.getElementById('users-count');
    const requestsCount = document.getElementById('requests-count');
    const successRate = document.getElementById('success-rate');
    const responseTime = document.getElementById('response-time');

    if (usersCount) {
        setInterval(() => {
            const current = parseInt(usersCount.textContent.replace(',', ''));
            const newValue = current + Math.floor(Math.random() * 10);
            usersCount.textContent = newValue.toLocaleString();
        }, 5000);
    }

    if (requestsCount) {
        setInterval(() => {
            const current = parseInt(requestsCount.textContent.replace(',', ''));
            const newValue = current + Math.floor(Math.random() * 50);
            requestsCount.textContent = newValue.toLocaleString();
        }, 3000);
    }

    if (responseTime) {
        setInterval(() => {
            const time = 100 + Math.floor(Math.random() * 50);
            responseTime.textContent = `${time}ms`;
        }, 4000);
    }
}

// Show notification badge after some time
setTimeout(() => {
    if (notificationBadge && !chatWidget.classList.contains('active')) {
        notificationBadge.style.display = 'flex';
    }
}, 3000);

// Initialize animations and updates
document.addEventListener('DOMContentLoaded', () => {
    animateStats();
    updateStatistics();
});

// Add welcome message when page loads
window.addEventListener('load', () => {
    // Simulate a welcome notification
    setTimeout(() => {
        if (!chatWidget.classList.contains('active')) {
            floatingBtn.classList.add('pulse');
            setTimeout(() => {
                floatingBtn.classList.remove('pulse');
            }, 2000);
        }
    }, 2000);
});
