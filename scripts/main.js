function renderPoem(poem, containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;
    container.innerHTML = `
        <h2>${poem.title}</h2>
        <div class="poem-author">${poem.author}</div>
        <div class="poem-text">
            ${poem.lines.map(line => `<div>${line}</div>`).join('')}
        </div>
    `;
}

function animatePoemLines(containerId) {
    const lines = document.querySelectorAll(`#${containerId} .poem-text div`);
    lines.forEach((line, i) => {
        line.style.animationDelay = `${i * 0.08 + 0.1}s`;
    });
}

// Load both poems with their respective emotion scores
Promise.all([
    fetch('assets/data/hadji_dimitar_bg.json').then(res => res.json()),
    fetch('assets/data/hadji_dimitar_en.json').then(res => res.json()),
    fetch('assets/data/emotion_results_line_by_line.json').then(res => res.json()),
    fetch('assets/data/emotion_results_NoNeutral_HadjiDimitarBG_lines.json').then(res => res.json())
])
.then(([bgPoem, enPoem, enEmotions, bgEmotions]) => {
    // Render both poems first
    renderPoem(bgPoem, 'hadji_dimitar_bg');
    renderPoem(enPoem, 'hadji_dimitar_en');
    
    // Add emotion scores to English poem
    const enContainer = document.getElementById('hadji_dimitar_en');
    const enLines = enContainer.querySelectorAll('.poem-text div');
    enLines.forEach((lineElement, index) => {
        if (enEmotions && enEmotions.lines && enEmotions.lines[index]) {
            const emotions = enEmotions.lines[index].emotions
                .sort((a, b) => b.score - a.score)
                .slice(0, 2);
                
            const emotionScore = document.createElement('span');
            emotionScore.className = 'emotion-score';
            emotionScore.textContent = `(${emotions.map(e => `${e.label}: ${(e.score * 100).toFixed(1)}%`).join(', ')})`;
            
            lineElement.appendChild(emotionScore);
        }
    });

    // Add emotion scores to Bulgarian poem
    const bgContainer = document.getElementById('hadji_dimitar_bg');
    const bgLines = bgContainer.querySelectorAll('.poem-text div');
    bgLines.forEach((lineElement, index) => {
        if (bgEmotions && bgEmotions.lines_analysis && bgEmotions.lines_analysis[index]) {
            const emotions = bgEmotions.lines_analysis[index].emotions
                .sort((a, b) => b.rel_score - a.rel_score)
                .slice(0, 2);
                
            const emotionScore = document.createElement('span');
            emotionScore.className = 'emotion-score';
            emotionScore.textContent = `(${emotions.map(e => `${e.label}: ${(e.rel_score * 100).toFixed(1)}%`).join(', ')})`;
            
            lineElement.appendChild(emotionScore);
        }
    });
    
    // Animate both poems
    animatePoemLines('hadji_dimitar_bg');
    animatePoemLines('hadji_dimitar_en');
})
.catch(error => {
    console.error('Error loading data:', error);
});


















// function renderPoem(poem, containerId) {
//     const container = document.getElementById(containerId);
//     if (!container) return;
//     container.innerHTML = `
//         <h2>${poem.title}</h2>
//         <div class="poem-author">${poem.author}</div>
//         <div class="poem-text">
//             ${poem.lines.map(line => `<div>${line}</div>`).join('')}
//         </div>
//     `;
// }

// function animatePoemLines(containerId) {
//     const lines = document.querySelectorAll(`#${containerId} .poem-text div`);
//     lines.forEach((line, i) => {
//         line.style.animationDelay = `${i * 0.08 + 0.1}s`;
//     });
// }

// function renderPoemWithTop2Emotions(poem, containerId) {
//     const container = document.getElementById(containerId);
//     if (!container) return;
//     container.innerHTML = `
//         <h2>${poem.title || ''}</h2>
//         <div class="poem-author">${poem.author || ''}</div>
//         <div class="poem-text">
//             ${poem.lines.map(line => {
//                 const topEmotions = [...line.emotions]
//                     .sort((a, b) => b.score - a.score)
//                     .slice(0, 2);
//                 return `<div>
//                     ${line.text}
//                     <span class="emotion-score">
//                         (${topEmotions.map(e => `${e.label}: ${(e.score * 100).toFixed(1)}%`).join(', ')})
//                     </span>
//                 </div>`;
//             }).join('')}
//         </div>
//     `;
// }

// // Load Bulgarian poem
// fetch('assets/data/hadji_dimitar_bg.json')
//   .then(res => res.json())
//   .then(poem => {
//       console.log(poem); // See what the object looks like
//       renderPoem(poem, 'hadji_dimitar_bg');
//       animatePoemLines('hadji_dimitar_bg');
//   });

// // Load English poem
// fetch('assets/data/hadji_dimitar_en.json')
//   .then(res => res.json())
//   .then(poem => {
//       renderPoem(poem, 'hadji_dimitar_en');
//       animatePoemLines('hadji_dimitar_en');
//   });

// fetch('assets/data/emotion_results_line_by_line.json')
//   .then(res => res.json())
//   .then(poem => renderPoemWithTop2Emotions(poem, 'hadji_dimitar_en'));
