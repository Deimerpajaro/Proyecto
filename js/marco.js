let portal = document.getElementById('portal');
let x = 1;

for (let i = 0; i < 360;) {
    let logo = document.createElement("div");
    logo.className = "logo-"+x;
    logo.style.rotate = i * 2+'deg';
    let logoTranslation = 120;
    
    logo.style.transform = 'translate('+logoTranslation+'px)';

    portal.appendChild(logo);

    i = i + (360/3);
    x = x + 1;
} 